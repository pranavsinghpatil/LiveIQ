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

const SPORTS = ['All', 'Soccer', 'Basketball', 'Tennis'];
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

  const filtered = events.filter(e =>
    `${e.home_team} ${e.away_team} ${e.league}`.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">🏟️ Event Browser</h1>
        <p className="page-subtitle">Browse live and upcoming sports events across the globe</p>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 24, flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: 1, minWidth: 200 }}>
          <Search size={15} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input id="event-search" className="input" placeholder="Search teams, leagues..." value={search}
            onChange={e => setSearch(e.target.value)} style={{ paddingLeft: 36 }} />
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {SPORTS.map(s => (
            <button key={s} className={`btn ${sport === s ? 'btn-primary' : 'btn-ghost'} btn-sm`}
              onClick={() => setSport(s)}>{s}</button>
          ))}
        </div>
      </div>

      {/* Stats row */}
      <div className="grid-4" style={{ marginBottom: 24 }}>
        {[
          { label: 'Total Events', value: events.length, icon: '📊' },
          { label: 'Live Now', value: events.filter(e => e.status === 'In Progress').length, icon: '🔴' },
          { label: 'Upcoming', value: events.filter(e => e.status === 'NotStarted').length, icon: '⏰' },
          { label: 'Subscribed', value: subscribed.size, icon: '⭐' },
        ].map(stat => (
          <motion.div key={stat.label} className="glass stat-card" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            <div style={{ fontSize: 28 }}>{stat.icon}</div>
            <div className="stat-value" style={{ fontSize: 28 }}>{stat.value}</div>
            <div className="stat-label">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Event grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '48px', color: 'var(--text-muted)' }}>Loading events...</div>
      ) : (
        <div className="grid-3" style={{ gap: 14 }}>
          {filtered.map((event, i) => (
            <motion.div
              key={event.id}
              className="glass event-card"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03 }}
              onClick={() => navigate(`/live?event=${event.id}`)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                <div>
                  <span className={`badge badge-${STATUS_MAP[event.status] || 'pending'}`}>
                    {event.status === 'In Progress' && <span className="live-dot" style={{ width: 6, height: 6 }} />}
                    {event.status}
                  </span>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
                    🏆 {event.league || event.sport}
                  </div>
                </div>
                <button
                  id={`subscribe-${event.id}`}
                  className={`btn btn-sm ${subscribed.has(event.id) ? 'btn-primary' : 'btn-ghost'}`}
                  onClick={e => toggleSubscription(event.id, e)}
                  title={subscribed.has(event.id) ? 'Unsubscribe' : 'Subscribe'}
                >
                  {subscribed.has(event.id) ? <Star size={13} fill="currentColor" /> : <StarOff size={13} />}
                </button>
              </div>

              <div className="event-teams" style={{ marginBottom: 8 }}>
                {event.home_team} <span style={{ color: 'var(--text-muted)' }}>vs</span> {event.away_team}
              </div>

              {(event.home_score !== undefined && event.away_score !== undefined) && (
                <div className="event-score" style={{ marginBottom: 8 }}>
                  {event.home_score || '0'} — {event.away_score || '0'}
                </div>
              )}

              <div style={{ display: 'flex', gap: 12, fontSize: 12, color: 'var(--text-muted)' }}>
                {event.venue && <span>📍 {event.venue}</span>}
                {event.event_date && <span><Clock size={11} style={{ display: 'inline' }} /> {event.event_date.slice(0, 10)}</span>}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
