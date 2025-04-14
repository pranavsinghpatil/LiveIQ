from fastapi import APIRouter, Body
from core.podcast_simulator.podcast_simulator import PodcastSimulator
from app.services.podcast_simulator import TranscriptUpload, ChatRequest

router = APIRouter(
    prefix="/podcast",
    tags=["Podcast"]
)

# Temporary global for simplicity (use DI in full app)
simulator_instance = None

@router.post("/upload/")
def upload_transcript(payload: TranscriptUpload):
    """Upload and process a podcast transcript"""
    global simulator_instance
    try:
        simulator_instance = PodcastSimulator(payload.raw_transcript)
        return {
            "status": "success", 
            "message": "Transcript uploaded and processed", 
            "speakers": list(simulator_instance.speaker_data.keys())
        }
    except Exception as e:
        return {"status": "error", "message": f"Error processing transcript: {str(e)}"}

@router.post("/chat/")
def chat_with_speaker(payload: ChatRequest):
    """Chat with a specific speaker from the podcast"""
    global simulator_instance
    if not simulator_instance:
        return {"status": "error", "message": "Upload transcript first."}
    
    try:
        response = simulator_instance.get_response(payload.speaker, payload.user_msg)
        return {"status": "success", "speaker": payload.speaker, "response": response}
    except Exception as e:
        return {"status": "error", "message": f"Error getting response: {str(e)}"}

@router.post("/test/")
def test(payload: dict):
    """Test endpoint to verify router is working"""
    return {"status": "success", "you_sent": payload}
