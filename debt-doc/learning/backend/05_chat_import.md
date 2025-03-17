# Understanding the Chat Import System

## Overview

The chat import system is a core feature of ChatSynth that allows users to import chat conversations from different AI platforms (ChatGPT, Mistral, Gemini). Here's how it works:

## 1. Import Process

### Step 1: User Input
Users can import chats in two ways:
1. Paste chat content
2. Upload chat file

```python
# In backend/app/api/chat_import.py
from fastapi import APIRouter, UploadFile, File
from typing import Dict, Optional

router = APIRouter()

@router.post("/import/paste")
async def import_chat_paste(
    content: str,
    source: str,
    user_id: int
):
    # Validate content and source
    validate_import_data(content, source)
    
    # Process and save chat
    chat = await process_chat_import(content, source, user_id)
    return chat

@router.post("/import/file")
async def import_chat_file(
    file: UploadFile = File(...),
    source: str = None
):
    # Read file content
    content = await file.read()
    
    # Auto-detect source if not provided
    if not source:
        source = detect_chat_source(content)
    
    # Process and save chat
    chat = await process_chat_import(
        content.decode(),
        source,
        user_id
    )
    return chat
```

### Step 2: Source Detection
We detect which AI platform the chat is from:

```python
# In backend/app/services/chat_import.py
def detect_chat_source(content: str) -> str:
    # Try to parse content
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # If not JSON, try other formats
        return detect_from_text(content)
    
    # Check for platform-specific patterns
    if "messages" in data:
        if any(msg.get("model", "").startswith("gpt-") 
               for msg in data["messages"]):
            return "chatgpt"
        
        if any("mistral" in str(msg.get("model", "")).lower() 
               for msg in data["messages"]):
            return "mistral"
        
        if any("gemini" in str(msg.get("model", "")).lower() 
               for msg in data["messages"]):
            return "gemini"
    
    raise ValueError("Unknown chat source")

def detect_from_text(content: str) -> str:
    # Look for platform-specific patterns in text
    patterns = {
        "chatgpt": r"ChatGPT|GPT-3\.5|GPT-4",
        "mistral": r"Mistral|mistral-\d+",
        "gemini": r"Gemini|Google AI"
    }
    
    for source, pattern in patterns.items():
        if re.search(pattern, content):
            return source
    
    raise ValueError("Unknown chat source")
```

### Step 3: Content Parsing
Each platform has its own parser:

```python
# In backend/app/services/parsers/
from abc import ABC, abstractmethod
from typing import List, Dict

class ChatParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> Dict:
        pass
    
    @abstractmethod
    def validate(self, content: str) -> bool:
        pass

class ChatGPTParser(ChatParser):
    def parse(self, content: str) -> Dict:
        # Parse ChatGPT format
        data = json.loads(content)
        
        messages = []
        for msg in data["messages"]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg.get("timestamp"),
                "model": msg.get("model", "gpt-3.5-turbo")
            })
        
        return {
            "messages": messages,
            "metadata": {
                "platform": "chatgpt",
                "model": data.get("model"),
                "created_at": data.get("created_at")
            }
        }
    
    def validate(self, content: str) -> bool:
        try:
            data = json.loads(content)
            return (
                "messages" in data and
                all("role" in msg and "content" in msg 
                    for msg in data["messages"])
            )
        except:
            return False

class MistralParser(ChatParser):
    def parse(self, content: str) -> Dict:
        # Parse Mistral format
        data = json.loads(content)
        
        messages = []
        for msg in data["conversation"]:
            messages.append({
                "role": "assistant" if msg["from_ai"] else "user",
                "content": msg["text"],
                "timestamp": msg.get("timestamp")
            })
        
        return {
            "messages": messages,
            "metadata": {
                "platform": "mistral",
                "model": data.get("model"),
                "created_at": data.get("start_time")
            }
        }
    
    def validate(self, content: str) -> bool:
        try:
            data = json.loads(content)
            return (
                "conversation" in data and
                all("text" in msg and "from_ai" in msg 
                    for msg in data["conversation"])
            )
        except:
            return False

class GeminiParser(ChatParser):
    def parse(self, content: str) -> Dict:
        # Parse Gemini format
        data = json.loads(content)
        
        messages = []
        for msg in data["chat"]:
            messages.append({
                "role": msg["author"],
                "content": msg["text"],
                "timestamp": msg.get("time")
            })
        
        return {
            "messages": messages,
            "metadata": {
                "platform": "gemini",
                "model": "gemini-pro",
                "created_at": data.get("start_time")
            }
        }
    
    def validate(self, content: str) -> bool:
        try:
            data = json.loads(content)
            return (
                "chat" in data and
                all("author" in msg and "text" in msg 
                    for msg in data["chat"])
            )
        except:
            return False
```

### Step 4: Data Processing
After parsing, we process the chat:

```python
# In backend/app/services/chat_processor.py
class ChatProcessor:
    def __init__(self):
        self.parsers = {
            "chatgpt": ChatGPTParser(),
            "mistral": MistralParser(),
            "gemini": GeminiParser()
        }
    
    async def process_chat(
        self,
        content: str,
        source: str,
        user_id: int
    ) -> Dict:
        # Get correct parser
        parser = self.parsers.get(source)
        if not parser:
            raise ValueError(f"Unsupported source: {source}")
        
        # Validate content
        if not parser.validate(content):
            raise ValueError("Invalid chat format")
        
        # Parse content
        chat_data = parser.parse(content)
        
        # Generate summary
        summary = await self.generate_summary(chat_data)
        
        # Extract topics
        topics = await self.extract_topics(chat_data)
        
        # Save to database
        chat = ChatLog(
            user_id=user_id,
            source=source,
            content=chat_data["messages"],
            summary=summary,
            topics=topics,
            metadata=chat_data["metadata"]
        )
        db.add(chat)
        await db.commit()
        
        return chat
    
    async def generate_summary(self, chat_data: Dict) -> str:
        # Combine messages into context
        context = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in chat_data["messages"]
        )
        
        # Use AI to generate summary
        summary = await openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this conversation:"},
                {"role": "user", "content": context}
            ]
        )
        
        return summary.choices[0].message.content
    
    async def extract_topics(self, chat_data: Dict) -> List[str]:
        # Similar to summary, but extract key topics
        context = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in chat_data["messages"]
        )
        
        topics = await openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract key topics:"},
                {"role": "user", "content": context}
            ]
        )
        
        return topics.choices[0].message.content.split(",")
```

## 2. Frontend Integration

### Import Component
Here's how users interact with the import system:

```typescript
// In frontend/src/components/ChatImport.tsx
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { importChat } from '../store/actions';

interface ChatImportProps {
    onSuccess?: () => void;
}

export const ChatImport: React.FC<ChatImportProps> = ({
    onSuccess
}) => {
    const [content, setContent] = useState('');
    const [source, setSource] = useState<string>('');
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const dispatch = useDispatch();
    
    // Handle paste import
    const handlePasteImport = async () => {
        try {
            setLoading(true);
            setError(null);
            
            const result = await dispatch(
                importChat({
                    type: 'paste',
                    content,
                    source
                })
            );
            
            if (importChat.fulfilled.match(result)) {
                setContent('');
                setSource('');
                onSuccess?.();
            }
        } catch (err) {
            setError('Failed to import chat');
        } finally {
            setLoading(false);
        }
    };
    
    // Handle file import
    const handleFileImport = async () => {
        if (!file) return;
        
        try {
            setLoading(true);
            setError(null);
            
            const result = await dispatch(
                importChat({
                    type: 'file',
                    file,
                    source
                })
            );
            
            if (importChat.fulfilled.match(result)) {
                setFile(null);
                setSource('');
                onSuccess?.();
            }
        } catch (err) {
            setError('Failed to import chat');
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="chat-import">
            <h2>Import Chat</h2>
            
            {/* Source Selection */}
            <div className="source-select">
                <label>Source:</label>
                <select
                    value={source}
                    onChange={e => setSource(e.target.value)}
                >
                    <option value="">Auto-detect</option>
                    <option value="chatgpt">ChatGPT</option>
                    <option value="mistral">Mistral</option>
                    <option value="gemini">Gemini</option>
                </select>
            </div>
            
            {/* Paste Import */}
            <div className="paste-import">
                <h3>Paste Chat</h3>
                <textarea
                    value={content}
                    onChange={e => setContent(e.target.value)}
                    placeholder="Paste chat content here..."
                    rows={10}
                />
                <button
                    onClick={handlePasteImport}
                    disabled={!content || loading}
                >
                    Import Pasted Chat
                </button>
            </div>
            
            {/* File Import */}
            <div className="file-import">
                <h3>Upload File</h3>
                <input
                    type="file"
                    accept=".json,.txt"
                    onChange={e => setFile(e.files?.[0] || null)}
                />
                <button
                    onClick={handleFileImport}
                    disabled={!file || loading}
                >
                    Import File
                </button>
            </div>
            
            {/* Error Display */}
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            
            {/* Loading State */}
            {loading && (
                <div className="loading">
                    Importing chat...
                </div>
            )}
        </div>
    );
};
```

## Common Questions

1. **What chat formats are supported?**
   - ChatGPT JSON export
   - Mistral conversation format
   - Gemini chat export
   - Plain text (with auto-detection)

2. **How is the source detected?**
   - JSON structure analysis
   - Platform-specific patterns
   - Model name detection
   - User can override detection

3. **What happens if import fails?**
   - Validation errors shown
   - Original content preserved
   - User can try again
   - Detailed error messages

## Best Practices

1. **Input Validation**
   - Check format before parsing
   - Validate required fields
   - Handle malformed input
   - Provide clear errors

2. **Error Handling**
   - Catch parsing errors
   - Show user-friendly messages
   - Log detailed errors
   - Preserve user input

3. **Performance**
   - Async processing
   - Batch database operations
   - Stream large files
   - Cache parsed results
