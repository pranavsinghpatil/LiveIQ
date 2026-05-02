import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Activity, Cpu, Users, Zap, Brain, ExternalLink } from 'lucide-react';
import api from '../lib/api';
import { useAuthStore } from '../lib/auth';
import { toast } from '../components/Toast';

const BULL_BOARD_URL = import.meta.env.VITE_BULL_BOARD_URL || 'http://localhost:3001/admin/queues';

export default function AdminDashboard() {
  const { isAnalyst } = useAuthStore();
  const [stats, setStats] = useState<any>(null);
  const [aiLogs, setAiLogs] = useState<any[]>([]);
  const [modelAccuracy, setModelAccuracy] = useState<any[]>([]);
  const [failedJobs, setFailedJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { if (isAnalyst()) load(); }, []);

  async function load() {
    setLoading(true);
    try {
      const [statsRes, logsRes, accuracyRes] = await Promise.all([
        api.get('/api/admin/stats'),
        api.get('/api/admin/ai-call-log?limit=20'),
        api.get('/api/admin/predictions/model-accuracy'),
      ]);
      setStats(statsRes.data);
      setAiLogs(logsRes.data);
      setModelAccuracy(accuracyRes.data);

      try {
        const fjRes = await fetch(`${BULL_BOARD_URL.replace('/admin/queues', '')}/api/failed-jobs`);
        if (fjRes.ok) setFailedJobs(await fjRes.json());
      } catch {}
    } catch { toast.error('Failed to load admin data'); }
    finally { setLoading(false); }
  }

  if (!isAnalyst()) return (
    <div className="page"><div className="glass card" style={{ padding: 40, textAlign: 'center' }}>
      <Activity size={40} style={{ opacity: 0.3, marginBottom: 12 }} />
      <p>Admin Dashboard requires <span style={{ color: 'var(--accent-primary)' }}>Analyst</span> role.</p>
    </div></div>
  );

  const chartData = aiLogs.slice(0, 15).map(l => ({ model: l.model.slice(0, 10), latency: l.latency_ms || 0, success: l.success })).reverse();

  return (
    <div className="page">
      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 className="page-title">Admin Dashboard</h1>
            <p className="page-subtitle">Queue health, AI call log, WebSocket connections, system stats</p>
          </div>
          <a id="bull-board-link" href={BULL_BOARD_URL} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
            <ExternalLink size={14} /> Bull Board
          </a>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        {stats && [
          { label: 'Total Events', value: stats.total_events, icon: <Activity size={18} />, color: 'var(--text-primary)' },
          { label: 'Total Analyses', value: stats.total_analyses, icon: <Brain size={18} />, color: 'var(--accent-secondary)' },
          { label: 'AI API Calls', value: stats.total_ai_calls, icon: <Cpu size={18} />, color: 'var(--accent-cyan)' },
          { label: 'WS Connections', value: stats.active_ws_connections, icon: <Users size={18} />, color: 'var(--accent-green)' },
        ].map(s => (
          <motion.div key={s.label} className="card" style={{ padding: '20px' }} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            <div style={{ color: s.color, marginBottom: 12 }}>{s.icon}</div>
            <div className="stat-value" style={{ fontSize: 24, fontFamily: 'JetBrains Mono', fontWeight: 700, marginBottom: 4, color: 'var(--text-primary)' }}>{s.value}</div>
            <div className="stat-label" style={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>{s.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid-2" style={{ marginBottom: 16 }}>
        {/* Latency chart */}
        <div className="card">
          <div className="section-label">AI Latency Log</div>
          <div style={{ display: 'flex', gap: 16, marginBottom: 16, fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span style={{ color: 'var(--text-muted)' }}>Gemini Avg: <strong style={{ color: 'var(--text-primary)' }}>{stats?.avg_gemini_latency_ms}ms</strong></span>
            <span style={{ color: 'var(--text-muted)' }}>Groq Avg: <strong style={{ color: 'var(--text-primary)' }}>{stats?.avg_groq_latency_ms}ms</strong></span>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={chartData}>
              <XAxis dataKey="model" tick={{ fill: '#71717a', fontSize: 10, fontFamily: 'JetBrains Mono' }} />
              <YAxis tick={{ fill: '#71717a', fontSize: 10, fontFamily: 'JetBrains Mono' }} />
              <Tooltip contentStyle={{ background: '#111114', border: '1px solid #27272a', borderRadius: 4, fontSize: 12 }} />
              <Bar dataKey="latency" name="Latency (ms)" radius={[2, 2, 0, 0]}>
                {chartData.map((e, i) => (
                  <Cell key={i} fill={e.model.includes('groq') ? 'var(--text-muted)' : 'var(--text-primary)'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* AI Call Log table */}
        <div className="card" style={{ maxHeight: 290, overflowY: 'auto', padding: '20px 24px' }}>
          <div className="section-label" style={{ marginBottom: 12 }}>Recent AI Calls</div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
            <thead>
              <tr style={{ color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '1px solid var(--border)' }}>
                <th style={{ textAlign: 'left', padding: '8px 4px', fontWeight: 600 }}>Model</th>
                <th style={{ textAlign: 'right', padding: '8px 4px', fontWeight: 600 }}>Latency</th>
                <th style={{ textAlign: 'center', padding: '8px 4px', fontWeight: 600 }}>Status</th>
                <th style={{ textAlign: 'right', padding: '8px 4px', fontWeight: 600 }}>Time</th>
              </tr>
            </thead>
            <tbody>
              {aiLogs.map(log => (
                <tr key={log.id} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '10px 4px', color: 'var(--text-primary)', fontFamily: 'JetBrains Mono' }}>{log.model.slice(0, 14)}</td>
                  <td style={{ padding: '10px 4px', textAlign: 'right', fontFamily: 'JetBrains Mono', color: 'var(--text-secondary)' }}>{log.latency_ms}ms</td>
                  <td style={{ padding: '10px 4px', textAlign: 'center' }}>
                    <span className={`badge ${log.success ? 'badge-live' : 'badge-failed'}`} style={{ fontSize: 9 }}>{log.success ? 'OK' : 'ERR'}</span>
                  </td>
                  <td style={{ padding: '10px 4px', textAlign: 'right', color: 'var(--text-muted)', fontFamily: 'JetBrains Mono' }}>{new Date(log.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'})}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Model Accuracy */}
      {modelAccuracy.length > 0 && (
        <div className="card" style={{ marginBottom: 16 }}>
          <div className="section-label">Model Accuracy Comparison (Bonus)</div>
          <div className="grid-2">
            {modelAccuracy.map(m => (
              <div key={m.model} style={{ padding: 16, background: 'var(--bg-card)', borderRadius: 4, border: '1px solid var(--border)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                  <div style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)' }}>{m.model}</div>
                  <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{m.accurate_predictions} / {m.total_predictions} HIGH CONF</div>
                </div>
                <div style={{ fontSize: 24, fontFamily: 'JetBrains Mono', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.5px' }}>
                  {(m.accuracy_rate * 100).toFixed(0)}% <span style={{ fontSize: 12, fontWeight: 400, color: 'var(--text-muted)' }}>Accuracy</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bull Board embed info */}
      <div className="card" style={{ borderColor: 'var(--border)' }}>
        <div className="section-label">BullMQ Queue Monitor</div>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 16 }}>
          Bull Board is running as a separate Node.js service at <code style={{ color: 'var(--text-primary)', background: 'var(--bg-base)', border: '1px solid var(--border)', padding: '2px 6px', borderRadius: 4, fontFamily: 'JetBrains Mono' }}>{BULL_BOARD_URL}</code>
        </p>
        <a href={BULL_BOARD_URL} target="_blank" rel="noopener noreferrer" className="btn btn-ghost" style={{ border: '1px solid var(--border)' }}>
          <ExternalLink size={14} /> Open Dashboard
        </a>
      </div>
    </div>
  );
}
