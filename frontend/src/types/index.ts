export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export interface ChatLog {
  id: string;
  title: string;
  platform: string;
  messages: ChatMessage[];
  createdAt: string;
  updatedAt: string;
  tags: string[];
  summary?: string;
  metadata?: Record<string, any>;
}

export interface User {
  id: string;
  username: string;
  email: string;
  isGuest: boolean;
  createdAt: string;
  updatedAt: string;
  preferences?: Record<string, any>;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isGuest: boolean;
  isLoading: boolean;
  error: string | null;
  remainingImports: number;
  remainingMessages: number;
}

export interface SearchFilters {
  platform?: string;
  startDate?: string;
  endDate?: string;
  tags?: string[];
  query?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

export interface ImportChatRequest {
  platform: string;
  content: string;
  title?: string;
  tags?: string[];
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  language: string;
  notifications: boolean;
}
