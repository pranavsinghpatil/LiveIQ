import express from 'express';
import dotenv from 'dotenv';
dotenv.config();

import { setupBullBoard } from './bullboard';
import workers from './workers';
import { allQueues } from './queues';
import { ingestionQueue, accumulationQueue, commentaryQueue, analysisQueue, alertQueue, reportQueue } from './queues';

const app = express();
app.use(express.json());

// ── Bull Board ──────────────────────────────────────────────────────────────
setupBullBoard(app);

// ── Internal HTTP Endpoints (called by FastAPI) ─────────────────────────────
app.post('/internal/jobs/:jobType', async (req, res) => {
  const { jobType } = req.params;
  const payload = req.body;

  try {
    switch (jobType) {
      case 'ingest':
        await ingestionQueue.add('ingest-event', payload, {
          attempts: 3,
          backoff: { type: 'exponential', delay: 1000 },
        });
        break;
      case 'accumulate':
        await accumulationQueue.add('stream-accumulation', payload, {
          attempts: 3,
          backoff: { type: 'exponential', delay: 500 },
        });
        break;
      case 'commentary':
        await commentaryQueue.add('groq-commentary', payload, {
          attempts: 2,
          backoff: { type: 'fixed', delay: 500 },
        });
        break;
      case 'analysis':
        await analysisQueue.add('gemini-analysis', payload, {
          attempts: 2,
          backoff: { type: 'fixed', delay: 2000 },
        });
        break;
      case 'alerts':
        await alertQueue.add('alert-rules', payload, {
          attempts: 2,
          backoff: { type: 'fixed', delay: 1000 },
        });
        break;
      case 'report':
        await reportQueue.add('post-event-report', payload, {
          attempts: 2,
          backoff: { type: 'fixed', delay: 5000 },
        });
        break;
      default:
        return res.status(400).json({ error: `Unknown job type: ${jobType}` });
    }
    res.json({ queued: true, jobType, payload });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// ── Queue Stats API ─────────────────────────────────────────────────────────
app.get('/api/queue-stats', async (req, res) => {
  const stats = await Promise.all(
    allQueues.map(async (queue) => {
      const counts = await queue.getJobCounts('waiting', 'active', 'completed', 'failed', 'delayed');
      return { name: queue.name, ...counts };
    })
  );
  res.json(stats);
});

// ── Failed Jobs API (Bonus: BullMQ retry dashboard) ─────────────────────────
app.get('/api/failed-jobs', async (req, res) => {
  const failedJobs = await Promise.all(
    allQueues.map(async (queue) => {
      const failed = await queue.getFailed(0, 20);
      return {
        queue: queue.name,
        jobs: failed.map((job) => ({
          id: job.id,
          name: job.name,
          data: job.data,
          failedReason: job.failedReason,
          attemptsMade: job.attemptsMade,
          timestamp: new Date(job.timestamp).toISOString(),
          processedOn: job.processedOn ? new Date(job.processedOn).toISOString() : null,
        })),
      };
    })
  );
  res.json(failedJobs);
});

// ── Health ───────────────────────────────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ status: 'ok', workers: workers.length, queues: allQueues.length });
});

const PORT = process.env.QUEUE_PORT || 3001;
app.listen(PORT, () => {
  console.log(`\n🚀 Queue Workers running on http://localhost:${PORT}`);
  console.log(`📊 Bull Board at http://localhost:${PORT}/admin/queues`);
  console.log(`🔧 ${workers.length} workers active: Ingestion, Accumulation, Commentary, Analysis, Alert, Report\n`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('[Workers] Shutting down...');
  await Promise.all(workers.map(({ worker }) => worker.close()));
  await Promise.all(allQueues.map((q) => q.close()));
  process.exit(0);
});
