# ThemeToggle Component

## Purpose
The ThemeToggle component provides an intuitive interface for switching between light and dark themes in VoxStitch, featuring smooth transitions and animated icons.

## Component Structure

### Main Component
```typescript
interface ThemeToggleProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'icon' | 'button';
  className?: string;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({
  size = 'md',
  variant = 'icon',
  className
}) => {
  // Component implementation
};
```

## Features

### 1. Theme Management
```typescript
const useThemeControl = () => {
  const { theme, setTheme } = useTheme();
  const [isTransitioning, setIsTransitioning] = useState(false);

  const toggleTheme = useCallback(() => {
    setIsTransitioning(true);
    setTheme(theme === 'dark' ? 'light' : 'dark');
    setTimeout(() => setIsTransitioning(false), 200);
  }, [theme, setTheme]);

  return {
    isDark: theme === 'dark',
    isTransitioning,
    toggleTheme
  };
};
```

### 2. Animated Icons
```typescript
const SunIcon: React.FC<{ className?: string }> = ({ className }) => (
  <motion.svg
    viewBox="0 0 24 24"
    fill="none"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    initial={{ scale: 0.5, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    exit={{ scale: 0.5, opacity: 0 }}
    transition={{ duration: 0.2 }}
  >
    <circle cx="12" cy="12" r="5" />
    <line x1="12" y1="1" x2="12" y2="3" />
    <line x1="12" y1="21" x2="12" y2="23" />
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line x1="1" y1="12" x2="3" y2="12" />
    <line x1="21" y1="12" x2="23" y2="12" />
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
  </motion.svg>
);

const MoonIcon: React.FC<{ className?: string }> = ({ className }) => (
  <motion.svg
    viewBox="0 0 24 24"
    fill="none"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    initial={{ scale: 0.5, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    exit={{ scale: 0.5, opacity: 0 }}
    transition={{ duration: 0.2 }}
  >
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
  </motion.svg>
);
```

## Variants

### 1. Icon Variant
```typescript
const IconToggle: React.FC<{
  isDark: boolean;
  size: ThemeToggleProps['size'];
}> = ({ isDark, size }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  return (
    <AnimatePresence mode="wait">
      {isDark ? (
        <MoonIcon className={clsx(
          sizeClasses[size],
          'text-yellow-400'
        )} />
      ) : (
        <SunIcon className={clsx(
          sizeClasses[size],
          'text-yellow-500'
        )} />
      )}
    </AnimatePresence>
  );
};
```

### 2. Button Variant
```typescript
const ButtonToggle: React.FC<{
  isDark: boolean;
  size: ThemeToggleProps['size'];
}> = ({ isDark, size }) => {
  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  return (
    <span className={clsx(
      'flex items-center space-x-2',
      sizeClasses[size]
    )}>
      <IconToggle isDark={isDark} size={size} />
      <span>
        {isDark ? 'Dark' : 'Light'} Mode
      </span>
    </span>
  );
};
```

## State Management

### Theme Persistence
```typescript
const useThemePersistence = () => {
  const { theme } = useTheme();

  useEffect(() => {
    localStorage.setItem('voxstitch-theme', theme);
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  return theme;
};
```

### System Preference Detection
```typescript
const useSystemTheme = () => {
  const [systemTheme, setSystemTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e: MediaQueryListEvent) => {
      setSystemTheme(e.matches ? 'dark' : 'light');
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return systemTheme;
};
```

## Integration

### Layout Integration
```typescript
const ThemeControl: React.FC = () => (
  <div className="flex items-center space-x-4">
    <ThemeToggle variant="button" />
    <Button
      variant="ghost"
      onClick={() => setTheme('system')}
    >
      Use System
    </Button>
  </div>
);
```

### Sidebar Integration
```typescript
const SidebarThemeToggle: React.FC = () => (
  <div className="px-4 py-2 border-t border-primary/10">
    <ThemeToggle
      variant="button"
      size="lg"
    />
  </div>
);
```

## Animation

### Transition Effects
```typescript
const useThemeTransition = () => {
  const [isTransitioning, setIsTransitioning] = useState(false);

  const startTransition = () => {
    setIsTransitioning(true);
    document.documentElement.classList.add('transitioning');
    setTimeout(() => {
      setIsTransitioning(false);
      document.documentElement.classList.remove('transitioning');
    }, 200);
  };

  return { isTransitioning, startTransition };
};
```

## Testing
```typescript
describe('ThemeToggle', () => {
  it('toggles theme on click', () => {
    const { getByRole } = render(<ThemeToggle />);
    const button = getByRole('button');
    
    fireEvent.click(button);
    expect(document.documentElement).toHaveClass('dark');
    
    fireEvent.click(button);
    expect(document.documentElement).not.toHaveClass('dark');
  });

  it('respects size prop', () => {
    const { container } = render(<ThemeToggle size="lg" />);
    expect(container.firstChild).toHaveClass('w-8 h-8');
  });
});
```

## Recent Updates
- Added gradient styling
- Improved animations
- Enhanced system theme detection
- Added button variant
- Improved accessibility

## Accessibility Features
- ARIA labels
- Keyboard support
- High contrast mode
- Screen reader support
- Focus management

## Performance Considerations
- Debounced transitions
- Memoized components
- Optimized animations
- Efficient state updates
- Minimal DOM updates
