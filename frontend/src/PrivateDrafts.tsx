import { useEffect, useRef, useState } from 'react';

type Activity = { id: string } & Record<string, string | null>;
type Content = { service_date: string | null; vehicle_duty: string | null; realtime_duty: string | null; physical_bus: null; activities: Activity[] };
type Saved = { id: string; created_at: string; expires_at: string; revision: number; draft: Content };
type Summary = Pick<Saved, 'id' | 'expires_at' | 'revision'> & { service_date: string | null };
type Pending = { path: string; body: { operation_id: string; expected_revision: number; draft: Content } };
type Props = { request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>; dirtyChanged: (dirty: boolean) => void; expired: () => void; suspended: boolean };
const empty = (): Content => ({ service_date: null, vehicle_duty: null, realtime_duty: null, physical_bus: null, activities: [] });
const fields = [['type', 'Aktivitetstype'], ['raw_code', 'Opprinnelig kode'], ['start', 'Start med dato og Oslo-offset'], ['end', 'Slutt med dato og Oslo-offset'], ['source_start', 'Opprinnelig startklokke'], ['source_end', 'Opprinnelig sluttklokke'], ['from_place', 'Fra sted'], ['to_place', 'Til sted'], ['trip', 'Turnummer'], ['line', 'Linje'], ['direction', 'Retning'], ['uncertainty', 'Usikkerhet / ukjente fakta'], ['provenance', 'Kilde / manuell rettelse']] as const;
const uuid = (v: unknown): v is string => typeof v === 'string' && /^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(v);
const canonical = (value: any): string => JSON.stringify(value, (_, v) => v && typeof v === 'object' && !Array.isArray(v) ? Object.fromEntries(Object.keys(v).sort().map(k => [k, v[k]])) : v);
const calendar = (v: unknown) => typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v) && Number.isFinite(Date.parse(v)) && new Date(v).toISOString().slice(0, 10) === v;
function instant(v: any) {
  if (v === null) return true;
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}T([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?[+-]([01]\d|2[0-3]):[0-5]\d$/.test(v) || !calendar(v.slice(0, 10)) || !Number.isFinite(Date.parse(v))) return false;
  // Browser ICU may alias historical Oslo rules to Berlin. The backend validates
  // those offsets; keep syntax/calendar/interval validation here without guessing.
  if (Number(v.slice(0, 4)) < 1970) return true;
  const local = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Oslo', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(new Date(v));
  return local === v.slice(0, 16).replace('T', ' ');
}
function validContent(draft: any) {
  const nullable = (v: any, max: number) => v === null || (typeof v === 'string' && v.length <= max);
  return draft && Object.keys(draft).sort().join() === 'activities,physical_bus,realtime_duty,service_date,vehicle_duty'
    && (draft.service_date === null || calendar(draft.service_date)) && nullable(draft.vehicle_duty, 100)
    && (draft.realtime_duty === null || typeof draft.realtime_duty === 'string' && /^\d{3}$/.test(draft.realtime_duty)) && draft.physical_bus === null
    && Array.isArray(draft.activities) && draft.activities.length <= 200
    && new Set(draft.activities.map((a: any) => a?.id)).size === draft.activities.length
    && draft.activities.every((a: any) => a && uuid(a.id) && Object.keys(a).length === fields.length + 1
      && fields.every(([key]) => nullable(a[key], ['uncertainty', 'provenance'].includes(key) ? 1000 : ['from_place', 'to_place'].includes(key) ? 300 : key === 'start' || key === 'end' ? 40 : 100))
      && instant(a.start) && instant(a.end) && (!a.start || !a.end || Date.parse(a.end) >= Date.parse(a.start)));
}
function valid(value: any): value is Saved {
  return value && uuid(value.id) && Number.isInteger(value.revision) && value.revision > 0
    && Number.isFinite(Date.parse(value.created_at)) && Date.parse(value.expires_at) - Date.parse(value.created_at) === 7 * 86400000
    && Date.parse(value.expires_at) > Date.now() && validContent(value.draft);
}

export function PrivateDrafts({ request, mutation, dirtyChanged, expired, suspended }: Props) {
  const [list, setList] = useState<Summary[]>([]);
  const [saved, setSaved] = useState<Saved | null>(null);
  const [content, setContent] = useState<Content>(empty);
  const [pending, setPending] = useState<Pending | null>(null);
  const [comparison, setComparison] = useState<Saved | null>(null);
  const [message, setMessage] = useState('Nytt utkast. Ikke lagret.');
  const [busy, setBusy] = useState(false);
  const [draftExpired, setDraftExpired] = useState(false);
  const alive = useRef(true);
  const title = useRef<HTMLHeadingElement>(null);
  const dirty = canonical(content) !== canonical(saved?.draft ?? empty()) || !!pending;
  function failed(error: any) {
    if (error?.status === 401) { expired(); return; }
    setMessage(error?.status === 410 ? 'Utkastet eller lagringsforsøket er utløpt. Lokale endringer er ikke lagret.' : error?.status === 404 ? 'Tilgangen ble avvist.' : 'Tjenesten er utilgjengelig. Lokale endringer er ikke lagret.');
  }
  async function refresh() {
    try { const result = await request('/drafts'); if (alive.current && Array.isArray(result.drafts)) setList(result.drafts); }
    catch (error) { if (alive.current) failed(error); }
  }
  useEffect(() => { alive.current = true; void refresh(); return () => { alive.current = false; }; }, []);
  useEffect(() => { dirtyChanged(dirty); return () => dirtyChanged(false); }, [dirty]);
  useEffect(() => {
    setDraftExpired(false);
    if (!saved) return;
    const expire = () => { setDraftExpired(true); setMessage('Utkastet er utløpt. Lokale endringer er ikke lagret.'); };
    const remaining = Date.parse(saved.expires_at) - Date.now();
    if (remaining <= 0) { expire(); return; }
    const timer = window.setTimeout(expire, remaining);
    return () => clearTimeout(timer);
  }, [saved]);
  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => { if (dirty) { event.preventDefault(); event.returnValue = ''; } };
    const navigate = (event: MouseEvent) => { if (dirty && (event.target as Element)?.closest('a') && !window.confirm('Ulagrede endringer går tapt. Vil du fortsette?')) event.preventDefault(); };
    window.addEventListener('beforeunload', warn); document.addEventListener('click', navigate);
    return () => { window.removeEventListener('beforeunload', warn); document.removeEventListener('click', navigate); };
  }, [dirty]);
  function adopt(value: Saved) { setSaved(value); setContent(value.draft); setPending(null); setComparison(null); setMessage(`Lagret. Versjon ${value.revision}.`); title.current?.focus(); }
  async function reopen(id: string) {
    if (dirty && !window.confirm('Ulagrede endringer går tapt. Åpne lagret utkast?')) return;
    setBusy(true);
    try { const value = await request('/drafts/' + id); if (!valid(value) || value.id !== id) throw Error(); if (alive.current) adopt(value); }
    catch (error) { if (alive.current) failed(error); }
    finally { if (alive.current) setBusy(false); }
  }
  async function acknowledge(value: any, operation: Pending) {
    if (!valid(value) || value.revision !== operation.body.expected_revision + 1 || canonical(value.draft) !== canonical(operation.body.draft)
      || (saved && value.id !== saved.id)) throw Error('Invalid acknowledgement');
    if (alive.current) { adopt(value); await refresh(); }
  }
  async function send(operation: Pending) {
    try { await acknowledge(await mutation(operation.path, operation.body), operation); }
    catch (error: any) {
      if (!alive.current) return;
      if (error?.status === 401) { expired(); return; }
      if (error?.status === 409) {
        setMessage('Konflikt. Dine lokale endringer er beholdt. Sammenlign med lagret versjon.');
        if (saved) { try { const value = await request('/drafts/' + saved.id); if (alive.current && valid(value)) setComparison(value); } catch (e) { failed(e); } }
      } else if ([404, 410, 413, 422].includes(error?.status)) {
        setPending(null);
        if (error.status === 413) setMessage('Utkastet er for stort. Forkort tekst eller fjern aktiviteter før du lagrer igjen. Ingen endringer er lagret.');
        else if (error.status === 422) setMessage('Kontroller feltene. Bruk eksplisitt dato og gyldig Oslo-offset; slutt kan ikke være før start. Ingen endringer er lagret.');
        else failed(error);
      } else setMessage('Lagring er uavklart. Behold siden åpen. Kontroller eller prøv samme lagringsforsøk igjen.');
    }
  }
  async function save() {
    setBusy(true); setMessage('Lagrer …');
    try {
      let operation = pending;
      if (!operation) {
        const candidate = { operation_id: '00000000-0000-4000-8000-000000000000', expected_revision: saved?.revision ?? 0, draft: content };
        if (new TextEncoder().encode(JSON.stringify(candidate)).byteLength > 1048576) {
          setMessage('Utkastet er for stort. Forkort tekst eller fjern aktiviteter før du lagrer igjen. Ingen endringer er lagret.');
          return;
        }
        const issued = await mutation('/draft-operations', { draft_id: saved?.id ?? null });
        if (!uuid(issued.operation_id) || !Number.isFinite(Date.parse(issued.expires_at))) throw Error();
        operation = { path: saved ? '/drafts/' + saved.id : '/drafts', body: { operation_id: issued.operation_id, expected_revision: saved?.revision ?? 0, draft: structuredClone(content) } };
        if (!alive.current) return;
        setPending(operation);
      }
      await send(operation);
    } catch (error) { if (alive.current) failed(error); }
    finally { if (alive.current) setBusy(false); }
  }
  async function settle() {
    if (!pending) return;
    setBusy(true);
    try {
      const result = await request('/draft-operations/' + pending.body.operation_id);
      if (result.state === 'accepted') await acknowledge(result.result, pending);
      else if (result.state === 'pending' && result.result === null) setMessage('Forsøket er ikke lagret. Prøv samme lagringsforsøk igjen.');
      else throw Error();
    } catch (error) { if (alive.current) failed(error); }
    finally { if (alive.current) setBusy(false); }
  }
  function edit(next: Content) { setContent(next); setMessage('Ulagrede endringer.'); }
  return <section aria-label="Private utkast" hidden={suspended}>
    <h2>Mine utkast</h2>
    <p>Utkast slettes sju dager etter opprettelse. Ulagrede endringer finnes bare mens denne siden er åpen.</p>
    <div className="controls"><button disabled={busy} onClick={() => { if (!dirty || window.confirm('Ulagrede endringer går tapt. Opprette nytt utkast?')) { setSaved(null); setContent(empty()); setPending(null); setComparison(null); setMessage('Nytt utkast. Ikke lagret.'); title.current?.focus(); } }}>Nytt utkast</button><button disabled={busy} onClick={() => void refresh()}>Oppdater listen</button></div>
    {list.length === 0 ? <p>Ingen lagrede utkast.</p> : <ul>{list.map(item => <li key={item.id}><button disabled={busy} onClick={() => void reopen(item.id)}>Åpne {item.service_date ?? 'ukjent tjenestedato'} · versjon {item.revision}</button> <span>Utløper {new Date(item.expires_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' })}</span></li>)}</ul>}
    <h2 ref={title} tabIndex={-1}>{saved ? 'Rediger utkast' : 'Nytt manuelt utkast'}</h2>
    <p role="status" aria-live="polite" className="status">{message}</p>
    {saved && <p>Utløper {new Date(saved.expires_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' })}. Fristen forlenges ikke.</p>}
    <form className="draft-form" onSubmit={event => { event.preventDefault(); void save(); }}>
      <fieldset disabled={busy || !!pending || suspended || draftExpired}><legend>Dagens opplysninger</legend>
        <label>Tjenestedato<input type="date" value={content.service_date ?? ''} onChange={e => edit({ ...content, service_date: e.target.value || null })} /></label>
        <label>Vognløp<input maxLength={100} value={content.vehicle_duty ?? ''} onChange={e => edit({ ...content, vehicle_duty: e.target.value || null })} /></label>
        <label>Sanntidsverdi (tre sifre)<input maxLength={3} pattern="[0-9]{3}" value={content.realtime_duty ?? ''} onChange={e => edit({ ...content, realtime_duty: e.target.value || null })} /></label>
        <p>Fysisk buss: ukjent.</p>
        <p>Tidspunkt: YYYY-MM-DDTHH:mm+01:00 (vinter) eller +02:00 (sommer). Behold opprinnelig klokke, for eksempel 25:10, i kildefeltet. Tomme felt betyr ukjent.</p>
        {content.activities.map((activity, index) => <fieldset key={activity.id}><legend>Aktivitet {index + 1}</legend><div className="draft-grid">{fields.map(([key, label]) => <label key={key}>{label}<input maxLength={['uncertainty', 'provenance'].includes(key) ? 1000 : ['from_place', 'to_place'].includes(key) ? 300 : key === 'start' || key === 'end' ? 40 : 100} value={activity[key] ?? ''} onChange={e => edit({ ...content, activities: content.activities.map(a => a.id === activity.id ? { ...a, [key]: e.target.value || null } : a) })} /></label>)}</div>
          <div className="controls"><button type="button" disabled={index === 0} onClick={() => { const rows = [...content.activities]; [rows[index - 1], rows[index]] = [rows[index], rows[index - 1]]; edit({ ...content, activities: rows }); }}>Flytt opp</button><button type="button" onClick={() => edit({ ...content, activities: content.activities.filter(a => a.id !== activity.id) })}>Fjern aktivitet {index + 1}</button></div>
        </fieldset>)}
        <button type="button" disabled={content.activities.length >= 200} onClick={() => edit({ ...content, activities: [...content.activities, { id: crypto.randomUUID(), ...Object.fromEntries(fields.map(([key]) => [key, null])) }] })}>Legg til aktivitet</button>
      </fieldset>
      <button disabled={busy || suspended || !!comparison || draftExpired} type="submit">{pending ? 'Prøv samme lagringsforsøk igjen' : 'Lagre utkast'}</button>
    </form>
    {pending && <button disabled={busy} onClick={() => void settle()}>Kontroller lagringsforsøket</button>}
    {comparison && <section aria-label="Sammenlign versjoner"><h3>Lagret versjon {comparison.revision}</h3><p>Lokale endringer står i skjemaet. Last inn lagret versjon for å forkaste dem.</p><dl><dt>Tjenestedato</dt><dd>{comparison.draft.service_date ?? 'Ukjent'}</dd><dt>Vognløp</dt><dd>{comparison.draft.vehicle_duty ?? 'Ukjent'}</dd><dt>Sanntidsverdi</dt><dd>{comparison.draft.realtime_duty ?? 'Ukjent'}</dd></dl><ol>{comparison.draft.activities.map(activity => <li key={activity.id}><dl>{fields.map(([key, label]) => <div className="fact" key={key}><dt>{label}</dt><dd>{activity[key] ?? 'Ukjent'}</dd></div>)}</dl></li>)}</ol><button onClick={() => { if (window.confirm('Forkaste lokale endringer og laste lagret versjon?')) adopt(comparison); }}>Last inn lagret versjon</button></section>}
  </section>;
}
