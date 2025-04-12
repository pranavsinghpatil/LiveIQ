"""
Chat routes for VoxStitch.
Handles chat uploads, imports, and management.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import tempfile
from typing import Optional

from ..utils.media_processor import media_processor

# Create router with tags for better API documentation
router = APIRouter(tags=["chats"])

class ChatUpload(BaseModel):
    user_id: str
    title: str
    content: str
    media_type: str

@router.post("")  # Empty string since prefix already includes /api/chats
async def upload_chat(chat: ChatUpload, file: Optional[UploadFile] = None):
    """
    Upload a chat from various sources:
    - Direct text content
    - File upload (PDF, image, video)
    - Link import (YouTube, ChatGPT, webpage)
    """
    try:
        # Handle direct content upload
        if chat.media_type == "text":
            return {  # Return dict directly, FastAPI will handle JSON conversion
                "status": "success",
                "data": {
                    "type": "text",
                    "content": chat.content,
                    "title": chat.title,
                    "user_id": chat.user_id
                }
            }

        # Handle file upload
        if file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(await file.read())
                temp_path = temp_file.name

            try:
                result = await media_processor.process_file(temp_path, file.content_type)
                os.unlink(temp_path)  # Clean up temp file
                
                return {
                    "status": "success",
                    "data": {
                        **result,
                        "title": chat.title,
                        "user_id": chat.user_id
                    }
                }
            except Exception as e:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise e

        # Handle link import
        if chat.media_type == "link":
            result = await media_processor.process_link(chat.content)
            return {
                "status": "success",
                "data": {
                    **result,
                    "title": chat.title,
                    "user_id": chat.user_id
                }
            }

        raise HTTPException(status_code=400, detail="Invalid media type")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
