// src/components/auth/Login.tsx
import { useState } from 'react';
import { supabase } from '../../utils/api';

export default function Login({ onLogin }: { onLogin?: () => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) setError(error.message);
    else onLogin?.();
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-lg font-semibold mb-4">Login</h2>
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
        className="input"
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
        className="input mt-2"
      />
      <button onClick={handleLogin} className="btn-primary mt-4">Login</button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}
