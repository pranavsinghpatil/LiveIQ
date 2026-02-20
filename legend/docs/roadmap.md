# Roadmap

🏁 Phase 1 — Text-only CLI prototype
🏁 Phase 2 — FastAPI endpoint + JSON schema

🧩 Phase 3 — MeshMemory UI + image toggle

🌈 Phase 4 — Image-enhanced cards
- diagram templates for ML
- icons for vocab
- PDF snapshots

🧠 Phase 5 — Quality feedback loop
- thumbs up/down to refine future generations

🔮 Phase 6 — Multi-modal memory analytics

## Phase 0 – Design & Manual Prototyping

- [ ] Define flashcard quality examples (good vs bad).
- [ ] Manually generate decks via LLM + CSV → import into Anki.
- [ ] Finalize JSON schema for `cards` output.

---

## Phase 1 – CLI Prototype

- [ ] Implement `LLMClient` (start with one provider).
- [ ] Implement `flashcard_generator.py`:
  - [ ] Prompt builder.
  - [ ] JSON parsing + validation.
- [ ] Implement `anki_builder.py` using `genanki`.
- [ ] CLI script:
  - input: text file + config.
  - output: `.apkg`.

---

## Phase 2 – Web API

- [ ] Setup FastAPI project.
- [ ] Define `POST /anki/generate` endpoint.
- [ ] Wire LLM + deck builder into endpoint.
- [ ] Return `.apkg` as downloadable file.
- [ ] Basic error handling and logging.

---

## Phase 3 – MeshMemory Integration

- [ ] Endpoint to accept MeshMemory node IDs / search queries.
- [ ] Retrieval logic to gather relevant text chunks from MeshMemory.
- [ ] UI:
  - [ ] Add “Generate Anki Deck” button in MeshMemory.
  - [ ] Form for preferences (difficulty, style, max cards).
  - [ ] Basic preview of generated cards.

---

## Phase 4 – Quality & Personalization

- [ ] Improve prompts for:
  - [ ] GRE vocab.
  - [ ] ML/AI conceptual decks.
  - [ ] Math / formulas.
- [ ] Add optional tags (topic, difficulty).
- [ ] Add simple heuristics to drop low-quality cards.

---

## Phase 5 – Advanced Features (later)

- [ ] Support cloze deletions.
- [ ] Support LaTeX formulas.
- [ ] Support code blocks in cards.
- [ ] User feedback loop:
  - Thumbs up/down on cards.
  - Option to regenerate subsets of cards.

---

## Priorities

Short-term focus:
- Make **one** pipeline rock-solid:
  - GRE / ML notes → JSON cards → `.apkg` → review in Anki.
- Use it yourself daily for real studying.

Then:
- Gradually layer nicer UI and more model options on top.