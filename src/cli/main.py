import typer
import os
from dotenv import load_dotenv
from src.core.llm import get_llm_client
from src.core.generator import FlashcardGenerator
from src.core.schemas import DeckConfig
from src.core.anki import AnkiDeckBuilder

load_dotenv()

app = typer.Typer()

@app.command()
def generate(
    input_file: str = typer.Argument(..., help="Path to the input text file"),
    output: str = typer.Option("output.apkg", help="Path to the output .apkg file"),
    provider: str = typer.Option("gemini", help="LLM provider: gemini, openai, anthropic, ollama"),
    model: str = typer.Option(None, help="Model name (for Ollama)"),
    deck_name: str = typer.Option("MeshCards Deck", help="Name of the Anki deck"),
    difficulty: str = typer.Option("Intermediate", help="Difficulty: Beginner, Intermediate, Advanced"),
    style: str = typer.Option("Mixed", help="Style: Conceptual, Vocabulary, Formula, Mixed"),
    max_cards: int = typer.Option(20, help="Maximum number of cards to generate")
):
    """
    Generate Anki flashcards from a text file.
    """
    if not os.path.exists(input_file):
        typer.echo(f"Error: Input file '{input_file}' not found.")
        raise typer.Exit(code=1)

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Get API key from env
    api_key = os.getenv(f"{provider.upper()}_API_KEY")
    if provider != "ollama" and not api_key:
        typer.echo(f"Error: {provider.upper()}_API_KEY environment variable not set.")
        raise typer.Exit(code=1)

    typer.echo(f"Initializing {provider} client...")
    try:
        llm_client = get_llm_client(provider, api_key, model)
    except Exception as e:
        typer.echo(f"Error initializing LLM client: {e}")
        raise typer.Exit(code=1)

    generator = FlashcardGenerator(llm_client)
    config = DeckConfig(
        name=deck_name,
        difficulty=difficulty,
        style=style,
        max_cards=max_cards
    )

    typer.echo("Generating flashcards...")
    try:
        cards = generator.generate_flashcards(text, config)
        typer.echo(f"Generated {len(cards)} cards.")
    except Exception as e:
        typer.echo(f"Error generating cards: {e}")
        raise typer.Exit(code=1)

    typer.echo("Creating Anki deck...")
    builder = AnkiDeckBuilder()
    builder.create_apkg(cards, deck_name, output)
    
    typer.echo(f"Success! Deck saved to {output}")

if __name__ == "__main__":
    app()
