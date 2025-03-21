import { useState } from 'react';
import { useQuery } from 'react-query';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import { ChatList } from '../components/chat/ChatList';
import { SearchBar } from '../components/chat/SearchBar';
import { ImportChat } from '../components/chat/ImportChat';

interface ChatMessage {
  role: string;
  content: string;
  timestamp?: string;
}

interface ChatLog {
  id: string;
  source: string;
  content: ChatMessage[];
  meta_data: {
    platform: string;
    model?: string;
    summary?: string;
  };
  created_at: string;
  tags: string[];
}

export const Dashboard = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);

  const { data: chats, isLoading, error } = useQuery<ChatLog[]>(
    ['chats', searchTerm, selectedPlatform],
    async () => {
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (selectedPlatform) params.append('platform', selectedPlatform);
      
      const response = await api.get(`/chats?${params.toString()}`);
      return response.data;
    }
  );

  const handleChatClick = (chatId: string) => {
    navigate(`/chats/${chatId}`);
  };

  const platforms = [
    { id: 'chatgpt', name: 'ChatGPT' },
    { id: 'gemini', name: 'Gemini' },
    { id: 'mistral', name: 'Mistral' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">AI Chat Dashboard</h1>
            <p className="mt-1 text-sm text-gray-500">
              Manage and analyze your conversations across multiple AI platforms
            </p>
          </div>
          <ImportChat />
        </div>

        <div className="bg-white shadow rounded-lg">
          <div className="p-4 border-b border-gray-200">
            <SearchBar
              value={searchTerm}
              onChange={(value) => setSearchTerm(value)}
              onPlatformChange={setSelectedPlatform}
              platforms={platforms}
            />
          </div>

          {error ? (
            <div className="p-4 text-red-600">Failed to load chats. Please try again.</div>
          ) : isLoading ? (
            <div className="p-4 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            </div>
          ) : !chats?.length ? (
            <div className="p-8 text-center text-gray-500">
              <p className="text-lg">No chats found</p>
              <p className="mt-1 text-sm">Import your first chat to get started</p>
            </div>
          ) : (
            <ChatList chats={chats} onChatClick={handleChatClick} />
          )}
        </div>
      </div>
    </div>
  );
};
