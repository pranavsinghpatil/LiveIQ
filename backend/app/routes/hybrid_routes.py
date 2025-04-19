# routes/hybrid_routes.py

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from app.models.hybrid_models import HybridCreate, Hybrid
from core.services.hybrid_service import HybridService
from app.services.supabase_client import supabase
from app.models.user_models import User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/hybrids", tags=["Hybrids"])
hybrid_service = HybridService(supabase)

@router.post("", response_model=Hybrid)
def create_hybrid(hybrid_data: HybridCreate, user: User = Depends(get_current_user)):
    try:
        return hybrid_service.create_hybrid(hybrid_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Hybrid])
def get_hybrids(user: User = Depends(get_current_user)):
    try:
        return hybrid_service.get_all_hybrids(user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{hybrid_id}", response_model=Hybrid)
def get_hybrid(hybrid_id: str, user: User = Depends(get_current_user)):
    try:
        return hybrid_service.get_hybrid_by_id(hybrid_id, user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{hybrid_id}")
def delete_hybrid(hybrid_id: str, user: User = Depends(get_current_user)):
    try:
        return hybrid_service.delete_hybrid(hybrid_id, user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
