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
from models.chat import ChatThread, Message
from supabase_Client import supabase
from datetime import datetime
from ..utils.media_processor import media_processor
from models.group import ThreadGroup

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
# -------------------core------------------------


@router.post("/chat/create")
def create_chat(chat: ChatThread):
    data = chat.dict()
    data["created_at"] = datetime.now().isoformat()
    res = supabase.table("chat_threads").insert(data).execute()
    return res.data

@router.post("/message/send")
def send_message(msg: Message):
    msg.timestamp = datetime.now()
    res = supabase.table("messages").insert(msg.dict()).execute()
    return res.data

@router.get("/chat/{chat_id}/messages")
def get_chat_messages(chat_id: str):
    res = supabase.table("messages").select("*").eq("thread_id", chat_id).order("timestamp").execute()
    return res.data


@router.post("/group/create")
def create_thread_group(group: ThreadGroup):
    group.created_at = datetime.now()
    res = supabase.table("thread_groups").insert(group.dict()).execute()
    return res.data

@router.get("/group/{group_id}")
def get_thread_group(group_id: str):
    res = supabase.table("thread_groups").select("*").eq("id", group_id).single().execute()
    return res.data

@router.post("/group/{group_id}/add_thread")
def add_thread_to_group(group_id: str, thread_id: str):
    group = supabase.table("thread_groups").select("*").eq("id", group_id).single().execute().data
    if group:
        group["thread_ids"].append(thread_id)
        group["updated_at"] = datetime.now().isoformat()
        supabase.table("thread_groups").update(group).eq("id", group_id).execute()
        return {"status": "added"}
    return {"error": "group not found"}