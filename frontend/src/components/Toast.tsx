import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

interface Toast { id: string; type: 'success' | 'error' | 'info'; message: string; }

let listeners: ((t: Toast[]) => void)[] = [];
let toasts: Toast[] = [];

function notify(type: Toast['type'], message: string) {
  const t: Toast = { id: Math.random().toString(36).slice(2), type, message };
  toasts = [...toasts, t];
  listeners.forEach(l => l(toasts));
  setTimeout(() => {
    toasts = toasts.filter(x => x.id !== t.id);
    listeners.forEach(l => l(toasts));
  }, 4000);
}

export const toast = {
  success: (msg: string) => notify('success', msg),
  error: (msg: string) => notify('error', msg),
  info: (msg: string) => notify('info', msg),
};

export function ToastContainer() {
  const [items, setItems] = useState<Toast[]>([]);
  
  useEffect(() => {
    listeners.push(setItems);
    return () => { listeners = listeners.filter(l => l !== setItems); };
  }, []);

  const remove = (id: string) => {
    toasts = toasts.filter(t => t.id !== id);
    setItems(toasts);
  };

  const icons = {
    success: <CheckCircle2 size={18} color="var(--accent-green)" />,
    error: <AlertCircle size={18} color="var(--accent-red)" />,
    info: <Info size={18} color="var(--accent-cyan)" />
  };

  const borders = {
    success: 'rgba(16, 185, 129, 0.4)',
    error: 'rgba(239, 68, 68, 0.4)',
    info: 'rgba(0, 240, 255, 0.4)'
  };

  return (
    <div style={{
      position: 'fixed', bottom: 24, right: 24, zIndex: 9999,
      display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'flex-end',
      pointerEvents: 'none'
    }}>
      <AnimatePresence mode="popLayout">
        {items.map(t => (
          <motion.div
            key={t.id}
            layout
            initial={{ opacity: 0, y: 20, scale: 0.9, filter: 'blur(10px)' }}
            animate={{ opacity: 1, y: 0, scale: 1, filter: 'blur(0px)' }}
            exit={{ opacity: 0, scale: 0.85, filter: 'blur(10px)' }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            style={{
              background: 'rgba(10, 10, 15, 0.8)',
              backdropFilter: 'blur(40px)',
              border: `1px solid ${borders[t.type]}`,
              borderRadius: '12px',
              padding: '14px 18px',
              display: 'flex', alignItems: 'center', gap: 12,
              boxShadow: `0 8px 32px rgba(0,0,0,0.4), 0 0 20px ${borders[t.type].replace('0.4', '0.1')}`,
              pointerEvents: 'auto',
              minWidth: '280px', maxWidth: '400px'
            }}
          >
            {icons[t.type]}
            <span style={{ 
              fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', flex: 1,
              letterSpacing: '0.01em'
            }}>
              {t.message}
            </span>
            <button 
              onClick={() => remove(t.id)}
              style={{
                background: 'transparent', border: 'none', color: 'var(--text-muted)',
                cursor: 'pointer', padding: 4, display: 'flex', alignItems: 'center',
                transition: 'color 0.2s'
              }}
              onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
              onMouseOut={e => e.currentTarget.style.color = 'var(--text-muted)'}
            >
              <X size={14} />
            </button>
            
            {/* Progress bar */}
            <motion.div
              initial={{ width: '100%' }}
              animate={{ width: '0%' }}
              transition={{ duration: 4, ease: 'linear' }}
              style={{
                position: 'absolute', bottom: 0, left: 0, height: 3,
                background: borders[t.type].replace('0.4', '1'),
                borderBottomLeftRadius: 12, borderBottomRightRadius: 12
              }}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
