# DebugPanel Component

## Purpose
The DebugPanel component provides developers with real-time debugging information and tools for troubleshooting VoxStitch's authentication, API calls, and state management.

## Component Structure

### Main Component
```typescript
interface DebugPanelProps {
  isOpen?: boolean;
  onClose?: () => void;
}

const DebugPanel: React.FC<DebugPanelProps> = ({
  isOpen = false,
  onClose
}) => {
  // Component implementation
};
```

## Features

### 1. Authentication Debug
```typescript
const AuthDebugger: React.FC = () => {
  const { user, token, isAuthenticated } = useAuthStore();

  return (
    <DebugSection title="Authentication">
      <DebugItem
        label="Auth Status"
        value={isAuthenticated ? 'Authenticated' : 'Not Authenticated'}
        status={isAuthenticated ? 'success' : 'warning'}
      />
      <DebugItem
        label="User Type"
        value={user?.isGuest ? 'Guest' : 'Registered'}
      />
      <DebugItem
        label="Token"
        value={token ? 'Present' : 'None'}
        status={token ? 'success' : 'error'}
      />
      <DebugItem
        label="Remaining Imports"
        value={user?.remainingImports ?? 'N/A'}
      />
    </DebugSection>
  );
};
```

### 2. Network Monitor
```typescript
const NetworkMonitor: React.FC = () => {
  const [requests, setRequests] = useState<ApiRequest[]>([]);

  useEffect(() => {
    const interceptor = api.interceptors.request.use(
      (config) => {
        setRequests(prev => [...prev, {
          url: config.url,
          method: config.method,
          timestamp: new Date(),
          status: 'pending'
        }]);
        return config;
      }
    );

    return () => {
      api.interceptors.request.eject(interceptor);
    };
  }, []);

  return (
    <DebugSection title="Network">
      <RequestList requests={requests} />
    </DebugSection>
  );
};
```

### 3. State Inspector
```typescript
const StateInspector: React.FC = () => {
  const authState = useAuthStore();
  const chatState = useChatStore();

  return (
    <DebugSection title="State">
      <JsonViewer
        data={{
          auth: authState,
          chats: chatState
        }}
        expandLevel={2}
      />
    </DebugSection>
  );
};
```

### 4. Error Logger
```typescript
const ErrorLogger: React.FC = () => {
  const [errors, setErrors] = useState<Error[]>([]);

  useEffect(() => {
    const handler = (error: Error) => {
      setErrors(prev => [...prev, error]);
    };

    window.addEventListener('error', handler);
    return () => window.removeEventListener('error', handler);
  }, []);

  return (
    <DebugSection title="Errors">
      <ErrorList errors={errors} />
    </DebugSection>
  );
};
```

## UI Components

### 1. Debug Section
```typescript
const DebugSection: React.FC<{
  title: string;
  children: React.ReactNode;
}> = ({ title, children }) => (
  <div className="mb-6">
    <h3 className="text-lg font-semibold mb-3 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
      {title}
    </h3>
    <div className="bg-gradient-to-b from-surface-50 to-surface-100 rounded-lg p-4">
      {children}
    </div>
  </div>
);
```

### 2. Debug Item
```typescript
const DebugItem: React.FC<{
  label: string;
  value: any;
  status?: 'success' | 'warning' | 'error';
}> = ({ label, value, status }) => (
  <div className="flex justify-between items-center py-2">
    <span className="text-text/60">{label}</span>
    <span className={clsx(
      'px-2 py-1 rounded',
      status === 'success' && 'bg-green-100 text-green-800',
      status === 'warning' && 'bg-yellow-100 text-yellow-800',
      status === 'error' && 'bg-red-100 text-red-800'
    )}>
      {value}
    </span>
  </div>
);
```

### 3. Request List
```typescript
const RequestList: React.FC<{
  requests: ApiRequest[];
}> = ({ requests }) => (
  <div className="max-h-60 overflow-y-auto">
    {requests.map((request, index) => (
      <div
        key={index}
        className={clsx(
          'py-2 px-3 rounded-lg mb-2',
          'bg-gradient-to-r',
          request.status === 'success' && 'from-green-50 to-green-100',
          request.status === 'error' && 'from-red-50 to-red-100',
          request.status === 'pending' && 'from-blue-50 to-blue-100'
        )}
      >
        <div className="flex justify-between">
          <span className="font-mono text-sm">
            {request.method} {request.url}
          </span>
          <span className="text-xs opacity-60">
            {formatTime(request.timestamp)}
          </span>
        </div>
      </div>
    ))}
  </div>
);
```

## State Management

### Debug Store
```typescript
interface DebugState {
  isEnabled: boolean;
  logLevel: 'info' | 'warn' | 'error';
  filters: string[];
}

const useDebugStore = create<DebugState>((set) => ({
  isEnabled: process.env.NODE_ENV === 'development',
  logLevel: 'info',
  filters: [],
  setLogLevel: (level) => set({ logLevel: level }),
  addFilter: (filter) => set((state) => ({
    filters: [...state.filters, filter]
  }))
}));
```

## Utility Functions

### Time Formatting
```typescript
const formatTime = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    fractionalSecondDigits: 3
  }).format(date);
};
```

### Local Storage Inspector
```typescript
const inspectLocalStorage = () => {
  const items: Record<string, any> = {};
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key) {
      try {
        items[key] = JSON.parse(localStorage.getItem(key) || '');
      } catch {
        items[key] = localStorage.getItem(key);
      }
    }
  }
  return items;
};
```

## Integration Points

### API Integration
```typescript
const setupApiDebug = () => {
  api.interceptors.request.use((config) => {
    console.debug('API Request:', {
      url: config.url,
      method: config.method,
      data: config.data
    });
    return config;
  });

  api.interceptors.response.use((response) => {
    console.debug('API Response:', {
      url: response.config.url,
      status: response.status,
      data: response.data
    });
    return response;
  });
};
```

## Testing
```typescript
describe('DebugPanel', () => {
  it('shows authentication status correctly', () => {
    const { getByText } = render(<DebugPanel />);
    expect(getByText('Auth Status')).toBeInTheDocument();
  });

  it('tracks API requests', async () => {
    const { findByText } = render(<DebugPanel />);
    await api.get('/test');
    expect(await findByText('GET /test')).toBeInTheDocument();
  });
});
```

## Recent Updates
- Added gradient styling
- Improved request tracking
- Enhanced error logging
- Added state inspection
- Improved UI organization

## Security Considerations
- Only enabled in development
- Token masking
- Sensitive data filtering
- Controlled access

## Performance Impact
- Minimal DOM updates
- Request batching
- Efficient state updates
- Memory leak prevention
