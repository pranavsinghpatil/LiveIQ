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
            <h1 className="page-title">⚙️ Admin Dashboard</h1>
            <p className="page-subtitle">Queue health, AI call log, WebSocket connections, system stats</p>
          </div>
          <a id="bull-board-link" href={BULL_BOARD_URL} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
            <ExternalLink size={14} /> Bull Board
          </a>
        </div>
      </div>

      {/* Stats */}
      <div className="grid-4" style={{ marginBottom: 24 }}>
        {stats && [
          { label: 'Total Events', value: stats.total_events, icon: <Activity size={20} />, color: 'var(--accent-primary)' },
          { label: 'Total Analyses', value: stats.total_analyses, icon: <Brain size={20} />, color: 'var(--accent-secondary)' },
          { label: 'AI API Calls', value: stats.total_ai_calls, icon: <Cpu size={20} />, color: 'var(--accent-cyan)' },
          { label: 'WS Connections', value: stats.active_ws_connections, icon: <Users size={20} />, color: 'var(--accent-green)' },
        ].map(s => (
          <motion.div key={s.label} className="glass stat-card" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            <div style={{ color: s.color, marginBottom: 8 }}>{s.icon}</div>
            <div className="stat-value" style={{ color: s.color }}>{s.value}</div>
            <div className="stat-label">{s.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid-2" style={{ marginBottom: 16 }}>
        {/* Latency chart */}
        <div className="glass card">
          <div className="section-label">AI Latency Log</div>
          <div style={{ display: 'flex', gap: 16, marginBottom: 8, fontSize: 12 }}>
            <span style={{ color: 'var(--text-muted)' }}>Gemini avg: <strong style={{ color: 'var(--accent-secondary)' }}>{stats?.avg_gemini_latency_ms}ms</strong></span>
            <span style={{ color: 'var(--text-muted)' }}>Groq avg: <strong style={{ color: 'var(--accent-cyan)' }}>{stats?.avg_groq_latency_ms}ms</strong></span>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={chartData}>
              <XAxis dataKey="model" tick={{ fill: '#475569', fontSize: 10 }} />
              <YAxis tick={{ fill: '#475569', fontSize: 10 }} />
              <Tooltip contentStyle={{ background: '#0d1117', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8 }} />
              <Bar dataKey="latency" name="Latency (ms)" radius={[4, 4, 0, 0]}>
                {chartData.map((e, i) => (
                  <Cell key={i} fill={e.model.includes('groq') ? 'rgba(6,182,212,0.7)' : 'rgba(139,92,246,0.7)'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* AI Call Log table */}
        <div className="glass card" style={{ maxHeight: 280, overflowY: 'auto' }}>
          <div className="section-label">Recent AI Calls</div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
            <thead>
              <tr style={{ color: 'var(--text-muted)' }}>
                <th style={{ textAlign: 'left', padding: '6px 8px' }}>Model</th>
                <th style={{ textAlign: 'right', padding: '6px 8px' }}>Latency</th>
                <th style={{ textAlign: 'center', padding: '6px 8px' }}>Status</th>
                <th style={{ textAlign: 'right', padding: '6px 8px' }}>Time</th>
              </tr>
            </thead>
            <tbody>
              {aiLogs.map(log => (
                <tr key={log.id} style={{ borderTop: '1px solid var(--glass-border)' }}>
                  <td style={{ padding: '7px 8px' }}>{log.model.includes('groq') ? '⚡' : '🧠'} {log.model.slice(0, 14)}</td>
                  <td style={{ padding: '7px 8px', textAlign: 'right', fontFamily: 'JetBrains Mono', color: 'var(--text-secondary)' }}>{log.latency_ms}ms</td>
                  <td style={{ padding: '7px 8px', textAlign: 'center' }}>
                    <span className={`badge ${log.success ? 'badge-live' : 'badge-failed'}`} style={{ fontSize: 9 }}>{log.success ? 'OK' : 'ERR'}</span>
                  </td>
                  <td style={{ padding: '7px 8px', textAlign: 'right', color: 'var(--text-muted)' }}>{new Date(log.created_at).toLocaleTimeString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Model Accuracy */}
      {modelAccuracy.length > 0 && (
        <div className="glass card" style={{ marginBottom: 16 }}>
          <div className="section-label">🏆 Model Accuracy Comparison (Bonus)</div>
          <div className="grid-2">
            {modelAccuracy.map(m => (
              <div key={m.model} style={{ padding: 16, background: 'var(--glass-bg)', borderRadius: 12, border: '1px solid var(--glass-border)' }}>
                <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 8 }}>{m.model.includes('gemini') ? '🧠' : '⚡'} {m.model}</div>
                <div style={{ fontSize: 36, fontWeight: 900, color: m.model.includes('gemini') ? 'var(--accent-secondary)' : 'var(--accent-cyan)' }}>
                  {(m.accuracy_rate * 100).toFixed(0)}%
                </div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{m.accurate_predictions}/{m.total_predictions} high-confidence</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bull Board embed info */}
      <div className="glass card" style={{ borderColor: 'rgba(99,102,241,0.2)' }}>
        <div className="section-label">📊 BullMQ Queue Monitor</div>
        <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 16 }}>
          Bull Board is running as a separate Node.js service at <code style={{ color: 'var(--accent-cyan)', background: 'rgba(6,182,212,0.1)', padding: '2px 6px', borderRadius: 4 }}>{BULL_BOARD_URL}</code>
        </p>
        <a href={BULL_BOARD_URL} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
          <ExternalLink size={14} /> Open Bull Board Dashboard
        </a>
      </div>
    </div>
  );
}
