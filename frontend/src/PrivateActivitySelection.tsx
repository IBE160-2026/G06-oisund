import { useEffect, useRef, useState } from 'react';
import type { Content } from './PrivateDrafts';
import { activityChoiceLabel } from './activityChoiceLabel';
import { PrivateDayOverview } from './PrivateDayOverview';
import { SelectedActivityDetails } from './SelectedActivityDetails';
import { useWorkdayResource, type ResourceProps } from './useWorkdayResource';
import { OutcomeEditor, type Progress } from './PrivateWorkdayProgress';

type Selection = { workday_id: string; activity_id: string | null; revision: number; expires_at: string };
type Props = ResourceProps & { content: Content; classifications: Record<string, string>; finalEnd: string; factsAvailable: boolean; activityOpen: boolean; openActivity: () => void; backToDay: () => void; navigationLocked: boolean; progress: Progress };
export function PrivateActivitySelection(props: Props) {
  const { content, classifications } = props;
  const [consulted, setConsulted] = useState<string | null>(null);
  const r = useWorkdayResource<Selection>(props, 'selection', v => Object.keys(v).sort().join() === 'activity_id,expires_at,revision,workday_id'
    && (v.activity_id === null && v.revision === 0 || v.revision > 0 && typeof v.activity_id === 'string' && content.activities.some(a => a.id === v.activity_id)),
    (v, op) => v.revision === op.expected_revision + 1 && v.activity_id === op.activity_id);
  const { saved, comparison, pending, proposal, rejected, busy, available, message, load, send, resolve, adoptCurrent } = r;
  const status = useRef<HTMLParagraphElement>(null);
  const requestedOpen = useRef(false);
  const returnFocus = useRef(false);
  const day = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (message === 'Aktivitetsvalget er lagret.' && requestedOpen.current) {
      requestedOpen.current = false;
      // Another day controller may have acquired unsaved input or recovery
      // while this reply was in flight. Keep that controller reachable.
      if (!props.navigationLocked) { if (props.activityOpen) status.current?.focus(); else props.openActivity(); }
    }
  }, [message]);
  useEffect(() => {
    if (props.activityOpen && !props.navigationLocked) status.current?.focus();
    if (!props.activityOpen && returnFocus.current) {
      returnFocus.current = false;
      const target = day.current?.querySelector<HTMLButtonElement>('[data-open-activity]');
      let ancestor = target?.parentElement;
      while (ancestor && ancestor !== day.current) { if (ancestor instanceof HTMLDetailsElement) ancestor.open = true; ancestor = ancestor.parentElement; }
      if (target && !target.disabled) target.focus(); else status.current?.focus();
    }
  }, [props.activityOpen]);
  const back = () => { requestedOpen.current = false; returnFocus.current = true; props.backToDay(); };
  const visible = available && props.factsAvailable;
  const selected = (props.progress.terminal ? consulted : null) ?? saved?.activity_id ?? null, index = content.activities.findIndex(a => a.id === selected);
  const disabled = busy || !!pending || !!comparison || rejected || props.suspended || props.navigationLocked || !saved || !visible;
  const label = (id: string) => activityChoiceLabel(content.activities.find(a => a.id === id), classifications[id]);
  const choose = (id: string) => { if (!disabled && id !== selected) { if (props.progress.terminal) { setConsulted(id); props.openActivity(); } else { requestedOpen.current = true; void send(id); } } };
  return <>
    <section className="private-activity-selection" aria-label="Aktivitetsvalg">
      {!props.activityOpen && <h4>Manuelt aktivitetsvalg</h4>}<p ref={status} tabIndex={-1} role="status" aria-label="Aktivitetsvalgstatus">{message}</p>

      <div className="controls">{props.activityOpen && <button onClick={back}>Tilbake til dagen</button>}<button disabled={disabled || index <= 0} onClick={() => choose(content.activities[index - 1].id)}>{index < 0 ? 'Velg en aktivitet først' : index === 0 ? 'Ingen forrige aktivitet' : 'Forrige aktivitet'}</button><button disabled={disabled || index < 0 || index === content.activities.length - 1} onClick={() => choose(content.activities[index + 1].id)}>{index < 0 ? 'Velg en aktivitet først' : index === content.activities.length - 1 ? 'Ingen neste aktivitet' : 'Neste aktivitet'}</button></div>
      {visible && saved ? selected ? props.activityOpen ? <><SelectedActivityDetails readOnly={props.progress.terminal} content={content} classifications={classifications} activityId={selected} /><OutcomeEditor progress={props.progress} activityId={selected} suspended={props.suspended || props.navigationLocked || busy || !!pending || !!comparison || rejected} /></> : <><p>{props.progress.terminal ? 'Lesevisning' : 'Manuelt valgt'} · Aktivitet {index + 1} av {content.activities.length}</p><button disabled={disabled} onClick={props.openActivity}>Åpne valgt aktivitet</button></> : <p><strong>Ingen aktivitet valgt</strong></p> : <p>Lagret aktivitetsvalg kan ikke bekreftes.</p>}
      {proposal?.activity_id && <p>Lokalt forslag (ikke gjeldende lagret valg): {label(proposal.activity_id)}</p>}
      {comparison && <div className="import-warning">{visible && <p>Gjeldende lagret valg: {comparison.activity_id ? label(comparison.activity_id) : 'Ingen aktivitet valgt'}</p>}<button disabled={busy || props.suspended} onClick={async () => { await adoptCurrent('Lagret aktivitetsvalg er lastet inn. Det lokale forslaget er fjernet.'); status.current?.focus(); }}>Last inn lagret aktivitetsvalg</button></div>}
      {pending && <div className="controls"><button disabled={busy || props.suspended} onClick={() => void send()}>Prøv samme aktivitetsvalg igjen</button><button disabled={busy || props.suspended} onClick={() => void send(undefined, true)}>Kontroller aktivitetsvalget</button></div>}
      {rejected && saved && <div className="controls"><button disabled={!visible || busy || props.suspended} onClick={() => void send(proposal?.activity_id)}>Prøv avvist aktivitetsvalg igjen</button><button disabled={busy || props.suspended} onClick={() => { resolve(saved, 'Avvist aktivitetsvalg er avbrutt. Lagret valg er uendret.'); status.current?.focus(); }}>Avbryt avvist aktivitetsvalg</button></div>}
      <button disabled={busy || props.suspended || !!comparison} onClick={() => void load()}>Kontroller plantilgang og aktivitetsvalg</button>
    </section>
    {visible && <div ref={day} hidden={props.activityOpen}><PrivateDayOverview content={content} classifications={classifications} finalEnd={props.finalEnd} expiresAt={props.expiresAt} selectedId={selected} openSelected={props.openActivity} openDisabled={props.navigationLocked || props.suspended} choose={choose} selectionDisabled={disabled} outcomes={props.progress.snapshot?.outcomes.outcomes} readOnly={props.progress.terminal} /></div>}
  </>;
}
