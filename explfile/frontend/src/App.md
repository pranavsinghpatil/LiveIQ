# App.tsx

## Purpose
The root component of the VoxStitch application that sets up the main routing structure, global providers, and application-wide configuration.

## Key Features

### Router Setup
- Implements React Router for navigation
- Defines protected and public routes
- Handles route-based code splitting for better performance

### Global Providers
1. **QueryClientProvider**
   - Configures React Query for API data management
   - Sets up global query cache settings
   - Handles API request retries and error boundaries

2. **ThemeProvider**
   - Manages application-wide theme settings
   - Handles dark/light mode preferences
   - Provides theme context to all components

3. **AuthProvider**
   - Manages authentication state
   - Handles token persistence
   - Provides user context globally

### Route Structure
```typescript
<BrowserRouter>
  <Routes>
    {/* Public Routes */}
    <Route path="/" element={<Home />} />
    <Route path="/login" element={<Login />} />
    <Route path="/register" element={<Register />} />
    
    {/* Protected Routes */}
    <Route element={<PrivateRoute />}>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/chats/:id" element={<ChatView />} />
    </Route>
  </Routes>
</BrowserRouter>
```

### Error Boundaries
- Implements React Error Boundary for graceful error handling
- Provides fallback UI for runtime errors
- Logs errors to monitoring service

### Performance Optimizations
- Implements React.lazy for code splitting
- Uses Suspense boundaries for loading states
- Configures service worker for PWA support

## Integration Points

### API Configuration
- Sets up axios interceptors
- Configures base URL and headers
- Handles authentication token injection

### State Management
- Initializes Zustand stores
- Sets up persistence configuration
- Handles hydration of initial state

### Theme System
- Loads user theme preferences
- Sets up system theme detection
- Provides theme switching functionality

## Related Components

### Direct Children
- `MainLayout`: Main application layout wrapper
- `PrivateRoute`: Authentication guard component
- `ErrorBoundary`: Global error handler

### Key Dependencies
- React Router for navigation
- React Query for data fetching
- Zustand for state management
- Tailwind CSS for styling

## Recent Updates
- Added gradient-based theme system
- Improved error handling
- Enhanced authentication flow
- Added performance monitoring
- Updated routing structure for new features

## Code Structure
```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/theme';
import { ErrorBoundary } from './components/ErrorBoundary';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
});

export const App = () => {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <BrowserRouter>
            <Routes>
              {/* Route definitions */}
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
};
```

## Testing
- Unit tests for routing logic
- Integration tests for provider setup
- E2E tests for main user flows

## Security Considerations
- Protected route implementation
- Authentication state management
- Token handling and storage
- XSS prevention measures
