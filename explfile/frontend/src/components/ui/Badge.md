# Badge Component

## Purpose
The Badge component provides visual indicators for status, counts, or labels in VoxStitch, featuring various styles and sizes with gradient effects.

## Component Structure

### Main Component
```typescript
interface BadgeProps {
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  rounded?: boolean;
  className?: string;
  children: React.ReactNode;
}

const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  size = 'md',
  rounded = false,
  className,
  children
}) => {
  // Component implementation
};
```

## Variants

### 1. Default Badge
```typescript
const defaultStyles = clsx(
  'bg-gradient-to-r from-surface-100 to-surface-200',
  'text-text',
  'border border-primary/20'
);
```

### 2. Primary Badge
```typescript
const primaryStyles = clsx(
  'bg-gradient-to-r from-primary-500 to-primary-600',
  'text-white'
);
```

### 3. Success Badge
```typescript
const successStyles = clsx(
  'bg-gradient-to-r from-green-500 to-green-600',
  'text-white'
);
```

### 4. Warning Badge
```typescript
const warningStyles = clsx(
  'bg-gradient-to-r from-yellow-500 to-yellow-600',
  'text-white'
);
```

### 5. Error Badge
```typescript
const errorStyles = clsx(
  'bg-gradient-to-r from-red-500 to-red-600',
  'text-white'
);
```

### 6. Info Badge
```typescript
const infoStyles = clsx(
  'bg-gradient-to-r from-blue-500 to-blue-600',
  'text-white'
);
```

## Size Variants

### Size Configuration
```typescript
const sizeStyles = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base'
};
```

## Features

### 1. Counter Badge
```typescript
interface CounterBadgeProps extends BadgeProps {
  count: number;
  max?: number;
}

const CounterBadge: React.FC<CounterBadgeProps> = ({
  count,
  max = 99,
  ...props
}) => (
  <Badge {...props}>
    {count > max ? `${max}+` : count}
  </Badge>
);
```

### 2. Status Badge
```typescript
interface StatusBadgeProps extends BadgeProps {
  status: 'online' | 'offline' | 'away' | 'busy';
}

const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  ...props
}) => {
  const statusConfig = {
    online: { variant: 'success', text: 'Online' },
    offline: { variant: 'default', text: 'Offline' },
    away: { variant: 'warning', text: 'Away' },
    busy: { variant: 'error', text: 'Busy' }
  };

  const config = statusConfig[status];

  return (
    <Badge
      variant={config.variant as BadgeProps['variant']}
      {...props}
    >
      <span className="flex items-center space-x-1">
        <span className="w-1.5 h-1.5 rounded-full bg-current" />
        <span>{config.text}</span>
      </span>
    </Badge>
  );
};
```

## Composition

### Badge Group
```typescript
interface BadgeGroupProps {
  spacing?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

const BadgeGroup: React.FC<BadgeGroupProps> = ({
  spacing = 'md',
  children
}) => {
  const spacingStyles = {
    sm: 'space-x-1',
    md: 'space-x-2',
    lg: 'space-x-3'
  };

  return (
    <div className={clsx('flex items-center', spacingStyles[spacing])}>
      {children}
    </div>
  );
};
```

## Usage Examples

### Basic Usage
```typescript
<Badge variant="primary">New</Badge>
```

### Counter Example
```typescript
<CounterBadge
  count={150}
  max={99}
  variant="primary"
  size="sm"
/>
```

### Status Example
```typescript
<StatusBadge status="online" size="md" />
```

### Badge Group Example
```typescript
<BadgeGroup>
  <Badge variant="primary">Feature</Badge>
  <Badge variant="success">Approved</Badge>
  <Badge variant="warning">In Progress</Badge>
</BadgeGroup>
```

## Animation

### Pulse Animation
```typescript
const PulsingBadge: React.FC<BadgeProps> = (props) => (
  <Badge
    {...props}
    className={clsx(
      'animate-pulse',
      props.className
    )}
  />
);
```

### Notification Animation
```typescript
const NotificationBadge: React.FC<BadgeProps> = (props) => (
  <Badge
    {...props}
    className={clsx(
      'relative',
      'after:content-[""] after:absolute after:-inset-1',
      'after:bg-current after:rounded-full after:opacity-30',
      'after:animate-ping',
      props.className
    )}
  />
);
```

## Integration Points

### Button Integration
```typescript
const ButtonWithBadge: React.FC<{
  badgeContent: React.ReactNode;
  children: React.ReactNode;
}> = ({ badgeContent, children }) => (
  <div className="relative inline-flex">
    <Button>{children}</Button>
    <Badge
      variant="primary"
      size="sm"
      className="absolute -top-2 -right-2"
    >
      {badgeContent}
    </Badge>
  </div>
);
```

### Menu Integration
```typescript
const MenuItemWithBadge: React.FC<{
  label: string;
  badgeContent: React.ReactNode;
}> = ({ label, badgeContent }) => (
  <div className="flex items-center justify-between px-4 py-2">
    <span>{label}</span>
    <Badge variant="primary" size="sm">
      {badgeContent}
    </Badge>
  </div>
);
```

## Testing
```typescript
describe('Badge', () => {
  it('renders with correct variant styles', () => {
    const { container } = render(
      <Badge variant="primary">Test</Badge>
    );
    expect(container.firstChild).toHaveClass('bg-gradient-to-r');
  });

  it('handles counter overflow correctly', () => {
    const { getByText } = render(
      <CounterBadge count={150} max={99} />
    );
    expect(getByText('99+')).toBeInTheDocument();
  });
});
```

## Recent Updates
- Added gradient styling
- Improved animations
- Enhanced status indicators
- Added counter variant
- Improved accessibility

## Accessibility Features
- ARIA labels
- Color contrast
- Screen reader support
- Focus visibility
- Semantic markup

## Performance Considerations
- Memoized styles
- Optimized animations
- Efficient updates
- Minimal DOM changes
- CSS optimization
