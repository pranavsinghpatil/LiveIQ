// src/components/chat/FileUploader.tsx
import { useState } from 'react'

export default function FileUploader() {
  const [file, setFile] = useState<File | null>(null)

  const handleFileUpload = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    const res = await fetch('http://localhost:8000/upload_file', {
      method: 'POST',
      body: formData,
    })

    const result = await res.json()
    console.log(result)
  }

  return (
    <div className="mb-4">
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-2"
      />
      <button
        onClick={handleFileUpload}
        className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
      >
        Upload
      </button>
    </div>
  )
}
