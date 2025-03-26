# Register Page

## Purpose
The Register page enables new users to create accounts in VoxStitch, offering a seamless onboarding experience with social signup options and guest account upgrades.

## Component Structure

### Main Component
```typescript
interface RegisterProps {
  className?: string;
}

const Register: React.FC<RegisterProps> = ({
  className
}) => {
  // Component implementation
};
```

## Features

### 1. Registration Form
```typescript
const RegistrationForm: React.FC = () => {
  const { register } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (values: RegisterFormValues) => {
    setIsLoading(true);
    setError(null);

    try {
      await register(values);
      navigate('/dashboard');
    } catch (err) {
      setError('Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <div className="space-y-4">
        <FormField
          label="Full Name"
          name="name"
          type="text"
          required
          autoFocus
        />
        <FormField
          label="Email"
          name="email"
          type="email"
          required
        />
        <FormField
          label="Password"
          name="password"
          type="password"
          required
        />
        <FormField
          label="Confirm Password"
          name="confirmPassword"
          type="password"
          required
        />
        <div className="space-y-2">
          <Checkbox
            label="I agree to the Terms of Service and Privacy Policy"
            name="terms"
            required
          />
          <Checkbox
            label="Subscribe to our newsletter"
            name="newsletter"
          />
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
          Create Account
        </Button>
      </div>
    </Form>
  );
};
```

### 2. Social Registration
```typescript
const SocialRegistration: React.FC = () => (
  <div className="space-y-3">
    <Button
      variant="outline"
      fullWidth
      leftIcon={<GoogleIcon />}
      onClick={() => signUpWithGoogle()}
    >
      Sign up with Google
    </Button>
    <Button
      variant="outline"
      fullWidth
      leftIcon={<GithubIcon />}
      onClick={() => signUpWithGithub()}
    >
      Sign up with GitHub
    </Button>
    <Button
      variant="outline"
      fullWidth
      leftIcon={<AppleIcon />}
      onClick={() => signUpWithApple()}
    >
      Sign up with Apple
    </Button>
  </div>
);
```

### 3. Guest Upgrade
```typescript
const GuestUpgrade: React.FC = () => {
  const { user, upgradeGuestAccount } = useAuthStore();

  if (!user?.isGuest) {
    return null;
  }

  return (
    <div className={clsx(
      'p-4 rounded-lg',
      'bg-gradient-to-r from-primary-500/10 to-primary-600/10'
    )}>
      <h3 className="text-lg font-semibold mb-2">
        Upgrade Your Guest Account
      </h3>
      <p className="text-text/60 mb-4">
        Keep your existing chats and unlock unlimited access.
      </p>
      <Button
        variant="primary"
        onClick={upgradeGuestAccount}
        fullWidth
      >
        Upgrade Now
      </Button>
    </div>
  );
};
```

## State Management

### Registration State
```typescript
const useRegistration = () => {
  const { register, upgradeGuestAccount } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRegister = async (values: RegisterFormValues) => {
    setIsLoading(true);
    setError(null);

    try {
      if (values.password !== values.confirmPassword) {
        throw new Error('Passwords do not match');
      }

      await register(values);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGuestUpgrade = async (values: RegisterFormValues) => {
    setIsLoading(true);
    setError(null);

    try {
      await upgradeGuestAccount(values);
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to upgrade account. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    error,
    handleRegister,
    handleGuestUpgrade
  };
};
```

## UI Components

### 1. Password Strength Indicator
```typescript
interface PasswordStrengthProps {
  password: string;
}

const PasswordStrength: React.FC<PasswordStrengthProps> = ({
  password
}) => {
  const strength = calculatePasswordStrength(password);

  return (
    <div className="mt-1">
      <div className="h-1 w-full bg-surface-200 rounded-full overflow-hidden">
        <div
          className={clsx(
            'h-full transition-all duration-300',
            'bg-gradient-to-r',
            strength === 'weak' && 'from-red-500 to-red-600 w-1/3',
            strength === 'medium' && 'from-yellow-500 to-yellow-600 w-2/3',
            strength === 'strong' && 'from-green-500 to-green-600 w-full'
          )}
        />
      </div>
      <p className={clsx(
        'text-xs mt-1',
        strength === 'weak' && 'text-red-600',
        strength === 'medium' && 'text-yellow-600',
        strength === 'strong' && 'text-green-600'
      )}>
        Password strength: {strength}
      </p>
    </div>
  );
};
```

### 2. Terms Dialog
```typescript
const TermsDialog: React.FC<{
  isOpen: boolean;
  onClose: () => void;
}> = ({ isOpen, onClose }) => (
  <Dialog
    open={isOpen}
    onClose={onClose}
    className="max-w-2xl w-full"
  >
    <div className="p-6">
      <h2 className="text-lg font-semibold mb-4">
        Terms of Service
      </h2>
      <div className="prose prose-sm max-h-96 overflow-y-auto">
        {/* Terms content */}
      </div>
      <div className="mt-6 flex justify-end">
        <Button
          variant="primary"
          onClick={onClose}
        >
          I Agree
        </Button>
      </div>
    </div>
  </Dialog>
);
```

## Integration Points

### OAuth Integration
```typescript
const useOAuthRegistration = () => {
  const signUpWithGoogle = async () => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      const credential = GoogleAuthProvider.credentialFromResult(result);
      await handleOAuthRegistration(credential);
    } catch (error) {
      console.error('Google sign-up failed:', error);
    }
  };

  const signUpWithGithub = async () => {
    const provider = new GithubAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      const credential = GithubAuthProvider.credentialFromResult(result);
      await handleOAuthRegistration(credential);
    } catch (error) {
      console.error('GitHub sign-up failed:', error);
    }
  };

  return { signUpWithGoogle, signUpWithGithub };
};
```

## Testing
```typescript
describe('Register', () => {
  it('validates password match', async () => {
    const { getByLabelText, getByText } = render(<Register />);
    
    fireEvent.change(getByLabelText('Password'), {
      target: { value: 'password123' }
    });
    fireEvent.change(getByLabelText('Confirm Password'), {
      target: { value: 'password456' }
    });
    
    fireEvent.click(getByText('Create Account'));
    
    expect(await getByText('Passwords do not match')).toBeInTheDocument();
  });

  it('handles guest upgrade correctly', async () => {
    const { getByText } = render(<Register />);
    
    fireEvent.click(getByText('Upgrade Now'));
    
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });
});
```

## Recent Updates
- Added gradient styling
- Improved form validation
- Enhanced password strength indicator
- Added social registration
- Improved guest upgrade flow

## Accessibility Features
- ARIA labels
- Error announcements
- Focus management
- Keyboard navigation
- Loading indicators

## Security Considerations
- Password strength requirements
- Email verification
- Rate limiting
- CSRF protection
- OAuth security best practices
