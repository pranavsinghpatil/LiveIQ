import express from 'express';
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';
import { allQueues } from '../queues';

export function setupBullBoard(app: express.Application) {
  const serverAdapter = new ExpressAdapter();
  serverAdapter.setBasePath('/admin/queues');

  createBullBoard({
    queues: allQueues.map((q) => new BullMQAdapter(q)),
    serverAdapter,
  });

  app.use('/admin/queues', serverAdapter.getRouter());
  console.log('[BullBoard] Mounted at /admin/queues');
}
