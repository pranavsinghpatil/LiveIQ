from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from typing import List, Optional
from .models.chat_models import Chat, ChatCreate
from .models.user_models import User, UserCreate
from datetime import datetime
import os
import jwt
from dotenv import load_dotenv
from .routes.auth_routes import auth_router  
from routes.chat_routes import router as chat_router

load_dotenv()

# Supabase Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Using the anon key for client operations
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required Supabase environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="VoxStitch Backend",
    description="Backend API for VoxStitch chat aggregator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTH HELPERS ---
def get_current_user(request: Request) -> Optional[User]:
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
    return {"message": "Welcome to VoxStitch Backend!"}

@app.get("/api/chats", response_model=List[Chat])
def get_chats(request: Request):
    user = get_current_user(request)
    if not user:
        return []

    res = supabase.from_("chats").select("*").eq("user_id", user.id).order("created_at", desc=True).execute()
    if res.error:
        raise HTTPException(status_code=500, detail=str(res.error))
    return res.data

@app.get("/api/chats/{chat_id}", response_model=Chat)
def get_chat(chat_id: str, request: Request):
    user = get_current_user(request)

    query = supabase.from_("chats").select("*").eq("id", chat_id)
    if user:
        query = query.eq("user_id", user.id)
    else:
        query = query.is_("user_id", None)
    res = query.single().execute()

    if res.error:
        raise HTTPException(status_code=404, detail="Chat not found")
    return res.data

@app.patch("/api/chats/{chat_id}", response_model=Chat)
def update_chat(chat_id: str, chat_update: ChatCreate, request: Request):
    user = get_current_user(request)
    chat = supabase.from_("chats").select("id", "user_id").eq("id", chat_id).single().execute()

    if chat.error or (user and chat.data["user_id"] != user.id):
        raise HTTPException(status_code=404, detail="Chat not found or unauthorized")

    res = supabase.from_("chats").update(chat_update.dict(exclude_unset=True)).eq("id", chat_id).execute()
    if res.error:
        raise HTTPException(status_code=500, detail=str(res.error))
    return res.data[0]

@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: str, request: Request):
    user = get_current_user(request)
    chat = supabase.from_("chats").select("id", "user_id").eq("id", chat_id).single().execute()

    if chat.error or (user and chat.data["user_id"] != user.id):
        raise HTTPException(status_code=404, detail="Chat not found or unauthorized")

    res = supabase.from_("chats").delete().eq("id", chat_id).execute()
    if res.error:
        raise HTTPException(status_code=500, detail=str(res.error))
    return {"message": "Chat deleted"}

# Supabase auth 
@app.post("/api/auth/register")
def register_user(user: UserCreate):
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

# Include chat routes
# app.include_router(chats.router, prefix="/api/chats", tags=["chats"])
# app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/api", tags=["Chat"])