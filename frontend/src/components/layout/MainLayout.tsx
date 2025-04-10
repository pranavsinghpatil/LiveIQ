// src/layouts/MainLayout.tsx
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { Button } from '../ui/Button';
import useAuthStore from '../../stores/authStore';

export function MainLayout() {
  const navigate = useNavigate();
  const { token, isGuest, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link to="/" className="text-2xl font-bold text-primary">
              VoxStitch
            </Link>

            <nav className="flex items-center gap-4">
              {token || isGuest ? (
                <>
                  <Link to="/dashboard" className="text-text/60 hover:text-text">
                    Dashboard
                  </Link>
                  {isGuest ? (
                    <Button onClick={() => navigate('/register')} variant="outline">
                      Create Account
                    </Button>
                  ) : (
                    <Button onClick={handleLogout} variant="outline">
                      Sign Out
                    </Button>
                  )}
                </>
              ) : (
                <>
                  <Button onClick={() => navigate('/register')} variant="outline">
                    Sign Up
                  </Button>
                  <Button onClick={() => navigate('/login')}>Sign In</Button>
                </>
              )}
            </nav>
          </div>
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4">
        <Outlet />
      </main>

      <footer className="bg-white dark:bg-gray-800 shadow mt-8">
        <div className="container mx-auto px-4 py-4">
          <div className="text-center text-text/60">
            <p> 2025 VoxStitch. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
