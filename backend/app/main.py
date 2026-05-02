"""
FastAPI Main Application Entry Point
Live Event Intelligence Platform
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import init_db
from app.services.redis_service import get_redis, close_redis
from app.services.scheduler import start_scheduler, stop_scheduler
from app.routers import auth, events, alerts, admin
from app.routers.websocket import router as ws_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    # Startup
    print("[INIT] Starting Live Event Intelligence Platform...")
    await init_db()
    print("[INIT] Database initialized")
    await get_redis()
    print("[INIT] Redis connected")
    start_scheduler()
    print("[INIT] Scheduler started")
    yield
    # Shutdown
    stop_scheduler()
    await close_redis()
    print("[INIT] Shutdown complete")


app = FastAPI(
    title="Live Event Intelligence Platform",
    description="""
    Production-grade real-time sports event intelligence platform.
    
    ## Features
    - 🏟️ **Live Sports Events** — TheSportsDB API + mock data
    - 🤖 **AI Commentary** — Groq Llama 3.1 8B (< 2s)
    - 🧠 **AI Analysis** — Gemini 1.5 Flash (every 5 min)
    - 📡 **Real-time Push** — WebSocket + Redis pub/sub
    - ⚡ **Pipeline Tracking** — 8-stage pipeline stepper
    - 🔔 **Smart Alerts** — Custom rule engine
    - 📊 **Post-event Reports** — Full Gemini narrative
    
    ## Auth
    - JWT Bearer token required for most endpoints
    - Two roles: `analyst` (full access) and `viewer` (read-only, max 3 subs)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, events, alerts, admin, internal
from app.routers.websocket import router as ws_router

# ... inside main ...

# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(alerts.router)
app.include_router(admin.router)
app.include_router(internal.router)
app.include_router(ws_router)


@app.get("/", tags=["health"])
async def health_check():
    return {
        "status": "online",
        "service": "Live Event Intelligence Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "websocket": "/ws/events/{event_id}",
        "bull_board": "http://localhost:3001/admin/queues",
    }


@app.get("/health", tags=["health"])
async def detailed_health():
    from app.services.redis_service import get_redis
    try:
        r = await get_redis()
        await r.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "disconnected"

    return {
        "status": "healthy",
        "redis": redis_status,
        "scheduler": "running",
        "use_mock": settings.use_mock,
    }
