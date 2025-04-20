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

class APIKeyUpdate(BaseModel):
    provider: str
    api_key: str

class LLMModelMetadata(BaseModel):
    name: str
    provider: str
    description: Optional[str] = None
