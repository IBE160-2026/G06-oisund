import { useEffect, useRef, useState } from 'react';

type Resolution = { state: 'resolved' | 'ambiguous' | 'gap'; candidates: string[] };
type Props = { label: 'Start' | 'Slutt'; value: string | null; defaultDate: string | null; disabled: boolean;
  resolve: (body: object) => Promise<unknown>; onValue: (value: string | null) => void;
  onState: (dirty: boolean, unresolved: boolean) => void; expired: () => void };
const parts = (value: string | null, day: string | null) => ({ date: value?.slice(0, 10) ?? day ?? '', clock: value?.match(/T(\d{2}:\d{2}(?::\d{2})?)/)?.[1] ?? '' });

export function PrivateTimeInput(props: Props) {
  const original = useRef({ value: props.value, ...parts(props.value, props.defaultDate) }).current;
  const [date, setDate] = useState(original.date), [clock, setClock] = useState(original.clock);
  const [touched, setTouched] = useState(false), [selected, setSelected] = useState(props.value);
  const [options, setOptions] = useState<string[]>([]);
  const [state, setState] = useState(props.value ? 'saved' : 'empty');
  const [retry, setRetry] = useState(0);
  const callbacks = useRef(props); callbacks.current = props;
  const generation = useRef(0);
  const unresolved = !['saved', 'empty', 'resolved'].includes(state);
  const dirty = touched && (date !== original.date || clock !== original.clock || selected !== original.value);
  useEffect(() => { callbacks.current.onState(dirty, unresolved); }, [dirty, unresolved]);
  useEffect(() => {
    if (!touched && !selected && !clock) setDate(props.defaultDate ?? '');
  }, [props.defaultDate, touched, clock, selected]);
  useEffect(() => {
    if (!touched || props.disabled) return;
    const current = ++generation.current;
    let active = true;
    setOptions([]);
    if (!date && !clock) { setState('empty'); return; }
    if (!date || !clock) { setState('incomplete'); return; }
    setState('resolving');
    const timer = window.setTimeout(() => {
      void callbacks.current.resolve({ calendar_date: date, clock }).then(raw => {
        if (!active || current !== generation.current) return;
        const value = raw as Resolution;
        if (!value || !Array.isArray(value.candidates) || value.candidates.length > 2
          || !value.candidates.every(v => typeof v === 'string' && v.startsWith(date + 'T' + clock) && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?[+-]\d{2}:\d{2}$/.test(v) && Number.isFinite(Date.parse(v)))
          || !(['gap', 'resolved', 'ambiguous'][value.candidates.length] === value.state)
          || new Set(value.candidates).size !== value.candidates.length
          || (value.candidates.length === 2 && Date.parse(value.candidates[0]) >= Date.parse(value.candidates[1]))) throw Error();
        setOptions(value.candidates);
        setState(value.state === 'ambiguous' && selected && value.candidates.includes(selected) ? 'resolved' : value.state);
        if (value.state === 'resolved') { setSelected(value.candidates[0]); callbacks.current.onValue(value.candidates[0]); }
      }).catch((error: any) => {
        if (!active || current !== generation.current) return;
        if (error?.status === 401) { callbacks.current.expired(); return; }
        setState(error?.status === 422 ? 'invalid' : 'unavailable');
      });
    }, 150);
    return () => { active = false; clearTimeout(timer); };
  }, [date, clock, touched, retry, props.disabled]);
  function change(day: string, time: string) {
    generation.current++;
    setDate(day); setClock(time); setTouched(true); setSelected(null); setOptions([]);
    setState(!day && !time ? 'empty' : 'incomplete'); callbacks.current.onState(true, !!(day || time)); callbacks.current.onValue(null);
  }
  function nextDay() {
    const base = date || props.defaultDate;
    if (!base) return;
    const next = new Date(base + 'T12:00:00Z'); next.setUTCDate(next.getUTCDate() + 1);
    if (Number.isFinite(next.getTime()) && next.getUTCFullYear() <= 9999) change(next.toISOString().slice(0, 10), clock);
  }
  const messages: Record<string, string> = { empty: 'Klokkeslett er ukjent.', saved: 'Lagret tidspunkt i Oslo-tid.', resolved: 'Tidspunktet er klart i Oslo-tid.', incomplete: 'Fyll ut både dato og klokkeslett, eller tøm tidspunktet.', resolving: 'Kontrollerer Oslo-tid …', gap: 'Dette klokkeslettet finnes ikke i Oslo når klokken stilles frem. Velg et annet tidspunkt.', ambiguous: 'Dette klokkeslettet forekommer to ganger. Velg første eller andre forekomst.', invalid: 'Kontroller dato og klokkeslett.', unavailable: 'Tidspunktet kunne ikke kontrolleres. Inndata er beholdt. Prøv igjen.' };
  return <fieldset disabled={props.disabled}><legend>{props.label} (Oslo-tid)</legend>
    <label>{props.label}dato<input type="date" value={date} onChange={e => change(e.target.value, clock)} /></label>
    <label>{props.label === 'Start' ? 'Starttid' : 'Sluttid'}<input type="time" step="1" value={clock} onChange={e => change(date, e.target.value)} /></label>
    <div className="controls"><button type="button" disabled={!date && !props.defaultDate} onClick={nextDay}>{props.label}: neste dag</button>
      <button type="button" onClick={() => { generation.current++; setDate(props.defaultDate ?? ''); setClock(''); setTouched(false); setSelected(null); setOptions([]); setState('empty'); callbacks.current.onState(false, false); callbacks.current.onValue(null); }}>{props.label}: tøm tidspunkt</button></div>
    {options.length === 2 && <label>{props.label}: forekomst<select aria-label={props.label + ': forekomst'} value={selected ?? ''} onChange={e => { if (options.includes(e.target.value)) { setSelected(e.target.value); setState('resolved'); callbacks.current.onValue(e.target.value); } }}><option value="" disabled>Velg forekomst</option><option value={options[0]}>Første forekomst</option><option value={options[1]}>Andre forekomst</option></select></label>}
    <p aria-live="polite">{messages[state]}</p>
    {state === 'unavailable' && <button type="button" onClick={() => setRetry(value => value + 1)}>Kontroller {props.label.toLowerCase()}tid igjen</button>}
  </fieldset>;
}
