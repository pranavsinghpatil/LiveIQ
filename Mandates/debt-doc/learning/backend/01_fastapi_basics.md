# Understanding FastAPI in ChatSynth

## What is FastAPI?

FastAPI is a modern web framework for building APIs with Python. Think of it as a tool that helps us create web services (like what ChatSynth needs) quickly and efficiently.

### Why We Chose FastAPI
1. **Speed**: It's one of the fastest Python frameworks
2. **Easy to Learn**: Uses simple Python code
3. **Automatic Documentation**: Creates API docs automatically
4. **Type Checking**: Helps catch errors before they happen

## Basic Concepts Explained

### 1. Routes
Routes are like addresses for our API. When someone wants to talk to our application, they use these addresses.

```python
# This is our main.py file
from fastapi import FastAPI

app = FastAPI()

# This creates a route at http://localhost:8000/
@app.get("/")
def read_root():
    return {"message": "Welcome to ChatSynth"}

# Let's break this down:
# 1. @app.get("/") - This is a decorator that tells FastAPI this function handles GET requests
# 2. def read_root() - This is a regular Python function
# 3. return {...} - We return data that will be sent to the user
```

### 2. Path Parameters
These are values we can get from the URL:

```python
# This route will be like: http://localhost:8000/chats/123
@app.get("/chats/{chat_id}")
def get_chat(chat_id: int):
    # chat_id will be automatically converted to an integer
    return {"chat_id": chat_id}

# Breaking it down:
# 1. {chat_id} in the URL is a path parameter
# 2. chat_id: int tells FastAPI to convert the value to an integer
# 3. If someone tries to use a letter instead of a number, FastAPI will return an error
```

### 3. Query Parameters
These are optional parameters in the URL:

```python
# This can handle URLs like:
# http://localhost:8000/chats?skip=0&limit=10
@app.get("/chats")
def list_chats(skip: int = 0, limit: int = 10):
    # skip and limit are optional with default values
    return {"skip": skip, "limit": limit}

# Understanding the parts:
# 1. skip: int = 0 creates an optional parameter with default value 0
# 2. The URL uses ? to start query parameters
# 3. & separates multiple parameters
```

### 4. Request Body
When we need to receive data from the user (like when creating a new chat):

```python
# First, we create a model for our data
from pydantic import BaseModel

class ChatCreate(BaseModel):
    title: str
    content: str
    source: str  # like 'chatgpt' or 'mistral'

# Then we use it in our route
@app.post("/chats")
def create_chat(chat: ChatCreate):
    # FastAPI will:
    # 1. Read the JSON from the request
    # 2. Convert it to our ChatCreate model
    # 3. Validate all the data
    # 4. Give us a Python object to work with
    return {
        "title": chat.title,
        "content": chat.content,
        "source": chat.source
    }

# If someone sends invalid data, FastAPI automatically returns an error
```

### 5. Dependencies
Dependencies help us reuse code and manage things like database connections:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

# This function gets our database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# We use it in our routes like this
@app.get("/chats/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    # Now we have a database connection to use
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    return chat

# Breaking it down:
# 1. Depends(get_db) tells FastAPI to run get_db
# 2. The database connection is automatically passed to our function
# 3. FastAPI handles closing the connection when we're done
```

### 6. Error Handling
How we handle things that go wrong:

```python
from fastapi import HTTPException

@app.get("/chats/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        # If we don't find the chat, we raise an error
        raise HTTPException(
            status_code=404,
            detail=f"Chat {chat_id} not found"
        )
    return chat

# Understanding error handling:
# 1. HTTPException is FastAPI's way of returning error responses
# 2. status_code=404 means "not found"
# 3. detail is the message we send back to explain what went wrong
```

## Practical Example: Chat Import

Let's look at a real feature from ChatSynth:

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import json

# First, our data model
class ChatImport(BaseModel):
    content: str
    source: str
    metadata: Optional[dict] = None
    
    # Validate the source platform
    @validator("source")
    def validate_source(cls, v):
        valid_sources = ["chatgpt", "mistral", "gemini"]
        if v not in valid_sources:
            raise ValueError(
                f"Invalid source. Must be one of: {valid_sources}"
            )
        return v

# The route that handles chat imports
@app.post("/chats/import")
async def import_chat(
    chat_data: ChatImport,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # 1. Create a new chat record
        new_chat = Chat(
            user_id=current_user.id,
            source=chat_data.source,
            content=chat_data.content,
            metadata=chat_data.metadata or {}
        )
        
        # 2. Save it to the database
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        
        # 3. Return the created chat
        return {
            "message": "Chat imported successfully",
            "chat_id": new_chat.id
        }
        
    except Exception as e:
        # If anything goes wrong, rollback the database
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to import chat: {str(e)}"
        )

# Let's break down what's happening:
# 1. We validate the incoming data using ChatImport model
# 2. We get a database connection using Depends(get_db)
# 3. We check the user is logged in with Depends(get_current_user)
# 4. We create a new chat record in the database
# 5. If anything goes wrong, we rollback and return an error
# 6. If successful, we return the new chat's ID
```

## Practice Exercise

Try to create a new route that:
1. Lists all chats for the current user
2. Allows filtering by source platform
3. Includes pagination

Here's a starter template:
```python
@app.get("/chats/my")
async def list_my_chats(
    source: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Your code here
    pass
```

## Next Steps
1. Try the practice exercise
2. Read about database models in the next guide
3. Learn about authentication in FastAPI
