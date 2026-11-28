import { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import type { Plan } from './PrivateConfirmation';
import type { Content } from './PrivateDrafts';
import type { Lifecycle } from './PrivateWorkdayProgress';
import { DrivingPeriodRows, passengerPeriod, drivingClock, drivingTime, endPlace } from './drivingPeriods';
import { privateNow } from './privateClock';
import { observeOperationalTime, useOperationalNow } from './operationalNotices';
import { ActiveRoadLimits } from './PrivateRoadLimits';
import { DrivingSpeed, PositionAssistance } from './PositionAssistance';
import { usePilotRoad } from './PrivateRoadArea';
import { referenceDestination, useFrozenRouteReferences } from './PrivateRouteReference';
import { readWorkdayAnchor, type PositionAnchorContinuity, type SavedStopAnchor } from './positionAnchorClient';
import { PrivateDrivingAnchor } from './PrivateDrivingAnchor';
import { useDrivingStops, type DrivingStopState } from './drivingStops';
import type { StopCall } from './stopProgression';
import './driving.css';

type Activity = Content['activities'][number];
type Request = (path: string) => Promise<any>;
type Mutation = (path: string, body: object) => Promise<any>;
type Props = { visible: boolean; plan: Plan; lifecycle: Lifecycle; request: Request; mutation: Mutation; expired: () => void;
  back: () => void; anchorContinuity: PositionAnchorContinuity; correction?: SavedStopAnchor; };
type Notice = {id: string; title: string; scope: 'stops' | 'section' | 'area' | 'line' | 'network' | 'uncertain';
  positions: number[]; cancelled: number[]; valid_until: string; urgent: boolean; from?: string; to?: string; area?: string};

const emptyStops: DrivingStopState = {calls: [], position: null, phase: 'unknown'};
const timestamp = (value: string | null) => value ? Date.parse(value) : NaN;

export function activityAt(activities: Activity[], now: number) {
  // A boundary shared by two activities belongs to the new activity. Keep the
  // first activity reachable when starting before its planned reporting time.
  const first = activities[0];
  if (first && now < timestamp(first.start)) return first;
  for (let index = activities.length - 1; index >= 0; index--) {
    const activity = activities[index];
    if (timestamp(activity.start) <= now && now < timestamp(activity.end)) return activity;
  }
  return null;
}

function useDriverNotices(planId: string, activityId: string | undefined, request: Request) {
  const [response, setResponse] = useState<{activity: string; notices: Notice[]; old: boolean}>();
  const [failed, setFailed] = useState(false);
  const access = useRef(request);
  access.current = request;
  const now = useOperationalNow(true);
  useEffect(() => {
    setResponse(undefined); setFailed(false);
    if (!activityId) return;
    let mounted = true, reading = false;
    async function refresh() {
      if (reading) return;
      reading = true;
      try {
        const data = await access.current('/workdays/' + planId + '/driving-notices/' + activityId);
        if (!mounted) return;
        if (data?.workday_id !== planId || data.activity_id !== activityId || !Number.isFinite(Date.parse(data.server_now))
          || !Array.isArray(data.notices) || data.notices.length > 1000 || !data.notices.every((item: any) =>
            typeof item?.id === 'string' && typeof item.title === 'string' && Number.isFinite(Date.parse(item.valid_until))
            && typeof item.urgent === 'boolean' && ['stops', 'section', 'area', 'line', 'network', 'uncertain'].includes(item.scope)
            && [item.positions, item.cancelled].every(positions => Array.isArray(positions) && positions.every(value => Number.isSafeInteger(value) && value > 0 && value <= 250)))) throw Error();
        observeOperationalTime(data.server_now);
        setResponse({activity: activityId!, notices: data.notices, old: data.old || data.feed !== 'complete'});
        setFailed(false);
      } catch {
        if (mounted) setFailed(true);
      } finally { reading = false; }
    }
    void refresh();
    const timer = window.setInterval(refresh, 3000);
    return () => { mounted = false; window.clearInterval(timer); };
  }, [planId, activityId]);
  return {entries: response?.activity === activityId ? response?.notices.filter(item => Date.parse(item.valid_until) > now) ?? [] : [],
    offline: failed || !!response?.old};
}

function WarningMark() {
  return <svg className="driving-warning-mark" width="26" height="26" viewBox="0 0 32 32" role="img" aria-label="Avvik ved stoppet">
    <path d="M16 2 31 29H1Z" fill="#F5C842" stroke="#171717" strokeWidth="2" strokeLinejoin="round"/>
    <path d="M16 10v10" stroke="#171717" strokeWidth="3" strokeLinecap="round"/><circle cx="16" cy="25" r="1.7" fill="#171717"/>
  </svg>;
}

function NoticeStrip({items}: {items: Notice[]}) {
  if (!items.length) return null;
  return <aside className="driving-alerts" aria-label="Avvik for kjøringen">
    {items.slice(0, 2).map(item => <div key={item.id} className="driving-alert">
      <span className="driving-role"><WarningMark /> {item.scope === 'uncertain' ? 'Strekning uavklart' : item.scope === 'area' ? 'Område · ' + item.area : 'Trafikkavvik'}</span>
      <strong>{item.scope === 'section' ? 'Omkjøring fra ' + item.from + ' til ' + item.to : item.title}</strong>
      {item.scope === 'section' && <span>{item.title}</span>}
    </div>)}
    {items.length > 2 && <span>{items.length - 2} flere avvik i Dagen din</span>}
  </aside>;
}

function stopRows({calls, position, phase}: DrivingStopState) {
  const index = calls.findIndex(call => call.position === position);
  if (index < 0) return [{role:'Deretter', call:calls[1]}, {role:'Første stopp', call:calls[0], focus:true}];
  if (phase === 'moving' && !calls[index+1]) return [{role:'Siste stopp', call:calls[index], focus:true}];
  if (phase === 'moving') return [{role:'Deretter', call:calls[index+2]}, {role:'Neste stopp', call:calls[index+1], focus:true},
    {role:'Passert', call:calls[index]}];
  return [{role:'Deretter', call:calls[index+2]}, {role:'Neste stopp', call:calls[index+1]},
    {role:phase === 'here' ? 'Her nå' : phase === 'manual' ? 'Valgt stopp' : 'Sist registrert', call:calls[index], focus:true}];
}

function Stops({state, notices}: {state: DrivingStopState; notices: Notice[]}) {
  const contains = (notice: Notice, position: number | null) => position !== null && notice.positions.includes(position);
  const index = state.calls.findIndex(call => call.position === state.position);
  const next = state.calls[index + 1]?.position ?? null;
  const displayed = notices.filter(notice => {
    if (!notice.positions.length) return true;
    if (notice.urgent) return notice.positions.some(value => value >= (state.position ?? 0));
    if (notice.scope === 'section') return notice.positions.some(value => value >= (state.position ?? 1));
    return state.phase === 'here' && contains(notice, state.position) || state.phase === 'moving' && contains(notice,next);
  });
  return <div className={'driving-content' + (displayed.length ? ' with-alerts' : '')}>
    <NoticeStrip items={displayed}/>
    <ol className="driving-sequence" aria-label="Holdeplassprogresjon" data-phase={state.phase}>
      {stopRows(state).map(({role,call,focus}) => <StopRow key={role} role={role} call={call} focus={focus} notices={notices}/>)}
    </ol>
  </div>;
}

function StopRow({role, call, focus, notices}: {role: string; call: StopCall | undefined; focus?: boolean; notices: Notice[]}) {
  const affected = call && notices.some(notice => notice.positions.includes(call.position));
  const cancelled = call && notices.some(notice => notice.cancelled.includes(call.position));
  return <li className={'driving-stop' + (focus ? ' focus-stop' : '')} data-stop-position={call?.position}>
    <span className="driving-role">{role}</span>
    <span className="driving-stop-name">{call?.name ?? (call ? 'Ukjent navn' : '—')}{affected && <WarningMark />}</span>
    {cancelled && <strong className="driving-cancelled">Betjenes ikke</strong>}
  </li>;
}

function DrivingTrip({plan, activity, request, mutation, anchorContinuity, notices, changed, handoff}: Props & {activity: Activity; notices: Notice[];
 changed: (value: DrivingStopState) => void; handoff?: string}) {
  const view = useDrivingStops({workdayId: plan.id, activityId: activity.id, expiresAt: plan.expires_at, request, mutation}, anchorContinuity, handoff);
  useEffect(() => { changed(view); }, [view, changed]);
  if (!view.calls.length) return <div className={'driving-content' + (notices.length ? ' with-alerts' : '')}>
    <NoticeStrip items={notices.filter(item => !item.positions.length)}/>
    <div className="driving-task"><span className="driving-role">Neste stopp</span><strong>Holdeplassdata uavklart</strong><p>{activity.from_place ?? 'Ukjent avreisested'} → {activity.to_place ?? 'Ukjent ankomststed'}</p></div>
  </div>;
  return <Stops state={view} notices={notices}/>;
}

export function PrivateDriving(props: Props) {
  const {plan,lifecycle,request,expired,back,visible} = props;
  const [now, setNow] = useState(privateNow);
  const [manual, setManual] = useState<SavedStopAnchor | null>(props.correction ?? null);
  useEffect(() => {
    let current = true;
    void readWorkdayAnchor({workdayId:plan.id, expiresAt:plan.expires_at, request}).then(anchor => {
      if (current) setManual(anchor);
    }).catch(() => {});
    return () => { current = false; };
  }, [plan.id]);
  const [last, setLast] = useState<{activity: string; view: DrivingStopState}>();
  const title = useRef<HTMLHeadingElement>(null);
  useEffect(() => { if (visible) title.current?.focus(); }, [visible]);
  useEffect(() => {
    const timer = window.setInterval(() => setNow(privateNow()), 1000);
    return () => window.clearInterval(timer);
  }, []);
  const scheduled = activityAt(plan.draft.activities, now);
  const lastActivity = plan.draft.activities.find(activity => activity.id === last?.activity);
  const finishing = last?.view.calls.at(-1)?.position;
  // Keep a still-running passenger leg over its planned end until the live
  // position has reached its terminus. A remembered or missing fix cannot pin a leg.
  const runningLate = lastActivity && last?.view.position && finishing && last.view.position < finishing
    && ['here', 'moving'].includes(last.view.phase) && now >= timestamp(lastActivity.end)
    && now < timestamp(lastActivity.end) + 20 * 60_000;
  const manuallySelected = plan.draft.activities.find(item => item.id === manual?.activity_id);
  const manualLimit = manuallySelected && manual
    ? manual.origin === 'manual' ? Math.max(timestamp(manuallySelected.end), Date.parse(manual.saved_at) + 20*60_000)
      : timestamp(manuallySelected.end) : 0;
  const activity = manuallySelected && now < manualLimit ? manuallySelected : runningLate ? lastActivity : scheduled;
  const activeId = activity?.id;
  const kind = activity ? plan.classifications[activity.id] ?? activity.type : null;
  const passenger = kind === 'trip' && (activity === manuallySelected || timestamp(activity!.start) <= now);
  const period = passengerPeriod(plan, now);
  const routes = useFrozenRouteReferences({workdayId: plan.id, serviceDate: plan.draft.service_date,
    expiresAt: plan.expires_at, available: true, request, expired});
  const reference = routes.references.find(ref => ref.activity_id === activeId);
  const destinations = reference && referenceDestination(reference);
  const upcoming = routes.references.find(ref => ref.activity_id === period.next?.id);
  const road = usePilotRoad(request);
  const noticeActivity = activeId ?? period.rows[0]?.id ?? period.next?.id;
  const {entries, offline} = useDriverNotices(plan.id, noticeActivity, request);
  const view = (last?.activity === activeId ? last?.view : null) ?? emptyStops;
  const changed = useMemo(() => (view: DrivingStopState) => { if (activeId) setLast({activity:activeId,view}); }, [activeId]);
  const region = passenger ? view.phase === 'here' ? 'På holdeplass' : view.phase === 'manual' ? 'Manuelt holdepunkt' : view.phase === 'moving' ? 'Mellom stopp' : 'Posisjonen er uavklart'
    : null;
  const previousCall = last?.view.calls.at(-1);
  const handoff = last?.activity !== activeId && last?.view.phase === 'here' && last.view.position === previousCall?.position
    ? previousCall?.quay_id ?? undefined : undefined;
  const verify = async () => {
    const live = await request('/workdays/' + plan.id + '/lifecycle');
    if (live?.workday_id !== plan.id || live?.state !== 'active' || live?.started_at !== lifecycle.started_at
        || Date.parse(live.expires_at) <= privateNow()) throw Error();
  };
  return createPortal(<main className="driving-view" aria-label="Kjørevisning" hidden={!visible} data-workday-id={plan.id}
      data-period={passenger ? undefined : period.title} data-activity-id={activeId} data-journey-id={reference?.journey_id} data-started-at={lifecycle.started_at ?? undefined}>
    <PositionAssistance authorized expiresAt={plan.expires_at} verifyAccess={verify} showSpeed={false}>
      <div className="driving-topline"><span>Kjøring</span><time dateTime={new Date(now).toISOString()}>{drivingClock.format(now)}</time></div>
      <div className="driving-orientation">
        <div className="driving-route">
          {passenger && <span className="driving-line" aria-label={'Linje ' + (activity?.line ?? 'ukjent')}>{activity?.line ?? '—'}</span>}
          <div><h1 ref={title} tabIndex={-1}>{passenger ? destinations || activity?.to_place || 'Destinasjon uavklart' : period.title}</h1>
            {passenger && <p>{activity?.direction ?? 'Retning uavklart'}</p>}
            {passenger && (view.phase === 'here' || view.phase === 'manual') && view.position === reference?.start_position && now < timestamp(activity?.start ?? null)
              && <p className="driving-ready-status">Klar ved stoppet · planlagt avgang {drivingTime(activity?.start ?? null)}</p>}</div>
        </div>
        <div className="driving-trip-meta">{passenger ? <><span>Tur {activity?.trip ?? 'ukjent'}</span><span>Passasjertur</span></> : null}</div>
        <div className="driver-speed-area"><ActiveRoadLimits {...road} driving/><DrivingSpeed/></div>
      </div>
      {passenger && activity ? <DrivingTrip key={activity.id} {...props} activity={activity} notices={entries} changed={changed} handoff={handoff}/>
        : <div className="driving-period">
            <DrivingPeriodRows plan={plan} period={period} now={now}/>
            <div className="driving-departure">
              <span className="driving-role">{period.final ? 'Planlagt skiftslutt' : period.title === 'Før første tur' ? 'Første avgang' : 'Neste avgang'}</span>
              {period.next ? <>
                <strong>{drivingTime(period.next.start)} · {upcoming?.calls[upcoming.start_position - 1]?.name || period.next.from_place || 'Ukjent første stopp'}</strong>
                <p>Linje {period.next.line ?? 'ukjent'} · {upcoming && referenceDestination(upcoming) || period.next.to_place || 'Ukjent destinasjon'}</p>
                {period.nextDuty && <p>Vognløp {period.nextDuty}</p>}
                <PrivateDrivingAnchor key={period.next.id} authority={{workdayId:plan.id, activityId:period.next.id, expiresAt:plan.expires_at, request, mutation:props.mutation}}
                  continuity={props.anchorContinuity} firstOnly saved={setManual}/>
              </> : <strong>{drivingTime(plan.final_end)}{endPlace(plan) && ' · ' + endPlace(plan)}</strong>}
              <NoticeStrip items={entries.filter(item => !item.positions.length)}/>
            </div>
          </div>}
      <footer className="driving-footer"><div>{region && <strong>{region}</strong>}{offline && <span>Trafikkavvik kan være utdaterte</span>}</div>
        <button type="button" onClick={back}>Til Dagen din</button>
      </footer>
    </PositionAssistance>
  </main>, document.body);
}
