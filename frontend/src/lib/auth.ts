import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  role: 'analyst' | 'viewer';
}

interface AuthStore {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  isAnalyst: () => boolean;
}

export const useAuthStore = create<AuthStore>((set, get) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('token'),

  setAuth: (user, token) => {
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('token', token);
    set({ user, token });
  },

  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    set({ user: null, token: null });
  },

  isAnalyst: () => get().user?.role === 'analyst',
}));
