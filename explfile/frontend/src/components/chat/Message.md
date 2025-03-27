# Message Component Documentation

## Overview
The Message component renders individual chat messages with support for different content types, media attachments, and interactive features.

## Component Implementation

### Component Structure
```typescript
interface MessageProps {
  message: ChatMessage;
  onMediaPlay?: (media: MediaAttachment) => void;
  onAction?: (message: ChatMessage, action: MessageAction) => void;
  isHighlighted?: boolean;
}

const Message: React.FC<MessageProps> = ({
  message,
  onMediaPlay,
  onAction,
  isHighlighted
}) => {
  const [isActionsVisible, setIsActionsVisible] = useState(false);
  
  // Handle message hover
  const handleMouseEnter = () => {
    setIsActionsVisible(true);
  };
  
  const handleMouseLeave = () => {
    setIsActionsVisible(false);
  };
  
  // Handle media click
  const handleMediaClick = (media: MediaAttachment) => {
    onMediaPlay?.(media);
  };
  
  // Handle message action
  const handleAction = (action: MessageAction) => {
    onAction?.(message, action);
  };
  
  // Render message content based on type
  const renderContent = () => {
    if (message.type === 'code') {
      return (
        <pre className="code-block">
          <code>{message.content}</code>
        </pre>
      );
    }
    
    if (message.type === 'math') {
      return (
        <div className="math-block">
          {renderMathFormula(message.content)}
        </div>
      );
    }
    
    return (
      <div className="text-content">
        {message.content}
      </div>
    );
  };
  
  // Render media attachments
  const renderMedia = () => {
    if (!message.attachments?.length) {
      return null;
    }
    
    return (
      <div className="media-grid">
        {message.attachments.map((media) => (
          <div
            key={media.id}
            className="media-item"
            onClick={() => handleMediaClick(media)}
          >
            {media.type === 'image' ? (
              <img
                src={media.thumbnail_url || media.url}
                alt={media.metadata.filename}
                loading="lazy"
              />
            ) : (
              <div className="media-placeholder">
                <MediaTypeIcon type={media.type} />
                <span>{media.metadata.filename}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };
  
  return (
    <div
      className={clsx('message', {
        'message-highlighted': isHighlighted,
        'message-user': message.sender === 'user',
        'message-assistant': message.sender === 'assistant'
      })}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {/* Message header */}
      <div className="message-header">
        <div className="sender-info">
          <Avatar
            src={message.sender_avatar}
            name={message.sender_name || message.sender}
            size="sm"
          />
          <span className="sender-name">
            {message.sender_name || message.sender}
          </span>
        </div>
        
        <div className="message-time">
          {formatMessageTime(message.timestamp)}
        </div>
      </div>
      
      {/* Message content */}
      <div className="message-content">
        {renderContent()}
        {renderMedia()}
      </div>
      
      {/* Message actions */}
      {isActionsVisible && (
        <div className="message-actions">
          <Button
            variant="icon"
            size="sm"
            onClick={() => handleAction('copy')}
            title="Copy message"
          >
            <CopyIcon />
          </Button>
          
          <Button
            variant="icon"
            size="sm"
            onClick={() => handleAction('bookmark')}
            title="Bookmark message"
          >
            <BookmarkIcon />
          </Button>
          
          <Button
            variant="icon"
            size="sm"
            onClick={() => handleAction('share')}
            title="Share message"
          >
            <ShareIcon />
          </Button>
        </div>
      )}
    </div>
  );
};
```

## Styling

### CSS Modules
```scss
.message {
  position: relative;
  padding: 1rem;
  border-radius: 0.5rem;
  background: var(--color-background);
  transition: background-color 0.2s;
  
  &:hover {
    background: var(--color-background-dark);
  }
  
  &.message-highlighted {
    background: var(--color-primary/10);
    border: 1px solid var(--color-primary/30);
  }
  
  &.message-user {
    margin-left: auto;
    max-width: 80%;
    
    .message-content {
      color: var(--color-text);
    }
  }
  
  &.message-assistant {
    margin-right: auto;
    max-width: 80%;
    
    .message-content {
      color: var(--color-text-secondary);
    }
  }
  
  .message-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    
    .sender-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      
      .sender-name {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--color-text-secondary);
      }
    }
    
    .message-time {
      font-size: 0.75rem;
      color: var(--color-text-secondary);
    }
  }
  
  .message-content {
    font-size: 0.875rem;
    line-height: 1.5;
    
    .code-block {
      margin: 0.5rem 0;
      padding: 1rem;
      border-radius: 0.25rem;
      background: var(--color-background-dark);
      font-family: monospace;
      font-size: 0.8125rem;
      overflow-x: auto;
    }
    
    .math-block {
      margin: 0.5rem 0;
      padding: 0.5rem;
      border-radius: 0.25rem;
      background: var(--color-background-dark);
      overflow-x: auto;
    }
  }
  
  .media-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.5rem;
    margin-top: 0.5rem;
    
    .media-item {
      position: relative;
      aspect-ratio: 1;
      border-radius: 0.25rem;
      overflow: hidden;
      cursor: pointer;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      .media-placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding: 1rem;
        background: var(--color-background-dark);
        
        svg {
          width: 2rem;
          height: 2rem;
          color: var(--color-text-secondary);
          margin-bottom: 0.5rem;
        }
        
        span {
          font-size: 0.75rem;
          color: var(--color-text-secondary);
          text-align: center;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          max-width: 100%;
        }
      }
    }
  }
  
  .message-actions {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    display: flex;
    gap: 0.25rem;
    padding: 0.25rem;
    border-radius: 0.25rem;
    background: var(--color-background);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
}
```

## Usage Examples

### Basic Usage
```typescript
function ChatMessage() {
  const message: ChatMessage = {
    id: '1',
    sender: 'user',
    content: 'Hello, world!',
    timestamp: new Date().toISOString()
  };
  
  return (
    <Message
      message={message}
      onAction={(message, action) => {
        console.log(`Action ${action} on message:`, message);
      }}
    />
  );
}
```

### With Media Attachments
```typescript
function MediaMessage() {
  const message: ChatMessage = {
    id: '2',
    sender: 'assistant',
    content: 'Here are some images:',
    timestamp: new Date().toISOString(),
    attachments: [
      {
        id: '1',
        type: 'image',
        url: 'image1.jpg',
        thumbnail_url: 'thumb1.jpg',
        metadata: {
          filename: 'image1.jpg',
          size: 1024
        }
      },
      {
        id: '2',
        type: 'image',
        url: 'image2.jpg',
        thumbnail_url: 'thumb2.jpg',
        metadata: {
          filename: 'image2.jpg',
          size: 2048
        }
      }
    ]
  };
  
  return (
    <Message
      message={message}
      onMediaPlay={(media) => {
        console.log('Playing media:', media);
      }}
    />
  );
}
```

### With Code Blocks
```typescript
function CodeMessage() {
  const message: ChatMessage = {
    id: '3',
    sender: 'assistant',
    content: `
      function hello() {
        console.log('Hello, world!');
      }
    `,
    type: 'code',
    language: 'javascript',
    timestamp: new Date().toISOString()
  };
  
  return (
    <Message
      message={message}
      highlightSyntax
    />
  );
}
```

## Media Types

### Type Definitions
```typescript
interface MediaTypeConfig {
  icon: React.ComponentType;
  accept: string[];
  maxSize: number;
}

const mediaTypes: Record<MediaType, MediaTypeConfig> = {
  image: {
    icon: ImageIcon,
    accept: ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    maxSize: 5 * 1024 * 1024 // 5MB
  },
  audio: {
    icon: AudioIcon,
    accept: ['.mp3', '.wav', '.ogg', '.m4a'],
    maxSize: 10 * 1024 * 1024 // 10MB
  },
  video: {
    icon: VideoIcon,
    accept: ['.mp4', '.webm', '.mov'],
    maxSize: 50 * 1024 * 1024 // 50MB
  },
  document: {
    icon: DocumentIcon,
    accept: ['.pdf', '.doc', '.docx', '.txt', '.md'],
    maxSize: 10 * 1024 * 1024 // 10MB
  }
};
```

### Media Validation
```typescript
const validateMedia = (
  file: File,
  type: MediaType
): ValidationResult => {
  const config = mediaTypes[type];
  
  // Check file type
  const extension = `.${file.name.split('.').pop()}`;
  if (!config.accept.includes(extension.toLowerCase())) {
    return {
      valid: false,
      error: `Invalid file type. Accepted types: ${config.accept.join(', ')}`
    };
  }
  
  // Check file size
  if (file.size > config.maxSize) {
    return {
      valid: false,
      error: `File too large. Maximum size: ${formatBytes(config.maxSize)}`
    };
  }
  
  return { valid: true };
};
```

## Message Actions

### Action Handlers
```typescript
const messageActions: Record<MessageAction, ActionHandler> = {
  copy: {
    icon: CopyIcon,
    label: 'Copy',
    handler: async (message) => {
      await copyToClipboard(message.content);
      toast.success('Message copied to clipboard');
    }
  },
  bookmark: {
    icon: BookmarkIcon,
    label: 'Bookmark',
    handler: async (message) => {
      await toggleBookmark(message.id);
      toast.success('Bookmark toggled');
    }
  },
  share: {
    icon: ShareIcon,
    label: 'Share',
    handler: async (message) => {
      const url = await generateShareUrl(message.id);
      await copyToClipboard(url);
      toast.success('Share link copied to clipboard');
    }
  }
};
```

### Action Menu
```typescript
function MessageActions({ message, onAction }: MessageActionsProps) {
  return (
    <Menu>
      <MenuButton>
        <MoreIcon />
      </MenuButton>
      
      <MenuList>
        {Object.entries(messageActions).map(([key, action]) => (
          <MenuItem
            key={key}
            icon={<action.icon />}
            onClick={() => onAction(message, key as MessageAction)}
          >
            {action.label}
          </MenuItem>
        ))}
      </MenuList>
    </Menu>
  );
}
```

## Error Handling

### Error Types
```typescript
type MessageError =
  | 'MEDIA_LOAD_ERROR'
  | 'COPY_ERROR'
  | 'SHARE_ERROR'
  | 'BOOKMARK_ERROR';

interface MessageErrorDetails {
  code: MessageError;
  message: string;
}
```

### Error Handlers
```typescript
const handleMessageError = (error: unknown): MessageErrorDetails => {
  if (error instanceof MediaError) {
    return {
      code: 'MEDIA_LOAD_ERROR',
      message: 'Failed to load media content'
    };
  }
  
  if (error instanceof ClipboardError) {
    return {
      code: 'COPY_ERROR',
      message: 'Failed to copy to clipboard'
    };
  }
  
  return {
    code: 'SHARE_ERROR',
    message: 'Failed to share message'
  };
};
```
