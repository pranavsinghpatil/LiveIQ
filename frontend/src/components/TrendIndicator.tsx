import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

type Trend = 'momentum' | 'stable' | 'reversal';

export function TrendIndicator({ trend }: { trend?: Trend }) {
  if (!trend) return null;
  const config = {
    momentum: { icon: <TrendingUp size={14} />, label: 'Momentum', color: 'var(--accent-cyan)' },
    stable:   { icon: <Minus size={14} />,       label: 'Stable',   color: 'var(--text-secondary)' },
    reversal: { icon: <TrendingDown size={14} />, label: 'Reversal', color: 'var(--accent-primary)' },
  };
  const { icon, label, color } = config[trend];
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 8,
      padding: '4px 10px', borderRadius: 4, fontSize: 11, fontWeight: 600, 
      textTransform: 'uppercase', letterSpacing: '0.05em',
      border: `1px solid rgba(255, 255, 255, 0.1)`, color: color,
      background: `color-mix(in srgb, ${color} 10%, transparent)`
    }}>
      {icon} {label}
    </span>
  );
}

export function ConfidenceBar({ value }: { value?: number }) {
  const pct = ((value ?? 0) * 100).toFixed(0);
  const color = (value ?? 0) >= 0.7 ? 'var(--accent-cyan)' : (value ?? 0) >= 0.4 ? '#f59e0b' : 'var(--accent-red)';
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        <span style={{ color: 'var(--text-muted)' }}>Confidence</span>
        <span style={{ fontWeight: 800, color, fontFamily: 'JetBrains Mono' }}>{pct}%</span>
      </div>
      <div style={{ width: '100%', height: 4, background: 'rgba(255,255,255,0.05)', borderRadius: 2, overflow: 'hidden' }}>
        <div style={{ 
          width: `${pct}%`, height: '100%', 
          background: color, 
          transition: 'width 0.8s ease' 
        }} />
      </div>
    </div>
  );
}
