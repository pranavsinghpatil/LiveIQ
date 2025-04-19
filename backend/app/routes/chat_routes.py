"""
Chat routes for VoxStitch.
Handles chat uploads, imports, and management.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional, List
from ..models.chat import Chat, ChatCreate, ChatThread, Message
from ..services.auth_service import get_current_user
from ..models.user_models import User
from ..utils.media_processor import media_processor
from ..models.group import ThreadGroup
from ..services.supabase_client import supabase
from datetime import datetime
import logging
import traceback

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
    title: str = Form(...),
    file: Optional[UploadFile] = File(None),
    content: Optional[str] = Form(None),
    media_type: str = Form("text"),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a chat from various sources:
    - Direct text content
    - File upload (PDF, image, video)
    - Link import (YouTube, ChatGPT, webpage)
    """
    try:
        # Check user limits for chat imports
        if current_user.guest and current_user.chat_imports_remaining <= 0:
            raise HTTPException(
                status_code=403, 
                detail="Guest user has reached chat import limit. Please upgrade to continue."
            )

        if file:
            # Process the uploaded file
            content = await media_processor.process_file(file)
            media_type = media_processor.get_media_type(file.filename)
        elif not content:
            raise HTTPException(status_code=400, detail="Either file or content must be provided")

        # Create chat thread
        chat_thread = ChatThread(
            title=title,
            source="upload",
            format=media_type,
            created_at=datetime.utcnow(),
            content=content,
            user_id=current_user.id
        )
        
        # Save to Supabase
        result = supabase.table("chat_threads").insert(chat_thread.dict()).execute()
        
        # Update user's chat import count if they're a guest
        if current_user.guest:
            supabase.table("users").update({
                "chat_imports_remaining": current_user.chat_imports_remaining - 1
            }).eq("id", current_user.id).execute()
        
        return JSONResponse(content={
            "status": "success",
            "data": result.data[0] if result.data else None
        })
        
    except Exception as e:
        logger.error(f"Error uploading chat: {str(e)}")
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
