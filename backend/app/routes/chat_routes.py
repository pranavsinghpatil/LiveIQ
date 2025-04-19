"""
Chat routes for VoxStitch.
Handles chat uploads, imports, and management.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from ..models.chat import Chat, ChatCreate, ChatThread, Message
from ..services.auth_service import get_current_user
from ..models.user_models import User
from ..utils.media_processor import media_processor
from ..models.group import ThreadGroup
from ..services.supabase_client import supabase
from datetime import datetime
import os
import logging
import traceback
import tempfile
from core.ingestion.chat_ingestor import chat_ingestor
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Create router with tags for better API documentation
routes = APIRouter(tags=["chats"])
logger = logging.getLogger(__name__)

@routes.post("/group/create", response_model=ThreadGroup)
async def create_thread_group(group: ThreadGroup, current_user: User = Depends(get_current_user)):
    """Create a new thread group"""
    try:
        # Initialize group data
        group_data = group.dict()
        group_data["created_at"] = datetime.utcnow().isoformat()
        group_data["user_id"] = current_user.id
        if not group_data.get("thread_ids"):
            group_data["thread_ids"] = []

        # Save to Supabase
        res = supabase.table("thread_groups").insert(group_data).execute()
        
        if res.error:
            logger.error(f"Error creating group: {str(res.error)}")
            raise HTTPException(status_code=500, detail=str(res.error))
            
        return res.data[0]
    except Exception as e:
        logger.error(f"Error creating group: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@routes.get("/group/{group_id}", response_model=ThreadGroup)
async def get_thread_group(group_id: str, current_user: User = Depends(get_current_user)):
    """Get a thread group by ID"""
    try:
        res = supabase.table("thread_groups").select("*").eq("id", group_id).single().execute()
        
        if res.error:
            logger.error(f"Error getting group: {str(res.error)}")
            raise HTTPException(status_code=404, detail="Group not found")
            
        return res.data
    except Exception as e:
        logger.error(f"Error getting group: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@routes.post("/group/{group_id}/add_thread")
async def add_thread_to_group(
    group_id: str, 
    thread_id: str, 
    current_user: User = Depends(get_current_user)
):
    """Add a chat thread to a group"""
    try:
        # Get the group
        res = supabase.table("thread_groups").select("*").eq("id", group_id).single().execute()
        if res.error:
            raise HTTPException(status_code=404, detail="Group not found")

        group = res.data
        
        # Verify ownership
        if group.get("user_id") != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this group")

        # Add thread ID if not already present
        if thread_id not in group["thread_ids"]:
            group["thread_ids"].append(thread_id)
            group["updated_at"] = datetime.utcnow().isoformat()
            
            # Update the group
            update_res = supabase.table("thread_groups").update(group).eq("id", group_id).execute()
            if update_res.error:
                raise HTTPException(status_code=500, detail=str(update_res.error))

        return {"status": "success", "message": "Thread added to group"}
    except Exception as e:
        logger.error(f"Error adding thread to group: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@routes.post("/upload")
async def upload_chat(
    user_id: str = Form(...),
    title: str = Form(...),
    media_type: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        print(f"Received: user_id={user_id}, title={title}, media_type={media_type}, content={content}, file={file}")
        file_path, file_type = None, None

        if media_type == "file":
            if not file:
                raise HTTPException(status_code=400, detail="File not uploaded")
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(await file.read())
                file_path = temp.name
                file_type = file.content_type

        # Call ingestor
        result = await chat_ingestor.ingest(
            media_type=media_type,
            content=content,
            file_path=file_path,
            file_type=file_type
        )

        # Clean up temp file if exists
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        # If no content could be extracted, return a clear error and skip Supabase insert
        if result.get("content") is None:
            return {
                "status": "error",
                "message": "Unsupported file type or failed to extract content",
                "metadata": result.get("metadata", {})
            }

        chat_data = {
            "user_id": user_id,
            "title": title,
            "content": result.get("content"),
            "media_type": media_type,
            "created_at": result.get("created_at") or None,
        }
        insert_res = supabase.table("chats").insert(chat_data).execute()
        if getattr(insert_res, 'error', None):
            raise HTTPException(status_code=500, detail="Failed to save chat to database")
        # Return only the relevant fields
        return {
            "status": "success",
            "data": {
                "id": insert_res.data[0]["id"] if insert_res.data and "id" in insert_res.data[0] else None,
                "user_id": user_id,
                "title": title,
                "content": result.get("content"),
                "media_type": media_type
            }
        }

    except Exception as e:
        print(traceback.format_exc())  # Print full error trace
        raise HTTPException(status_code=500, detail=str(e))

@routes.post("/chat/create")
async def create_chat(chat: ChatThread, current_user: User = Depends(get_current_user)):
    """Create a new chat thread"""
    try:
        data = chat.dict()
        data["created_at"] = datetime.utcnow().isoformat()
        data["user_id"] = current_user.id
        res = supabase.table("chat_threads").insert(data).execute()
        return res.data[0]
    except Exception as e:
        logger.error(f"Error creating chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@routes.post("/message/send")
async def send_message(msg: Message, current_user: User = Depends(get_current_user)):
    """Send a message in a chat thread"""
    try:
        # Check user limits for messages
        if current_user.guest and current_user.messages_remaining <= 0:
            raise HTTPException(
                status_code=403, 
                detail="Guest user has reached message limit. Please upgrade to continue."
            )

        msg.timestamp = datetime.utcnow()
        msg.user_id = current_user.id
        res = supabase.table("messages").insert(msg.dict()).execute()
        
        # Update user's message count if they're a guest
        if current_user.guest:
            supabase.table("users").update({
                "messages_remaining": current_user.messages_remaining - 1
            }).eq("id", current_user.id).execute()
            
        return res.data[0]
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@routes.get("/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: str, current_user: User = Depends(get_current_user)):
    """Get all messages in a chat thread"""
    try:
        # First verify chat access
        chat = supabase.table("chat_threads").select("user_id").eq("id", chat_id).single().execute()
        if chat.error:
            raise HTTPException(status_code=404, detail="Chat not found")
            
        if chat.data["user_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this chat")
            
        # Get messages
        res = supabase.table("messages").select("*").eq("thread_id", chat_id).order("timestamp").execute()
        return res.data
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.services.chat_service import send_message, get_history

router = APIRouter()

class ChatRequest(BaseModel):
    chat_id: str
    user_input: str
    provider: Optional[str] = "google"
    model: Optional[str] = None

@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Received /api/chat request: chat_id={request.chat_id}, provider={request.provider}, model={request.model}")
        logger.info(f"User input: {request.user_input}")
        reply = send_message(
            chat_id=request.chat_id,
            user_input=request.user_input,
            provider=request.provider,
            model=request.model
        )
        return {"reply": reply}
    except (ValueError, TypeError) as ve:
        logger.error(f"Validation error in /api/chat: {str(ve)}")
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        logger.error(f"Internal error in /api/chat: {str(e)}\n" + traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e), "trace": traceback.format_exc()})

@router.get("/chat/history/{chat_id}")
def get_chat_history(chat_id: str):
    return {"history": get_history(chat_id)}

class ChatUploadRequest(BaseModel):
    user_id: str
    title: str
    content: Optional[str] = None
    media_type: str  # "text", "file", "link"

@router.post("/upload")
async def upload_chat(
    user_id: str = Form(...),
    title: str = Form(...),
    media_type: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        print(f"Received: user_id={user_id}, title={title}, media_type={media_type}, content={content}, file={file}")
        file_path, file_type = None, None

        if media_type == "file":
            if not file:
                raise HTTPException(status_code=400, detail="File not uploaded")
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(await file.read())
                file_path = temp.name
                file_type = file.content_type

        # Call ingestor
        result = await chat_ingestor.ingest(
            media_type=media_type,
            content=content,
            file_path=file_path,
            file_type=file_type
        )

        # Clean up temp file if exists
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        return {
            "status": "success",
            "data": {
                "user_id": user_id,
                "title": title,
                **result
            }
        }

    except Exception as e:
        print(traceback.format_exc())  # Print full error trace
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
def list_chats(user_id: str):
    try:
        res = supabase.from_("chats").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        if res.error:
            raise HTTPException(status_code=500, detail=str(res.error))
        return {"status": "success", "chats": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
