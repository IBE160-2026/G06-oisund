import { privateNow } from './privateClock';
import { useCallback, useEffect, useRef, useState } from 'react';
import { validContent, type Content, type Saved } from './PrivateDrafts';
import { SourceFacts } from './PrivateImport';
import { recoverOperation } from './recoverOperation';


import { NoticeScreens, usePrivateNotices } from './PrivateNotices';
import { PrivateWorkdayView } from './PrivateWorkdayView';
import { effectiveDuty, activityFactMissing, displayFact, currentUncertainty } from './draftInterpretation';

type Review = { operation_id: string; operation_expires_at: string; draft_id: string; revision: number; draft: Content; blockers: string[]; unknowns: { id: string; label: string }[]; classifications_required: string[]; supported_types: string[]; final_end: string | null; expires_at: string | null };
type Decisions = { operation_id: string; expected_revision: number; acknowledgements: string[]; classifications: Record<string, string> };
export type Plan = { id: string; source_draft_id: string; source_revision: number; confirmed_at: string; final_end: string; expires_at: string; state: 'confirmed'; draft: Content; acknowledgements: string[]; classifications: Record<string, string>; unknowns: { id: string; label: string }[] };
type Summary = Pick<Plan, 'id' | 'source_draft_id' | 'source_revision' | 'expires_at'> & { service_date: string | null };
type Deletion = { id: string; expires_at: string; body: { operation_id: string; source_revision: number } };
type Props = { saved: Saved | null; clean: boolean; request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>; expired: () => void; suspended: boolean; lock: (value: boolean) => void; settingsBlocked: (value: boolean) => void; screen: 'upload' | 'import' | 'editor' | 'direct' | 'approval' | 'plan'; showPlan: () => void; showPreparation: () => void; planChanged: (value: boolean) => void; consultationChanged: (value: boolean) => void; registryDirty: (value: boolean) => void; registryOpen: (value: boolean) => void; registryNavigation: number };
const uuid = (v: any): v is string => typeof v === 'string' && /^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(v);
const canonical = (v: any): string => JSON.stringify(v, (_, value) => value && typeof value === 'object' && !Array.isArray(value) ? Object.fromEntries(Object.keys(value).sort().map(key => [key, value[key]])) : value);
const live = (v: any) => typeof v === 'string' && Number.isFinite(Date.parse(v)) && Date.parse(v) > privateNow();
const date = (v: string) => new Date(v).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' });
const finalEnd = (content: Content) => Math.max(...content.activities.map(a => Date.parse(a.end ?? '')));
const typeLabels: Record<string, string> = { trip: 'Passasjertur', deadhead: 'Tomkjøring', deadhead_car: 'Tomkjøring med CAR', 'Tomkjøring med CAR': 'Tomkjøring med CAR (kildetype)', CAR: 'CAR', 'Sign-on': 'Oppmøte', 'Sign-off': 'Avslutning', MealBreak: 'Matpause', Coffee: 'Kaffepause', 'Split break': 'Deltskiftpause', 'Paid meal before': 'Betalt matpause før', 'Paid meal after': 'Betalt matpause etter', 'Travel to': 'Reise til', 'Travel from': 'Reise fra', Fadder: 'Fadder', Instruktør: 'Instruktør', manual: 'Manuelt klassifisert arbeid' };
const supportedTypes = Object.keys(typeLabels);
function validCandidates(value: Review): boolean {
  const expected = value.draft.activities.flatMap((activity, index) => {
    if (activity.type !== 'trip' && !value.classifications_required.includes(activity.id)) return [];
    const prefix = `Aktivitet ${index + 1}: `;
    return [
      ...[['from_place', 'fra sted'], ['to_place', 'til sted'], ['trip', 'turnummer'], ['line', 'linje'], ['direction', 'retning']].filter(([field]) => activityFactMissing(activity[field])).map(([field, title]) => ({ id: activity.id + ':' + field, label: prefix + title + ' er ukjent.' })),
      ...(activityFactMissing(currentUncertainty(value.draft, activity)) ? [] : [{ id: activity.id + ':uncertainty', label: prefix + currentUncertainty(value.draft, activity) }]),
    ];
  });
  return expected.length === value.unknowns.length && value.unknowns.every(item => expected.some(candidate => candidate.id === item.id && candidate.label === item.label));
}
export function validPlan(value: any): value is Plan {
  return value && Object.keys(value).sort().join() === 'acknowledgements,classifications,confirmed_at,draft,expires_at,final_end,id,source_draft_id,source_revision,state,unknowns'
    && uuid(value.id) && uuid(value.source_draft_id) && Number.isInteger(value.source_revision) && value.source_revision > 0
    && value.state === 'confirmed' && Number.isFinite(Date.parse(value.confirmed_at)) && live(value.expires_at)
    && validContent(value.draft) && value.draft.service_date && value.draft.activities.length > 0
    && value.draft.activities.every((a: any, i: number) => a.start && a.end && (i === 0 || Date.parse(a.start) >= Date.parse(value.draft.activities[i - 1].start)))
    && Date.parse(value.final_end) === finalEnd(value.draft) && Date.parse(value.expires_at) <= Date.parse(value.final_end) + 7 * 86400000
    && Array.isArray(value.acknowledgements) && value.acknowledgements.length <= 3000 && value.acknowledgements.every((v: any) => typeof v === 'string' && v.length <= 200)
    && new Set(value.acknowledgements).size === value.acknowledgements.length && value.classifications && typeof value.classifications === 'object' && !Array.isArray(value.classifications)
    && Array.isArray(value.unknowns) && value.unknowns.length === value.acknowledgements.length && new Set(value.unknowns.map((v: any) => v?.id)).size === value.unknowns.length && value.unknowns.every((v: any) => v && typeof v.label === 'string' && value.acknowledgements.includes(v.id))
    && canonical(Object.keys(value.classifications).sort()) === canonical(value.draft.activities.filter((a: any) => !supportedTypes.includes(a.type)).map((a: any) => a.id).sort())
    && Object.entries(value.classifications).every(([, kind]) => supportedTypes.includes(kind as string));
}
const factNames: Record<string, string> = { type: 'Aktivitetstype', raw_code: 'Opprinnelig kode', start: 'Start med dato og Oslo-offset', end: 'Slutt med dato og Oslo-offset', source_start: 'Opprinnelig startklokke', source_end: 'Opprinnelig sluttklokke', from_place: 'Fra sted', to_place: 'Til sted', trip: 'Turnummer', line: 'Linje', direction: 'Retning', uncertainty: 'Usikkerhet / ukjente fakta', provenance: 'Kilde / manuell rettelse' };
export function Facts({ content, classifications = {}, historical = false }: { content: Content; classifications?: Record<string, string>; historical?: boolean }) {
  return <><dl>{Object.entries(content).filter(([key]) => !['activities', 'import_metadata', 'vehicle_duty_changes'].includes(key)).map(([key, value]) => <div key={key}><dt>{{ service_date: 'Tjenestedato', vehicle_duty: 'Vognløp', realtime_duty: 'Sanntidsverdi', physical_bus: historical ? 'Fysisk buss ved bekreftelse (historisk)' : 'Fysisk buss (manuelt i utkastet)' }[key] ?? key}</dt><dd>{String(value ?? 'Ukjent')}</dd></div>)}</dl>
    <ol>{content.activities.map((activity, index) => <li key={activity.id}><h4>Aktivitet {index + 1}</h4><p>Vognløp: {effectiveDuty(content, index) ?? 'Ukjent'}</p><dl>{Object.entries(activity).filter(([key]) => key !== 'id').map(([key, value]) => <div className="fact" key={key}><dt>{factNames[key] ?? key}</dt><dd>{activityFactMissing(key === 'uncertainty' && !historical ? currentUncertainty(content, activity) : value) ? 'Ukjent' : key === 'uncertainty' && !historical ? currentUncertainty(content, activity) : displayFact(key, value)}</dd></div>)}</dl>{classifications[activity.id] && <p>Eksplisitt klassifisert som: {typeLabels[classifications[activity.id]]}</p>}</li>)}</ol>
    {content.import_metadata && <details><summary>Bevarte kildefakta</summary><SourceFacts metadata={content.import_metadata} historical={historical} /></details>}
    </>;
}

export function PrivateConfirmation({ saved, clean, request, mutation, expired, suspended, lock, settingsBlocked, screen, showPlan, showPreparation, planChanged, consultationChanged, registryDirty, registryOpen, registryNavigation }: Props) {
  const [noticeReaderOpen, setNoticeReaderOpen] = useState(false);
  const [planOpen, setPlanOpen] = useState(0);
  const [activityOpen, setActivityOpen] = useState(false);
  const dayTitle = useRef<HTMLHeadingElement>(null);
  const presentation = useRef({ screen, version: 0 });
  if (presentation.current.screen !== screen) presentation.current = { screen, version: presentation.current.version + 1 };
  const availabilityRef = useRef({ bus: true, selection: true, start: true });
  const [planAvailable, setPlanAvailable] = useState(true);
  const guardAvailability = useCallback((key: 'bus' | 'selection' | 'start', value: boolean) => {
    availabilityRef.current[key] = value; setPlanAvailable(Object.values(availabilityRef.current).every(Boolean));
  }, []);
  const busAvailability = useCallback((value: boolean) => guardAvailability('bus', value), [guardAvailability]);
  const selectionAvailability = useCallback((value: boolean) => guardAvailability('selection', value), [guardAvailability]);
  const startAvailability = useCallback((value: boolean) => guardAvailability('start', value), [guardAvailability]);
  const lockRef = useRef({ bus: false, selection: false, start: false, outcome: false, notice: false });
  const [busLocked, setBusLocked] = useState(false);
  const [dayNavigationLocked, setDayNavigationLocked] = useState(false);
  const busLockedRef = useRef(false);
  const guardChild = useCallback((key: 'bus' | 'selection' | 'start' | 'outcome' | 'notice', value: boolean) => {
    lockRef.current[key] = value;
    const locked = Object.values(lockRef.current).some(Boolean);
    busLockedRef.current = locked;
    if (value) { reading.current++; epoch.current++; setBusy(false); }
    setBusLocked(locked); setDayNavigationLocked(lockRef.current.bus || lockRef.current.start);
  }, []);
  const guardBus = useCallback((value: boolean) => guardChild('bus', value), [guardChild]);
  const guardSelection = useCallback((value: boolean) => guardChild('selection', value), [guardChild]);
  const guardStart = useCallback((value: boolean) => guardChild('start', value), [guardChild]);
  const guardOutcome = useCallback((value: boolean) => guardChild('outcome', value), [guardChild]);

  const notices = usePrivateNotices({ suspended, request, mutation, expired, lock: registryDirty, changed: () => {} });
  useEffect(() => { registryOpen(notices.screen !== 'day' || screen === 'plan' && noticeReaderOpen); }, [notices.screen, noticeReaderOpen, screen]);
  useEffect(() => { notices.navigate('day'); }, [registryNavigation]);
  const [review, setReview] = useState<Review | null>(null);
  const [acks, setAcks] = useState<string[]>([]);
  const [classes, setClasses] = useState<Record<string, string>>({});
  const [pending, setPending] = useState<Decisions | null>(null);
  const relevantUnknowns = (value: Review, classifications: Record<string, string>) => value.unknowns.filter(item => {
    const activity = value.draft.activities.find(activity => item.id.startsWith(activity.id + ':'));
    return !!activity && (classifications[activity.id] ?? activity.type) === 'trip';
  });
  const visibleUnknowns = review ? relevantUnknowns(review, classes) : [];
  const [deleting, setDeleting] = useState<Deletion | null>(null);
  const deletionRef = useRef<Deletion | null>(null), reading = useRef(0), sendingDeletion = useRef(false);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [items, setItems] = useState<Summary[]>([]);
  const [cursor, setCursor] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('Lagre utkastet før gjennomgang.');
  const alive = useRef(true), epoch = useRef(0);
  const reviewRead = useRef<{ selected: string; generation: number } | null>(null);
  const planRead = useRef<{ id: string; generation: number } | null>(null);
  const title = useRef<HTMLHeadingElement>(null);
  const selected = saved ? saved.id + ':' + saved.revision : '';
  useEffect(() => { availabilityRef.current = { bus: true, selection: true, start: true }; setPlanAvailable(true); }, [plan?.id, planOpen]);
  useEffect(() => { planChanged(!!plan); }, [!!plan]);
  useEffect(() => { consultationChanged(!!plan && screen === 'plan' && activityOpen); }, [screen, activityOpen, !!plan]);
  useEffect(() => { if (screen === 'plan' && !activityOpen) dayTitle.current?.focus(); }, [screen, plan?.id]);
  useEffect(() => { alive.current = true; return () => { alive.current = false; }; }, []);
  useEffect(() => { lock(!!pending || !!deleting || busLocked); return () => lock(false); }, [pending, deleting, busLocked]);
  useEffect(() => { settingsBlocked(busy || !!review && (acks.length > 0 || Object.values(classes).some(Boolean))); return () => settingsBlocked(false); }, [busy, !!review, acks, classes]);
  useEffect(() => { epoch.current++; if (!pending) { setReview(null); setAcks([]); setClasses({}); } }, [selected, clean]);
  useEffect(() => { if (screen === 'approval') { title.current?.focus(); if (clean && !review && !pending) void begin(); } }, [screen, clean]);
  useEffect(() => {
    if (!plan) { setActivityOpen(false); if (screen === 'plan') showPreparation(); }
  }, [!!plan, screen]);
  useEffect(() => {
    const deadline = deleting?.expires_at ?? plan?.expires_at;
    if (!deadline) return;
    let timer = 0;
    const check = () => {
      const remaining = Date.parse(deadline) - privateNow();
      if (remaining <= 0) {
        if (plan && planRead.current?.id === plan.id && planRead.current.generation === reading.current) { reading.current++; planRead.current = null; setBusy(false); }
        if (deleting) { reading.current++; deletionRef.current = null; setDeleting(null); setBusy(false); }
        setPlan(null); setActivityOpen(false);
        if (!pending && !review) setMessage('Planen eller gjennomgangen er utløpt. Kontroller listen på nytt.');
        if (screen === 'plan') showPreparation();
      } else timer = window.setTimeout(check, Math.min(remaining, 1000));
    };
    check(); return () => clearTimeout(timer);
  }, [plan, deleting, screen, !!pending, !!review]);
  useEffect(() => {
    // A confirmation receipt can outlive its source and an unrelated old plan.
    const deadline = pending ? review?.expires_at : review ? review.blockers.length === 0 && review.expires_at && saved ? new Date(Math.min(Date.parse(review.expires_at), Date.parse(saved.expires_at))).toISOString() : saved?.expires_at : null;
    if (!deadline) return;
    let timer = 0;
    const check = () => {
      const remaining = Date.parse(deadline) - privateNow();
      if (remaining <= 0) { reading.current++; epoch.current++; setBusy(false); setReview(null); setPending(null); setAcks([]); setClasses({}); setMessage('Planen eller gjennomgangen er utløpt. Kontroller listen på nytt.'); }
      else timer = window.setTimeout(check, Math.min(remaining, 1000));
    };
    check(); return () => clearTimeout(timer);
  }, [review, pending, saved?.expires_at]);
  useEffect(() => {
    if (!items.length) return;
    let timer = 0;
    const check = () => {
      const remaining = Math.min(...items.map(item => Date.parse(item.expires_at))) - privateNow();
      if (remaining <= 0) { setItems(current => current.filter(item => live(item.expires_at))); setCursor(null); }
      else timer = window.setTimeout(check, Math.min(remaining, 1000));
    };
    check(); return () => clearTimeout(timer);
  }, [items]);
  function failure(error: any) {
    if (error?.status === 401) { expired(); return; }
    setMessage(error?.status === 409 ? 'Utkastet er endret eller har allerede en plan. Last inn utkastet eller oppdater planlisten.' : [404, 410].includes(error?.status) ? 'Tilgangen ble avvist eller fristen er utløpt.' : error?.status === 429 ? 'For mange uavklarte gjennomganger. Vent til de utløper.' : 'Tjenesten kunne ikke bekrefte svaret. Prøv igjen.');
  }
  async function list(more = false, afterConfirmation = false) {
    const generation = reading.current;
    setBusy(true);
    try {
      const value = await request('/workdays' + (more && cursor ? '?cursor=' + cursor : ''));
      if (!alive.current || generation !== reading.current || deletionRef.current || busLockedRef.current) return;
      if (!value || Object.keys(value).sort().join() !== 'next_cursor,workdays' || !Array.isArray(value.workdays) || value.workdays.length > 50 || !(value.next_cursor === null || uuid(value.next_cursor))
        || !value.workdays.every((v: any) => v && uuid(v.id) && uuid(v.source_draft_id) && Number.isInteger(v.source_revision) && v.source_revision > 0 && live(v.expires_at) && (v.service_date === null || /^\d{4}-\d{2}-\d{2}$/.test(v.service_date)))) throw Error();
      const combined = more ? [...items, ...value.workdays] : value.workdays;
      if (new Set(combined.map((v: Summary) => v.id)).size !== combined.length) throw Error();
      setItems(combined); setCursor(value.next_cursor); setMessage(afterConfirmation ? 'Planen er bekreftet. Planlisten er oppdatert.' : 'Planlisten er oppdatert.');
    } catch (error: any) { if (alive.current && generation === reading.current && !deletionRef.current) { if (afterConfirmation && error?.status !== 401) setMessage('Planen er bekreftet. Planlisten kunne ikke oppdateres. Prøv Oppdater planlisten.'); else failure(error); } }
    finally { if (alive.current && generation === reading.current) setBusy(false); }
  }
  useEffect(() => { void list(); }, []);
  async function begin() {
    if (!saved || !clean || pending || deletionRef.current || busLockedRef.current) return;
    const generation = epoch.current;
    if (reviewRead.current?.selected === selected && reviewRead.current.generation === generation) return;
    const attempt = { selected, generation }; reviewRead.current = attempt;
    setBusy(true);
    try {
      const value = await mutation('/workday-reviews', { draft_id: saved.id, expected_revision: saved.revision });
      if (!alive.current || generation !== epoch.current) return;
      if (!value || Object.keys(value).sort().join() !== 'blockers,classifications_required,draft,draft_id,expires_at,final_end,operation_expires_at,operation_id,revision,supported_types,unknowns' || !uuid(value.operation_id) || value.draft_id !== saved.id || value.revision !== saved.revision || canonical(value.draft) !== canonical(saved.draft)
        || Date.parse(value.operation_expires_at) !== Date.parse(saved.expires_at) || !live(value.operation_expires_at)
        || !Array.isArray(value.blockers) || !value.blockers.every((v: any) => typeof v === 'string') || !Array.isArray(value.unknowns) || value.unknowns.length > 3000
        || !value.unknowns.every((v: any) => v && typeof v.id === 'string' && v.id.length <= 200 && typeof v.label === 'string') || new Set(value.unknowns.map((v: any) => v.id)).size !== value.unknowns.length
        || !Array.isArray(value.classifications_required) || !value.classifications_required.every((id: any) => saved.draft.activities.some(a => a.id === id)) || new Set(value.classifications_required).size !== value.classifications_required.length
        || canonical([...value.classifications_required].sort()) !== canonical(saved.draft.activities.filter(activity => !supportedTypes.includes(activity.type ?? '')).map(activity => activity.id).sort())
        || !Array.isArray(value.supported_types) || canonical([...value.supported_types].sort()) !== canonical([...supportedTypes].sort())
        || !validCandidates(value)
        || (value.blockers.length === 0 && (Date.parse(value.final_end) !== finalEnd(saved.draft) || Date.parse(value.expires_at) - Date.parse(value.final_end) !== 7 * 86400000 || !live(value.expires_at)))) throw Error();
      setReview(value); setAcks([]); setClasses({}); setMessage('Gjennomgå den lagrede versjonen og beslutningene som er oppført.'); title.current?.focus();
    } catch (error) { if (alive.current && generation === epoch.current) failure(error); }
    finally { if (reviewRead.current === attempt) { reviewRead.current = null; if (alive.current) setBusy(false); } }
  }
  async function accept(value: any, decisions: Decisions, generation: number, authorityEpoch: number) {
    if (!review || !validPlan(value) || value.source_draft_id !== review.draft_id || value.source_revision !== review.revision
      || canonical(value.draft) !== canonical(review.draft) || Date.parse(value.expires_at) > Date.parse(review.expires_at!)
      || canonical(value.unknowns) !== canonical(relevantUnknowns(review, decisions.classifications))
      || canonical([...value.acknowledgements].sort()) !== canonical([...decisions.acknowledgements].sort()) || canonical(value.classifications) !== canonical(decisions.classifications)) throw Error();
    const latest = await request('/workdays/' + value.id);
    if (!validPlan(latest) || latest.id !== value.id || latest.source_draft_id !== value.source_draft_id || latest.source_revision !== value.source_revision
      || canonical(latest.draft) !== canonical(value.draft) || canonical(latest.classifications) !== canonical(value.classifications)
      || canonical(latest.acknowledgements) !== canonical(value.acknowledgements) || Date.parse(latest.expires_at) > Date.parse(value.expires_at)) throw Error();
    if (!alive.current || generation !== reading.current || authorityEpoch !== epoch.current || deletionRef.current || busLockedRef.current) return false;
    setPlan(latest); setActivityOpen(false); showPlan(); setPending(null); setReview(null); setMessage('Planen er bekreftet. Lagret plan er hentet.'); title.current?.focus();
    return true;
  }
  async function send(lookup = false) {
    if (!review || busLockedRef.current) return;
    const generation = reading.current, authorityEpoch = epoch.current;
    const decisions = pending ?? { operation_id: review.operation_id, expected_revision: review.revision, acknowledgements: [...acks].sort(), classifications: { ...classes } };
    let checking = false;
    setPending(decisions); setBusy(true); setMessage('Bekreftelse er uavklart til svaret er kontrollert.');
    try {
      let value;
      if (lookup || pending) {
        const status = await request('/workday-operations/' + decisions.operation_id);
        if (!status || Object.keys(status).sort().join() !== 'result,state') throw Error();
        if (status.state === 'accepted') { checking = true; if (await accept(status.result, decisions, generation, authorityEpoch)) await list(false, true); return; }
        if (status.state !== 'pending' || status.result !== null) throw Error();
        if (lookup) { setMessage('Serveren har ikke registrert en bekreftelse for forsøket. Beslutningene er beholdt. Prøv samme bekreftelse igjen.'); return; }
      }
      value = await mutation('/drafts/' + review.draft_id + '/confirm', decisions);
      if (!alive.current || generation !== reading.current || deletionRef.current || busLockedRef.current) return;
      if (lookup) {
        if (!value || Object.keys(value).sort().join() !== 'result,state') throw Error();
        if (value.state === 'pending' && value.result === null) { setMessage('Forsøket er ikke akseptert. Prøv samme bekreftelse igjen.'); return; }
        if (value?.state !== 'accepted') throw Error();
        if (!await accept(value.result, decisions, generation, authorityEpoch)) return;
      } else {
        checking = true;
        const operation = await request('/workday-operations/' + decisions.operation_id);
        if (!alive.current || generation !== reading.current || deletionRef.current || busLockedRef.current) return;
        if (!operation || Object.keys(operation).sort().join() !== 'result,state' || operation.state !== 'accepted' || canonical(operation.result) !== canonical(value)) throw Error();
        if (!await accept(value, decisions, generation, authorityEpoch)) return;
      }
      await list(false, true);
    } catch (error: any) {
      if (!alive.current || generation !== reading.current || deletionRef.current || busLockedRef.current) return;
      if (error?.status === 401 || !checking && !lookup && typeof error.apiDetail === 'string' && [
        'Tilgangen ble avvist.', 'Bekreftelsesforsøket er utløpt.', 'Utkastet, forsøket eller planens frist er utløpt.',
        'Bekreftelsesforsøket gjelder en annen versjon.', 'Bekreftelsesforsøket har andre beslutninger.',
        'Utkastet er endret. Gjennomgå den lagrede versjonen på nytt.', 'Utkastet har allerede en bekreftet plan. Åpne planen.',
        'Rett blokkeringene og klassifiser alle ukjente aktivitetstyper.', 'Alle oppførte ukjente opplysninger må gjennomgås og godtas for denne versjonen.',
        'Kontroller feltene.', 'Forespørselen er for stor.',
      ].includes(error.apiDetail)) { setPending(null); setReview(null); failure(error); }
      else setMessage('Bekreftelsen er uavklart. Behold siden åpen og kontroller eller prøv samme bekreftelse igjen.');
    } finally { if (alive.current && generation === reading.current) setBusy(false); }
  }
  async function reopen(id: string) {
    if (busLockedRef.current) return;
    const openingScreen = presentation.current.version;
    const generation = ++reading.current;
    const read = { id, generation }; planRead.current = read;
    setBusy(true);
    try { const value = await request('/workdays/' + id); if (!alive.current || generation !== reading.current || openingScreen !== presentation.current.version || deletionRef.current || busLockedRef.current) return; const summary = items.find(item => item.id === id); if (!validPlan(value) || value.id !== id || !summary || value.source_draft_id !== summary.source_draft_id || value.source_revision !== summary.source_revision || value.draft.service_date !== summary.service_date || Date.parse(value.expires_at) > Date.parse(summary.expires_at)) throw Error(); setPlanOpen(current => current + 1); setPlan(value); setActivityOpen(false); showPlan(); setMessage('Bekreftet plan åpnet. Fristen er uendret.'); title.current?.focus(); }
    catch (error: any) { if (alive.current && generation === reading.current && !deletionRef.current) { if ([404, 410].includes(error?.status)) setPlan(current => current?.id === id ? null : current); failure(error); } }
    finally { if (planRead.current === read) planRead.current = null; if (alive.current && generation === reading.current) setBusy(false); }
  }
  async function remove(lookup = false) {
    if (sendingDeletion.current || suspended || busLockedRef.current) return;
    const retry = !!deletionRef.current;
    let operation = deletionRef.current;
    if (!operation) {
      if (!plan || !window.confirm('Slette denne bekreftede planen? Dette kan ikke angres. Kildeutkastet beholdes.')) return;
      operation = { id: plan.id, expires_at: plan.expires_at, body: { operation_id: crypto.randomUUID(), source_revision: plan.source_revision } };
      deletionRef.current = operation; setDeleting(operation); reading.current++; epoch.current++;
    }
    sendingDeletion.current = true; setBusy(true); setMessage('Slettingen er uavklart til svaret er kontrollert.');
    try {
      const original = operation;
      const status = () => request('/workday-deletions/' + original.body.operation_id);
      const mutate = () => mutation('/workdays/' + original.id + '/delete', original.body);
      const authorize = async () => {
        const current = await request('/workdays/' + original.id);
        if (!validPlan(current) || current.id !== original.id || current.source_revision !== original.body.source_revision || Date.parse(current.expires_at) > Date.parse(original.expires_at)
          || !alive.current || deletionRef.current !== original) throw Error();
      };
      const value = lookup ? await status() : retry ? await recoverOperation(status, authorize, mutate) : await mutate();
      if (!alive.current || deletionRef.current !== operation) return;
      if (!value || Object.keys(value).sort().join() !== 'deleted_id,operation_id,source_revision' || value.deleted_id !== operation.id || value.operation_id !== operation.body.operation_id || value.source_revision !== operation.body.source_revision || !live(operation.expires_at)) throw Error();
      // Guarded reads revalidate the displayed session after receiving their
      // body, including when a notification was missed during a mutation.
      if (!lookup && canonical(await request('/workday-deletions/' + operation.body.operation_id)) !== canonical(value)) throw Error();
      if (!alive.current || deletionRef.current !== operation || !live(operation.expires_at)) return;
      reading.current++; epoch.current++; deletionRef.current = null; setDeleting(null); setPlan(null); setReview(null); setPending(null); setItems(current => current.filter(item => item.id !== operation.id)); showPreparation();
      setMessage('Den bekreftede planen er slettet. Kildeutkastet beholdes. Et utkast som allerede er brukt til bekreftelse krever et nytt, separat utkast for en ny plan.'); title.current?.focus();
    } catch (error: any) {
      if (!alive.current || deletionRef.current !== operation) return;
      if (error?.status === 401) { expired(); return; }
      // Transport status alone cannot distinguish a private denial from an
      // HTML proxy response after acceptance. Retain the original identity.
      setMessage([409, 410, 422].includes(error?.status) ? 'Tilgangen, planversjonen eller fristen ble avvist. Slettingen er uavklart; behold siden åpen og kontroller samme forsøk.' : 'Slettingen er uavklart. Behold siden åpen og kontroller eller prøv samme sletting igjen.');
    } finally { sendingDeletion.current = false; if (alive.current) setBusy(false); }
  }
  async function abandonMissingPlan() {
    if (!plan || !busLockedRef.current || suspended || busy || deletionRef.current || pending) return;
    const original = plan;
    const generation = ++reading.current;
    setBusy(true);
    const absent = async () => {
      let missing = false;
      try { await request('/workdays/' + original.id); }
      catch (error: any) {
        if (error?.status === 404 && error.apiDetail === 'Tilgangen ble avvist.'
          || error?.status === 410 && error.apiDetail === 'Planen er utløpt.') missing = true;
        else throw error;
      }
      if (!missing) throw Error();
      // An error response does not receive the wrapper's successful-body
      // postvalidation. Verify the same displayed session after each denial.
      await request('/auth/session');
      if (!alive.current || generation !== reading.current || !live(original.expires_at)) throw Error();
    };
    try {
      await absent();
      if (!window.confirm('Planen finnes ikke lenger eller er utløpt. Oppgi uavklarte forsøk og forkast lokale endringer for denne planen? Lagring blir ikke bekreftet. Avviksregisteret beholdes.')) return;
      await absent();
      reading.current++; epoch.current++;
      setPlan(null); setActivityOpen(false); setNoticeReaderOpen(false);
      // Child unmounts release their locks; keep independent account notices.
      setItems(current => current.filter(item => item.id !== original.id));
      showPreparation(); setMessage('Den bortfalte planen er lukket. Lokale planforsøk er oppgitt uten bekreftet lagring. Avviksregisteret er beholdt.');
    } catch (error: any) {
      if (alive.current && generation === reading.current) {
        if (error?.status === 401) expired();
        else setMessage('Bortfalt plan kunne ikke bekreftes. Uavklart forsøk og lokale endringer er beholdt. Ingen lagring er bekreftet.');
      }
    } finally { if (alive.current) setBusy(false); }
  }
  return <section className="private-confirmation" aria-label="Bekreft plan" aria-busy={busy}>
    <p hidden={screen === 'plan' && activityOpen && /^(Bekreftet plan åpnet|Planen er bekreftet|Planlisten er oppdatert)/.test(message)} role="status" aria-label="Bekreftelsesstatus">{message}</p>
    <div hidden={screen !== 'approval' || notices.screen !== 'day'}>
    <h2 ref={title} tabIndex={-1}>Gjennomgå og bekreft</h2>
    <p>Bekreftelse lagrer en egen plan. Planen utløper sju dager etter siste aktivitetsslutt. Gjennomgang gjelder bare den lagrede versjonen.</p>
    <p>Et utkast som allerede er brukt til bekreftelse krever et nytt, separat utkast for en ny plan.</p>
    {!review && <button disabled={!saved || !clean || busy || !!pending || !!deleting || busLocked || suspended} onClick={() => void begin()}>Prøv gjennomgang på nytt</button>}
    {!clean && <p>Lagre endringene før gjennomgang. Endringer opphever tidligere gjennomgang.</p>}
    {review && <section aria-label="Gjennomgått versjon"><h3>Lagret versjon {review.revision}</h3><p>Siste aktivitetsslutt: {review.final_end ? date(review.final_end) : 'Uavklart'}. Planen utløper: {review.expires_at ? date(review.expires_at) : 'Uavklart'}.</p>
      {review.blockers.length > 0 && <div className="import-warning"><h4>Rett før bekreftelse</h4><ul>{review.blockers.map((v, i) => <li key={i}>{v}</li>)}</ul></div>}
      <p>Tjenestedato {review.draft.service_date ?? 'ukjent'} · vognløp {review.draft.vehicle_duty ?? 'ukjent'} · buss/vogn {review.draft.physical_bus ?? 'ukjent'} · {review.draft.activities.length} aktiviteter.</p><details><summary>Vis alle opplysninger i lagret versjon</summary><Facts content={review.draft} classifications={classes} /></details>
      <p>Godta manglende turinformasjon og gjeldende usikkerhet for passasjerturer der de er oppført nedenfor. Ukjent aktivitetstype må klassifiseres.</p>
      <fieldset disabled={busy || !!pending || suspended}><legend>Beslutninger for versjon {review.revision}</legend>
        {review.classifications_required.map(id => { const index = review.draft.activities.findIndex(a => a.id === id), activity = review.draft.activities[index]; return <div key={id} className="classification-decision"><p id={'classification-context-' + id}>Opprinnelig kode: {displayFact('raw_code', activity.raw_code) ?? 'Ukjent'}. Oppgitt type: {displayFact('type', activity.type) ?? 'Ukjent'}. Start: {activity.start ? date(activity.start) : 'Ukjent dato og tid'} · slutt: {activity.end ? date(activity.end) : 'Ukjent dato og tid'}. Fra: {displayFact('from_place', activity.from_place) ?? 'Ukjent'} · til: {displayFact('to_place', activity.to_place) ?? 'Ukjent'}.</p><label>Klassifisering aktivitet {index + 1}<select aria-describedby={'classification-context-' + id} value={classes[id] ?? ''} onChange={e => { const next = { ...classes, [id]: e.target.value }; setClasses(next); const allowed = new Set(relevantUnknowns(review, next).map(item => item.id)); setAcks(current => current.filter(id => allowed.has(id))); }}><option value="">Velg eksplisitt type</option>{review.supported_types.map(kind => <option key={kind} value={kind}>{typeLabels[kind]}</option>)}</select></label></div>; })}
        {visibleUnknowns.map(item => <label className="confirmation-ack" key={item.id}><input type="checkbox" checked={acks.includes(item.id)} onChange={e => setAcks(current => e.target.checked ? [...current, item.id] : current.filter(id => id !== item.id))} />Jeg har gjennomgått og godtar: {item.label}</label>)}
      </fieldset>
      {!pending && <div className="controls"><button disabled={busy || busLocked || suspended || review.blockers.length > 0 || acks.length !== visibleUnknowns.length || review.classifications_required.some(id => !classes[id])} onClick={() => void send()}>Bekreft gjennomgått plan</button><button disabled={busy} onClick={() => { setReview(null); setAcks([]); setClasses({}); setMessage('Gjennomgangen er avbrutt. Utkastet er uendret.'); }}>Avbryt gjennomgang</button></div>}
    </section>}
    {pending && <div className="controls"><button disabled={busy || busLocked || suspended} onClick={() => void send()}>Prøv samme bekreftelse igjen</button><button disabled={busy || busLocked || suspended} onClick={() => void send(true)}>Kontroller bekreftelsen</button></div>}
    </div>
    <div hidden={screen === 'plan' && noticeReaderOpen}><NoticeScreens visible={screen !== 'plan' || !noticeReaderOpen} notices={notices} serviceDate={plan?.draft.service_date ?? null} back={() => notices.navigate('day')} /></div>
    {(!plan || screen !== 'plan') && notices.screen === 'day' && <button id="notice-entry-preparation" disabled={suspended} onClick={notices.open}>Manuelt vedlikeholdte avvik</button>}
    {plan && <PrivateWorkdayView validPlan={validPlan} historicalDetails={<Facts historical content={plan.draft} classifications={plan.classifications} />} busy={busy} key={plan.id + ':' + planOpen} plan={plan} hidden={screen !== 'plan'} activityOpen={activityOpen} setActivityOpen={setActivityOpen} request={request} mutation={mutation} suspended={suspended || !!deleting || !!pending} expired={expired} planAvailable={planAvailable} dayNavigationLocked={dayNavigationLocked} busLocked={busLocked} guardBus={guardBus} guardSelection={guardSelection} guardStart={guardStart} guardOutcome={guardOutcome} notices={notices} readerChanged={setNoticeReaderOpen} busAvailability={busAvailability} selectionAvailability={selectionAvailability} startAvailability={startAvailability} remove={() => void remove()} closeView={() => { setPlan(null); showPreparation(); }} showPreparation={showPreparation} shorten={value => setPlan(current => current?.id === plan.id && Date.parse(value) < Date.parse(current.expires_at) ? { ...current, expires_at: value } : current)} />}
    {plan && screen === 'plan' && busLocked && <button disabled={busy || suspended || !!deleting || !!pending} onClick={() => void abandonMissingPlan()}>Oppgi uavklart forsøk og lukk planen</button>}
    <div hidden={screen !== 'plan'}>{deleting && <div className="controls"><button disabled={busy || suspended} onClick={() => void remove()}>Prøv samme sletting igjen</button><button disabled={busy || suspended} onClick={() => void remove(true)}>Kontroller slettingen</button></div>}</div>
    <div hidden={screen !== 'upload' || notices.screen !== 'day'}><h3>Mine bekreftede planer</h3><button disabled={busy || !!pending || !!deleting || busLocked || suspended} onClick={() => void list()}>Oppdater planlisten</button>
    {items.length === 0 && <p>Ingen planer er lastet.</p>}<ul>{items.map(item => <li key={item.id}><button disabled={busy || !!pending || !!deleting || busLocked || suspended} onClick={() => void reopen(item.id)}>Åpne plan {item.service_date ?? 'ukjent dato'} · versjon {item.source_revision}</button> Utløper {date(item.expires_at)}</li>)}</ul>
    {cursor && <button disabled={busy || !!pending || !!deleting || busLocked || suspended} onClick={() => void list(true)}>Last flere planer</button>}
    </div>
  </section>;
}
