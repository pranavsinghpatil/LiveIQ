# UI Store Documentation

## Overview
The UI store manages the global UI state of the application, including theme settings, modals, toasts, and layout preferences.

## Store Implementation

### Store Definition
```typescript
interface UiStore {
  // Theme
  theme: Theme;
  isDarkMode: boolean;
  
  // Layout
  isSidebarOpen: boolean;
  isImportDialogOpen: boolean;
  isSettingsOpen: boolean;
  
  // Modals
  modals: Record<string, Modal>;
  activeModal: string | null;
  
  // Toasts
  toasts: Toast[];
  
  // Actions
  toggleTheme: () => void;
  toggleSidebar: () => void;
  toggleImportDialog: () => void;
  toggleSettings: () => void;
  openModal: (modal: Modal) => void;
  closeModal: (id: string) => void;
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
}

const useUiStore = create<UiStore>((set, get) => ({
  // Initial theme state
  theme: defaultTheme,
  isDarkMode: false,
  
  // Initial layout state
  isSidebarOpen: true,
  isImportDialogOpen: false,
  isSettingsOpen: false,
  
  // Initial modal state
  modals: {},
  activeModal: null,
  
  // Initial toast state
  toasts: [],
  
  // Theme actions
  toggleTheme: () => {
    set((state) => {
      const isDarkMode = !state.isDarkMode;
      return {
        isDarkMode,
        theme: isDarkMode ? darkTheme : lightTheme
      };
    });
  },
  
  // Layout actions
  toggleSidebar: () => {
    set((state) => ({
      isSidebarOpen: !state.isSidebarOpen
    }));
  },
  
  toggleImportDialog: () => {
    set((state) => ({
      isImportDialogOpen: !state.isImportDialogOpen
    }));
  },
  
  toggleSettings: () => {
    set((state) => ({
      isSettingsOpen: !state.isSettingsOpen
    }));
  },
  
  // Modal actions
  openModal: (modal: Modal) => {
    set((state) => ({
      modals: {
        ...state.modals,
        [modal.id]: modal
      },
      activeModal: modal.id
    }));
  },
  
  closeModal: (id: string) => {
    set((state) => {
      const { [id]: _, ...remainingModals } = state.modals;
      return {
        modals: remainingModals,
        activeModal: state.activeModal === id ? null : state.activeModal
      };
    });
  },
  
  // Toast actions
  addToast: (toast) => {
    const id = generateId();
    set((state) => ({
      toasts: [...state.toasts, { ...toast, id }]
    }));
    
    // Auto remove toast after duration
    if (toast.duration) {
      setTimeout(() => {
        get().removeToast(id);
      }, toast.duration);
    }
  },
  
  removeToast: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((toast) => toast.id !== id)
    }));
  }
}));
```

## Theme Configuration

### Theme Types
```typescript
interface Theme {
  mode: 'light' | 'dark';
  colors: {
    background: string;
    backgroundDark: string;
    text: string;
    textSecondary: string;
    primary: string;
    primaryHover: string;
    border: string;
    error: string;
    success: string;
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  borderRadius: {
    sm: string;
    md: string;
    lg: string;
    full: string;
  };
  typography: {
    fontFamily: string;
    fontSize: {
      xs: string;
      sm: string;
      md: string;
      lg: string;
      xl: string;
    };
    fontWeight: {
      normal: number;
      medium: number;
      bold: number;
    };
  };
}
```

### Theme Presets
```typescript
const lightTheme: Theme = {
  mode: 'light',
  colors: {
    background: '#ffffff',
    backgroundDark: '#f5f5f5',
    text: '#1a1a1a',
    textSecondary: '#666666',
    primary: '#0066cc',
    primaryHover: '#0052a3',
    border: '#e0e0e0',
    error: '#dc2626',
    success: '#16a34a'
  },
  // ... other theme properties
};

const darkTheme: Theme = {
  mode: 'dark',
  colors: {
    background: '#1a1a1a',
    backgroundDark: '#262626',
    text: '#ffffff',
    textSecondary: '#a3a3a3',
    primary: '#3b82f6',
    primaryHover: '#2563eb',
    border: '#404040',
    error: '#ef4444',
    success: '#22c55e'
  },
  // ... other theme properties
};
```

## Modal System

### Modal Types
```typescript
interface Modal {
  id: string;
  title: string;
  content: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
  onClose?: () => void;
}

interface ModalState {
  isOpen: boolean;
  data?: any;
}
```

### Modal Components
```typescript
function ModalManager() {
  const { modals, activeModal, closeModal } = useUiStore();
  
  if (!activeModal) {
    return null;
  }
  
  const modal = modals[activeModal];
  
  return (
    <Dialog
      open={true}
      onClose={() => {
        modal.onClose?.();
        closeModal(modal.id);
      }}
      className={`modal-${modal.size || 'md'}`}
    >
      <Dialog.Title>{modal.title}</Dialog.Title>
      <Dialog.Content>{modal.content}</Dialog.Content>
    </Dialog>
  );
}
```

## Toast System

### Toast Types
```typescript
interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}
```

### Toast Components
```typescript
function ToastManager() {
  const { toasts, removeToast } = useUiStore();
  
  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`toast toast-${toast.type}`}
          onClick={() => removeToast(toast.id)}
        >
          {toast.message}
        </div>
      ))}
    </div>
  );
}
```

## Usage Examples

### Theme Usage
```typescript
function ThemeToggle() {
  const { isDarkMode, toggleTheme } = useUiStore();
  
  return (
    <button onClick={toggleTheme}>
      {isDarkMode ? 'Light Mode' : 'Dark Mode'}
    </button>
  );
}

function ThemedComponent() {
  const { theme } = useUiStore();
  
  return (
    <div
      style={{
        backgroundColor: theme.colors.background,
        color: theme.colors.text
      }}
    >
      Themed content
    </div>
  );
}
```

### Modal Usage
```typescript
function App() {
  const { openModal } = useUiStore();
  
  const handleOpenSettings = () => {
    openModal({
      id: 'settings',
      title: 'Settings',
      content: <SettingsForm />,
      size: 'lg'
    });
  };
  
  return (
    <>
      <button onClick={handleOpenSettings}>Open Settings</button>
      <ModalManager />
    </>
  );
}
```

### Toast Usage
```typescript
function ImportButton() {
  const { addToast } = useUiStore();
  
  const handleImport = async () => {
    try {
      await importChat();
      addToast({
        type: 'success',
        message: 'Chat imported successfully',
        duration: 3000
      });
    } catch (error) {
      addToast({
        type: 'error',
        message: 'Failed to import chat',
        duration: 5000
      });
    }
  };
  
  return <button onClick={handleImport}>Import Chat</button>;
}
```

## Store Persistence

### Persistence Configuration
```typescript
interface UiPersistConfig {
  key: string;
  whitelist: (keyof UiStore)[];
}

const persistUiStore = (config: UiPersistConfig) => {
  const stored = localStorage.getItem(config.key);
  if (stored) {
    const parsed = JSON.parse(stored);
    const filtered = config.whitelist.reduce((acc, key) => {
      if (key in parsed) {
        acc[key] = parsed[key];
      }
      return acc;
    }, {} as Partial<UiStore>);
    
    useUiStore.setState(filtered);
  }
  
  useUiStore.subscribe((state) => {
    const filtered = config.whitelist.reduce((acc, key) => {
      acc[key] = state[key];
      return acc;
    }, {} as Partial<UiStore>);
    
    localStorage.setItem(config.key, JSON.stringify(filtered));
  });
};
```

### Usage
```typescript
persistUiStore({
  key: 'voxstitch-ui',
  whitelist: ['isDarkMode', 'isSidebarOpen']
});
```

## Responsive Layout

### Breakpoint System
```typescript
const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px'
};

const useBreakpoint = () => {
  const [breakpoint, setBreakpoint] = useState('sm');
  
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      if (width >= 1280) setBreakpoint('xl');
      else if (width >= 1024) setBreakpoint('lg');
      else if (width >= 768) setBreakpoint('md');
      else setBreakpoint('sm');
    };
    
    window.addEventListener('resize', handleResize);
    handleResize();
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  return breakpoint;
};
```

### Responsive Layout Components
```typescript
function ResponsiveLayout() {
  const { isSidebarOpen } = useUiStore();
  const breakpoint = useBreakpoint();
  
  const showSidebar = breakpoint !== 'sm' || isSidebarOpen;
  
  return (
    <div className="layout">
      {showSidebar && <Sidebar />}
      <main className={showSidebar ? 'with-sidebar' : ''}>
        <Outlet />
      </main>
    </div>
  );
}
```
