import { Link, useNavigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const Home = () => {
  const navigate = useNavigate();
  const { isGuest, guestUsage, token } = useAuthStore();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <nav className="flex justify-end mb-8">
          <Link 
            to="/login"
            className="px-6 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            Login
          </Link>
        </nav>
        
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 dark:text-white mb-6">
            Welcome to VoxStitch
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-12">
            Your unified hub for AI conversations across ChatGPT, Mistral, and Gemini.
            Import, organize, and analyze your chat history with ease.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="px-8 py-3 text-base font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              Get Started
            </Link>
            <Link
              to="/login?guest=true"
              className="px-8 py-3 text-base font-medium text-primary-700 bg-primary-100 rounded-lg hover:bg-primary-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              Try as Guest
            </Link>
          </div>
          
          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Multi-Platform Support
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Import chats from ChatGPT, Mistral, and Gemini in various formats.
              </p>
            </div>
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Smart Organization
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Automatically categorize and tag your conversations for easy access.
              </p>
            </div>
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Advanced Search
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Find any conversation with our powerful search and filtering system.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      {isGuest && (
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4">Welcome to VoxStitch</h1>
            <p className="text-xl text-text/60">Your AI Chat Aggregator</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">Import Chats</h2>
              <p className="text-text/60 mb-4">
                Import your chat logs from various AI platforms like ChatGPT, Mistral, and Gemini.
              </p>
              {isGuest && (
                <p className="text-sm text-primary mb-2">
                  {2 - guestUsage.chatImports} chat imports remaining in guest mode
                </p>
              )}
            </Card>

            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">Organize & Search</h2>
              <p className="text-text/60 mb-4">
                Keep your AI conversations organized and easily searchable.
              </p>
            </Card>

            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">Interactive Chat</h2>
              <p className="text-text/60 mb-4">
                Continue your conversations with AI assistants.
              </p>
              {isGuest && (
                <p className="text-sm text-primary mb-2">
                  {5 - guestUsage.messages} messages remaining in guest mode
                </p>
              )}
            </Card>
          </div>

          <div className="text-center">
            <Card className="p-6 max-w-2xl mx-auto">
              <h2 className="text-xl font-semibold mb-4">You're in Guest Mode</h2>
              <p className="text-text/60 mb-6">
                Create an account to unlock unlimited chat imports, messages, and more features.
              </p>
              <div className="flex justify-center space-x-4">
                <Button onClick={() => navigate('/register')}>Create Account</Button>
                <Button onClick={() => navigate('/login')} variant="outline">Sign In</Button>
              </div>
            </Card>
          </div>

          <div className="mt-12">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold mb-4">Get Started</h2>
              <div className="flex justify-center space-x-4">
                <Button onClick={() => navigate('/dashboard')}>Go to Dashboard</Button>
                {!token && !isGuest && (
                  <>
                    <Button onClick={() => navigate('/register')} variant="outline">Create Account</Button>
                    <Button onClick={() => navigate('/login')} variant="outline">Sign In</Button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
