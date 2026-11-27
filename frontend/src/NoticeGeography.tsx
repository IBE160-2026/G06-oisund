import { useRef, useState } from 'react';

export type NoticeStop = { ref: string; name: string };
export type Geography = {
  kind: 'stops' | 'section' | 'area'; direction: 'outbound' | 'inbound' | null;
  stops: NoticeStop[]; cancelled: NoticeStop[]; start: NoticeStop | null; end: NoticeStop | null;
  via: NoticeStop[]; area: string | null; route_ref?: string | null;
};
const refPattern = /^(?:(?:NSR:(?:StopPlace|Quay))|TRO:ScheduledStopPoint):[\w.:/-]{1,140}$/;
const stop = (value: any): value is NoticeStop => !!value && typeof value.ref === 'string' && refPattern.test(value.ref)
  && typeof value.name === 'string' && value.name.length > 0 && value.name.length <= 180;
export function validGeography(value: any): value is Geography {
  if (!value || !['stops', 'section', 'area'].includes(value.kind)
    || ![null, 'outbound', 'inbound'].includes(value.direction)
    || ![value.stops, value.via, value.cancelled].every(list => Array.isArray(list) && list.length <= 24 && list.every(stop)
      && new Set(list.map(item => item.ref)).size === list.length)
    || value.via.length > 12) return false;
  if (value.route_ref && (value.kind !== 'section' || typeof value.route_ref !== 'string' || !/^TRO:Route:[A-Za-z0-9_./-]{1,200}$/.test(value.route_ref))) return false;
  if (value.kind === 'area') return typeof value.area === 'string' && !!value.area.trim() && value.area.length <= 120
    && value.direction === null && value.start === null && value.end === null && !value.stops.length && !value.via.length && !value.cancelled.length;
  if (value.kind === 'section') return value.area === null && !value.stops.length && stop(value.start) && stop(value.end) && value.start.ref !== value.end.ref;
  return value.area === null && value.start === null && value.end === null && !value.via.length && !!value.stops.length
    && value.cancelled.every((item: NoticeStop) => value.stops.some((target: NoticeStop) => target.ref === item.ref));
}

export function geographyLabel(scope: Geography): string {
  if (scope.kind === 'area') return 'Område · ' + scope.area;
  if (scope.kind === 'section') return (scope.start?.name ?? 'Ukjent start') + ' → ' + (scope.end?.name ?? 'Ukjent slutt');
  return scope.stops.map(item => item.name + (item.ref.startsWith('NSR:Quay:') ? ' (plattform)' : '')).join(', ');
}

type Search = { request: (path: string) => Promise<any>; date: string | null; line?: string };
function StopPicker({ title, selected, select, plural, request, date, line }: Search & {
  title: string; selected: NoticeStop[]; select: (stops: NoticeStop[]) => void; plural?: boolean;
}) {
  const [mode, setMode] = useState('stop');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<NoticeStop[]>([]);
  const [message, setMessage] = useState('');
  const generation = useRef(0);
  function edit() { generation.current++; setResults([]); setMessage(''); }
  async function search() {
    const value = query.trim();
    if (value.length < 2) return;
    const attempt = ++generation.current;
    setMessage('Søker i rutedata …');
    setResults([]);
    const params = new URLSearchParams({query: value, mode, ...(date ? {day: date} : {}), ...(line ? {line} : {})});
    try {
      const reply = await request('/notice-stop-options?' + params);
      if (attempt !== generation.current) return;
      if (!Array.isArray(reply?.stops) || !reply.stops.every(stop)) throw Error();
      setResults(reply.stops);
      setMessage(reply.stops.length ? '' : 'Ingen treff i de daterte rutedataene.');
    } catch { if (attempt === generation.current) setMessage('Holdeplasser kunne ikke hentes. Prøv igjen.'); }
  }
  return <fieldset className="notice-stop-picker"><legend>{title}</legend>
    {!!selected.length && <ul>{selected.map(item => <li key={item.ref}>{item.name}{item.ref.startsWith('NSR:Quay:') ? ' · ' + item.ref.split(':').at(-1) : ''}
      <button type="button" onClick={() => select(selected.filter(other => other.ref !== item.ref))}>Fjern {item.name}</button></li>)}</ul>}
    <div className="controls">
      <label>Oppslag<select value={mode} onChange={event => { setMode(event.target.value); edit(); }}><option value="stop">Holdeplass</option><option value="platform">Plattform</option></select></label>
      <label>Søk etter navn<input value={query} maxLength={80} onChange={event => { setQuery(event.target.value); edit(); }}
        onKeyDown={event => { if (event.key === 'Enter') { event.preventDefault(); void search(); } }} /></label>
      <button type="button" disabled={query.trim().length < 2} onClick={() => void search()}>Søk</button>
    </div>
    <p role="status">{message}</p>
    {!!results.length && <ul>{results.map(item => <li key={item.ref}><button type="button" disabled={selected.some(old => old.ref === item.ref)}
      onClick={() => { select(plural ? [...selected,item] : [item]); setResults([]); setQuery(''); }}>
      Velg {item.name}{mode === 'platform' ? ' · plattform ' + item.ref.split(':').at(-1) : ''}
    </button></li>)}</ul>}
  </fieldset>;
}

type RouteOption = {ref: string; name: string; via: string; direction: string};
function RoutePicker({date, line, value, set, request}: Search & {value: Geography; set: (scope: Geography) => void}) {
  const [options, setOptions] = useState<RouteOption[]>([]);
  const [status, setStatus] = useState('');
  const latest = useRef(value);
  latest.current = value;
  async function load() {
    if (!date || !line || !value.start || !value.end) return;
    setStatus('Henter rutevarianter …');
    try {
      const query = new URLSearchParams({day:date,line,start:value.start.ref,end:value.end.ref,
        ...(value.direction ? {direction:value.direction} : {})});
      const response = await request('/notice-route-options?' + query);
      if (latest.current !== value) return;
      if (!Array.isArray(response.routes) || !response.routes.every((item: RouteOption) =>
        typeof item?.ref === 'string' && typeof item.name === 'string' && typeof item.via === 'string'
        && ['inbound','outbound'].includes(item.direction))) throw Error();
      setOptions(response.routes);
      setStatus(response.routes.length ? '' : 'Ingen daterte rutevarianter dekker begge stopp.');
    } catch { if (latest.current === value) setStatus('Rutevariantene kunne ikke hentes.'); }
  }
  return <details>
    <summary>Avgrens til én trasé (valgfritt)</summary>
    <p>Velg en trasé bare hvis avvikskilden avgrenser omkjøringen til akkurat denne varianten.</p>
    <button type="button" disabled={!date || !line || !value.start || !value.end} onClick={() => void load()}>Hent rutevarianter</button>
    <p role="status">{status}</p>
    {(options.length > 0 || value.route_ref) && <label>Rutevariant<select value={value.route_ref ?? ''} onChange={event => set({...value, route_ref: event.target.value || null})}>
      <option value="">Ingen bestemt variant</option>
      {value.route_ref && !options.some(item => item.ref === value.route_ref) && <option value={value.route_ref}>{value.route_ref}</option>}
      {options.map(item => <option key={item.ref} value={item.ref}>{item.direction === 'outbound' ? 'Utgående' : 'Inngående'} · {item.name}{item.via ? ' · via ' + item.via : ''} · {item.ref}</option>)}
    </select></label>}
  </details>;
}

export function NoticeGeographyEditor({ value, set, ...search }: Search & {
  value: Geography | null | undefined; set: (value: Geography | null) => void;
}) {
  function kind(value: string) {
    if (value === 'line') return set(null);
    set({kind: value as Geography['kind'], direction: null, stops: [], cancelled: [], via: [], start: null, end: null, route_ref: null, area: value === 'area' ? '' : null});
  }
  const typed = value && value.kind !== 'area';
  return <fieldset className="notice-geography"><legend>Hvor gjelder avviket?</legend>
    <label>Avgrensning<select value={value?.kind ?? 'line'} onChange={event => kind(event.target.value)}>
      <option value="line">Linje eller hele bybussnettet</option><option value="stops">Holdeplasser eller plattformer</option>
      <option value="section">Fra–til-strekning</option><option value="area">Navngitt område</option>
    </select></label>
    {value?.kind === 'area' && <label>Område<input placeholder="Tromsø sentrum" maxLength={120} value={value.area ?? ''} onChange={event => set({...value, area: event.target.value})} /></label>}
    {typed && <label>Retning<select value={value.direction ?? ''} onChange={event => set({...value, direction: (event.target.value || null) as Geography['direction'], route_ref: null})}>
      <option value="">Begge retninger</option><option value="outbound">Utgående</option><option value="inbound">Inngående</option>
    </select></label>}
    {value?.kind === 'stops' && <>
      <StopPicker {...search} title="Berørte stopp eller plattformer" selected={value.stops} plural
        select={stops => set({...value, stops, cancelled: value.cancelled.filter(item => stops.some(target => item.ref === target.ref))})} />
      {value.stops.length > 0 && <fieldset><legend>Stopp som ikke betjenes</legend>{value.stops.map(item =>
        <label key={item.ref}><input type="checkbox" checked={value.cancelled.some(target => target.ref === item.ref)}
          onChange={event => set({...value, cancelled: event.target.checked ? [...value.cancelled,item] : value.cancelled.filter(target => target.ref !== item.ref)})} />{item.name} betjenes ikke</label>
      )}</fieldset>}
    </>}
    {value?.kind === 'section' && <>
      <StopPicker {...search} title="Fra stopp" selected={value.start ? [value.start] : []} select={stops => set({...value, start: stops[0] ?? null, route_ref: null})} />
      <StopPicker {...search} title="Til stopp" selected={value.end ? [value.end] : []} select={stops => set({...value, end: stops[0] ?? null, route_ref: null})} />
      <p>Legg til stopp i kjørerekkefølge hvis rutene mellom endepunktene går ulike veger.</p>
      <StopPicker {...search} title="Kjører via (valgfritt)" selected={value.via} plural select={via => set({...value, via})} />
      <RoutePicker key={[search.date,search.line,value.direction,value.start?.ref,value.end?.ref].join(' ')} {...search} value={value} set={set} />
      <StopPicker {...search} title="Stopp som ikke betjenes (valgfritt)" selected={value.cancelled} plural select={cancelled => set({...value, cancelled})} />
    </>}
  </fieldset>;
}
