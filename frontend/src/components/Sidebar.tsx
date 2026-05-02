import { NavLink, useNavigate } from 'react-router-dom';
import { Tv, List, Zap, BarChart3, Bell, FileText, Settings, LogOut, Radio } from 'lucide-react';
import { useAuthStore } from '../lib/auth';
import { motion } from 'framer-motion';

const NAV = [
  { to: '/events', icon: <List size={17} />, label: 'Event Browser' },
  { to: '/live', icon: <Radio size={17} />, label: 'Live Event' },
  { to: '/analysis', icon: <Zap size={17} />, label: 'AI Analysis' },
  { to: '/predictions', icon: <BarChart3 size={17} />, label: 'Predictions' },
  { to: '/alerts', icon: <Bell size={17} />, label: 'Alert Manager' },
  { to: '/reports', icon: <FileText size={17} />, label: 'Post-Event Reports' },
  { to: '/admin', icon: <Settings size={17} />, label: 'Admin Dashboard' },
];

export function Sidebar() {
  const { user, logout, isAnalyst } = useAuthStore();
  const navigate = useNavigate();

  return (
    <nav className="sidebar">
      <div className="sidebar-logo">
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ display: 'flex', alignItems: 'center', gap: 10 }}
        >
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: 'var(--gradient-primary)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Tv size={18} color="white" />
          </div>
          <div>
            <div className="logo-text">LiveIQ</div>
            <div style={{ fontSize: 10, color: 'var(--text-muted)', letterSpacing: '0.05em' }}>INTELLIGENCE PLATFORM</div>
          </div>
        </motion.div>
      </div>

      <div style={{ flex: 1 }}>
        {NAV.filter(n => n.to !== '/admin' || isAnalyst()).map((item, i) => (
          <motion.div key={item.to} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}>
            <NavLink to={item.to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              {item.icon}
              <span>{item.label}</span>
            </NavLink>
          </motion.div>
        ))}
      </div>

      <div style={{ padding: '16px 20px', borderTop: '1px solid var(--glass-border)', marginTop: 8 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
          <div style={{
            width: 32, height: 32, borderRadius: '50%',
            background: 'var(--gradient-primary)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 13, fontWeight: 700, color: 'white',
          }}>
            {user?.email?.[0]?.toUpperCase()}
          </div>
          <div style={{ overflow: 'hidden' }}>
            <div style={{ fontSize: 12, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {user?.email}
            </div>
            <span className={`badge badge-${user?.role}`} style={{ fontSize: 9 }}>{user?.role}</span>
          </div>
        </div>
        <button className="btn btn-ghost btn-sm" style={{ width: '100%' }}
          onClick={() => { logout(); navigate('/auth'); }}>
          <LogOut size={14} /> Sign out
        </button>
      </div>
    </nav>
  );
}
