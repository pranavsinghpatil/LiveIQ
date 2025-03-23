import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type UserRole = 'admin' | 'user' | 'guest';

export interface User {
  id: string;
  username: string;
  email: string;
  role: UserRole;
  remainingImports?: number;
  remainingMessages?: number;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  decrementRemainingImports: () => void;
  decrementRemainingMessages: () => void;
  getRemainingImports: () => number;
  getRemainingMessages: () => number;
  hasReachedImportLimit: () => boolean;
  hasReachedMessageLimit: () => boolean;
  isGuest: () => boolean;
  needsLogin: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      setAuth: (user, token) => {
        // Initialize limits for guest users if not already set
        if (user.role === 'guest') {
          user.remainingImports = user.remainingImports ?? 2;
          user.remainingMessages = user.remainingMessages ?? 5;
        }
        
        set({
          user,
          token,
          isAuthenticated: true,
        });
        
        // Store token in localStorage for API requests
        localStorage.setItem('token', token);
      },
      
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
        
        // Remove token from localStorage
        localStorage.removeItem('token');
      },
      
      decrementRemainingImports: () => {
        const { user } = get();
        
        if (user && user.role === 'guest' && user.remainingImports !== undefined) {
          set({
            user: {
              ...user,
              remainingImports: Math.max(0, user.remainingImports - 1),
            },
          });
        }
      },
      
      decrementRemainingMessages: () => {
        const { user } = get();
        
        if (user && user.role === 'guest' && user.remainingMessages !== undefined) {
          set({
            user: {
              ...user,
              remainingMessages: Math.max(0, user.remainingMessages - 1),
            },
          });
        }
      },
      
      getRemainingImports: () => {
        const { user } = get();
        
        if (user && user.role === 'guest' && user.remainingImports !== undefined) {
          return user.remainingImports;
        }
        
        return Infinity;
      },
      
      getRemainingMessages: () => {
        const { user } = get();
        
        if (user && user.role === 'guest' && user.remainingMessages !== undefined) {
          return user.remainingMessages;
        }
        
        return Infinity;
      },
      
      hasReachedImportLimit: () => {
        return get().getRemainingImports() <= 0;
      },
      
      hasReachedMessageLimit: () => {
        return get().getRemainingMessages() <= 0;
      },

      isGuest: () => {
        const { user } = get();
        return user?.role === 'guest';
      },

      needsLogin: () => {
        const { hasReachedImportLimit, hasReachedMessageLimit, isGuest } = get();
        return isGuest() && (hasReachedImportLimit() || hasReachedMessageLimit());
      }
    }),
    {
      name: 'auth-storage',
      // Only persist specific fields
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
