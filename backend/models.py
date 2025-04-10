"""
Database models for VoxStitch.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --------------------
# User Models
# --------------------

class User(BaseModel):
    id: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str  # Supabase will hash this internally

class UserOut(BaseModel):
    id: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

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
