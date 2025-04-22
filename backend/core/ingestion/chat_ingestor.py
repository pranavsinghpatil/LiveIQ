from typing import Optional, Dict, Any
from datetime import datetime
import os, traceback, logging
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from app.utils.html_chat_parser import parse_chatgpt_html, detect_html_chat_source

logger = logging.getLogger(__name__)


def extract_youtube_id(url: str) -> Optional[str]:
    parsed = urlparse(url)
    if parsed.hostname and "youtube" in parsed.hostname:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif parsed.hostname and "youtu.be" in parsed.hostname:
        return parsed.path.strip("/")
    return None

def get_youtube_transcript(video_id: str) -> str:
    try:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        except:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi"])
        return " ".join([x["text"] for x in transcript])
    except Exception as e:
        raise ValueError("Failed to fetch transcript: " + str(e))

class ChatIngestor:
    async def ingest_text(self, content: str) -> Dict:
        return {
            "content": content,
            "media_type": "text",
            "created_at": datetime.utcnow().isoformat()
        }

    async def ingest_pdf(self, file_path: str) -> Dict:
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in doc])
        return {
            "content": text,
            "media_type": "pdf",
            "created_at": datetime.utcnow().isoformat()
        }

    async def ingest_image(self, file_path: str) -> Dict:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return {
            "content": text,
            "media_type": "image",
            "created_at": datetime.utcnow().isoformat()
        }

    async def ingest_youtube(self, url: str) -> Dict:
        vid = extract_youtube_id(url)
        if not vid:
            raise ValueError("Invalid YouTube link")
        text = get_youtube_transcript(vid)
        return {
            "content": text,
            "media_type": "youtube",
            "created_at": datetime.utcnow().isoformat()
        }

    async def ingest_html(self, file_path: str) -> Dict:
        source = detect_html_chat_source(file_path)
        if source == "chatgpt":
            history = parse_chatgpt_html(file_path)
            text = "\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in history])
            return {
                "content": text.strip(),
                "media_type": "chatgpt_html",
                "metadata": {"source": "ChatGPT HTML"},
                "created_at": datetime.utcnow().isoformat()
            }
        # Future: Add more parsers for other platforms (gemini, claude, grok, etc.)
        else:
            # fallback: just extract all text
            with open(file_path, "r", encoding="utf-8") as f:
                raw = f.read()
            return {
                "content": raw,
                "media_type": f"{source}_html" if source != "unknown" else "html",
                "metadata": {"source": source},
                "created_at": datetime.utcnow().isoformat()
            }

    async def ingest_file(self, file_path: str, ext: str) -> Dict[str, Any]:
        ext = ext.lower()
        if ext == "pdf":
            return await self.ingest_pdf(file_path)
        elif ext in ["png", "jpg", "jpeg"]:
            return await self.ingest_image(file_path)
        elif ext in ["html", "htm"]:
            return await self.ingest_html(file_path)
        elif ext in ["txt", "md", "json"]:
            with open(file_path, "r", encoding="utf-8") as f:
                return await self.ingest_text(f.read())
        else:
            raise ValueError(f"Unsupported file type: {ext}")

chat_ingestor = ChatIngestor()
