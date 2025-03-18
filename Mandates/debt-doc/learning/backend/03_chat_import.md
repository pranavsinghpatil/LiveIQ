# Understanding Chat Import System

## What is Chat Import?

The chat import system is how ChatSynth takes conversations from different AI platforms (like ChatGPT, Mistral, or Gemini) and stores them in our system. Think of it like a universal translator that can understand different chat formats.

## Basic Concepts

### 1. Chat Data Structure
First, let's understand how we store chats:

```python
# In models.py - Our chat data model
class ChatLog(Base):
    """Database model for storing chat logs
    
    This model stores:
    1. The chat content from any platform
    2. Where the chat came from (source)
    3. Who owns the chat (user_id)
    4. Extra information about the chat (metadata)
    
    Example chat content:
    {
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
    }
    """
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source = Column(String(50))  # chatgpt, mistral, etc.
    content = Column(JSONB)      # The actual chat data
    metadata = Column(JSONB)     # Extra information
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Let's break down each field:
    # 1. user_id: Who owns this chat
    # 2. source: Which AI platform it's from
    # 3. content: The actual chat messages
    # 4. metadata: Things like chat title, tags, etc.

# In schemas.py - How we accept chat data
class ChatImport(BaseModel):
    """Schema for importing a chat
    
    This defines what data we need when someone
    wants to import a chat into our system.
    """
    content: str      # The chat content
    source: str      # Which platform it's from
    metadata: Optional[dict] = None  # Optional extra info
    
    @validator("source")
    def validate_source(cls, v):
        """Make sure we support this chat platform
        
        Args:
            v: The source platform name
            
        Returns:
            The validated source name
            
        Raises:
            ValueError if source is not supported
        """
        valid_sources = ["chatgpt", "mistral", "gemini"]
        if v not in valid_sources:
            raise ValueError(f"Invalid source. Must be one of: {valid_sources}")
        return v
```

### 2. Platform-Specific Importers
We use different importers for each platform because they all format their chats differently:

```python
# In importers/base.py - Base importer class
class ChatImporter(ABC):
    """Base class for all chat importers
    
    Each platform (ChatGPT, Mistral, etc.) will have its
    own importer that inherits from this class.
    """
    @abstractmethod
    async def import_chat(self, content: str) -> dict:
        """Convert platform-specific chat to our format
        
        Args:
            content: Raw chat content from the platform
            
        Returns:
            Dict with standardized chat format
        """
        pass
    
    @abstractmethod
    def validate_format(self, content: str) -> bool:
        """Check if content matches this platform's format
        
        Args:
            content: Raw chat content to check
            
        Returns:
            True if content matches this platform's format
        """
        pass

# In importers/chatgpt.py - ChatGPT specific importer
class ChatGPTImporter(ChatImporter):
    """Handles importing chats from ChatGPT
    
    ChatGPT format looks like:
    {
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"}
        ]
    }
    """
    async def import_chat(self, content: str) -> dict:
        # 1. Parse the JSON content
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        # 2. Validate structure
        if "messages" not in data:
            raise ValueError("No messages found in chat")
            
        # 3. Convert to our format
        messages = []
        for msg in data["messages"]:
            if "role" not in msg or "content" not in msg:
                raise ValueError("Invalid message format")
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
            
        return {
            "messages": messages,
            "platform_data": {
                "type": "chatgpt",
                "version": "1.0"
            }
        }
    
    def validate_format(self, content: str) -> bool:
        try:
            data = json.loads(content)
            return (
                isinstance(data, dict) and
                "messages" in data and
                isinstance(data["messages"], list) and
                all(
                    isinstance(m, dict) and
                    "role" in m and
                    "content" in m
                    for m in data["messages"]
                )
            )
        except:
            return False

# In importers/mistral.py - Mistral specific importer
class MistralImporter(ChatImporter):
    """Handles importing chats from Mistral
    
    Mistral format looks like:
    {
        "conversation": {
            "messages": [
                {"from": "human", "text": "Hello"},
                {"from": "assistant", "text": "Hi!"}
            ]
        }
    }
    """
    async def import_chat(self, content: str) -> dict:
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
            
        if not isinstance(data, dict) or "conversation" not in data:
            raise ValueError("Invalid Mistral chat format")
            
        conv = data["conversation"]
        if "messages" not in conv:
            raise ValueError("No messages found in chat")
            
        # Convert Mistral format to our format
        messages = []
        for msg in conv["messages"]:
            if "from" not in msg or "text" not in msg:
                raise ValueError("Invalid message format")
                
            # Convert Mistral roles to our format
            role = "user" if msg["from"] == "human" else "assistant"
            messages.append({
                "role": role,
                "content": msg["text"]
            })
            
        return {
            "messages": messages,
            "platform_data": {
                "type": "mistral",
                "version": "1.0"
            }
        }
```

### 3. Import Service
This brings everything together:

```python
# In services/chat_import.py
class ChatImportService:
    """Handles the entire chat import process
    
    This service:
    1. Figures out which importer to use
    2. Validates the chat data
    3. Saves it to our database
    """
    def __init__(self):
        self.importers = {
            "chatgpt": ChatGPTImporter(),
            "mistral": MistralImporter(),
            "gemini": GeminiImporter()
        }
    
    async def import_chat(
        self,
        content: str,
        source: str,
        user_id: int,
        db: Session
    ) -> ChatLog:
        """Import a chat from any supported platform
        
        Args:
            content: The raw chat content
            source: Which platform it's from
            user_id: Who's importing the chat
            db: Database session
            
        Returns:
            The imported ChatLog
            
        Raises:
            ValueError: If import fails
        """
        # 1. Get the right importer
        importer = self.importers.get(source)
        if not importer:
            raise ValueError(f"Unsupported platform: {source}")
        
        # 2. Validate the format
        if not importer.validate_format(content):
            raise ValueError(f"Invalid {source} chat format")
        
        try:
            # 3. Convert to our format
            chat_data = await importer.import_chat(content)
            
            # 4. Create chat log
            chat_log = ChatLog(
                user_id=user_id,
                source=source,
                content=chat_data,
                metadata={
                    "imported_at": datetime.utcnow().isoformat(),
                    "original_source": source
                }
            )
            
            # 5. Save to database
            db.add(chat_log)
            db.commit()
            db.refresh(chat_log)
            
            return chat_log
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Import failed: {str(e)}")
```

### 4. API Endpoint
Finally, let's see how users can import chats:

```python
# In routes/chat.py
@app.post("/chats/import")
async def import_chat(
    chat_data: ChatImport,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    import_service: ChatImportService = Depends(get_import_service)
):
    """Import a chat from any supported platform
    
    Example request:
    POST /chats/import
    {
        "content": "{\"messages\": [...]}",
        "source": "chatgpt"
    }
    """
    try:
        # Import the chat
        chat_log = await import_service.import_chat(
            content=chat_data.content,
            source=chat_data.source,
            user_id=current_user.id,
            db=db
        )
        
        # Return success response
        return {
            "message": "Chat imported successfully",
            "chat_id": chat_log.id
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to import chat"
        )
```

## Practice Exercise

Try to create a new importer for another AI platform:
1. Create a new importer class
2. Handle the platform's specific format
3. Convert it to our standard format

Here's a starter template:
```python
class CustomImporter(ChatImporter):
    async def import_chat(self, content: str) -> dict:
        # Your code here
        pass
    
    def validate_format(self, content: str) -> bool:
        # Your code here
        pass
```

## Next Steps
1. Try the practice exercise
2. Learn about chat processing
3. Study error handling
4. Explore chat export features
