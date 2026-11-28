import { useEffect, useRef, useState } from 'react';
import { privateNow } from './privateClock';
import { readStopProjection, usePositionAnchor, type PositionAnchorContinuity, type SavedStopAnchor,
  type StopAuthority, type StopProjection } from './positionAnchorClient';

export function PrivateDrivingAnchor({authority, continuity, firstOnly = false, saved, lock, disabled = false}: {
  authority: StopAuthority; continuity: PositionAnchorContinuity; firstOnly?: boolean;
  saved: (anchor: SavedStopAnchor) => void; lock?: (value: boolean) => void; disabled?: boolean;
}) {
  const [projection, setProjection] = useState<StopProjection>();
  const [selected, setSelected] = useState('');
  const [unavailable, setUnavailable] = useState(false);
  const current = useRef(authority);
  current.current = authority;
  const anchor = usePositionAnchor(authority, continuity, () => setUnavailable(true));
  useEffect(() => {
    let mounted = true;
    const scope = current.current;
    void scope.request('/workdays/' + scope.workdayId + '/position-coordinates/' + scope.activityId)
      .then(value => {
        if (!mounted) return;
        const view = readStopProjection(value, scope);
        if (view.terminal || !view.route?.compatible) throw Error();
        setProjection(view);
        setSelected(view.calls[0]?.occurrence_id ?? '');
      }).catch(() => { if (mounted) setUnavailable(true); });
    return () => { mounted = false; };
  }, [authority.workdayId, authority.activityId]);
  useEffect(() => { lock?.(anchor.pending || anchor.writing); return () => lock?.(false); }, [lock, anchor.pending, anchor.writing]);
  const call = projection?.calls.find(item => item.occurrence_id === selected);
  const qualified = call?.quay_id && call.stop_place_id;
  const blocked = disabled || anchor.loading || anchor.writing || (!anchor.pending && (!qualified || !anchor.canRecordManual()));
  async function confirm() {
    const route = projection?.route;
    if (!route || !call || blocked) return;
    const value = anchor.pending ? await anchor.send(undefined, true) : await anchor.send({
      activity_id: authority.activityId, route_basis: route.basis,
      occurrence_id: call.occurrence_id, coordinate_revision: call.coordinates?.revision ?? null,
      origin: 'manual', evidence_at: new Date(privateNow()).toISOString(), driving: true,
    });
    if (value?.anchor?.activity_id === authority.activityId && value.anchor.occurrence_id === call.occurrence_id) saved(value.anchor);
  }
  return <div className={firstOnly ? 'ready-at-stop' : 'day-stop-choice'}>
    {!firstOnly && projection && <label>Holdeplass<select aria-label="Holdeplass" value={selected} disabled={disabled || anchor.pending}
      onChange={event => setSelected(event.target.value)}>
      {projection.calls.map(item => <option key={item.occurrence_id} value={item.occurrence_id}
        disabled={!item.quay_id || !item.stop_place_id}>Stopp {item.position} · {item.name ?? 'Ukjent'}</option>)}
    </select></label>}
    <button type="button" className={firstOnly ? 'ready-button' : undefined} disabled={blocked || unavailable} onClick={() => void confirm()}>
      {firstOnly ? 'Klar på første stopp' : 'Bruk valgt stopp'}
    </button>
    {projection && !qualified && <p>Velg et stopp med bekreftet plattform i Dagen din.</p>}
    {(unavailable || anchor.message) && <p role="status">{unavailable ? 'Holdeplassene for turen kunne ikke bekreftes.' : anchor.message}</p>}
  </div>;
}
