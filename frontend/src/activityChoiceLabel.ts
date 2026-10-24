import type { Content } from './PrivateDrafts';
import { activityFactMissing } from './draftInterpretation';
import { dayTypeLabels, osloDateTime } from './dayOverview';

// Choices share the overview's per-type identifier semantics. A missing route
// is meaningful for passenger work, but is not an invented fact on a pause.
export function activityChoiceLabel(activity: Content['activities'][number] | undefined, kind?: string): string {
  if (!activity) return 'Ukjent';
  const type = kind ?? activity.type ?? '';
  const known = (v: string | null | undefined) => activityFactMissing(v) ? 'Ukjent' : v;
  const identifiers = [['line', 'Linje'], ['trip', 'Tur'], ['direction', 'Retning']].filter(([field]) => type === 'trip'
    || field === 'trip' && ['deadhead', 'deadhead_car', 'Tomkjøring med CAR', 'CAR'].includes(type)
    || !activityFactMissing(activity[field]));
  const places = [['from_place', 'Fra'], ['to_place', 'Til']].filter(([field]) => type === 'trip' || !activityFactMissing(activity[field]));
  return [dayTypeLabels[type] ?? 'Ukjent aktivitetstype', ...identifiers.map(([field, title]) => `${title}: ${known(activity[field])}`),
    ...places.map(([field, title]) => `${title}: ${known(activity[field])}`),
    `Planlagt start: ${activity.start ? osloDateTime(activity.start) : 'Ukjent'}`].join(' · ');
}
