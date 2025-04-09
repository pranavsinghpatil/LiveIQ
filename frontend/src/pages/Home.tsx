import { useNavigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export function Home() {
  const navigate = useNavigate();
  const { isGuest, guestUsage, token } = useAuthStore();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
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

        {isGuest && (
          <div className="mb-12">
            <Card className="p-6 max-w-2xl mx-auto">
              <h2 className="text-xl font-semibold mb-4">You're in Guest Mode</h2>
              <p className="text-text/60 mb-6">
                Create an account to unlock unlimited chat imports, messages, and more features:
                <ul className="list-disc list-inside mt-2">
                  <li>Unlimited chat imports</li>
                  <li>Unlimited messages</li>
                  <li>Advanced search and filtering</li>
                  <li>Custom tags and organization</li>
                  <li>Export and backup features</li>
                </ul>
              </p>
              <div className="flex flex-col sm:flex-row justify-center gap-4">
                <Button onClick={() => navigate('/register')} className="w-full sm:w-auto">
                  Create Account
                </Button>
                <Button onClick={() => navigate('/login')} variant="outline" className="w-full sm:w-auto">
                  Sign In
                </Button>
              </div>
            </Card>
          </div>
        )}

        <div className="text-center">
          <div className="mb-8">
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Button onClick={() => navigate('/dashboard')} className="w-full sm:w-auto">
                Go to Dashboard
              </Button>
              {!token && !isGuest && (
                <>
                  <Button onClick={() => navigate('/register')} variant="outline" className="w-full sm:w-auto">
                    Create Account
                  </Button>
                  <Button onClick={() => navigate('/login')} variant="outline" className="w-full sm:w-auto">
                    Sign In
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
