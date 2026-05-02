"""
APScheduler jobs for:
- Event ingestion every 60s
- Gemini analysis every 5 minutes
"""
import json
import uuid
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, delete
from app.database import AsyncSessionLocal
from app.models import Event, EventStream, PipelineStatus
from app.services.sportsdb import fetch_live_events, normalize_event
from app.services.ai_service import generate_groq_commentary, generate_gemini_analysis, generate_groq_prediction
from app.services.pipeline_service import initialize_pipeline_stages, update_stage, get_pipeline_stages
from app.services.redis_service import (
    set_commentary_lock, set_analysis_lock,
    publish_event, cache_update, get_redis
)
from app.services.weather_service import get_weather_for_venue
from app.models import Commentary, EventAnalysis, AICallLog, TrendEnum
from app.config import get_settings
import httpx

settings = get_settings()
scheduler = AsyncIOScheduler()


async def _notify_nodejs_worker(job_type: str, payload: dict):
    """Send job to Node.js BullMQ workers via HTTP."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"http://localhost:3001/internal/jobs/{job_type}",
                json=payload,
            )
    except Exception as e:
        print(f"[Scheduler] Could not notify Node.js worker ({job_type}): {e}")


async def ingest_events_job():
    """Stage 1 + 2: Ingest events from TheSportsDB and accumulate stream."""
    print(f"[Scheduler] Running event ingestion at {datetime.utcnow()}")
    async with AsyncSessionLocal() as db:
        try:
            raw_events = await fetch_live_events()
            for raw in raw_events[:20]:  # Limit to 20 events per cycle
                normalized = normalize_event(raw)
                event_id = normalized["id"]
                if not event_id:
                    continue

                # Upsert event
                result = await db.execute(select(Event).where(Event.id == event_id))
                event = result.scalar_one_or_none()

                if event is None:
                    event_date = None
                    if normalized.get("event_date"):
                        try:
                            event_date = datetime.strptime(normalized["event_date"], "%Y-%m-%d")
                        except Exception:
                            pass

                    event = Event(
                        id=event_id,
                        sport=normalized["sport"],
                        league=normalized.get("league"),
                        home_team=normalized["home_team"],
                        away_team=normalized["away_team"],
                        home_score=normalized.get("home_score"),
                        away_score=normalized.get("away_score"),
                        status=normalized.get("status", "NotStarted"),
                        venue=normalized.get("venue"),
                        event_date=event_date,
                    )
                    db.add(event)
                    await db.flush()

                    # Stage 1: Initialize pipeline stages
                    await initialize_pipeline_stages(db, event_id)

                else:
                    # Update scores and status
                    event.home_score = normalized.get("home_score", event.home_score)
                    event.away_score = normalized.get("away_score", event.away_score)
                    event.status = normalized.get("status", event.status)
                    event.updated_at = datetime.utcnow()

                # Stage 1 → active → done
                await update_stage(db, event_id, 1, PipelineStatus.active)

                # Stage 2: Append to rolling 50-event stream
                await update_stage(db, event_id, 2, PipelineStatus.active)
                stream_entry = EventStream(
                    id=str(uuid.uuid4()),
                    event_id=event_id,
                    data=normalized["raw_data"] if isinstance(normalized.get("raw_data"), dict) else normalized,
                    ingested_at=datetime.utcnow(),
                )
                db.add(stream_entry)
                await db.flush()

                # Trim to max 50 rows
                count_result = await db.execute(
                    select(EventStream.id)
                    .where(EventStream.event_id == event_id)
                    .order_by(EventStream.ingested_at.asc())
                )
                all_ids = [row[0] for row in count_result.fetchall()]
                if len(all_ids) > 50:
                    to_delete = all_ids[:len(all_ids) - 50]
                    await db.execute(delete(EventStream).where(EventStream.id.in_(to_delete)))

                await update_stage(db, event_id, 1, PipelineStatus.done)
                await update_stage(db, event_id, 2, PipelineStatus.done)

                # Stage 3: Groq commentary (debounced — max 1/60s per event)
                if await set_commentary_lock(event_id, ttl=60):
                    await run_groq_commentary(db, event_id, normalized)

                # Publish stage update via WebSocket
                await _publish_stage_update(event_id)

            await db.commit()
        except Exception as e:
            print(f"[Scheduler] Ingest error: {e}")
            await db.rollback()


async def run_groq_commentary(db, event_id: str, event_data: dict):
    """Stage 3: Generate Groq commentary."""
    try:
        await update_stage(db, event_id, 3, PipelineStatus.active)
        commentary_text, latency_ms = await generate_groq_commentary(event_data)

        commentary = Commentary(
            id=str(uuid.uuid4()),
            event_id=event_id,
            text=commentary_text,
            model="groq-llama-3.1-8b",
            latency_ms=latency_ms,
        )
        db.add(commentary)

        log = AICallLog(
            id=str(uuid.uuid4()),
            model="groq-llama-3.1-8b",
            event_id=event_id,
            latency_ms=latency_ms,
            success=True,
        )
        db.add(log)
        await db.flush()

        # Update event's last_commentary_at
        result = await db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()
        if event:
            event.last_commentary_at = datetime.utcnow()

        await update_stage(db, event_id, 3, PipelineStatus.done)

        # Push to WebSocket
        ws_payload = json.dumps({
            "type": "commentary",
            "event_id": event_id,
            "data": {
                "text": commentary_text,
                "latency_ms": latency_ms,
                "model": "groq-llama-3.1-8b",
            },
            "timestamp": datetime.utcnow().isoformat(),
        })
        await publish_event(f"event:{event_id}:updates", ws_payload)
        await cache_update(event_id, ws_payload)

    except Exception as e:
        print(f"[Groq] Commentary error for {event_id}: {e}")
        await update_stage(db, event_id, 3, PipelineStatus.failed, str(e))


async def gemini_analysis_job():
    """Stage 4: Run Gemini analysis for all active events every 5 minutes."""
    print(f"[Scheduler] Running Gemini analysis at {datetime.utcnow()}")
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Event).where(Event.status.notin_(["Final", "FT", "Finished"]))
            )
            active_events = result.scalars().all()

            for event in active_events:
                if not await set_analysis_lock(event.id, ttl=290):
                    continue  # Skip if analysis already running

                try:
                    await _run_full_analysis(db, event)
                except Exception as e:
                    print(f"[Gemini] Analysis error for {event.id}: {e}")

            await db.commit()
        except Exception as e:
            print(f"[Scheduler] Gemini analysis job error: {e}")


async def _run_full_analysis(db, event):
    """Stages 4-7 for a single event."""
    event_id = event.id

    # Fetch stream
    stream_result = await db.execute(
        select(EventStream)
        .where(EventStream.event_id == event_id)
        .order_by(EventStream.ingested_at.desc())
        .limit(50)
    )
    stream_data = [s.data for s in stream_result.scalars().all()]

    event_dict = {
        "id": event.id,
        "sport": event.sport,
        "home_team": event.home_team,
        "away_team": event.away_team,
        "home_score": event.home_score,
        "away_score": event.away_score,
        "status": event.status,
        "venue": event.venue,
    }

    # Stage 4: Gemini Analysis
    await update_stage(db, event_id, 4, PipelineStatus.active)

    # Bonus: Weather injection
    weather = None
    if event.venue:
        weather = await get_weather_for_venue(event.venue)

    analysis_output, latency_ms = await generate_gemini_analysis(event_dict, stream_data, weather)

    # Bonus: Multi-model debate
    groq_prediction, groq_confidence, _ = await generate_groq_prediction(event_dict, stream_data)

    analysis = EventAnalysis(
        id=str(uuid.uuid4()),
        event_id=event_id,
        updated_summary=analysis_output.updated_summary,
        key_moments=analysis_output.key_moments,
        trend=analysis_output.trend,
        prediction=analysis_output.prediction,
        confidence=analysis_output.confidence,
        model="gemini-1.5-flash",
        groq_prediction=groq_prediction,
        groq_confidence=groq_confidence,
        weather_conditions=weather,
    )
    db.add(analysis)

    log = AICallLog(
        id=str(uuid.uuid4()),
        model="gemini-1.5-flash",
        event_id=event_id,
        latency_ms=latency_ms,
        success=True,
    )
    db.add(log)
    await db.flush()
    await update_stage(db, event_id, 4, PipelineStatus.done)

    # Stage 5: Publish to Redis
    await update_stage(db, event_id, 5, PipelineStatus.active)
    analysis_payload = json.dumps({
        "type": "analysis",
        "event_id": event_id,
        "data": {
            "updated_summary": analysis_output.updated_summary,
            "key_moments": analysis_output.key_moments,
            "trend": analysis_output.trend.value if hasattr(analysis_output.trend, 'value') else analysis_output.trend,
            "prediction": analysis_output.prediction,
            "confidence": analysis_output.confidence,
            "groq_prediction": groq_prediction,
            "groq_confidence": groq_confidence,
            "weather_conditions": weather,
        },
        "timestamp": datetime.utcnow().isoformat(),
    })
    await publish_event(f"event:{event_id}:updates", analysis_payload)
    await cache_update(event_id, analysis_payload)
    await update_stage(db, event_id, 5, PipelineStatus.done)

    # Stage 6: WebSocket push (handled by WS endpoint subscribing to Redis)
    await update_stage(db, event_id, 6, PipelineStatus.active)
    await update_stage(db, event_id, 6, PipelineStatus.done)

    # Stage 7: Alert rule evaluation
    await update_stage(db, event_id, 7, PipelineStatus.active)
    await _evaluate_alert_rules(db, event_id, analysis_output, groq_prediction)
    await update_stage(db, event_id, 7, PipelineStatus.done)

    # Publish stage update
    await _publish_stage_update(event_id)

    # Check if event finished → trigger report
    if event.status in ["Final", "FT", "Finished"]:
        await _enqueue_report_job(event_id)


async def _evaluate_alert_rules(db, event_id: str, analysis, groq_pred: str):
    """Stage 7: Evaluate user-defined alert rules."""
    from app.models import AlertRule, Alert, AlertRuleType
    result = await db.execute(
        select(AlertRule).where(
            AlertRule.event_id == event_id,
            AlertRule.is_active == True,
        )
    )
    rules = result.scalars().all()

    for rule in rules:
        triggered = False
        matched_data = {}

        if rule.rule_type == AlertRuleType.keyword_detected:
            keyword = rule.rule_value.get("keyword", "").lower()
            # Check Groq commentary (last commentary for this event)
            from app.models import Commentary
            last_commentary = await db.execute(
                select(Commentary)
                .where(Commentary.event_id == event_id)
                .order_by(Commentary.created_at.desc())
                .limit(1)
            )
            comm = last_commentary.scalar_one_or_none()
            if comm and keyword in comm.text.lower():
                triggered = True
                matched_data = {"keyword": keyword, "found_in": comm.text[:100]}

        elif rule.rule_type == AlertRuleType.trend_change:
            target_trend = rule.rule_value.get("trend", "reversal")
            current_trend = analysis.trend.value if hasattr(analysis.trend, 'value') else str(analysis.trend)
            if current_trend == target_trend:
                triggered = True
                matched_data = {"trend": current_trend}

        if triggered:
            alert = Alert(
                id=str(uuid.uuid4()),
                user_id=rule.user_id,
                event_id=event_id,
                rule_id=rule.id,
                matched_rule={
                    "rule_type": rule.rule_type.value,
                    "rule_value": rule.rule_value,
                    "matched_data": matched_data,
                },
            )
            db.add(alert)

            # Push WS alert to rule owner
            alert_payload = json.dumps({
                "type": "alert",
                "event_id": event_id,
                "data": {
                    "rule_type": rule.rule_type.value,
                    "message": f"Alert triggered: {rule.rule_type.value}",
                    "matched_data": matched_data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            })
            await publish_event(f"user:{rule.user_id}:alerts", alert_payload)

    await db.flush()


async def _publish_stage_update(event_id: str):
    """Publish pipeline stage update to WebSocket clients."""
    payload = json.dumps({
        "type": "stage_update",
        "event_id": event_id,
        "data": {"message": "Pipeline stages updated"},
        "timestamp": datetime.utcnow().isoformat(),
    })
    await publish_event(f"event:{event_id}:updates", payload)


async def _enqueue_report_job(event_id: str):
    """Enqueue post-event report generation (Stage 8)."""
    await _notify_nodejs_worker("report", {"event_id": event_id})


def start_scheduler():
    """Start APScheduler with all jobs."""
    scheduler.add_job(
        ingest_events_job,
        "interval",
        seconds=settings.ingest_interval_seconds,
        id="ingest_events",
        replace_existing=True,
    )
    scheduler.add_job(
        gemini_analysis_job,
        "interval",
        seconds=settings.analysis_interval_seconds,
        id="gemini_analysis",
        replace_existing=True,
    )
    scheduler.start()
    print("[Scheduler] Started: ingest every 60s, analysis every 5min")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
