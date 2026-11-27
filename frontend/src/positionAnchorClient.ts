import { useLayoutEffect, useRef, useState } from 'react';
import { privateNow } from './privateClock.ts';
import { recoverOperation } from './recoverOperation.ts';
import type { StopCall } from './stopProgression';

export type StopRoute = {
  activity_id: string | null; service_date: string | null; journey_id: string | null; pattern_id: string | null;
  decision_revision: number | null; start_position: number; end_position: number;
  basis: string; compatible: boolean; source_version: string | null;
};
export type StopProjection = {
  route: StopRoute | null; calls: StopCall[]; reason: string | null; terminal: boolean;
  source: { revision: string; provider: string; source_url: string; license_url: string } | null;
};
type Provenance = {
  activity_id: string; service_date: string; journey_id: string; pattern_id: string; occurrence_id: string;
  revision: number; route_basis: string; origin: 'manual' | 'gps'; evidence_at: string;
  quay_id: string; stop_place_id: string; coordinate_revision: string | null;
  mapping_revision: string | null; quay_version: string | null; stop_place_version: string | null;
};
export type SavedStopAnchor = Provenance & {
  workday_id: string; saved_at: string; asserted_at: string | null; carried_from: Provenance | null;
};
export type AnchorCommand = {
  activity_id: string; route_basis: string; occurrence_id: string; coordinate_revision: string | null;
  origin: 'manual' | 'gps'; evidence_at: string; carried_from_revision?: number;
};
type Operation = AnchorCommand & { operation_id: string; expected_revision: number };
type Latest = { workday_id: string; expires_at: string; revision: number; terminal: boolean; anchor: SavedStopAnchor | null };
type Receipt = { workday_id: string; operation_id: string; accepted_revision: number; accepted_at: string };
type PendingAnchor = { workdayId: string; operation: Operation; dispatch: Promise<unknown> | null };
export type PositionAnchorContinuity = { pending: PendingAnchor | null };

export function createPositionAnchorContinuity(): PositionAnchorContinuity {
  return { pending: null };
}

export type StopAuthority = {
  workdayId: string; activityId: string; expiresAt: string;
  request: (path: string) => Promise<unknown>; mutation: (path: string, body: object) => Promise<unknown>;
};
const text = (value: unknown): value is string => typeof value === 'string' && value.length > 0;
const time = (value: unknown) => text(value) && Number.isFinite(Date.parse(value));
const revision = (value: unknown): value is number => typeof value === 'number' && Number.isSafeInteger(value) && value >= 0;
const digest = (value: unknown) => text(value) && /^[a-f0-9]{64}$/.test(value);
const stopSourceUrls = new Set([
  'https://developer.entur.org/stop-places-v1-read/',
  'https://developer.entur.no/open-data/stops',
]);
const pinnedNsrArchive = /^https:\/\/storage\.googleapis\.com\/marduk-production\/tiamat\/(?:CurrentAndFuture|55_Troms)_latest\.zip\?generation=[0-9]{1,20}$/;
const boundedPoint = (value: any) => value === null || (value && Number.isFinite(value.latitude)
  && Math.abs(value.latitude) <= 90 && Number.isFinite(value.longitude) && Math.abs(value.longitude) <= 180
  && ['revision', 'mapping_revision', 'quay_version', 'stop_place_version'].every(key => text(value[key])));
const validTime = (value: any) => value === null || (value && (value.utc === null || time(value.utc))
  && (value.calendar_time === null || time(value.calendar_time)));
const validProvenance = (value: any) => value && revision(value.revision) && value.revision > 0 && digest(value.route_basis)
  && ['activity_id', 'service_date', 'journey_id', 'pattern_id', 'occurrence_id', 'quay_id', 'stop_place_id'].every(key => text(value[key]))
  && ['coordinate_revision', 'mapping_revision', 'quay_version', 'stop_place_version'].every(key => value[key] === null || text(value[key]))
  && (value.origin === 'gps' || value.origin === 'manual') && time(value.evidence_at);
const validScope = (value: any, auth: StopAuthority) => value && value.workday_id === auth.workdayId
  && typeof value.terminal === 'boolean' && time(value.expires_at) && Date.parse(value.expires_at) > privateNow()
  && Date.parse(value.expires_at) <= Date.parse(auth.expiresAt);

export function readStopProjection(value: any, auth: StopAuthority): StopProjection {
  if (!validScope(value, auth) || value.activity_id !== auth.activityId
      || !(value.reason === null || text(value.reason)) || !Array.isArray(value.calls) || value.calls.length > 250
      || (value.route === null && value.calls.length !== 0)) throw Error();
  if (value.route !== null) {
    const route = value.route;
    if (!route || !['compatible', 'unverified', 'incompatible'].includes(route.status)
      || typeof route.compatible !== 'boolean' || (route.compatible && route.activity_id !== auth.activityId)
      || !digest(route.basis) || !revision(route.start_position) || !revision(route.end_position)
      || route.start_position < 1 || route.end_position - route.start_position + 1 !== value.calls.length
      || !['activity_id', 'service_date', 'journey_id', 'pattern_id', 'source_version'].every(key => route[key] === null || text(route[key]))
      || !(route.decision_revision === null || revision(route.decision_revision))
      || (route.compatible && (!revision(route.decision_revision) || route.decision_revision < 1
        || !['service_date', 'journey_id', 'pattern_id', 'source_version'].every(key => text(route[key]))))) throw Error();
    const ids = new Set<string>();
    value.calls.forEach((call: any, index: number) => {
      if (!call || call.position !== route.start_position + index || !text(call.occurrence_id) || ids.has(call.occurrence_id)
        || !boundedPoint(call.coordinates) || !validTime(call.arrival) || !validTime(call.departure)
        || !['name', 'stop_place_id', 'quay_id', 'coordinate_issue'].every(key => call[key] === null || text(call[key]))) throw Error();
      ids.add(call.occurrence_id);
    });
  }
  if (value.source !== null && (!value.source || value.source.contract !== 'nsr-quay-coordinate-v1'
    || !['revision', 'source_url', 'license_url', 'provider'].every(key => text(value.source[key]))
    || !(stopSourceUrls.has(value.source.source_url) || pinnedNsrArchive.test(value.source.source_url))
    || value.source.license_url !== 'https://data.norge.no/nlod/en/2.0')) throw Error();
  return value;
}

export function proposeStop(anchor: SavedStopAnchor, workdayId: string, route: StopRoute | null, calls: StopCall[]) {
  if (anchor.workday_id !== workdayId || !route?.compatible || route.activity_id === anchor.activity_id) return null;
  const candidates = calls.filter(call => call.quay_id === anchor.quay_id);
  if (candidates.length === 0) return { kind: 'no-match' as const };
  if (candidates.length > 1) return { kind: 'ambiguous' as const, calls: candidates };
  const [call] = candidates, point = call.coordinates;
  if (call.stop_place_id !== anchor.stop_place_id || !point || point.revision !== anchor.coordinate_revision
      || point.mapping_revision !== anchor.mapping_revision || point.quay_version !== anchor.quay_version
      || point.stop_place_version !== anchor.stop_place_version) return { kind: 'unverified' as const };
  return { kind: 'unique' as const, call };
}

function validLatest(value: any, auth: StopAuthority): value is Latest {
  return validScope(value, auth) && revision(value.revision)
    && (value.revision === 0 ? value.anchor === null : validProvenance(value.anchor)
      && value.anchor.workday_id === auth.workdayId && value.anchor.revision === value.revision
      && time(value.anchor.saved_at) && (value.anchor.asserted_at === null || time(value.anchor.asserted_at))
      && (value.anchor.carried_from === null || validProvenance(value.anchor.carried_from)));
}

export function usePositionAnchor(auth: StopAuthority, continuity: PositionAnchorContinuity, deny: () => void) {
  const epoch = useRef(0), live = useRef(false), busy = useRef(false), authority = useRef(auth);
  const latest = useRef<Latest | null>(null), reloading = useRef(false);
  const queued = useRef<AnchorCommand | null>(null);
  const pendingForWorkday = () => continuity.pending?.workdayId === auth.workdayId ? continuity.pending : null;
  const [view, setView] = useState<Latest | null>(null);
  const [pending, setPending] = useState(() => Boolean(pendingForWorkday()));
  const [writing, setWriting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('Henter lagret holdepunkt …');
  authority.current = auth;
  const denied = useRef(deny);
  denied.current = deny;
  const base = '/workdays/' + auth.workdayId + '/position-anchor';
  const alive = (version: number) => live.current && version === epoch.current;

  async function current(version: number, publish: boolean) {
    const value = await authority.current.request(base);
    if (!alive(version) || !validLatest(value, authority.current)) throw Error();
    if (publish) { latest.current = value; setView(value); }
    return value;
  }

  function discardQueue() { queued.current = null; }
  function clearPending() {
    if (pendingForWorkday()) continuity.pending = null;
    setPending(false);
  }

  function forget() {
    epoch.current++;
    clearPending();
    latest.current = null; busy.current = false; reloading.current = false; queued.current = null;
    setView(null); setLoading(false); setWriting(false);
    setMessage('Lagret holdepunkt er utilgjengelig.');
  }

  function canRecordManual() {
    const value = latest.current;
    return live.current && value !== null && !value.terminal && Date.parse(value.expires_at) > privateNow()
      && !reloading.current && !busy.current && pendingForWorkday() === null;
  }

  async function load() {
    if (busy.current || reloading.current) return;
    const version = epoch.current;
    reloading.current = true;
    setLoading(true);
    try {
      await current(version, true);
      setMessage(pendingForWorkday() ? 'Et forsøk på å lagre holdepunkt er uavklart.' : '');
    } catch (error: any) {
      if (!alive(version)) return;
      latest.current = null;
      setView(null);
      setMessage(pendingForWorkday() ? 'Lagringen er uavklart, og lagret status er utilgjengelig.'
        : 'Lagret holdepunkt er utilgjengelig.');
      if ([401, 404, 410].includes(error?.status)) denied.current();
    } finally {
      if (alive(version)) {
        reloading.current = false;
        setLoading(false);
      }
    }
  }

  useLayoutEffect(() => {
    live.current = true;
    void load();
    return () => {
      live.current = false;
      epoch.current++;
      // Prior workday commands remain recoverable with an explicit receipt check.
      latest.current = null; busy.current = false; reloading.current = false; queued.current = null;
    };
  }, [auth.workdayId, auth.activityId, continuity]);

  async function send(command?: AnchorCommand, retry = false) {
    if (!live.current || reloading.current) return;
    let entry = pendingForWorkday();
    if (busy.current || (entry && !retry)) {
      if (busy.current && command?.origin === 'gps' && entry?.operation.activity_id === auth.activityId)
        queued.current = command;
      return;
    }
    if (!entry) {
      if (retry || !command || !canRecordManual() || !latest.current) return;
      const operation = { ...command, operation_id: crypto.randomUUID(), expected_revision: latest.current.revision };
      entry = { workdayId: auth.workdayId, operation, dispatch: null };
      continuity.pending = entry;
    }
    const original = entry.operation;
    const pendingEntry = entry;
    const version = epoch.current;
    busy.current = true;
    setWriting(true);
    setPending(true);
    setMessage('Lagring av holdepunkt er uavklart.');
    let dispatchedRejection = false;
    let noLongerCurrent: Latest | null = null;
    try {
      const dispatch = async () => {
        if (!alive(version)) throw Error();
        const attempt = authority.current.mutation(base, original);
        pendingEntry.dispatch = attempt;
        try { return await attempt; }
        catch (error: any) {
          dispatchedRejection = typeof error?.apiDetail === 'string' &&
            ([409, 429].includes(error?.status) || error?.status === 422 && [
              'Velg en forekomst i den bekreftede kjøringen.',
              'Holdeplassen har ingen bekreftet plattformkobling for dette lagringsforsøket.',
              'Tidspunktet for holdepunktet kunne ikke bekreftes.',
            ].includes(error.apiDetail));
          throw error;
        } finally {
          if (pendingEntry.dispatch === attempt) pendingEntry.dispatch = null;
        }
      };
      const lookup = () => authority.current.request(base + '/operations/' + original.operation_id);
      if (retry && pendingEntry.dispatch) {
        // Wait for the prior mount to finish dispatching before checking absence.
        await pendingEntry.dispatch.catch(() => undefined);
        if (!alive(version)) return;
      }
      const rec = (retry ? await recoverOperation(lookup, async () => {
        const value = await current(version, false);
        if (value.terminal || value.revision !== original.expected_revision || original.activity_id !== auth.activityId) {
          noLongerCurrent = value;
          throw Error();
        }
      }, dispatch) : await dispatch()) as Receipt;
      if (!alive(version)) return;
      if (!rec || rec.operation_id !== original.operation_id || rec.workday_id !== auth.workdayId
        || rec.accepted_revision !== original.expected_revision + 1 || !time(rec.accepted_at)) throw Error();
      const value = await current(version, false);
      if (value.revision < rec.accepted_revision || (value.revision === rec.accepted_revision
          && (!value.anchor || value.anchor.route_basis !== original.route_basis || value.anchor.activity_id !== original.activity_id
            || value.anchor.occurrence_id !== original.occurrence_id || value.anchor.coordinate_revision !== original.coordinate_revision
            || value.anchor.origin !== original.origin || Date.parse(value.anchor.evidence_at) !== Date.parse(original.evidence_at)
            || Date.parse(value.anchor.saved_at) !== Date.parse(rec.accepted_at)))) throw Error();
      latest.current = value;
      setView(value);
      clearPending();
      if (value.revision > rec.accepted_revision) {
        discardQueue();
        setMessage('Forsøket ble lagret. Et nyere holdepunkt finnes.');
      } else setMessage('Holdepunktet er lagret.');
    } catch (error: any) {
      if (!alive(version)) return;
      discardQueue();
      if ([401, 410].includes(error?.status)) {
        denied.current();
        return;
      }
      if (noLongerCurrent) {
        latest.current = noLongerCurrent; setView(noLongerCurrent);
        clearPending();
        setMessage('Forsøket ble ikke lagret. Lagret status er endret.');
      } else if (dispatchedRejection) {
        clearPending();
        try { await current(version, true); }
        catch {
          if (!alive(version)) return;
          latest.current = null;
          setView(null);
        }
        if (alive(version)) setMessage('Forslaget ble ikke lagret. ' + error.apiDetail);
      } else setMessage('Lagringen er uavklart. Kontroller eller prøv samme forsøk.');
    } finally {
      if (alive(version)) {
        busy.current = false;
        setWriting(false);
        if (!pendingForWorkday() && queued.current && !latest.current?.terminal) {
          const next = queued.current;
          queued.current = null;
          void send(next);
        }
      }
    }
  }
  const pendingActivity = pendingForWorkday()?.operation.activity_id;
  return { view, pending, priorActivity: Boolean(pendingActivity && pendingActivity !== auth.activityId),
    writing, loading, message, canRecordManual, load, send, discardQueue, forget };
}
