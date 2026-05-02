import { Queue } from 'bullmq';
import { redisConnection } from '../redis';

export const ingestionQueue = new Queue('event-ingestion', { connection: redisConnection });
export const accumulationQueue = new Queue('stream-accumulation', { connection: redisConnection });
export const commentaryQueue = new Queue('groq-commentary', { connection: redisConnection });
export const analysisQueue = new Queue('gemini-analysis', { connection: redisConnection });
export const alertQueue = new Queue('alert-rules', { connection: redisConnection });
export const reportQueue = new Queue('post-event-report', { connection: redisConnection });

export const allQueues = [
  ingestionQueue,
  accumulationQueue,
  commentaryQueue,
  analysisQueue,
  alertQueue,
  reportQueue,
];
