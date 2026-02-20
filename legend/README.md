# MeshCards

MeshCards is a tool to generate Anki flashcards (`.apkg`) from personal notes using LLMs.

## Features

- **Personalized Generation**: Create cards from your own notes.
- **Multi-Provider Support**: Works with Gemini, OpenAI, Anthropic, and Ollama.
- **Direct Export**: Generates `.apkg` files ready for import into Anki.
- **CLI Tool**: Simple command-line interface for quick generation.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

## Usage (CLI)

Generate a deck from a text file:

```bash
python -m src.cli.main input.txt --output my_deck.apkg --provider gemini
```

### Options

- `--output`: Path to the output `.apkg` file (default: `output.apkg`).
- `--provider`: LLM provider (`gemini`, `openai`, `anthropic`, `ollama`).
- `--model`: Specific model name (useful for Ollama).
- `--deck-name`: Name of the deck in Anki.
- `--difficulty`: `Beginner`, `Intermediate`, `Advanced`.
- `--style`: `Conceptual`, `Vocabulary`, `Formula`, `Mixed`.
- `--max-cards`: Maximum number of cards to generate.

## Project Structure

- `src/core`: Core logic (LLM clients, Generator, Anki builder).
- `src/cli`: Command-line interface.
- `src/api`: Web API (Coming Soon).