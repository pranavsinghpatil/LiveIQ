import { useState } from 'react';

interface Toast { id: string; type: 'success' | 'error' | 'info'; message: string; }

let listeners: ((t: Toast[]) => void)[] = [];
let toasts: Toast[] = [];

function notify(type: Toast['type'], message: string) {
  const t: Toast = { id: Math.random().toString(36).slice(2), type, message };
  toasts = [...toasts, t];
  listeners.forEach(l => l(toasts));
  setTimeout(() => {
    toasts = toasts.filter(x => x.id !== t.id);
    listeners.forEach(l => l(toasts));
  }, 4000);
}

export const toast = {
  success: (msg: string) => notify('success', msg),
  error: (msg: string) => notify('error', msg),
  info: (msg: string) => notify('info', msg),
};

export function ToastContainer() {
  const [items, setItems] = useState<Toast[]>([]);
  listeners = [setItems];
  return (
    <div className="toast-container">
      {items.map(t => (
        <div key={t.id} className={`toast toast-${t.type}`}>{t.message}</div>
      ))}
    </div>
  );
}
