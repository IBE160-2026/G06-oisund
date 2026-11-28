import { useState } from 'react';
import type { Plan } from './PrivateConfirmation';
import type { ResourceProps } from './useWorkdayResource';
import { activityChoiceLabel } from './activityChoiceLabel';
import { useFrozenRouteReferences } from './PrivateRouteReference';
import { PrivateDrivingAnchor } from './PrivateDrivingAnchor';
import type { PositionAnchorContinuity, SavedStopAnchor } from './positionAnchorClient';

export function PrivateTourCorrection({plan, request, mutation, expired, available, continuity, guard, saved}: {
  plan: Plan; request: ResourceProps['request']; mutation: ResourceProps['mutation']; expired: () => void;
  available: boolean; continuity: PositionAnchorContinuity; guard: (value: boolean) => void;
  saved: (anchor: SavedStopAnchor) => void;
}) {
  const [open, setOpen] = useState(false);
  const [trip, setTrip] = useState('');
  const [stop, setStop] = useState<number>();
  const [pending, setPending] = useState(false);
  const options = useFrozenRouteReferences({workdayId:plan.id, serviceDate:plan.draft.service_date,
    expiresAt:plan.expires_at, available:open && available, request, expired});
  const trips = plan.draft.activities.filter(activity => (plan.classifications[activity.id] ?? activity.type) === 'trip');
  const choices = trips.filter(activity => options.references.some(reference => reference.activity_id === activity.id && reference.status === 'compatible'));
  const activityId = choices.some(activity => activity.id === trip) ? trip : choices[0]?.id;
  const lock = useState(() => (value:boolean) => { setPending(value); guard(value); })[0];
  if (!available && !open) return null;
  return <details className="day-tour-correction" open={open} onToggle={event => setOpen(event.currentTarget.open)}>
    <summary onClick={event => { if (pending) event.preventDefault(); }}>Korriger tur og stopp</summary>
    {open && (activityId ? <>
      <label>Passasjertur<select aria-label="Passasjertur" value={activityId} disabled={pending || !available}
        onChange={event => { setTrip(event.target.value); setStop(undefined); }}>
        {choices.map(activity => <option key={activity.id} value={activity.id}>{activityChoiceLabel(activity, 'trip')}</option>)}
      </select></label>
      <PrivateDrivingAnchor key={activityId} authority={{workdayId:plan.id, activityId, expiresAt:plan.expires_at, request, mutation}}
        continuity={continuity} lock={lock} disabled={!available} saved={anchor => {
          setStop(anchor.revision);
          saved(anchor);
        }} />
      {stop && <p role="status">Tur og stopp er lagret for kjørevisningen.</p>}
    </> : <p>{options.failed ? 'Avgangene kunne ikke hentes.' : options.loaded ? 'Planen har ingen passasjerturer med bekreftet rute.' : 'Henter avgangene …'}</p>)}
  </details>;
}
