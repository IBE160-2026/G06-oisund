import { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import type { Plan } from './PrivateConfirmation';
import { PrivateBus } from './PrivateBus';
import { PrivateShiftStart } from './PrivateShiftStart';
import { PrivateActivitySelection } from './PrivateActivitySelection';
import { ProgressScreens, useWorkdayProgress } from './PrivateWorkdayProgress';
import { osloDateTime } from './dayOverview';
import type { NoticeController } from './PrivateNotices';
import { PrivateNoticeReader } from './PrivateNoticeReader';

type Props = {
  plan: Plan; hidden: boolean; activityOpen: boolean; setActivityOpen: (value: boolean) => void;
  request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>;
  busy: boolean; suspended: boolean; expired: () => void; planAvailable: boolean; dayNavigationLocked: boolean; busLocked: boolean;
  guardBus: (value: boolean) => void; guardSelection: (value: boolean) => void; guardStart: (value: boolean) => void; guardOutcome: (value: boolean) => void;
  notices: NoticeController; readerChanged: (value: boolean) => void;
  busAvailability: (value: boolean) => void; selectionAvailability: (value: boolean) => void; startAvailability: (value: boolean) => void;
  remove: () => void; closeView: () => void; showPreparation: () => void; shorten: (value: string) => void;
  validPlan: (value: any) => boolean; historicalDetails: ReactNode;
};
export function PrivateWorkdayView(props: Props) {
  const { plan } = props;
  const [readerOpen, setReaderOpen] = useState(false);
  useEffect(() => { props.readerChanged(readerOpen); return () => props.readerChanged(false); }, [readerOpen]);
  const readerEntry = useRef<HTMLButtonElement>(null);
  const [progressLocked, setProgressLocked] = useState(false);
  const [startReview, setStartReview] = useState(false);

  const lockProgress = useCallback((value: boolean) => { setProgressLocked(value); props.guardOutcome(value); }, [props.guardOutcome]);

  const progress = useWorkdayProgress({ id: plan.id, content: plan.draft, expiresAt: plan.expires_at, validPlan: props.validPlan, request: props.request, mutation: props.mutation, expired: props.expired, suspended: props.suspended, lock: lockProgress, shorten: props.shorten });
  useEffect(() => { if (startReview && progress.terminal) { setStartReview(false); progress.setScreen('recap'); } }, [startReview, progress.terminal]);
  const refresh = () => { void progress.load(); };
  const request = props.request;
  const mutation = async (path: string, body: object) => {
    try { const value = await props.mutation(path, body); refresh(); return value; }
    catch (error) { refresh(); throw error; }
  };
  const visible = props.planAvailable && !!progress.snapshot;
  const notices = props.notices;
  const special = readerOpen || progress.screen !== 'day' || startReview || notices.screen !== 'day';
  const startChanged = useCallback(() => { void progress.load(); }, [plan.id]);
  const dayTitle = useRef<HTMLHeadingElement>(null);
  useEffect(() => { if (!props.hidden && !props.activityOpen && progress.screen === 'day') dayTitle.current?.focus(); }, [props.hidden, progress.screen]);
  function openActivity() { props.setActivityOpen(true); }
  return <section hidden={props.hidden} aria-label="Bekreftet plan">
    <PrivateNoticeReader id={plan.id} expiresAt={plan.expires_at} open={readerOpen && !props.hidden} available={visible} suspended={props.suspended} request={props.request} expired={props.expired} shorten={props.shorten} back={() => { setReaderOpen(false); notices.navigate('day'); props.setActivityOpen(false); progress.setScreen('day'); window.setTimeout(() => readerEntry.current?.focus(), 0); }} maintenance={() => { setReaderOpen(false); if (notices.screen === 'day') notices.open(); else window.setTimeout(() => notices.title.current?.focus(), 0); }} />
    <div hidden={readerOpen || startReview || notices.screen !== 'day'}><ProgressScreens progress={progress} content={plan.draft} classifications={plan.classifications} suspended={props.suspended} showPreparation={props.showPreparation} showDay={() => { props.setActivityOpen(false); progress.setScreen('day'); }} leaveLocked={props.busy || props.busLocked || progressLocked} factsAvailable={visible} compact={props.activityOpen && progress.screen === 'day'} /></div>
    <div hidden={readerOpen || startReview || progress.screen !== 'day'}><button ref={readerEntry} disabled={props.suspended || !visible} onClick={() => setReaderOpen(true)}>Les avvik for linjer og datoer</button></div>
    <div hidden={special}>
      <div hidden={props.activityOpen}><h2 ref={dayTitle} tabIndex={-1}>Dagen din</h2>{visible ? <><h3>Bekreftet plan · versjon {plan.source_revision}</h3><p>Historisk bekreftelse: {osloDateTime(plan.confirmed_at)}.</p><p>Siste aktivitetsslutt: {osloDateTime(plan.final_end)}. Utløper {osloDateTime(plan.expires_at)}. Fristen forlenges ikke.</p></> : <p>Planfakta er skjult til plantilgangen er kontrollert.</p>}
        <div hidden={progress.terminal && !props.busLocked}><PrivateBus id={plan.id} expiresAt={plan.expires_at} request={request} mutation={mutation} readOnly={progress.terminal} suspended={props.suspended} expired={props.expired} lock={props.guardBus} availability={props.busAvailability} factsAvailable={visible} shorten={props.shorten} /></div>
        {progress.terminal && visible && <><p>Skiftet er {progress.snapshot!.lifecycle.state === 'ended' ? 'avsluttet' : 'avbrutt'}. Dagen er skrivebeskyttet.</p><p>Fysisk buss: {progress.snapshot!.bus.physical_bus ?? 'Ukjent'}</p><button onClick={() => progress.setScreen('recap')}>Åpne oppsummering</button></>}
      </div>
      <PrivateActivitySelection id={plan.id} expiresAt={plan.expires_at} content={plan.draft} classifications={plan.classifications} finalEnd={plan.final_end} activityOpen={props.activityOpen} navigationLocked={props.dayNavigationLocked} openActivity={openActivity} backToDay={() => props.setActivityOpen(false)} request={request} mutation={mutation} suspended={props.suspended} expired={props.expired} lock={props.guardSelection} availability={props.selectionAvailability} factsAvailable={visible} shorten={props.shorten} progress={progress} />
    </div>
    <div hidden={readerOpen || notices.screen !== 'day' || progress.screen !== 'day' || progress.terminal && !props.busLocked}><PrivateShiftStart id={plan.id} expiresAt={plan.expires_at} blocked={props.busy || props.busLocked || progressLocked || progress.busy} reviewing={startReview} review={setStartReview} plannedStart={plan.draft.activities[0].start!} request={request} mutation={mutation} readOnly={progress.terminal} suspended={props.suspended} expired={props.expired} lock={props.guardStart} availability={props.startAvailability} factsAvailable={visible} changed={startChanged} shorten={props.shorten} /></div>
    <div hidden={special}>
      <div hidden={props.activityOpen}>{visible && <><p>Historiske fakta og godtatte ukjente opplysninger gjelder tidspunktet for bekreftelsen. Bussregistreringen gjelder nå.</p><details className="day-confirmed-details"><summary>Bekreftede detaljer og historisk kilde</summary>{props.historicalDetails}</details><details><summary>Godtatte ukjente fakta</summary><ul>{plan.unknowns.map(item => <li key={item.id}>{item.label}</li>)}</ul></details></>}
      </div>
        {!progress.terminal && <><p>{progress.snapshot?.lifecycle.state !== 'active' ? 'Start skiftet før du avslutter eller avbryter.' : 'Avslutning og avbrudd krever en egen bekreftelse.'}</p>{progressLocked && <p>Gå tilbake til aktivitetsstatusen og lagre, avbryt et ulagret forslag eller kontroller det uavklarte forsøket før avslutning.</p>}<div className="controls"><button disabled={!visible || progress.snapshot?.lifecycle.state !== 'active' || props.busLocked || progressLocked || progress.busy || props.suspended} onClick={e => void progress.beginClose('ended', e.currentTarget)}>Avslutt skift</button><button disabled={!visible || progress.snapshot?.lifecycle.state !== 'active' || props.busLocked || progressLocked || progress.busy || props.suspended} onClick={e => void progress.beginClose('aborted', e.currentTarget)}>Avbryt skift</button></div></>}
      <div hidden={props.activityOpen}><button id="notice-entry-day" ref={notices.entry} disabled={props.suspended} onClick={notices.open}>Manuelt vedlikeholdte avvik</button>{(notices.dirty || notices.pending) && <p>Et avviksforslag eller uavklart forsøk er beholdt. Åpne avvik for å fortsette eller kontrollere.</p>}<div className="controls"><button disabled={!visible || props.busLocked || progressLocked || props.suspended} onClick={props.remove}>Slett bekreftet plan</button><button disabled={props.busy || props.suspended || props.busLocked || progressLocked} onClick={props.closeView}>Lukk planen</button></div><p>Lukk planen lukker bare visningen. Slett bekreftet plan er en egen personvernhandling.</p>
      </div>
    </div>
  </section>;
}
