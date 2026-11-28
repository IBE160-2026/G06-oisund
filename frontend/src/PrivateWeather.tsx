import { useEffect, useRef, useState } from 'react';

type Hour = {time: string; temperature: number; wind: number; symbol: string | null};
type Forecast = {place: string; day: string; current: Hour | null; hours: Hour[]; updated: string | null; stale: boolean};
const time = new Intl.DateTimeFormat('nb-NO', {timeZone:'Europe/Oslo', hour:'2-digit', minute:'2-digit', hourCycle:'h23'});
const date = new Intl.DateTimeFormat('nb-NO', {timeZone:'Europe/Oslo', weekday:'short', day:'numeric', month:'short'});
const dateTime = new Intl.DateTimeFormat('nb-NO', {timeZone:'Europe/Oslo', dateStyle:'short', timeStyle:'short'});
const number = new Intl.NumberFormat('nb-NO', {maximumFractionDigits:1});
const validTime = (value: unknown) => typeof value === 'string' && Number.isFinite(Date.parse(value));
const validHour = (row: any) => row && validTime(row.time) && Number.isFinite(row.temperature) && Number.isFinite(row.wind)
  && row.wind >= 0 && (row.symbol === null || typeof row.symbol === 'string');

function condition(symbol: string | null) {
  if (symbol?.includes('thunder')) return {label:'Torden', icon:'thunder'};
  if (symbol?.includes('snow') || symbol?.includes('sleet')) return {label:symbol.includes('sleet') ? 'Sludd' : 'Snø', icon:'snow'};
  if (symbol?.includes('rain')) return {label:'Regn', icon:'rain'};
  if (symbol === 'fog') return {label:'Tåke', icon:'fog'};
  if (symbol?.startsWith('clearsky')) return {label:'Klart', icon:/night|polartwilight/.test(symbol) ? 'moon' : 'sun'};
  if (symbol?.startsWith('fair') || symbol?.startsWith('partlycloudy')) return {label:'Delvis skyet', icon:'cloud'};
  if (symbol === 'cloudy') return {label:'Overskyet', icon:'cloud'};
  return {label:'Værtilstand ukjent', icon:'unknown'};
}
function WeatherIcon({icon}: {icon:string}) {
  const cloud = <path d="M7 18a4 4 0 0 1 0-8 6 6 0 0 1 11-2 5 5 0 0 1 0 10Z"/>;
  return <svg viewBox="0 0 24 24" fill="none" className={'weather-icon ' + icon} stroke="currentColor" strokeWidth="1.6"
    strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {icon === 'sun' ? <><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></>
      : icon === 'moon' ? <path d="M20 16a8 8 0 0 1-10-11 8.2 8.2 0 1 0 10 11Z"/>
      : icon === 'fog' ? <path d="M4 7h12M2 12h20M6 17h13"/>
      : icon === 'unknown' ? <path d="M8 8a4 4 0 0 1 8 0c0 2-4 3-4 6m0 4h.01"/>
      : <>{cloud}{icon === 'rain' && <path d="m7 21-1 2m7-2-1 2m7-2-1 2"/>}
        {icon === 'snow' && <path d="M7 22h.01M12 22h.01M17 22h.01"/>}
        {icon === 'thunder' && <path d="m12 17-2 3h4l-2 3"/>}</>}
  </svg>;
}
function Wind({value}: {value:number}) {
  return <span className={value >= 13.9 ? 'weather-wind strong-wind' : 'weather-wind'}>
    <svg viewBox="0 0 24 20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" aria-hidden="true">
      <path d="M2 6h12a2 2 0 1 0-2-2M2 10h17a2 2 0 1 1-2 2M2 14h10a2 2 0 1 1-2 2"/>
    </svg>
    <span>{number.format(value)} m/s{value >= 13.9 && <small>Kraftig vind</small>}</span>
  </span>;
}
function WeatherValues({hour}: {hour: Hour}) {
  const current = condition(hour.symbol);
  return <><span className="weather-condition"><WeatherIcon icon={current.icon}/>{current.label}</span>
    <span className="weather-temperature">{number.format(hour.temperature)} °C</span><Wind value={hour.wind}/></>;
}

export function PrivateWeather({request, open}: {request:(path:string)=>Promise<any>; open:boolean}) {
  const [value, setValue] = useState<Forecast>();
  const [failed, setFailed] = useState(false);
  const req = useRef(request);
  req.current = request;
  useEffect(() => {
    if (!open) return;
    let live = true;
    async function load() {
      try {
        const data = await req.current('/tromso-weather');
        if (data?.place !== 'Tromsø' || !/^\d{4}-\d{2}-\d{2}$/.test(data.day)
            || !(data.current === null || validHour(data.current))
            || !Array.isArray(data.hours) || data.hours.length > 25 || !data.hours.every(validHour)
            || !(data.updated === null || validTime(data.updated)) || typeof data.stale !== 'boolean') throw Error();
        if (live) { setValue(data); setFailed(false); }
      } catch {
        if (live) setFailed(true);
      }
    }
    void load();
    const timer = setInterval(load, 10 * 60_000);
    return () => { live = false; clearInterval(timer); };
  }, [open]);
  return <details className="day-weather" aria-label="Vær i Tromsø">
    <summary><span className="weather-location">Tromsø {value?.current && <time dateTime={value.current.time}>· {date.format(new Date(value.current.time))} kl. {time.format(new Date(value.current.time))}</time>}</span>
      {value?.current ? <span className="weather-values"><WeatherValues hour={value.current}/></span>
        : <span>{failed || value ? 'Vær utilgjengelig' : 'Henter vær …'}</span>}
      {value?.updated && (failed || value.stale) && <small>Sist oppdatert {dateTime.format(new Date(value.updated))}</small>}
    </summary>
    <div className="weather-detail">
      <strong>Dagens prognose · Tromsø {value?.day && new Date(value.day + 'T12:00:00Z').toLocaleDateString('nb-NO',{timeZone:'Europe/Oslo'})}</strong>
      {value?.updated && <p>Oppdatert {dateTime.format(new Date(value.updated))}</p>}
      {value && value.hours.length > 0 ? <ul>{value.hours.map(hour => <li key={hour.time}>
        <time dateTime={hour.time}>{time.format(new Date(hour.time))}</time><WeatherValues hour={hour}/>
      </li>)}</ul> : <p>Prognosen er midlertidig utilgjengelig.</p>}
      <a href="https://www.met.no/" target="_blank" rel="noreferrer">Værdata fra Meteorologisk institutt</a>
    </div>
  </details>;
}
