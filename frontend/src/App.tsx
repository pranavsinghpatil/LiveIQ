import { Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ProtectedRoute from "./routes/ProtectedRoute";
import { Login } from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";
import { Home } from './pages/Home';
import { Register } from './pages/RegisterPage';
import { ChatView } from './pages/ChatView';
import { MainLayout } from './layouts/MainLayout';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-light-100 dark:bg-dark-200 text-gray-900 dark:text-gray-100 transition-colors duration-200">
        <Routes>
          {/* Public routes */}
          <Route path="/" element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          } />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected routes that require authentication */}
          <Route element={<MainLayout />}>
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/chat/:id" element={
              <ProtectedRoute requireAuth>
                <ChatView />
              </ProtectedRoute>
            } />
          </Route>

          {/* 404 route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </QueryClientProvider>
  );
}
