# Frontend Code Documentation

*Last Updated: 2025-03-17*

## Overview

ChatSynth's frontend is built using React with TypeScript, focusing on a responsive and intuitive user interface for managing chat logs across multiple AI platforms.

## Component Architecture

### 1. Layout Components

#### AppLayout
```typescript
// src/components/layout/AppLayout.tsx
const AppLayout: React.FC = () => {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Header />
        <Outlet />
      </div>
    </div>
  );
};
```

**Purpose**: Main application layout with navigation and content areas
**Features**:
- Responsive sidebar
- Dynamic content area
- Mobile-friendly design

#### Sidebar Navigation
```typescript
// src/components/layout/Sidebar.tsx
const Sidebar: React.FC = () => {
  const platforms = useSelector(selectPlatforms);
  
  return (
    <nav className="sidebar">
      <PlatformList platforms={platforms} />
      <TagFilter />
      <DateFilter />
    </nav>
  );
};
```

### 2. Chat Components

#### ChatDashboard
```typescript
// src/components/chat/ChatDashboard.tsx
const ChatDashboard: React.FC = () => {
  const chats = useSelector(selectFilteredChats);
  const dispatch = useDispatch();
  
  useEffect(() => {
    dispatch(fetchChats());
  }, []);
  
  return (
    <div className="chat-dashboard">
      <SearchBar />
      <ChatList chats={chats} />
      <ChatPagination />
    </div>
  );
};
```

**Features**:
- Real-time updates
- Infinite scrolling
- Advanced filtering
- Search functionality

#### ChatViewer
```typescript
// src/components/chat/ChatViewer.tsx
const ChatViewer: React.FC<{ chatId: string }> = ({ chatId }) => {
  const chat = useSelector(state => selectChatById(state, chatId));
  const [activeVersion, setActiveVersion] = useState<number>(1);
  
  return (
    <div className="chat-viewer">
      <ChatHeader chat={chat} />
      <ChatContent 
        content={chat.content} 
        version={activeVersion}
      />
      <AnnotationPanel chatId={chatId} />
      <VersionControl
        versions={chat.versions}
        active={activeVersion}
        onChange={setActiveVersion}
      />
    </div>
  );
};
```

### 3. Import Components

#### ChatImporter
```typescript
// src/components/import/ChatImporter.tsx
const ChatImporter: React.FC = () => {
  const [source, setSource] = useState<string>("");
  const [content, setContent] = useState<string>("");
  
  const handleImport = async () => {
    try {
      await importChat({ source, content });
      showSuccess("Chat imported successfully");
    } catch (error) {
      showError("Failed to import chat");
    }
  };
  
  return (
    <div className="chat-importer">
      <PlatformSelector
        value={source}
        onChange={setSource}
      />
      <ContentInput
        value={content}
        onChange={setContent}
      />
      <ImportButton onClick={handleImport} />
    </div>
  );
};
```

**Supported Platforms**:
- ChatGPT
- Mistral
- Gemini

### 4. Search Components

#### SearchBar
```typescript
// src/components/search/SearchBar.tsx
const SearchBar: React.FC = () => {
  const [query, setQuery] = useState("");
  const debouncedSearch = useDebounce(query, 300);
  
  useEffect(() => {
    if (debouncedSearch) {
      dispatch(searchChats(debouncedSearch));
    }
  }, [debouncedSearch]);
  
  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search chats..."
      />
      <FilterPanel />
    </div>
  );
};
```

#### FilterPanel
```typescript
// src/components/search/FilterPanel.tsx
const FilterPanel: React.FC = () => {
  const filters = useSelector(selectFilters);
  
  return (
    <div className="filter-panel">
      <PlatformFilter
        selected={filters.platforms}
        onChange={updatePlatformFilter}
      />
      <DateRangeFilter
        range={filters.dateRange}
        onChange={updateDateFilter}
      />
      <TagFilter
        tags={filters.tags}
        onChange={updateTagFilter}
      />
    </div>
  );
};
```

## State Management

### 1. Redux Store Structure

#### Store Configuration
```typescript
// src/store/index.ts
const store = configureStore({
  reducer: {
    chats: chatsReducer,
    filters: filtersReducer,
    auth: authReducer,
    ui: uiReducer
  },
  middleware: getDefaultMiddleware()
    .concat(chatMiddleware)
});
```

#### Chat Slice
```typescript
// src/store/slices/chatSlice.ts
interface ChatState {
  ids: string[];
  entities: Record<string, Chat>;
  loading: boolean;
  error: string | null;
}

const chatSlice = createSlice({
  name: 'chats',
  initialState,
  reducers: {
    addChat: (state, action) => {
      chatsAdapter.addOne(state, action.payload);
    },
    updateChat: (state, action) => {
      chatsAdapter.updateOne(state, action.payload);
    },
    setChats: (state, action) => {
      chatsAdapter.setAll(state, action.payload);
    }
  }
});
```

### 2. API Integration

#### Chat Service
```typescript
// src/services/chatService.ts
class ChatService {
  async importChat(data: ChatImport): Promise<Chat> {
    const response = await api.post('/chats/import', data);
    return response.data;
  }
  
  async searchChats(query: string, filters: ChatFilters): Promise<Chat[]> {
    const response = await api.get('/chats/search', {
      params: { query, ...filters }
    });
    return response.data;
  }
  
  async updateAnnotation(
    chatId: string,
    annotation: Annotation
  ): Promise<void> {
    await api.post(`/chats/${chatId}/annotations`, annotation);
  }
}
```

### 3. WebSocket Integration

#### Real-time Updates
```typescript
// src/services/websocket.ts
class WebSocketService {
  private ws: WebSocket;
  
  constructor() {
    this.ws = new WebSocket(WS_URL);
    this.setupListeners();
  }
  
  private setupListeners() {
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case 'chat_updated':
          store.dispatch(updateChat(data.payload));
          break;
        case 'annotation_added':
          store.dispatch(addAnnotation(data.payload));
          break;
      }
    };
  }
}
```

## UI Components

### 1. Common Components

#### Button
```typescript
// src/components/common/Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  variant,
  loading,
  onClick,
  children
}) => {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={loading}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
};
```

#### Modal
```typescript
// src/components/common/Modal.tsx
const Modal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay">
      <div className="modal">
        <header>
          <h2>{title}</h2>
          <button onClick={onClose}>&times;</button>
        </header>
        <div className="modal-content">
          {children}
        </div>
      </div>
    </div>
  );
};
```

## Hooks and Utilities

### 1. Custom Hooks

#### useDebounce
```typescript
// src/hooks/useDebounce.ts
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);
  
  return debouncedValue;
}
```

#### useChat
```typescript
// src/hooks/useChat.ts
function useChat(chatId: string) {
  const chat = useSelector(state => selectChatById(state, chatId));
  const dispatch = useDispatch();
  
  const updateChat = useCallback((data: Partial<Chat>) => {
    dispatch(updateChatAction({ id: chatId, changes: data }));
  }, [chatId]);
  
  return { chat, updateChat };
}
```

### 2. Utility Functions

#### formatters
```typescript
// src/utils/formatters.ts
export const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString();
};

export const truncateText = (text: string, length: number): string => {
  return text.length > length
    ? `${text.substring(0, length)}...`
    : text;
};
```

#### validators
```typescript
// src/utils/validators.ts
export const validateChatImport = (data: ChatImport): boolean => {
  if (!data.content) return false;
  if (!VALID_SOURCES.includes(data.source)) return false;
  return true;
};
```

## Testing Strategy

### 1. Component Tests

#### ChatList Test
```typescript
// src/components/chat/ChatList.test.tsx
describe('ChatList', () => {
  it('renders chat items', () => {
    const chats = [
      { id: '1', title: 'Chat 1' },
      { id: '2', title: 'Chat 2' }
    ];
    
    render(<ChatList chats={chats} />);
    expect(screen.getByText('Chat 1')).toBeInTheDocument();
    expect(screen.getByText('Chat 2')).toBeInTheDocument();
  });
  
  it('handles empty state', () => {
    render(<ChatList chats={[]} />);
    expect(screen.getByText('No chats found')).toBeInTheDocument();
  });
});
```

### 2. Integration Tests

#### Chat Import Flow
```typescript
// src/tests/integration/chatImport.test.tsx
describe('Chat Import Flow', () => {
  it('successfully imports chat', async () => {
    render(<ChatImport />);
    
    // Fill form
    fireEvent.change(
      screen.getByPlaceholderText('Paste chat content'),
      { target: { value: 'test chat' } }
    );
    
    // Select platform
    fireEvent.click(screen.getByText('ChatGPT'));
    
    // Submit
    fireEvent.click(screen.getByText('Import'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('Import successful')).toBeInTheDocument();
    });
  });
});
```

## Performance Optimizations

### 1. Code Splitting
```typescript
// src/App.tsx
const ChatView = lazy(() => import('./pages/ChatView'));
const ImportPage = lazy(() => import('./pages/ImportPage'));
const SettingsPage = lazy(() => import('./pages/SettingsPage'));

const App: React.FC = () => {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/chat/:id" element={<ChatView />} />
        <Route path="/import" element={<ImportPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Suspense>
  );
};
```

### 2. Memoization
```typescript
// src/components/chat/ChatItem.tsx
const ChatItem = memo<ChatItemProps>(({ chat }) => {
  const handleClick = useCallback(() => {
    console.log('Chat clicked:', chat.id);
  }, [chat.id]);
  
  return (
    <div onClick={handleClick}>
      {chat.title}
    </div>
  );
});
```

## Next Steps

### 1. Planned Improvements
- Add drag-and-drop file upload
- Implement chat merging
- Add export templates
- Enhance mobile experience

### 2. Technical Debt
- Optimize bundle size
- Add error boundaries
- Improve accessibility
- Add E2E tests
