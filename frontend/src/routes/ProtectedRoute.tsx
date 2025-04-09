// src/routes/ProtectedRoute.tsx
import { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';

interface ProtectedRouteProps {
  children: ReactNode;
  requireAuth?: boolean;
}

export default function ProtectedRoute({ children, requireAuth = false }: ProtectedRouteProps) {
  const { token, isGuest } = useAuthStore();

  // If the route requires auth and user is not authenticated, redirect to login
  if (requireAuth && !token && !isGuest) {
    return <Navigate to="/login" />;
  }

  // If user is not authenticated and not a guest, automatically make them a guest
  if (!token && !isGuest) {
    useAuthStore.getState().setIsGuest(true);
  }

  return <>{children}</>;
}
