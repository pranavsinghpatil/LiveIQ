# VoxStitch (ChatSynth) Backend File Structure

This document outlines the backend file structure for the VoxStitch (formerly ChatSynth) project. It is organized for clarity, modularity, and scalability.

---

## Root: `/backend`

- `.env`, `.env.template`          # Environment variables
- `requirements.txt`               # Python dependencies
- `main.py`                        # (Legacy) Entrypoint, not used in modular app
- `test.py`, `test_supabase.py`, `test_upload.py` # Test scripts
- `memory_db.py`, `models.py`      # (Legacy/utility) modules
- `/uploads/`                      # Uploaded files storage
- `/docs/`                         # Documentation
- `/benv/`                         # Python virtual environment (ignore in repo)

## App Core: `/backend/app`

- `main.py`                        # FastAPI main application entrypoint
- `/controllers/`                  # (Optional) Controller logic
- `/middlewares/`                  # Custom FastAPI middleware (auth, CORS, etc.)
- `/models/`                       # Pydantic schemas for API (chat, user, hybrid, etc.)
- `/routes/`                       # All API route definitions
- `/services/`                     # Business logic and integrations
- `/utils/`                        # Utilities and helpers

### `/app/models/`
- `chat.py`                        # Chat, ChatThread, Message models
- `file_models.py`                 # File upload models
- `group.py`                       # (Legacy) Grouping models
- `hybrid_models.py`               # Hybrid chat models
- `thread_models.py`               # Thread models
- `user_models.py`                 # User, Auth models

### `/app/routes/`
- `auth_routes.py`                 # Auth endpoints (register, login, token)
- `chat_routes.py`                 # Chat, message, and context endpoints
- `hybrid_routes.py`               # Hybrid chat creation, context, reply
- `linker.py`                      # Link import endpoints (YouTube, etc.)
- `podcast_simulator.py`           # Podcast simulation endpoints
- `thread_routes.py`               # Thread CRUD endpoints
- `upload.py`                      # File upload endpoints

### `/app/services/`
- `auth_service.py`                # Auth helpers
- `chat_service.py`                # Chat business logic
- `hybrid_service.py`              # Hybrid business logic
- `supabase_client.py`             # Supabase DB integration
- `thread_service.py`              # Thread business logic

### `/app/utils/`
- `media_processor.py`             # Media file processing
- `...`                            # Other custom utilities

## Core Logic: `/backend/core`

- `/db/`
  - `memory.py`                    # In-memory DB for chat, thread, hybrid context
- `/llm/`
  - `llm_client.py`                # LLM API integration
  - `llm_models.py`                # LLM-related schemas
  - `llm_routes.py`                # LLM and hybrid endpoints (in-memory logic)
  - `llm_service.py`               # LLM business logic
- `/services/`
  - `chat_service.py`, `hybrid_service.py`, `thread_service.py` # Core business logic
- `/ingest/`, `/ingestion/`
  - Handlers for file and link ingestion
- `/podcast_simulator/`
  - Podcast transcript and simulation logic

---

## Example: Key API Endpoints

- `/api/chats/`                    # Chat management
- `/api/chats/{chat_id}/message`   # Add message to chat
- `/api/hybrid/create`             # Create hybrid chat
- `/api/hybrid/{hybrid_id}/chats`  # List chats in a hybrid
- `/api/llm/chat`                  # LLM chat
- `/api/llm/hybrid/register`       # Register hybrid context (in-memory)

---

## Notes
- All business logic is separated from route definitions for maintainability.
- Models are shared between core, app, and services for consistency.
- Legacy files (e.g., group.py) are being phased out in favor of hybrid logic.
- Supabase is used for persistent storage; memory.py for fast prototyping and ephemeral context.

---

*For more details, see individual module docstrings or ask for a component-specific breakdown.*
