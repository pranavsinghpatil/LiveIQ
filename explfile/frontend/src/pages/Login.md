# Login Page

## Purpose
The Login page provides secure authentication for VoxStitch users, offering multiple login options including social authentication and guest access with usage limits.

## Component Structure

### Main Component
```typescript
interface LoginProps {
  className?: string;
}

const Login: React.FC<LoginProps> = ({
  className
}) => {
  // Component implementation
};
```

## Features

### 1. Login Form
```typescript
const LoginForm: React.FC = () => {
  const { login } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (values: LoginFormValues) => {
    setIsLoading(true);
    setError(null);

    try {
      await login(values);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <div className="space-y-4">
        <FormField
          label="Email"
          name="email"
          type="email"
          required
          autoFocus
        />
        <FormField
          label="Password"
          name="password"
          type="password"
          required
        />
        <div className="flex items-center justify-between">
          <Checkbox
            label="Remember me"
            name="remember"
          />
          <Link
            to="/forgot-password"
            className="text-sm text-primary-600 hover:text-primary-700"
          >
            Forgot password?
          </Link>
        </div>
        {error && (
          <Alert variant="error">
            {error}
          </Alert>
        )}
        <Button
          type="submit"
          variant="primary"
          isLoading={isLoading}
          fullWidth
        >
          Sign In
        </Button>
      </div>
    </Form>
  );
};
```

### 2. Social Authentication
```typescript
const SocialAuth: React.FC = () => (
  <div className="space-y-3">
    <Button
      variant="outline"
      fullWidth
      leftIcon={<GoogleIcon />}
      onClick={() => signInWithGoogle()}
    >
      Continue with Google
    </Button>
    <Button
      variant="outline"
      fullWidth
      leftIcon={<GithubIcon />}
      onClick={() => signInWithGithub()}
    >
      Continue with GitHub
    </Button>
    <Button
      variant="outline"
      fullWidth
      leftIcon={<AppleIcon />}
      onClick={() => signInWithApple()}
    >
      Continue with Apple
    </Button>
  </div>
);
```

### 3. Guest Access
```typescript
const GuestAccess: React.FC = () => {
  const { loginAsGuest } = useAuthStore();

  return (
    <div className="text-center">
      <Button
        variant="ghost"
        onClick={loginAsGuest}
      >
        Continue as Guest
      </Button>
      <p className="mt-2 text-sm text-text/60">
        Limited to 2 chat imports and 5 messages
      </p>
    </div>
  );
};
```

## State Management

### Authentication State
```typescript
const useAuth = () => {
  const { login, loginAsGuest } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (values: LoginFormValues) => {
    setIsLoading(true);
    setError(null);

    try {
      await login(values);
      navigate('/dashboard');
    } catch (err) {
      setError('Authentication failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGuestLogin = async () => {
    setIsLoading(true);
    setError(null);

    try {
      await loginAsGuest();
      navigate('/dashboard');
    } catch (err) {
      setError('Guest access is currently unavailable.');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    error,
    handleLogin,
    handleGuestLogin
  };
};
```

## UI Components

### 1. Form Field
```typescript
interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

const FormField: React.FC<FormFieldProps> = ({
  label,
  error,
  ...props
}) => (
  <div>
    <label className="block text-sm font-medium text-text/80 mb-1">
      {label}
    </label>
    <input
      className={clsx(
        'w-full px-4 py-2 rounded-lg',
        'bg-gradient-to-r from-surface-100 to-surface-200',
        'border border-primary/20',
        'focus:outline-none focus:ring-2 focus:ring-primary/20',
        error && 'border-red-500 focus:ring-red-500/20'
      )}
      {...props}
    />
    {error && (
      <p className="mt-1 text-sm text-red-600">
        {error}
      </p>
    )}
  </div>
);
```

### 2. Alert Component
```typescript
interface AlertProps {
  variant: 'error' | 'warning' | 'success' | 'info';
  children: React.ReactNode;
}

const Alert: React.FC<AlertProps> = ({
  variant,
  children
}) => {
  const styles = {
    error: 'bg-gradient-to-r from-red-50 to-red-100 text-red-800',
    warning: 'bg-gradient-to-r from-yellow-50 to-yellow-100 text-yellow-800',
    success: 'bg-gradient-to-r from-green-50 to-green-100 text-green-800',
    info: 'bg-gradient-to-r from-blue-50 to-blue-100 text-blue-800'
  };

  return (
    <div className={clsx(
      'p-4 rounded-lg',
      styles[variant]
    )}>
      {children}
    </div>
  );
};
```

## Integration Points

### OAuth Integration
```typescript
const useOAuth = () => {
  const signInWithGoogle = async () => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      const credential = GoogleAuthProvider.credentialFromResult(result);
      await handleOAuthLogin(credential);
    } catch (error) {
      console.error('Google sign-in failed:', error);
    }
  };

  const signInWithGithub = async () => {
    const provider = new GithubAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      const credential = GithubAuthProvider.credentialFromResult(result);
      await handleOAuthLogin(credential);
    } catch (error) {
      console.error('GitHub sign-in failed:', error);
    }
  };

  return { signInWithGoogle, signInWithGithub };
};
```

## Testing
```typescript
describe('Login', () => {
  it('handles form submission correctly', async () => {
    const { getByLabelText, getByRole } = render(<Login />);
    
    fireEvent.change(getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(getByLabelText('Password'), {
      target: { value: 'password123' }
    });
    
    fireEvent.click(getByRole('button', { name: 'Sign In' }));
    
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  it('displays error message on invalid credentials', async () => {
    const { getByText, getByRole } = render(<Login />);
    
    fireEvent.click(getByRole('button', { name: 'Sign In' }));
    
    expect(await getByText('Invalid credentials')).toBeInTheDocument();
  });
});
```

## Recent Updates
- Added gradient styling
- Improved form validation
- Enhanced error handling
- Added social authentication
- Improved guest access

## Accessibility Features
- ARIA labels
- Error announcements
- Focus management
- Keyboard navigation
- Loading indicators

## Security Considerations
- Password strength validation
- Rate limiting
- CSRF protection
- Secure session handling
- OAuth security best practices
