import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Tv, Mail, Lock, User, Eye, EyeOff } from 'lucide-react';
import api from '../lib/api';
import { useAuthStore } from '../lib/auth';
import { toast } from '../components/Toast';

export default function AuthPage() {
  const [tab, setTab] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'analyst' | 'viewer'>('viewer');
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      if (tab === 'register') {
        const res = await api.post('/api/auth/register', { email, password, role });
        setAuth(res.data.user, res.data.access_token);
        toast.success('Account created! Welcome to LiveIQ.');
      } else {
        const form = new FormData();
        form.append('username', email);
        form.append('password', password);
        const res = await api.post('/api/auth/token', form, { headers: { 'Content-Type': 'multipart/form-data' } });
        setAuth(res.data.user, res.data.access_token);
        toast.success('Welcome back!');
      }
      navigate('/events');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ width: 56, height: 56, borderRadius: 16, background: 'var(--text-primary)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', marginBottom: 16 }}>
            <Tv size={26} color="var(--bg-base)" />
          </div>
          <h1 style={{ fontSize: 28, fontWeight: 900, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>LiveIQ</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 4, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Intelligence Platform</p>
        </div>

        <div className="card auth-card">
          <div className="auth-tabs">
            <button className={`auth-tab ${tab === 'login' ? 'active' : ''}`} onClick={() => setTab('login')}>Sign In</button>
            <button className={`auth-tab ${tab === 'register' ? 'active' : ''}`} onClick={() => setTab('register')}>Create Account</button>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label"><Mail size={12} style={{ display: 'inline', marginRight: 4 }} />Email</label>
              <input id="email" className="input" type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} required />
            </div>

            <div className="form-group">
              <label className="form-label"><Lock size={12} style={{ display: 'inline', marginRight: 4 }} />Password</label>
              <div style={{ position: 'relative' }}>
                <input id="password" className="input" type={showPw ? 'text' : 'password'} placeholder="Min 6 characters" value={password} onChange={e => setPassword(e.target.value)} required style={{ paddingRight: 44 }} />
                <button type="button" onClick={() => setShowPw(!showPw)} style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}>
                  {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {tab === 'register' && (
              <div className="form-group">
                <label className="form-label"><User size={12} style={{ display: 'inline', marginRight: 4 }} />Role</label>
                <select id="role" className="input" value={role} onChange={e => setRole(e.target.value as 'analyst' | 'viewer')}>
                  <option value="viewer">Viewer — Read-only, max 3 subscriptions</option>
                  <option value="analyst">Analyst — Full access, custom alerts, reports</option>
                </select>
              </div>
            )}

            <button id="auth-submit" type="submit" className="btn btn-primary btn-lg" style={{ width: '100%', justifyContent: 'center', marginTop: 8 }} disabled={loading}>
              {loading ? 'Please wait...' : tab === 'login' ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <div style={{ marginTop: 24, padding: '14px', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12, color: 'var(--text-secondary)' }}>
            <strong style={{ color: 'var(--text-primary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Demo credentials</strong><br /><br />
            Analyst: analyst@demo.com / demo123<br />
            Viewer: viewer@demo.com / demo123
          </div>
        </div>
      </motion.div>
    </div>
  );
}
