import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import api from '../lib/api';
import { TrendIndicator, ConfidenceBar } from '../components/TrendIndicator';
import { toast } from '../components/Toast';

interface Analysis { id: string; event_id: string; updated_summary?: string; key_moments?: string[]; trend?: any; prediction?: string; confidence?: number; groq_prediction?: string; groq_confidence?: number; weather_conditions?: string; created_at: string; }

export default function AIAnalysis() {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [selected, setSelected] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAllAnalyses();
  }, []);

  async function loadAllAnalyses() {
    setLoading(true);
    try {
      // Load subscribed events and their latest analyses
      const subRes = await api.get('/api/events/my/subscriptions');
      const subs = subRes.data;
      const allAnalyses: Analysis[] = [];
      await Promise.all(subs.map(async (sub: any) => {
        try {
          const r = await api.get(`/api/events/${sub.event_id}/analyses?limit=5`);
          allAnalyses.push(...r.data);
        } catch {}
      }));
      const sorted = allAnalyses.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      setAnalyses(sorted);
      if (sorted.length > 0) setSelected(sorted[0]);
    } catch { toast.error('Failed to load analyses'); }
    finally { setLoading(false); }
  }

  const chartData = analyses.slice(0, 10).map((a, i) => ({
    name: `Analysis ${analyses.length - i}`,
    confidence: Math.round((a.confidence || 0) * 100),
    groq: Math.round((a.groq_confidence || 0) * 100),
  })).reverse();

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">🧠 AI Analysis Panel</h1>
        <p className="page-subtitle">Gemini Flash deep analysis — trend direction, predictions, key moments</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 16 }}>
        {/* Analysis list */}
        <div className="glass card" style={{ maxHeight: 680, overflowY: 'auto' }}>
          <div className="section-label">Recent Analyses</div>
          {loading ? <div style={{ color: 'var(--text-muted)', fontSize: 14 }}>Loading...</div> : analyses.map((a, i) => (
            <motion.div
              key={a.id}
              onClick={() => setSelected(a)}
              initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.03 }}
              style={{
                padding: '12px', borderRadius: 8, cursor: 'pointer', marginBottom: 8,
                background: selected?.id === a.id ? 'rgba(99,102,241,0.15)' : 'var(--glass-bg)',
                border: `1px solid ${selected?.id === a.id ? 'rgba(99,102,241,0.4)' : 'var(--glass-border)'}`,
              }}
            >
              <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 4 }}>Event {a.event_id.slice(0, 8)}...</div>
              <TrendIndicator trend={a.trend} />
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>{new Date(a.created_at).toLocaleTimeString()}</div>
            </motion.div>
          ))}
          {!loading && analyses.length === 0 && (
            <div style={{ color: 'var(--text-muted)', fontSize: 14, textAlign: 'center', padding: '24px 0' }}>
              Subscribe to events to see analyses here
            </div>
          )}
        </div>

        {/* Detail panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {selected ? (
            <>
              <div className="glass card">
                <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 16 }}>
                  <TrendIndicator trend={selected.trend} />
                  {selected.weather_conditions && <span style={{ fontSize: 12, color: 'var(--accent-cyan)' }}>🌤️ {selected.weather_conditions}</span>}
                </div>
                <p style={{ fontSize: 15, lineHeight: 1.7, color: 'var(--text-secondary)', marginBottom: 20 }}>{selected.updated_summary}</p>
                <ConfidenceBar value={selected.confidence} />
              </div>

              <div className="grid-2">
                <div className="glass card">
                  <div className="section-label">🔮 Gemini Prediction</div>
                  <p style={{ fontSize: 14, lineHeight: 1.6 }}>{selected.prediction}</p>
                </div>
                {selected.groq_prediction && (
                  <div className="glass card" style={{ borderColor: 'rgba(6,182,212,0.2)' }}>
                    <div className="section-label" style={{ color: 'var(--accent-cyan)' }}>⚡ Groq Prediction</div>
                    <p style={{ fontSize: 14, lineHeight: 1.6 }}>{selected.groq_prediction}</p>
                    {selected.groq_confidence && <div style={{ marginTop: 12 }}><ConfidenceBar value={selected.groq_confidence} /></div>}
                  </div>
                )}
              </div>

              {selected.key_moments && selected.key_moments.length > 0 && (
                <div className="glass card">
                  <div className="section-label">⚡ Key Moments</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {selected.key_moments.map((m, i) => (
                      <div key={i} style={{ display: 'flex', gap: 12, alignItems: 'flex-start', padding: '10px 14px', background: 'var(--glass-bg)', borderRadius: 8 }}>
                        <span style={{ width: 24, height: 24, borderRadius: '50%', background: 'var(--gradient-primary)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>{i + 1}</span>
                        <span style={{ fontSize: 13, lineHeight: 1.5 }}>{m}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Confidence chart */}
              {chartData.length > 1 && (
                <div className="glass card">
                  <div className="section-label">Confidence Over Time</div>
                  <ResponsiveContainer width="100%" height={180}>
                    <LineChart data={chartData}>
                      <XAxis dataKey="name" tick={{ fill: '#475569', fontSize: 11 }} />
                      <YAxis domain={[0, 100]} tick={{ fill: '#475569', fontSize: 11 }} />
                      <Tooltip contentStyle={{ background: '#0d1117', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8 }} />
                      <Line type="monotone" dataKey="confidence" stroke="#6366f1" strokeWidth={2} dot={false} name="Gemini" />
                      <Line type="monotone" dataKey="groq" stroke="#06b6d4" strokeWidth={2} dot={false} name="Groq" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}
            </>
          ) : (
            <div className="glass card" style={{ textAlign: 'center', padding: '60px', color: 'var(--text-muted)' }}>
              Select an analysis from the list
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
