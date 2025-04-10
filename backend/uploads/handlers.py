from fastapi import UploadFile
import os
import shutil
from uuid import uuid4

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "mp3", "mp4", "txt"}

def is_allowed(filename: str) -> bool:
    return filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS

def save_upload(file: UploadFile) -> str:
    if not is_allowed(file.filename):
        raise ValueError("File type not supported")
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path

