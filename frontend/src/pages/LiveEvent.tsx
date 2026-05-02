import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Wifi, WifiOff, RefreshCw, CloudSun } from 'lucide-react';
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
      const newId = `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
      setCommentaries(prev => [{ id: newId, text: c.text, model: c.model, latency_ms: c.latency_ms, created_at: msg.timestamp }, ...prev.slice(0, 49)]);
    } else if (msg.type === 'analysis') {
      setAnalysis(msg.data as Analysis);
    } else if (msg.type === 'stage_update') {
      loadStages();
    } else if (msg.type === 'alert') {
      toast.info((msg.data as any).message);
    }
  }, []);

  const { connected } = useWebSocket(eventId, { onMessage: handleWsMessage });

  useEffect(() => { if (eventId) { loadEvent(); loadStages(); loadCommentaries(); loadAnalysis(); } }, [eventId]);
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
  async function loadStages() { try { const r = await api.get(`/api/events/${eventId}/stages`); setStages(r.data); } catch {} }
  async function loadCommentaries() { try { const r = await api.get(`/api/events/${eventId}/commentary`); setCommentaries(r.data); } catch {} }
  async function loadAnalysis() { try { const r = await api.get(`/api/events/${eventId}/analyses?limit=1`); if (r.data[0]) setAnalysis(r.data[0]); } catch {} }

  // ── Empty / Loading states ──────────────────────────────
  if (!eventId) return (
    <div className="page">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="card"
        style={{ padding: '80px 40px', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <WifiOff size={28} color="var(--text-muted)" style={{ marginBottom: 16, opacity: 0.4 }} />
        <p style={{ fontSize: 15, fontWeight: 500, color: 'var(--text-secondary)', marginBottom: 4 }}>No Event Selected</p>
        <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>Open the Event Browser and select a match to watch.</p>
      </motion.div>
    </div>
  );

  if (loading) return (
    <div className="page" style={{ height: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 2 }}
        style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
        <RefreshCw size={24} color="var(--text-muted)" />
        <span style={{ fontSize: 12, color: 'var(--text-muted)', letterSpacing: '0.05em' }}>Loading event...</span>
      </motion.div>
    </div>
  );

  const isLive = event?.status === 'In Progress';

  return (
    <div className="page" style={{ paddingBottom: 60 }}>

      {/* ── Event Header ───────────────────────── */}
      <div style={{ marginBottom: 28 }}>
        {/* Top meta row */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            {isLive && <span className="live-dot" />}
            <span style={{ fontSize: 11, fontWeight: 600, color: isLive ? 'var(--accent-green)' : 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              {event?.status}
            </span>
          </div>
          {(event?.league || event?.sport) && (
            <>
              <span style={{ color: 'rgba(255,255,255,0.15)', fontSize: 12 }}>·</span>
              <span style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                {event?.league || event?.sport}
              </span>
            </>
          )}
          {event?.venue && (
            <>
              <span style={{ color: 'rgba(255,255,255,0.15)', fontSize: 12 }}>·</span>
              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{event.venue}</span>
            </>
          )}
          {/* Connection pill — pushed right */}
          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 5 }}>
            {connected
              ? <><Wifi size={11} color="var(--accent-green)" /><span style={{ fontSize: 11, color: 'var(--accent-green)', fontWeight: 500 }}>Live</span></>
              : <><WifiOff size={11} color="var(--text-muted)" /><span style={{ fontSize: 11, color: 'var(--text-muted)' }}>Offline</span></>
            }
          </div>
        </div>

        {/* Teams + Score */}
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 20 }}>
          <h1 style={{ fontSize: 26, fontWeight: 600, color: 'var(--text-primary)', margin: 0, lineHeight: 1.2 }}>
            {event?.home_team}
            <span style={{ color: 'var(--text-muted)', fontWeight: 400, fontSize: 20, margin: '0 12px' }}>vs</span>
            {event?.away_team}
          </h1>
          <div style={{ fontSize: 32, fontWeight: 600, fontFamily: 'JetBrains Mono, monospace', color: 'var(--text-primary)', letterSpacing: '-0.5px', flexShrink: 0 }}>
            {event?.home_score ?? '0'} — {event?.away_score ?? '0'}
          </div>
        </div>

        {/* Divider */}
        <div style={{ height: 1, background: 'rgba(255,255,255,0.06)', marginTop: 20 }} />
      </div>

      {/* ── Main Grid ──────────────────────────── */}
      <div className="live-grid">

        {/* Column 1: Commentary */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', minHeight: 480 }}>
          <CommentaryFeed items={commentaries} />
        </div>

        {/* Column 2: AI Analysis */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div>
            <p style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 12 }}>
              AI Analysis
            </p>

            {/* Weather */}
            {analysis?.weather_conditions && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 14 }}>
                <CloudSun size={12} color="var(--text-muted)" />
                <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{analysis.weather_conditions}</span>
              </div>
            )}

            {/* Summary */}
            {analysis ? (
              <p style={{ fontSize: 13, lineHeight: 1.65, color: 'var(--text-secondary)', margin: 0 }}>
                {analysis.updated_summary}
              </p>
            ) : (
              <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: 0 }}>Awaiting analysis...</p>
            )}
          </div>

          {analysis && (
            <>
              {/* Trend + Confidence */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                <TrendIndicator trend={analysis.trend} />
                <ConfidenceBar value={analysis.confidence} />
              </div>

              {/* Gemini Prediction */}
              {analysis.prediction && (
                <div style={{ padding: '14px 16px', background: 'rgba(255,255,255,0.02)', borderRadius: 8, border: '1px solid rgba(255,255,255,0.06)' }}>
                  <p style={{ fontSize: 10, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 6 }}>Gemini Prediction</p>
                  <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: 0, lineHeight: 1.55 }}>{analysis.prediction}</p>
                </div>
              )}

              {/* Groq Prediction */}
              {analysis.groq_prediction && (
                <div style={{ padding: '14px 16px', background: 'rgba(255,255,255,0.02)', borderRadius: 8, border: '1px solid rgba(255,255,255,0.06)' }}>
                  <p style={{ fontSize: 10, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 6 }}>Groq Prediction</p>
                  <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: 0, lineHeight: 1.55 }}>{analysis.groq_prediction}</p>
                  {analysis.groq_confidence && (
                    <p style={{ fontSize: 11, color: 'var(--text-muted)', margin: '6px 0 0', fontFamily: 'JetBrains Mono, monospace' }}>
                      Confidence: {(analysis.groq_confidence * 100).toFixed(0)}%
                    </p>
                  )}
                </div>
              )}

              {/* Key Moments */}
              {analysis.key_moments && analysis.key_moments.length > 0 && (
                <div>
                  <p style={{ fontSize: 10, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 10 }}>Key Moments</p>
                  <div style={{ display: 'flex', flexDirection: 'column' }}>
                    {analysis.key_moments.map((m, i) => (
                      <div key={i} style={{ display: 'flex', gap: 10, padding: '8px 0', borderTop: i === 0 ? 'none' : '1px solid rgba(255,255,255,0.04)', alignItems: 'flex-start' }}>
                        <span style={{ fontSize: 10, fontFamily: 'JetBrains Mono, monospace', color: 'var(--text-muted)', paddingTop: 1, flexShrink: 0 }}>
                          {String(i + 1).padStart(2, '0')}
                        </span>
                        <span style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>{m}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Column 3: Pipeline */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <p style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0 }}>
              Pipeline
            </p>
            <button className="btn btn-ghost" style={{ padding: '4px 6px', fontSize: 11, color: 'var(--text-muted)' }} onClick={loadStages}>
              <RefreshCw size={12} />
            </button>
          </div>
          <PipelineStepper stages={stages} />
        </div>

      </div>
    </div>
  );
}
