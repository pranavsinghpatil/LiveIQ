# Chat Import Service

## Purpose
The Chat Import Service handles the processing, validation, and storage of chat conversations from various AI platforms into VoxStitch's unified format.

## Core Features

### Chat Import Handler
```python
class ChatImportService:
    def __init__(self, db: Session):
        self.db = db
        self.parsers = {
            "chatgpt": ChatGPTParser(),
            "mistral": MistralParser(),
            "gemini": GeminiParser(),
            "claude": ClaudeParser(),
        }

    async def import_chat(
        self,
        file: UploadFile,
        platform: str,
        user: User
    ) -> Chat:
        # Validate user limits
        if user.is_guest and user.remaining_imports <= 0:
            raise GuestLimitError()

        # Process the chat
        content = await self._process_file(file, platform)
        chat = await self._save_chat(content, platform, user)

        # Update user limits if guest
        if user.is_guest:
            await self._update_guest_limits(user)

        return chat
```

### File Processing

#### Content Validation
```python
async def _process_file(
    self,
    file: UploadFile,
    platform: str
) -> dict:
    # Validate file type
    if not self._is_valid_file_type(file):
        raise InvalidFileError()

    # Read file content
    content = await file.read()
    
    # Parse based on platform
    parser = self.parsers.get(platform)
    if not parser:
        raise UnsupportedPlatformError()

    return await parser.parse(content)
```

#### Platform-Specific Parsers
```python
class ChatGPTParser:
    async def parse(self, content: bytes) -> dict:
        data = json.loads(content)
        return {
            "messages": self._extract_messages(data),
            "metadata": self._extract_metadata(data),
            "platform_data": self._extract_platform_data(data)
        }

class MistralParser:
    async def parse(self, content: bytes) -> dict:
        # Similar structure but with Mistral-specific parsing
        pass
```

### Database Operations

#### Chat Storage
```python
async def _save_chat(
    self,
    content: dict,
    platform: str,
    user: User
) -> Chat:
    chat = Chat(
        user_id=user.id,
        platform=platform,
        content=content,
        created_at=datetime.utcnow()
    )
    self.db.add(chat)
    await self.db.commit()
    await self.db.refresh(chat)
    return chat
```

#### Guest Limit Management
```python
async def _update_guest_limits(self, user: User):
    user.remaining_imports -= 1
    self.db.add(user)
    await self.db.commit()
    await self.db.refresh(user)
```

## Data Processing Features

### Message Extraction
```python
def _extract_messages(self, data: dict) -> List[Message]:
    return [
        Message(
            role=msg["role"],
            content=msg["content"],
            timestamp=msg.get("timestamp"),
            metadata=msg.get("metadata", {})
        )
        for msg in data["messages"]
    ]
```

### Metadata Processing
```python
def _extract_metadata(self, data: dict) -> dict:
    return {
        "title": data.get("title"),
        "created_at": data.get("created_at"),
        "model": data.get("model"),
        "tags": data.get("tags", []),
        "platform_version": data.get("version")
    }
```

## Error Handling

### Custom Exceptions
```python
class ChatImportError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidFileError(ChatImportError):
    def __init__(self):
        super().__init__("Invalid file format")

class UnsupportedPlatformError(ChatImportError):
    def __init__(self):
        super().__init__("Unsupported chat platform")
```

### Error Processing
```python
def _handle_import_error(self, error: Exception) -> None:
    if isinstance(error, json.JSONDecodeError):
        raise InvalidFileError()
    if isinstance(error, KeyError):
        raise ChatImportError("Missing required data")
    raise error
```

## File Type Validation

### MIME Type Checking
```python
def _is_valid_file_type(self, file: UploadFile) -> bool:
    valid_types = [
        "application/json",
        "text/plain",
        "text/markdown"
    ]
    return file.content_type in valid_types
```

### File Size Validation
```python
async def _validate_file_size(
    self,
    file: UploadFile,
    max_size: int = 10 * 1024 * 1024  # 10MB
) -> None:
    content = await file.read()
    if len(content) > max_size:
        raise FileTooLargeError()
    await file.seek(0)
```

## Content Sanitization

### HTML Sanitization
```python
def _sanitize_content(self, content: str) -> str:
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
```

### Data Normalization
```python
def _normalize_timestamps(self, data: dict) -> dict:
    for message in data["messages"]:
        if "timestamp" in message:
            message["timestamp"] = parse_datetime(
                message["timestamp"]
            ).isoformat()
    return data
```

## Performance Optimizations

### Batch Processing
```python
async def import_multiple_chats(
    self,
    files: List[UploadFile],
    platform: str,
    user: User
) -> List[Chat]:
    chats = []
    for file in files:
        chat = await self.import_chat(file, platform, user)
        chats.append(chat)
    return chats
```

### Caching
```python
@cached(ttl=3600)
async def get_platform_config(self, platform: str) -> dict:
    return await self._load_platform_config(platform)
```

## Related Components
- `models/chat.py`: Chat data models
- `schemas/chat.py`: Pydantic schemas
- `api/chat.py`: API endpoints
- `utils/parsers.py`: Platform-specific parsers

## Recent Updates
- Added support for new platforms
- Improved error handling
- Enhanced content sanitization
- Added batch processing
- Optimized file handling
