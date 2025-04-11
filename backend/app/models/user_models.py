from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --------------------
# User Models
# --------------------

class User(BaseModel):
    id: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str  # Supabase will hash this internally

class UserOut(BaseModel):
    id: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True