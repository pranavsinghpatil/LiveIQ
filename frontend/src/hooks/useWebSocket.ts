import { useEffect, useRef, useState, useCallback } from 'react';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

export interface WSMessage {
  type: 'commentary' | 'analysis' | 'stage_update' | 'alert' | 'connected' | 'error';
  event_id: string;
  data: Record<string, unknown>;
  timestamp: string;
}

interface UseWebSocketOptions {
  onMessage?: (msg: WSMessage) => void;
  reconnectDelay?: number;
}

export function useWebSocket(
  eventId: string | null,
  options: UseWebSocketOptions = {}
) {
  const [connected, setConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  const connect = useCallback(() => {
    if (!eventId) return;
    const token = localStorage.getItem('token');
    const url = `${WS_URL}/ws/events/${eventId}${token ? `?token=${token}` : ''}`;

    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      console.log(`[WS] Connected to event ${eventId}`);
    };

    ws.onmessage = (event) => {
      try {
        const msg: WSMessage = JSON.parse(event.data);
        setLastMessage(msg);
        options.onMessage?.(msg);
      } catch (e) {
        // ignore ping/pong
      }
    };

    ws.onclose = () => {
      setConnected(false);
      // Auto-reconnect
      reconnectTimer.current = setTimeout(() => {
        console.log(`[WS] Reconnecting to event ${eventId}...`);
        connect();
      }, options.reconnectDelay || 3000);
    };

    ws.onerror = (err) => {
      console.error('[WS] Error:', err);
    };
  }, [eventId]);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectTimer.current);
      wsRef.current?.close();
    };
  }, [connect]);

  const sendPing = useCallback(() => {
    wsRef.current?.send('ping');
  }, []);

  return { connected, lastMessage, sendPing };
}
