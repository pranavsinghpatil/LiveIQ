# Understanding Database Schema and Models

## Overview

ChatSynth uses PostgreSQL with SQLAlchemy ORM. Our schema is designed to efficiently store and query chat conversations from multiple AI platforms.

## 1. Core Models

### Users
```python
# In backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chats = relationship("ChatLog", back_populates="user")
    tags = relationship("Tag", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"
```

### Chat Logs
```python
# In backend/app/models/chat.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source = Column(String, nullable=False)  # chatgpt, mistral, gemini
    content = Column(JSON, nullable=False)   # Chat messages
    summary = Column(String)                 # AI-generated summary
    metadata = Column(JSON)                  # Platform-specific data
    
    # Relationships
    user = relationship("User", back_populates="chats")
    tags = relationship("Tag", secondary="chat_tags")
    versions = relationship("ChatVersion", back_populates="chat")
    annotations = relationship("Annotation", back_populates="chat")
    
    def __repr__(self):
        return f"<ChatLog {self.id} from {self.source}>"
```

### Tags
```python
# In backend/app/models/tag.py
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    color = Column(String, default="#808080")  # Hex color
    
    # Relationships
    user = relationship("User", back_populates="tags")
    chats = relationship("ChatLog", secondary="chat_tags")
    
    def __repr__(self):
        return f"<Tag {self.name}>"

# Association table for many-to-many relationship
chat_tags = Table(
    "chat_tags",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chat_logs.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
    PrimaryKeyConstraint("chat_id", "tag_id")
)
```

### Chat Versions
```python
# In backend/app/models/version.py
class ChatVersion(Base):
    __tablename__ = "chat_versions"
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chat_logs.id"))
    content = Column(JSON, nullable=False)  # Chat state at this version
    created_at = Column(DateTime, default=datetime.utcnow)
    comment = Column(String)  # Optional version comment
    
    # Relationship
    chat = relationship("ChatLog", back_populates="versions")
    
    def __repr__(self):
        return f"<ChatVersion {self.id} for chat {self.chat_id}>"
```

### Annotations
```python
# In backend/app/models/annotation.py
class Annotation(Base):
    __tablename__ = "annotations"
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chat_logs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    position = Column(JSON)  # Where in chat to show annotation
    
    # Relationships
    chat = relationship("ChatLog", back_populates="annotations")
    user = relationship("User")
    
    def __repr__(self):
        return f"<Annotation {self.id} for chat {self.chat_id}>"
```

## 2. Database Configuration

```python
# In backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/chatsynth"

# Create engine with connection pool
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=10
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 3. Database Operations

### Basic CRUD Operations
```python
# In backend/app/crud/chat.py
from sqlalchemy.orm import Session
from typing import List, Optional

class ChatCRUD:
    def create_chat(
        self,
        db: Session,
        user_id: int,
        chat_data: dict
    ) -> ChatLog:
        chat = ChatLog(
            user_id=user_id,
            source=chat_data["source"],
            content=chat_data["content"],
            metadata=chat_data.get("metadata", {})
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat
    
    def get_chat(
        self,
        db: Session,
        chat_id: int
    ) -> Optional[ChatLog]:
        return db.query(ChatLog)\
            .filter(ChatLog.id == chat_id)\
            .first()
    
    def get_user_chats(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChatLog]:
        return db.query(ChatLog)\
            .filter(ChatLog.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def update_chat(
        self,
        db: Session,
        chat_id: int,
        chat_data: dict
    ) -> Optional[ChatLog]:
        chat = self.get_chat(db, chat_id)
        if not chat:
            return None
        
        # Create version before update
        version = ChatVersion(
            chat_id=chat.id,
            content=chat.content
        )
        db.add(version)
        
        # Update chat
        for key, value in chat_data.items():
            setattr(chat, key, value)
        
        db.commit()
        db.refresh(chat)
        return chat
    
    def delete_chat(
        self,
        db: Session,
        chat_id: int
    ) -> bool:
        chat = self.get_chat(db, chat_id)
        if not chat:
            return False
        
        db.delete(chat)
        db.commit()
        return True
```

### Advanced Queries
```python
# In backend/app/crud/search.py
from sqlalchemy import func, or_
from typing import List

class ChatSearch:
    def search_chats(
        self,
        db: Session,
        user_id: int,
        query: str = None,
        tags: List[str] = None,
        source: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100
    ) -> List[ChatLog]:
        # Start with base query
        base_query = db.query(ChatLog)\
            .filter(ChatLog.user_id == user_id)
        
        # Add content search if query provided
        if query:
            base_query = base_query.filter(
                or_(
                    # Search in content
                    ChatLog.content.op('->>')('messages').contains(query),
                    # Search in summary
                    ChatLog.summary.ilike(f"%{query}%")
                )
            )
        
        # Filter by tags
        if tags:
            base_query = base_query\
                .join(chat_tags)\
                .join(Tag)\
                .filter(Tag.name.in_(tags))
        
        # Filter by source
        if source:
            base_query = base_query.filter(
                ChatLog.source == source
            )
        
        # Filter by date range
        if start_date:
            base_query = base_query.filter(
                ChatLog.created_at >= start_date
            )
        if end_date:
            base_query = base_query.filter(
                ChatLog.created_at <= end_date
            )
        
        return base_query.limit(limit).all()
```

## 4. Database Indexes

```sql
-- In migrations/versions/xxx_add_indexes.py

-- Index for text search
CREATE INDEX idx_chat_content ON chat_logs
USING gin(to_tsvector('english', content::text));

-- Index for tag lookups
CREATE INDEX idx_chat_tags ON chat_tags(chat_id, tag_id);

-- Index for user's chats
CREATE INDEX idx_user_chats ON chat_logs(user_id);

-- Index for source filtering
CREATE INDEX idx_chat_source ON chat_logs(source);

-- Composite index for date range queries
CREATE INDEX idx_chat_dates ON chat_logs(user_id, created_at);
```

## 5. Best Practices

### 1. Connection Management
```python
# In backend/app/core/database.py
from contextlib import contextmanager

@contextmanager
def transaction():
    """Transaction context manager"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
```

### 2. Query Optimization
```python
# In backend/app/crud/chat.py
def get_chat_with_related(
    self,
    db: Session,
    chat_id: int
) -> Optional[ChatLog]:
    # Load chat with related data in one query
    return db.query(ChatLog)\
        .options(
            joinedload(ChatLog.tags),
            joinedload(ChatLog.annotations),
            joinedload(ChatLog.versions)
        )\
        .filter(ChatLog.id == chat_id)\
        .first()
```

### 3. Batch Operations
```python
# In backend/app/crud/chat.py
def bulk_tag_chats(
    self,
    db: Session,
    chat_ids: List[int],
    tag_ids: List[int]
) -> None:
    # Create all associations at once
    associations = [
        {"chat_id": chat_id, "tag_id": tag_id}
        for chat_id in chat_ids
        for tag_id in tag_ids
    ]
    
    db.execute(chat_tags.insert(), associations)
    db.commit()
```

## Common Questions

1. **Why use PostgreSQL?**
   - JSON support for chat data
   - Full-text search capabilities
   - Robust transaction support
   - Good performance at scale

2. **How to handle migrations?**
   - Use Alembic for schema changes
   - Version control migrations
   - Test migrations before deploy
   - Have rollback plans

3. **Performance considerations?**
   - Use appropriate indexes
   - Optimize queries
   - Batch operations
   - Monitor query times
