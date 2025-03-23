"""
Database models for ChatSynth.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default='user')  # user, guest, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chats = relationship("ChatLog", back_populates="user")

class ChatLog(Base):
    """Chat log model storing conversations from different platforms."""
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    platform = Column(String(20), nullable=False)  # ChatGPT, Mistral, Gemini
    imported_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    """Individual messages within a chat."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    # Relationships
    chat = relationship("ChatLog", back_populates="messages")
