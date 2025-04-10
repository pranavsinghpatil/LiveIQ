// src/pages/dashboard.tsx
// new
// src/pages/dashboard.tsx
import { useQuery } from '@tanstack/react-query';
import { chatAPI, type Chat } from '../utils/api';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import useAuthStore from '../stores/authStore';

export function Dashboard() {
  const { isGuest, guestUsage } = useAuthStore();
  const { data: chats = [], isLoading, error } = useQuery({
    queryKey: ['chats'],
    queryFn: chatAPI.getChats,
  });

  if (isLoading) {
    return (
      <div className="p-4">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="space-y-3">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <Card className="p-4 text-red-500">
          Failed to load chats. Please try again later.
        </Card>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Your Chats</h1>
        <Button>Import Chat</Button>
      </div>

      {isGuest && (
        <Card className="p-4 bg-primary/5 border-primary/20">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="font-semibold">Guest Mode Limits</h2>
              <p className="text-sm text-text/60">
                Chat Imports: {guestUsage.chatImports}/2 • Messages: {guestUsage.messages}/5
              </p>
            </div>
            <Button variant="outline">Upgrade Now</Button>
          </div>
        </Card>
      )}

      {chats.length === 0 ? (
        <Card className="p-8 text-center">
          <h3 className="text-xl font-semibold mb-2">No chats yet</h3>
          <p className="text-text/60 mb-4">
            Import your first chat to get started
          </p>
          <Button>Import Chat</Button>
        </Card>
      ) : (
        <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {chats.map((chat: Chat) => (
            <Card key={chat.id} className="p-4">
              <h3 className="font-semibold">{chat.title}</h3>
              <p className="text-sm text-text/60 mb-2">{chat.description}</p>
              <div className="flex justify-between items-center text-xs text-text/40">
                <span>{chat.platform}</span>
                <span>{new Date(chat.created_at).toLocaleDateString()}</span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
