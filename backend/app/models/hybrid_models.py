# app/models/hybrid_models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class HybridBase(BaseModel):
    title: str
    chat_ids: List[str]

class HybridCreate(HybridBase):
    user_id: str  # UUID of the user

class Hybrid(HybridBase):
    id: UUID
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

