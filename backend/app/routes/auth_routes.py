from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user_models import UserCreate, User, UserOut
from app.services.auth_service import authenticate_user, create_user, get_current_user, oauth2_scheme

auth_router = APIRouter()

# Security configuration
SECRET_KEY = "your-secret-key"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@auth_router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    """Register a new user."""
    result = await create_user(user.email, user.password, user.username)
    if not result:
        raise HTTPException(status_code=400, detail="Registration failed")
    
    return UserOut(
        id=result.user.id,
        email=result.user.email,
        username=result.user.user_metadata.get("username", "unknown")
    )

@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token."""
    result = await authenticate_user(form_data.username, form_data.password)
    if not result:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": result.session.access_token,
        "token_type": "bearer"
    }

@auth_router.get("/me", response_model=UserOut)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """Get current user profile."""
    user = await get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return UserOut(
        id=user.user.id,
        email=user.user.email,
        username=user.user.user_metadata.get("username", "unknown")
    )

@auth_router.get("/test")
def test():
    return {"msg": "router working"}
