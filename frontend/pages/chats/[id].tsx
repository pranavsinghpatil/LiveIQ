import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import api from '../../services/api';
import { useAuthStore } from '../../store/auth';

const ChatPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const { token } = useAuthStore();

  useEffect(() => {
    if (!token) {
      router.replace('/');
      return;
    }
    if (!id) return;
    setLoading(true);
    api.get(`/api/chats/message/${id}`)
      .then((res: any) => setMessages(res.data))
      .finally(() => setLoading(false));
  }, [id, token, router]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setLoading(true);
    await api.post('/api/chats/send_message', { chat_id: id, content: input });
    setInput('');
    // Re-fetch messages
    api.get(`/api/chats/message/${id}`)
      .then((res: any) => setMessages(res.data))
      .finally(() => setLoading(false));
  };

  return (
    <div className="max-w-2xl mx-auto py-8">
      <h1 className="text-2xl font-bold mb-4">Chat</h1>
      <div className="bg-background-dark rounded-lg p-4 mb-4 min-h-[200px]">
        {loading ? (
          <div>Loading messages...</div>
        ) : (
          <ul>
            {messages.map((msg, idx) => (
              <li key={idx} className="mb-2">
                <span className="font-bold">{msg.sender}: </span>{msg.content}
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          className="flex-1 border border-primary/30 rounded px-3 py-2"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button
          className="bg-primary text-white rounded px-4 py-2"
          onClick={sendMessage}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatPage;
