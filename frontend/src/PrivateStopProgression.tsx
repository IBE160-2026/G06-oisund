import { useEffect, useId, useLayoutEffect, useRef, useState } from 'react';
import { usePositionAssistance } from './PositionAssistance';
import { privateNow } from './privateClock';
import { proposeStop, readStopProjection, usePositionAnchor, type PositionAnchorContinuity, type SavedStopAnchor, type StopAuthority, type StopProjection } from './positionAnchorClient';
import { StopProgression, type StopAssertion, type StopCall, type StopProgress } from './stopProgression';
import type { PositionReason } from './positionSource';

type Assistance = NonNullable<ReturnType<typeof usePositionAssistance>>;
type Props = StopAuthority & { anchorContinuity: PositionAnchorContinuity; visible: boolean };
const initialProgress: StopProgress = { assertion: null, estimate: null, stale: false, reason: 'waiting' };
const routeMessages: Record<string, string> = {
  'route-missing': 'Aktiviteten har ingen bekreftet kjøring.',
  'route-identity-unverified': 'Identiteten eller driftsdatoen for kjøringen er ubekreftet.',
  'route-incompatible': 'Den valgte rutekilden er ubekreftet eller uforenlig.',
  'range-invalid': 'Den valgte rekken av holdeplassforekomster kunne ikke bekreftes.',
  'mapping-unverified': 'Plattformkoblingen er ubekreftet.',
  'coordinate-version-missing': 'Kjøringen mangler en bundet koordinatversjon.',
  'coordinate-missing': 'Plattformkoordinater mangler.',
  'coordinate-ambiguous': 'Flere koordinatposter for plattformen.',
  'coordinate-invalid': 'Plattformkoordinatene er ugyldige.',
  'call-time-unverified': 'Forekomsten mangler bekreftet dato og klokkeslett.',
  'validity-unknown': 'Plattformens daterte koordinatgyldighet er ukjent.',
  'validity-mismatch': 'Koordinatversjonen er ikke gyldig på tidspunktet for forekomsten.',
  'coordinate-unverified': 'Plattformkoordinatene er ubekreftet.',
};
const sourceMessages: Record<PositionReason, string> = {
  off: 'Holdeplassmåling er av.',
  paused: 'Posisjon er satt på pause. Velg forekomst for å gjenoppta.',
  hidden: 'Posisjon ble stoppet da siden ble skjult. Velg forekomst for å gjenoppta.',
  access: 'Tilgangen må bekreftes på nytt.',
  unsupported: 'Nettleseren tilbyr ikke posisjonsmåling.',
  insecure: 'Posisjon krever en sikker testadresse.',
  denied: 'Posisjonstilgangen ble avvist.',
  unavailable: 'Posisjonsmåling er utilgjengelig.',
  timeout: 'Posisjonsmålingen tok for lang tid.',
  gap: 'Posisjonsmålingene er blitt for gamle. Velg forekomst for å gjenoppta.',
  clock: 'Måletiden kunne ikke bekreftes. Velg forekomst for å gjenoppta.',
  invalid: 'En måling kunne ikke brukes.',
  acquiring: 'Venter på nye posisjonsmålinger.',
};
const progressMessages: Record<StopProgress['reason'], string> = {
  waiting: 'Venter på nye posisjonsmålinger.',
  protecting: 'Det nye manuelle holdepunktet beholdes mens nye målinger vurderes.',
  tracking: 'Venter på sammenhengende målinger for neste forekomst.',
  poor: 'En posisjonsmåling er for unøyaktig eller ugyldig.',
  stale: 'Posisjonsmålingene er blitt for gamle.',
  ambiguous: 'Målingene passer flere forekomster. Velg forekomst manuelt.',
  reanchor: 'Målingene bryter med den valgte retningen. Kontroller forekomsten manuelt.',
  'range-end': 'Siste forekomst i den valgte rekken.',
  manual: 'Måling mottatt. Neste forekomst må velges manuelt.',
};
const clockLabel = new Intl.DateTimeFormat('nb-NO', {
  timeZone: 'Europe/Oslo', dateStyle: 'short', timeStyle: 'medium',
});
function evidenceLabel(value: number | string, now: number) {
  const instant = typeof value === 'number' ? value : Date.parse(value);
  const seconds = Math.max(0, Math.floor((now - instant) / 1000));
  const age = seconds >= 60 ? Math.floor(seconds / 60) + ' min' : seconds + ' s';
  return clockLabel.format(instant) + ' · ' + age + ' siden';
}
const basisLabel = (basis: 'manual' | 'gps') => basis === 'manual' ? 'manuelt valgt' : 'GPS-anslag';
function callLabel(call: StopCall) {
  const time = call.departure?.utc ?? call.arrival?.utc;
  return call.position + '. ' + (call.name ?? call.quay_id ?? call.occurrence_id)
    + (time ? ' · ' + clockLabel.format(Date.parse(time)) : '');
}

export function PrivateStopProgression({ visible, ...props }: Props) {
  const assistance = usePositionAssistance();
  return assistance && visible ? <StopPanel key={props.workdayId + ':' + props.activityId} {...props} assistance={assistance} /> : null;
}

function StopPanel({ assistance, anchorContinuity, ...authority }: Omit<Props, 'visible'> & { assistance: Assistance }) {
  const name = useId();
  const { source, start, stop } = assistance;
  const auth = useRef(authority);
  auth.current = authority;
  const mounted = useRef(false), want = useRef(false), attempt = useRef(0), active = useRef(false);
  const routeEpoch = useRef(0);
  const lastGeneration = useRef<number | null>(null);
  const machine = useRef<StopProgression | null>(null), frozen = useRef<StopProjection | null>(null);
  const [projection, setProjection] = useState<StopProjection | null>(null);
  const [routeLoading, setRouteLoading] = useState(true);
  const [routeUnavailable, setRouteUnavailable] = useState(false);
  const [measuring, setMeasuring] = useState(false);
  const [starting, setStarting] = useState(false);
  const [reason, setReason] = useState<PositionReason>('off');
  const [progress, setProgress] = useState(initialProgress);
  const [chosen, setChosen] = useState('');
  const [rejectedProposal, setRejectedProposal] = useState(0);
  const [carry, setCarry] = useState<SavedStopAnchor | null>(null);
  const [now, setNow] = useState(() => privateNow());
  const anchor = usePositionAnchor(authority, anchorContinuity, deny);
  const anchorApi = useRef(anchor);
  anchorApi.current = anchor;

  function cancel(clear: boolean) {
    attempt.current++;
    want.current = false;
    active.current = false;
    anchorApi.current.discardQueue();
    machine.current?.interrupt(clear);
    setProgress(machine.current?.read() ?? initialProgress);
    setChosen('');
    setStarting(false);
    setMeasuring(false);
    if (clear) setCarry(null);
  }

  function deny() {
    routeEpoch.current++;
    cancel(true);
    source.deactivate('stops');
    anchorApi.current.forget();
    frozen.current = null;
    machine.current = null;
    setProjection(null);
    setRouteLoading(false);
    setRouteUnavailable(true);
  }

  async function loadRoute() {
    const version = ++routeEpoch.current;
    setRouteLoading(true);
    try {
      const bound = auth.current;
      const value = readStopProjection(await bound.request('/workdays/' + bound.workdayId
        + '/position-coordinates/' + bound.activityId), auth.current);
      if (!mounted.current || version !== routeEpoch.current) return;
      if (value.terminal || frozen.current && frozen.current.route?.basis !== value.route?.basis) {
        cancel(true);
        source.deactivate('stops');
      }
      if (!machine.current || frozen.current?.route?.basis !== value.route?.basis) machine.current = new StopProgression(value.calls);
      frozen.current = value;
      setProjection(value);
      setRouteUnavailable(false);
    } catch (error: any) {
      if (!mounted.current || version !== routeEpoch.current) return;
      if ([401, 404, 410].includes(error?.status)) deny();
      else {
        cancel(false);
        source.deactivate('stops');
        setRouteUnavailable(true);
      }
    } finally { if (mounted.current && version === routeEpoch.current) setRouteLoading(false); }
  }

  useLayoutEffect(() => {
    mounted.current = true;
    void loadRoute();
    return () => {
      mounted.current = false;
      routeEpoch.current++;
      want.current = false;
      attempt.current++;
      anchorApi.current.discardQueue();
    };
  }, []);

  const terminal = projection?.terminal || anchor.view?.terminal;
  useLayoutEffect(() => {
    if (terminal) {
      cancel(true);
      source.deactivate('stops');
    }
  }, [terminal, source]);

  useLayoutEffect(() => {
    const unsubscribe = source.subscribe('stops', {
      state(next, subscribed) {
        const previous = lastGeneration.current;
        lastGeneration.current = next.generation;
        if (subscribed && want.current) {
          if (!active.current || previous !== next.generation) machine.current?.bind(next.generation);
          active.current = true;
          setMeasuring(true);
          if (next.reason === 'invalid') {
            machine.current?.invalidate('poor');
            setProgress(machine.current?.read() ?? initialProgress);
          }
          setReason(next.reason);
          return;
        }
        if (want.current || active.current || previous !== null && previous !== next.generation && next.reason !== 'acquiring') {
          cancel(next.reason === 'off' || next.reason === 'access');
          setReason(next.reason);
        }
      },
      fix(fix) {
        if (!active.current || !want.current || !machine.current) return;
        const estimate = machine.current.receive(fix, performance.now());
        setProgress(machine.current.read());
        setNow(privateNow());
        if (estimate) save(estimate);
      },
    });
    return () => {
      attempt.current++;
      want.current = false;
      active.current = false;
      machine.current?.interrupt(true);
      unsubscribe();
      source.deactivate('stops');
    };
  }, [source]);

  const ages = Boolean(progress.estimate || anchor.view?.anchor);
  useEffect(() => {
    if (!ages) return;
    const timer = setInterval(() => setNow(privateNow()), 10_000);
    return () => clearInterval(timer);
  }, [ages]);

  function persistable(occurrenceId: string) {
    const current = frozen.current;
    const call = current?.calls.find(item => item.occurrence_id === occurrenceId);
    return Boolean(current?.route?.compatible && call?.stop_place_id && call.quay_id);
  }

  function save(estimate: StopAssertion, previous?: SavedStopAnchor) {
    const route = frozen.current?.route, call = frozen.current?.calls.find(item => item.occurrence_id === estimate.occurrenceId);
    if (!route?.compatible || !route.activity_id || !call || !call.stop_place_id || !call.quay_id || frozen.current?.terminal
        || estimate.basis === 'gps' && !active.current || Date.parse(auth.current.expiresAt) <= privateNow()) return;
    void anchorApi.current.send({
      activity_id: route.activity_id, route_basis: route.basis, occurrence_id: call.occurrence_id,
      coordinate_revision: call.coordinates?.revision ?? null, origin: estimate.basis,
      evidence_at: new Date(estimate.evidenceAt).toISOString(),
      ...(previous ? { carried_from_revision: previous.revision } : {}),
    });
  }

  function choose(id: string, previous?: SavedStopAnchor) {
    if (terminal || routeLoading || Date.parse(auth.current.expiresAt) <= privateNow()
        || (persistable(id) && !anchorApi.current.canRecordManual())
        || !machine.current?.choose(id, Date.now(), performance.now())) return false;
    const next = machine.current.read();
    setProgress(next);
    setChosen(id);
    setCarry(previous ?? null);
    setNow(privateNow());
    if (next.assertion) save(next.assertion, previous);
    return true;
  }

  async function begin() {
    if (terminal || routeUnavailable || starting || measuring || !projection?.route?.compatible
        || !anchorApi.current.canRecordManual() || !machine.current?.canFollow(chosen)) return;
    if ((progress.stale || progress.assertion?.occurrenceId !== chosen) && !choose(chosen)) return;
    const version = ++attempt.current;
    want.current = true;
    setStarting(true);
    try {
      await start('stops', () => want.current && version === attempt.current);
    } finally {
      if (version === attempt.current) {
        if (!active.current) want.current = false;
        setStarting(false);
      }
    }
  }

  const route = projection?.route, calls = projection?.calls ?? [];
  const selected = calls.find(call => call.occurrence_id === chosen);
  const canSave = anchor.view !== null && !anchor.loading && !anchor.pending && !anchor.writing;
  const selectedCanSave = selected && persistable(selected.occurrence_id);
  const previous = !anchor.pending ? anchor.view?.anchor ?? null : null;
  const proposal = previous && previous.revision !== rejectedProposal ? proposeStop(previous, authority.workdayId, route ?? null, calls) : null;
  const historicalCall = previous && previous.route_basis === route?.basis && previous.activity_id === authority.activityId
    ? calls.find(call => call.occurrence_id === previous.occurrence_id) : null;
  const coordinateCount = calls.filter(call => call.coordinates !== null).length;
  const issues = [...new Set(calls.map(call => call.coordinate_issue).filter((issue): issue is string => issue !== null))];
  const estimatedCall = calls.find(call => call.occurrence_id === progress.estimate?.occurrenceId);
  if (terminal) return <section aria-label="Holdeplassassistanse"><p>Skiftet er avsluttet. Holdeplassassistanse er skrivebeskyttet.</p></section>;

  return <section className="private-position-assistance" aria-labelledby={name}>
    <h3 id={name}>Holdeplassassistanse</h3>
    <p role="status">Rutedata. {routeLoading ? 'Henter bekreftet kjøring …'
      : routeUnavailable ? 'Rutedata er utilgjengelige for GPS-assistanse.'
      : projection?.reason ? routeMessages[projection.reason] ?? 'Rutedata er ubekreftet.'
      : coordinateCount === calls.length ? 'Plattformkoordinatene er tidskvalifisert.'
      : coordinateCount > 0 ? 'Deler av rekken må følges manuelt.' : 'Følg holdeplassene manuelt.'}</p>
    {route && <>
      <p>Driftsdato {route.service_date ?? 'ukjent'} · forekomster {route.start_position}–{route.end_position}
        {route.decision_revision && ' · ruteversjon ' + route.decision_revision}
        {route.source_version && ' · kilde ' + route.source_version.slice(0, 12)}</p>
      {issues.length > 0 && <p>{issues.map(issue => routeMessages[issue] ?? 'Ubekreftede koordinater.').join(' ')}</p>}
      {projection?.source && <p>Kartlegging {projection.source.revision}. Avgrenset uttrekk fra <a href={projection.source.source_url}
        target="_blank" rel="noreferrer">Entur NSR</a> under <a href={projection.source.license_url}
        target="_blank" rel="noreferrer">Norsk lisens for offentlige data (NLOD)</a>.</p>}
      <details>
        <summary>Planlagte holdeplassforekomster</summary>
        <ol start={route.start_position}>
          {calls.map(call => <li key={call.occurrence_id}>
            {call.name ?? call.quay_id ?? call.occurrence_id}
            {call.arrival?.utc && ' · ankomst ' + clockLabel.format(Date.parse(call.arrival.utc))}
            {call.departure?.utc && ' · avgang ' + clockLabel.format(Date.parse(call.departure.utc))}
            {call.coordinate_issue && ' · ' + (routeMessages[call.coordinate_issue] ?? 'Følges manuelt.')}
          </li>)}
        </ol>
      </details>
    </>}
    <p role="status">Posisjonsmåling. {measuring ? progressMessages[progress.reason] : sourceMessages[reason]}</p>
    {estimatedCall && progress.estimate && <p><strong>{progress.stale ? 'Tidligere holdepunkt' : 'Veiledende holdepunkt'}</strong>{' '}
      {callLabel(estimatedCall)} · {basisLabel(progress.estimate.basis)} · {evidenceLabel(progress.estimate.evidenceAt, now)}
    </p>}
    {!progress.estimate && historicalCall && previous && <p>Tidligere lagret holdepunkt. {callLabel(historicalCall)} ·{' '}
      {basisLabel(previous.origin)} · {evidenceLabel(previous.evidence_at, now)}. Velg forekomst på nytt.</p>}
    {progress.assertion && progress.assertion !== progress.estimate && <p>Sist manuelt valgt {calls.find(
      call => call.occurrence_id === progress.assertion?.occurrenceId)?.position} · {evidenceLabel(progress.assertion.evidenceAt, now)}</p>}
    {proposal?.kind === 'unique' && previous && <div>
      <p>Forslag fra forrige kjøring. {callLabel(proposal.call)} · {basisLabel(previous.origin)} · {evidenceLabel(previous.evidence_at, now)}.</p>
      <div className="controls">
        <button disabled={starting || measuring || !canSave} onClick={() => {
          if (choose(proposal.call.occurrence_id, previous)) setRejectedProposal(previous.revision);
        }}>Bruk foreslått forekomst</button>
        <button onClick={() => setRejectedProposal(previous.revision)}>Velg selv</button>
      </div>
    </div>}
    {proposal?.kind === 'ambiguous' && <p>Den lagrede plattformen brukes flere ganger her ({proposal.calls.map(call => call.position).join(', ')}). Velg forekomst manuelt.</p>}
    {proposal?.kind === 'no-match' && <p>Den lagrede plattformen finnes ikke i den valgte rekken. Velg forekomst manuelt.</p>}
    {proposal?.kind === 'unverified' && <p>Koblingen til den lagrede plattformen kunne ikke bekreftes. Velg forekomst manuelt.</p>}
    {carry && <p>Kilde for forslaget. {basisLabel(carry.origin)} · {evidenceLabel(carry.evidence_at, now)}.</p>}
    {calls.length > 0 && <>
      <label htmlFor={name + '-stop'}>Holdeplassforekomst</label>
      <select id={name + '-stop'} value={chosen} onChange={event => setChosen(event.currentTarget.value)} disabled={starting}>
        <option value="">Velg forekomst</option>
        {calls.map(call => <option key={call.occurrence_id} value={call.occurrence_id}>{callLabel(call)}</option>)}
      </select>
      <div className="controls">
        <button disabled={!selected || starting || routeLoading || selectedCanSave && !canSave} onClick={() => choose(chosen)}>
          {measuring ? 'Korriger til valgt forekomst' : 'Sett manuelt holdepunkt'}
        </button>
        {!measuring && <button disabled={!selected || starting || routeLoading || routeUnavailable || !canSave
          || !route?.compatible || !machine.current?.canFollow(chosen)} onClick={() => void begin()}>
          {reason === 'off' ? 'Start holdeplassassistanse' : 'Gjenoppta holdeplassassistanse'}
        </button>}
        {(measuring || starting) && <button onClick={() => stop('paused')}>Pause holdeplassassistanse</button>}
        {(reason !== 'off' || measuring || starting || progress.estimate) && <button onClick={() => stop('off')}>Slå av holdeplassassistanse</button>}
      </div>
    </>}
    {anchor.message && <p role="status">{anchor.message}</p>}
    {selected && !selectedCanSave && <p>Valget gjelder i denne visningen.</p>}
    {anchor.pending && <button disabled={anchor.writing || anchor.loading} onClick={() => void anchor.send(undefined, true)}>
      {anchor.priorActivity ? 'Kontroller uavklart holdepunkt' : 'Kontroller eller prøv samme holdepunkt igjen'}
    </button>}
    {(routeUnavailable || !anchor.view && !anchor.pending && !anchor.loading) && <button disabled={routeLoading}
      onClick={() => { void loadRoute(); void anchor.load(); }}>Hent rutedata og lagret holdepunkt</button>}
  </section>;
}
