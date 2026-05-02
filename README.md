# 📺 LiveIQ — Live Event Intelligence Platform

> **Assignment 5 of 5** — Production-grade real-time sports event intelligence platform  
> Stack: FastAPI · Gemini 1.5 Flash · Groq Llama 3.1 · BullMQ · WebSockets · Redis · React + Vite

![LiveIQ Platform](./docs/screenshot-auth.png)

---

## 🏗️ Architecture

```
TheSportsDB / Mock Data
        ↓ (APScheduler 60s)
[Stage 1] Event Ingestion   → BullMQ → DB
[Stage 2] Stream Accumulation → Rolling 50-event window
[Stage 3] Groq Commentary   → Llama 3.1 8B → < 2s → WebSocket
[Stage 4] Gemini Analysis   → Every 5min → Pydantic output
[Stage 5] Redis Pub/Sub     → event:{id}:updates channel
[Stage 6] WebSocket Push    → All subscribed clients
[Stage 7] Alert Engine      → BullMQ → keyword/score/trend rules
[Stage 8] Post-Event Report → Gemini narrative + accuracy
```

---

## ⚡ Quick Start (Local Dev)

### Prerequisites
- Python 3.11+
- Node.js 20+
- Redis: `docker run -d -p 6379:6379 redis`

### 1. Backend (FastAPI)
```bash
cd backend
cp .env.example .env
# Edit .env: add GEMINI_API_KEY and GROQ_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
→ API: http://localhost:8000  
→ Docs: http://localhost:8000/docs

### 2. Queue Workers (BullMQ + Bull Board)
```bash
cd queue-workers
npm install
npm run dev
```
→ Bull Board: http://localhost:3001/admin/queues

### 3. Frontend (Vite + React)
```bash
cd frontend
npm install
npm run dev
```
→ App: http://localhost:5173

### 4. Docker Compose (Full Stack)
```bash
docker-compose up --build
```

---

## 🔑 Environment Variables

See `backend/.env.example`:

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio key (free at aistudio.google.com) |
| `GROQ_API_KEY` | Groq API key (free at console.groq.com) |
| `USE_MOCK=true` | Use mock_livescore.json instead of live API |
| `DATABASE_URL` | SQLite (default) or PostgreSQL |
| `REDIS_URL` | Redis connection string |
| `SECRET_KEY` | JWT signing secret |

---

## 📺 8 Screens

| Screen | URL | Role |
|---|---|---|
| Sign Up / Login | `/auth` | Public |
| Event Browser | `/events` | All |
| **Live Event View** ⭐ | `/live?event={id}` | All |
| AI Analysis Panel | `/analysis` | All |
| Prediction Board | `/predictions` | All |
| Alert Manager | `/alerts` | Analyst |
| Post-Event Report | `/reports` | Analyst |
| Admin Dashboard | `/admin` | Analyst |

---

## 🔌 WebSocket — Multi-client Test

Open two browser tabs to the same event:
```
ws://localhost:8000/ws/events/{event_id}?token={jwt}
```
Both clients receive live updates simultaneously. On reconnect, the last 10 cached updates are replayed.

**Screenshot showing 2 simultaneous clients:**  
*(Run `wscat -c "ws://localhost:8000/ws/events/evt001"` in two terminals)*

---

## 🗄️ Pipeline Stages Table

All 8 stages are tracked in `pipeline_stages`:

| Column | Type |
|---|---|
| event_id | VARCHAR (FK) |
| stage_number | INT (1-8) |
| stage_name | VARCHAR |
| status | pending / active / done / failed |
| started_at | TIMESTAMP |
| completed_at | TIMESTAMP |

Exposed at: `GET /api/events/{id}/stages`  
Frontend polls every 10s + receives real-time updates via WebSocket.

---

## 🐂 BullMQ Workers

| Queue | Purpose | Stage |
|---|---|---|
| `event-ingestion` | Fetch from TheSportsDB | 1 |
| `stream-accumulation` | Rolling 50-event window | 2 |
| `groq-commentary` | Llama 3.1 8B commentary | 3 |
| `gemini-analysis` | Gemini Flash deep analysis | 4 |
| `alert-rules` | Rule evaluation | 7 |
| `post-event-report` | Final narrative + accuracy | 8 |

Bull Board: http://localhost:3001/admin/queues

---

## 🎁 Bonus Challenges Implemented

### 1. Multi-Model Debate Mode (+10 pts)
- Gemini Flash and Groq Llama produce **competing predictions** for every event
- Side-by-side display in AI Analysis Panel and Live Event View
- Accuracy tracking: `GET /api/admin/predictions/model-accuracy`

### 2. Weather Injection (+10 pts)
- Open-Meteo API (free, no key) fetches venue weather
- Injected into Gemini analysis prompt: `"Current conditions: 12°C, heavy rain"`
- Displayed in Live Event View with 🌤️ indicator

### Testing Bonus Features:
```bash
# Model accuracy
curl http://localhost:8000/api/admin/predictions/model-accuracy -H "Authorization: Bearer {token}"

# Weather is auto-injected when venue coordinates are known
# Check event analysis for weather_conditions field
```

---

## 🔐 Auth & RBAC

| Role | Access |
|---|---|
| `analyst` | Full access — alerts, reports, admin, unlimited subscriptions |
| `viewer` | Read-only — max 3 event subscriptions, no alert rules |

Enforced via FastAPI `Depends()` at every endpoint.

---

## 📊 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Create account |
| POST | `/api/auth/token` | Public | Login, get JWT |
| GET | `/api/events` | Public | List events |
| GET | `/api/events/{id}/stages` | Public | Pipeline stages |
| POST | `/api/events/{id}/subscribe` | Auth | Subscribe |
| GET | `/api/events/{id}/analyses` | Auth | AI analyses |
| GET | `/api/events/{id}/report` | Analyst | Post-event report |
| POST | `/api/alerts/rules` | Analyst | Create alert rule |
| GET | `/api/admin/stats` | Analyst | System stats |
| GET | `/api/admin/predictions/model-accuracy` | Analyst | Bonus: model comparison |
| WS | `/ws/events/{id}` | Optional | Live event stream |
| WS | `/ws/users/{id}/alerts` | Auth | User alert channel |

Full Swagger docs: http://localhost:8000/docs

---

## 🧪 Development with Mock Data

```bash
# In backend/.env:
USE_MOCK=true
```

`mock_livescore.json` contains **50 sample events** across 3 sports:
- ⚽ Soccer (EPL, La Liga, Serie A, Bundesliga, Champions League)
- 🏀 Basketball (NBA, EuroLeague)
- 🎾 Tennis (Wimbledon, US Open, French Open)

---

## 📁 Project Structure

```
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── main.py         # App entry point
│   │   ├── models/         # SQLAlchemy ORM
│   │   ├── schemas/        # Pydantic v2 schemas
│   │   ├── routers/        # FastAPI routers (auth, events, alerts, admin)
│   │   ├── services/       # AI, Redis, pipeline, scheduler
│   │   └── auth/           # JWT + RBAC
│   ├── mock_livescore.json # 50 sample events
│   └── .env.example
├── queue-workers/           # Node.js BullMQ workers
│   └── src/
│       ├── workers/        # 6 worker types
│       ├── queues/         # Queue definitions
│       └── bullboard/      # Bull Board at /admin/queues
├── frontend/                # Vite + React + TypeScript
│   └── src/
│       ├── pages/          # 8 screens
│       ├── components/     # PipelineStepper, CommentaryFeed, etc.
│       ├── hooks/          # useWebSocket
│       └── lib/            # API client, auth store
└── docker-compose.yml
```
