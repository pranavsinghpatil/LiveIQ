import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Brain, Radio } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface Commentary {
  id: string;
  text: string;
  model: string;
  latency_ms?: number;
  created_at: string;
}

export function CommentaryFeed({ items }: { items: Commentary[] }) {
  const isGroq = items.length > 0 && items[0].model?.toLowerCase().includes('groq');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>

      {/* Header */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        marginBottom: 16, paddingBottom: 14,
        borderBottom: '1px solid rgba(255,255,255,0.06)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Radio size={13} color="var(--text-muted)" />
          <span style={{ fontSize: 12, fontWeight: 500, color: 'var(--text-secondary)' }}>
            Live Commentary
          </span>
        </div>
        {items.length > 0 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
            {isGroq
              ? <Zap size={11} color="var(--text-muted)" />
              : <Brain size={11} color="var(--text-muted)" />
            }
            <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
              {isGroq ? 'Groq Llama' : 'Gemini'}
            </span>
          </div>
        )}
      </div>

      {/* Feed */}
      <div style={{ flex: 1, overflowY: 'auto', paddingRight: 4, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <AnimatePresence mode="popLayout" initial={false}>
          {items.length === 0 ? (
            <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '48px 0', fontSize: 13 }}>
              Waiting for live commentary...
            </div>
          ) : items.map((item, idx) => (
            <motion.div
              key={item.id}
              layout
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25, ease: 'easeOut' }}
            >
              <div style={{
                padding: '12px 0',
                borderBottom: '1px solid rgba(255,255,255,0.04)',
              }}>
                {/* Timestamp — only on latest */}
                {idx === 0 && (
                  <div style={{
                    fontSize: 10, color: 'var(--text-muted)', marginBottom: 5,
                    fontFamily: 'JetBrains Mono, monospace', letterSpacing: '0.02em'
                  }}>
                    just now
                  </div>
                )}
                <p style={{
                  fontSize: 13.5,
                  lineHeight: 1.6,
                  color: idx === 0
                    ? 'var(--text-primary)'
                    : idx < 4
                      ? 'var(--text-secondary)'
                      : 'var(--text-muted)',
                  margin: 0,
                  fontWeight: idx === 0 ? 500 : 400,
                  transition: 'color 0.5s ease',
                }}>
                  {item.text}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Footer count */}
      {items.length > 0 && (
        <div style={{ paddingTop: 12, borderTop: '1px solid rgba(255,255,255,0.04)', marginTop: 4 }}>
          <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
            {items.length} update{items.length !== 1 ? 's' : ''} this session
          </span>
        </div>
      )}
    </div>
  );
}
