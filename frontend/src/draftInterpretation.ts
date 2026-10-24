import type { Content } from './PrivateDrafts';

// Compare persisted facts with the original interpretation, never the last save.
// Stable activity IDs also distinguish manual additions from removed source rows.
export const sourceFields: Record<string, string> = { type: 'kind', raw_code: 'label', start: 'start_instant', end: 'end_instant', source_start: 'start', source_end: 'end', from_place: 'origin', to_place: 'destination', trip: 'trip_id', line: 'line' };
export function originalActivity(content: Content, id: string): Record<string, string | null> | undefined {
  const source = content.import_metadata?.activities.find(row => row.activity_id === id);
  if (!source) return;
  return Object.fromEntries(Object.entries(sourceFields).map(([field, key]) => [field, field === 'type'
    ? source.origins.kind === 'unresolved' ? null : source.kind === 'deadhead_car' ? 'Tomkjøring med CAR' : source.kind
    : source[key]]));
}
export function sameFact(field: string, current: string | null, original: string | null): boolean {
  if (current === original) return true;
  if ((field === 'start' || field === 'end') && current && original) return Date.parse(current) === Date.parse(original);
  if ((field === 'source_start' || field === 'source_end') && current && original) {
    const clock = (value: string) => /^\d{1,2}:\d{2}(:00)?$/.test(value) ? value.split(':').slice(0, 2).map(Number).join(':') : value;
    return clock(current) === clock(original);
  }
  return false;
}
// Python str.strip's explicit whitespace set, used by activity assessment.
// Unlike bus absence, U+001C–001F count as blank here; FEFF remains meaningful.
export const activityFactMissing = (value: string | null | undefined): boolean => value == null || /^[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]*$/u.test(value);
export const displayFact = (field: string, value: string | null | undefined) => (field === 'type' || field === 'kind' || field === 'raw_code' || field === 'label') && (value === 'trip' || value === 'Trip') ? 'tur' : value;
export function currentUncertainty(content: Content, activity: Content['activities'][number], trim = true): string {
  let value = activity.uncertainty ?? '';
  // Exact retained document fragments are neutral even with unknown positions;
  // this does not attach an unlocated annotation to the displayed activity.
  for (const marker of sourceMarkers(content)) value = value.split(marker.fragment).join('');
  return trim ? value.replace(/^[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+|[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+$/gu, '') : value;
}
export function currentUnknowns(activity: Content['activities'][number]): string[] {
  const result = [['type', 'aktivitetstype'], ['start', 'start'], ['end', 'slutt'], ['from_place', 'fra sted'], ['to_place', 'til sted']].filter(([field]) => activityFactMissing(activity[field])).map(([, label]) => label);
  if (activity.type === 'trip' && activityFactMissing(activity.trip)) result.push('turnummer');
  if (activity.type === 'trip' && activityFactMissing(activity.line)) result.push('linje');
  if (activity.type === 'trip' && activityFactMissing(activity.direction)) result.push('retning');
  return result;
}

export type DutyChange = { from_activity_id: string; vehicle_duty: string | null; realtime_duty: string | null };
export const dutySuffix = (duty: string | null) => duty?.match(/([0-9]{3})$/)?.[1] ?? null;
export function dutyChanges(content: Content): DutyChange[] {
  if (content.vehicle_duty_changes !== undefined) return content.vehicle_duty_changes;
  const metadata = content.import_metadata;
  if (!metadata) return [];
  let previous = metadata.duties[0]?.value;
  const changes: DutyChange[] = [];
  for (const duty of metadata.duties) {
    const anchor = metadata.activities[duty.after_activity]?.activity_id;
    if (duty.value !== previous && anchor && content.activities.some(activity => activity.id === anchor)) {
      changes.push({ from_activity_id: anchor, vehicle_duty: duty.value, realtime_duty: dutySuffix(duty.value) });
      previous = duty.value;
    }
  }
  return changes;
}
export function effectiveDuty(content: Content, index: number): string | null {
  const changes = dutyChanges(content);
  let duty = content.vehicle_duty;
  for (const activity of content.activities.slice(0, index + 1)) {
    const change = changes.find(value => value.from_activity_id === activity.id);
    if (change) duty = change.vehicle_duty;
  }
  return duty;
}
export function importIssues(content: Content): { activityId?: string; text: string }[] {
  const metadata = content.import_metadata;
  if (!metadata) return [];
  const result: { activityId?: string; text: string }[] = metadata.unresolved.map(issue => {
    const names: Record<string, string> = {
      unresolved_time: `Kontroller ${issue.field === 'start' ? 'start' : issue.field === 'end' ? 'slutt' : 'tidspunkt'}: klokkeslett eller kalenderdato er ukjent.`,
      missing_endpoint: 'Endested mangler i tolkningen. Kontroller mot kilden.',
      unrecognized_source_line: 'En kilderad kunne ikke tolkes. Kontroller kilden.',
      unproven_calendar_interval: 'Kalenderdatoene kunne ikke fastslås fra skiftintervallet.',
      reversed_activity_time: 'Slutt ligger før start. Kontroller dato og klokkeslett.',
    };
    const source = metadata.activities.find(activity => activity.source_order === issue.activity);
    const point = issue.provenance;
    return { activityId: source?.activity_id, text: (names[issue.code] ?? `Ukjent kildeusikkerhet (${issue.code}).`) + (point ? ` Side ${point.page}${point.column ? `, kolonne ${point.column}` : ''}${point.line ? `, linje ${point.line}` : ''}.` : '') };
  });
  for (const source of metadata.activities) {
    if (source.origins.kind === 'unresolved') result.push({ activityId: source.activity_id, text: 'Aktivitetstypen er uavklart.' });
  }
  const seen = new Set<string>();
  return result.filter(issue => {
    const key = (issue.activityId ?? '') + ':' + issue.text;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}
type Marker = { activityId?: string; text: string; fragment: string };
const markerCache = new WeakMap<Content, Marker[]>();
export function sourceMarkers(content: Content): Marker[] {
  const cached = markerCache.get(content);
  if (cached) return cached;
  const metadata = content.import_metadata;
  if (!metadata) return [];
  const result: { activityId?: string; text: string; fragment: string }[] = [];
  for (const marker of metadata.annotations) {
    const candidates: { line: number; id: string; order: number }[] = [];
    for (const source of metadata.activities) for (const points of Object.values(source.provenance)) {
      if (Array.isArray(points)) for (const point of points) {
        if (marker.provenance.line != null && marker.provenance.column != null && point.line != null && point.page === marker.provenance.page && point.column === marker.provenance.column && point.line <= marker.provenance.line) candidates.push({ line: point.line, id: source.activity_id, order: source.source_order });
      }
    }
    candidates.sort((a, b) => b.line - a.line || b.order - a.order);
    result.push({ activityId: candidates[0]?.id, text: `Kildemerke: ${marker.value} (side ${marker.provenance.page}).`, fragment: `Kildemerket ${marker.value} har ukjent betydning (side ${marker.provenance.page}).` });
  }
  markerCache.set(content, result);
  return result;
}
