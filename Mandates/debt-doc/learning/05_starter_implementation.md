# ChatSynth Starter Implementation

This guide provides a minimal but functional implementation of ChatSynth's core features. We'll focus on the essential components that handle chat aggregation and processing.

## 1. Project Setup

### 1.1 Project Structure
```
chatsynth/
├── backend/
│   ├── __init__.py
│   ├── models.py        # Database models
│   ├── store.py         # Message storage
│   ├── processor.py     # Message processing
│   └── platforms/       # Platform handlers
│       ├── __init__.py
│       ├── base.py
│       ├── chatgpt.py
│       └── discord.py
├── frontend/
│   ├── index.html       # Simple web interface
│   └── static/
│       └── main.js      # Frontend logic
└── requirements.txt     # Dependencies
```

### 1.2 Dependencies
```txt
# requirements.txt
fastapi==0.104.1
sqlalchemy==2.0.23
pydantic==2.5.2
uvicorn==0.24.0
python-multipart==0.0.6
aiosqlite==0.19.0
```

## 2. Core Implementation

### 2.1 Database Models
```python
# backend/models.py
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Message(Base):
    """Basic message model."""
    __tablename__ = 'messages'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)

# Create database
def init_db():
    engine = create_engine('sqlite:///chatsynth.db')
    Base.metadata.create_all(engine)
    return engine
```

### 2.2 Message Store
```python
# backend/store.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import List, Optional
from .models import Message

class MessageStore:
    """Handle message storage and retrieval."""
    
    def __init__(self, db_url: str = 'sqlite:///chatsynth.db'):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_message(self, message: Message) -> None:
        """Add a new message."""
        with self.Session() as session:
            session.add(message)
            session.commit()
    
    def get_messages(
        self,
        platform: Optional[str] = None,
        limit: int = 100
    ) -> List[Message]:
        """Get messages with optional platform filter."""
        with self.Session() as session:
            query = session.query(Message)
            if platform:
                query = query.filter(Message.platform == platform)
            return query.order_by(Message.timestamp.desc())\
                       .limit(limit)\
                       .all()
    
    def search_messages(self, keyword: str) -> List[Message]:
        """Search messages for keyword."""
        with self.Session() as session:
            return session.query(Message)\
                         .filter(Message.content.contains(keyword))\
                         .all()
```

### 2.3 Platform Handlers
```python
# backend/platforms/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models import Message

class Platform(ABC):
    """Base platform handler."""
    
    @abstractmethod
    def parse_message(self, raw_data: Dict[str, Any]) -> Message:
        """Convert platform-specific format to our Message model."""
        pass
    
    @abstractmethod
    def format_message(self, message: Message) -> Dict[str, Any]:
        """Convert our Message model to platform-specific format."""
        pass

# backend/platforms/chatgpt.py
from .base import Platform
from ..models import Message
from typing import Dict, Any

class ChatGPTPlatform(Platform):
    """Handle ChatGPT messages."""
    
    def parse_message(self, raw_data: Dict[str, Any]) -> Message:
        return Message(
            content=raw_data['content'],
            sender=raw_data['role'],
            platform='chatgpt',
            metadata={'raw': raw_data}
        )
    
    def format_message(self, message: Message) -> Dict[str, Any]:
        return {
            'role': message.sender,
            'content': message.content
        }

# backend/platforms/discord.py
from .base import Platform
from ..models import Message
from typing import Dict, Any

class DiscordPlatform(Platform):
    """Handle Discord messages."""
    
    def parse_message(self, raw_data: Dict[str, Any]) -> Message:
        return Message(
            content=raw_data['content'],
            sender=raw_data['author']['username'],
            platform='discord',
            metadata={'raw': raw_data}
        )
    
    def format_message(self, message: Message) -> Dict[str, Any]:
        return {
            'content': message.content,
            'author': {
                'username': message.sender
            }
        }
```

### 2.4 Message Processor
```python
# backend/processor.py
from typing import Dict, Any, List
from .models import Message
from .store import MessageStore
from .platforms.base import Platform

class MessageProcessor:
    """Process and analyze messages."""
    
    def __init__(self, store: MessageStore):
        self.store = store
        self.platforms: Dict[str, Platform] = {}
    
    def register_platform(self, name: str, handler: Platform) -> None:
        """Register a platform handler."""
        self.platforms[name] = handler
    
    def process_message(
        self,
        content: str,
        platform: str,
        raw_data: Dict[str, Any]
    ) -> Message:
        """Process a new message."""
        # Get platform handler
        handler = self.platforms.get(platform)
        if not handler:
            raise ValueError(f"Unknown platform: {platform}")
        
        # Parse message
        message = handler.parse_message(raw_data)
        
        # Add analysis
        message.metadata['analysis'] = self._analyze_message(message)
        
        # Store message
        self.store.add_message(message)
        
        return message
    
    def _analyze_message(self, message: Message) -> Dict[str, Any]:
        """Perform basic message analysis."""
        words = message.content.split()
        return {
            'word_count': len(words),
            'char_count': len(message.content),
            'has_question': '?' in message.content,
            'has_code': '```' in message.content
        }
```

## 3. API Implementation

### 3.1 FastAPI Routes
```python
# backend/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from .processor import MessageProcessor
from .store import MessageStore
from .platforms.chatgpt import ChatGPTPlatform
from .platforms.discord import DiscordPlatform

app = FastAPI()

# Initialize components
store = MessageStore()
processor = MessageProcessor(store)

# Register platforms
processor.register_platform('chatgpt', ChatGPTPlatform())
processor.register_platform('discord', DiscordPlatform())

class MessageIn(BaseModel):
    """Input message format."""
    content: str
    platform: str
    raw_data: Dict[str, Any]

class MessageOut(BaseModel):
    """Output message format."""
    id: str
    content: str
    sender: str
    platform: str
    timestamp: str
    analysis: Dict[str, Any]

@app.post("/messages/", response_model=MessageOut)
async def create_message(message: MessageIn):
    """Create a new message."""
    try:
        msg = processor.process_message(
            content=message.content,
            platform=message.platform,
            raw_data=message.raw_data
        )
        
        return MessageOut(
            id=msg.id,
            content=msg.content,
            sender=msg.sender,
            platform=msg.platform,
            timestamp=msg.timestamp.isoformat(),
            analysis=msg.metadata['analysis']
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/messages/", response_model=List[MessageOut])
async def get_messages(platform: str = None, limit: int = 100):
    """Get messages with optional platform filter."""
    messages = store.get_messages(platform=platform, limit=limit)
    return [
        MessageOut(
            id=msg.id,
            content=msg.content,
            sender=msg.sender,
            platform=msg.platform,
            timestamp=msg.timestamp.isoformat(),
            analysis=msg.metadata.get('analysis', {})
        )
        for msg in messages
    ]

@app.get("/search/", response_model=List[MessageOut])
async def search_messages(keyword: str):
    """Search messages."""
    messages = store.search_messages(keyword)
    return [
        MessageOut(
            id=msg.id,
            content=msg.content,
            sender=msg.sender,
            platform=msg.platform,
            timestamp=msg.timestamp.isoformat(),
            analysis=msg.metadata.get('analysis', {})
        )
        for msg in messages
    ]
```

### 3.2 Simple Web Interface
```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>ChatSynth</title>
    <style>
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .messages {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ChatSynth</h1>
        
        <div class="controls">
            <select id="platform">
                <option value="chatgpt">ChatGPT</option>
                <option value="discord">Discord</option>
            </select>
            <input type="text" id="search" placeholder="Search messages...">
            <button onclick="searchMessages()">Search</button>
        </div>
        
        <div class="messages" id="messages"></div>
        
        <div class="input-area">
            <input type="text" id="content" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script src="/static/main.js"></script>
</body>
</html>

<!-- frontend/static/main.js -->
async function sendMessage() {
    const content = document.getElementById('content').value;
    const platform = document.getElementById('platform').value;
    
    if (!content) return;
    
    try {
        const response = await fetch('/messages/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content,
                platform,
                raw_data: {
                    content,
                    role: 'user',
                    author: { username: 'user' }
                }
            })
        });
        
        if (response.ok) {
            document.getElementById('content').value = '';
            loadMessages();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadMessages() {
    try {
        const platform = document.getElementById('platform').value;
        const response = await fetch(`/messages/?platform=${platform}`);
        const messages = await response.json();
        
        displayMessages(messages);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function searchMessages() {
    const keyword = document.getElementById('search').value;
    
    try {
        const response = await fetch(`/search/?keyword=${keyword}`);
        const messages = await response.json();
        
        displayMessages(messages);
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayMessages(messages) {
    const container = document.getElementById('messages');
    container.innerHTML = '';
    
    messages.forEach(msg => {
        const div = document.createElement('div');
        div.className = 'message';
        div.innerHTML = `
            <strong>${msg.sender} (${msg.platform}):</strong>
            <p>${msg.content}</p>
            <small>
                Words: ${msg.analysis.word_count},
                Chars: ${msg.analysis.char_count}
            </small>
        `;
        container.appendChild(div);
    });
    
    container.scrollTop = container.scrollHeight;
}

// Load messages on startup
loadMessages();

// Auto-reload messages every 5 seconds
setInterval(loadMessages, 5000);
```

## 4. Running the Project

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database:**
   ```python
   from backend.models import init_db
   init_db()
   ```

3. **Start the Server:**
   ```bash
   uvicorn backend.api:app --reload
   ```

4. **Open the Web Interface:**
   - Open `frontend/index.html` in a web browser
   - Or serve it using a simple HTTP server:
     ```bash
     python -m http.server
     ```

## 5. Next Steps

1. **Add Features:**
   - User authentication
   - Message threading
   - Real-time updates
   - File attachments
   - Rich text formatting

2. **Improve Analysis:**
   - Sentiment analysis
   - Topic detection
   - Language detection
   - Code highlighting

3. **Enhance UI:**
   - Better styling
   - Message grouping
   - Search filters
   - Platform-specific views

4. **Add Platforms:**
   - More AI platforms
   - Social media
   - Custom sources
   - Import/export tools

Remember:
- Start with the basics
- Add features gradually
- Test thoroughly
- Keep code organized
- Document changes
- Handle errors properly
