import { useState } from 'react';
import { CityDepartures } from './PrivateRouteReference';
import { PrivateRoadArea } from './PrivateRoadArea';

export function PrivateDayTools({request, expiresAt, available}: {
  request:(path:string)=>Promise<any>; expiresAt:string; available:boolean;
}) {
  const [road, setRoad] = useState(false);
  return <div className="day-road-tools">
    <button type="button" aria-expanded={road} disabled={!available} onClick={() => setRoad(value => !value)}>
      {road ? 'Lukk vegområde og GPS-fart' : 'Åpne vegområde og GPS-fart'}
    </button>
    {road && available && <PrivateRoadArea expiresAt={expiresAt} request={request} verifyAccess={() => request('/auth/session')}/>}
    <CityDepartures request={request} suspended={!available}/>
  </div>;
}
