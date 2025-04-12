""" 
Authentication and security utilities for ChatSynth.
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required Supabase environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def authenticate_user(email: str, password: str):
    """Authenticate a user with Supabase."""
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if hasattr(res, 'error') and res.error:
            return None
        return res
    except Exception:
        return None

async def get_current_user(token: str):
    """Get the current user from Supabase using the session token."""
    try:
        user = supabase.auth.get_user(token)
        return user
    except Exception:
        return None

async def create_user(email: str, password: str, username: str):
    """Create a new user in Supabase."""
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        })
        if hasattr(res, 'error') and res.error:
            return None
        return res
    except Exception:
        return None
