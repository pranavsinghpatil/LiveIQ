import json
import httpx
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import Event
from app.services.sportsdb import fetch_live_events
from app.config import get_settings

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
    """Stage 1: Enqueue events from TheSportsDB."""
    print(f"[Scheduler] Running event ingestion at {datetime.utcnow()}")
    try:
        raw_events = await fetch_live_events()
        for raw in raw_events[:20]:  # Limit to 20 events per cycle
            event_id = raw.get("idEvent", raw.get("id"))
            if event_id:
                # Fire and forget to BullMQ
                await _notify_nodejs_worker("ingest", {
                    "event_id": str(event_id),
                    "raw_data": raw
                })
    except Exception as e:
        print(f"[Scheduler] Ingest error: {e}")

async def gemini_analysis_job():
    """Stage 4: Enqueue Gemini analysis for all active events every 5 minutes."""
    print(f"[Scheduler] Running Gemini analysis at {datetime.utcnow()}")
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Event).where(Event.status.notin_(["Final", "FT", "Finished"]))
            )
            active_events = result.scalars().all()

            for event in active_events:
                await _notify_nodejs_worker("analysis", {"event_id": event.id})
                
        except Exception as e:
            print(f"[Scheduler] Gemini analysis job error: {e}")

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
