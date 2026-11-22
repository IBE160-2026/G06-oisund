export const POSITION_OPTIONS: PositionOptions = { maximumAge: 0, enableHighAccuracy: true, timeout: 10_000 };
export const RAW_FIX_GAP_MS = 10_000;
const CLOCK_DRIFT_MS = 1_000;

export type PositionConsumer = 'speed' | 'stops' | 'road';
export type PositionReason = 'off' | 'paused' | 'hidden' | 'access' | 'unsupported' | 'insecure'
  | 'denied' | 'unavailable' | 'timeout' | 'gap' | 'clock' | 'invalid' | 'acquiring';
export type PositionFix = Readonly<{
  generation: number;
  acquiredAt: number;
  receivedWallMs: number;
  receivedMonoMs: number;
  latitude: number;
  longitude: number;
  accuracyM: number;
  speedMps: number | null;
  heading: number | null;
}>;
export type PositionState = Readonly<{
  generation: number;
  running: boolean;
  reason: PositionReason;
}>;
type Observer = { state: (state: PositionState, active: boolean) => void; fix: (fix: PositionFix) => void };
type Clock = { wall: () => number; monotonic: () => number };
type SourceOptions = {
  geolocation: Pick<Geolocation, 'watchPosition' | 'clearWatch'> | null;
  secure: boolean;
  allowed: () => boolean;
  clock: Clock;
};

const errorReason = (code: number): PositionReason => code === 1 ? 'denied' : code === 3 ? 'timeout' : 'unavailable';
const validNumber = (value: unknown, min: number, max: number): value is number =>
  typeof value === 'number' && Number.isFinite(value) && value >= min && value <= max;

export function fixAge(fix: PositionFix, mono: number) {
  return fix.receivedWallMs - fix.acquiredAt + mono - fix.receivedMonoMs;
}

export function distanceMetres(a: Pick<PositionFix, 'latitude' | 'longitude'>, b: Pick<PositionFix, 'latitude' | 'longitude'>) {
  const rad = Math.PI / 180;
  const sinLat = Math.sin((b.latitude - a.latitude) * rad / 2);
  const sinLon = Math.sin((b.longitude - a.longitude) * rad / 2);
  const squared = sinLat ** 2 + Math.cos(a.latitude * rad) * Math.cos(b.latitude * rad) * sinLon ** 2;
  return 12_742_008.8 * Math.asin(Math.min(1, Math.sqrt(squared)));
}

export class PositionSource {
  private readonly observers = new Map<Observer, PositionConsumer>();
  private readonly requested = new Set<PositionConsumer>();
  private value: PositionState = { generation: 0, running: false, reason: 'off' };
  private watch: number | undefined;
  private timer: ReturnType<typeof setTimeout> | undefined;
  private gapDeadline = 0;
  private clockOffset = 0;
  private previousTimestamp = -Infinity;

  constructor(private readonly options: SourceOptions) {}

  get running() { return this.value.running; }

  subscribe(consumer: PositionConsumer, observer: Observer) {
    this.observers.set(observer, consumer);
    observer.state(this.value, this.requested.has(consumer));
    return () => { this.observers.delete(observer); };
  }

  private report(reason: PositionReason, running = this.value.running, generation = this.value.generation) {
    this.value = { generation, running, reason };
    this.observers.forEach((consumer, observer) => observer.state(this.value, this.requested.has(consumer)));
  }

  activate(consumer: PositionConsumer) {
    if (!this.options.allowed()) { this.stop('access'); return; }
    if (!this.options.secure) { this.stop('insecure'); return; }
    const location = this.options.geolocation;
    if (!location) { this.stop('unsupported'); return; }
    this.requested.add(consumer);
    if (this.value.running) { this.report(this.value.reason); return; }

    const generation = this.value.generation + 1;
    const mono = this.options.clock.monotonic();
    this.clockOffset = this.options.clock.wall() - mono;
    this.gapDeadline = mono + RAW_FIX_GAP_MS;
    this.previousTimestamp = -Infinity;
    this.report('acquiring', true, generation);
    this.scheduleGap();
    try {
      const id = location.watchPosition(
        position => this.receive(position, generation),
        error => { if (this.isLive(generation)) this.stop(errorReason(error.code)); },
        POSITION_OPTIONS,
      );
      if (this.isLive(generation)) this.watch = id;
      else location.clearWatch(id);
    } catch {
      if (this.isLive(generation)) this.stop('unavailable');
    }
  }

  deactivate(consumer: PositionConsumer) {
    if (!this.requested.delete(consumer)) return;
    if (this.requested.size === 0) this.stop('off');
    else this.report(this.value.reason);
  }

  stop(reason: PositionReason) {
    const watch = this.watch;
    this.watch = undefined;
    clearTimeout(this.timer);
    this.requested.clear();
    this.previousTimestamp = -Infinity;
    this.gapDeadline = 0;
    const generation = this.value.generation + 1;
    this.report(reason, false, generation);
    if (watch !== undefined) this.options.geolocation?.clearWatch(watch);
  }

  private isLive(generation: number) {
    return this.value.running && this.value.generation === generation;
  }

  verify() {
    if (!this.value.running) return;
    const mono = this.options.clock.monotonic();
    const wall = this.options.clock.wall();
    if (!this.options.allowed()) this.stop('access');
    else if (Math.abs(wall - mono - this.clockOffset) > CLOCK_DRIFT_MS) this.stop('clock');
    else if (mono >= this.gapDeadline) this.stop('gap');
  }

  private scheduleGap() {
    clearTimeout(this.timer);
    this.timer = setTimeout(() => {
      this.verify();
      if (this.value.running) this.scheduleGap();
    }, Math.max(1, this.gapDeadline - this.options.clock.monotonic()));
  }

  private receive(position: GeolocationPosition, generation: number) {
    if (!this.isLive(generation)) return;
    this.verify();
    if (!this.isLive(generation)) return;
    const wall = this.options.clock.wall();
    const mono = this.options.clock.monotonic();
    const timestamp = position.timestamp;
    if (!Number.isFinite(timestamp) || timestamp > wall) { this.stop('clock'); return; }
    if (timestamp <= this.previousTimestamp) return;
    this.previousTimestamp = timestamp;
    const coordinates = position.coords;
    if (!coordinates || !validNumber(coordinates.latitude, -90, 90)
        || !validNumber(coordinates.longitude, -180, 180) || !validNumber(coordinates.accuracy, 0, Infinity)
        || wall - timestamp >= RAW_FIX_GAP_MS) {
      this.report('invalid');
      return;
    }
    const fix: PositionFix = {
      generation, acquiredAt: timestamp, receivedWallMs: wall, receivedMonoMs: mono,
      latitude: coordinates.latitude, longitude: coordinates.longitude, accuracyM: coordinates.accuracy,
      speedMps: validNumber(coordinates.speed, 0, Infinity) ? coordinates.speed : null,
      heading: validNumber(coordinates.heading, 0, 360) && coordinates.heading < 360 ? coordinates.heading : null,
    };
    this.gapDeadline = mono + RAW_FIX_GAP_MS - (wall - timestamp);
    this.scheduleGap();
    if (this.value.reason === 'invalid') this.report('acquiring');
    this.observers.forEach((consumer, observer) => {
      if (this.isLive(generation) && this.requested.has(consumer)) observer.fix(fix);
    });
  }
}
