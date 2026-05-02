import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import api from '../lib/api';
import { TrendIndicator, ConfidenceBar } from '../components/TrendIndicator';
import { toast } from '../components/Toast';

export default function PredictionBoard() {
  const [predictions, setPredictions] = useState<any[]>([]);
  const [modelAccuracy, setModelAccuracy] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  async function load() {
    setLoading(true);
    try {
      const subRes = await api.get('/api/events/my/subscriptions');
      const all: any[] = [];
      await Promise.all(subRes.data.map(async (sub: any) => {
        try {
          const [eventRes, anaRes] = await Promise.all([
            api.get(`/api/events/${sub.event_id}`),
            api.get(`/api/events/${sub.event_id}/analyses?limit=1`),
          ]);
          if (anaRes.data[0]) {
            all.push({ ...anaRes.data[0], event: eventRes.data });
          }
        } catch {}
      }));
      setPredictions(all);

      try {
        const accRes = await api.get('/api/admin/predictions/model-accuracy');
        setModelAccuracy(accRes.data);
      } catch {}
    } catch { toast.error('Failed to load predictions'); }
    finally { setLoading(false); }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">🔮 Prediction Board</h1>
        <p className="page-subtitle">AI predictions across all subscribed events with confidence tracking</p>
      </div>

      {/* Model Accuracy (Bonus) */}
      {modelAccuracy.length > 0 && (
        <div className="glass card" style={{ marginBottom: 24 }}>
          <div className="section-label">🏆 Model Accuracy — Multi-Model Debate</div>
          <div className="grid-2">
            {modelAccuracy.map((m) => (
              <div key={m.model} style={{ padding: '16px', background: 'var(--glass-bg)', borderRadius: 12, border: '1px solid var(--glass-border)' }}>
                <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 8 }}>
                  {m.model.includes('gemini') ? '🧠' : '⚡'} {m.model}
                </div>
                <div className="score-display" style={{ fontSize: 36 }}>{(m.accuracy_rate * 100).toFixed(0)}%</div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>
                  {m.accurate_predictions} / {m.total_predictions} predictions
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: 48, color: 'var(--text-muted)' }}>Loading predictions...</div>
      ) : predictions.length === 0 ? (
        <div className="glass card" style={{ textAlign: 'center', padding: 48, color: 'var(--text-muted)' }}>
          Subscribe to events to see AI predictions here
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {predictions.map((p, i) => (
            <motion.div key={p.id} className="glass card" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: 24, alignItems: 'center' }}>
                <div>
                  <div style={{ fontSize: 16, fontWeight: 700, marginBottom: 4 }}>
                    {p.event?.home_team} vs {p.event?.away_team}
                  </div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{p.event?.league} • {p.event?.sport}</div>
                  <div style={{ marginTop: 8 }}><TrendIndicator trend={p.trend} /></div>
                </div>
                <div style={{ textAlign: 'center', padding: '0 16px', borderLeft: '1px solid var(--glass-border)', borderRight: '1px solid var(--glass-border)' }}>
                  <div style={{ fontSize: 28, fontWeight: 800, fontFamily: 'JetBrains Mono' }}>
                    {p.event?.home_score || '0'} — {p.event?.away_score || '0'}
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{p.event?.status}</div>
                </div>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--accent-primary)', marginBottom: 6 }}>🧠 GEMINI</div>
                  <p style={{ fontSize: 13, marginBottom: 10 }}>{p.prediction}</p>
                  <ConfidenceBar value={p.confidence} />
                  {p.groq_prediction && (
                    <div style={{ marginTop: 12 }}>
                      <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--accent-cyan)', marginBottom: 4 }}>⚡ GROQ</div>
                      <p style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{p.groq_prediction}</p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
