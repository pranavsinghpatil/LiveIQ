# ChatList Component

## Purpose
The ChatList component displays a list of imported chats in VoxStitch, providing sorting, filtering, and interaction capabilities for managing chat conversations.

## Component Structure

### Main Component
```typescript
interface ChatListProps {
  onChatSelect: (chatId: string) => void;
  selectedChatId?: string;
  filter?: ChatFilter;
  sortBy?: SortOption;
}

const ChatList: React.FC<ChatListProps> = ({
  onChatSelect,
  selectedChatId,
  filter,
  sortBy = 'newest'
}) => {
  // Component implementation
};
```

### Chat Item Component
```typescript
interface ChatItemProps {
  chat: Chat;
  isSelected: boolean;
  onClick: () => void;
}

const ChatItem: React.FC<ChatItemProps> = ({
  chat,
  isSelected,
  onClick
}) => {
  return (
    <div
      className={clsx(
        'p-4 rounded-lg cursor-pointer transition-all',
        'hover:bg-gradient-to-r hover:from-primary-500/10 hover:to-primary-600/10',
        isSelected && 'bg-gradient-to-r from-primary-500/20 to-primary-600/20'
      )}
      onClick={onClick}
    >
      {/* Chat item content */}
    </div>
  );
};
```

## Features

### 1. Chat Filtering
```typescript
const filterChats = (chats: Chat[], filter: ChatFilter) => {
  return chats.filter(chat => {
    if (filter.platform && chat.platform !== filter.platform) return false;
    if (filter.dateRange) {
      const chatDate = new Date(chat.createdAt);
      if (chatDate < filter.dateRange.start || chatDate > filter.dateRange.end) {
        return false;
      }
    }
    if (filter.search) {
      return chat.title.toLowerCase().includes(filter.search.toLowerCase());
    }
    return true;
  });
};
```

### 2. Chat Sorting
```typescript
const sortChats = (chats: Chat[], sortBy: SortOption) => {
  return [...chats].sort((a, b) => {
    switch (sortBy) {
      case 'newest':
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
      case 'oldest':
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
      case 'platform':
        return a.platform.localeCompare(b.platform);
      default:
        return 0;
    }
  });
};
```

### 3. Virtual Scrolling
```typescript
const VirtualizedChatList: React.FC<{chats: Chat[]}> = ({ chats }) => {
  return (
    <VirtualList
      height={800}
      itemCount={chats.length}
      itemSize={100}
      width="100%"
    >
      {({ index, style }) => (
        <ChatItem
          chat={chats[index]}
          style={style}
        />
      )}
    </VirtualList>
  );
};
```

### 4. Chat Actions
```typescript
const ChatActions: React.FC<{chat: Chat}> = ({ chat }) => {
  return (
    <div className="flex gap-2">
      <IconButton
        icon={<StarIcon />}
        onClick={() => toggleFavorite(chat.id)}
        className={chat.isFavorite ? 'text-yellow-500' : 'text-gray-400'}
      />
      <IconButton
        icon={<ShareIcon />}
        onClick={() => shareChat(chat.id)}
      />
      <IconButton
        icon={<TrashIcon />}
        onClick={() => deleteChat(chat.id)}
        className="text-red-400"
      />
    </div>
  );
};
```

## State Management

### Chat Data Store
```typescript
interface ChatStore {
  chats: Chat[];
  loading: boolean;
  error: string | null;
  fetchChats: () => Promise<void>;
  deleteChat: (id: string) => Promise<void>;
  updateChat: (id: string, data: Partial<Chat>) => Promise<void>;
}

const useChatStore = create<ChatStore>((set) => ({
  chats: [],
  loading: false,
  error: null,
  fetchChats: async () => {
    set({ loading: true });
    try {
      const response = await api.get('/chats');
      set({ chats: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  // Other actions
}));
```

## UI/UX Features

### 1. Loading States
```typescript
const LoadingState: React.FC = () => (
  <div className="space-y-4">
    {Array.from({ length: 5 }).map((_, i) => (
      <div
        key={i}
        className="animate-pulse bg-gradient-to-r from-gray-200 to-gray-300 h-24 rounded-lg"
      />
    ))}
  </div>
);
```

### 2. Empty State
```typescript
const EmptyState: React.FC = () => (
  <div className="text-center py-8">
    <div className="text-6xl mb-4">💬</div>
    <h3 className="text-xl font-semibold mb-2">No Chats Yet</h3>
    <p className="text-gray-500">
      Import your first chat to get started
    </p>
    <Button
      variant="primary"
      className="mt-4"
      onClick={() => openImportDialog()}
    >
      Import Chat
    </Button>
  </div>
);
```

### 3. Error State
```typescript
const ErrorState: React.FC<{error: string}> = ({ error }) => (
  <div className="text-center py-8 text-red-500">
    <AlertIcon className="w-12 h-12 mx-auto mb-4" />
    <h3 className="text-xl font-semibold mb-2">Error Loading Chats</h3>
    <p>{error}</p>
    <Button
      variant="outline"
      className="mt-4"
      onClick={() => window.location.reload()}
    >
      Retry
    </Button>
  </div>
);
```

## Performance Optimizations

### 1. Memoization
```typescript
const MemoizedChatItem = React.memo(ChatItem, (prev, next) => {
  return (
    prev.chat.id === next.chat.id &&
    prev.isSelected === next.isSelected &&
    prev.chat.updatedAt === next.chat.updatedAt
  );
});
```

### 2. Debounced Search
```typescript
const debouncedSearch = useCallback(
  debounce((term: string) => {
    setSearchTerm(term);
  }, 300),
  []
);
```

## Integration Points

### API Integration
```typescript
const fetchChats = async () => {
  try {
    const response = await api.get('/chats');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch chats:', error);
    throw error;
  }
};
```

### Event Handling
```typescript
const handleChatSelect = (chatId: string) => {
  onChatSelect(chatId);
  trackEvent('chat_selected', { chatId });
};
```

## Related Components
- `ImportChat`: For importing new chats
- `SearchBar`: For filtering chats
- `ChatView`: For displaying selected chat
- `FilterPanel`: For advanced filtering options

## Testing
```typescript
describe('ChatList', () => {
  it('renders chat items correctly', () => {
    const chats = mockChats;
    render(<ChatList chats={chats} />);
    expect(screen.getAllByRole('listitem')).toHaveLength(chats.length);
  });

  it('handles empty state', () => {
    render(<ChatList chats={[]} />);
    expect(screen.getByText('No Chats Yet')).toBeInTheDocument();
  });
});
```

## Recent Updates
- Added gradient hover effects
- Improved virtual scrolling performance
- Enhanced filtering capabilities
- Added chat actions menu
- Improved loading states

## Accessibility Features
- Keyboard navigation support
- ARIA labels and roles
- Focus management
- Screen reader support
