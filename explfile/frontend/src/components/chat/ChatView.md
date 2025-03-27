# ChatView Component Documentation

## Overview
The ChatView component displays the selected chat conversation with messages, media attachments, and analysis results. It supports message navigation, media playback, and chat analysis features.

## Component Implementation

### Component Structure
```typescript
interface ChatViewProps {
  chatId: string;
  onClose?: () => void;
}

const ChatView: React.FC<ChatViewProps> = ({ chatId, onClose }) => {
  const { chat, isLoading } = useChatStore(
    (state) => ({
      chat: state.chats[chatId],
      isLoading: state.isLoading
    })
  );
  
  // Message list ref for scrolling
  const messageListRef = useRef<HTMLDivElement>(null);
  
  // Auto scroll to bottom on new messages
  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [chat?.messages]);
  
  // Handle media playback
  const handleMediaPlay = (media: MediaAttachment) => {
    switch (media.type) {
      case 'audio':
      case 'video':
        // Show media player modal
        openModal({
          id: 'media-player',
          title: 'Media Player',
          content: <MediaPlayer media={media} />
        });
        break;
      case 'image':
        // Show image viewer
        openModal({
          id: 'image-viewer',
          title: 'Image Viewer',
          content: <ImageViewer image={media} />
        });
        break;
    }
  };
  
  // Handle message actions
  const handleMessageAction = (
    message: ChatMessage,
    action: MessageAction
  ) => {
    switch (action) {
      case 'copy':
        copyToClipboard(message.content);
        toast.success('Message copied to clipboard');
        break;
      case 'bookmark':
        toggleBookmark(chatId, message.id);
        break;
      case 'share':
        shareMessage(chatId, message.id);
        break;
    }
  };
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  if (!chat) {
    return <div>Chat not found</div>;
  }
  
  return (
    <div className="chat-view">
      {/* Chat header */}
      <header className="chat-header">
        <div className="chat-info">
          <h2>{chat.title}</h2>
          <span className="platform-badge">
            {chat.platform}
          </span>
        </div>
        
        <div className="chat-actions">
          <Button
            variant="icon"
            onClick={() => exportChat(chatId)}
            title="Export Chat"
          >
            <ExportIcon />
          </Button>
          
          <Button
            variant="icon"
            onClick={() => shareChat(chatId)}
            title="Share Chat"
          >
            <ShareIcon />
          </Button>
          
          <Button
            variant="icon"
            onClick={onClose}
            title="Close Chat"
          >
            <CloseIcon />
          </Button>
        </div>
      </header>
      
      {/* Chat analysis */}
      {chat.summary && (
        <div className="chat-analysis">
          <div className="summary">
            <h3>Summary</h3>
            <p>{chat.summary}</p>
          </div>
          
          {chat.topics && (
            <div className="topics">
              <h3>Topics</h3>
              <div className="topic-tags">
                {chat.topics.map((topic) => (
                  <span key={topic} className="topic-tag">
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {chat.sentiment && (
            <div className="sentiment">
              <h3>Sentiment</h3>
              <div className={`sentiment-score ${chat.sentiment.overall_sentiment}`}>
                {chat.sentiment.overall_sentiment}
                <span className="confidence">
                  {(chat.sentiment.confidence_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Message list */}
      <div className="message-list" ref={messageListRef}>
        {chat.messages.map((message) => (
          <Message
            key={message.id}
            message={message}
            onMediaPlay={handleMediaPlay}
            onAction={handleMessageAction}
          />
        ))}
      </div>
    </div>
  );
};
```

## Styling

### CSS Modules
```scss
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--color-background);
  
  .chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid var(--color-border);
    background: var(--color-background-dark);
    
    .chat-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      
      h2 {
        margin: 0;
        font-size: 1.25rem;
      }
      
      .platform-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        background: var(--color-primary);
        color: white;
        font-size: 0.75rem;
        text-transform: uppercase;
      }
    }
    
    .chat-actions {
      display: flex;
      gap: 0.5rem;
    }
  }
  
  .chat-analysis {
    padding: 1rem;
    border-bottom: 1px solid var(--color-border);
    background: var(--color-background-dark);
    
    h3 {
      margin: 0 0 0.5rem;
      font-size: 1rem;
      color: var(--color-text-secondary);
    }
    
    .summary {
      margin-bottom: 1rem;
      
      p {
        margin: 0;
        font-size: 0.875rem;
        line-height: 1.5;
      }
    }
    
    .topics {
      margin-bottom: 1rem;
      
      .topic-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        
        .topic-tag {
          padding: 0.25rem 0.5rem;
          border-radius: 9999px;
          background: var(--color-primary/20);
          color: var(--color-primary);
          font-size: 0.75rem;
        }
      }
    }
    
    .sentiment {
      .sentiment-score {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        
        &.positive {
          background: var(--color-success/20);
          color: var(--color-success);
        }
        
        &.negative {
          background: var(--color-error/20);
          color: var(--color-error);
        }
        
        &.neutral {
          background: var(--color-text-secondary/20);
          color: var(--color-text-secondary);
        }
        
        .confidence {
          font-size: 0.75rem;
          opacity: 0.8;
        }
      }
    }
  }
  
  .message-list {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
}
```

## Usage Examples

### Basic Usage
```typescript
function ChatPage() {
  const { selectedChat } = useChatStore();
  
  if (!selectedChat) {
    return <div>No chat selected</div>;
  }
  
  return (
    <ChatView
      chatId={selectedChat}
      onClose={() => {
        // Handle close
      }}
    />
  );
}
```

### With Custom Message Rendering
```typescript
function CustomChatView() {
  const renderMessage = (message: ChatMessage) => {
    switch (message.type) {
      case 'code':
        return (
          <CodeBlock
            language={message.language}
            code={message.content}
          />
        );
      case 'math':
        return (
          <MathRenderer
            formula={message.content}
          />
        );
      default:
        return message.content;
    }
  };
  
  return (
    <ChatView
      chatId={selectedChat}
      messageRenderer={renderMessage}
    />
  );
}
```

### With Real-time Updates
```typescript
function LiveChatView() {
  const socket = useWebSocket();
  
  useEffect(() => {
    socket.on('message', (message) => {
      // Update chat with new message
      updateChat(chatId, {
        messages: [...chat.messages, message]
      });
    });
    
    return () => {
      socket.off('message');
    };
  }, [chatId]);
  
  return (
    <ChatView
      chatId={chatId}
      live={true}
    />
  );
}
```

## Media Handling

### Media Types
```typescript
type MediaType = 'image' | 'audio' | 'video' | 'document';

interface MediaAttachment {
  id: string;
  type: MediaType;
  url: string;
  thumbnail_url?: string;
  metadata: {
    filename: string;
    size: number;
    duration?: number;
    resolution?: string;
  };
}
```

### Media Player
```typescript
interface MediaPlayerProps {
  media: MediaAttachment;
  onClose?: () => void;
}

const MediaPlayer: React.FC<MediaPlayerProps> = ({
  media,
  onClose
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  
  const handleTimeUpdate = (e: React.SyntheticEvent<HTMLMediaElement>) => {
    setCurrentTime(e.currentTarget.currentTime);
  };
  
  const handleLoadedMetadata = (e: React.SyntheticEvent<HTMLMediaElement>) => {
    setDuration(e.currentTarget.duration);
  };
  
  return (
    <div className="media-player">
      {media.type === 'video' ? (
        <video
          src={media.url}
          controls
          autoPlay
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
        />
      ) : (
        <audio
          src={media.url}
          controls
          autoPlay
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
        />
      )}
      
      <div className="media-controls">
        <div className="time-display">
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>
        
        <Button
          variant="icon"
          onClick={() => onClose?.()}
        >
          <CloseIcon />
        </Button>
      </div>
    </div>
  );
};
```

## Message Actions

### Action Types
```typescript
type MessageAction =
  | 'copy'
  | 'bookmark'
  | 'share'
  | 'edit'
  | 'delete';

interface MessageActionHandler {
  action: MessageAction;
  handler: (message: ChatMessage) => void;
  icon: React.ComponentType;
  label: string;
}

const messageActions: MessageActionHandler[] = [
  {
    action: 'copy',
    handler: (message) => {
      copyToClipboard(message.content);
      toast.success('Message copied to clipboard');
    },
    icon: CopyIcon,
    label: 'Copy'
  },
  {
    action: 'bookmark',
    handler: (message) => {
      toggleBookmark(message.id);
      toast.success('Bookmark toggled');
    },
    icon: BookmarkIcon,
    label: 'Bookmark'
  },
  {
    action: 'share',
    handler: (message) => {
      shareMessage(message);
    },
    icon: ShareIcon,
    label: 'Share'
  }
];
```

## Error Handling

### Error Types
```typescript
type ChatViewError =
  | 'CHAT_NOT_FOUND'
  | 'MEDIA_LOAD_ERROR'
  | 'NETWORK_ERROR';

interface ChatViewErrorDetails {
  code: ChatViewError;
  message: string;
}
```

### Error Handlers
```typescript
const handleChatViewError = (error: unknown): ChatViewErrorDetails => {
  if (error instanceof NotFoundError) {
    return {
      code: 'CHAT_NOT_FOUND',
      message: 'Chat not found or has been deleted'
    };
  }
  
  if (error instanceof MediaError) {
    return {
      code: 'MEDIA_LOAD_ERROR',
      message: 'Failed to load media content'
    };
  }
  
  return {
    code: 'NETWORK_ERROR',
    message: 'Failed to load chat. Please check your connection'
  };
};
```
