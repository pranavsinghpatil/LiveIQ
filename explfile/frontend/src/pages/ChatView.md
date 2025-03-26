# ChatView Page

## Purpose
The ChatView page displays detailed chat conversations in VoxStitch, providing message history, context linking, and annotation capabilities with a modern gradient-styled interface.

## Component Structure

### Main Component
```typescript
interface ChatViewProps {
  className?: string;
}

const ChatView: React.FC<ChatViewProps> = ({
  className
}) => {
  // Component implementation
};
```

## Features

### 1. Chat Header
```typescript
const ChatHeader: React.FC<{ chat: Chat }> = ({ chat }) => (
  <div className="sticky top-0 z-10 bg-surface-50/80 backdrop-blur-sm border-b border-primary/20">
    <div className="px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <PlatformIcon
            platform={chat.platform}
            className="w-8 h-8"
          />
          <div>
            <h1 className="text-xl font-semibold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
              {chat.title}
            </h1>
            <p className="text-sm text-text/60">
              {formatDate(chat.createdAt)} • {chat.messageCount} messages
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <Button
            variant="ghost"
            leftIcon={<EditIcon />}
            onClick={() => openAnnotationPanel()}
          >
            Annotate
          </Button>
          <Button
            variant="ghost"
            leftIcon={<ShareIcon />}
            onClick={() => openShareDialog()}
          >
            Share
          </Button>
          <Button
            variant="ghost"
            leftIcon={<DownloadIcon />}
            onClick={() => exportChat(chat.id)}
          >
            Export
          </Button>
        </div>
      </div>
    </div>
  </div>
);
```

### 2. Message List
```typescript
const MessageList: React.FC<{
  messages: Message[];
  annotations: Annotation[];
}> = ({ messages, annotations }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex-1 overflow-y-auto px-6 py-4">
      <div className="space-y-6">
        {messages.map((message) => (
          <MessageItem
            key={message.id}
            message={message}
            annotation={annotations.find(a => a.messageId === message.id)}
          />
        ))}
      </div>
      <div ref={messagesEndRef} />
    </div>
  );
};
```

### 3. Message Item
```typescript
const MessageItem: React.FC<{
  message: Message;
  annotation?: Annotation;
}> = ({ message, annotation }) => (
  <div className={clsx(
    'group relative',
    'rounded-lg p-4',
    'bg-gradient-to-r',
    message.role === 'user'
      ? 'from-primary-500/5 to-primary-600/5'
      : 'from-surface-100 to-surface-200'
  )}>
    <div className="flex items-start space-x-3">
      <Avatar
        user={message.role === 'user' ? message.user : message.assistant}
        className="w-8 h-8"
      />
      <div className="flex-1">
        <div className="flex items-center space-x-2">
          <span className="font-medium">
            {message.role === 'user' ? message.user.name : 'Assistant'}
          </span>
          <span className="text-sm text-text/60">
            {formatTime(message.timestamp)}
          </span>
        </div>
        <div className="mt-1 prose prose-sm max-w-none">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
        {annotation && (
          <div className="mt-3 p-3 rounded-lg bg-yellow-50 border border-yellow-200">
            <p className="text-sm text-yellow-800">
              {annotation.content}
            </p>
          </div>
        )}
      </div>
    </div>
    <div className={clsx(
      'absolute right-4 top-4',
      'opacity-0 group-hover:opacity-100',
      'transition-opacity'
    )}>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => openAnnotationDialog(message.id)}
      >
        <PencilIcon className="w-4 h-4" />
      </Button>
    </div>
  </div>
);
```

### 4. Annotation Panel
```typescript
const AnnotationPanel: React.FC<{
  isOpen: boolean;
  onClose: () => void;
}> = ({ isOpen, onClose }) => (
  <div className={clsx(
    'fixed inset-y-0 right-0 w-96',
    'bg-gradient-to-b from-surface-50 to-surface-100',
    'border-l border-primary/20',
    'transform transition-transform duration-200',
    isOpen ? 'translate-x-0' : 'translate-x-full'
  )}>
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-primary/20">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Annotations</h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
          >
            <XIcon className="w-5 h-5" />
          </Button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        <AnnotationList />
      </div>
    </div>
  </div>
);
```

## State Management

### Chat State
```typescript
const useChatState = (chatId: string) => {
  const [chat, setChat] = useState<Chat | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [annotations, setAnnotations] = useState<Annotation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchChat = async () => {
      try {
        const [chatResponse, messagesResponse, annotationsResponse] = await Promise.all([
          api.get(`/chats/${chatId}`),
          api.get(`/chats/${chatId}/messages`),
          api.get(`/chats/${chatId}/annotations`)
        ]);

        setChat(chatResponse.data);
        setMessages(messagesResponse.data);
        setAnnotations(annotationsResponse.data);
      } catch (error) {
        console.error('Failed to fetch chat:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchChat();
  }, [chatId]);

  return {
    chat,
    messages,
    annotations,
    isLoading
  };
};
```

### Annotation State
```typescript
const useAnnotations = (chatId: string) => {
  const [annotations, setAnnotations] = useState<Annotation[]>([]);

  const addAnnotation = async (messageId: string, content: string) => {
    try {
      const response = await api.post(`/chats/${chatId}/annotations`, {
        messageId,
        content
      });
      setAnnotations(prev => [...prev, response.data]);
    } catch (error) {
      console.error('Failed to add annotation:', error);
    }
  };

  const updateAnnotation = async (annotationId: string, content: string) => {
    try {
      const response = await api.put(`/annotations/${annotationId}`, {
        content
      });
      setAnnotations(prev =>
        prev.map(a => a.id === annotationId ? response.data : a)
      );
    } catch (error) {
      console.error('Failed to update annotation:', error);
    }
  };

  return {
    annotations,
    addAnnotation,
    updateAnnotation
  };
};
```

## UI Components

### 1. Loading State
```typescript
const ChatSkeleton: React.FC = () => (
  <div className="h-full flex flex-col">
    <div className="px-6 py-4 border-b border-primary/20">
      <div className="animate-pulse space-y-2">
        <div className="h-6 w-1/3 bg-gradient-to-r from-surface-200 to-surface-300 rounded" />
        <div className="h-4 w-1/4 bg-gradient-to-r from-surface-200 to-surface-300 rounded" />
      </div>
    </div>
    <div className="flex-1 p-6">
      <div className="space-y-6">
        {Array.from({ length: 5 }).map((_, i) => (
          <div
            key={i}
            className="animate-pulse space-y-2"
          >
            <div className="h-4 w-1/6 bg-gradient-to-r from-surface-200 to-surface-300 rounded" />
            <div className="h-20 bg-gradient-to-r from-surface-200 to-surface-300 rounded" />
          </div>
        ))}
      </div>
    </div>
  </div>
);
```

### 2. Share Dialog
```typescript
const ShareDialog: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  chatId: string;
}> = ({ isOpen, onClose, chatId }) => (
  <Dialog
    open={isOpen}
    onClose={onClose}
    className="max-w-md w-full"
  >
    <div className="p-6">
      <h2 className="text-lg font-semibold mb-4">
        Share Chat
      </h2>
      <div className="space-y-4">
        <div>
          <label className="text-sm font-medium text-text/60">
            Share Link
          </label>
          <div className="mt-1 flex items-center space-x-2">
            <Input
              value={`${window.location.origin}/chats/${chatId}`}
              readOnly
            />
            <Button
              variant="primary"
              onClick={() => copyToClipboard()}
            >
              Copy
            </Button>
          </div>
        </div>
        <div>
          <label className="text-sm font-medium text-text/60">
            Share Settings
          </label>
          <div className="mt-1 space-y-2">
            <Checkbox
              label="Allow comments"
              checked={allowComments}
              onChange={setAllowComments}
            />
            <Checkbox
              label="Allow annotations"
              checked={allowAnnotations}
              onChange={setAllowAnnotations}
            />
          </div>
        </div>
      </div>
    </div>
  </Dialog>
);
```

## Integration Points

### Export Integration
```typescript
const useExport = () => {
  const exportChat = async (chatId: string) => {
    try {
      const response = await api.get(`/chats/${chatId}/export`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(response.data);
      const link = document.createElement('a');
      link.href = url;
      link.download = `chat-${chatId}.json`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to export chat:', error);
    }
  };

  return { exportChat };
};
```

## Testing
```typescript
describe('ChatView', () => {
  it('loads chat data correctly', async () => {
    const { findByText } = render(<ChatView />);
    expect(await findByText('Chat Title')).toBeInTheDocument();
  });

  it('displays messages in correct order', () => {
    const { getAllByRole } = render(<ChatView />);
    const messages = getAllByRole('article');
    expect(messages).toHaveLength(5);
  });

  it('handles annotations correctly', () => {
    const { getByText } = render(<ChatView />);
    expect(getByText('Add Annotation')).toBeEnabled();
  });
});
```

## Recent Updates
- Added gradient styling
- Improved message display
- Enhanced annotation system
- Added sharing functionality
- Improved loading states

## Accessibility Features
- ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support
- Loading indicators

## Performance Considerations
- Message virtualization
- Lazy loading
- Optimized re-renders
- Efficient data fetching
- Image optimization
