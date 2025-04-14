from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi import Request

app = FastAPI()
router = APIRouter()

# Clean model
class TranscriptUpload(BaseModel):
    raw_transcript: str

# Working route
@router.post("/podcast/upload/")
def upload_transcript(payload: TranscriptUpload):
    return {
        "status": "Transcript uploaded",
        "received": payload.raw_transcript
    }

app.include_router(router)