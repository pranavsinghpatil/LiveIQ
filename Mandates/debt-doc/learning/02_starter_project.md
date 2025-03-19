# ChatSynth Starter Project

This guide walks you through building a simple but functional chat message processor. We'll start with the basics and gradually add features.

## Part 1: Basic Message Handler

### Step 1: Create a Simple Message Class
```python
# file: chat_message.py

from datetime import datetime
from typing import Optional, Dict, Any

class ChatMessage:
    """A simple chat message class to get started."""
    
    def __init__(
        self,
        content: str,
        sender: str,
        platform: str = "unknown"
    ):
        self.content = content
        self.sender = sender
        self.platform = platform
        self.timestamp = datetime.now()
        self.metadata: Dict[str, Any] = {}
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the message."""
        self.metadata[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format."""
        return {
            "content": self.content,
            "sender": self.sender,
            "platform": self.platform,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    def __str__(self) -> str:
        """String representation of the message."""
        return f"[{self.timestamp}] {self.sender}: {self.content}"

# Test the class
def test_chat_message():
    # Create a message
    msg = ChatMessage(
        content="Hello, world!",
        sender="John",
        platform="test"
    )
    
    # Add some metadata
    msg.add_metadata("language", "en")
    
    # Print the message
    print(msg)
    print("As dictionary:", msg.to_dict())

if __name__ == "__main__":
    test_chat_message()
```

### Step 2: Create a Message Store
```python
# file: message_store.py

from typing import List, Dict, Optional
from chat_message import ChatMessage

class MessageStore:
    """Simple in-memory store for chat messages."""
    
    def __init__(self):
        self.messages: List[ChatMessage] = []
        self.platforms: Dict[str, List[ChatMessage]] = {}
    
    def add_message(self, message: ChatMessage) -> None:
        """Add a message to the store."""
        # Add to main list
        self.messages.append(message)
        
        # Add to platform-specific list
        if message.platform not in self.platforms:
            self.platforms[message.platform] = []
        self.platforms[message.platform].append(message)
    
    def get_messages(
        self,
        platform: Optional[str] = None,
        limit: int = 10
    ) -> List[ChatMessage]:
        """Get messages, optionally filtered by platform."""
        if platform:
            messages = self.platforms.get(platform, [])
        else:
            messages = self.messages
        
        return messages[-limit:]
    
    def search_messages(self, keyword: str) -> List[ChatMessage]:
        """Search messages for a keyword."""
        return [
            msg for msg in self.messages
            if keyword.lower() in msg.content.lower()
        ]

# Test the store
def test_message_store():
    # Create store
    store = MessageStore()
    
    # Add some messages
    messages = [
        ChatMessage("Hello from ChatGPT", "AI", "chatgpt"),
        ChatMessage("Hi from Claude", "AI", "claude"),
        ChatMessage("Hey from user", "User", "chatgpt")
    ]
    
    for msg in messages:
        store.add_message(msg)
    
    # Test retrieval
    print("\nAll messages:")
    for msg in store.get_messages():
        print(msg)
    
    print("\nChatGPT messages:")
    for msg in store.get_messages(platform="chatgpt"):
        print(msg)
    
    print("\nSearch for 'Hi':")
    for msg in store.search_messages("Hi"):
        print(msg)

if __name__ == "__main__":
    test_message_store()
```

### Step 3: Add Basic Processing
```python
# file: message_processor.py

from typing import List, Dict, Any
from chat_message import ChatMessage
from message_store import MessageStore

class MessageProcessor:
    """Process and analyze chat messages."""
    
    def __init__(self):
        self.store = MessageStore()
    
    def process_message(self, message: ChatMessage) -> Dict[str, Any]:
        """Process a single message."""
        # Add basic analysis
        analysis = {
            "word_count": len(message.content.split()),
            "char_count": len(message.content),
            "has_question": "?" in message.content
        }
        
        # Add analysis to message metadata
        message.add_metadata("analysis", analysis)
        
        # Store the message
        self.store.add_message(message)
        
        return analysis
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about the conversation."""
        messages = self.store.get_messages()
        
        if not messages:
            return {"message_count": 0}
        
        # Calculate stats
        stats = {
            "message_count": len(messages),
            "platform_counts": {},
            "sender_counts": {},
            "avg_word_count": 0
        }
        
        total_words = 0
        
        for msg in messages:
            # Count by platform
            platform = msg.platform
            stats["platform_counts"][platform] = \
                stats["platform_counts"].get(platform, 0) + 1
            
            # Count by sender
            sender = msg.sender
            stats["sender_counts"][sender] = \
                stats["sender_counts"].get(sender, 0) + 1
            
            # Add to word count
            total_words += msg.metadata.get("analysis", {}).get("word_count", 0)
        
        # Calculate average
        stats["avg_word_count"] = total_words / len(messages)
        
        return stats

# Test the processor
def test_message_processor():
    # Create processor
    processor = MessageProcessor()
    
    # Process some messages
    messages = [
        ChatMessage("Hello! How are you?", "User", "chatgpt"),
        ChatMessage("I'm doing well, thanks for asking.", "AI", "chatgpt"),
        ChatMessage("That's great to hear!", "User", "claude")
    ]
    
    print("Processing messages:")
    for msg in messages:
        analysis = processor.process_message(msg)
        print(f"\nMessage: {msg}")
        print(f"Analysis: {analysis}")
    
    print("\nConversation stats:")
    stats = processor.get_conversation_stats()
    print(stats)

if __name__ == "__main__":
    test_message_processor()
```

### Step 4: Create a Simple CLI
```python
# file: chat_cli.py

from chat_message import ChatMessage
from message_processor import MessageProcessor

def main():
    """Simple CLI for chat message processing."""
    processor = MessageProcessor()
    
    while True:
        print("\nChatSynth CLI")
        print("1. Add message")
        print("2. View recent messages")
        print("3. View stats")
        print("4. Search messages")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == "1":
            # Add message
            content = input("Enter message: ")
            sender = input("Enter sender: ")
            platform = input("Enter platform: ")
            
            msg = ChatMessage(content, sender, platform)
            processor.process_message(msg)
            print("Message added!")
        
        elif choice == "2":
            # View messages
            platform = input("Enter platform (or press Enter for all): ").strip()
            messages = processor.store.get_messages(
                platform=platform if platform else None
            )
            
            print("\nRecent messages:")
            for msg in messages:
                print(msg)
        
        elif choice == "3":
            # View stats
            stats = processor.get_conversation_stats()
            print("\nConversation stats:")
            for key, value in stats.items():
                print(f"{key}: {value}")
        
        elif choice == "4":
            # Search messages
            keyword = input("Enter search term: ")
            messages = processor.store.search_messages(keyword)
            
            print("\nSearch results:")
            for msg in messages:
                print(msg)
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
```

## How to Use This Project

1. **Start with Understanding:**
   - Read through each file's code
   - Look up any unfamiliar concepts
   - Run each test function to see how it works

2. **Practice by Extending:**
   - Add new message metadata
   - Implement more analysis features
   - Add message validation
   - Improve the search function
   - Add message export/import

3. **Learning Projects:**

   a. **Add Message Validation:**
   ```python
   def validate_message(message: ChatMessage) -> bool:
       """Add your validation logic here."""
       if not message.content.strip():
           return False
       if len(message.content) > 1000:
           return False
       return True
   ```

   b. **Add Message Export:**
   ```python
   def export_messages(filename: str) -> None:
       """Export messages to a file."""
       messages = [msg.to_dict() for msg in store.get_messages()]
       with open(filename, 'w') as f:
           json.dump(messages, f, indent=2)
   ```

   c. **Add Basic Analytics:**
   ```python
   def analyze_sentiment(content: str) -> str:
       """Simple sentiment analysis."""
       positive = ['happy', 'good', 'great', 'awesome']
       negative = ['sad', 'bad', 'awful', 'terrible']
       
       words = content.lower().split()
       pos_count = sum(1 for w in words if w in positive)
       neg_count = sum(1 for w in words if w in negative)
       
       if pos_count > neg_count:
           return 'positive'
       elif neg_count > pos_count:
           return 'negative'
       return 'neutral'
   ```

4. **Next Steps:**
   - Add persistent storage (SQLite)
   - Implement message threading
   - Add user authentication
   - Create a web interface
   - Add platform-specific formatters

## Learning Exercises

1. **Basic:**
   - Add message editing
   - Implement message deletion
   - Add timestamp filtering
   - Create message categories

2. **Intermediate:**
   - Add JSON import/export
   - Implement message threading
   - Add basic text analysis
   - Create message formatting

3. **Advanced:**
   - Add SQLite storage
   - Implement WebSocket updates
   - Add platform integrations
   - Create a web interface

Remember:
- Write tests for new features
- Document your code
- Handle errors gracefully
- Keep the code organized
- Use type hints
- Follow PEP 8 style
