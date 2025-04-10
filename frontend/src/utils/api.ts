// src/utils/api.ts
import axios, { AxiosError } from 'axios';
import useAuthStore from '../stores/authStore';

export const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

// Add a request interceptor to add the auth token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // If unauthorized and not in guest mode, clear token
      if (!useAuthStore.getState().isGuest) {
        useAuthStore.getState().logout();
      }
    }
    return Promise.reject(error);
  }
);

export interface ChatCreate {
  platform: string;
  title: string;
  content: Array<{ role: string; content: string }>;
  metadata?: Record<string, any>;
}

export interface Chat {
  id: number;
  title: string;
  description: string;
  platform: string;
  created_at: string;
  userId: string;
  updatedAt: string;
}

export const chatAPI = {
  createChat: async (chat: ChatCreate) => {
    const response = await api.post<Chat>('/api/chats', chat);
    return response.data;
  },
  
  getChats: async (): Promise<Chat[]> => {
    try {
      const response = await api.get<Chat[]>('/api/chats');
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError && error.response?.status === 401 && useAuthStore.getState().isGuest) {
        return []; // Return empty array for guest users
      }
      throw error;
    }
  },
  
  getChat: async (id: string) => {
    const response = await api.get<Chat>(`/api/chats/${id}`);
    return response.data;
  },
  
  updateChat: async (id: string, chat: Partial<ChatCreate>) => {
    const response = await api.patch<Chat>(`/api/chats/${id}`, chat);
    return response.data;
  },
  
  deleteChat: async (id: string) => {
    await api.delete(`/api/chats/${id}`);
  }
};

export const authAPI = {
  register: async (userData: { username: string; password: string }) => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },
  login: async (userData: { username: string; password: string }) => {
    const response = await api.post('/api/auth/login', new URLSearchParams({
      username: userData.username,
      password: userData.password,
    }));
    return response.data;
  },
};

export default api;
