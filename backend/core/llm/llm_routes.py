from fastapi import APIRouter
from .llm_models import LLMChatRequest, LLMChatResponse, APIKeyUpdate, LLMModelMetadata
from .llm_service import generate_llm_response, update_api_key, get_supported_models

router = APIRouter(prefix="/api/llm", tags=["LLM"])

@router.post("/chat", response_model=LLMChatResponse)
def llm_chat(request: LLMChatRequest):
    return generate_llm_response(request)

@router.post("/set-key")
def set_user_api_key(payload: APIKeyUpdate):
    return update_api_key(payload)

@router.get("/models", response_model=list[LLMModelMetadata])
def list_supported_models():
    return get_supported_models()
