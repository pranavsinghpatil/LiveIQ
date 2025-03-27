# SignupForm Component Documentation

## Overview
The SignupForm component handles new user registration with email/password and social signup options.

## Component Implementation

### Component Structure
```typescript
interface SignupFormProps {
  onSuccess?: () => void;
  redirectTo?: string;
}

const SignupForm: React.FC<SignupFormProps> = ({
  onSuccess,
  redirectTo = '/dashboard'
}) => {
  const { signup, signupWithSocial } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  // Form validation
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  // Form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      await signup({
        name: formData.name,
        email: formData.email,
        password: formData.password
      });
      
      onSuccess?.();
      navigate(redirectTo);
    } catch (error) {
      setError(getErrorMessage(error));
    } finally {
      setIsLoading(false);
    }
  };
  
  // Social signup handlers
  const handleSocialSignup = async (provider: SocialProvider) => {
    try {
      await signupWithSocial(provider);
      onSuccess?.();
      navigate(redirectTo);
    } catch (error) {
      setError(getErrorMessage(error));
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="signup-form">
      {/* Name input */}
      <Input
        label="Name"
        value={formData.name}
        onChange={(value) => setFormData({ ...formData, name: value })}
        error={errors.name}
        required
      />
      
      {/* Email input */}
      <Input
        type="email"
        label="Email"
        value={formData.email}
        onChange={(value) => setFormData({ ...formData, email: value })}
        error={errors.email}
        required
      />
      
      {/* Password input */}
      <Input
        type="password"
        label="Password"
        value={formData.password}
        onChange={(value) => setFormData({ ...formData, password: value })}
        error={errors.password}
        required
        minLength={6}
      />
      
      {/* Confirm password input */}
      <Input
        type="password"
        label="Confirm Password"
        value={formData.confirmPassword}
        onChange={(value) => setFormData({ ...formData, confirmPassword: value })}
        error={errors.confirmPassword}
        required
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
        disabled={isLoading}
        loading={isLoading}
      >
        Sign Up
      </Button>
      
      {/* Social signup buttons */}
      <div className="social-buttons">
        <Button
          variant="outline"
          onClick={() => handleSocialSignup('google')}
        >
          <GoogleIcon /> Sign up with Google
        </Button>
        
        <Button
          variant="outline"
          onClick={() => handleSocialSignup('github')}
        >
          <GithubIcon /> Sign up with GitHub
        </Button>
        
        <Button
          variant="outline"
          onClick={() => handleSocialSignup('apple')}
        >
          <AppleIcon /> Sign up with Apple
        </Button>
      </div>
      
      {/* Login link */}
      <div className="login-link">
        Already have an account?{' '}
        <Link to="/login">Log In</Link>
      </div>
    </form>
  );
};
```

## Styling

### CSS Modules
```scss
.signup-form {
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
  
  .login-link {
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
function SignupPage() {
  return (
    <div className="signup-page">
      <h1>Create Account</h1>
      <SignupForm
        onSuccess={() => {
          toast.success('Account created successfully!');
        }}
        redirectTo="/onboarding"
      />
    </div>
  );
}
```

### With Custom Validation
```typescript
function CustomSignupForm() {
  const customValidation = (values: FormValues) => {
    const errors: FormErrors = {};
    
    // Custom password strength validation
    if (values.password) {
      const strength = calculatePasswordStrength(values.password);
      if (strength < 80) {
        errors.password = 'Password is too weak';
      }
    }
    
    return errors;
  };
  
  return (
    <SignupForm
      validate={customValidation}
      passwordStrengthMeter
    />
  );
}
```

### With Terms Agreement
```typescript
function SignupWithTerms() {
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  
  return (
    <SignupForm
      extraFields={
        <Checkbox
          label="I agree to the Terms and Privacy Policy"
          checked={agreedToTerms}
          onChange={setAgreedToTerms}
          required
        />
      }
      submitDisabled={!agreedToTerms}
    />
  );
}
```

## Form Validation

### Validation Schema
```typescript
interface ValidationSchema {
  name: {
    required: boolean;
    minLength: number;
    maxLength: number;
  };
  email: {
    required: boolean;
    pattern: RegExp;
  };
  password: {
    required: boolean;
    minLength: number;
    maxLength: number;
    pattern: RegExp;
    strengthChecks: {
      minLength: number;
      uppercase: boolean;
      lowercase: boolean;
      numbers: boolean;
      symbols: boolean;
    };
  };
}

const validationSchema: ValidationSchema = {
  name: {
    required: true,
    minLength: 2,
    maxLength: 50
  },
  email: {
    required: true,
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  },
  password: {
    required: true,
    minLength: 6,
    maxLength: 50,
    pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/,
    strengthChecks: {
      minLength: 8,
      uppercase: true,
      lowercase: true,
      numbers: true,
      symbols: true
    }
  }
};
```

### Password Strength Meter
```typescript
interface PasswordStrength {
  score: number;
  feedback: string[];
}

const calculatePasswordStrength = (password: string): PasswordStrength => {
  const strength: PasswordStrength = {
    score: 0,
    feedback: []
  };
  
  // Length check
  if (password.length >= 8) {
    strength.score += 20;
  } else {
    strength.feedback.push('Password should be at least 8 characters');
  }
  
  // Uppercase check
  if (/[A-Z]/.test(password)) {
    strength.score += 20;
  } else {
    strength.feedback.push('Add uppercase letters');
  }
  
  // Lowercase check
  if (/[a-z]/.test(password)) {
    strength.score += 20;
  } else {
    strength.feedback.push('Add lowercase letters');
  }
  
  // Numbers check
  if (/\d/.test(password)) {
    strength.score += 20;
  } else {
    strength.feedback.push('Add numbers');
  }
  
  // Symbols check
  if (/[!@#$%^&*]/.test(password)) {
    strength.score += 20;
  } else {
    strength.feedback.push('Add special characters');
  }
  
  return strength;
};
```

## Social Authentication

### Provider Configuration
```typescript
interface SignupProviderConfig extends SocialProviderConfig {
  requiredFields: string[];
  termsRequired: boolean;
}

const signupProviders: SignupProviderConfig[] = [
  {
    id: 'google',
    name: 'Google',
    icon: GoogleIcon,
    scopes: ['profile', 'email'],
    clientId: process.env.GOOGLE_CLIENT_ID,
    requiredFields: ['name', 'email'],
    termsRequired: true
  },
  {
    id: 'github',
    name: 'GitHub',
    icon: GithubIcon,
    scopes: ['user:email'],
    clientId: process.env.GITHUB_CLIENT_ID,
    requiredFields: ['name', 'email'],
    termsRequired: true
  },
  {
    id: 'apple',
    name: 'Apple',
    icon: AppleIcon,
    scopes: ['name', 'email'],
    clientId: process.env.APPLE_CLIENT_ID,
    requiredFields: ['name', 'email'],
    termsRequired: true
  }
];
```

### Profile Completion
```typescript
interface ProfileCompletion {
  requiredFields: string[];
  optionalFields: string[];
  data: Record<string, any>;
}

const handleProfileCompletion = async (
  provider: SocialProvider,
  userData: any
): Promise<void> => {
  const config = signupProviders.find(p => p.id === provider);
  if (!config) throw new Error('Invalid provider');
  
  // Check required fields
  const missing = config.requiredFields.filter(
    field => !userData[field]
  );
  
  if (missing.length > 0) {
    // Show profile completion form
    const completion = await showProfileCompletion({
      requiredFields: missing,
      optionalFields: ['avatar', 'bio'],
      data: userData
    });
    
    // Update user data
    Object.assign(userData, completion);
  }
  
  // Continue with signup
  await signupWithSocial(provider, userData);
};
```

## Error Handling

### Error Types
```typescript
type SignupError =
  | 'EMAIL_IN_USE'
  | 'INVALID_EMAIL'
  | 'WEAK_PASSWORD'
  | 'SOCIAL_AUTH_ERROR'
  | 'NETWORK_ERROR';

interface SignupErrorDetails {
  code: SignupError;
  message: string;
  field?: string;
}
```

### Error Handlers
```typescript
const handleSignupError = (error: unknown): SignupErrorDetails => {
  if (isApiError(error)) {
    switch (error.code) {
      case 'auth/email-already-in-use':
        return {
          code: 'EMAIL_IN_USE',
          message: 'This email is already registered',
          field: 'email'
        };
      case 'auth/invalid-email':
        return {
          code: 'INVALID_EMAIL',
          message: 'Invalid email format',
          field: 'email'
        };
      case 'auth/weak-password':
        return {
          code: 'WEAK_PASSWORD',
          message: 'Password is too weak',
          field: 'password'
        };
      // ... other cases
    }
  }
  
  return {
    code: 'NETWORK_ERROR',
    message: 'Failed to create account. Please try again'
  };
};
```
