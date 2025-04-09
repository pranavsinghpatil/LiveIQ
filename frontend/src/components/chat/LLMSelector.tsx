// src/components/chat/LLMSelector.tsx
import { useState } from 'react'

const models = ['gpt-3.5-turbo', 'claude-v1', 'gemini-pro', 'mistral-7b']

export default function LLMSelector({ selected, onSelect }: {
  selected: string
  onSelect: (model: string) => void
}) {
  const [open, setOpen] = useState(false)

  return (
    <div className="relative mb-4">
      <button
        onClick={() => setOpen(!open)}
        className="border px-4 py-2 rounded w-full bg-white text-left"
      >
        {selected ? `Model: ${selected}` : 'Select a model'}
      </button>
      {open && (
        <div className="absolute z-10 w-full bg-white border mt-1 rounded shadow">
          {models.map((model) => (
            <div
              key={model}
              onClick={() => {
                onSelect(model)
                setOpen(false)
              }}
              className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
            >
              {model}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
