// User types
export interface User {
  id: string;
  username: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  created_at: string;
}

// Authentication types
export interface AuthResponse {
  token: string;
  user: User;
}

// Message types
export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

// Chat types
export interface ChatBase {
  platform: string;
  title: string;
  content: Message[];
  metadata?: Record<string, any>;
}

export interface ChatCreate extends ChatBase {}

export interface Chat extends ChatBase {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface ChatLog {
  id: string;
  user_id: string;
  platform: 'chatgpt' | 'mistral' | 'gemini' | string;
  imported_at: string;
  messages: Message[];
}

// Import types
export interface ImportChatRequest {
  platform: string;
  content: string;
}

export interface ImportChatProps {
  onImport: (chat: ChatCreate) => Promise<void>;
  onClose: () => void;
}

// API Error types
export interface ApiError {
  status: number;
  message: string;
  details?: any;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: null | {
    id: string;
    email: string;
    name?: string;
  };
  loading: boolean;
  error: string | null;
}
