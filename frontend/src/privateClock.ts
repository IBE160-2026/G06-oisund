// Memory only. A slow/frozen device clock must never prolong private authority.
// Keep fast-device-clock rejection, and never move the server estimate backwards.
let anchor: { instant: number; elapsed: number } | null = null;
export function privateNow() {
  return Math.max(Date.now(), anchor ? anchor.instant + performance.now() - anchor.elapsed : -Infinity);
}
export function observePrivateTime(value: string | null, requestedAt: number, rounded = false) {
  const instant = value === null ? NaN : Date.parse(value);
  if (!Number.isFinite(instant)) return;
  const elapsed = performance.now();
  // HTTP Date has second precision: use its upper bound, and conservatively
  // count the whole request interval, including delayed delivery/JSON parsing.
  const estimate = instant + (rounded ? 1000 : 0) + Math.max(0, elapsed - requestedAt);
  anchor = { instant: Math.max(estimate, anchor ? anchor.instant + elapsed - anchor.elapsed : -Infinity), elapsed };
}
