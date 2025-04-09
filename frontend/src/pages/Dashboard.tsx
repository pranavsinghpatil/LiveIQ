// src/pages/dashboard.tsx
// new
// src/pages/dashboard.tsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/ui/Card';

interface Chat {
  id: number;
  title: string;
  platform: string;
  created_at: string;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [chats, setChats] = useState<Chat[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/api/chats', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch chats');
        }

        const data = await response.json();
        setChats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchChats();
  }, []);

  if (isLoading) {
    return (
      <div className="container mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-text mb-8">Loading...</h1>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-text mb-4">Error</h1>
        <p className="text-text/60">{error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-text">Your Chats</h1>
        <button
          className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors"
          onClick={() => navigate('/chat/new')}
        >
          Import Chat
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {chats.length === 0 ? (
          <Card className="p-6 text-center">
            <h3 className="text-lg font-medium text-text mb-2">No chats yet</h3>
            <p className="text-text/60 mb-4">Import your first chat to get started</p>
            <button
              className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors"
              onClick={() => navigate('/chat/new')}
            >
              Import Chat
            </button>
          </Card>
        ) : (
          chats.map((chat) => (
            <Card key={chat.id} className="p-6">
              <h3 className="text-lg font-medium text-text mb-2">{chat.title}</h3>
              <p className="text-text/60 mb-4">Platform: {chat.platform}</p>
              <div className="flex justify-between items-center">
                <span className="text-sm text-text/40">
                  {new Date(chat.created_at).toLocaleDateString()}
                </span>
                <button
                  className="px-3 py-1 text-sm bg-primary text-white rounded-md hover:bg-primary-dark transition-colors"
                  onClick={() => navigate(`/chat/${chat.id}`)}
                >
                  View
                </button>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
