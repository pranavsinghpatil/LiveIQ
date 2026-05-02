import redis.asyncio as aioredis
from typing import Optional
from app.config import get_settings

settings = get_settings()

_redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def close_redis():
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


async def publish_event(channel: str, message: str):
    r = await get_redis()
    await r.publish(channel, message)


async def cache_update(event_id: str, message: str, max_items: int = 10):
    """Cache last N updates for WS reconnect catchup."""
    r = await get_redis()
    key = f"event:{event_id}:cache"
    await r.rpush(key, message)
    await r.ltrim(key, -max_items, -1)
    await r.expire(key, 86400)  # 24h TTL


async def get_cached_updates(event_id: str) -> list:
    r = await get_redis()
    key = f"event:{event_id}:cache"
    return await r.lrange(key, 0, -1)


async def set_commentary_lock(event_id: str, ttl: int = 60) -> bool:
    """Debounce lock for Groq commentary — returns True if lock was acquired."""
    r = await get_redis()
    key = f"commentary_lock:{event_id}"
    result = await r.set(key, "1", nx=True, ex=ttl)
    return result is not None


async def set_analysis_lock(event_id: str, ttl: int = 290) -> bool:
    """Lock for Gemini analysis — prevents concurrent analysis jobs."""
    r = await get_redis()
    key = f"analysis_lock:{event_id}"
    result = await r.set(key, "1", nx=True, ex=ttl)
    return result is not None


async def track_ws_connection(event_id: str, client_id: str):
    r = await get_redis()
    await r.sadd(f"ws_clients:{event_id}", client_id)
    await r.expire(f"ws_clients:{event_id}", 86400)


async def remove_ws_connection(event_id: str, client_id: str):
    r = await get_redis()
    await r.srem(f"ws_clients:{event_id}", client_id)


async def get_ws_connection_count(event_id: Optional[str] = None) -> int:
    r = await get_redis()
    if event_id:
        return await r.scard(f"ws_clients:{event_id}")
    # Count all WS connections
    keys = await r.keys("ws_clients:*")
    total = 0
    for key in keys:
        total += await r.scard(key)
    return total
