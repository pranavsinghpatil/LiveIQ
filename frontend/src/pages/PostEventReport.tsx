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
    <div className="page"><div className="glass card" style={{ padding: 40, textAlign: 'center' }}>
      <FileText size={40} style={{ opacity: 0.3, marginBottom: 12 }} />
      <p>Post-event reports require <span style={{ color: 'var(--accent-primary)' }}>Analyst</span> role.</p>
    </div></div>
  );

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">📋 Post-Event Reports</h1>
        <p className="page-subtitle">Full Gemini narrative, key moments, prediction accuracy review</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: 16 }}>
        <div className="glass card" style={{ maxHeight: 680, overflowY: 'auto' }}>
          <div className="section-label">Finished Events</div>
          {events.map((e, i) => (
            <motion.div
              key={e.id} onClick={() => loadReport(e.id)}
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.03 }}
              style={{
                padding: 12, borderRadius: 8, cursor: 'pointer', marginBottom: 8,
                background: selected === e.id ? 'rgba(99,102,241,0.15)' : 'var(--glass-bg)',
                border: `1px solid ${selected === e.id ? 'rgba(99,102,241,0.4)' : 'var(--glass-border)'}`,
              }}
            >
              <div style={{ fontSize: 13, fontWeight: 600 }}>{e.home_team} vs {e.away_team}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 3 }}>
                {e.home_score} — {e.away_score} · {e.sport}
              </div>
            </motion.div>
          ))}
        </div>

        <div>
          {loading && <div className="glass card" style={{ textAlign: 'center', padding: 48, color: 'var(--text-muted)' }}>Loading report...</div>}
          {report && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div className="glass card">
                <div style={{ display: 'flex', gap: 16, alignItems: 'center', marginBottom: 16 }}>
                  <div>
                    <div className="section-label">Prediction Accuracy</div>
                    <div style={{ fontSize: 48, fontWeight: 900, color: (report.prediction_accuracy || 0) >= 0.7 ? 'var(--accent-green)' : 'var(--accent-yellow)' }}>
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
                <div className="glass card">
                  <div className="section-label">⚡ Top 5 Key Moments</div>
                  {report.key_moments.map((m: string, i: number) => (
                    <div key={i} style={{ display: 'flex', gap: 12, padding: '12px 0', borderBottom: '1px solid var(--glass-border)' }}>
                      <span style={{ width: 28, height: 28, borderRadius: '50%', background: 'var(--gradient-primary)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 12, fontWeight: 700, flexShrink: 0 }}>{i + 1}</span>
                      <span style={{ fontSize: 14, lineHeight: 1.5 }}>{m}</span>
                    </div>
                  ))}
                </div>
              )}
              <div style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', gap: 6, alignItems: 'center' }}>
                <Clock size={12} /> Generated: {new Date(report.generated_at).toLocaleString()}
              </div>
            </div>
          )}
          {!loading && !report && (
            <div className="glass card" style={{ textAlign: 'center', padding: 48, color: 'var(--text-muted)' }}>
              <FileText size={32} style={{ opacity: 0.3, marginBottom: 12 }} /><br />
              Select a finished event to view its report
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
