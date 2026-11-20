import { useEffect, useRef, useState } from 'react';
import { validContent, type Content } from './PrivateDrafts';
import { pdfUploadError } from './pdfUpload';

type Fact = string | number | null;
export type ImportMetadata = {
  version: 1; qualification: 'bounded-layout' | 'partial'; timezone: 'Europe/Oslo';
  header: Record<string, Fact | string[]>; header_provenance: Record<string, any>;
  activities: (Record<string, any> & { activity_id: string; source_order: number; pages: number[]; provenance: Record<string, any>; origins: Record<string, string> })[];
  duties: { value: string; suffix: string | null; after_activity: number; provenance: any }[];
  annotations: { value: string; meaning: null; provenance: any }[];
  unresolved: { code: string; activity: number | null; field: string | null; provenance: any }[];
  pause_groups: { rows: number[]; start: string | null; end: string | null; labels: string[]; kind: string }[];
};
const keys = (value: any, allowed: string[]) => !!value && typeof value === 'object' && !Array.isArray(value) && Object.keys(value).every(key => allowed.includes(key));
const text = (value: any, limit = 300): value is string => typeof value === 'string' && Array.from(value).length <= limit;
const nullableText = (value: any, limit = 300) => value === null || text(value, limit);
const integer = (value: any, min: number, max: number) => Number.isInteger(value) && value >= min && value <= max;
const location = (v: any) => keys(v, ['page', 'column', 'line', 'region', 'field']) && integer(v.page, 1, 20)
  && (v.column === null || integer(v.column, 1, 2)) && (v.line === null || integer(v.line, 1, 10000)) && (v.region === null || v.region === 'header') && nullableText(v.field, 100);
const derivation = (v: any) => keys(v, ['derived_from', 'rule']) && Array.isArray(v.derived_from) && v.derived_from.length <= 10 && v.derived_from.every((s: any) => text(s, 100)) && nullableText(v.rule, 100);
const list = (v: any, max: number, check: (item: any) => boolean) => Array.isArray(v) && v.length <= max && v.every((item: any) => check(item));
const headerKeys = ['shift_id', 'service_date', 'weekday', 'department', 'start', 'end', 'origin', 'destination', 'work', 'span', 'supplements', 'pages', 'start_instant', 'end_instant', 'end_day'];
const sourceKeys = ['label', 'kind', 'line', 'trip_id', 'origin', 'destination', 'start', 'end', 'start_instant', 'end_instant', 'start_day', 'end_day', 'pages', 'provenance', 'source_order', 'activity_id', 'origins'];
const fieldKeys = ['label', 'kind', 'line', 'trip_id', 'origin', 'destination', 'start', 'end', 'start_instant', 'end_instant', 'start_day', 'end_day'];
export function validMetadata(v: any): v is ImportMetadata {
  return keys(v, ['version', 'qualification', 'timezone', 'header', 'header_provenance', 'activities', 'duties', 'annotations', 'unresolved', 'pause_groups'])
    && v.version === 1 && ['bounded-layout', 'partial'].includes(v.qualification) && v.timezone === 'Europe/Oslo'
    && keys(v.header, headerKeys) && Object.keys(v.header).length === headerKeys.length
    && headerKeys.filter(k => !['pages', 'end_day', 'supplements'].includes(k)).every(k => nullableText(v.header[k]))
    && integer(v.header.pages, 1, 20) && (v.header.end_day === null || integer(v.header.end_day, 0, 1)) && list(v.header.supplements, 50, text)
    && keys(v.header_provenance, headerKeys) && Object.keys(v.header_provenance).length === headerKeys.length && Object.values(v.header_provenance).every(p => location(p) || derivation(p))
    && list(v.activities, 200, a => keys(a, sourceKeys) && Object.keys(a).length === sourceKeys.length
      && /^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(a.activity_id)
      && sourceKeys.filter(k => !['activity_id', 'source_order', 'pages', 'provenance', 'origins', 'start_day', 'end_day'].includes(k)).every(k => nullableText(a[k]))
      && integer(a.source_order, 1, 200) && list(a.pages, 20, p => integer(p, 1, 20))
      && ['start_day', 'end_day'].every(k => a[k] === null || integer(a[k], 0, 1))
      && keys(a.provenance, fieldKeys) && Object.keys(a.provenance).length === fieldKeys.length && Object.values(a.provenance).every(p => derivation(p) || list(p, 20, location))
      && keys(a.origins, fieldKeys) && Object.keys(a.origins).length === fieldKeys.length && Object.values(a.origins).every(o => ['extracted', 'derived', 'unresolved'].includes(o as string)))
    && v.activities.every((a: any, i: number) => a.source_order === i + 1) && new Set(v.activities.map((a: any) => a.activity_id)).size === v.activities.length
    && list(v.duties, 200, d => keys(d, ['value', 'suffix', 'after_activity', 'provenance']) && text(d.value, 100) && (d.suffix === null || /^\d{3}$/.test(d.suffix)) && integer(d.after_activity, 0, 200) && location(d.provenance))
    && list(v.annotations, 400, a => keys(a, ['value', 'meaning', 'provenance']) && text(a.value, 100) && a.meaning === null && location(a.provenance))
    && list(v.unresolved, 1000, u => keys(u, ['code', 'activity', 'field', 'provenance']) && text(u.code, 100) && (u.activity === null || integer(u.activity, 1, 200)) && nullableText(u.field, 100) && (u.provenance === null || location(u.provenance)))
    && list(v.pause_groups, 200, p => keys(p, ['rows', 'start', 'end', 'labels', 'kind']) && list(p.rows, 200, n => integer(n, 1, 200)) && nullableText(p.start, 40) && nullableText(p.end, 40) && list(p.labels, 200, text) && ['meal', 'split', 'coffee', 'paid_meal'].includes(p.kind));
}

const pauseNames: Record<string, string> = { meal: 'matpause', coffee: 'kaffepause', split: 'deltskiftpause', paid_meal: 'betalt pause' };
const uncertaintyNames: Record<string, string> = { unresolved_time: 'Klokkeslett eller kalenderdato er uavklart', unclassified_time: 'Ett klokkeslett står i første tidskolonne; start og slutt er uavklart', missing_endpoint: 'Endested mangler', unrecognized_source_line: 'Kilderad kunne ikke tolkes', unproven_calendar_interval: 'Skiftintervallet kunne ikke fastslås', reversed_activity_time: 'Slutt ligger før start' };
const show = (v: unknown) => v === null || v === undefined ? 'Ukjent / uavklart' : Array.isArray(v) ? v.join(', ') : String(v);
const sourceDay = (value: unknown) => typeof value === 'string' ? value.slice(0, 10) : 'Ukjent dato';
const activityKind = (value: string) => value === 'trip' || value === 'Trip' ? 'tur' : value === 'deadhead_car' ? 'Tomkjøring med CAR' : value;
const factNames: Record<string, string> = { label: 'Aktivitetsnavn', kind: 'Type', line: 'Linje', trip_id: 'Turnummer', origin: 'Fra sted', destination: 'Til sted', start: 'Startklokke', end: 'Sluttklokke', start_instant: 'Start med kalenderdato', end_instant: 'Slutt med kalenderdato', start_day: 'Startdag', end_day: 'Sluttdag', service_date: 'Tjenestedato', span: 'Utstrekk', pages: 'Sider', shift_id: 'Skift', weekday: 'Ukedag', department: 'Avdeling', work: 'Arbeidstid', supplements: 'Tillegg' };
function reference(path: string): string {
  const parts = path.split('.');
  if (parts[0] === 'activities') return `aktivitet ${parts[1]}: ${factNames[parts[2]] ?? parts[2]}`;
  if (parts[0] === 'header') return `overskrift: ${factNames[parts[1]] ?? parts[1]}`;
  return path === 'timezone' ? 'tidssone Europe/Oslo' : path === 'document.pages' ? 'dokumentets sider' : path;
}
function sourceReference(p: any): string {
  if (Array.isArray(p)) return p.map(sourceReference).join('; ');
  if (p.derived_from) return `Avledet fra ${p.derived_from.map(reference).join(', ')}${p.rule ? `; regel: ${p.rule === 'unique instant in header interval' ? 'entydig tidspunkt innenfor oppgitt skiftintervall' : p.rule}` : ''}`;
  return [`side ${p.page}`, p.region === 'header' ? 'overskrift' : null, p.column ? `kolonne ${p.column}` : null, p.line ? `linje ${p.line}` : null, p.field ? `felt ${factNames[p.field] ?? p.field}` : null].filter(Boolean).join(', ');
}
export function SourceFacts({ metadata: m, historical = false }: { metadata: ImportMetadata; historical?: boolean }) {
  return <section className="import-facts" aria-label="Kildefakta fra PDF"><h3>{historical ? 'Historiske kildefakta fra PDF · før rettelser og bekreftelse' : 'Kildefakta fra PDF · ikke bekreftet'}</h3>{historical && <p>Dette er den opprinnelige tolkningen. Rettede og bekreftede fakta i dagsoversikten gjelder.</p>}
    <p>{m.qualification === 'partial' ? 'Delvis tolkning. Uavklarte felt må vurderes.' : 'Tolket med den avgrensede tekst-PDF-adapteren.'} Ingen garanti for fullstendighet. Andre oppsett, OCR, sommertidsbytte og mellomstopp er ikke kvalifisert.</p>
    <p>Kalenderdatoer er avledet fra tjenestedato, skiftstart og oppgitt utstrekk. Ukjente fakta beholdes. Buss er ikke oppgitt i kilden.</p>
    <dl className="source-header">{Object.entries(m.header).map(([key, value]) => <div key={key}><dt>{({ shift_id: 'Skift', service_date: 'Tjenestedato', weekday: 'Ukedag i kilden', department: 'Avdeling', start: 'Skiftstart', end: 'Skiftslutt i overskrift', origin: 'Oppmøtested', destination: 'Sluttsted i overskrift', work: 'Arbeidstid', span: 'Utstrekk', supplements: 'Tillegg', pages: 'Sider', start_instant: 'Avledet startdato', end_instant: 'Avledet sluttdato', end_day: 'Sluttdag relativt til tjenestedato' } as Record<string, string>)[key]}</dt><dd>{show(value)}<br /><small>{sourceReference(m.header_provenance[key])}</small></dd></div>)}</dl>
    <p>Overskriftens slutt kan avvike fra siste aktivitet. Det legges ikke til noen aktivitet for mellomrommet.</p>
    <h4>Vognløp i kildeorden</h4><ul>{m.duties.map((d, i) => <li key={i}>{d.value} · sanntidsverdi {show(d.suffix)} · etter aktivitet {d.after_activity} · {sourceReference(d.provenance)}</li>)}</ul>
    <ol>{m.activities.map(a => <li key={a.activity_id}><h4>{a.source_order}. {activityKind(a.label)} · side {a.pages.join(', ')}</h4>
      <div className="import-columns"><dl>{['start', 'end', 'origin', 'destination', 'trip_id', 'line'].map(key => <div key={key}><dt>{({ start: 'Kildestart', end: 'Kildeslutt', origin: 'Fra', destination: 'Til', trip_id: 'Tur', line: 'Linje' } as Record<string, string>)[key]}</dt><dd>{show(a[key])} · {a.origins[key] === 'unresolved' ? 'uavklart' : 'kilde'}</dd></div>)}</dl><dl><dt>Tolket type</dt><dd>{a.origins.kind === 'unresolved' ? 'Ukjent / uavklart' : activityKind(a.kind)} · {a.origins.kind === 'unresolved' ? 'uavklart' : 'avledet'}</dd><dt>Start med kalenderdato</dt><dd>{show(a.start_instant)}</dd><dt>Slutt med kalenderdato</dt><dd>{show(a.end_instant)}</dd><dt>Feltplasseringer</dt><dd>{Object.entries(a.provenance).filter(([, p]) => Array.isArray(p)).map(([key, p]) => `${factNames[key] ?? key}: ${sourceReference(p)}`).join(' · ')}</dd><dt>Avledningsgrunnlag per kalenderfelt</dt><dd>{Object.entries(a.provenance).filter(([, p]) => !Array.isArray(p)).map(([key, p]) => <p key={key}>{factNames[key] ?? key}: {sourceReference(p)}</p>)}</dd></dl></div></li>)}</ol>
    <h4>Pausegrupper · kilderadene beholdes</h4><ul>{m.pause_groups.map((p, i) => <li key={i}>{pauseNames[p.kind]} · aktiviteter {p.rows.join(', ')} · {show(p.start)} – {show(p.end)}</li>)}</ul>
    <h4>Uavklart i kilden</h4>{m.unresolved.length ? <ul>{m.unresolved.map((u, i) => <li key={i}>{u.activity ? `Aktivitet ${u.activity}: ` : ''}{uncertaintyNames[u.code] ?? `Ukjent kildeusikkerhet (${u.code})`} {u.field ? `(${factNames[u.field] ?? u.field})` : ''}{u.provenance ? ` · ${sourceReference(u.provenance)}` : ''}</li>)}</ul> : <p>Ingen særskilt usikkerhet rapportert av adapteren. Kontroller hele tolkningen.</p>}
    {m.annotations.length > 0 && <p>Kildemerker: {m.annotations.map(a => `${a.value} (${sourceReference(a.provenance)})`).join(', ')}.</p>}
  </section>;
}

export function PrivateImport({ upload, adopt, expired, suspended, locked, stage, reviewReady, backToUpload, settingsBlocked }: { upload: (file: File, signal: AbortSignal) => Promise<any>; adopt: (content: Content, intent: 'edit' | 'approve') => boolean; expired: () => void; suspended: boolean; locked: boolean; stage: 'upload' | 'review'; reviewReady: () => void; backToUpload: () => void; settingsBlocked: (value: boolean) => void }) {
  const [review, setReview] = useState<Content | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('Velg en tekst-PDF for en midlertidig gjennomgang. Originalen og filnavnet lagres ikke.');
  const controller = useRef<AbortController | null>(null);
  const epoch = useRef(0);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => { settingsBlocked(busy || !!review); return () => settingsBlocked(false); }, [busy, review, settingsBlocked]);
  useEffect(() => { if (stage === 'review') heading.current?.focus(); }, [stage]);
  function cancel(text = 'Importen er avbrutt. Tidligere arbeid er beholdt.') { epoch.current++; controller.current?.abort(); controller.current = null; setBusy(false); setReview(null); setMessage(text); }
  useEffect(() => () => { epoch.current++; controller.current?.abort(); }, []);
  useEffect(() => { if (suspended) cancel(); }, [suspended]);
  async function select(file?: File) {
    if (!file) return;
    cancel();
    if (file.size > 10 * 1024 * 1024 || !file.name.toLowerCase().endsWith('.pdf')) { setMessage('Velg en tekst-PDF på høyst 10 MiB. Du kan bruke manuelt utkast.'); return; }
    const current = epoch.current;
    const abort = new AbortController(); controller.current = abort;
    setBusy(true); setMessage('Tolker PDF … Du kan avbryte.');
    try {
      const value = await upload(file, abort.signal);
      if (current !== epoch.current) return;
      if (!validContent(value) || !value.import_metadata || value.physical_bus !== null) throw Object.assign(Error(), { importFailure: 'response' });
      setReview(value); reviewReady(); setMessage('Gjennomgangen er klar. Kontroller kildefakta før du bruker dem i et separat utkast.'); heading.current?.focus();
    } catch (error: any) {
      if (current !== epoch.current) return;
      if (error?.status === 401) { expired(); return; }
      setMessage(pdfUploadError(error));
    } finally { if (current === epoch.current) { setBusy(false); controller.current = null; } }
  }
  return <section aria-label="Importer tekst-PDF"><h3 ref={heading} tabIndex={-1}>Gjennomgå en tekst-PDF</h3><p aria-live="polite">{message}</p>
    <label hidden={stage !== 'upload'}>Velg tekst-PDF<input type="file" accept=".pdf,application/pdf" disabled={busy || suspended || locked} onChange={event => {
      const input = event.currentTarget, file = input.files?.[0];
      void select(file).finally(() => { if (input.files?.[0] === file) input.value = ''; });
    }} /></label>
    {stage === 'upload' && review && <button onClick={reviewReady}>Fortsett importgjennomgang</button>}
    {(busy || review) && <button onClick={() => { cancel(); backToUpload(); }}>{busy ? 'Avbryt import' : 'Forkast gjennomgang'}</button>}
    {stage === 'review' && review?.import_metadata && <><h3>Importsammendrag</h3><p>Skift {show(review.import_metadata.header.shift_id)} · {show(review.service_date)} · {review.activities.length} aktiviteter · vognløp {show(review.vehicle_duty)}.</p><p className="import-summary-interval">Oppgitt skift: {show(review.import_metadata.header.start)} · {show(review.import_metadata.header.origin)} → {show(review.import_metadata.header.end)} · {show(review.import_metadata.header.destination)}. Avledede kalenderdatoer: {sourceDay(review.import_metadata.header.start_instant)} – {sourceDay(review.import_metadata.header.end_instant)}.</p><p>Buss/vogn er ukjent. {review.import_metadata.unresolved.length} kildevarsler. Ukjente fakta og aktivitetstyper avgjøres ved godkjenning. Ingenting er lagret ennå.</p><details><summary>Vis alle kildefakta fra PDF</summary><SourceFacts metadata={review.import_metadata} /></details><div className="controls"><button disabled={suspended || locked} onClick={() => { if (adopt(review, 'edit')) cancel('Tolkningen er overført til et separat, ulagret utkast.'); }}>Rett eller legg til opplysninger</button><button disabled={suspended || locked} onClick={() => { if (adopt(review, 'approve')) cancel('Lagring er startet uttrykkelig.'); }}>Alt stemmer – lagre og fortsett</button></div></>}
  </section>;
}
