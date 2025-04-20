from memory_db import chat_memory
from core.llm.llm_client import chat
from core.services.hybrid_service import get_hybrid_context

def get_hybrid_reply(hybrid_id: str, user_message: str, provider: str = "google", model: str = None):
    # Get combined chat history
    history = get_hybrid_context(hybrid_id)

    # Add current user message
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages += [{"role": "user", "content": msg} for msg in history]
    messages.append({"role": "user", "content": user_message})

    # Call the LLM
    reply = chat(messages, provider=provider, model=model)

    # Update memory
    chat_memory[hybrid_id].append(user_message)
    chat_memory[hybrid_id].append(reply)

    return reply
