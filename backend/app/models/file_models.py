from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --------------------
# File Models
# --------------------


class File(BaseModel):
    id: str
    chat_id: str
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

class FileCreate(BaseModel):
    chat_id: str
    file_name: str
    file_type: str
    file_size: int
    file_url: str