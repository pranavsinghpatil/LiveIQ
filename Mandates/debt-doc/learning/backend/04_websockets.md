# Understanding WebSockets in ChatSynth

## What are WebSockets?

WebSockets provide a two-way communication channel between your browser and the server. Unlike regular HTTP requests:
- Connection stays open
- Both sides can send messages
- Real-time updates

In ChatSynth, we use WebSockets for:
1. Live chat updates
2. Real-time notifications
3. Collaborative features

## Basic Implementation

### 1. Server-Side Setup
Here's how we set up WebSockets in FastAPI:

```python
# In backend/app/websockets.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List

# Store active connections
class ConnectionManager:
    def __init__(self):
        # Keep track of active connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        # Accept the connection
        await websocket.accept()
        
        # Add to active connections
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    async def disconnect(self, websocket: WebSocket, user_id: int):
        # Remove from active connections
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_message(self, message: dict, user_id: int):
        # Send to all connections for this user
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

# Create manager instance
manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Connect
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Wait for messages
            data = await websocket.receive_json()
            
            # Handle different message types
            if data["type"] == "chat_update":
                # Process chat update
                updated_chat = process_chat_update(data["chat"])
                
                # Send update to all user's connections
                await manager.send_message({
                    "type": "chat_updated",
                    "chat": updated_chat
                }, user_id)
                
            elif data["type"] == "notification":
                # Handle notification
                await manager.send_message({
                    "type": "notification",
                    "message": data["message"]
                }, user_id)
    
    except WebSocketDisconnect:
        # Clean up on disconnect
        await manager.disconnect(websocket, user_id)
```

### 2. Client-Side Integration
Here's how we use WebSockets in our React frontend:

```typescript
// In frontend/src/hooks/useWebSocket.ts
import { useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { updateChat, addNotification } from '../store/actions';

interface WebSocketMessage {
    type: string;
    [key: string]: any;
}

export function useWebSocket(userId: number) {
    const ws = useRef<WebSocket | null>(null);
    const dispatch = useDispatch();
    
    useEffect(() => {
        // Create WebSocket connection
        ws.current = new WebSocket(
            `ws://localhost:8000/ws/${userId}`
        );
        
        // Handle connection open
        ws.current.onopen = () => {
            console.log('WebSocket Connected');
        };
        
        // Handle messages
        ws.current.onmessage = (event) => {
            const data: WebSocketMessage = JSON.parse(event.data);
            
            switch (data.type) {
                case 'chat_updated':
                    // Update chat in Redux store
                    dispatch(updateChat(data.chat));
                    break;
                    
                case 'notification':
                    // Show notification
                    dispatch(addNotification(data.message));
                    break;
                    
                default:
                    console.warn('Unknown message type:', data.type);
            }
        };
        
        // Handle errors
        ws.current.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        // Clean up on unmount
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, [userId, dispatch]);
    
    // Function to send messages
    const sendMessage = (message: WebSocketMessage) => {
        if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify(message));
        }
    };
    
    return { sendMessage };
}

// Using the hook in a component
function ChatEditor({ chatId }: { chatId: number }) {
    const { sendMessage } = useWebSocket(userId);
    
    const handleUpdate = (newContent: string) => {
        // Send update through WebSocket
        sendMessage({
            type: 'chat_update',
            chat: {
                id: chatId,
                content: newContent
            }
        });
    };
    
    return (
        <div>
            {/* Chat editor UI */}
        </div>
    );
}
```

## Real-Time Features

### 1. Live Chat Updates
When a chat is modified:

```typescript
// In frontend/src/components/ChatViewer.tsx
function ChatViewer({ chatId }: { chatId: number }) {
    const { sendMessage } = useWebSocket(userId);
    const chat = useSelector(state => 
        selectChatById(state, chatId)
    );
    
    // Handle edit
    const handleEdit = async (messageId: number, newContent: string) => {
        // Send update through WebSocket
        sendMessage({
            type: 'chat_update',
            chat: {
                id: chatId,
                messageId: messageId,
                content: newContent
            }
        });
    };
    
    return (
        <div className="chat-viewer">
            {chat.messages.map(message => (
                <ChatMessage
                    key={message.id}
                    message={message}
                    onEdit={handleEdit}
                />
            ))}
        </div>
    );
}
```

### 2. Real-Time Notifications
For system notifications:

```typescript
// In frontend/src/components/NotificationSystem.tsx
function NotificationSystem() {
    const { sendMessage } = useWebSocket(userId);
    const notifications = useSelector(
        state => state.notifications
    );
    
    // Show notifications
    return (
        <div className="notifications">
            {notifications.map(notification => (
                <Notification
                    key={notification.id}
                    message={notification.message}
                    type={notification.type}
                />
            ))}
        </div>
    );
}

// Notification component
function Notification({ message, type }: NotificationProps) {
    return (
        <div className={`notification ${type}`}>
            {message}
        </div>
    );
}
```

### 3. Error Handling
Robust error handling for WebSocket connections:

```typescript
// In frontend/src/hooks/useWebSocket.ts
function useWebSocket(userId: number) {
    // ... previous code ...
    
    // Reconnection logic
    const [retryCount, setRetryCount] = useState(0);
    const maxRetries = 5;
    
    const connect = useCallback(() => {
        ws.current = new WebSocket(
            `ws://localhost:8000/ws/${userId}`
        );
        
        ws.current.onclose = () => {
            console.log('WebSocket disconnected');
            
            // Try to reconnect
            if (retryCount < maxRetries) {
                setTimeout(() => {
                    setRetryCount(prev => prev + 1);
                    connect();
                }, 1000 * Math.pow(2, retryCount)); // Exponential backoff
            }
        };
        
        // Reset retry count on successful connection
        ws.current.onopen = () => {
            setRetryCount(0);
        };
    }, [userId, retryCount]);
    
    useEffect(() => {
        connect();
        
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, [connect]);
    
    // ... rest of the code ...
}
```

## Best Practices

1. **Connection Management**
   - Keep track of active connections
   - Clean up on disconnect
   - Handle reconnection gracefully

2. **Message Types**
   - Use clear message types
   - Validate message format
   - Handle unknown types

3. **Error Handling**
   - Implement reconnection logic
   - Log errors appropriately
   - Show user-friendly messages

4. **Performance**
   - Don't send unnecessary updates
   - Batch multiple changes
   - Use appropriate data structures

## Common Questions

1. **When to use WebSockets vs HTTP?**
   - WebSockets: Real-time updates
   - HTTP: Regular requests
   - Consider data frequency

2. **How to handle disconnections?**
   - Implement reconnection logic
   - Store unsent messages
   - Show connection status

3. **Security considerations?**
   - Authenticate connections
   - Validate messages
   - Use secure WebSocket (wss://)
