"""
Simple in-memory DB for chat memory (can replace with Redis or Supabase later)
"""

from typing import Dict, List

# Dict[chat_id, List[Dict[role, content]]]
chat_memory: Dict[str, List[Dict[str, str]]] = {}

def get_context(chat_id: str) -> List[Dict[str, str]]:
    """Get full chat history for a given chat"""
    return chat_memory.get(chat_id, [])

def append_to_context(chat_id: str, message: Dict[str, str]):
    """Append a new message to the chat memory"""
    if chat_id not in chat_memory:
        chat_memory[chat_id] = []
    chat_memory[chat_id].append(message)

def clear_context(chat_id: str):
    """Clear memory for a chat"""
    chat_memory.pop(chat_id, None)

# --------------------- FOR PODCAST -------------------------------
def set_context(chat_id: str, messages: List[Dict[str, str]]):
    """Explicitly set context for a given chat"""
    chat_memory[chat_id] = messages
