import assert from 'node:assert/strict';
import { test } from 'node:test';
import { bindings, RoadLimits, WARNING_METRES, type RoadManifest } from '../src/roadLimits.ts';
import type { PositionFix } from '../src/positionSource.ts';

const epoch = Date.parse('2026-11-20T12:00:00Z');
const degree = 111_195.08;
const metres = (east: number, north = 0) => [east / degree, north / degree] as const;
type Edge = RoadManifest['packages'][number]['edges'][number];
const edge = (id: string, from: string, to: string, start: number, end: number, kmh: number | null, successors: string[]): Edge =>
  ({ id, from, to, length: end - start, shape: [metres(start), metres(end)], kmh, successors });
const a = edge('A', 'N0', 'N1', 0, 420, 50, ['B']);
const b = edge('B', 'N1', 'N2', 420, 620, 30, ['C']);
const c = edge('C', 'N2', 'N3', 620, 1_100, 70, []);
const snapshot = (edges: Edge[] = [a, b, c], path = edges.map(item => item.id)): RoadManifest => ({
  id: 'synthetic-west', revision: '1', profile: 'SL-LAB-1', uncertaintyM: 8,
  retrievedAt: new Date(epoch - 5_000).toISOString(), checkedAt: new Date(epoch - 1_000).toISOString(),
  validUntil: new Date(epoch + 300_000).toISOString(), path, packages: [{ id: 'whole', revision: '1', edges }],
});
const fix = (east: number, time: number, north = 0, extras: Partial<PositionFix> = {}): PositionFix => ({
  longitude: metres(east, north)[0], latitude: metres(east, north)[1], accuracyM: 8, heading: null, speedMps: null,
  generation: 1, acquiredAt: epoch + time, receivedWallMs: epoch + time, receivedMonoMs: time, ...extras,
});
function path(engine: RoadLimits, positions: number[], start = 0) {
  for (const [i, position] of positions.entries()) engine.receive(fix(position, start + 1_000 * i));
  return engine.read(start + 1_000 * (positions.length - 1), epoch + start + 1_000 * (positions.length - 1));
}

test('current limit waits for motion, three fixes and two seconds', () => {
  assert.equal(WARNING_METRES, 300);
  const still = new RoadLimits(snapshot());
  assert.deepEqual(path(still, [100, 100, 100]).current, { reason: 'waiting' });
  const engine = new RoadLimits(snapshot());
  assert.deepEqual(path(engine, [80, 90]).current, { reason: 'waiting' });
  assert.deepEqual(engine.receive(fix(100, 2_000)).current, { kmh: 50 });
  assert.notEqual(engine.read(2_000, epoch + 2_000).next, null);
});

test('nearest warning is shown only within the whole 300 m interval and on late start', () => {
  const engine = new RoadLimits(snapshot());
  assert.equal('kmh' in path(engine, [98, 110, 122]).next, false);
  assert.deepEqual(engine.receive(fix(134, 3_000)).next, { kmh: 30, metres: 290, id: 'N1:A:B' });
  const late = new RoadLimits(snapshot());
  assert.deepEqual(path(late, [274, 286, 298]).next, { kmh: 30, metres: 120, id: 'N1:A:B' });
  const up = new RoadLimits(snapshot());
  assert.deepEqual(path(up, [472, 484, 496]).next, { kmh: 70, metres: 120, id: 'N2:B:C' });
  const uncertain = new RoadLimits(snapshot());
  uncertain.receive(fix(60, 0, 0, { accuracyM: 25 }));
  uncertain.receive(fix(100, 1_000, 0, { accuracyM: 25 }));
  const nearThreshold = uncertain.receive(fix(135, 2_000, 0, { accuracyM: 25 }));
  assert.deepEqual(nearThreshold.current, { kmh: 50 });
  assert.deepEqual(nearThreshold.next, { reason: 'uncertain' });
});

test('boundary overlap clears the old value and passage requires new evidence', () => {
  const engine = new RoadLimits(snapshot());
  assert.deepEqual(path(engine, [376, 388, 400]).current, { kmh: 50 });
  for (const [i, position] of [410, 418, 429, 441, 453].entries()) {
    assert.equal('kmh' in engine.receive(fix(position, 3_000 + i * 1_000)).current, position === 410);
  }
  const after = engine.receive(fix(465, 8_000));
  assert.deepEqual(after.current, { kmh: 30 });
  assert.deepEqual(after.next, { kmh: 70, metres: 160, id: 'N2:B:C' });
});

test('unsupported onward branch, uncovered data and expired sources are distinct', () => {
  const split = { ...a, successors: ['B', 'T'] };
  const diverted: Edge = { id: 'T', from: 'N1', to: 'N4', kmh: 40, length: 200, successors: [], shape: [metres(420), metres(420, 200)] };
  const unknownBranch = new RoadLimits(snapshot([split, b, c, diverted], ['A']));
  const branch = path(unknownBranch, [150, 165, 180]);
  assert.deepEqual(branch.current, { kmh: 50 });
  assert.deepEqual(branch.next, { reason: 'branch' });
  const directed = new RoadLimits(snapshot([split, b, c, diverted], ['A', 'B', 'C']));
  assert.equal('kmh' in path(directed, [150, 165, 180]).next, true);
  const gap = new RoadLimits(snapshot([a], ['A']));
  assert.deepEqual(path(gap, [150, 165, 180]).next, { reason: 'coverage' });
  const expired = new RoadLimits({ ...snapshot(), validUntil: new Date(epoch + 1_900).toISOString() });
  assert.deepEqual(path(expired, [150, 165, 180]).current, { reason: 'source' });
});

test('an unresolved exit blocks lookahead while the approached road remains qualified', () => {
  const approach = { ...a, successors: ['B', 'exit-med'] };
  const exit: Edge = { id: 'exit-med', from: 'N1', to: 'N4', kmh: null, length: 40,
    successors: [], shape: [metres(420), metres(420, 40)] };
  const reverseExit: Edge = { ...exit, id: 'exit-mot', from: 'N4', to: 'N1', shape: [...exit.shape].reverse(), successors: ['B'] };
  const engine = new RoadLimits(snapshot([approach, b, c, exit, reverseExit], []));
  assert.deepEqual(path(engine, [145, 160, 175]), { current: { kmh: 50 }, next: { reason: 'branch' } });
  assert.deepEqual(path(engine, [220, 260, 300, 340, 380, 402, 418, 436, 453, 470], 3_000), {
    current: { kmh: 30 }, next: { kmh: 70, metres: 150, id: 'N2:B:C' },
  });
  const partial = new RoadLimits(snapshot([approach, b, c], []));
  assert.deepEqual(path(partial, [145, 160, 175]).next, { reason: 'branch' });
});

test('parallel roads stay unknown, stale data clears, and no jump invents a transition', () => {
  const parallel = { ...edge('D', 'P1', 'P2', 0, 420, 20, []), shape: [metres(0, 6), metres(420, 6)] };
  assert.deepEqual(path(new RoadLimits(snapshot([a, b, c, parallel], ['A', 'B', 'C'])), [95, 110, 125]).current, { reason: 'uncertain' });
  const engine = new RoadLimits(snapshot());
  assert.deepEqual(path(engine, [95, 110, 125]).current, { kmh: 50 });
  assert.deepEqual(engine.read(7_001, epoch + 7_001).current, { reason: 'stale' });
  assert.deepEqual(path(engine, [135, 150, 165], 8_000).current, { kmh: 50 });
  assert.deepEqual(engine.receive(fix(500, 11_000)).current, { reason: 'uncertain' });
});

test('package ordering and overlap preserve the physical result; conflicts are rejected', () => {
  const original = snapshot();
  const left = { id: 'left', revision: '1', edges: [a, b] };
  const right = { id: 'right', revision: '1', edges: [b, c] };
  const expected = path(new RoadLimits(original), [220, 230, 240]);
  for (const packs of [[left, right], [right, left]]) {
    assert.deepEqual(path(new RoadLimits({ ...original, packages: packs }), [220, 230, 240]), expected);
  }
  assert.equal(bindings({ ...original, packages: [left, { ...right, edges: [{ ...b, kmh: 40 }, c] }] }), null);
});

test('a second manifest and renamed topology need no matcher or warning changes', () => {
  const name = (item: string) => 'east-' + item;
  const edges = [a, b, c].map(item => ({
    ...item, id: name(item.id), from: name(item.from), to: name(item.to), successors: item.successors.map(name),
  }));
  const engine = new RoadLimits({ ...snapshot(edges), id: 'synthetic-east' });
  const result = path(engine, [145, 160, 175]);
  assert.deepEqual(result.current, { kmh: 50 });
  assert.deepEqual(result.next, { kmh: 30, metres: 250, id: 'east-N1:east-A:east-B' });
});

test('a dated route-neutral area permits preview geometry without leaking stale speed limits', () => {
  const previousWeek = new Date(epoch - 8 * 86_400_000).toISOString();
  const area: RoadManifest = {
    ...snapshot([{ ...a, confirmedTransitions: ['B'] }, b, c], []),
    profile: 'NVDB-AREA-1',
    validFrom: new Date(epoch - 100_000).toISOString(),
    retrievedAt: previousWeek,
  };
  const geometry = {
    ...area,
    checkedAt: previousWeek,
    packages: area.packages.map(pack => ({ ...pack, edges: pack.edges.map(segment => ({ ...segment, kmh: null })) })),
  };
  assert.equal(bindings({ ...area, path: ['A', 'B'] }), null);
  assert.equal(new RoadLimits(geometry).isFresh(epoch - 100_001), false);
  assert.equal(new RoadLimits(geometry).isFresh(epoch + 300_000), false);
  assert.deepEqual(path(new RoadLimits(geometry), [145, 160, 175]).current, { reason: 'unverified' });
  assert.deepEqual(path(new RoadLimits(area), [145, 160, 175]).current, { reason: 'source' });
  const current = { ...area, retrievedAt: snapshot().retrievedAt };
  assert.deepEqual(path(new RoadLimits(current), [145, 160, 175]).next, { kmh: 30, metres: 250, id: 'N1:A:B' });
  const unlocated = { ...current, packages: snapshot([a, b, c], []).packages };
  assert.deepEqual(path(new RoadLimits(unlocated), [145, 160, 175]).next, { reason: 'unverified' });
});

test('an area distinguishes both directions during slow motion across several GPS fixes', () => {
  const opposite = { ...a, id: 'reverse-A', from: a.to, to: a.from, shape: [...a.shape].reverse(), successors: [] };
  const area: RoadManifest = {
    ...snapshot([a, opposite, b], []), profile: 'NVDB-AREA-1', uncertaintyM: 10,
    validFrom: new Date(epoch - 30_000).toISOString(),
  };
  assert.deepEqual(path(new RoadLimits(area), [145, 151, 157, 163, 169]).current, { kmh: 50 });
});

test('a changed area withholds a transition into a masked road and keeps a distant warning', () => {
  const west = { ...a, confirmedTransitions: ['B'] };
  const east = { ...b, confirmedTransitions: ['C'] };
  const area: RoadManifest = {
    ...snapshot([west, east, c], []), profile: 'NVDB-AREA-1',
    validFrom: new Date(epoch - 30_000).toISOString(),
  };
  assert.equal('kmh' in path(new RoadLimits(area), [145, 160, 175]).next, true);
  const maskedNext = { ...area, packages: [{ ...area.packages[0], edges: [west, { ...east, kmh: null }, c] }] };
  const approach = path(new RoadLimits(maskedNext), [145, 160, 175]);
  assert.deepEqual(approach.current, { kmh: 50 });
  assert.equal('kmh' in approach.next, false);
  const masked = { ...area, packages: [{ ...area.packages[0], edges: [{ ...west, kmh: null }, east, c] }] };
  assert.deepEqual(path(new RoadLimits(masked), [145, 160, 175]), {
    current: { reason: 'unverified' }, next: { reason: 'unverified' },
  });
  assert.deepEqual(path(new RoadLimits(masked), [465, 480, 495]).next, { kmh: 70, metres: 130, id: 'N2:B:C' });
});

test('a registered area expires at its situation lease and can renew the unchanged revision', () => {
  const area: RoadManifest = {
    ...snapshot([a, b, c], []), profile: 'NVDB-AREA-1',
    validFrom: new Date(epoch - 30_000).toISOString(),
    situationLeaseUntil: new Date(epoch + 7_000).toISOString(),
  };
  const expired = new RoadLimits(area);
  assert.deepEqual(path(expired, [145, 160, 175]).current, { kmh: 50 });
  assert.deepEqual(expired.read(7_000, epoch + 7_000).current, { reason: 'source' });
  const renewed = new RoadLimits(area);
  renewed.renewSituationLease(new Date(epoch + 20_000).toISOString(), epoch + 4_000);
  assert.deepEqual(path(renewed, [145, 160, 175], 9_000).current, { kmh: 50 });
});
