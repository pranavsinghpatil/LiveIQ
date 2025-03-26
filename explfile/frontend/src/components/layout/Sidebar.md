# Sidebar Component

## Purpose
The Sidebar component provides primary navigation and quick actions in VoxStitch, offering easy access to different sections of the application and import functionality.

## Component Structure

### Main Component
```typescript
interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  onClose,
  className
}) => {
  // Component implementation
};
```

## Features

### 1. Navigation Menu
```typescript
const NavigationMenu: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="space-y-2">
      {NAV_ITEMS.map((item) => (
        <NavItem
          key={item.path}
          {...item}
          isActive={location.pathname === item.path}
        />
      ))}
    </nav>
  );
};
```

### 2. Quick Actions
```typescript
const QuickActions: React.FC = () => {
  const { openImportDialog } = useImportChat();
  const { user } = useAuthStore();

  return (
    <div className="space-y-3">
      <Button
        variant="primary"
        className="w-full"
        onClick={openImportDialog}
        disabled={user?.isGuest && user.remainingImports === 0}
      >
        <PlusIcon className="w-5 h-5 mr-2" />
        Import Chat
      </Button>
      {/* Other quick actions */}
    </div>
  );
};
```

### 3. User Section
```typescript
const UserSection: React.FC = () => {
  const { user } = useAuthStore();

  return (
    <div className={clsx(
      'p-4 rounded-lg',
      'bg-gradient-to-r from-primary-500/10 to-primary-600/10'
    )}>
      <div className="flex items-center space-x-3">
        <Avatar user={user} size="lg" />
        <div>
          <h3 className="font-semibold">
            {user?.name || 'Guest User'}
          </h3>
          {user?.isGuest && (
            <p className="text-sm text-text/60">
              {user.remainingImports} imports remaining
            </p>
          )}
        </div>
      </div>
    </div>
  );
};
```

## UI Components

### 1. Navigation Item
```typescript
interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  path: string;
  isActive: boolean;
}

const NavItem: React.FC<NavItemProps> = ({
  icon,
  label,
  path,
  isActive
}) => (
  <Link
    to={path}
    className={clsx(
      'flex items-center space-x-3 px-4 py-3 rounded-lg',
      'transition-colors duration-200',
      isActive
        ? 'bg-gradient-to-r from-primary-500/20 to-primary-600/20'
        : 'hover:bg-gradient-to-r hover:from-primary-500/10 hover:to-primary-600/10'
    )}
  >
    <span className={clsx(
      'text-xl',
      isActive ? 'text-primary-500' : 'text-text/60'
    )}>
      {icon}
    </span>
    <span className={isActive ? 'font-medium' : ''}>
      {label}
    </span>
  </Link>
);
```

### 2. Section Header
```typescript
const SectionHeader: React.FC<{
  title: string;
  action?: React.ReactNode;
}> = ({ title, action }) => (
  <div className="flex items-center justify-between px-4 py-2">
    <h2 className="text-sm font-semibold text-text/60 uppercase tracking-wider">
      {title}
    </h2>
    {action}
  </div>
);
```

## State Management

### Sidebar State
```typescript
const useSidebarState = () => {
  const [isOpen, setIsOpen] = useState(false);
  const isMobile = useMediaQuery('(max-width: 1024px)');

  useEffect(() => {
    if (!isMobile) {
      setIsOpen(true);
    }
  }, [isMobile]);

  return { isOpen, setIsOpen, isMobile };
};
```

### Navigation State
```typescript
const useNavigation = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const activeSection = useMemo(() => {
    return NAV_ITEMS.find(item => 
      location.pathname.startsWith(item.path)
    );
  }, [location.pathname]);

  return { activeSection, navigate };
};
```

## Layout Management

### Responsive Layout
```typescript
const SidebarLayout: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}> = ({ isOpen, onClose, children }) => {
  const isMobile = useMediaQuery('(max-width: 1024px)');

  if (isMobile) {
    return (
      <Dialog
        open={isOpen}
        onClose={onClose}
        className="fixed inset-y-0 left-0 w-64"
      >
        {children}
      </Dialog>
    );
  }

  return (
    <aside className="hidden lg:block w-64 flex-shrink-0">
      {children}
    </aside>
  );
};
```

### Content Organization
```typescript
const SidebarContent: React.FC = () => (
  <div className="h-full flex flex-col bg-gradient-to-b from-surface-50 to-surface-100">
    <div className="flex-1 overflow-y-auto py-4 space-y-6">
      <UserSection />
      <QuickActions />
      <NavigationMenu />
    </div>
    <div className="p-4 border-t border-primary/10">
      <ThemeToggle />
    </div>
  </div>
);
```

## Integration Points

### Import Dialog Integration
```typescript
const ImportAction: React.FC = () => {
  const { openImportDialog } = useImportChat();
  const { user } = useAuthStore();

  const handleImportClick = () => {
    if (user?.isGuest && user.remainingImports === 0) {
      openUpgradeDialog();
    } else {
      openImportDialog();
    }
  };

  return (
    <Button
      variant="primary"
      onClick={handleImportClick}
      className="w-full"
    >
      Import Chat
    </Button>
  );
};
```

## Event Handling

### Click Outside
```typescript
const useClickOutside = (ref: React.RefObject<HTMLElement>, handler: () => void) => {
  useEffect(() => {
    const listener = (event: MouseEvent) => {
      if (!ref.current?.contains(event.target as Node)) {
        handler();
      }
    };

    document.addEventListener('mousedown', listener);
    return () => document.removeEventListener('mousedown', listener);
  }, [ref, handler]);
};
```

## Related Components
- `Header`: Top navigation bar
- `ImportChat`: Chat import dialog
- `ThemeToggle`: Theme switching
- `Avatar`: User avatar display

## Testing
```typescript
describe('Sidebar', () => {
  it('shows correct navigation items', () => {
    const { getAllByRole } = render(<Sidebar />);
    const navItems = getAllByRole('link');
    expect(navItems).toHaveLength(NAV_ITEMS.length);
  });

  it('handles mobile responsiveness', () => {
    const { container } = render(<Sidebar />);
    expect(container).toHaveClass('lg:block');
  });
});
```

## Recent Updates
- Added gradient styling
- Improved mobile responsiveness
- Enhanced theme integration
- Added quick actions
- Improved user section

## Accessibility Features
- ARIA labels
- Keyboard navigation
- Focus trapping in mobile view
- Screen reader announcements
- Color contrast compliance
