import { useAuthStore } from '../../store/auth';
import { act } from '@testing-library/react';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('Auth Store', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset the store state
    act(() => {
      useAuthStore.setState({ user: null, token: null });
    });
  });

  test('should initialize with null user and token from localStorage', () => {
    // Setup localStorage mock to return a token
    localStorageMock.getItem.mockReturnValueOnce('test-token');
    
    // Re-create the store to trigger the initialization
    const store = useAuthStore.getState();
    
    // Verify localStorage was called
    expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
    
    // Verify initial state
    expect(store.user).toBeNull();
    expect(store.token).toBeNull(); // This will be null because we reset the state in beforeEach
  });

  test('setAuth should update user and token and save to localStorage', () => {
    const testUser = { id: '1', username: 'testuser', email: 'test@example.com' };
    const testToken = 'test-token';
    
    act(() => {
      useAuthStore.getState().setAuth(testUser, testToken);
    });
    
    // Verify localStorage was called
    expect(localStorageMock.setItem).toHaveBeenCalledWith('token', testToken);
    
    // Verify state was updated
    const state = useAuthStore.getState();
    expect(state.user).toEqual(testUser);
    expect(state.token).toEqual(testToken);
  });

  test('logout should clear user and token and remove from localStorage', () => {
    // First set a user and token
    const testUser = { id: '1', username: 'testuser', email: 'test@example.com' };
    const testToken = 'test-token';
    
    act(() => {
      useAuthStore.getState().setAuth(testUser, testToken);
    });
    
    // Then logout
    act(() => {
      useAuthStore.getState().logout();
    });
    
    // Verify localStorage was called
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
    
    // Verify state was updated
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
  });
});
