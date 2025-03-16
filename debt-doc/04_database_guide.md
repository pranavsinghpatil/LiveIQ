# Database Guide

*Last Updated: 2025-03-17*

## Database Overview

ChatSynth uses PostgreSQL as its primary database, with Redis for caching. This guide explains the database schema, relationships, and common operations.

## Schema Design

### Core Tables

#### 1. Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
```

**Purpose**: Stores user account information
**Location**: `backend/app/models/user.py`
**Key Fields**:
- `id`: Unique identifier
- `email`: User's email (unique)
- `hashed_password`: Bcrypt hashed password

#### 2. Chat Logs Table
```sql
CREATE TABLE chat_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    source VARCHAR(100),
    content JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_chat_logs_user_id ON chat_logs(user_id);
CREATE INDEX idx_chat_logs_created_at ON chat_logs(created_at);
CREATE INDEX idx_chat_logs_source ON chat_logs(source);
```

**Purpose**: Stores imported chat conversations
**Location**: `backend/app/models/chat.py`
**Key Fields**:
- `content`: JSON structure containing the chat messages
- `metadata`: Additional information about the chat
- `source`: Origin of the chat (e.g., "openai", "anthropic")

#### 3. Tags Table
```sql
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_log_tags (
    chat_log_id INTEGER REFERENCES chat_logs(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (chat_log_id, tag_id)
);
```

**Purpose**: Organizes chat logs with user-defined tags
**Location**: `backend/app/models/tag.py`

## SQLAlchemy Models

### User Model
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Relationships
    chat_logs = relationship("ChatLog", back_populates="user")
    tags = relationship("Tag", back_populates="user")
```

### ChatLog Model
```python
class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(JSONB)
    
    # Relationships
    user = relationship("User", back_populates="chat_logs")
    tags = relationship("Tag", secondary="chat_log_tags")
```

## Common Database Operations

### 1. User Operations
```python
# Create user
async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    return db_user

# Get user by email
async def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
```

### 2. Chat Log Operations
```python
# Add chat log
async def create_chat_log(db: Session, chat: ChatLogCreate, user_id: int):
    db_chat = ChatLog(
        user_id=user_id,
        content=chat.content,
        metadata=chat.metadata
    )
    db.add(db_chat)
    db.commit()
    return db_chat

# Get user's chat logs
async def get_user_chat_logs(db: Session, user_id: int):
    return db.query(ChatLog).filter(ChatLog.user_id == user_id).all()
```

## Database Migration

We use Alembic for database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Redis Cache Structure

### 1. Session Cache
```python
# Key format: session:{user_id}
# Value: JSON string of session data
await redis.set(f"session:{user_id}", session_data, expire=3600)
```

### 2. Chat Cache
```python
# Key format: chat:{chat_id}
# Value: JSON string of chat data
await redis.set(f"chat:{chat_id}", chat_data, expire=1800)
```

## Performance Optimization

### 1. Indexing Strategy
- B-tree indexes on frequently queried columns
- Composite indexes for common query patterns
- Regular index maintenance

### 2. Query Optimization
```python
# Efficient querying with joins
def get_user_chats_with_tags(db: Session, user_id: int):
    return (
        db.query(ChatLog)
        .options(joinedload(ChatLog.tags))
        .filter(ChatLog.user_id == user_id)
        .all()
    )
```

### 3. Connection Pooling
```python
# Database connection pool configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)
```

## Backup and Recovery

### 1. Backup Strategy
```bash
# Daily backup script
pg_dump -U postgres -d chatsynth > backup_$(date +%Y%m%d).sql
```

### 2. Recovery Process
```bash
# Restore from backup
psql -U postgres -d chatsynth < backup_file.sql
```

## Common Issues and Solutions

### 1. Connection Issues
```python
# Handling connection timeouts
from sqlalchemy import exc
try:
    db.query(User).all()
except exc.OperationalError:
    db.rollback()
```

### 2. Deadlocks
```python
# Handling deadlocks
from sqlalchemy import exc
try:
    with db.begin():
        # transaction code
except exc.DBDeadlockError:
    # retry logic
```

## Next Steps
1. Review the [API Documentation](./05_api_documentation.md)
2. Set up your local database
3. Try running some sample queries
