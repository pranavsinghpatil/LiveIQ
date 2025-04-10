// src/pages/NotFound.tsx
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';

export function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="text-center">
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <p className="text-xl text-text/60 mb-8">Page not found</p>
        <Button onClick={() => navigate('/')}>Go Home</Button>
      </div>
    </div>
  );
}
