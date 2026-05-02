import { Worker } from 'bullmq';
import axios from 'axios';
import { redisConnection } from '../redis';

const BACKEND_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

// ── Ingestion Worker (Stage 1) ─────────────────────────────────────────────
export const ingestionWorker = new Worker(
  'event-ingestion',
  async (job) => {
    console.log(`[IngestionWorker] Processing job ${job.id}`, job.data);
    const { event_id, raw_data } = job.data;
    try {
      await axios.post(`${BACKEND_URL}/internal/ingest`, { event_id, raw_data });
    } catch (e: any) {
      console.error(`[IngestionWorker] Failed: ${e.message}`);
      throw e;
    }
    return { event_id, processed: true };
  },
  {
    connection: redisConnection,
    concurrency: 5,
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
  }
);

// ── Accumulation Worker (Stage 2) ─────────────────────────────────────────
export const accumulationWorker = new Worker(
  'stream-accumulation',
  async (job) => {
    console.log(`[AccumulationWorker] Processing job ${job.id}`);
    const { event_id, normalized } = job.data;
    try {
      await axios.post(`${BACKEND_URL}/internal/accumulate/${event_id}`, { normalized });
    } catch (e: any) {
      console.error(`[AccumulationWorker] Failed: ${e.message}`);
      throw e;
    }
    return { event_id, accumulated: true };
  },
  {
    connection: redisConnection,
    concurrency: 3,
  }
);

// ── Commentary Worker (Stage 3) ───────────────────────────────────────────
export const commentaryWorker = new Worker(
  'groq-commentary',
  async (job) => {
    console.log(`[CommentaryWorker] Job ${job.id} for event ${job.data.event_id}`);
    const { event_id, normalized } = job.data;
    try {
      await axios.post(`${BACKEND_URL}/internal/commentary/${event_id}`, { normalized });
    } catch (e: any) {
      console.error(`[CommentaryWorker] Failed: ${e.message}`);
      throw e;
    }
    return { event_id, commentary_triggered: true };
  },
  {
    connection: redisConnection,
    concurrency: 2,
    limiter: { max: 10, duration: 60000 },
  }
);

// ── Analysis Worker (Stage 4) ─────────────────────────────────────────────
export const analysisWorker = new Worker(
  'gemini-analysis',
  async (job) => {
    console.log(`[AnalysisWorker] Job ${job.id} for event ${job.data.event_id}`);
    const { event_id } = job.data;
    try {
      await axios.post(`${BACKEND_URL}/internal/analysis/${event_id}`);
    } catch (e: any) {
      console.error(`[AnalysisWorker] Failed: ${e.message}`);
      throw e;
    }
    return { event_id, analysis_triggered: true };
  },
  {
    connection: redisConnection,
    concurrency: 2,
    limiter: { max: 12, duration: 60000 },
  }
);

// ── Alert Worker (Stage 7) ─────────────────────────────────────────────────
export const alertWorker = new Worker(
  'alert-rules',
  async (job) => {
    console.log(`[AlertWorker] Evaluating rules for event ${job.data.event_id}`);
    const { event_id } = job.data;
    try {
      await axios.post(`${BACKEND_URL}/internal/alerts/${event_id}`);
    } catch (e: any) {
      console.error(`[AlertWorker] Failed: ${e.message}`);
      throw e;
    }
    return { event_id, rules_evaluated: true };
  },
  {
    connection: redisConnection,
    concurrency: 5,
  }
);

// ── Report Worker (Stage 8) ───────────────────────────────────────────────
export const reportWorker = new Worker(
  'post-event-report',
  async (job) => {
    console.log(`[ReportWorker] Generating report for event ${job.data.event_id}`);
    const { event_id } = job.data;
    try {
      await axios.post(`${BACKEND_URL}/internal/reports/${event_id}`);
    } catch (e: any) {
      console.error(`[ReportWorker] Failed to trigger report: ${e.message}`);
      throw e;
    }
    return { event_id, report_generated: true };
  },
  {
    connection: redisConnection,
    concurrency: 1,
    attempts: 2,
    backoff: { type: 'fixed', delay: 5000 },
  }
);

// ── Worker Event Handlers ─────────────────────────────────────────────────
const workers = [
  { name: 'Ingestion', worker: ingestionWorker },
  { name: 'Accumulation', worker: accumulationWorker },
  { name: 'Commentary', worker: commentaryWorker },
  { name: 'Analysis', worker: analysisWorker },
  { name: 'Alert', worker: alertWorker },
  { name: 'Report', worker: reportWorker },
];

workers.forEach(({ name, worker }) => {
  worker.on('completed', (job) => {
    console.log(`[${name}Worker] Job ${job.id} completed`);
  });
  worker.on('failed', (job, err) => {
    console.error(`[${name}Worker] Job ${job?.id} failed:`, err.message);
  });
  worker.on('active', (job) => {
    console.log(`[${name}Worker] Job ${job.id} started`);
  });
});

export default workers;
