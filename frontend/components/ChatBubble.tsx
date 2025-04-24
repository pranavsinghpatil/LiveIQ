import React from 'react';

interface ChatBubbleProps {
  message: string;
  sender: 'user' | 'ai';
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message, sender }) => (
  <div
    className={`max-w-xs px-4 py-2 rounded-lg shadow mb-2 text-sm ${
      sender === 'user'
        ? 'bg-primary text-white ml-auto'
        : 'bg-background-dark text-text mr-auto'
    }`}
  >
    {message}
  </div>
);

export default ChatBubble;
