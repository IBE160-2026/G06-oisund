import type { Content } from './PrivateDrafts';
import { activityFactMissing, currentUncertainty, sourceMarkers } from './draftInterpretation';
import { dayTypeLabels, osloDateTime } from './dayOverview';

// Read only: the caller supplies an acknowledged member, never a proposal.
export function SelectedActivityDetails({ content, classifications, activityId }: { content: Content; classifications: Record<string, string>; activityId: string }) {
  const index = content.activities.findIndex(activity => activity.id === activityId);
  if (index < 0) return null;
  const activity = content.activities[index];
  const kind = classifications[activity.id] ?? activity.type ?? '';
  const known = (value: string | null | undefined) => activityFactMissing(value) ? 'Ukjent' : value;
  const identifiers = [['line', 'Linje'], ['trip', 'Turnummer'], ['direction', 'Retning']].filter(([field]) => kind === 'trip'
    || field === 'trip' && ['deadhead', 'deadhead_car', 'Tomkjøring med CAR', 'CAR'].includes(kind) || !activityFactMissing(activity[field]));
  const uncertainty = currentUncertainty(content, activity);
  return <div className="selected-activity" data-selected-activity-id={activity.id}>
    <h3>{kind === 'trip' ? 'Valgt tur' : 'Valgt aktivitet'}</h3>
    <p><strong>Manuelt valgt · Aktivitet {index + 1} av {content.activities.length}</strong></p>
    <dl className="selected-facts">
      <div><dt>Aktivitetstype: </dt><dd>{dayTypeLabels[kind] ?? known(kind)}</dd></div>
      <div><dt>Planlagt start: </dt><dd>{activity.start ? osloDateTime(activity.start) : 'Ukjent'}</dd></div>
      <div><dt>Planlagt slutt: </dt><dd>{activity.end ? osloDateTime(activity.end) : 'Ukjent'}</dd></div>
      {identifiers.map(([field, label]) => <div key={field}><dt>{label}: </dt><dd>{known(activity[field])}</dd></div>)}
      <div><dt>Fra: </dt><dd>{known(activity.from_place)}</dd></div>
      <div><dt>Til: </dt><dd>{known(activity.to_place)}</dd></div>
    </dl>
    <p>Alle kalenderdatoer og klokkeslett vises i Europe/Oslo.</p>
    {uncertainty && <p className="current-unknown">Gjeldende usikkerhet: {uncertainty}</p>}
    {sourceMarkers(content).filter(marker => marker.activityId === activity.id).map((marker, i) => <p key={i}>{marker.text}</p>)}
    <p>Stoppdata er ikke tilgjengelig i denne visningen.</p>
  </div>;
}
