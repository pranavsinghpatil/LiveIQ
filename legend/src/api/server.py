from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import shutil
import os
import tempfile
from dotenv import load_dotenv

from src.core.llm import get_llm_client
from src.core.generator import FlashcardGenerator
from src.core.schemas import DeckConfig
from src.core.anki import AnkiDeckBuilder

load_dotenv()

app = FastAPI(title="MeshCards API", version="0.1.0")

@app.post("/generate")
async def generate_deck(
    file: UploadFile = File(...),
    provider: str = Form("gemini"),
    model: Optional[str] = Form(None),
    deck_name: str = Form("MeshCards Deck"),
    difficulty: str = Form("Intermediate"),
    style: str = Form("Mixed"),
    max_cards: int = Form(20)
):
    # 1. Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name

    try:
        # 2. Read content (assuming text for now)
        # TODO: Add PDF parsing support
        with open(tmp_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 3. Initialize LLM
        api_key = os.getenv(f"{provider.upper()}_API_KEY")
        if provider != "ollama" and not api_key:
             raise HTTPException(status_code=500, detail=f"{provider.upper()}_API_KEY not set")
        
        llm_client = get_llm_client(provider, api_key, model)
        generator = FlashcardGenerator(llm_client)

        # 4. Generate Cards
        config = DeckConfig(
            name=deck_name,
            difficulty=difficulty,
            style=style,
            max_cards=max_cards
        )
        cards = generator.generate_flashcards(text, config)

        # 5. Create .apkg
        builder = AnkiDeckBuilder()
        output_filename = f"{deck_name.replace(' ', '_')}.apkg"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)
        builder.create_apkg(cards, deck_name, output_path)

        # 6. Return file
        return FileResponse(
            output_path, 
            media_type="application/octet-stream", 
            filename=output_filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
