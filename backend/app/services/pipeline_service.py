"""
Pipeline Stage Manager — updates pipeline_stages table.
This is the single source of truth for the stepper UI.
All updates happen inside workers, NOT in API handlers.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models import PipelineStage, PipelineStatus, Event

STAGE_DEFINITIONS = {
    1: "Event Ingestion",
    2: "Stream Accumulation",
    3: "Groq Commentary",
    4: "Gemini Analysis",
    5: "Redis Pub/Sub Publish",
    6: "WebSocket Push",
    7: "Alert Rule Evaluation",
    8: "Post-Event Report",
}


async def initialize_pipeline_stages(db: AsyncSession, event_id: str):
    """Create all 8 pipeline stages for an event in 'pending' state."""
    for stage_num, stage_name in STAGE_DEFINITIONS.items():
        existing = await db.execute(
            select(PipelineStage).where(
                PipelineStage.event_id == event_id,
                PipelineStage.stage_number == stage_num,
            )
        )
        if existing.scalar_one_or_none() is None:
            stage = PipelineStage(
                id=str(uuid.uuid4()),
                event_id=event_id,
                stage_number=stage_num,
                stage_name=stage_name,
                status=PipelineStatus.pending,
            )
            db.add(stage)
    await db.commit()


async def update_stage(
    db: AsyncSession,
    event_id: str,
    stage_number: int,
    status: PipelineStatus,
    error_message: Optional[str] = None,
):
    """Update a specific pipeline stage status with timestamps."""
    now = datetime.utcnow()
    result = await db.execute(
        select(PipelineStage).where(
            PipelineStage.event_id == event_id,
            PipelineStage.stage_number == stage_number,
        )
    )
    stage = result.scalar_one_or_none()

    if stage is None:
        stage = PipelineStage(
            id=str(uuid.uuid4()),
            event_id=event_id,
            stage_number=stage_number,
            stage_name=STAGE_DEFINITIONS.get(stage_number, f"Stage {stage_number}"),
            status=status,
        )
        db.add(stage)
    else:
        stage.status = status
        stage.error_message = error_message

    if status == PipelineStatus.active:
        stage.started_at = now
    elif status in (PipelineStatus.done, PipelineStatus.failed):
        stage.completed_at = now
        if stage.started_at is None:
            stage.started_at = now

    await db.commit()
    await db.refresh(stage)
    return stage


async def get_pipeline_stages(db: AsyncSession, event_id: str) -> list:
    """Get all 8 pipeline stages for an event."""
    result = await db.execute(
        select(PipelineStage)
        .where(PipelineStage.event_id == event_id)
        .order_by(PipelineStage.stage_number)
    )
    return result.scalars().all()
