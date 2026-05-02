import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './lib/auth';
import { Sidebar } from './components/Sidebar';
import { ToastContainer } from './components/Toast';
import AuthPage from './pages/Auth';
import EventBrowser from './pages/EventBrowser';
import LiveEventView from './pages/LiveEvent';
import AIAnalysis from './pages/AIAnalysis';
import PredictionBoard from './pages/PredictionBoard';
import AlertManager from './pages/AlertManager';
import PostEventReport from './pages/PostEventReport';
import AdminDashboard from './pages/AdminDashboard';

function PrivateLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">{children}</main>
    </div>
  );
}

function RequireAuth({ children }: { children: React.ReactElement }) {
  const { token } = useAuthStore();
  return token ? children : <Navigate to="/auth" replace />;
}

import { Sun, Moon } from 'lucide-react';
import { useState, useEffect } from 'react';

function ThemeToggle() {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <div 
      className="theme-toggle" 
      onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}
      title="Toggle Theme"
    >
      {theme === 'dark' ? <Sun size={24} /> : <Moon size={24} />}
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <ToastContainer />
      <ThemeToggle />
      <Routes>
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/" element={<Navigate to="/events" replace />} />
        <Route path="/events" element={<RequireAuth><PrivateLayout><EventBrowser /></PrivateLayout></RequireAuth>} />
        <Route path="/live" element={<RequireAuth><PrivateLayout><LiveEventView /></PrivateLayout></RequireAuth>} />
        <Route path="/analysis" element={<RequireAuth><PrivateLayout><AIAnalysis /></PrivateLayout></RequireAuth>} />
        <Route path="/predictions" element={<RequireAuth><PrivateLayout><PredictionBoard /></PrivateLayout></RequireAuth>} />
        <Route path="/alerts" element={<RequireAuth><PrivateLayout><AlertManager /></PrivateLayout></RequireAuth>} />
        <Route path="/reports" element={<RequireAuth><PrivateLayout><PostEventReport /></PrivateLayout></RequireAuth>} />
        <Route path="/admin" element={<RequireAuth><PrivateLayout><AdminDashboard /></PrivateLayout></RequireAuth>} />
      </Routes>
    </BrowserRouter>
  );
}
