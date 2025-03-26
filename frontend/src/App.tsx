import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainLayout } from './layouts/MainLayout';
import { PrivateRoute } from './components/auth/PrivateRoute';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { ChatView } from './pages/ChatView';
import { Home } from './pages/Home';

// Create a client
const queryClient = new QueryClient();

function App() {
  const location = useLocation();

  // Initialize dark mode based on user preference
  useEffect(() => {
    // Check if user has a saved preference
    const savedTheme = localStorage.getItem('theme');
    
    // Check for saved theme or system preference
    if (savedTheme === 'dark' || 
        (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    // Set page title to reflect VoxStitch branding
    document.title = 'VoxStitch | AI Chat Aggregator';
  }, []);

  // Reset scroll position when navigating
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-light-100 dark:bg-dark-200 text-gray-900 dark:text-gray-100 transition-colors duration-200">
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected routes */}
          <Route element={<MainLayout />}>
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/chats/:id"
              element={
                <PrivateRoute>
                  <ChatView />
                </PrivateRoute>
              }
            />
          </Route>
        </Routes>
      </div>
    </QueryClientProvider>
  );
}

export default App;
