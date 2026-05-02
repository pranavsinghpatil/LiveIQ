from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field
from app.models import UserRole, PipelineStatus, TrendEnum, AlertRuleType


# ── Auth Schemas ───────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole = UserRole.viewer
    notification_prefs: dict = {}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    role: UserRole
    notification_prefs: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ── Event Schemas ──────────────────────────────────────────────────────────────

class EventOut(BaseModel):
    id: str
    sport: str
    league: Optional[str]
    home_team: str
    away_team: str
    home_score: Optional[str]
    away_score: Optional[str]
    status: str
    venue: Optional[str]
    event_date: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class EventStreamItem(BaseModel):
    id: str
    event_id: str
    data: dict
    ingested_at: datetime

    model_config = {"from_attributes": True}


# ── Pipeline Stage Schemas ─────────────────────────────────────────────────────

class PipelineStageOut(BaseModel):
    id: str
    event_id: str
    stage_number: int
    stage_name: str
    status: PipelineStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

    model_config = {"from_attributes": True}


# ── Commentary Schemas ─────────────────────────────────────────────────────────

class CommentaryOut(BaseModel):
    id: str
    event_id: str
    text: str
    model: str
    latency_ms: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Analysis Schemas ───────────────────────────────────────────────────────────

class GeminiAnalysisOutput(BaseModel):
    updated_summary: str
    key_moments: List[str]
    trend: TrendEnum
    prediction: str
    confidence: float = Field(ge=0.0, le=1.0)


class AnalysisOut(BaseModel):
    id: str
    event_id: str
    updated_summary: Optional[str]
    key_moments: Optional[List[str]]
    trend: Optional[TrendEnum]
    prediction: Optional[str]
    confidence: Optional[float]
    model: str
    groq_prediction: Optional[str]
    groq_confidence: Optional[float]
    weather_conditions: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Subscription Schemas ───────────────────────────────────────────────────────

class SubscriptionOut(BaseModel):
    id: str
    user_id: str
    event_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Alert Rule Schemas ─────────────────────────────────────────────────────────

class AlertRuleCreate(BaseModel):
    event_id: str
    rule_type: AlertRuleType
    rule_value: dict  # {"keyword": "injury"} or {"threshold": 3, "operator": "gt"}


class AlertRuleOut(BaseModel):
    id: str
    user_id: str
    event_id: str
    rule_type: AlertRuleType
    rule_value: dict
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertOut(BaseModel):
    id: str
    user_id: str
    event_id: str
    rule_id: str
    matched_rule: Optional[dict]
    triggered_at: datetime

    model_config = {"from_attributes": True}


# ── Report Schemas ─────────────────────────────────────────────────────────────

class EventReportOut(BaseModel):
    id: str
    event_id: str
    narrative: Optional[str]
    key_moments: Optional[List[str]]
    prediction_accuracy: Optional[float]
    generated_at: datetime

    model_config = {"from_attributes": True}


# ── AI Call Log Schemas ────────────────────────────────────────────────────────

class AICallLogOut(BaseModel):
    id: str
    model: str
    event_id: Optional[str]
    prompt_tokens: int
    completion_tokens: int
    latency_ms: Optional[int]
    success: bool
    error_message: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── WebSocket Message Schemas ──────────────────────────────────────────────────

class WSMessage(BaseModel):
    type: str  # "commentary" | "analysis" | "stage_update" | "alert" | "error"
    event_id: str
    data: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Prediction Model Accuracy (Bonus) ─────────────────────────────────────────

class ModelAccuracy(BaseModel):
    model: str
    total_predictions: int
    accurate_predictions: int
    accuracy_rate: float
