# ImportChat Component

## Purpose
The ImportChat component is a critical part of VoxStitch (formerly ChatSynth) that enables users to import conversations from various AI platforms. It supports multiple import methods including URLs, file uploads, and media content (video/audio) with optional transcripts.

## Component Implementation

### Component Structure
```typescript
interface ImportChatProps {
  isOpen?: boolean;
  onClose?: () => void;
  standalone?: boolean;
  onImportSuccess?: (data: ImportResponse) => void;
}

const ImportChat: React.FC<ImportChatProps> = ({
  isOpen = false,
  onClose = () => {},
  standalone = false,
  onImportSuccess
}) => {
  // Local state for standalone mode
  const [localIsOpen, setLocalIsOpen] = useState(standalone ? true : isOpen);
  
  // Form state
  const [importType, setImportType] = useState<ImportType>('link');
  const [platform, setPlatform] = useState<Platform>('chatgpt');
  const [customPlatform, setCustomPlatform] = useState('');
  const [linkUrl, setLinkUrl] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [transcript, setTranscript] = useState<File | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Auth store for guest limits
  const { user, isGuest } = useAuthStore();
  
  // Effect to sync isOpen prop with local state
  useEffect(() => {
    if (!standalone) {
      setLocalIsOpen(isOpen);
    }
  }, [isOpen, standalone]);
  
  // Check if guest user has reached import limit
  const hasReachedImportLimit = () => {
    if (!isGuest || !user) return false;
    return user.imports >= 2; // Guest limit is 2 imports
  };
  
  // Handle dialog close
  const handleClose = () => {
    if (standalone) {
      setLocalIsOpen(false);
    }
    onClose();
  };
  
  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
    setError('');
  };
  
  // Handle transcript file selection
  const handleTranscriptChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setTranscript(selectedFile);
  };
  
  // Handle form submission
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    // Validate inputs
    if (importType === 'link' && !linkUrl) {
      setError('Please enter a valid URL');
      return;
    }
    
    if ((importType === 'file' || importType === 'video' || importType === 'audio') && !file) {
      setError('Please select a file to upload');
      return;
    }
    
    // Check guest limits
    if (hasReachedImportLimit()) {
      setError('You have reached the guest import limit. Please sign up for full access.');
      return;
    }
    
    // Prepare form data
    const formData = new FormData();
    formData.append('import_type', importType);
    formData.append('platform', platform === 'other' ? customPlatform : platform);
    
    if (importType === 'link') {
      formData.append('url', linkUrl);
    } else {
      if (file) {
        formData.append('file', file);
      }
      
      if ((importType === 'video' || importType === 'audio') && transcript) {
        formData.append('transcript', transcript);
      }
    }
    
    // Submit import request
    try {
      setIsLoading(true);
      setError('');
      
      const response = await api.post('/chats/import', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      // Handle success
      if (response.data) {
        if (onImportSuccess) {
          onImportSuccess(response.data);
        }
        handleClose();
      }
    } catch (err) {
      // Handle error
      const errorMessage = getErrorMessage(err);
      setError(errorMessage || 'Failed to import chat. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  // Render platform selection
  const renderPlatformSelection = () => (
    <div className="platform-selection">
      <label htmlFor="platform">Platform</label>
      <select
        id="platform"
        value={platform}
        onChange={(e) => setPlatform(e.target.value as Platform)}
        disabled={isLoading}
      >
        <option value="chatgpt">ChatGPT</option>
        <option value="gemini">Google Gemini</option>
        <option value="mistral">Mistral AI</option>
        <option value="claude">Anthropic Claude</option>
        <option value="other">Other</option>
      </select>
      
      {platform === 'other' && (
        <input
          type="text"
          placeholder="Enter platform name"
          value={customPlatform}
          onChange={(e) => setCustomPlatform(e.target.value)}
          disabled={isLoading}
        />
      )}
    </div>
  );
  
  // Render import type selection
  const renderImportTypeSelection = () => (
    <div className="import-type-selection">
      <div className="import-types">
        <button
          type="button"
          className={`import-type-btn ${importType === 'link' ? 'active' : ''}`}
          onClick={() => setImportType('link')}
          disabled={isLoading}
        >
          <LinkIcon />
          <span>Link</span>
        </button>
        
        <button
          type="button"
          className={`import-type-btn ${importType === 'file' ? 'active' : ''}`}
          onClick={() => setImportType('file')}
          disabled={isLoading}
        >
          <FileIcon />
          <span>File</span>
        </button>
        
        <button
          type="button"
          className={`import-type-btn ${importType === 'video' ? 'active' : ''}`}
          onClick={() => setImportType('video')}
          disabled={isLoading}
        >
          <VideoIcon />
          <span>Video</span>
        </button>
        
        <button
          type="button"
          className={`import-type-btn ${importType === 'audio' ? 'active' : ''}`}
          onClick={() => setImportType('audio')}
          disabled={isLoading}
        >
          <AudioIcon />
          <span>Audio</span>
        </button>
      </div>
    </div>
  );
  
  // Render import form based on type
  const renderImportForm = () => {
    switch (importType) {
      case 'link':
        return (
          <div className="import-form-link">
            <label htmlFor="link-url">URL</label>
            <input
              id="link-url"
              type="url"
              placeholder="Enter chat URL"
              value={linkUrl}
              onChange={(e) => setLinkUrl(e.target.value)}
              disabled={isLoading}
            />
          </div>
        );
      
      case 'file':
        return (
          <div className="import-form-file">
            <label htmlFor="file-upload">Chat File</label>
            <div className="file-upload-container">
              <input
                id="file-upload"
                type="file"
                accept=".json,.txt,.md,.html"
                onChange={handleFileChange}
                disabled={isLoading}
              />
              <div className="file-upload-label">
                {file ? file.name : 'Choose a file'}
              </div>
            </div>
          </div>
        );
      
      case 'video':
      case 'audio':
        return (
          <div className="import-form-media">
            <div className="media-upload">
              <label htmlFor="media-upload">
                {importType === 'video' ? 'Video File' : 'Audio File'}
              </label>
              <div className="file-upload-container">
                <input
                  id="media-upload"
                  type="file"
                  accept={importType === 'video' ? 'video/*' : 'audio/*'}
                  onChange={handleFileChange}
                  disabled={isLoading}
                />
                <div className="file-upload-label">
                  {file ? file.name : `Choose a ${importType} file`}
                </div>
              </div>
            </div>
            
            <div className="transcript-upload">
              <label htmlFor="transcript-upload">Transcript (Optional)</label>
              <div className="file-upload-container">
                <input
                  id="transcript-upload"
                  type="file"
                  accept=".txt,.srt,.vtt"
                  onChange={handleTranscriptChange}
                  disabled={isLoading}
                />
                <div className="file-upload-label">
                  {transcript ? transcript.name : 'Choose a transcript file'}
                </div>
              </div>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };
  
  // Main render
  if (!localIsOpen) {
    return standalone ? (
      <button
        className="import-chat-btn"
        onClick={() => setLocalIsOpen(true)}
      >
        Import Chat
      </button>
    ) : null;
  }
  
  return (
    <div className="import-chat-modal">
      <div className="modal-overlay" onClick={handleClose} />
      
      <div className="modal-content">
        <div className="modal-header">
          <h2>Import Chat</h2>
          <button
            className="close-btn"
            onClick={handleClose}
            disabled={isLoading}
          >
            <CloseIcon />
          </button>
        </div>
        
        <form onSubmit={handleSubmit}>
          {renderImportTypeSelection()}
          {renderPlatformSelection()}
          {renderImportForm()}
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          {hasReachedImportLimit() && (
            <div className="limit-warning">
              <WarningIcon />
              <p>
                Guest users are limited to 2 chat imports.
                <a href="/signup">Sign up</a> for unlimited imports.
              </p>
            </div>
          )}
          
          <div className="modal-actions">
            <button
              type="button"
              className="cancel-btn"
              onClick={handleClose}
              disabled={isLoading}
            >
              Cancel
            </button>
            
            <button
              type="submit"
              className="import-btn"
              disabled={isLoading || hasReachedImportLimit()}
            >
              {isLoading ? 'Importing...' : 'Import'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
```

## Styling

### CSS Modules
```scss
.import-chat-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
  }
  
  .modal-content {
    position: relative;
    width: 90%;
    max-width: 500px;
    background: var(--color-background);
    border-radius: 0.5rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    z-index: 1;
    
    @media (max-width: 768px) {
      width: 95%;
      padding: 1rem;
    }
  }
  
  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    
    h2 {
      margin: 0;
      font-size: 1.25rem;
      color: var(--color-text);
    }
    
    .close-btn {
      background: transparent;
      border: none;
      color: var(--color-text-secondary);
      cursor: pointer;
      padding: 0.25rem;
      
      &:hover {
        color: var(--color-text);
      }
      
      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    }
  }
  
  .import-type-selection {
    margin-bottom: 1.5rem;
    
    .import-types {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.5rem;
      
      @media (max-width: 480px) {
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem 1rem;
      }
    }
    
    .import-type-btn {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 0.75rem;
      background: var(--color-background-dark);
      border: 1px solid var(--color-border);
      border-radius: 0.25rem;
      cursor: pointer;
      transition: all 0.2s;
      
      svg {
        width: 1.5rem;
        height: 1.5rem;
        margin-bottom: 0.5rem;
        color: var(--color-text-secondary);
      }
      
      span {
        font-size: 0.75rem;
        color: var(--color-text-secondary);
      }
      
      &.active {
        background: var(--color-primary/10);
        border-color: var(--color-primary);
        
        svg, span {
          color: var(--color-primary);
        }
      }
      
      &:hover:not(:disabled) {
        background: var(--color-background-dark);
        border-color: var(--color-primary/50);
      }
      
      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    }
  }
  
  .platform-selection {
    margin-bottom: 1.5rem;
    
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-size: 0.875rem;
      color: var(--color-text-secondary);
    }
    
    select {
      width: 100%;
      padding: 0.75rem;
      background: var(--color-background-dark);
      border: 1px solid var(--color-border);
      border-radius: 0.25rem;
      color: var(--color-text);
      font-size: 0.875rem;
      
      &:focus {
        border-color: var(--color-primary);
        outline: none;
      }
      
      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    }
    
    input[type="text"] {
      width: 100%;
      padding: 0.75rem;
      margin-top: 0.5rem;
      background: var(--color-background-dark);
      border: 1px solid var(--color-border);
      border-radius: 0.25rem;
      color: var(--color-text);
      font-size: 0.875rem;
      
      &:focus {
        border-color: var(--color-primary);
        outline: none;
      }
      
      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    }
  }
  
  .import-form-link,
  .import-form-file,
  .import-form-media {
    margin-bottom: 1.5rem;
    
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-size: 0.875rem;
      color: var(--color-text-secondary);
    }
    
    input[type="url"] {
      width: 100%;
      padding: 0.75rem;
      background: var(--color-background-dark);
      border: 1px solid var(--color-border);
      border-radius: 0.25rem;
      color: var(--color-text);
      font-size: 0.875rem;
      
      &:focus {
        border-color: var(--color-primary);
        outline: none;
      }
      
      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    }
    
    .file-upload-container {
      position: relative;
      overflow: hidden;
      display: inline-block;
      width: 100%;
      
      input[type="file"] {
        position: absolute;
        left: 0;
        top: 0;
        opacity: 0;
        width: 100%;
        height: 100%;
        cursor: pointer;
        
        &:disabled {
          cursor: not-allowed;
        }
      }
      
      .file-upload-label {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        background: var(--color-background-dark);
        border: 1px solid var(--color-border);
        border-radius: 0.25rem;
        color: var(--color-text);
        font-size: 0.875rem;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        
        &:hover {
          border-color: var(--color-primary/50);
        }
      }
    }
  }
  
  .import-form-media {
    .media-upload,
    .transcript-upload {
      margin-bottom: 1rem;
    }
  }
  
  .error-message {
    padding: 0.75rem;
    margin-bottom: 1.5rem;
    background: var(--color-error/10);
    border: 1px solid var(--color-error);
    border-radius: 0.25rem;
    color: var(--color-error);
    font-size: 0.875rem;
  }
  
  .limit-warning {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.75rem;
    margin-bottom: 1.5rem;
    background: var(--color-warning/10);
    border: 1px solid var(--color-warning);
    border-radius: 0.25rem;
    
    svg {
      width: 1.25rem;
      height: 1.25rem;
      color: var(--color-warning);
      flex-shrink: 0;
    }
    
    p {
      margin: 0;
      font-size: 0.875rem;
      color: var(--color-text);
      
      a {
        color: var(--color-primary);
        text-decoration: none;
        font-weight: 500;
        margin-left: 0.25rem;
        
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    
    button {
      padding: 0.75rem 1.5rem;
      border-radius: 0.25rem;
      font-size: 0.875rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      
      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    }
    
    .cancel-btn {
      background: transparent;
      border: 1px solid var(--color-border);
      color: var(--color-text-secondary);
      
      &:hover:not(:disabled) {
        background: var(--color-background-dark);
        color: var(--color-text);
      }
    }
    
    .import-btn {
      background: var(--color-primary);
      border: 1px solid var(--color-primary);
      color: white;
      
      &:hover:not(:disabled) {
        background: var(--color-primary-dark);
      }
    }
  }
}

.import-chat-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  border: none;
  border-radius: 0.25rem;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  
  svg {
    width: 1rem;
    height: 1rem;
  }
  
  &:hover {
    background: var(--color-primary-dark);
  }
}
```

## Usage Examples

### Basic Usage
```typescript
function ChatPage() {
  const [isImportOpen, setIsImportOpen] = useState(false);
  
  const handleImportSuccess = (data) => {
    console.log('Import successful:', data);
    // Update chat list or navigate to the new chat
  };
  
  return (
    <div>
      <button onClick={() => setIsImportOpen(true)}>
        Import Chat
      </button>
      
      <ImportChat
        isOpen={isImportOpen}
        onClose={() => setIsImportOpen(false)}
        onImportSuccess={handleImportSuccess}
      />
    </div>
  );
}
```

### Standalone Mode
```typescript
function ImportPage() {
  const navigate = useNavigate();
  
  const handleImportSuccess = (data) => {
    toast.success('Chat imported successfully!');
    navigate(`/chats/${data.chat_id}`);
  };
  
  return (
    <div className="import-page">
      <h1>Import Your Chats</h1>
      <p>Import your conversations from various AI platforms.</p>
      
      <ImportChat
        standalone
        onImportSuccess={handleImportSuccess}
      />
    </div>
  );
}
```

### With Custom Styling
```typescript
function CustomImportButton() {
  const [isImportOpen, setIsImportOpen] = useState(false);
  
  return (
    <>
      <button
        className="custom-import-button"
        onClick={() => setIsImportOpen(true)}
      >
        <ImportIcon />
        Import New Chat
      </button>
      
      <ImportChat
        isOpen={isImportOpen}
        onClose={() => setIsImportOpen(false)}
      />
    </>
  );
}
```

## Type Definitions

```typescript
type ImportType = 'link' | 'file' | 'video' | 'audio';

type Platform = 'chatgpt' | 'gemini' | 'mistral' | 'claude' | 'other';

interface ImportResponse {
  chat_id: string;
  title: string;
  platform: string;
  message_count: number;
  success: boolean;
}
```

## Error Handling

```typescript
const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    // API error response
    const response = error.response;
    if (response?.data?.message) {
      return response.data.message;
    }
    
    if (response?.status === 413) {
      return 'File too large. Maximum size is 10MB.';
    }
    
    if (response?.status === 415) {
      return 'Unsupported file format.';
    }
    
    if (response?.status === 401) {
      return 'Authentication required. Please log in.';
    }
    
    if (response?.status === 403) {
      return 'You have reached your import limit. Please upgrade your account.';
    }
    
    return 'Server error. Please try again later.';
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'An unknown error occurred.';
}
