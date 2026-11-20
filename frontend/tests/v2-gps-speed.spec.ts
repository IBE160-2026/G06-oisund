import { type Page } from '@playwright/test';
import { expect, openedPlan, setup, test } from './private-activity-helpers';

setup();

async function syntheticPosition(page: Page) {
  await page.addInitScript(() => {
    const callbacks: Array<{ success: PositionCallback; error: PositionErrorCallback }> = [];
    const active = new Set<number>();
    const state = {
      count: () => active.size,
      watches: () => callbacks.length,
      fix(speed: number | null, index = callbacks.length - 1, east = 0) {
        callbacks[index].success({
          timestamp: Date.now(),
          coords: {
            latitude: 68.123456, longitude: 18.654321 + east / (111_195.08 * Math.cos(68.123456 * Math.PI / 180)),
            accuracy: 8, speed, heading: null,
          },
        } as GeolocationPosition);
      },
      deny() { callbacks.at(-1)?.error({ code: 1 } as GeolocationPositionError); },
    };
    Object.defineProperty(window, 'v2SyntheticPosition', { value: state });
    Object.defineProperty(navigator, 'geolocation', { value: {
      watchPosition(success: PositionCallback, error: PositionErrorCallback) {
        callbacks.push({ success, error });
        active.add(callbacks.length);
        return callbacks.length;
      },
      clearWatch(id: number) { active.delete(id); },
    } });
  });
}

declare global {
  interface Window {
    v2SyntheticPosition: {
      count: () => number;
      watches: () => number;
      fix: (speed: number | null, index?: number, east?: number) => void;
      deny: () => void;
    };
  }
}

test('private activity uses explicit GPS opt-in, freshness and one watch across changed context', async ({ page, context }) => {
  await page.clock.install();
  await syntheticPosition(page);
  const { plan, activities } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  const start = page.getByRole('button', { name: 'Start fartsmåling', exact: true });
  const speed = page.getByLabel('Målt egen fart');
  await expect(start).toBeEnabled();
  expect(await page.evaluate(() => window.v2SyntheticPosition.watches())).toBe(0);
  const outgoing: string[] = [];
  page.on('request', request => { outgoing.push(request.url() + (request.postData() ?? '')); });
  await start.click();
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(1);
  await page.evaluate(() => window.v2SyntheticPosition.fix(10));
  await expect(speed).toHaveText('— km/t');
  await page.clock.fastForward(1_000);
  await page.evaluate(() => window.v2SyntheticPosition.fix(10));
  await expect(speed).toHaveText('36 km/t');
  await page.clock.fastForward(3_001);
  await expect(speed).toHaveText('— km/t');
  await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click();
  await expect(page.locator('[data-selected-activity-id]')).toHaveAttribute('data-selected-activity-id', activities[1].id);
  await expect(start).toBeEnabled();
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(0);
  await page.evaluate(() => window.v2SyntheticPosition.fix(10, 0));
  await expect(speed).toHaveText('— km/t');
  expect(await page.evaluate(() => window.v2SyntheticPosition.watches())).toBe(1);
  expect(outgoing.some(value => value.includes('68.123456') || value.includes('18.654321'))).toBe(false);
  expect(await page.evaluate(() => JSON.stringify({ ...sessionStorage, ...localStorage }))).not.toContain('68.123456');
  expect(plan.draft.activities[0].id).toBe(activities[0].id);
});

test('denied and hidden location requires explicit resume and clears current data', async ({ page, context }) => {
  await syntheticPosition(page);
  await openedPlan(page, context);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await page.getByRole('button', { name: 'Start fartsmåling', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(1);
  await page.evaluate(() => window.v2SyntheticPosition.deny());
  const panel = page.getByRole('region', { name: 'Egen fart (GPS)' });
  await expect(panel.getByRole('status')).toContainText('Posisjonstilgangen er avvist');
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(0);
  await panel.getByRole('button', { name: 'Gjenoppta fartsmåling' }).click();
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(1);
  await page.evaluate(() => window.dispatchEvent(new Event('pagehide')));
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(0);
  await page.evaluate(() => window.dispatchEvent(new Event('pageshow')));
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.watches())).toBe(2);
});

test('account settings stop the watch and a changed server selection blocks location access', async ({ page, context }) => {
  await page.clock.install();
  await syntheticPosition(page);
  const { activities } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  const speed = page.getByRole('region', { name: 'Egen fart (GPS)' });
  await speed.getByRole('button', { name: 'Start fartsmåling' }).click();
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(1);
  await page.getByRole('button', { name: 'Brukerinnstillinger', exact: true }).click();
  await expect(speed).toBeHidden();
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(0);
  await page.getByRole('button', { name: 'Avbryt', exact: true }).click();
  await expect(speed).toBeVisible();
  expect(await page.evaluate(() => window.v2SyntheticPosition.watches())).toBe(1);

  let changed = false, changedReads = 0;
  await page.route('**/workdays/*/selection', async route => {
    const response = await route.fetch();
    if (!changed || route.request().method() !== 'GET') { await route.fulfill({ response }); return; }
    changedReads++;
    await route.fulfill({ response, json: { ...await response.json(), activity_id: activities[1].id, revision: 2 } });
  });
  await speed.getByRole('button', { name: /fartsmåling/ }).click();
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(1);
  changed = true;
  for (let step = 0; step < 3; step++) {
    await page.clock.fastForward(8_000);
    await page.evaluate(() => window.v2SyntheticPosition.fix(10));
    expect(await page.evaluate(() => window.v2SyntheticPosition.count())).toBe(1);
  }
  await page.clock.fastForward(8_000);
  await expect.poll(() => page.evaluate(() => window.v2SyntheticPosition.count())).toBe(0);
  expect(changedReads).toBeGreaterThanOrEqual(1);
  await speed.getByRole('button', { name: /fartsmåling/ }).click();
  await expect(speed.getByRole('status')).toContainText('Tilgangen');
  expect(await page.evaluate(() => window.v2SyntheticPosition.watches())).toBe(2);
});
