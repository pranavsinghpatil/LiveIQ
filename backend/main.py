from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

import models
from database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VoxStitch Backend",
    description="API for managing AI chat logs across multiple platforms",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", 
                  "http://localhost:3003", "http://localhost:3004", "http://localhost:3005",
                  "http://localhost:3006", "http://localhost:3007"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = "your-secret-key"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper Functions
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

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Auth Routes
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/register", response_model=models.User)
def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Chat Routes
@app.post("/api/chats", response_model=models.Chat)
def create_chat(chat: models.ChatCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_chat = models.Chat(**chat.dict(), user_id=current_user.id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@app.get("/api/chats", response_model=List[models.Chat])
def get_chats(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Chat).filter(models.Chat.user_id == current_user.id).all()

@app.get("/api/chats/{chat_id}", response_model=models.Chat)
def get_chat(chat_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id, models.Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@app.patch("/api/chats/{chat_id}", response_model=models.Chat)
def update_chat(chat_id: int, chat_update: models.ChatCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id, models.Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    for field, value in chat_update.dict(exclude_unset=True).items():
        setattr(chat, field, value)
    
    db.commit()
    db.refresh(chat)
    return chat

@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id, models.Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted"}

@app.get("/protected-route")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "You have access to this route"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to VoxStitch Backend!"}
