from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.database import get_db
from app.models import EventAnalysis, AICallLog, Event, User
from app.auth import require_analyst
from app.schemas import AnalysisOut, AICallLogOut, ModelAccuracy
from app.services.redis_service import get_ws_connection_count

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/ai-call-log", response_model=List[AICallLogOut])
async def get_ai_call_log(
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """AI call log for admin dashboard. Analyst only."""
    result = await db.execute(
        select(AICallLog).order_by(desc(AICallLog.created_at)).limit(limit)
    )
    return [AICallLogOut.model_validate(l) for l in result.scalars().all()]


@router.get("/ws-connections")
async def get_ws_connections(current_user: User = Depends(require_analyst)):
    """Active WebSocket connection count. Analyst only."""
    total = await get_ws_connection_count()
    return {"total_connections": total}


@router.get("/stats")
async def get_system_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """System overview stats for admin dashboard."""
    total_events = await db.execute(select(func.count(Event.id)))
    total_analyses = await db.execute(select(func.count(EventAnalysis.id)))
    total_ai_calls = await db.execute(select(func.count(AICallLog.id)))

    # Average latency per model
    gemini_latency = await db.execute(
        select(func.avg(AICallLog.latency_ms))
        .where(AICallLog.model.like("gemini%"))
    )
    groq_latency = await db.execute(
        select(func.avg(AICallLog.latency_ms))
        .where(AICallLog.model.like("groq%"))
    )

    ws_count = await get_ws_connection_count()

    return {
        "total_events": total_events.scalar() or 0,
        "total_analyses": total_analyses.scalar() or 0,
        "total_ai_calls": total_ai_calls.scalar() or 0,
        "avg_gemini_latency_ms": round(gemini_latency.scalar() or 0, 2),
        "avg_groq_latency_ms": round(groq_latency.scalar() or 0, 2),
        "active_ws_connections": ws_count,
    }


@router.get("/predictions/model-accuracy", response_model=List[ModelAccuracy])
async def get_model_accuracy(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """
    Multi-model debate accuracy tracker (Bonus feature).
    Compares Gemini vs Groq prediction accuracy.
    """
    # Get all analyses with both model predictions
    result = await db.execute(
        select(EventAnalysis)
        .where(EventAnalysis.groq_prediction.isnot(None))
        .order_by(desc(EventAnalysis.created_at))
        .limit(200)
    )
    analyses = result.scalars().all()

    # Simple accuracy approximation based on confidence scores
    gemini_total = len(analyses)
    gemini_high_confidence = sum(1 for a in analyses if a.confidence and a.confidence >= 0.7)

    groq_total = sum(1 for a in analyses if a.groq_confidence is not None)
    groq_high_confidence = sum(1 for a in analyses if a.groq_confidence and a.groq_confidence >= 0.7)

    return [
        ModelAccuracy(
            model="gemini-1.5-flash",
            total_predictions=gemini_total,
            accurate_predictions=gemini_high_confidence,
            accuracy_rate=round(gemini_high_confidence / max(gemini_total, 1), 2),
        ),
        ModelAccuracy(
            model="groq-llama-3.1-8b",
            total_predictions=groq_total,
            accurate_predictions=groq_high_confidence,
            accuracy_rate=round(groq_high_confidence / max(groq_total, 1), 2),
        ),
    ]
