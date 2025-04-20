from .llm_client import chat, set_api_key
from .llm_models import LLMChatRequest, LLMChatResponse, APIKeyUpdate, LLMModelMetadata
from core.db.memory import get_context, append_to_context
from .llm_models import LLMChatRequest, LLMChatResponse

def generate_llm_response(payload: LLMChatRequest) -> LLMChatResponse:
    # Get chat_id from first message if sent
    chat_id = payload.chat_id or "default"

    # Load memory from in-memory DB
    history = get_context(chat_id)

    # Add new message
    for m in payload.messages:
        history.append(m.dict())

    # Send full history to LLM
    reply = chat(
        messages=history,
        provider=payload.provider,
        model=payload.model
    )

    # Append assistant reply to memory
    append_to_context(chat_id, {"role": "assistant", "content": reply})

    return LLMChatResponse(reply=reply)


def update_api_key(payload: APIKeyUpdate) -> dict:
    set_api_key(payload.provider, payload.api_key)
    return {"status": "updated", "provider": payload.provider}

def get_supported_models() -> list[LLMModelMetadata]:
    return [
        LLMModelMetadata(name="gpt-3.5-turbo", provider="openai", description="OpenAI's fast & cheap model"),
        LLMModelMetadata(name="gpt-4", provider="openai", description="OpenAI's best model"),
        LLMModelMetadata(name="claude-3-opus-20240229", provider="anthropic", description="Claude's best reasoning model"),
        LLMModelMetadata(name="gemini-1.5-pro", provider="google", description="Google’s flagship model"),
        LLMModelMetadata(name="mistral-large-latest", provider="mistral", description="Open-weight, performant"),
        LLMModelMetadata(name="deepseek-chat", provider="deepseek", description="Highly capable open model")
    ]
