# Dashboard Page

## Purpose
The Dashboard page serves as the main interface for VoxStitch, displaying the user's chat history, providing import functionality, and offering powerful search and filtering capabilities.

## Component Structure

### Main Component
```typescript
interface DashboardProps {
  className?: string;
}

const Dashboard: React.FC<DashboardProps> = ({
  className
}) => {
  // Component implementation
};
```

## Features

### 1. Chat Overview
```typescript
const ChatOverview: React.FC = () => {
  const { chats, isLoading } = useChats();
  const { user } = useAuthStore();

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
            Your Chats
          </h1>
          <p className="text-text/60 mt-1">
            {chats.length} conversations from various platforms
          </p>
        </div>
        <ImportButton
          disabled={user?.isGuest && user.remainingImports === 0}
        />
      </header>
      {isLoading ? (
        <ChatListSkeleton />
      ) : (
        <ChatList chats={chats} />
      )}
    </div>
  );
};
```

### 2. Analytics Section
```typescript
const AnalyticsSection: React.FC = () => {
  const { analytics } = useAnalytics();

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard
        title="Total Chats"
        value={analytics.totalChats}
        icon={<ChatIcon />}
        trend={analytics.chatsTrend}
      />
      <StatCard
        title="Active Platforms"
        value={analytics.platforms.length}
        icon={<PlatformIcon />}
      />
      <StatCard
        title="Total Messages"
        value={analytics.totalMessages}
        icon={<MessageIcon />}
        trend={analytics.messageTrend}
      />
    </div>
  );
};
```

### 3. Recent Activity
```typescript
const RecentActivity: React.FC = () => {
  const { activities } = useActivity();

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
      <div className="space-y-4">
        {activities.map((activity) => (
          <ActivityItem
            key={activity.id}
            activity={activity}
          />
        ))}
      </div>
    </Card>
  );
};
```

### 4. Platform Distribution
```typescript
const PlatformDistribution: React.FC = () => {
  const { platforms } = usePlatforms();

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">
        Chat Platforms
      </h2>
      <div className="space-y-4">
        {platforms.map((platform) => (
          <PlatformStats
            key={platform.id}
            platform={platform}
          />
        ))}
      </div>
    </Card>
  );
};
```

## State Management

### Chat State
```typescript
const useChats = () => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await api.get('/chats');
        setChats(response.data);
      } catch (error) {
        console.error('Failed to fetch chats:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchChats();
  }, []);

  return { chats, isLoading };
};
```

### Analytics State
```typescript
const useAnalytics = () => {
  const [analytics, setAnalytics] = useState<Analytics>({
    totalChats: 0,
    totalMessages: 0,
    platforms: [],
    chatsTrend: 0,
    messageTrend: 0
  });

  useEffect(() => {
    const fetchAnalytics = async () => {
      const response = await api.get('/analytics');
      setAnalytics(response.data);
    };

    fetchAnalytics();
  }, []);

  return { analytics };
};
```

## UI Components

### 1. Stat Card
```typescript
interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  trend?: number;
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  trend
}) => (
  <Card className="p-6">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-text/60">{title}</p>
        <p className="text-2xl font-bold mt-1">{value}</p>
      </div>
      <div className={clsx(
        'p-3 rounded-lg',
        'bg-gradient-to-r from-primary-500/10 to-primary-600/10'
      )}>
        {icon}
      </div>
    </div>
    {trend && (
      <div className="mt-4 flex items-center space-x-2">
        <TrendIcon
          trend={trend}
          className={trend > 0 ? 'text-green-500' : 'text-red-500'}
        />
        <span className={clsx(
          'text-sm',
          trend > 0 ? 'text-green-600' : 'text-red-600'
        )}>
          {Math.abs(trend)}% from last month
        </span>
      </div>
    )}
  </Card>
);
```

### 2. Activity Item
```typescript
interface ActivityItemProps {
  activity: Activity;
}

const ActivityItem: React.FC<ActivityItemProps> = ({
  activity
}) => (
  <div className="flex items-center space-x-4">
    <div className={clsx(
      'p-2 rounded-lg',
      'bg-gradient-to-r from-primary-500/10 to-primary-600/10'
    )}>
      <ActivityIcon type={activity.type} />
    </div>
    <div>
      <p className="font-medium">{activity.description}</p>
      <p className="text-sm text-text/60">
        {formatTimeAgo(activity.timestamp)}
      </p>
    </div>
  </div>
);
```

## Integration Points

### Import Dialog Integration
```typescript
const ImportButton: React.FC<{ disabled?: boolean }> = ({
  disabled
}) => {
  const { openImportDialog } = useImportChat();
  const { user } = useAuthStore();

  const handleClick = () => {
    if (user?.isGuest && user.remainingImports === 0) {
      openUpgradeDialog();
    } else {
      openImportDialog();
    }
  };

  return (
    <Button
      variant="primary"
      onClick={handleClick}
      disabled={disabled}
      leftIcon={<PlusIcon />}
    >
      Import Chat
    </Button>
  );
};
```

### Search Integration
```typescript
const SearchSection: React.FC = () => {
  const { searchTerm, setSearchTerm } = useSearch();

  return (
    <div className="mb-6">
      <SearchBar
        value={searchTerm}
        onChange={setSearchTerm}
        placeholder="Search your chats..."
        className="w-full md:max-w-md"
      />
    </div>
  );
};
```

## Testing
```typescript
describe('Dashboard', () => {
  it('displays chat overview correctly', async () => {
    const { findByText } = render(<Dashboard />);
    expect(await findByText('Your Chats')).toBeInTheDocument();
  });

  it('shows import button for non-guest users', () => {
    const { getByText } = render(<Dashboard />);
    expect(getByText('Import Chat')).toBeEnabled();
  });

  it('disables import button for guests with no imports', () => {
    const { getByText } = render(<Dashboard />);
    expect(getByText('Import Chat')).toBeDisabled();
  });
});
```

## Recent Updates
- Added gradient styling
- Improved analytics display
- Enhanced activity feed
- Added platform statistics
- Improved loading states

## Accessibility Features
- ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support
- Loading indicators

## Performance Considerations
- Data pagination
- Lazy loading
- Memoized components
- Optimized re-renders
- Efficient data fetching
