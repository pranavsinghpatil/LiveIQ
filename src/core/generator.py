from typing import List
from .schemas import Flashcard, DeckConfig, GenerationResponse
from .llm import LLMClient

class FlashcardGenerator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate_flashcards(self, text: str, config: DeckConfig) -> List[Flashcard]:
        prompt = self._build_prompt(text, config)
        response_json = self.llm_client.generate_json(prompt)
        
        # Validate against schema
        generation_response = GenerationResponse(**response_json)
        return generation_response.cards

    def _build_prompt(self, text: str, config: DeckConfig) -> str:
        return f"""
        You are an expert tutor helping a student create Anki flashcards.
        
        **Goal**: Create a list of high-quality flashcards from the provided text.
        
        **Configuration**:
        - Difficulty: {config.difficulty}
        - Style: {config.style}
        - Max Cards: {config.max_cards}
        
        **Instructions**:
        1. Extract the most important concepts, definitions, and relationships.
        2. Create Question/Answer pairs.
        3. Ensure the answer is concise but complete.
        4. Add relevant tags (e.g., topic, concept type).
        5. Output MUST be valid JSON matching this schema:
        {{
            "deck_name": "{config.name}",
            "cards": [
                {{
                    "front": "Question here",
                    "back": "Answer here",
                    "tags": ["tag1", "tag2"]
                }}
            ]
        }}

        **Source Text**:
        {text}
        """
