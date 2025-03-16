# Frontend Development Guide

*Last Updated: 2025-03-17*

## Frontend Overview

The ChatSynth frontend is built using React with TypeScript, utilizing Vite as the build tool. This guide covers the application structure, key components, and development practices.

## Project Structure
```
frontend/
├── src/
│   ├── components/         # React components
│   │   ├── auth/          # Authentication components
│   │   ├── chat/          # Chat interface components
│   │   ├── common/        # Reusable components
│   │   └── layout/        # Layout components
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API integration
│   ├── store/             # Redux state management
│   ├── styles/            # Global styles
│   ├── types/             # TypeScript types
│   └── utils/             # Helper functions
```

## Key Components

### 1. Authentication Components
Location: `src/components/auth/`

#### Login Form
```typescript
// src/components/auth/LoginForm.tsx
import { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';

export const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

### 2. Chat Interface
Location: `src/components/chat/`

#### Chat List
```typescript
// src/components/chat/ChatList.tsx
import { useChats } from '@/hooks/useChats';

export const ChatList: React.FC = () => {
  const { chats, loading } = useChats();

  if (loading) return <Spinner />;

  return (
    <div className="chat-list">
      {chats.map(chat => (
        <ChatItem key={chat.id} chat={chat} />
      ))}
    </div>
  );
};
```

## Custom Hooks

### 1. Authentication Hook
```typescript
// src/hooks/useAuth.ts
import { useDispatch } from 'react-redux';
import { login as loginAction } from '@/store/authSlice';

export const useAuth = () => {
  const dispatch = useDispatch();

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login(email, password);
      dispatch(loginAction(response.data));
    } catch (error) {
      handleError(error);
    }
  };

  return { login };
};
```

### 2. Chat Hook
```typescript
// src/hooks/useChats.ts
import { useState, useEffect } from 'react';
import { chatService } from '@/services/chat';

export const useChats = () => {
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChats();
  }, []);

  const fetchChats = async () => {
    try {
      const response = await chatService.getChats();
      setChats(response.data);
    } finally {
      setLoading(false);
    }
  };

  return { chats, loading, fetchChats };
};
```

## State Management

### 1. Redux Store Configuration
```typescript
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import chatReducer from './chatSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    chat: chatReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 2. Auth Slice
```typescript
// src/store/authSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  user: User | null;
  token: string | null;
}

const initialState: AuthState = {
  user: null,
  token: null,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action: PayloadAction<LoginResponse>) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
    },
  },
});
```

## API Integration

### 1. API Service Setup
```typescript
// src/services/api.ts
import axios from 'axios';
import { store } from '@/store';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
  const token = store.getState().auth.token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 2. Chat Service
```typescript
// src/services/chat.ts
import api from './api';

export const chatService = {
  getChats: () => api.get('/chats'),
  getChatById: (id: number) => api.get(`/chats/${id}`),
  importChat: (data: ChatImport) => api.post('/chats/import', data),
};
```

## Routing

### Route Configuration
```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { PrivateRoute } from './components/common/PrivateRoute';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <DashboardPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};
```

## Styling

### 1. Material-UI Theme
```typescript
// src/styles/theme.ts
import { createTheme } from '@mui/material';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});
```

### 2. Global Styles
```typescript
// src/styles/global.ts
import { css } from '@emotion/react';

export const globalStyles = css`
  body {
    margin: 0;
    font-family: 'Roboto', sans-serif;
  }
`;
```

## Error Handling

### Error Boundary
```typescript
// src/components/common/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return <h1>Sorry.. there was an error</h1>;
    }

    return this.props.children;
  }
}
```

## Testing

### Component Testing
```typescript
// src/components/auth/LoginForm.test.tsx
import { render, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('submits the form with email and password', async () => {
    const { getByLabelText, getByRole } = render(<LoginForm />);
    
    fireEvent.change(getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    });
    
    fireEvent.change(getByLabelText(/password/i), {
      target: { value: 'password123' },
    });
    
    fireEvent.click(getByRole('button', { name: /login/i }));
    
    await waitFor(() => {
      // Assert form submission
    });
  });
});
```

## Performance Optimization

### 1. Code Splitting
```typescript
// src/pages/index.ts
import { lazy } from 'react';

export const DashboardPage = lazy(() => import('./DashboardPage'));
export const ChatPage = lazy(() => import('./ChatPage'));
```

### 2. Memoization
```typescript
// src/components/chat/ChatItem.tsx
import { memo } from 'react';

export const ChatItem = memo<ChatItemProps>(({ chat }) => {
  return (
    <div className="chat-item">
      {/* Chat item content */}
    </div>
  );
});
```

## Development Workflow

1. Start the development server:
```bash
npm run dev
```

2. Build for production:
```bash
npm run build
```

3. Run tests:
```bash
npm test
```

## Common Issues & Solutions

### 1. State Management
- Use Redux for global state
- Use local state for component-specific data
- Implement proper loading and error states

### 2. Performance
- Implement lazy loading for routes
- Use React.memo for expensive components
- Optimize re-renders with useMemo and useCallback

### 3. Type Safety
- Define proper TypeScript interfaces
- Use strict type checking
- Implement proper error boundaries

## Next Steps
1. Review the [Development Workflow](./07_development_workflow.md)
2. Set up your local development environment
3. Try building a simple feature
