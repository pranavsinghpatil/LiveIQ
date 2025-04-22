from pydantic import BaseModel
from typing import Optional

class TextIngestRequest(BaseModel):
    text: str

class LinkIngestRequest(BaseModel):
    url: str

class IngestedContent(BaseModel):
    content: str
    media_type: str
    created_at: str
