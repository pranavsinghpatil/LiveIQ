from ..services.message_service import get_messages_by_chat

def build_context(chat_id: str, max_messages: int = 10) -> str:
    """
    Generates a text context from the latest chat messages.

    Args:
        chat_id: Chat thread ID
        max_messages: How many recent messages to include in context

    Returns:
        A string representing the LLM context
    """
    messages = get_messages_by_chat(chat_id)
    if not messages:
        return ""

    context_lines = []
    for msg in messages[-max_messages:]:  # take last N messages
        role = msg['role']
        content = msg['content']
        context_lines.append(f"{role.capitalize()}: {content.strip()}")

    return "\n".join(context_lines)
