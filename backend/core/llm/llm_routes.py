from fastapi import APIRouter
from .llm_models import LLMChatRequest, LLMChatResponse, APIKeyUpdate, LLMModelMetadata, LLMThreadRequest, LLMThreadResponse, HybridCreateRequest, HybridChatRequest
from .llm_service import generate_llm_response, update_api_key, get_supported_models, generate_thread_response, generate_hybrid_reply
from core.db.memory import register_hybrid

# Remove prefix here; let main.py handle the prefix
router = APIRouter(tags=["LLM"])

@router.post("/chat", response_model=LLMChatResponse)
def llm_chat(request: LLMChatRequest):
    return generate_llm_response(request)

@router.post("/thread", response_model=LLMThreadResponse)
def create_thread(request: LLMThreadRequest):
    return generate_thread_response(request)

@router.post("/hybrid/register")
def register_hybrid_api(payload: HybridCreateRequest):
    register_hybrid(payload.hybrid_id, payload.chat_ids)
    return {"status": "registered", "hybrid_id": payload.hybrid_id}

@router.post("/hybrid/chat", response_model=LLMChatResponse)
def hybrid_chat(payload: HybridChatRequest):
    return generate_hybrid_reply(payload)

@router.post("/set-key")
def set_user_api_key(payload: APIKeyUpdate):
    return update_api_key(payload)

@router.get("/models", response_model=list[LLMModelMetadata])
def list_supported_models():
    return get_supported_models()
