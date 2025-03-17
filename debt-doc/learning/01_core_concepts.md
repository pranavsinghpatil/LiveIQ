# Core Concepts of ChatSynth

This guide explains the fundamental concepts of ChatSynth in simple terms, helping you understand how everything works together.

## 1. What is ChatSynth?

ChatSynth is like a digital filing cabinet for your AI chat conversations. Instead of having your chats scattered across different AI platforms (ChatGPT, Mistral, Gemini), ChatSynth brings them all into one place.

### Key Features Explained:

1. **Multi-platform Chat Import**
   - What it means: You can bring in chats from different AI platforms
   - How it works: 
     ```python
     # Each chat has a source field
     chat = {
         "source": "chatgpt",  # Which AI platform it's from
         "content": {...},     # The actual chat content
         "metadata": {...}     # Extra information
     }
     ```

2. **Unified Dashboard**
   - What it means: One screen to see all your chats
   - Benefits:
     - No switching between platforms
     - Consistent interface
     - Easy organization

3. **Search and Filtering**
   - What it means: Find any chat quickly
   - How it works:
     ```sql
     -- We use special database indexes
     CREATE INDEX idx_chat_content ON chat_logs 
     USING gin(to_tsvector('english', content));
     
     -- This lets us search inside chat content
     SELECT * FROM chat_logs 
     WHERE to_tsvector('english', content) @@ to_tsquery('search_term');
     ```

4. **Automated Summarization**
   - What it means: ChatSynth can create short summaries of long conversations
   - When it happens:
     - When importing a chat
     - When updating a chat
     - On user request

5. **Tagging System**
   - What it means: Add labels to organize chats
   - Example:
     ```python
     # A chat can have multiple tags
     chat = {
         "id": 1,
         "tags": ["work", "important", "python"]
     }
     ```

## 2. How Data Flows Through ChatSynth

Let's follow a chat from import to display:

### Step 1: User Imports Chat
```python
# 1. User pastes chat from ChatGPT
raw_chat = """
{
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
}
"""

# 2. ChatSynth validates the format
if not is_valid_chat_format(raw_chat):
    raise ValueError("Invalid chat format")

# 3. Converts to internal format
chat_data = convert_to_internal_format(raw_chat)
```

### Step 2: Data Processing
```python
# 1. Generate summary
summary = generate_summary(chat_data)

# 2. Extract metadata
metadata = {
    "platform": "chatgpt",
    "message_count": len(chat_data["messages"]),
    "created_at": datetime.now()
}

# 3. Save to database
new_chat = ChatLog(
    user_id=current_user.id,
    content=chat_data,
    summary=summary,
    metadata=metadata
)
db.add(new_chat)
db.commit()
```

### Step 3: Frontend Display
```typescript
// 1. Load chat in React component
function ChatViewer({ chatId }: { chatId: string }) {
    // Get chat from Redux store
    const chat = useSelector(state => 
        selectChatById(state, chatId)
    );
    
    return (
        <div className="chat-viewer">
            {/* Show chat messages */}
            {chat.messages.map(message => (
                <ChatMessage
                    key={message.id}
                    content={message.content}
                    role={message.role}
                />
            ))}
        </div>
    );
}
```

## 3. Database Structure

### Main Tables:
1. **Users Table**
   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       email VARCHAR(255) UNIQUE,
       hashed_password VARCHAR(255)
   );
   -- This stores user accounts
   ```

2. **Chat Logs Table**
   ```sql
   CREATE TABLE chat_logs (
       id SERIAL PRIMARY KEY,
       user_id INTEGER REFERENCES users(id),
       source VARCHAR(50),
       content JSONB,
       summary TEXT,
       metadata JSONB
   );
   -- This stores all the chats
   ```

3. **Tags Table**
   ```sql
   CREATE TABLE tags (
       id SERIAL PRIMARY KEY,
       name VARCHAR(50),
       user_id INTEGER REFERENCES users(id)
   );
   -- This stores chat labels
   ```

4. **Chat Tags Table**
   ```sql
   CREATE TABLE chat_tags (
       chat_id INTEGER REFERENCES chat_logs(id),
       tag_id INTEGER REFERENCES tags(id),
       PRIMARY KEY (chat_id, tag_id)
   );
   -- This connects chats with their tags
   ```

## 4. Security Model

### User Authentication
```python
# 1. When user logs in
def login_user(email: str, password: str):
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("User not found")
    
    # Check password
    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid password")
    
    # Create session token
    token = create_jwt_token(user.id)
    return token

# 2. Checking user access
def get_user_chats(user_id: int):
    # Only return chats owned by this user
    return db.query(ChatLog)\
        .filter(ChatLog.user_id == user_id)\
        .all()
```

### Data Privacy
1. Each chat belongs to one user
2. Users can only see their own chats
3. All API endpoints check user ownership
4. Passwords are always hashed
5. Sensitive data is encrypted

## 5. Real-time Features

### WebSocket Connection
```python
# Backend WebSocket handler
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Get message from client
            data = await websocket.receive_json()
            
            # Handle different message types
            if data["type"] == "chat_update":
                # Send update to client
                await websocket.send_json({
                    "type": "update",
                    "data": process_update(data)
                })
    except WebSocketDisconnect:
        # Handle disconnection
        pass
```

### Frontend Connection
```typescript
// WebSocket connection in React
function useWebSocket() {
    useEffect(() => {
        // Connect to WebSocket
        const ws = new WebSocket('ws://localhost:8000/ws');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            // Handle different updates
            switch (data.type) {
                case "chat_updated":
                    // Update chat in Redux store
                    dispatch(updateChat(data.chat));
                    break;
                    
                case "new_chat":
                    // Add new chat to store
                    dispatch(addChat(data.chat));
                    break;
            }
        };
        
        return () => ws.close();
    }, []);
}
```

## 6. Understanding Each Part

### Backend Parts:
1. **FastAPI Application**
   - Handles web requests
   - Manages database
   - Processes chats

2. **Database (PostgreSQL)**
   - Stores all data
   - Handles searching
   - Manages relationships

3. **Redis Cache**
   - Speeds up common requests
   - Handles real-time features
   - Manages user sessions

### Frontend Parts:
1. **React Components**
   - Show user interface
   - Handle user input
   - Display chats

2. **Redux Store**
   - Manages application state
   - Handles data updates
   - Keeps UI in sync

3. **TypeScript**
   - Adds type safety
   - Catches errors early
   - Makes code clearer

## 7. Common Operations

### Importing a Chat
```python
# Steps involved:
# 1. Validate input
def validate_chat(content: str, source: str):
    if source not in VALID_SOURCES:
        raise ValueError("Invalid source")
    try:
        json.loads(content)  # Check JSON format
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

# 2. Process chat
def process_chat(content: str):
    # Parse content
    data = json.loads(content)
    
    # Extract messages
    messages = []
    for msg in data["messages"]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    return {
        "messages": messages,
        "processed_at": datetime.now()
    }

# 3. Save chat
def save_chat(user_id: int, chat_data: dict):
    chat = ChatLog(
        user_id=user_id,
        content=chat_data,
        source=chat_data["source"]
    )
    db.add(chat)
    db.commit()
    return chat
```

### Searching Chats
```python
# Different ways to search:
# 1. By content
def search_content(query: str, user_id: int):
    return db.query(ChatLog)\
        .filter(
            ChatLog.user_id == user_id,
            ChatLog.content.contains(query)
        )\
        .all()

# 2. By tags
def search_by_tags(tags: List[str], user_id: int):
    return db.query(ChatLog)\
        .join(ChatTags)\
        .join(Tag)\
        .filter(
            ChatLog.user_id == user_id,
            Tag.name.in_(tags)
        )\
        .all()

# 3. Combined search
def advanced_search(
    query: str,
    tags: List[str],
    source: str,
    user_id: int
):
    base_query = db.query(ChatLog)\
        .filter(ChatLog.user_id == user_id)
    
    if query:
        base_query = base_query.filter(
            ChatLog.content.contains(query)
        )
    
    if tags:
        base_query = base_query\
            .join(ChatTags)\
            .join(Tag)\
            .filter(Tag.name.in_(tags))
    
    if source:
        base_query = base_query.filter(
            ChatLog.source == source
        )
    
    return base_query.all()
```

## Next Steps

1. **Start with Backend**
   - Learn FastAPI basics
   - Understand database models
   - Study authentication system

2. **Move to Frontend**
   - Learn React fundamentals
   - Understand TypeScript
   - Study Redux state management

3. **Practice with Features**
   - Try importing chats
   - Use search and filters
   - Work with WebSocket updates
