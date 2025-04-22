"""
Simple in-memory DB for chat memory (can replace with Redis or Supabase later)
"""

from typing import Dict, List

# Dict[chat_id, List[Dict[role, content]]]
chat_memory: Dict[str, List[Dict[str, str]]] = {}
thread_memory: Dict[str, List[Dict[str, str]]] = {}
# Dict[hybrid_id, List[chat_ids]]
hybrid_registry: Dict[str, List[str]] = {}

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

def set_context(chat_id: str, messages: List[Dict[str, str]]):
    """Explicitly set context for a given chat"""
    chat_memory[chat_id] = messages

def append_thread(chat_id: str, thread: Dict[str, str]):
    """Append a new thread to the thread memory"""
    if chat_id not in thread_memory:
        thread_memory[chat_id] = []
    thread_memory[chat_id].append(thread)

def get_threads(chat_id: str) -> List[Dict[str, str]]:
    """Get all threads for a given chat"""
    return thread_memory.get(chat_id, [])

def clear_thread_memory(chat_id: str):
    """Clear thread memory for a chat"""
    thread_memory.pop(chat_id, None)

def register_hybrid(hybrid_id: str, chat_ids: List[str]):
    hybrid_registry[hybrid_id] = chat_ids

def get_hybrid_context(hybrid_id: str) -> List[Dict[str, str]]:
    chats = hybrid_registry.get(hybrid_id, [])
    merged = []
    for cid in chats:
        merged.extend(get_context(cid))
    return merged
