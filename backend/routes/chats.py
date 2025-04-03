from fastapi import APIRouter, HTTPException
from models import ChatImport, MergeChatsRequest
from database import supabase_client
from typing import List
import json
import uuid


chat_router = APIRouter()


@chat_router.get("/get_chats")
async def get_chats():
    response = supabase_client.table("chats").select("*").execute()
    return {"chats": response.data}


# @chat_router.post("/merge_chats")
# async def merge_chats(request: MergeChatsRequest):
#     chat_ids = request.chat_ids  # Extract chat_ids from request object
#     chats = supabase_client.table("chats").select("*").in_("id", chat_ids).execute()
#     merged_content = [msg for chat in chats.data for msg in chat["content"]]
    
#     merged_chat = {"platform": "Hybrid", "format": "text", "content": merged_content}
#     response = supabase_client.table("chats").insert(merged_chat).execute()

#     return {"message": "Chats merged successfully!", "merged_chat_id": response.data[0]["id"]}


@chat_router.post("/merge_chats")
async def merge_chats(request: MergeChatsRequest):
    valid_chat_ids = []
    invalid_chat_ids = []

    # Validate UUIDs
    for chat_id in request.chat_ids:
        try:
            valid_chat_ids.append(str(uuid.UUID(chat_id)))
        except ValueError:
            invalid_chat_ids.append(chat_id)

    if invalid_chat_ids:
        raise HTTPException(
            status_code=400, 
            detail={"error": "Invalid UUIDs detected", "invalid_chat_ids": invalid_chat_ids}
        )

    # Query the database with only valid UUIDs
    chats = supabase_client.table("chats").select("*").in_("id", valid_chat_ids).execute()
    merged_content = [msg for chat in chats.data for msg in chat["content"]]
    
    merged_chat = {"platform": "Hybrid", "format": "text", "content": merged_content}
    response = supabase_client.table("chats").insert(merged_chat).execute()

    return {"message": "Chats merged successfully!", "merged_chat_id": response.data[0]["id"]}

@chat_router.post("/import_chat")
async def import_chat(chat_data: dict):
    if isinstance(chat_data["content"], str):
        chat_data["content"] = json.loads(chat_data["content"])
    if isinstance(chat_data["metadata"], str):
        chat_data["metadata"] = json.loads(chat_data["metadata"])

    # print("Final Chat Data to Insert:", chat_data)
    response = supabase_client.table("chats").insert(chat_data).execute()
    # print("Supabase Response:", response)

    # ✅ Fix: Check response correctly
    if hasattr(response, "data") and response.data is None:
        raise HTTPException(status_code=500, detail="Failed to insert data into Supabase.")

    return {"message": "Chat imported successfully!"}
