from typing import Dict
from uuid import uuid4
from datetime import datetime

# Dict[thread_id, thread_data]
thread_db: Dict[str, dict] = {}

def create_thread(title: str, chat_ids: list[str]) -> dict:
    thread_id = str(uuid4())
    thread = {
        "id": thread_id,
        "title": title,
        "chat_ids": chat_ids,
        "created_at": datetime.utcnow()
    }
    thread_db[thread_id] = thread
    return thread

def get_thread(thread_id: str) -> dict:
    return thread_db.get(thread_id)

def list_threads() -> list:
    return list(thread_db.values())

def update_thread(thread_id: str, data: dict) -> dict:
    if thread_id not in thread_db:
        return None
    thread_db[thread_id].update(data)
    return thread_db[thread_id]

def delete_thread(thread_id: str) -> bool:
    return thread_db.pop(thread_id, None) is not None
