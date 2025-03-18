# Database Guide

*Last Updated: 2025-03-17*

## Database Overview

ChatSynth uses PostgreSQL as its primary database to store chat logs from multiple AI platforms (ChatGPT, Mistral, Gemini), along with user data, annotations, and version history. Redis is used for caching and real-time features.

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
- `full_name`: User's full name

#### 2. Chat Logs Table
```sql
CREATE TABLE chat_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    source VARCHAR(100),
    content JSONB,
    metadata JSONB,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_chat_logs_user_id ON chat_logs(user_id);
CREATE INDEX idx_chat_logs_source ON chat_logs(source);
CREATE INDEX idx_chat_logs_created_at ON chat_logs(created_at);
CREATE INDEX gin_idx_chat_logs_content ON chat_logs USING gin(content);
```

**Purpose**: Stores imported chat conversations from various AI platforms
**Location**: `backend/app/models/chat.py`
**Key Fields**:
- `content`: JSON structure containing the chat messages
- `metadata`: Platform-specific metadata
- `source`: Origin platform (e.g., "chatgpt", "mistral", "gemini")
- `summary`: Auto-generated summary using NLP

#### 3. Tags Table
```sql
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_tags (
    chat_id INTEGER REFERENCES chat_logs(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (chat_id, tag_id)
);

-- Indexes
CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name ON tags(name);
```

**Purpose**: Enables chat organization through user-defined tags
**Location**: `backend/app/models/tag.py`

#### 4. Annotations Table
```sql
CREATE TABLE annotations (
    id SERIAL PRIMARY KEY,
    chat_log_id INTEGER REFERENCES chat_logs(id),
    content TEXT,
    position JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_annotations_chat_log_id ON annotations(chat_log_id);
```

**Purpose**: Stores user annotations and highlights for chat logs
**Location**: `backend/app/models/annotation.py`
**Key Fields**:
- `content`: Annotation text
- `position`: JSON object storing start/end indices in chat

#### 5. Chat Versions Table
```sql
CREATE TABLE chat_versions (
    id SERIAL PRIMARY KEY,
    chat_log_id INTEGER REFERENCES chat_logs(id),
    content JSONB,
    version_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_chat_versions_chat_log_id ON chat_versions(chat_log_id);
```

**Purpose**: Maintains version history of chat logs
**Location**: `backend/app/models/version.py`

## Common Database Operations

### 1. Chat Import Operations
```python
async def import_chat(db: Session, chat_data: ChatImport, user_id: int):
    # Create new chat log
    chat_log = ChatLog(
        user_id=user_id,
        title=chat_data.title,
        source=chat_data.source,
        content=chat_data.content,
        metadata=chat_data.metadata
    )
    db.add(chat_log)
    await db.flush()
    
    # Generate and store summary
    summary = await generate_summary(chat_data.content)
    chat_log.summary = summary
    
    # Create initial version
    version = ChatVersion(
        chat_log_id=chat_log.id,
        content=chat_data.content,
        version_number=1
    )
    db.add(version)
    
    await db.commit()
    return chat_log
```

### 2. Search Operations
```python
async def search_chats(
    db: Session,
    user_id: int,
    query: str,
    source: Optional[str] = None,
    tags: Optional[List[str]] = None
):
    query = (
        db.query(ChatLog)
        .filter(ChatLog.user_id == user_id)
        .filter(
            or_(
                ChatLog.content.contains(query),
                ChatLog.summary.contains(query)
            )
        )
    )
    
    if source:
        query = query.filter(ChatLog.source == source)
    
    if tags:
        query = query.join(ChatLog.tags).filter(Tag.name.in_(tags))
    
    return await query.all()
```

### 3. Annotation Operations
```python
async def add_annotation(
    db: Session,
    chat_id: int,
    content: str,
    position: Dict
):
    annotation = Annotation(
        chat_log_id=chat_id,
        content=content,
        position=position
    )
    db.add(annotation)
    await db.commit()
    return annotation
```

## Performance Optimization

### 1. Indexing Strategy
- GIN index for JSONB content search
- B-tree indexes for foreign keys and common filters
- Composite indexes for frequently combined queries

### 2. Query Optimization
```python
# Efficient chat retrieval with related data
def get_chat_with_details(db: Session, chat_id: int):
    return (
        db.query(ChatLog)
        .options(
            joinedload(ChatLog.tags),
            joinedload(ChatLog.annotations),
            joinedload(ChatLog.versions)
        )
        .filter(ChatLog.id == chat_id)
        .first()
    )
```

### 3. Caching Strategy
```python
# Cache frequently accessed chat data
async def get_cached_chat(redis: Redis, chat_id: int):
    cache_key = f"chat:{chat_id}"
    cached = await redis.get(cache_key)
    
    if cached:
        return json.loads(cached)
        
    chat = await get_chat_with_details(db, chat_id)
    await redis.set(
        cache_key,
        json.dumps(chat),
        expire=3600
    )
    return chat
```

## Data Migration

We use Alembic for database migrations:

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

## Backup Strategy

### 1. Regular Backups
```bash
# Daily backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -Fc chatsynth > backup_${TIMESTAMP}.dump
```

### 2. Restore Process
```bash
# Restore from backup
pg_restore -d chatsynth backup_file.dump
```

## Security Measures

### 1. Data Protection
- Encrypted sensitive data
- Input validation
- Parameterized queries
- Regular security audits

### 2. Access Control
```python
# Example permission check
def check_chat_access(user_id: int, chat_id: int):
    chat = db.query(ChatLog).filter(
        ChatLog.id == chat_id,
        ChatLog.user_id == user_id
    ).first()
    if not chat:
        raise HTTPException(status_code=403)
    return chat
```

## Next Steps
1. Implement full-text search using PostgreSQL's tsearch
2. Add support for chat log merging
3. Implement real-time collaboration features
4. Add analytics capabilities
