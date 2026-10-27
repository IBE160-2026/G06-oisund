import { privateNow, observePrivateTime } from './privateClock';
import { useEffect, useRef, useState } from 'react';
import { recoverOperation } from './recoverOperation';
import { PrivateTimeInput } from './PrivateTimeInput';

import { osloDateTime } from './dayOverview';

type Content = { title: string; line_tags: string[]; line_scope: 'selected' | 'all'; summary: string | null; description: string | null; source_note: string | null; source_url: string | null; source_updated_at: string | null; valid_from: string | null; valid_until: string | null };
export type Notice = Content & { id: string; workday_id: string | null; revision: number; status: 'registered' | 'ended_manually'; entered_at: string; edited_at: string; checked_at: string | null; checked_revision: number | null; expires_at: string };
type Command = { path: string; kind: 'save' | 'check' | 'end'; target: string | null; before: Notice | null; body: { operation_id: string; expected_revision: number; content?: Content } };
type Props = { suspended: boolean; request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>; expired: () => void; lock: (value: boolean) => void; changed: () => void };
const uuid = (v: any): v is string => typeof v === 'string' && /^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(v);
const stamp = (v: any): v is string => {
  if (typeof v !== 'string') return false;
  const m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{1,6}))?)?(Z|[+-](\d{2}):(\d{2}))$/.exec(v);
  if (!m) return false;
  const [year, month, day, hour, minute, second] = m.slice(1, 7).map(Number);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  return year >= 1 && month >= 1 && month <= 12 && day >= 1 && day <= [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    && hour <= 23 && minute <= 59 && (!m[6] || second <= 59) && (!m[9] || Number(m[9]) <= 23 && Number(m[10]) <= 59) && Number.isFinite(Date.parse(v));
};
const instantKey = (value: string) => Date.parse(value) + ':' + (value.match(/\.(\d+)/)?.[1] ?? '').padEnd(6, '0').slice(3);
const timeFields = new Set(['source_updated_at', 'valid_from', 'valid_until', 'entered_at', 'edited_at', 'checked_at', 'expires_at']);
const canonical = (v: any): string => JSON.stringify(v, (key, value) => timeFields.has(key) && stamp(value) ? instantKey(value) : value && typeof value === 'object' && !Array.isArray(value) ? Object.fromEntries(Object.keys(value).sort().map(key => [key, value[key]])) : value);
const empty = (): Content => ({ title: '', line_tags: [], line_scope: 'selected', summary: null, description: null, source_note: null, source_url: null, source_updated_at: null, valid_from: null, valid_until: null });
// The API supplies authoritative Oslo calendar fields; preserve them verbatim.
const content = (v: Content): Content => ({ title: v.title, line_tags: v.line_tags, line_scope: v.line_scope ?? 'selected', summary: v.summary ?? null, description: v.description ?? null, source_note: v.source_note ?? null, source_url: v.source_url, source_updated_at: v.source_updated_at, valid_from: v.valid_from, valid_until: v.valid_until });
const sourceDateTime = (v: string) => `${v.slice(8, 10)}.${v.slice(5, 7)}.${v.slice(0, 4)}, ${v.slice(11, 19).replace(/[Z+-].*$/, '')} (Oslo-tid)`;
const tagText = (tags: string[]) => tags.map(v => /[",]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v).join(', ');
function parseTags(value: string): string[] | string {
  // One bounded CSV record: ordinary commas still work; doubled quotes preserve
  // a literal quote inside a quoted tag. No inferred splitting of saved tags.
  if (value.length > 30500) return 'Linjefeltet er for langt. Oppgi maks 50 linjer med 300 tegn hver.';
  const result: string[] = []; let i = 0;
  while (i < value.length) {
    while (value[i] === ' ') i++;
    let tag = '';
    if (value[i] === '"') {
      i++; let closed = false;
      while (i < value.length) {
        if (value[i] === '"') { if (value[i + 1] === '"') { tag += '"'; i += 2; } else { i++; closed = true; break; } }
        else tag += value[i++];
      }
      if (!closed) return 'CSV: en sitert linje mangler avsluttende anførselstegn.';
      while (value[i] === ' ') i++;
      if (i < value.length && value[i] !== ',') return 'CSV: etter avsluttende anførselstegn er bare komma tillatt.';
    } else {
      while (i < value.length && value[i] !== ',') { if (value[i] === '"') return 'CSV: omslutt hele linjen med anførselstegn og doble indre anførselstegn.'; tag += value[i++]; }
    }
    tag = tag.trim(); if (tag) result.push(tag);
    if (result.length > 50) return 'Oppgi maks 50 linjer.';
    if (value[i] === ',') i++;
  }
  return [...new Set(result)];
}
const http = (v: any) => { try { const u = new URL(v); return typeof v === 'string' && Array.from(v).length <= 2048 && /^https?:$/.test(u.protocol) && !!u.hostname && !/[\s\\\x00-\x1f\x7f]/.test(v); } catch { return false; } };
const plain = (v: any, max: number) => typeof v === 'string' && v.trim() === v && v.length > 0 && Array.from(v).length <= max && !/[\x00-\x1f\x7f-\x9f\uD800-\uDFFF]/u.test(v);
const multiline = (v: any, max: number) => typeof v === 'string' && v.trim() === v && v.length > 0 && Array.from(v).length <= max && !/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\uD800-\uDFFF]/u.test(v);
const nullable = (v: any) => v === null || stamp(v);
const sameInstant = (a: string | null, b: string | null) => a === null ? b === null : b !== null && stamp(a) && stamp(b) && instantKey(a) === instantKey(b);
function sameContent(a: Content, b: Content) { return ['summary', 'description', 'source_note'].every(k => (a[k as keyof Content] ?? null) === (b[k as keyof Content] ?? null)) && (a.line_scope ?? 'selected') === (b.line_scope ?? 'selected') && a.title === b.title && canonical(a.line_tags) === canonical(b.line_tags) && a.source_url === b.source_url && ['source_updated_at', 'valid_from', 'valid_until'].every(k => sameInstant(a[k as keyof Content] as string | null, b[k as keyof Content] as string | null)); }
export function validNotice(v: any, _id?: string): v is Notice {
  return v && Object.keys(v).filter(k => !['summary', 'description', 'source_note', 'line_scope'].includes(k)).sort().join() === 'checked_at,checked_revision,edited_at,entered_at,expires_at,id,line_tags,revision,source_updated_at,source_url,status,title,valid_from,valid_until,workday_id'
    && uuid(v.id) && (v.workday_id === null || uuid(v.workday_id)) && Number.isSafeInteger(v.revision) && v.revision > 0 && plain(v.title, 300) && (v.source_url === null || http(v.source_url))
    && ['selected', 'all'].includes(v.line_scope ?? 'selected') && (v.summary == null || plain(v.summary, 1000)) && (v.source_note == null || plain(v.source_note, 500)) && (v.description == null || multiline(v.description, 5000))
    && Array.isArray(v.line_tags) && ((v.line_scope ?? 'selected') === 'all' ? v.line_tags.length === 0 : v.line_tags.length > 0) && v.line_tags.length <= 50 && v.line_tags.every((t: any) => plain(t, 300)) && new Set(v.line_tags).size === v.line_tags.length
    && ['registered', 'ended_manually'].includes(v.status) && ['entered_at', 'edited_at', 'expires_at'].every(k => stamp(v[k])) && Date.parse(v.entered_at) <= Date.parse(v.edited_at) && Date.parse(v.edited_at) < Date.parse(v.expires_at)
    && ['source_updated_at', 'valid_from', 'valid_until'].every(k => nullable(v[k])) && (!v.valid_from || !v.valid_until || Date.parse(v.valid_from) <= Date.parse(v.valid_until))
    && (v.checked_at === null && v.checked_revision === null || stamp(v.checked_at) && Date.parse(v.checked_at) >= Date.parse(v.entered_at) && Date.parse(v.checked_at) < Date.parse(v.expires_at) && Number.isSafeInteger(v.checked_revision) && v.checked_revision > 0 && v.checked_revision <= v.revision);
}

// This controller remains mounted above day/activity/management/editor switches.
// Its original command and proposals live in memory only.
export function usePrivateNotices(props: Props) {
  const [screen, setScreen] = useState<'day' | 'list' | 'editor'>('day');
  const [records, setRecords] = useState<Notice[]>([]), [available, setAvailable] = useState(false), [busy, setBusy] = useState(false);
  const [denied, setDenied] = useState(false);
  const [pending, setPending] = useState<Command | null>(null);
  const [draft, setDraft] = useState<Content | null>(null), [base, setBase] = useState<Notice | null>(null), [tags, setTags] = useState('');
  const [timeStates, setTimeStates] = useState<Record<string, { dirty: boolean; unresolved: boolean }>>({});
  const [comparison, setComparison] = useState<Notice | null>(null), [conflict, setConflict] = useState(false), [editorKey, setEditorKey] = useState(0);
  const [expanded, setExpanded] = useState<string | null>(null), [message, setMessage] = useState('Avvikslisten er ikke hentet.');
  const [validationAttempted, setValidationAttempted] = useState(false);
  const [now, setNow] = useState(privateNow());
  useEffect(() => { const timer = window.setInterval(() => setNow(privateNow()), 1000); return () => clearInterval(timer); }, []);
  const alive = useRef(true), sending = useRef(false), original = useRef<Command | null>(null), generation = useRef(0), navigation = useRef(0);
  const title = useRef<HTMLHeadingElement>(null), entry = useRef<HTMLButtonElement>(null);
  const entryId = useRef(''), invokingButton = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    setRecords(current => current.some(value => Date.parse(value.expires_at) <= now) ? current.filter(value => Date.parse(value.expires_at) > now) : current);
    const expired = (value: Notice | null | undefined) => !!value && Date.parse(value.expires_at) <= now;
    // Ending validity creates readable history. Only independent storage
    // retention loss removes saved editor/receipt/comparison presentation.
    if (!expired(base) && !expired(comparison) && !expired(original.current?.before)) return;
    generation.current++; navigation.current++; sending.current = false;
    original.current = null; setPending(null); setBase(null); setDraft(null);
    setTags(''); setTimeStates({}); setComparison(null); setConflict(false);
    setExpanded(null); setEditorKey(value => value+1); setBusy(false);
    if (screen === 'editor') setScreen('list');
    setMessage('Avvikets lagringstid er utløpt. Private felt er fjernet.');
    props.lock(false); props.changed();
  }, [now, base, comparison, pending]);
  const tagResult = parseTags(tags);
  const parsedTags = Array.isArray(tagResult) ? tagResult : null;
  const tagError = typeof tagResult === 'string' ? tagResult : null;
  const normalized = draft ? { ...draft, title: draft.title.trim(), summary: draft.summary?.trim() || null, description: draft.description?.trim() || null, source_note: draft.source_note?.trim() || null, source_url: draft.source_url?.trim() || null, line_tags: draft.line_scope === 'all' ? [] : parsedTags ?? [] } : null;
  const dirty = !!draft && (!base || !sameContent(normalized!, base) || tags !== tagText(base.line_tags)
    || ['title', 'summary', 'description', 'source_note', 'source_url'].some(k => (draft[k as keyof Content] ?? '') !== (base[k as keyof Content] ?? ''))
    || Object.values(timeStates).some(v => v.dirty));
  const unresolvedTime = Object.values(timeStates).some(v => v.unresolved);
  const intervalError = !!draft?.valid_from && !!draft?.valid_until && Date.parse(draft.valid_from) > Date.parse(draft.valid_until);
  const errors = normalized ? {
    title: !plain(normalized.title, 300) ? 'Tittel er påkrevd: skriv 1–300 tegn uten kontrolltegn.' : null,
    line_tags: normalized.line_scope === 'all' ? null : !tags.trim() ? 'Linjer er påkrevd: oppgi minst en linje fra kilden eller velg Alle linjer.' : tagError ?? (!normalized.line_tags.length ? 'Oppgi minst en linje fra kilden eller velg Alle linjer.' : normalized.line_tags.some(v => !plain(v, 300)) ? 'Hver linje må ha 1–300 tegn uten kontrolltegn.' : null),
    summary: normalized.summary !== null && !plain(normalized.summary, 1000) ? 'Kort forklaring: maks 1000 tegn uten kontrolltegn.' : null,
    description: normalized.description !== null && !multiline(normalized.description, 5000) ? 'Detaljert forklaring: maks 5000 tegn; linjeskift og tabulator er tillatt.' : null,
    source_note: normalized.source_note !== null && !plain(normalized.source_note, 500) ? 'Kildebeskrivelse: maks 500 tegn uten kontrolltegn.' : null,
    valid_until: !normalized.valid_until || Date.parse(normalized.valid_until) <= now ? 'Oppgi en fremtidig sluttdato. Et tomt klokkeslett betyr 23:59:59 på Oslo-datoen.' : null,
    source_url: normalized.source_url !== null && !http(normalized.source_url) ? 'Kildelenken må være en gyldig HTTP(S)-adresse, for eksempel https://svipper.no/, maks 2048 tegn og uten mellomrom, omvendt skråstrek eller kontrolltegn.' : null,
  } : {};
  const fieldErrors = Object.values(errors).filter((v): v is string => !!v);
  const authority = null;
  const terminal = !!base && !editable(base, now);
  const mutable = available && !terminal && !props.suspended;
  async function request(path: string) {
    try { return await props.request(path); }
    catch (error: any) { if ([404, 410].includes(error?.status)) await props.request('/auth/session'); throw error; }
  }
  useEffect(() => { props.lock(dirty || !!pending); }, [dirty, pending]);
  useEffect(() => { alive.current = true; return () => { alive.current = false; generation.current++; props.lock(false); }; }, []);
  function navigate(value: 'day' | 'list' | 'editor') { navigation.current++; setScreen(value); }
  useEffect(() => {
    if (screen !== 'day') return;
    // Parent navigation reveals the actual invoker after this render.
    const frame = requestAnimationFrame(() => { const invoker = [document.getElementById(entryId.current), invokingButton.current, entry.current].find(candidate => candidate?.getClientRects().length); invoker?.focus(); });
    return () => cancelAnimationFrame(frame);
  }, [screen]);
  function unavailable(error: any, version: number) {
    if (!alive.current || version !== generation.current) return;
    if (error?.status === 401) { props.expired(); return; }
    setAvailable(false);
    if ([404, 410].includes(error?.status)) { setDenied(true); setComparison(null); }
    props.changed();
  }
  async function current(version = generation.current) {
    let cursor: string | null = null; const all: Notice[] = [];
    do {
      const requestedAt = performance.now();
      const value = await request('/notices' + (cursor ? '?cursor=' + cursor : ''));
      if (!alive.current || version !== generation.current) throw Error('Superseded read');
      if (!value || Object.keys(value).sort().join() !== 'next_cursor,notices,server_now' || !stamp(value.server_now)
        || !Array.isArray(value.notices) || value.notices.length > 50 || !(value.next_cursor === null || uuid(value.next_cursor))
        || value.next_cursor && (cursor && value.next_cursor <= cursor || value.notices.some((v: any) => v.id > value.next_cursor))
        || !value.notices.every((v: any) => validNotice(v) && Date.parse(v.expires_at) > Date.parse(value.server_now))) throw Error();
      // Count the whole request interval conservatively: a delayed response
      // must not grant a fresh validity interval from its arrival time.
      observePrivateTime(value.server_now, requestedAt); setNow(privateNow());
      all.push(...value.notices); cursor = value.next_cursor;
      if (new Set(all.map(v => v.id)).size !== all.length) throw Error();
    } while (cursor);
    setRecords(all); setAvailable(true); setDenied(false); props.changed();
    const newer = base && all.find(v => v.id === base.id && v.revision > base.revision);
    if (draft && newer && !original.current) { setComparison(newer); setConflict(true); }
    return { records: all, serverNow: privateNow() };
  }
  async function load() {
    if (sending.current || props.suspended) return;
    const version = ++generation.current; setBusy(true);
    try { await current(version); if (alive.current && version === generation.current) setMessage(original.current ? 'Forsøket er fortsatt uavklart. Kontroller eller prøv samme forsøk.' : 'Lagrede avvik er hentet.'); }
    catch (error: any) { if (alive.current && version === generation.current) { unavailable(error, version); setMessage('Avvikslisten er utilgjengelig. Prøv igjen eller kontroller originalkilden.'); } }
    finally { if (alive.current && version === generation.current) setBusy(false); }
  }
  function open(event?: { currentTarget: HTMLButtonElement }) { const invoker = event?.currentTarget ?? (document.activeElement instanceof HTMLButtonElement ? document.activeElement : null); entryId.current = invoker?.id ?? ''; invokingButton.current = invoker; navigate('list'); void load(); }
  function edit(value: Notice | null) {
    if (!available || props.suspended || pending || draft || value && !editable(value, now)) return;
    setValidationAttempted(false);
    setBase(value); setDraft(value ? content(value) : empty()); setTags(value ? tagText(value.line_tags) : ''); setTimeStates({}); setComparison(null); setConflict(false); setEditorKey(v => v + 1); navigate('editor');
  }
  function discard() {
    if (pending || sending.current) return;
    setDraft(null); setBase(null); setTimeStates({}); setComparison(null); setConflict(false); setEditorKey(v => v + 1); navigate('list'); setMessage('Ulagrede endringer er forkastet.');
  }
  function accepted(v: Notice, op: Command) {
    if (v.revision !== op.body.expected_revision + 1 || op.target && v.id !== op.target) return false;
    if (op.kind === 'save') return sameContent(v, op.body.content!) && v.status === (op.before?.status ?? 'registered') && sameInstant(v.checked_at, op.before?.checked_at ?? null) && v.checked_revision === (op.before?.checked_revision ?? null) && (op.before ? sameInstant(v.entered_at, op.before.entered_at) : v.checked_at === null && sameInstant(v.entered_at, v.edited_at));
    if (!op.before || !sameContent(v, op.before) || !sameInstant(v.entered_at, op.before.entered_at)) return false;
    return op.kind === 'check' ? v.status === op.before.status && v.checked_revision === v.revision && stamp(v.checked_at) && sameInstant(v.edited_at, op.before.edited_at)
      : v.status === 'ended_manually' && sameInstant(v.checked_at, op.before.checked_at) && v.checked_revision === op.before.checked_revision;
  }
  async function send(command?: Command, lookup = false) {
    if (sending.current || props.suspended) return;
    const retry = !!original.current;
    const op = original.current ?? command; if (!op) return;
    const destination = navigation.current, version = ++generation.current; original.current = op; setPending(op); props.lock(true); sending.current = true; setBusy(true); setMessage('Lagringen er uavklart til svaret er kontrollert.');
    let verified = false, dispatched = false;
    try {
      const status = () => request('/workday-notice-operations/' + op.body.operation_id);
      const mutate = () => { dispatched = true; return props.mutation(op.path, op.body); };
      const authorize = async () => {
        const latest = await current(version);
        const target = latest.records.find(v => v.id === op.target);
        // An absent receipt authorizes a retry only while this original command
        // still has a live target/deadline. Never dispatch an expired original.
        if (op.target ? !target || !editable(target, latest.serverNow) : !op.body.content?.valid_until || Date.parse(op.body.content.valid_until) <= latest.serverNow) {
          throw Object.assign(Error('Original command cannot be recovered'), { noticeUnrecoverable: true });
        }
      };
      const value = lookup ? await status() : retry ? await recoverOperation(status, authorize, mutate) : await mutate();
      if (!alive.current || version !== generation.current) return;
      if (!value || Object.keys(value).sort().join() !== 'operation_id,result' || value.operation_id !== op.body.operation_id || !validNotice(value.result) || !accepted(value.result, op)) throw Error();
      verified = true;
      if (!lookup && canonical(await request('/workday-notice-operations/' + op.body.operation_id)) !== canonical(value)) throw Error();
      if (!alive.current || version !== generation.current) return;
      const latest = await current(version); if (!alive.current || version !== generation.current) return;
      const saved = latest.records.find(v => v.id === value.result.id);
      // These two fields are mutable authority/provenance, not historical
      // command effects: retention can change and parent deletion sets NULL.
      if (!saved || saved.revision < value.result.revision
        || saved.workday_id !== value.result.workday_id && !(saved.workday_id === null && value.result.workday_id !== null)
        || saved.revision === value.result.revision && canonical({ ...saved, expires_at: value.result.expires_at, workday_id: value.result.workday_id }) !== canonical(value.result)) throw Error();
      original.current = null; setPending(null); setExpanded(saved.id);
      if (saved.revision > value.result.revision && op.kind === 'save') { setComparison(saved); setConflict(true); setMessage('Forsøket ble lagret. Et nyere avvik finnes. Forslaget er beholdt for sammenligning.'); }
      else { if (op.kind === 'save') { setDraft(null); setBase(null); setTimeStates({}); setEditorKey(v => v + 1); } setMessage(op.kind === 'check' ? 'Kildekontrollen er lagret.' : op.kind === 'end' ? 'Avviket er avsluttet manuelt.' : 'Avviket er lagret.'); if (destination === navigation.current) navigate('list'); }
    } catch (error: any) {
      if (!alive.current || version !== generation.current) return;
      if (error?.status === 401) { props.expired(); return; }
      if ([404, 410].includes(error?.status)) {
        try { await props.request('/auth/session'); if (!alive.current || version !== generation.current) return; }
        catch (access: any) { if (access?.status === 401) props.expired(); return; }
      }
      let unrecoverable = error?.noticeUnrecoverable === true;
      const retentionDenied = error?.status === 410 && ['Lagringsforsøket er utløpt.', 'Avvikets lagringstid er utløpt.'].includes(error.apiDetail);
      const absent = error?.status === 404 && error.apiDetail === 'Tilgangen ble avvist.';
      if (retentionDenied || absent) {
        try {
          const latest = await current(version);
          const target = latest.records.find(v => v.id === op.target);
          unrecoverable = retentionDenied || (op.target ? !target || !editable(target, latest.serverNow) : !!op.body.content?.valid_until && Date.parse(op.body.content.valid_until) <= latest.serverNow);
        } catch (readError: any) {
          if (readError?.status === 401) { props.expired(); return; }
          // A failed or malformed current read is not proof of disappearance.
        }
      }
      if (unrecoverable) {
        original.current = null; setPending(null);
        setMessage('Lagringsutfallet kan ikke gjenopprettes etter utløpt lagringstid eller bortfalt avvik. Et lokalt forslag er beholdt og kan forkastes. Det opprinnelige forsøket sendes ikke igjen.');
        return;
      }
      const detail = error?.apiDetail;
      const capacityDetail = error?.status === 429 && detail && typeof detail === 'object'
        && Object.keys(detail).sort().join() === 'code,message'
        && (detail.code === 'notice_capacity' && detail.message === 'Registeret har allerede 200 avvik.'
          || detail.code === 'notice_receipt_capacity' && detail.message === 'For mange lagringsforsøk. Vent til tidligere avvik utløper.');
      const known = dispatched && !verified && (
        !op.target && (error?.status === 404 && detail === 'Tilgangen ble avvist.' || error?.status === 410 && detail === 'Lagringsforsøket er utløpt.')
        ||
        error?.status === 409 && ['Lagringsforsøket har annet innhold eller tidligere versjon. Kontroller originalforsøket.', 'Lagret avvik er endret. Hent og gjennomgå på nytt.', 'Avviket er utløpt eller avsluttet manuelt og er skrivebeskyttet.', 'Avviket er utløpt og er skrivebeskyttet.'].includes(detail)
        || error?.status === 422 && ['Kontroller feltene.', 'Oppgi en fremtidig sluttdato for avviket.', 'Sluttdatoen gir lagringstid utenfor støttet kalender.'].includes(detail)
        || capacityDetail);
      if (known) {
        const capacity = capacityDetail ? detail.code === 'notice_capacity' ? 'Registeret har allerede 200 avvik. Forslaget er beholdt og kan forkastes.' : 'For mange lagringsforsøk. Vent til tidligere avvik utløper. Forslaget er beholdt og kan forkastes.' : null;
        original.current = null; setPending(null); setConflict(error.status === 409); setMessage(capacity ?? 'Forsøket ble avvist. Forslaget er beholdt. Hent lagrede avvik og sammenlign før et nytt forsøk.');
        try { const latest = await current(version); if (alive.current && version === generation.current) setComparison(latest.records.find(v => v.id === op.target) ?? null); }
        catch (readError) { unavailable(readError, version); }
      } else { if ([404, 410].includes(error?.status)) unavailable(error, version); setMessage('Lagringen er uavklart. Kontroller eller prøv samme forsøk.'); }
    } finally { if (version === generation.current) { sending.current = false; if (alive.current) setBusy(false); } }
  }
  async function save() {
    if (intervalError) { setMessage('Gyldig til må være samtidig med eller etter Gyldig fra. Rett gyldighetsintervallet før lagring.'); return; }
    if (sending.current || busy || !mutable || !normalized || pending || conflict || unresolvedTime || fieldErrors.length) { setValidationAttempted(true); return; }
    setValidationAttempted(false);
    let operationId = crypto.randomUUID();
    if (!base) {
      const version = generation.current;
      sending.current = true; setBusy(true);
      try {
        const issued = await props.mutation('/notice-operations', {});
        if (!alive.current || version !== generation.current) return;
        if (!issued || Object.keys(issued).sort().join() !== 'expires_at,operation_id' || !uuid(issued.operation_id) || !stamp(issued.expires_at)) throw Error();
        operationId = issued.operation_id;
      } catch (error: any) {
        if (alive.current && version === generation.current) {
          if (error?.status === 401) props.expired();
          setMessage('Lagringsforsøket kunne ikke opprettes. Forslaget er beholdt. Prøv Lagre avvik igjen.');
        }
        return;
      } finally { sending.current = false; if (alive.current) setBusy(false); }
    }
    void send({ path: '/notices' + (base ? '/' + base.id : ''), kind: 'save', target: base?.id ?? null, before: base, body: { operation_id: operationId, expected_revision: base?.revision ?? 0, content: normalized } });
  }
  function action(value: Notice, kind: 'check' | 'end') {
    if (!available || props.suspended || !editable(value, now) || dirty || pending || busy) return;
    if (kind === 'end' && !window.confirm('Avslutte dette avviket manuelt? Dette avslutter bare avviket, ikke skiftet.')) return;
    void send({ path: '/notices/' + value.id + '/' + kind, kind, target: value.id, before: value, body: { operation_id: crypto.randomUUID(), expected_revision: value.revision } });
  }
  function reviewComparison() {
    if (pending || !available || !draft || base && !comparison || comparison && !editable(comparison, now)) return;
    if (comparison) setBase(comparison); setComparison(null); setConflict(false); setMessage('Lagret avvik er gjennomgått. Det beholdte forslaget kan lagres med et nytt uttrykkelig forsøk.');
  }
  const feedback = validationAttempted && screen === 'editor' ? fieldErrors.length ? 'Ikke lagret. ' + fieldErrors.join(' ') : 'Endringene er ikke lagret. Kontroller lagringskravene og trykk Lagre avvik når feltene er klare.'
    : dirty && !pending && !busy && /^(Avviket er lagret\.|Lagrede avvik er hentet\.|Kildekontrollen er lagret\.|Avviket er avsluttet manuelt\.)$/.test(message)
      ? 'Ulagrede avviksendringer. Inndata finnes bare mens siden er åpen.' : message;
  return { screen, navigate, open, entry, title, records, now, available, denied, busy, mutable, terminal, authority, draft, setDraft, tags, setTags, parsedTags, tagError, dirty, pending, expanded, setExpanded, message: feedback, load, edit, discard, save, send, action, comparison, conflict, reviewComparison, editorKey, timeStates, setTimeStates, unresolvedTime, intervalError, fieldErrors, errors, props };
}

export type NoticeController = ReturnType<typeof usePrivateNotices>;
export function NoticeScreens({ notices: n, back, visible = true }: { notices: NoticeController; serviceDate: string | null; back: () => void; visible?: boolean }) {
  // Reader-to-maintenance also reveals an ancestor after the screen switch.
  useEffect(() => { if (visible && n.screen !== 'day') n.title.current?.focus(); }, [visible, n.screen]);
  const p = n.props;
  const disabled = !n.mutable || n.busy || !!n.pending;
  return <section className="private-notices" hidden={n.screen === 'day'} aria-label="Avviksvedlikehold">
    <h2 ref={n.title} tabIndex={-1}>{n.screen === 'editor' ? 'Rediger avvik' : 'Manuelt vedlikeholdte avvik'}</h2>
    <p>Forlengelse må lagres før gjeldende sluttid. Utløpte og manuelt avsluttede avvik er skrivebeskyttet historikk. Ingen av delene bekrefter at veien er klar eller at kilden er kontrollert.</p><p>Felles avviksregister for kontoen. Avvik brukes automatisk på alle relevante bekreftede dager frem til sluttdatoen.</p>
    {n.screen !== 'editor' && <p role="status" aria-label="Avviksstatus">{n.message}</p>}
    {n.terminal && <p>Avviket er utløpt eller avsluttet manuelt og er skrivebeskyttet.</p>}
    {!n.available && <p>Eventuelle tidligere viste opplysninger er ikke oppdatert.</p>}
    <div className="controls"><button disabled={p.suspended} onClick={back}>Tilbake til dagen</button><button disabled={n.busy || p.suspended} onClick={() => void n.load()}>Hent lagrede avvik</button></div>
    {n.pending && <div className="controls"><button disabled={n.busy || p.suspended} onClick={() => void n.send(undefined, true)}>Kontroller avvikslagringen</button><button disabled={n.busy || p.suspended} onClick={() => void n.send()}>Prøv samme avvikslagring igjen</button></div>}
    <div hidden={n.screen !== 'list'}>
      {n.draft ? <button onClick={() => n.navigate('editor')}>Tilbake til ulagret avvik</button> : <button disabled={!n.available || n.busy || !!n.pending || p.suspended} onClick={() => n.edit(null)}>Registrer avvik</button>}
      {n.available && n.records.length === 0 && <p>Ingen avvik er registrert her. Kontroller originalkilden.</p>}
      <ul className="notice-list">{(!n.denied ? n.records.filter(v => Date.parse(v.expires_at) > n.now) : []).map(value => <li key={value.id}><details open={n.expanded === value.id} onToggle={e => { if (e.currentTarget.open) n.setExpanded(value.id); }}><summary>{value.title} · {noticeStatus(value, n.now)}</summary><NoticeFacts value={value} now={n.now} />
        {editable(value, n.now) && <div className="controls"><button disabled={disabled || !!n.draft} onClick={() => n.edit(value)}>Rediger {value.title}</button><button disabled={disabled || n.dirty} onClick={() => n.action(value, 'check')}>Kontrollerte kilden nå</button>{value.status === 'registered' && <button disabled={disabled || n.dirty} onClick={() => n.action(value, 'end')}>Avslutt avvik manuelt</button>}</div>}
        <p>Kildekontroll registrerer ditt uttrykkelige kontrolltidspunkt. Det er ingen automatisk kontroll eller garanti for dekning.</p>
      </details></li>)}</ul>
    </div>
    <div hidden={n.screen !== 'editor'}>
      <button onClick={() => n.navigate('list')}>Tilbake til avvik</button>
      <p>Gi trafikkmeldingen en tittel. Bruk kort forklaring til et sammendrag og detaljert forklaring til hele meldingen, instruksjoner og separate tidsvinduer. Velg bestemte linjer og oppgi dem fra kilden, eller velg Alle linjer uttrykkelig.</p>
      <p>Tittel og et uttrykkelig linjevalg er påkrevd. Sluttdato er påkrevd. Forklaringer, kildebeskrivelse, lenke og øvrige tidspunkt er valgfrie. La kildens oppdateringstid og start stå tomme når de ikke er oppgitt.</p>
      {n.draft && <div key={n.editorKey}><fieldset disabled={disabled}><legend>Kildeopplysninger</legend>
        <label>Tittel<input value={n.draft.title} aria-invalid={!!n.errors.title} aria-describedby={n.errors.title ? 'notice-title-error' : undefined} onChange={e => n.setDraft(v => v && ({ ...v, title: e.target.value }))} /></label>
        {n.errors.title && <p id="notice-title-error">{n.errors.title}</p>}
        <label>Kort forklaring<input value={n.draft.summary ?? ''} aria-invalid={!!n.errors.summary} aria-describedby={n.errors.summary ? 'notice-summary-error' : undefined} onChange={e => n.setDraft(v => v && ({ ...v, summary: e.target.value }))} /></label>
        {n.errors.summary && <p id="notice-summary-error">{n.errors.summary}</p>}
        <label>Detaljert forklaring<textarea aria-label="Detaljert forklaring" aria-invalid={!!n.errors.description} aria-describedby={n.errors.description ? 'notice-description-error' : undefined} rows={7} value={n.draft.description ?? ''} onChange={e => n.setDraft(v => v && ({ ...v, description: e.target.value }))} /></label>
        {n.errors.description && <p id="notice-description-error">{n.errors.description}</p>}
        <label>Linjeomfang<select aria-label="Linjeomfang" aria-invalid={!!n.errors.line_tags} aria-describedby={n.errors.line_tags ? 'notice-line_tags-error' : undefined} value={n.draft.line_scope} onChange={e => n.setDraft(v => v && ({ ...v, line_scope: e.target.value as 'selected' | 'all' }))}><option value="selected">Bestemte linjer</option><option value="all">Alle linjer</option></select></label>
        <div hidden={n.draft.line_scope === 'all'}><label>Linjer fra kilden (kommaseparert)<input value={n.tags} aria-invalid={!!n.errors.line_tags} aria-describedby={n.errors.line_tags ? 'notice-line_tags-error' : undefined} onChange={e => n.setTags(e.target.value)} /></label>
        <p>Oppgi linjene eller kopier hele ruteoverskriften fra kilden, maks 300 tegn per linje. Ingen linjenumre hentes automatisk ut av teksten.</p>
        <p>Linjer med komma eller anførselstegn omsluttes av doble anførselstegn. Et anførselstegn i en slik linje skrives to ganger.</p>
        {n.draft.line_scope === 'selected' && n.tagError && <p role="alert">{n.tagError}</p>}</div>
        {n.errors.line_tags && <p id="notice-line_tags-error">{n.errors.line_tags}</p>}
        <label>Kildebeskrivelse<input value={n.draft.source_note ?? ''} aria-invalid={!!n.errors.source_note} aria-describedby={n.errors.source_note ? 'notice-source_note-error' : undefined} onChange={e => n.setDraft(v => v && ({ ...v, source_note: e.target.value }))} /></label>
        {n.errors.source_note && <p id="notice-source_note-error">{n.errors.source_note}</p>}
        <label>Originalkilde (HTTP eller HTTPS)<input type="url" aria-invalid={!!n.errors.source_url} aria-describedby={n.errors.source_url ? 'notice-source_url-error' : undefined} value={n.draft.source_url ?? ''} onChange={e => n.setDraft(v => v && ({ ...v, source_url: e.target.value }))} /></label>
        <p>Valgfri HTTP(S)-lenke, også til en felles trafikkoversikt. For SMS kan du la lenken stå tom og beskrive kilden.</p>
        {n.errors.source_url && <p id="notice-source_url-error">{n.errors.source_url}</p>}
        <p>Tomme valgfrie tidspunkt betyr ukjent. Oppgi dato og tid i Oslo, og velg forekomst når klokken stilles tilbake.</p>
        {(['source_updated_at', 'valid_from', 'valid_until'] as const).map((field, i) => <PrivateTimeInput dateOnlyEnd={field === 'valid_until'} key={field} label={['Kilden oppdatert', 'Gyldig fra', 'Gyldig til'][i]} value={n.draft![field]} defaultDate={null} disabled={disabled} resolve={body => p.mutation('/draft-times/resolve', body)} expired={p.expired} onValue={value => n.setDraft(v => v && ({ ...v, [field]: value }))} onState={(dirty, unresolved) => n.setTimeStates(values => { const old = values[field]; return old?.dirty === dirty && old?.unresolved === unresolved ? values : { ...values, [field]: { dirty, unresolved } }; })} />)}
      </fieldset>
      {n.intervalError && <p role="alert">Gyldig til må være samtidig med eller etter Gyldig fra. Rett gyldighetsintervallet før lagring.</p>}
      {n.conflict && <div className="import-warning"><p>Det lagrede avviket er endret. Ditt forslag er beholdt.</p>
                {n.comparison && !n.denied && <><h3>Nyere lagret avvik</h3><NoticeFacts value={n.comparison} now={n.now} /><button disabled={!n.available || n.busy || !!n.pending || p.suspended || !editable(n.comparison, n.now)} onClick={n.reviewComparison}>Jeg har sammenlignet; behold mitt forslag</button></>}
        {!n.comparison && n.available && !n.terminal && <button disabled={disabled} onClick={n.reviewComparison}>Jeg har gjennomgått registeret; behold mitt forslag</button>}
      </div>}
      <section aria-label="Lagringskrav" aria-live="polite">
        {n.fieldErrors.length > 0 && <><p>Før avviket kan lagres:</p><ul>{n.fieldErrors.map(error => <li key={error}>{error}</li>)}</ul></>}
        {n.unresolvedTime && <p>Kan ikke lagre: {Object.entries(n.timeStates).filter(([, state]) => state.unresolved).map(([field]) => ({ source_updated_at: 'Kilden oppdatert', valid_from: 'Gyldig fra', valid_until: 'Gyldig til' })[field]).join(', ')} er ufullstendig eller uavklart. Se meldingen ved tidspunktet: fyll ut både dato og klokkeslett, velg forekomst ved klokkeomstilling, velg et annet klokkeslett hvis det ikke finnes, eller prøv kontrollen igjen hvis tjenesten er utilgjengelig. Tøm tidspunktet for å lagre det som ukjent.</p>}
        {n.intervalError && <p>Kan ikke lagre: Gyldig til må være samtidig med eller etter Gyldig fra.</p>}
        {n.pending ? <p>Lagringen må avklares. Bruk «Kontroller avvikslagringen» eller «Prøv samme avvikslagring igjen» øverst.</p> : n.busy ? <p>Venter på svar før du kan lagre.</p> : n.terminal ? <p>Avviket er utløpt eller avsluttet manuelt. Det kan ikke lagres.</p> : !n.mutable ? <p>Lagring er utilgjengelig. Hent lagrede avvik eller gå tilbake til dagen og kontroller status.</p> : n.conflict && <p>Sammenlign lagret avvik før et nytt lagringsforsøk.</p>}
      </section>
      <div className="controls"><button disabled={disabled || n.conflict || n.unresolvedTime || n.intervalError || (n.draft?.line_scope === 'selected' && n.parsedTags === null)} onClick={n.save}>Lagre avvik</button><button disabled={!!n.pending || n.busy} onClick={n.discard}>Forkast ulagrede endringer</button></div>
      {n.screen === 'editor' && <p role="status" aria-label="Avviksstatus">{n.message}</p>}
      <p>{n.dirty ? 'Ulagrede endringer finnes bare mens siden er åpen.' : 'Ingen ulagrede endringer.'}</p></div>}
    </div>
  </section>;
}

export const editable = (v: Notice, now = privateNow()) => v.status === 'registered' && (!v.valid_until || Date.parse(v.valid_until) > now) && Date.parse(v.expires_at) > now;
export const noticeStatus = (v: Notice, now = privateNow()) => v.status === 'ended_manually' ? 'Avsluttet manuelt' : !v.valid_until ? 'Mangler sluttdato' : Date.parse(v.valid_until) <= now ? 'Utløpt' : 'Registrert';

export function NoticeFacts({ value: v, now }: { value: Notice; now: number }) {
  return <div className="notice-facts"><p>Tittel: {v.title}</p><p>Linjer fra kilden: {v.line_scope === 'all' ? 'Alle linjer' : tagText(v.line_tags)}</p><p>Status: {noticeStatus(v, now)}</p>
    {v.summary && <p>Kort forklaring: {v.summary}</p>}
    {v.description && <p style={{ whiteSpace: 'pre-wrap' }}>Detaljert forklaring: {v.description}</p>}
    {v.source_note && <p>Kildebeskrivelse: {v.source_note}</p>}
    {v.source_url && <p><a href={v.source_url} target="_blank" rel="noopener noreferrer">{v.source_url}</a></p>}
    <p>{v.source_updated_at ? 'Kilden oppdatert: ' + sourceDateTime(v.source_updated_at) : 'Kildens oppdateringstid er ukjent'}</p>
    <p>{!v.valid_from && !v.valid_until ? 'Gyldighet ukjent' : (v.valid_from && v.valid_until ? 'Gyldighet: ' : 'Delvis kjent gyldighet: ') + (v.valid_from ? 'fra ' + sourceDateTime(v.valid_from) : 'fra ukjent') + (v.valid_until ? ' til ' + sourceDateTime(v.valid_until) : ' til ukjent')}</p>
    <p>Registrert: {osloDateTime(v.entered_at)}</p><p>Sist endret: {osloDateTime(v.edited_at)}</p><p>{v.checked_at ? (v.checked_revision === v.revision ? 'Sist kontrollert: ' : 'Kontrollert før siste endring: ') + osloDateTime(v.checked_at) : 'Ikke kontrollert'}</p>
  </div>;
}
