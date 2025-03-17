# API Documentation

*Last Updated: 2025-03-17*

## API Overview

The ChatSynth API is built using FastAPI and follows RESTful principles. This guide documents all available endpoints, their request/response formats, and usage examples.

## Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://api.chatsynth.com/api/v1`

## Authentication

### JWT Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

### Authentication Endpoints

#### 1. User Registration
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
}
```

**Response**:
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
}
```

**Implementation**: `backend/app/api/auth.py`
```python
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(db, user)
```

#### 2. User Login
```http
POST /auth/login
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "securepassword"
}
```

**Response**:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
}
```

## Chat Management

### 1. Import Chat Log
```http
POST /chats/import
Content-Type: application/json
Authorization: Bearer <token>

{
    "title": "OpenAI Chat #123",
    "source": "openai",
    "content": {
        "messages": [
            {
                "role": "user",
                "content": "Hello, AI!"
            },
            {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            }
        ]
    }
}
```

**Response**:
```json
{
    "id": 1,
    "title": "OpenAI Chat #123",
    "created_at": "2025-03-17T00:00:00Z"
}
```

**Implementation**: `backend/app/api/chats.py`
```python
@router.post("/import", response_model=ChatLogResponse)
async def import_chat(
    chat: ChatLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_chat_log(db, chat, current_user.id)
```

### 2. List Chat Logs
```http
GET /chats
Authorization: Bearer <token>
```

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `source`: Filter by source
- `start_date`: Filter by start date
- `end_date`: Filter by end date

**Response**:
```json
{
    "items": [
        {
            "id": 1,
            "title": "OpenAI Chat #123",
            "source": "openai",
            "created_at": "2025-03-17T00:00:00Z"
        }
    ],
    "total": 1,
    "page": 1,
    "pages": 1
}
```

### 3. Get Chat Log Details
```http
GET /chats/{chat_id}
Authorization: Bearer <token>
```

**Response**:
```json
{
    "id": 1,
    "title": "OpenAI Chat #123",
    "source": "openai",
    "content": {
        "messages": [...]
    },
    "created_at": "2025-03-17T00:00:00Z",
    "tags": ["important", "work"]
}
```

## Tag Management

### 1. Create Tag
```http
POST /tags
Content-Type: application/json
Authorization: Bearer <token>

{
    "name": "important"
}
```

**Response**:
```json
{
    "id": 1,
    "name": "important"
}
```

### 2. Tag Chat Log
```http
POST /chats/{chat_id}/tags
Content-Type: application/json
Authorization: Bearer <token>

{
    "tag_ids": [1, 2, 3]
}
```

## Search

### 1. Search Chat Logs
```http
GET /search
Authorization: Bearer <token>
```

**Query Parameters**:
- `q`: Search query
- `source`: Filter by source
- `tags`: Comma-separated tag IDs
- `start_date`: Filter by start date
- `end_date`: Filter by end date

**Response**:
```json
{
    "items": [
        {
            "id": 1,
            "title": "OpenAI Chat #123",
            "snippet": "Highlighted search result...",
            "score": 0.95
        }
    ],
    "total": 1
}
```

## Error Handling

### Common Error Responses

#### 1. Authentication Error
```json
{
    "detail": "Could not validate credentials"
}
```

#### 2. Validation Error
```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "invalid email format",
            "type": "value_error"
        }
    ]
}
```

#### 3. Not Found Error
```json
{
    "detail": "Chat log not found"
}
```

## Rate Limiting

The API implements rate limiting per user:
- Authentication endpoints: 5 requests per minute
- Other endpoints: 100 requests per minute

```python
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    # Rate limiting implementation
```

## WebSocket Endpoints

### Real-time Updates
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

// Listen for updates
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update received:', data);
};
```

## API Versioning

The API uses URL versioning:
- `/api/v1/` - Current version
- Future versions will be `/api/v2/`, etc.

## Testing the API

### Using curl
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user@example.com", "password": "password"}'

# Get chat logs
curl http://localhost:8000/api/v1/chats \
  -H "Authorization: Bearer <token>"
```

### Using the Swagger UI
- Development: `http://localhost:8000/docs`
- Production: `https://api.chatsynth.com/docs`

## Next Steps
1. Review the [Frontend Guide](./06_frontend_guide.md)
2. Set up your development environment
3. Try making some API calls
