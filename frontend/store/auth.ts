import { create } from 'zustand';

type AuthStore = {
  token: string | null;
  setToken: (token: string) => void;
};

export const useAuthStore = create<AuthStore>((set) => ({
  token: null,
  setToken: (token) => set({ token }),
}));
