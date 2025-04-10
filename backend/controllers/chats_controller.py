from backend.models import ChatUpload
from datetime import datetime
import uuid
from backend.supabase_Client import supabase

def upload_chat(chat_data: ChatUpload):
    chat_id = str(uuid.uuid4())
    payload = {
        "id": chat_id,
        "user_id": chat_data.user_id,
        "title": chat_data.title,
        "content": chat_data.content,
        "media_type": chat_data.media_type,
        "created_at": chat_data.created_at or datetime.utcnow()
    }

    response = supabase.table("chats").insert(payload).execute()
    return response
