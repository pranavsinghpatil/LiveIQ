import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import App from '../../App';
import { useAuthStore } from '../../store/auth';

// Mock auth store
jest.mock('../../store/auth', () => ({
  useAuthStore: jest.fn()
}));

// Mock react-query hooks
jest.mock('react-query', () => ({
  ...jest.requireActual('react-query'),
  useQuery: jest.fn().mockReturnValue({
    data: [],
    isLoading: false,
    error: null
  })
}));

describe('User Journey', () => {
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
    mockUseAuthStore.mockImplementation(() => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isGuest: () => false,
      getRemainingImports: () => Infinity,
      decrementRemainingImports: jest.fn(),
      hasReachedImportLimit: () => false,
      setAuth: jest.fn(),
      logout: jest.fn(),
      needsLogin: () => true,
      decrementRemainingMessages: jest.fn(),
      getRemainingMessages: () => Infinity,
      hasReachedMessageLimit: () => false
    }));
  });

  test('guest user journey', async () => {
    const user = userEvent.setup();
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </QueryClientProvider>
    );

    // Verify we're on the login page
    expect(screen.getByText(/Sign in to your account/i)).toBeInTheDocument();

    // Continue as guest
    const guestButton = screen.getByText(/Continue as Guest/i);
    await user.click(guestButton);

    // Verify we're on the dashboard with guest limits
    await waitFor(() => {
      expect(screen.getByText(/Recent Chats/i)).toBeInTheDocument();
      expect(screen.getByText(/2 imports remaining/i)).toBeInTheDocument();
    });

    // Try to import a chat
    const importButton = screen.getByText(/Import Chat/i);
    await user.click(importButton);

    // Verify import modal appears
    await waitFor(() => {
      expect(screen.getByText(/Import from URL or File/i)).toBeInTheDocument();
    });
  });

  test('registered user journey', async () => {
    const user = userEvent.setup();
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </QueryClientProvider>
    );

    // Fill in login form
    const emailInput = screen.getByLabelText(/Email/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInput, 'password123');

    // Submit login form
    const signInButton = screen.getByRole('button', { name: /Sign in/i });
    await user.click(signInButton);

    // Mock successful login
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

    // Verify we're on the dashboard
    await waitFor(() => {
      expect(screen.getByText(/Recent Chats/i)).toBeInTheDocument();
    });

    // Try to import a chat
    const importButton = screen.getByText(/Import Chat/i);
    await user.click(importButton);

    // Verify import modal appears
    await waitFor(() => {
      expect(screen.getByText(/Import from URL or File/i)).toBeInTheDocument();
    });
  });
});
