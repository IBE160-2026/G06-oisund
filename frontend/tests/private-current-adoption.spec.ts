import { test, expect, openedPlan, API, post, randomUUID, setup, beforeUnload } from './private-activity-helpers';
import type { Page, BrowserContext } from '@playwright/test';

setup();
test.use({ actionTimeout: 15000 });
type Resource = 'bus' | 'selection';
async function conflicted(page: Page, context: BrowserContext, resource: Resource, advance = true) {
  const { plan, activities } = await openedPlan(page, context);
  const path = '/workdays/' + plan.id + (resource === 'bus' ? '/physical-bus' : '/selection');
  const scope = page.getByRole('region', { name: resource === 'bus' ? 'Fysisk buss' : 'Aktivitetsvalg', exact: true });
  const load = scope.getByRole('button', { name: resource === 'bus' ? 'Last inn lagret buss' : 'Last inn lagret aktivitetsvalg', exact: true });
  const command = (revision: number, third: boolean) => ({ operation_id: randomUUID(), expected_revision: revision, ...(resource === 'bus' ? { physical_bus: third ? 'Synthetic current C' : 'Synthetic comparison B' } : { activity_id: activities[third ? 2 : 0].id }) });
  if (resource === 'bus') await scope.getByLabel('Fysisk buss', { exact: true }).fill('Synthetic local proposal A');
  const b = await post(context, path, command(0, false));
  await page.getByRole('button', { name: resource === 'bus' ? 'Lagre fysisk buss' : 'Velg aktivitet 2', exact: true }).click();
  await expect(load).toBeEnabled();
  if (resource === 'bus') await expect(scope.getByLabel('Fysisk buss', { exact: true })).toHaveValue('Synthetic local proposal A');
  else await expect(scope.getByText(/^Lokalt forslag/)).toContainText('24');
  const c = advance ? await post(context, path, command(1, true)) : b;
  let reads = 0, writes = 0;
  page.on('request', request => { if (request.url() === API + path) { if (request.method() === 'GET') reads++; if (request.method() === 'POST') writes++; } });
  return { plan, activities, path, scope, load, c: c.result, reads: () => reads, writes: () => writes };
}
async function proposalRetained(page: Page, resource: Resource, scope: any) {
  if (resource === 'bus') await expect(scope.getByLabel('Fysisk buss', { exact: true })).toHaveValue('Synthetic local proposal A');
  else await expect(scope.getByText(/^Lokalt forslag/)).toContainText('24');
  expect(await beforeUnload(page)).toBe(true);
}

for (const resource of ['bus', 'selection'] as const) {
  test(`${resource}: adopting comparison reads actual newer C without another write`, async ({ page, context }) => {
    const state = await conflicted(page, context, resource);
    await state.load.click();
    await expect.poll(state.reads).toBe(1);
    if (resource === 'bus') await expect(state.scope.getByLabel('Fysisk buss', { exact: true })).toHaveValue('Synthetic current C');
    else {
      await expect(state.scope.getByText(/^Manuelt valgt/)).toContainText('Aktivitet 3');
      await expect(state.scope.getByText(/^Lokalt forslag/)).toHaveCount(0);
    }
    expect(state.writes()).toBe(0);
    expect(await beforeUnload(page)).toBe(false);
    expect(await (await context.request.get(API + state.path)).json()).toEqual(state.c);
  });

  for (const shortened of [false, true]) test(`${resource}: actual equal-revision adoption succeeds with ${shortened ? 'legitimately shortened' : 'unchanged'} deadline`, async ({ page, context }) => {
    const state = await conflicted(page, context, resource, false);
    if (shortened) {
      await post(context, '/workdays/' + state.plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 });
      await post(context, '/workdays/' + state.plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
    }
    const expected = await (await context.request.get(API + state.path)).json();
    expect(expected.revision).toBe(state.c.revision);
    if (shortened) expect(Date.parse(expected.expires_at)).toBeLessThan(Date.parse(state.c.expires_at));
    else expect(expected.expires_at).toBe(state.c.expires_at);
    await state.load.click();
    await expect.poll(state.reads).toBe(1);
    if (resource === 'bus') await expect(state.scope.getByLabel('Fysisk buss', { exact: true })).toHaveValue('Synthetic comparison B');
    else {
      await expect(state.scope.getByText(/^Manuelt valgt/)).toContainText('Aktivitet 1');
      await expect(state.scope.getByText(/^Lokalt forslag/)).toHaveCount(0);
    }
    expect(await beforeUnload(page)).toBe(false);
    expect(state.writes()).toBe(0);
    expect(await (await context.request.get(API + state.path)).json()).toEqual(expected);
  });

  for (const failure of ['unavailable', 'regressed', 'changed-equal-revision', 'expired-timestamp', 'renewed-deadline', 'denied', 'unauthorized'] as const) {
    test(`${resource}: ${failure} fresh adoption never replaces local proposal with cached comparison`, async ({ page, context }) => {
      const state = await conflicted(page, context, resource);
      await page.route('**:8001' + state.path, async route => {
        if (failure === 'unavailable') return route.fulfill({ status: 503, json: { detail: 'Synthetic unavailable current read' } });
        if (failure === 'denied') return route.fulfill({ status: 410, json: { detail: 'Tilgangen ble avvist.' } });
        if (failure === 'unauthorized') return route.fulfill({ status: 401, json: { detail: 'Økten er utløpt.' } });
        if (failure === 'renewed-deadline') {
          // Controlled response adaptation of real saved C: only the future
          // retention deadline is renewed. The actual database is unchanged.
          const response = await route.fetch(), value = await response.json();
          value.expires_at = new Date(Date.parse(value.expires_at) + 86400000).toISOString();
          return route.fulfill({ response, json: value });
        }
        const value = { ...state.c, ...(failure === 'expired-timestamp' ? { expires_at: '2000-01-01T00:00:00+00:00' } : { revision: failure === 'regressed' ? 0 : 1 }) };
        await route.fulfill({ json: value });
      });
      await state.load.click();
      await expect.poll(state.reads).toBe(1);
      expect(state.writes()).toBe(0);
      if (failure === 'unauthorized') {
        await expect(page.getByRole('heading', { name: 'Logg inn', exact: true })).toBeVisible();
        await expect(state.scope).toHaveCount(0);
      } else {
        await proposalRetained(page, resource, state.scope);
        // Retry remains reachable even when current authority has been denied.
        await expect(state.load).toBeEnabled();
        await page.unroute('**:8001' + state.path);
        await state.load.click();
        await expect.poll(state.reads).toBe(2);
        if (resource === 'bus') await expect(state.scope.getByLabel('Fysisk buss', { exact: true })).toHaveValue('Synthetic current C');
        else await expect(state.scope.getByText(/^Manuelt valgt/)).toContainText('Aktivitet 3');
        expect(await beforeUnload(page)).toBe(false);
        expect(state.writes()).toBe(0);
      }
    });
  }
}
