"""
Main FastAPI application module for VoxStitch.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .models.user_models import User, UserCreate
from .models.chat import Chat, ChatCreate
from .services.supabase_client import supabase, SUPABASE_JWT_SECRET
from .routes.auth_routes import routes as auth_router
from .routes.chat_routes import routes as chat_router
import jwt
from datetime import datetime
from .routes import podcast_simulator
from .routes.chat_routes import router as chat_router
from app.routes.hybrid_routes import router as hybrid_router
from .routes import chat_routes


# from core.podcast.route import router as podcast_router

app = FastAPI(
    title="VoxStitch API",
    description="Backend API for VoxStitch - AI Chat Log Aggregator",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "VoxStitch API is running!"}

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTH HELPERS ---
def get_current_user(request: Request) -> Optional[User]:
    """Get current user from JWT token in request header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return User(id=payload["sub"], email=payload["email"], username=payload.get("user_metadata", {}).get("username", "unknown"))
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- ROUTES ---

@app.get("/")
async def root():
    return {
        "message": "Welcome to VoxStitch API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/api/chats", response_model=List[Chat])
def get_chats(request: Request):
    """Get all chats for the current user"""
    user = get_current_user(request)
    if not user:
        return []

    res = supabase.table("chats").select("*").eq("user_id", user.id).order("created_at", desc=True).execute()
    if hasattr(res, 'error') and res.error:
        raise HTTPException(status_code=500, detail=str(res.error))
    return res.data

@app.get("/api/chats/{chat_id}", response_model=Chat)
def get_chat(chat_id: str, request: Request):
    """Get a specific chat by ID"""
    user = get_current_user(request)

    query = supabase.table("chats").select("*").eq("id", chat_id)
    if user:
        query = query.eq("user_id", user.id)
    else:
        query = query.is_("user_id", None)
    res = query.single().execute()

    if hasattr(res, 'error') and res.error:
        raise HTTPException(status_code=404, detail="Chat not found")
    return res.data

@app.patch("/api/chats/{chat_id}", response_model=Chat)
def update_chat(chat_id: str, chat_update: ChatCreate, request: Request):
    """Update a chat by ID"""
    user = get_current_user(request)
    chat = supabase.table("chats").select("id", "user_id").eq("id", chat_id).single().execute()

    # Fix: Only check .error if it exists, since some responses may not have it
    if hasattr(chat, "error") and chat.error:
        raise HTTPException(status_code=404, detail="Chat not found")
    if user and (not hasattr(chat, "data") or chat.data["user_id"] != user.id):
        raise HTTPException(status_code=404, detail="Chat not found or unauthorized")

    res = supabase.table("chats").update(chat_update.dict(exclude_unset=True)).eq("id", chat_id).execute()
    # Fix: Only check .error if it exists
    if hasattr(res, "error") and res.error:
        raise HTTPException(status_code=500, detail=str(res.error))
    return res.data[0]

@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: str, request: Request):
    """Delete a chat by ID"""
    user = get_current_user(request)
    chat = supabase.table("chats").select("id", "user_id").eq("id", chat_id).single().execute()

    # Fix: Only check .error if it exists
    if hasattr(chat, "error") and chat.error:
        raise HTTPException(status_code=404, detail="Chat not found or unauthorized")
    if user and (not hasattr(chat, "data") or chat.data["user_id"] != user.id):
        raise HTTPException(status_code=404, detail="Chat not found or unauthorized")

    res = supabase.table("chats").delete().eq("id", chat_id).execute()
    # Fix: Only check .error if it exists
    if hasattr(res, "error") and res.error:
        raise HTTPException(status_code=500, detail=str(res.error))
    return {"message": "Chat deleted"}

# Supabase auth 
@app.post("/api/auth/register")
def register_user(user: UserCreate):
    """Register a new user"""
    try:
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {"username": user.username}
            }
        })
        if hasattr(res, 'error') and res.error:
            raise HTTPException(status_code=400, detail=str(res.error))
        return {"message": "Registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
def login_user(user: UserCreate):
    """Login with email and password"""
    try:
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        if hasattr(res, 'error') and res.error:
            raise HTTPException(status_code=401, detail=str(res.error))
        return {
            "access_token": res.session.access_token,
            "user": {
                "id": res.user.id,
                "email": res.user.email,
                "username": res.user.user_metadata.get("username", "unknown")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Include routers for additional functionality
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chats", tags=["chats"])
app.include_router(podcast_simulator.router, prefix="/api", tags=["podcast"])
app.include_router(hybrid_router, prefix="/api")
app.include_router(chat_routes.router)
app.include_router(chat_router, prefix="/api/chats", tags=["chat-messages"])

# Debug: Print all registered routes

@app.on_event("startup")
async def print_routes():
    print("\n=== REGISTERED ROUTES ===")
    for route in app.routes:
        print(f"{route.methods} {route.path}")
    print("=========================\n")
# print("\n=== REGISTERED ROUTES ===")
# for route in app.routes:
#     print(f"{route.methods} {route.path}")
# print("=========================\n")