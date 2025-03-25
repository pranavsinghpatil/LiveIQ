import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { PencilIcon, ChatBubbleLeftIcon, VideoCameraIcon } from '@heroicons/react/24/outline';
import { api } from '../utils/api';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

interface ChatMessage {
  role: string;
  content: string;
  timestamp?: string;
  platform?: string;
}

interface ChatLog {
  id: string;
  source: string;
  content: ChatMessage[];
  meta_data: {
    platform: string;
    type: string;
    title?: string;
    summary?: string;
    participants?: string[];
  };
  created_at: string;
  tags: string[];
}

type UpdateTagsInput = {
  chatId: string;
  tags: string[];
};

type SendMessageInput = {
  content: string;
  platform: string;
};

export const ChatView = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);
  const [newTag, setNewTag] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState<string>('auto');

  // Fetch chat data
  const { data: chat, isLoading } = useQuery<ChatLog>({
    queryKey: ['chat', id],
    queryFn: async () => {
      const response = await api.get<ChatLog>(`/chats/${id}`);
      return response.data;
    },
    enabled: !!id,
  });

  // Fetch related chats
  const { data: relatedChats } = useQuery<ChatLog[]>({
    queryKey: ['related-chats', id],
    queryFn: async () => {
      const response = await api.get<ChatLog[]>(`/chats/${id}/related`);
      return response.data;
    },
    enabled: !!id,
  });

  // Update tags mutation
  const updateTagsMutation = useMutation<ChatLog, Error, UpdateTagsInput>({
    mutationFn: async ({ chatId, tags }) => {
      const response = await api.patch<ChatLog>(`/chats/${chatId}`, { tags });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat', id] });
    },
  });

  // Send message mutation
  const sendMessageMutation = useMutation<ChatLog, Error, SendMessageInput>({
    mutationFn: async ({ content, platform }) => {
      const response = await api.post<ChatLog>(`/chats/${id}/messages`, {
        content,
        platform,
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat', id] });
    },
  });

  const handleAddTag = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTag.trim() || !chat) return;

    const newTags = [...chat.tags, newTag.trim()];
    updateTagsMutation.mutate({ chatId: chat.id, tags: newTags });
    setNewTag('');
  };

  const handleRemoveTag = (tagToRemove: string) => {
    if (!chat) return;

    const newTags = chat.tags.filter((tag) => tag !== tagToRemove);
    updateTagsMutation.mutate({ chatId: chat.id, tags: newTags });
  };

  const renderMessage = (message: ChatMessage, index: number) => {
    const isUser = message.role === 'user';
    return (
      <div
        key={index}
        className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div
          className={`max-w-[70%] rounded-lg p-4 ${
            isUser
              ? 'bg-primary-100 text-primary-900'
              : 'bg-gray-100 text-gray-900'
          }`}
        >
          {message.platform && (
            <div className="text-xs text-gray-500 mb-1">
              via {message.platform}
            </div>
          )}
          <div className="whitespace-pre-wrap">{message.content}</div>
          {message.timestamp && (
            <div className="text-xs text-gray-500 mt-1">
              {new Date(message.timestamp).toLocaleString()}
            </div>
          )}
        </div>
      </div>
    );
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!chat) {
    return <div>Chat not found</div>;
  }

  const isPodcast = chat.meta_data.type === 'video' || chat.meta_data.type === 'podcast';

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Main Chat Area */}
        <div className="md:col-span-2">
          <Card className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-2xl font-bold">
                {chat.meta_data.title || `Chat from ${chat.meta_data.platform}`}
              </h1>
              <div className="flex space-x-2">
                <Button
                  variant="outline"
                  onClick={() => setIsEditing(!isEditing)}
                >
                  <PencilIcon className="h-5 w-5" />
                </Button>
              </div>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mb-4">
              {chat.tags.map((tag: string) => (
                <span
                  key={tag}
                  className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                >
                  {tag}
                  {isEditing && (
                    <button
                      onClick={() => handleRemoveTag(tag)}
                      className="ml-1 text-primary-600 hover:text-primary-800"
                    >
                      ×
                    </button>
                  )}
                </span>
              ))}
              {isEditing && (
                <form onSubmit={handleAddTag} className="inline-flex">
                  <input
                    type="text"
                    value={newTag}
                    onChange={(e) => setNewTag(e.target.value)}
                    className="text-sm border-gray-300 rounded-md"
                    placeholder="Add tag"
                  />
                  <Button type="submit" className="ml-2">
                    Add
                  </Button>
                </form>
              )}
            </div>

            {/* Chat Messages */}
            <div className="space-y-4">
              {chat.content.map((message, index) => renderMessage(message, index))}
            </div>

            {/* Message Input */}
            <div className="mt-6">
              <div className="flex items-center space-x-4 mb-4">
                <select
                  value={selectedPlatform}
                  onChange={(e) => setSelectedPlatform(e.target.value)}
                  className="rounded-md border-gray-300"
                >
                  <option value="auto">Auto (Same as source)</option>
                  <option value="chatgpt">ChatGPT</option>
                  <option value="mistral">Mistral AI</option>
                  <option value="gemini">Google Gemini</option>
                </select>
              </div>
              <div className="flex space-x-4">
                <input
                  type="text"
                  placeholder="Type your message..."
                  className="flex-1 rounded-md border-gray-300"
                  onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => {
                    if (e.key === 'Enter') {
                      const content = e.currentTarget.value;
                      if (content.trim()) {
                        sendMessageMutation.mutate({
                          content,
                          platform: selectedPlatform === 'auto' ? chat.meta_data.platform : selectedPlatform,
                        });
                        e.currentTarget.value = '';
                      }
                    }
                  }}
                />
                <Button>Send</Button>
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="md:col-span-1">
          {/* Meta Information */}
          <Card className="mb-6">
            <h2 className="text-lg font-semibold mb-4">Details</h2>
            <dl className="space-y-2">
              <dt className="text-sm font-medium text-gray-500">Platform</dt>
              <dd className="text-sm text-gray-900">{chat.meta_data.platform}</dd>
              <dt className="text-sm font-medium text-gray-500">Type</dt>
              <dd className="text-sm text-gray-900">{chat.meta_data.type}</dd>
              {isPodcast && chat.meta_data.participants && (
                <>
                  <dt className="text-sm font-medium text-gray-500">
                    Participants
                  </dt>
                  <dd className="text-sm text-gray-900">
                    {chat.meta_data.participants.join(', ')}
                  </dd>
                </>
              )}
              <dt className="text-sm font-medium text-gray-500">Created</dt>
              <dd className="text-sm text-gray-900">
                {new Date(chat.created_at).toLocaleString()}
              </dd>
            </dl>
          </Card>

          {/* Related Chats */}
          {relatedChats && relatedChats.length > 0 && (
            <Card>
              <h2 className="text-lg font-semibold mb-4">Related Chats</h2>
              <div className="space-y-4">
                {relatedChats.map((relatedChat: ChatLog) => (
                  <button
                    key={relatedChat.id}
                    onClick={() => navigate(`/chat/${relatedChat.id}`)}
                    className="block w-full text-left p-4 rounded-lg hover:bg-gray-50"
                  >
                    <div className="flex items-center">
                      {relatedChat.meta_data.type === 'video' ? (
                        <VideoCameraIcon className="h-5 w-5 text-gray-400 mr-2" />
                      ) : (
                        <ChatBubbleLeftIcon className="h-5 w-5 text-gray-400 mr-2" />
                      )}
                      <div>
                        <div className="font-medium">
                          {relatedChat.meta_data.title ||
                            `Chat from ${relatedChat.meta_data.platform}`}
                        </div>
                        <div className="text-sm text-gray-500">
                          {new Date(relatedChat.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
