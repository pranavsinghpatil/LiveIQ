from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./chatsynth.db"  # SQLite as fallback for development
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Association tables
chat_tags = Table(
    'chat_tags',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat_logs.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chat_logs = relationship("ChatLog", back_populates="user")
    tags = relationship("Tag", back_populates="user")

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    source = Column(String)  # e.g., 'chatgpt', 'mistral', 'gemini'
    content = Column(JSON)  # Store the actual chat content
    metadata = Column(JSON)  # Store platform-specific metadata
    summary = Column(String)  # Auto-generated summary
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_logs")
    tags = relationship("Tag", secondary=chat_tags, back_populates="chats")
    annotations = relationship("Annotation", back_populates="chat_log")
    versions = relationship("ChatVersion", back_populates="chat_log")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="tags")
    chats = relationship("ChatLog", secondary=chat_tags, back_populates="tags")

class Annotation(Base):
    __tablename__ = "annotations"
    
    id = Column(Integer, primary_key=True)
    chat_log_id = Column(Integer, ForeignKey("chat_logs.id"))
    content = Column(String)
    position = Column(JSON)  # Store position info (start/end indices)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chat_log = relationship("ChatLog", back_populates="annotations")

class ChatVersion(Base):
    __tablename__ = "chat_versions"
    
    id = Column(Integer, primary_key=True)
    chat_log_id = Column(Integer, ForeignKey("chat_logs.id"))
    content = Column(JSON)  # Store the version content
    version_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chat_log = relationship("ChatLog", back_populates="versions")
