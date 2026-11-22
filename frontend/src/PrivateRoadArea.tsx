import { useCallback, useLayoutEffect, useRef, useState } from 'react';
import { ActiveRoadLimits, type RoadResponse, type RoadRevision } from './PrivateRoadLimits';
import { PositionAssistance } from './PositionAssistance';

const areas = [
  ['tromsoya', 'Tromsøya'],
  ['kvaloya', 'Kvaløya (Eidkjosen–Slettaelva)'],
  ['fastlandet', 'Fastlandet (Skjelnan/Malmvegen–Solligården)'],
] as const;

type Props = {
  expiresAt: string;
  verifyAccess: () => Promise<unknown>;
  request: (path: string) => Promise<unknown>;
};

export function PrivateRoadArea({ expiresAt, verifyAccess, request }: Props) {
  const [area, setArea] = useState('');
  const areaRequest = useRef(request);
  useLayoutEffect(() => { areaRequest.current = request; }, [request]);
  const checkRevision = useCallback(async () => {
    return await areaRequest.current('/road-areas/' + area + '/revision') as RoadRevision | null;
  }, [area]);

  const loadRoad = useCallback(async (): Promise<RoadResponse> => {
    try {
      const result = await areaRequest.current('/road-areas/' + area) as RoadResponse;
      if (result?.status === 'road-unqualified') return result;
      if (result?.status === 'qualified' && result.manifest?.id === area
          && result.manifest.profile === 'NVDB-AREA-1'
          && typeof result.confirmed === 'number' && Number.isInteger(result.confirmed) && result.confirmed >= 0) return result;
    } catch {
      return { status: 'unavailable' };
    }
    return { status: 'unavailable' };
  }, [area]);

  return <section aria-label="Vegområde og GPS-fart">
    <PositionAssistance authorized expiresAt={expiresAt} verifyAccess={verifyAccess}>
      <label>
        Vegområde
        <select value={area} onChange={event => setArea(event.target.value)}>
          <option value="">Velg område</option>
          {areas.map(([id, label]) => <option key={id} value={id}>{label}</option>)}
        </select>
      </label>
      {area && <ActiveRoadLimits key={area} loadRoad={loadRoad} checkRevision={checkRevision} />}
    </PositionAssistance>
  </section>;
}
