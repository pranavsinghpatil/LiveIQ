# ChatSynth Practical Exercises

This guide provides hands-on exercises to help you understand and implement ChatSynth features. Each exercise builds upon previous ones and includes explanations.

## 1. Basic Python Exercises

### Exercise 1: Message Handling
```python
"""
Goal: Learn basic string manipulation and dictionaries
Skills: String operations, dictionary handling, basic functions
"""

# Exercise: Create a function that parses a chat message
def parse_message(raw_message: str) -> dict:
    """
    Convert a raw message string into a structured format
    Example input: "John: Hello, how are you?"
    Expected output: {"sender": "John", "content": "Hello, how are you?"}
    """
    # Your code here
    pass

# Test cases to try:
test_messages = [
    "John: Hello, how are you?",
    "Mary: I'm doing great!",
    "Invalid message"
]

# Solution explanation:
"""
1. Split the message on first ':' using split(':', 1)
2. Check if split was successful
3. Create dictionary with sender and content
4. Handle error cases
"""

# Example solution:
def parse_message_solution(raw_message: str) -> dict:
    try:
        sender, content = raw_message.split(':', 1)
        return {
            'sender': sender.strip(),
            'content': content.strip()
        }
    except ValueError:
        return {
            'sender': 'unknown',
            'content': raw_message
        }
```

### Exercise 2: Message Storage
```python
"""
Goal: Learn list operations and basic classes
Skills: Classes, lists, methods, basic error handling
"""

# Exercise: Create a class to store chat messages
class MessageStore:
    """
    Store and manage chat messages
    Features needed:
    - Add messages
    - Get all messages
    - Get messages by sender
    """
    def __init__(self):
        # Initialize your storage
        pass
    
    def add_message(self, message: dict):
        # Add a message to storage
        pass
    
    def get_messages(self):
        # Return all messages
        pass
    
    def get_by_sender(self, sender: str):
        # Return messages from a specific sender
        pass

# Solution explanation:
"""
1. Use a list to store messages
2. add_message: append to list
3. get_messages: return full list
4. get_by_sender: use list comprehension
"""

# Example solution:
class MessageStore_Solution:
    def __init__(self):
        self.messages = []
    
    def add_message(self, message: dict):
        if not isinstance(message, dict):
            raise ValueError("Message must be a dictionary")
        self.messages.append(message)
    
    def get_messages(self):
        return self.messages
    
    def get_by_sender(self, sender: str):
        return [
            msg for msg in self.messages 
            if msg['sender'] == sender
        ]
```

## 2. Intermediate Exercises

### Exercise 1: Message Processing
```python
"""
Goal: Learn text processing and analysis
Skills: String methods, regular expressions, data structures
"""

# Exercise: Create a message analyzer
class MessageAnalyzer:
    """
    Analyze chat messages for:
    - Word count
    - Character count
    - Most common words
    - Question detection
    """
    def analyze(self, message: str) -> dict:
        # Your code here
        pass

# Test cases:
test_messages = [
    "Hello, how are you doing today?",
    "I'm doing great! Thanks for asking.",
    "This is a test message with some repeated words. Test test test!"
]

# Solution explanation:
"""
1. Split message into words
2. Count words and characters
3. Create word frequency dictionary
4. Check for question marks
"""

# Example solution:
from collections import Counter

class MessageAnalyzer_Solution:
    def analyze(self, message: str) -> dict:
        words = message.lower().split()
        word_freq = Counter(words)
        
        return {
            'word_count': len(words),
            'char_count': len(message),
            'common_words': word_freq.most_common(3),
            'is_question': '?' in message
        }
```

### Exercise 2: Chat Platform Integration
```python
"""
Goal: Learn about different chat formats
Skills: Inheritance, polymorphism, format handling
"""

# Exercise: Create platform-specific message handlers
class ChatPlatform:
    """
    Base class for chat platforms
    Each platform has different message formats
    """
    def format_message(self, message: dict) -> str:
        # Convert message dict to platform format
        pass
    
    def parse_message(self, raw_message: str) -> dict:
        # Convert platform format to message dict
        pass

# Example platforms to implement:
class DiscordChat(ChatPlatform):
    pass

class SlackChat(ChatPlatform):
    pass

# Solution explanation:
"""
1. Create base class with common methods
2. Override methods for each platform
3. Handle platform-specific formats
4. Maintain consistent internal format
"""

# Example solution:
class ChatPlatform_Solution:
    def format_message(self, message: dict) -> str:
        return f"{message['sender']}: {message['content']}"
    
    def parse_message(self, raw_message: str) -> dict:
        return parse_message_solution(raw_message)

class DiscordChat_Solution(ChatPlatform_Solution):
    def format_message(self, message: dict) -> str:
        return f"**{message['sender']}** {message['content']}"
```

## 3. Advanced Exercises

### Exercise 1: Database Integration
```python
"""
Goal: Learn database operations
Skills: SQLAlchemy, database design, CRUD operations
"""

# Exercise: Create database models and operations
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    """
    Database model for messages
    Include:
    - ID
    - Sender
    - Content
    - Timestamp
    - Platform
    """
    __tablename__ = 'messages'
    
    # Define your columns here

# Solution explanation:
"""
1. Create SQLAlchemy models
2. Define relationships
3. Implement CRUD operations
4. Handle database connections
"""

# Example solution:
class Message_Solution(Base):
    __tablename__ = 'messages'
    
    id = Column(String, primary_key=True)
    sender = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    platform = Column(String)
```

### Exercise 2: Real-time Chat
```python
"""
Goal: Learn WebSocket implementation
Skills: FastAPI, WebSocket, async/await
"""

# Exercise: Implement real-time chat server
from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

class ChatServer:
    """
    WebSocket chat server
    Features:
    - Connect clients
    - Broadcast messages
    - Handle disconnections
    """
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        # Handle new connection
        pass
    
    async def broadcast(self, message: str):
        # Send message to all clients
        pass

# Solution explanation:
"""
1. Manage WebSocket connections
2. Handle connection lifecycle
3. Implement message broadcasting
4. Handle errors and disconnections
"""

# Example solution:
class ChatServer_Solution:
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.connections:
            try:
                await connection.send_text(message)
            except:
                self.connections.remove(connection)
```

## Practice Projects

### Project 1: Simple Chat Client
```python
"""
Build a command-line chat client that can:
1. Send/receive messages
2. Store message history
3. Show online users
4. Support basic commands
"""

# Start with this structure:
class ChatClient:
    def __init__(self, username: str):
        self.username = username
        self.messages = []
        self.online_users = set()
    
    def run(self):
        """Main client loop"""
        while True:
            command = input("> ")
            if command == "/quit":
                break
            self.handle_command(command)
    
    def handle_command(self, command: str):
        """Handle user commands"""
        # Implement command handling
        pass

# Extend with features like:
# - Message formatting
# - Command history
# - Tab completion
# - Color output
```

### Project 2: Chat Bot
```python
"""
Create a simple chat bot that can:
1. Respond to basic commands
2. Remember context
3. Handle different message types
4. Integrate with your chat system
"""

class ChatBot:
    def __init__(self, name: str):
        self.name = name
        self.context = {}
        self.commands = {
            'help': self.show_help,
            'echo': self.echo_message,
            # Add more commands
        }
    
    def process_message(self, message: str) -> str:
        """Process incoming messages"""
        if message.startswith('/'):
            return self.handle_command(message[1:])
        return self.generate_response(message)
    
    def generate_response(self, message: str) -> str:
        """Generate a response based on message"""
        # Implement response generation
        pass

# Add features like:
# - Natural language processing
# - Pattern matching
# - State management
# - Learning capabilities
```

## Learning Tips

1. **Start Small**
   - Begin with basic functionality
   - Add features incrementally
   - Test each addition thoroughly

2. **Debug Effectively**
   - Use print statements strategically
   - Check variable values
   - Read error messages carefully

3. **Practice Regularly**
   - Set aside coding time daily
   - Complete one exercise at a time
   - Review and improve solutions

4. **Build Projects**
   - Start with command-line tools
   - Add features gradually
   - Focus on code organization

## Next Steps

1. **Basic Skills**
   - Complete all basic exercises
   - Understand each solution
   - Try variations of exercises

2. **Intermediate Skills**
   - Implement platform handlers
   - Add more analysis features
   - Create custom chat formats

3. **Advanced Features**
   - Add database storage
   - Implement real-time chat
   - Create a web interface

Remember:
- Take your time with each exercise
- Make sure you understand before moving on
- Practice typing out the code
- Experiment with modifications
- Ask questions when stuck
