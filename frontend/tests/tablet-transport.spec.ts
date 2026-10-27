import { test, expect, type Page } from '@playwright/test';

// Boundary regression for the combined main/tablet frontend. No real accounts,
// cookies, Cloudflare tokens, Docker commands or database connections are used.
async function fixture(page: Page, baseURL: string | undefined) {
  if (!baseURL || !/^http:\/\/127\.0\.0\.1:1848[13]$/.test(baseURL)) throw Error('Expected strict loopback tablet baseURL');
  const allowedOrigin = new URL(baseURL).origin;
  const now = Date.now();
  const session = {
    account_id: 'a0000000-0000-4000-8000-000000000001',
    created_at: new Date(now - 60_000).toISOString(),
    expires_at: new Date(now - 60_000 + 14 * 86400_000).toISOString(),
  };
  const state = { loggedIn: false, available: true, serverTime: now, logoutFails: false, unexpected: [] as string[], apiCalls: [] as string[] };
  await page.route('**/*', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.origin !== allowedOrigin) {
      state.unexpected.push(url.origin + url.pathname);
      await route.abort(); return;
    }
    if (!url.pathname.startsWith('/private-api/')) { await route.continue(); return; }
    const path = url.pathname.slice('/private-api'.length);
    state.apiCalls.push(request.method() + ' ' + path);
    const reply = (status: number, body: object) => route.fulfill({
      status, contentType: 'application/json', body: JSON.stringify(body),
      headers: { Date: new Date(state.serverTime).toUTCString(), 'Cache-Control': 'no-store' },
    });
    if (!state.available) { await reply(503, { detail: 'Tjenesten er utilgjengelig.' }); return; }
    if (path === '/auth/csrf') { await reply(200, { csrf_token: 'synthetic-browser-proof' }); return; }
    if (path === '/auth/login' && request.method() === 'POST') { state.loggedIn = true; await reply(200, session); return; }
    if (path === '/auth/logout' && request.method() === 'POST') { if (state.logoutFails) { await reply(503, { detail: 'Synthetic logout unavailable.' }); return; } state.loggedIn = false; await reply(200, { revoked: true }); return; }
    if (!state.loggedIn) { await reply(401, { detail: 'Logg inn på nytt.' }); return; }
    if (path === '/auth/session') { await reply(200, session); return; }
    if (path === '/drafts') { await reply(200, { drafts: [], next_cursor: null }); return; }
    if (path === '/workdays') { await reply(200, { workdays: [], next_cursor: null }); return; }
    await reply(404, { detail: 'Synthetic fixture has no such resource.' });
  });
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill('synthetic-tablet-browser');
  await page.getByLabel('Passord', { exact: true }).fill('synthetic-not-a-real-password');
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
  // Finish the initial authenticated reads before a test changes server time.
  await page.waitForLoadState('networkidle');
  return state;
}

test('tablet API base overrides the configured legacy API and logout stays effective after reload', async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  expect(state.apiCalls).toContain('POST /auth/login');
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Tilgangsstatus' })).toHaveText('Du er logget ut.');
  await page.reload();
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeHidden();
  expect(state.apiCalls).toContain('POST /auth/logout');
  expect(state.unexpected).toEqual([]);
});

test('session suspension hides private input and restores the same unsaved proposal', async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click();
  await page.getByLabel('Vognløp', { exact: true }).fill('FIKTIV-BROWSER-RETAINED');
  state.available = false;
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true })).toBeVisible();
  await expect(page.getByLabel('Vognløp', { exact: true })).toBeHidden();
  state.available = true;
  await page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true }).click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('FIKTIV-BROWSER-RETAINED');
  expect(state.unexpected).toEqual([]);
});

test('main server-clock expiry remains enforced with the relative tablet API', async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  state.serverTime = Date.now() + 15 * 86400_000;
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeHidden();
  await expect(page.getByRole('status', { name: 'Tilgangsstatus' })).toContainText('utløpt');
  expect(state.unexpected).toEqual([]);
});


test('actual dedicated tablet entry changes theme and preserves only preference across reload and logout', async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  const theme = page.getByRole('button', { name: 'Nattmodus', exact: true });
  await expect(theme).toHaveAttribute('aria-pressed', 'false');
  const before = await page.locator('main').evaluate(node => getComputedStyle(node).backgroundColor);
  await theme.click();
  await expect(theme).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'night');
  expect(await page.locator('main').evaluate(node => getComputedStyle(node).backgroundColor)).not.toBe(before);
  await page.reload();
  await expect(theme).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await page.reload();
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  await expect(theme).toHaveAttribute('aria-pressed', 'true');
  expect(await page.evaluate(async () => ({ local: { ...localStorage }, session: { ...sessionStorage }, databases: await indexedDB.databases(), caches: await caches.keys(), workers: (await navigator.serviceWorker.getRegistrations()).map(worker => worker.scope) }))).toEqual({ local: { 'ibe160-theme': 'night' }, session: {}, databases: [], caches: [], workers: [] });
  expect(state.unexpected).toEqual([]);
});


test('failed logout keeps private content locked through reload and settles only after retry while theme persists', async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  const theme = page.getByRole('button', { name: 'Nattmodus', exact: true });
  await theme.click();
  state.logoutFails = true;
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  const status = page.getByRole('status', { name: 'Tilgangsstatus' });
  const retry = page.getByRole('button', { name: 'Prøv utlogging igjen', exact: true });
  await expect(status).toContainText('Utlogging er ikke bekreftet');
  await expect(retry).toBeEnabled();
  expect(state.loggedIn).toBe(true); // Server session remains valid: the UI must shield it.
  expect(await page.context().cookies()).toEqual(expect.arrayContaining([expect.objectContaining({ name: 'private_logout_pending', value: '1' })]));
  const callsBeforeReload = state.apiCalls.length;
  await page.reload();
  await expect(retry).toBeEnabled();
  await expect(status).toContainText('Privat innhold er låst');
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeHidden();
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeHidden();
  await expect(theme).toHaveAttribute('aria-pressed', 'true');
  expect(state.apiCalls.slice(callsBeforeReload)).toEqual(['GET /auth/csrf', 'POST /auth/logout']);
  state.logoutFails = false;
  await retry.click();
  await expect(status).toHaveText('Du er logget ut.');
  expect(state.loggedIn).toBe(false);
  expect((await page.context().cookies()).some(cookie => cookie.name === 'private_logout_pending')).toBe(false);
  await page.reload();
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeHidden();
  await expect(theme).toHaveAttribute('aria-pressed', 'true');
  expect(state.unexpected).toEqual([]);
});
