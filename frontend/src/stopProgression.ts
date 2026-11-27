import { distanceMetres, fixAge, RAW_FIX_GAP_MS, type PositionFix } from './positionSource.ts';

export type StopPoint = {
  latitude: number; longitude: number; revision: string; mapping_revision: string;
  stop_place_version: string; quay_version: string;
};
export type StopCall = {
  position: number; occurrence_id: string; name: string | null;
  stop_place_id: string | null; quay_id: string | null;
  arrival: { utc: string | null; calendar_time: string | null } | null;
  departure: { utc: string | null; calendar_time: string | null } | null;
  coordinates: StopPoint | null; coordinate_issue: string | null;
};
type Reason = 'waiting' | 'protecting' | 'tracking' | 'poor' | 'stale' | 'ambiguous' | 'reanchor' | 'range-end' | 'manual';
export type StopAssertion = { occurrenceId: string; basis: 'manual' | 'gps'; evidenceAt: number };
export type StopProgress = {
  assertion: StopAssertion | null; estimate: StopAssertion | null; stale: boolean; reason: Reason;
};

// Conservative trial values. These gates require qualification on the
// supported carriageway/stop layout and device before real GPS use.
export const MANUAL_PROTECTION_MS = 20_000;
const WINDOW_MS = 30_000;
// Keep the full qualification span even with one fix per second.
const MAX_SAMPLES = 64;
const MIN_SPAN_MS = 6_000;
const ACCURACY_LIMIT_M = 30;
const ENTER_RADIUS_M = 45;
const LEAVE_RADIUS_M = 55;
const CORRIDOR_MARGIN_M = 45;
const COMPETITOR_MARGIN_M = 14;
const MAX_SPEED_MPS = 35;

export class StopProgression {
  private state: StopProgress = { assertion: null, estimate: null, stale: false, reason: 'waiting' };
  private samples: PositionFix[] = [];
  private generation: number | null = null;
  private assertionMono = 0;
  private lastAcquisition = -Infinity;
  private needsAnchor = false;

  constructor(private readonly calls: readonly StopCall[]) {}

  read() { return this.state; }

  canFollow(occurrenceId: string) {
    const at = this.calls.findIndex(call => call.occurrence_id === occurrenceId);
    return at >= 0 && Boolean(this.calls[at].coordinates && this.calls[at + 1]?.coordinates);
  }

  choose(occurrenceId: string, wall: number, mono: number) {
    if (!this.calls.some(call => call.occurrence_id === occurrenceId)) return false;
    const assertion: StopAssertion = { occurrenceId, evidenceAt: wall, basis: 'manual' };
    this.samples = [];
    this.lastAcquisition = wall;
    this.assertionMono = mono;
    this.needsAnchor = false;
    this.state = { assertion, estimate: assertion, reason: 'protecting', stale: false };
    return true;
  }

  restore(assertion: StopAssertion, mono: number) {
    if (!this.calls.some(call => call.occurrence_id === assertion.occurrenceId)) return;
    this.assertionMono = assertion.basis === 'manual' ? mono : -Infinity;
    this.samples = [];
    this.lastAcquisition = assertion.evidenceAt;
    this.needsAnchor = false;
    this.state = { assertion, estimate: assertion, reason: 'waiting', stale: false };
  }

  bind(generation: number) {
    this.generation = generation;
    this.samples = [];
  }

  interrupt(clear = false) {
    this.generation = null;
    this.samples = [];
    this.state = clear
      ? { assertion: null, estimate: null, stale: false, reason: 'waiting' }
      : { ...this.state, stale: Boolean(this.state.estimate), reason: 'stale' };
  }

  invalidate(reason: 'poor' | 'stale') {
    this.samples = [];
    this.state = { ...this.state, reason: this.needsAnchor ? 'reanchor' : reason, stale: this.state.estimate?.basis === 'gps' };
  }

  private requireAnchor() {
    this.samples = [];
    this.needsAnchor = true;
    this.state = { ...this.state, reason: 'reanchor', stale: this.state.estimate?.basis === 'gps' };
  }

  receive(fix: PositionFix, mono: number) {
    const { estimate, assertion } = this.state;
    if (!estimate || !assertion || this.needsAnchor || fix.generation !== this.generation || !Number.isFinite(fix.acquiredAt)
        || fix.acquiredAt <= this.lastAcquisition || fix.acquiredAt > fix.receivedWallMs) return null;
    this.lastAcquisition = fix.acquiredAt;
    const age = fixAge(fix, mono);
    if (!Number.isFinite(age) || age < 0 || age >= RAW_FIX_GAP_MS) { this.invalidate('stale'); return null; }
    if (!Number.isFinite(fix.accuracyM) || fix.accuracyM < 0 || fix.accuracyM > ACCURACY_LIMIT_M) {
      this.invalidate('poor');
      return null;
    }
    const at = this.calls.findIndex(call => call.occurrence_id === estimate.occurrenceId);
    const current = this.calls[at]?.coordinates, next = this.calls[at + 1];
    const target = next?.coordinates;
    if (!next || !current || !target) {
      this.state = { ...this.state, reason: next ? 'manual' : 'range-end' };
      return null;
    }
    const segment = distanceMetres(current, target);
    const previous = this.samples.at(-1);
    const since = previous ? (fix.acquiredAt - previous.acquiredAt) / 1000 : 0;
    const protectedNow = mono - this.assertionMono < MANUAL_PROTECTION_MS;
    if (previous && (since >= RAW_FIX_GAP_MS / 1000
      || distanceMetres(previous, fix) > since * MAX_SPEED_MPS + previous.accuracyM + fix.accuracyM)) {
      if (!protectedNow && previous.receivedMonoMs - this.assertionMono >= MANUAL_PROTECTION_MS) {
        this.requireAnchor();
        return null;
      }
      // A discarded pre-protection sample cannot invalidate the manual choice.
      // Qualify a new coherent sequence without it.
      this.samples = [];
    }
    this.samples = [...this.samples.filter(sample => fix.acquiredAt - sample.acquiredAt <= WINDOW_MS), fix].slice(-MAX_SAMPLES);
    if (protectedNow) {
      this.state = { ...this.state, reason: 'protecting' };
      return null;
    }
    const withinCorridor = (sample: PositionFix) =>
      distanceMetres(current, sample) + distanceMetres(target, sample) <= segment + CORRIDOR_MARGIN_M + sample.accuracyM;
    if (this.samples.length >= 3 && this.samples.slice(-3).every(sample => !withinCorridor(sample))) {
      this.requireAnchor();
      return null;
    }
    const near = distanceMetres(target, fix);
    const competing = this.calls.some((call, index) => index !== at + 1 && call.coordinates
      && distanceMetres(call.coordinates, fix) <= near + COMPETITOR_MARGIN_M + 2 * fix.accuracyM);
    if (near + fix.accuracyM <= ENTER_RADIUS_M && competing) {
      this.state = { ...this.state, reason: 'ambiguous' };
      return null;
    }
    // Form a consecutive approach since the last contradictory fix.
    let lastOutside = this.samples.length - 1;
    while (lastOutside >= 0 && withinCorridor(this.samples[lastOutside])) lastOutside--;
    const approach = this.samples.slice(lastOutside + 1);
    const first = approach[0], middle = approach.length > 2 ? approach[approach.length - 2] : undefined;
    const supported = first && middle && fix.acquiredAt - first.acquiredAt >= MIN_SPAN_MS
      && distanceMetres(current, fix) - fix.accuracyM >= LEAVE_RADIUS_M
      && near + fix.accuracyM <= ENTER_RADIUS_M
      && distanceMetres(target, first) - near > first.accuracyM + fix.accuracyM + COMPETITOR_MARGIN_M
      && distanceMetres(target, middle) >= near - (middle.accuracyM + fix.accuracyM)
      && approach.every((sample, index) => index === 0
        || distanceMetres(target, sample) <= distanceMetres(target, approach[index - 1]) + sample.accuracyM);
    if (!supported) {
      this.state = { ...this.state, reason: 'tracking' };
      return null;
    }
    const advanced: StopAssertion = { occurrenceId: next.occurrence_id, basis: 'gps', evidenceAt: fix.acquiredAt };
    this.state = { ...this.state, estimate: advanced, stale: false,
      reason: !this.calls[at + 2] ? 'range-end' : this.calls[at + 2].coordinates ? 'tracking' : 'manual' };
    this.samples = [];
    return advanced;
  }
}
