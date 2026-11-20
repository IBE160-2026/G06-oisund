import assert from 'node:assert/strict';
import { test } from 'node:test';
import { proposeStop, type SavedStopAnchor, type StopRoute } from '../src/positionAnchorClient.ts';
import { StopProgression, type StopCall } from '../src/stopProgression.ts';
import type { PositionFix } from '../src/positionSource.ts';

const base = Date.parse('2026-11-02T23:24:00+01:00');
const point = (latitude: number, longitude: number) => ({
  latitude, longitude, revision: 'synthetic-c1', mapping_revision: 'synthetic-m1', stop_place_version: '1', quay_version: '1',
});
const points = {
  B: point(69.0010, 18.0100), C: point(69.0040, 18.0200), D: point(69.0060, 18.0120),
  E: point(69.0030, 18.0300), F: point(69.0040, 18.0400), G: point(69.0050, 18.0500),
};
type Letter = keyof typeof points;
const call = (trip: string, position: number, letter: Letter): StopCall => ({
  position, occurrence_id: trip + '-o' + position, name: letter, stop_place_id: 'FIX:SP:' + letter,
  quay_id: 'FIX:Q:' + letter, coordinates: points[letter], coordinate_issue: null, arrival: null, departure: null,
});
const tripA = ['B', 'C', 'D', 'B', 'E', 'F', 'G'].map((letter, index) => call('A', index + 2, letter as Letter));
const tripB = ['G', 'D', 'C'].map((letter, index) => call('B', index + 3, letter as Letter));
const fix = (time: number, latitude: number, longitude: number, options?: Partial<PositionFix>): PositionFix => ({
  generation: 1, acquiredAt: base + time, receivedWallMs: base + time + 1000, receivedMonoMs: time + 1000,
  latitude, longitude, accuracyM: 8, speedMps: null, heading: null, ...options,
});
function publish(engine: StopProgression, sample: PositionFix) {
  return engine.receive(sample, sample.receivedMonoMs);
}
function approach(engine: StopProgression, time: number, from: Letter, to: Letter, generation = 1) {
  const segment = [0.68, 0.89, 1];
  return segment.map((part, index) => publish(engine, fix(time + index * 4000,
    points[from].latitude + part * (points[to].latitude - points[from].latitude),
    points[from].longitude + part * (points[to].longitude - points[from].longitude), { generation })));
}

test('start uses the selected occurrence and only coherent departure/approach advances one occurrence', () => {
  const engine = new StopProgression(tripA);
  assert.equal(engine.choose('A-o1', base, 0), false);
  assert.equal(engine.choose('B-o3', base, 0), false);
  assert.equal(engine.choose('A-o2', base, 0), true);
  engine.bind(1);
  assert.equal(publish(engine, fix(1000, points.C.latitude, points.C.longitude)), null);
  assert.deepEqual(approach(engine, 33000, 'B', 'C').map(value => value?.occurrenceId), [undefined, undefined, 'A-o3']);
  assert.equal(engine.read().assertion?.occurrenceId, 'A-o2');
  assert.equal(engine.read().estimate?.basis, 'gps');
  assert.equal(tripA.filter(item => item.quay_id === 'FIX:Q:B').length, 2);
});

test('a late callback cannot resume 3→6 and correction resists a contradictory early fix', () => {
  const engine = new StopProgression(tripA);
  engine.choose('A-o3', base, 0);
  engine.bind(1);
  engine.interrupt();
  assert.equal(engine.read().stale, true);
  assert.equal(engine.read().estimate?.occurrenceId, 'A-o3');
  assert.ok(approach(engine, 21000, 'C', 'D').every(result => result === null));
  assert.equal(engine.choose('A-o6', base + 40000, 40000), true);
  engine.bind(2);
  assert.equal(publish(engine, fix(41000, points.F.latitude, points.F.longitude, { generation: 2 })), null);
  assert.equal(engine.read().reason, 'protecting');
  assert.equal(engine.read().estimate?.occurrenceId, 'A-o6');
  assert.equal(publish(engine, fix(61000, points.F.latitude, points.F.longitude)), null);
  assert.deepEqual(approach(engine, 63000, 'E', 'F', 2).map(value => value?.occurrenceId), [undefined, undefined, 'A-o7']);
  assert.equal(engine.read().assertion?.occurrenceId, 'A-o6');
  assert.equal(engine.read().assertion?.evidenceAt, base + 40000);
  engine.interrupt(true);
  assert.equal(engine.read().estimate, null);
});

test('weak, stale, duplicated, implausible and overlapping fixes never advance by age or point alone', () => {
  const engine = new StopProgression(tripA);
  engine.choose('A-o4', base, 0);
  engine.bind(1);
  const raw = fix(21000, points.B.latitude, points.B.longitude, { accuracyM: 31 });
  assert.equal(publish(engine, raw), null);
  assert.equal(engine.read().reason, 'poor');
  assert.equal(publish(engine, raw), null);
  assert.equal(publish(engine, fix(23000, points.B.latitude, points.B.longitude, { receivedWallMs: base + 35_000 })), null);
  assert.equal(engine.read().reason, 'stale');
  assert.ok(approach(engine, 31000, 'D', 'B').every(value => value === null));
  assert.equal(engine.read().reason, 'ambiguous');
  assert.equal(engine.read().estimate?.occurrenceId, 'A-o4');
  assert.equal(publish(engine, fix(40000, points.G.latitude, points.G.longitude)), null);
  assert.equal(engine.read().reason, 'reanchor');
  const missing = new StopProgression([tripA[0], { ...tripA[1], coordinates: null, coordinate_issue: 'validity-unknown' }]);
  assert.equal(missing.canFollow('A-o2'), false);
});

test('a post-protection jump requires an explicit correction before later coherent fixes can advance', () => {
  const engine = new StopProgression(tripA);
  engine.choose('A-o2', base, 0);
  engine.bind(1);
  publish(engine, fix(21_000, points.B.latitude, points.B.longitude));
  assert.equal(publish(engine, fix(22_000, points.F.latitude, points.F.longitude)), null);
  assert.equal(engine.read().reason, 'reanchor');
  engine.invalidate('poor');
  assert.equal(engine.read().reason, 'reanchor');
  assert.ok(approach(engine, 25_000, 'B', 'C').every(value => value === null));
  assert.equal(engine.read().estimate?.occurrenceId, 'A-o2');
  assert.equal(engine.choose('A-o2', base + 40_000, 40_000), true);
  assert.deepEqual(approach(engine, 61_000, 'B', 'C').map(value => value?.occurrenceId),
    [undefined, undefined, 'A-o3']);
});

test('A-o8 maps by exact proven Quay to B-o3 after midnight, preserving original origin and time', () => {
  const anchor: SavedStopAnchor = {
    workday_id: 'W1', activity_id: 'A', service_date: '2026-11-02', journey_id: 'A-journey', pattern_id: 'A-pattern',
    occurrence_id: 'A-o8', revision: 6, route_basis: 'a'.repeat(64), origin: 'gps',
    evidence_at: '2026-11-02T23:48:00+01:00', saved_at: '2026-11-02T23:48:02+01:00', asserted_at: null, carried_from: null,
    quay_id: 'FIX:Q:G', stop_place_id: 'FIX:SP:G', coordinate_revision: 'synthetic-c1', mapping_revision: 'synthetic-m1',
    quay_version: '1', stop_place_version: '1',
  };
  const route: StopRoute = { activity_id: 'B', service_date: '2026-11-03', journey_id: 'B-journey', pattern_id: 'B-pattern',
    decision_revision: 1, start_position: 3, end_position: 5, basis: 'b'.repeat(64), compatible: true, source_version: 'synthetic' };
  const result = proposeStop(anchor, 'W1', route, tripB);
  assert.equal(result?.kind === 'unique' && result.call.occurrence_id, 'B-o3');
  assert.equal(Date.parse('2026-11-03T00:08:00+01:00') - Date.parse(anchor.evidence_at), 20 * 60 * 1000);
  assert.equal(anchor.origin, 'gps');
  assert.equal(proposeStop(anchor, 'W2', route, tripB), null);
  assert.equal(proposeStop(anchor, 'W1', route, tripB.slice(1))?.kind, 'no-match');
  assert.equal(proposeStop(anchor, 'W1', route, [...tripB, call('B', 6, 'G')])?.kind, 'ambiguous');
  assert.equal(proposeStop(anchor, 'W1', route, [{ ...tripB[0], quay_id: 'FIX:Q:G-other' }, ...tripB.slice(1)])?.kind, 'no-match');
  assert.equal(proposeStop(anchor, 'W1', route, [{ ...tripB[0], coordinates: null }, ...tripB.slice(1)])?.kind, 'unverified');
});
