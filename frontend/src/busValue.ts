// Explicit Unicode White_Space. FEFF and formatting around meaningful text survive.
export const normalizeBus = (value: string | null): string | null => value === null || /^[\u0009-\u000d\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]*$/u.test(value) ? null : value;
export function busError(value: string | null): string | null {
  if (value?.includes('\0')) return 'NUL-tegn kan ikke lagres. Inndata er beholdt.';
  if (value !== null && Array.from(value).length > 100) return 'Maksimum er 100 tegn. Inndata er beholdt.';
  return null;
}
