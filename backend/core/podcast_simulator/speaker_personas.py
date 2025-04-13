from typing import Dict

def create_personas(speaker_data: Dict[str, list]) -> Dict[str, str]:
    """
    Generates prompt-style persona descriptions from speakers' text
    """
    personas = {}

    for speaker, quotes in speaker_data.items():
        sample = " ".join(quotes[:5])
        personas[speaker] = f"""
        You are {speaker}, based on these quotes: "{sample}".
        Respond in the same tone, mannerisms, and knowledge.
        """
    
    return personas
