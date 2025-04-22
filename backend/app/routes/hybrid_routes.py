# routes/hybrid_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.services.hybrid_service import create_hybrid_chat, get_hybrid_context
from ..services.llm_reply_service import get_hybrid_reply
from typing import Optional

# Remove prefix here; let main.py handle the prefix
router = APIRouter(tags=["hybrid"])

class HybridCreateRequest(BaseModel):
    user_id: str
    chat_ids: list[str]
    title: str

class HybridReplyRequest(BaseModel):
    hybrid_id: str
    user_input: str
    provider: Optional[str] = "google"  # Default LLM
    model: Optional[str] = None

@router.post("/create")
async def create_hybrid(request: HybridCreateRequest):
    try:
        hybrid_id = create_hybrid_chat(
            user_id=request.user_id,
            title=request.title,
            source_chat_ids=request.chat_ids
        )
        return {
            "status": "success",
            "hybrid_chat_id": hybrid_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/context/{hybrid_id}")
async def get_context(hybrid_id: str):
    try:
        context = get_hybrid_context(hybrid_id)
        return {
            "status": "success",
            "context": context
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/reply")
async def hybrid_chat_reply(request: HybridReplyRequest):
    try:
        response = get_hybrid_reply(
            hybrid_id=request.hybrid_id,
            user_message=request.user_input,
            provider=request.provider,
            model=request.model
        )
        return {
            "status": "success",
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
