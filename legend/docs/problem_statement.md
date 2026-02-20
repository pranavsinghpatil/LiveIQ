# Problem Statement
mainly:

People take thousands of notes.
But:
- They **don’t create flashcards**
- They **can’t retain complex content**
- Visual learners lack **illustration support**

MeshCards solves this by:
- generating **personalized** Q/A cards from notes,
- offering optional **AI-generated images**,
- allowing complete control over:
  - when images are used
  - what style of images to generate
  - which topics need visuals

This eliminates the flashcard bottleneck.

## 1. Background

Learners today have access to:
- Massive amounts of content (courses, videos, blogs, papers).
- Flexible note-taking tools (Notion, Obsidian, MeshMemory, markdown, etc.).
- Powerful learning algorithms via Anki and spaced repetition.

Yet, most learners still struggle with:
- **Consistently remembering** what they learn.
- **Turning notes into actionable review material**.

---

## 2. Core Problems

### Problem 1: Flashcard creation is a bottleneck

- Creating good Anki cards requires:
  - identifying key concepts,
  - phrasing clear questions,
  - writing concise answers,
  - tagging and organizing.
- This is cognitively heavy and time-consuming.
- Result: learners postpone it or never do it at all.

### Problem 2: Notes are disconnected from spaced repetition

- Notes and Anki usually live in separate silos.
- There is no smooth “from note → deck” pipeline.
- Learners end up:
  - re-reading notes,
  - cramming,
  - or relying on generic decks that don’t match **their own understanding or sources**.

### Problem 3: Existing AI tools are generic, not personal

- Generic “AI flashcard generators” often:
  - work only on web articles / URLs, not personal notes.
  - produce shallow or noisy cards.
  - don’t integrate with Anki as `.apkg`.
- They rarely leverage:
  - the learner’s existing note structure,
  - or topic relationships (graphs, tags, embeddings).

---

## 3. User Needs

The target user needs:

1. A way to **quickly convert their own notes** (text, PDFs, MeshMemory nodes) into flashcards.
2. Control over:
   - difficulty level,
   - focus (definitions / intuition / formulas / examples),
   - number of cards generated.
3. Output that:
   - imports cleanly into Anki,
   - is structured and tagged,
   - feels like something a **human expert** could have written.

---

## 4. Problem Definition (short version)

> Given a set of personal study notes (text, documents, or knowledge graph nodes),  
> how can we automatically generate a **high-quality, personalized Anki deck (.apkg)**  
> that:
> - captures the most important concepts,
> - matches the learner’s level and goals,
> - and significantly reduces manual card-creation effort?

---

## 5. Constraints & Challenges

- **Quality control**  
  - LLMs can hallucinate or create low-quality questions.
  - We need prompt design, structure, and validation to keep cards useful.
- **Context limits**  
  - Large notes may not fit directly into the model context.
  - Need retrieval and chunking strategies.
- **Export format**  
  - Must produce valid `.apkg` files.
- **Personalization vs simplicity**  
  - Provide meaningful options without overwhelming the user.

---

## 6. Success Criteria

We consider the problem well-addressed if:

- A learner can:
  - select a topic / set of notes,
  - configure basic preferences,
  - and obtain an Anki deck within minutes.
- The resulting cards:
  - are clear, correct, and focused on understanding,
  - are good enough that the learner chooses to actually review them.
- The workflow becomes part of regular study habits, not a one-off gimmick.
