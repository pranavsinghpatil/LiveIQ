from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ThreadBase(BaseModel):
    title: str

class ThreadCreate(ThreadBase):
    chat_ids: List[str]

class ThreadUpdate(BaseModel):
    title: Optional[str]
    chat_ids: Optional[List[str]]

class Thread(ThreadBase):
    id: str
    chat_ids: List[str]
    created_at: datetime
