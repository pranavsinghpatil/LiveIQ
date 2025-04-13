from pydantic import BaseModel

class TranscriptUpload(BaseModel):
    raw_transcript: str

class ChatRequest(BaseModel):
    speaker: str
    user_msg: str
