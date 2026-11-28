import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { usePositionAssistance } from './PositionAssistance';
import { distanceMetres, type PositionFix } from './positionSource';
import { StopProgression, type StopCall, type StopAssertion } from './stopProgression';
import { readStopProjection, usePositionAnchor, type PositionAnchorContinuity, type StopAuthority, type StopProjection } from './positionAnchorClient';

export type DrivingStopState = { calls: StopCall[]; position: number | null; phase: 'unknown' | 'remembered' | 'manual' | 'here' | 'moving' };

export function useDrivingStops(authority: StopAuthority, continuity: PositionAnchorContinuity, handoff?: string) {
  const access = usePositionAssistance();
  const source = access?.source;
  const current = useRef(authority);
  current.current = authority;
  const engine = useRef<StopProgression | null>(null);
  const firstFix = useRef<PositionFix | null>(null);
  const platform = useRef(handoff);
  const generation = useRef<number | undefined>(undefined);
  const [projection, setProjection] = useState<StopProjection | null>(null);
  const [view, setView] = useState<DrivingStopState>({calls: [], position: null, phase: 'unknown'});
  const anchor = usePositionAnchor(authority, continuity, () => {
    engine.current = null;
    setProjection(null);
    setView({calls: [], position: null, phase: 'unknown'});
  });
  const recoveryTried = useRef(false);
  useEffect(() => {
    if (!anchor.pending) recoveryTried.current = false;
    else if (!anchor.loading && !anchor.writing && !recoveryTried.current) {
      recoveryTried.current = true;
      void anchor.send(undefined, true);
    }
  }, [anchor.pending, anchor.loading, anchor.writing]);
  const latest = useRef(anchor);
  latest.current = anchor;
  const permission = useRef(access);
  permission.current = access;

  useEffect(() => {
    let active = true;
    const auth = current.current;
    void auth.request('/workdays/' + auth.workdayId + '/position-coordinates/' + auth.activityId).then(value => {
      if (!active) return;
      const route = readStopProjection(value, auth);
      if (route.terminal) return;
      engine.current = new StopProgression(route.calls);
      setProjection(route);
      const samePlatform = platform.current && route.calls[0]?.quay_id === platform.current;
      setView({calls: route.calls, position: samePlatform ? route.calls[0].position : null, phase: samePlatform ? 'here' : 'unknown'});
    }).catch(() => {});
    return () => { active = false; engine.current = null; };
  }, [authority.workdayId, authority.activityId]);

  useLayoutEffect(() => {
    const prior = anchor.view?.anchor;
    if (!prior || !projection?.route?.compatible || prior.activity_id !== authority.activityId
        || prior.route_basis !== projection.route.basis || engine.current?.read().estimate) return;
    const located = projection.calls.find(call => call.occurrence_id === prior.occurrence_id);
    if (!located) return;
    engine.current?.restore({occurrenceId: located.occurrence_id, basis: prior.origin, evidenceAt: Date.parse(prior.evidence_at)}, performance.now(), Date.now());
    setView({calls: projection.calls, position: located.position, phase: prior.origin === 'manual' ? 'manual' : 'remembered'});
  }, [projection, authority.activityId, anchor.view]);

  useEffect(() => {
    if (!source || !projection?.route?.compatible || !projection.calls.length) return;
    const route = projection.route, calls = projection.calls;
    const persist = (estimate: StopAssertion) => {
      const point = calls.find(call => call.occurrence_id === estimate.occurrenceId);
      if (!point?.coordinates) return;
      void latest.current.send({activity_id: current.current.activityId, route_basis: route.basis,
        occurrence_id: estimate.occurrenceId, coordinate_revision: point.coordinates.revision,
        origin: 'gps', evidence_at: new Date(estimate.evidenceAt).toISOString(), driving: true});
    };
    let listening = true;
    let retry: ReturnType<typeof setTimeout> | undefined;
    const resume = () => {
      if (document.visibilityState === 'visible') void permission.current?.start('stops', () => listening);
    };
    const unwatch = source.subscribe('stops', {
      state(live, subscribed) {
        if (!subscribed || ['invalid', 'timeout', 'gap', 'clock'].includes(live.reason)) {
          firstFix.current = null;
          setView(previous => previous.position === null || previous.phase === 'manual' ? previous : {...previous, phase: 'remembered'});
        }
        clearTimeout(retry);
        if (!subscribed) {
          if (['gap', 'clock', 'timeout', 'unavailable'].includes(live.reason)) retry = setTimeout(resume, 3000);
          return;
        }
        if (generation.current !== live.generation) {
          generation.current = live.generation;
          engine.current?.bind(live.generation);
        }
      },
      fix(fix) {
        const tracker = engine.current;
        if (!tracker || fix.accuracyM > 25) return;
        const state = tracker.read();
        if (!state.estimate) {
          // A departure starts on its exact first qualified platform. Require
          // consecutive live fixes inside its accuracy-adjusted perimeter.
          const own = latest.current.view?.anchor;
          if (own?.activity_id === current.current.activityId || !latest.current.canRecordManual()) return;
          const initial = calls[0];
          if (!initial.coordinates || distanceMetres(initial.coordinates, fix) + fix.accuracyM > 40) {
            firstFix.current = null;
            return;
          }
          const old = firstFix.current;
          firstFix.current = fix;
          if (!old || fix.acquiredAt - old.acquiredAt < 500 || fix.acquiredAt - old.acquiredAt > 5000) return;
          const seed = {occurrenceId: initial.occurrence_id, basis: 'gps' as const, evidenceAt: fix.acquiredAt};
          tracker.restore(seed, performance.now());
          tracker.bind(fix.generation);
          persist(seed);
          setView({calls, position: initial.position, phase: 'here'});
          return;
        }
        const estimate = tracker.receive(fix, performance.now());
        const currentState = tracker.read();
        const located = calls.find(call => call.occurrence_id === currentState.estimate?.occurrenceId);
        if (!located?.coordinates) return;
        if (estimate) persist(estimate);
        const delta = distanceMetres(located.coordinates, fix);
        const phase = currentState.stale || currentState.reason === 'reanchor' || currentState.reason === 'ambiguous' ? 'remembered'
          : delta + fix.accuracyM <= 45 ? 'here' : delta - fix.accuracyM >= 55 ? 'moving' : null;
        setView(previous => ({calls, position: located.position,
          phase: phase ?? (previous.position === located.position ? previous.phase : 'here')}));
      },
    });
    resume();
    document.addEventListener('visibilitychange', resume);
    return () => {
      listening = false;
      clearTimeout(retry);
      document.removeEventListener('visibilitychange', resume);
      unwatch();
      source.deactivate('stops');
    };
  }, [projection, source]);
  return view;
}
