from .transcript_parser import parse_transcript
from .speaker_personas import create_personas
from ..models import Message

class PodcastSimulator:
    def __init__(self, raw_transcript: str):
        self.speaker_data = parse_transcript(raw_transcript)
        self.personas = create_personas(self.speaker_data)

    def get_response(self, speaker: str, user_msg: str) -> str:
        """
        Simulates conversation with selected speaker
        """
        prompt = f"{self.personas[speaker]}\n\nUser: {user_msg}\n{speaker}:"
        # Here call your language model
        return f"(Simulated) {speaker} replies to: '{user_msg}'"
