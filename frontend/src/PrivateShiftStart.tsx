import { useEffect, useRef } from 'react';
import { osloDateTime } from './dayOverview';
import { useWorkdayResource, type ResourceProps } from './useWorkdayResource';
import { validLifecycle, type Lifecycle } from './PrivateWorkdayProgress';

export function PrivateShiftStart(props: ResourceProps & { plannedStart: string; factsAvailable: boolean; readOnly?: boolean; changed?: () => void; blocked: boolean; reviewing: boolean; review: (value: boolean) => void }) {
  const resource = useWorkdayResource<Lifecycle>(props, 'start', validLifecycle,
    v => v.state === 'active' && v.revision === 1);
  const { saved, pending, rejected, busy, message, load, send, resolve } = resource;
  const available = resource.available && props.factsAvailable;
  const status = useRef<HTMLParagraphElement>(null);
  const title = useRef<HTMLHeadingElement>(null), returnTo = useRef<HTMLButtonElement | null>(null);
  useEffect(() => { if (props.reviewing) title.current?.focus(); }, [props.reviewing]);
  function cancel() { props.review(false); window.setTimeout(() => returnTo.current?.focus(), 0); }
  useEffect(() => { if (saved) props.changed?.(); }, [saved?.revision]);
  useEffect(() => { if (message === 'Skiftstart er lagret.') status.current?.focus(); }, [message]);
  return <section className="private-shift-start" aria-label="Skiftstart">
    <div hidden={props.reviewing}>
    <h4>Skiftstart</h4>{available && <p>Planlagt start: {osloDateTime(props.plannedStart)}. Dette er første bekreftede aktivitetsstart.</p>}
    <p ref={status} tabIndex={-1} role="status" aria-label="Skiftstatus">{message}</p>
    <p><strong>{pending ? 'Skiftstart er uavklart' : saved && available ? saved.state === 'active' ? 'Startet manuelt' : ['ended', 'aborted'].includes(saved.state) ? 'Skiftet er avsluttet' : 'Ikke startet' : 'Skiftstatus er ukjent / utilgjengelig'}</strong></p>
    {saved && available && saved.started_at && <p>Faktisk start (lagret av serveren): {osloDateTime(saved.started_at)}</p>}
    <p>Skiftstart registreres bare ved en uttrykkelig manuell handling. Registreringen er ikke bevis på fysisk kjøring og velger eller fullfører ingen aktivitet.</p>
    {pending ? <div className="controls"><button disabled={busy || props.suspended} onClick={() => void send()}>Prøv samme skiftstart igjen</button><button disabled={busy || props.suspended} onClick={() => void send(undefined, true)}>Kontroller skiftstarten</button></div>
      : !props.readOnly && !rejected && saved && available && saved.state === 'confirmed' && <button disabled={busy || props.suspended || props.blocked} onClick={event => { returnTo.current = event.currentTarget; props.review(true); }}>Start skift</button>}
    {rejected && saved && <div className="controls"><button hidden={props.readOnly} disabled={!available || busy || props.suspended} onClick={() => void send()}>Prøv avvist skiftstart igjen</button><button disabled={busy || props.suspended} onClick={() => { resolve(saved, 'Avvist skiftstart er avbrutt. Lagret skiftstatus er uendret.'); status.current?.focus(); }}>Avbryt avvist skiftstart</button></div>}
    <button disabled={busy || props.suspended} onClick={() => void load()}>Hent skiftstatus igjen</button>
    </div>
    {props.reviewing && <section aria-label="Bekreft skiftstart"><h2 ref={title} tabIndex={-1}>Start skiftet?</h2><p>Start lagrer faktisk første start hos serveren. Valgt aktivitet og aktivitetsstatus endres ikke.</p>{available && <p>Planlagt start: {osloDateTime(props.plannedStart)}.</p>}<div className="controls"><button disabled={!available || props.readOnly || busy || props.blocked || props.suspended || saved?.state !== 'confirmed'} onClick={() => { props.review(false); void send(); }}>Bekreft skiftstart</button><button onClick={cancel}>Tilbake uten å starte</button></div></section>}
  </section>;
}
