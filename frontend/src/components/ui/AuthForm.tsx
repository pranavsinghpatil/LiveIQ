// src/components/ui/AuthForm.tsx
import { useState } from 'react'
import { supabase } from '@/utils/supabaseClient'

export default function AuthForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [authType, setAuthType] = useState<'login' | 'signup'>('login')

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    if (authType === 'signup') {
      await supabase.auth.signUp({ email, password })
    } else {
      await supabase.auth.signInWithPassword({ email, password })
    }
    setLoading(false)
  }

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-xl font-bold mb-2 text-center">
        {authType === 'login' ? 'Log In' : 'Sign Up'}
      </h2>
      <form onSubmit={handleAuth} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          className="w-full px-4 py-2 border rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full px-4 py-2 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 w-full rounded hover:bg-blue-700"
        >
          {loading ? 'Processing...' : authType === 'login' ? 'Log In' : 'Sign Up'}
        </button>
        <p className="text-sm text-center text-gray-600">
          {authType === 'login' ? 'New here?' : 'Already have an account?'}{' '}
          <button
            type="button"
            onClick={() => setAuthType(authType === 'login' ? 'signup' : 'login')}
            className="text-blue-500 underline"
          >
            {authType === 'login' ? 'Sign Up' : 'Log In'}
          </button>
        </p>
      </form>
    </div>
  )
}
