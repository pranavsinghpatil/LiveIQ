import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import AlertRule, Alert, User, UserRole, Event
from app.auth import get_current_user, require_analyst
from app.schemas import AlertRuleCreate, AlertRuleOut, AlertOut

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.post("/rules", response_model=AlertRuleOut, status_code=201)
async def create_alert_rule(
    rule_data: AlertRuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_analyst),  # Analyst only
):
    """Create a custom alert rule. Analyst only. Max 5 per event."""
    # Check event exists
    result = await db.execute(select(Event).where(Event.id == rule_data.event_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Event not found")

    # Enforce max 5 rules per event per user
    count_result = await db.execute(
        select(func.count(AlertRule.id)).where(
            AlertRule.user_id == current_user.id,
            AlertRule.event_id == rule_data.event_id,
        )
    )
    if count_result.scalar() >= 5:
        raise HTTPException(
            status_code=400,
            detail="Maximum 5 alert rules per event reached",
        )

    rule = AlertRule(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        event_id=rule_data.event_id,
        rule_type=rule_data.rule_type,
        rule_value=rule_data.rule_value,
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return AlertRuleOut.model_validate(rule)


@router.get("/rules", response_model=List[AlertRuleOut])
async def get_my_alert_rules(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AlertRule).where(AlertRule.user_id == current_user.id)
    )
    return [AlertRuleOut.model_validate(r) for r in result.scalars().all()]


@router.delete("/rules/{rule_id}", status_code=204)
async def delete_alert_rule(
    rule_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AlertRule).where(
            AlertRule.id == rule_id,
            AlertRule.user_id == current_user.id,
        )
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    await db.delete(rule)
    await db.commit()


@router.patch("/rules/{rule_id}/toggle", response_model=AlertRuleOut)
async def toggle_alert_rule(
    rule_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AlertRule).where(
            AlertRule.id == rule_id,
            AlertRule.user_id == current_user.id,
        )
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    rule.is_active = not rule.is_active
    await db.commit()
    await db.refresh(rule)
    return AlertRuleOut.model_validate(rule)


@router.get("/history", response_model=List[AlertOut])
async def get_alert_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get recent alert history for the current user."""
    result = await db.execute(
        select(Alert)
        .where(Alert.user_id == current_user.id)
        .order_by(Alert.triggered_at.desc())
        .limit(50)
    )
    return [AlertOut.model_validate(a) for a in result.scalars().all()]
