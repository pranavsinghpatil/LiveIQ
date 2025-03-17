# Backend Code Documentation

*Last Updated: 2025-03-17*

## Database Models

### User Model
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    full_name = Column(String)
```

**Purpose**: Manages user authentication and profile data
**Location**: `backend/app/models/user.py`
**Dependencies**: SQLAlchemy, bcrypt

**Key Methods**:
- `create_user(email, password)`: Creates new user with hashed password
- `verify_password(password)`: Validates password hash
- `update_profile(data)`: Updates user profile information

### ChatLog Model
```python
class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    source = Column(String)
    content = Column(JSON)
    metadata = Column(JSON)
    summary = Column(String)
```

**Purpose**: Stores chat conversations from various AI platforms
**Location**: `backend/app/models/chat.py`
**Dependencies**: SQLAlchemy, json

**Key Methods**:
- `import_chat(data)`: Imports chat from external platform
- `generate_summary()`: Creates automated summary using NLP
- `export_chat(format)`: Exports chat in specified format

## API Endpoints

### Authentication Routes
```python
@router.post("/auth/login")
async def login(credentials: LoginCredentials):
    """
    Authenticates user and returns JWT token
    
    Args:
        credentials (LoginCredentials): Email and password
        
    Returns:
        dict: Access token and user info
        
    Raises:
        HTTPException: If credentials invalid
    """
```

**Location**: `backend/app/api/auth.py`
**Dependencies**: FastAPI, JWT

### Chat Management Routes
```python
@router.post("/chat/import")
async def import_chat(
    chat_data: ChatImport,
    current_user: User = Depends(get_current_user)
):
    """
    Imports chat from external platform
    
    Args:
        chat_data (ChatImport): Chat content and metadata
        current_user (User): Authenticated user
        
    Returns:
        ChatLog: Imported chat details
    """
```

**Location**: `backend/app/api/chat.py`
**Dependencies**: FastAPI, pydantic

## Services

### Chat Import Service
```python
class ChatImportService:
    async def import_from_chatgpt(self, data: dict) -> ChatLog:
        """Imports chat from ChatGPT"""
        
    async def import_from_mistral(self, data: dict) -> ChatLog:
        """Imports chat from Mistral"""
        
    async def import_from_gemini(self, data: dict) -> ChatLog:
        """Imports chat from Gemini"""
```

**Purpose**: Handles chat import from different platforms
**Location**: `backend/app/services/chat_import.py`
**Dependencies**: aiohttp, beautifulsoup4

### Summarization Service
```python
class SummarizationService:
    async def generate_summary(self, content: str) -> str:
        """
        Generates chat summary using NLP
        
        Args:
            content (str): Chat content
            
        Returns:
            str: Generated summary
        """
```

**Purpose**: Creates automated summaries of chat conversations
**Location**: `backend/app/services/summarization.py`
**Dependencies**: transformers, torch

## Utility Functions

### Database Utilities
```python
async def get_db():
    """Database dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def paginate_query(query, page: int, size: int):
    """Adds pagination to database query"""
```

**Location**: `backend/app/utils/database.py`
**Dependencies**: SQLAlchemy

### Authentication Utilities
```python
def create_access_token(data: dict) -> str:
    """Creates JWT token"""

def verify_token(token: str) -> dict:
    """Verifies JWT token"""
```

**Location**: `backend/app/utils/auth.py`
**Dependencies**: PyJWT

## Performance Optimizations

### Database Query Optimization
```python
# Use select_from for complex joins
query = (
    select(ChatLog)
    .select_from(join(ChatLog, Tag))
    .where(Tag.name.in_(tags))
)

# Use bulk operations
db.bulk_insert_mappings(ChatLog, chat_logs)
```

### Caching Strategy
```python
@cache(ttl=3600)
async def get_user_chats(user_id: int):
    """Cached chat retrieval"""
```

## Error Handling

### Global Exception Handler
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handles HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

### Custom Exceptions
```python
class ChatImportError(Exception):
    """Raised when chat import fails"""

class InvalidFormatError(Exception):
    """Raised when chat format is invalid"""
```

## Testing

### Unit Tests
```python
def test_chat_import():
    """Tests chat import functionality"""
    service = ChatImportService()
    result = service.import_from_chatgpt(sample_data)
    assert result.source == "chatgpt"
```

### Integration Tests
```python
async def test_chat_api():
    """Tests chat API endpoints"""
    response = await client.post(
        "/chat/import",
        json=sample_chat_data
    )
    assert response.status_code == 200
```

## Deployment

### Environment Variables
```python
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
```

### Database Migrations
```python
# Create migration
alembic revision --autogenerate -m "Add chat version"

# Apply migration
alembic upgrade head
```

## Security Measures

### Input Validation
```python
class ChatImport(BaseModel):
    """Chat import validation"""
    content: str
    source: str
    metadata: Optional[dict]
    
    @validator("source")
    def validate_source(cls, v):
        if v not in VALID_SOURCES:
            raise ValueError("Invalid source")
        return v
```

### Rate Limiting
```python
@limiter.limit("5/minute")
async def import_chat():
    """Rate-limited chat import"""
```

## Next Steps
1. Implement full-text search
2. Add real-time updates
3. Enhance error handling
4. Improve test coverage
5. Add monitoring
