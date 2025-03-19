# ChatSynth Step-by-Step Tutorial

This tutorial breaks down ChatSynth's implementation into small, manageable steps. Each step builds on the previous one, helping you understand the system piece by piece.

## Step 1: Basic Message Handling

### 1.1 Create a Message Class
```python
# file: message.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class Message:
    """Basic message structure."""
    content: str
    sender: str
    platform: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

# Try it out:
message = Message(
    content="Hello, world!",
    sender="User",
    platform="tutorial"
)
print(f"{message.sender}: {message.content}")
```

### 1.2 Add Message Validation
```python
# Add to message.py
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class Message:
    content: str
    sender: str
    platform: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate message after initialization."""
        if not self.content.strip():
            raise ValueError("Message content cannot be empty")
        if len(self.content) > 1000:
            raise ValueError("Message too long (max 1000 chars)")
        if not self.sender.strip():
            raise ValueError("Sender cannot be empty")

# Try it:
try:
    invalid_message = Message("", "User", "tutorial")
except ValueError as e:
    print(f"Error: {e}")
```

## Step 2: Message Storage

### 2.1 Create an In-Memory Store
```python
# file: store.py
from typing import List, Dict, Optional
from message import Message

class MessageStore:
    """Store messages in memory."""
    
    def __init__(self):
        self.messages: List[Message] = []
        self.by_platform: Dict[str, List[Message]] = {}
        self.by_sender: Dict[str, List[Message]] = []
    
    def add(self, message: Message) -> None:
        """Add a message to the store."""
        # Add to main list
        self.messages.append(message)
        
        # Add to platform index
        if message.platform not in self.by_platform:
            self.by_platform[message.platform] = []
        self.by_platform[message.platform].append(message)
        
        # Add to sender index
        if message.sender not in self.by_sender:
            self.by_sender[message.sender] = []
        self.by_sender[message.sender].append(message)
    
    def get_by_platform(self, platform: str) -> List[Message]:
        """Get all messages from a platform."""
        return self.by_platform.get(platform, [])
    
    def get_by_sender(self, sender: str) -> List[Message]:
        """Get all messages from a sender."""
        return self.by_sender.get(sender, [])

# Try it:
store = MessageStore()
store.add(Message("Hello!", "Alice", "tutorial"))
store.add(Message("Hi!", "Bob", "tutorial"))
print(f"Messages from Alice: {len(store.get_by_sender('Alice'))}")
```

## Step 3: Basic Chat Processing

### 3.1 Create a Message Processor
```python
# file: processor.py
from typing import Dict, Any, List
from message import Message
from store import MessageStore

class MessageProcessor:
    """Process and analyze messages."""
    
    def __init__(self):
        self.store = MessageStore()
    
    def process(self, message: Message) -> Dict[str, Any]:
        """Process a single message."""
        # Basic analysis
        analysis = self._analyze_message(message)
        
        # Add analysis to metadata
        message.metadata['analysis'] = analysis
        
        # Store message
        self.store.add(message)
        
        return analysis
    
    def _analyze_message(self, message: Message) -> Dict[str, Any]:
        """Analyze message content."""
        words = message.content.split()
        
        return {
            'word_count': len(words),
            'char_count': len(message.content),
            'has_question': '?' in message.content,
            'has_exclamation': '!' in message.content
        }

# Try it:
processor = MessageProcessor()
result = processor.process(
    Message("How are you today?", "Alice", "tutorial")
)
print(f"Analysis: {result}")
```

## Step 4: Platform Integration

### 4.1 Create Platform Handlers
```python
# file: platforms.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from message import Message

class Platform(ABC):
    """Base class for chat platforms."""
    
    @abstractmethod
    def format_message(self, message: Message) -> str:
        """Format message for platform."""
        pass
    
    @abstractmethod
    def parse_message(self, raw: Dict[str, Any]) -> Message:
        """Parse platform message into our format."""
        pass

class ChatGPTPlatform(Platform):
    """Handler for ChatGPT messages."""
    
    def format_message(self, message: Message) -> str:
        return f"{message.sender}: {message.content}"
    
    def parse_message(self, raw: Dict[str, Any]) -> Message:
        return Message(
            content=raw['content'],
            sender=raw['role'],
            platform='chatgpt',
            metadata={'raw': raw}
        )

class DiscordPlatform(Platform):
    """Handler for Discord messages."""
    
    def format_message(self, message: Message) -> str:
        return f"**{message.sender}**: {message.content}"
    
    def parse_message(self, raw: Dict[str, Any]) -> Message:
        return Message(
            content=raw['content'],
            sender=raw['author']['name'],
            platform='discord',
            metadata={'raw': raw}
        )

# Try it:
chatgpt = ChatGPTPlatform()
msg = Message("Hello!", "user", "chatgpt")
print(f"ChatGPT format: {chatgpt.format_message(msg)}")

discord = DiscordPlatform()
print(f"Discord format: {discord.format_message(msg)}")
```

## Step 5: Database Integration

### 5.1 Set Up Database Models
```python
# file: models.py
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MessageModel(Base):
    """Database model for messages."""
    __tablename__ = 'messages'
    
    id = Column(String, primary_key=True)
    content = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)

# Create tables:
engine = create_engine('sqlite:///chat.db')
Base.metadata.create_all(engine)
```

### 5.2 Create Database Store
```python
# file: db_store.py
from sqlalchemy.orm import sessionmaker
from models import MessageModel
from message import Message
import uuid

class DatabaseStore:
    """Store messages in database."""
    
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)
    
    def add(self, message: Message) -> None:
        """Add message to database."""
        with self.Session() as session:
            db_message = MessageModel(
                id=str(uuid.uuid4()),
                content=message.content,
                sender=message.sender,
                platform=message.platform,
                timestamp=message.timestamp,
                metadata=message.metadata
            )
            session.add(db_message)
            session.commit()
    
    def get_by_platform(self, platform: str) -> List[Message]:
        """Get messages from platform."""
        with self.Session() as session:
            db_messages = session.query(MessageModel)\
                .filter_by(platform=platform)\
                .all()
            
            return [
                Message(
                    content=m.content,
                    sender=m.sender,
                    platform=m.platform,
                    timestamp=m.timestamp,
                    metadata=m.metadata
                )
                for m in db_messages
            ]

# Try it:
from sqlalchemy import create_engine
engine = create_engine('sqlite:///chat.db')
db_store = DatabaseStore(engine)
db_store.add(Message("Hello from DB!", "User", "tutorial"))
```

## Step 6: API Implementation

### 6.1 Create FastAPI Routes
```python
# file: api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from message import Message
from processor import MessageProcessor

app = FastAPI()
processor = MessageProcessor()

class MessageIn(BaseModel):
    """Input message format."""
    content: str
    sender: str
    platform: str

class MessageOut(BaseModel):
    """Output message format."""
    content: str
    sender: str
    platform: str
    timestamp: str
    analysis: dict

@app.post("/messages/", response_model=MessageOut)
async def create_message(message: MessageIn):
    """Create a new message."""
    try:
        msg = Message(
            content=message.content,
            sender=message.sender,
            platform=message.platform
        )
        analysis = processor.process(msg)
        
        return MessageOut(
            content=msg.content,
            sender=msg.sender,
            platform=msg.platform,
            timestamp=msg.timestamp.isoformat(),
            analysis=analysis
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/messages/{platform}", response_model=List[MessageOut])
async def get_messages(platform: str):
    """Get messages from a platform."""
    messages = processor.store.get_by_platform(platform)
    return [
        MessageOut(
            content=msg.content,
            sender=msg.sender,
            platform=msg.platform,
            timestamp=msg.timestamp.isoformat(),
            analysis=msg.metadata.get('analysis', {})
        )
        for msg in messages
    ]

# Run with: uvicorn api:app --reload
```

## Step 7: Adding Real-time Features

### 7.1 Implement WebSocket Chat
```python
# file: realtime.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from message import Message
from processor import MessageProcessor

app = FastAPI()
processor = MessageProcessor()

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Handle new connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        """Handle disconnection."""
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        """Send message to all connections."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                await self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """Handle WebSocket connection."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Process message
            message = Message(
                content=data,
                sender=client_id,
                platform="websocket"
            )
            processor.process(message)
            
            # Broadcast to all clients
            await manager.broadcast(
                f"{message.sender}: {message.content}"
            )
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

# Run with: uvicorn realtime:app --reload
```

## Step 8: Adding a Simple Frontend

### 8.1 Create HTML Interface
```html
<!-- file: index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>ChatSynth</title>
    <style>
        #messages {
            height: 300px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div id="messages"></div>
    <input type="text" id="messageInput" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        const clientId = Math.random().toString(36).substr(2, 9);
        const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
        const messages = document.getElementById('messages');
        const input = document.getElementById('messageInput');

        ws.onmessage = function(event) {
            const message = document.createElement('div');
            message.textContent = event.data;
            messages.appendChild(message);
            messages.scrollTop = messages.scrollHeight;
        };

        function sendMessage() {
            if (input.value) {
                ws.send(input.value);
                input.value = '';
            }
        }

        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```

## Practice Exercises

1. **Message Features**
   - Add message threading
   - Implement message editing
   - Add message reactions
   - Create message categories

2. **Platform Integration**
   - Add more platforms
   - Implement format conversion
   - Add platform-specific features
   - Create import/export tools

3. **Analysis Features**
   - Add sentiment analysis
   - Implement topic detection
   - Create message summaries
   - Add language detection

4. **UI Improvements**
   - Add user authentication
   - Implement file sharing
   - Add message search
   - Create chat rooms

## Next Steps

1. **Study the Code**
   - Read through each component
   - Understand the relationships
   - Try the examples
   - Make small changes

2. **Build Features**
   - Start with message handling
   - Add storage capabilities
   - Implement real-time chat
   - Create the user interface

3. **Extend the System**
   - Add more platforms
   - Improve message processing
   - Enhance the user interface
   - Add advanced features

Remember:
- Take it step by step
- Test each component
- Handle errors properly
- Keep the code organized
- Document your changes
- Ask for help when needed
