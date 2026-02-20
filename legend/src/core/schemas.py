from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Flashcard(BaseModel):
    front: str = Field(..., description="The question or front side of the card")
    back: str = Field(..., description="The answer or back side of the card")
    tags: List[str] = Field(default_factory=list, description="Tags for the card")

class DeckConfig(BaseModel):
    name: str = Field(..., description="Name of the Anki deck")
    difficulty: Literal["Beginner", "Intermediate", "Advanced"] = "Intermediate"
    style: Literal["Conceptual", "Vocabulary", "Formula", "Mixed"] = "Mixed"
    max_cards: int = Field(default=20, ge=1, le=100)

class GenerationResponse(BaseModel):
    deck_name: str
    cards: List[Flashcard]
