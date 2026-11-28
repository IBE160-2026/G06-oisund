import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { Plan } from './PrivateConfirmation';
import { PrivateDriving } from './PrivateDriving';
import { PrivateBus } from './PrivateBus';
import { PrivateShiftStart } from './PrivateShiftStart';
import { PrivateDayOverview } from './PrivateDayOverview';
import { PrivateDayTools } from './PrivateDayTools';
import { PrivateTourCorrection } from './PrivateTourCorrection';
import { PrivateWeather } from './PrivateWeather';
import { referenceDestination, useFrozenRouteReferences } from './PrivateRouteReference';
import { ProgressScreens, useWorkdayProgress } from './PrivateWorkdayProgress';
import { osloDateTime } from './dayOverview';
import type { NoticeController } from './PrivateNotices';
import { PrivateNoticeReader } from './PrivateNoticeReader';
import { PrivateAutomaticNotices } from './PrivateAutomaticNotices';
import { createPositionAnchorContinuity, type SavedStopAnchor } from './positionAnchorClient';

type Props = {
  plan: Plan; hidden: boolean; activitiesOpen: boolean; toggleActivities: () => void;
  request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>;
  busy: boolean; suspended: boolean; expired: () => void; planAvailable: boolean; busLocked: boolean;
  guardBus: (value: boolean) => void; guardSelection: (value: boolean) => void; guardStart: (value: boolean) => void; guardOutcome: (value: boolean) => void;
  notices: NoticeController; readerChanged: (value: boolean) => void;
  busAvailability: (value: boolean) => void; startAvailability: (value: boolean) => void;
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
  const [correction, setCorrection] = useState<SavedStopAnchor>();

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
  const driveMounted = driving && visible && !props.hidden && !props.suspended && lifecycle?.state === 'active';
  const openDriving = () => setDriving(true);
  useEffect(() => { if (progress.terminal) setDriving(false); }, [progress.terminal]);
  const notices = props.notices;
  const special = readerOpen || automaticOpen || progress.screen !== 'day' || startReview || notices.screen !== 'day';
  const startChanged = useCallback(() => { void progress.load(); }, [plan.id]);
  const startEntry = useRef<HTMLButtonElement>(null);
  const dayTitle = useRef<HTMLHeadingElement>(null);
  function readyToStart() {
    if (lifecycle?.state !== 'confirmed' || !startEntry.current) return false;
    requestAnimationFrame(() => startEntry.current?.focus());
    return true;
  }
  useEffect(() => { if (!props.hidden && progress.screen === 'day') dayTitle.current?.focus(); }, [props.hidden, progress.screen]);
  const routes = useFrozenRouteReferences({workdayId:plan.id, serviceDate:plan.draft.service_date, expiresAt:plan.expires_at,
    request, expired:props.expired, available:visible && !props.hidden && props.activitiesOpen});
  const destinations = new Map(routes.references.map(reference => [reference.activity_id, referenceDestination(reference)]));
  return <section hidden={props.hidden} aria-label="Bekreftet plan">
    {driveMounted && lifecycle && <PrivateDriving visible={driving} plan={plan} lifecycle={lifecycle} request={request} mutation={props.mutation}
      expired={props.expired} anchorContinuity={anchorContinuity} correction={correction}
      back={() => { setDriving(false); window.setTimeout(() => dayTitle.current?.focus(), 0); }} />}
    <PrivateNoticeReader id={plan.id} expiresAt={plan.expires_at} open={readerOpen && !props.hidden} available={visible} suspended={props.suspended} request={props.request} expired={props.expired} shorten={props.shorten} back={() => { setReaderOpen(false); notices.navigate('day'); progress.setScreen('day'); window.setTimeout(() => readerEntry.current?.focus(), 0); }} maintenance={() => { setReaderOpen(false); if (notices.screen === 'day') notices.open(); else window.setTimeout(() => notices.title.current?.focus(), 0); }} />
    <PrivateAutomaticNotices plan={plan} open={automaticOpen && !props.hidden} available={visible} suspended={props.suspended} request={props.request} mutation={props.mutation} expired={props.expired} shorten={props.shorten} back={() => { setAutomaticOpen(false); if (notices.screen === 'day') window.setTimeout(() => automaticEntry.current?.focus(), 0); }} />
    <div hidden={readerOpen || automaticOpen || startReview || notices.screen !== 'day'}><ProgressScreens progress={progress} content={plan.draft} classifications={plan.classifications} suspended={props.suspended} showPreparation={props.showPreparation} showDay={() => { progress.setScreen('day'); }} leaveLocked={props.busy || props.busLocked || progressLocked} factsAvailable={visible} compact={progress.screen === 'day'} /></div>
    <div hidden={special}>
      <header className="workday-heading"><div><h2 ref={dayTitle} tabIndex={-1}>Dagen din</h2>
        {visible ? <p>Bekreftet plan · {plan.draft.service_date} · versjon {plan.source_revision}</p> : <p>Kontrollerer plantilgang …</p>}
        </div><PrivateWeather request={request} open={!special && !props.hidden && !props.suspended}/></header>
    </div>
    <div hidden={readerOpen || automaticOpen || notices.screen !== 'day' || progress.screen !== 'day' || progress.terminal && !props.busLocked}><PrivateShiftStart id={plan.id} expiresAt={plan.expires_at} blocked={props.busy || props.busLocked || progressLocked || progress.busy} reviewing={startReview} review={setStartReview} startEntry={startEntry} plannedStart={plan.draft.activities[0].start!} request={request} mutation={mutation} readOnly={progress.terminal} suspended={props.suspended} expired={props.expired} lock={props.guardStart} availability={props.startAvailability} factsAvailable={visible} changed={startChanged} started={openDriving} shorten={props.shorten} /></div>
    <div hidden={special}>
      <div>
        {lifecycle?.state === 'active' && <div className="controls" aria-label="Aktivt skift">
          <button disabled={props.suspended || props.busLocked || progressLocked}
            onClick={openDriving}>Gjenoppta kjøring</button>
          <button disabled={!visible || progress.snapshot?.lifecycle.state !== 'active' || props.busLocked || progressLocked || progress.busy || props.suspended} onClick={e => void progress.beginClose('ended', e.currentTarget)}>Avslutt skift</button>
          <button disabled={!visible || progress.snapshot?.lifecycle.state !== 'active' || props.busLocked || progressLocked || progress.busy || props.suspended} onClick={e => void progress.beginClose('aborted', e.currentTarget)}>Avbryt skift</button>
        </div>}

        {progress.terminal && visible && <><p>Skiftet er {progress.snapshot!.lifecycle.state === 'ended' ? 'avsluttet' : 'avbrutt'}. Dagen er skrivebeskyttet.</p><p>Fysisk buss: {progress.snapshot!.bus.physical_bus ?? 'Ukjent'}</p><button onClick={() => progress.setScreen('recap')}>Åpne oppsummering</button></>}
      </div>
      <section className="workday-tools" aria-label="Førerverktøy">
        <div className="controls">
          <button ref={readerEntry} disabled={props.suspended || !visible} onClick={() => setReaderOpen(true)}>Les avvik for linjer og datoer</button>
          <button ref={automaticEntry} disabled={props.suspended || !visible} onClick={() => setAutomaticOpen(true)}>Automatiske avvik</button>
          <button id="notice-entry-day" ref={notices.entry} disabled={props.suspended} onClick={notices.open}>Manuelt vedlikeholdte avvik</button>
        </div>
        {(notices.dirty || notices.pending) && <p>Åpne avvik for å fortsette med det lagrede forslaget eller forsøket.</p>}
        <PrivateDayTools request={request} expiresAt={plan.expires_at} available={visible && !props.hidden && !special && !props.suspended}/>
        <PrivateTourCorrection plan={plan} request={request} mutation={props.mutation} expired={props.expired} continuity={anchorContinuity}
          available={visible && !props.suspended && !progress.terminal} guard={props.guardSelection} saved={setCorrection}/>
      </section>
      <div hidden={progress.terminal && !props.busLocked}><PrivateBus id={plan.id} expiresAt={plan.expires_at} request={request} mutation={mutation} readOnly={progress.terminal} suspended={props.suspended} expired={props.expired} lock={props.guardBus} availability={props.busAvailability} factsAvailable={visible} afterSave={readyToStart} shorten={props.shorten} /></div>
      {visible && <>
        <button type="button" className="day-list-toggle" aria-expanded={props.activitiesOpen} aria-controls={'planned-' + plan.id}
          onClick={props.toggleActivities}>{props.activitiesOpen ? 'Skjul planlagte aktiviteter' : 'Vis planlagte aktiviteter (' + plan.draft.activities.length + ')'}</button>
        <div id={'planned-' + plan.id} hidden={!props.activitiesOpen}>
          {props.activitiesOpen && <PrivateDayOverview destinations={destinations} content={plan.draft} classifications={plan.classifications}
            finalEnd={plan.final_end} expiresAt={plan.expires_at} outcomes={progress.snapshot?.outcomes.outcomes}/>}
        </div>
        <details className="day-confirmed-details"><summary>Bekreftede detaljer og historisk kilde</summary>{props.historicalDetails}</details>
        <details><summary>Godtatte ukjente fakta</summary><ul>{plan.unknowns.map(item => <li key={item.id}>{item.label}</li>)}</ul></details>
        <p>Bekreftet {osloDateTime(plan.confirmed_at)}. Planen utløper {osloDateTime(plan.expires_at)}.</p>
      </>}
      <div className="controls">
        <button disabled={!visible || props.busLocked || progressLocked || props.suspended} onClick={props.remove}>Slett bekreftet plan</button>
        <button disabled={props.busy || props.suspended || props.busLocked || progressLocked} onClick={props.closeView}>Lukk planen</button>
      </div>
    </div>
  </section>;
}
