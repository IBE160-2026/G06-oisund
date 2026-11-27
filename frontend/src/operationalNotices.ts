import { useEffect, useState } from 'react';


type Window = { start: string | null; end: string | null };
export type OperationalStatus = 'active' | 'upcoming' | 'uncertain';
const stamp = (value: string | null) => value ? Date.parse(value) : NaN;
let noticeClock: { instant: number; receivedAt: number } | null = null;
function operationalTime() {
  return noticeClock ? noticeClock.instant + performance.now() - noticeClock.receivedAt : Date.now();
}

export function observeOperationalTime(serverNow: string) {
  const instant = Date.parse(serverNow);
  // The server timestamp precedes receipt. A conservative lower bound keeps
  // the notice visible through its validity, independently of session clocks.
  if (Number.isFinite(instant) && (!noticeClock || instant > operationalTime())) {
    noticeClock = { instant, receivedAt: performance.now() };
  }
}

export function automaticNoticeStatus(source: { progress: string | null; windows: Window[] }, now: number): OperationalStatus | null {
  if (source.progress === 'closed') return null;
  const windows = source.windows.map(window => ({ start: stamp(window.start), end: stamp(window.end) }));
  const remaining = windows.filter(window => !Number.isFinite(window.end) || window.end > now);
  if (windows.length && !remaining.length) return null;
  if (source.progress !== 'open' || !remaining.length) return 'uncertain';
  if (remaining.some(({ start, end }) => Number.isFinite(end) && start <= now && now < end)) return 'active';
  if (remaining.every(({ start, end }) => now < start && start < end)) return 'upcoming';
  return 'uncertain';
}

export const statusLabel: Record<OperationalStatus, string> = {
  active: 'Aktiv', upcoming: 'Kommende', uncertain: 'Uavklart',
};

export function useOperationalNow(open: boolean) {
  const [now, setNow] = useState(operationalTime);
  useEffect(() => {
    if (!open) return;
    setNow(operationalTime());
    const timer = window.setInterval(() => setNow(operationalTime()), 1000);
    return () => window.clearInterval(timer);
  }, [open]);
  return now;
}
