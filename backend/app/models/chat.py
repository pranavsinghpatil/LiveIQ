from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from typing import List, Optional
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


class Message(BaseModel):
    id: Optional[str]
    thread_id: str
    sender: str  # user / assistant / speaker
    role: str  # system / assistant / user
    content: str
    timestamp: datetime
    context_vector: Optional[List[float]] = None

class ChatThread(BaseModel):
    id: Optional[str]
    title: str
    source: str  # chatgpt, claude, podcast, etc.
    format: str  # text, pdf, link, screenshot
    created_at: datetime
    updated_at: Optional[datetime]
    summary: Optional[str] = None
    metadata: Optional[dict] = None

class ChatMessage(BaseModel):
    chat_id: str
    user_id: str  # <-- add this line
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)