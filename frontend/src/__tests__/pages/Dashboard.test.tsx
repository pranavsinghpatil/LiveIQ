import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Dashboard } from '../../pages/Dashboard';
import { useAuthStore } from '../../store/auth';

// Mock auth store
jest.mock('../../store/auth', () => ({
  useAuthStore: jest.fn()
}));

// Mock react-query hooks
jest.mock('react-query', () => ({
  ...jest.requireActual('react-query'),
  useQuery: jest.fn().mockReturnValue({
    data: [
      { id: '1', title: 'Test Chat', source: 'chatgpt', created_at: '2024-03-23T00:00:00Z' }
    ],
    isLoading: false,
    error: null
  })
}));

describe('Dashboard Page', () => {
  const mockUseAuthStore = useAuthStore as jest.MockedFunction<typeof useAuthStore>;
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock auth store with default values
    mockUseAuthStore.mockImplementation(() => ({
      user: {
        id: 'test-user',
        username: 'testuser',
        email: 'test@example.com',
        role: 'user' as const
      },
      token: 'test-token',
      isAuthenticated: true,
      isGuest: () => false,
      getRemainingImports: () => Infinity,
      decrementRemainingImports: jest.fn(),
      hasReachedImportLimit: () => false,
      setAuth: jest.fn(),
      logout: jest.fn(),
      needsLogin: () => false,
      decrementRemainingMessages: jest.fn(),
      getRemainingMessages: () => Infinity,
      hasReachedMessageLimit: () => false
    }));
  });

  test('renders dashboard for logged in user', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Dashboard />
        </BrowserRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText(/Recent Chats/i)).toBeInTheDocument();
    expect(screen.getByText(/Test Chat/i)).toBeInTheDocument();
  });

  test('shows guest user limits', () => {
    mockUseAuthStore.mockImplementation(() => ({
      user: {
        id: 'guest-user',
        username: 'guest',
        email: 'guest@example.com',
        role: 'guest' as const,
        remainingImports: 1
      },
      token: 'guest-token',
      isAuthenticated: true,
      isGuest: () => true,
      getRemainingImports: () => 1,
      decrementRemainingImports: jest.fn(),
      hasReachedImportLimit: () => false,
      setAuth: jest.fn(),
      logout: jest.fn(),
      needsLogin: () => false,
      decrementRemainingMessages: jest.fn(),
      getRemainingMessages: () => 5,
      hasReachedMessageLimit: () => false
    }));

    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Dashboard />
        </BrowserRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText(/1 import remaining/i)).toBeInTheDocument();
  });
});
