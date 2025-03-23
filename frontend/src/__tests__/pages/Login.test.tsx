import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, useNavigate } from 'react-router-dom';
import { Login } from '../../pages/Login';
import type { AuthState } from '../../store/auth';
import { api } from '../../utils/api';

// Mock dependencies
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn()
}));

// Mock the auth store with proper typing
const mockAuthStore = {
  setAuth: jest.fn(),
  user: null,
  token: null,
  isAuthenticated: false
} as unknown as AuthState & { setAuth: jest.Mock };

jest.mock('../../store/auth', () => ({
  useAuthStore: jest.fn(() => mockAuthStore)
}));

jest.mock('../../utils/api', () => ({
  api: {
    post: jest.fn()
  }
}));

describe('Login Component', () => {
  const mockNavigate = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useNavigate as jest.Mock).mockReturnValue(mockNavigate);
  });

  it('renders login form', () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    expect(screen.getByPlaceholderText('Email address')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /continue as guest/i })).toBeInTheDocument();
  });

  it('handles successful login', async () => {
    const mockUser = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
      role: 'user'
    };
    const mockToken = 'test-token';

    (api.post as jest.Mock).mockResolvedValueOnce({
      data: { user: mockUser, token: mockToken }
    });

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('Email address'), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/auth/login', {
        email: 'test@example.com',
        password: 'password123'
      });
      expect(mockAuthStore.setAuth).toHaveBeenCalledWith(mockUser, mockToken);
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  it('handles login error', async () => {
    (api.post as jest.Mock).mockRejectedValueOnce(new Error('Invalid credentials'));

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('Email address'), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'wrongpassword' }
    });
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText('Invalid email or password')).toBeInTheDocument();
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  });

  it('handles guest login', async () => {
    const mockGuest = {
      id: '2',
      username: 'guest',
      email: 'guest@example.com',
      role: 'guest'
    };
    const mockToken = 'guest-token';

    (api.post as jest.Mock).mockResolvedValueOnce({
      data: { user: mockGuest, token: mockToken }
    });

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole('button', { name: /continue as guest/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/auth/guest');
      expect(mockAuthStore.setAuth).toHaveBeenCalledWith(mockGuest, mockToken);
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });
});
