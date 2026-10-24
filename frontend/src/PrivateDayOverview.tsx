import type { Content } from './PrivateDrafts';
import { activityFactMissing, currentUncertainty, displayFact, sourceMarkers, currentUnknowns, importIssues, originalActivity, sameFact } from './draftInterpretation';
import { dayTypeLabels, osloDateTime, projectDay, type DayMember } from './dayOverview';

const known = (value: string | null | undefined) => activityFactMissing(value) ? 'Ukjent' : value;
const fieldNames: Record<string, string> = { type: 'Aktivitetstype', raw_code: 'Kode', start: 'Start', end: 'Slutt', source_start: 'Kildestart', source_end: 'Kildeslutt', from_place: 'Fra sted', to_place: 'Til sted', trip: 'Turnummer', line: 'Linje' };
const interval = (start: string, end: string) => `${osloDateTime(start)} – ${osloDateTime(end)}`;
function Duty({ member }: { member: DayMember }) {
  return <p>Vognløp: {known(member.duty)} · Sanntidsverdi: {member.suffix ?? (member.duty?.startsWith('CAR') ? 'Ikke utledet for CAR' : 'Ukjent')}</p>;
}
function Member({ member, content, grouped = false }: { member: DayMember; content: Content; grouped?: boolean }) {
  const a = member.activity;
  const original = originalActivity(content, a.id);
  const corrected = original && Object.entries(original).filter(([field, value]) => !sameFact(field, a[field], value)).map(([field]) => field);
  const unknowns = currentUnknowns({ ...a, type: member.kind });
  const identifiers = [['line', 'Linje'], ['trip', 'Tur'], ['direction', 'Retning']].filter(([field]) => member.kind === 'trip' || field === 'trip' && ['deadhead', 'deadhead_car', 'Tomkjøring med CAR', 'CAR'].includes(member.kind) || !activityFactMissing(a[field]));
  return <div className="day-member" data-activity-id={a.id}>
    {grouped && <><p><strong>{dayTypeLabels[member.kind] ?? 'Ukjent aktivitetstype'}</strong></p><p>{interval(a.start!, a.end!)}</p></>}
    {a.raw_code && <p>Kode: {displayFact('raw_code', a.raw_code)}</p>}
    {a.type !== member.kind && <p>Oppgitt type: {known(displayFact('type', a.type))} · Bekreftet klassifisering: {dayTypeLabels[member.kind] ?? member.kind}</p>}
    <p>Fra: {known(a.from_place)} → Til: {known(a.to_place)}</p>
    {identifiers.length > 0 && <p>{identifiers.map(([field, label]) => `${label}: ${known(a[field])}`).join(' · ')}</p>}
    <Duty member={member} />{sourceMarkers(content).filter(marker => marker.activityId === a.id).map((marker, i) => <p key={i}>{marker.text}</p>)}
    {unknowns.length > 0 && <p>Ukjent: {unknowns.join(', ')}.</p>}
    {currentUncertainty(content, a) && <p className="day-uncertainty">Usikkerhet: {currentUncertainty(content, a)}</p>}
    <details><summary>Kilde og rettelser · aktivitet {member.index + 1}</summary>
      <p>Kilde / manuell rettelse: {known(a.provenance)}</p>
      <p>{original ? corrected?.length ? 'Rettet fra opprinnelig tolkning.' : 'Bevarte fakta fra opprinnelig tolkning.' : 'Manuelt opprettet aktivitet.'}</p>
      {original && <dl>{Object.entries(original).map(([field, value]) => <div key={field}><dt>{fieldNames[field] ?? field}{corrected?.includes(field) ? ' · rettet' : ''}</dt><dd>Bekreftet: {known(displayFact(field, a[field]))} · Opprinnelig: {known(displayFact(field, value))}</dd></div>)}</dl>}
      {(a.source_start || a.source_end) && <p>Kildeklokker: {known(a.source_start)} – {known(a.source_end)}</p>}
    </details>
  </div>;
}

export function PrivateDayOverview({ content, classifications, finalEnd, expiresAt }: { content: Content; classifications: Record<string, string>; finalEnd: string; expiresAt: string }) {
  const day = projectDay(content, classifications);
  const first = day.reporting[0];
  const header = content.import_metadata?.header;
  const sourceStart = typeof header?.start_instant === 'string' && Number.isFinite(Date.parse(header.start_instant)) ? osloDateTime(header.start_instant) : header?.start;
  const issues = importIssues(content);
  const unmatched = issues.filter(issue => !content.activities.some(activity => activity.id === issue.activityId));
  const sourceWarning = (text: string, index: number) => <p className="day-source-information" key={index}>Opprinnelig kildeusikkerhet (før rettelser og bekreftelse): {text} Bekreftede fakta i oversikten gjelder.</p>;
  return <section className="day-overview" aria-label="Dagsoversikt">
    <h3>Dagen din · bekreftet plan</h3>
    <p>Tjenestedato: <span>{content.service_date}</span>. Alle kalenderdatoer og klokkeslett vises i Europe/Oslo.</p>
    <div className="day-reporting"><h4>Oppmøte</h4>
      {first ? <p><strong>{osloDateTime(first.activity.start!)}</strong> · Sted: {known(first.activity.from_place)}</p> : <p><strong>Ukjent · ingen bekreftet Sign-on.</strong></p>}
      {!first && header?.start && <p>Kildeinformasjon · start i overskriften: {String(sourceStart)}. Dette er ikke et bekreftet oppmøte.</p>}
      {day.reporting.slice(1).map(member => <p key={member.activity.id}>Senere oppmøte: {osloDateTime(member.activity.start!)} · Sted: {known(member.activity.from_place)}</p>)}
    </div>
    <p><strong>Planlagt siste aktivitetsslutt: {osloDateTime(finalEnd)}.</strong></p>
    <p>Fast utløpsfrist: {osloDateTime(expiresAt)}. Visning og bussendringer forlenger ikke fristen.</p>
    <p>Opplysningene er planlagte. Vognløp og CAR fastslår ikke faktisk buss eller bussbytte.</p>
    {unmatched.map((issue, index) => sourceWarning(issue.text, index))}
    {sourceMarkers(content).filter(marker => !content.activities.some(activity => activity.id === marker.activityId)).map((marker, index) => <p key={'marker-' + index}>{marker.text}</p>)}
    <ol className="day-list" role="list" aria-label="Planlagte aktiviteter og tidsrom">{day.rows.map(row => row.type === 'gap'
      ? <li className="day-gap" key={row.id}><strong>Uklassifisert tidsrom</strong><p>{interval(row.start, row.end)}</p><p>Ingen aktivitet er oppgitt for tidsrommet.</p></li>
      : <li className="day-activity" key={row.id} data-day-row={row.id}>
        <h4>{row.label}</h4><p className="day-time">{interval(row.start, row.end)}</p>
        {row.overlap && <p className="day-uncertainty">Overlapper en tidligere planlagt aktivitet.</p>}
        {issues.filter(issue => row.members.some(member => member.activity.id === issue.activityId)).map((issue, index) => sourceWarning(issue.text, index))}
        {row.members.length > 1 ? <><p>{row.members.length} sammenhengende pauserader. Vognløp: {row.members.filter((member, index) => index === 0 || member.duty !== row.members[index - 1].duty).map(member => `${osloDateTime(member.activity.start!)}: ${member.duty ?? 'Ukjent'} (sanntidsverdi ${member.suffix ?? 'ukjent / ikke utledet'})`).join(' → ')}. Hver del vises i detaljene.</p>
          {row.members.map(member => <div key={member.activity.id}>{currentUnknowns({ ...member.activity, type: member.kind }).length > 0 && <p>Del {member.index + 1} · Ukjent: {currentUnknowns({ ...member.activity, type: member.kind }).join(', ')}.</p>}{currentUncertainty(content, member.activity) && <p className="day-uncertainty">Del {member.index + 1} · Usikkerhet: {currentUncertainty(content, member.activity)}</p>}</div>)}
          <details><summary>Vis {row.members.length} pauserader</summary>{row.members.map(member => <Member key={member.activity.id} member={member} content={content} grouped />)}</details></>
          : <Member member={row.members[0]} content={content} />}
      </li>)}</ol>
  </section>;
}
