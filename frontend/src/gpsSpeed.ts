import { distanceMetres, fixAge, type PositionFix } from './positionSource.ts';

export const SPEED_PROFILE = 'GPS-LAB-1';
export const SPEED_MAX_AGE_MS = 3_000;

type Sample = PositionFix & { speedMps: number };
type UnknownSpeed = { kind: 'unknown'; reason: 'waiting' | 'missing' | 'inaccurate' | 'stale' | 'jump' };
type QualifiedSpeed = {
  kind: 'qualified';
  valueMps: number;
  displayKmh: string;
  acquiredAt: number;
  validUntilMono: number;
  generation: number;
  profile: typeof SPEED_PROFILE;
  origin: 'browser-reported';
};
export type SpeedReading = UnknownSpeed | QualifiedSpeed;

function displaySpeed(value: number) {
  const rounded = Math.round(value * 3.6);
  return value > 0 && rounded === 0 ? '<1' : String(rounded);
}

export class GpsSpeed {
  private anchor: Sample | null = null;
  private value: SpeedReading = { kind: 'unknown', reason: 'waiting' };

  clear(reason: UnknownSpeed['reason'] = 'waiting'): SpeedReading {
    this.anchor = null;
    this.value = { kind: 'unknown', reason };
    return this.value;
  }

  read(mono: number): SpeedReading {
    if (this.anchor && fixAge(this.anchor, mono) >= SPEED_MAX_AGE_MS) return this.clear('stale');
    return this.value;
  }

  receive(fix: PositionFix): SpeedReading {
    const { speedMps } = fix;
    const nowMono = fix.receivedMonoMs;
    this.read(nowMono);
    if (fixAge(fix, nowMono) >= SPEED_MAX_AGE_MS) return this.clear('stale');
    if (fix.accuracyM > 30) return this.clear('inaccurate');
    if (speedMps === null || !Number.isFinite(speedMps) || speedMps < 0 || speedMps > 55.56) return this.clear('missing');
    const previous = this.anchor;
    const current = { ...fix, speedMps };
    const seconds = previous ? (current.acquiredAt - previous.acquiredAt) / 1_000 : Infinity;
    if (!previous || previous.generation !== current.generation || seconds >= 3) {
      this.anchor = current;
      this.value = { kind: 'unknown', reason: 'waiting' };
      return this.value;
    }
    if (seconds < 0.5) return this.value;
    if (Math.abs(current.speedMps - previous.speedMps) / seconds > 12
        || distanceMetres(previous, current) > 60 * seconds + previous.accuracyM + current.accuracyM) {
      return this.clear('jump');
    }
    this.anchor = current;
    this.value = {
      kind: 'qualified', valueMps: speedMps, displayKmh: displaySpeed(speedMps),
      acquiredAt: current.acquiredAt, validUntilMono: nowMono + SPEED_MAX_AGE_MS - fixAge(fix, nowMono),
      generation: current.generation, profile: SPEED_PROFILE, origin: 'browser-reported',
    };
    return this.value;
  }
}
