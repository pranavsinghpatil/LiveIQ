import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Clock } from 'lucide-react';
import api from '../lib/api';
import { useAuthStore } from '../lib/auth';
import { toast } from '../components/Toast';

export default function PostEventReport() {
  const { isAnalyst } = useAuthStore();
  const [events, setEvents] = useState<any[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { loadFinishedEvents(); }, []);

  async function loadFinishedEvents() {
    try {
      const res = await api.get('/api/events', { params: { status: 'Final' } });
      setEvents(res.data.slice(0, 20));
    } catch { toast.error('Failed to load events'); }
  }

  async function loadReport(eventId: string) {
    setSelected(eventId); setLoading(true); setReport(null);
    try {
      const r = await api.get(`/api/events/${eventId}/report`);
      setReport(r.data);
    } catch (e: any) {
      if (e.response?.status === 404) toast.info('Report not available yet for this event');
      else toast.error('Failed to load report');
    } finally { setLoading(false); }
  }

  if (!isAnalyst()) return (
    <div className="page">
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="glass card" style={{ padding: '80px 40px', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 24, border: '1px solid var(--border)' }}>
          <FileText size={24} color="var(--text-muted)" />
        </div>
        <h2 style={{ fontSize: 24, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 8 }}>Access Denied</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Post-event reports require <strong style={{ color: 'var(--accent-cyan)' }}>Analyst</strong> role.</p>
      </motion.div>
    </div>
  );

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Post-Event Reports</h1>
        <p className="page-subtitle">Full narrative, key moments, prediction accuracy review</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: 24 }}>
        <div className="card" style={{ maxHeight: 680, overflowY: 'auto' }}>
          <div className="section-label">Finished Events</div>
          {events.map((e, i) => (
            <motion.div
              key={e.id} onClick={() => loadReport(e.id)}
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.03 }}
              style={{
                padding: 16, borderRadius: 8, cursor: 'pointer', marginBottom: 8,
                background: selected === e.id ? 'var(--bg-hover)' : 'var(--bg-base)',
                border: `1px solid ${selected === e.id ? 'var(--text-primary)' : 'var(--border)'}`,
              }}
            >
              <div style={{ fontSize: 13, fontWeight: 700, marginBottom: 4 }}>{e.home_team} vs {e.away_team}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', fontFamily: 'JetBrains Mono' }}>
                {e.home_score} — {e.away_score} <span style={{ fontFamily: 'Inter', textTransform: 'uppercase', letterSpacing: '0.05em', marginLeft: 6 }}>· {e.sport}</span>
              </div>
            </motion.div>
          ))}
        </div>

        <div>
          {loading && (
            <div className="glass card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 0' }}>
              <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 2 }} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
                <FileText size={32} color="var(--accent-cyan)" style={{ filter: 'drop-shadow(0 0 10px rgba(0,240,255,0.5))' }} />
                <span style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent-cyan)', fontWeight: 800 }}>Generating Report...</span>
              </motion.div>
            </div>
          )}
          {report && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div className="card">
                <div style={{ display: 'flex', gap: 24, alignItems: 'center', marginBottom: 16 }}>
                  <div style={{ paddingRight: 24, borderRight: '1px solid var(--border)' }}>
                    <div className="section-label">Accuracy</div>
                    <div style={{ fontSize: 48, fontFamily: 'JetBrains Mono', fontWeight: 700, color: (report.prediction_accuracy || 0) >= 0.7 ? 'var(--text-primary)' : 'var(--text-secondary)', letterSpacing: '-2px' }}>
                      {((report.prediction_accuracy || 0) * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div style={{ flex: 1 }}>
                    <div className="section-label">Match Narrative</div>
                    <p style={{ fontSize: 14, lineHeight: 1.7, color: 'var(--text-secondary)', whiteSpace: 'pre-line' }}>{report.narrative}</p>
                  </div>
                </div>
              </div>

              {report.key_moments?.length > 0 && (
                <div className="card">
                  <div className="section-label">Top 5 Key Moments</div>
                  {report.key_moments.map((m: string, i: number) => (
                    <div key={i} style={{ display: 'flex', gap: 16, padding: '16px 0', borderBottom: '1px solid var(--border)' }}>
                      <span style={{ width: 28, height: 28, borderRadius: '4px', background: 'var(--bg-base)', border: '1px solid var(--border)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 12, fontWeight: 700, fontFamily: 'JetBrains Mono', color: 'var(--text-secondary)', flexShrink: 0 }}>0{i + 1}</span>
                      <span style={{ fontSize: 13, lineHeight: 1.6, color: 'var(--text-primary)' }}>{m}</span>
                    </div>
                  ))}
                </div>
              )}
              <div style={{ fontSize: 11, color: 'var(--text-muted)', display: 'flex', gap: 6, alignItems: 'center', fontFamily: 'JetBrains Mono', marginTop: 8 }}>
                <Clock size={11} /> GENERATED: {new Date(report.generated_at).toLocaleString()}
              </div>
            </div>
          )}
          {!loading && !report && (
            <div className="glass card empty-state" style={{ padding: '80px 40px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 24, border: '1px solid var(--border)' }}>
                <FileText size={24} color="var(--text-muted)" />
              </div>
              <p style={{ color: 'var(--text-secondary)' }}>Select a finished event to view its full analytical narrative.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
