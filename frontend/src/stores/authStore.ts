import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  isGuest: boolean;
  guestUsage: {
    chatImports: number;
    messages: number;
  };
  setToken: (token: string | null) => void;
  setIsGuest: (isGuest: boolean) => void;
  incrementChatImports: () => void;
  incrementMessages: () => void;
  logout: () => void;
  canImportChat: () => boolean;
  canSendMessage: () => boolean;
}

const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      isGuest: false,
      guestUsage: {
        chatImports: 0,
        messages: 0,
      },
      setToken: (token) => set({ token }),
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
      logout: () =>
        set({
          token: null,
          isGuest: false,
          guestUsage: {
            chatImports: 0,
            messages: 0,
          },
        }),
      canImportChat: () => {
        const { isGuest, guestUsage } = get();
        return !isGuest || guestUsage.chatImports < 2;
      },
      canSendMessage: () => {
        const { isGuest, guestUsage } = get();
        return !isGuest || guestUsage.messages < 5;
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);

export default useAuthStore;
