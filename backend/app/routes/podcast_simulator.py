from fastapi import APIRouter, Body
from core.podcast_simulator.podcast_simulator import PodcastSimulator
from app.services.podcast_simulator import TranscriptUpload, ChatRequest

router = APIRouter()

# Temporary global for simplicity (use DI in full app)
simulator_instance = None

@router.post("/podcast/upload/")
def upload_transcript(raw_transcript: str = Body(...)):
    global simulator_instance
    simulator_instance = PodcastSimulator(raw_transcript)
    return {"status": "Transcript uploaded and processed", "speakers": list(simulator_instance.speaker_data.keys())}

@router.post("/podcast/chat/")
def chat_with_speaker(speaker: str = Body(...), user_msg: str = Body(...)):
    if not simulator_instance:
        return {"error": "Upload transcript first."}
    
    response = simulator_instance.get_response(speaker, user_msg)
    return {"speaker": speaker, "response": response}

@router.post("/podcast/upload/")
def upload_transcript(payload: TranscriptUpload):
    global simulator_instance
    simulator_instance = PodcastSimulator(payload.raw_transcript)
    return {
        "status": "Transcript uploaded and processed",
        "speakers": list(simulator_instance.speaker_data.keys())
    }

@router.post("/podcast/chat/")
def chat_with_speaker(payload: ChatRequest):
    if not simulator_instance:
        return {"error": "Upload transcript first."}
    
    response = simulator_instance.get_response(payload.speaker, payload.user_msg)
    return {"speaker": payload.speaker, "response": response}
