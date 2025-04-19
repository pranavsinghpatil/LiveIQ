# core/services/hybrid_service.py

from supabase import Client
from app.models.hybrid_models import HybridCreate, Hybrid
from datetime import datetime
import uuid

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
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        res = self.supabase.table("hybrids").insert(payload).execute()
        if res.error:
            raise Exception(res.error.message)
        return res.data[0]

    def get_all_hybrids(self, user_id: str):
        res = self.supabase.table("hybrids").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        if res.error:
            raise Exception(res.error.message)
        return res.data

    def get_hybrid_by_id(self, hybrid_id: str, user_id: str):
        res = self.supabase.table("hybrids").select("*").eq("id", hybrid_id).eq("user_id", user_id).single().execute()
        if res.error:
            raise Exception(res.error.message)
        return res.data

    def delete_hybrid(self, hybrid_id: str, user_id: str):
        res = self.supabase.table("hybrids").delete().eq("id", hybrid_id).eq("user_id", user_id).execute()
        if res.error:
            raise Exception(res.error.message)
        return {"message": "Hybrid deleted successfully"}
