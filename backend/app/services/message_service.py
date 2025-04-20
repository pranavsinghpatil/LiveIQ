from ..services.supabase_client import supabase
from ..models.chat import ChatMessage
from uuid import uuid4
from datetime import datetime

def insert_message(message: ChatMessage):
    # Ensure timestamp is ISO string for Supabase/JSON compatibility
    payload = {
        "id": str(uuid4()),
        "chat_id": message.chat_id,
        "role": message.role,
        "content": message.content,
        "timestamp": message.timestamp.isoformat() if message.timestamp else None,
    }

    response = supabase.table("chats_messages").insert(payload).execute()
    # Add more detailed error logging for debugging
    if hasattr(response, 'error') and response.error:
        import logging
        logging.error(f"Supabase insert error: {response.error}")
        logging.error(f"Supabase response: {response}")
        raise Exception(f"Error inserting message: {response.error}")
    if hasattr(response, 'status_code') and response.status_code == 404:
        import logging
        logging.error(f"Supabase 404 error: Table 'chats_messages' may not exist or is misspelled.")
        logging.error(f"Supabase response: {response}")
        raise Exception("Supabase 404 error: Table 'chats_messages' may not exist or is misspelled.")
    return response.data

def get_messages_by_chat(chat_id: str):
    # Fix: Supabase Python client expects 'desc' boolean, not 'asc' keyword
    response = supabase.from_("chats_messages").select("*").eq("chat_id", chat_id).order("timestamp", desc=False).execute()
    # Fix: Only check .error if it exists on the response object
    if hasattr(response, 'error') and response.error:
        raise Exception(f"Error fetching messages: {response.error}")
    return response.data

def save_message(chat_id: str, user_id: str, role: str, content: str, timestamp=None):
    """
    Save a message to the chats_messages table. Used for both user and assistant messages.
    """
    from uuid import uuid4
    payload = {
        "id": str(uuid4()),
        "chat_id": chat_id,
        "user_id": user_id,
        "role": role,
        "content": content,
        "timestamp": (timestamp or datetime.utcnow()).isoformat(),
    }
    response = supabase.table("chats_messages").insert(payload).execute()
    if hasattr(response, 'error') and response.error:
        import logging
        logging.error(f"Supabase insert error: {response.error}")
        logging.error(f"Supabase response: {response}")
        raise Exception(f"Error inserting message: {response.error}")
    return response.data
