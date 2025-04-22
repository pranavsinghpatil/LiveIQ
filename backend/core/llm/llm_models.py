from pydantic import BaseModel
from typing import List, Optional, Dict

class LLMChatMessage(BaseModel):
    role: str
    content: str

class LLMChatRequest(BaseModel):
    chat_id: Optional[str] = "default"
    messages: List[LLMChatMessage]
    provider: Optional[str] = "google"
    model: Optional[str] = None

class LLMChatResponse(BaseModel):
    reply: str

class LLMThreadRequest(BaseModel):
    chat_id: str
    message_id: str  # UUID or hash of the message
    selected_text: str
    provider: Optional[str] = "google"
    model: Optional[str] = None

class LLMThreadResponse(BaseModel):
    thread_id: str
    reply: str

class HybridCreateRequest(BaseModel):
    hybrid_id: str
    chat_ids: List[str]

class HybridChatRequest(BaseModel):
    hybrid_id: str
    user_message: str
    provider: Optional[str] = "google"
    model: Optional[str] = None

class APIKeyUpdate(BaseModel):
    provider: str
    api_key: str

class LLMModelMetadata(BaseModel):
    name: str
    provider: str
    description: Optional[str] = None
