import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, Loader2, XCircle } from 'lucide-react';

interface Stage {
  stage_number: number;
  stage_name: string;
  status: 'pending' | 'active' | 'done' | 'failed';
  started_at?: string;
  completed_at?: string;
}

interface FallbackStage {
  stage_number: number;
  stage_name: string;
  status: 'pending';
  started_at?: string;
  completed_at?: string;
}



function StepIcon({ status, number }: { status: Stage['status']; number: number }) {
  if (status === 'done') return <CheckCircle size={18} />;
  if (status === 'active') return <Loader2 size={18} className="animate-spin" />;
  if (status === 'failed') return <XCircle size={18} />;
  return <span style={{ fontSize: 12, fontWeight: 700 }}>{number}</span>;
}

function formatDuration(start?: string, end?: string) {
  if (!start) return null;
  const s = new Date(start).getTime();
  const e = end ? new Date(end).getTime() : Date.now();
  const ms = e - s;
  return ms < 1000 ? `${ms}ms` : `${(ms / 1000).toFixed(1)}s`;
}

export function PipelineStepper({ stages }: { stages: Stage[] }) {
  const filled: (Stage | FallbackStage)[] = stages.length > 0 ? stages : Array.from({ length: 8 }, (_, i) => ({
    stage_number: i + 1,
    stage_name: ['Event Ingestion','Stream Accumulation','Groq Commentary','Gemini Analysis','Redis Pub/Sub Publish','WebSocket Push','Alert Rule Evaluation','Post-Event Report'][i],
    status: 'pending' as const,
    started_at: undefined,
    completed_at: undefined,
  }));

  return (
    <div className="stepper">
      {filled.map((stage, idx) => (
        <motion.div
          key={stage.stage_number}
          className="step-item"
          initial={{ opacity: 0, x: -8 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.04 }}
          style={{ '--step-line-color': stage.status === 'done' ? 'rgba(16,185,129,0.4)' : 'rgba(99,102,241,0.2)' } as React.CSSProperties}
        >
          <div className={`step-icon ${stage.status}`}>
            <StepIcon status={stage.status} number={stage.stage_number} />
          </div>
          <div className="step-content">
            <div className="step-name">
              {stage.stage_name}
            </div>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 3 }}>
              <span className={`badge badge-${stage.status === 'done' ? 'done' : stage.status === 'active' ? 'live' : stage.status === 'failed' ? 'failed' : 'pending'}`} style={{ fontSize: 10 }}>
                {stage.status === 'active' && <span className="live-dot" style={{ width: 6, height: 6 }} />}
                {stage.status}
              </span>
              {stage.started_at && (
                <span className="step-time">
                  {formatDuration(stage.started_at, stage.completed_at)}
                </span>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
