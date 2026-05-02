import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';
import api from '../lib/api';
import { useWebSocket } from '../hooks/useWebSocket';
import type { WSMessage } from '../hooks/useWebSocket';
import { PipelineStepper } from '../components/PipelineStepper';
import { CommentaryFeed } from '../components/CommentaryFeed';
import { TrendIndicator, ConfidenceBar } from '../components/TrendIndicator';
import { toast } from '../components/Toast';

interface Stage { stage_number: number; stage_name: string; status: 'pending'|'active'|'done'|'failed'; started_at?: string; completed_at?: string; }
interface Commentary { id: string; text: string; model: string; latency_ms?: number; created_at: string; }
interface Analysis { updated_summary?: string; key_moments?: string[]; trend?: 'momentum'|'stable'|'reversal'; prediction?: string; confidence?: number; groq_prediction?: string; groq_confidence?: number; weather_conditions?: string; }
interface EventDetail { id: string; sport: string; league?: string; home_team: string; away_team: string; home_score?: string; away_score?: string; status: string; venue?: string; }

export default function LiveEventView() {
  const [params] = useSearchParams();
  const eventId = params.get('event');
  const [event, setEvent] = useState<EventDetail | null>(null);
  const [stages, setStages] = useState<Stage[]>([]);
  const [commentaries, setCommentaries] = useState<Commentary[]>([]);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);

  const handleWsMessage = useCallback((msg: WSMessage) => {
    if (msg.type === 'commentary') {
      const c = msg.data as any;
      setCommentaries(prev => [{ id: Date.now().toString(), text: c.text, model: c.model, latency_ms: c.latency_ms, created_at: msg.timestamp }, ...prev.slice(0, 49)]);
    } else if (msg.type === 'analysis') {
      setAnalysis(msg.data as Analysis);
    } else if (msg.type === 'stage_update') {
      loadStages();
    } else if (msg.type === 'alert') {
      toast.info(`🔔 Alert: ${(msg.data as any).message}`);
    }
  }, []);

  const { connected } = useWebSocket(eventId, { onMessage: handleWsMessage });

  useEffect(() => { if (eventId) { loadEvent(); loadStages(); loadCommentaries(); loadAnalysis(); } }, [eventId]);

  // Poll stages every 10s as fallback
  useEffect(() => {
    if (!eventId) return;
    const iv = setInterval(loadStages, 10000);
    return () => clearInterval(iv);
  }, [eventId]);

  async function loadEvent() {
    try { const r = await api.get(`/api/events/${eventId}`); setEvent(r.data); }
    catch { toast.error('Event not found'); }
    finally { setLoading(false); }
  }
  async function loadStages() {
    try { const r = await api.get(`/api/events/${eventId}/stages`); setStages(r.data); } catch {}
  }
  async function loadCommentaries() {
    try { const r = await api.get(`/api/events/${eventId}/commentary`); setCommentaries(r.data); } catch {}
  }
  async function loadAnalysis() {
    try { const r = await api.get(`/api/events/${eventId}/analyses?limit=1`); if (r.data[0]) setAnalysis(r.data[0]); } catch {}
  }

  if (!eventId) return <div className="page"><div className="glass card" style={{ padding: 40, textAlign: 'center' }}>Select an event from the Event Browser to view live data.</div></div>;
  if (loading) return <div className="page" style={{ textAlign: 'center', padding: '80px' }}>Loading event...</div>;

  return (
    <div className="page">
      {/* Header */}
      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 8 }}>
              <span className={`badge badge-${event?.status === 'In Progress' ? 'live' : 'done'}`}>
                {event?.status === 'In Progress' && <span className="live-dot" style={{ width: 6, height: 6 }} />}
                {event?.status}
              </span>
              <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>🏆 {event?.league || event?.sport}</span>
            </div>
            <h1 className="page-title">{event?.home_team} <span style={{ color: 'var(--text-muted)' }}>vs</span> {event?.away_team}</h1>
            {event?.venue && <p className="page-subtitle">📍 {event.venue}</p>}
          </div>
          <div style={{ textAlign: 'center' }}>
            <div className="score-display">{event?.home_score || '0'} — {event?.away_score || '0'}</div>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'center', marginTop: 8 }}>
              {connected ? <span style={{ color: 'var(--accent-green)', fontSize: 12, display: 'flex', gap: 4, alignItems: 'center' }}><Wifi size={12} />Live</span>
                         : <span style={{ color: 'var(--accent-red)', fontSize: 12, display: 'flex', gap: 4, alignItems: 'center' }}><WifiOff size={12} />Reconnecting...</span>}
            </div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 340px', gap: 16 }}>
        {/* Commentary Feed */}
        <div className="glass card">
          <div className="section-label">⚡ Live Commentary (Groq Llama)</div>
          <CommentaryFeed items={commentaries} />
        </div>

        {/* AI Analysis */}
        <div className="glass card">
          <div className="section-label">🧠 AI Analysis (Gemini)</div>
          {analysis ? (
            <div>
              {analysis.weather_conditions && (
                <div style={{ marginBottom: 12, padding: '8px 12px', background: 'rgba(6,182,212,0.1)', borderRadius: 8, fontSize: 13, color: 'var(--accent-cyan)' }}>
                  🌤️ {analysis.weather_conditions}
                </div>
              )}
              <p style={{ fontSize: 14, lineHeight: 1.6, color: 'var(--text-secondary)', marginBottom: 16 }}>{analysis.updated_summary}</p>
              <div style={{ marginBottom: 16 }}>
                <TrendIndicator trend={analysis.trend} />
              </div>
              <ConfidenceBar value={analysis.confidence} />
              <div style={{ marginTop: 16, padding: 12, background: 'rgba(99,102,241,0.08)', borderRadius: 8 }}>
                <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--accent-primary)', marginBottom: 6 }}>PREDICTION</div>
                <p style={{ fontSize: 13 }}>{analysis.prediction}</p>
              </div>
              {analysis.key_moments && analysis.key_moments.length > 0 && (
                <div style={{ marginTop: 14 }}>
                  <div className="section-label">Key Moments</div>
                  {analysis.key_moments.map((m, i) => (
                    <div key={i} style={{ fontSize: 13, padding: '6px 0', borderBottom: '1px solid var(--glass-border)', color: 'var(--text-secondary)' }}>
                      {i + 1}. {m}
                    </div>
                  ))}
                </div>
              )}
              {/* Multi-model debate bonus */}
              {analysis.groq_prediction && (
                <div style={{ marginTop: 14, padding: 12, background: 'rgba(6,182,212,0.08)', borderRadius: 8 }}>
                  <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--accent-cyan)', marginBottom: 6 }}>⚡ GROQ PREDICTION</div>
                  <p style={{ fontSize: 13 }}>{analysis.groq_prediction}</p>
                  {analysis.groq_confidence && <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>Confidence: {(analysis.groq_confidence * 100).toFixed(0)}%</div>}
                </div>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '32px 0', fontSize: 14 }}>
              <RefreshCw size={24} style={{ marginBottom: 8, opacity: 0.4 }} /><br />
              AI analysis runs every 5 minutes. Waiting for first analysis...
            </div>
          )}
        </div>

        {/* Pipeline Stepper */}
        <div className="glass card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <div className="section-label" style={{ marginBottom: 0 }}>Pipeline Status</div>
            <button className="btn btn-ghost btn-sm" onClick={loadStages}><RefreshCw size={12} /></button>
          </div>
          <PipelineStepper stages={stages} />
        </div>
      </div>
    </div>
  );
}
