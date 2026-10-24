import type { Content } from './PrivateDrafts';
import { dutySuffix, effectiveDuty } from './draftInterpretation';

export const dayTypeLabels: Record<string, string> = {
  trip: 'Passasjertur', deadhead: 'Tomkjøring', deadhead_car: 'Tomkjøring med CAR',
  'Tomkjøring med CAR': 'Tomkjøring med CAR', CAR: 'CAR',
  'Sign-on': 'Oppmøte', 'Sign-off': 'Avslutning', MealBreak: 'Matpause', Coffee: 'Kaffepause',
  'Split break': 'Deltskiftpause', 'Paid meal before': 'Betalt matpause før', 'Paid meal after': 'Betalt matpause etter',
  'Travel to': 'Reise til', 'Travel from': 'Reise fra', Fadder: 'Fadder', Instruktør: 'Instruktør', manual: 'Manuelt klassifisert arbeid',
};
const pauses = new Set(['MealBreak', 'Coffee', 'Split break', 'Paid meal before', 'Paid meal after']);
export type DayMember = { activity: Content['activities'][number]; index: number; kind: string; duty: string | null; suffix: string | null };
export type DayActivity = { type: 'activity'; id: string; start: string; end: string; label: string; members: DayMember[]; overlap: boolean };
export type DayGap = { type: 'gap'; id: string; start: string; end: string };
export type DayOverview = { reporting: DayMember[]; rows: (DayActivity | DayGap)[] };

// Confirmed order and calendar instants are authoritative. Source pause_groups
// describe an earlier interpretation and must never override corrected facts.
export function projectDay(content: Content, classifications: Record<string, string> = {}): DayOverview {
  const members = content.activities.map((activity, index) => {
    const duty = effectiveDuty(content, index);
    return { activity: { ...activity }, index, kind: classifications[activity.id] ?? activity.type ?? '', duty, suffix: dutySuffix(duty) };
  });
  const grouped: DayActivity[] = [];
  for (const member of members) {
    const { activity, kind } = member;
    const previous = grouped.at(-1);
    if (previous && pauses.has(kind) && previous.members.every(row => pauses.has(row.kind))
      && Date.parse(previous.end) === Date.parse(activity.start ?? '')) {
      previous.members.push(member);
      previous.end = activity.end!;
    } else grouped.push({ type: 'activity', id: activity.id, start: activity.start!, end: activity.end!, label: '', members: [member], overlap: false });
  }
  const rows: DayOverview['rows'] = [];
  let greatestEnd = -Infinity;
  let greatestEndValue = '';
  for (const row of grouped) {
    const kinds = row.members.map(member => member.kind);
    row.label = kinds.length === 1 ? dayTypeLabels[kinds[0]] ?? 'Ukjent aktivitetstype' : kinds.every(kind => pauses.has(kind))
      ? kinds.includes('MealBreak') ? 'Matpause' : kinds.includes('Split break') ? 'Deltskiftpause' : kinds.every(kind => kind === 'Coffee') ? 'Kaffepause' : 'Betalt matpause'
      : dayTypeLabels[kinds[0]] ?? 'Ukjent aktivitetstype';
    const start = Date.parse(row.start), end = Date.parse(row.end);
    if (start > greatestEnd && Number.isFinite(greatestEnd)) rows.push({ type: 'gap', id: 'gap-before-' + row.id, start: greatestEndValue, end: row.start });
    row.overlap = start < greatestEnd;
    rows.push(row);
    if (end > greatestEnd) { greatestEnd = end; greatestEndValue = row.end; }
  }
  return { reporting: members.filter(member => member.kind === 'Sign-on'), rows };
}

export const osloDateTime = (value: string) => new Intl.DateTimeFormat('nb-NO', {
  timeZone: 'Europe/Oslo', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
}).format(new Date(value));
