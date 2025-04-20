# core/services/hybrid_service.py

from supabase import Client
from app.models.hybrid_models import HybridCreate, Hybrid
from datetime import datetime
import uuid
from app.services.supabase_client import supabase

class HybridService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_hybrid(self, hybrid_data: HybridCreate):
        new_id = str(uuid.uuid4())
        payload = {
            "id": new_id,
            "title": hybrid_data.title,
            "chat_ids": hybrid_data.chat_ids,
            "user_id": hybrid_data.user_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        res = self.supabase.table("hybrids").insert(payload).execute()
        if hasattr(res, "status_code") and res.status_code >= 400:
            raise Exception(getattr(res, "data", "Unknown error"))
        return getattr(res, "data", res)

    def get_all_hybrids(self, user_id: str):
        res = self.supabase.table("hybrids").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        if hasattr(res, "status_code") and res.status_code >= 400:
            raise Exception(getattr(res, "data", "Unknown error"))
        return getattr(res, "data", res)

    def get_hybrid_by_id(self, hybrid_id: str, user_id: str):
        res = self.supabase.table("hybrids").select("*").eq("id", hybrid_id).eq("user_id", user_id).single().execute()
        if hasattr(res, "status_code") and res.status_code >= 400:
            raise Exception(getattr(res, "data", "Unknown error"))
        return getattr(res, "data", res)

    def delete_hybrid(self, hybrid_id: str, user_id: str):
        res = self.supabase.table("hybrids").delete().eq("id", hybrid_id).eq("user_id", user_id).execute()
        if hasattr(res, "status_code") and res.status_code >= 400:
            raise Exception(getattr(res, "data", "Unknown error"))
        return {"message": "Hybrid deleted successfully"}

_hybrid_service = HybridService(supabase)

def create_hybrid_chat(user_id: str, title: str, source_chat_ids: list[str]):
    from app.models.hybrid_models import HybridCreate
    hybrid_data = HybridCreate(user_id=user_id, title=title, chat_ids=source_chat_ids)
    result = _hybrid_service.create_hybrid(hybrid_data)
    # result may be a list, dict, or other type depending on supabase-py version
    if isinstance(result, dict) and "id" in result:
        return result["id"]
    elif isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "id" in result[0]:
        return result[0]["id"]
    return result

def get_hybrid_context(hybrid_id: str):
    # Fetch the hybrid chat record from Supabase
    res = supabase.table("hybrids").select("*").eq("id", hybrid_id).single().execute()
    if hasattr(res, "status_code") and res.status_code >= 400:
        raise Exception(getattr(res, "data", "Unknown error"))
    return getattr(res, "data", res)
