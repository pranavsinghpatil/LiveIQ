# Database Module

## Purpose
The database module handles all database operations for VoxStitch, providing a robust SQLAlchemy configuration and session management for PostgreSQL integration.

## Module Structure

### Database Configuration
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/voxstitch"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```

## Core Features

### 1. Session Management
```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def get_db() -> Generator:
    """
    Context manager for database sessions.
    Ensures proper handling of session lifecycle and error cases.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

### 2. Connection Pool Management
```python
def configure_pool(
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_timeout: int = 30,
    pool_recycle: int = 1800
) -> None:
    """
    Configure the database connection pool settings.
    
    Args:
        pool_size: Base number of connections to keep open
        max_overflow: Maximum number of connections above pool_size
        pool_timeout: Seconds to wait before timing out on connection attempt
        pool_recycle: Seconds before connections are recycled
    """
    global engine
    engine.dispose()
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle
    )
    SessionLocal.configure(bind=engine)
```

## Database Models

### 1. User Model
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_guest = Column(Boolean, default=False)
    remaining_imports = Column(Integer, default=2)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 2. Chat Model
```python
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    platform = Column(String)
    content = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="chats")
```

## Database Operations

### 1. CRUD Operations
```python
class CRUDBase:
    def __init__(self, model: Type[Base]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[Base]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Base]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> Base:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Base,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Base:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Base:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

### 2. Query Optimization
```python
def optimize_query(query: Query) -> Query:
    """
    Apply query optimizations like eager loading relationships
    and selecting only necessary columns.
    """
    if hasattr(query.column_descriptions[0]['type'], '__mapper__'):
        mapper = query.column_descriptions[0]['type'].__mapper__
        if mapper.relationships:
            query = query.options(
                *[
                    joinedload(rel.key)
                    for rel in mapper.relationships
                ]
            )
    return query
```

## Migration Management

### 1. Alembic Configuration
```python
from alembic import context
from logging.config import fileConfig

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

### 2. Migration Scripts
```python
def upgrade() -> None:
    """
    Example migration upgrade script.
    """
    op.create_table(
        'chats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('platform', sa.String(), nullable=True),
        sa.Column('content', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chats_id'), 'chats', ['id'], unique=False)
```

## Integration Points

### 1. FastAPI Integration
```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db_session():
    """
    FastAPI dependency for database sessions.
    """
    with get_db() as session:
        yield session

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db_session)):
    return crud.user.get(db=db, id=user_id)
```

### 2. Background Tasks
```python
from fastapi.background import BackgroundTasks

def cleanup_expired_sessions(db: Session):
    """
    Background task to clean up expired sessions.
    """
    expired = (
        db.query(Session)
        .filter(Session.expires_at < datetime.utcnow())
        .all()
    )
    for session in expired:
        db.delete(session)
    db.commit()

@app.post("/login")
async def login(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_session)
):
    background_tasks.add_task(cleanup_expired_sessions, db)
    # Login logic here
```

## Testing

### 1. Test Configuration
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def test_engine():
    return create_engine(
        "postgresql://test:test@localhost:5432/test_db",
        pool_pre_ping=True
    )

@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
```

### 2. Test Cases
```python
def test_create_user(test_db):
    user = User(
        email="test@example.com",
        hashed_password="hashed"
    )
    test_db.add(user)
    test_db.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
```

## Recent Updates
- Added connection pooling
- Improved session management
- Enhanced query optimization
- Added migration support
- Improved testing setup

## Security Considerations
- SQL injection prevention
- Connection encryption
- Password hashing
- Session management
- Access control

## Performance Optimization
- Connection pooling
- Query optimization
- Index management
- Cache integration
- Batch operations
