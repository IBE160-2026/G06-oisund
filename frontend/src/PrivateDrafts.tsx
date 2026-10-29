import { privateNow } from './privateClock';
import { useEffect, useRef, useState } from 'react';
import { recoverOperation } from './recoverOperation';
import { PrivateTimeInput } from './PrivateTimeInput';
import { PrivateConfirmation } from './PrivateConfirmation';
import { PrivateImport, SourceFacts, validMetadata, type ImportMetadata } from './PrivateImport';
import { dutyChanges, effectiveDuty, dutySuffix, importIssues, originalActivity, sameFact, currentUnknowns, currentUncertainty, displayFact, sourceMarkers, type DutyChange } from './draftInterpretation';
import { normalizeBus, busError } from './busValue';

type Activity = { id: string } & Record<string, string | null>;
export type Content = { service_date: string | null; vehicle_duty: string | null; realtime_duty: string | null; physical_bus: string | null; activities: Activity[]; import_metadata?: ImportMetadata; vehicle_duty_changes?: DutyChange[] };
export type Saved = { id: string; created_at: string; expires_at: string; revision: number; draft: Content };
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
    && Date.parse(value.expires_at) > privateNow() && validContent(value.draft);
}
function validSummary(value: any): value is Summary {
  return value && uuid(value.id) && Number.isInteger(value.revision) && value.revision > 0 && value.revision <= 2147483647
    && (value.service_date === null || calendar(value.service_date))
    && typeof value.created_at === 'string' && value.created_at.length <= 40 && Number.isFinite(Date.parse(value.created_at))
    && typeof value.expires_at === 'string' && value.expires_at.length <= 40 && Date.parse(value.expires_at) > privateNow()
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
    {original && <details className="activity-comparison"><summary>Opprinnelig og gjeldende · aktivitet {index + 1}</summary><dl>{compared.map(([key, label]) => <div className="comparison-fact" key={key}><dt>{label}{!pending(key) && !sameFact(key, activity[key], original[key]) && <span className="correction-marker"> · Manuelt rettet</span>}</dt><dd>Opprinnelig: {displayFact(key, original[key]) ?? 'Ukjent'}</dd><dd>Gjeldende: {pending(key) ? 'Inntastet tidspunkt er uavklart; inndata er beholdt.' : displayFact(key, activity[key]) ?? 'Ukjent'}</dd></div>)}</dl><p>Retning, usikkerhetsnotat og kilde / manuell rettelse har ikke eget sammenligningsgrunnlag. Notater kan komme fra importen eller være manuelt skrevet.</p></details>}
  </>;
}

export function PrivateDrafts({ upload, request, mutation, dirtyChanged, expired, suspended }: Props) {
  const [screen, setScreen] = useState<'upload' | 'import' | 'editor' | 'direct' | 'approval' | 'plan'>('upload');
  const [hasPlan, setHasPlan] = useState(false); const [consulting, setConsulting] = useState(false);
  const preparationTitle = useRef<HTMLHeadingElement>(null);
  useEffect(() => { if (screen === 'upload') preparationTitle.current?.focus(); if (screen === 'editor') title.current?.focus(); }, [screen]);
  const [registryOpen, setRegistryOpen] = useState(false), [registryNavigation, setRegistryNavigation] = useState(0);
  const [registryDirty, setRegistryDirty] = useState(false);
  const [confirmationLocked, setConfirmationLocked] = useState(false);
  const [list, setList] = useState<Summary[]>([]);
  const [listState, setListState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [nextCursor, setNextCursor] = useState<string | null>(null);
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
  const continueAfterSave = useRef(false);
  const directTitle = useRef<HTMLHeadingElement>(null);
  const [sourceEpoch, setSourceEpoch] = useState(0);
  useEffect(() => { if (screen === 'direct') directTitle.current?.focus(); }, [screen]);
  function showApproval() { setRegistryNavigation(value => value + 1); setScreen('approval'); }
  const loadedCount = useRef<HTMLParagraphElement>(null);
  const focusLoadedCount = useRef(false);
  const changes = dutyChanges(content);
  const issues = importIssues(content);
  const dirty = canonical(content) !== canonical(saved?.draft ?? empty()) || !!pending || !!pendingDelete || saveUnavailable || Object.values(timeStates).some(value => value.dirty);
  const unresolvedTimes = Object.values(timeStates).some(value => value.unresolved);
  const busOtherChanges = !saved || canonical({ ...content, physical_bus: saved.draft.physical_bus }) !== canonical(saved.draft) || Object.values(timeStates).some(value => value.dirty || value.unresolved);
  const busMessage = !saved ? 'Utkastet er ikke lagret. Buss kan ikke lagres separat nå. Bruk Lagre hele utkastet med buss for å lagre alle opplysningene uttrykkelig.' : busOtherChanges ? 'Andre opplysninger er også ulagret. Buss kan ikke lagres separat nå. Bruk Lagre hele utkastet med buss for å lagre alle endringene uttrykkelig.' : 'Bare bussendringen lagres som ny utkastversjon. Andre opplysninger er allerede lagret.';
  const entryLocked = busy || !!pending || !!pendingDelete || saveUnavailable || suspended || draftExpired;
  function resetTimes() { timeStatesRef.current = {}; setTimeStates({}); setTimeEpoch(value => value + 1); }
  function timeState(id: string, field: string, dirty: boolean, unresolved: boolean) {
    const current = timeStatesRef.current, key = id + ':' + field;
    if (current[key]?.dirty === dirty && current[key]?.unresolved === unresolved) return;
    timeStatesRef.current = { ...current, [key]: { dirty, unresolved } }; setTimeStates(timeStatesRef.current);
  }
  function removeTimeStates(id: string) { timeStatesRef.current = Object.fromEntries(Object.entries(timeStatesRef.current).filter(([key]) => !key.startsWith(id + ':'))); setTimeStates(timeStatesRef.current); }
  function changeTime(id: string, field: string, value: string | null) {
    continueAfterSave.current = false;
    setContent(current => ({ ...current, activities: current.activities.map(activity => activity.id === id ? { ...activity, [field]: value } : activity) }));
    setMessage('Ulagrede endringer.');
  }
  function failed(error: any) {
    if (error?.status === 401) { expired(); return; }
    setMessage(pending ? 'Lagring er uavklart. Tjenesten kunne ikke bekrefte utfallet. Det opprinnelige forsøket og inndata er beholdt.' : error?.status === 410 ? 'Utkastet eller lagringsforsøket er utløpt. Inndata er beholdt.' : error?.status === 404 ? 'Tilgangen ble avvist.' : 'Tjenesten er utilgjengelig. Inndata er beholdt.');
  }
  async function refresh(cursor: string | null = null) {
    const epoch = deletionEpoch.current;
    const sequence = ++listRequest.current;
    setListState('loading');
    try {
      const result = await request('/drafts' + (cursor ? '?cursor=' + cursor : ''));
      if (!alive.current || epoch !== deletionEpoch.current || sequence !== listRequest.current) return;
      if (!result || Object.keys(result).sort().join() !== 'drafts,next_cursor' || !Array.isArray(result.drafts) || result.drafts.length > 50 || !result.drafts.every(validSummary)
        || new Set(result.drafts.map((item: Summary) => item.id)).size !== result.drafts.length
        || result.drafts.some((item: Summary, index: number) => (index > 0 && item.id <= result.drafts[index - 1].id) || (cursor && item.id <= cursor))
        || (result.next_cursor !== null && (!uuid(result.next_cursor) || cursor && result.next_cursor <= cursor || result.drafts.some((item: Summary) => item.id > result.next_cursor)))) {
        setListState('error'); return;
      }
      const rows = result.drafts.map(({ id, revision, expires_at, service_date }: Summary) => ({ id, revision, expires_at, service_date }));
      focusLoadedCount.current = !!cursor && result.next_cursor === null;
      setList(current => cursor ? [...current, ...rows.filter((row: Summary) => !current.some(item => item.id === row.id))] : rows);
      setNextCursor(result.next_cursor);
      setListState('ready');
    } catch (error: any) { if (alive.current && epoch === deletionEpoch.current && sequence === listRequest.current) { setListState('error'); if (error?.status === 401) expired(); } }
  }
  useEffect(() => { alive.current = true; void refresh(); return () => { alive.current = false; }; }, []);
  useEffect(() => { if (focusLoadedCount.current) { focusLoadedCount.current = false; loadedCount.current?.focus(); } }, [list]);
  useEffect(() => { dirtyChanged(dirty || confirmationLocked || registryDirty); return () => dirtyChanged(false); }, [dirty, confirmationLocked, registryDirty]);
  useEffect(() => {
    const timer = window.setInterval(() => setList(current => current.some(row => Date.parse(row.expires_at) <= privateNow()) ? current.filter(row => Date.parse(row.expires_at) > privateNow()) : current), 1000);
    return () => clearInterval(timer);
  }, []);
  useEffect(() => {
    setDraftExpired(false);
    if (!saved) return;
    const expire = () => { setDraftExpired(true); deletionEpoch.current++; listRequest.current++; resetTimes(); setContent(empty()); setSaved(null); setPending(null); setPendingDelete(null); setComparison(null); setSaveUnavailable(false); setList(current => current.filter(row => row.id !== saved.id)); setMessage('Utkastet er utløpt. Lagringsutfallet kan ikke bekreftes, og utkastet kan ikke åpnes igjen.'); };
    let timer: number;
    const checkDeadline = () => {
      const remaining = Date.parse(saved.expires_at) - privateNow();
      if (remaining <= 0) { expire(); return; }
      // Recheck the original deadline as the shared server clock advances.
      timer = window.setTimeout(checkDeadline, Math.min(remaining, 1000));
    };
    checkDeadline();
    return () => clearTimeout(timer);
  }, [saved]);
  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => { if (dirty || confirmationLocked || registryDirty) { event.preventDefault(); event.returnValue = ''; } };
    const navigate = (event: MouseEvent) => { if ((dirty || confirmationLocked || registryDirty) && (event.target as Element)?.closest('a') && !window.confirm('Ulagrede endringer eller uavklart busslagring/bekreftelse/sletting går tapt. Vil du fortsette?')) event.preventDefault(); };
    window.addEventListener('beforeunload', warn); document.addEventListener('click', navigate);
    return () => { window.removeEventListener('beforeunload', warn); document.removeEventListener('click', navigate); };
  }, [dirty, confirmationLocked, registryDirty]);
  function adopt(value: Saved, reopening = true) { resetTimes(); if (reopening) { setSourceEpoch(value => value + 1); setScreen('editor'); } setSaveUnavailable(false); setSaved(value); setContent(value.draft); setPending(null); setComparison(null); setMessage(`Lagret. Versjon ${value.revision}.`); if (reopening) title.current?.focus(); else if (continueAfterSave.current) { continueAfterSave.current = false; showApproval(); } }
  function terminalSave(status: number, targetId = saved?.id ?? null) {
    if (targetId) {
      deletionEpoch.current++; listRequest.current++; resetTimes(); setContent(empty()); setSaved(null); setComparison(null); setPendingDelete(null); setList(current => current.filter(row => row.id !== targetId));
    }
    setPending(null); setSaveUnavailable(true);
    setMessage(`Lagring er ikke bekreftet. ${status === 410 ? 'Lagringsforsøket er utløpt.' : 'Lagringsforsøket finnes ikke lenger eller er utilgjengelig.'} ${targetId ? 'Private felt fra det utløpte utkastet er fjernet.' : 'Lokale inndata er beholdt for gjennomgang og kan ikke sendes på nytt.'} Velg Nytt utkast eller Tilbakestill for å starte med et tomt skjema.`);
  }
  async function reopen(id: string, confirmed = false) {
    if (!confirmed && dirty && !window.confirm('Ulagrede endringer går tapt. Åpne lagret utkast?')) return;
    const epoch = deletionEpoch.current;
    setBusy(true);
    const shown = confirmed ? comparison : null;
    try {
      const value = await request('/drafts/' + id);
      if (epoch !== deletionEpoch.current) return;
      if (!valid(value) || value.id !== id || shown && (value.id !== shown.id || value.created_at !== shown.created_at || value.expires_at !== shown.expires_at
        || value.revision < shown.revision || value.revision === shown.revision && canonical(value) !== canonical(shown))) throw Error();
      if (alive.current) adopt(value);
    }
    catch (error: any) { if (alive.current && epoch === deletionEpoch.current) { if (saved?.id === id && terminalDraftError(error)) terminalSave(error.status); else failed(error); } }
    finally { if (alive.current) setBusy(false); }
  }
  async function acknowledge(value: any, operation: Pending, verified = () => {}, epoch = deletionEpoch.current) {
    if (!valid(value) || value.revision !== operation.body.expected_revision + 1 || canonical(value.draft) !== canonical(operation.body.draft)
      || (operation.path !== '/drafts' && operation.path !== '/drafts/' + value.id)) throw Error('Invalid acknowledgement');
    verified();
    // Historical receipts prove an effect, while this authorized read establishes
    // the current revision available for reopening and confirmation.
    const latest = await request('/drafts/' + value.id);
    if (epoch !== deletionEpoch.current) return;
    if (!valid(latest) || latest.id !== value.id || latest.created_at !== value.created_at || latest.expires_at !== value.expires_at
      || latest.revision < value.revision || latest.revision === value.revision && canonical(latest) !== canonical(value)) throw Error('Invalid current draft');
    if (!alive.current) return;
    if (latest.revision > value.revision) {
      setPending(null); setComparison(latest);
      setMessage('Forsøket ble lagret. En nyere lagret versjon finnes. Ditt opprinnelige forslag er beholdt. Sammenlign før du laster inn lagret versjon.');
    } else adopt(latest, false);
    await refresh();
  }
  async function send(operation: Pending) {
    const epoch = deletionEpoch.current;
    let accepted = false;
    try { await acknowledge(await mutation(operation.path, operation.body), operation, () => { accepted = true; }, epoch); }
    catch (error: any) {
      if (!alive.current || epoch !== deletionEpoch.current) return;
      if (error?.status === 401) { expired(); return; }
      if (!accepted && error?.status === 409 && ['Utkastet er endret. Sammenlign med lagret versjon før du fortsetter.', 'Lagringsforsøket har annet innhold. Behold dine lokale endringer.'].includes(error.apiDetail)) {
        setPending(null);
        setMessage('Konflikt. Dine lokale endringer er beholdt. Sammenlign med lagret versjon.');
        if (saved) { const requestedId = saved.id; try { const value = await request('/drafts/' + requestedId); if (alive.current && epoch === deletionEpoch.current && valid(value) && value.id === requestedId) setComparison(value); } catch (e) { if (alive.current && epoch === deletionEpoch.current) failed(e); } }
      } else if (terminalDraftError(error)) {
        terminalSave(error.status, operation.path === '/drafts' ? null : operation.path.slice('/drafts/'.length));
      } else if (!accepted && (error?.status === 413 && error.apiDetail === 'Forespørselen er for stor.' || error?.status === 422 && error.apiDetail === 'Kontroller feltene.')) {
        setPending(null);
        if (error.status === 413) setMessage('Utkastet er for stort. Forkort tekst eller fjern aktiviteter før du lagrer igjen. Ingen endringer er lagret.');
        else if (error.status === 422) setMessage('Kontroller feltene og aktivitetenes datoer og klokkeslett. Velg riktig kalenderdag eller neste dag ved nattarbeid. Ingen endringer er lagret.');
        else failed(error);
      } else setMessage('Lagring er uavklart. Behold siden åpen. Kontroller eller prøv samme lagringsforsøk igjen.');
    }
  }
  async function save(proposal = content, fresh = false) {
    const epoch = deletionEpoch.current;
    if (saveUnavailable) return;
    if (!pending && busError(proposal.physical_bus)) { setMessage(busError(proposal.physical_bus)!); return; }
    if (Object.values(timeStatesRef.current).some(value => value.unresolved)) { setMessage('Kontroller uavklarte datoer og klokkeslett før lagring. Inndata er beholdt.'); return; }
    const invalidInterval = proposal.activities.findIndex(activity => activity.start && activity.end && Date.parse(activity.end) < Date.parse(activity.start));
    if (invalidInterval >= 0) { setMessage(`Aktivitet ${invalidInterval + 1}: Slutt er før start. Kontroller dato og klokkeslett, og bruk «Slutt: neste dag» ved nattarbeid. Inndata er beholdt.`); return; }
    const returnTo = document.activeElement as HTMLElement | null;
    const position = window.scrollY;
    const timeContainer = returnTo?.closest('[data-draft-time]');
    const timeIdentity = timeContainer?.getAttribute('data-draft-time');
    const controlIndex = timeContainer ? Array.from(timeContainer.querySelectorAll('input,select,button')).indexOf(returnTo!) : -1;
    const restoreEditor = screen === 'editor';
    setBusy(true); setMessage('Lagrer …');
    try {
      let operation = pending;
      if (operation) { await settle(true); return; }
      if (!operation) {
        const candidate = { operation_id: '00000000-0000-4000-8000-000000000000', expected_revision: (fresh ? 0 : saved?.revision) ?? 0, draft: proposal };
        if (new TextEncoder().encode(JSON.stringify(candidate)).byteLength > 1048576) {
          setMessage('Utkastet er for stort. Forkort tekst eller fjern aktiviteter før du lagrer igjen. Ingen endringer er lagret.');
          return;
        }
        const issued = await mutation('/draft-operations', { draft_id: fresh ? null : saved?.id ?? null });
        if (epoch !== deletionEpoch.current) return;
        if (!uuid(issued.operation_id) || !Number.isFinite(Date.parse(issued.expires_at))) throw Error();
        operation = { path: !fresh && saved ? '/drafts/' + saved.id : '/drafts', body: { operation_id: issued.operation_id, expected_revision: (fresh ? 0 : saved?.revision) ?? 0, draft: { ...structuredClone(proposal), physical_bus: normalizeBus(proposal.physical_bus) } } };
        if (!alive.current) return;
        setPending(operation);
      }
      await send(operation);
    } catch (error: any) { if (alive.current && epoch === deletionEpoch.current) { if (terminalDraftError(error)) terminalSave(error.status, fresh ? null : saved?.id ?? null); else failed(error); } }
    finally { if (alive.current) { setBusy(false); if (restoreEditor) requestAnimationFrame(() => {
      const replacementContainer = timeIdentity ? Array.from(document.querySelectorAll('[data-draft-time]')).find(element => element.getAttribute('data-draft-time') === timeIdentity) : null;
      const replacement = replacementContainer?.querySelectorAll<HTMLElement>('input,select,button')[controlIndex] ?? replacementContainer?.querySelector<HTMLInputElement>('input');
      const target = returnTo?.isConnected ? returnTo : replacement;
      if (target?.getClientRects().length) target.focus({ preventScroll: true });
      window.scrollTo({ top: position });
    }); } }
  }
  function terminalDraftError(error: any) {
    return error?.status === 404 && error.apiDetail === 'Tilgangen ble avvist.'
      || error?.status === 410 && ['Lagringsforsøket er utløpt. Det kan ikke gjenopprettes.', 'Lagringsforsøket er utløpt.', 'Utkastet er utløpt.', 'Utkastet er utløpt og kan ikke åpnes igjen.'].includes(error.apiDetail);
  }
  async function settle(retry = false) {
    if (!pending) return;
    const operation = pending;
    const epoch = deletionEpoch.current;
    setBusy(true);
    try {
      const result = await request('/draft-operations/' + operation.body.operation_id);
      if (epoch !== deletionEpoch.current) return;
      if (!result || Object.keys(result).sort().join() !== 'result,state') throw Error();
      if (result.state === 'accepted') await acknowledge(result.result, operation, () => {}, epoch);
      else if (result.state === 'pending' && result.result === null) {
        if (retry) await send(operation);
        else setMessage('Serveren har ikke registrert en lagring for forsøket. Inndata er beholdt. Du kan prøve samme lagringsforsøk igjen.');
      }
      else throw Error();
    } catch (error: any) { if (alive.current && epoch === deletionEpoch.current) { if (error?.status === 401) expired(); else if (terminalDraftError(error)) terminalSave(error.status, operation.path === '/drafts' ? null : operation.path.slice('/drafts/'.length)); else setMessage('Lagring er uavklart. Tjenesten kunne ikke bekrefte utfallet. Det opprinnelige forsøket og inndata er beholdt.'); } }
    finally { if (alive.current) setBusy(false); }
  }
  function edit(next: Content) {
    continueAfterSave.current = false;
    setContent(current => ({ ...next, ...(current.vehicle_duty_changes === undefined && current.activities.map(a => a.id).join() !== next.activities.map(a => a.id).join() ? { vehicle_duty_changes: dutyChanges(current).filter(change => next.activities.some(a => a.id === change.from_activity_id)) } : {}), realtime_duty: realtime(next.vehicle_duty), activities: next.activities.map(activity => {
      const existing = current.activities.find(value => value.id === activity.id);
      return existing ? { ...activity, start: existing.start, end: existing.end } : activity;
    }) }));
    setMessage('Ulagrede endringer.');
  }
  function reset() {
    continueAfterSave.current = false;
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
    const epoch = deletionEpoch.current;
    const retry = !!pendingDelete;
    let operation = pendingDelete;
    if (!operation) {
      if (!saved || pending || !window.confirm('Slette dette lagrede utkastet og lokale endringer? Dette kan ikke angres.')) return;
      operation = { id: saved.id, body: { operation_id: crypto.randomUUID(), expected_revision: saved.revision } };
      setPendingDelete(operation);
    }
    setBusy(true); setMessage(lookup ? 'Kontrollerer sletting …' : 'Sletter …');
    let dispatchRefusal = false;
    try {
      const original = operation;
      const status = () => request('/draft-deletions/' + original.body.operation_id);
      const mutate = async () => {
        try { return await mutation('/drafts/' + original.id + '/delete', original.body); }
        catch (error) { dispatchRefusal = true; throw error; }
      };
      const authorize = async () => { const value = await request('/drafts/' + original.id); if (!valid(value) || value.id !== original.id) throw Error(); };
      const result = lookup ? await status() : retry ? await recoverOperation(status, authorize, mutate) : await mutate();
      if (epoch !== deletionEpoch.current) return;
      acknowledgeDelete(result, operation);
    } catch (error: any) {
      if (!alive.current || epoch !== deletionEpoch.current) return;
      if (error?.status === 401) { expired(); return; }
      if (dispatchRefusal && error?.status === 410 && ['Slettingsforsøket er utløpt.', 'Utkastet er utløpt.', 'Utkastet er utløpt og kan ikke åpnes igjen.'].includes(error.apiDetail)) {
        deletionEpoch.current++;
        resetTimes();
        setList(current => current.filter(item => item.id !== operation.id));
        setListState('ready');
        setSaved(null); setContent(empty()); setPendingDelete(null); setComparison(null);
        setMessage('Sletting kunne ikke bekreftes fordi utkastet eller slettingsforsøket er utløpt. Du kan opprette et nytt utkast.'); title.current?.focus();
      } else if (dispatchRefusal && error?.status === 409 && ['Slettingsforsøket har annet innhold.', 'Utkastet er endret. Sammenlign med lagret versjon før sletting.'].includes(error.apiDetail)) {
        setPendingDelete(null); setMessage('Konflikt. Utkastet er endret og er ikke slettet. Dine lokale endringer er beholdt.');
        try { const value = await request('/drafts/' + operation.id); if (alive.current && epoch === deletionEpoch.current && valid(value) && value.id === operation.id) setComparison(value); } catch (e) { if (alive.current && epoch === deletionEpoch.current) failed(e); }
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
  return <div className={'private-drafts' + (consulting ? ' consulting' : '')} hidden={suspended}><section aria-label="Private utkast">
    <nav className="private-screen-nav" aria-label="Plan og forberedelse"><button disabled={confirmationLocked || !!pending || !!pendingDelete || busy || suspended} aria-current={screen === 'upload' ? 'page' : undefined} onClick={() => { continueAfterSave.current = false; setScreen('upload'); setRegistryNavigation(v => v + 1); }}>Forberedelse og planlister</button><button disabled={confirmationLocked || !!pending || !!pendingDelete || busy || suspended} aria-current={screen === 'editor' ? 'page' : undefined} onClick={() => { continueAfterSave.current = false; setScreen('editor'); setRegistryNavigation(v => v + 1); }}>Kontroller og rediger utkast</button><button hidden={screen === 'plan'} disabled={!saved || dirty || entryLocked || !!comparison || confirmationLocked} aria-current={screen === 'approval' ? 'page' : undefined} onClick={showApproval}>Til godkjenning</button>{hasPlan && <button disabled={confirmationLocked || !!pending || !!pendingDelete || busy || suspended} aria-current={screen === 'plan' ? 'page' : undefined} onClick={() => { setScreen('plan'); setRegistryNavigation(v => v + 1); }}>Til den åpne planen</button>}</nav>
    <div hidden={registryOpen || screen !== 'upload'}><h2 ref={preparationTitle} tabIndex={-1}>Mine utkast</h2></div>
    <p hidden={registryOpen || screen !== 'upload'} role="status" aria-live="polite" className="status">{screen === 'upload' ? message : null}</p><fieldset hidden={registryOpen} className="confirmation-editor" disabled={confirmationLocked}>
    <div hidden={screen !== 'upload' && screen !== 'import'}><PrivateImport stage={screen === 'import' ? 'review' : 'upload'} reviewReady={() => setScreen(current => current === 'upload' ? 'import' : current)} backToUpload={() => setScreen('upload')} upload={upload} suspended={suspended} locked={entryLocked || !!comparison} expired={expired} adopt={(value, intent) => { if (dirty && !window.confirm('Ulagrede endringer går tapt. Bruke importen som et separat nytt utkast?')) return false; resetTimes(); setSourceEpoch(current => current + 1); setSaved(null); setContent(value); setComparison(null); setSaveUnavailable(false); setMessage('Importen er et separat, ulagret utkast. Kontroller fakta og lagre uttrykkelig.'); setScreen(intent === 'approve' ? 'direct' : 'editor'); continueAfterSave.current = intent === 'approve'; if (intent === 'approve') void save(value, true); return true; }} /></div>
    <div hidden={screen !== 'upload'}>
    <p>Utkast slettes sju dager etter opprettelse. Ulagrede endringer finnes bare mens denne siden er åpen.</p>
    <div className="controls"><button disabled={busy || !!pending || !!pendingDelete} onClick={() => { if (!dirty || window.confirm('Ulagrede endringer går tapt. Opprette nytt utkast?')) { resetTimes(); setSaveUnavailable(false); setSaved(null); setContent(empty()); setPending(null); setComparison(null); setMessage('Nytt utkast. Ikke lagret.'); setScreen('editor'); } }}>Nytt utkast</button><button disabled={busy || !!pendingDelete} onClick={() => void refresh()}>Oppdater listen</button></div>
    {listState === 'loading' && <p>Laster lagrede utkast …</p>}
    {listState === 'error' && <p>Listen er utilgjengelig. Prøv Oppdater listen igjen.</p>}
    {list.length === 0 ? listState === 'ready' && <p>Ingen lagrede utkast.</p> : <ul>{list.map(item => <li key={item.id}><button disabled={busy || !!pending || !!pendingDelete || saveUnavailable} onClick={() => void reopen(item.id)}>Åpne {item.service_date ?? 'ukjent tjenestedato'} · versjon {item.revision}</button> <span>Utløper {new Date(item.expires_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' })}</span></li>)}</ul>}
    <p className="draft-loaded-count" ref={loadedCount} tabIndex={-1} aria-live="polite">{listState === 'ready' ? `Lastet ${list.length} utkast.` : listState === 'loading' ? 'Antall utkast avklares …' : 'Antall utkast er utilgjengelig.'}</p>
    {nextCursor && <button disabled={listState === 'loading' || busy || !!pendingDelete} onClick={() => void refresh(nextCursor)}>Vis flere utkast</button>}
    </div>
    <div hidden={screen !== 'direct'}><h2 ref={directTitle} tabIndex={-1}>Lagre import og fortsett</h2><p>{content.service_date ?? 'Ukjent tjenestedato'} · vognløp {content.vehicle_duty ?? 'ukjent'} · {content.activities.length} aktiviteter.</p><p role="status" aria-label="Direkte lagringsstatus">{screen === 'direct' ? message : null}</p>
      {pending && <div className="controls"><button disabled={busy || suspended} onClick={() => void save()}>Prøv samme lagringsforsøk igjen</button><button disabled={busy || suspended} onClick={() => void settle()}>Kontroller lagringsforsøket</button></div>}
      {!busy && !pending && <div className="controls"><button disabled={suspended} onClick={() => { continueAfterSave.current = false; setScreen('editor'); }}>Rett eller legg til opplysninger</button><button disabled={suspended || saveUnavailable || !!comparison || draftExpired} onClick={() => { continueAfterSave.current = true; void save(); }}>Lagre import og prøv igjen</button></div>}
      {comparison && <p>En nyere lagret versjon finnes. Åpne rettelser for å sammenligne. Ditt opprinnelige forslag er beholdt.</p>}
    </div>
    <div hidden={screen !== 'editor'}><h2 ref={title} tabIndex={-1}>{saved ? 'Rediger utkast' : 'Nytt manuelt utkast'}</h2>

    {saved && <p>Utløper {new Date(saved.expires_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' })}. Fristen forlenges ikke.</p>}
    {content.import_metadata && <details key={'source:' + sourceEpoch} className="source-disclosure"><summary>Vis kildefakta fra PDF</summary><SourceFacts metadata={content.import_metadata} /></details>}
    {issues.length > 0 && <section className="import-warning" aria-label="Usikkerheter fra importen"><h3>Kontroller usikkerheter fra importen</h3>
      <p>Historiske varsler fra den opprinnelige tolkningen beholdes også etter manuelle rettelser. Se gjeldende ukjente fakta ved hver aktivitet. Du kan lagre et uferdig utkast; det er ikke bekreftet.</p>
      <ul>{issues.map((issue, index) => {
        const activityIndex = content.activities.findIndex(activity => activity.id === issue.activityId);
        return <li key={index}>{issue.text} {activityIndex >= 0 && <button type="button" onClick={() => document.getElementById('activity-' + issue.activityId)?.focus()}>Se aktivitet {activityIndex + 1}</button>}{issue.activityId && activityIndex < 0 && <span> Opprinnelig aktivitet er fjernet fra utkastet.</span>}</li>;
      })}</ul></section>}
    <button disabled={!saved || dirty || entryLocked || !!comparison} onClick={showApproval}>Gjennomgå lagret utkast</button><form className="draft-form" onSubmit={event => { event.preventDefault(); void save(); }}>
      <fieldset disabled={entryLocked}><legend>Dagens opplysninger</legend>
        <label>Tjenestedato<input type="date" value={content.service_date ?? ''} onChange={e => edit({ ...content, service_date: e.target.value || null })} /></label>
        <label>Vognløp<input maxLength={200} value={content.vehicle_duty ?? ''} onChange={e => edit({ ...content, vehicle_duty: boundedText(e.target.value, 100) || null })} /></label>
        <p>Vognløp ved starten av dagen. Bytter kan angis ved aktivitetene nedenfor og gjelder fra den aktiviteten til neste bytte. Et vognløpsbytte endrer ikke Buss/vogn.</p>
        <button type="button" onClick={() => edit({ ...content, vehicle_duty: null })}>Tøm vognløp</button>
        <p>Sanntidsverdi: {content.realtime_duty ?? 'ukjent'} (avledet fra vognløp).</p>
        <label>Buss/vogn<input value={content.physical_bus ?? ''} aria-invalid={!!busError(content.physical_bus)} aria-describedby={busError(content.physical_bus) ? 'draft-bus-error' : undefined} onChange={e => { edit({ ...content, physical_bus: e.target.value || null }); const error = busError(e.target.value); if (error) setMessage(error); }} /></label>
        <button type="button" disabled={entryLocked || !!comparison || !!busError(content.physical_bus) || normalizeBus(content.physical_bus) === normalizeBus(saved?.draft.physical_bus ?? null)} onClick={() => { if (busOtherChanges) return; void save(); }}>Lagre buss/vogn</button><button type="button" onClick={() => edit({ ...content, physical_bus: null })}>Tøm buss/vogn</button><p aria-live="polite" aria-label="Buss i utkast">{busMessage} {message}</p><button type="button" disabled={entryLocked || !!comparison || unresolvedTimes || !!busError(content.physical_bus)} onClick={() => void save()}>Lagre hele utkastet med buss</button>
        {busError(content.physical_bus) && <p id="draft-bus-error">{busError(content.physical_bus)}</p>}
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
          <div className="draft-grid">{(['start', 'end'] as const).map(field => <div key={timeEpoch + ':' + field} data-draft-time={activity.id + ':' + field}><PrivateTimeInput label={field === 'start' ? 'Start' : 'Slutt'} value={activity[field]} defaultDate={content.service_date} disabled={entryLocked} resolve={body => mutation('/draft-times/resolve', body)} onValue={value => changeTime(activity.id, field, value)} onState={(dirty, unresolved) => timeState(activity.id, field, dirty, unresolved)} expired={expired} /></div>)}</div>
          {sourceMarkers(content).filter(marker => marker.activityId === activity.id).map((marker, i) => <p key={'marker-' + i}>{marker.text}</p>)}<div className="draft-grid">{fields.filter(([key]) => key !== 'start' && key !== 'end').map(([key, label]) => <label key={key} className={key === 'uncertainty' && issues.some(issue => issue.activityId === activity.id) ? 'import-warning' : undefined}>{label}<input aria-label={label} aria-describedby={key === 'uncertainty' && issues.some(issue => issue.activityId === activity.id) ? 'uncertainty-source-' + activity.id : undefined} maxLength={2 * textLimit(key)} value={(key === 'uncertainty' ? currentUncertainty(content, activity, false) : displayFact(key, activity[key])) ?? ''} onChange={e => edit({ ...content, activities: content.activities.map(a => a.id === activity.id ? { ...a, [key]: (e.target.value === 'tur' && displayFact(key, a[key]) === 'tur' ? a[key] : key === 'type' && e.target.value === 'tur' ? 'trip' : boundedText(e.target.value, textLimit(key))) || null } : a) })} />{key === 'uncertainty' && issues.some(issue => issue.activityId === activity.id) && <small id={'uncertainty-source-' + activity.id}>Fra importen: {issues.filter(issue => issue.activityId === activity.id).map(issue => issue.text).join(' ')}</small>}</label>)}</div>
          <div className="controls"><button type="button" disabled={index === 0} onClick={() => { const rows = [...content.activities]; [rows[index - 1], rows[index]] = [rows[index], rows[index - 1]]; edit({ ...content, activities: rows }); }}>Flytt opp</button><button type="button" onClick={() => removeActivity(activity)}>Fjern aktivitet {index + 1}</button></div>
        </fieldset>)}
        <button type="button" disabled={content.activities.length >= 200} onClick={() => edit({ ...content, activities: [...content.activities, { id: crypto.randomUUID(), ...Object.fromEntries(fields.map(([key]) => [key, null])) }] })}>Legg til aktivitet</button>
      </fieldset>
      {unresolvedTimes && <p>Kontroller uavklarte datoer og klokkeslett før lagring. Inndata er beholdt.</p>}
      <button disabled={busy || suspended || !!comparison || !!pendingDelete || saveUnavailable || draftExpired || unresolvedTimes || !pending && !!busError(content.physical_bus)} type="submit">{pending ? 'Prøv samme lagringsforsøk igjen' : 'Lagre utkast'}</button>
      <p role="status" aria-label="Lagringsstatus">{screen === 'editor' ? message : null}</p><button type="button" disabled={!saved || dirty || entryLocked || !!comparison} onClick={showApproval}>Fortsett til godkjenning</button>
    </form>
    <div className="controls"><button disabled={busy || !!pending || !!pendingDelete || suspended} onClick={reset}>{saved && !saveUnavailable ? 'Forkast endringer' : 'Tilbakestill utkast'}</button>{saved && <button disabled={busy || !!pending || !!pendingDelete || saveUnavailable || suspended || draftExpired || !!comparison} onClick={() => void removeDraft()}>Slett utkast</button>}</div>
    {pendingDelete && <div className="controls"><button disabled={busy} onClick={() => void removeDraft()}>Prøv samme slettingsforsøk igjen</button><button disabled={busy} onClick={() => void removeDraft(true)}>Kontroller slettingen</button></div>}
    {pending && <button disabled={busy} onClick={() => void settle()}>Kontroller lagringsforsøket</button>}
    {comparison && <section aria-label="Sammenlign versjoner"><h3>Lagret versjon {comparison.revision}</h3><p>Lokale endringer står i skjemaet. Last inn lagret versjon for å forkaste dem.</p><dl><dt>Tjenestedato</dt><dd>{comparison.draft.service_date ?? 'Ukjent'}</dd><dt>Vognløp</dt><dd>{comparison.draft.vehicle_duty ?? 'Ukjent'}</dd><dt>Sanntidsverdi</dt><dd>{comparison.draft.realtime_duty ?? 'Ukjent'}</dd><dt>Buss/vogn</dt><dd>{comparison.draft.physical_bus ?? 'Ukjent'}</dd></dl><ol>{comparison.draft.activities.map((activity, index) => <li key={activity.id}><dl><dt>Gjeldende vognløp</dt><dd>{effectiveDuty(comparison.draft, index) ?? 'Ukjent'} · sanntidsverdi {dutySuffix(effectiveDuty(comparison.draft, index)) ?? 'Ukjent'}</dd>{fields.map(([key, label]) => <div className="fact" key={key}><dt>{label}</dt><dd>{displayFact(key, activity[key]) ?? 'Ukjent'}</dd></div>)}</dl></li>)}</ol><button onClick={() => { if (window.confirm('Forkaste lokale endringer og laste lagret versjon?')) void reopen(comparison.id, true); }}>Last inn lagret versjon</button></section>}
    </div></fieldset>
    </section>
    <PrivateConfirmation registryOpen={setRegistryOpen} registryNavigation={registryNavigation} registryDirty={setRegistryDirty} consultationChanged={setConsulting} screen={screen} showPlan={() => setScreen('plan')} showPreparation={() => setScreen('upload')} planChanged={setHasPlan} saved={saved} clean={!dirty && !busy && !comparison && !draftExpired} request={request} mutation={mutation} expired={expired} suspended={suspended} lock={setConfirmationLocked} />
  </div>;
}
