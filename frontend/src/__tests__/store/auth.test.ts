import { act } from '@testing-library/react';
import { useAuthStore } from '../../store/auth';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
  length: 0,
  key: jest.fn()
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('Auth Store', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    useAuthStore.setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isGuest: () => false,
      getRemainingImports: () => Infinity,
      decrementRemainingImports: () => {},
      hasReachedImportLimit: () => false,
      setAuth: () => {},
      logout: () => {},
      needsLogin: () => true,
      decrementRemainingMessages: () => {},
      getRemainingMessages: () => Infinity,
      hasReachedMessageLimit: () => false
    });
  });

  test('should initialize with default state', () => {
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(state.isGuest()).toBe(false);
    expect(state.needsLogin()).toBe(true);
  });

  test('should set auth state correctly', () => {
    const mockUser = {
      id: 'test-123',
      username: 'testuser',
      email: 'test@example.com',
      role: 'user' as const
    };
    const mockToken = 'test-token';

    act(() => {
      useAuthStore.getState().setAuth(mockUser, mockToken);
    });

    const state = useAuthStore.getState();
    expect(state.user).toEqual(mockUser);
    expect(state.token).toBe(mockToken);
    expect(state.isAuthenticated).toBe(true);
    expect(state.needsLogin()).toBe(false);
    expect(localStorageMock.setItem).toHaveBeenCalledWith('token', mockToken);
  });

  test('should handle guest user correctly', () => {
    const mockGuestUser = {
      id: 'guest-123',
      username: 'guest',
      email: 'guest@example.com',
      role: 'guest' as const
    };
    const mockToken = 'guest-token';

    act(() => {
      useAuthStore.getState().setAuth(mockGuestUser, mockToken);
    });

    const state = useAuthStore.getState();
    expect(state.user).toEqual(mockGuestUser);
    expect(state.token).toBe(mockToken);
    expect(state.isAuthenticated).toBe(true);
    expect(state.isGuest()).toBe(true);
    expect(state.getRemainingImports()).toBe(2);
    expect(state.getRemainingMessages()).toBe(5);
  });

  test('should handle logout correctly', () => {
    const mockUser = {
      id: 'test-123',
      username: 'testuser',
      email: 'test@example.com',
      role: 'user' as const
    };
    const mockToken = 'test-token';

    // First set the auth state
    act(() => {
      useAuthStore.getState().setAuth(mockUser, mockToken);
    });

    // Then logout
    act(() => {
      useAuthStore.getState().logout();
    });

    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
  });

  test('should handle import limits correctly', () => {
    const mockGuestUser = {
      id: 'guest-123',
      username: 'guest',
      email: 'guest@example.com',
      role: 'guest' as const
    };
    const mockToken = 'guest-token';

    act(() => {
      useAuthStore.getState().setAuth(mockGuestUser, mockToken);
    });

    const state = useAuthStore.getState();
    expect(state.getRemainingImports()).toBe(2);
    
    act(() => {
      state.decrementRemainingImports();
    });

    expect(state.getRemainingImports()).toBe(1);
    expect(state.hasReachedImportLimit()).toBe(false);

    act(() => {
      state.decrementRemainingImports();
    });

    expect(state.getRemainingImports()).toBe(0);
    expect(state.hasReachedImportLimit()).toBe(true);
  });

  test('should handle message limits correctly', () => {
    const mockGuestUser = {
      id: 'guest-123',
      username: 'guest',
      email: 'guest@example.com',
      role: 'guest' as const
    };
    const mockToken = 'guest-token';

    act(() => {
      useAuthStore.getState().setAuth(mockGuestUser, mockToken);
    });

    const state = useAuthStore.getState();
    expect(state.getRemainingMessages()).toBe(5);
    
    act(() => {
      state.decrementRemainingMessages();
    });

    expect(state.getRemainingMessages()).toBe(4);
    expect(state.hasReachedMessageLimit()).toBe(false);

    // Decrement to zero
    for (let i = 0; i < 4; i++) {
      act(() => {
        state.decrementRemainingMessages();
      });
    }

    expect(state.getRemainingMessages()).toBe(0);
    expect(state.hasReachedMessageLimit()).toBe(true);
  });
});
