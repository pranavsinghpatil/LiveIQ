"""
Main API router for ChatSynth.
Implements core endpoints for user management and chat operations.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db, init_db
from models import User, ChatLog, Message
from schemas import UserCreate, User as UserSchema, Token, ChatLogCreate, ChatLog as ChatLogSchema
from auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
    oauth2_scheme,
)

app = FastAPI(title="ChatSynth API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to ChatSynth API. Visit /docs for API documentation."}

@app.post("/auth/login", response_model=Token)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    token = create_access_token(data={"sub": user.email})
    return {"token": token, "user": user}

@app.post("/auth/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role="user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    token = create_access_token(data={"sub": db_user.email})
    return {"token": token, "user": db_user}

@app.post("/auth/guest", response_model=Token)
async def guest_login(db: Session = Depends(get_db)):
    # Create temporary guest user
    guest_user = User(
        email=f"guest_{datetime.now().timestamp()}@chatsynth.com",
        username=f"guest_{datetime.now().timestamp()}",
        hashed_password=get_password_hash("guest"),
        role="guest"
    )
    db.add(guest_user)
    db.commit()
    db.refresh(guest_user)
    
    token = create_access_token(data={"sub": guest_user.email})
    return {"token": token, "user": guest_user}

@app.get("/chats", response_model=List[ChatLogSchema])
async def get_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    platform: Optional[str] = None
):
    query = db.query(ChatLog).filter(ChatLog.user_id == current_user.id)
    if platform:
        query = query.filter(ChatLog.platform == platform)
    return query.all()

@app.post("/chats/import", response_model=ChatLogSchema)
async def import_chat(
    chat: ChatLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check guest user limits
    if current_user.role == "guest":
        chat_count = db.query(ChatLog).filter(ChatLog.user_id == current_user.id).count()
        if chat_count >= 2:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Guest users can only import 2 chats. Please register for unlimited access.",
            )
    
    chat_log = ChatLog(
        platform=chat.platform,
        user_id=current_user.id,
        imported_at=datetime.now()
    )
    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)
    
    # Parse and store messages
    messages = []  # You would implement actual parsing logic here
    for msg in messages:
        message = Message(
            chat_id=chat_log.id,
            role=msg.get("role", "user"),
            content=msg.get("content", ""),
            timestamp=msg.get("timestamp", datetime.now())
        )
        db.add(message)
    
    db.commit()
    return chat_log

@app.get("/chats/{chat_id}", response_model=ChatLogSchema)
async def get_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(ChatLog).filter(
        ChatLog.id == chat_id,
        ChatLog.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    return chat

@app.delete("/chats/{chat_id}")
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(ChatLog).filter(
        ChatLog.id == chat_id,
        ChatLog.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully"}
