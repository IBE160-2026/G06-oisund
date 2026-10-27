import { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';
import { PrivateAccess } from './PrivateAccess';
import { FictionalAssessment } from './FictionalAssessment';

type Activity = { id: string; kind: 'trip' | 'break'; start: string; end: string; place: string | null; trip_code: string | null; provenance: 'fictional-planned' };
type Day = { fictional: true; service_date: string; timezone: 'Europe/Oslo'; vehicle_duty: string | null; physical_bus: string | null; activities: Activity[] };
type Saved = { id: string; day: Day; created_at: string; expires_at: string };
const API = 'http://127.0.0.1:8000';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function validInstant(value: unknown): value is string {
  if (typeof value !== 'string') return false;
  const parts = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$/.exec(value);
  if (!parts) return false;
  const [, year, month, day, hour, minute, second] = parts.map(Number);
  return month >= 1 && month <= 12 && day >= 1 && day <= new Date(Date.UTC(year, month, 0)).getUTCDate()
    && hour < 24 && minute < 60 && second < 60 && Number.isFinite(Date.parse(value));
}
function validDay(value: unknown): value is Day {
  if (!value || typeof value !== 'object') return false;
  const d = value as Day;
  return d.fictional === true && d.timezone === 'Europe/Oslo' && /^\d{4}-\d{2}-\d{2}$/.test(d.service_date)
    && (d.vehicle_duty === null || typeof d.vehicle_duty === 'string') && (d.physical_bus === null || typeof d.physical_bus === 'string')
    && Array.isArray(d.activities) && d.activities.length > 0 && d.activities.every(a => UUID.test(a.id)
      && ['trip', 'break'].includes(a.kind) && a.provenance === 'fictional-planned'
      && Number.isFinite(Date.parse(a.start)) && Number.isFinite(Date.parse(a.end))
      && (a.place === null || typeof a.place === 'string') && (a.trip_code === null || typeof a.trip_code === 'string'));
}
function validSaved(value: unknown): value is Saved {
  const r = value as Saved;
  if (!r || !UUID.test(r.id) || !validDay(r.day) || !validInstant(r.created_at) || !validInstant(r.expires_at)) return false;
  const created = Date.parse(r.created_at), expires = Date.parse(r.expires_at), now = Date.now();
  return Number.isFinite(created) && Number.isFinite(expires) && created <= now
    && expires - created === 7 * 86400000 && expires > now;
}
class ExpiredResponse extends Error {}
async function request(path: string, options?: RequestInit): Promise<unknown> {
  const response = await fetch(API + path, { ...options, cache: 'no-store', signal: AbortSignal.timeout(10000) });
  if (response.status === 410) throw new ExpiredResponse('Utløpt eller ukjent eksempel. Last inn et nytt eksempel.');
  if (!response.ok) throw new Error(response.status === 409 ? 'Konflikt: lagringsforsøket har andre verdier.' : 'Tjenesten er utilgjengelig eller avviste forespørselen.');
  if (!response.headers.get('content-type')?.includes('application/json')) throw new Error('Ugyldig svar fra tjenesten.');
  return response.json();
}
const display = (iso: string) => new Intl.DateTimeFormat('nb-NO', { dateStyle: 'short', timeStyle: 'short', timeZone: 'Europe/Oslo' }).format(new Date(iso));

function App() {
  const [day, setDay] = useState<Day | null>(null);
  const [operation, setOperation] = useState<string | null>(null);
  const [saved, setSaved] = useState<Saved | null>(null);
  const [identifier, setIdentifier] = useState(new URLSearchParams(location.search).get('day') ?? '');
  const [message, setMessage] = useState('Laster fiktivt eksempel …');
  const [busy, setBusy] = useState(false);
  const initialized = useRef(false);

  function clearExpired() {
    setDay(null); setSaved(null); setOperation(null); setIdentifier('');
    history.replaceState(null, '', location.pathname);
    setMessage('Utløpt eller ukjent eksempel. Last inn et nytt fiktivt eksempel.');
  }

  useEffect(() => {
    if (!saved) return;
    const remaining = Date.parse(saved.expires_at) - Date.now();
    if (remaining <= 0) { clearExpired(); return; }
    const timer = window.setTimeout(clearExpired, remaining);
    return () => window.clearTimeout(timer);
  }, [saved]);

  async function example() {
    setBusy(true); setMessage('Laster fiktivt eksempel …');
    try {
      const fixture = await request('/fixture');
      const op = await request('/operations', { method: 'POST' }) as { operation_id: string };
      if (!validDay(fixture) || !UUID.test(op.operation_id)) throw new Error('Ugyldig svar fra tjenesten.');
      setDay(fixture); setOperation(op.operation_id); setSaved(null); setIdentifier('');
      history.replaceState(null, '', location.pathname);
      setMessage('Ikke lagret. Eksemplet er planlagt og fiktivt.');
    } catch (error) { setMessage('Utilgjengelig. ' + (error instanceof Error ? error.message : 'Prøv igjen.')); }
    finally { setBusy(false); }
  }
  async function reopen(id = identifier) {
    if (!UUID.test(id)) { setMessage('Velg et tidligere lagret eksempel først.'); return; }
    setBusy(true); setMessage('Henter lagret eksempel …');
    try {
      const result = await request('/days/' + id);
      if (!validSaved(result) || result.id !== id) throw new Error('Ugyldig svar fra tjenesten.');
      setDay(result.day); setSaved(result); setOperation(null); setIdentifier(result.id);
      history.replaceState(null, '', '?day=' + result.id);
      setMessage('Lagret eksempel er hentet fra tjenesten.');
    } catch (error) {
      if (error instanceof ExpiredResponse) clearExpired();
      else setMessage('Henting er ikke bekreftet. ' + (error instanceof Error ? error.message : 'Tjenesten er utilgjengelig.'));
    }
    finally { setBusy(false); }
  }
  async function save() {
    if (!day || !operation) return;
    setBusy(true); setMessage('Lagrer …');
    try {
      const result = await request('/days', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ operation_id: operation, day }) });
      if (!validSaved(result) || JSON.stringify(result.day) !== JSON.stringify(day)) throw new Error('Lagringssvaret kunne ikke bekreftes.');
      setSaved(result); setIdentifier(result.id);
      history.replaceState(null, '', '?day=' + result.id);
      setMessage('Lagret og bekreftet av tjenesten.');
    } catch (error) {
      if (error instanceof ExpiredResponse) clearExpired();
      else setMessage('Lagring er ikke bekreftet. Behold siden åpen og prøv samme lagring igjen. ' + (error instanceof Error ? error.message : 'Tjenesten er utilgjengelig.'));
    }
    finally { setBusy(false); }
  }
  useEffect(() => { if (!initialized.current) { initialized.current = true; if (identifier) void reopen(identifier); else void example(); } }, []);
  return <main>
    <p className="badge">Fiktive demodata</p>
    <h1>Fiktiv arbeidsdag</h1>
    <p><a href="/demo.html">Prøv gjentakbar simulering uten backend</a></p>
    <p>Kun et fast eksempel for lokal vurdering. Demoen krever ingen innlogging og viser ingen private arbeidsdager. Bruk oversikten mens du står stille.</p>
    <p role="status" aria-live="polite" className="status">{message}</p>
    <div className="controls">
      <button disabled={busy} onClick={() => void example()}>Last inn nytt fiktivt eksempel</button>
      <button disabled={busy || !day || !operation} onClick={() => void save()}>Lagre fiktiv dag{saved && operation ? ' igjen' : ''}</button>
      <button disabled={busy || !identifier} onClick={() => void reopen()}>Åpne lagret dag på nytt</button>
    </div>
    {day && <section aria-labelledby="day-heading">
      <h2 id="day-heading">Tjenestedato {day.service_date}</h2>
      <dl><dt>Tidssone</dt><dd>{day.timezone}</dd><dt>Vognløp</dt><dd>{day.vehicle_duty ?? 'Ukjent'}</dd><dt>Fysisk buss</dt><dd>{day.physical_bus ?? 'Ukjent'}</dd></dl>
      <h2>Planlagte, fiktive aktiviteter</h2>
      <ol>{day.activities.map(a => <li key={a.id}><h3>{a.kind === 'trip' ? 'Tur' : 'Pause'}</h3><p>{display(a.start)} – {display(a.end)}</p><p>Sted: {a.place ?? 'Ukjent'} · Turkode: {a.trip_code ?? 'Ukjent'}</p><p>Fiktiv · Planlagt</p></li>)}</ol>
    </section>}
    {saved && <p>Bekreftet lagret {display(saved.created_at)}. Slettes senest {display(saved.expires_at)}. Nettadressen åpner dette fiktive eksemplet på nytt.</p>}
    <p>Et nytt eksempel og lagrede dager utløper etter syv dager. Gjentatt lagring forlenger ikke fristen. Usendte data finnes bare mens siden er åpen.</p>
    <p><a href="/private">Gå til privat tilgang</a>. Har du en aktiv økt, åpnes arbeidsrommet. Å åpne demoen logger deg ikke ut.</p>
  </main>;
}
createRoot(document.getElementById('root')!).render(location.pathname === '/demo' ? <FictionalAssessment /> : location.pathname === '/private' ? <PrivateAccess /> : <App />);
