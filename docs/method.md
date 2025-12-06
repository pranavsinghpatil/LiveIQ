# Method

1️⃣ Retrieval  
- Select text from: raw input / file / MeshMemory

2️⃣ Flashcard Text Generation  
- LLM outputs structured JSON:
  - front, back, tags, difficulty label

3️⃣ Image Generation (optional per user)  
- If enabled, send a structured prompt to Nano Banana:
  - with context, desired graphic type, simplification rules

4️⃣ Validation  
- Remove duplicates
- Drop hallucinated or trivial cards
- Enforce max length

5️⃣ Deck Assembly  
- Text + images converted to `.apkg` with genanki

6️⃣ Delivery  
- Preview → download

This document describes **how** MeshCards will solve the problem:
from raw notes → to personalized Anki decks.

---

## 1. High-level pipeline

1. **Input collection**
   - User selects:
     - raw text (paste),
     - uploaded file (e.g. PDF),
     - or notes from MeshMemory (via search / graph selection).

2. **Preprocessing + retrieval**
   - Normalize text (cleaning, splitting, removing noise).
   - If using MeshMemory:
     - use vector search + graph neighbors to select the most relevant chunks.
   - Produce a focused set of **study chunks** that will feed the LLM.

3. **LLM-driven flashcard generation**
   - Send selected chunks + user preferences (difficulty, style, max cards) to an LLM.
   - Use a strict, schema-focused prompt to generate:
     - a JSON object with `deck_name` and `cards`.
   - Each card includes:
     - type (e.g. `"basic"` initially),
     - front (question),
     - back (answer),
     - optional tags.

4. **Validation & post-processing**
   - Validate JSON output (schema, required fields).
   - Filter out duplicates or trivial cards.
   - Optionally apply:
     - length constraints,
     - basic checks for empty or nonsensical cards.

5. **Deck construction (Anki)**
   - Use a deck-building library (e.g. `genanki` in Python).
   - Map cards to Anki note model:
     - fields: `Question`, `Answer`, `Tags`.
   - Generate a `.apkg` Anki deck file.

6. **Delivery**
   - Return the `.apkg` file to the user for download.
   - Optionally present a preview of cards before export.

---

## 2. LLM usage pattern

### Inputs to LLM

- `notes_context`: selected text chunks.
- `user_profile` (optional): e.g. “CS graduate, preparing for GRE + ML interviews.”
- `preferences`:
  - difficulty: beginner / intermediate / advanced.
  - card_focus: definitions / intuition / formulas / examples.
  - max_cards: integer limit.

### Outputs from LLM

The LLM must return JSON like:

```json
{
  "deck_name": "Transformer Attention - Core Concepts",
  "cards": [
    {
      "type": "basic",
      "front": "What is the key idea of self-attention in transformer architectures?",
      "back": "Self-attention allows each token to attend to other tokens in the same sequence to compute a context-aware representation."
    }
  ]
}
We enforce this via:

explicit instructions in the system prompt,

“return only JSON, no extra text” constraint,

server-side parsing and validation.

3. Personalization logic
Personalization is applied mainly in the prompt:

Difficulty:

Beginner → focus on basic definitions and high-level explanations.

Intermediate → mix of definitions + “why” questions.

Advanced → more derivations, edge cases, connections between concepts.

Style:

GRE vocabulary → word, definition, part of speech, example sentence, synonym/antonym.

Conceptual → “explain”, “compare”, “why does this fail?” type questions.

Formula-heavy → cards about equations, meanings of terms, typical use-cases.

The backend translates user settings into prompt instructions:

“Assume the learner is an intermediate-level ML student preparing for GRE Quant.
Prioritize conceptual and problem-oriented questions.”

4. Integration with MeshMemory (optional but important)
When integrated with MeshMemory:

User selects a node / topic / tag / search query.

Backend:

fetches related chunks using embeddings + graph structure.

merges them into a coherent context.

LLM uses this context to generate cards.

MeshMemory can store:

metadata about generated decks,

links between notes and the corresponding Anki decks.

This turns MeshMemory into a source of truth for knowledge,
and MeshCards into a memory engine on top.

5. Implementation phases
Phase 1: CLI prototype
Simple script:

input: text file + JSON config.

output: .apkg file.

Uses:

genanki for deck creation,

an LLM client for card generation.

Phase 2: Web API
FastAPI backend endpoint:

POST /anki/generate

Accepts:

notes (text or reference IDs),

preferences.

Returns:

downloadable .apkg.

Phase 3: MeshMemory integration + UI
Add UI components to:

choose notes / topics,

configure preferences,

preview cards,

download deck.

6. Future extensions
Support for:

cloze deletions,

code-based cards (question on front, code snippet explanation on back),

images and LaTeX rendering.

Feedback loop:

user marks bad / good cards,

system learns to generate better ones over time.

Analytics:

track which topics get repeated deck generations (signal of difficulty).

yaml
Copy code
