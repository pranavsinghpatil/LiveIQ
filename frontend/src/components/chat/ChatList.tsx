import { format } from 'date-fns';
import { Card } from '../ui/Card';
import type { ChatLog } from '../../types';
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

interface ChatListProps {
  chats: ChatLog[];
  onChatClick: (chatId: string) => void;
}

export const ChatList = ({ chats, onChatClick }: ChatListProps) => {
  if (!chats.length) {
    return (
      <Card className="p-8 text-center text-gray-500">
        <p className="text-lg">No chats found</p>
        <p className="mt-1 text-sm">Import your first chat to get started</p>
      </Card>
    );
  }

  const getSourceIcon = (source: string) => {
    switch (source.toLowerCase()) {
      case 'chatgpt':
        return '🤖';
      case 'mistral':
        return '🌟';
      case 'gemini':
        return '♊';
      default:
        return <ChatBubbleLeftRightIcon className="h-5 w-5" />;
    }
  };

  const getSummary = (messages: any[]) => {
    if (messages.length > 0) {
      const firstMessage = messages[0].content || '';
      return firstMessage.slice(0, 100) + '...';
    }
    return 'No preview available';
  };

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      {chats.map((chat) => (
        <Card
          key={chat.id}
          className="cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => onChatClick(chat.id)}
        >
          <div className="p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold">{chat.title}</h3>
              <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                {getSourceIcon(chat.platform)}
              </span>
            </div>
            <div className="text-sm text-gray-500">
              {format(new Date(chat.createdAt), 'MMM d, yyyy')}
            </div>
            <p className="mt-1 text-sm text-gray-500 line-clamp-2">
              {getSummary(chat.messages)}
            </p>
            {chat.tags && chat.tags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {chat.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </Card>
      ))}
    </div>
  );
};
