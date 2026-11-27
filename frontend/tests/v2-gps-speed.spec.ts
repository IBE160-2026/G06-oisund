import { type Page } from '@playwright/test';
import type { RoadManifest } from '../src/roadLimits';
import { account, expect, openedPlan, setup, test } from './private-activity-helpers';

setup();

async function syntheticPosition(page: Page) {
  await page.addInitScript(() => {
    const callbacks: Array<{ success: PositionCallback; error: PositionErrorCallback }> = [];
    const active = new Set<number>();
    const state = {
      count: () => active.size,
      watches: () => callbacks.length,
      fix(speed: number | null, index = callbacks.length - 1, east = 0, accuracy = 8, acquiredAt = Date.now()) {
        callbacks[index].success({
          timestamp: acquiredAt,
          coords: {
            latitude: 68.123456, longitude: 18.654321 + east / (111_195.08 * Math.cos(68.123456 * Math.PI / 180)),
            accuracy, speed, heading: null,
          },
        } as GeolocationPosition);
      },
      fail(code: number) { callbacks.at(-1)?.error({ code } as GeolocationPositionError); },
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
      fix: (speed: number | null, index?: number, east?: number, accuracy?: number, acquiredAt?: number) => void;
      fail: (code: number) => void;
    };
  }
}

function roadManifest(epoch: number, revision = '1', current = 50, next = 30, boundary = 420): RoadManifest {
  const iso = (offset: number) => new Date(epoch + offset).toISOString();
  const point = (east: number) => [18.654321 + east / (111_195.08 * Math.cos(68.123456 * Math.PI / 180)), 68.123456] as const;
  const before = 'before-' + revision;
  const after = 'after-' + revision;
  return {
    id: 'synthetic-road', revision, profile: 'SL-LAB-1', uncertaintyM: 8,
    retrievedAt: iso(-4_000), checkedAt: iso(-4_000), validUntil: iso(60_000),
    path: [before, after],
    packages: [{ id: 'synthetic-one', revision, edges: [
      { id: before, from: 'a', to: 'b', shape: [point(0), point(boundary)], length: boundary, kmh: current, successors: [after] },
      { id: after, from: 'b', to: 'c', shape: [point(boundary), point(800)], length: 800 - boundary, kmh: next, successors: [] },
    ] }],
  };
}

type RoadReply = { status: 'qualified'; manifest: RoadManifest } | { status: 'road-unqualified' };

async function stubRoad(page: Page, reply: () => RoadReply | Promise<RoadReply>, serverTime?: number) {
  await page.route('**/road-reference/**', async route => route.fulfill({
    json: await reply(),
    headers: {
      'Access-Control-Allow-Origin': new URL(page.url()).origin,
      'Access-Control-Allow-Credentials': 'true',
      ...(serverTime === undefined ? {} : { Date: new Date(serverTime).toUTCString(), 'Access-Control-Expose-Headers': 'Date' }),
    },
  }));
}

test('standalone GPS shares one watch across the pilot network and clears on exit or access loss', async ({ page }) => {
  await page.clock.install();
  await syntheticPosition(page);
  const requests: string[] = [];
  page.on('request', request => requests.push(request.url() + (request.postData() ?? '')));
  let sessionUnavailable = false;
  let revision = '1';
  let roadAvailable = false;
  await page.route('**/auth/session', route => sessionUnavailable ? route.abort() : route.continue());
  await page.route('**/road-areas/*', async route => {
    const id = new URL(route.request().url()).pathname.split('/').at(-1);
    const base = roadManifest(Date.now(), revision);
    const manifest = {
      ...base, id, profile: 'NVDB-AREA-1', validFrom: base.retrievedAt, path: [],
      packages: base.packages.map(pack => ({ ...pack, edges: pack.edges.map(edge => ({ ...edge, kmh: null })) })),
    };
    await route.fulfill({
      json: !roadAvailable ? { status: 'road-unqualified' } : { status: 'qualified', manifest, confirmed: 0 },
      headers: { 'Access-Control-Allow-Origin': new URL(page.url()).origin, 'Access-Control-Allow-Credentials': 'true' },
    });
  });
  await page.route('**/road-areas/*/revision', route => {
    revision = 'updated-by-public-import';
    return route.fulfill({
      json: { revision },
      headers: { 'Access-Control-Allow-Origin': new URL(page.url()).origin, 'Access-Control-Allow-Credentials': 'true' },
    });
  });
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  const open = page.getByRole('button', { name: 'Åpne vegområde og GPS-fart' });
  const back = page.getByRole('button', { name: 'Tilbake til arbeidsområdet' });
  const panel = page.getByRole('region', { name: 'Vegområde og GPS-fart' });
  const active = () => page.evaluate(() => window.v2SyntheticPosition.count());
  const watched = () => page.evaluate(() => window.v2SyntheticPosition.watches());
  await open.click();
  await expect(panel.getByLabel('Vegområde', { exact: true })).toHaveCount(0);
  await expect(panel.getByText('Vegmatching følger posisjonen', { exact: false })).toBeVisible();
  expect(await watched()).toBe(0);
  expect(requests.filter(url => url.includes('/road-areas/'))).toHaveLength(0);
  await panel.getByRole('button', { name: 'Start fartsmåling' }).click();
  await expect.poll(active).toBe(1);
  await panel.getByRole('button', { name: 'Start vegmatching' }).click();
  await expect(panel.getByText('Veggrunnlag mangler for Tromsø bybuss på dagens dato.')).toBeVisible();
  roadAvailable = true;
  await panel.getByRole('button', { name: 'Start vegmatching' }).click();
  await expect(panel.getByText('Ingen fartsgrenser er bekreftet i dette uttaket.')).toBeVisible();
  expect(await watched()).toBe(1);
  await page.evaluate(() => window.v2SyntheticPosition.fix(10));
  await page.clock.fastForward(1_000);
  await page.evaluate(() => window.v2SyntheticPosition.fix(10, undefined, 18));
  await expect(panel.getByLabel('Målt egen fart')).toHaveText('36 km/t');
  for (let step = 0; step < 5; step++) {
    await page.clock.runFor(7_000);
    await page.evaluate(() => window.v2SyntheticPosition.fix(10));
  }
  await expect.poll(() => requests.filter(url => url.endsWith('/road-areas/pilot')).length).toBe(3);
  await expect(panel.getByRole('button', { name: 'Stopp vegmatching' })).toBeVisible();
  expect(await active()).toBe(1);
  expect(await active()).toBe(1);
  await back.click();
  await expect.poll(active).toBe(0);
  await open.click();
  await page.evaluate(() => window.v2SyntheticPosition.fix(10, 0));
  await expect(panel.getByLabel('Målt egen fart')).toHaveText('— km/t');
  await panel.getByRole('button', { name: 'Start fartsmåling' }).click();
  await expect.poll(active).toBe(1);
  sessionUnavailable = true;
  for (let step = 0; step < 5; step++) {
    await page.clock.runFor(7_000);
    if (!await active()) break;
    await page.evaluate(() => window.v2SyntheticPosition.fix(10));
  }
  await expect.poll(active).toBe(0);
  await expect(panel).toBeHidden();
  sessionUnavailable = false;
  await page.getByRole('button', { name: 'Kontroller tilgang igjen' }).click();
  await expect(panel.getByRole('button', { name: 'Start fartsmåling' })).toBeVisible();
  expect(await active()).toBe(0);
  expect(requests.filter(url => url.includes('/road-areas/')).map(url => new URL(url).pathname))
    .toEqual(['/road-areas/pilot', '/road-areas/pilot', '/road-areas/pilot/revision', '/road-areas/pilot']);
  expect(requests.some(value => value.includes('68.123456') || value.includes('18.654321'))).toBe(false);
});

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
  await page.evaluate(() => window.v2SyntheticPosition.fail(1));
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

test('road signs and own speed have independent availability and share one GPS watch', async ({ page, context }) => {
  await page.clock.install();
  await syntheticPosition(page);
  const manifest = roadManifest(Date.now());
  await stubRoad(page, () => ({ status: 'qualified', manifest }));
  await openedPlan(page, context, true);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  const road = page.getByRole('region', { name: 'Fartsgrense', exact: true });
  const roadStatus = road.getByRole('status');
  const startRoad = road.getByRole('button', { name: 'Start vegmatching' });
  const speed = page.getByLabel('Målt egen fart');
  const speedPanel = page.getByRole('region', { name: 'Egen fart (GPS)' });
  const watchCount = () => page.evaluate(() => window.v2SyntheticPosition.watches());
  const activeCount = () => page.evaluate(() => window.v2SyntheticPosition.count());
  async function fixes(eastings: number[], kmh: number | null = null) {
    for (const east of eastings) {
      await page.clock.fastForward(1_000);
      await page.evaluate(({ east, speed }) => window.v2SyntheticPosition.fix(speed, undefined, east), {
        east, speed: kmh === null ? null : kmh / 3.6,
      });
    }
  }
  await expect(road.getByRole('img')).toHaveCount(0);
  await expect(speed).toHaveText('— km/t');
  for (const [index, message] of ['Posisjonstilgangen er avvist', 'Posisjon er utilgjengelig'].entries()) {
    await startRoad.click();
    await expect.poll(watchCount).toBe(index + 1);
    await page.evaluate(code => window.v2SyntheticPosition.fail(code), index + 1);
    await expect(roadStatus).toContainText(message);
    await expect(startRoad).toBeEnabled();
    await expect(road.getByRole('img')).toHaveCount(0);
    expect(await activeCount()).toBe(0);
  }
  await startRoad.click();
  await expect.poll(activeCount).toBe(1);
  await fixes([145, 160, 175]);
  await expect(roadStatus).toBeEmpty();
  await expect(road.getByRole('img', { name: '50 km/t' })).toBeVisible();
  await expect(road.getByRole('img', { name: '30 km/t' })).toBeVisible();
  await expect(road).toContainText('ca. 250 m');
  await expect(speed).toHaveText('— km/t');
  await page.clock.fastForward(1_000);
  await page.evaluate(() => window.v2SyntheticPosition.fix(null, undefined, 190, -1));
  await expect(roadStatus).toHaveText('Posisjonsmålingen kunne ikke brukes.');
  await expect(road.getByRole('img')).toHaveCount(0);
  await fixes([205, 220, 235]);
  await expect(roadStatus).toBeEmpty();
  await expect(road.getByRole('img', { name: '50 km/t' })).toBeVisible();
  expect(await watchCount()).toBe(3);

  await page.evaluate(() => window.v2SyntheticPosition.fail(3));
  await expect(roadStatus).toContainText('Posisjonsmålingen tok for lang tid');
  await expect(road.getByRole('img')).toHaveCount(0);
  await page.clock.fastForward(1_000);
  await page.evaluate(() => window.v2SyntheticPosition.fix(null, 2, 250));
  await expect(roadStatus).toContainText('Posisjonsmålingen tok for lang tid');
  expect(await activeCount()).toBe(0);
  await startRoad.click();
  await expect.poll(activeCount).toBe(1);
  await fixes([265, 280]);
  await expect(road.getByRole('img')).toHaveCount(0);
  await fixes([295]);
  await expect(road.getByRole('img', { name: '50 km/t' })).toBeVisible();

  const beginSpeed = speedPanel.getByRole('button', { name: /fartsmåling/ });
  await beginSpeed.click();
  await expect(beginSpeed).toHaveCount(0);
  await fixes([310, 325], 36);
  await expect(speed).toHaveText('36 km/t');
  await expect(road.getByRole('img', { name: '50 km/t' })).toBeVisible();
  expect(await watchCount()).toBe(4);
  await road.getByRole('button', { name: 'Stopp vegmatching' }).click();
  await expect(road.getByRole('img')).toHaveCount(0);
  await expect(speed).toHaveText('36 km/t');
  expect(await activeCount()).toBe(1);
  await page.evaluate(() => window.v2SyntheticPosition.fail(1));
  await expect(speed).toHaveText('— km/t');
  await expect(roadStatus).toBeEmpty();
  await startRoad.click();
  await expect.poll(activeCount).toBe(1);
  await speedPanel.getByRole('button', { name: 'Pause posisjon' }).click();
  await expect(roadStatus).toContainText('Posisjon er satt på pause');
  await speedPanel.getByRole('button', { name: 'Slå av posisjon' }).click();
  await expect(roadStatus).toBeEmpty();
  expect(await activeCount()).toBe(0);
});

test('explicit road restart requalifies the entire snapshot before counting new fixes', async ({ page, context }) => {
  await page.clock.install();
  await syntheticPosition(page);
  const epoch = Date.now();
  const original: RoadReply = { status: 'qualified', manifest: roadManifest(epoch) };
  const replacement: RoadReply = { status: 'qualified', manifest: roadManifest(epoch, '2', 60, 40, 450) };
  let response: RoadReply | Promise<RoadReply> = original;
  let requests = 0;
  await stubRoad(page, () => { requests++; return response; });
  await openedPlan(page, context, true);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();

  const road = page.getByRole('region', { name: 'Fartsgrense', exact: true });
  const status = road.getByRole('status');
  const signs = road.getByRole('img');
  const start = road.getByRole('button', { name: 'Start vegmatching' });
  const stop = road.getByRole('button', { name: 'Stopp vegmatching' });
  const speed = page.getByRole('region', { name: 'Egen fart (GPS)' });
  const ownSpeed = page.getByLabel('Målt egen fart');
  const watches = () => page.evaluate(() => window.v2SyntheticPosition.watches());
  const active = () => page.evaluate(() => window.v2SyntheticPosition.count());
  async function fixes(eastings: number[]) {
    for (const east of eastings) {
      await page.clock.fastForward(1_000);
      await page.evaluate(value => window.v2SyntheticPosition.fix(10, undefined, value), east);
    }
  }
  function holdReply() {
    let release!: (reply: RoadReply) => void;
    response = new Promise(resolve => { release = resolve; });
    return release;
  }

  await speed.getByRole('button', { name: 'Start fartsmåling' }).click();
  await expect.poll(active).toBe(1);
  await start.click();
  await expect(stop).toBeVisible();
  await fixes([145, 160, 175]);
  await expect(road.getByRole('img', { name: '50 km/t' })).toBeVisible();
  await expect(road.getByRole('img', { name: '30 km/t' })).toBeVisible();
  await expect(ownSpeed).toHaveText('36 km/t');
  await stop.click();

  response = { status: 'qualified', manifest: { ...original.manifest, validUntil: new Date(epoch).toISOString() } };
  await start.click();
  await expect(status).toContainText('Vegdata er utløpt');
  await expect(signs).toHaveCount(0);
  const beforeWithdraw = requests;
  const withdraw = holdReply();
  await start.click();
  await expect.poll(() => requests).toBe(beforeWithdraw + 1);
  await page.clock.fastForward(1_000);
  await page.evaluate(() => window.v2SyntheticPosition.fix(10, undefined, 180, -1));
  withdraw({ status: 'road-unqualified' });
  await expect(status).toContainText('Kvalifisert veggrunnlag mangler');
  await expect(signs).toHaveCount(0);

  const beforeReplace = requests;
  const replace = holdReply();
  await start.click();
  await expect.poll(() => requests).toBe(beforeReplace + 1);
  await fixes([190, 205]);
  await expect(signs).toHaveCount(0);
  await expect(ownSpeed).toHaveText('36 km/t');
  await page.clock.fastForward(100);
  const acquiredBeforeRestart = await page.evaluate(() => Date.now());
  await page.clock.fastForward(100);
  replace(replacement);
  await expect(stop).toBeVisible();
  await page.evaluate(time => window.v2SyntheticPosition.fix(10, undefined, 210, 8, time), acquiredBeforeRestart);
  await fixes([220, 235]);
  await expect(signs).toHaveCount(0);
  await fixes([250]);
  await expect(road.getByRole('img', { name: '60 km/t' })).toBeVisible();
  await expect(road.getByRole('img', { name: '40 km/t' })).toBeVisible();
  await expect(signs).toHaveCount(2);
  expect(await watches()).toBe(1);
  await stop.click();

  const beforePause = requests;
  const late = holdReply();
  await start.click();
  await expect.poll(() => requests).toBe(beforePause + 1);
  await speed.getByRole('button', { name: 'Pause posisjon' }).click();
  await expect(status).toContainText('Posisjon er satt på pause');
  await expect(start).toBeEnabled();
  const current = holdReply();
  await start.click();
  await expect.poll(() => requests).toBe(beforePause + 2);
  const completed = page.waitForResponse('**/road-reference/**');
  late(original);
  await (await completed).finished();
  await expect(status).toContainText('Kontrollerer veggrunnlaget');
  await expect(signs).toHaveCount(0);
  expect(await active()).toBe(0);
  current(replacement);
  await expect(stop).toBeVisible();
  await fixes([265, 280, 295]);
  await expect(road.getByRole('img', { name: '60 km/t' })).toBeVisible();
  await expect(road.getByRole('img', { name: '40 km/t' })).toBeVisible();
  expect(await watches()).toBe(2);
});

test('road source retry checks qualification and cancellation before sensing', async ({ page, context }) => {
  await page.clock.install();
  await syntheticPosition(page);
  const epoch = Date.now();
  let reply: RoadReply | Promise<RoadReply> = { status: 'road-unqualified' };
  let requests = 0;
  await stubRoad(page, () => { requests++; return reply; }, epoch);
  await openedPlan(page, context, true);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();

  const road = page.getByRole('region', { name: 'Fartsgrense', exact: true });
  const status = road.getByRole('status');
  const start = road.getByRole('button', { name: 'Start vegmatching' });
  const watches = () => page.evaluate(() => window.v2SyntheticPosition.watches());
  const candidate = roadManifest(epoch - 60_000);
  const expired: RoadReply = { status: 'qualified', manifest: { ...candidate, validUntil: new Date(epoch - 10_000).toISOString() } };
  await expect(status).toContainText('Kvalifisert veggrunnlag mangler');
  reply = expired;
  await road.getByRole('button', { name: 'Kontroller veggrunnlaget på nytt' }).click();
  await expect(start).toBeEnabled();
  expect(await watches()).toBe(0);

  await page.clock.setSystemTime(new Date(epoch - 30_000));
  const beforeExpiry = requests;
  await start.click();
  await expect(status).toContainText('Vegdata er utløpt');
  expect(await watches()).toBe(0);
  expect(requests).toBe(beforeExpiry + 1);

  let late!: (answer: RoadReply) => void;
  reply = new Promise(resolve => { late = resolve; });
  await start.click();
  await expect.poll(() => requests).toBe(beforeExpiry + 2);
  await expect(status).toContainText('Kontrollerer veggrunnlaget');
  await road.getByRole('button', { name: 'Avbryt vegoppstart' }).click();
  await expect(start).toBeEnabled();
  const completed = page.waitForResponse('**/road-reference/**');
  late({ status: 'qualified', manifest: roadManifest(epoch) });
  await (await completed).finished();
  await expect(status).toBeEmpty();
  expect(await watches()).toBe(0);
});
