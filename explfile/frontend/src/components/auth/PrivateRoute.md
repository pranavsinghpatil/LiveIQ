# PrivateRoute Component

## Purpose
The PrivateRoute component serves as an authentication guard for protected routes in VoxStitch, ensuring that only authenticated users can access certain parts of the application.

## Component Structure

### Main Component
```typescript
interface PrivateRouteProps {
  children: React.ReactNode;
  allowGuest?: boolean;
  requiredPermissions?: string[];
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({
  children,
  allowGuest = false,
  requiredPermissions = []
}) => {
  // Component implementation
};
```

## Core Features

### Authentication Check
```typescript
const AuthCheck: React.FC = () => {
  const { isAuthenticated, isLoading, user } = useAuthStore();
  const location = useLocation();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        state={{ from: location }}
        replace
      />
    );
  }

  return null;
};
```

### Guest Mode Handling
```typescript
const GuestCheck: React.FC<{ allowGuest: boolean }> = ({ allowGuest }) => {
  const { user } = useAuthStore();

  if (user?.isGuest && !allowGuest) {
    return (
      <div className="p-4 bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-lg">
        <h2 className="text-lg font-semibold text-yellow-800">
          Guest Access Limited
        </h2>
        <p className="text-yellow-700">
          Please sign up for full access to this feature.
        </p>
        <Button
          variant="primary"
          className="mt-4"
          onClick={() => navigate('/register')}
        >
          Sign Up Now
        </Button>
      </div>
    );
  }

  return null;
};
```

### Permission Validation
```typescript
const PermissionCheck: React.FC<{
  requiredPermissions: string[]
}> = ({ requiredPermissions }) => {
  const { user } = useAuthStore();

  const hasRequiredPermissions = useMemo(() => {
    return requiredPermissions.every(
      permission => user?.permissions?.includes(permission)
    );
  }, [user?.permissions, requiredPermissions]);

  if (!hasRequiredPermissions) {
    return (
      <div className="p-4 bg-gradient-to-r from-red-50 to-red-100 rounded-lg">
        <h2 className="text-lg font-semibold text-red-800">
          Access Denied
        </h2>
        <p className="text-red-700">
          You don't have permission to access this page.
        </p>
      </div>
    );
  }

  return null;
};
```

## State Management

### Authentication State
```typescript
const useAuthGuard = () => {
  const { isAuthenticated, isLoading, user } = useAuthStore();
  const location = useLocation();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate('/login', { state: { from: location } });
    }
  }, [isAuthenticated, isLoading, location]);

  return { isAuthenticated, isLoading, user };
};
```

### Route State
```typescript
const useRouteState = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const returnToPath = useMemo(() => {
    return location.state?.from?.pathname || '/dashboard';
  }, [location.state]);

  return { returnToPath, navigate };
};
```

## UI Components

### Loading Screen
```typescript
const LoadingScreen: React.FC = () => (
  <div className="fixed inset-0 bg-surface-900/50 backdrop-blur-sm flex items-center justify-center">
    <div className="bg-gradient-to-b from-surface-50 to-surface-100 p-8 rounded-lg shadow-xl">
      <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin mx-auto" />
      <p className="mt-4 text-center text-text/60">
        Verifying access...
      </p>
    </div>
  </div>
);
```

### Error Messages
```typescript
const AccessDeniedMessage: React.FC<{
  message: string;
  actionText?: string;
  onAction?: () => void;
}> = ({ message, actionText, onAction }) => (
  <div className="p-6 bg-gradient-to-r from-red-50 to-red-100 rounded-lg">
    <AlertIcon className="w-12 h-12 text-red-500 mx-auto mb-4" />
    <h2 className="text-xl font-semibold text-red-800 text-center mb-2">
      Access Denied
    </h2>
    <p className="text-red-700 text-center mb-4">
      {message}
    </p>
    {actionText && onAction && (
      <Button
        variant="primary"
        className="w-full"
        onClick={onAction}
      >
        {actionText}
      </Button>
    )}
  </div>
);
```

## Integration Points

### Route Integration
```typescript
// In App.tsx
<Routes>
  <Route path="/login" element={<Login />} />
  <Route path="/register" element={<Register />} />
  <Route
    element={
      <PrivateRoute
        allowGuest={false}
        requiredPermissions={['read:chats']}
      >
        <DashboardLayout />
      </PrivateRoute>
    }
  >
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/chats/:id" element={<ChatView />} />
  </Route>
</Routes>
```

### Auth Store Integration
```typescript
const useAuthRedirect = () => {
  const { isAuthenticated } = useAuthStore();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      const returnPath = location.state?.from?.pathname || '/dashboard';
      navigate(returnPath, { replace: true });
    }
  }, [isAuthenticated, location.state, navigate]);
};
```

## Error Handling

### Authentication Errors
```typescript
const handleAuthError = (error: AuthError) => {
  switch (error.code) {
    case 'TOKEN_EXPIRED':
      return <SessionExpiredMessage />;
    case 'INVALID_PERMISSIONS':
      return <AccessDeniedMessage />;
    default:
      return <GeneralErrorMessage />;
  }
};
```

## Related Components
- `Login`: User login form
- `Register`: User registration form
- `AuthProvider`: Authentication context provider
- `GuestBanner`: Guest mode notification

## Testing
```typescript
describe('PrivateRoute', () => {
  it('redirects to login when not authenticated', () => {
    const { getByText } = render(
      <PrivateRoute>
        <div>Protected Content</div>
      </PrivateRoute>
    );
    
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });

  it('allows guest access when specified', () => {
    const { getByText } = render(
      <PrivateRoute allowGuest>
        <div>Guest Content</div>
      </PrivateRoute>
    );
    
    expect(getByText('Guest Content')).toBeInTheDocument();
  });
});
```

## Recent Updates
- Added gradient styling to messages
- Improved loading states
- Enhanced error messages
- Added permission checking
- Improved guest mode handling

## Security Considerations
- Token validation
- Permission checks
- Route protection
- Session management
- XSS prevention

## Accessibility Features
- Focus management
- Screen reader support
- Keyboard navigation
- ARIA attributes
- Loading state announcements
