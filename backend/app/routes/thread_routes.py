from fastapi import APIRouter, HTTPException
from app.models.thread_models import Thread, ThreadCreate, ThreadUpdate
from core.services.thread_service import handle_create_thread, handle_get_thread, handle_list_threads, handle_update_thread, handle_delete_thread

router = APIRouter(prefix="/api/threads", tags=["Threads"])

@router.post("/", response_model=Thread)
def create_thread(payload: ThreadCreate):
    return thread_service.handle_create_thread(payload)

@router.get("/", response_model=list[Thread])
def list_all_threads():
    return thread_service.handle_list_threads()

@router.get("/{thread_id}", response_model=Thread)
def get_thread(thread_id: str):
    thread = thread_service.handle_get_thread(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

@router.patch("/{thread_id}", response_model=Thread)
def update_thread(thread_id: str, payload: ThreadUpdate):
    updated = thread_service.handle_update_thread(thread_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Thread not found or update failed")
    return updated

@router.delete("/{thread_id}")
def delete_thread(thread_id: str):
    success = thread_service.handle_delete_thread(thread_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {"status": "deleted"}
