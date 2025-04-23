from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --------------------
# User Models
# --------------------

class Token(BaseModel):
    """Token response model for authentication"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token data model for JWT claims"""
    username: Optional[str] = None
    exp: Optional[datetime] = None

class UserBase(BaseModel):
    """Base user model with common fields"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class User(UserBase):
    """User model for responses"""
    id: str
    disabled: Optional[bool] = False
    guest: Optional[bool] = False
    chat_imports_remaining: Optional[int] = None
    messages_remaining: Optional[int] = None

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    """User model for registration"""
    password: str  # Supabase will hash this internally

class UserRegistrationResponse(BaseModel):
    status: str
    message: str
    data: User

class UserInDB(User):
    """User model for database operations"""
    hashed_password: str

class UserOut(BaseModel):
    """User model for public responses"""
    id: str
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    guest: Optional[bool] = False
    chat_imports_remaining: Optional[int] = None
    messages_remaining: Optional[int] = None

    class Config:
        from_attributes = True