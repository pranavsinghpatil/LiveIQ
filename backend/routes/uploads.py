from fastapi import APIRouter, File, UploadFile, HTTPException
import os
from database import supabase_client, BUCKET_NAME

upload_router = APIRouter()

@upload_router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    
    allowed_formats = ["txt", "json", "pdf", "png", "jpg", "jpeg", "mp3", "mp4"]
    if file_ext not in allowed_formats:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    file_content = await file.read()
    file_path = f"{BUCKET_NAME}/{file.filename}"

    response = supabase_client.storage.from_(BUCKET_NAME).upload(file_path, file_content)
    
    if response.error:
        raise HTTPException(status_code=500, detail="File upload failed")

    file_url = supabase_client.storage.from_(BUCKET_NAME).get_public_url(file_path)
    return {"message": "File uploaded successfully", "file_url": file_url}
