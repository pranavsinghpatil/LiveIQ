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
  id: string;
  chat_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

// Chat types
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

// API Error types
export interface ApiError {
  status: number;
  message: string;
  details?: any;
}
