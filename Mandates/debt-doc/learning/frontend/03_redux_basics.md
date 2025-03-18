# Understanding Redux in ChatSynth

## What is Redux?

Redux is like a central storage for all our app's data. Think of it as a big container where we keep all the chats, user info, and settings. This helps us:
1. Keep data organized
2. Share data between components
3. Update data consistently

## Basic Concepts

### 1. Store
The store is where all our data lives:

```typescript
// In store/index.ts - Setting up our store
import { configureStore } from '@reduxjs/toolkit';

// Our store setup
const store = configureStore({
    reducer: {
        chats: chatsReducer,     // Handles chat data
        auth: authReducer,       // Handles user login
        ui: uiReducer           // Handles UI state
    }
});

// Let's break this down:
// 1. configureStore creates our data container
// 2. reducer tells Redux how to update data
// 3. Each reducer handles specific data (chats, auth, etc.)
```

### 2. Slices
Slices are pieces of our store for different features:

```typescript
// In store/slices/chatSlice.ts - Managing chat data
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Define what chat data looks like
interface ChatState {
    items: ChatConversation[];  // List of chats
    loading: boolean;          // Are we loading?
    error: string | null;      // Any error message
    selectedChatId: number | null;  // Currently selected chat
}

// Initial state when app starts
const initialState: ChatState = {
    items: [],
    loading: false,
    error: null,
    selectedChatId: null
};

// Create the chat slice
const chatSlice = createSlice({
    name: 'chats',
    initialState,
    reducers: {
        // Start loading chats
        startLoading: (state) => {
            state.loading = true;
            state.error = null;
        },
        
        // Successfully loaded chats
        chatsLoaded: (state, action: PayloadAction<ChatConversation[]>) => {
            state.items = action.payload;
            state.loading = false;
        },
        
        // Failed to load chats
        loadError: (state, action: PayloadAction<string>) => {
            state.loading = false;
            state.error = action.payload;
        },
        
        // Select a chat
        selectChat: (state, action: PayloadAction<number>) => {
            state.selectedChatId = action.payload;
        }
    }
});

// Understanding the parts:
// 1. interface ChatState - Shape of our data
// 2. initialState - Starting data
// 3. reducers - Functions to update data
// 4. PayloadAction - Type for data being passed
```

### 3. Actions
Actions are how we tell Redux to update data:

```typescript
// In store/actions/chatActions.ts
import { createAsyncThunk } from '@reduxjs/toolkit';

// Action to load chats
export const loadChats = createAsyncThunk(
    'chats/load',
    async (_, { rejectWithValue }) => {
        try {
            // Get chats from API
            const response = await fetch('/api/chats');
            const data = await response.json();
            return data;
        } catch (error) {
            return rejectWithValue('Failed to load chats');
        }
    }
);

// Action to import a new chat
export const importChat = createAsyncThunk(
    'chats/import',
    async (chatData: {
        content: string;
        source: string;
    }, { rejectWithValue }) => {
        try {
            const response = await fetch('/api/chats/import', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(chatData)
            });
            return await response.json();
        } catch (error) {
            return rejectWithValue('Failed to import chat');
        }
    }
);

// Understanding actions:
// 1. createAsyncThunk handles async operations
// 2. First argument is action type
// 3. Second argument is async function
// 4. rejectWithValue handles errors
```

### 4. Using Redux in Components
How we connect components to Redux:

```typescript
// In components/ChatList.tsx
import { useSelector, useDispatch } from 'react-redux';
import { loadChats, selectChat } from '../store/actions/chatActions';

const ChatList: React.FC = () => {
    // Get data from Redux
    const chats = useSelector((state: RootState) => state.chats.items);
    const loading = useSelector((state: RootState) => state.chats.loading);
    const error = useSelector((state: RootState) => state.chats.error);
    
    // Get dispatch function
    const dispatch = useDispatch();
    
    // Load chats when component mounts
    useEffect(() => {
        dispatch(loadChats());
    }, [dispatch]);
    
    // Handle chat selection
    const handleChatClick = (chatId: number) => {
        dispatch(selectChat(chatId));
    };
    
    // Show loading state
    if (loading) {
        return <div>Loading chats...</div>;
    }
    
    // Show error if any
    if (error) {
        return <div className="error">{error}</div>;
    }
    
    // Show chat list
    return (
        <div className="chat-list">
            {chats.map(chat => (
                <ChatPreview
                    key={chat.id}
                    chat={chat}
                    onClick={() => handleChatClick(chat.id)}
                />
            ))}
        </div>
    );
};

// Understanding Redux in components:
// 1. useSelector gets data from store
// 2. useDispatch gets function to update store
// 3. dispatch(action) updates the store
```

### 5. Real Example: Chat Import Feature

```typescript
// In components/ChatImport.tsx
import { useDispatch, useSelector } from 'react-redux';
import { importChat } from '../store/actions/chatActions';

const ChatImport: React.FC = () => {
    // Local state for form
    const [content, setContent] = useState('');
    const [source, setSource] = useState<'chatgpt' | 'mistral' | 'gemini'>('chatgpt');
    
    // Get Redux dispatch
    const dispatch = useDispatch();
    
    // Get import status from Redux
    const importing = useSelector((state: RootState) => state.chats.importing);
    const importError = useSelector((state: RootState) => state.chats.importError);
    
    // Handle form submission
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Dispatch import action
        const result = await dispatch(importChat({
            content,
            source
        }));
        
        // Check if import succeeded
        if (importChat.fulfilled.match(result)) {
            // Clear form
            setContent('');
            setSource('chatgpt');
            // Show success message
            toast.success('Chat imported successfully');
        }
    };
    
    return (
        <form onSubmit={handleSubmit} className="chat-import">
            <select
                value={source}
                onChange={e => setSource(e.target.value as typeof source)}
            >
                <option value="chatgpt">ChatGPT</option>
                <option value="mistral">Mistral</option>
                <option value="gemini">Gemini</option>
            </select>
            
            <textarea
                value={content}
                onChange={e => setContent(e.target.value)}
                placeholder="Paste chat content here..."
            />
            
            {importError && (
                <div className="error">{importError}</div>
            )}
            
            <button type="submit" disabled={importing}>
                {importing ? 'Importing...' : 'Import Chat'}
            </button>
        </form>
    );
};

// Understanding this component:
// 1. Local state for form fields
// 2. Redux state for import status
// 3. dispatch(importChat) to start import
// 4. Handle success/error cases
```

## Practice Exercise

Create a chat filter feature using Redux:

```typescript
// Your task: Complete these files

// 1. Create slice for filters
interface FilterState {
    source?: string;
    tags?: string[];
    dateRange?: {
        start: string;
        end: string;
    };
}

const filterSlice = createSlice({
    name: 'filters',
    initialState: {
        // Your code here
    },
    reducers: {
        // Your code here
    }
});

// 2. Create component using the filters
const ChatFilter: React.FC = () => {
    // Your code here
};
```

## Next Steps
1. Try the practice exercise
2. Learn about Redux middleware
3. Study Redux Toolkit features
4. Explore Redux DevTools

## Common Questions

1. **Why use Redux?**
   - Central data storage
   - Predictable updates
   - Easy debugging
   - State persistence

2. **When to use Redux vs local state?**
   - Redux for shared data
   - Local state for component-specific data
   - Redux for complex updates
   - Local state for simple forms

3. **Redux Toolkit vs plain Redux?**
   - Simpler setup
   - Less boilerplate
   - Better TypeScript support
   - Built-in best practices
