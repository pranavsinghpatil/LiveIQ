# Home.tsx

## Purpose
The Home page serves as the landing page for VoxStitch, providing users with their first interaction point and access to authentication options.

## Component Structure

### Main Sections

#### Hero Section
```typescript
const HeroSection: React.FC = () => (
  <section className="relative h-screen flex items-center justify-center bg-gradient-to-br from-primary-900/60 to-primary-600/30">
    <div className="text-center space-y-6">
      <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
        Welcome to VoxStitch
      </h1>
      <p className="text-xl text-text/80">
        Your AI Conversation Hub
      </p>
    </div>
  </section>
);
```

#### Authentication Options
```typescript
const AuthOptions: React.FC = () => {
  const { loginAsGuest } = useAuthStore();
  
  return (
    <div className="flex gap-4 justify-center">
      <Button
        variant="primary"
        onClick={() => navigate('/login')}
      >
        Sign In
      </Button>
      <Button
        variant="outline"
        onClick={() => navigate('/register')}
      >
        Create Account
      </Button>
      <Button
        variant="ghost"
        onClick={loginAsGuest}
      >
        Continue as Guest
      </Button>
    </div>
  );
};
```

## Features

### 1. Guest Mode Access
- Quick entry point for new users
- Clear display of limitations
- Smooth upgrade path

### 2. Social Authentication
```typescript
const SocialAuth: React.FC = () => (
  <div className="space-y-4">
    <Button
      variant="social"
      icon={<GoogleIcon />}
      onClick={() => handleSocialLogin('google')}
    >
      Continue with Google
    </Button>
    {/* Other social login buttons */}
  </div>
);
```

### 3. Feature Showcase
- Platform integration demos
- Usage statistics
- Testimonials section

## State Management

### Authentication State
```typescript
const Home: React.FC = () => {
  const { isAuthenticated, user } = useAuthStore();
  
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated]);
  
  // Component render
};
```

### Loading States
```typescript
const [isLoading, setIsLoading] = useState(false);
const handleGuestLogin = async () => {
  setIsLoading(true);
  try {
    await loginAsGuest();
    navigate('/dashboard');
  } catch (error) {
    toast.error('Failed to login as guest');
  } finally {
    setIsLoading(false);
  }
};
```

## UI/UX Features

### 1. Responsive Design
```typescript
const ResponsiveLayout: React.FC = ({ children }) => (
  <div className="
    px-4 
    md:px-8 
    lg:px-16 
    max-w-7xl 
    mx-auto
    grid 
    gap-8 
    md:grid-cols-2
  ">
    {children}
  </div>
);
```

### 2. Animations
```typescript
const FadeInSection: React.FC = ({ children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
  >
    {children}
  </motion.div>
);
```

### 3. Theme Integration
- Gradient backgrounds
- Consistent color scheme
- Dark mode support

## Integration Points

### API Connections
- Authentication endpoints
- Feature statistics
- Platform status

### State Management
- Auth store integration
- Theme preferences
- User settings

## Error Handling

### Authentication Errors
```typescript
const handleLoginError = (error: ApiError) => {
  switch (error.code) {
    case 'RATE_LIMITED':
      toast.error('Too many attempts. Please try again later.');
      break;
    case 'SERVICE_UNAVAILABLE':
      toast.error('Service temporarily unavailable');
      break;
    default:
      toast.error('Failed to log in. Please try again.');
  }
};
```

## Performance Optimizations

### Code Splitting
```typescript
const FeatureShowcase = lazy(() => import('./FeatureShowcase'));
const Testimonials = lazy(() => import('./Testimonials'));
```

### Image Optimization
- Lazy loading
- Responsive images
- WebP format support

## Related Components
- `Login.tsx`: User login form
- `Register.tsx`: User registration
- `Dashboard.tsx`: Main app interface
- `ImportChat.tsx`: Chat import functionality

## Testing
```typescript
describe('Home Page', () => {
  it('redirects authenticated users to dashboard', () => {
    // Test implementation
  });
  
  it('displays guest mode limitations correctly', () => {
    // Test implementation
  });
});
```

## Recent Updates
- Added gradient design system
- Improved mobile responsiveness
- Enhanced social login UI
- Added feature showcase
- Improved performance metrics

## Security Considerations
- Protected route handling
- Social auth security
- Rate limiting
- Data validation

## Accessibility
- ARIA labels
- Keyboard navigation
- Color contrast
- Screen reader support
