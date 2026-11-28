import { createContext, useContext, useEffect, useLayoutEffect, useRef, useState, type ReactNode } from 'react';
import { GpsSpeed, type SpeedReading } from './gpsSpeed';
import { PositionSource, type PositionConsumer, type PositionReason, type PositionState } from './positionSource';
import { privateNow } from './privateClock';

type SourceAccess = {
  source: PositionSource;
  start: (consumer: PositionConsumer, stillWanted?: () => boolean) => Promise<void>;
  stop: (reason: 'off' | 'paused') => void;
};
const PositionContext = createContext<SourceAccess | null>(null);

export function usePositionAssistance() {
  return useContext(PositionContext);
}

export const positionSourceMessage: Record<PositionReason, string> = {
  off: 'Posisjon er av.',
  paused: 'Posisjon er satt på pause.',
  hidden: 'Posisjon ble stoppet da siden ble skjult.',
  access: 'Tilgangen må være bekreftet før måling.',
  unsupported: 'Nettleseren tilbyr ikke en posisjonstjeneste.',
  insecure: 'Posisjon krever en sikker testadresse.',
  denied: 'Posisjonstilgangen er avvist. Kontroller nettleserens og enhetens tillatelser.',
  unavailable: 'Posisjon er utilgjengelig. Kontroller enhetens posisjonstjeneste.',
  timeout: 'Posisjonsmålingen tok for lang tid.',
  gap: 'Ingen brukbar posisjonsmåling på 10 sekunder.',
  clock: 'Tiden for målingene kunne ikke bekreftes.',
  invalid: 'Posisjonsmålingen kunne ikke brukes.',
  acquiring: 'Venter på måling.',
};
const speedMessage: Record<Extract<SpeedReading, { kind: 'unknown' }>['reason'], string> = {
  waiting: 'Venter på sammenhengende målinger.',
  missing: 'Fart er utilgjengelig fra posisjonstjenesten.',
  inaccurate: 'Posisjonsmålingen er for unøyaktig.',
  stale: 'Fartsmålingen er for gammel.',
  jump: 'Målingene var ikke sammenhengende.',
};

function SpeedPanel({ source, start, stop, compact = false }: SourceAccess & {compact?:boolean}) {
  const [view, setView] = useState<{ state: PositionState; active: boolean }>({
    state: { generation: 0, running: false, reason: 'off' }, active: false,
  });
  const [speed, setSpeed] = useState<SpeedReading>({ kind: 'unknown', reason: 'waiting' });
  const [starting, setStarting] = useState(false);
  const [attempted, setAttempted] = useState(false);
  useLayoutEffect(() => {
    const estimate = new GpsSpeed();
    let expiry: ReturnType<typeof setTimeout> | undefined;
    const show = (reading: SpeedReading) => {
      clearTimeout(expiry);
      setSpeed(reading);
      if (reading.kind === 'qualified') {
        const expire = () => {
          source.verify();
          const remaining = reading.validUntilMono - performance.now();
          if (remaining > 0) expiry = setTimeout(expire, Math.ceil(remaining));
          else setSpeed(estimate.read(performance.now()));
        };
        expiry = setTimeout(expire, Math.max(1, Math.ceil(reading.validUntilMono - performance.now())));
      }
    };
    const unsubscribe = source.subscribe('speed', {
      state: (state, active) => {
        setView({ state, active });
        if (!active || state.reason === 'invalid') show(estimate.clear());
      },
      fix: fix => show(estimate.receive(fix)),
    });
    return () => { clearTimeout(expiry); unsubscribe(); source.deactivate('speed'); };
  }, [source]);

  const beginAccess = useRef(start);
  beginAccess.current = start;
  useEffect(() => {
    if (!compact) return;
    let current = true;
    const resume = () => { if (document.visibilityState === 'visible') void beginAccess.current('speed', () => current); };
    resume();
    document.addEventListener('visibilitychange', resume);
    return () => { current = false; document.removeEventListener('visibilitychange', resume); };
  }, [source, compact]);
  useEffect(() => {
    if (!compact || view.active || !['gap','clock','timeout','unavailable'].includes(view.state.reason)) return;
    let alive = true;
    const timer = setTimeout(() => void beginAccess.current('speed', () => alive), 3000);
    return () => { alive = false; clearTimeout(timer); };
  }, [compact, view.state.reason, view.active]);
  const usable = view.active && speed.kind === 'qualified' && speed.validUntilMono > performance.now();
  const status = view.active && view.state.reason !== 'invalid' && speed.kind === 'unknown'
    ? speedMessage[speed.reason] : usable ? '' : positionSourceMessage[view.state.reason === 'off' && view.state.running ? 'acquiring' : view.state.reason];
  async function begin() {
    setAttempted(true);
    setStarting(true);
    try { await start('speed'); }
    finally { setStarting(false); }
  }
  if (compact) return usable ? <div className="driving-own-speed" aria-label="Egen GPS-fart">GPS-fart <strong>{speed.displayKmh} km/t</strong></div> : null;
  return <section className="private-position-assistance" aria-label="Egen fart (GPS)">
    <p>Egen fart (GPS) <strong aria-label="Målt egen fart">{usable ? speed.displayKmh : '—'} km/t</strong></p>
    <p role="status">{status}</p>
    <div className="controls">
      {!view.active && <button disabled={starting} onClick={() => void begin()}>
        {!attempted || view.state.reason === 'off' ? 'Start fartsmåling' : 'Gjenoppta fartsmåling'}
      </button>}
      {view.state.running && <button onClick={() => stop('paused')}>Pause posisjon</button>}
      {view.state.reason !== 'off' && <button onClick={() => stop('off')}>Slå av posisjon</button>}
    </div>
  </section>;
}

export function DrivingSpeed() {
  const context = usePositionAssistance();
  return context && <SpeedPanel {...context} compact/>;
}

type Props = { authorized: boolean; expiresAt: string; verifyAccess: () => Promise<unknown>; showSpeed?: boolean; children?: ReactNode };
export function PositionAssistance({ authorized, expiresAt, verifyAccess, showSpeed = true, children }: Props) {
  const access = useRef({ authorized, expiresAt, verifyAccess });
  const attempt = useRef(0);
  const allowed = () => access.current.authorized && document.visibilityState === 'visible'
    && Date.parse(access.current.expiresAt) > privateNow();
  const [source] = useState(() => new PositionSource({
    geolocation: typeof navigator.geolocation?.watchPosition === 'function' && typeof navigator.geolocation?.clearWatch === 'function'
      ? navigator.geolocation : null,
    secure: window.isSecureContext,
    allowed,
    clock: { wall: () => Date.now(), monotonic: () => performance.now() },
  }));

  useLayoutEffect(() => {
    const changed = access.current.authorized !== authorized || access.current.expiresAt !== expiresAt;
    access.current = { authorized, expiresAt, verifyAccess };
    if (changed) attempt.current++;
    if (!authorized) source.stop('access');
    if (!authorized) return;
    let deadline: ReturnType<typeof setTimeout>;
    function atDeadline() {
      const remaining = Date.parse(expiresAt) - privateNow();
      if (remaining > 0) deadline = setTimeout(atDeadline, Math.min(remaining, 2_147_483_647));
      else source.stop('access');
    }
    atDeadline();
    return () => clearTimeout(deadline);
  }, [authorized, expiresAt, source, verifyAccess]);

  useLayoutEffect(() => {
    const hide = () => { attempt.current++; source.stop('hidden'); };
    const visibility = () => { if (document.visibilityState !== 'visible') hide(); };
    let pending = false;
    const validation = setInterval(async () => {
      if (!source.running || pending) return;
      source.verify();
      if (!source.running) return;
      pending = true;
      const checking = attempt.current;
      try { await access.current.verifyAccess(); }
      catch { if (attempt.current === checking) { attempt.current++; source.stop('access'); } }
      finally { pending = false; }
    }, 30_000);
    document.addEventListener('visibilitychange', visibility);
    window.addEventListener('pagehide', hide);
    return () => {
      attempt.current++;
      clearInterval(validation);
      document.removeEventListener('visibilitychange', visibility);
      window.removeEventListener('pagehide', hide);
      source.stop('off');
    };
  }, [source]);

  const value: SourceAccess = {
    source,
    async start(consumer, stillWanted) {
      if (!allowed()) { source.stop('access'); return; }
      const generation = attempt.current;
      try { await access.current.verifyAccess(); }
      catch { if (attempt.current === generation && stillWanted?.() !== false) source.stop('access'); return; }
      if (attempt.current === generation && allowed() && stillWanted?.() !== false) source.activate(consumer);
    },
    stop(reason) { attempt.current++; source.stop(reason); },
  };
  if (!authorized) return null;
  return <PositionContext.Provider value={value}>
    {showSpeed && <SpeedPanel {...value} />}
    {children}
  </PositionContext.Provider>;
}
