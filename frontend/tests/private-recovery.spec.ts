import { test, expect, setup, account, API, post, openedPlan, beforeUnload, randomUUID, activityScreen, shiftStatus } from './private-activity-helpers';
import { editor, preparation } from './private-screen-helpers';
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';

setup();
const status = (page: any) => page.getByRole('region', { name: 'Private utkast', exact: true }).getByRole('status');
const save = (page: any) => page.getByRole('button', { name: 'Lagre utkast', exact: true });
const retry = (page: any) => page.getByRole('button', { name: 'Prøv samme lagringsforsøk igjen', exact: true });
async function draft(page: any) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible(); await editor(page);
  await page.getByLabel('Tjenestedato', { exact: true }).fill('2031-01-02');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('Original proposal');
}
async function suspension(page: any) {
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByRole('button', { name: 'Kontroller lagringsforsøket' })).toBeEnabled();
}

test('before acceptance repeated retries require status and preserve immutable command through suspension', async ({ page, context }) => {
  await draft(page); const sent: any[] = [];
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() === 'POST') { sent.push(route.request().postDataJSON()); await route.abort(); } else await route.continue();
  });
  await save(page).click(); await expect(status(page)).toContainText('Lagring er uavklart');
  await page.route('**:8001/draft-operations/*', route => route.abort());
  for (let i = 0; i < 2; i++) {
    await retry(page).click(); await expect(status(page)).toContainText('Lagring er uavklart');
    expect(sent).toHaveLength(1);
  }
  expect(await beforeUnload(page)).toBe(true); await suspension(page);
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal');
  await page.unroute('**:8001/draft-operations/*'); await page.unroute('**:8001/drafts');
  page.on('request', request => { if (request.method() === 'POST' && new URL(request.url()).pathname === '/drafts') sent.push(request.postDataJSON()); });
  await retry(page).click(); await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  expect(sent).toHaveLength(2); expect(sent[1]).toEqual(sent[0]);
  expect((await (await context.request.get(API + '/drafts')).json()).drafts).toHaveLength(1);
  expect(await beforeUnload(page)).toBe(false);
  await page.reload(); await preparation(page);
  await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal');
});

test('a real request deadline before backend acceptance or forwarding retains the original command for status-first retry', async ({ page, context }) => {
  test.setTimeout(45000); await draft(page);
  let release!: () => void, original: any;
  const held = new Promise<void>(resolve => { release = resolve; });
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    original = route.request().postDataJSON();
    // Do not forward the write. Let the application's actual 10 s signal expire.
    await held; await route.abort().catch(() => {});
  });
  try {
    await save(page).click(); await expect(status(page)).toHaveText('Lagrer …');
    await expect(status(page)).toContainText('Lagring er uavklart', { timeout: 15000 });
    expect((await (await context.request.get(API + '/drafts')).json()).drafts).toHaveLength(0);
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal');
    expect(await beforeUnload(page)).toBe(true);
  } finally { release(); }
  await page.unroute('**:8001/drafts');
  let retried: any;
  page.on('request', request => { if (request.method() === 'POST' && new URL(request.url()).pathname === '/drafts') retried = request.postDataJSON(); });
  await retry(page).click(); await expect(status(page)).toHaveText('Lagret. Versjon 1.'); expect(retried).toEqual(original);
  expect((await (await context.request.get(API + '/drafts')).json()).drafts).toHaveLength(1);
});

test('fresh save preflight failure sends no write POST and retains unconfirmed input after restoration', async ({ page, context }) => {
  await draft(page); const posts: string[] = [];
  // Install the failure only after initial list/plan reads finish. Otherwise
  // their own authorization check can suspend the editor before the save click.
  await expect(page.locator('.draft-loaded-count')).toHaveText('Lastet 0 utkast.');
  await expect(page.locator('.private-confirmation')).toHaveAttribute('aria-busy', 'false');
  page.on('request', request => { if (request.method() === 'POST') posts.push(new URL(request.url()).pathname); });
  await page.route('**:8001/auth/session', route => route.abort());
  await save(page).click();
  await expect(page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true })).toBeEnabled();
  expect(posts).toEqual([]); expect(await beforeUnload(page)).toBe(true);
  await page.unroute('**:8001/auth/session'); await page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal');
  await expect(status(page)).not.toHaveText(/Lagret\. Versjon/);
  expect((await (await context.request.get(API + '/drafts')).json()).drafts).toHaveLength(0);
  await save(page).click(); await expect(status(page)).toHaveText('Lagret. Versjon 1.');
});

test('absent bus receipt authorization race resends the exact original command and cannot overwrite another window', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/physical-bus'; const commands: any[] = [];
  const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true });
  await expect(bus.getByLabel('Fysisk buss', { exact: true })).toBeEnabled();
  await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET') return route.continue();
    commands.push(route.request().postDataJSON()); await route.abort();
  });
  await bus.getByLabel('Fysisk buss', { exact: true }).fill('Original bus proposal'); await page.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click();
  const recover = page.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true }); await expect(recover).toBeEnabled();
  expect((await context.request.get(API + '/workday-bus-operations/' + commands[0].operation_id)).status()).toBe(404);
  await page.unroute('**:8001' + path); let raced = false;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'POST') { commands.push(route.request().postDataJSON()); return route.continue(); }
    if (raced) return route.continue();
    const response = await route.fetch(); raced = true;
    await post(context, path, { operation_id: randomUUID(), expected_revision: 0, physical_bus: 'Another window bus' });
    await route.fulfill({ response });
  });
  await recover.click(); await expect(bus.getByRole('status')).toContainText('annet vindu');
  expect(commands).toHaveLength(2); expect(commands[1]).toEqual(commands[0]);
  await expect(bus.getByLabel('Fysisk buss', { exact: true })).toHaveValue('Original bus proposal');
  const saved = await (await context.request.get(API + path)).json(); expect(saved.physical_bus).toBe('Another window bus'); expect(saved.revision).toBe(1);
  expect((await context.request.get(API + '/workday-bus-operations/' + commands[0].operation_id)).status()).toBe(404);
});

for (const code of [409, 422, 404, 410, 413, 503]) test(`lost acceptance with HTML proxy ${code} never establishes rejection or redispatches`, async ({ page, context }) => {
  await draft(page); let original: any;
  const writes: any[] = [];
  page.on('request', request => {
    if (request.method() === 'POST' && /^\/drafts(?:\/[^/]+)?$/.test(new URL(request.url()).pathname)) writes.push(request.postDataJSON());
  });
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    original = await (await route.fetch()).json(); await route.fulfill({ status: code, contentType: 'text/html', body: '<html>Proxy unavailable</html>' });
  });
  await save(page).click(); await expect(status(page)).toContainText('Lagring er uavklart');
  const check = page.getByRole('button', { name: 'Kontroller lagringsforsøket', exact: true });
  await expect(check).toBeEnabled();
  let failedLookups = 0;
  await page.route('**:8001/draft-operations/*', route => { failedLookups++; return route.abort(); });
  await check.click();
  await expect.poll(() => failedLookups).toBe(1);
  // Keep the fault until the lookup has actually finished. Its existing
  // unresolved text alone cannot prove that a newly started check settled.
  await expect(check).toBeEnabled(); await expect(retry(page)).toBeEnabled();
  await expect(status(page)).toContainText('Lagring er uavklart'); await expect(status(page)).not.toContainText('ikke lagret');
  // Exercise a retained background list refresh without navigating away from
  // the unresolved editor; the preparation button is intentionally hidden.
  const refreshed = page.waitForResponse(response => response.request().method() === 'GET' && new URL(response.url()).pathname === '/drafts');
  await page.getByRole('button', { name: 'Oppdater listen', exact: true, includeHidden: true }).evaluate((button: HTMLButtonElement) => button.click());
  await refreshed;
  await expect(status(page)).toContainText('Lagring er uavklart');
  expect(writes).toHaveLength(1);
  await page.unroute('**:8001/draft-operations/*');
  await retry(page).click(); await expect(status(page)).toHaveText('Lagret. Versjon 1.'); expect(writes).toHaveLength(1);
  const rows = (await (await context.request.get(API + '/drafts')).json()).drafts;
  expect(rows).toHaveLength(1); expect(rows[0].id).toBe(original.id); expect(rows[0].revision).toBe(1);
  expect(await (await context.request.get(API + '/drafts/' + original.id)).json()).toEqual(original);
});

test('historical acceptance compares latest revision and adoption reads again before discarding proposal', async ({ page, context }) => {
  await draft(page); let original: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    original = await (await route.fetch()).json(); await route.abort();
  });
  await save(page).click(); await expect(status(page)).toContainText('Lagring er uavklart'); await page.unroute('**:8001/drafts');
  const update = async (revision: number, bus: string) => post(context, '/drafts/' + original.id, { operation_id: (await post(context, '/draft-operations', { draft_id: original.id })).operation_id, expected_revision: revision, draft: { ...original.draft, physical_bus: bus } });
  await update(1, 'Newer saved bus'); await retry(page).click();
  await expect(status(page)).toContainText('En nyere lagret versjon');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal');
  const comparison = page.getByRole('region', { name: 'Sammenlign versjoner', exact: true });
  await expect(comparison).toContainText('Newer saved bus'); await expect(save(page)).toBeDisabled();
  await update(2, 'Newest saved bus');
  page.once('dialog', dialog => dialog.accept());
  await comparison.getByRole('button', { name: 'Last inn lagret versjon', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 3.');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Newest saved bus');
  expect((await (await context.request.get(API + '/drafts/' + original.id)).json()).expires_at).toBe(original.expires_at);
});

for (const response of ['regressed', 'retimed', 'contradictory']) test(`comparison adoption preserves proposal when current draft is ${response}`, async ({ page, context }) => {
  await draft(page); let original: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    original = await (await route.fetch()).json(); await route.abort();
  });
  await save(page).click(); await expect(retry(page)).toBeEnabled(); await page.unroute('**:8001/drafts');
  const latest = await post(context, '/drafts/' + original.id, { operation_id: (await post(context, '/draft-operations', { draft_id: original.id })).operation_id, expected_revision: 1, draft: { ...original.draft, physical_bus: 'Shown newer comparison' } });
  await retry(page).click(); const comparison = page.getByRole('region', { name: 'Sammenlign versjoner', exact: true });
  await expect(comparison).toContainText('Shown newer comparison');
  const invalid = response === 'regressed' ? original : response === 'retimed' ? { ...latest, created_at: new Date(Date.parse(latest.created_at) + 1000).toISOString(), expires_at: new Date(Date.parse(latest.expires_at) + 1000).toISOString() } : { ...latest, draft: { ...latest.draft, physical_bus: 'Contradictory same revision' } };
  await page.route('**:8001/drafts/' + original.id, route => route.fulfill({ json: invalid }));
  page.once('dialog', dialog => dialog.accept()); await comparison.getByRole('button', { name: 'Last inn lagret versjon', exact: true }).click();
  await expect(status(page)).toContainText('Inndata er beholdt');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal');
  await expect(comparison).toContainText('Shown newer comparison'); await expect(save(page)).toBeDisabled(); expect(await beforeUnload(page)).toBe(true);
});

test('typed rejection preserves editable input while failed current read after acceptance stays unknown', async ({ page }) => {
  await draft(page);
  await page.route('**:8001/drafts', route => route.request().method() === 'POST' ? route.fulfill({ status: 422, json: { detail: 'Kontroller feltene.' } }) : route.continue());
  await save(page).click(); await expect(status(page)).toContainText('Ingen endringer er lagret');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toBeEnabled();
  await page.unroute('**:8001/drafts');
  await page.route('**:8001/drafts/*', route => route.request().method() === 'GET' ? route.fulfill({ status: 422, json: { detail: 'Kontroller feltene.' } }) : route.continue());
  await save(page).click(); await expect(status(page)).toContainText('Lagring er uavklart');
  await expect(status(page)).not.toContainText('Ingen endringer er lagret');
  await page.unroute('**:8001/drafts/*'); await retry(page).click(); await expect(status(page)).toHaveText('Lagret. Versjon 1.');
});

test('real API stop and start retains uncertain accepted command and recovers once', async ({ page, context }) => {
  test.setTimeout(90000); await draft(page); let original: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    original = await (await route.fetch()).json(); await route.abort();
  });
  await save(page).click(); await expect(status(page)).toContainText('Lagring er uavklart');
  const compose = (...args: string[]) => execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', ...args], { cwd: '..', encoding: 'utf8', timeout: 45000 });
  try {
    compose('stop', 'private-api'); await retry(page).click();
    await expect(page.getByRole('status', { name: 'Tilgangsstatus', exact: true })).toContainText('Tilgangen kan ikke bekreftes');
    await expect(page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true })).toBeVisible();
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal'); expect(await beforeUnload(page)).toBe(true);
  } finally { compose('start', '--wait', 'private-api'); }
  await page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Original proposal');
  await retry(page).click(); await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  expect((await (await context.request.get(API + '/drafts/' + original.id)).json()).revision).toBe(1);
});

test('notice save check and manual end recover with status first and reader refresh shows only saved facts', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click(); await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
  await page.getByLabel('Tittel', { exact: true }).fill('Synthetic outage notice');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20');
  let writes = 0; const commands: any[] = [];
  await page.route('**:8001/notices**', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    writes++; commands.push(route.request().postDataJSON()); await route.fetch(); await route.abort();
  });
  const noticeStatus = page.getByRole('status', { name: 'Avviksstatus', exact: true });
  const noticeRetry = page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true });
  const recover = async (action: () => Promise<any>, expected: string) => {
    await action(); await expect(noticeRetry).toBeEnabled(); await expect(noticeStatus).toContainText('uavklart');
    await page.route('**:8001/workday-notice-operations/*', route => route.abort());
    await noticeRetry.click(); await expect(noticeRetry).toBeEnabled(); await expect(noticeStatus).toContainText('uavklart');
    await page.unroute('**:8001/workday-notice-operations/*');
    await page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }).click(); await expect(noticeStatus).toHaveText(expected);
  };
  await recover(() => page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(), 'Avviket er lagret.');
  expect(writes).toBe(1);
  if (!await page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).isVisible()) await page.locator('.notice-list summary').click();
  await recover(() => page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).click(), 'Kildekontrollen er lagret.');
  page.once('dialog', dialog => dialog.accept());
  await recover(() => page.getByRole('button', { name: 'Avslutt avvik manuelt', exact: true }).click(), 'Avviket er avsluttet manuelt.');
  expect(writes).toBe(3); expect(new Set(commands.map(body => body.operation_id)).size).toBe(3);
  const records = (await (await context.request.get(API + '/notices')).json()).notices;
  expect(records).toHaveLength(1); expect(records[0].status).toBe('ended_manually'); expect(records[0].revision).toBe(3); expect(records[0].checked_revision).toBe(2);
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
  await expect(reader.getByRole('status')).toHaveText('Lagrede avvik er hentet.');
  await expect(reader.locator('summary')).toHaveCount(0);
  await page.route('**:8001/workdays/' + plan.id + '/notice-reader*', route => route.abort());
  await reader.getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click();
  await expect(reader.getByRole('status')).toContainText('utilgjengelig');
  await expect(reader.locator('summary')).toHaveCount(0);
  await page.unroute('**:8001/workdays/' + plan.id + '/notice-reader*');
  await reader.getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click();
  await expect(reader.getByRole('status')).toHaveText('Lagrede avvik er hentet.');
  await expect(reader.locator('summary')).toHaveCount(0);
  await expect(reader).toContainText('Ingen lagrede avvik samsvarer med valget.');
  expect((await (await context.request.get(API + '/notices')).json()).notices).toEqual(records);
});

test('notice edits replace a previous saved message with explicit unsaved status', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click(); await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
  await page.getByLabel('Tittel', { exact: true }).fill('Saved notice');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20');
  const noticeStatus = page.getByRole('status', { name: 'Avviksstatus', exact: true });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(noticeStatus).toHaveText('Avviket er lagret.');
  await page.getByRole('button', { name: 'Rediger Saved notice', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Retained unsaved proposal');
  await expect(noticeStatus).toHaveText('Ulagrede avviksendringer. Inndata finnes bare mens siden er åpen.');
  await expect(noticeStatus).not.toContainText('er lagret');
  const saved = (await (await context.request.get(API + '/notices')).json()).notices;
  expect(saved).toHaveLength(1); expect(saved[0].title).toBe('Saved notice');
  expect(await beforeUnload(page)).toBe(true);
});

test('dirty notice survives actual API suspension and same-session restoration before explicit save', async ({ page, context }) => {
  test.setTimeout(90000); const { plan } = await openedPlan(page, context);
  const notice = (await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { title: 'Saved notice before outage', line_tags: ['20'], source_url: null, source_updated_at: null, valid_from: null, valid_until: '2031-01-04T23:59:59+01:00' } })).result;
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await page.locator('.notice-list summary').click(); await page.getByRole('button', { name: 'Rediger ' + notice.title, exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Retained edited notice during outage');
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill('First retained line\nSecond retained line');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20, 24');
  const compose = (...args: string[]) => execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', ...args], { cwd: '..', encoding: 'utf8', timeout: 45000 });
  let writes = 0; page.on('request', request => { if (request.method() === 'POST' && request.url().includes('/notices')) writes++; });
  try {
    compose('stop', 'private-api');
    await page.evaluate(() => { window.dispatchEvent(new Event('pagehide')); window.dispatchEvent(new Event('pageshow')); });
    await expect(page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true })).toBeEnabled();
    await expect(page.getByLabel('Tittel', { exact: true })).toBeHidden(); expect(await beforeUnload(page)).toBe(true); expect(writes).toBe(0);
  } finally { compose('start', '--wait', 'private-api'); }
  await page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true }).click();
  await expect(page.getByLabel('Tittel', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Retained edited notice during outage');
  await expect(page.getByLabel('Detaljert forklaring', { exact: true })).toHaveValue('First retained line\nSecond retained line');
  await expect(page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true })).toHaveValue('20, 24');
  expect((await (await context.request.get(API + '/notices')).json()).notices).toEqual([notice]); expect(writes).toBe(0);
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toHaveText('Avviket er lagret.');
  const saved = (await (await context.request.get(API + '/notices')).json()).notices;
  expect(saved).toHaveLength(1); expect(saved[0].revision).toBe(2); expect(saved[0].title).toBe('Retained edited notice during outage'); expect(writes).toBe(1);
});

async function measureRecovery(page: any, scope: any, control: any, name: string) {
  await control.focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab'); await expect(control).toBeFocused(); await control.scrollIntoViewIfNeeded();
  const metrics = await scope.evaluate((region: Element) => {
    const light = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
    const ratio = (a: string, b: string) => (Math.max(light(a), light(b)) + .05) / (Math.min(light(a), light(b)) + .05);
    const bg = (element: Element): string => { const value = getComputedStyle(element).backgroundColor; return value === 'rgba(0, 0, 0, 0)' || value === 'transparent' ? element.parentElement ? bg(element.parentElement) : 'rgb(255,255,255)' : value; };
    const focused = document.activeElement!, style = getComputedStyle(focused), rect = focused.getBoundingClientRect();
    const visible = [...region.querySelectorAll('p,button,label,h2,h3,h4,input,textarea,select')].filter(node => node.getBoundingClientRect().height > 0);
    const controls = visible.filter(node => ['BUTTON', 'INPUT', 'TEXTAREA', 'SELECT'].includes(node.tagName) && !(node as HTMLInputElement).disabled).map(node => { const s = getComputedStyle(node); return { name: node.textContent, height: node.getBoundingClientRect().height, text: ratio(s.color, bg(node)), boundary: ratio(s.borderTopColor, bg(node.parentElement!)) }; });
    return { overflow: document.documentElement.scrollWidth > innerWidth, text: Math.min(...visible.map(node => ratio(getComputedStyle(node).color, bg(node)))), focus: ratio(style.outlineColor, bg(focused.parentElement!)), focusWidth: parseFloat(style.outlineWidth), focusVisible: focused.matches(':focus-visible'), focusNotObscured: focused.contains(document.elementFromPoint(Math.min(innerWidth - 1, rect.x + rect.width / 2), Math.min(innerHeight - 1, rect.y + rect.height / 2))), controls };
  });
  expect(metrics.overflow).toBe(false); expect(metrics.text).toBeGreaterThanOrEqual(4.5); expect(metrics.focus).toBeGreaterThanOrEqual(3); expect(metrics.focusWidth).toBeGreaterThanOrEqual(2); expect(metrics.focusVisible).toBe(true); expect(metrics.focusNotObscured).toBe(true);
  for (const measured of metrics.controls) { expect(measured.height).toBeGreaterThanOrEqual(58); expect(measured.text).toBeGreaterThanOrEqual(4.5); expect(measured.boundary).toBeGreaterThanOrEqual(3); }
  await page.screenshot({ path: '../docs/evidence/' + name + '.png', fullPage: true }); writeFileSync('../docs/evidence/' + name + '.json', JSON.stringify(metrics, null, 2) + '\n');
}

for (const resource of ['notice', 'outcome']) for (const night of [false, true]) test(`narrow enlarged ${night ? 'Night' : 'Day'} ${resource} recovery long-message controls remain accessible`, async ({ page, context }) => {
  await openedPlan(page, context); await page.setViewportSize({ width: 390, height: 844 });
  await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
  if (night) await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  if (resource === 'notice') {
    await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click(); await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
    await page.getByLabel('Tittel', { exact: true }).fill('Langt lokalt avviksforslag om omkjøring ved et svært langt norsk stedsnavn');
    await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20, 24');
    await page.getByLabel('Detaljert forklaring', { exact: true }).fill('Lokalt forslag under utilgjengelig server. '.repeat(12));
    await page.route('**:8001/notices', route => route.request().method() === 'POST' ? route.abort() : route.continue());
    await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); const recover = page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }); await expect(recover).toBeEnabled();
    await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toContainText('uavklart');
    await measureRecovery(page, page.getByRole('region', { name: 'Avviksvedlikehold', exact: true }), recover, '11-5-crossday-recovery-notice-390-' + (night ? 'night' : 'day'));
  } else {
    await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
    await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
    await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('interrupted');
    await page.route('**:8001/workdays/*/outcome', route => route.abort()); await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click();
    const recover = page.getByRole('button', { name: 'Prøv samme aktivitetsstatus igjen', exact: true }); await expect(recover).toBeEnabled();
    await expect(page.getByText('Uavklart lagringsforsøk for aktivitet 1: Avbrutt.', { exact: false })).toBeVisible();
    await measureRecovery(page, page.getByRole('region', { name: 'Bekreftet plan', exact: true }), recover, '11-6-recovery-outcome-390-' + (night ? 'night' : 'day'));
  }
});

for (const width of [390, 768]) for (const night of [false, true]) test(`enlarged ${width}px ${night ? 'Night' : 'Day'} recovery preserves contrast and keyboard focus without overflow`, async ({ page }) => {
  await draft(page); await page.setViewportSize({ width, height: 1024 });
  await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
  if (night) await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.route('**:8001/drafts', route => route.request().method() === 'POST' ? route.abort() : route.continue());
  await save(page).click(); await expect(status(page)).toContainText('Lagring er uavklart');
  const control = retry(page); await control.focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab'); await expect(control).toBeFocused(); await control.scrollIntoViewIfNeeded();
  const metrics = await control.evaluate((node: HTMLElement) => {
    const light = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
    const ratio = (a: string, b: string) => (Math.max(light(a), light(b)) + .05) / (Math.min(light(a), light(b)) + .05);
    const bg = (element: Element): string => { const value = getComputedStyle(element).backgroundColor; return value === 'rgba(0, 0, 0, 0)' || value === 'transparent' ? element.parentElement ? bg(element.parentElement) : 'rgb(255,255,255)' : value; };
    const s = getComputedStyle(node), rect = node.getBoundingClientRect();
    const controls = [node, ...document.querySelectorAll('button')].filter((button, index, all) => all.indexOf(button) === index && button.getBoundingClientRect().height > 0 && /Kontroller lagringsforsøket/.test(button.textContent ?? '') || button === node).map(button => {
      const style = getComputedStyle(button); return { name: button.textContent, height: button.getBoundingClientRect().height, text: ratio(style.color, bg(button)), boundary: ratio(style.borderTopColor, bg(button.parentElement!)) };
    });
    const status = document.querySelector('.private-drafts p.status')!;
    return { overflow: document.documentElement.scrollWidth > innerWidth, height: rect.height, text: ratio(getComputedStyle(status).color, bg(status)), focus: ratio(s.outlineColor, bg(node.parentElement!)), focusVisible: node.matches(':focus-visible'), outlineWidth: parseFloat(s.outlineWidth), focusNotObscured: node.contains(document.elementFromPoint(Math.min(innerWidth - 1, rect.x + rect.width / 2), Math.min(innerHeight - 1, rect.y + rect.height / 2))), controls };
  });
  expect(metrics.overflow).toBe(false); expect(metrics.text).toBeGreaterThanOrEqual(4.5); expect(metrics.focus).toBeGreaterThanOrEqual(3); expect(metrics.height).toBeGreaterThanOrEqual(58); expect(metrics.focusVisible).toBe(true); expect(metrics.outlineWidth).toBeGreaterThanOrEqual(2); expect(metrics.focusNotObscured).toBe(true);
  for (const measured of metrics.controls) { expect(measured.height).toBeGreaterThanOrEqual(58); expect(measured.text).toBeGreaterThanOrEqual(4.5); expect(measured.boundary).toBeGreaterThanOrEqual(3); }
  const name = '../docs/evidence/11-6-recovery-' + width + '-' + (night ? 'night' : 'day');
  await page.screenshot({ path: name + '.png', fullPage: true }); writeFileSync(name + '.json', JSON.stringify(metrics, null, 2) + '\n');
});
