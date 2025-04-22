"""
Chat routes for VoxStitch.
Handles chat uploads, imports, and management.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from ..models.chat import Chat, ChatCreate, ChatThread, Message, ChatMessage
from ..services.auth_service import get_current_user
from ..models.user_models import User
from ..utils.media_processor import media_processor
from ..services.supabase_client import supabase
from ..services.context_service import build_context
from datetime import datetime
from pydantic import BaseModel
import os
import logging
import traceback
import tempfile
from core.ingest.chat_ingestor import chat_ingestor
from supabase import create_client, Client
from dotenv import load_dotenv
import magic
from ..services.message_service import insert_message, get_messages_by_chat
from uuid import UUID

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Create router with tags for better API documentation
router = APIRouter(tags=["chats"])
logger = logging.getLogger(__name__)

# ------------------- CHAT ROUTES -------------------

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
            logger.info(f"File received: name={file.filename}, type={file.content_type}")
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(await file.read())
                file_path = temp.name
            # Use python-magic for accurate detection
            file_type = magic.from_file(file_path, mime=True)
            logger.info(f"Detected file type (magic): {file_type}")
            logger.info(f"File saved at: {file_path}")

        # Call ingestor
        result = await chat_ingestor.ingest(
            media_type=media_type,
            content=content,
            file_path=file_path,
            file_type=file_type
        )

        print(f"[DEBUG] media_type: {media_type}, file_path: {file_path}")
        print(f"[DEBUG] ingestion result: {result}")
        logger.info(f"Ingestor result: {result}")
        # If no content could be extracted, return a clear error and skip Supabase insert
        if result.get("content") is None:
            print("[DEBUG] No extractable content found, returning error response.")
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
        
        # Insert into Supabase
        logger.info(f"Inserting into Supabase: {chat_data}")
        try:
            insert_res = supabase.table("chats").insert(chat_data).execute()
            
            # Log the raw response for debugging
            logger.info(f"Raw Supabase response: {insert_res}")
            
            if hasattr(insert_res, 'error') and insert_res.error:
                logger.error(f"Supabase insert error: {insert_res.error}")
                raise HTTPException(status_code=500, detail=f"Failed to save chat to database: {insert_res.error}")
                
            # Log the response data for debugging
            logger.info(f"Supabase insert data: {insert_res.data}")
            
            # Extract the ID from the response
            chat_id = None
            if insert_res.data and len(insert_res.data) > 0:
                chat_id = insert_res.data[0].get("id")
                logger.info(f"Extracted chat ID: {chat_id}")
            else:
                logger.warning("No data returned from Supabase insert")
                
            response = {
                "status": "success",
                "data": {
                    "id": chat_id,
                    "user_id": user_id,
                    "title": title,
                    "content": result.get("content"),
                    "media_type": media_type
                }
            }
            logger.info(f"Final response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Exception during Supabase insert: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        print(traceback.format_exc())  # Print full error trace
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", response_model=ChatThread)
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

@router.post("/send_message", response_model=Message)
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

@router.get("/messages/{chat_id}", response_model=List[ChatMessage])
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

@router.get("/user/{user_id}")
def list_chats(user_id: str):
    try:
        logger.info(f"Fetching chats for user_id: {user_id}")
        try:
            res = supabase.table("chats").select("*").eq("user_id", user_id).order(column="created_at", desc=True).execute()
            logger.info(f"Raw Supabase response from select: {res}")
            if hasattr(res, 'error') and res.error:
                logger.error(f"Supabase select error: {res.error}")
                raise HTTPException(status_code=500, detail=f"Failed to fetch chats: {res.error}")
            logger.info(f"Found {len(res.data)} chats for user {user_id}")
            return {
                "status": "success", 
                "chats": res.data
            }
        except Exception as e:
            logger.error(f"Exception during Supabase select: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error listing chats: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# ------------------- MESSAGE ROUTES -------------------

@router.post("/message")
async def post_message(message: ChatMessage):
    try:
        result = insert_message(message)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/message/{chat_id}")
async def get_chat_memory(chat_id: str):
    try:
        history = get_messages_by_chat(chat_id)
        return {"status": "success", "messages": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------- CONTEXT ROUTES -------------------

@router.get("/context/{chat_id}")
async def get_context(chat_id: str):
    try:
        context = build_context(chat_id)
        return {"chat_id": chat_id, "context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------- LLM integration ROUTES -------------------

from ..services.context_service import build_context
from ..services.message_service import save_message
from core.llm.llm_client import chat as llm_chat

@router.post("/reply")
async def generate_reply(payload: dict):
    """
    Takes a user message, sends to LLM with history context,
    returns + stores assistant reply
    """
    try:
        chat_id = payload["chat_id"]
        user_id = payload["user_id"]
        user_message = payload["message"]
        provider = payload.get("provider", "google")  # default: Gemini
        model = payload.get("model")  # Optional

        # 1. Save user message
        save_message(chat_id, user_id, "user", user_message)

        # 2. Build chat context
        context = build_context(chat_id)

        # 3. Prepare LLM messages (system + history + new msg)
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for line in context.splitlines():
            if ": " in line:
                role, content = line.split(": ", 1)
                messages.append({"role": role.lower(), "content": content})
        messages.append({"role": "user", "content": user_message})

        # 4. Ask LLM
        response = llm_chat(messages, provider=provider, model=model)

        # 5. Save assistant reply
        save_message(chat_id, user_id, "assistant", response)

        return {
            "status": "success",
            "reply": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/reply")
# def reply_get_not_allowed():
#     raise HTTPException(status_code=405, detail="GET not allowed on /reply. Use POST.")

# ------------------- PATCH ----------------

class ChatUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    media_type: Optional[str] = None

@router.patch("/{chat_id}")
async def update_chat(chat_id: str, update: ChatUpdate):
    try:
        logger.info(f"Updating chat {chat_id} with data: {update}")
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        res = supabase.table("chats").update(update_data).eq("id", chat_id).execute()

        # Fix: Only check .error if it exists
        if hasattr(res, "error") and res.error:
            logger.error(f"Supabase update error: {res.error}")
            raise HTTPException(status_code=500, detail=str(res.error))

        logger.info(f"Chat {chat_id} updated successfully")
        return {
            "status": "success",
            "message": "Chat updated successfully",
            "data": res.data[0] if res.data and len(res.data) > 0 else None
        }
    except Exception as e:
        logger.error(f"Error updating chat: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# ------------------- DELETE ----------------

@router.delete("/{chat_id}")
def delete_chat(chat_id: str):
    try:
        res = supabase.from_("chats").delete().eq("id", chat_id).execute()

        if res.error:
            raise HTTPException(status_code=500, detail=str(res.error))

        return {
            "status": "success",
            "message": f"Chat {chat_id} deleted."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------- PARAMETERIZED ROUTE LAST -------------------

@router.get("/{chat_id}")
def get_chat(chat_id: UUID):
    try:
        query = supabase.table("chats").select("*").eq("id", str(chat_id))
        query = query.is_("user_id", None)
        res = query.single().execute()
        if hasattr(res, 'error') and res.error:
            raise HTTPException(status_code=404, detail="Chat not found")
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
