# auth.ts (Store)

## Purpose
The authentication store manages the global authentication state for VoxStitch, handling user sessions, permissions, and guest mode limitations.

## Key Features

### State Structure
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  remainingImports: number; // For guest users
  remainingMessages: number; // For guest users
}
```

### Core Functionality

#### Authentication Methods
1. **Regular Login**
   ```typescript
   login: async (email: string, password: string) => {
     // Handles user authentication
     // Sets tokens and user data
     // Updates authentication state
   }
   ```

2. **Guest Login**
   ```typescript
   loginAsGuest: async () => {
     // Creates temporary guest session
     // Sets usage limits
     // Tracks remaining actions
   }
   ```

3. **Social Authentication**
   ```typescript
   socialLogin: async (provider: 'google' | 'github' | 'apple') => {
     // Handles OAuth flow
     // Processes provider response
     // Updates user session
   }
   ```

### Usage Tracking
- Monitors guest user activity limits
- Tracks remaining imports and messages
- Triggers upgrade prompts when limits are reached

### Token Management
- Handles JWT token storage
- Manages token refresh cycles
- Handles token expiration

## Integration Points

### API Integration
- Works with `api.ts` for authentication requests
- Handles API error responses
- Manages request headers

### Component Integration
- Provides auth state to protected routes
- Supplies user data to components
- Manages loading states

## Usage Example
```typescript
const { user, isAuthenticated, login, logout } = useAuthStore();

// In components
if (isAuthenticated) {
  // Show authenticated content
} else {
  // Show login options
}
```

## State Persistence
- Uses localStorage for token persistence
- Implements secure storage practices
- Handles state rehydration

## Error Handling
- Manages authentication errors
- Provides error messages to UI
- Handles network issues

## Security Features
1. **Token Security**
   - Secure token storage
   - Automatic token refresh
   - Token invalidation on logout

2. **Guest Mode Security**
   - Rate limiting
   - Usage tracking
   - Upgrade path security

3. **Session Management**
   - Session timeout handling
   - Multiple device handling
   - Secure session storage

## Related Files
- `PrivateRoute.tsx`: Uses auth state for route protection
- `Login.tsx`: Consumes login methods
- `api.ts`: Uses auth tokens for requests
- `ImportChat.tsx`: Checks guest limitations

## Recent Updates
- Added gradient-based UI feedback
- Improved error messaging
- Enhanced guest mode tracking
- Added social authentication support
- Improved token refresh logic

## Testing
```typescript
describe('auth store', () => {
  it('handles guest login correctly', async () => {
    const { loginAsGuest, user } = useAuthStore();
    await loginAsGuest();
    expect(user.role).toBe('guest');
    expect(user.remainingImports).toBe(2);
  });
});
```

## Performance Considerations
- Minimizes state updates
- Implements memoization
- Optimizes token refresh

## Security Best Practices
- No sensitive data in localStorage
- Secure token handling
- XSS prevention
- CSRF protection

## Upgrade Path
- Smooth transition from guest to registered user
- Data preservation during upgrade
- Seamless limit removal

## Error States
```typescript
type AuthError =
  | 'INVALID_CREDENTIALS'
  | 'NETWORK_ERROR'
  | 'SESSION_EXPIRED'
  | 'RATE_LIMITED'
  | 'GUEST_LIMIT_REACHED';
```

## Guest Limitations
- 2 chat imports maximum
- 5 messages per chat
- Limited export functionality
- Basic search capabilities
