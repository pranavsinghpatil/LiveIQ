import IORedis from 'ioredis';
import dotenv from 'dotenv';
dotenv.config();

export const redisConnection = new IORedis(
  process.env.QUEUE_REDIS_URL || 'redis://localhost:6379',
  { maxRetriesPerRequest: null }
);

redisConnection.on('connect', () => console.log('[Redis] Connected'));
redisConnection.on('error', (err) => console.error('[Redis] Error:', err));
