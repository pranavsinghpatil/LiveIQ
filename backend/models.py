"""
Database models for VoxStitch.
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    chats = relationship("Chat", back_populates="user")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    title = Column(String)
    content = Column(JSON)
    chat_metadata = Column(JSON, nullable=True)  # Renamed from metadata to chat_metadata
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    user = relationship("User", back_populates="chats")

# Pydantic Models
class MessageContent(BaseModel):
    role: str
    content: str

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatBase(BaseModel):
    platform: str
    title: str
    content: List[MessageContent]
    chat_metadata: Optional[Dict[str, Any]] = None

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True