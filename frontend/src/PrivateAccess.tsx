import { useEffect, useRef, useState } from 'react';
import { PrivateDrafts } from './PrivateDrafts';

const API = 'http://127.0.0.1:8001';
// Only a logout lock, never an account, credential or private presentation. A cookie
// survives reload and is shared across tabs, unlike private browser data stores.
const PENDING = 'private_logout_pending';
const pending = () => document.cookie.split(';').some(c => c.trim() === PENDING + '=1');
function markPending(value: boolean) {
  document.cookie = `${PENDING}=${value ? '1' : ''}; Path=/; SameSite=Strict; Max-Age=${value ? 14 * 86400 : 0}`;
}
type Session = { account_id: string; created_at: string; expires_at: string };
function validSession(value: unknown): value is Session {
  const s = value as Session;
  return !!s && typeof s.account_id === 'string' && /^[0-9a-f-]{36}$/i.test(s.account_id)
    && Number.isFinite(Date.parse(s.created_at)) && Number.isFinite(Date.parse(s.expires_at))
    && Date.parse(s.expires_at) - Date.parse(s.created_at) === 14 * 86400000
    && Date.parse(s.expires_at) > Date.now();
}

export function PrivateAccess() {
  const [session, setSession] = useState<Session | null>(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [locked, setLocked] = useState(pending);
  const [busy, setBusy] = useState(true);
  const [message, setMessage] = useState('Kontrollerer tilgang …');
  const generation = useRef(0);
  const lockKnown = useRef(pending());
  const channel = useRef<BroadcastChannel | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  const usernameInput = useRef<HTMLInputElement>(null);
  const [focusLogin, setFocusLogin] = useState(false);
  const [suspended, setSuspended] = useState(false);
  const draftDirty = useRef(false);

  async function request(path: string, options?: RequestInit) {
    const response = await fetch(API + path, { ...options, credentials: 'include', cache: 'no-store', signal: AbortSignal.timeout(10000) });
    if (!response.ok || !response.headers.get('content-type')?.includes('application/json')) {
      const error = new Error(response.status === 401 ? 'Logg inn på nytt. Brukernavn eller passord kan være feil.' : response.status === 429 ? 'For mange forsøk. Vent 15 minutter før du prøver igjen.' : 'Tjenesten er utilgjengelig eller avviste forespørselen.');
      throw Object.assign(error, { status: response.status });
    }
    return response.json();
  }
  async function mutation(path: string, body?: object) {
    if (!navigator.locks) throw new Error('Nettleseren støtter ikke sikker innlogging.');
    return navigator.locks.request('private-auth-mutations', async () => {
      if (path !== '/auth/logout' && pending()) throw new Error('Fullfør utlogging først.');
      const proof = await request('/auth/csrf');
      if (typeof proof.csrf_token !== 'string') throw new Error('Tilgangen kunne ikke bekreftes.');
      if (path !== '/auth/logout' && pending()) throw new Error('Fullfør utlogging først.');
      return request(path, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': proof.csrf_token }, body: JSON.stringify(body ?? {}) });
    });
  }
  function clear(text: string) {
    generation.current++; setSession(null); setPassword(''); setUsername(''); setMessage(text);
  }
  async function logout() {
    if (!pending() && draftDirty.current && !window.confirm('Ulagrede endringer går tapt ved utlogging. Vil du logge ut?')) return;
    lockKnown.current = true;
    markPending(true); setLocked(true); clear('Utlogging er ikke bekreftet. Privat innhold er låst.'); setBusy(true);
    channel.current?.postMessage('logout-pending');
    const current = generation.current;
    try {
      const result = await mutation('/auth/logout');
      if (current !== generation.current) return;
      if (result.revoked !== true) throw new Error();
      markPending(false); lockKnown.current = false; setLocked(false); setMessage('Du er logget ut.');
      channel.current?.postMessage('logout-confirmed');
      setFocusLogin(true);
    } catch {
      if (current === generation.current) setMessage('Utlogging er ikke bekreftet. Privat innhold er låst. Prøv utlogging igjen når tjenesten er tilgjengelig.');
    } finally { if (current === generation.current) setBusy(false); }
  }
  async function restore() {
    if (pending()) { await logout(); return; }
    const current = ++generation.current;
    setBusy(true);
    try {
      const result = await request('/auth/session');
      if (current !== generation.current || pending()) return;
      if (!validSession(result)) throw new Error('Logg inn på nytt.');
      setSession(previous => previous?.account_id === result.account_id && previous.created_at === result.created_at ? previous : result); setSuspended(false); setMessage('Du er logget inn.');
    } catch (error: any) {
      if (current === generation.current) {
        if (error?.status === 401) { setSession(null); setSuspended(false); setMessage('Logg inn for å åpne privat arbeidsrom.'); }
        else { setSuspended(true); setMessage('Tilgangen kan ikke bekreftes. Privat innhold er skjult. Prøv igjen når tjenesten er tilgjengelig.'); }
      }
    } finally { if (current === generation.current) setBusy(false); }
  }
  async function login(event: React.FormEvent) {
    event.preventDefault();
    if (pending()) { await logout(); return; }
    const current = ++generation.current;
    setBusy(true); setMessage('Logger inn …');
    const credentials = { username, password };
    setPassword('');
    try {
      const result = await mutation('/auth/login', credentials);
      if (current !== generation.current || pending()) return;
      if (!validSession(result)) throw new Error('Tilgangen kunne ikke bekreftes.');
      setUsername(''); setSession(result); setSuspended(false); setMessage('Du er logget inn.');
    } catch (error) {
      if (current === generation.current) setMessage(error instanceof Error ? error.message : 'Innlogging er ikke bekreftet.');
    } finally { if (current === generation.current) setBusy(false); }
  }
  useEffect(() => {
    const notifications = new BroadcastChannel('private-access-security');
    channel.current = notifications;
    notifications.onmessage = event => {
      if (event.data === 'logout-pending') {
        lockKnown.current = true; setLocked(true); clear('Utlogging er ikke bekreftet. Privat innhold er låst.'); setBusy(false);
      } else if (event.data === 'logout-confirmed') {
        lockKnown.current = false; setLocked(false); clear('Du er logget ut.'); setBusy(false);
        setFocusLogin(true);
      }
    };
    void restore();
    // BFCache/history must not resurrect a private view; revalidate with the server.
    function hide() { generation.current++; setSuspended(true); setMessage('Kontrollerer tilgang …'); }
    function show() { void restore(); }
    function visibility() {
      if (document.visibilityState === 'hidden') hide();
      else show();
    }
    window.addEventListener('pagehide', hide);
    window.addEventListener('pageshow', show);
    document.addEventListener('visibilitychange', visibility);
    const monitor = window.setInterval(() => {
      if (pending() && !lockKnown.current) { lockKnown.current = true; setLocked(true); clear('Utlogging er ikke bekreftet. Privat innhold er låst.'); setBusy(false); }
    }, 500);
    return () => { generation.current++; notifications.close(); channel.current = null; clearInterval(monitor); window.removeEventListener('pagehide', hide); window.removeEventListener('pageshow', show); document.removeEventListener('visibilitychange', visibility); };
  }, []);
  useEffect(() => {
    if (!session) return;
    heading.current?.focus();
    const expire = () => { clear('Økten er utløpt. Logg inn på nytt.'); setBusy(false); setFocusLogin(true); };
    const remaining = Date.parse(session.expires_at) - Date.now();
    if (remaining <= 0) { expire(); return; }
    const timer = window.setTimeout(expire, remaining);
    return () => clearTimeout(timer);
  }, [session]);
  useEffect(() => {
    if (focusLogin && !session && !locked && !busy) { usernameInput.current?.focus(); setFocusLogin(false); }
  }, [focusLogin, session, locked, busy]);

  return <main>
    <p className="badge">Privat tilgang</p>
    <h1 ref={heading} tabIndex={-1}>{session && !locked ? 'Privat arbeidsrom' : 'Logg inn'}</h1>
    <p role="status" aria-label="Tilgangsstatus" aria-live="polite" className="status">{message}</p>
    {suspended && session && !locked && <button disabled={busy} onClick={() => void restore()}>Kontroller tilgang igjen</button>}
    {locked ? <button disabled={busy} onClick={() => void logout()}>Prøv utlogging igjen</button>
      : session ? <section aria-label="Privat arbeidsrom">
        <PrivateDrafts key={session.account_id + session.created_at} request={async path => { if (pending() || suspended) throw Error(); return request(path); }} mutation={mutation} dirtyChanged={value => { draftDirty.current = value; }} expired={() => { clear('Økten er utløpt. Logg inn på nytt.'); setBusy(false); setFocusLogin(true); }} suspended={suspended} />
        <p>Økten utløper {new Intl.DateTimeFormat('nb-NO', { dateStyle: 'short', timeStyle: 'short', timeZone: 'Europe/Oslo' }).format(new Date(session.expires_at))}.</p>
        <button disabled={busy} onClick={() => void logout()}>Logg ut</button>
      </section> : <form onSubmit={event => void login(event)} aria-label="Innlogging">
        <label htmlFor="private-username">Brukernavn</label>
        <input ref={usernameInput} id="private-username" name="username" autoComplete="username" required maxLength={100} value={username} onChange={event => setUsername(event.target.value)} disabled={busy} />
        <label htmlFor="private-password">Passord</label>
        <input id="private-password" name="password" type="password" autoComplete="current-password" required maxLength={256} value={password} onChange={event => setPassword(event.target.value)} disabled={busy} />
        <button disabled={busy} type="submit">Logg inn</button>
      </form>}
    <p>Tilgang opprettes av den som drifter løsningen. Bruk arbeidsrommet mens du står stille.</p>
    <a href="/">Åpne fiktiv demo</a>
  </main>;
}
