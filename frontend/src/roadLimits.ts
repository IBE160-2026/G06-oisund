import { distanceMetres, fixAge, type PositionFix } from './positionSource.ts';

export const WARNING_METRES = 300;
const WARNING_RESET_METRES = 320;
const FIX_AGE_MS = 5_000;
const EARTH_METRES_PER_DEGREE = 111_195.08;

type Point = readonly [longitude: number, latitude: number];
type Edge = {
  id: string;
  from: string;
  to: string;
  length: number;
  shape: Point[];
  kmh: number | null;
  successors: string[];
  confirmedTransitions?: string[];
};
export type RoadManifest = {
  id: string;
  revision: string;
  checkedAt: string;
  retrievedAt: string;
  validFrom?: string;
  validUntil: string;
  situationLeaseUntil?: string;
  profile: 'SL-LAB-1' | 'NVDB-AREA-1';
  uncertaintyM: number;
  path: string[];
  packages: { id: string; revision: string; edges: Edge[] }[];
};
type Match = { edge: Edge; offset: number; lateral: number; tangent: number };
type RoadReason = 'waiting' | 'stale' | 'uncertain' | 'source' | 'coverage' | 'unverified';
type AheadReason = RoadReason | 'clear' | 'branch';
export type RoadReading = {
  current: { kmh: number } | { reason: RoadReason };
  next: { kmh: number; metres: number; id: string } | { reason: AheadReason };
};
const unknown = (reason: RoadReason): RoadReading => ({ current: { reason }, next: { reason } });
const finite = (value: unknown, minimum: number, maximum: number): value is number =>
  typeof value === 'number' && Number.isFinite(value) && value >= minimum && value <= maximum;
const key = (value: unknown): value is string => typeof value === 'string' && value.length > 0 && value.length <= 160;
const timestamp = (value: unknown) => typeof value === 'string' ? Date.parse(value) : NaN;

function validEdge(edge: Edge, area: boolean) {
  return !!edge && key(edge.id) && key(edge.from) && key(edge.to)
    && finite(edge.length, area ? Number.MIN_VALUE : 0.1, 100_000)
    && (edge.kmh === null || finite(edge.kmh, 1, 130) && Number.isInteger(edge.kmh))
    && Array.isArray(edge.shape) && edge.shape.length >= 2 && edge.shape.length <= (area ? 1024 : 256)
    && edge.shape.every(value => Array.isArray(value) && value.length === 2
      && finite(value[0], -180, 180) && finite(value[1], -90, 90))
    && edge.shape.some(value => value[0] !== edge.shape[0][0] || value[1] !== edge.shape[0][1])
    && Array.isArray(edge.successors) && edge.successors.length <= (area ? 32 : 8)
    && edge.successors.every(key) && new Set(edge.successors).size === edge.successors.length
    && (!area || edge.confirmedTransitions === undefined || Array.isArray(edge.confirmedTransitions)
      && edge.confirmedTransitions.length <= edge.successors.length
      && edge.confirmedTransitions.every(id => edge.successors.includes(id)));
}

export function bindings(manifest: RoadManifest): Map<string, Edge> | null {
  const area = manifest?.profile === 'NVDB-AREA-1';
  const maxEdges = area ? 20_000 : 500;
  if (!manifest || !key(manifest.id) || !key(manifest.revision) || !area && manifest.profile !== 'SL-LAB-1'
      || !finite(manifest.uncertaintyM, 1, 35) || !Array.isArray(manifest.packages) || !manifest.packages.length
      || manifest.packages.length > (area ? 1 : 10) || !Array.isArray(manifest.path) || manifest.path.length > (area ? 0 : 500)
      || ![manifest.checkedAt, manifest.retrievedAt, manifest.validUntil].every(value => Number.isFinite(timestamp(value)))) return null;
  if (area && !(timestamp(manifest.validFrom) < timestamp(manifest.validUntil))) return null;
  if (area && manifest.situationLeaseUntil !== undefined && !Number.isFinite(timestamp(manifest.situationLeaseUntil))) return null;
  const result = new Map<string, Edge>();
  const packageIds = new Set<string>();
  let vertices = 0;
  for (const pack of manifest.packages) {
    if (!pack || !key(pack.id) || !key(pack.revision) || !Array.isArray(pack.edges)
        || packageIds.has(pack.id) || pack.edges.length > maxEdges) return null;
    packageIds.add(pack.id);
    for (const edge of pack.edges) {
      if (!validEdge(edge, area)) return null;
      const existing = result.get(edge.id);
      if (existing && (area || JSON.stringify(existing) !== JSON.stringify(edge))) return null;
      result.set(edge.id, edge);
      vertices += edge.shape.length;
      if (result.size > maxEdges || area && vertices > 350_000) return null;
    }
  }
  if (area && !result.size) return null;
  for (const edge of result.values()) {
    if (edge.successors.some(id => result.has(id) && result.get(id)?.from !== edge.to)) return null;
  }
  if (new Set(manifest.path).size !== manifest.path.length
      || manifest.path.some((id, i) => !result.has(id) || i > 0 && !result.get(manifest.path[i - 1])?.successors.includes(id))) return null;
  return result;
}

function projected(edge: Edge, fix: PositionFix, longitudeScale: number): Match | null {
  let offset = 0;
  let nearest: Match | null = null;
  for (let i = 1; i < edge.shape.length; i++) {
    const [ax, ay] = edge.shape[i - 1], [bx, by] = edge.shape[i];
    const x = (ax - fix.longitude) * longitudeScale, y = (ay - fix.latitude) * EARTH_METRES_PER_DEGREE;
    const dx = (bx - ax) * longitudeScale, dy = (by - ay) * EARTH_METRES_PER_DEGREE;
    const length = Math.hypot(dx, dy);
    if (length === 0) continue;
    const fraction = Math.max(0, Math.min(1, -(x * dx + y * dy) / length ** 2));
    const lateral = Math.hypot(x + fraction * dx, y + fraction * dy);
    if (!nearest || lateral < nearest.lateral) nearest = {
      edge, lateral, offset: offset + length * fraction, tangent: Math.atan2(dx, dy),
    };
    offset += length;
  }
  return nearest && { ...nearest, offset: nearest.offset * edge.length / offset };
}

function bearing(from: PositionFix, to: PositionFix) {
  return Math.atan2((to.longitude - from.longitude) * Math.cos(to.latitude * Math.PI / 180), to.latitude - from.latitude);
}

function compatibleDirection(actual: number, expected: number) {
  return Math.cos(actual - expected) >= Math.cos(20 * Math.PI / 180);
}

type Anchor = { fix: PositionFix; match: Match };
type Extent = { edge: Edge; west: number; east: number; south: number; north: number };

function extent(edge: Edge): Extent {
  let west = Infinity, east = -Infinity, south = Infinity, north = -Infinity;
  for (const [lon, lat] of edge.shape) {
    west = Math.min(west, lon);
    east = Math.max(east, lon);
    south = Math.min(south, lat);
    north = Math.max(north, lat);
  }
  return { edge, west, east, south, north };
}

export class RoadLimits {
  private readonly edges: Map<string, Edge> | null;
  private readonly extents: Extent[];
  private readonly geometryOnly: boolean;
  private situationLease: number;
  private previous: PositionFix | null = null;
  private recent: PositionFix[] = [];
  private window: Anchor[] = [];
  private reading: RoadReading = unknown('waiting');
  private establishedLimit: number | null = null;
  private warningId: string | null = null;
  private wentOffPath = false;
  private directed = false;

  constructor(private readonly manifest: RoadManifest) {
    this.edges = bindings(manifest);
    this.extents = this.edges ? Array.from(this.edges.values(), extent) : [];
    this.geometryOnly = manifest?.profile === 'NVDB-AREA-1' && this.extents.every(({ edge }) => edge.kmh === null);
    this.situationLease = manifest?.profile === 'NVDB-AREA-1' && manifest.situationLeaseUntil !== undefined
      ? timestamp(manifest.situationLeaseUntil) : Infinity;
  }

  reset(reason: RoadReason = 'waiting') {
    this.previous = null;
    this.recent = [];
    this.window = [];
    this.establishedLimit = null;
    this.warningId = null;
    this.wentOffPath = false;
    this.directed = false;
    return (this.reading = unknown(reason));
  }

  isFresh(wall: number) {
    const checked = timestamp(this.manifest.checkedAt), retrieved = timestamp(this.manifest.retrievedAt);
    if (!this.edges || wall >= Math.min(timestamp(this.manifest.validUntil), this.situationLease)
        || wall < checked || wall < retrieved) return false;
    if (this.manifest.profile === 'NVDB-AREA-1' && wall < timestamp(this.manifest.validFrom)) return false;
    return this.geometryOnly || wall - checked <= 86_400_000 && wall - retrieved <= 604_800_000;
  }

  expiresAt(): number {
    if (this.geometryOnly) return timestamp(this.manifest.validUntil);
    return Math.min(timestamp(this.manifest.validUntil), this.situationLease, timestamp(this.manifest.checkedAt) + 86_400_001,
      timestamp(this.manifest.retrievedAt) + 604_800_001);
  }

  matchesRevision(revision: unknown): boolean {
    return revision === this.manifest.revision;
  }

  renewSituationLease(value: unknown, wall: number) {
    const observed = timestamp(value);
    if (observed > this.situationLease && wall < observed && observed - wall <= 305_000) this.situationLease = observed;
  }

  read(mono: number, wall: number): RoadReading {
    if (!this.isFresh(wall)) return this.reset('source');
    if (this.previous && fixAge(this.previous, mono) > FIX_AGE_MS) return this.reset('stale');
    return this.reading;
  }

  private coherent(prior: Anchor, candidate: Match, budget: number, radius: number) {
    if (prior.match.edge.id === candidate.edge.id) {
      const delta = candidate.offset - prior.match.offset;
      return delta >= -radius && delta <= budget;
    }
    const initial = prior.match.edge;
    const pending = initial.successors.map(id => ({ id, travelled: initial.length - prior.match.offset, depth: 1 }));
    const shortest = new Map<string, number>();
    while (pending.length) {
      const next = pending.shift()!;
      if (next.travelled > budget || next.depth > 8 || (shortest.get(next.id) ?? Infinity) <= next.travelled) continue;
      shortest.set(next.id, next.travelled);
      if (next.id === candidate.edge.id && next.travelled + candidate.offset <= budget) return true;
      const edge = this.edges?.get(next.id);
      edge?.successors.forEach(id => pending.push({ id, travelled: next.travelled + edge.length, depth: next.depth + 1 }));
    }
    return false;
  }

  receive(fix: PositionFix, wall = fix.receivedWallMs): RoadReading {
    const mono = fix.receivedMonoMs;
    if (!this.isFresh(wall)) return this.reset('source');
    if (fixAge(fix, mono) < 0 || fixAge(fix, mono) > FIX_AGE_MS) return this.reset('stale');
    if (!finite(fix.accuracyM, 0, 25)) return this.reset('uncertain');
    if (this.previous?.generation !== fix.generation || this.previous && fix.acquiredAt - this.previous.acquiredAt > FIX_AGE_MS) this.reset();
    const previous = this.previous;
    if (previous && fix.acquiredAt <= previous.acquiredAt) return this.reading;
    this.previous = fix;
    const travel = previous ? distanceMetres(previous, fix) : 0;
    const elapsed = previous ? (fix.acquiredAt - previous.acquiredAt) / 1_000 : 0;
    // A reported accuracy can widen the calibrated interval. It cannot establish a smaller one.
    const radius = Math.max(this.manifest.uncertaintyM, fix.accuracyM);
    if (previous && travel > 60 * elapsed + 2 * radius) return this.reset('uncertain');
    let directionFrom = previous && travel >= radius ? previous : null;
    if (this.manifest.profile === 'NVDB-AREA-1') {
      this.recent = this.recent.filter(sample => fix.acquiredAt - sample.acquiredAt <= 3_000);
      directionFrom ??= this.recent.find(sample =>
        distanceMetres(sample, fix) >= Math.max(radius, sample.accuracyM)) ?? null;
      this.recent = [fix, ...this.recent].slice(0, 12);
    }
    const direction = directionFrom ? bearing(directionFrom, fix) : null;
    const prior = this.window.at(-1);
    const candidates: Match[] = [];
    const longitudeScale = EARTH_METRES_PER_DEGREE * Math.cos(fix.latitude * Math.PI / 180);
    const lonRange = radius / longitudeScale;
    const latRange = radius / EARTH_METRES_PER_DEGREE;
    for (const { edge, west, east, south, north } of this.extents) {
      if (west > fix.longitude + lonRange || east < fix.longitude - lonRange
          || south > fix.latitude + latRange || north < fix.latitude - latRange) continue;
      const candidate = projected(edge, fix, longitudeScale);
      if (!candidate || candidate.lateral > radius) continue;
      if (direction !== null && !compatibleDirection(direction, candidate.tangent)) continue;
      if (prior && !this.coherent(prior, candidate, travel + 2 * radius, radius)) continue;
      candidates.push(candidate);
    }
    if (candidates.length !== 1 || direction === null && !prior && previous !== null) {
      this.window = [];
      this.warningId = null;
      this.directed = false;
      return (this.reading = unknown('uncertain'));
    }
    const match = candidates[0];
    if (direction !== null) this.directed = true;
    if (!this.manifest.path.includes(match.edge.id)) this.wentOffPath = true;
    this.window.push({ fix, match });
    this.window = this.window.filter(point => fixAge(point.fix, mono) <= FIX_AGE_MS).slice(-12);
    if (!this.directed || this.window.length < 3 || fix.acquiredAt - this.window[0].fix.acquiredAt < 2_000) {
      return (this.reading = unknown('waiting'));
    }
    if (match.edge.kmh === null || match.offset - radius < 0 || match.offset + radius > match.edge.length) {
      this.warningId = null;
      return (this.reading = unknown(this.manifest.profile === 'NVDB-AREA-1'
        ? match.edge.kmh === null ? 'unverified' : 'uncertain' : 'coverage'));
    }
    if (this.establishedLimit !== null && match.edge.kmh !== this.establishedLimit
        && this.window.slice(-3).some(point => {
          const sampleRadius = Math.max(this.manifest.uncertaintyM, point.fix.accuracyM);
          return point.match.edge.kmh !== match.edge.kmh || point.match.offset - sampleRadius < 5
            || point.match.offset + sampleRadius > point.match.edge.length;
        })) {
      this.warningId = null;
      return (this.reading = unknown('uncertain'));
    }
    this.establishedLimit = match.edge.kmh;
    const next = this.predict(match, radius);
    this.warningId = 'id' in next ? next.id : null;
    return (this.reading = { current: { kmh: match.edge.kmh }, next });
  }

  private predict(match: Match, radius: number): RoadReading['next'] {
    let edge = match.edge;
    let distance = edge.length - match.offset;
    const visited = new Set<string>([edge.id]);
    while (distance - radius <= WARNING_RESET_METRES) {
      const pathIndex = this.wentOffPath ? -1 : this.manifest.path.indexOf(edge.id);
      const expected = pathIndex < 0 ? undefined : this.manifest.path[pathIndex + 1];
      const chosen = expected ?? (edge.successors.length === 1 ? edge.successors[0] : undefined);
      if (!chosen) return { reason: edge.successors.length > 1 ? 'branch' : 'coverage' };
      const successor = this.edges?.get(chosen);
      if (!successor || visited.has(chosen) || successor.kmh === null) return { reason: 'coverage' };
      if (successor.kmh !== match.edge.kmh) {
        if (this.manifest.profile === 'NVDB-AREA-1' && !edge.confirmedTransitions?.includes(chosen)) {
          return { reason: 'unverified' };
        }
        const id = edge.to + ':' + edge.id + ':' + successor.id;
        const boundary = this.warningId === id ? WARNING_RESET_METRES : WARNING_METRES;
        if (distance - radius > 0 && distance + radius <= boundary) {
          // Stabilize decimal ties from the geometry projection before rounding to tens.
          const metres = Math.round(distance * 1000) / 1000;
          return { id, kmh: successor.kmh, metres: Math.max(10, Math.round(metres / 10) * 10) };
        }
        return { reason: distance - radius > WARNING_METRES ? 'clear' : 'uncertain' };
      }
      visited.add(chosen);
      edge = successor;
      distance += edge.length;
    }
    return { reason: 'clear' };
  }
}
