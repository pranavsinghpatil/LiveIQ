import json
import asyncio
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.services.redis_service import (
    get_cached_updates, track_ws_connection, remove_ws_connection, get_redis
)
from app.auth import get_settings
from app.config import get_settings as config_settings

router = APIRouter(tags=["websocket"])
settings = config_settings()


class ConnectionManager:
    """Manages active WebSocket connections per event."""

    def __init__(self):
        # event_id → set of WebSockets
        self.active_connections: dict[str, set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, event_id: str, client_id: str):
        await websocket.accept()
        if event_id not in self.active_connections:
            self.active_connections[event_id] = set()
        self.active_connections[event_id].add(websocket)
        await track_ws_connection(event_id, client_id)

    def disconnect(self, websocket: WebSocket, event_id: str):
        if event_id in self.active_connections:
            self.active_connections[event_id].discard(websocket)
            if not self.active_connections[event_id]:
                del self.active_connections[event_id]

    async def broadcast_to_event(self, event_id: str, message: str):
        if event_id not in self.active_connections:
            return
        dead = set()
        for ws in self.active_connections[event_id]:
            try:
                await ws.send_text(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.active_connections[event_id].discard(ws)


manager = ConnectionManager()


@router.websocket("/ws/events/{event_id}")
async def websocket_event(
    websocket: WebSocket,
    event_id: str,
    token: str = Query(None),
):
    """
    WebSocket endpoint for live event updates.
    Subscribes to Redis pub/sub channel: event:{event_id}:updates
    On reconnect: sends last 10 cached updates.
    """
    client_id = str(uuid.uuid4())
    await manager.connect(websocket, event_id, client_id)

    # Send catchup payload (last 10 cached updates on reconnect)
    cached = await get_cached_updates(event_id)
    for cached_msg in cached:
        try:
            await websocket.send_text(cached_msg)
        except Exception:
            break

    # Send welcome message
    await websocket.send_text(json.dumps({
        "type": "connected",
        "event_id": event_id,
        "client_id": client_id,
        "data": {"message": f"Connected to event {event_id}"},
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
    }))

    # Subscribe to Redis pub/sub in background
    redis_task = asyncio.create_task(
        _redis_subscriber(websocket, event_id, client_id)
    )

    try:
        while True:
            # Keep connection alive, handle client messages
            data = await websocket.receive_text()
            # Echo ping/pong
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        pass
    finally:
        redis_task.cancel()
        manager.disconnect(websocket, event_id)
        await remove_ws_connection(event_id, client_id)


async def _redis_subscriber(websocket: WebSocket, event_id: str, client_id: str):
    """Subscribe to Redis pub/sub and forward messages to WebSocket client."""
    try:
        r = await get_redis()
        pubsub = r.pubsub()
        await pubsub.subscribe(f"event:{event_id}:updates")

        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    await websocket.send_text(message["data"])
                except Exception:
                    break
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"[WS] Redis subscriber error: {e}")
    finally:
        try:
            await pubsub.unsubscribe(f"event:{event_id}:updates")
            await pubsub.close()
        except Exception:
            pass


@router.websocket("/ws/users/{user_id}/alerts")
async def websocket_user_alerts(
    websocket: WebSocket,
    user_id: str,
    token: str = Query(None),
):
    """
    WebSocket endpoint for user-specific alert notifications.
    Subscribes to: user:{user_id}:alerts
    """
    client_id = str(uuid.uuid4())
    await websocket.accept()

    r = await get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(f"user:{user_id}:alerts")

    await websocket.send_text(json.dumps({
        "type": "connected",
        "data": {"message": f"Alert channel connected for user {user_id}"},
    }))

    async def redis_listener():
        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    await websocket.send_text(message["data"])
                except Exception:
                    break

    listener_task = asyncio.create_task(redis_listener())

    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        pass
    finally:
        listener_task.cancel()
        await pubsub.unsubscribe(f"user:{user_id}:alerts")
        await pubsub.close()
