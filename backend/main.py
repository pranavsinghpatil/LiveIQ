from fastapi import FastAPI
from routes.chats import chat_router

app = FastAPI()
app.include_router(chat_router, prefix="/api")
