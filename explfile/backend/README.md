# Backend Architecture

## Overview
The backend of VoxStitch is built using FastAPI, providing a robust and high-performance API server that handles chat imports, user authentication, and data processing.

## Directory Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── auth/
│   │   ├── chat/
│   │   ├── user/
│   │   └── utils/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── alembic/
└── requirements.txt
```

## Key Components

### 1. Core Modules

#### Authentication Module (`core/auth/`)
- JWT token handling
- User authentication
- Session management
- Guest mode implementation
- Social auth integration

#### Chat Module (`core/chat/`)
- Chat import processing
- Platform-specific parsers
- Content validation
- Search functionality
- Export capabilities

#### User Module (`core/user/`)
- User management
- Profile handling
- Usage tracking
- Permissions system

#### Utilities (`core/utils/`)
- Common helper functions
- Data processing utilities
- Error handling
- Logging setup

### 2. Data Models (`models/`)

#### User Model
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_guest = Column(Boolean, default=False)
    remaining_imports = Column(Integer)
    remaining_messages = Column(Integer)
```

#### Chat Model
```python
class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    platform = Column(String)
    content = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 3. API Endpoints

#### Authentication Endpoints
```python
@router.post("/auth/login")
async def login(credentials: LoginCredentials):
    # Login logic

@router.post("/auth/guest")
async def guest_login():
    # Guest login logic

@router.post("/auth/refresh")
async def refresh_token():
    # Token refresh logic
```

#### Chat Endpoints
```python
@router.post("/chats/import")
async def import_chat(
    file: UploadFile = File(...),
    platform: str = Form(...),
    user: User = Depends(get_current_user)
):
    # Chat import logic

@router.get("/chats/{chat_id}")
async def get_chat(
    chat_id: UUID,
    user: User = Depends(get_current_user)
):
    # Chat retrieval logic
```

### 4. Services

#### Chat Import Service
```python
class ChatImportService:
    async def import_from_file(
        self,
        file: UploadFile,
        platform: str,
        user: User
    ) -> Chat:
        # File processing
        # Content validation
        # Database storage
```

#### User Service
```python
class UserService:
    async def create_guest_user(self) -> User:
        # Guest user creation
        # Usage limit setup
```

## Security Features

### 1. Authentication
- JWT token-based authentication
- Secure password hashing
- Token refresh mechanism
- Rate limiting

### 2. Data Protection
- Input validation
- SQL injection prevention
- XSS protection
- CORS configuration

### 3. Guest Mode Security
- Usage limitations
- Resource access control
- Upgrade path security

## Database Integration

### 1. SQLAlchemy Setup
```python
DATABASE_URL = config.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### 2. Migrations
- Alembic integration
- Version control for schema
- Automated migrations

## Error Handling

### 1. Custom Exceptions
```python
class ChatImportError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=400,
            detail=detail
        )

class GuestLimitError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Guest user limit reached"
        )
```

### 2. Error Middleware
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

## Testing

### 1. Unit Tests
```python
def test_guest_user_creation():
    user = await UserService().create_guest_user()
    assert user.is_guest
    assert user.remaining_imports == 2
```

### 2. Integration Tests
```python
async def test_chat_import():
    response = await client.post(
        "/chats/import",
        files={"file": ("chat.json", json_content)}
    )
    assert response.status_code == 200
```

## Performance Optimizations

### 1. Caching
- Redis integration
- Query result caching
- Token caching

### 2. Async Operations
- Asynchronous database queries
- Background tasks
- File processing optimization

## Monitoring and Logging

### 1. Logging Setup
```python
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    }
})
```

### 2. Metrics
- Request timing
- Error tracking
- Resource usage monitoring

## Recent Updates
- Enhanced chat import processing
- Improved error handling
- Added guest mode limitations
- Optimized database queries
- Enhanced security measures
