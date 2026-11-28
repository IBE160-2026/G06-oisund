import type { Plan } from './PrivateConfirmation';
import { dayTypeLabels } from './dayOverview';
import { effectiveDuty } from './draftInterpretation';
import type { Content } from './PrivateDrafts';

type Activity = Content['activities'][number];
export const drivingClock = new Intl.DateTimeFormat('nb-NO', {timeZone:'Europe/Oslo', hour:'2-digit', minute:'2-digit', hourCycle:'h23'});
export const drivingTime = (value: string | null) => value && Number.isFinite(Date.parse(value)) ? drivingClock.format(new Date(value)) : 'Ukjent tid';
const stamp = (value: unknown) => typeof value === 'string' ? Date.parse(value) : NaN;
const usableText = (value: unknown) => typeof value === 'string' && value.trim() ? value : null;
const kindOf = (plan:Plan, activity: Activity) => plan.classifications[activity.id] ?? activity.type ?? '';

export function passengerPeriod(plan: Plan, now: number) {
  const rows = plan.draft.activities;
  const trips = rows.flatMap((activity,index) => kindOf(plan,activity) === 'trip' ? [index] : []);
  const next = trips.find(index => stamp(rows[index].start) > now);
  const previous = [...trips].reverse().find(index => stamp(rows[index].start) <= now);
  const start = previous === undefined ? 0 : previous + 1;
  const end = next ?? rows.length;
  const title = previous === undefined && next !== undefined ? 'Før første tur'
    : next !== undefined ? 'Mellom turer' : trips.length ? 'Etter siste tur' : 'Planlagt skiftarbeid';
  return {title, rows:rows.slice(start,end), offset:start, next: next === undefined ? undefined : rows[next],
    nextDuty: next === undefined ? null : effectiveDuty(plan.draft,next), final:next === undefined};
}

function places(plan: Plan, activity: Activity, index: number) {
  const rows = plan.draft.activities, header = plan.draft.import_metadata?.header;
  const kind = kindOf(plan, activity);
  let from = usableText(activity.from_place), to = usableText(activity.to_place);
  if (kind === 'Sign-on') {
    if (index === 0 && stamp(activity.start) === stamp(header?.start_instant ?? null)) from ??= usableText(header?.origin);
    else from ??= usableText(rows[index+1]?.from_place);
  }
  if (kind === 'Sign-off') {
    if (index === rows.length - 1 && stamp(activity.end) === stamp(header?.end_instant ?? null)) to ??= usableText(header?.destination);
    else to ??= usableText(rows[index-1]?.to_place);
  }
  return from && to && from !== to ? from + ' → ' + to : from ?? to;
}
export function endPlace(plan: Plan) {
  const last = plan.draft.activities.find(activity => stamp(activity.end) === stamp(plan.final_end));
  const header = plan.draft.import_metadata?.header;
  return usableText(last?.to_place) ?? (stamp(header?.end_instant ?? null) === stamp(plan.final_end) ? usableText(header?.destination) : null);
}

export function DrivingPeriodRows({plan, period, now}: {plan:Plan; period:ReturnType<typeof passengerPeriod>; now:number}) {
  let previousDuty = period.offset > 0 ? effectiveDuty(plan.draft, period.offset - 1) : null;
  return <ol className="driving-period-list" aria-label="Planlagt arbeid">{period.rows.map((activity,index) => {
    const row = period.offset + index;
    const place = places(plan,activity,row);
    const kind = kindOf(plan,activity);
    const duty = effectiveDuty(plan.draft,row);
    const changing = previousDuty !== null && duty !== null && previousDuty !== duty;
    previousDuty = duty;
    return <li key={activity.id} data-period-activity={kind}>
      <time dateTime={activity.start ?? undefined}>{drivingTime(activity.start)}–{drivingTime(activity.end)}</time>
      <div><strong>{kind === 'Sign-on' && now < stamp(activity.start) ? 'Planlagt oppmøte' : dayTypeLabels[kind] ?? kind}</strong>
        {place && <span>{place}</span>}{changing && <span>Vognløpsbytte · {duty}</span>}</div>
    </li>;
  })}</ol>;
}
