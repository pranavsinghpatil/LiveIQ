# Header Component

## Purpose
The Header component serves as the main navigation bar for VoxStitch, providing access to key features, user account management, and theme controls.

## Component Structure

### Main Component
```typescript
interface HeaderProps {
  onSidebarToggle?: () => void;
}

const Header: React.FC<HeaderProps> = ({
  onSidebarToggle
}) => {
  // Component implementation
};
```

## Features

### 1. Navigation Controls
```typescript
const NavigationControls: React.FC<{
  onSidebarToggle: () => void;
}> = ({ onSidebarToggle }) => (
  <div className="flex items-center">
    <button
      onClick={onSidebarToggle}
      className={clsx(
        'p-2 rounded-lg',
        'hover:bg-gradient-to-r hover:from-primary-500/10 hover:to-primary-600/10',
        'lg:hidden'  // Only show on mobile
      )}
    >
      <MenuIcon className="w-6 h-6" />
    </button>
    <Link
      to="/"
      className="ml-4 flex items-center space-x-2"
    >
      <Logo className="w-8 h-8" />
      <span className="text-xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
        VoxStitch
      </span>
    </Link>
  </div>
);
```

### 2. Search Integration
```typescript
const HeaderSearch: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={clsx(
      'hidden md:block',
      'transition-all duration-200 ease-in-out',
      isExpanded ? 'w-96' : 'w-64'
    )}>
      <SearchBar
        onFocus={() => setIsExpanded(true)}
        onBlur={() => setIsExpanded(false)}
        className="w-full"
      />
    </div>
  );
};
```

### 3. User Menu
```typescript
const UserMenu: React.FC = () => {
  const { user, logout } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={clsx(
          'flex items-center space-x-2 p-2 rounded-lg',
          'hover:bg-gradient-to-r hover:from-primary-500/10 hover:to-primary-600/10'
        )}
      >
        <Avatar user={user} />
        <span className="hidden md:block">
          {user?.name || 'Guest User'}
        </span>
        <ChevronDownIcon className="w-4 h-4" />
      </button>

      {isOpen && (
        <UserMenuDropdown
          user={user}
          onLogout={logout}
          onClose={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};
```

### 4. Theme Toggle
```typescript
const HeaderActions: React.FC = () => (
  <div className="flex items-center space-x-4">
    <ThemeToggle />
    <NotificationBell />
    <UserMenu />
  </div>
);
```

## UI Components

### 1. Notification Bell
```typescript
const NotificationBell: React.FC = () => {
  const [count, setCount] = useState(0);

  return (
    <button className="relative p-2">
      <BellIcon className="w-6 h-6" />
      {count > 0 && (
        <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-gradient-to-r from-red-500 to-red-600 text-white text-xs flex items-center justify-center">
          {count}
        </span>
      )}
    </button>
  );
};
```

### 2. User Menu Dropdown
```typescript
const UserMenuDropdown: React.FC<{
  user: User;
  onLogout: () => void;
  onClose: () => void;
}> = ({ user, onLogout, onClose }) => (
  <div className={clsx(
    'absolute right-0 mt-2 w-48',
    'bg-gradient-to-b from-surface-50 to-surface-100',
    'rounded-lg shadow-lg border border-primary/20',
    'py-2'
  )}>
    <MenuItem
      icon={<UserIcon />}
      label="Profile"
      onClick={() => navigate('/profile')}
    />
    <MenuItem
      icon={<SettingsIcon />}
      label="Settings"
      onClick={() => navigate('/settings')}
    />
    {user.isGuest && (
      <MenuItem
        icon={<UpgradeIcon />}
        label="Upgrade Account"
        onClick={() => navigate('/register')}
      />
    )}
    <MenuDivider />
    <MenuItem
      icon={<LogoutIcon />}
      label="Sign Out"
      onClick={onLogout}
    />
  </div>
);
```

## State Management

### Theme State
```typescript
const useThemeState = () => {
  const { theme, setTheme } = useTheme();
  const [isTransitioning, setIsTransitioning] = useState(false);

  const toggleTheme = useCallback(() => {
    setIsTransitioning(true);
    setTheme(theme === 'dark' ? 'light' : 'dark');
    setTimeout(() => setIsTransitioning(false), 200);
  }, [theme, setTheme]);

  return { theme, toggleTheme, isTransitioning };
};
```

### Notification State
```typescript
const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  useEffect(() => {
    const fetchNotifications = async () => {
      const response = await api.get('/notifications');
      setNotifications(response.data);
    };

    fetchNotifications();
  }, []);

  return { notifications, unreadCount: notifications.filter(n => !n.read).length };
};
```

## Responsive Design

### Mobile Optimization
```typescript
const MobileHeader: React.FC = () => (
  <div className="lg:hidden">
    <div className="flex justify-between items-center px-4 py-2">
      <NavigationControls />
      <HeaderActions />
    </div>
    <div className="px-4 py-2">
      <SearchBar />
    </div>
  </div>
);
```

### Desktop Layout
```typescript
const DesktopHeader: React.FC = () => (
  <div className="hidden lg:flex justify-between items-center px-6 py-3">
    <div className="flex items-center space-x-8">
      <NavigationControls />
      <HeaderSearch />
    </div>
    <HeaderActions />
  </div>
);
```

## Integration Points

### Route Integration
```typescript
const HeaderNavigation: React.FC = () => {
  const location = useLocation();
  
  return (
    <nav className="hidden md:flex space-x-6">
      <NavLink
        to="/dashboard"
        className={({ isActive }) => clsx(
          'px-3 py-2 rounded-lg transition-colors',
          isActive && 'bg-gradient-to-r from-primary-500/10 to-primary-600/10'
        )}
      >
        Dashboard
      </NavLink>
      {/* Other navigation links */}
    </nav>
  );
};
```

### Authentication Integration
```typescript
const AuthenticatedHeader: React.FC = () => {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <PublicHeader />;
  }

  return <PrivateHeader />;
};
```

## Event Handling

### Scroll Behavior
```typescript
const useHeaderScroll = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return isScrolled;
};
```

## Related Components
- `SearchBar`: Global search functionality
- `ThemeToggle`: Theme switching
- `UserMenu`: User account management
- `Sidebar`: Mobile navigation drawer

## Testing
```typescript
describe('Header', () => {
  it('renders user menu for authenticated users', () => {
    const { getByText } = render(<Header />);
    expect(getByText('User Menu')).toBeInTheDocument();
  });

  it('shows upgrade prompt for guest users', () => {
    const { getByText } = render(<Header />);
    expect(getByText('Upgrade Account')).toBeInTheDocument();
  });
});
```

## Recent Updates
- Added gradient styling
- Improved mobile responsiveness
- Enhanced theme transitions
- Added notification system
- Improved user menu interactions

## Accessibility Features
- ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support
- Color contrast compliance
