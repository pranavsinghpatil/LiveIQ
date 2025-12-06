# Architecture

Core modules:

- `retrieval.py` — text selection from sources
- `flashcard_generator.py` — LLM prompt + JSON enforcement
- `image_generator.py` — Nano Banana interface
- `anki_builder.py` — handles media fields (.apkg with images)
- `schemas.py` — strict Pydantic models for validation

Data Schema (.apkg):

- Fields:
  - `Front`
  - `Back`
  - `Image` (optional media)
  - `Tags`

## 1. Overview

MeshCards is composed of three main layers:

1. **Input + Retrieval Layer**
2. **LLM Generation Layer**
3. **Deck Construction + Delivery Layer**

It can run:
- as a standalone service, or
- as a feature embedded into MeshMemory.

---

## 2. Components

### 2.1 Backend (API)

- **Framework**: FastAPI (Python)
- **Core modules**:
  - `llm_client.py`: abstraction over different LLM providers.
  - `retrieval.py`: interfaces with MeshMemory / local text preprocessing.
  - `flashcard_generator.py`: prompt building + response parsing.
  - `anki_builder.py`: uses `genanki` (or equivalent) to build `.apkg`.
  - `schemas.py`: Pydantic models for request/response data.

#### Key endpoint

- `POST /anki/generate`
  - Request body:
    - `source_type`: `"raw_text" | "file" | "meshmemory"`
    - `content` or `note_ids` or `file_id`
    - `preferences` (difficulty, style, max_cards, etc.)
  - Response:
    - `.apkg` file (as binary content)  
      or
    - JSON with a pre-signed URL / download link.

---

### 2.2 LLM Layer

- **LLMClient interface** (pseudo):

  ```python
  class LLMClient:
      def generate_flashcards(self, notes_context: str, preferences: dict) -> dict:
          ...
Implementations:

GeminiLLMClient

GroqLLMClient

LocalOllamaLLMClient

BananaHostedLLMClient

This keeps the architecture flexible and avoids hard dependency on one provider.

2.3 Deck Builder Layer
Uses genanki to:

define models (fields, templates),

iterate over generated cards,

add them as Note objects,

write .apkg package.

Separation:

flashcard_generator.py → creates card data.

anki_builder.py → converts card data into an Anki deck file.

3. Data Flow
Request comes in

/anki/generate with notes + preferences.

Source handling

If raw_text: use directly (with cleaning).

If file: extract text (PDF parser, etc.).

If meshmemory: call MeshMemory API (search/graph) to get relevant text chunks.

LLM generation

Build prompt from:

context text,

preferences.

Call LLMClient.generate_flashcards.

Receive JSON with cards.

Validation

Validate JSON structure with Pydantic.

Optionally prune / adjust cards.

Deck creation

Build deck via anki_builder.

Write to .apkg.

Response

Return .apkg file as response body (with correct headers).

4. Deployment considerations
Can run as:

local dev server (uvicorn),

containerized (Docker) service,

part of a larger stack with MeshMemory.

Secrets:

LLM API keys via environment variables.

Resource constraints:

Use streaming / pagination for large notes.

Limit max_cards per request.

5. Integration points
MeshMemory:

shared embeddings / recall API.

optional UI integration (button “Generate Anki Deck" inside MeshMemory).

External note sources:

import endpoints for:

markdown files,

folders,

exported notes, etc.

yaml
Copy code
