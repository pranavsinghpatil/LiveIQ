from fastapi import APIRouter, UploadFile, File, HTTPException
from core.ingest.handlers import save_upload
from core.ingest.chat_ingestor import chat_ingestor

router = APIRouter(prefix="/api/upload", tags=["Uploads"])

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    try:
        path = save_upload(file)
        media_type = "file"
        content = await chat_ingestor.ingest(
            media_type=media_type,
            file_path=path,
            file_type=file.content_type
        )
        return {"status": "success", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
