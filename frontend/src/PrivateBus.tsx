import { useEffect, useRef, useState } from 'react';
import { normalizeBus as normalized, busError } from './busValue';

type Bus = { workday_id: string; physical_bus: string | null; revision: number; expires_at: string };
type Operation = { operation_id: string; expected_revision: number; physical_bus: string | null };
type Props = { id: string; expiresAt: string; request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>; suspended: boolean; expired: () => void; lock: (value: boolean) => void; availability: (value: boolean) => void };
export function PrivateBus({ id, expiresAt, request, mutation, suspended, expired, lock, availability }: Props) {
  const [saved, setSaved] = useState<Bus | null>(null), [text, setText] = useState('');
  const [pending, setPending] = useState<Operation | null>(null), [comparison, setComparison] = useState<Bus | null>(null);
  const [busy, setBusy] = useState(true), [message, setMessage] = useState('Henter gjeldende registrering …');
  const [focusInput, setFocusInput] = useState(false);
  const [available, setAvailable] = useState(true);
  const alive = useRef(true), sending = useRef(false), editing = useRef(false), generation = useRef(0);
  const input = useRef<HTMLInputElement>(null);
  const path = '/workdays/' + id + '/physical-bus';
  useEffect(() => { if (focusInput && saved && !busy && !pending && !comparison && !suspended) { input.current?.focus(); setFocusInput(false); } }, [focusInput, saved, busy, pending, comparison, suspended]);
  function valid(v: any): v is Bus {
    return v && Object.keys(v).sort().join() === 'expires_at,physical_bus,revision,workday_id' && v.workday_id === id
      && Number.isSafeInteger(v.revision) && v.revision >= 0 && (v.physical_bus === null || typeof v.physical_bus === 'string' && Array.from(v.physical_bus).length <= 100 && !v.physical_bus.includes('\0') && normalized(v.physical_bus) !== null)
      && Date.parse(v.expires_at) === Date.parse(expiresAt) && Date.parse(expiresAt) > Date.now();
  }
  function adopt(value: Bus) { setSaved(value); setText(value.physical_bus ?? ''); setComparison(null); setPending(null); editing.current = false; lock(false); }
  async function current(): Promise<Bus> {
    try {
      const value = await request(path);
      if (!valid(value)) throw Error();
      if (alive.current) { setAvailable(true); availability(true); }
      return value;
    } catch (error: any) {
      if ([404, 410].includes(error?.status)) {
        // A denied read has no successful body for the wrapper to post-validate.
        // Revalidate the displayed session before retaining any local input.
        await request('/auth/session');
        if (alive.current) { setAvailable(false); availability(false); }
      }
      throw error;
    }
  }
  async function revalidate() {
    if (sending.current || suspended) return;
    setBusy(true);
    try { const value = await current(); if (alive.current) { if (!editing.current && !pending) adopt(value); else setSaved(value); setMessage(pending ? 'Plantilgangen er kontrollert. Busslagringen er fortsatt uavklart; kontroller samme forsøk.' : editing.current ? 'Plantilgangen er kontrollert. Ditt lokale forslag er beholdt.' : 'Plantilgangen og gjeldende registrering er kontrollert.'); } }
    catch (error: any) { if (alive.current) { if (error?.status === 401) expired(); else setMessage('Plantilgangen kan ikke bekreftes. Lokalt forslag og uavklart forsøk er beholdt.'); } }
    finally { if (alive.current) setBusy(false); }
  }
  async function load() {
    if (editing.current) return;
    const version = ++generation.current; setBusy(true);
    try {
      const value = await current();
      if (!alive.current || version !== generation.current || editing.current) return;
      if (!valid(value)) throw Error();
      adopt(value); setMessage(value.revision ? 'Lagret manuell registrering.' : value.physical_bus ? 'Manuell verdi fra bekreftelsen. Ingen ny registrering er lagret.' : 'Ukjent. Ingen fysisk buss er registrert.');
    } catch (error: any) { if (alive.current && version === generation.current) { if (error?.status === 401) expired(); else { setSaved(null); setMessage('Registreringen kunne ikke hentes. Prøv igjen.'); } } }
    finally { if (alive.current && version === generation.current) setBusy(false); }
  }
  useEffect(() => { alive.current = true; void load(); return () => { alive.current = false; generation.current++; lock(false); }; }, [id]);
  function change(value: string) {
    editing.current = !!busError(value) || normalized(value) !== saved?.physical_bus; generation.current++; lock(editing.current); setText(value); setMessage(editing.current ? 'Ulagret manuell registrering.' : 'Ingen ulagret bussendring.');
    const error = busError(value); if (error) setMessage(error);
  }
  async function send(lookup = false) {
    if (!saved || sending.current || suspended) return;
    if (!pending && busError(text)) { setMessage(busError(text)!); return; }
    const operation = pending ?? { operation_id: crypto.randomUUID(), expected_revision: saved.revision, physical_bus: normalized(text) };
    sending.current = true; editing.current = true; lock(true); setPending(operation); setBusy(true); setMessage('Lagringen er uavklart til svaret er kontrollert.');
    let verifying = false;
    try {
      const receipt = lookup ? await request('/workday-bus-operations/' + operation.operation_id) : await mutation(path, operation);
      if (!alive.current) return;
      if (!receipt || Object.keys(receipt).sort().join() !== 'operation_id,result' || receipt.operation_id !== operation.operation_id || !valid(receipt.result)
        || receipt.result.revision !== operation.expected_revision + 1 || receipt.result.physical_bus !== operation.physical_bus) throw Error();
      verifying = true;
      const latest = await current();
      if (!alive.current) return;
      if (latest.revision < receipt.result.revision || latest.revision === receipt.result.revision && latest.physical_bus !== receipt.result.physical_bus) throw Error();
      if (latest.revision > receipt.result.revision) { setPending(null); setComparison(latest); setMessage('Forsøket ble lagret, men en nyere registrering finnes. Sammenlign og last inn lagret verdi.'); }
      else { adopt(latest); setFocusInput(true); setMessage('Fysisk buss er lagret.'); }
    } catch (error: any) {
      if (!alive.current) return;
      if (error?.status === 401) { expired(); return; }
      if (!verifying && !lookup && error?.status === 429 && error.apiDetail && Object.keys(error.apiDetail).sort().join() === 'code,message' && error.apiDetail.code === 'bus_receipt_capacity' && error.apiDetail.message === 'For mange lagringsforsøk. Vent til tidligere planer utløper.') {
        try {
          await request('/auth/session');
          if (!alive.current) return;
          setPending(null); setFocusInput(true); setMessage('Lagringen ble avvist: grensen på 2000 lagringsforsøk er nådd. Forslaget er beholdt og kan redigeres eller avbrytes. Vent til tidligere planer utløper før ny lagring.');
        } catch { if (alive.current) setMessage('Lagringen er uavklart. Kontroller eller prøv samme lagring igjen.'); }
        return;
      }
      if (!verifying && !lookup && error?.status === 409) {
        try { const latest = await current(); if (!alive.current) return; if (latest.revision <= operation.expected_revision) throw Error(); setComparison(latest); setPending(null); setMessage('Registreringen er endret i et annet vindu. Sammenlign og last inn lagret verdi.'); }
        catch { if (alive.current) setMessage('Lagringen er uavklart. Kontroller eller prøv samme lagring igjen.'); }
      } else {
        if (!verifying && [404, 410].includes(error?.status)) { try { await current(); } catch { /* Preserve the same unresolved operation; current() guards presentation. */ } }
        if (alive.current) setMessage('Lagringen er uavklart. Kontroller eller prøv samme lagring igjen.');
      }
    } finally { sending.current = false; if (alive.current) setBusy(false); }
  }
  return <section className="private-bus" aria-label="Fysisk buss">
    <h4>Fysisk buss</h4><p>Gjeldende manuell registrering. Vognløp og sanntidsverdi fastsetter ikke hvilken buss du kjører.</p>
    <p role="status" aria-label="Bussstatus">{message}</p>
    {!available && <p>Gjeldende buss og planfakta er skjult fordi plantilgangen ikke er bekreftet. Teksten under er ditt lokale forslag.</p>}
    {!available && <button disabled={busy || suspended} onClick={() => void revalidate()}>Kontroller plantilgangen</button>}
    {saved ? <>{available && <p>Lagret verdi: <span className="bus-value">{saved.physical_bus ?? 'Ukjent'}</span> · bussversjon {saved.revision}</p>}
      <label>Fysisk buss<input ref={input} value={text} autoComplete="off" aria-invalid={!!busError(text)} aria-describedby={busError(text) ? 'physical-bus-error' : undefined} disabled={busy || !!pending || !!comparison || suspended} onChange={event => change(event.target.value)} /></label>
      <button type="button" disabled={busy || !!pending || !!comparison || suspended} onClick={() => change('')}>Tøm fysisk buss</button>
      {busError(text) && <p id="physical-bus-error">{busError(text)}</p>}
      <p>Inntil 100 tegn. Tomt felt betyr ukjent. Tekst og innledende nuller bevares.</p>
      {comparison && available && <div className="import-warning"><p>Nyere lagret verdi: <span className="bus-value">{comparison.physical_bus ?? 'Ukjent'}</span> · bussversjon {comparison.revision}</p><p>Ditt inntastede forslag: <span className="bus-value">{normalized(text) ?? 'Ukjent'}</span></p><button disabled={busy || suspended} onClick={() => { adopt(comparison); setFocusInput(true); setMessage('Lagret verdi er lastet inn. Du kan korrigere den og lagre på nytt.'); }}>Last inn lagret buss</button></div>}
      {pending ? <div className="controls"><button disabled={busy || suspended} onClick={() => void send()}>Prøv samme busslagring igjen</button><button disabled={busy || suspended} onClick={() => void send(true)}>Kontroller busslagringen</button></div>
        : !comparison && <div className="controls"><button disabled={busy || suspended || !editing.current || !!busError(text)} onClick={() => void send()}>Lagre fysisk buss</button><button disabled={busy || suspended || !editing.current} onClick={() => { adopt(saved); setMessage('Endringen er avbrutt. Lagret registrering er uendret.'); input.current?.focus(); }}>Avbryt bussendring</button></div>}</>
      : <button disabled={busy || suspended} onClick={() => void load()}>Hent bussregistreringen igjen</button>}
  </section>;
}
