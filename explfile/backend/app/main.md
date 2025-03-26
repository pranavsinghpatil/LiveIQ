# main.py - FastAPI Application Entry Point

## Purpose
The main entry point for the VoxStitch backend application, configuring FastAPI, middleware, routers, and core dependencies.

## Core Configuration

### FastAPI Setup
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VoxStitch API",
    description="Backend API for VoxStitch chat aggregation platform",
    version="1.0.0"
)
```

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Router Integration

### Authentication Router
```python
from app.core.auth.router import router as auth_router

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)
```

### Chat Router
```python
from app.core.chat.router import router as chat_router

app.include_router(
    chat_router,
    prefix="/chats",
    tags=["Chats"]
)
```

### User Router
```python
from app.core.user.router import router as user_router

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)
```

## Middleware Setup

### Authentication Middleware
```python
@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    if not request.url.path.startswith("/auth"):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401)
        # Token validation logic
    return await call_next(request)
```

### Request Logging
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request processed in {process_time:.2f}s")
    return response
```

## Database Integration

### Database Setup
```python
from app.core.database import engine, Base

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### Database Session
```python
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    try:
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
```

## Error Handling

### Global Exception Handler
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

### Validation Error Handler
```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

## Health Checks

### Basic Health Check
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": app.version,
        "timestamp": datetime.utcnow()
    }
```

### Database Health Check
```python
@app.get("/health/db")
async def db_health_check():
    try:
        await database.fetch_one("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "detail": str(e)}
        )
```

## OpenAPI Documentation

### Swagger UI Configuration
```python
app.swagger_ui_parameters = {
    "defaultModelsExpandDepth": -1,
    "operationsSorter": "method",
    "tagsSorter": "alpha",
    "persistAuthorization": True,
}
```

### API Documentation
```python
app.openapi_tags = [
    {
        "name": "Authentication",
        "description": "Operations related to user authentication"
    },
    {
        "name": "Chats",
        "description": "Chat import and management endpoints"
    },
    {
        "name": "Users",
        "description": "User management and profile operations"
    }
]
```

## Background Tasks

### Task Queue Setup
```python
from app.core.tasks import init_background_tasks

@app.on_event("startup")
async def start_background_tasks():
    await init_background_tasks()
```

### Cleanup Tasks
```python
@app.on_event("shutdown")
async def shutdown_event():
    # Close database connections
    await engine.dispose()
    # Stop background tasks
    await cleanup_background_tasks()
```

## Security Features

### Rate Limiting
```python
from fastapi_limiter import FastAPILimiter
import redis.asyncio

@app.on_event("startup")
async def configure_limiter():
    redis = redis.asyncio.from_url("redis://localhost")
    await FastAPILimiter.init(redis)
```

### Security Headers
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(HTTPSRedirectMiddleware)  # Production only
```

## Environment Configuration

### Settings Management
```python
from app.core.config import Settings

settings = Settings()
app.state.settings = settings
```

### Environment Variables
```python
DATABASE_URL = settings.DATABASE_URL
REDIS_URL = settings.REDIS_URL
JWT_SECRET = settings.JWT_SECRET
```

## Related Files
- `core/auth/router.py`: Authentication routes
- `core/chat/router.py`: Chat management routes
- `core/user/router.py`: User management routes
- `core/config.py`: Application configuration
- `core/database.py`: Database setup

## Recent Updates
- Added rate limiting
- Enhanced error handling
- Improved database connection management
- Added health check endpoints
- Updated OpenAPI documentation
