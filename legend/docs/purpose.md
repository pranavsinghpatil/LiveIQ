# Purpose

## 1. Core Purpose

The purpose of MeshCards is:

> To transform personal notes into **high-quality, personalized Anki decks** with minimal friction, so learners can reliably move from passive reading to active recall.

This project exists to solve a very specific bottleneck:
- Creating flashcards is powerful but **tedious**.
- AI can summarize, but rarely gives **usable Anki decks tied to your actual notes**.

MeshCards aims to be the missing link between:
- Note-taking tools (MeshMemory, Obsidian, markdown, PDFs)
- and
- Spaced repetition tools (Anki).

---

## 2. What MeshCards must do (non-negotiable)

1. **Accept real study material**  
   - Paste raw text / upload files / pick notes from MeshMemory.
2. **Generate flashcards that are actually useful**  
   - Clear Q/A, not vague summaries.
   - Focus on important concepts, not random trivia.
3. **Allow personalization**  
   - Beginner / intermediate / advanced difficulty.
   - Styles like GRE vocab, conceptual understanding, formulas, etc.
4. **Export as `.apkg` for Anki**  
   - User downloads the deck and imports with a few clicks.

---

## 3. Who this project is designed for

### Primary user

- A self-motivated learner with lots of notes who:
  - Knows Anki or is willing to use it.
  - Values long-term retention.
  - Wants to save time on card creation.

### Secondary user

- Anyone curious about:
  - RAG + LLMs,
  - personal knowledge bases,
  - or building a smarter study workflow around existing notes.

---

## 4. Constraints & guardrails

- **Local-first friendly**  
  - Should be compatible with a local stack (e.g. Ollama + local notes), especially when used with MeshMemory.
- **No vendor lock-in**  
  - LLM choices should be pluggable: Gemini, Groq, Banana-hosted models, local models, etc.
- **Respect existing workflows**  
  - Don’t replace Anki.
  - Don’t force users into a new note-taking environment.
  - Be a bridge, not a whole ecosystem.

---

## 5. Success criteria

MeshCards is successful if:

- It becomes natural to say:
  > “I studied X today, let me generate a deck from my notes.”
- Users (including you) **actually use the decks** consistently.
- The system reduces:
  - friction to create flashcards,
  - cognitive load in deciding what to memorize,
  - and manual effort in formatting cards.

---

## 6. Non-goals (for now)

To stay focused, MeshCards is **not** trying to:

- Replace Anki’s scheduling algorithm.
- Build its own spaced repetition app.
- Cover every advanced Anki feature (cloze, image occlusion, audio, etc.) in v1.
- Solve summarization / explanation of notes generally (MeshMemory already covers that space).

The purpose is narrow:
> “Turn the best parts of your notes into personalized, import-ready Anki decks.”
