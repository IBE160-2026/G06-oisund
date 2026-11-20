import { PasswordRecovery, type RecoveryFields } from './PasswordRecovery';
import { PasswordChange, type PasswordFields } from './PasswordChange';
import { ThemeControl } from './theme';
import { privateNow, observePrivateTime } from './privateClock';
import { useEffect, useRef, useState } from 'react';
import { PrivateDrafts } from './PrivateDrafts';
import { readPdfBytes, waitForPdfAccess } from './pdfUpload';

const apiEnvironment = (import.meta as ImportMeta & { env: Record<string, string | undefined> }).env;
const configuredApi = apiEnvironment.VITE_PRIVATE_API_BASE;
if (configuredApi !== undefined && configuredApi !== '/private-api') throw Error('Invalid private API configuration');
const API = configuredApi ?? apiEnvironment.VITE_PRIVATE_API ?? 'http://127.0.0.1:8001';
// Only a logout lock, never an account, credential or private presentation. A cookie
// survives reload and is shared across tabs, unlike private browser data stores.
const PENDING = 'private_logout_pending';
const pending = () => document.cookie.split(';').some(c => c.trim() === PENDING + '=1');
function markPending(value: boolean) {
  document.cookie = `${PENDING}=${value ? '1' : ''}; Path=/; SameSite=Strict; Max-Age=${value ? 14 * 86400 : 0}${location.protocol === 'https:' ? '; Secure' : ''}`;
}
type Session = { account_id: string; created_at: string; expires_at: string };
const sameSession = (left: Session | null, right: Session) => left?.account_id === right.account_id && left.created_at === right.created_at;
function validSession(value: unknown): value is Session {
  const s = value as Session;
  return !!s && typeof s.account_id === 'string' && /^[0-9a-f-]{36}$/i.test(s.account_id)
    && Number.isFinite(Date.parse(s.created_at)) && Number.isFinite(Date.parse(s.expires_at))
    && Date.parse(s.expires_at) - Date.parse(s.created_at) === 14 * 86400000
    && Date.parse(s.expires_at) > privateNow();
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
  const settingsBlocked = useRef(false);
  const [settings, setSettings] = useState(false);
  const [recovery, setRecovery] = useState(false);
  const recoveryButton = useRef<HTMLButtonElement>(null);
  const recoveryOpen = useRef(false);
  const [passwordBusy, setPasswordBusy] = useState(false);
  // Only outcome metadata survives lifecycle invalidation; never credentials.
  const passwordOutcome = useRef<'pending' | 'unknown' | 'changed' | null>(null);
  const settingsButton = useRef<HTMLButtonElement>(null);
  const activeSession = useRef<Session | null>(null);
  const accessSuspended = useRef(false);
  const restoring = useRef<Promise<void> | null>(null);

  function recoveryScreen(value: boolean) { recoveryOpen.current = value; setRecovery(value); }
  function suspend(value: boolean) { accessSuspended.current = value; setSuspended(value); }
  function acceptSession(value: Session) { activeSession.current = value; setSession(previous => sameSession(previous, value) ? previous : value); }

  async function workspace(expected: Session, action: (check: () => void) => Promise<any>, signal?: AbortSignal, readOnly = false) {
    const epoch = generation.current;
    const check = () => {
      if (epoch !== generation.current || !sameSession(activeSession.current, expected) || pending() || accessSuspended.current || signal?.aborted) throw Error('Tilgangen må kontrolleres på nytt.');
    };
    check();
    if (!navigator.locks) throw Error('Nettleseren støtter ikke sikker innlogging.');
    const validate = async () => {
      check();
      let current: unknown;
      try {
        current = await request('/auth/session', signal ? { signal: AbortSignal.any([signal, AbortSignal.timeout(10000)]) } : undefined);
      } catch (error: any) {
        check();
        if (error?.status !== 401) {
          suspend(true); setBusy(false);
          setMessage('Tilgangen kan ikke bekreftes. Privat innhold er skjult. Prøv igjen når tjenesten er tilgjengelig.');
        }
        throw error;
      }
      check();
      const candidate = current as Session;
      if (sameSession(candidate, expected) && Date.parse(candidate.expires_at) <= privateNow()) {
        throw Object.assign(Error('Økten er utløpt.'), { status: 401 });
      }
      if (!validSession(current) || !sameSession(current, expected)) {
        clear('Innloggingen er endret i et annet vindu. Privat innhold er fjernet. Kontroller tilgang på nytt.');
        suspend(false); setBusy(false); setFocusLogin(true);
        throw Error('Innloggingen er endret.');
      }
    };
    const locked = <T,>(run: () => Promise<T>) => navigator.locks.request('private-auth-mutations', { signal }, run);
    try {
      if (readOnly) {
        // Slow reads must not block save/logout. Validate both sides so a reply
        // fetched across a cookie change cannot enter the old workspace.
        await locked(validate);
        check();
        const value = await action(check);
        await locked(validate);
        check();
        return value;
      }
      return await locked(async () => {
        await validate();
        const value = await action(check);
        check();
        return value;
      });
    } catch (error: any) {
      // A late 401 must not reach an older child's expiry callback after a
      // hide/show cycle has already restored this same session successfully.
      if (epoch !== generation.current || !sameSession(activeSession.current, expected)) throw Error('Forespørselen er ikke lenger aktuell.');
      if (error?.status === 401 && epoch === generation.current && sameSession(activeSession.current, expected)) {
        clear('Økten er utløpt. Logg inn på nytt.'); suspend(false); setBusy(false); setFocusLogin(true);
      }
      throw error;
    }
  }

  async function request(path: string, options?: RequestInit) {
    const requestedAt = performance.now();
    const response = await fetch(API + path, { ...options, credentials: 'include', cache: 'no-store', signal: options?.signal ?? AbortSignal.timeout(10000) });
    observePrivateTime(response.headers.get('Date'), requestedAt, true);
    if (!response.ok || !response.headers.get('content-type')?.includes('application/json')) {
      let apiDetail: unknown;
      if (!response.ok && response.headers.get('content-type')?.includes('application/json')) {
        try { const body = await response.json(); if (body && Object.keys(body).join() === 'detail') apiDetail = body.detail; } catch { /* A transport status alone never settles an uncertain write. */ }
      }
      const error = new Error(response.status === 401 ? 'Logg inn på nytt. Brukernavn eller passord kan være feil.' : response.status === 429 ? 'For mange forsøk. Vent 15 minutter før du prøver igjen.' : 'Tjenesten er utilgjengelig eller avviste forespørselen.');
      throw Object.assign(error, { status: response.status, apiDetail });
    }
    try { return await response.json(); }
    catch (error) {
      if (error instanceof SyntaxError) throw Object.assign(Error('Serveren returnerte et ugyldig svar.'), { importFailure: 'response' });
      throw error;
    }
  }
  async function upload(file: File, signal: AbortSignal) {
    if (!session) throw Error();
    const bytes = await readPdfBytes(file, signal);
    // Android's native picker can return its change event before the visible
    // page's session check finishes. Wait for that check, then let workspace
    // enforce the original account/session and cancellation as usual.
    await waitForPdfAccess(
      () => !accessSuspended.current && !restoring.current && document.visibilityState === 'visible',
      () => sameSession(activeSession.current, session) && !pending(), signal);
    return workspace(session, async check => {
      const proof = await request('/auth/csrf', { signal: AbortSignal.any([signal, AbortSignal.timeout(10000)]) });
      check();
      if (typeof proof.csrf_token !== 'string') throw Error();
      return request('/imports/pdf', { method: 'POST', headers: { 'Content-Type': 'application/pdf', 'X-CSRF-Token': proof.csrf_token }, body: bytes, signal: AbortSignal.any([signal, AbortSignal.timeout(45000)]) });
    }, signal);
  }
  async function mutation(path: string, body?: object, expected?: Session, dispatched?: () => void) {
    if (!navigator.locks) throw new Error('Nettleseren støtter ikke sikker innlogging.');
    const send = async (check: () => void = () => {}) => {
      if (path !== '/auth/logout' && pending()) throw new Error('Fullfør utlogging først.');
      const proof = await request('/auth/csrf');
      check();
      if (typeof proof.csrf_token !== 'string') throw new Error('Tilgangen kunne ikke bekreftes.');
      if (path !== '/auth/logout' && pending()) throw new Error('Fullfør utlogging først.');
      dispatched?.();
      const result = await request(path, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': proof.csrf_token }, body: JSON.stringify(body ?? {}) });
      if (path === '/auth/login' && validSession(result)) channel.current?.postMessage('session-changed');
      return result;
    };
    return expected ? workspace(expected, send) : navigator.locks.request('private-auth-mutations', () => send());
  }
  function clear(text: string) {
    generation.current++; recoveryScreen(false); setSettings(false); activeSession.current = null; setSession(null); setPassword(''); setUsername(''); setMessage(text);
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
      markPending(false); lockKnown.current = false; setLocked(false);
      setMessage(passwordOutcome.current === 'changed' ? 'Passordet er endret. Du er logget ut. Logg inn med det nye passordet.' : passwordOutcome.current ? 'Du er logget ut. Prøv å logge inn med det nye passordet. Resultatet av passordendringen var ikke bekreftet.' : 'Du er logget ut.');
      passwordOutcome.current = null;
      channel.current?.postMessage('logout-confirmed');
      setFocusLogin(true);
    } catch {
      if (current === generation.current) setMessage('Utlogging er ikke bekreftet. Privat innhold er låst. Prøv utlogging igjen når tjenesten er tilgjengelig.');
    } finally { if (current === generation.current) setBusy(false); }
  }
  function openSettings() {
    if (settingsBlocked.current) { setMessage('Lagre eller forkast endringer og avklar pågående handlinger før du endrer passord.'); return; }
    setSettings(true); setMessage('Brukerinnstillinger');
  }
  function cancelSettings() {
    setSettings(false); setMessage('Du er logget inn.');
    requestAnimationFrame(() => settingsButton.current?.focus());
  }
  async function changePassword(fields: PasswordFields) {
    if (!session || settingsBlocked.current || passwordBusy) throw Error('Avklar pågående arbeid først.');
    const current = generation.current;
    setPasswordBusy(true);
    try {
      const result = await mutation('/auth/password/change', fields, session, () => { passwordOutcome.current = 'pending'; });
      if (result?.changed !== true || Object.keys(result).join() !== 'changed') throw Error();
      passwordOutcome.current = 'changed'; presentPasswordOutcome();
      channel.current?.postMessage('session-changed'); setFocusLogin(true);
    } catch (error: any) {
      if (!passwordOutcome.current) {
        // No password POST was dispatched. Preserve suspension/expiry decisions
        // already made by workspace; only the current presentation gets feedback.
        if (current !== generation.current) return;
        const text = 'Passordendringen ble ikke sendt. Passordfeltene er tømt. Kontroller tilgang og prøv igjen når tjenesten er tilgjengelig.';
        setMessage(text);
        throw Error(text);
      }
      if (current === generation.current && error?.status === 400 && error.apiDetail?.code === 'current_password') {
        passwordOutcome.current = null;
        throw Object.assign(Error('Gjeldende passord er feil.'), { field: 'current_password' });
      }
      if (current === generation.current && [403, 422, 429].includes(error?.status) && error.apiDetail) {
        passwordOutcome.current = null;
        throw Error(error.status === 429 ? error.message : 'Kontroller feltene og prøv igjen.');
      }
      // A lost/malformed reply may follow a commit. Never retry credentials.
      passwordOutcome.current = 'unknown'; presentPasswordOutcome();
      channel.current?.postMessage('logout-pending');
    } finally { setPasswordBusy(false); }
  }
  async function recoverPassword(fields: RecoveryFields) {
    if (session || passwordBusy || pending()) throw Error('Logg ut før du gjenoppretter tilgang.');
    const current = generation.current;
    setPasswordBusy(true);
    try {
      const result = await mutation('/auth/password/recover', fields, undefined, () => {
        if (current !== generation.current || activeSession.current || accessSuspended.current) throw Error();
        passwordOutcome.current = 'pending';
      });
      if (result?.changed !== true || Object.keys(result).join() !== 'changed') throw Error();
      passwordOutcome.current = 'changed'; presentPasswordOutcome();
      channel.current?.postMessage('session-changed'); setFocusLogin(true);
    } catch (error: any) {
      if (!passwordOutcome.current) {
        if (current !== generation.current) return;
        throw Error('Forespørselen ble ikke sendt. Feltene er tømt. Kontroller tilgang og prøv igjen.');
      }
      if (current === generation.current && error?.status === 400 && error.apiDetail === 'Koden kunne ikke brukes. Kontroller opplysningene eller kontakt operatøren.') {
        passwordOutcome.current = null;
        throw Object.assign(Error('Koden kunne ikke brukes. Kontroller opplysningene eller kontakt operatøren. Hvis et tidligere resultat var usikkert, prøv innlogging med det nye passordet først.'), { field: 'code' });
      }
      if (current === generation.current && [403, 409, 422, 429].includes(error?.status) && typeof error.apiDetail === 'string') {
        passwordOutcome.current = null;
        if (error.status === 409) { recoveryScreen(false); await restore(); return; }
        throw Error(error.status === 429 ? error.message : 'Kontroller feltene og prøv igjen.');
      }
      passwordOutcome.current = 'unknown'; presentPasswordOutcome();
      channel.current?.postMessage('logout-pending');
    } finally { setPasswordBusy(false); }
  }
  function presentPasswordOutcome() {
    const changed = passwordOutcome.current === 'changed';
    if (!changed) { lockKnown.current = true; markPending(true); setLocked(true); }
    const finishLogout = pending() || lockKnown.current;
    if (finishLogout) setLocked(true);
    clear(changed ? (finishLogout ? 'Passordet er endret. Fullfør utlogging med «Prøv utlogging igjen», og logg deretter inn med det nye passordet.' : 'Passordet er endret. Alle enheter er logget ut. Logg inn med det nye passordet.') : 'Resultatet av passordendringen er ukjent. Passordene er fjernet. Fullfør utlogging, og prøv deretter å logge inn med det nye passordet. Kontakt operatøren for ny kode ved behov; ikke send koden på nytt automatisk.');
    suspend(false); setBusy(false);
  }
  function restore() {
    const attempt = restoreSession();
    restoring.current = attempt;
    void attempt.finally(() => { if (restoring.current === attempt) restoring.current = null; });
    return attempt;
  }
  async function restoreSession() {
    if (passwordOutcome.current) { presentPasswordOutcome(); return; }
    if (pending()) { await logout(); return; }
    const current = ++generation.current;
    setBusy(true);
    try {
      const result = await request('/auth/session');
      if (current !== generation.current || pending()) return;
      if (!validSession(result)) throw new Error('Logg inn på nytt.');
      acceptSession(result); suspend(false); setMessage('Du er logget inn.');
    } catch (error: any) {
      if (current === generation.current) {
        if (error?.status === 401) { activeSession.current = null; setSession(null); suspend(false); setMessage('Logg inn for å åpne privat arbeidsrom.'); }
        else { suspend(true); setMessage('Tilgangen kan ikke bekreftes. Privat innhold er skjult. Prøv igjen når tjenesten er tilgjengelig.'); }
      }
    } finally { if (current === generation.current) setBusy(false); }
  }
  async function login(event: React.FormEvent) {
    event.preventDefault();
    if (Array.from(password).length > 256) { setMessage('Passord må ha høyst 256 tegn.'); return; }
    if (pending()) { await logout(); return; }
    const current = ++generation.current;
    setBusy(true); setMessage('Logger inn …');
    const credentials = { username, password };
    setPassword('');
    try {
      const result = await mutation('/auth/login', credentials);
      if (current !== generation.current || pending()) return;
      if (!validSession(result)) throw new Error('Tilgangen kunne ikke bekreftes.');
      passwordOutcome.current = null;
      setUsername(''); acceptSession(result); suspend(false); setMessage('Du er logget inn.');
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
      } else if (event.data === 'session-changed' && (activeSession.current || recoveryOpen.current)) {
        clear('Innloggingen er endret i et annet vindu. Privat innhold er fjernet. Kontroller tilgang på nytt.');
        suspend(false); setBusy(false); setFocusLogin(true);
      }
    };
    void restore();
    // BFCache/history must not resurrect a private view; revalidate with the server.
    function hide() {
      generation.current++; recoveryScreen(false); suspend(true); setMessage('Kontrollerer tilgang …');
      if (passwordOutcome.current) { clear('Kontrollerer passordendringen …'); }
    }
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
    let timer: number;
    const checkDeadline = () => {
      const remaining = Date.parse(session.expires_at) - privateNow();
      if (remaining <= 0) { expire(); return; }
      // Recheck the original deadline as the shared server clock advances.
      timer = window.setTimeout(checkDeadline, Math.min(remaining, 1000));
    };
    checkDeadline();
    return () => clearTimeout(timer);
  }, [session]);
  useEffect(() => {
    if (focusLogin && !session && !locked && !busy) { usernameInput.current?.focus(); setFocusLogin(false); }
  }, [focusLogin, session, locked, busy]);

  return <main className={session && !locked ? 'private-workspace' : undefined}>
    <ThemeControl /><header className="private-access-header"><p className="badge">Privat tilgang</p>
    <h1 ref={heading} tabIndex={-1}>{session && !locked ? 'Privat arbeidsrom' : 'Logg inn'}</h1>
    <p role="status" aria-label="Tilgangsstatus" aria-live="polite" className="status">{message}</p></header>
    {suspended && session && !locked && <button disabled={busy} onClick={() => void restore()}>Kontroller tilgang igjen</button>}
    {locked ? <button disabled={busy || passwordBusy} onClick={() => void logout()}>Prøv utlogging igjen</button>
      : session ? <section aria-label="Privat arbeidsrom">
        <div hidden={settings}><PrivateDrafts key={session.account_id + session.created_at} upload={upload} request={path => workspace(session, () => request(path), undefined, true)} mutation={(path, body) => mutation(path, body, session)} dirtyChanged={value => { draftDirty.current = value; }} settingsBlocked={value => { settingsBlocked.current = value; }} expired={() => { if (sameSession(activeSession.current, session)) { clear('Økten er utløpt. Logg inn på nytt.'); setBusy(false); setFocusLogin(true); } }} suspended={suspended} /></div>
        {settings && !suspended && <PasswordChange submit={changePassword} cancel={cancelSettings} busy={passwordBusy} />}
        <p>Økten utløper {new Intl.DateTimeFormat('nb-NO', { dateStyle: 'short', timeStyle: 'short', timeZone: 'Europe/Oslo' }).format(new Date(session.expires_at))}.</p>
        <button ref={settingsButton} hidden={settings} disabled={busy || suspended} onClick={openSettings}>Brukerinnstillinger</button>
        <button disabled={busy || passwordBusy} onClick={() => void logout()}>Logg ut</button>
      </section> : recovery && !suspended ? <PasswordRecovery submit={recoverPassword} busy={passwordBusy} cancel={() => { recoveryScreen(false); requestAnimationFrame(() => recoveryButton.current?.focus()); }} /> : <form onSubmit={event => void login(event)} aria-label="Innlogging">
        <label htmlFor="private-username">Brukernavn</label>
        <input ref={usernameInput} id="private-username" name="username" autoComplete="username" required maxLength={100} value={username} onChange={event => setUsername(event.target.value)} disabled={busy} />
        <label htmlFor="private-password">Passord</label>
        <input id="private-password" name="password" type="password" autoComplete="current-password" required value={password} onChange={event => setPassword(event.target.value)} disabled={busy} />
        <button disabled={busy} type="submit">Logg inn</button>
      </form>}
    {!session && !locked && !recovery && <button ref={recoveryButton} disabled={busy || passwordBusy || suspended} onClick={() => { passwordOutcome.current = null; setPassword(''); recoveryScreen(true); }}>Glemt passord?</button>}
    <p>Tilgang opprettes av den som drifter løsningen. Bruk arbeidsrommet mens du står stille.</p>
    <a href="/">Åpne fiktiv demo</a>
  </main>;
}
