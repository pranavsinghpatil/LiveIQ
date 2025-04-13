# models/group.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ThreadGroup(BaseModel):
    id: Optional[str]
    title: str
    description: Optional[str]
    thread_ids: List[str]  # ChatThread IDs
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    global_summary: Optional[str] = None
