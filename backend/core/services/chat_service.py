"""
Chat Service: Handles context-aware chat logic using the LLM client.
"""

from typing import List, Optional
from core.llm.llm_client import chat as chat_with_llm, Message, ModelProvider

# 🧠 In-memory "chat sessions" for now
chat_contexts: dict[str, List[Message]] = {}

def send_message(
    chat_id: str,
    user_input: str,
    provider: str = "google",
    model: Optional[str] = None
) -> str:
    """
    Handle chat message, append to history, and get LLM response.
    """

    # Initialize if new chat
    if chat_id not in chat_contexts:
        chat_contexts[chat_id] = []

    # Add user input to chat history
    chat_contexts[chat_id].append(Message(role="user", content=user_input))

    # Call LLM
    response_text = chat_with_llm(
        messages=chat_contexts[chat_id],
        provider=provider,
        model=model
    )

    # Add response to context
    chat_contexts[chat_id].append(Message(role="assistant", content=response_text))

    return response_text


def get_history(chat_id: str) -> List[dict]:
    """Return chat history for debugging (optional)."""
    return [m.to_dict() for m in chat_contexts.get(chat_id, [])]
