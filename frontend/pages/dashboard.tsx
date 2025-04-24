import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import api from "../services/api";

export default function Dashboard() {
  const router = useRouter();
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchChats = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await api.get("/api/chats", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setChats(res.data);
    } catch (err) {
      console.error("Failed to load chats:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChat = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await api.post(
        "/api/chats/create",
        { title: "New Chat", content: "" },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      router.push(`/chat/${res.data.id}`);
    } catch (err) {
      console.error("Chat creation failed", err);
    }
  };

  useEffect(() => {
    fetchChats();
  }, []);

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">📚 VoxStitch Dashboard</h1>

      <button
        onClick={handleCreateChat}
        className="mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        + New Chat
      </button>

      {loading ? (
        <p>Loading chats...</p>
      ) : (
        <ul className="space-y-3">
          {chats.map((chat: any) => (
            <li
              key={chat.id}
              onClick={() => router.push(`/chat/${chat.id}`)}
              className="bg-white p-4 rounded shadow hover:bg-gray-50 cursor-pointer"
            >
              <h2 className="text-xl font-semibold">{chat.title}</h2>
              <p className="text-sm text-gray-600">{chat.content?.slice(0, 50)}...</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
