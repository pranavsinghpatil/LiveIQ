# VoxStitch API Reference

## Authentication

### POST /api/auth/login
Login with email and password.

```typescript
Request:
{
  "email": string,
  "password": string
}

Response:
{
  "token": string,
  "user": {
    "id": string,
    "email": string,
    "name": string,
    "is_guest": boolean,
    "guest_imports_remaining": number | null,
    "guest_messages_remaining": number | null
  }
}
```

### POST /api/auth/register
Register a new user.

```typescript
Request:
{
  "email": string,
  "password": string,
  "name": string
}

Response:
{
  "token": string,
  "user": {
    "id": string,
    "email": string,
    "name": string,
    "is_guest": false
  }
}
```

### POST /api/auth/guest
Create guest session.

```typescript
Request: {}

Response:
{
  "token": string,
  "user": {
    "id": string,
    "email": string,
    "name": "Guest User",
    "is_guest": true,
    "guest_imports_remaining": 2,
    "guest_messages_remaining": 5
  }
}
```

### GET /api/auth/{provider}/url
Get OAuth URL for social login.

```typescript
Parameters:
- provider: "google" | "github" | "apple"

Response:
{
  "url": string
}
```

### POST /api/auth/{provider}/callback
Handle OAuth callback.

```typescript
Parameters:
- provider: "google" | "github" | "apple"

Request:
{
  "code": string,
  "state": string
}

Response:
{
  "token": string,
  "user": {
    "id": string,
    "email": string,
    "name": string,
    "is_guest": false
  }
}
```

## Chat Management

### POST /api/chats/import
Import a new chat.

```typescript
Request:
{
  "platform": string,
  "title": string,
  "messages": Array<{
    "sender": string,
    "content": string,
    "timestamp": string
  }>,
  "media_files": Array<File> | null
}

Response:
{
  "id": string,
  "title": string,
  "platform": string,
  "created_at": string,
  "updated_at": string,
  "message_count": number,
  "participants": string[],
  "has_media": boolean,
  "tags": string[]
}
```

### GET /api/chats/{chat_id}
Get chat by ID.

```typescript
Parameters:
- chat_id: string

Response:
{
  "processed_chat": {
    "id": string,
    "title": string,
    "platform": string,
    "summary": string,
    "topics": string[],
    "sentiment": {
      "overall_sentiment": string,
      "confidence_score": number
    },
    "key_insights": string[],
    "metadata": {
      "message_count": number,
      "participants": string[],
      "duration": number | null
    }
  },
  "media_content": Array<{
    "id": string,
    "type": string,
    "content": object,
    "file_url": string,
    "created_at": string
  }>,
  "metadata": {
    "id": string,
    "title": string,
    "platform": string,
    "created_at": string,
    "updated_at": string,
    "message_count": number,
    "participants": string[],
    "has_media": boolean,
    "tags": string[]
  }
}
```

### GET /api/chats
Search chats.

```typescript
Query Parameters:
- query: string | null
- platform: string | null
- start_date: string | null
- end_date: string | null
- tags: string[] | null
- page: number (default: 1)
- page_size: number (default: 10)

Response:
{
  "chats": Array<{
    "id": string,
    "title": string,
    "platform": string,
    "created_at": string,
    "updated_at": string,
    "message_count": number,
    "participants": string[],
    "has_media": boolean,
    "tags": string[]
  }>,
  "total": number,
  "page": number,
  "page_size": number
}
```

### PATCH /api/chats/{chat_id}
Update chat metadata.

```typescript
Parameters:
- chat_id: string

Request:
{
  "title": string | null,
  "tags": string[] | null
}

Response:
{
  "id": string,
  "title": string,
  "platform": string,
  "created_at": string,
  "updated_at": string,
  "message_count": number,
  "participants": string[],
  "has_media": boolean,
  "tags": string[]
}
```

### DELETE /api/chats/{chat_id}
Delete chat.

```typescript
Parameters:
- chat_id: string

Response:
{
  "success": true
}
```

## Media Processing

### POST /api/media/upload
Upload and process media file.

```typescript
Request:
- FormData with file

Response:
{
  "id": string,
  "type": string,
  "content": {
    // Content varies based on media type
    "transcript": string | null,
    "segments": object[] | null,
    "visual_analysis": object | null,
    "text": string | null
  },
  "file_url": string,
  "created_at": string
}
```

### GET /api/media/{media_id}
Get media file URL.

```typescript
Parameters:
- media_id: string

Response:
{
  "url": string,
  "expires_at": string
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```typescript
{
  "detail": string
}
```

### 401 Unauthorized
```typescript
{
  "detail": "Invalid token" | "Token has expired" | "Token has been revoked"
}
```

### 403 Forbidden
```typescript
{
  "detail": "Guest import limit reached" | "Guest message limit reached"
}
```

### 404 Not Found
```typescript
{
  "detail": string
}
```

### 429 Too Many Requests
```typescript
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```typescript
{
  "detail": "Internal server error"
}
```
