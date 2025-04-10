// src/routes/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { token, isGuest } = useAuthStore();

  if (!token && !isGuest) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
