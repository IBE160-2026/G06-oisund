import { useEffect, useRef, useState } from 'react';
import { PrivateTimeInput } from './PrivateTimeInput';
import { PrivateImport, SourceFacts, validMetadata, type ImportMetadata } from './PrivateImport';
import { dutyChanges, effectiveDuty, dutySuffix, importIssues, originalActivity, sameFact, currentUnknowns, type DutyChange } from './draftInterpretation';

type Activity = { id: string } & Record<string, string | null>;
export type Content = { service_date: string | null; vehicle_duty: string | null; realtime_duty: string | null; physical_bus: string | null; activities: Activity[]; import_metadata?: ImportMetadata; vehicle_duty_changes?: DutyChange[] };
type Saved = { id: string; created_at: string; expires_at: string; revision: number; draft: Content };
type Summary = Pick<Saved, 'id' | 'expires_at' | 'revision'> & { service_date: string | null };
type Pending = { path: string; body: { operation_id: string; expected_revision: number; draft: Content } };
type PendingDelete = { id: string; body: { operation_id: string; expected_revision: number } };
type Props = { upload: (file: File, signal: AbortSignal) => Promise<any>; request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>; dirtyChanged: (dirty: boolean) => void; expired: () => void; suspended: boolean };
const empty = (): Content => ({ service_date: null, vehicle_duty: null, realtime_duty: null, physical_bus: null, activities: [] });
const realtime = (duty: string | null) => duty?.match(/([0-9]{3})$/)?.[1] ?? null;
const fields = [['type', 'Aktivitetstype'], ['raw_code', 'Opprinnelig kode'], ['start', 'Start med dato og Oslo-offset'], ['end', 'Slutt med dato og Oslo-offset'], ['source_start', 'Opprinnelig startklokke'], ['source_end', 'Opprinnelig sluttklokke'], ['from_place', 'Fra sted'], ['to_place', 'Til sted'], ['trip', 'Turnummer'], ['line', 'Linje'], ['direction', 'Retning'], ['uncertainty', 'Usikkerhet / ukjente fakta'], ['provenance', 'Kilde / manuell rettelse']] as const;
const textLimit = (key: string) => ['uncertainty', 'provenance'].includes(key) ? 1000 : ['from_place', 'to_place'].includes(key) ? 300 : key === 'start' || key === 'end' ? 40 : 100;
const boundedText = (value: string, max: number) => Array.from(value).slice(0, max).join('');
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
export function validContent(draft: any) {
  const nullable = (v: any, max: number) => v === null || (typeof v === 'string' && Array.from(v).length <= max);
  return draft && Object.keys(draft).filter(key => !['import_metadata', 'vehicle_duty_changes'].includes(key)).sort().join() === 'activities,physical_bus,realtime_duty,service_date,vehicle_duty'
    && (draft.import_metadata === undefined || validMetadata(draft.import_metadata))
    && (draft.service_date === null || calendar(draft.service_date)) && nullable(draft.vehicle_duty, 100)
    && draft.realtime_duty === realtime(draft.vehicle_duty) && nullable(draft.physical_bus, 100)
    && Array.isArray(draft.activities) && draft.activities.length <= 200
    && new Set(draft.activities.map((a: any) => a?.id)).size === draft.activities.length
    && draft.activities.every((a: any) => a && uuid(a.id) && Object.keys(a).length === fields.length + 1
      && fields.every(([key]) => nullable(a[key], textLimit(key)))
      && instant(a.start) && instant(a.end) && (!a.start || !a.end || Date.parse(a.end) >= Date.parse(a.start)))
    && (draft.vehicle_duty_changes === undefined || (Array.isArray(draft.vehicle_duty_changes) && draft.vehicle_duty_changes.length <= 200
      && new Set(draft.vehicle_duty_changes.map((change: any) => change?.from_activity_id)).size === draft.vehicle_duty_changes.length
      && draft.vehicle_duty_changes.every((change: any) => change && Object.keys(change).sort().join() === 'from_activity_id,realtime_duty,vehicle_duty'
        && draft.activities.some((activity: Activity) => activity.id === change.from_activity_id) && nullable(change.vehicle_duty, 100) && change.realtime_duty === dutySuffix(change.vehicle_duty))));
}
function valid(value: any): value is Saved {
  return value && uuid(value.id) && Number.isInteger(value.revision) && value.revision > 0
    && Number.isFinite(Date.parse(value.created_at)) && Date.parse(value.expires_at) - Date.parse(value.created_at) === 7 * 86400000
    && Date.parse(value.expires_at) > Date.now() && validContent(value.draft);
}
function validSummary(value: any): value is Summary {
  return value && uuid(value.id) && Number.isInteger(value.revision) && value.revision > 0 && value.revision <= 2147483647
    && (value.service_date === null || calendar(value.service_date))
    && typeof value.created_at === 'string' && value.created_at.length <= 40 && Number.isFinite(Date.parse(value.created_at))
    && typeof value.expires_at === 'string' && value.expires_at.length <= 40 && Date.parse(value.expires_at) > Date.now()
    && Date.parse(value.expires_at) - Date.parse(value.created_at) === 7 * 86400000;
}

function ActivityComparison({ content, activity, index, unresolved }: { content: Content; activity: Activity; index: number; unresolved: { start: boolean; end: boolean } }) {
  const original = originalActivity(content, activity.id);
  const pending = (field: string) => field === 'start' ? unresolved.start : field === 'end' ? unresolved.end : false;
  const unknowns = currentUnknowns(activity).filter(label => !(label === 'start' && unresolved.start) && !(label === 'slutt' && unresolved.end));
  const compared = fields.filter(([key]) => original && key in original);
  const changed = compared.some(([key]) => !pending(key) && !sameFact(key, activity[key], original![key]));
  return <>
    <p className="activity-origin">{original ? 'Fra PDF · opprinnelig tolkning bevart' : 'Manuell aktivitet · ingen opprinnelig tolkning'}</p>
    {(unresolved.start || unresolved.end) && <p className="pending-time">Inntastet {unresolved.start && unresolved.end ? 'start og slutt' : unresolved.start ? 'start' : 'slutt'} er uavklart. Kontroller dato og klokkeslett. Inndata er beholdt.</p>}
    {unknowns.length > 0 && <p className="current-unknown">Gjeldende ukjente fakta: {unknowns.join(', ')}. Tomme steder betyr ukjent. Utkastet er ikke bekreftet.</p>}
    {changed && <p className="correction-marker">Manuelt rettet fra opprinnelig tolkning. Åpne sammenligningen for feltverdier.</p>}
    {original && <details className="activity-comparison"><summary>Opprinnelig og gjeldende · aktivitet {index + 1}</summary><dl>{compared.map(([key, label]) => <div className="comparison-fact" key={key}><dt>{label}{!pending(key) && !sameFact(key, activity[key], original[key]) && <span className="correction-marker"> · Manuelt rettet</span>}</dt><dd>Opprinnelig: {original[key] ?? 'Ukjent'}</dd><dd>Gjeldende: {pending(key) ? 'Inntastet tidspunkt er uavklart; inndata er beholdt.' : activity[key] ?? 'Ukjent'}</dd></div>)}</dl><p>Retning, usikkerhetsnotat og kilde / manuell rettelse har ikke eget sammenligningsgrunnlag. Notater kan komme fra importen eller være manuelt skrevet.</p></details>}
  </>;
}

export function PrivateDrafts({ upload, request, mutation, dirtyChanged, expired, suspended }: Props) {
  const [night, setNight] = useState(false);
  const [list, setList] = useState<Summary[]>([]);
  const [listState, setListState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [saved, setSaved] = useState<Saved | null>(null);
  const [content, setContent] = useState<Content>(empty);
  const [pending, setPending] = useState<Pending | null>(null);
  const [saveUnavailable, setSaveUnavailable] = useState(false);
  const [pendingDelete, setPendingDelete] = useState<PendingDelete | null>(null);
  const [comparison, setComparison] = useState<Saved | null>(null);
  const [message, setMessage] = useState('Nytt utkast. Ikke lagret.');
  const [busy, setBusy] = useState(false);
  const [draftExpired, setDraftExpired] = useState(false);
  const [timeEpoch, setTimeEpoch] = useState(0);
  const [timeStates, setTimeStates] = useState<Record<string, { dirty: boolean; unresolved: boolean }>>({});
  const timeStatesRef = useRef(timeStates);
  const alive = useRef(true);
  const deletionEpoch = useRef(0);
  const listRequest = useRef(0);
  const title = useRef<HTMLHeadingElement>(null);
  const changes = dutyChanges(content);
  const issues = importIssues(content);
  const dirty = canonical(content) !== canonical(saved?.draft ?? empty()) || !!pending || !!pendingDelete || saveUnavailable || Object.values(timeStates).some(value => value.dirty);
  const unresolvedTimes = Object.values(timeStates).some(value => value.unresolved);
  const entryLocked = busy || !!pending || !!pendingDelete || saveUnavailable || suspended || draftExpired;
  function resetTimes() { timeStatesRef.current = {}; setTimeStates({}); setTimeEpoch(value => value + 1); }
  function timeState(id: string, field: string, dirty: boolean, unresolved: boolean) {
    const current = timeStatesRef.current, key = id + ':' + field;
    if (current[key]?.dirty === dirty && current[key]?.unresolved === unresolved) return;
    timeStatesRef.current = { ...current, [key]: { dirty, unresolved } }; setTimeStates(timeStatesRef.current);
  }
  function removeTimeStates(id: string) { timeStatesRef.current = Object.fromEntries(Object.entries(timeStatesRef.current).filter(([key]) => !key.startsWith(id + ':'))); setTimeStates(timeStatesRef.current); }
  function changeTime(id: string, field: string, value: string | null) {
    setContent(current => ({ ...current, activities: current.activities.map(activity => activity.id === id ? { ...activity, [field]: value } : activity) }));
    setMessage('Ulagrede endringer.');
  }
  function failed(error: any) {
    if (error?.status === 401) { expired(); return; }
    setMessage(error?.status === 410 ? 'Utkastet eller lagringsforsøket er utløpt. Lokale endringer er ikke lagret.' : error?.status === 404 ? 'Tilgangen ble avvist.' : 'Tjenesten er utilgjengelig. Lokale endringer er ikke lagret.');
  }
  async function refresh() {
    const epoch = deletionEpoch.current;
    const sequence = ++listRequest.current;
    setListState('loading');
    try {
      const result = await request('/drafts');
      if (!alive.current || epoch !== deletionEpoch.current || sequence !== listRequest.current) return;
      if (!result || !Array.isArray(result.drafts) || result.drafts.length > 200 || !result.drafts.every(validSummary)
        || new Set(result.drafts.map((item: Summary) => item.id)).size !== result.drafts.length) {
        setListState('error'); setMessage('Listen kunne ikke lastes. Prøv Oppdater listen igjen. Skjemaet er beholdt.'); return;
      }
      setList(result.drafts.map(({ id, revision, expires_at, service_date }: Summary) => ({ id, revision, expires_at, service_date })));
      setListState('ready');
      setMessage(current => current.startsWith('Listen kunne ikke lastes.') ? 'Listen er oppdatert.' : current);
    } catch (error) { if (alive.current && epoch === deletionEpoch.current && sequence === listRequest.current) { setListState('error'); failed(error); } }
  }
  useEffect(() => { alive.current = true; void refresh(); return () => { alive.current = false; }; }, []);
  useEffect(() => { dirtyChanged(dirty); return () => dirtyChanged(false); }, [dirty]);
  useEffect(() => {
    setDraftExpired(false);
    if (!saved) return;
    const expire = () => { setDraftExpired(true); if (saved.draft.import_metadata) { resetTimes(); setContent(empty()); setSaved(null); setPending(null); setComparison(null); } setMessage('Utkastet er utløpt. Lokale endringer er ikke lagret.'); };
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
  function adopt(value: Saved) { resetTimes(); setSaveUnavailable(false); setSaved(value); setContent(value.draft); setPending(null); setComparison(null); setMessage(`Lagret. Versjon ${value.revision}.`); title.current?.focus(); }
  function terminalSave(status: number) {
    setPending(null); setSaveUnavailable(true);
    setMessage(`Lagring er ikke bekreftet. ${status === 410 ? 'Lagringsforsøket er utløpt.' : 'Lagringsforsøket finnes ikke lenger eller er utilgjengelig.'} Lokale inndata er beholdt for gjennomgang og kan ikke sendes på nytt. Velg Nytt utkast eller Tilbakestill for å starte med et tomt skjema.`);
  }
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
        setPending(null);
        setMessage('Konflikt. Dine lokale endringer er beholdt. Sammenlign med lagret versjon.');
        if (saved) { try { const value = await request('/drafts/' + saved.id); if (alive.current && valid(value)) setComparison(value); } catch (e) { failed(e); } }
      } else if ([404, 410].includes(error?.status)) {
        terminalSave(error.status);
      } else if ([413, 422].includes(error?.status)) {
        setPending(null);
        if (error.status === 413) setMessage('Utkastet er for stort. Forkort tekst eller fjern aktiviteter før du lagrer igjen. Ingen endringer er lagret.');
        else if (error.status === 422) setMessage('Kontroller feltene og aktivitetenes datoer og klokkeslett. Velg riktig kalenderdag eller neste dag ved nattarbeid. Ingen endringer er lagret.');
        else failed(error);
      } else setMessage('Lagring er uavklart. Behold siden åpen. Kontroller eller prøv samme lagringsforsøk igjen.');
    }
  }
  async function save() {
    if (saveUnavailable) return;
    if (Object.values(timeStatesRef.current).some(value => value.unresolved)) { setMessage('Kontroller uavklarte datoer og klokkeslett før lagring. Inndata er beholdt.'); return; }
    const invalidInterval = content.activities.findIndex(activity => activity.start && activity.end && Date.parse(activity.end) < Date.parse(activity.start));
    if (invalidInterval >= 0) { setMessage(`Aktivitet ${invalidInterval + 1}: Slutt er før start. Kontroller dato og klokkeslett, og bruk «Slutt: neste dag» ved nattarbeid. Inndata er beholdt.`); return; }
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
    } catch (error: any) { if (alive.current) { if ([404, 410].includes(error?.status)) terminalSave(error.status); else failed(error); } }
    finally { if (alive.current) setBusy(false); }
  }
  function edit(next: Content) {
    setContent(current => ({ ...next, ...(current.vehicle_duty_changes === undefined && current.activities.map(a => a.id).join() !== next.activities.map(a => a.id).join() ? { vehicle_duty_changes: dutyChanges(current).filter(change => next.activities.some(a => a.id === change.from_activity_id)) } : {}), realtime_duty: realtime(next.vehicle_duty), activities: next.activities.map(activity => {
      const existing = current.activities.find(value => value.id === activity.id);
      return existing ? { ...activity, start: existing.start, end: existing.end } : activity;
    }) }));
    setMessage('Ulagrede endringer.');
  }
  function reset() {
    if (pending || pendingDelete || !window.confirm(saved && !saveUnavailable ? 'Forkaste alle endringer siden siste lagring? Dette gjelder endrede felt, nye og fjernede aktiviteter og endret rekkefølge. Sist lagrede versjon beholdes.' : 'Tømme det ulagrede utkastet?')) return;
    if (saveUnavailable) { setSaveUnavailable(false); setSaved(null); resetTimes(); setContent(empty()); setComparison(null); setMessage('Nytt utkast. Ikke lagret.'); title.current?.focus(); return; }
    resetTimes(); setContent(saved ? structuredClone(saved.draft) : empty()); setComparison(null);
    setMessage(saved ? `Lagret. Versjon ${saved.revision}. Lokale endringer er forkastet.` : 'Nytt utkast. Ikke lagret.'); title.current?.focus();
  }
  function acknowledgeDelete(value: any, operation: PendingDelete) {
    if (!value || value.deleted_id !== operation.id || Object.keys(value).length !== 1) throw Error();
    if (!alive.current) return;
    deletionEpoch.current++;
    resetTimes();
    setList(current => current.filter(item => item.id !== operation.id));
    setListState('ready');
    setSaved(null); setContent(empty()); setPendingDelete(null); setComparison(null);
    setMessage('Utkastet er slettet.'); title.current?.focus();
  }
  async function removeDraft(lookup = false) {
    let operation = pendingDelete;
    if (!operation) {
      if (!saved || pending || !window.confirm('Slette dette lagrede utkastet og lokale endringer? Dette kan ikke angres.')) return;
      operation = { id: saved.id, body: { operation_id: crypto.randomUUID(), expected_revision: saved.revision } };
      setPendingDelete(operation);
    }
    setBusy(true); setMessage(lookup ? 'Kontrollerer sletting …' : 'Sletter …');
    try {
      const result = lookup ? await request('/draft-deletions/' + operation.body.operation_id) : await mutation('/drafts/' + operation.id + '/delete', operation.body);
      acknowledgeDelete(result, operation);
    } catch (error: any) {
      if (!alive.current) return;
      if (error?.status === 401) { expired(); return; }
      if (error?.status === 410) {
        deletionEpoch.current++;
        resetTimes();
        setList(current => current.filter(item => item.id !== operation.id));
        setListState('ready');
        setSaved(null); setContent(empty()); setPendingDelete(null); setComparison(null);
        setMessage('Sletting kunne ikke bekreftes fordi utkastet eller slettingsforsøket er utløpt. Du kan opprette et nytt utkast.'); title.current?.focus();
      } else if (error?.status === 409) {
        setPendingDelete(null); setMessage('Konflikt. Utkastet er endret og er ikke slettet. Dine lokale endringer er beholdt.');
        try { const value = await request('/drafts/' + operation.id); if (alive.current && valid(value)) setComparison(value); } catch (e) { if (alive.current) failed(e); }
      } else {
        const reason = error?.status === 404 ? 'Tilgangen til bekreftelsen ble avvist.' : error?.status === 410 ? 'Utkastet eller slettingsforsøket er utløpt.' : 'Tjenesten kunne ikke bekrefte slettingen.';
        setMessage(`Sletting er ikke bekreftet. ${reason} Utkastet er låst. Kontroller eller prøv samme slettingsforsøk igjen.`);
      }
    } finally { if (alive.current) setBusy(false); }
  }
  function removeActivity(activity: Activity) {
    const populated = Object.entries(activity).some(([key, value]) => key !== 'id' && value !== null && value !== '')
      || Object.entries(timeStatesRef.current).some(([key, state]) => key.startsWith(activity.id + ':') && (state.dirty || state.unresolved));
    if (populated && !window.confirm('Fjerne denne aktiviteten og inndataene? Endringen lagres først når du lagrer utkastet.')) return;
    removeTimeStates(activity.id); edit({ ...content, ...(content.vehicle_duty_changes !== undefined || changes.length ? { vehicle_duty_changes: changes.filter(change => change.from_activity_id !== activity.id) } : {}), activities: content.activities.filter(value => value.id !== activity.id) }); title.current?.focus();
  }
  function setDutyChange(id: string, value: string | null | undefined) {
    const next = changes.filter(change => change.from_activity_id !== id);
    if (value !== undefined) next.push({ from_activity_id: id, vehicle_duty: value, realtime_duty: dutySuffix(value) });
    edit({ ...content, vehicle_duty_changes: next });
  }
  return <section aria-label="Private utkast" className={night ? 'private-drafts night' : 'private-drafts'} hidden={suspended}>
    <button type="button" aria-pressed={night} onClick={() => setNight(value => !value)}>Nattmodus</button>
    <h2>Mine utkast</h2>
    <PrivateImport upload={upload} suspended={suspended} locked={entryLocked || !!comparison} expired={expired} adopt={value => { if (dirty && !window.confirm('Ulagrede endringer går tapt. Bruke importen som et separat nytt utkast?')) return false; resetTimes(); setSaved(null); setContent(value); setComparison(null); setSaveUnavailable(false); setMessage('Importen er et separat, ulagret utkast. Kontroller fakta og lagre uttrykkelig.'); title.current?.focus(); return true; }} />
    <p>Utkast slettes sju dager etter opprettelse. Ulagrede endringer finnes bare mens denne siden er åpen.</p>
    <div className="controls"><button disabled={busy || !!pending || !!pendingDelete} onClick={() => { if (!dirty || window.confirm('Ulagrede endringer går tapt. Opprette nytt utkast?')) { resetTimes(); setSaveUnavailable(false); setSaved(null); setContent(empty()); setPending(null); setComparison(null); setMessage('Nytt utkast. Ikke lagret.'); title.current?.focus(); } }}>Nytt utkast</button><button disabled={busy || !!pendingDelete} onClick={() => void refresh()}>Oppdater listen</button></div>
    {listState === 'loading' && <p>Laster lagrede utkast …</p>}
    {listState === 'error' && <p>Listen er utilgjengelig. Prøv Oppdater listen igjen.</p>}
    {list.length === 0 ? listState === 'ready' && <p>Ingen lagrede utkast.</p> : <ul>{list.map(item => <li key={item.id}><button disabled={busy || !!pending || !!pendingDelete || saveUnavailable} onClick={() => void reopen(item.id)}>Åpne {item.service_date ?? 'ukjent tjenestedato'} · versjon {item.revision}</button> <span>Utløper {new Date(item.expires_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' })}</span></li>)}</ul>}
    <h2 ref={title} tabIndex={-1}>{saved ? 'Rediger utkast' : 'Nytt manuelt utkast'}</h2>
    <p role="status" aria-live="polite" className="status">{message}</p>
    {saved && <p>Utløper {new Date(saved.expires_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' })}. Fristen forlenges ikke.</p>}
    {content.import_metadata && <details key={'source:' + (saved?.id ?? 'new') + ':' + timeEpoch} className="source-disclosure"><summary>Vis kildefakta fra PDF</summary><SourceFacts metadata={content.import_metadata} /></details>}
    {issues.length > 0 && <section className="import-warning" aria-label="Usikkerheter fra importen"><h3>Kontroller usikkerheter fra importen</h3>
      <p>Historiske varsler fra den opprinnelige tolkningen beholdes også etter manuelle rettelser. Se gjeldende ukjente fakta ved hver aktivitet. Du kan lagre et uferdig utkast; det er ikke bekreftet.</p>
      <ul>{issues.map((issue, index) => {
        const activityIndex = content.activities.findIndex(activity => activity.id === issue.activityId);
        return <li key={index}>{issue.text} {activityIndex >= 0 && <button type="button" onClick={() => document.getElementById('activity-' + issue.activityId)?.focus()}>Se aktivitet {activityIndex + 1}</button>}{issue.activityId && activityIndex < 0 && <span> Opprinnelig aktivitet er fjernet fra utkastet.</span>}</li>;
      })}</ul></section>}
    <form className="draft-form" onSubmit={event => { event.preventDefault(); void save(); }}>
      <fieldset disabled={entryLocked}><legend>Dagens opplysninger</legend>
        <label>Tjenestedato<input type="date" value={content.service_date ?? ''} onChange={e => edit({ ...content, service_date: e.target.value || null })} /></label>
        <label>Vognløp<input maxLength={200} value={content.vehicle_duty ?? ''} onChange={e => edit({ ...content, vehicle_duty: boundedText(e.target.value, 100) || null })} /></label>
        <p>Vognløp ved starten av dagen. Bytter kan angis ved aktivitetene nedenfor og gjelder fra den aktiviteten til neste bytte. Et vognløpsbytte endrer ikke Buss/vogn.</p>
        <button type="button" onClick={() => edit({ ...content, vehicle_duty: null })}>Tøm vognløp</button>
        <p>Sanntidsverdi: {content.realtime_duty ?? 'ukjent'} (avledet fra vognløp).</p>
        <label>Buss/vogn<input maxLength={200} value={content.physical_bus ?? ''} onChange={e => edit({ ...content, physical_bus: boundedText(e.target.value, 100) || null })} /></label>
        <p>Alle klokkeslett bruker Oslo-tid. Velg riktig kalenderdag for nattarbeid. Opprinnelige klokker som 25:10 kan beholdes i kildefeltene. Tomme klokkeslett betyr ukjent.</p>
        {!content.service_date && <p className="current-unknown">Gjeldende ukjent opplysning: tjenestedato.</p>}
        {content.activities.length === 0 && <p className="current-unknown">Ingen aktiviteter. Utkastet er uferdig og ikke bekreftet.</p>}
        {content.activities.map((activity, index) => <fieldset key={activity.id} id={'activity-' + activity.id} tabIndex={-1}><legend>Aktivitet {index + 1}</legend>
          <ActivityComparison content={content} activity={activity} index={index} unresolved={{ start: !!timeStates[activity.id + ':start']?.unresolved, end: !!timeStates[activity.id + ':end']?.unresolved }} />
          <p>Gjeldende vognløp: {effectiveDuty(content, index) ?? 'ukjent'} · sanntidsverdi {dutySuffix(effectiveDuty(content, index)) ?? 'ukjent'}.</p>
          {changes.some(change => change.from_activity_id === activity.id) ? <div className="duty-change">
            <label>Vognløp fra aktivitet {index + 1}<input maxLength={200} value={changes.find(change => change.from_activity_id === activity.id)?.vehicle_duty ?? ''} onChange={event => setDutyChange(activity.id, boundedText(event.target.value, 100) || null)} /></label>
            <button type="button" onClick={() => setDutyChange(activity.id, undefined)}>Fjern vognløpsbytte fra aktivitet {index + 1}</button>
          </div> : <button type="button" onClick={() => setDutyChange(activity.id, effectiveDuty(content, index))}>Bytt vognløp fra aktivitet {index + 1}</button>}
          <div className="draft-grid">{(['start', 'end'] as const).map(field => <PrivateTimeInput key={timeEpoch + ':' + field} label={field === 'start' ? 'Start' : 'Slutt'} value={activity[field]} defaultDate={content.service_date} disabled={entryLocked} resolve={body => mutation('/draft-times/resolve', body)} onValue={value => changeTime(activity.id, field, value)} onState={(dirty, unresolved) => timeState(activity.id, field, dirty, unresolved)} expired={expired} />)}</div>
          <div className="draft-grid">{fields.filter(([key]) => key !== 'start' && key !== 'end').map(([key, label]) => <label key={key} className={key === 'uncertainty' && issues.some(issue => issue.activityId === activity.id) ? 'import-warning' : undefined}>{label}<input aria-label={label} aria-describedby={key === 'uncertainty' && issues.some(issue => issue.activityId === activity.id) ? 'uncertainty-source-' + activity.id : undefined} maxLength={2 * textLimit(key)} value={activity[key] ?? ''} onChange={e => edit({ ...content, activities: content.activities.map(a => a.id === activity.id ? { ...a, [key]: boundedText(e.target.value, textLimit(key)) || null } : a) })} />{key === 'uncertainty' && issues.some(issue => issue.activityId === activity.id) && <small id={'uncertainty-source-' + activity.id}>Fra importen: {issues.filter(issue => issue.activityId === activity.id).map(issue => issue.text).join(' ')}</small>}</label>)}</div>
          <div className="controls"><button type="button" disabled={index === 0} onClick={() => { const rows = [...content.activities]; [rows[index - 1], rows[index]] = [rows[index], rows[index - 1]]; edit({ ...content, activities: rows }); }}>Flytt opp</button><button type="button" onClick={() => removeActivity(activity)}>Fjern aktivitet {index + 1}</button></div>
        </fieldset>)}
        <button type="button" disabled={content.activities.length >= 200} onClick={() => edit({ ...content, activities: [...content.activities, { id: crypto.randomUUID(), ...Object.fromEntries(fields.map(([key]) => [key, null])) }] })}>Legg til aktivitet</button>
      </fieldset>
      {unresolvedTimes && <p>Kontroller uavklarte datoer og klokkeslett før lagring. Inndata er beholdt.</p>}
      <button disabled={busy || suspended || !!comparison || !!pendingDelete || saveUnavailable || draftExpired || unresolvedTimes} type="submit">{pending ? 'Prøv samme lagringsforsøk igjen' : 'Lagre utkast'}</button>
    </form>
    <div className="controls"><button disabled={busy || !!pending || !!pendingDelete || suspended} onClick={reset}>{saved && !saveUnavailable ? 'Forkast endringer' : 'Tilbakestill utkast'}</button>{saved && <button disabled={busy || !!pending || !!pendingDelete || saveUnavailable || suspended || draftExpired || !!comparison} onClick={() => void removeDraft()}>Slett utkast</button>}</div>
    {pendingDelete && <div className="controls"><button disabled={busy} onClick={() => void removeDraft()}>Prøv samme slettingsforsøk igjen</button><button disabled={busy} onClick={() => void removeDraft(true)}>Kontroller slettingen</button></div>}
    {pending && <button disabled={busy} onClick={() => void settle()}>Kontroller lagringsforsøket</button>}
    {comparison && <section aria-label="Sammenlign versjoner"><h3>Lagret versjon {comparison.revision}</h3><p>Lokale endringer står i skjemaet. Last inn lagret versjon for å forkaste dem.</p><dl><dt>Tjenestedato</dt><dd>{comparison.draft.service_date ?? 'Ukjent'}</dd><dt>Vognløp</dt><dd>{comparison.draft.vehicle_duty ?? 'Ukjent'}</dd><dt>Sanntidsverdi</dt><dd>{comparison.draft.realtime_duty ?? 'Ukjent'}</dd><dt>Buss/vogn</dt><dd>{comparison.draft.physical_bus ?? 'Ukjent'}</dd></dl><ol>{comparison.draft.activities.map((activity, index) => <li key={activity.id}><dl><dt>Gjeldende vognløp</dt><dd>{effectiveDuty(comparison.draft, index) ?? 'Ukjent'} · sanntidsverdi {dutySuffix(effectiveDuty(comparison.draft, index)) ?? 'Ukjent'}</dd>{fields.map(([key, label]) => <div className="fact" key={key}><dt>{label}</dt><dd>{activity[key] ?? 'Ukjent'}</dd></div>)}</dl></li>)}</ol><button onClick={() => { if (window.confirm('Forkaste lokale endringer og laste lagret versjon?')) adopt(comparison); }}>Last inn lagret versjon</button></section>}
  </section>;
}
