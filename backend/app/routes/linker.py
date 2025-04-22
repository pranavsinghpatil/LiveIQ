from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.ingest.link_importer import import_youtube_transcript

router = APIRouter(prefix="/api/process", tags=["Link Importer"])

class LinkPayload(BaseModel):
    url: str

# Temporarily disable ChatGPT link import for stability
# @router.post("/chatgpt")
# def process_chatgpt_link(payload: LinkPayload):
#     try:
#         content = import_chatgpt_link(payload.url)
#         return {"source": "ChatGPT", "content": content}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/youtube")
def process_youtube_link(payload: LinkPayload):
    try:
        content = import_youtube_transcript(payload.url)
        return {"source": "YouTube", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
