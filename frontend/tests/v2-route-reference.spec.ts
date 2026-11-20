import { expect, test } from '@playwright/test';

const date = '2026-11-23';
const draftId = '00000000-0000-4000-8000-000000000020';
const activityId = '00000000-0000-4000-8000-000000000021';
const sessionId = '00000000-0000-4000-8000-000000000022';
const operationId = '00000000-0000-4000-8000-000000000023';
const journeyId = 'TRO:ServiceJourney:synthetic-v2';
const patternId = 'TRO:JourneyPattern:synthetic-v2';
const lineId = 'TRO:Line:1_20';
const original = { sha256: 'a'.repeat(64), provider: 'Syntetisk test', observed_at: '2026-11-20T02:00:00Z', generation: 'test' };
const start = { raw_time: '10:00:00', raw_day_offset: null, day_offset: 0, calendar_time: date + 'T10:00:00+01:00', utc: date + 'T09:00:00Z' };
const end = { raw_time: '11:00:00', raw_day_offset: null, day_offset: 0, calendar_time: date + 'T11:00:00+01:00', utc: date + 'T10:00:00Z' };
const calls = [
  { position: 1, name: 'Første stopp', headsign: 'Kildeskilt', occurrence_id: 'synthetic-1', scheduled_stop_point_id: 'A', quay_id: 'NSR:Quay:1', stop_place_id: null, arrival: null, departure: start },
  { position: 2, name: 'Siste stopp', headsign: 'Kildeskilt', occurrence_id: 'synthetic-2', scheduled_stop_point_id: 'B', quay_id: 'NSR:Quay:1', stop_place_id: null, arrival: end, departure: null },
];
const journey = { journey_id: journeyId, pattern_id: patternId, line_id: lineId, direction: 'outbound', headsign: 'Kildeskilt', service_date: date, calls };
const summary = { journey_id: journeyId, pattern_id: patternId, direction: 'outbound', headsign: 'Kildeskilt', start, end,
  from_name: 'Første stopp', to_name: 'Siste stopp', matching_ranges: [[1, 2]], ranges_truncated: false };
const draft = { id: draftId, revision: 1, created_at: '2026-11-20T02:00:00Z', expires_at: '2026-11-27T02:00:00Z',
  draft: { service_date: date, vehicle_duty: null, realtime_duty: null, physical_bus: '1234', activities: [{
    id: activityId, type: 'trip', raw_code: 'Trip', source_start: '10:00', source_end: '11:00',
    start: date + 'T10:00:00+01:00', end: date + 'T11:00:00+01:00', from_place: 'Første stopp', to_place: 'Siste stopp',
    trip: '0007', line: '20', direction: 'Manuell retning', uncertainty: null, provenance: null,
  }] } };

for (const rechecked of [false, true]) {
test(`saved draft requires explicit choice and recovers a lost reply (${rechecked ? 'rechecked' : 'original'} source)`, async ({ page }) => {
  const source = rechecked ? { ...original, checked_at: '2026-11-20T02:05:00Z' } : original;
  await page.clock.setFixedTime(new Date('2026-11-20T03:00:00Z'));
  let writes = 0;
  let receipt: any = null;
  let reviewCommand: any = null;
  const supported = ['trip', 'deadhead', 'deadhead_car', 'Tomkjøring med CAR', 'CAR', 'Sign-on', 'Sign-off', 'MealBreak', 'Coffee',
    'Split break', 'Paid meal before', 'Paid meal after', 'Travel to', 'Travel from', 'Fadder', 'Instruktør', 'manual'];

  await page.route(url => /^(\/auth\/|\/drafts|\/workdays|\/workday-reviews)/.test(url.pathname), async route => {
    const url = new URL(route.request().url());
    const method = route.request().method();
    const responseHeaders = { 'Access-Control-Allow-Origin': new URL(page.url()).origin,
      'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': 'content-type,x-csrf-token',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS' };
    const reply = (json: unknown, status = 200) => route.fulfill({ status, headers: responseHeaders, json });
    if (method === 'OPTIONS') return route.fulfill({ status: 204, headers: responseHeaders });
    if (url.pathname === '/auth/session') return reply({ account_id: sessionId, created_at: draft.created_at, expires_at: '2026-12-04T02:00:00Z' });
    if (url.pathname === '/auth/csrf') return reply({ csrf_token: 'synthetic' });
    if (url.pathname === '/drafts') return reply({ drafts: [{ id: draftId, revision: 1, service_date: date,
      created_at: draft.created_at, expires_at: draft.expires_at }], next_cursor: null });
    if (url.pathname === '/drafts/' + draftId) return reply(draft);
    if (url.pathname === '/workdays') return reply({ workdays: [], next_cursor: null });
    if (url.pathname.endsWith('/route-departures')) {
      const state = { draft_id: draftId, draft_revision: 1, activity_id: activityId, coverage: 'complete', source_state: 'available',
        service_date: date, expected_count: 1, reasons: [], provenance: source, outcome: 'possible' };
      return reply(url.searchParams.has('journey_id') ? { ...state, journey } : { ...state, journeys: [summary] });
    }
    if (url.pathname.endsWith('/route-references') && method === 'GET')
      return reply({ draft_id: draftId, draft_revision: 1, route_revision: receipt ? 1 : 0, references: receipt ? [receipt.reference] : [], outdated: [] });
    if (url.pathname.endsWith('/route-references') && method === 'POST') {
      writes++;
      const command = route.request().postDataJSON();
      const choices = Object.fromEntries(Object.entries(command.selection.field_decisions).map(([key, value]) =>
        [key, { manual: null, ...(value as object) }]));
      receipt = { operation_id: command.operation_id, draft_id: draftId, draft_revision: 1, activity_id: activityId,
        route_revision: 1, current_route_revision: 1, reference: { ...journey, activity_id: activityId, decision_revision: 1,
          start_position: command.selection.start_position, end_position: command.selection.end_position,
          status: 'compatible', field_decisions: choices, provenance: source, selected_at: '2026-11-20T03:00:00Z' } };
      return route.abort();
    }
    if (url.pathname.includes('/route-reference-operations/')) return reply({ state: 'accepted', result: receipt });
    if (url.pathname === '/workday-reviews') {
      reviewCommand = route.request().postDataJSON();
      return reply({ draft_id: draftId, revision: 1, draft: draft.draft, operation_id: operationId,
        operation_expires_at: draft.expires_at, blockers: [], unknowns: [], classifications_required: [], supported_types: supported,
        final_end: end.calendar_time, expires_at: '2026-11-30T10:00:00Z' });
    }
    return reply({ detail: 'Synthetic route unavailable' }, 404);
  });

  await page.goto('/private');
  await page.getByRole('button', { name: 'Åpne 2026-11-23 · versjon 1' }).click();
  await page.getByText('Planlagte avganger for linje 20', { exact: true }).click();
  await page.getByLabel('Lagret passasjertur').selectOption(activityId);
  await page.getByRole('button', { name: 'Søk på driftsdatoen' }).click();
  await expect(page.getByText('Én mulig avgang og stoppstrekning', { exact: false })).toBeVisible();
  await page.getByText('Kildegrunnlag', { exact: true }).first().click();
  const sourceClock = page.getByText('Kildearkiv kontrollert', { exact: false });
  if (rechecked) await expect(sourceClock).toHaveText(/kontrollert .*03:05.*Ferskhet beregnes fra .*03:00/);
  else await expect(sourceClock).toHaveText(/kontrollert .*03:00.*Publikasjonstid/);
  await page.getByLabel('Planlagt avgang').selectOption(journeyId);
  await expect(page.getByRole('heading', { name: 'Planlagt avgang til Kildeskilt' })).toBeFocused();
  await expect(page.getByRole('button', { name: 'Lagre valgt avgang og strekning' })).toBeDisabled();
  expect(writes).toBe(0);
  await page.getByRole('button', { name: 'Velg mulig strekning 1–2' }).click();
  await page.getByRole('button', { name: 'Lagre valgt avgang og strekning' }).click();
  await expect(page.getByText('Lagringen er uavklart.', { exact: false })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Til godkjenning', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Fortsett til godkjenning', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: 'Kontroller lagringsforsøket' }).click();
  await expect(page.getByRole('heading', { name: 'Lagret rutevalg · versjon 1' })).toBeVisible();
  expect(writes).toBe(1);

  await page.getByRole('button', { name: 'Til godkjenning', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Lagrede rutevalg som følger planen' })).toBeVisible();
  expect(reviewCommand.expected_route_revision).toBe(1);
  await expect(page.getByRole('button', { name: 'Bekreft gjennomgått plan' })).toBeDisabled();
  await page.getByRole('checkbox', { name: 'Jeg har gjennomgått rutevalgene og vil bevare dem i planen.' }).check();
  await expect(page.getByRole('button', { name: 'Bekreft gjennomgått plan' })).toBeEnabled();
});
}
