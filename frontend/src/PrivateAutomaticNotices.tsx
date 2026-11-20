import { useEffect, useRef, useState } from 'react';
import { osloDateTime } from './dayOverview';
import type { Plan } from './PrivateConfirmation';

const groups = {
  'possible-relevance': 'Mulig relevans',
  'review': 'Til gjennomgang',
  'broad-context': 'Overordnet informasjon',
  'outside-scope': 'Utenfor omfanget',
};
const reasons: Record<string, string> = {
  'exact-line-planned-overlap': 'Kvalifisert linje og overlapp med planlagt tid.',
  'uncertain-validity': 'Gyldighetstiden er ukjent eller ufullstendig.',
  'open-ended-validity': 'Kilden oppgir ingen slutt for minst én gyldighetsperiode.',
  'unresolved-qualifiers': 'Avgrensning etter stopp, retning, rute eller tur må vurderes.',
  'source-closed': 'Kilden har eksplisitt avsluttet sin melding.',
  'source-status-unknown': 'Kilden oppgir ingen kvalifisert status.',
  'validity-expired': 'De oppgitte gyldighetsperiodene har utløpt.',
  'other-mode': 'Kilden oppgir en annen transportform enn buss.',
  'stop-scope-unverified': 'Meldingen gjelder stopp. Koblingen til planens stopp er uavklart.',
  'explicit-broad-scope': 'Kilden oppgir uttrykkelig et bredt omfang.',
  'scope-unresolved': 'Kilden gir ingen kvalifisert linjekobling eller kjent bredt omfang.',
  'authority-unverified': 'Oppgitt myndighet eller operatør samsvarer ikke med den kvalifiserte koblingen.',
  'line-binding-unavailable': 'Linje-ID-en har ingen kvalifisert kobling for forsøket.',
  'no-matching-printed-line': 'Planen har ingen eksakt samsvarende linjebetegnelse.',
  'uncertain-planned-time': 'En mulig planaktivitet har uavklart tid.',
  'no-dated-binding': 'Linjekoblingen er ikke kvalifisert for denne datoen.',
  'no-planned-overlap': 'Ingen gyldighetsperiode overlapper den kvalifiserte aktiviteten.',
  'retained-private-evidence': 'Tidligere gjennomgang er beholdt med grunnlaget som ble brukt.',
};
const actions = {
  'unresolved': 'La stå uavklart', 'associate': 'Knytt til aktivitet', 'day-context': 'Behold som dagskontekst', 'dismiss': 'Legg bort for denne planen',
};
const decisions: Record<keyof typeof actions, string> = {
  unresolved: 'Uavklart', associate: 'Knyttet til aktivitet', 'day-context': 'Beholdt som dagskontekst', dismiss: 'Lagt bort for denne planen',
};
const healthLabels = {
  'never-qualified': 'Ingen komplett innsamling ennå', collecting: 'Innsamling pågår', complete: 'Komplett innsamling for TRO',
  partial: 'Delvis innsamling. Dagens dekning er ukjent.', unavailable: 'Kilden er utilgjengelig. Dagens dekning er ukjent.',
};
const observations = {
  seen: 'Denne revisjonen ble sett i siste komplette innsamling', 'seen-partial': 'Denne revisjonen ble sett i en delvis innsamling',
  'other-revision-seen': 'En annen revisjon av meldingen ble sett i siste komplette innsamling',
  'other-revision-seen-partial': 'En annen revisjon av meldingen ble sett i en delvis innsamling',
  unknown: 'Observasjon er uavklart i det siste forsøket', 'not-seen': 'Meldingen ble ikke sett i siste komplette innsamling',
};

type Action = keyof typeof actions;
type Group = keyof typeof groups;
type Selector = { kind: string; value: string | null; children: Selector[] };
type Localized = { text: string; language: string | null };
type Evidence = {
  participant: string; situation: string; version: string | null; publisher_updated_at: string | null;
  source_created_at: string | null; progress: string | null; source_type: string | null;
  report_type: string | null; severity: string | null;
  summary: Localized[]; description: Localized[]; advice: Localized[]; links: string[];
  windows: { start: string | null; end: string | null }[]; affects: Selector[];
};
type Source = {
  revision: string; basis: string; observation: keyof typeof observations; content: Evidence;
  first_seen: string; last_seen: string; identity_last_seen: string; fetched_at: string; response_at: string; conflict_count: number;
  conflicts: { revision: string; content: Evidence; last_seen: string }[];
};
type Choice = { action: Action; activity_id: string | null; reason: string | null; manual_notice_id: string | null };
type Decision = Choice & { plan_revision: number; source_basis: string; source_revision: string; decided_at: string;
  evidence: Evidence; source_response_at: string; source_observed_at: string; source_generation: string | null; source_conflicts: number };
type Manual = { id: string; title: string; summary: string | null; description: string | null; source_note: string | null;
  source_url: string | null; status: string; source_updated_at: string | null; checked_at: string | null; ended_at: string | null };
type Entry = { situation: string; classification: Group; reasons: string[]; review_revision: number; decision: Decision | null; validity_expired: boolean;
  needs_reassessment: boolean; source: Source | null; manual: Manual | null;
  matches: { id: string; line: string; line_ref: string; authority_ref: string; dates: string[] }[] };
type Page = { workday_id: string; expires_at: string; plan_revision: number; server_now: string; total: number;
  entries: Entry[]; page_counts: Partial<Record<Group, number>>; next_cursor: string | null;
  lifecycle: { revision: number; state: 'unstarted' | 'active' | 'ended' | 'aborted' };
  health: { status: keyof typeof healthLabels; old: boolean; failure: string | null; generation: string | null; evidence_kind: 'provider' | 'synthetic';
    attempt_at: string | null; result_at: string | null; baseline_at: string | null; synchronized_at: string | null;
    response_at: string | null; baseline_count: number | null; attempt_count: number; attempt_pages: number } };
type ExpectedBasis = { situation: string; expected_revision: number; expected_plan_revision: number;
  expected_lifecycle_revision: number; expected_source_basis: string };
type Operation = Choice & ExpectedBasis & { operation_id: string };
type ReviewBasis = { expected: ExpectedBasis; key: string; evidence: Evidence | null };
type Proposal = { basis: ReviewBasis; choice: Choice; conflict: boolean };

const empty: Choice = { action: 'unresolved', activity_id: null, reason: null, manual_notice_id: null };
const isString = (s: unknown): s is string => typeof s === 'string';
const nullable = (s: unknown) => s === null || isString(s);
const count = (n: unknown) => typeof n === 'number' && Number.isSafeInteger(n) && n >= 0;
const digest = (s: unknown) => isString(s) && /^[0-9a-f]{64}$/.test(s);
const uuid = (s: unknown): s is string => isString(s) && /^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/.test(s);
const timestamp = (s: unknown): s is string => isString(s) && Number.isFinite(Date.parse(s));
const optionalTime = (s: unknown) => s === null || timestamp(s);
const situationPrefix = 'TRO:SituationNumber:';
const itemKey = (s: unknown) => isString(s) && s.startsWith(situationPrefix) && s.length > situationPrefix.length &&
  Array.from(s).length <= 200 && !/[\0\p{Surrogate}]/u.test(s);
const own = (v: object, key: unknown): boolean => isString(key) && Object.hasOwn(v, key);
const safeUrl = (s: string) => {
  try { const url = new URL(s); return ['https:', 'http:'].includes(url.protocol) && !url.username && !url.password ? s : undefined; }
  catch { return undefined; }
};

function evidence(value: any, situation: string): value is Evidence {
  function selector(item: any, depth: number): boolean {
    return depth <= 32 && item && isString(item.kind) && nullable(item.value) && Array.isArray(item.children) && item.children.every((child: any) => selector(child, depth + 1));
  }
  return value && value.participant === 'TRO' && value.situation === situation &&
    ['version', 'publisher_updated_at', 'source_created_at', 'progress', 'source_type', 'report_type', 'severity'].every(key => nullable(value[key])) &&
    ['summary', 'description', 'advice'].every(key => Array.isArray(value[key]) && value[key].every((item: any) => item && isString(item.text) && nullable(item.language))) &&
    Array.isArray(value.links) && value.links.every((link: unknown) => isString(link) && safeUrl(link)) &&
    Array.isArray(value.windows) && value.windows.every((window: any) => window && nullable(window.start) && nullable(window.end)) &&
    Array.isArray(value.affects) && value.affects.every((item: any) => selector(item, 1));
}

function decision(value: any, situation: string): value is Decision {
  return value && own(actions, value.action) && nullable(value.reason) && (value.activity_id === null || uuid(value.activity_id)) &&
    (value.manual_notice_id === null || uuid(value.manual_notice_id)) && count(value.plan_revision) && digest(value.source_basis) &&
    digest(value.source_revision) && timestamp(value.decided_at) && evidence(value.evidence, situation) &&
    timestamp(value.source_response_at) && timestamp(value.source_observed_at) &&
    (value.source_generation === null || uuid(value.source_generation)) && count(value.source_conflicts);
}

function validPage(value: any, plan: Plan): value is Page {
  const h = value?.health, stage = value?.lifecycle;
  return value?.workday_id === plan.id && value.plan_revision === plan.source_revision && timestamp(value.expires_at) &&
    Date.parse(value.expires_at) <= Date.parse(plan.expires_at) && timestamp(value.server_now) &&
    Date.parse(value.expires_at) > Date.parse(value.server_now) && count(value.total) && (value.next_cursor === null || itemKey(value.next_cursor)) &&
    stage && ['unstarted', 'active', 'ended', 'aborted'].includes(stage.state) && count(stage.revision) &&
    h && own(healthLabels, h.status) && h.provider === 'Entur' && h.dataset === 'TRO' && h.stream === 'SIRI-SX' && ['provider', 'synthetic'].includes(h.evidence_kind) &&
    typeof h.old === 'boolean' && nullable(h.failure) && (h.generation === null || uuid(h.generation)) &&
    ['attempt_at', 'result_at', 'response_at', 'baseline_at', 'synchronized_at'].every(x => optionalTime(h[x])) &&
    (h.baseline_count === null || count(h.baseline_count)) && count(h.attempt_count) && count(h.attempt_pages) && value.page_counts &&
    Object.entries(value.page_counts).every(([key, n]) => own(groups, key) && count(n)) && Array.isArray(value.entries) && value.entries.length <= 10 &&
    value.entries.every((row: any) => {
      if (!row || !itemKey(row.situation) || !own(groups, row.classification) || !Array.isArray(row.reasons) || !row.reasons.every(isString) ||
        !count(row.review_revision) || typeof row.needs_reassessment !== 'boolean' || typeof row.validity_expired !== 'boolean' ||
        !(row.decision === null || decision(row.decision, row.situation)) ||
        !Array.isArray(row.matches) || !row.matches.every((match: any) => match && uuid(match.id) && isString(match.line) && isString(match.line_ref) && isString(match.authority_ref) && Array.isArray(match.dates) && match.dates.every(isString))) return false;
      const s = row.source, m = row.manual;
      return (s === null || s && own(observations, s.observation) && digest(s.revision) && digest(s.basis) && evidence(s.content, row.situation) &&
        [s.first_seen, s.last_seen, s.identity_last_seen, s.fetched_at, s.response_at].every(timestamp) && count(s.conflict_count) && Array.isArray(s.conflicts) &&
        s.conflicts.every((item: any) => item && digest(item.revision) && timestamp(item.last_seen) && evidence(item.content, row.situation))) &&
        (m === null || m && uuid(m.id) && isString(m.title) && isString(m.status) &&
          ['summary', 'description', 'source_note', 'source_url'].every(key => nullable(m[key])) &&
          ['source_updated_at', 'checked_at', 'ended_at'].every(key => optionalTime(m[key])));
    });
}

function reviewBasis(page: Page, item: Entry): ReviewBasis | null {
  const source = item.source?.basis ?? item.decision?.source_basis;
  if (!source) return null;
  const expected = { situation: item.situation, expected_revision: item.review_revision, expected_plan_revision: page.plan_revision,
    expected_lifecycle_revision: page.lifecycle.revision, expected_source_basis: source };
  const key = JSON.stringify([page.workday_id, expected, page.lifecycle.state, Date.parse(page.expires_at),
    item.source?.observation ?? null, item.classification, item.validity_expired, page.health.old]);
  return { expected, key, evidence: item.source?.content ?? item.decision?.evidence ?? null };
}

function confirmed(value: any, op: Operation, workday: string) {
  return value?.workday_id === workday && value.operation_id === op.operation_id && value.situation === op.situation &&
    value.revision === op.expected_revision + 1 && decision(value.decision, op.situation) &&
    value.decision.plan_revision === op.expected_plan_revision && value.decision.source_basis === op.expected_source_basis &&
    value.decision.action === op.action && value.decision.activity_id === op.activity_id &&
    value.decision.reason === op.reason && value.decision.manual_notice_id === op.manual_notice_id;
}

const showTime = (value: string | null) => timestamp(value) ? osloDateTime(value) : value || 'Ukjent';
const formatActivity = (activity: Plan['draft']['activities'][number], i: number) =>
  [`Aktivitet ${i + 1}`, activity.line && `Linje ${activity.line}`, activity.trip && `tur ${activity.trip}`, activity.start && osloDateTime(activity.start), activity.to_place].filter(Boolean).join(' · ');

function Selectors({ nodes }: { nodes: Selector[] }) {
  return <ul>{nodes.map((node, index) => <li key={index}>{node.kind}{node.value && <> · {node.value}</>}{node.children.length > 0 && <Selectors nodes={node.children} />}</li>)}</ul>;
}

function SourceFacts({ value }: { value: Evidence }) {
  return <div className="automatic-notice-facts">
    <p>{value.participant} · {value.situation}</p>
    <dl><dt>Kildens status</dt><dd>{value.progress === 'open' ? 'Åpen' : value.progress === 'closed' ? 'Avsluttet av kilden' : value.progress ?? 'Ukjent'}</dd>
      <dt>Kildens versjon</dt><dd>{value.version ?? 'Ukjent'}</dd><dt>Opprettet hos kilden</dt><dd>{value.source_created_at ?? 'Ukjent'}</dd>
      <dt>Oppdatert hos kilden</dt><dd>{value.publisher_updated_at ?? 'Ukjent'}</dd></dl>
    {(['summary', 'description', 'advice'] as const).flatMap(field => value[field].map((item, index) => <p key={field + index}>{item.text}</p>))}
    {value.windows.length ? <ul aria-label="Gyldighetsperioder">{value.windows.map((window, index) => <li key={index}>{window.start ?? 'Ukjent start'} – {window.end ?? 'Ingen oppgitt slutt'}</li>)}</ul> : <p>Gyldighetsperiode er ukjent.</p>}
    {value.links.length ? <ul>{value.links.map((link, index) => <li key={index}><a href={safeUrl(link)} target="_blank" rel="noopener noreferrer">Åpne kildelenke {value.links.length > 1 ? index + 1 : ''}</a></li>)}</ul> : <p>Ingen lenke til selve meldingen er oppgitt.</p>}
    {!!value.affects.length && <details><summary>Berørte linjer, steder og vilkår</summary><Selectors nodes={value.affects} /></details>}
  </div>;
}

function ManualFacts({ manual }: { manual: Manual }) {
  return <div className="automatic-notice-facts"><h4>Lenket manuelt avvik</h4><p>{manual.title}</p><p>{manual.summary}</p><p>{manual.description}</p><p>{manual.source_note}</p>
    <dl><dt>Oppdatert hos manuell kilde</dt><dd>{showTime(manual.source_updated_at)}</dd><dt>Sist kontrollert manuelt</dt><dd>{showTime(manual.checked_at)}</dd>
      <dt>Status</dt><dd>{manual.status === 'ended_manually' ? 'Avsluttet manuelt' : 'Registrert'}</dd><dt>Avsluttet manuelt</dt><dd>{showTime(manual.ended_at)}</dd></dl>
    {manual.source_url && safeUrl(manual.source_url) && <a href={manual.source_url} target="_blank" rel="noopener noreferrer">Åpne manuell kilde</a>}
  </div>;
}

type Props = { plan: Plan; open: boolean; available: boolean; suspended: boolean; back: () => void; expired: () => void;
  request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>; shorten: (value: string) => void };

export function PrivateAutomaticNotices(props: Props) {
  const { plan, open, available, suspended, request, mutation } = props;
  const path = `/workdays/${plan.id}/automatic-notices`;
  const [page, setPage] = useState<Page | null>(null);
  const [cursors, setCursors] = useState<(string | null)[]>([null]);
  const [selected, setSelected] = useState<string | null>(null);
  const [proposal, setProposal] = useState<Proposal | null>(null);
  const [manuals, setManuals] = useState<{ id: string; title: string }[]>([]);
  const [message, setMessage] = useState('');
  const [pending, setPending] = useState<Operation | null>(null);
  const [loading, setLoading] = useState(false);
  const [writing, setWriting] = useState(false);
  const title = useRef<HTMLHeadingElement>(null);
  const sequence = useRef(0);
  const pendingRef = useRef<Operation | null>(null);
  const writeRef = useRef(false);
  const screen = useRef({ open, suspended, available, id: plan.id });
  screen.current = { open, suspended, available, id: plan.id };
  const shown = open && available && !suspended;
  const live = () => screen.current.id === plan.id && screen.current.open && !screen.current.suspended && screen.current.available;
  const row = page?.entries.find(item => item.situation === selected);
  const displayedBasis = page && row ? reviewBasis(page, row) : null;
  const choice = proposal?.choice ?? empty;
  const changed = !!proposal && (proposal.conflict || proposal.basis.key !== displayedBasis?.key);
  const activityLabels = new Map(plan.draft.activities.map((item, index) => [item.id, formatActivity(item, index)]));

  async function load(cursor = cursors.at(-1) ?? null) {
    if (!live()) return;
    const generation = ++sequence.current;
    setLoading(true);
    try {
      const value = await request(path + (cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''));
      if (generation !== sequence.current || !live()) return;
      if (!validPage(value, plan)) throw Error();
      props.shorten(value.expires_at);
      setPage(value);
      setProposal(current => {
        if (!current || current.conflict) return current;
        const item = value.entries.find(entry => entry.situation === current.basis.expected.situation);
        return item && reviewBasis(value, item)?.key === current.basis.key ? current : { ...current, conflict: true };
      });
    } catch (error: any) {
      if (generation !== sequence.current || !live()) return;
      setPage(null);
      if (error?.status === 410) props.expired();
      setMessage([401, 403, 404, 410].includes(error?.status) ? 'Tilgangen til planen må kontrolleres.' : 'Automatiske avvik kunne ikke hentes.');
    } finally { if (generation === sequence.current) setLoading(false); }
  }

  useEffect(() => {
    if (shown) { title.current?.focus(); void load(); }
    else { sequence.current++; setPage(null); setManuals([]); }
    return () => { sequence.current++; };
  }, [shown, plan.id]);

  function inspect(item: Entry) {
    setSelected(item.situation);
    const basis = page ? reviewBasis(page, item) : null;
    const saved = item.source ? item.decision : null;
    setProposal(basis ? { basis, conflict: false, choice: saved ? { action: saved.action, activity_id: saved.activity_id,
      reason: saved.reason, manual_notice_id: saved.manual_notice_id } : empty } : null);
    setMessage('');
  }

  function setChoice(choice: Choice) {
    setProposal(current => current && { ...current, choice });
  }

  function confirmComparison() {
    if (!displayedBasis || !proposal || loading || pending || writing) return;
    setProposal({ ...proposal, basis: displayedBasis, conflict: false });
    setMessage('Forslaget er vurdert mot oppdaterte opplysninger.');
  }

  async function manualChoices() {
    const generation = sequence.current;
    const records: typeof manuals = [];
    let cursor: string | null = null;
    try {
      for (let i = 0; i < 5; i++) {
        const value = await request('/notices' + (cursor ? `?cursor=${encodeURIComponent(cursor)}` : ''));
        if (generation !== sequence.current || !live()) return;
        if (!value || !Array.isArray(value.notices) || value.notices.length > 50 ||
          !value.notices.every((item: any) => item && uuid(item.id) && isString(item.title)) ||
          !(value.next_cursor === null || uuid(value.next_cursor) && value.next_cursor !== cursor)) throw Error();
        records.push(...value.notices.map((item: Manual) => ({ id: item.id, title: item.title })));
        cursor = value.next_cursor;
        if (!cursor) { setManuals(records); return; }
      }
      throw Error();
    } catch (error: any) {
      if (generation !== sequence.current || !live()) return;
      if ([401, 403].includes(error?.status)) { setPage(null); setManuals([]); }
      setMessage('Manuelt vedlikeholdte avvik kunne ikke hentes.');
    }
  }

  function clearPending() { pendingRef.current = null; setPending(null); }

  async function send(op: Operation, lookup: boolean) {
    if (writeRef.current || !live()) return;
    const generation = sequence.current;
    writeRef.current = true;
    pendingRef.current = op;
    setPending(op);
    setWriting(true);
    try {
      const value = lookup ? await request(`${path}/operations/${op.operation_id}`) : await mutation(path + '/review', op);
      if (generation !== sequence.current || !live()) return;
      if (!confirmed(value, op, plan.id)) throw Error();
      clearPending();
      setProposal(null);
      setMessage('Gjennomgangen er lagret.');
      // A receipt confirms only that operation. The current projection has authority over a competing later save.
      await load();
    } catch (error: any) {
      if (generation !== sequence.current || !live()) return;
      if ([401, 403, 410].includes(error?.status) || (!lookup && error?.status === 404)) {
        setPage(null); setManuals([]);
        if (error?.status === 410) props.expired();
        setMessage('Tilgangen må kontrolleres før forsøket kan bekreftes.');
      } else if (!lookup && [409, 422, 429].includes(error?.status)) {
        clearPending();
        if (error.status === 409) setProposal(current => current && { ...current, conflict: true });
        setMessage(error.status === 409 ? 'Dagens grunnlag er endret. Sammenlign opplysningene før du lagrer forslaget på nytt.' : 'Forslaget ble avvist og kan redigeres eller forkastes.');
        await load();
      } else {
        setMessage('Lagringen er uavklart. Kontroller forsøket eller send det opprinnelige forslaget på nytt.');
        if (lookup && error?.status === 404) await load();
      }
    } finally { writeRef.current = false; setWriting(false); }
  }

  const mutable = !!page && ['unstarted', 'active'].includes(page.lifecycle.state);
  const validChoice = row && (row.source || choice.action === 'unresolved' && !choice.manual_notice_id) &&
    (choice.action !== 'associate' || !!choice.activity_id && activityLabels.has(choice.activity_id)) &&
    (choice.action !== 'dismiss' || !!choice.reason?.trim());
  const saveAllowed = mutable && !loading && !writing && !pending && proposal && !changed && validChoice;
  function save() {
    if (!saveAllowed || !proposal || pendingRef.current) return;
    void send({ ...proposal.choice, ...proposal.basis.expected, operation_id: crypto.randomUUID() }, false);
  }
  const clock = page?.health;
  return <section hidden={!open} aria-label="Automatiske avvik">
    <h2 ref={title} tabIndex={-1}>Automatiske avvik</h2>
    <div className="controls"><button type="button" onClick={props.back}>Tilbake til planen</button><button type="button" disabled={!shown || loading || writing} onClick={() => void load()}>Hent status</button></div>
    <p role="status">{shown ? message || (loading ? 'Henter automatiske avvik …' : '') : 'Planopplysninger er skjult mens tilgangen kontrolleres.'}</p>
    {shown && pending && <div className="controls"><button disabled={writing} onClick={() => void send(pending, true)}>Kontroller lagringsforsøk</button><button disabled={writing || !mutable} onClick={() => void send(pending, false)}>Send opprinnelig forslag på nytt</button></div>}
    {shown && page && clock && <>
      <p>{healthLabels[clock.status]}{clock.old && ' Det siste komplette grunnlaget er eldre enn 15 minutter.'}</p>
      <dl><dt>Siste forsøk</dt><dd>{showTime(clock.attempt_at)}</dd><dt>Siste svar fra kilden</dt><dd>{showTime(clock.response_at)}</dd>
        <dt>Siste komplette grunnlag</dt><dd>{showTime(clock.baseline_at)}</dd><dt>Sist komplett synkronisert</dt><dd>{showTime(clock.synchronized_at)}</dd>
        <dt>Resultat registrert</dt><dd>{showTime(clock.result_at)}</dd></dl>
      {clock.attempt_at && <p>{clock.attempt_pages} validerte sider og {clock.attempt_count} observerte meldinger i siste forsøk.</p>}
      {clock.failure && <p>Innsamlingsfeil · {clock.failure}</p>}
      {clock.baseline_count !== null && <p>Siste komplette grunnlag inneholdt {clock.baseline_count} meldinger i det undersøkte TRO-omfanget.</p>}
      <p>{clock.evidence_kind === 'synthetic' ? 'Kontrollerte testdata i Entur SIRI-SX-format for TRO.' : 'Passasjerinformasjon fra Entur AS, SIRI-SX for TRO under NLOD.'} Linje og plantid er vurdert lokalt.</p>
      <p><a href="https://developer.entur.no/open-data/realtime" target="_blank" rel="noopener noreferrer">Enturs kildebeskrivelse</a>{' · '}<a href="https://data.norge.no/nlod/no/2.0" target="_blank" rel="noopener noreferrer">NLOD</a>{' · '}<a href="https://svipper.no/" target="_blank" rel="noopener noreferrer">Åpne Svipper for manuell kontroll</a></p>
      <p>{page.total} oppføringer tilgjengelige for gjennomgang, inkludert tidligere observasjoner.</p>
      {(Object.keys(groups) as Group[]).map(group => page.page_counts[group] ? <section key={group} aria-label={groups[group]}><h3>{groups[group]} · {page.page_counts[group]} på denne siden</h3>
        <ul>{page.entries.filter(entry => entry.classification === group).map(entry => <li key={entry.situation}>
          <button type="button" disabled={!!pending || writing} onClick={() => inspect(entry)} aria-pressed={entry.situation === selected}>{entry.source?.content.summary.find(item => item.text)?.text || entry.decision?.evidence.summary.find(item => item.text)?.text || entry.situation}</button>
          <p>{entry.reasons.map(reason => reasons[reason] ?? reason).join(' ')}{entry.needs_reassessment && ' Tidligere valg må vurderes på nytt.'}</p>
          {entry.decision && !entry.needs_reassessment && <p>Privat valg · {decisions[entry.decision.action]}</p>}
        </li>)}</ul></section> : null)}
      <div className="controls">{cursors.length > 1 && <button disabled={loading || !!pending} onClick={() => { const previous = cursors.slice(0, -1); setCursors(previous); setSelected(null); setProposal(null); void load(previous.at(-1) ?? null); }}>Forrige side</button>}
        {page.next_cursor && <button disabled={loading || !!pending} onClick={() => { setCursors([...cursors, page.next_cursor]); setSelected(null); setProposal(null); void load(page.next_cursor); }}>Neste side</button>}</div>
      {row && <section><h3>Gjennomgang av melding</h3>
        {row.source && <><p>{observations[row.source.observation]}</p><div className="automatic-notice-comparison"><SourceFacts value={row.source.content} />{row.manual && <ManualFacts manual={row.manual} />}</div>
          <dl><dt>Svar fra kilden</dt><dd>{showTime(row.source.response_at)}</dd><dt>Hentet</dt><dd>{showTime(row.source.fetched_at)}</dd><dt>Først observert</dt><dd>{showTime(row.source.first_seen)}</dd><dt>Revisjonen sist observert</dt><dd>{showTime(row.source.last_seen)}</dd><dt>Meldingen sist observert</dt><dd>{showTime(row.source.identity_last_seen)}</dd></dl>
          {row.source.conflict_count > 0 && <details><summary>Motstridende kildeopplysninger · {row.source.conflict_count} observert</summary>{row.source.conflict_count > row.source.conflicts.length && <p>Viser de {row.source.conflicts.length} sist observerte.</p>}
            <div className="automatic-notice-comparison">{row.source.conflicts.map(item => <section key={item.revision}><p>Observert {showTime(item.last_seen)}</p><SourceFacts value={item.content} /></section>)}</div></details>}</>}
        {!!row.matches.length && <ul aria-label="Mulig relevante planaktiviteter">{row.matches.map(match => <li key={match.id}>{activityLabels.get(match.id)} · {match.line_ref} · {match.authority_ref} · {match.dates.join(', ')}</li>)}</ul>}
        {row.decision && <div><p>{row.needs_reassessment ? 'Tidligere privat valg' : 'Privat valg'} · {decisions[row.decision.action]} · {showTime(row.decision.decided_at)}{row.decision.reason ? ` · ${row.decision.reason}` : ''}</p>
          {row.decision.activity_id && <p>{activityLabels.get(row.decision.activity_id) ?? 'Tidligere planaktivitet'}</p>}
          {row.decision.manual_notice_id && !row.manual && <p>Det lenkede manuelle avviket er ikke lenger tilgjengelig.</p>}
          {row.needs_reassessment && <details open><summary>Grunnlag fra tidligere gjennomgang</summary><div className="automatic-notice-comparison"><SourceFacts value={row.decision.evidence} />{!row.source && row.manual && <ManualFacts manual={row.manual} />}</div>
            <dl><dt>Kildesvar ved gjennomgangen</dt><dd>{showTime(row.decision.source_response_at)}</dd><dt>Observert før gjennomgangen</dt><dd>{showTime(row.decision.source_observed_at)}</dd></dl></details>}
        </div>}
        {!mutable && <p>Planen er skrivebeskyttet.</p>}
        {mutable && !proposal && !pending && <button type="button" disabled={loading || !displayedBasis} onClick={() => inspect(row)}>Start ny gjennomgang</button>}
        {mutable && proposal && <fieldset disabled={writing || !!pending}><legend>Privat gjennomgang</legend>
          <label>Valg <select aria-label="Valg" value={choice.action} onChange={event => setChoice({ ...choice, action: event.target.value as Action, reason: null, activity_id: null })}>{(Object.keys(actions) as Action[]).filter(action => row.source || action === 'unresolved').map(action => <option key={action} value={action}>{actions[action]}</option>)}</select></label>
          {choice.action === 'associate' && <label>Planaktivitet <select aria-label="Planaktivitet" value={choice.activity_id ?? ''} onChange={event => setChoice({ ...choice, activity_id: event.target.value || null })}><option value="">Velg aktivitet</option>{plan.draft.activities.map((activity, index) => <option key={activity.id} value={activity.id}>{formatActivity(activity, index)}</option>)}</select></label>}
          {choice.action === 'dismiss' && <label>Grunn til å legge bort <input maxLength={300} value={choice.reason ?? ''} onChange={event => setChoice({ ...choice, reason: event.target.value })} /></label>}
          {row.source && <><button type="button" onClick={() => void manualChoices()}>Hent manuelle avvik for lenking</button>
            {(manuals.length > 0 || choice.manual_notice_id) && <label>Lenket manuelt avvik <select aria-label="Lenket manuelt avvik" value={choice.manual_notice_id ?? ''} onChange={event => setChoice({ ...choice, manual_notice_id: event.target.value || null })}><option value="">Ingen lenke</option>{choice.manual_notice_id && !manuals.some(m => m.id === choice.manual_notice_id) && <option value={choice.manual_notice_id}>{row.manual?.title ?? 'Tidligere lenke'}</option>}{manuals.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></label>}</>}
          {changed && <><p>Grunnlaget for det ulagrede forslaget er endret. Sammenlign opplysningene før du beholder forslaget.</p>
            {proposal.basis.evidence && proposal.basis.expected.expected_source_basis !== displayedBasis?.expected.expected_source_basis &&
              <details><summary>Kildeopplysninger da forslaget ble startet</summary><SourceFacts value={proposal.basis.evidence} /></details>}
            <button type="button" disabled={loading || !displayedBasis || !validChoice} onClick={confirmComparison}>Sammenlignet. Behold forslaget</button></>}
          <div className="controls"><button type="button" disabled={!saveAllowed} onClick={save}>Lagre gjennomgang</button><button type="button" onClick={() => inspect(row)}>Forkast ulagret forslag</button></div>
        </fieldset>}
      </section>}
    </>}
  </section>;
}
