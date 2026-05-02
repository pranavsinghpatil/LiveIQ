import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

type Trend = 'momentum' | 'stable' | 'reversal';

export function TrendIndicator({ trend }: { trend?: Trend }) {
  if (!trend) return null;
  const config = {
    momentum: { icon: <TrendingUp size={14} />, label: 'Momentum', cls: 'trend-momentum' },
    stable:   { icon: <Minus size={14} />,       label: 'Stable',   cls: 'trend-stable'   },
    reversal: { icon: <TrendingDown size={14} />, label: 'Reversal', cls: 'trend-reversal' },
  };
  const { icon, label, cls } = config[trend];
  return (
    <span className={`trend-badge ${cls}`}>
      {icon} {label}
    </span>
  );
}

export function ConfidenceBar({ value }: { value?: number }) {
  const pct = ((value ?? 0) * 100).toFixed(0);
  const color = (value ?? 0) >= 0.7 ? 'var(--accent-green)' : (value ?? 0) >= 0.4 ? 'var(--accent-yellow)' : 'var(--accent-red)';
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 6 }}>
        <span style={{ color: 'var(--text-secondary)' }}>Confidence</span>
        <span style={{ fontWeight: 700, color }}>{pct}%</span>
      </div>
      <div className="confidence-bar">
        <div className="confidence-fill" style={{ width: `${pct}%`, background: `linear-gradient(90deg, ${color}, ${color}aa)` }} />
      </div>
    </div>
  );
}
