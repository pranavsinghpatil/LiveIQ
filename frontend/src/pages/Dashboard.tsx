import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../utils/api';
import { ChatList } from '../components/chat/ChatList';
import { SearchBar } from '../components/chat/SearchBar';
import { ImportChat } from '../components/chat/ImportChat';
import type { ChatLog } from '../types';
import { Card } from '../components/ui/Card';

export const Dashboard = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);

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

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
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
