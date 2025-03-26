import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth';
import { Button } from '../ui/Button';
import { UserIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';

export const Header = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="flex items-center justify-between px-6 py-4 bg-background border-b border-primary/20">
      <div className="flex items-center space-x-4">
        <h1 className="text-2xl font-bold text-text">VoxStitch</h1>
      </div>

      <div className="flex items-center space-x-4">
        <Button
          variant="ghost"
          onClick={() => navigate('/settings')}
          className="p-2 hover:bg-primary/10"
        >
          <Cog6ToothIcon className="h-5 w-5 text-text" />
        </Button>
        
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            onClick={() => navigate('/profile')}
            className="flex items-center space-x-2 hover:bg-primary/10"
          >
            <UserIcon className="h-5 w-5 text-text" />
            <span className="text-text">{user?.username || 'Guest'}</span>
          </Button>
          <Button
            variant="outline"
            onClick={handleLogout}
            className="text-text border-primary/30 hover:bg-primary/10"
          >
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
};
