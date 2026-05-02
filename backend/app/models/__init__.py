import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, Float, Integer, Text,
    DateTime, Enum as SAEnum, ForeignKey, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship, DeclarativeBase
import enum


class Base(DeclarativeBase):
    pass


def gen_uuid():
    return str(uuid.uuid4())


# ── Enums ──────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    analyst = "analyst"
    viewer = "viewer"


class PipelineStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    done = "done"
    failed = "failed"


class TrendEnum(str, enum.Enum):
    momentum = "momentum"
    stable = "stable"
    reversal = "reversal"


class AlertRuleType(str, enum.Enum):
    keyword_detected = "keyword_detected"
    score_threshold = "score_threshold"
    trend_change = "trend_change"


# ── Models ─────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.viewer, nullable=False)
    notification_prefs = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")
    alert_rules = relationship("AlertRule", back_populates="user")
    alerts = relationship("Alert", back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)  # TheSportsDB ID
    sport = Column(String, nullable=False)
    league = Column(String)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_score = Column(String)
    away_score = Column(String)
    status = Column(String, default="NotStarted")
    venue = Column(String)
    event_date = Column(DateTime)
    last_commentary_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    stream = relationship("EventStream", back_populates="event", cascade="all, delete-orphan")
    analyses = relationship("EventAnalysis", back_populates="event")
    pipeline_stages = relationship("PipelineStage", back_populates="event")
    subscriptions = relationship("Subscription", back_populates="event")
    alert_rules = relationship("AlertRule", back_populates="event")
    alerts = relationship("Alert", back_populates="event")
    report = relationship("EventReport", back_populates="event", uselist=False)
    commentaries = relationship("Commentary", back_populates="event")


class EventStream(Base):
    __tablename__ = "event_stream"

    id = Column(String, primary_key=True, default=gen_uuid)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    data = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="stream")


class Commentary(Base):
    __tablename__ = "commentaries"

    id = Column(String, primary_key=True, default=gen_uuid)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    model = Column(String, default="groq-llama")
    latency_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="commentaries")


class EventAnalysis(Base):
    __tablename__ = "event_analyses"

    id = Column(String, primary_key=True, default=gen_uuid)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    updated_summary = Column(Text)
    key_moments = Column(JSON, default=list)
    trend = Column(SAEnum(TrendEnum))
    prediction = Column(Text)
    confidence = Column(Float)
    model = Column(String, default="gemini")
    # For multi-model debate bonus
    groq_prediction = Column(Text)
    groq_confidence = Column(Float)
    # Weather bonus
    weather_conditions = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="analyses")


class PipelineStage(Base):
    __tablename__ = "pipeline_stages"

    id = Column(String, primary_key=True, default=gen_uuid)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    stage_number = Column(Integer, nullable=False)
    stage_name = Column(String, nullable=False)
    status = Column(SAEnum(PipelineStatus), default=PipelineStatus.pending)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)

    __table_args__ = (UniqueConstraint("event_id", "stage_number", name="uq_event_stage"),)

    event = relationship("Event", back_populates="pipeline_stages")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uq_user_event_sub"),)

    user = relationship("User", back_populates="subscriptions")
    event = relationship("Event", back_populates="subscriptions")


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_type = Column(SAEnum(AlertRuleType), nullable=False)
    rule_value = Column(JSON, nullable=False)  # {"keyword": "injury"} or {"threshold": 3, "operator": "gt"}
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="alert_rules")
    event = relationship("Event", back_populates="alert_rules")
    alerts = relationship("Alert", back_populates="rule")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    rule_id = Column(String, ForeignKey("alert_rules.id", ondelete="CASCADE"), nullable=False)
    matched_rule = Column(JSON)
    triggered_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="alerts")
    event = relationship("Event", back_populates="alerts")
    rule = relationship("AlertRule", back_populates="alerts")


class EventReport(Base):
    __tablename__ = "event_reports"

    id = Column(String, primary_key=True, default=gen_uuid)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, unique=True)
    narrative = Column(Text)
    key_moments = Column(JSON, default=list)
    prediction_accuracy = Column(Float)
    generated_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="report")


class AICallLog(Base):
    __tablename__ = "ai_call_log"

    id = Column(String, primary_key=True, default=gen_uuid)
    model = Column(String, nullable=False)
    event_id = Column(String)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    latency_ms = Column(Integer)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
