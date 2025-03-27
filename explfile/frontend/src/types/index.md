# Types Documentation

## Core Types

### User Types
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  is_guest: boolean;
  guest_imports_remaining?: number;
  guest_messages_remaining?: number;
  avatar_url?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}
```

### Chat Types
```typescript
interface ChatMessage {
  id: string;
  sender: string;
  content: string;
  timestamp: string;
  attachments?: MediaAttachment[];
}

interface Chat {
  id: string;
  title: string;
  platform: Platform;
  messages: ChatMessage[];
  summary?: string;
  topics?: string[];
  sentiment?: ChatSentiment;
  metadata: ChatMetadata;
  created_at: string;
  updated_at: string;
}

interface ChatMetadata {
  message_count: number;
  participants: string[];
  duration?: number;
  has_media: boolean;
  tags: string[];
}

interface ChatSentiment {
  overall_sentiment: 'positive' | 'negative' | 'neutral';
  confidence_score: number;
}
```

### Media Types
```typescript
interface MediaAttachment {
  id: string;
  type: MediaType;
  url: string;
  thumbnail_url?: string;
  content?: MediaContent;
  metadata: MediaMetadata;
}

interface MediaContent {
  transcript?: string;
  segments?: MediaSegment[];
  visual_analysis?: VisualAnalysis;
  text?: string;
}

interface MediaSegment {
  start: number;
  end: number;
  text: string;
  speaker?: string;
}

interface MediaMetadata {
  filename: string;
  size: number;
  duration?: number;
  resolution?: string;
  format: string;
  created_at: string;
}

interface VisualAnalysis {
  objects: string[];
  text: string[];
  scene_description: string;
  confidence_score: number;
}
```

### Search Types
```typescript
interface SearchFilters {
  platform?: Platform;
  startDate?: string;
  endDate?: string;
  tags?: string[];
  hasMedia?: boolean;
}

interface SearchResults {
  chats: Chat[];
  total: number;
  page: number;
  page_size: number;
}

interface SearchState {
  query: string;
  filters: SearchFilters;
  results: SearchResults | null;
  isLoading: boolean;
  error: string | null;
}
```

### UI Types
```typescript
interface Theme {
  mode: 'light' | 'dark';
  colors: {
    background: string;
    backgroundDark: string;
    text: string;
    textSecondary: string;
    primary: string;
    primaryHover: string;
    border: string;
    error: string;
    success: string;
  };
}

interface Modal {
  isOpen: boolean;
  title: string;
  content: React.ReactNode;
  onClose: () => void;
}

interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}
```

### API Types
```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

interface ApiError {
  status: number;
  message: string;
  details?: Record<string, any>;
}

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
```

### Store Types
```typescript
interface RootState {
  auth: AuthState;
  chats: ChatsState;
  search: SearchState;
  ui: UiState;
}

interface ChatsState {
  chats: Record<string, Chat>;
  selectedChat: string | null;
  isLoading: boolean;
  error: string | null;
}

interface UiState {
  theme: Theme;
  modals: Record<string, Modal>;
  toasts: Toast[];
  isSidebarOpen: boolean;
  isImportDialogOpen: boolean;
}
```

### Enum Types
```typescript
enum Platform {
  CHATGPT = 'chatgpt',
  MISTRAL = 'mistral',
  GEMINI = 'gemini',
  CUSTOM = 'custom'
}

enum MediaType {
  AUDIO = 'audio',
  VIDEO = 'video',
  IMAGE = 'image',
  DOCUMENT = 'document'
}

enum SortOrder {
  ASC = 'asc',
  DESC = 'desc'
}

enum SortField {
  CREATED_AT = 'created_at',
  UPDATED_AT = 'updated_at',
  TITLE = 'title',
  MESSAGE_COUNT = 'message_count'
}
```

## Type Guards

### User Type Guards
```typescript
function isUser(obj: any): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'string' &&
    typeof obj.email === 'string' &&
    typeof obj.name === 'string' &&
    typeof obj.is_guest === 'boolean'
  );
}

function isGuestUser(user: User): boolean {
  return user.is_guest === true;
}
```

### Chat Type Guards
```typescript
function isChat(obj: any): obj is Chat {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'string' &&
    typeof obj.title === 'string' &&
    Array.isArray(obj.messages) &&
    typeof obj.created_at === 'string'
  );
}

function hasMedia(chat: Chat): boolean {
  return chat.metadata.has_media === true;
}
```

### API Type Guards
```typescript
function isApiError(obj: any): obj is ApiError {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.status === 'number' &&
    typeof obj.message === 'string'
  );
}

function isPaginatedResponse<T>(obj: any): obj is PaginatedResponse<T> {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    Array.isArray(obj.items) &&
    typeof obj.total === 'number' &&
    typeof obj.page === 'number' &&
    typeof obj.page_size === 'number'
  );
}
```

## Type Utilities

### Generic Types
```typescript
type Nullable<T> = T | null;
type Optional<T> = T | undefined;
type LoadingState<T> = {
  data: T | null;
  isLoading: boolean;
  error: string | null;
};

type ActionMap<M extends { [index: string]: any }> = {
  [Key in keyof M]: M[Key] extends undefined
    ? {
        type: Key;
      }
    : {
        type: Key;
        payload: M[Key];
      };
};
```

### Store Action Types
```typescript
type AuthAction = ActionMap<{
  LOGIN_SUCCESS: { user: User; token: string };
  LOGIN_FAILURE: { error: string };
  LOGOUT: undefined;
  UPDATE_USER: { user: Partial<User> };
}>[keyof ActionMap<any>];

type ChatAction = ActionMap<{
  SET_CHATS: { chats: Chat[] };
  ADD_CHAT: { chat: Chat };
  UPDATE_CHAT: { chatId: string; updates: Partial<Chat> };
  DELETE_CHAT: { chatId: string };
  SELECT_CHAT: { chatId: string | null };
}>[keyof ActionMap<any>];
```

### Component Props Types
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'text';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

interface InputProps {
  type?: 'text' | 'password' | 'email' | 'number';
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  disabled?: boolean;
}
```
