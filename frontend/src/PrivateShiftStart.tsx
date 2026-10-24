import { useEffect, useRef } from 'react';
import { osloDateTime } from './dayOverview';
import { useWorkdayResource, type ResourceProps } from './useWorkdayResource';

type Lifecycle = { workday_id: string; state: 'confirmed' | 'active'; started_at: string | null; revision: number; expires_at: string };
export function PrivateShiftStart(props: ResourceProps & { plannedStart: string; factsAvailable: boolean }) {
  const resource = useWorkdayResource<Lifecycle>(props, 'start', v => Object.keys(v).sort().join() === 'expires_at,revision,started_at,state,workday_id'
    && (v.state === 'confirmed' && v.revision === 0 && v.started_at === null || v.state === 'active' && v.revision === 1 && typeof v.started_at === 'string' && Number.isFinite(Date.parse(v.started_at)) && Date.parse(v.started_at) < Date.parse(v.expires_at)),
    v => v.state === 'active' && v.revision === 1);
  const { saved, pending, rejected, busy, message, load, send, resolve } = resource;
  const available = resource.available && props.factsAvailable;
  const status = useRef<HTMLParagraphElement>(null);
  useEffect(() => { if (message === 'Skiftstart er lagret.') status.current?.focus(); }, [message]);
  return <section className="private-shift-start" aria-label="Skiftstart">
    <h4>Skiftstart</h4>{available && <p>Planlagt start: {osloDateTime(props.plannedStart)}. Dette er første bekreftede aktivitetsstart.</p>}
    <p ref={status} tabIndex={-1} role="status" aria-label="Skiftstatus">{message}</p>
    <p><strong>{pending ? 'Skiftstart er uavklart' : saved && available ? saved.state === 'active' ? 'Startet manuelt' : 'Ikke startet' : 'Skiftstatus er ukjent / utilgjengelig'}</strong></p>
    {saved && available && saved.started_at && <p>Faktisk start (lagret av serveren): {osloDateTime(saved.started_at)}</p>}
    <p>Skiftstart registreres bare ved en uttrykkelig manuell handling. Registreringen er ikke bevis på fysisk kjøring og velger eller fullfører ingen aktivitet.</p>
    {pending ? <div className="controls"><button disabled={busy || props.suspended} onClick={() => void send()}>Prøv samme skiftstart igjen</button><button disabled={busy || props.suspended} onClick={() => void send(undefined, true)}>Kontroller skiftstarten</button></div>
      : !rejected && saved && available && saved.state === 'confirmed' && <button disabled={busy || props.suspended} onClick={() => void send()}>Start skift</button>}
    {rejected && saved && <div className="controls"><button disabled={busy || props.suspended} onClick={() => void send()}>Prøv avvist skiftstart igjen</button><button disabled={busy || props.suspended} onClick={() => { resolve(saved, 'Avvist skiftstart er avbrutt. Lagret skiftstatus er uendret.'); status.current?.focus(); }}>Avbryt avvist skiftstart</button></div>}
    <button disabled={busy || props.suspended} onClick={() => void load()}>Hent skiftstatus igjen</button>
  </section>;
}
