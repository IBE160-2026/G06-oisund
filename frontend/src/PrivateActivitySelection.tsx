import { useEffect, useRef } from 'react';
import type { Content } from './PrivateDrafts';
import { activityChoiceLabel } from './activityChoiceLabel';
import { PrivateDayOverview } from './PrivateDayOverview';
import { useWorkdayResource, type ResourceProps } from './useWorkdayResource';

type Selection = { workday_id: string; activity_id: string | null; revision: number; expires_at: string };
type Props = ResourceProps & { content: Content; classifications: Record<string, string>; finalEnd: string; factsAvailable: boolean };
export function PrivateActivitySelection(props: Props) {
  const { content, classifications } = props;
  const r = useWorkdayResource<Selection>(props, 'selection', v => Object.keys(v).sort().join() === 'activity_id,expires_at,revision,workday_id'
    && (v.activity_id === null && v.revision === 0 || v.revision > 0 && typeof v.activity_id === 'string' && content.activities.some(a => a.id === v.activity_id)),
    (v, op) => v.revision === op.expected_revision + 1 && v.activity_id === op.activity_id);
  const { saved, comparison, pending, proposal, rejected, busy, available, message, load, send, resolve } = r;
  const status = useRef<HTMLParagraphElement>(null);
  useEffect(() => { if (message === 'Aktivitetsvalget er lagret.') status.current?.focus(); }, [message]);
  const visible = available && props.factsAvailable;
  const selected = saved?.activity_id ?? null, index = content.activities.findIndex(a => a.id === selected);
  const disabled = busy || !!pending || !!comparison || rejected || props.suspended || !saved || !visible;
  const label = (id: string) => activityChoiceLabel(content.activities.find(a => a.id === id), classifications[id]);
  const choose = (id: string) => { if (!disabled && id !== selected) void send(id); };
  return <>
    <section className="private-activity-selection" aria-label="Aktivitetsvalg">
      <h4>Manuelt aktivitetsvalg</h4><p ref={status} tabIndex={-1} role="status" aria-label="Aktivitetsstatus">{message}</p>
      {visible && saved ? selected ? <div className="selected-activity"><h3>{(classifications[selected] ?? content.activities[index]?.type) === 'trip' ? 'Valgt tur' : 'Valgt aktivitet'}</h3><p><strong>Manuelt valgt · Aktivitet {index + 1} av {content.activities.length}</strong></p><p>{label(selected)}</p></div> : <p><strong>Ingen aktivitet valgt</strong></p> : <p>Lagret aktivitetsvalg kan ikke bekreftes.</p>}
      {proposal?.activity_id && <p>Lokalt forslag (ikke gjeldende lagret valg): {label(proposal.activity_id)}</p>}
      {comparison && visible && <div className="import-warning"><p>Gjeldende lagret valg: {comparison.activity_id ? label(comparison.activity_id) : 'Ingen aktivitet valgt'}</p><button disabled={busy || props.suspended} onClick={() => { resolve(comparison, 'Lagret aktivitetsvalg er lastet inn. Det lokale forslaget er fjernet.'); status.current?.focus(); }}>Last inn lagret aktivitetsvalg</button></div>}
      <div className="controls"><button disabled={disabled || index <= 0} onClick={() => choose(content.activities[index - 1].id)}>{index < 0 ? 'Velg en aktivitet først' : index === 0 ? 'Ingen forrige aktivitet' : 'Forrige aktivitet'}</button><button disabled={disabled || index < 0 || index === content.activities.length - 1} onClick={() => choose(content.activities[index + 1].id)}>{index < 0 ? 'Velg en aktivitet først' : index === content.activities.length - 1 ? 'Ingen neste aktivitet' : 'Neste aktivitet'}</button></div>
      {pending && <div className="controls"><button disabled={busy || props.suspended} onClick={() => void send()}>Prøv samme aktivitetsvalg igjen</button><button disabled={busy || props.suspended} onClick={() => void send(undefined, true)}>Kontroller aktivitetsvalget</button></div>}
      {rejected && saved && <div className="controls"><button disabled={busy || props.suspended} onClick={() => void send(proposal?.activity_id)}>Prøv avvist aktivitetsvalg igjen</button><button disabled={busy || props.suspended} onClick={() => { resolve(saved, 'Avvist aktivitetsvalg er avbrutt. Lagret valg er uendret.'); status.current?.focus(); }}>Avbryt avvist aktivitetsvalg</button></div>}
      <button disabled={busy || props.suspended || !!comparison} onClick={() => void load()}>Kontroller plantilgang og aktivitetsvalg</button>
    </section>
    {visible && <PrivateDayOverview content={content} classifications={classifications} finalEnd={props.finalEnd} expiresAt={props.expiresAt} selectedId={selected} choose={choose} selectionDisabled={disabled} />}
  </>;
}
