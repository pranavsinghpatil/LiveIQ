from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, model_validator
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..models.user_models import UserCreate as UserCreateModel, UserRegistrationResponse
from ..services.supabase_client import supabase
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create router
routes = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    disabled: Optional[bool] = None

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_email_or_username(self):
        if not (self.email or self.username):
            raise ValueError('Either email or username must be provided')
        return self

    class Config:
        extra = "forbid"

# Temporary user database with hashed password
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@voxstitch.com",
        "full_name": "Admin User",
        "hashed_password": pwd_context.hash("admin123"),
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@routes.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreateModel):
    """Register a new user with email and password"""
    logger.info(f"Received registration request for user: {user.username}")
    try:
        if user.username in fake_users_db:
            logger.warning(f"Registration failed: Username '{user.username}' already exists in fake_users_db.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

        # Try Supabase registration first
        try:
            res = supabase.auth.sign_up({
                "email": user.email,
                "password": user.password,
                "options": {
                    "data": {"username": user.username}
                }
            })
            if hasattr(res, 'error') and res.error:
                logger.error(f"Supabase registration error: {getattr(res.error, 'message', str(res.error))}")
                logger.error(f"Supabase response: {res}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=getattr(res.error, 'message', str(res.error)))
            logger.info(f"Supabase registration success: user_id={getattr(res.user, 'id', None)} email={getattr(res.user, 'email', None)}")
            logger.debug("RETURNING FINAL RESPONSE ---> %s", {
                "status": "success",
                "message": "User registered successfully",
                "data": {
                    "id": res.user.id,
                    "email": res.user.email,
                    "username": user.username
                }
            })
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "status": "success",
                    "message": "User registered successfully",
                    "data": {
                        "id": res.user.id,
                        "email": res.user.email,
                        "username": user.username
                    }
                }
            )


            # return {
            #     "status": "success",
            #     "message": "User registered successfully",
            #     "data": {
            #         "id": res.user.id,
            #         "email": res.user.email,
            #         "username": user.username
            #     }
            # }
        except Exception as e:
            logger.warning(f"Supabase registration failed, falling back to local: {str(e)}", exc_info=True)

        # Fallback to local registration
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict["id"] = str(len(fake_users_db) + 1)  # Simple ID generation
        user_dict["hashed_password"] = hashed_password
        user_dict["disabled"] = False

        fake_users_db[user.username] = user_dict
        logger.info(f"Successfully registered user: {user.username} (local fallback)")
        return {
            "status": "success",
            "message": "User registered successfully",
            "data": User(**user_dict)
        }
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@routes.post("/login")
async def login_user(user: LoginRequest):
    """Login with email or username and password using Supabase"""
    try:
        if user.email:
            res = supabase.auth.sign_in_with_password({
                "email": user.email,
                "password": user.password
            })
        elif user.username:
            email = None
            if user.username in fake_users_db:
                email = fake_users_db[user.username].get("email")
            else:
                users_resp = supabase.table("users").select("email").eq("username", user.username).execute()
                if users_resp.data and len(users_resp.data) > 0:
                    email = users_resp.data[0]["email"]
            if not email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username not found")
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": user.password
            })
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username required")

        if hasattr(res, 'error') and res.error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(res.error))
        return {
            "status": "success",
            "message": "User logged in successfully",
            "data": {
                "access_token": res.session.access_token,
                "user": {
                    "id": res.user.id,
                    "email": res.user.email,
                    "username": res.user.user_metadata.get("username", "unknown")
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@routes.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get access token using username and password"""
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {
        "status": "success",
        "message": "Access token created",
        "data": {"access_token": access_token, "token_type": "bearer"}
    }

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return User(**user)

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Get current active user"""
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

@routes.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return {
        "status": "success",
        "message": "User profile retrieved",
        "data": current_user
    }

@routes.get("/test")
async def test():
    """Test endpoint to verify router is working"""
    return {"status": "success", "message": "Auth router working"}
