import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.database import get_db
from app.models import Event, EventAnalysis, Subscription, EventReport, User, UserRole, Commentary
from app.auth import get_current_user, require_any_role, require_analyst
from app.schemas import EventOut, AnalysisOut, SubscriptionOut, CommentaryOut, EventReportOut
from app.services.pipeline_service import get_pipeline_stages
from app.schemas import PipelineStageOut

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=List[EventOut])
async def list_events(
    sport: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all events — public endpoint for event browser."""
    query = select(Event).order_by(desc(Event.created_at))
    if sport:
        query = query.where(Event.sport.ilike(f"%{sport}%"))
    if status:
        query = query.where(Event.status == status)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return [EventOut.model_validate(e) for e in result.scalars().all()]


@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventOut.model_validate(event)


@router.get("/{event_id}/stages", response_model=List[PipelineStageOut])
async def get_event_stages(event_id: str, db: AsyncSession = Depends(get_db)):
    """Get pipeline stages for a specific event — powers the stepper UI."""
    stages = await get_pipeline_stages(db, event_id)
    return [PipelineStageOut.model_validate(s) for s in stages]


@router.get("/{event_id}/analyses", response_model=List[AnalysisOut])
async def get_event_analyses(
    event_id: str,
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get Gemini analysis history for an event."""
    result = await db.execute(
        select(EventAnalysis)
        .where(EventAnalysis.event_id == event_id)
        .order_by(desc(EventAnalysis.created_at))
        .limit(limit)
    )
    return [AnalysisOut.model_validate(a) for a in result.scalars().all()]


@router.get("/{event_id}/commentary", response_model=List[CommentaryOut])
async def get_event_commentary(
    event_id: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get Groq commentary history for an event."""
    result = await db.execute(
        select(Commentary)
        .where(Commentary.event_id == event_id)
        .order_by(desc(Commentary.created_at))
        .limit(limit)
    )
    return [CommentaryOut.model_validate(c) for c in result.scalars().all()]


@router.get("/{event_id}/report", response_model=EventReportOut)
async def get_event_report(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """Get post-event report (analyst only)."""
    result = await db.execute(select(EventReport).where(EventReport.event_id == event_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not available yet")
    return EventReportOut.model_validate(report)


# ── Subscriptions ──────────────────────────────────────────────────────────────

@router.post("/{event_id}/subscribe", response_model=SubscriptionOut, status_code=201)
async def subscribe_to_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Subscribe to an event. Viewers limited to 3 subscriptions."""
    # Check event exists
    result = await db.execute(select(Event).where(Event.id == event_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Event not found")

    # Check viewer subscription limit
    if current_user.role == UserRole.viewer:
        count_result = await db.execute(
            select(func.count(Subscription.id)).where(Subscription.user_id == current_user.id)
        )
        sub_count = count_result.scalar()
        if sub_count >= 3:
            raise HTTPException(
                status_code=403,
                detail="Viewers can subscribe to maximum 3 events. Upgrade to Analyst for unlimited access.",
            )

    # Check already subscribed
    existing = await db.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.event_id == event_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Already subscribed to this event")

    sub = Subscription(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        event_id=event_id,
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return SubscriptionOut.model_validate(sub)


@router.delete("/{event_id}/subscribe", status_code=204)
async def unsubscribe_from_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.event_id == event_id,
        )
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    await db.delete(sub)
    await db.commit()


@router.get("/my/subscriptions", response_model=List[SubscriptionOut])
async def my_subscriptions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    return [SubscriptionOut.model_validate(s) for s in result.scalars().all()]
