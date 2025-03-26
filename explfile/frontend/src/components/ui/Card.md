# Card Component

## Purpose
The Card component provides a consistent container for content display in VoxStitch, featuring flexible layouts, hover effects, and gradient styling.

## Component Structure

### Main Component
```typescript
interface CardProps {
  variant?: 'default' | 'interactive' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
  children: React.ReactNode;
  onClick?: () => void;
}

const Card: React.FC<CardProps> = ({
  variant = 'default',
  padding = 'md',
  className,
  children,
  onClick
}) => {
  // Component implementation
};
```

## Variants

### 1. Default Card
```typescript
const defaultStyles = clsx(
  'bg-gradient-to-b from-surface-50 to-surface-100',
  'border border-primary/20',
  'rounded-lg'
);
```

### 2. Interactive Card
```typescript
const interactiveStyles = clsx(
  'bg-gradient-to-b from-surface-50 to-surface-100',
  'border border-primary/20',
  'rounded-lg',
  'transition-all duration-200',
  'hover:shadow-lg hover:scale-[1.02]',
  'hover:border-primary/30',
  'active:scale-[0.98]',
  'cursor-pointer'
);
```

### 3. Elevated Card
```typescript
const elevatedStyles = clsx(
  'bg-gradient-to-b from-surface-50 to-surface-100',
  'border border-primary/20',
  'rounded-lg',
  'shadow-lg'
);
```

## Sub-Components

### 1. Card Header
```typescript
interface CardHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  className?: string;
}

const CardHeader: React.FC<CardHeaderProps> = ({
  title,
  subtitle,
  action,
  className
}) => (
  <div className={clsx(
    'flex items-start justify-between',
    'border-b border-primary/10',
    'p-4',
    className
  )}>
    <div>
      <h3 className="text-lg font-semibold">
        {title}
      </h3>
      {subtitle && (
        <p className="text-sm text-text/60 mt-1">
          {subtitle}
        </p>
      )}
    </div>
    {action && (
      <div className="ml-4">
        {action}
      </div>
    )}
  </div>
);
```

### 2. Card Content
```typescript
interface CardContentProps {
  className?: string;
  children: React.ReactNode;
}

const CardContent: React.FC<CardContentProps> = ({
  className,
  children
}) => (
  <div className={clsx('p-4', className)}>
    {children}
  </div>
);
```

### 3. Card Footer
```typescript
interface CardFooterProps {
  className?: string;
  children: React.ReactNode;
}

const CardFooter: React.FC<CardFooterProps> = ({
  className,
  children
}) => (
  <div className={clsx(
    'border-t border-primary/10',
    'p-4',
    'mt-auto',
    className
  )}>
    {children}
  </div>
);
```

## Features

### 1. Hover Effects
```typescript
const useHoverEffect = (variant: CardProps['variant']) => {
  const [isHovered, setIsHovered] = useState(false);

  if (variant !== 'interactive') {
    return {};
  }

  return {
    onMouseEnter: () => setIsHovered(true),
    onMouseLeave: () => setIsHovered(false),
    className: clsx(
      isHovered && [
        'shadow-lg',
        'scale-[1.02]',
        'border-primary/30'
      ]
    )
  };
};
```

### 2. Loading State
```typescript
interface CardSkeletonProps {
  lines?: number;
  hasHeader?: boolean;
  hasFooter?: boolean;
}

const CardSkeleton: React.FC<CardSkeletonProps> = ({
  lines = 3,
  hasHeader = false,
  hasFooter = false
}) => (
  <div className={defaultStyles}>
    {hasHeader && (
      <div className="p-4 border-b border-primary/10">
        <div className="h-6 w-1/3 bg-gradient-to-r from-surface-200 to-surface-300 rounded animate-pulse" />
      </div>
    )}
    <div className="p-4 space-y-3">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-4 bg-gradient-to-r from-surface-200 to-surface-300 rounded animate-pulse"
          style={{ width: `${Math.random() * 50 + 50}%` }}
        />
      ))}
    </div>
    {hasFooter && (
      <div className="p-4 border-t border-primary/10">
        <div className="h-4 w-1/4 bg-gradient-to-r from-surface-200 to-surface-300 rounded animate-pulse" />
      </div>
    )}
  </div>
);
```

## Composition

### Layout Composition
```typescript
const CompoundCard: React.FC<CardProps> = ({
  children,
  ...props
}) => (
  <Card {...props}>
    <CardHeader
      title="Card Title"
      subtitle="Card Subtitle"
      action={<Button variant="ghost">Action</Button>}
    />
    <CardContent>
      {children}
    </CardContent>
    <CardFooter>
      Footer Content
    </CardFooter>
  </Card>
);
```

## Usage Examples

### Basic Usage
```typescript
<Card>
  <p>Simple card content</p>
</Card>
```

### Interactive Card
```typescript
<Card
  variant="interactive"
  onClick={() => handleCardClick()}
>
  <CardHeader title="Click Me" />
  <CardContent>
    Interactive card content
  </CardContent>
</Card>
```

### Loading State
```typescript
<CardSkeleton
  lines={4}
  hasHeader
  hasFooter
/>
```

## Integration Points

### List Integration
```typescript
const CardList: React.FC<{
  items: Array<{ id: string; title: string; content: string }>;
}> = ({ items }) => (
  <div className="space-y-4">
    {items.map(item => (
      <Card
        key={item.id}
        variant="interactive"
      >
        <CardHeader title={item.title} />
        <CardContent>
          {item.content}
        </CardContent>
      </Card>
    ))}
  </div>
);
```

## Testing
```typescript
describe('Card', () => {
  it('renders with correct variant styles', () => {
    const { container } = render(
      <Card variant="elevated">Content</Card>
    );
    expect(container.firstChild).toHaveClass('shadow-lg');
  });

  it('handles click events on interactive variant', () => {
    const handleClick = jest.fn();
    const { container } = render(
      <Card variant="interactive" onClick={handleClick}>
        Click Me
      </Card>
    );
    fireEvent.click(container.firstChild!);
    expect(handleClick).toHaveBeenCalled();
  });
});
```

## Recent Updates
- Added gradient styling
- Improved hover effects
- Enhanced loading states
- Added compound components
- Improved accessibility

## Accessibility Features
- Semantic HTML structure
- ARIA labels
- Keyboard interaction
- Focus management
- Screen reader support

## Performance Considerations
- Memoized styles
- Conditional rendering
- Optimized animations
- Efficient state updates
- Minimal DOM updates
