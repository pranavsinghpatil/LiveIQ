// src/layouts/MainLayout.tsx
import { useEffect, useState } from 'react'
import { supabase } from '@/utils/supabaseClient'
import { useNavigate } from 'react-router-dom'

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      setUser(data?.user || null)
      setLoading(false)
    })
  }, [])

  if (loading) return <div>Loading...</div>
  if (!user) return <div>Please login first.</div>

  return <div>{children}</div>
}
