import { privateNow } from './privateClock';
import { useEffect, useRef, useState } from 'react';
import { recoverOperation } from './recoverOperation';
import type { Content } from './PrivateDrafts';
import { osloDateTime } from './dayOverview';
import { activityChoiceLabel } from './activityChoiceLabel';
import type { Plan } from './PrivateConfirmation';
import { busError, normalizeBus } from './busValue';

export const outcomeLabels = { unregistered: 'Ikke registrert', completed: 'Fullført manuelt', skipped: 'Hoppet over', interrupted: 'Avbrutt' };
export type Outcome = keyof typeof outcomeLabels;
export type Lifecycle = { workday_id: string; state: 'confirmed' | 'active' | 'ended' | 'aborted'; started_at: string | null; ended_at: string | null; revision: number; expires_at: string };
type Snapshot = { plan: Plan; lifecycle: Lifecycle; outcomes: { workday_id: string; revision: number; expires_at: string; outcomes: { activity_id: string; outcome: Outcome }[] }; bus: { workday_id: string; revision: number; physical_bus: string | null; expires_at: string } };
type Command = { kind: 'outcome'; body: { operation_id: string; expected_revision: number; expected_lifecycle_revision: number; activity_id: string; outcome: Outcome } }
  | { kind: 'close'; body: { operation_id: string; expected_revision: number; expected_outcome_revision: number; action: 'ended' | 'aborted' } };
type Props = { id: string; content: Content; expiresAt: string; validPlan: (v: any) => boolean; request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>; expired: () => void; suspended: boolean; lock: (v: boolean) => void; shorten: (v: string) => void };
const keys = (v: any, names: string) => v && Object.keys(v).sort().join() === names;
const stamp = (v: any) => typeof v === 'string' && Number.isFinite(Date.parse(v));
export function validLifecycle(v: any): v is Lifecycle {
  return keys(v, 'ended_at,expires_at,revision,started_at,state,workday_id') && stamp(v.expires_at) && (
    v.state === 'confirmed' && v.revision === 0 && v.started_at === null && v.ended_at === null ||
    v.state === 'active' && v.revision === 1 && stamp(v.started_at) && Date.parse(v.started_at) < Date.parse(v.expires_at) && v.ended_at === null ||
    ['ended', 'aborted'].includes(v.state) && v.revision === 2 && stamp(v.started_at) && stamp(v.ended_at) && Date.parse(v.ended_at) >= Date.parse(v.started_at) && Date.parse(v.ended_at) < Date.parse(v.expires_at));
}
export function useWorkdayProgress(props: Props) {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null), [pending, setPending] = useState<Command | null>(null);
  const [message, setMessage] = useState('Henter skift og registrerte aktivitetsstatuser …'), [busy, setBusy] = useState(true);
  const [proposals, setProposals] = useState<Record<string, Outcome>>({});
  const [screen, setScreen] = useState<'day' | 'close' | 'recap'>('day'), [action, setAction] = useState<'ended' | 'aborted'>('ended');
  const [review, setReview] = useState<Snapshot | null>(null);
  const alive = useRef(true), sending = useRef(false), current = useRef<Snapshot | null>(null), original = useRef<Command | null>(null), dirty = useRef(false), generation = useRef(0), navigation = useRef(0);
  const title = useRef<HTMLHeadingElement>(null), returnTo = useRef<HTMLElement | null>(null), initiallyOpened = useRef(false);
  const terminal = !!snapshot && ['ended', 'aborted'].includes(snapshot.lifecycle.state);
  function valid(v: any): v is Snapshot {
    if (!keys(v, 'bus,lifecycle,outcomes,plan') || !props.validPlan(v.plan) || v.plan.id !== props.id || JSON.stringify(v.plan.draft) !== JSON.stringify(props.content) || !validLifecycle(v.lifecycle)) return false;
    const o = v.outcomes, b = v.bus;
    return [v.lifecycle, o, b].every(item => item?.workday_id === props.id && stamp(item.expires_at) && Date.parse(item.expires_at) === Date.parse(v.plan.expires_at))
      && Date.parse(v.plan.expires_at) <= Date.parse(props.expiresAt) && Date.parse(v.plan.expires_at) > privateNow()
      && keys(o, 'expires_at,outcomes,revision,workday_id') && Number.isSafeInteger(o.revision) && o.revision >= 0 && Array.isArray(o.outcomes) && o.outcomes.length === props.content.activities.length
      && o.outcomes.every((item: any, i: number) => keys(item, 'activity_id,outcome') && item.activity_id === props.content.activities[i].id && Object.hasOwn(outcomeLabels, item.outcome))
      && keys(b, 'expires_at,physical_bus,revision,workday_id') && Number.isSafeInteger(b.revision) && b.revision >= 0 && (b.physical_bus === null || typeof b.physical_bus === 'string' && !busError(b.physical_bus) && normalizeBus(b.physical_bus) !== null)
      && (!['ended', 'aborted'].includes(v.lifecycle.state) || Date.parse(v.plan.expires_at) <= Date.parse(v.lifecycle.ended_at) + 7 * 86400000);
  }
  function navigate(value: 'day' | 'close' | 'recap') { navigation.current++; setScreen(value); }
  async function fetchCurrent(version = generation.current) {
    const value = await props.request('/workdays/' + props.id + '/recap');
    if (!valid(value)) throw Error('Invalid current workday');
    if (!alive.current || version !== generation.current) throw Error('Superseded read');
    const previous = current.current;
    if (previous && (value.lifecycle.revision < previous.lifecycle.revision || value.outcomes.revision < previous.outcomes.revision || value.bus.revision < previous.bus.revision || Date.parse(value.plan.expires_at) > Date.parse(previous.plan.expires_at))) return previous;
    if (alive.current) { current.current = value; setSnapshot(value); props.shorten(value.plan.expires_at); }
    return value as Snapshot;
  }
  async function load(openTerminal = false) {
    if (sending.current || props.suspended) return;
    const version = ++generation.current, destination = navigation.current; setBusy(true);
    try { const value = await fetchCurrent(version); if (alive.current && version === generation.current) { setMessage(original.current ? 'Forsøket er fortsatt uavklart. Kontroller eller prøv samme forsøk.' : 'Lagret skift og aktivitetsstatus er hentet.'); if ((openTerminal || !initiallyOpened.current) && destination === navigation.current && ['ended', 'aborted'].includes(value.lifecycle.state)) navigate('recap'); initiallyOpened.current = true; } }
    catch (error: any) { if (alive.current && version === generation.current) { if (error?.status === 401) props.expired(); else { setSnapshot(null); current.current = null; setMessage('Skift og aktivitetsstatus kan ikke bekreftes. Hent lagret status igjen.'); } } }
    finally { if (alive.current && version === generation.current) setBusy(false); }
  }
  useEffect(() => { alive.current = true; initiallyOpened.current = false; void load(true); const refresh = () => { if (!original.current && !dirty.current) void load(false); }; window.addEventListener('focus', refresh); return () => { alive.current = false; generation.current++; props.lock(false); window.removeEventListener('focus', refresh); }; }, [props.id]);
  useEffect(() => { title.current?.focus(); }, [screen]);
  useEffect(() => { dirty.current = Object.keys(proposals).length > 0; props.lock(!!pending || dirty.current); }, [pending, proposals]);
  function propose(id: string, value: Outcome) {
    setProposals(previous => { const next = { ...previous }; if (snapshot?.outcomes.outcomes.find(item => item.activity_id === id)?.outcome === value) delete next[id]; else next[id] = value; return next; });
  }
  function clearProposal(id: string) { setProposals(previous => { const next = { ...previous }; delete next[id]; return next; }); }
  async function send(command?: Command, lookup = false) {
    if (sending.current || props.suspended) return;
    const retry = !!original.current;
    const op = original.current ?? command; if (!op) return;
    generation.current++; original.current = op; setPending(op); sending.current = true; setBusy(true); props.lock(true); setMessage('Forsøket er uavklart til svaret er kontrollert.');
    let accepted = false;
    try {
      const status = () => props.request('/workday-' + op.kind + '-operations/' + op.body.operation_id);
      const mutate = () => props.mutation('/workdays/' + props.id + '/' + op.kind, op.body);
      const value = lookup ? await status() : retry ? await recoverOperation(status, fetchCurrent, mutate) : await mutate();
      if (!alive.current) return;
      if (!keys(value, 'operation_id,result') || value.operation_id !== op.body.operation_id || value.result?.workday_id !== props.id || !stamp(value.result.expires_at)) throw Error();
      if (op.kind === 'close') { if (!validLifecycle(value.result) || value.result.state !== op.body.action || value.result.revision !== op.body.expected_revision + 1) throw Error(); }
      else {
        const result = value.result;
        if (!keys(result, 'expires_at,outcomes,revision,workday_id') || result.revision !== op.body.expected_revision + 1 || !Array.isArray(result.outcomes) || result.outcomes.length !== props.content.activities.length || !result.outcomes.every((item: any, i: number) => keys(item, 'activity_id,outcome') && item.activity_id === props.content.activities[i].id && Object.hasOwn(outcomeLabels, item.outcome)) || result.outcomes.find((item: any) => item.activity_id === op.body.activity_id)?.outcome !== op.body.outcome) throw Error();
      }
      accepted = true;
      const latest = await fetchCurrent(); if (!alive.current) return;
      if (op.kind === 'close' && (latest.lifecycle.state !== value.result.state || latest.lifecycle.ended_at !== value.result.ended_at || latest.lifecycle.started_at !== value.result.started_at || latest.lifecycle.revision !== value.result.revision || Date.parse(latest.plan.expires_at) > Date.parse(value.result.expires_at))) throw Error();
      if (op.kind === 'outcome' && (latest.outcomes.revision < value.result.revision || latest.outcomes.revision === value.result.revision && JSON.stringify(latest.outcomes.outcomes) !== JSON.stringify(value.result.outcomes))) throw Error();
      original.current = null; setPending(null);
      if (op.kind === 'outcome' && latest.outcomes.outcomes.find(item => item.activity_id === op.body.activity_id)?.outcome === op.body.outcome) clearProposal(op.body.activity_id);
      setMessage(op.kind === 'close' ? 'Skiftet er avsluttet og skrivebeskyttet.' : latest.outcomes.revision > value.result.revision ? 'Aktivitetsstatusen ble lagret. En nyere lagret versjon vises; ditt forslag er beholdt hvis statusen er endret. Sammenlign før et nytt forsøk.' : 'Aktivitetsstatusen er lagret.');
      if (op.kind === 'close') { setReview(null); navigate('recap'); }
    } catch (error: any) {
      if (!alive.current) return;
      if (error?.status === 401) { props.expired(); return; }
      if (!lookup && !accepted && error?.status === 429 && keys(error.apiDetail, 'code,message') && error.apiDetail.code === op.kind + '_receipt_capacity' && error.apiDetail.message === 'For mange lagringsforsøk. Vent til tidligere planer utløper.') {
        // This validated rejection establishes no accepted effect even if a
        // subsequent read is unavailable. Keep the local proposal cancellable.
        try { await fetchCurrent(); }
        catch (readError: any) { if (readError?.status === 401) { props.expired(); return; } if (alive.current) { setSnapshot(null); current.current = null; } }
        if (!alive.current) return;
        original.current = null; setPending(null); setReview(null);
        setMessage('Forsøket ble avvist: grensen på 2000 lagringsforsøk er nådd. Forslaget er beholdt og kan avbrytes. Vent til tidligere planer utløper før du prøver igjen.');
        return;
      }
      // Only a typed known rejection permits dropping the command identity.
      if (!lookup && !accepted && [409, 422].includes(error?.status) && ['Lagringsforsøket har annet innhold.', 'Skiftet må være startet og aktivt.', 'Lagret status er endret. Hent og gjennomgå den på nytt.', 'Aktiviteten tilhører ikke planen.'].includes(error.apiDetail)) {
        try { const latest = await fetchCurrent(); if (!alive.current) return; original.current = null; setPending(null); setReview(null); setMessage('Forsøket ble avvist. Forslaget er beholdt. Gjennomgå lagret status før du prøver på nytt.'); if (['ended', 'aborted'].includes(latest.lifecycle.state)) navigate('recap'); }
        catch { setMessage('Forsøket er uavklart. Kontroller eller prøv samme forsøk.'); }
      } else { if ([404, 410].includes(error?.status)) { setSnapshot(null); current.current = null; } setMessage('Forsøket er uavklart. Kontroller eller prøv samme forsøk.'); }
    } finally { sending.current = false; if (alive.current) setBusy(false); }
  }
  async function beginClose(value: 'ended' | 'aborted', target: HTMLElement) {
    if (Object.keys(proposals).length || pending || props.suspended || busy) return;
    const version = ++generation.current; returnTo.current = target; setAction(value); setReview(null); navigate('close'); setBusy(true);
    try { const latest = await fetchCurrent(); if (alive.current) { if (latest.lifecycle.state === 'active') setReview(latest); else if (['ended', 'aborted'].includes(latest.lifecycle.state)) navigate('recap'); } }
    catch (error: any) { if (error?.status === 401) props.expired(); else setMessage('Lagret status kan ikke hentes. Hent på nytt før bekreftelse.'); }
    finally { if (alive.current && version === generation.current) setBusy(false); }
  }
  function cancelClose() { setReview(null); navigate('day'); window.setTimeout(() => returnTo.current?.focus(), 0); }
  return { snapshot, terminal, pending, busy, message, proposals, screen, setScreen: navigate, action, review, title, load, propose, clearProposal, send, beginClose, cancelClose };
}
export type Progress = ReturnType<typeof useWorkdayProgress>;
export function OutcomeEditor({ progress: p, activityId, suspended }: { progress: Progress; activityId: string; suspended: boolean }) {
  const saved = p.snapshot?.outcomes.outcomes.find(item => item.activity_id === activityId)?.outcome;
  const proposed = p.proposals[activityId] ?? saved ?? 'unregistered';
  return <section aria-label="Registrert aktivitetsstatus"><h3>Registrert aktivitetsstatus</h3><p>Lagret: {saved ? outcomeLabels[saved] : 'Ukjent / utilgjengelig'}</p>
    {p.terminal ? <p>Skiftet er avsluttet. Aktivitetsstatusen er skrivebeskyttet.</p> : p.snapshot?.lifecycle.state !== 'active' ? <p>Start skiftet før du registrerer aktivitetsstatus.</p> : <><label>Manuell aktivitetsstatus<select aria-label="Manuell aktivitetsstatus" disabled={suspended || !!p.pending || p.busy} value={proposed} onChange={e => p.propose(activityId, e.target.value as Outcome)}>{Object.entries(outcomeLabels).map(([value, label]) => <option value={value} key={value}>{label}</option>)}</select></label><p>Valget lagres bare når du trykker Lagre aktivitetsstatus.</p><div className="controls"><button disabled={suspended || !!p.pending || p.busy || !Object.hasOwn(p.proposals, activityId)} onClick={() => void p.send({ kind: 'outcome', body: { operation_id: crypto.randomUUID(), expected_revision: p.snapshot!.outcomes.revision, expected_lifecycle_revision: p.snapshot!.lifecycle.revision, activity_id: activityId, outcome: proposed } })}>Lagre aktivitetsstatus</button><button disabled={!!p.pending || p.busy || !Object.hasOwn(p.proposals, activityId)} onClick={() => p.clearProposal(activityId)}>Avbryt ulagret aktivitetsstatus</button></div></>}
  </section>;
}
function Counts({ snapshot }: { snapshot: Snapshot }) {
  return <dl>{Object.entries(outcomeLabels).map(([value, label]) => <div key={value}><dt>{label}</dt><dd>{snapshot.outcomes.outcomes.filter(item => item.outcome === value).length}</dd></div>)}</dl>;
}
export function ProgressScreens({ progress: p, content, classifications, suspended, showPreparation, showDay, factsAvailable, compact, leaveLocked }: { progress: Progress; content: Content; classifications: Record<string, string>; suspended: boolean; showPreparation: () => void; showDay: () => void; factsAvailable: boolean; compact: boolean; leaveLocked: boolean }) {
  const pendingOutcome = p.pending?.kind === 'outcome' ? p.pending.body : null;
  return <>
    <p hidden={compact && /^(Henter skift|Lagret skift og aktivitetsstatus)/.test(p.message)} role="status" aria-label="Aktivitetsstatus og avslutningsstatus">{p.message}</p>
    {!factsAvailable && p.screen !== 'day' && <><p>Planfakta er skjult til plantilgangen er kontrollert.</p><button onClick={showDay}>Tilbake til dagen for å kontrollere plantilgangen</button></>}
    {!p.pending && Object.keys(p.proposals).length > 0 && <section aria-label="Ulagrede forslag til aktivitetsstatus"><p>{p.terminal ? 'Skiftet er avsluttet. Disse lokale forslagene er ikke lagret.' : !factsAvailable ? 'Lagrede planfakta er utilgjengelige. Disse lokale forslagene til aktivitetsstatus er ikke lagret og kan forkastes.' : 'Disse lokale forslagene til aktivitetsstatus er ikke lagret. Dagsoversikten viser lagrede statuser.'}</p>{Object.entries(p.proposals).map(([id, value]) => <div key={id}><p>Aktivitet {content.activities.findIndex(a => a.id === id) + 1}: {outcomeLabels[value]}</p>{factsAvailable && <p>{activityChoiceLabel(content.activities.find(a => a.id === id), classifications[id])}</p>}<button onClick={() => p.clearProposal(id)}>Forkast ulagret aktivitetsstatus for aktivitet {content.activities.findIndex(a => a.id === id) + 1}</button></div>)}</section>}
    {p.pending && <div className="controls">{pendingOutcome && <p>Uavklart lagringsforsøk for aktivitet {content.activities.findIndex(a => a.id === pendingOutcome.activity_id) + 1}: {outcomeLabels[pendingOutcome.outcome]}. Dette er det opprinnelige forsøket, ikke statusen til aktiviteten du ser på nå.</p>}<button disabled={p.busy || suspended} onClick={() => void p.send()}>Prøv samme {p.pending.kind === 'close' ? 'avslutning' : 'aktivitetsstatus'} igjen</button><button disabled={p.busy || suspended} onClick={() => void p.send(undefined, true)}>Kontroller {p.pending.kind === 'close' ? 'avslutningen' : 'aktivitetsstatusen'}</button></div>}
    <button hidden={compact && factsAvailable && !p.pending} disabled={p.busy || suspended} onClick={() => void p.load()}>Hent skift og aktivitetsstatus igjen</button>
    {p.screen === 'close' && <section aria-label="Bekreft avslutning"><h2 ref={p.title} tabIndex={-1}>{p.action === 'ended' ? 'Avslutt skift' : 'Avbryt skift'}</h2>{p.review && factsAvailable && <><p>Faktisk første start: {osloDateTime(p.review.lifecycle.started_at!)}.</p><Counts snapshot={p.review} /><details><summary>Ikke registrerte aktiviteter ({p.review.outcomes.outcomes.filter(item => item.outcome === 'unregistered').length})</summary><ol>{p.review.outcomes.outcomes.filter(item => item.outcome === 'unregistered').map(item => { const index = content.activities.findIndex(a => a.id === item.activity_id); return <li key={item.activity_id} data-unregistered-id={item.activity_id}>Aktivitet {index + 1}: {activityChoiceLabel(content.activities[index], classifications[item.activity_id])}</li>; })}</ol></details><p>Ikke registrerte aktiviteter forblir ikke registrert. Skiftet kan ikke gjenopptas eller endres etter bekreftelse.</p><button disabled={p.busy || suspended || !!p.pending} onClick={() => void p.send({ kind: 'close', body: { operation_id: crypto.randomUUID(), expected_revision: p.review!.lifecycle.revision, expected_outcome_revision: p.review!.outcomes.revision, action: p.action } })}>{p.action === 'ended' ? 'Bekreft avslutning' : 'Bekreft avbrudd'}</button></>}<button disabled={p.busy || !!p.pending} onClick={p.cancelClose}>Tilbake uten å avslutte</button>{!p.review && !p.pending && <p>Hent lagret status og åpne bekreftelsen på nytt for å gjennomgå oppdaterte antall.</p>}</section>}
    {p.screen === 'recap' && factsAvailable && p.terminal && p.snapshot && <section aria-label="Oppsummering av skift"><h2 ref={p.title} tabIndex={-1}>{p.snapshot.lifecycle.state === 'ended' ? 'Skift avsluttet' : 'Skift avbrutt'}</h2><p>Takk for i dag</p><p>Tjenestedato: {content.service_date}</p><p>Planlagt start: {osloDateTime(content.activities[0].start!)}. Planlagt siste slutt: {osloDateTime(p.snapshot.plan.final_end)}.</p><p>Faktisk første start: {osloDateTime(p.snapshot.lifecycle.started_at!)}. Avsluttet av serveren: {osloDateTime(p.snapshot.lifecycle.ended_at!)}.</p><p>Fysisk buss: {p.snapshot.bus.physical_bus ?? 'Ukjent'}. Utløper: {osloDateTime(p.snapshot.plan.expires_at)}.</p><Counts snapshot={p.snapshot} /><ol>{p.snapshot.outcomes.outcomes.map((item, index) => <li key={item.activity_id}><p>Aktivitet {index + 1}: {activityChoiceLabel(content.activities[index], classifications[item.activity_id])}</p><strong>{outcomeLabels[item.outcome]}</strong></li>)}</ol><div className="controls"><button onClick={showDay}>Tilbake til dagen</button><button disabled={leaveLocked || suspended || !!p.pending || Object.keys(p.proposals).length > 0} onClick={() => { if (!leaveLocked && !suspended && !p.pending && Object.keys(p.proposals).length === 0) showPreparation(); }}>Til forberedelse og planlisten</button></div><p>Oppsummeringen viser manuelle registreringer. Den fastslår ikke fysisk kjøring.</p></section>}
  </>;
}
