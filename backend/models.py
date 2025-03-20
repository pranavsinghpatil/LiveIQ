"""
Database models for ChatSynth.
Implements the core data structures for users, chat logs, and metadata.
"""

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Table, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Association table for chat tags
chat_tags = Table(
    'chat_tags',
    Base.metadata,
    Column('chat_id', String, ForeignKey('chatlogs.id')),
    Column('tag_id', String, ForeignKey('tags.id'))
)

class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chatlogs = relationship("ChatLog", back_populates="user")
    annotations = relationship("Annotation", back_populates="user")

class ChatLog(Base):
    """Main chat log model storing conversations from different platforms."""
    __tablename__ = 'chatlogs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    source = Column(String, nullable=False)  # Platform: ChatGPT, Mistral, Gemini
    title = Column(String)
    content = Column(JSON, nullable=False)  # Full chat content
    summary = Column(String)  # Auto-generated summary
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta_data = Column(JSON, default=dict)  # Platform-specific metadata
    
    # Relationships
    user = relationship("User", back_populates="chatlogs")
    versions = relationship("ChatVersion", back_populates="chatlog")
    annotations = relationship("Annotation", back_populates="chatlog")
    tags = relationship("Tag", secondary=chat_tags, back_populates="chatlogs")

class ChatVersion(Base):
    """Version history for chat logs."""
    __tablename__ = 'chatversions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chatlog_id = Column(String, ForeignKey('chatlogs.id'), nullable=False)
    content = Column(JSON, nullable=False)  # Snapshot of chat content
    version = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    meta_data = Column(JSON, default=dict)  # Version-specific metadata
    
    # Relationships
    chatlog = relationship("ChatLog", back_populates="versions")

class Annotation(Base):
    """User annotations for chat logs."""
    __tablename__ = 'annotations'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    chatlog_id = Column(String, ForeignKey('chatlogs.id'), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta_data = Column(JSON, default=dict)  # Annotation metadata (e.g., position)
    
    # Relationships
    user = relationship("User", back_populates="annotations")
    chatlog = relationship("ChatLog", back_populates="annotations")

class Tag(Base):
    """Tags for organizing chat logs."""
    __tablename__ = 'tags'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    chatlogs = relationship("ChatLog", secondary=chat_tags, back_populates="tags")
