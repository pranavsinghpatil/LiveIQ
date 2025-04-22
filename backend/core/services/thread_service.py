from core.db.thread_store import create_thread, get_thread, list_threads, update_thread, delete_thread
from app.models.thread_models import ThreadCreate, ThreadUpdate

def handle_create_thread(payload: ThreadCreate) -> dict:
    return create_thread(payload.title, payload.chat_ids)

def handle_get_thread(thread_id: str) -> dict:
    return get_thread(thread_id)

def handle_list_threads() -> list:
    return list_threads()

def handle_update_thread(thread_id: str, payload: ThreadUpdate) -> dict:
    return update_thread(thread_id, payload.dict(exclude_unset=True))

def handle_delete_thread(thread_id: str) -> bool:
    return delete_thread(thread_id)
