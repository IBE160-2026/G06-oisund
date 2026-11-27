import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { positionSourceMessage, usePositionAssistance } from './PositionAssistance';
import { privateNow } from './privateClock';
import type { PositionReason } from './positionSource';
import { bindings, RoadLimits, type RoadManifest, type RoadReading } from './roadLimits';

type Props = { workdayId: string; activityId: string; request: (path: string) => Promise<unknown> };
type RoadProblem = 'route-unqualified' | 'road-unqualified' | 'unavailable';
export type RoadResponse = { status: RoadProblem } | { status: 'qualified'; manifest: RoadManifest; confirmed?: number };
export type RoadRevision = { revision?: unknown; situationLeaseUntil?: unknown };
const EMPTY: RoadReading = { current: { reason: 'waiting' }, next: { reason: 'waiting' } };
const reasons: Record<string, string> = {
  waiting: 'Venter på sammenhengende målinger.',
  stale: 'Posisjonsmålingen er for gammel.',
  uncertain: 'Vegvalg eller passering er usikker.',
  source: 'Vegdata er utløpt eller utilgjengelig.',
  coverage: 'Vegdata dekker ikke det aktuelle området.',
  unverified: 'Fartsgrensen eller overgangen er ikke bekreftet.',
  branch: 'Videre veg er usikker.',
  clear: 'Ingen registrert endring innen 300 m i kvalifisert vegdata.',
};
const officialValues = new Set([30, 40, 50, 60, 70]);
const roadMessage = {
  waiting: 'Henter veggrunnlag …',
  unavailable: 'Veggrunnlaget kunne ikke kontrolleres.',
  'route-unqualified': 'Fartsgrense krever en kvalifisert rute for valgt aktivitet.',
  'road-unqualified': 'Kvalifisert veggrunnlag mangler for valgt rute.',
  expired: reasons.source,
  changed: 'Veggrunnlaget er endret. Start vegmatching på nytt for å hente gjeldende uttak.',
};

function Sign({ value, size }: { value: number; size: number }) {
  return officialValues.has(value)
    ? <img src={`/assets/road-signs/362_${value}.jpg`} alt={`${value} km/t`} width={size} height={size} style={{ objectFit: 'contain' }} />
    : <strong>{value} km/t</strong>;
}

type ActiveProps = {
  loadRoad: () => Promise<RoadResponse>;
  checkRevision?: () => Promise<RoadRevision | null>;
  driving?: boolean;
};

export function ActiveRoadLimits({ loadRoad, checkRevision, driving = false }: ActiveProps) {
  const access = usePositionAssistance();
  const source = access?.source;
  const pending = useRef<symbol | null>(null);
  const matcher = useRef<RoadLimits | null>(null);
  const roadOn = useRef(false);
  const [active, setActive] = useState(false);
  const [starting, setStarting] = useState(false);
  const [interruption, setInterruption] = useState<PositionReason | null>(null);
  const [problem, setProblem] = useState<RoadProblem | 'expired' | 'changed' | null>(null);
  const [confirmed, setConfirmed] = useState<number>();
  const [reading, setReading] = useState(EMPTY);
  useLayoutEffect(() => {
    if (!source) return;
    let wasActive = false;
    let activatedAt = Infinity;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const keep = source.subscribe('road', {
      state: (state, on) => {
        roadOn.current = on;
        setActive(on);
        if (state.reason === 'off') setInterruption(null);
        else if (on || wasActive || !state.running && pending.current) {
          setInterruption(state.reason === 'acquiring' ? null : state.reason);
        }
        if (on && !wasActive) activatedAt = Date.now();
        wasActive = on;
        if (!state.running && pending.current) {
          pending.current = null;
          setStarting(false);
        }
        if (!on || state.reason === 'invalid') {
          clearTimeout(timer);
          setReading(matcher.current?.reset() ?? EMPTY);
          if (!on && !pending.current) matcher.current = null;
        }
      },
      fix: fix => {
        const limits = matcher.current;
        if (!limits || fix.acquiredAt < activatedAt) return;
        clearTimeout(timer);
        const now = privateNow();
        setReading(limits.receive(fix, now));
        const age = fix.receivedWallMs - fix.acquiredAt + performance.now() - fix.receivedMonoMs;
        const untilExpiry = Math.min(Math.floor(5_000 - age) + 1, limits.expiresAt() - now);
        timer = setTimeout(() => setReading(limits.read(performance.now(), privateNow())), Math.max(1, untilExpiry));
      },
    });
    return () => {
      roadOn.current = false;
      pending.current = null;
      matcher.current = null;
      clearTimeout(timer);
      keep();
      source.deactivate('road');
    };
  }, [source]);

  useEffect(() => {
    if (!checkRevision || !active || !source || !matcher.current) return;
    let running = true;
    let checking = false;
    const timer = setInterval(async () => {
      const current = matcher.current;
      if (checking || !current) return;
      checking = true;
      let changed = false;
      try {
        const review = await checkRevision();
        if (!running || !roadOn.current || matcher.current !== current) return;
        if (current.matchesRevision(review?.revision)) {
          current.renewSituationLease(review?.situationLeaseUntil, privateNow());
          return;
        }
        changed = true;
        current.reset();
        matcher.current = null;
        setReading(EMPTY);
        const response = await loadRoad();
        if (!running || !roadOn.current || matcher.current) return;
        if (response.status === 'qualified') {
          const next = new RoadLimits(response.manifest);
          if (!current.matchesRevision(response.manifest.revision) && next.isFresh(privateNow())) {
            matcher.current = next;
            setConfirmed(response.confirmed);
            return;
          }
        }
        source.deactivate('road');
        setProblem('changed');
      } catch {
        if (running && roadOn.current && (matcher.current === current || changed && !matcher.current)) {
          source.deactivate('road');
          setProblem('unavailable');
        }
      } finally {
        checking = false;
      }
    }, 30_000);
    return () => { running = false; clearInterval(timer); };
  }, [active, checkRevision, loadRoad, source]);

  async function start() {
    if (!access || pending.current) return;
    const attempt = Symbol();
    pending.current = attempt;
    const isPending = () => pending.current === attempt;
    setInterruption(null);
    setProblem(null);
    setConfirmed(undefined);
    setReading(EMPTY);
    setStarting(true);
    try {
      const response = await loadRoad();
      if (!isPending()) return;
      if (response.status !== 'qualified') { setProblem(response.status); return; }
      const limits = new RoadLimits(response.manifest);
      if (!limits.isFresh(privateNow())) { setProblem('expired'); return; }
      matcher.current = limits;
      setConfirmed(response.confirmed);
      await access.start('road', () => isPending() && limits.isFresh(privateNow()));
      if (isPending() && !limits.isFresh(privateNow())) {
        matcher.current = null;
        source?.deactivate('road');
        setProblem('expired');
      }
    } finally {
      if (isPending()) {
        pending.current = null;
        setStarting(false);
      }
    }
  }
  function stop() {
    pending.current = null;
    matcher.current = null;
    source?.deactivate('road');
    setInterruption(null);
    setStarting(false);
  }
  useEffect(() => {
    if (!driving || !source) return;
    const resume = () => { if (!roadOn.current && document.visibilityState === 'visible') void start(); };
    resume();
    document.addEventListener('visibilitychange', resume);
    return () => document.removeEventListener('visibilitychange', resume);
  }, [driving, source, loadRoad]);
  useEffect(() => {
    if (!driving || active || starting || (!problem && !['gap', 'clock', 'timeout', 'unavailable'].includes(interruption ?? ''))) return;
    const timer = setTimeout(() => { if (document.visibilityState === 'visible') void start(); }, problem ? 15_000 : 3000);
    return () => clearTimeout(timer);
  }, [driving, active, starting, problem, interruption]);

  if (driving) {
    const current = 'kmh' in reading.current ? reading.current.kmh : null;
    const next = 'kmh' in reading.next ? reading.next : null;
    return <section className="driving-speed" aria-label="Fartsgrense">
      {current === null
        ? <div className="driving-sign unknown" aria-label="Fartsgrense ukjent">–</div>
        : <div className={'driving-sign' + (current >= 100 ? ' three-digits' : '')} aria-label={current + ' km/t'}>{current}</div>}
      {current !== null && next ? <p>Om {next.metres} m: {next.kmh} km/t</p> : current === null && <p>Ukjent</p>}
    </section>;
  }

  const showDetails = active && !interruption;
  const problemMessage = checkRevision && problem === 'road-unqualified'
    ? 'Veggrunnlag mangler for Tromsø bybuss på dagens dato.'
    : problem ? roadMessage[problem] : null;
  return <>
    <dl>
      <dt>Registrert vegfartsgrense</dt>
      <dd>{'kmh' in reading.current ? <Sign value={reading.current.kmh} size={68} /> : <>{showDetails ? 'Ukjent · ' + reasons[reading.current.reason] : '—'}</>}</dd>
      <dt>Neste fartsgrense</dt>
      <dd>{'kmh' in reading.next ? <><Sign value={reading.next.kmh} size={42} /> ca. {reading.next.metres} m</> : <>{showDetails ? 'Ukjent · ' + reasons[reading.next.reason] : '—'}</>}</dd>
    </dl>
    <div role="status">{interruption ? positionSourceMessage[interruption]
      : problemMessage ?? (starting && !active ? 'Kontrollerer veggrunnlaget og tilgangen …'
        : active && confirmed === 0 ? 'Ingen fartsgrenser er bekreftet i dette uttaket.' : '')}</div>
    <button disabled={!source || starting} onClick={() => active ? stop() : void start()}>
      {active ? 'Stopp vegmatching' : 'Start vegmatching'}
    </button>
    {starting && <button onClick={stop}>Avbryt vegoppstart</button>}
    <p>Skiltillustrasjoner: Statens vegvesen, <a href="https://data.norge.no/nlod/no">NLOD</a>.</p>
  </>;
}

export function PrivateRoadLimits({ workdayId, activityId, request }: Props) {
  const [status, setStatus] = useState<RoadResponse['status'] | 'waiting'>('waiting');
  const [check, setCheck] = useState(0);
  const stableRequest = useState(() => request)[0];
  const loadRoad = useCallback(async (): Promise<RoadResponse> => {
    try {
      const response = await stableRequest('/workdays/' + workdayId + '/road-reference/' + activityId) as RoadResponse;
      if (response?.status === 'qualified' && response.manifest?.profile === 'SL-LAB-1' && bindings(response.manifest)) return response;
      if (response?.status === 'route-unqualified' || response?.status === 'road-unqualified') return response;
    } catch {
      return { status: 'unavailable' };
    }
    return { status: 'unavailable' };
  }, [activityId, stableRequest, workdayId]);
  useEffect(() => {
    let current = true;
    void loadRoad().then(response => { if (current) setStatus(response.status); });
    return () => { current = false; };
  }, [check, loadRoad]);
  return <section aria-label="Fartsgrense">
    {status === 'qualified'
      ? <ActiveRoadLimits key={workdayId + ':' + activityId} loadRoad={loadRoad} />
      : <>
        <p role="status">{status === 'waiting' ? roadMessage[status] : 'Ukjent · ' + roadMessage[status]}</p>
        {status !== 'waiting' && <button onClick={() => { setStatus('waiting'); setCheck(value => value + 1); }}>
          Kontroller veggrunnlaget på nytt
        </button>}
      </>}
  </section>;
}
