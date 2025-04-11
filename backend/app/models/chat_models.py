from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
# --------------------
# Chat Models
# --------------------

class Chat(BaseModel):
    id: str
    user_id: Optional[str]
    title: str
    content: str
    media_type: Optional[str] = "text"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

class ChatCreate(BaseModel):
    title: str
    content: str
    media_type: Optional[str] = "text"
