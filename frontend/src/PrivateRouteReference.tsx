import { useEffect, useRef, useState } from 'react';
import { privateNow } from './privateClock';
import type { Saved } from './PrivateDrafts';

type Request = (path: string) => Promise<any>;
type Mutation = (path: string, body: object) => Promise<any>;
type Time = { raw_time: string; raw_day_offset: string | null; day_offset: number; calendar_time: string | null; utc: string | null };
type Call = {
  position: number; occurrence_id: string; scheduled_stop_point_id: string; stop_place_id: string | null;
  quay_id: string | null; name: string; headsign: string; arrival: Time | null; departure: Time | null;
};
type Journey = {
  journey_id: string; line_id: string; pattern_id: string; direction: string; service_date: string;
  headsign: string; calls: Call[];
};
type Provenance = {
  provider: string; generation: string; sha256: string; observed_at: string;
  checked_at?: string; line_publication: string | null; timezone: string;
};
type Mode = 'keep' | 'source' | 'manual' | 'unknown';
type Choice = { mode: Mode; manual?: string };
type FieldChoices = Record<'direction' | 'destination' | 'stops', Choice>;
type Comparison = 'same_version' | 'same_facts' | 'changed' | 'missing' | 'stale' | 'unavailable';
export type Reference = Journey & {
  activity_id: string; decision_revision: number; start_position: number; end_position: number;
  provenance: Provenance; status: 'compatible' | 'incompatible' | 'unverified'; field_decisions: FieldChoices;
  selected_at: string; comparison?: Comparison;
};
type DraftRoutes = { draft_id: string; draft_revision: number; route_revision: number; references: Reference[]; outdated: Reference[] };
type Summary = Pick<Journey, 'journey_id' | 'pattern_id' | 'direction' | 'headsign'> & {
  start: Time; end: Time; from_name: string; to_name: string; matching_ranges: number[][]; ranges_truncated: boolean;
};
type Coverage = 'complete' | 'partial' | 'unavailable';
type SourceState = 'available' | 'stale' | 'outside_scope' | 'unavailable';
type Overview = {
  coverage: Coverage; source_state: SourceState; provenance: Provenance | null; service_date: string;
  expected_count: number | null; reasons: string[]; journeys: Summary[];
  outcome: 'possible' | 'alternatives' | 'not_found' | 'insufficient';
};
type Operation = {
  operation_id: string; expected_draft_revision: number; expected_route_revision: number; activity_id: string;
  selection: null | { journey_id: string; source_sha256: string; start_position: number; end_position: number; field_decisions: FieldChoices };
};

const fields = [['direction', 'Retning'], ['destination', 'Destinasjonsvisning'], ['stops', 'Stoppoversikt']] as const;
const keepChoices = (): FieldChoices => ({ direction: { mode: 'keep' }, destination: { mode: 'keep' }, stops: { mode: 'keep' } });
const direction = (value: string) => value === 'outbound' ? 'Utgående' : value === 'inbound' ? 'Inngående' : value;
const validTime = (value: any): value is Time | null => value === null || value && typeof value.raw_time === 'string'
  && Number.isInteger(value.day_offset) && (value.calendar_time === null || typeof value.calendar_time === 'string')
  && (value.utc === null || typeof value.utc === 'string' && Number.isFinite(Date.parse(value.utc)));
const validJourney = (value: any): value is Journey => value && typeof value.journey_id === 'string'
  && value.line_id === 'TRO:Line:1_20' && typeof value.pattern_id === 'string' && ['outbound', 'inbound'].includes(value.direction)
  && typeof value.headsign === 'string' && typeof value.service_date === 'string'
  && Array.isArray(value.calls) && value.calls.length >= 2 && value.calls.length <= 120
  && value.calls.every((call: any, i: number) => call?.position === i + 1 && typeof call.name === 'string'
    && typeof call.occurrence_id === 'string' && typeof call.headsign === 'string'
    && (call.quay_id === null || /^NSR:Quay:/.test(call.quay_id)) && validTime(call.arrival) && validTime(call.departure));
const validProvenance = (value: any): value is Provenance => value && typeof value.provider === 'string'
  && typeof value.generation === 'string' && typeof value.sha256 === 'string' && /^[a-f0-9]{64}$/.test(value.sha256)
  && Number.isFinite(Date.parse(value.observed_at))
  && (value.checked_at === undefined || typeof value.checked_at === 'string' && Number.isFinite(Date.parse(value.checked_at)));
function validReference(value: any): value is Reference {
  return typeof value?.activity_id === 'string' && Number.isInteger(value.decision_revision) && value.decision_revision > 0
    && Number.isInteger(value.start_position) && Number.isInteger(value.end_position)
    && Number.isFinite(Date.parse(value.selected_at))
    && ['compatible', 'incompatible', 'unverified'].includes(value.status)
    && fields.every(([key]) => ['keep', 'source', 'manual', 'unknown'].includes(value.field_decisions?.[key]?.mode)
      && (value.field_decisions[key].mode !== 'manual' || typeof value.field_decisions[key].manual === 'string'))
    && validProvenance(value.provenance) && validJourney(value)
    && (value as Reference).start_position >= 1 && (value as Reference).end_position > (value as Reference).start_position
    && (value as Reference).end_position <= value.calls.length;
}
const summaryValid = (item: any): item is Summary => item && typeof item.journey_id === 'string'
  && typeof item.pattern_id === 'string' && typeof item.headsign === 'string' && typeof item.from_name === 'string' && typeof item.to_name === 'string'
  && ['outbound', 'inbound'].includes(item.direction) && item.start && item.end && validTime(item.start) && validTime(item.end)
  && Array.isArray(item.matching_ranges) && item.matching_ranges.every((range: any) => Array.isArray(range)
      && range.length === 2 && range.every(pos => Number.isSafeInteger(pos) && pos >= 1 && pos <= 120));
const scope = (draft: Saved) => '/drafts/' + draft.id;
const draftPath = (draft: Saved) => scope(draft) + '/route-references?revision=' + draft.revision;
export const pilotDate = (value: string | null) => !!value && /^2026-11-2[3-9]$/.test(value);

export async function readDraftRoutes(request: Request, draft: Saved): Promise<DraftRoutes> {
  const result = await request(draftPath(draft));
  if (!result || result.draft_id !== draft.id || result.draft_revision !== draft.revision
    || !Number.isSafeInteger(result.route_revision) || result.route_revision < 0
    || !Array.isArray(result.references) || result.references.length > 200 || !result.references.every((value: any) =>
      validReference(value) && value.service_date === draft.draft.service_date
      && draft.draft.activities.some(a => a.id === value.activity_id))
    || !Array.isArray(result.outdated) || result.outdated.length > 200 || !result.outdated.every(validReference)) {
    throw new Error('Invalid draft route response');
  }
  return result;
}

function shownTime(value: Time | null) {
  if (!value) return 'Ukjent';
  const raw = value.raw_time + (value.day_offset ? ' +' + value.day_offset + ' døgn' : '');
  return value.calendar_time ? raw : raw + ' (UTC uavklart)';
}

const reviewStatus: Record<Reference['status'], string> = {
  compatible: 'Planlagt tid og stedsnavn stemmer med lagret utkast',
  incompatible: 'Avviker fra lagret tidspunkt eller tillatt på- og avstigning',
  unverified: 'Uverifisert sammenheng med turen i utkastet',
};
const comparisonText: Record<Comparison, string> = {
  same_version: 'Samme kildeversjon',
  same_facts: 'Ny kildeversjon med samme planlagte avgangsfakta',
  changed: 'Avgangsfakta er endret i kilden. Det lagrede valget er beholdt.',
  missing: 'Avgangen mangler i den kontrollerte kildeversjonen. Det lagrede valget er beholdt.',
  stale: 'Kildekontrollen er eldre enn 24 timer. Det lagrede valget er beholdt.',
  unavailable: 'Avgangsfakta kan ikke kontrolleres mot kilden nå.',
};
const choiceText: Record<Mode, string> = { keep: 'Behold utkastet', source: 'Vis kildeverdien', manual: 'Vis manuell verdi', unknown: 'Ukjent' };

function Calls({ journey, start = 1, end = journey.calls.length }: { journey: Journey; start?: number; end?: number }) {
  return <ol start={start}>{journey.calls.filter(call => call.position >= start && call.position <= end).map(call =>
    <li key={call.occurrence_id}>
      <strong>{call.name}</strong> · {call.headsign}
      <div>Ankomst {shownTime(call.arrival)} · avgang {shownTime(call.departure)}</div>
      <details><summary>Klokke og kildeidentitet</summary>
        <p>Forekomst {call.position} · {call.occurrence_id}</p>
        <p>Planlagt stoppunkt {call.scheduled_stop_point_id} · plattform {call.quay_id ?? 'Ukjent'} · stoppested {call.stop_place_id ?? 'Ukjent'}</p>
        <p>Ankomst {call.arrival ? (call.arrival.calendar_time ?? 'Uavklart') + ' · UTC ' + (call.arrival.utc ?? 'uavklart') + ' · kildeoffset ' + (call.arrival.raw_day_offset ?? 'ikke angitt') : 'Ukjent'}</p>
        <p>Avgang {call.departure ? (call.departure.calendar_time ?? 'Uavklart') + ' · UTC ' + (call.departure.utc ?? 'uavklart') + ' · kildeoffset ' + (call.departure.raw_day_offset ?? 'ikke angitt') : 'Ukjent'}</p>
      </details>
    </li>)}</ol>;
}

function SourceFacts({ source }: { source: Provenance }) {
  const observed = new Date(source.observed_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' });
  const checked = source.checked_at && new Date(source.checked_at).toLocaleString('nb-NO', { timeZone: 'Europe/Oslo' });
  return <details><summary>Kildegrunnlag</summary><p>{source.provider} · generasjon {source.generation} · {source.timezone}</p>
    <p>Kildearkiv kontrollert {checked || observed}.{checked && ` Ferskhet beregnes fra ${observed}.`} Publikasjonstid fra kildefilen {source.line_publication ?? 'Ukjent'}.</p>
    <p>SHA-256 <span style={{ overflowWrap: 'anywhere' }}>{source.sha256}</span></p></details>;
}

function ReferenceDetails({ reference }: { reference: Reference }) {
  const first = reference.calls[reference.start_position - 1], last = reference.calls[reference.end_position - 1];
  return <div style={{ overflowWrap: 'anywhere' }}>
    <p>Driftsdato {reference.service_date} · {direction(reference.direction)} · {first.name} → {last.name}</p>
    <p>Planlagt destinasjonsvisning fra forekomst {first.position}: {first.headsign}</p>
    <p>{reviewStatus[reference.status]}.</p>
    {reference.comparison && reference.comparison !== 'same_version' && <p>{comparisonText[reference.comparison]}</p>}
    <details><summary>Valgte forekomster {reference.start_position}–{reference.end_position}</summary>
      <p>{reference.journey_id} · {reference.pattern_id}</p>
      <Calls journey={reference} start={reference.start_position} end={reference.end_position} />
    </details>
    <dl>{fields.map(([key, title]) => <div key={key}><dt>{title}</dt><dd>{choiceText[reference.field_decisions[key].mode]}
      {reference.field_decisions[key].manual ? ' · ' + reference.field_decisions[key].manual : ''}</dd></div>)}</dl>
    <SourceFacts source={reference.provenance} />
  </div>;
}

const outcomeText: Record<Overview['outcome'], string> = {
  possible: 'Én mulig avgang og stoppstrekning etter sammenligning av lagret klokkeslett og stedsnavn.',
  alternatives: 'Flere mulige avganger eller stoppstrekninger. Sammenlign før du velger.',
  not_found: 'Ingen avganger stemmer med både de lagrede klokkeslettene og de samme stedsnavnene i denne kontrollerte kilden.',
  insufficient: 'Opplysningene gir ikke grunnlag for å fastslå én mulig avgang eller at avgangen mangler.',
};
const coverageText: Record<Coverage, string> = { complete: 'Kontrollert datodekning', partial: 'Delvis datodekning', unavailable: 'Datodekning utilgjengelig' };
const sourceText: Record<SourceState, string> = { available: 'Gyldig kildekontroll', stale: 'Kildekontroll eldre enn 24 timer', outside_scope: 'Dato utenfor pilotperioden', unavailable: 'Kildefilen er utilgjengelig' };
const reasonsText: Record<string, string> = {
  outside_manifest: 'Linje 20 er i dette oppslaget avgrenset til 23.–29. november 2026.',
  archive_unavailable: 'Arkivet kunne ikke lastes eller verifiseres.',
  unresolved_calendar: 'En eller flere kalenderregler kunne ikke kontrolleres.',
  unresolved_journey: 'En eller flere avganger mangler kontrollerbare forekomster.',
  unresolved_time: 'En eller flere klokker kunne ikke tolkes entydig til UTC.',
  count_mismatch: 'Antall aktive avganger avviker fra den uavhengige kontrollen.',
  outside_source_validity: 'Datoen dekkes ikke av kildefilens gyldighet.',
};

function validateReceipt(value: any, draft: Saved, op: Operation) {
  if (!value || value.operation_id !== op.operation_id || value.draft_id !== draft.id
    || value.activity_id !== op.activity_id || value.draft_revision !== op.expected_draft_revision
    || value.route_revision !== op.expected_route_revision + 1 || !Number.isSafeInteger(value.current_route_revision)
    || value.current_route_revision < value.route_revision) throw new Error('Invalid route receipt');
  if (op.selection === null ? value.reference !== null : !validReference(value.reference)
    || value.reference.journey_id !== op.selection.journey_id || value.reference.provenance.sha256 !== op.selection.source_sha256
    || value.reference.start_position !== op.selection.start_position || value.reference.end_position !== op.selection.end_position
    || fields.some(([key]) => op.selection?.field_decisions[key].mode !== value.reference.field_decisions[key].mode
      || (op.selection?.field_decisions[key].manual ?? null) !== value.reference.field_decisions[key].manual)) {
    throw new Error('Unconfirmed route receipt');
  }
}

export function DraftRouteReview({ draft, request, mutation, suspended, lock, expired }: {
  draft: Saved; request: Request; mutation: Mutation; suspended: boolean; lock: (value: boolean) => void; expired: () => void;
}) {
  const [activityId, setActivityId] = useState('');
  const [routes, setRoutes] = useState<DraftRoutes | null>(null);
  const [overview, setOverview] = useState<Overview | null>(null);
  const [journey, setJourney] = useState<Journey | null>(null);
  const [range, setRange] = useState({ start: 0, end: 0 });
  const [choices, setChoices] = useState<FieldChoices>(keepChoices);
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const [pending, setPending] = useState<Operation | null>(null);
  const [sending, setSending] = useState(false);
  const active = useRef(true);
  const epoch = useRef(0);
  const details = useRef<HTMLHeadingElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const act = draft.draft.activities.find(a => a.id === activityId);
  const imported = draft.draft.import_metadata?.activities.find(a => a.activity_id === activityId);
  const target = scope(draft) + '/route-references';
  const departurePath = scope(draft) + '/route-departures?revision=' + draft.revision
    + '&activity_id=' + encodeURIComponent(activityId);
  useEffect(() => { active.current = true; return () => { active.current = false; epoch.current++; }; }, []);
  useEffect(() => { lock(!!pending || sending); return () => lock(false); }, [pending, sending, lock]);

  function failure(error: any) {
    if (error?.status === 401) { expired(); return; }
    if ([404, 410].includes(error?.status)) { setOverview(null); setRoutes(null); setJourney(null); setPending(null); }
    setMessage(error?.status === 409 ? 'Utkastet, rutekilden eller rutevalget er endret. Last inn gjeldende opplysninger og sammenlign.' :
      [403, 404, 410].includes(error?.status) ? 'Tilgangen til rutereferansen utløp eller ble avvist.' :
      'Kunne ikke kontrollere rutekilden eller rutevalget. Prøv igjen.');
  }

  async function load(search: boolean) {
    const generation = ++epoch.current;
    setBusy(true);
    setMessage('');
    try {
      const state = await readDraftRoutes(request, draft);
      let snapshot = null;
      if (search) {
        snapshot = await request(departurePath);
        if (!snapshot || snapshot.draft_id !== draft.id || snapshot.draft_revision !== draft.revision || snapshot.activity_id !== activityId
          || snapshot.service_date !== draft.draft.service_date || !Array.isArray(snapshot.journeys) || snapshot.journeys.length > 160
          || !snapshot.journeys.every(summaryValid) || !(snapshot.coverage in coverageText) || !(snapshot.source_state in sourceText)
          || !(snapshot.outcome in outcomeText) || !Array.isArray(snapshot.reasons)
          || !(snapshot.provenance === null || validProvenance(snapshot.provenance))) throw new Error('Invalid route snapshot');
      }
      if (!active.current || generation !== epoch.current) return;
      setRoutes(state);
      if (search) { setOverview(snapshot); setJourney(null); setRange({ start: 0, end: 0 }); }
      setMessage(search ? 'Ruteoppslaget er oppdatert.' : 'Gjeldende lagrede rutevalg er hentet.');
    } catch (error) { if (active.current && generation === epoch.current) failure(error); }
    finally { if (active.current && generation === epoch.current) setBusy(false); }
  }

  async function inspect(id: string) {
    const generation = ++epoch.current;
    setBusy(true);
    setJourney(null);
    setRange({ start: 0, end: 0 });
    setChoices(keepChoices());
    try {
      const value = await request(departurePath + '&journey_id=' + encodeURIComponent(id));
      if (!active.current || generation !== epoch.current) return;
      if (!value || value.draft_id !== draft.id || value.draft_revision !== draft.revision || value.activity_id !== activityId
        || !validJourney(value.journey) || value.journey.journey_id !== id || value.journey.service_date !== draft.draft.service_date
        || value.provenance?.sha256 !== overview?.provenance?.sha256) throw new Error('Invalid route detail');
      setJourney(value.journey);
      setMessage('');
      requestAnimationFrame(() => details.current?.focus());
    } catch (error) { if (active.current && generation === epoch.current) failure(error); }
    finally { if (active.current && generation === epoch.current) setBusy(false); }
  }

  async function persist(op: Operation, retry: boolean, lookupOnly = false) {
    if (sending || suspended) return;
    const generation = ++epoch.current;
    const operationURL = scope(draft) + '/route-reference-operations/' + op.operation_id;
    let dispatched = false;
    let accepted = false;
    setPending(op); setSending(true); setMessage('Kontrollerer om rutevalget er lagret …');
    try {
      if (retry) {
        const receipt = await request(operationURL);
        if (receipt?.state === 'accepted') validateReceipt(receipt.result, draft, op);
        else {
          if (receipt?.state !== 'pending' || receipt.result !== null) throw new Error('Invalid route operation');
          if (lookupOnly) { setMessage('Forsøket er uavklart. Prøv samme lagring igjen.'); return; }
          const current = await readDraftRoutes(request, draft);
          if (current.route_revision !== op.expected_route_revision) {
            setRoutes(current); setPending(null);
            setMessage('Et annet rutevalg ble lagret. Sammenlign med gjeldende valg før du lagrer på nytt.');
            return;
          }
          dispatched = true;
          validateReceipt(await mutation(target, op), draft, op);
          dispatched = false;
        }
      } else {
        dispatched = true;
        validateReceipt(await mutation(target, op), draft, op);
        dispatched = false;
      }
      const receipt = await request(operationURL);
      if (receipt?.state !== 'accepted') throw new Error('Missing route receipt');
      validateReceipt(receipt.result, draft, op);
      accepted = true;
      const current = await readDraftRoutes(request, draft);
      if (!active.current || generation !== epoch.current) return;
      if (current.route_revision < receipt.result.route_revision) throw new Error('Invalid current revision');
      setRoutes(current); setPending(null);
      setMessage(current.route_revision > receipt.result.route_revision ? 'Lagringen er bekreftet. En nyere ruteversjon er hentet.' :
        op.selection ? 'Rutevalget er lagret.' : 'Rutevalget er fjernet.');
    } catch (error: any) {
      if (!active.current || generation !== epoch.current) return;
      if (error?.status === 401 || [403, 404, 410].includes(error?.status)) { setPending(null); failure(error); }
      else if (accepted && error?.status === 409) {
        setPending(null); setRoutes(null); setOverview(null); setJourney(null);
        setMessage('Lagringen er bekreftet. Last inn gjeldende utkast for å se nyere opplysninger.');
      }
      else if (dispatched && typeof error?.apiDetail === 'string' && [409, 422, 429].includes(error?.status)) {
        setPending(null);
        if (error.status === 409) setRoutes(null);
        setMessage(error.apiDetail);
      } else setMessage('Lagringen er uavklart. Kontroller forsøket eller prøv samme lagring igjen.');
    } finally { if (active.current && generation === epoch.current) setSending(false); }
  }

  function save(selection: Operation['selection'], id = activityId) {
    if (!routes || !id || busy || pending) return;
    void persist({ operation_id: crypto.randomUUID(), expected_draft_revision: draft.revision,
      expected_route_revision: routes.route_revision, activity_id: id, selection }, false);
  }

  const tripOptions = draft.draft.activities.filter(a => a.type === 'trip');
  const blocked = busy || sending || !!pending || suspended;
  const ready = !!journey && !!overview?.provenance && !!routes && range.start > 0 && range.end > range.start
    && fields.every(([key]) => choices[key].mode !== 'manual' || !!choices[key].manual?.trim());
  const pendingRoutes = routes?.outdated.filter(reference => draft.draft.activities.some(a => a.id === reference.activity_id));
  return <details style={{ overflowWrap: 'anywhere' }}>
    <summary>Planlagte avganger for linje 20</summary>
    <p>Oppslaget gjelder driftsdatoen i det lagrede utkastet, begge retninger og publiserte varianter. Pilotperioden er 23.–29. november 2026.</p>
    {tripOptions.length > 0 && <div className="controls"><label>Lagret passasjertur <select disabled={blocked} value={activityId} onChange={event => {
      setActivityId(event.target.value); setOverview(null); setJourney(null); setMessage('');
    }}><option value="">Velg tur</option>{tripOptions.map(activity => <option key={activity.id} value={activity.id}>
      {activity.source_start ?? activity.start ?? 'Ukjent klokkeslett'} · {activity.from_place ?? 'Ukjent'} → {activity.to_place ?? 'Ukjent'}
    </option>)}</select></label><button ref={trigger} onClick={() => void load(true)} disabled={blocked || !activityId}>Søk på driftsdatoen</button></div>}
    {pilotDate(draft.draft.service_date) && <button onClick={() => void load(false)} disabled={blocked}>Hent lagrede rutevalg</button>}
    {!tripOptions.length && <p>Utkastet mangler en lagret passasjertur.</p>}
    <p role="status">{message}</p>
    {pending && <div className="controls">
      <button disabled={sending || suspended} onClick={() => void persist(pending, true, true)}>Kontroller lagringsforsøket</button>
      <button disabled={sending || suspended} onClick={() => void persist(pending, true)}>Prøv samme rutevalg igjen</button>
    </div>}
    {routes?.references.map(reference => <section key={reference.activity_id} aria-label="Lagret rutevalg">
      <h4>Lagret rutevalg · versjon {reference.decision_revision}</h4>
      <ReferenceDetails reference={reference} />
      <button disabled={blocked} onClick={() => save(null, reference.activity_id)}>Fjern rutevalget</button>
    </section>)}
    {pendingRoutes?.map(reference => <details key={reference.activity_id}><summary>Tidligere rutevalg for utkastet</summary>
      <p>Utkastversjonen er endret. Forekomstene må velges på nytt før referansen kan følge planen.</p>
      <ReferenceDetails reference={reference} />
    </details>)}
    {overview && <section aria-label="Daterte avganger">
      <h4>Driftsdato {overview.service_date ?? 'Ukjent'} · linje 20</h4>
      <p>{coverageText[overview.coverage]} · {sourceText[overview.source_state]}
        {overview.expected_count !== null && <> · {overview.journeys.length} av {overview.expected_count} forventede avganger</>}</p>
      {overview.reasons.map(reason => <p key={reason}>{reasonsText[reason] ?? 'Kildegrunnlaget er uavklart.'}</p>)}
      <p>{outcomeText[overview.outcome]}</p>
      {overview.provenance && <SourceFacts source={overview.provenance} />}
      {!!overview.journeys.length && <label>Planlagt avgang <select disabled={blocked} value={journey?.journey_id ?? ''}
        onChange={event => { if (event.target.value) void inspect(event.target.value); else setJourney(null); }}>
        <option value="">Velg avgang</option>{overview.journeys.map(item => <option key={item.journey_id} value={item.journey_id}>
          {shownTime(item.start)} · {direction(item.direction)} · {item.from_name} → {item.to_name} · {item.headsign}
          {item.matching_ranges.length ? ' · mulig strekning' : ''}
        </option>)}</select></label>}
    </section>}
    {journey && overview?.provenance && <section aria-label="Gjennomgå rutevalg">
      <h4 ref={details} tabIndex={-1}>Planlagt avgang til {journey.headsign}</h4>
      <p>{journey.journey_id} · {journey.pattern_id} · {direction(journey.direction)}</p>
      <p>Lagret utkast · {act?.from_place ?? 'Ukjent'} → {act?.to_place ?? 'Ukjent'} · retning {act?.direction ?? 'ukjent'}</p>
      {imported && <p>Importert · {imported.origin ?? 'Ukjent'} → {imported.destination ?? 'Ukjent'} · linje {imported.line ?? 'ukjent'}</p>}
      <details><summary>Alle planlagte stoppforekomster</summary><Calls journey={journey} /></details>
      {overview.journeys.find(item => item.journey_id === journey.journey_id)?.matching_ranges.map(([start, end]) =>
        <button key={start + ':' + end} disabled={blocked} onClick={() => setRange({ start, end })}>Velg mulig strekning {start}–{end}</button>)}
      {(['start', 'end'] as const).map(key => <label key={key}>{key === 'start' ? 'Første forekomst' : 'Siste forekomst'} <select
        disabled={blocked} value={range[key]} onChange={event => setRange({ ...range, [key]: Number(event.target.value) })}>
        <option value={0}>Velg forekomst</option>{journey.calls.map(call => <option key={call.occurrence_id} value={call.position}>
          {call.position}. {call.name} · {shownTime(key === 'start' ? call.departure : call.arrival ?? call.departure)}
        </option>)}</select></label>)}
      <fieldset disabled={blocked}><legend>Visningsvalg for rutereferansen</legend>
        {fields.map(([key, text]) => <div key={key}><label>{text} <select value={choices[key].mode} onChange={event =>
          setChoices({ ...choices, [key]: { mode: event.target.value as Mode } })}>
          {Object.entries(choiceText).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select></label>{choices[key].mode === 'manual' && <label>{text} · manuell verdi <input maxLength={300} value={choices[key].manual ?? ''}
          onChange={event => setChoices({ ...choices, [key]: { mode: 'manual', manual: event.target.value } })} /></label>}</div>)}
      </fieldset>
      <div className="controls">
        <button disabled={blocked || !ready} onClick={() => save({ journey_id: journey.journey_id,
          source_sha256: overview.provenance!.sha256, start_position: range.start, end_position: range.end, field_decisions: choices })}>Lagre valgt avgang og strekning</button>
        <button disabled={blocked} onClick={() => { setJourney(null); setRange({ start: 0, end: 0 }); trigger.current?.focus(); }}>Avbryt rutevalg</button>
      </div>
    </section>}
  </details>;
}

export function FrozenRouteReference({ workdayId, activityId, expiresAt, serviceDate, request, expired, available }: {
  workdayId: string; activityId: string; expiresAt: string; serviceDate: string | null;
  request: Request; expired: () => void; available: boolean;
}) {
  const [reference, setReference] = useState<Reference | null>(null);
  const [failed, setFailed] = useState(false);
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    setReference(null); setFailed(false);
    if (!available || !pilotDate(serviceDate)) return;
    let current = true;
    const deadline = Date.parse(expiresAt);
    const timer = window.setTimeout(() => { if (current) setReference(null); }, Math.max(0, deadline - privateNow()));
    void request('/workdays/' + workdayId + '/route-references').then(value => {
      if (!current || deadline <= privateNow()) return;
      if (!value || value.workday_id !== workdayId || !Array.isArray(value.references) || !value.references.every(validReference))
        throw new Error('Invalid frozen routes');
      setReference(value.references.find((entry: Reference) => entry.activity_id === activityId && entry.service_date === serviceDate) ?? null);
    }).catch(error => {
      if (!current) return;
      if (error?.status === 401) expired();
      else setFailed(true);
    });
    return () => { current = false; clearTimeout(timer); };
  }, [workdayId, activityId, serviceDate, expiresAt, available, retry]);
  if (!available || Date.parse(expiresAt) <= privateNow()) return null;
  if (failed) return <p>Kunne ikke hente rutereferansen. <button onClick={() => setRetry(value => value + 1)}>Prøv igjen</button></p>;
  return reference && <section aria-label="Rutereferanse fra bekreftelsen">
    <h4>Planlagt rutereferanse fra bekreftelsen</h4><ReferenceDetails reference={reference} />
  </section>;
}

export function ApprovalRouteReferences({ references }: { references: Reference[] }) {
  if (!references.length) return null;
  return <section aria-label="Rutevalg i gjennomgått plan">
    <h4>Lagrede rutevalg som følger planen</h4>
    {references.map(reference => <ReferenceDetails key={reference.activity_id} reference={reference} />)}
  </section>;
}
