import { test, expect, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';

// Generated solely from test_pdf_import.synthetic_text_pdf(), never owner files.
const syntheticImport = JSON.parse(readFileSync(new URL('./fixtures/pdf-upload.json', import.meta.url), 'utf8').replace(/^\uFEFF/, ''));

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
  const state = { loggedIn: false, available: true, serverTime: now, logoutFails: false, unexpected: [] as string[], apiCalls: [] as string[], importStatus: 200, importBody: syntheticImport as object, importedBytes: [] as number[] };
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
    if (path === '/imports/pdf') {
      state.importedBytes = [...(request.postDataBuffer() ?? [])];
      await reply(state.importStatus, state.importBody); return;
    }
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

const syntheticPdf = { name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-synthetic-transport-\x00\xff', 'latin1') };

test('mobile PDF upload sends memory bytes and keeps the picker alive while reading', async ({ page, baseURL }) => {
  await page.addInitScript(() => {
    const originalRead = FileReader.prototype.readAsArrayBuffer;
    FileReader.prototype.readAsArrayBuffer = function (blob: Blob) {
      (window as any).pickerRetained = !!document.querySelector<HTMLInputElement>('input[type=file]')?.files?.length;
      return originalRead.call(this, blob);
    };
    const originalFetch = window.fetch;
    window.fetch = (input, init) => {
      if (String(input).endsWith('/imports/pdf')) {
        (window as any).memoryUpload = init?.body instanceof ArrayBuffer;
        // Model the iOS failure: disk-backed File is silently sent empty.
        if (init?.body instanceof File) init = { ...init, body: new ArrayBuffer(0) };
      }
      return originalFetch(input, init);
    };
  });
  const state = await fixture(page, baseURL);
  // Response validation is independent of transport. A malformed 200 must be
  // identified as a response failure rather than a damaged source PDF.
  state.importBody = {};
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles(syntheticPdf);
  await expect(page.getByText('Serveren returnerte et svar som ikke kunne brukes.', { exact: false })).toBeVisible();
  expect(await page.evaluate(() => [(window as any).memoryUpload, (window as any).pickerRetained])).toEqual([true, true]);
  expect(state.importedBytes).toEqual([...syntheticPdf.buffer]);
  await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toHaveValue('');
  expect(state.apiCalls).not.toContain('POST /drafts');
  expect(state.unexpected).toEqual([]);
});

for (const mode of ['error', 'short', 'timeout', 'cancel', 'logout', 'hidden'] as const) test(`PDF local read ${mode} never uploads or saves stale bytes`, async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  await page.evaluate(mode => {
    const originalRead = FileReader.prototype.readAsArrayBuffer;
    FileReader.prototype.readAsArrayBuffer = function (blob: Blob) {
      (window as any).pdfReader = this;
      if (mode === 'error') { queueMicrotask(() => this.dispatchEvent(new ProgressEvent('error'))); return; }
      if (mode === 'short') {
        Object.defineProperty(this, 'result', { value: new ArrayBuffer(1) });
        queueMicrotask(() => this.dispatchEvent(new ProgressEvent('load'))); return;
      }
      (window as any).completePdfRead = () => originalRead.call(this, blob);
    };
  }, mode);
  if (mode === 'timeout') await page.clock.install();
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles(syntheticPdf);
  if (mode === 'timeout') await page.clock.fastForward(10001);
  if (mode === 'cancel') await page.getByRole('button', { name: 'Avbryt import', exact: true }).click();
  if (mode === 'logout') await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  if (mode === 'hidden') await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  if (['error', 'short', 'timeout'].includes(mode)) await expect(page.getByText('PDF-filen kunne ikke leses fra enheten.', { exact: false })).toBeVisible();
  if (mode === 'cancel') await expect(page.getByText('Importen er avbrutt.', { exact: false })).toBeVisible();
  if (mode === 'logout') await expect(page.getByRole('status', { name: 'Tilgangsstatus' })).toHaveText('Du er logget ut.');
  if (mode === 'hidden') await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toBeHidden();
  // A completed native read after timeout/cancel/unmount cannot resume upload.
  await page.evaluate(() => (window as any).completePdfRead?.());
  await expect.poll(() => page.evaluate(() => (window as any).pdfReader.onload === null)).toBe(true);
  expect(state.apiCalls).not.toContain('POST /imports/pdf');
  expect(state.apiCalls).not.toContain('POST /drafts');
});

for (const [status, message] of [[403, 'Tilgangen til opplastingen ble avvist.'], [413, 'PDF-en er for stor.'], [422, 'PDF-en kunne ikke tolkes.'], [429, 'Import er opptatt.'], [503, 'Tjenesten er midlertidig utilgjengelig.']] as const) test(`PDF HTTP ${status} has an actionable error`, async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  state.importStatus = status;
  state.importBody = { detail: 'Synthetic error' };
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles(syntheticPdf);
  await expect(page.getByText(message, { exact: false })).toBeVisible();
  expect(state.apiCalls).not.toContain('POST /drafts');
  if (status !== 422) await expect(page.getByText('PDF-en kunne ikke tolkes.', { exact: false })).toHaveCount(0);
});

for (const order of ['selection-first', 'visibility-first'] as const)
for (const outcome of ['restored', 'cancel', 'logout', 'expired', 'different-account', 'unavailable'] as const) test(`native file picker ${order} handles ${outcome} access revalidation`, async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toBeHidden();
  let release!: () => void, started!: () => void;
  const held = new Promise<void>(resolve => { release = resolve; });
  const checking = new Promise<void>(resolve => { started = resolve; });
  await page.route('**/auth/session', async route => {
    started(); await held;
    if (outcome === 'expired' || outcome === 'unavailable') {
      await route.fulfill({ status: outcome === 'expired' ? 401 : 503, contentType: 'application/json', body: '{"detail":"Synthetic rejection"}' }); return;
    }
    if (outcome === 'different-account') {
      const now = Date.now();
      await route.fulfill({ json: { account_id: 'b0000000-0000-4000-8000-000000000002', created_at: new Date(now).toISOString(), expires_at: new Date(now + 14 * 86400_000).toISOString() } }); return;
    }
    await route.fallback();
  });
  await page.evaluate(() => {
    const originalRead = FileReader.prototype.readAsArrayBuffer;
    FileReader.prototype.readAsArrayBuffer = function (blob: Blob) {
      this.addEventListener('load', () => { (window as any).pdfReadComplete = true; });
      return originalRead.call(this, blob);
    };
  });
  const returnToPage = () => page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  if (order === 'visibility-first') { await returnToPage(); await checking; }
  // Native pickers can deliver change while the page is revalidating; disabled
  // protects new clicks but does not cancel the already-open picker result.
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles(syntheticPdf);
  await expect.poll(() => page.evaluate(() => (window as any).pdfReadComplete)).toBe(true);
  if (order === 'selection-first') { await returnToPage(); await checking; }
  expect(state.apiCalls).not.toContain('POST /imports/pdf');
  if (outcome === 'cancel') {
    await page.getByRole('button', { name: 'Avbryt import', exact: true, includeHidden: true }).evaluate((button: HTMLButtonElement) => button.click());
    // Cancellation settles before the held session response is released.
    await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toHaveValue('', { timeout: 1000 });
  }
  if (outcome === 'logout') await page.evaluate(() => {
    const channel = new BroadcastChannel('private-access-security');
    channel.postMessage('logout-pending'); channel.close();
  });
  if (outcome === 'logout') await expect(page.getByRole('status', { name: 'Tilgangsstatus' })).toContainText('Privat innhold er låst');
  release();
  if (outcome === 'restored') {
    await expect.poll(() => state.importedBytes).toEqual([...syntheticPdf.buffer]);
    await expect(page.getByRole('button', { name: 'Rett eller legg til opplysninger', exact: true })).toBeVisible();
    await page.getByText('Vis alle kildefakta fra PDF', { exact: true }).click();
    const rows = page.getByRole('region', { name: 'Kildefakta fra PDF', exact: true }).locator(':scope > ol > li');
    await expect(rows).toHaveCount(syntheticImport.activities.length);
    await page.getByRole('button', { name: 'Rett eller legg til opplysninger', exact: true }).click();
    await expect(page.getByLabel('Aktivitetstype', { exact: true })).toHaveCount(syntheticImport.activities.length);
    expect(state.apiCalls).not.toContain('POST /drafts');
  } else {
    await page.waitForLoadState('networkidle');
    expect(state.apiCalls).not.toContain('POST /imports/pdf');
    expect(state.apiCalls).not.toContain('POST /drafts');
    await expect(page.getByRole('button', { name: 'Rett eller legg til opplysninger', exact: true })).toHaveCount(0);
  }
});

for (const failure of ['invalid-json', 'network', 'body-timeout'] as const) test(`PDF ${failure} is distinct from parser rejection`, async ({ page, baseURL }) => {
  const state = await fixture(page, baseURL);
  if (failure === 'body-timeout') {
    await page.evaluate(() => {
      const originalFetch = window.fetch;
      window.fetch = async (input, init) => {
        const response = await originalFetch(input, init);
        if (String(input).endsWith('/imports/pdf')) response.json = async () => { throw new DOMException('Synthetic body timeout', 'TimeoutError'); };
        return response;
      };
    });
  }
  await page.route('**/imports/pdf', route => failure === 'network' ? route.abort() : route.fulfill({ status: 200, contentType: 'application/json', body: '{' }));
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles(syntheticPdf);
  await expect(page.getByText(failure === 'network' ? 'Opplastingen kunne ikke fullføres.' : failure === 'body-timeout' ? 'Opplastingen eller tolkingen tok for lang tid.' : 'Serveren returnerte et svar som ikke kunne brukes.', { exact: false })).toBeVisible();
  expect(state.apiCalls).not.toContain('POST /drafts');
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
