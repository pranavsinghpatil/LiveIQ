🧠 VoxStitch — The Real Core Idea
1. Unified Conversational Memory
All AI chats (across tools like ChatGPT, Claude, Gemini, PDFs, screenshots, links, etc.) come together in one system.

Format-agnostic import: chat links, shared chat links, PDFs, screenshots, markdown, etc.

Every chat gets:

source (e.g., ChatGPT, Claude)

format (pdf, link, screenshot)

chat_id, thread_id, timestamp

Context snapshot (vector embeddings or LLM summary)

2. Thread Fusion & Hybrid Chat
Related threads are merged to build a hybrid context—you can talk to all the threads as if they’re one.

Detect related threads (topic, intent, entities, etc.)

Group them dynamically or manually

Let user chat with the group, not just individuals

Each chat carries its own memory + a fused memory of the group

3. Persistent Chat Context (Auto-Save + Benchmarks)
Chat updates its memory after each user message. After a benchmark (e.g., 5 turns), it re-evaluates to summarize and refresh context.

Stored context snapshots

Intent tracking & info persistence

Smart benchmarking (e.g., checkpoint every 5 messages, or when user manually flags)

4. Parallel Learning & Search-While-Chatting
If you're mid-chat and want to explore something new, create a child or parallel chat.

Branch out without disrupting the main chat

Later, fuse them back if needed

Interlinked chat relationships: parent_id, sibling_id, references

5. Podcast & Media Integration
Upload or link podcasts. Extract transcripts. Then...

Talk to any speaker

Simulate group chat with the podcast people

Summarize, query, extract quotes, etc.

Supports:

YouTube, Spotify, Google Podcasts, manual transcript, etc.

🔁 ThreadGroup (Hybrid Logic)

"multiple related chats should coalesce into a hybrid thread where they can access each other’s memory & context"

So now we’ll define a new structure called ThreadGroup that:

Groups related ChatThreads

Shares memory, summary, tags

Enables navigation between parallel contexts without breaking focus

