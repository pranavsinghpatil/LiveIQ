from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    token: str
    user: User

class MessageBase(BaseModel):
    role: str
    content: str
    timestamp: datetime

class Message(MessageBase):
    id: int
    chat_id: int

    class Config:
        from_attributes = True

class ChatLogBase(BaseModel):
    platform: str

class ChatLogCreate(ChatLogBase):
    content: str

class ChatLog(ChatLogBase):
    id: int
    user_id: int
    imported_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True
