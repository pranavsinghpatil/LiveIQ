import { format } from 'date-fns';
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

interface Chat {
  id: string;
  source: string;
  content: any;
  meta_data: any;
  created_at: string;
  tags: string[];
}

interface ChatListProps {
  chats: Chat[];
  onChatClick: (chatId: string) => void;
}

export const ChatList = ({ chats, onChatClick }: ChatListProps) => {
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

  const getSummary = (content: any) => {
    if (typeof content === 'string') {
      return content.slice(0, 100) + '...';
    }
    if (Array.isArray(content) && content.length > 0) {
      const firstMessage = content[0].content || content[0].message || '';
      return firstMessage.slice(0, 100) + '...';
    }
    return 'No preview available';
  };

  return (
    <div className="divide-y divide-gray-200">
      {chats.map((chat) => (
        <div
          key={chat.id}
          onClick={() => onChatClick(chat.id)}
          className="p-4 hover:bg-gray-50 cursor-pointer transition-colors duration-150"
        >
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 text-2xl">
              {getSourceIcon(chat.source)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-gray-900">
                  {chat.source}
                </p>
                <p className="text-sm text-gray-500">
                  {format(new Date(chat.created_at), 'MMM d, yyyy')}
                </p>
              </div>
              <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                {getSummary(chat.content)}
              </p>
              {chat.tags.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {chat.tags.map((tag) => (
                    <span
                      key={tag}
                      className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
