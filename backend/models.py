"""
Database models for VoxStitch.
"""

from pydantic import BaseModel
from typing import List, Optional

class ChatImport(BaseModel):
    platform: str  # e.g., ChatGPT, WhatsApp
    format: str  # e.g., JSON, TXT
    content: List[str]  # Messages in the chat
    metadata: Optional[dict] = None  # Extra details like timestamps


class MergeChatsRequest(BaseModel):
    chat_ids: List[str]