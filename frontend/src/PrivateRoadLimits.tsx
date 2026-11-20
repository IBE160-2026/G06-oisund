import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { positionSourceMessage, usePositionAssistance } from './PositionAssistance';
import { privateNow } from './privateClock';
import type { PositionReason } from './positionSource';
import { bindings, RoadLimits, type RoadManifest, type RoadReading } from './roadLimits';

type Props = { workdayId: string; activityId: string; request: (path: string) => Promise<unknown> };
type RoadProblem = 'route-unqualified' | 'road-unqualified' | 'unavailable';
type RoadResponse = { status: RoadProblem } | { status: 'qualified'; manifest: RoadManifest };
const EMPTY: RoadReading = { current: { reason: 'waiting' }, next: { reason: 'waiting' } };
const reasons: Record<string, string> = {
  waiting: 'Venter på sammenhengende målinger.',
  stale: 'Posisjonsmålingen er for gammel.',
  uncertain: 'Vegvalg eller passering er usikker.',
  source: 'Vegdata er utløpt eller utilgjengelig.',
  coverage: 'Vegdata dekker ikke det aktuelle området.',
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
};

function Sign({ value, size }: { value: number; size: number }) {
  return officialValues.has(value)
    ? <img src={`/assets/road-signs/362_${value}.jpg`} alt={`${value} km/t`} width={size} height={size} style={{ objectFit: 'contain' }} />
    : <strong>{value} km/t</strong>;
}

function ActiveRoadLimits({ loadRoad }: { loadRoad: () => Promise<RoadResponse> }) {
  const access = usePositionAssistance();
  const source = access?.source;
  const pending = useRef<symbol | null>(null);
  const matcher = useRef<RoadLimits | null>(null);
  const [active, setActive] = useState(false);
  const [starting, setStarting] = useState(false);
  const [interruption, setInterruption] = useState<PositionReason | null>(null);
  const [problem, setProblem] = useState<RoadProblem | 'expired' | null>(null);
  const [reading, setReading] = useState(EMPTY);
  useLayoutEffect(() => {
    if (!source) return;
    let wasActive = false;
    let activatedAt = Infinity;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const keep = source.subscribe('road', {
      state: (state, on) => {
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
      pending.current = null;
      matcher.current = null;
      clearTimeout(timer);
      keep();
      source.deactivate('road');
    };
  }, [source]);

  async function start() {
    if (!access || pending.current) return;
    const attempt = Symbol();
    pending.current = attempt;
    const isPending = () => pending.current === attempt;
    setInterruption(null);
    setProblem(null);
    setReading(EMPTY);
    setStarting(true);
    try {
      const response = await loadRoad();
      if (!isPending()) return;
      if (response.status !== 'qualified') { setProblem(response.status); return; }
      const limits = new RoadLimits(response.manifest);
      if (!limits.isFresh(privateNow())) { setProblem('expired'); return; }
      matcher.current = limits;
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
  const showDetails = active && !interruption;
  return <>
    <dl>
      <dt>Registrert vegfartsgrense</dt>
      <dd>{'kmh' in reading.current ? <Sign value={reading.current.kmh} size={68} /> : <>—{showDetails && ' ' + reasons[reading.current.reason]}</>}</dd>
      <dt>Neste fartsgrense</dt>
      <dd>{'kmh' in reading.next ? <><Sign value={reading.next.kmh} size={42} /> ca. {reading.next.metres} m</> : <>—{showDetails && ' ' + reasons[reading.next.reason]}</>}</dd>
    </dl>
    <div role="status">{interruption ? positionSourceMessage[interruption]
      : problem ? roadMessage[problem] : starting && !active ? 'Kontrollerer veggrunnlaget og tilgangen …' : ''}</div>
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
      if (response?.status === 'qualified' && bindings(response.manifest)) return response;
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
        <p role="status">{roadMessage[status]}</p>
        {status !== 'waiting' && <button onClick={() => { setStatus('waiting'); setCheck(value => value + 1); }}>
          Kontroller veggrunnlaget på nytt
        </button>}
      </>}
  </section>;
}
