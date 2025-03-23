import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ImportChat } from '../../../components/chat/ImportChat';
import type { AuthState, User } from '../../../store/auth';

// Mock useAuthStore to return a mock store
const mockUseStore = jest.fn();
jest.mock('../../../store/auth', () => ({
  useAuthStore: () => mockUseStore()
}));

describe('ImportChat', () => {
  const mockOnImportComplete = jest.fn();
  const mockUser: User = {
    id: 'test-id',
    username: 'test-user',
    email: 'test@example.com',
    role: 'guest',
    remainingImports: 2
  };

  const createMockStore = (overrides: Partial<AuthState>): AuthState => ({
    user: mockUser,
    token: 'test-token',
    isAuthenticated: true,
    setAuth: jest.fn(),
    logout: jest.fn(),
    decrementRemainingImports: jest.fn(),
    decrementRemainingMessages: jest.fn(),
    getRemainingImports: () => 2,
    getRemainingMessages: () => 5,
    hasReachedImportLimit: () => false,
    hasReachedMessageLimit: () => false,
    isGuest: () => true,
    needsLogin: () => false,
    ...overrides
  });

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders import button and handles guest user limits', () => {
    // Mock guest user with remaining imports
    const mockStore = createMockStore({
      getRemainingImports: () => 2,
      hasReachedImportLimit: () => false
    });
    mockUseStore.mockReturnValue(mockStore);

    render(<ImportChat onImportComplete={mockOnImportComplete} />);

    // Check if import button is rendered
    const importButton = screen.getByText('Import Chat');
    expect(importButton).toBeInTheDocument();
    expect(importButton).not.toBeDisabled();

    // Check if remaining imports message is shown
    expect(screen.getByText('2 imports remaining')).toBeInTheDocument();
  });

  it('disables import when limit is reached', () => {
    // Mock guest user with no remaining imports
    const mockStore = createMockStore({
      getRemainingImports: () => 0,
      hasReachedImportLimit: () => true
    });
    mockUseStore.mockReturnValue(mockStore);

    render(<ImportChat onImportComplete={mockOnImportComplete} />);

    // Check if import button is disabled
    const importButton = screen.getByText('Import Chat');
    expect(importButton).toBeDisabled();

    // Check if limit reached message is shown
    expect(screen.getByText('No imports remaining')).toBeInTheDocument();
  });

  it('opens modal on button click', async () => {
    // Mock non-guest user
    const mockStore = createMockStore({
      isGuest: () => false,
      getRemainingImports: () => Infinity,
      hasReachedImportLimit: () => false
    });
    mockUseStore.mockReturnValue(mockStore);

    render(<ImportChat onImportComplete={mockOnImportComplete} />);

    // Click import button
    fireEvent.click(screen.getByText('Import Chat'));

    // Check if modal is opened
    await waitFor(() => {
      expect(screen.getByText('Import from URL or File')).toBeInTheDocument();
    });
  });

  it('calls onImportComplete when import is successful', async () => {
    // Mock non-guest user
    const mockStore = createMockStore({
      isGuest: () => false,
      getRemainingImports: () => Infinity,
      hasReachedImportLimit: () => false
    });
    mockUseStore.mockReturnValue(mockStore);

    render(<ImportChat onImportComplete={mockOnImportComplete} />);

    // Open modal
    fireEvent.click(screen.getByText('Import Chat'));

    // Click import button in modal
    const importButton = screen.getByRole('button', { name: 'Import' });
    fireEvent.click(importButton);

    // Verify onImportComplete was called
    await waitFor(() => {
      expect(mockOnImportComplete).toHaveBeenCalled();
    });
  });
});
