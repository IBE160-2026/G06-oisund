import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { Plan } from './PrivateConfirmation';
import { PrivateDriving } from './PrivateDriving';
import { PrivateBus } from './PrivateBus';
import { PrivateShiftStart } from './PrivateShiftStart';
import { PrivateActivitySelection } from './PrivateActivitySelection';
import { ProgressScreens, useWorkdayProgress } from './PrivateWorkdayProgress';
import { osloDateTime } from './dayOverview';
import type { NoticeController } from './PrivateNotices';
import { PrivateNoticeReader } from './PrivateNoticeReader';
import { PrivateAutomaticNotices } from './PrivateAutomaticNotices';
import { createPositionAnchorContinuity } from './positionAnchorClient';

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
  const anchorContinuity = useMemo(createPositionAnchorContinuity, [plan.id]);
  const [readerOpen, setReaderOpen] = useState(false);
  const [automaticOpen, setAutomaticOpen] = useState(false);
  useEffect(() => { props.readerChanged(readerOpen || automaticOpen); return () => props.readerChanged(false); }, [readerOpen, automaticOpen]);
  const readerEntry = useRef<HTMLButtonElement>(null);
  const automaticEntry = useRef<HTMLButtonElement>(null);
  const [progressLocked, setProgressLocked] = useState(false);
  const [startReview, setStartReview] = useState(false);
  const [driving, setDriving] = useState(false);
  const [drivingInitialized, setDrivingInitialized] = useState(false);

  const lockProgress = useCallback((value: boolean) => { setProgressLocked(value); props.guardOutcome(value); }, [props.guardOutcome]);

  const progress = useWorkdayProgress({ id: plan.id, content: plan.draft, expiresAt: plan.expires_at, validPlan: props.validPlan, request: props.request, mutation: props.mutation, expired: props.expired, suspended: props.suspended, lock: lockProgress, shorten: props.shorten });
  useEffect(() => { if (startReview && progress.terminal) { setStartReview(false); progress.setScreen('recap'); } }, [startReview, progress.terminal]);
  const refresh = () => { void progress.load(); };
  const request = props.request;
  const mutation = async (path: string, body: object) => {
    try { const value = await props.mutation(path, body); refresh(); return value; }
    catch (error) { refresh(); throw error; }
  };
  const lifecycle = progress.snapshot?.lifecycle;
  const visible = props.planAvailable && !!progress.snapshot;
  const driveMounted = drivingInitialized && visible && !props.hidden && !props.suspended && lifecycle?.state === 'active';
  const openDriving = () => { setDrivingInitialized(true); setDriving(true); };
  useEffect(() => { if (progress.terminal) { setDriving(false); setDrivingInitialized(false); } }, [progress.terminal]);
  const notices = props.notices;
  const special = readerOpen || automaticOpen || progress.screen !== 'day' || startReview || notices.screen !== 'day';
  const noticeEntryAboveActivity = !props.activityOpen || notices.screen !== 'day';
  const startChanged = useCallback(() => { void progress.load(); }, [plan.id]);
  const startEntry = useRef<HTMLButtonElement>(null);
  const dayTitle = useRef<HTMLHeadingElement>(null);
  function readyToStart() {
    if (lifecycle?.state !== 'confirmed' || !startEntry.current) return false;
    requestAnimationFrame(() => startEntry.current?.focus());
    return true;
  }
  useEffect(() => { if (!props.hidden && !props.activityOpen && progress.screen === 'day') dayTitle.current?.focus(); }, [props.hidden, progress.screen]);
  function openActivity() { props.setActivityOpen(true); }
  const noticeEntry = <div className="controls" hidden={readerOpen || automaticOpen || startReview || progress.screen !== 'day'}><button ref={readerEntry} disabled={props.suspended || !visible} onClick={() => setReaderOpen(true)}>Les avvik for linjer og datoer</button><button ref={automaticEntry} disabled={props.suspended || !visible} onClick={() => setAutomaticOpen(true)}>Automatiske avvik</button></div>;
  return <section hidden={props.hidden} aria-label="Bekreftet plan">
    {driveMounted && lifecycle && <PrivateDriving visible={driving} plan={plan} lifecycle={lifecycle} request={request} mutation={props.mutation}
      expired={props.expired} anchorContinuity={anchorContinuity}
      back={() => { setDriving(false); window.setTimeout(() => dayTitle.current?.focus(), 0); }} />}
    <PrivateNoticeReader id={plan.id} expiresAt={plan.expires_at} open={readerOpen && !props.hidden} available={visible} suspended={props.suspended} request={props.request} expired={props.expired} shorten={props.shorten} back={() => { setReaderOpen(false); notices.navigate('day'); props.setActivityOpen(false); progress.setScreen('day'); window.setTimeout(() => readerEntry.current?.focus(), 0); }} maintenance={() => { setReaderOpen(false); if (notices.screen === 'day') notices.open(); else window.setTimeout(() => notices.title.current?.focus(), 0); }} />
    <PrivateAutomaticNotices plan={plan} open={automaticOpen && !props.hidden} available={visible} suspended={props.suspended} request={props.request} mutation={props.mutation} expired={props.expired} shorten={props.shorten} back={() => { setAutomaticOpen(false); if (notices.screen === 'day') window.setTimeout(() => automaticEntry.current?.focus(), 0); }} />
    <div hidden={readerOpen || automaticOpen || startReview || notices.screen !== 'day'}><ProgressScreens progress={progress} content={plan.draft} classifications={plan.classifications} suspended={props.suspended} showPreparation={props.showPreparation} showDay={() => { props.setActivityOpen(false); progress.setScreen('day'); }} leaveLocked={props.busy || props.busLocked || progressLocked} factsAvailable={visible} compact={props.activityOpen && progress.screen === 'day'} /></div>
    <div hidden={readerOpen || automaticOpen || notices.screen !== 'day' || progress.screen !== 'day' || props.activityOpen && !startReview || progress.terminal && !props.busLocked}><PrivateShiftStart id={plan.id} expiresAt={plan.expires_at} blocked={props.busy || props.busLocked || progressLocked || progress.busy} reviewing={startReview} review={setStartReview} startEntry={startEntry} plannedStart={plan.draft.activities[0].start!} request={request} mutation={mutation} readOnly={progress.terminal} suspended={props.suspended} expired={props.expired} lock={props.guardStart} availability={props.startAvailability} factsAvailable={visible} changed={startChanged} started={openDriving} shorten={props.shorten} /></div>
    {noticeEntryAboveActivity && noticeEntry}
    <div hidden={special}>
      <div hidden={props.activityOpen}><h2 ref={dayTitle} tabIndex={-1}>Dagen din</h2>{visible ? <><h3>Bekreftet plan · versjon {plan.source_revision}</h3><p>Historisk bekreftelse: {osloDateTime(plan.confirmed_at)}.</p><p>Siste aktivitetsslutt: {osloDateTime(plan.final_end)}. Utløper {osloDateTime(plan.expires_at)}. Fristen forlenges ikke.</p></> : <p>Planfakta er skjult til plantilgangen er kontrollert.</p>}
        {lifecycle?.state === 'active' && <div className="controls" aria-label="Aktivt skift">
          <button disabled={props.suspended || props.busLocked || progressLocked}
            onClick={openDriving}>Gjenoppta kjøring</button>
          <button disabled={!visible || progress.snapshot?.lifecycle.state !== 'active' || props.busLocked || progressLocked || progress.busy || props.suspended} onClick={e => void progress.beginClose('ended', e.currentTarget)}>Avslutt skift</button>
          <button disabled={!visible || progress.snapshot?.lifecycle.state !== 'active' || props.busLocked || progressLocked || progress.busy || props.suspended} onClick={e => void progress.beginClose('aborted', e.currentTarget)}>Avbryt skift</button>
        </div>}
        <div hidden={progress.terminal && !props.busLocked}><PrivateBus id={plan.id} expiresAt={plan.expires_at} request={request} mutation={mutation} readOnly={progress.terminal} suspended={props.suspended} expired={props.expired} lock={props.guardBus} availability={props.busAvailability} factsAvailable={visible} afterSave={readyToStart} shorten={props.shorten} /></div>
        {progress.terminal && visible && <><p>Skiftet er {progress.snapshot!.lifecycle.state === 'ended' ? 'avsluttet' : 'avbrutt'}. Dagen er skrivebeskyttet.</p><p>Fysisk buss: {progress.snapshot!.bus.physical_bus ?? 'Ukjent'}</p><button onClick={() => progress.setScreen('recap')}>Åpne oppsummering</button></>}
      </div>
      <PrivateActivitySelection id={plan.id} expiresAt={plan.expires_at} content={plan.draft} classifications={plan.classifications} finalEnd={plan.final_end} activityOpen={props.activityOpen} positionVisible={!special && !props.hidden} anchorContinuity={anchorContinuity} navigationLocked={props.dayNavigationLocked} openActivity={openActivity} backToDay={() => props.setActivityOpen(false)} request={request} mutation={mutation} suspended={props.suspended} expired={props.expired} lock={props.guardSelection} availability={props.selectionAvailability} factsAvailable={visible} shorten={props.shorten} progress={progress} />
      {!noticeEntryAboveActivity && noticeEntry}
    </div>

    <div hidden={special}>
      <div hidden={props.activityOpen}>{visible && <><p>Historiske fakta og godtatte ukjente opplysninger gjelder tidspunktet for bekreftelsen. Bussregistreringen gjelder nå.</p><details className="day-confirmed-details"><summary>Bekreftede detaljer og historisk kilde</summary>{props.historicalDetails}</details><details><summary>Godtatte ukjente fakta</summary><ul>{plan.unknowns.map(item => <li key={item.id}>{item.label}</li>)}</ul></details></>}
      </div>

      <div hidden={props.activityOpen}><button id="notice-entry-day" ref={notices.entry} disabled={props.suspended} onClick={notices.open}>Manuelt vedlikeholdte avvik</button>{(notices.dirty || notices.pending) && <p>Et avviksforslag eller uavklart forsøk er beholdt. Åpne avvik for å fortsette eller kontrollere.</p>}<div className="controls"><button disabled={!visible || props.busLocked || progressLocked || props.suspended} onClick={props.remove}>Slett bekreftet plan</button><button disabled={props.busy || props.suspended || props.busLocked || progressLocked} onClick={props.closeView}>Lukk planen</button></div><p>Lukk planen lukker bare visningen. Slett bekreftet plan er en egen personvernhandling.</p>
      </div>
    </div>
  </section>;
}
