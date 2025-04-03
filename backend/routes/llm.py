from fastapi import APIRouter, HTTPException
import requests
import os

llm_router = APIRouter()

GEMINI_API = os.getenv("GOOGLE_GEMINI_API")
CHATGPT_API = os.getenv("CHATGPT_API")

@llm_router.post("/chat_response")
async def chat_response(chat_id: str, model: str = "gemini"):
    chat_data = supabase_client.table("chats").select("*").eq("id", chat_id).execute().data
    
    if not chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")

    prompt = " ".join(chat_data[0]["content"])

    if model == "gemini":
        api_url = f"https://gemini-api-url.com/generate?api_key={GEMINI_API}"
    elif model == "chatgpt":
        api_url = f"https://chatgpt-api-url.com/generate?api_key={CHATGPT_API}"
    else:
        raise HTTPException(status_code=400, detail="Unsupported model")

    response = requests.post(api_url, json={"prompt": prompt})

    return {"response": response.json()}
