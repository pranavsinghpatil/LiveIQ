// src/components/chat/ChatDisplay.tsx
export default function ChatDisplay({ messages }: { messages: string[] }) {
  return (
    <div className="bg-gray-100 p-4 rounded max-h-[400px] overflow-y-auto space-y-2">
      {messages.map((msg, i) => (
        <div key={i} className="p-2 bg-white rounded shadow text-sm">
          {msg}
        </div>
      ))}
    </div>
  )
}
