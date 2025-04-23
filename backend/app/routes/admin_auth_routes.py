from fastapi import APIRouter, HTTPException, status
from app.services.supabase_admin import register_user_admin_api
from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional

router = APIRouter(prefix="/api/admin", tags=["admin-auth"])

class AdminRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

class AdminLoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_email_or_username(cls, values):
        if not (values.get('email') or values.get('username')):
            raise ValueError('Either email or username must be provided')
        return values

    class Config:
        extra = "forbid"

@router.post("/register", status_code=status.HTTP_201_CREATED)
def admin_register(request: AdminRegisterRequest):
    """Admin-level registration (rate-limit free, uses service role key)"""
    try:
        user = register_user_admin_api(request.email, request.password, request.username)
        return {"status": "success", "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def admin_login(request: AdminLoginRequest):
    """Admin login with either email or username (for admin testing)"""
    # This is a stub. Integrate with Supabase admin login if needed.
    # For now, just echo back the input for confirmation.
    return {"status": "success", "data": {"email": request.email, "username": request.username}}
