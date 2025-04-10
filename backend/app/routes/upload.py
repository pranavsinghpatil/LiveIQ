from fastapi import APIRouter, UploadFile, File, HTTPException
from uploads.handlers import save_upload

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        path = save_upload(file)
        return {"status": "success", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
