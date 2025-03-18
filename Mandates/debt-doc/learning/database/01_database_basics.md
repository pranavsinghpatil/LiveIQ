# Understanding Database in ChatSynth

## Database Basics

### What is a Database?
A database is like a digital filing cabinet where we store all our chat data in an organized way. In ChatSynth, we use PostgreSQL because:
1. It's great at handling JSON data (perfect for different chat formats)
2. It's reliable and widely used
3. It has powerful search features

## Our Database Structure

### 1. Users Table
This table stores information about our users:

```sql
-- This is what our users table looks like
CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- A unique number for each user
    email VARCHAR(255) UNIQUE,  -- User's email, must be unique
    hashed_password VARCHAR(255),  -- Encrypted password
    created_at TIMESTAMP DEFAULT NOW()  -- When the user signed up
);

-- Let's break this down:
-- 1. SERIAL PRIMARY KEY: Automatically gives each user a unique number
-- 2. VARCHAR(255): Text field with maximum 255 characters
-- 3. UNIQUE: No two users can have the same email
-- 4. TIMESTAMP: Stores date and time
```

### 2. Chat Logs Table
This is where we store all the chat conversations:

```sql
CREATE TABLE chat_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),  -- Links to the users table
    source VARCHAR(50),  -- Which AI platform (ChatGPT, Mistral, etc.)
    content JSONB,  -- The actual chat content
    metadata JSONB,  -- Additional information about the chat
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Understanding each part:
-- 1. user_id REFERENCES users(id): 
--    - This is called a "foreign key"
--    - It connects each chat to its owner
--    - If user_id is 5, this chat belongs to user #5

-- 2. JSONB:
--    - Stores JSON data efficiently
--    - Example content:
--      {
--        "messages": [
--          {"role": "user", "content": "Hello"},
--          {"role": "assistant", "content": "Hi there!"}
--        ]
--      }
```

### 3. Tags Table
For organizing chats with labels:

```sql
-- First, the tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    user_id INTEGER REFERENCES users(id)
);

-- Then, a table to connect tags to chats
CREATE TABLE chat_tags (
    chat_id INTEGER REFERENCES chat_logs(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (chat_id, tag_id)  -- Each chat-tag combination must be unique
);

-- This structure allows:
-- 1. One chat to have many tags
-- 2. One tag to be used on many chats
-- This is called a "many-to-many" relationship
```

## Using SQLAlchemy (Python Database Tool)

### 1. Database Models
These are Python classes that represent our database tables:

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

# Base model that all other models inherit from
class Base(DeclarativeBase):
    pass

# User model
class User(Base):
    __tablename__ = "users"  # This must match our table name
    
    # Define the columns
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Link to other tables
    chats = relationship("ChatLog", back_populates="user")
    
    # Let's break this down:
    # 1. Column(): Defines a database column
    # 2. relationship(): Connects to other tables
    # 3. back_populates: Makes the connection work both ways

# Chat Log model
class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source = Column(String(50))
    content = Column(JSONB)  # Stores JSON data
    metadata = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chats")
    tags = relationship("Tag", secondary="chat_tags")
    
    # Understanding relationships:
    # 1. user: Gives us the User object who owns this chat
    # 2. tags: Gives us all Tags for this chat
    # 3. secondary="chat_tags": Uses the chat_tags table to connect to Tags
```

### 2. Using the Models

Here's how we use these models in our code:

```python
# 1. Creating a new user
async def create_user(db: Session, email: str, password: str):
    # Create the user object
    new_user = User(
        email=email,
        hashed_password=hash_password(password)  # Always hash passwords!
    )
    
    # Add to database
    db.add(new_user)  # Stage the change
    db.commit()       # Save to database
    db.refresh(new_user)  # Get the latest data
    
    return new_user

# 2. Adding a chat log
async def create_chat(
    db: Session,
    user_id: int,
    content: str,
    source: str
):
    # Create chat object
    new_chat = ChatLog(
        user_id=user_id,
        content=content,
        source=source,
        metadata={}  # Empty metadata to start
    )
    
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    
    return new_chat

# 3. Finding chats for a user
async def get_user_chats(db: Session, user_id: int):
    return db.query(ChatLog)\
        .filter(ChatLog.user_id == user_id)\
        .order_by(ChatLog.created_at.desc())\
        .all()
    
    # This query:
    # 1. Starts with ChatLog table
    # 2. Filters to only show chats for our user
    # 3. Orders them newest first
    # 4. Gets all matching chats
```

### 3. Common Database Operations

```python
# 1. Adding tags to a chat
async def add_tag_to_chat(
    db: Session,
    chat_id: int,
    tag_name: str,
    user_id: int
):
    # First, find or create the tag
    tag = db.query(Tag)\
        .filter(Tag.name == tag_name, Tag.user_id == user_id)\
        .first()
    
    if not tag:
        tag = Tag(name=tag_name, user_id=user_id)
        db.add(tag)
    
    # Get the chat
    chat = db.query(ChatLog).get(chat_id)
    if not chat:
        raise ValueError("Chat not found")
    
    # Add tag to chat
    chat.tags.append(tag)
    db.commit()

# 2. Searching chats
async def search_chats(
    db: Session,
    user_id: int,
    search_term: str
):
    return db.query(ChatLog)\
        .filter(
            ChatLog.user_id == user_id,
            ChatLog.content.contains(search_term)  # Search in JSON
        )\
        .all()

# 3. Updating a chat
async def update_chat(
    db: Session,
    chat_id: int,
    new_content: str
):
    chat = db.query(ChatLog).get(chat_id)
    if not chat:
        raise ValueError("Chat not found")
    
    chat.content = new_content
    chat.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chat)
    
    return chat
```

## Practice Exercise

Try to write a function that:
1. Gets all chats for a user
2. Filters by a specific tag
3. Only returns chats from the last 7 days

Here's a starter template:
```python
async def get_recent_tagged_chats(
    db: Session,
    user_id: int,
    tag_name: str
):
    # Your code here
    pass
```

## Next Steps
1. Try the practice exercise
2. Learn about database migrations
3. Study database optimization techniques

## Common Questions

1. **Why use JSONB instead of TEXT for chat content?**
   - JSONB allows us to:
     - Store structured data
     - Query inside the JSON
     - Index the content
     - Validate the structure

2. **What's the difference between db.add() and db.commit()?**
   - db.add(): Tells SQLAlchemy we want to save this
   - db.commit(): Actually saves to the database
   - Think of add as "staging" and commit as "saving"

3. **Why use relationships?**
   - Makes it easy to get related data
   - Maintains data consistency
   - Prevents orphaned records
