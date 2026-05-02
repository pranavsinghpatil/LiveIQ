import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Brain } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface Commentary {
  id: string;
  text: string;
  model: string;
  latency_ms?: number;
  created_at: string;
}

export function CommentaryFeed({ items }: { items: Commentary[] }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, maxHeight: 400, overflowY: 'auto' }}>
      <AnimatePresence mode="popLayout">
        {items.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '24px 0', fontSize: 14 }}>
            Waiting for live commentary...
          </div>
        )}
        {items.map((item) => (
          <motion.div
            key={item.id}
            layout
            initial={{ opacity: 0, y: -8, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className={`commentary-item ${item.model.includes('groq') ? 'groq' : 'gemini'}`}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                {item.model.includes('groq') ? <Zap size={12} color="var(--accent-cyan)" /> : <Brain size={12} color="var(--accent-secondary)" />}
                <span style={{ fontSize: 11, fontWeight: 600, color: item.model.includes('groq') ? 'var(--accent-cyan)' : 'var(--accent-secondary)' }}>
                  {item.model.includes('groq') ? 'Groq Llama' : 'Gemini'}
                </span>
                {item.latency_ms && (
                  <span style={{ fontSize: 10, color: 'var(--text-muted)', fontFamily: 'JetBrains Mono, monospace' }}>
                    {item.latency_ms}ms
                  </span>
                )}
              </div>
              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                {formatDistanceToNow(new Date(item.created_at), { addSuffix: true })}
              </span>
            </div>
            <p style={{ fontSize: 14, lineHeight: 1.5, color: 'var(--text-primary)' }}>{item.text}</p>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
