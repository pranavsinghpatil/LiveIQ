# Development Workflow and Guidelines

*Last Updated: 2025-03-17*

This document outlines the development workflow, coding standards, and best practices for the ChatSynth project.

## Development Environment Setup

### Prerequisites
1. Python 3.9+
2. Node.js 18+
3. PostgreSQL 14+
4. Redis 6+

### Installation Steps
```bash
# Clone repository
git clone https://github.com/pranavsinghpatil/ChatSynth.git
cd ChatSynth

# Backend setup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

### Environment Configuration
```bash
# .env file
DATABASE_URL=postgresql://user:pass@localhost:5432/chatsynth
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-secret-key
ALLOWED_ORIGINS=http://localhost:3000
```

## Development Workflow

### 1. Feature Development

#### Branch Naming Convention
- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Performance: `perf/description`

#### Code Organization
```
backend/
├── app/
│   ├── api/            # API routes
│   ├── core/           # Core functionality
│   │   ├── config.py   # Configuration
│   │   ├── security.py # Security utils
│   │   └── database.py # Database setup
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic models
│   ├── services/       # Business logic
│   └── utils/          # Helper functions
└── tests/              # Test files

frontend/
├── src/
│   ├── components/     # React components
│   ├── services/       # API services
│   ├── store/          # State management
│   └── utils/          # Helper functions
└── tests/              # Test files
```

### 2. Code Standards

#### Python Style Guide
```python
# Use type hints
def import_chat(
    chat_data: ChatImport,
    user_id: int
) -> ChatLog:
    """
    Import chat from external platform.
    
    Args:
        chat_data: Chat data to import
        user_id: ID of the user
        
    Returns:
        ChatLog: Imported chat instance
        
    Raises:
        ValidationError: If chat data is invalid
    """
    validated_data = validate_chat_data(chat_data)
    return create_chat_log(validated_data, user_id)

# Use dependency injection
class ChatService:
    def __init__(
        self,
        db: Session,
        cache: Redis,
        config: Settings
    ):
        self.db = db
        self.cache = cache
        self.config = config
```

#### TypeScript Style Guide
```typescript
// Use interfaces for type definitions
interface Chat {
  id: string;
  title: string;
  content: Record<string, any>;
  metadata: {
    source: string;
    timestamp: string;
  };
}

// Use functional components
const ChatList: React.FC<{ chats: Chat[] }> = ({ chats }) => {
  return (
    <div className="chat-list">
      {chats.map(chat => (
        <ChatItem key={chat.id} chat={chat} />
      ))}
    </div>
  );
};

// Use proper error handling
const fetchChats = async (): Promise<Chat[]> => {
  try {
    const response = await api.get('/chats');
    return response.data;
  } catch (error) {
    handleError(error);
    return [];
  }
};
```

### 3. Testing Strategy

#### Backend Tests
```python
# Unit tests
def test_chat_import():
    chat_data = {"content": "test", "source": "chatgpt"}
    result = import_chat(chat_data, user_id=1)
    assert result.source == "chatgpt"
    assert result.user_id == 1

# Integration tests
@pytest.mark.asyncio
async def test_chat_api():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/chats/import",
            json={"content": "test", "source": "chatgpt"}
        )
        assert response.status_code == 200
```

#### Frontend Tests
```typescript
// Component tests
describe('ChatList', () => {
  it('renders chat items', () => {
    const chats = [
      { id: '1', title: 'Chat 1' },
      { id: '2', title: 'Chat 2' }
    ];
    
    render(<ChatList chats={chats} />);
    expect(screen.getByText('Chat 1')).toBeInTheDocument();
    expect(screen.getByText('Chat 2')).toBeInTheDocument();
  });
});

// API tests
describe('chatApi', () => {
  it('fetches chats', async () => {
    const mockChats = [{ id: '1', title: 'Chat 1' }];
    mock.onGet('/api/chats').reply(200, mockChats);
    
    const result = await chatApi.getChats();
    expect(result).toEqual(mockChats);
  });
});
```

### 4. Code Review Process

#### Review Checklist
1. Code Quality
   - [ ] Follows style guide
   - [ ] Proper error handling
   - [ ] Type safety
   - [ ] No code smells

2. Testing
   - [ ] Unit tests added
   - [ ] Integration tests added
   - [ ] Tests pass
   - [ ] Adequate coverage

3. Documentation
   - [ ] Code comments
   - [ ] API documentation
   - [ ] README updates
   - [ ] Change log entry

4. Security
   - [ ] Input validation
   - [ ] Authentication checks
   - [ ] Data sanitization
   - [ ] Error handling

### 5. Deployment Process

#### Staging Deployment
```bash
# Run tests
pytest backend/tests
npm test

# Build frontend
cd frontend
npm run build

# Deploy to staging
docker-compose -f docker-compose.staging.yml up -d
```

#### Production Deployment
```bash
# Database migrations
alembic upgrade head

# Deploy services
kubectl apply -f k8s/production/

# Verify deployment
kubectl get pods
kubectl logs -f deployment/chatsynth
```

## Best Practices

### 1. Error Handling
```python
# Backend error handling
class ChatError(Exception):
    """Base exception for chat operations"""
    pass

class ChatImportError(ChatError):
    """Raised when chat import fails"""
    pass

@app.exception_handler(ChatError)
async def chat_exception_handler(request: Request, exc: ChatError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

### 2. Logging
```python
# Structured logging
import structlog

logger = structlog.get_logger()

async def import_chat(chat_data: dict):
    logger.info(
        "importing_chat",
        source=chat_data["source"],
        user_id=chat_data["user_id"]
    )
    try:
        result = await process_import(chat_data)
        logger.info(
            "chat_imported",
            chat_id=result.id,
            status="success"
        )
        return result
    except Exception as e:
        logger.error(
            "chat_import_failed",
            error=str(e),
            chat_data=chat_data
        )
        raise
```

### 3. Performance
```python
# Use caching
@cache(ttl=3600)
async def get_user_chats(user_id: int):
    return await db.query(ChatLog).filter(
        ChatLog.user_id == user_id
    ).all()

# Optimize database queries
def get_chats_with_related():
    return (
        db.query(ChatLog)
        .options(
            selectinload(ChatLog.tags),
            selectinload(ChatLog.annotations)
        )
        .all()
    )
```

### 4. Security
```python
# Input validation
class ChatImport(BaseModel):
    content: str
    source: str
    metadata: Optional[dict] = None
    
    @validator("source")
    def validate_source(cls, v):
        if v not in VALID_SOURCES:
            raise ValueError(f"Invalid source: {v}")
        return v

# Authentication
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return get_user(db, user_id)
```

## Monitoring and Maintenance

### 1. Performance Monitoring
```python
# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 2. Error Tracking
```python
# Sentry integration
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

## Next Steps

### 1. Immediate Tasks
- [ ] Set up CI/CD pipeline
- [ ] Implement monitoring
- [ ] Add performance tests
- [ ] Update documentation

### 2. Future Improvements
- [ ] Add automated code quality checks
- [ ] Implement feature flags
- [ ] Add performance monitoring
- [ ] Enhance security measures
