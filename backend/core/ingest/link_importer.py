# --- YOUTUBE TRANSCRIPT IMPORT ---
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_youtube_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    if parsed.hostname == "youtu.be":
        return parsed.path.strip("/")
    return None

# Stable, single export for YouTube transcript import

def import_youtube_transcript(url: str) -> str:
    video_id = extract_youtube_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
    try:
        # Try English transcript first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except Exception:
        # Fallback: try Hindi (auto-generated)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        except Exception as e:
            raise ValueError(f"Could not retrieve YouTube transcript: {e}")
    return " ".join([item["text"] for item in transcript])
