import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { positionSourceMessage, usePositionAssistance } from './PositionAssistance';
import type { PositionReason } from './positionSource';
import { bindings, RoadLimits, type RoadManifest, type RoadReading } from './roadLimits';

type Props = { workdayId: string; activityId: string; request: (path: string) => Promise<unknown> };
type RoadResponse = { status: 'route-unqualified' | 'road-unqualified' } | { status: 'qualified'; manifest: RoadManifest };
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

function Sign({ value, size }: { value: number; size: number }) {
  return officialValues.has(value)
    ? <img src={`/assets/road-signs/362_${value}.jpg`} alt={`${value} km/t`} width={size} height={size} style={{ objectFit: 'contain' }} />
    : <strong>{value} km/t</strong>;
}

function ActiveRoadLimits({ manifest }: { manifest: RoadManifest }) {
  const access = usePositionAssistance();
  const source = access?.source;
  const wanted = useRef(false);
  const [active, setActive] = useState(false);
  const [starting, setStarting] = useState(false);
  const [interruption, setInterruption] = useState<PositionReason | null>(null);
  const [reading, setReading] = useState(EMPTY);
  useLayoutEffect(() => {
    if (!source) return;
    const limits = new RoadLimits(manifest);
    let timer: ReturnType<typeof setTimeout> | undefined;
    const keep = source.subscribe('road', {
      state: (state, on) => {
        setActive(on);
        if (state.reason === 'off') setInterruption(null);
        else if (wanted.current) setInterruption(state.reason === 'acquiring' ? null : state.reason);
        if (!state.running) wanted.current = false;
        if (!on || state.reason === 'invalid') {
          clearTimeout(timer);
          setReading(limits.reset());
        }
      },
      fix: fix => {
        clearTimeout(timer);
        setReading(limits.receive(fix));
        const age = fix.receivedWallMs - fix.acquiredAt + performance.now() - fix.receivedMonoMs;
        const untilExpiry = Math.min(Math.floor(5_000 - age) + 1, limits.expiresAt() - Date.now());
        timer = setTimeout(() => setReading(limits.read(performance.now(), Date.now())), Math.max(1, untilExpiry));
      },
    });
    return () => {
      wanted.current = false;
      clearTimeout(timer);
      keep();
      source.deactivate('road');
    };
  }, [manifest, source]);

  async function start() {
    wanted.current = true;
    setInterruption(null);
    setStarting(true);
    try { await access?.start('road', () => wanted.current); }
    finally { setStarting(false); }
  }
  function stop() {
    wanted.current = false;
    setInterruption(null);
    source?.deactivate('road');
  }
  const showDetails = active && !interruption;
  return <>
    <dl>
      <dt>Registrert vegfartsgrense</dt>
      <dd>{'kmh' in reading.current ? <Sign value={reading.current.kmh} size={68} /> : <>—{showDetails && ' ' + reasons[reading.current.reason]}</>}</dd>
      <dt>Neste fartsgrense</dt>
      <dd>{'kmh' in reading.next ? <><Sign value={reading.next.kmh} size={42} /> ca. {reading.next.metres} m</> : <>—{showDetails && ' ' + reasons[reading.next.reason]}</>}</dd>
    </dl>
    <div role="status">{interruption && positionSourceMessage[interruption]}</div>
    <button disabled={!source || starting} onClick={() => active ? stop() : void start()}>
      {active ? 'Stopp vegmatching' : 'Start vegmatching'}
    </button>
    <p>Skiltillustrasjoner: Statens vegvesen, <a href="https://data.norge.no/nlod/no">NLOD</a>.</p>
  </>;
}

export function PrivateRoadLimits({ workdayId, activityId, request }: Props) {
  const [result, setResult] = useState<RoadResponse | 'waiting' | 'unavailable'>('waiting');
  const stableRequest = useState(() => request)[0];
  useEffect(() => {
    let current = true;
    void stableRequest('/workdays/' + workdayId + '/road-reference/' + activityId).then(raw => {
      if (!current) return;
      const response = raw as RoadResponse;
      if (response?.status === 'qualified' && bindings(response.manifest)
          || response?.status === 'route-unqualified' || response?.status === 'road-unqualified') setResult(response);
      else setResult('unavailable');
    }).catch(() => { if (current) setResult('unavailable'); });
    return () => { current = false; };
  }, [activityId, stableRequest, workdayId]);
  return <section aria-label="Fartsgrense">
    {typeof result === 'object' && result.status === 'qualified'
      ? <ActiveRoadLimits manifest={result.manifest} />
      : <p role="status">{result === 'waiting' ? 'Henter veggrunnlag …' : result === 'unavailable'
        ? 'Veggrunnlaget kunne ikke kontrolleres.'
        : result.status === 'route-unqualified' ? 'Fartsgrense krever en kvalifisert rute for valgt aktivitet.'
          : 'Kvalifisert veggrunnlag mangler for valgt rute.'}</p>}
  </section>;
}
