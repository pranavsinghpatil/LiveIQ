import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Trash2, ToggleLeft, ToggleRight, Bell, BellOff } from 'lucide-react';
import api from '../lib/api';
import { useAuthStore } from '../lib/auth';
import { toast } from '../components/Toast';

const RULE_TYPES = [
  { value: 'keyword_detected', label: '🔤 Keyword Detected', desc: 'Alert when a keyword appears in commentary' },
  { value: 'score_threshold', label: '🎯 Score Threshold', desc: 'Alert when score gap exceeds a value' },
  { value: 'trend_change', label: '📈 Trend Change', desc: 'Alert when AI detects a trend shift' },
];

interface AlertRule { id: string; event_id: string; rule_type: string; rule_value: any; is_active: boolean; created_at: string; }
interface Alert { id: string; event_id: string; rule_type?: string; matched_rule: any; triggered_at: string; }

export default function AlertManager() {
  const { isAnalyst } = useAuthStore();
  const [rules, setRules] = useState<AlertRule[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ event_id: '', rule_type: 'keyword_detected', keyword: '', threshold: '3', operator: 'gt', trend: 'reversal' });

  useEffect(() => { loadRules(); loadAlerts(); loadEvents(); }, []);

  async function loadEvents() {
    try {
      const subRes = await api.get('/api/events/my/subscriptions');
      const evts = await Promise.all(subRes.data.map((s: any) => api.get(`/api/events/${s.event_id}`)));
      setEvents(evts.map(r => r.data));
      if (evts.length > 0 && !form.event_id) setForm(f => ({ ...f, event_id: evts[0].data.id }));
    } catch {}
  }
  async function loadRules() { try { const r = await api.get('/api/alerts/rules'); setRules(r.data); } catch {} }
  async function loadAlerts() { try { const r = await api.get('/api/alerts/history'); setAlerts(r.data); } catch {} }

  async function createRule() {
    const rule_value: any = {};
    if (form.rule_type === 'keyword_detected') rule_value.keyword = form.keyword;
    else if (form.rule_type === 'score_threshold') { rule_value.threshold = Number(form.threshold); rule_value.operator = form.operator; }
    else rule_value.trend = form.trend;
    try {
      await api.post('/api/alerts/rules', { event_id: form.event_id, rule_type: form.rule_type, rule_value });
      toast.success('Alert rule created!'); setShowForm(false); loadRules();
    } catch (e: any) { toast.error(e.response?.data?.detail || 'Failed'); }
  }

  async function deleteRule(id: string) {
    try { await api.delete(`/api/alerts/rules/${id}`); toast.info('Rule deleted'); loadRules(); } catch { toast.error('Failed'); }
  }
  async function toggleRule(id: string) {
    try { await api.patch(`/api/alerts/rules/${id}/toggle`); loadRules(); } catch {}
  }

  if (!isAnalyst()) return (
    <div className="page"><div className="glass card" style={{ padding: 40, textAlign: 'center' }}>
      <Bell size={40} style={{ opacity: 0.3, marginBottom: 12 }} />
      <p>Alert Manager is available for <span style={{ color: 'var(--accent-primary)' }}>Analyst</span> role only.</p>
    </div></div>
  );

  return (
    <div className="page">
      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 className="page-title">🔔 Alert Manager</h1>
            <p className="page-subtitle">Define custom alert rules — keyword, score threshold, trend changes</p>
          </div>
          <button id="create-rule-btn" className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            <Plus size={15} /> New Rule
          </button>
        </div>
      </div>

      {/* Create rule form */}
      {showForm && (
        <motion.div className="glass card" initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: 20 }}>
          <div className="section-label">Create Alert Rule</div>
          <div className="grid-2" style={{ gap: 16 }}>
            <div className="form-group">
              <label className="form-label">Event</label>
              <select id="rule-event" className="input" value={form.event_id} onChange={e => setForm(f => ({ ...f, event_id: e.target.value }))}>
                {events.map(e => <option key={e.id} value={e.id}>{e.home_team} vs {e.away_team}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Rule Type</label>
              <select id="rule-type" className="input" value={form.rule_type} onChange={e => setForm(f => ({ ...f, rule_type: e.target.value }))}>
                {RULE_TYPES.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
              </select>
            </div>
          </div>

          {form.rule_type === 'keyword_detected' && (
            <div className="form-group">
              <label className="form-label">Keyword (e.g. "injury", "penalty")</label>
              <input id="rule-keyword" className="input" placeholder="injury" value={form.keyword} onChange={e => setForm(f => ({ ...f, keyword: e.target.value }))} />
            </div>
          )}
          {form.rule_type === 'score_threshold' && (
            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Score Gap</label>
                <input id="rule-threshold" type="number" className="input" value={form.threshold} onChange={e => setForm(f => ({ ...f, threshold: e.target.value }))} />
              </div>
              <div className="form-group">
                <label className="form-label">Operator</label>
                <select id="rule-operator" className="input" value={form.operator} onChange={e => setForm(f => ({ ...f, operator: e.target.value }))}>
                  <option value="gt">Greater than (&gt;)</option>
                  <option value="lt">Less than (&lt;)</option>
                  <option value="gte">Greater or equal (&gt;=)</option>
                </select>
              </div>
            </div>
          )}
          {form.rule_type === 'trend_change' && (
            <div className="form-group">
              <label className="form-label">Target Trend</label>
              <select id="rule-trend" className="input" value={form.trend} onChange={e => setForm(f => ({ ...f, trend: e.target.value }))}>
                <option value="reversal">Reversal</option>
                <option value="momentum">Momentum</option>
                <option value="stable">Stable</option>
              </select>
            </div>
          )}
          <div style={{ display: 'flex', gap: 8 }}>
            <button id="save-rule-btn" className="btn btn-primary" onClick={createRule}>Save Rule</button>
            <button className="btn btn-ghost" onClick={() => setShowForm(false)}>Cancel</button>
          </div>
        </motion.div>
      )}

      <div className="grid-2">
        {/* Active rules */}
        <div>
          <div className="section-label">Active Rules ({rules.length}/5 max)</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {rules.map((rule, i) => (
              <motion.div key={rule.id} className="glass card" initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>
                      {RULE_TYPES.find(r => r.value === rule.rule_type)?.label}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)', fontFamily: 'JetBrains Mono' }}>
                      {JSON.stringify(rule.rule_value)}
                    </div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>Event: {rule.event_id.slice(0, 8)}...</div>
                  </div>
                  <div style={{ display: 'flex', gap: 6 }}>
                    <button className="btn btn-ghost btn-sm" onClick={() => toggleRule(rule.id)} title={rule.is_active ? 'Disable' : 'Enable'}>
                      {rule.is_active ? <ToggleRight size={15} color="var(--accent-green)" /> : <ToggleLeft size={15} />}
                    </button>
                    <button className="btn btn-ghost btn-sm" onClick={() => deleteRule(rule.id)}><Trash2 size={13} /></button>
                  </div>
                </div>
                <div style={{ marginTop: 8 }}>
                  <span className={`badge ${rule.is_active ? 'badge-live' : 'badge-pending'}`}>{rule.is_active ? 'Active' : 'Disabled'}</span>
                </div>
              </motion.div>
            ))}
            {rules.length === 0 && <div style={{ color: 'var(--text-muted)', fontSize: 14, padding: '16px 0' }}>No rules yet. Create your first alert rule above.</div>}
          </div>
        </div>

        {/* Alert history */}
        <div>
          <div className="section-label">Alert History</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {alerts.map((alert, i) => (
              <motion.div key={alert.id} className="glass card" initial={{ opacity: 0, x: 8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}
                style={{ borderColor: 'rgba(239,68,68,0.2)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600 }}>🔔 {alert.matched_rule?.rule_type?.replace(/_/g, ' ')}</div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{JSON.stringify(alert.matched_rule?.matched_data || {})}</div>
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{new Date(alert.triggered_at).toLocaleTimeString()}</div>
                </div>
              </motion.div>
            ))}
            {alerts.length === 0 && <div style={{ color: 'var(--text-muted)', fontSize: 14, padding: '16px 0' }}>No alerts triggered yet.</div>}
          </div>
        </div>
      </div>
    </div>
  );
}
