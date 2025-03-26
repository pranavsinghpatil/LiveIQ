import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../utils/api';
import { ChatList } from '../components/chat/ChatList';
import { SearchBar } from '../components/chat/SearchBar';
import { ImportChat } from '../components/chat/ImportChat';
import { Card } from '../components/ui/Card';
import { useAuthStore } from '../store/auth';

export const Dashboard = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);
  const { user } = useAuthStore();
  
  const isGuestUser = user?.role === 'guest';

  const { data: chats, isLoading, refetch } = useQuery({
    queryKey: ['chats', searchTerm, selectedPlatform],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (selectedPlatform) params.append('platform', selectedPlatform);
      
      const response = await api.get(`/chats?${params.toString()}`);
      return response.data;
    }
  });

  const handleChatClick = (chatId: string) => {
    navigate(`/chats/${chatId}`);
  };

  const handleImportComplete = () => {
    refetch();
  };

  const platforms = [
    { id: 'chatgpt', name: 'ChatGPT' },
    { id: 'gemini', name: 'Gemini' },
    { id: 'mistral', name: 'Mistral' },
  ];

  const handleLoginClick = () => {
    navigate('/');
    setTimeout(() => {
      const loginButton = document.querySelector('[data-testid="login-button"]') as HTMLButtonElement;
      if (loginButton) loginButton.click();
    }, 100);
  };

  const handleRegisterClick = () => {
    navigate('/');
    setTimeout(() => {
      const registerButton = document.querySelector('[data-testid="register-button"]') as HTMLButtonElement;
      if (registerButton) registerButton.click();
    }, 100);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {isGuestUser && (
        <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-300 px-4 py-3 rounded mb-6 flex justify-between items-center">
          <div>
            <p className="font-medium">You're using VoxStitch in guest mode</p>
            <p className="text-sm mt-1">Limited to 2 chat imports and 5 messages. Create an account for unlimited access.</p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleRegisterClick}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-md text-sm font-medium"
            >
              Sign Up
            </button>
            <button
              onClick={handleLoginClick}
              className="px-4 py-2 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium"
            >
              Log In
            </button>
          </div>
        </div>
      )}
      
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Your Chats</h1>
        <ImportChat onImportComplete={handleImportComplete} />
      </div>

      <Card className="mb-8">
        <SearchBar
          searchTerm={searchTerm}
          onSearch={setSearchTerm}
          onPlatformChange={setSelectedPlatform}
          selectedPlatform={selectedPlatform}
          platforms={platforms}
        />
      </Card>

      <ChatList chats={chats || []} onChatClick={handleChatClick} />
    </div>
  );
};
