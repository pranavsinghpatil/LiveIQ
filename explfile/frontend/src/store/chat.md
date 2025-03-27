# Chat Store Documentation

## Overview
The chat store manages the state of all chat-related data in the application using Zustand. It handles chat loading, importing, updating, and searching functionality.

## Store Implementation

### Store Definition
```typescript
interface ChatStore {
  // State
  chats: Record<string, Chat>;
  selectedChat: string | null;
  isLoading: boolean;
  error: string | null;
  searchResults: SearchResults | null;
  searchFilters: SearchFilters;
  
  // Actions
  loadChats: () => Promise<void>;
  importChat: (data: ImportChatData) => Promise<Chat>;
  updateChat: (chatId: string, updates: Partial<Chat>) => Promise<void>;
  deleteChat: (chatId: string) => Promise<void>;
  selectChat: (chatId: string | null) => void;
  searchChats: (query: string, filters?: SearchFilters) => Promise<void>;
  clearSearch: () => void;
}

const useChatStore = create<ChatStore>((set, get) => ({
  // Initial state
  chats: {},
  selectedChat: null,
  isLoading: false,
  error: null,
  searchResults: null,
  searchFilters: {},
  
  // Actions
  loadChats: async () => {
    set({ isLoading: true });
    try {
      const response = await api.get<Chat[]>('/api/chats');
      const chatsMap = response.data.reduce((acc, chat) => {
        acc[chat.id] = chat;
        return acc;
      }, {} as Record<string, Chat>);
      set({ chats: chatsMap, isLoading: false });
    } catch (error) {
      set({ error: getErrorMessage(error), isLoading: false });
    }
  },
  
  importChat: async (data) => {
    set({ isLoading: true });
    try {
      const response = await api.post<Chat>('/api/chats/import', data);
      const chat = response.data;
      set((state) => ({
        chats: { ...state.chats, [chat.id]: chat },
        isLoading: false
      }));
      return chat;
    } catch (error) {
      set({ error: getErrorMessage(error), isLoading: false });
      throw error;
    }
  },
  
  updateChat: async (chatId, updates) => {
    try {
      const response = await api.patch<Chat>(
        `/api/chats/${chatId}`,
        updates
      );
      const updatedChat = response.data;
      set((state) => ({
        chats: { ...state.chats, [chatId]: updatedChat }
      }));
    } catch (error) {
      set({ error: getErrorMessage(error) });
      throw error;
    }
  },
  
  deleteChat: async (chatId) => {
    try {
      await api.delete(`/api/chats/${chatId}`);
      set((state) => {
        const { [chatId]: _, ...remainingChats } = state.chats;
        return {
          chats: remainingChats,
          selectedChat: state.selectedChat === chatId ? null : state.selectedChat
        };
      });
    } catch (error) {
      set({ error: getErrorMessage(error) });
      throw error;
    }
  },
  
  selectChat: (chatId) => {
    set({ selectedChat: chatId });
  },
  
  searchChats: async (query, filters = {}) => {
    set({ isLoading: true });
    try {
      const response = await api.get<SearchResults>('/api/chats/search', {
        params: {
          query,
          ...filters
        }
      });
      set({
        searchResults: response.data,
        searchFilters: filters,
        isLoading: false
      });
    } catch (error) {
      set({
        error: getErrorMessage(error),
        searchResults: null,
        isLoading: false
      });
    }
  },
  
  clearSearch: () => {
    set({
      searchResults: null,
      searchFilters: {}
    });
  }
}));
```

## Usage Examples

### Loading Chats
```typescript
function ChatList() {
  const { chats, isLoading, loadChats } = useChatStore();
  
  useEffect(() => {
    loadChats();
  }, []);
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  return (
    <div>
      {Object.values(chats).map((chat) => (
        <ChatItem key={chat.id} chat={chat} />
      ))}
    </div>
  );
}
```

### Importing Chat
```typescript
function ImportDialog() {
  const { importChat } = useChatStore();
  const [file, setFile] = useState<File | null>(null);
  
  const handleImport = async () => {
    if (!file) return;
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const chat = await importChat({
        file: formData,
        platform: 'chatgpt'
      });
      
      toast.success('Chat imported successfully');
      onClose();
    } catch (error) {
      toast.error('Failed to import chat');
    }
  };
  
  return (
    <Dialog>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0])} />
      <Button onClick={handleImport}>Import</Button>
    </Dialog>
  );
}
```

### Searching Chats
```typescript
function SearchBar() {
  const { searchChats, searchFilters } = useChatStore();
  const [query, setQuery] = useState('');
  
  const handleSearch = () => {
    searchChats(query, searchFilters);
  };
  
  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search chats..."
      />
      <Button onClick={handleSearch}>Search</Button>
    </div>
  );
}
```

### Managing Selected Chat
```typescript
function ChatView() {
  const { selectedChat, chats, updateChat } = useChatStore();
  
  if (!selectedChat) {
    return <div>No chat selected</div>;
  }
  
  const chat = chats[selectedChat];
  
  const handleUpdateTitle = async (newTitle: string) => {
    try {
      await updateChat(selectedChat, { title: newTitle });
      toast.success('Chat updated successfully');
    } catch (error) {
      toast.error('Failed to update chat');
    }
  };
  
  return (
    <div>
      <h1>{chat.title}</h1>
      <Button onClick={() => handleUpdateTitle('New Title')}>
        Update Title
      </Button>
    </div>
  );
}
```

## Store Selectors

### Chat Selectors
```typescript
const selectChat = (id: string) => (state: ChatStore) => state.chats[id];

const selectChatsByPlatform = (platform: Platform) => 
  (state: ChatStore) =>
    Object.values(state.chats).filter(
      (chat) => chat.platform === platform
    );

const selectChatCount = (state: ChatStore) =>
  Object.keys(state.chats).length;

const selectHasChats = (state: ChatStore) =>
  selectChatCount(state) > 0;
```

### Search Selectors
```typescript
const selectSearchResults = (state: ChatStore) =>
  state.searchResults?.chats ?? [];

const selectIsSearching = (state: ChatStore) =>
  state.searchResults !== null;

const selectSearchTotal = (state: ChatStore) =>
  state.searchResults?.total ?? 0;
```

## Store Middleware

### Persistence Middleware
```typescript
const persistMiddleware = (config: PersistConfig) =>
  (store: ChatStore) => {
    if (config.loadFromStorage) {
      const stored = localStorage.getItem(config.key);
      if (stored) {
        store.setState(JSON.parse(stored));
      }
    }
    
    store.subscribe((state) => {
      if (config.saveToStorage) {
        localStorage.setItem(config.key, JSON.stringify(state));
      }
    });
  };
```

### Logging Middleware
```typescript
const loggingMiddleware = (store: ChatStore) => {
  store.subscribe((state) => {
    console.log('New state:', state);
  });
};
```

## Error Handling

### Error Types
```typescript
type ChatError =
  | 'IMPORT_ERROR'
  | 'UPDATE_ERROR'
  | 'DELETE_ERROR'
  | 'LOAD_ERROR'
  | 'SEARCH_ERROR';

interface ChatErrorDetails {
  code: ChatError;
  message: string;
  details?: Record<string, any>;
}
```

### Error Handlers
```typescript
const handleChatError = (error: unknown): ChatErrorDetails => {
  if (isApiError(error)) {
    return {
      code: 'IMPORT_ERROR',
      message: error.message,
      details: error.details
    };
  }
  
  return {
    code: 'IMPORT_ERROR',
    message: 'An unknown error occurred'
  };
};
```
