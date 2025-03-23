# ChatSynth API Documentation

## Authentication Endpoints

### 1. Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "user123",
  "password": "securepass"
}

Response:
{
  "token": "eyJ0eXAi...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user123",
    "role": "user",
    "created_at": "2025-03-23T12:00:00"
  }
}
```

### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass"
}

Response:
{
  "token": "eyJ0eXAi...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user123",
    "role": "user",
    "created_at": "2025-03-23T12:00:00"
  }
}
```

### 3. Guest Login
```http
POST /auth/guest

Response:
{
  "token": "eyJ0eXAi...",
  "user": {
    "id": 2,
    "email": "guest_1234567890@chatsynth.com",
    "username": "guest_1234567890",
    "role": "guest",
    "created_at": "2025-03-23T12:00:00"
  }
}
```

## Chat Management Endpoints

### 1. List Chats
```http
GET /chats
Authorization: Bearer <token>
Query Parameters:
- platform (optional): Filter by platform (chatgpt, mistral, gemini)

Response:
[
  {
    "id": 1,
    "platform": "chatgpt",
    "user_id": 1,
    "imported_at": "2025-03-23T12:00:00",
    "messages": [
      {
        "id": 1,
        "role": "user",
        "content": "Hello",
        "timestamp": "2025-03-23T12:00:00"
      },
      {
        "id": 2,
        "role": "assistant",
        "content": "Hi there!",
        "timestamp": "2025-03-23T12:00:01"
      }
    ]
  }
]
```

### 2. Import Chat
```http
POST /chats/import
Authorization: Bearer <token>
Content-Type: application/json

{
  "platform": "chatgpt",
  "content": "<chat content>"
}

Response:
{
  "id": 1,
  "platform": "chatgpt",
  "user_id": 1,
  "imported_at": "2025-03-23T12:00:00",
  "messages": []
}
```

### 3. Get Chat Details
```http
GET /chats/{chat_id}
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "platform": "chatgpt",
  "user_id": 1,
  "imported_at": "2025-03-23T12:00:00",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello",
      "timestamp": "2025-03-23T12:00:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Hi there!",
      "timestamp": "2025-03-23T12:00:01"
    }
  ]
}
```

### 4. Delete Chat
```http
DELETE /chats/{chat_id}
Authorization: Bearer <token>

Response:
{
  "message": "Chat deleted successfully"
}
```

## Error Responses

### 1. Authentication Errors
```http
401 Unauthorized
{
  "detail": "Could not validate credentials"
}
```

### 2. Permission Errors
```http
403 Forbidden
{
  "detail": "Guest users can only import 2 chats. Please register for unlimited access."
}
```

### 3. Not Found Errors
```http
404 Not Found
{
  "detail": "Chat not found"
}
```

### 4. Validation Errors
```http
400 Bad Request
{
  "detail": "Email already registered"
}
```

## Authentication

All endpoints except `/auth/login`, `/auth/register`, and `/auth/guest` require a valid JWT token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAi...
```

The token is obtained from the login/register/guest endpoints and should be included in all subsequent requests.

## Rate Limiting

Guest users are limited to:
- 2 chat imports
- 5 messages per chat

Regular users have no limitations.

## Platforms

Supported AI chat platforms:
1. ChatGPT
2. Mistral
3. Gemini
4. Claude (coming soon)
