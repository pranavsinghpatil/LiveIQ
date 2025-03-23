import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { TagIcon, PencilIcon } from '@heroicons/react/24/outline';
import { api } from '../utils/api';

interface ChatMessage {
  role: string;
  content: string;
  timestamp?: string;
}

interface ChatLog {
  id: string;
  source: string;
  content: ChatMessage[];
  meta_data: any;
  created_at: string;
  tags: string[];
}

export const ChatView = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);
  const [newTag, setNewTag] = useState('');

  const { data: chat, isLoading } = useQuery<ChatLog>(
    ['chat', id],
    async () => {
      const response = await api.get(`/chats/${id}`);
      return response.data;
    }
  );

  const updateTagsMutation = useMutation(
    async ({ chatId, tags }: { chatId: string; tags: string[] }) => {
      const response = await api.patch(`/chats/${chatId}`, { tags });
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['chat', id]);
      },
    }
  );

  const handleAddTag = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTag.trim() || !chat) return;

    const updatedTags = [...chat.tags, newTag.trim()];
    updateTagsMutation.mutate({ chatId: chat.id, tags: updatedTags });
    setNewTag('');
  };

  const handleRemoveTag = (tagToRemove: string) => {
    if (!chat) return;

    const updatedTags = chat.tags.filter((tag) => tag !== tagToRemove);
    updateTagsMutation.mutate({ chatId: chat.id, tags: updatedTags });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading chat...</div>
      </div>
    );
  }

  if (!chat) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">Chat not found</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            Chat from {chat.source}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Created on {new Date(chat.created_at).toLocaleDateString()}
          </p>
        </div>
        <button
          onClick={() => setIsEditing(!isEditing)}
          className="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <PencilIcon className="h-4 w-4 mr-1.5" />
          {isEditing ? 'Done' : 'Edit'}
        </button>
      </div>

      <div className="bg-white shadow rounded-lg divide-y divide-gray-200">
        {/* Tags Section */}
        <div className="p-4">
          <div className="flex items-center space-x-2 mb-2">
            <TagIcon className="h-5 w-5 text-gray-400" />
            <h3 className="text-sm font-medium text-gray-900">Tags</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {chat.tags.map((tag) => (
              <span
                key={tag}
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 ${
                  isEditing ? 'pr-1' : ''
                }`}
              >
                {tag}
                {isEditing && (
                  <button
                    onClick={() => handleRemoveTag(tag)}
                    className="ml-1 text-blue-600 hover:text-blue-800"
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
                  placeholder="Add tag"
                  className="w-24 text-sm border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                />
              </form>
            )}
          </div>
        </div>

        {/* Chat Content */}
        <div className="p-4">
          <div className="space-y-4">
            {chat.content.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-3xl px-4 py-2 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-primary-100 text-primary-900'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <div className="text-sm whitespace-pre-wrap">
                    {message.content}
                  </div>
                  {message.timestamp && (
                    <div className="mt-1 text-xs text-gray-500">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Metadata Section */}
        {chat.meta_data && Object.keys(chat.meta_data).length > 0 && (
          <div className="p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Metadata</h3>
            <div className="bg-gray-50 rounded p-3">
              <pre className="text-xs text-gray-600 overflow-auto">
                {JSON.stringify(chat.meta_data, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
