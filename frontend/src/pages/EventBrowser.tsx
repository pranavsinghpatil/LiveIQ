import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Search, Filter, Star, StarOff, Trophy, Clock } from 'lucide-react';
import api from '../lib/api';
import { toast } from '../components/Toast';

interface Event {
  id: string; sport: string; league?: string;
  home_team: string; away_team: string;
  home_score?: string; away_score?: string;
  status: string; venue?: string; event_date?: string;
}

const SPORTS = ['All', 'Subscribed', 'Soccer', 'Basketball', 'Tennis'];
const STATUS_MAP: Record<string, string> = {
  'In Progress': 'live', 'NotStarted': 'pending', 'Final': 'done', 'FT': 'done', 'Finished': 'done',
};

export default function EventBrowser() {
  const [events, setEvents] = useState<Event[]>([]);
  const [search, setSearch] = useState('');
  const [sport, setSport] = useState('All');
  const [subscribed, setSubscribed] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadEvents();
    loadSubscriptions();
  }, [sport]);

  async function loadEvents() {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (sport !== 'All') params.sport = sport;
      const res = await api.get('/api/events', { params });
      setEvents(res.data);
    } catch { toast.error('Failed to load events'); }
    finally { setLoading(false); }
  }

  async function loadSubscriptions() {
    try {
      const res = await api.get('/api/events/my/subscriptions');
      setSubscribed(new Set(res.data.map((s: any) => s.event_id)));
    } catch {}
  }

  async function toggleSubscription(eventId: string, e: React.MouseEvent) {
    e.stopPropagation();
    try {
      if (subscribed.has(eventId)) {
        await api.delete(`/api/events/${eventId}/subscribe`);
        setSubscribed(prev => { const n = new Set(prev); n.delete(eventId); return n; });
        toast.info('Unsubscribed from event');
      } else {
        await api.post(`/api/events/${eventId}/subscribe`);
        setSubscribed(prev => new Set([...prev, eventId]));
        toast.success('Subscribed! You\'ll receive live updates.');
      }
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Subscription failed');
    }
  }

  const filtered = events.filter(e => {
    const matchesSearch = `${e.home_team} ${e.away_team} ${e.league}`.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = sport === 'All' ? true : sport === 'Subscribed' ? subscribed.has(e.id) : e.sport === sport;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Event Browser</h1>
        <p className="page-subtitle">Browse live and upcoming sports events across the globe</p>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 32, flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: 1, minWidth: 200 }}>
          <Search size={15} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input id="event-search" className="input" placeholder="Search teams, leagues..." value={search}
            onChange={e => setSearch(e.target.value)} style={{ paddingLeft: 36 }} />
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {SPORTS.map(s => (
            <motion.button key={s} 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`btn ${sport === s ? 'btn-primary' : 'btn-ghost'}`}
              onClick={() => setSport(s)}>{s}</motion.button>
          ))}
        </div>
      </div>

      {/* Stats row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 32 }}>
        {[
          { label: 'Total Events', value: events.length },
          { label: 'Live Now', value: events.filter(e => e.status === 'In Progress').length },
          { label: 'Upcoming', value: events.filter(e => e.status === 'NotStarted').length },
          { label: 'Subscribed', value: subscribed.size },
        ].map(stat => (
          <motion.div key={stat.label} className="card" style={{ padding: '20px' }} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            <div className="stat-value" style={{ fontSize: 28, fontFamily: 'JetBrains Mono', fontWeight: 700, marginBottom: 4 }}>{stat.value}</div>
            <div className="stat-label" style={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Event grid */}
      {loading ? (
        <div className="glass card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 0' }}>
          <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 2 }} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
            <Trophy size={32} color="var(--accent-cyan)" style={{ filter: 'drop-shadow(0 0 10px rgba(0,240,255,0.5))' }} />
            <span style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent-cyan)', fontWeight: 800 }}>Loading Events...</span>
          </motion.div>
        </div>
      ) : filtered.length === 0 ? (
        <div className="glass card empty-state" style={{ padding: '80px 40px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 24, border: '1px solid var(--border)' }}>
            <Search size={24} color="var(--text-muted)" />
          </div>
          <h2 style={{ fontSize: 24, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 8 }}>No Events Found</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Try adjusting your search query or sport filter.</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 16 }}>
          {filtered.map((event, i) => (
            <motion.div
              key={event.id}
              className="card event-card"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03 }}
              onClick={() => navigate(`/live?event=${event.id}`)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                <div>
                  <span className={`badge badge-${STATUS_MAP[event.status] || 'pending'}`}>
                    {event.status === 'In Progress' && <span className="live-dot" style={{ width: 6, height: 6 }} />}
                    {event.status?.toUpperCase()}
                  </span>
                  <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    {event.league || event.sport}
                  </div>
                </div>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  id={`subscribe-${event.id}`}
                  className={`btn ${subscribed.has(event.id) ? 'btn-primary' : 'btn-ghost'}`}
                  style={{ padding: '8px', minWidth: 'unset', borderRadius: '50%' }}
                  onClick={e => toggleSubscription(event.id, e as any)}
                  title={subscribed.has(event.id) ? 'Unsubscribe' : 'Subscribe'}
                >
                  {subscribed.has(event.id) ? <Star size={16} fill="currentColor" /> : <StarOff size={16} />}
                </motion.button>
              </div>

              <div className="event-teams" style={{ marginBottom: 8 }}>
                {event.home_team} <span style={{ color: 'var(--text-muted)', fontWeight: 400 }}>vs</span> {event.away_team}
              </div>

              {(event.home_score !== undefined && event.away_score !== undefined) && (
                <div className="event-score" style={{ marginBottom: 8, fontSize: 24, fontWeight: 700, fontFamily: 'JetBrains Mono', letterSpacing: '-1px' }}>
                  {event.home_score || '0'} — {event.away_score || '0'}
                </div>
              )}

              <div style={{ display: 'flex', gap: 12, fontSize: 11, color: 'var(--text-muted)', marginTop: 12 }}>
                {event.venue && <span>{event.venue.toUpperCase()}</span>}
                {event.event_date && <span><Clock size={11} style={{ display: 'inline', marginBottom: -2 }} /> {event.event_date.slice(0, 10)}</span>}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
