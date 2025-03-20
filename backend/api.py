"""
Main API router for ChatSynth.
Implements core endpoints for user management and chat operations.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from .database import get_db
from .models import User, ChatLog, Tag
from .auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="ChatSynth API")

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatLogCreate(BaseModel):
    source: str
    title: Optional[str] = None
    content: dict
    metadata: Optional[dict] = None

class ChatLogResponse(BaseModel):
    id: str
    source: str
    title: Optional[str]
    content: dict
    summary: Optional[str]
    created_at: str
    updated_at: str
    metadata: dict
    tags: List[str]

    class Config:
        orm_mode = True

# Authentication endpoints
@app.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint to get access token."""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create new user account."""
    # Check if username exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create user
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Chat log endpoints
@app.post("/chatlogs/", response_model=ChatLogResponse)
async def create_chatlog(
    chatlog: ChatLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new chat log."""
    db_chatlog = ChatLog(
        user_id=current_user.id,
        source=chatlog.source,
        title=chatlog.title,
        content=chatlog.content,
        metadata=chatlog.metadata or {}
    )
    db.add(db_chatlog)
    db.commit()
    db.refresh(db_chatlog)
    return db_chatlog

@app.get("/chatlogs/", response_model=List[ChatLogResponse])
async def get_chatlogs(
    skip: int = 0,
    limit: int = 100,
    source: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's chat logs with optional filtering."""
    query = db.query(ChatLog).filter(ChatLog.user_id == current_user.id)
    if source:
        query = query.filter(ChatLog.source == source)
    return query.offset(skip).limit(limit).all()

@app.get("/chatlogs/{chatlog_id}", response_model=ChatLogResponse)
async def get_chatlog(
    chatlog_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific chat log."""
    chatlog = db.query(ChatLog)\
        .filter(ChatLog.id == chatlog_id)\
        .filter(ChatLog.user_id == current_user.id)\
        .first()
    if not chatlog:
        raise HTTPException(status_code=404, detail="Chat log not found")
    return chatlog

@app.put("/chatlogs/{chatlog_id}/tags")
async def update_chatlog_tags(
    chatlog_id: str,
    tags: List[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update tags for a chat log."""
    chatlog = db.query(ChatLog)\
        .filter(ChatLog.id == chatlog_id)\
        .filter(ChatLog.user_id == current_user.id)\
        .first()
    if not chatlog:
        raise HTTPException(status_code=404, detail="Chat log not found")
    
    # Clear existing tags
    chatlog.tags = []
    
    # Add new tags
    for tag_name in tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
        chatlog.tags.append(tag)
    
    db.commit()
    return {"status": "success"}
