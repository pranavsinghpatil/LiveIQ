from fastapi import APIRouter, UploadFile, HTTPException
from core.ingestion.chat_ingestor import chat_ingestor
from core.ingestion.ingestion_models import TextIngestRequest, LinkIngestRequest, IngestedContent
import os
from uuid import uuid4

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "mp3", "mp4", "txt", "html", "json", "md", "htm"}

router = APIRouter(prefix="/api/ingest", tags=["Ingestion"])

@router.post("/text", response_model=IngestedContent)
async def ingest_text(payload: TextIngestRequest):
    return await chat_ingestor.ingest_text(payload.text)

@router.post("/youtube", response_model=IngestedContent)
async def ingest_youtube(payload: LinkIngestRequest):
    try:
        return await chat_ingestor.ingest_youtube(payload.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/file", response_model=IngestedContent)
async def ingest_file(file: UploadFile):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail=f"Unsupported file type: .{ext}")
    filename = f"{uuid4().hex}.{ext}"
    file_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        return await chat_ingestor.ingest_file(file_path, ext)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
