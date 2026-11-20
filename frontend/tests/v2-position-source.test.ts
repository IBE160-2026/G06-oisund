import assert from 'node:assert/strict';
import { test } from 'node:test';
import { GpsSpeed } from '../src/gpsSpeed.ts';
import { POSITION_OPTIONS, PositionSource, type PositionFix, type PositionState } from '../src/positionSource.ts';

const origin = 1_790_000_000_000;
const position = (at: number, speed: number | null = null, accuracy = 10) => ({
  timestamp: origin + at,
  coords: { latitude: 69, longitude: 18, accuracy, speed, heading: null },
}) as GeolocationPosition;

function setup(t: { after: (fn: () => void) => void }, overrides: { missing?: boolean; insecure?: boolean } = {}) {
  const callbacks: Array<{ fix: PositionCallback; error: PositionErrorCallback }> = [];
  const stops: number[] = [];
  let mono = 0;
  let offset = origin;
  let allowed = true;
  const go = (at: number) => { mono = at; };
  const source = new PositionSource({
    geolocation: overrides.missing ? null : {
      watchPosition(fix, error, options) {
        assert.deepEqual(options, POSITION_OPTIONS);
        callbacks.push({ fix, error: error! });
        return callbacks.length;
      },
      clearWatch(id) { stops.push(id); },
    },
    secure: !overrides.insecure,
    allowed: () => allowed,
    clock: { wall: () => offset + mono, monotonic: () => mono },
  });
  t.after(() => source.stop('off'));
  const publish = (p: GeolocationPosition, index = callbacks.length - 1) => callbacks[index].fix(p);
  return { source, callbacks, stops, go, publish, drift: (ms: number) => { offset += ms; }, deny: () => { allowed = false; } };
}

const makeFix = (at: number, speedMps: number | null, values?: Partial<PositionFix>): PositionFix => ({
  generation: 1, acquiredAt: origin + at, receivedWallMs: origin + at, receivedMonoMs: at,
  latitude: 69, longitude: 18, accuracyM: 8, speedMps, heading: null, ...values,
});

test('one watch serves only explicitly active consumers, with late callbacks ignored after pause', t => {
  const { source, callbacks, stops, go, publish } = setup(t);
  const fixes: PositionFix[] = [], stopFixes: PositionFix[] = [];
  source.subscribe('speed', { state() {}, fix: fix => fixes.push(fix) });
  source.subscribe('stops', { state() {}, fix: fix => stopFixes.push(fix) });
  assert.equal(callbacks.length, 0);
  source.activate('speed');
  go(1_000);
  publish(position(1_000, null));
  assert.equal(fixes.at(-1)?.speedMps, null);
  assert.equal(stopFixes.length, 0);
  source.activate('stops');
  assert.equal(callbacks.length, 1);
  go(2_000);
  publish(position(2_000, 10));
  assert.equal(stopFixes.at(-1)?.acquiredAt, origin + 2_000);
  source.deactivate('speed');
  assert.equal(stops.length, 0);
  source.stop('paused');
  assert.deepEqual(stops, [1]);
  go(3_000);
  publish(position(3_000, 10));
  assert.equal(fixes.length, 2);
  assert.equal(stopFixes.length, 1);
  source.activate('speed');
  publish(position(3_000, 10), 0);
  assert.equal(fixes.length, 2);
  publish(position(3_000, 10));
  assert.equal(fixes.length, 3);
  assert.equal(stopFixes.length, 1);
});

test('a duplicate cannot move the hard gap deadline; forward and backward clock jumps invalidate', t => {
  const { source, callbacks, stops, go, publish, drift } = setup(t);
  let reason = '';
  source.subscribe('road', { state: state => { reason = state.reason; }, fix() {} });
  source.activate('road');
  go(1_000);
  publish(position(1_000));
  go(10_999);
  publish(position(1_000));
  source.verify();
  assert.equal(stops.length, 0);
  go(11_000);
  source.verify();
  assert.equal(reason, 'gap');
  source.activate('road');
  drift(1_001);
  source.verify();
  assert.equal(reason, 'clock');
  source.activate('road');
  drift(-1_001);
  source.verify();
  assert.equal(reason, 'clock');
  source.activate('road');
  publish(position(11_001), 3);
  assert.equal(reason, 'clock');
  assert.deepEqual(stops, [1, 2, 3, 4]);
  assert.equal(callbacks.length, 4);
});

test('missing API, insecure context, native errors and lost access clear the watch', t => {
  const read = (source: PositionSource) => {
    let state: PositionState | undefined;
    source.subscribe('speed', { state: value => { state = value; }, fix() {} });
    return () => state;
  };
  for (const [options, reason] of [[{ missing: true }, 'unsupported'], [{ insecure: true }, 'insecure']] as const) {
    const { source, callbacks } = setup(t, options);
    const state = read(source);
    source.activate('speed');
    assert.equal(state()?.reason, reason);
    assert.equal(callbacks.length, 0);
  }
  const { source, callbacks, deny } = setup(t);
  const state = read(source);
  for (const [index, [code, reason]] of [[1, 'denied'], [2, 'unavailable'], [3, 'timeout']].entries()) {
    source.activate('speed');
    callbacks[index].error({ code } as GeolocationPositionError);
    assert.equal(state()?.reason, reason);
    assert.equal(state()?.running, false);
  }
  source.activate('speed');
  deny();
  source.verify();
  assert.equal(state()?.reason, 'access');
});

test('speed requires a coherent native pair, distinguishes zero, small values and invalid numbers', () => {
  for (const [mps, value] of [[0, '0'], [0.1, '<1'], [0.5, '2'], [10, '36'], [12.5, '45']] as const) {
    const gps = new GpsSpeed();
    assert.deepEqual(gps.receive(makeFix(0, mps)), { kind: 'unknown', reason: 'waiting' });
    const current = gps.receive(makeFix(700, mps));
    assert.equal(current.kind === 'qualified' && current.displayKmh, value);
  }
  for (const value of [null, undefined, -1, 56, NaN, Infinity, '0']) {
    const gps = new GpsSpeed();
    gps.receive(makeFix(0, 10));
    assert.deepEqual(gps.receive(makeFix(1_000, value as number | null)), { kind: 'unknown', reason: 'missing' });
  }
});

test('exact freshness, irregular samples, inaccurate fixes and jumps require a new pair', () => {
  const gps = new GpsSpeed();
  gps.receive(makeFix(0, 0));
  assert.equal(gps.receive(makeFix(100, 10)).kind, 'unknown');
  assert.equal(gps.receive(makeFix(1_000, 5)).kind, 'qualified');
  assert.equal(gps.receive(makeFix(1_800, 10)).kind, 'qualified');
  assert.equal(gps.read(4_799).kind, 'qualified');
  assert.deepEqual(gps.read(4_800), { kind: 'unknown', reason: 'stale' });
  assert.equal(gps.receive(makeFix(5_000, 0)).kind, 'unknown');
  assert.deepEqual(gps.receive(makeFix(5_500, 15)), { kind: 'unknown', reason: 'jump' });
  assert.equal(gps.receive(makeFix(6_000, 10)).kind, 'unknown');
  assert.equal(gps.receive(makeFix(6_500, 10)).kind, 'qualified');
  assert.deepEqual(gps.receive(makeFix(7_000, 10, { longitude: 20 })), { kind: 'unknown', reason: 'jump' });
  assert.deepEqual(gps.receive(makeFix(7_500, 10, { accuracyM: 31 })), { kind: 'unknown', reason: 'inaccurate' });
  gps.receive(makeFix(8_000, 0));
  const delayed = gps.receive(makeFix(8_500, 0, { receivedWallMs: origin + 9_000, receivedMonoMs: 9_000 }));
  assert.equal(delayed.kind === 'qualified' && delayed.validUntilMono, 11_500);
  assert.equal(gps.read(11_500).kind, 'unknown');
});
