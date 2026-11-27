import { useCallback, useLayoutEffect, useRef } from 'react';
import { ActiveRoadLimits, type RoadResponse, type RoadRevision } from './PrivateRoadLimits';
import { PositionAssistance } from './PositionAssistance';

type Props = {
  expiresAt: string;
  verifyAccess: () => Promise<unknown>;
  request: (path: string) => Promise<unknown>;
};

export function usePilotRoad(request: Props['request']) {
  const areaRequest = useRef(request);
  useLayoutEffect(() => { areaRequest.current = request; }, [request]);
  const checkRevision = useCallback(async () => {
    return await areaRequest.current('/road-areas/pilot/revision') as RoadRevision | null;
  }, []);

  const loadRoad = useCallback(async (): Promise<RoadResponse> => {
    try {
      const result = await areaRequest.current('/road-areas/pilot') as RoadResponse;
      if (result?.status === 'road-unqualified') return result;
      if (result?.status === 'qualified' && result.manifest?.id === 'pilot'
          && result.manifest.profile === 'NVDB-AREA-1'
          && typeof result.confirmed === 'number' && Number.isInteger(result.confirmed) && result.confirmed >= 0) return result;
    } catch {
      return { status: 'unavailable' };
    }
    return { status: 'unavailable' };
  }, []);

  return {loadRoad, checkRevision};
}

export function PrivateRoadArea({expiresAt, verifyAccess, request}: Props) {
  const {loadRoad, checkRevision} = usePilotRoad(request);
  return <section aria-label="Vegområde og GPS-fart">
    <PositionAssistance authorized expiresAt={expiresAt} verifyAccess={verifyAccess}>
      <p>Vegmatching følger posisjonen på Tromsøya, Kvaløya og fastlandet.</p>
      <ActiveRoadLimits loadRoad={loadRoad} checkRevision={checkRevision} />
    </PositionAssistance>
  </section>;
}
