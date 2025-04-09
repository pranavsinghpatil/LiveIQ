// src/components/chat/ChatInput.tsx
import { useState } from 'react'

export default function ChatInput({ onSend }: { onSend: (msg: string) => void }) {
  const [message, setMessage] = useState('')

  return (
    <div className="flex space-x-2 mt-4">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
        className="flex-1 px-4 py-2 border rounded"
      />
      <button
        onClick={() => {
          onSend(message)
          setMessage('')
        }}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Send
      </button>
    </div>
  )
}
