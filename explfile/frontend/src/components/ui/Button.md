# Button Component

## Purpose
The Button component is a foundational UI element in VoxStitch that provides consistent styling and behavior for all interactive buttons throughout the application.

## Component Structure

### Main Component
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  fullWidth = false,
  className,
  children,
  disabled,
  ...props
}) => {
  // Component implementation
};
```

## Variants

### 1. Primary Button
```typescript
const primaryStyles = clsx(
  'bg-gradient-to-r from-primary-500 to-primary-600',
  'hover:from-primary-600 hover:to-primary-700',
  'active:from-primary-700 active:to-primary-800',
  'text-white',
  'shadow-sm',
  'disabled:from-primary-300 disabled:to-primary-400'
);
```

### 2. Secondary Button
```typescript
const secondaryStyles = clsx(
  'bg-gradient-to-r from-surface-100 to-surface-200',
  'hover:from-surface-200 hover:to-surface-300',
  'active:from-surface-300 active:to-surface-400',
  'text-text',
  'border border-primary/20',
  'disabled:from-surface-50 disabled:to-surface-100'
);
```

### 3. Outline Button
```typescript
const outlineStyles = clsx(
  'border-2 border-primary',
  'hover:bg-gradient-to-r hover:from-primary-50 hover:to-primary-100',
  'active:from-primary-100 active:to-primary-200',
  'text-primary-600',
  'disabled:border-primary-200 disabled:text-primary-200'
);
```

### 4. Ghost Button
```typescript
const ghostStyles = clsx(
  'hover:bg-gradient-to-r hover:from-primary-50/50 hover:to-primary-100/50',
  'active:from-primary-100/50 active:to-primary-200/50',
  'text-text',
  'disabled:text-text/40'
);
```

## Size Variants

### Size Configuration
```typescript
const sizeStyles = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
};

const iconSizes = {
  sm: 'w-4 h-4',
  md: 'w-5 h-5',
  lg: 'w-6 h-6'
};
```

## Features

### 1. Loading State
```typescript
const LoadingSpinner: React.FC<{ size: keyof typeof iconSizes }> = ({
  size
}) => (
  <div
    className={clsx(
      'animate-spin rounded-full border-2',
      'border-white/30 border-t-white',
      iconSizes[size]
    )}
  />
);
```

### 2. Icon Support
```typescript
const ButtonIcon: React.FC<{
  icon: React.ReactNode;
  position: 'left' | 'right';
  size: keyof typeof iconSizes;
}> = ({ icon, position, size }) => (
  <span
    className={clsx(
      'inline-flex items-center',
      position === 'left' ? 'mr-2' : 'ml-2',
      iconSizes[size]
    )}
  >
    {icon}
  </span>
);
```

## State Management

### Button States
```typescript
const useButtonState = (isLoading: boolean, disabled?: boolean) => {
  const isDisabled = isLoading || disabled;
  const showLoader = isLoading;
  
  return {
    isDisabled,
    showLoader,
    'aria-disabled': isDisabled,
    'aria-busy': isLoading
  };
};
```

## Composition

### Button Layout
```typescript
const ButtonContent: React.FC<{
  isLoading: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  size: keyof typeof iconSizes;
}> = ({ isLoading, leftIcon, rightIcon, children, size }) => (
  <>
    {isLoading && (
      <LoadingSpinner size={size} />
    )}
    {!isLoading && leftIcon && (
      <ButtonIcon icon={leftIcon} position="left" size={size} />
    )}
    <span className={isLoading ? 'opacity-0' : ''}>
      {children}
    </span>
    {!isLoading && rightIcon && (
      <ButtonIcon icon={rightIcon} position="right" size={size} />
    )}
  </>
);
```

## Usage Examples

### Basic Usage
```typescript
<Button variant="primary" onClick={handleClick}>
  Click Me
</Button>
```

### With Icons
```typescript
<Button
  variant="primary"
  leftIcon={<PlusIcon />}
  rightIcon={<ArrowRightIcon />}
>
  Create New
</Button>
```

### Loading State
```typescript
<Button
  variant="primary"
  isLoading={isSubmitting}
  onClick={handleSubmit}
>
  Save Changes
</Button>
```

## Integration Points

### Form Integration
```typescript
const SubmitButton: React.FC<{
  isSubmitting: boolean;
  text: string;
}> = ({ isSubmitting, text }) => (
  <Button
    type="submit"
    variant="primary"
    isLoading={isSubmitting}
    fullWidth
  >
    {text}
  </Button>
);
```

### Link Button
```typescript
const LinkButton: React.FC<ButtonProps & { to: string }> = ({
  to,
  ...props
}) => (
  <Link to={to}>
    <Button {...props} />
  </Link>
);
```

## Testing
```typescript
describe('Button', () => {
  it('renders with correct variant styles', () => {
    const { getByRole } = render(
      <Button variant="primary">Click Me</Button>
    );
    const button = getByRole('button');
    expect(button).toHaveClass('bg-gradient-to-r');
  });

  it('shows loading spinner when loading', () => {
    const { getByRole } = render(
      <Button isLoading>Loading</Button>
    );
    expect(getByRole('button')).toHaveAttribute('aria-busy', 'true');
  });
});
```

## Recent Updates
- Added gradient styling
- Improved loading states
- Enhanced accessibility
- Added icon support
- Improved state management

## Accessibility Features
- ARIA attributes
- Keyboard focus styles
- Loading state announcements
- Disabled state handling
- Color contrast compliance

## Performance Considerations
- Memoized styles
- Optimized re-renders
- Efficient state updates
- Minimal DOM updates
- CSS optimization
