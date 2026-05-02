from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # AI APIs
    gemini_api_key: str = ""
    groq_api_key: str = ""

    # TheSportsDB
    sportsdb_api_key: str = "123"
    use_mock: bool = True

    # Database
    database_url: str = "sqlite:///./live_events.db"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # JWT
    secret_key: str = "supersecret-change-this-in-production-32chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # Scheduler
    ingest_interval_seconds: int = 60
    analysis_interval_seconds: int = 300

    # App
    app_env: str = "development"
    port: int = 8000
    frontend_url: str = "http://localhost:5173"

    # Queue Workers
    queue_redis_url: str = "redis://localhost:6379"
    backend_api_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
