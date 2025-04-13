from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    id: str
    sender: str  # "user" or bot name
    content: str
    timestamp: datetime
    metadata: Optional[dict] = {}

class ChatThread(BaseModel):
    id: str
    title: Optional[str] = None
    source: Optional[str] = None  # "ChatGPT", "Claude", "Screenshot", etc
    messages: List[Message] = []
    context_summary: Optional[str] = None
    linked_thread_ids: List[str] = []

class PodcastSpeaker(BaseModel):
    name: str
    transcript: str
from pydantic import BaseModel

class TranscriptUpload(BaseModel):
    raw_transcript: str

class ChatRequest(BaseModel):
    speaker: str
    user_msg: str