// src/utils/api.ts
import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor to add the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized error (e.g., redirect to login)
      localStorage.removeItem("auth_token");
      window.location.href = "/login";
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

export interface Chat extends ChatCreate {
  id: string;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

export const chatAPI = {
  createChat: async (chat: ChatCreate) => {
    const response = await api.post<Chat>('/chats', chat);
    return response.data;
  },
  
  getChats: async () => {
    const response = await api.get<Chat[]>('/chats');
    return response.data;
  },
  
  getChat: async (id: string) => {
    const response = await api.get<Chat>(`/chats/${id}`);
    return response.data;
  },
  
  updateChat: async (id: string, chat: Partial<ChatCreate>) => {
    const response = await api.patch<Chat>(`/chats/${id}`, chat);
    return response.data;
  },
  
  deleteChat: async (id: string) => {
    await api.delete(`/chats/${id}`);
  }
};
