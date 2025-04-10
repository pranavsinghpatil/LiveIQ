import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface GuestUsage {
  chatImports: number;
  messages: number;
}

interface AuthState {
  token: string | null;
  isGuest: boolean;
  guestUsage: GuestUsage;
  setToken: (token: string | null) => void;
  setIsGuest: (isGuest: boolean) => void;
  incrementChatImports: () => void;
  incrementMessages: () => void;
  startGuestMode: () => void;
  logout: () => void;
}

const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      isGuest: false,
      guestUsage: {
        chatImports: 0,
        messages: 0,
      },
      setToken: (token) => set({ token, isGuest: false }),
      setIsGuest: (isGuest) => set({ isGuest }),
      incrementChatImports: () =>
        set((state) => ({
          guestUsage: {
            ...state.guestUsage,
            chatImports: state.guestUsage.chatImports + 1,
          },
        })),
      incrementMessages: () =>
        set((state) => ({
          guestUsage: {
            ...state.guestUsage,
            messages: state.guestUsage.messages + 1,
          },
        })),
      startGuestMode: () =>
        set({
          token: null,
          isGuest: true,
          guestUsage: {
            chatImports: 0,
            messages: 0,
          },
        }),
      logout: () =>
        set({
          token: null,
          isGuest: false,
          guestUsage: {
            chatImports: 0,
            messages: 0,
          },
        }),
    }),
    {
      name: 'auth-storage',
    }
  )
);

export default useAuthStore;
