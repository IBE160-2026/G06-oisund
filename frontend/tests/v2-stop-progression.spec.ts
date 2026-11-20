import { expect, openedPlan, setup, test } from './private-activity-helpers';

setup();

test('stop anchors require current authority, survive authorized navigation, and resume from an explicit occurrence', async ({ page, context }) => {
  await page.clock.install();
  await page.addInitScript(() => {
    const callbacks: PositionCallback[] = [];
    const active = new Set<number>();
    Object.defineProperty(navigator, 'geolocation', { value: {
      watchPosition(callback: PositionCallback) {
        callbacks.push(callback);
        active.add(callbacks.length);
        return callbacks.length;
      },
      clearWatch(id: number) { active.delete(id); },
    } });
    Object.assign(window, { progressionControl: {
      active: () => active.size,
      watches: () => callbacks.length,
      fix(longitude: number, watch = callbacks.length - 1) {
        callbacks[watch]({
          timestamp: Date.now(), coords: { latitude: 69.012345, longitude, accuracy: 8, speed: null, heading: null },
        } as GeolocationPosition);
      },
    } });
  });
  const { plan, activities } = await openedPlan(page, context);
  const activityId = activities[0].id;
  const routeBasis = 'b'.repeat(64);
  const revision = 'synthetic-coordinates-1';
  const pins = { revision, mapping_revision: 'synthetic-m1', stop_place_version: '1', quay_version: '1' };
  const calls = [18, 18.008, 18.016, 18, 18.030, 18.038].map((longitude, index) => ({
    position: index + 2, occurrence_id: 'A-o' + (index + 2), name: index === 3 ? 'Synthetic 2' : 'Synthetic ' + (index + 2),
    stop_place_id: 'FIX:SP:' + longitude, quay_id: 'FIX:Q:' + longitude,
    arrival: { utc: '2031-01-02T19:00:00Z', calendar_time: '2031-01-02T20:00:00+01:00' }, departure: null,
    coordinates: { latitude: 69.012345, longitude, ...pins }, coordinate_issue: null,
  }));
  const scope = { workday_id: plan.id, expires_at: plan.expires_at, terminal: false };
  const board = {
    activity_id: activityId, service_date: '2031-01-02', journey_id: 'synthetic-A', pattern_id: 'synthetic-pattern',
    decision_revision: 1, start_position: 2, end_position: 7, compatible: true, status: 'compatible',
    source_version: 'synthetic-snapshot-1', basis: routeBasis,
  };
  const writes: Record<string, any>[] = [];
  const released: string[] = [];
  const lookups: string[] = [];
  let current: Record<string, unknown> | null = null;
  let lastReceipt: Record<string, unknown> | null = null;
  let firstRead = true;
  let answerFirstRead!: () => void;
  const delayedFirstRead = new Promise<void>(resolve => { answerFirstRead = resolve; });
  const cors = { 'Access-Control-Allow-Origin': new URL(page.url()).origin, 'Access-Control-Allow-Credentials': 'true' };
  page.on('request', request => released.push(request.url() + (request.postData() ?? '')));
  await page.route('**/position-coordinates/**', route => route.fulfill({
    headers: cors, json: { ...scope, activity_id: activityId, route: board, calls, reason: null, source: null },
  }));
  await page.route(/\/position-anchor(?:\/operations\/[^/?]+)?$/, async route => {
    if (route.request().method() === 'POST') {
      const proposed = route.request().postDataJSON();
      writes.push(proposed);
      const call = calls.find(value => value.occurrence_id === proposed.occurrence_id)!;
      const savedAt = new Date().toISOString();
      current = {
        ...scope, activity_id: activityId, service_date: board.service_date,
        journey_id: board.journey_id, pattern_id: board.pattern_id, occurrence_id: proposed.occurrence_id, route_basis: routeBasis,
        quay_id: call.quay_id, stop_place_id: call.stop_place_id, coordinate_revision: revision,
        ...pins, revision: proposed.expected_revision + 1, origin: proposed.origin, evidence_at: proposed.evidence_at,
        asserted_at: proposed.origin === 'manual' ? proposed.evidence_at : null, saved_at: savedAt, carried_from: null,
      };
      lastReceipt = {
        workday_id: plan.id, operation_id: proposed.operation_id, accepted_revision: proposed.expected_revision + 1,
        accepted_at: savedAt,
      };
      if (writes.length === 1) return route.abort('failed');
      return route.fulfill({ headers: cors, json: lastReceipt });
    }
    if (route.request().url().includes('/operations/')) {
      lookups.push(route.request().url().split('/').at(-1)!);
      return route.fulfill({ headers: cors, json: lastReceipt });
    }
    if (firstRead) {
      firstRead = false;
      await delayedFirstRead;
      return route.fulfill({ headers: cors, status: 503, json: { detail: 'Tjenesten er utilgjengelig.' } });
    }
    return route.fulfill({ headers: cors, json: { ...scope, revision: current?.revision ?? 0, anchor: current } });
  });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  const panel = page.getByRole('region', { name: 'Holdeplassassistanse', exact: true });
  const options = panel.getByLabel('Holdeplassforekomst');
  const manual = panel.getByRole('button', { name: 'Sett manuelt holdepunkt' });
  const start = panel.getByRole('button', { name: 'Start holdeplassassistanse' });
  const controls = () => page.evaluate(() => {
    const injected = (window as any).progressionControl;
    return [injected.active(), injected.watches()];
  });
  await expect(panel).toContainText('forekomster 2–7');
  await expect(start).toBeDisabled();
  expect(await controls()).toEqual([0, 0]);
  await options.selectOption('A-o2');
  await expect(panel).toContainText('Henter lagret holdepunkt');
  await expect(manual).toBeDisabled();
  await expect(start).toBeDisabled();
  answerFirstRead();
  await expect(panel).toContainText('Lagret holdepunkt er utilgjengelig.');
  await expect(manual).toBeDisabled();
  await expect(start).toBeDisabled();
  await expect(panel.getByText('Veiledende holdepunkt')).toHaveCount(0);
  expect(writes).toHaveLength(0);
  await panel.getByRole('button', { name: 'Hent rutedata og lagret holdepunkt' }).click();
  await manual.click();
  await expect.poll(controls).toEqual([0, 0]);
  await expect(panel).toContainText('Lagringen er uavklart');
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await expect(panel).toHaveCount(0);
  await page.getByRole('button', { name: 'Åpne valgt aktivitet', exact: true }).click();
  await expect(panel).toContainText('Et forsøk på å lagre holdepunkt er uavklart.');
  await expect(panel.getByText('Veiledende holdepunkt')).toHaveCount(0);
  await panel.getByRole('button', { name: 'Kontroller eller prøv samme holdepunkt igjen' }).click();
  await expect(panel).toContainText('Holdepunktet er lagret.');
  expect(writes).toHaveLength(1);
  expect(lookups).toEqual([writes[0].operation_id]);
  await options.selectOption('A-o2');
  await start.click();
  await expect.poll(controls).toEqual([1, 1]);
  await expect.poll(() => writes.length).toBe(2);
  await expect(panel).toContainText('Holdepunktet er lagret.');
  await page.getByRole('button', { name: 'Start fartsmåling', exact: true }).click();
  await expect.poll(controls).toEqual([1, 1]);
  for (const longitude of [18, 18.0015, 18.0030, 18.0051, 18.0072, 18.008]) {
    await page.clock.fastForward(4_100);
    await page.evaluate(value => (window as any).progressionControl.fix(value), longitude);
  }
  await expect(panel.getByText('Veiledende holdepunkt')).toBeVisible();
  await expect(panel).toContainText('3. Synthetic 3');
  await expect.poll(() => writes.length).toBe(3);
  expect(writes[2]).toMatchObject({ occurrence_id: 'A-o3', origin: 'gps' });
  await expect(panel).toContainText('Holdepunktet er lagret.');
  await page.clock.fastForward(10_020);
  await expect.poll(controls).toEqual([0, 1]);
  await expect(panel.getByText('Tidligere holdepunkt', { exact: true })).toBeVisible();
  await page.evaluate(() => (window as any).progressionControl.fix(18.030, 0));
  await expect(panel.getByRole('button', { name: 'Gjenoppta holdeplassassistanse' })).toBeDisabled();
  await options.selectOption('A-o6');
  await panel.getByRole('button', { name: 'Gjenoppta holdeplassassistanse' }).click();
  await expect.poll(controls).toEqual([1, 2]);
  await expect.poll(() => writes.map(value => value.occurrence_id)).toEqual(['A-o2', 'A-o2', 'A-o3', 'A-o6']);
  await panel.getByRole('button', { name: 'Slå av holdeplassassistanse' }).click();
  await expect.poll(controls).toEqual([0, 2]);
  await expect(panel.getByText('Veiledende holdepunkt')).toHaveCount(0);
  expect(released.some(value => value.includes('69.012345') || value.includes('"latitude"'))).toBe(false);
  expect(await page.evaluate(() => JSON.stringify({ ...sessionStorage, ...localStorage }))).not.toContain('69.012345');
});
