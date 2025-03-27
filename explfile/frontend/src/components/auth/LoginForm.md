# LoginForm Component Documentation

## Overview
The LoginForm component handles user authentication through various methods including email/password, social logins, and guest access.

## Component Implementation

### Component Structure
```typescript
interface LoginFormProps {
  onSuccess?: () => void;
  redirectTo?: string;
}

const LoginForm: React.FC<LoginFormProps> = ({
  onSuccess,
  redirectTo = '/'
}) => {
  const { login, loginWithSocial, loginAsGuest } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  // Form validation
  const isValid = email && password && password.length >= 6;
  
  // Form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValid) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      await login(email, password);
      onSuccess?.();
      navigate(redirectTo);
    } catch (error) {
      setError(getErrorMessage(error));
    } finally {
      setIsLoading(false);
    }
  };
  
  // Social login handlers
  const handleSocialLogin = async (provider: SocialProvider) => {
    try {
      await loginWithSocial(provider);
      onSuccess?.();
      navigate(redirectTo);
    } catch (error) {
      setError(getErrorMessage(error));
    }
  };
  
  // Guest login handler
  const handleGuestLogin = async () => {
    try {
      await loginAsGuest();
      onSuccess?.();
      navigate(redirectTo);
    } catch (error) {
      setError(getErrorMessage(error));
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="login-form">
      {/* Email input */}
      <Input
        type="email"
        value={email}
        onChange={setEmail}
        placeholder="Email"
        required
      />
      
      {/* Password input */}
      <Input
        type="password"
        value={password}
        onChange={setPassword}
        placeholder="Password"
        required
        minLength={6}
      />
      
      {/* Error message */}
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {/* Submit button */}
      <Button
        type="submit"
        disabled={!isValid || isLoading}
        loading={isLoading}
      >
        Log In
      </Button>
      
      {/* Social login buttons */}
      <div className="social-buttons">
        <Button
          variant="outline"
          onClick={() => handleSocialLogin('google')}
        >
          <GoogleIcon /> Continue with Google
        </Button>
        
        <Button
          variant="outline"
          onClick={() => handleSocialLogin('github')}
        >
          <GithubIcon /> Continue with GitHub
        </Button>
        
        <Button
          variant="outline"
          onClick={() => handleSocialLogin('apple')}
        >
          <AppleIcon /> Continue with Apple
        </Button>
      </div>
      
      {/* Guest login */}
      <Button
        variant="text"
        onClick={handleGuestLogin}
      >
        Continue as Guest
      </Button>
      
      {/* Sign up link */}
      <div className="signup-link">
        Don't have an account?{' '}
        <Link to="/signup">Sign Up</Link>
      </div>
    </form>
  );
};
```

## Styling

### CSS Modules
```scss
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  
  .error-message {
    color: var(--color-error);
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }
  
  .social-buttons {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin: 1rem 0;
    
    button {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      
      svg {
        width: 1.25rem;
        height: 1.25rem;
      }
    }
  }
  
  .signup-link {
    text-align: center;
    font-size: 0.875rem;
    
    a {
      color: var(--color-primary);
      text-decoration: none;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }
}
```

## Usage Examples

### Basic Usage
```typescript
function LoginPage() {
  return (
    <div className="login-page">
      <h1>Welcome Back</h1>
      <LoginForm
        onSuccess={() => {
          toast.success('Successfully logged in!');
        }}
        redirectTo="/dashboard"
      />
    </div>
  );
}
```

### With Custom Styling
```typescript
function CustomLoginPage() {
  return (
    <div className="custom-login">
      <LoginForm
        className="custom-form"
        buttonVariant="primary"
        socialButtonVariant="secondary"
      />
    </div>
  );
}
```

### With Error Handling
```typescript
function LoginWithErrors() {
  const handleLoginError = (error: Error) => {
    if (error.message.includes('rate limit')) {
      toast.error('Too many attempts. Please try again later.');
    } else {
      toast.error('Login failed. Please check your credentials.');
    }
  };
  
  return (
    <LoginForm
      onError={handleLoginError}
      maxAttempts={3}
    />
  );
}
```

## Error Handling

### Error Types
```typescript
type LoginError =
  | 'INVALID_CREDENTIALS'
  | 'ACCOUNT_DISABLED'
  | 'RATE_LIMITED'
  | 'NETWORK_ERROR'
  | 'SOCIAL_AUTH_ERROR';

interface LoginErrorDetails {
  code: LoginError;
  message: string;
  retryAfter?: number;
}
```

### Error Handlers
```typescript
const handleLoginError = (error: unknown): LoginErrorDetails => {
  if (isApiError(error)) {
    switch (error.code) {
      case 'auth/wrong-password':
        return {
          code: 'INVALID_CREDENTIALS',
          message: 'Invalid email or password'
        };
      case 'auth/too-many-requests':
        return {
          code: 'RATE_LIMITED',
          message: 'Too many attempts. Please try again later',
          retryAfter: error.retryAfter
        };
      // ... other cases
    }
  }
  
  return {
    code: 'NETWORK_ERROR',
    message: 'Failed to connect. Please check your internet connection'
  };
};
```

## Form Validation

### Validation Rules
```typescript
interface ValidationRules {
  email: {
    pattern: RegExp;
    message: string;
  };
  password: {
    minLength: number;
    maxLength: number;
    pattern: RegExp;
    message: string;
  };
}

const validationRules: ValidationRules = {
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: 'Please enter a valid email address'
  },
  password: {
    minLength: 6,
    maxLength: 50,
    pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/,
    message: 'Password must be at least 6 characters with 1 letter and 1 number'
  }
};
```

### Validation Functions
```typescript
const validateForm = (values: FormValues): FormErrors => {
  const errors: FormErrors = {};
  
  // Validate email
  if (!values.email) {
    errors.email = 'Email is required';
  } else if (!validationRules.email.pattern.test(values.email)) {
    errors.email = validationRules.email.message;
  }
  
  // Validate password
  if (!values.password) {
    errors.password = 'Password is required';
  } else if (values.password.length < validationRules.password.minLength) {
    errors.password = validationRules.password.message;
  } else if (!validationRules.password.pattern.test(values.password)) {
    errors.password = validationRules.password.message;
  }
  
  return errors;
};
```

## Social Authentication

### Provider Configuration
```typescript
interface SocialProviderConfig {
  id: SocialProvider;
  name: string;
  icon: React.ComponentType;
  scopes: string[];
  clientId: string;
}

const socialProviders: SocialProviderConfig[] = [
  {
    id: 'google',
    name: 'Google',
    icon: GoogleIcon,
    scopes: ['profile', 'email'],
    clientId: process.env.GOOGLE_CLIENT_ID
  },
  {
    id: 'github',
    name: 'GitHub',
    icon: GithubIcon,
    scopes: ['user:email'],
    clientId: process.env.GITHUB_CLIENT_ID
  },
  {
    id: 'apple',
    name: 'Apple',
    icon: AppleIcon,
    scopes: ['name', 'email'],
    clientId: process.env.APPLE_CLIENT_ID
  }
];
```

### OAuth Flow
```typescript
const handleSocialAuth = async (provider: SocialProvider) => {
  try {
    // Get provider config
    const config = socialProviders.find(p => p.id === provider);
    if (!config) throw new Error('Invalid provider');
    
    // Initialize OAuth flow
    const auth = new OAuth2Client(config.clientId);
    
    // Open popup
    const popup = window.open(
      auth.getAuthUrl(config.scopes),
      'oauth',
      'width=500,height=600'
    );
    
    // Handle response
    const handleMessage = async (event: MessageEvent) => {
      if (event.origin !== window.location.origin) return;
      
      const { code } = event.data;
      if (!code) return;
      
      try {
        // Exchange code for tokens
        const tokens = await auth.getTokens(code);
        
        // Login with tokens
        await loginWithSocial(provider, tokens);
        
        // Close popup and cleanup
        popup?.close();
        window.removeEventListener('message', handleMessage);
        
        // Navigate on success
        onSuccess?.();
        navigate(redirectTo);
      } catch (error) {
        setError(getErrorMessage(error));
      }
    };
    
    window.addEventListener('message', handleMessage);
  } catch (error) {
    setError(getErrorMessage(error));
  }
};
```

## Guest Mode

### Guest Limits
```typescript
interface GuestLimits {
  maxImports: number;
  maxMessages: number;
  duration: number; // in milliseconds
}

const guestLimits: GuestLimits = {
  maxImports: 2,
  maxMessages: 5,
  duration: 24 * 60 * 60 * 1000 // 24 hours
};
```

### Guest Session Management
```typescript
const handleGuestSession = () => {
  // Start guest session
  const session = {
    startTime: Date.now(),
    imports: 0,
    messages: 0
  };
  
  // Store session
  localStorage.setItem('guest_session', JSON.stringify(session));
  
  // Check limits
  const checkLimits = () => {
    const stored = localStorage.getItem('guest_session');
    if (!stored) return false;
    
    const session = JSON.parse(stored);
    const elapsed = Date.now() - session.startTime;
    
    // Check duration
    if (elapsed > guestLimits.duration) {
      localStorage.removeItem('guest_session');
      return false;
    }
    
    // Check usage
    return {
      canImport: session.imports < guestLimits.maxImports,
      canMessage: session.messages < guestLimits.maxMessages,
      remaining: {
        imports: guestLimits.maxImports - session.imports,
        messages: guestLimits.maxMessages - session.messages
      }
    };
  };
  
  return { checkLimits };
};
```
