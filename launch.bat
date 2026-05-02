@echo off
SETLOCAL EnableDelayedExpansion

echo ======================================================
echo 📺 LiveIQ — Platform Launcher (Production Grade)
echo ======================================================

:: 0. Clean up previous instances
echo [0/5] Terminating previous instances...
taskkill /FI "WINDOWTITLE eq LiveIQ - *" /T /F >nul 2>&1

:: 1. Environment Checks
echo [1/5] Checking environment...

if not exist "backend\.env" (
    echo [!] backend\.env missing. Creating from example...
    copy backend\.env.example backend\.env >nul
    echo [!] ACTION REQUIRED: Open backend\.env and add your GEMINI_API_KEY and GROQ_API_KEY.
)

if not exist "queue-workers\.env" (
    echo [!] queue-workers\.env missing. Creating...
    echo QUEUE_REDIS_URL=redis://localhost:6379 > queue-workers\.env
    echo BACKEND_API_URL=http://localhost:8000 >> queue-workers\.env
    echo QUEUE_PORT=3001 >> queue-workers\.env
)

:: 2. Setup Backend Venv if missing
if not exist "backend\venv" (
    echo [!] Backend virtual environment missing. Setting up...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    echo [!] Installing backend dependencies - this may take a minute...
    pip install -r requirements.txt >nul
    cd ..
    echo [OK] Backend environment ready.
)

:: 3. Setup Node Modules if missing
if not exist "queue-workers\node_modules" (
    echo [!] Queue workers node_modules missing. Installing...
    cd queue-workers
    call npm install >nul
    cd ..
)

if not exist "frontend\node_modules" (
    echo [!] Frontend node_modules missing. Installing...
    cd frontend
    call npm install >nul
    cd ..
)

:: 4. Start Redis via Docker
echo [2/5] Starting Redis...
docker-compose up -d redis >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Redis failed to start via Docker. Ensure a local Redis is running on port 6379.
) else (
    echo [OK] Redis is active.
)

:: 5. Launch Components
echo [3/5] Booting Backend (FastAPI)...
start "LiveIQ - Backend" cmd /k "cd backend && call venv\Scripts\activate && echo [API] Starting... && uvicorn app.main:app --reload --port 8000"

echo [4/5] Booting Queue Workers...
start "LiveIQ - Workers" cmd /k "cd queue-workers && echo [WORKERS] Starting... && npm run dev"

echo [5/5] Booting Frontend (React)...
start "LiveIQ - Frontend" cmd /k "cd frontend && echo [UI] Starting... && npm run dev"

echo ======================================================
echo 🚀 ALL SYSTEMS LAUNCHED!
echo ======================================================
echo  [API]      http://localhost:8000/docs
echo  [UI]       http://localhost:5173
echo  [WORKERS]  http://localhost:3001/admin/queues
echo ======================================================
echo Keep terminal windows open to maintain the platform.
echo Press any key to exit this launcher.
pause >nul
