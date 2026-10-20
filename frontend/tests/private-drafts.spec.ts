import { test, expect, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';

const username = 'synthetic-drafts-browser-' + randomUUID();
const password = randomBytes(24).toString('hex');
function python(program: string) {
  if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project selection required');
  return execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'], { cwd: '..', input: 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n' + program, encoding: 'utf8' });
}
test.beforeAll(() => { python(`from app.auth import provision\nprovision(${JSON.stringify(username)}, ${JSON.stringify(password)})\nwith database() as conn:\n conn.execute('DELETE FROM login_limits')\n`); });
test.beforeEach(() => { python("with database() as conn:\n conn.execute('DELETE FROM login_limits')\n"); });
test.afterAll(() => { python(`with database() as conn:\n owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(username)},)).fetchone()['id']\n conn.execute('DELETE FROM drafts WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM draft_operations WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM draft_deletions WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM sessions WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM accounts WHERE id=%s',(owner,))\n conn.execute('DELETE FROM login_limits')\n`); });
async function login(page: Page) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(username);
  await page.getByLabel('Passord', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
}
async function fill(page: Page) {
  await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-10-24');
  await page.getByLabel('Vognløp', { exact: true }).fill('0007');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('Bus-0012');
  await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
  await page.getByLabel('Opprinnelig kode').fill('Unknown/42');
  await page.getByLabel('Startdato', { exact: true }).fill('2026-10-25');
  await page.getByLabel('Starttid', { exact: true }).fill('00:00');
  await page.getByLabel('Sluttdato', { exact: true }).fill('2026-10-25');
  await page.getByLabel('Sluttid', { exact: true }).fill('02:30');
  await page.getByLabel('Slutt: forekomst', { exact: true }).selectOption({ label: 'Andre forekomst' });
  await page.getByLabel('Opprinnelig startklokke').fill('24:00');
  await page.getByLabel('Opprinnelig sluttklokke').fill('26:30');
  await page.getByLabel('Kilde / manuell rettelse').fill('Manuell rettelse, ukjent sted.');
}
const status = (page: Page) => page.getByRole('region', { name: 'Private utkast' }).getByRole('status');

for (const width of [768, 1440]) test(`keyboard save and reopen midnight facts at ${width}px`, async ({ page }) => {
  await page.setViewportSize({ width, height: 1100 });
  await login(page); await fill(page);
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).focus();
  await page.keyboard.press('Enter');
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await expect(page.getByRole('heading', { name: 'Rediger utkast' })).toBeFocused();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  expect(await page.evaluate(async () => [localStorage.length, sessionStorage.length, (await indexedDB.databases()).length])).toEqual([0, 0, 0]);
  await page.screenshot({ path: `../Docs/evidence/9-4-${width}.png`, fullPage: true });
  await page.reload();
  await page.getByRole('button', { name: /Åpne 2026-10-24/ }).first().click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('0007');
  await expect(page.getByLabel('Opprinnelig sluttklokke')).toHaveValue('26:30');
  await expect(page.getByLabel('Sluttdato', { exact: true })).toHaveValue('2026-10-25');
  await expect(page.getByLabel('Sluttid', { exact: true })).toHaveValue('02:30');
  await page.getByLabel('Vognløp', { exact: true }).fill('local-unsaved');
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('local-unsaved');
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('button', { name: 'Nytt utkast', exact: true }).click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('local-unsaved');
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
});

test('lost acknowledgement, authorized lookup and HTML failure retain original operation', async ({ page }) => {
  await login(page); await fill(page);
  let original = '';
  let originalTarget = '';
  let accepted: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    original = route.request().postData()!; originalTarget = route.request().url();
    accepted = await (await route.fetch()).json(); await route.abort();
  });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Lagring er uavklart.');
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('0007');
  await expect(page.getByRole('button', { name: 'Tilbakestill utkast' })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Nytt utkast', exact: true })).toBeDisabled();
  await page.unroute('**:8001/drafts');
  await page.route('**:8001/auth/session', route => route.abort());
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByRole('button', { name: 'Kontroller tilgang igjen' })).toBeEnabled();
  await expect(page.getByLabel('Vognløp', { exact: true })).toBeHidden();
  await page.unroute('**:8001/auth/session');
  await page.getByRole('button', { name: 'Kontroller tilgang igjen' }).click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('0007');
  let committedRetry = '', committedTarget = '';
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    committedRetry = route.request().postData()!; committedTarget = route.request().url();
    const response = await route.fetch(); expect(await response.json()).toEqual(accepted);
    await route.fulfill({ response });
  });
  await page.getByRole('button', { name: 'Prøv samme lagringsforsøk igjen' }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  expect(committedTarget).toBe(originalTarget);
  expect(committedRetry).toBe(original);
  const owned = await (await page.request.get('http://127.0.0.1:8001/drafts')).json();
  expect(owned.drafts.filter((draft: any) => draft.id === accepted.id)).toEqual([expect.objectContaining({ id: accepted.id, revision: 1 })]);
  await page.unroute('**:8001/drafts');
  await page.getByLabel('Vognløp', { exact: true }).fill('new');
  await page.route('**:8001/drafts/*', route => route.request().method() === 'POST' ? route.fulfill({ contentType: 'text/html', body: '<html>login</html>' }) : route.continue());
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Lagring er uavklart.');
  await page.unroute('**:8001/drafts/*');
  let retry = '';
  page.on('request', request => { if (request.method() === 'POST' && new URL(request.url()).pathname.startsWith('/drafts/')) retry = request.postData()!; });
  await page.getByRole('button', { name: 'Prøv samme lagringsforsøk igjen' }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 2.');
  expect(JSON.parse(original).draft.vehicle_duty).toBe('0007');
  expect(JSON.parse(retry).draft.vehicle_duty).toBe('new');
});

test('stale revision preserves local input and offers saved comparison', async ({ page, context }) => {
  await login(page); await fill(page);
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  const other = await context.newPage();
  await other.goto('/private'); await other.getByRole('button', { name: /Åpne 2026-10-24/ }).first().click();
  await other.getByLabel('Vognløp', { exact: true }).fill('remote');
  await other.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(other)).toHaveText('Lagret. Versjon 2.');
  await page.bringToFront();
  await page.getByLabel('Vognløp', { exact: true }).fill('local');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Konflikt.');
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('local');
  await expect(page.getByRole('region', { name: 'Sammenlign versjoner' })).toContainText('remote');
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Last inn lagret versjon' }).click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('remote');
  await other.close();
});

test('JSON with an invalid acknowledgement stays unresolved until authorized lookup', async ({ page }) => {
  await login(page); await fill(page);
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    const response = await route.fetch(); const body = await response.json();
    await route.fulfill({ json: { ...body, revision: 999 } });
  });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Lagring er uavklart.');
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('0007');
  await page.unroute('**:8001/drafts');
  await page.getByRole('button', { name: 'Kontroller lagringsforsøket' }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
});

test('expired authorization clears unsaved private fields on revalidation', async ({ page }) => {
  await login(page); await fill(page);
  python(`with database() as conn:\n conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner IN (SELECT id FROM accounts WHERE username=%s)", (${JSON.stringify(username)},))\n`);
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveCount(0);
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0]);
});

test('413 keeps fields editable and a corrected draft can be saved', async ({ page }) => {
  await login(page); await fill(page);
  await page.route('**:8001/drafts', route => route.request().method() === 'POST' ? route.fulfill({ status: 413, json: { detail: 'Too large' } }) : route.continue());
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Utkastet er for stort. Forkort tekst eller fjern aktiviteter');
  await expect(page.getByLabel('Vognløp', { exact: true })).toBeEnabled();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('0007');
  await expect(page.getByRole('button', { name: 'Prøv samme lagringsforsøk igjen' })).toHaveCount(0);
  await page.getByLabel('Vognløp', { exact: true }).fill('corrected');
  await page.unroute('**:8001/drafts');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
});

test('UTF-8 size preflight preserves valid Unicode input without issuing a save', async ({ page }) => {
  await login(page);
  const id = randomUUID(), now = Date.now();
  const rows = Array.from({ length: 200 }, () => ({ id: randomUUID(), type: null, raw_code: null, start: null, end: null, source_start: null, source_end: null, from_place: null, to_place: null, trip: null, line: null, direction: null, uncertainty: '界'.repeat(1000), provenance: '界'.repeat(1000) }));
  const record = { id, created_at: new Date(now).toISOString(), expires_at: new Date(now + 7 * 86400000).toISOString(), revision: 1, draft: { service_date: null, vehicle_duty: null, realtime_duty: null, physical_bus: null, activities: rows } };
  await page.route('**:8001/drafts', route => route.fulfill({ json: { drafts: [{ ...record, service_date: null }] } }));
  await page.route('**:8001/drafts/' + id, route => route.fulfill({ json: record }));
  await page.getByRole('button', { name: 'Oppdater listen' }).click();
  await page.getByRole('button', { name: 'Åpne ukjent tjenestedato · versjon 1' }).click();
  let issued = false;
  page.on('request', request => { if (request.url().endsWith('/draft-operations') && request.method() === 'POST') issued = true; });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Utkastet er for stort.');
  await expect(page.getByLabel('Usikkerhet / ukjente fakta').first()).toBeEnabled();
  await expect(page.getByLabel('Usikkerhet / ukjente fakta').first()).toHaveValue('界'.repeat(1000));
  expect(issued).toBe(false);
});

test('slightly future server creation timestamps remain valid acknowledgements', async ({ page }) => {
  await login(page); await fill(page);
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    const response = await route.fetch(), body = await response.json();
    const serverTime = Date.now() + 60000;
    await route.fulfill({ json: { ...body, created_at: new Date(serverTime).toISOString(), expires_at: new Date(serverTime + 7 * 86400000).toISOString() } });
  });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
});

test('supported historical Oslo offset saves and reopens unchanged', async ({ page }) => {
  await login(page); await fill(page);
  await page.getByLabel('Startdato', { exact: true }).fill('1894-01-01');
  await page.getByLabel('Starttid', { exact: true }).fill('12:00');
  await page.getByLabel('Sluttdato', { exact: true }).fill('1894-01-01');
  await page.getByLabel('Sluttid', { exact: true }).fill('12:00');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.reload();
  await page.getByRole('button', { name: /Åpne 2026-10-24/ }).first().click();
  await expect(page.getByLabel('Startdato', { exact: true })).toHaveValue('1894-01-01');
  await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('12:00');
});

test('reorder and remove preserve ordered identities with their facts after reopen', async ({ page }) => {
  await login(page); await fill(page);
  await page.getByLabel('Opprinnelig kode').fill('A');
  for (const code of ['B', 'C']) {
    await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
    await page.getByLabel('Opprinnelig kode').last().fill(code);
  }
  const firstResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const original = await (await firstResponse).json();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.getByRole('button', { name: 'Flytt opp', exact: true }).nth(2).click();
  await page.getByRole('button', { name: 'Fjern aktivitet 1', exact: true }).focus();
  page.once('dialog', dialog => dialog.accept());
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Rediger utkast' })).toBeFocused();
  const secondResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts/' + original.id);
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const expected = [original.draft.activities[2], original.draft.activities[1]];
  expect((await (await secondResponse).json()).draft.activities).toEqual(expected);
  await expect(status(page)).toHaveText('Lagret. Versjon 2.');
  await page.reload();
  const reopened = page.waitForResponse(response => response.request().method() === 'GET' && new URL(response.url()).pathname === '/drafts/' + original.id);
  await page.getByRole('button', { name: /Åpne 2026-10-24 · versjon 2/ }).first().click();
  expect((await (await reopened).json()).draft.activities).toEqual(expected);
  await expect(page.getByLabel('Opprinnelig kode').nth(0)).toHaveValue('C');
  await expect(page.getByLabel('Opprinnelig kode').nth(1)).toHaveValue('B');
});

test('bus, derived suffix, clear and confirmed reset preserve the intended facts', async ({ page }) => {
  await login(page); await fill(page);
  await expect(page.getByText('Sanntidsverdi: 007 (avledet fra vognløp).', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Tøm vognløp' }).click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-0012');
  await expect(page.getByLabel('Opprinnelig kode')).toHaveValue('Unknown/42');
  await expect(page.getByText('Sanntidsverdi: ukjent (avledet fra vognløp).', { exact: true })).toBeVisible();
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('button', { name: 'Tilbakestill utkast' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-0012');
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Tilbakestill utkast' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
  await expect(page.getByLabel('Opprinnelig kode')).toHaveCount(0);
  await fill(page);
  await page.getByLabel('Vognløp', { exact: true }).fill('Duty-0009');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('unsaved-bus');
  await page.getByRole('button', { name: 'Tøm vognløp' }).click();
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('button', { name: 'Forkast endringer' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('unsaved-bus');
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Forkast endringer' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-0012');
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('Duty-0009');
  await expect(page.getByText('Sanntidsverdi: 009 (avledet fra vognløp).', { exact: true })).toBeVisible();
  await page.getByLabel('Buss/vogn', { exact: true }).fill('Bus-0008');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 2.');
  await page.reload();
  await page.getByRole('button', { name: /Åpne 2026-10-24 · versjon 2/ }).first().click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-0008');
});

test('confirmed deletion retains its identity through a committed lost reply', async ({ page }) => {
  await login(page); await fill(page);
  let saveBody = '', saved: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    saveBody = route.request().postData()!; const response = await route.fetch(); saved = await response.json(); await route.fulfill({ response });
  });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('button', { name: 'Slett utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  let original = '', originalTarget = '';
  await page.route('**:8001/drafts/*/delete', async route => { original = route.request().postData()!; originalTarget = route.request().url(); await route.fetch(); await route.abort(); });
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Slett utkast', exact: true }).click();
  await expect(status(page)).toContainText('Sletting er ikke bekreftet.');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Nytt utkast', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Forkast endringer' })).toBeDisabled();
  await page.unroute('**:8001/drafts/*/delete');
  let retry = '', retryTarget = '';
  await page.route('**:8001/drafts/*/delete', async route => { retry = route.request().postData()!; retryTarget = route.request().url(); await route.continue(); });
  await page.getByRole('button', { name: 'Prøv samme slettingsforsøk igjen' }).click();
  await expect(status(page)).toHaveText('Utkastet er slettet.');
  expect(retry).toBe(original); expect(retryTarget).toBe(originalTarget);
  expect((await page.request.get('http://127.0.0.1:8001/drafts/' + saved.id)).status()).toBe(404);
  const proof = await (await page.request.get('http://127.0.0.1:8001/auth/csrf')).json();
  expect((await page.request.post('http://127.0.0.1:8001/drafts', { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data: JSON.parse(saveBody) })).status()).toBe(404);
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
  const owned = await (await page.request.get('http://127.0.0.1:8001/drafts')).json();
  expect(owned.drafts.some((draft: any) => draft.id === saved.id)).toBe(false);
});

for (const committed of [false, true]) test(`deletion lookup settles only an accepted deletion (${committed})`, async ({ page }) => {
  await login(page); await fill(page);
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.route('**:8001/drafts/*/delete', async route => { if (committed) await route.fetch(); await route.abort(); });
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Slett utkast', exact: true }).click();
  await expect(status(page)).toContainText('Sletting er ikke bekreftet.');
  await page.getByRole('button', { name: 'Kontroller slettingen' }).click();
  if (committed) { await expect(status(page)).toHaveText('Utkastet er slettet.'); return; }
  await expect(status(page)).toContainText('Sletting er ikke bekreftet.');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-0012');
  await page.unroute('**:8001/drafts/*/delete');
  await page.getByRole('button', { name: 'Prøv samme slettingsforsøk igjen' }).click();
  await expect(status(page)).toHaveText('Utkastet er slettet.');
});

test('a delayed earlier list cannot replace the post-save revision list', async ({ page }) => {
  await login(page); await fill(page);
  await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-11-01');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const waiting = new Promise<void>(resolve => { entered = resolve; });
  let earlier = true;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'GET' || !earlier) { await route.continue(); return; }
    earlier = false; const response = await route.fetch(); entered(); await gate; await route.fulfill({ response });
  });
  try {
    await page.getByRole('button', { name: 'Oppdater listen' }).click(); await waiting;
    await page.getByLabel('Buss/vogn', { exact: true }).fill('newer-bus');
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    await expect(status(page)).toHaveText('Lagret. Versjon 2.');
    await expect(page.getByRole('button', { name: 'Åpne 2026-11-01 · versjon 2', exact: true })).toBeVisible();
    const late = page.waitForResponse(response => response.request().method() === 'GET' && new URL(response.url()).pathname === '/drafts');
    release(); await (await late).finished();
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve(null)))));
    await expect(page.getByRole('button', { name: 'Åpne 2026-11-01 · versjon 2', exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Åpne 2026-11-01 · versjon 1', exact: true })).toHaveCount(0);
  } finally { release(); }
});

for (const invalid of [null, { id: randomUUID(), revision: 1, expires_at: 'invalid', service_date: '2026-11-01' }]) test(`malformed summary remains recoverable (${invalid === null ? 'null' : 'invalid'})`, async ({ page }) => {
  await login(page); await fill(page);
  await page.route('**:8001/drafts', route => route.fulfill({ json: { drafts: [invalid] } }));
  await page.getByRole('button', { name: 'Oppdater listen' }).click();
  await expect(status(page)).toContainText('Listen kunne ikke lastes.');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-0012');
  await page.unroute('**:8001/drafts');
  await page.getByRole('button', { name: 'Oppdater listen' }).click();
  await expect(status(page)).toHaveText('Listen er oppdatert.');
  await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeEnabled();
});

test('expired deletion is unconfirmed and releases the form for a new draft', async ({ page }) => {
  await login(page); await fill(page);
  const response = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const saved = await (await response).json();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  python(`with database() as conn:\n conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (${JSON.stringify(saved.id)},))\n`);
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Slett utkast', exact: true }).click();
  await expect(status(page)).toContainText('Sletting kunne ikke bekreftes');
  await expect(status(page)).toContainText('utløpt');
  await expect(page.getByRole('button', { name: 'Prøv samme slettingsforsøk igjen' })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Nytt utkast', exact: true })).toBeEnabled();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
  await page.getByRole('button', { name: 'Nytt utkast', exact: true }).click();
  await page.getByLabel('Buss/vogn', { exact: true }).fill('replacement');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
});

test('backend-valid emoji text uses code-point limits through entry, save and reopen', async ({ page }) => {
  await login(page); await fill(page);
  const bus = '🙂'.repeat(100), note = '🙂'.repeat(1000);
  await page.getByLabel('Buss/vogn', { exact: true }).fill(bus);
  await page.getByLabel('Kilde / manuell rettelse').fill(note);
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue(bus);
  await expect(page.getByLabel('Kilde / manuell rettelse')).toHaveValue(note);
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.reload();
  await page.getByRole('button', { name: /Åpne 2026-10-24/ }).first().click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue(bus);
  await expect(page.getByLabel('Kilde / manuell rettelse')).toHaveValue(note);
});

test('stale deletion releases its lock and requires confirmed saved-version replacement', async ({ page, context }) => {
  await login(page); await fill(page);
  await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-11-02');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('local-unsaved');
  const other = await context.newPage();
  await other.goto('/private');
  await other.getByRole('button', { name: 'Åpne 2026-11-02 · versjon 1', exact: true }).click();
  await other.getByLabel('Buss/vogn', { exact: true }).fill('remote-newer');
  await other.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(other)).toHaveText('Lagret. Versjon 2.');
  await page.bringToFront();
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Slett utkast', exact: true }).click();
  await expect(status(page)).toContainText('Konflikt. Utkastet er endret og er ikke slettet.');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toBeEnabled();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('local-unsaved');
  await expect(page.getByRole('button', { name: 'Prøv samme slettingsforsøk igjen' })).toHaveCount(0);
  await expect(page.getByRole('region', { name: 'Sammenlign versjoner' })).toContainText('remote-newer');
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('button', { name: 'Last inn lagret versjon' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('local-unsaved');
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Last inn lagret versjon' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('remote-newer');
  await other.close();
});

test.describe('friendly Oslo time entry', () => {
  test.use({ timezoneId: 'America/New_York' });

  test('service defaults and explicit next day preserve entered dates when service date changes', async ({ page }) => {
    await login(page);
    await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-07-15');
    await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
    await expect(page.getByLabel('Startdato', { exact: true })).toHaveValue('2026-07-15');
    await expect(page.getByLabel('Sluttdato', { exact: true })).toHaveValue('2026-07-15');
    await page.getByLabel('Starttid', { exact: true }).fill('23:50');
    await page.getByLabel('Sluttid', { exact: true }).fill('00:10');
    await page.getByRole('button', { name: 'Slutt: neste dag' }).click();
    await expect(page.getByLabel('Sluttdato', { exact: true })).toHaveValue('2026-07-16');
    await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-07-20');
    await expect(page.getByLabel('Startdato', { exact: true })).toHaveValue('2026-07-15');
    await expect(page.getByLabel('Sluttdato', { exact: true })).toHaveValue('2026-07-16');
    const result = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    const saved = await (await result).json();
    expect(saved.draft.activities[0].start).toBe('2026-07-15T23:50+02:00');
    expect(saved.draft.activities[0].end).toBe('2026-07-16T00:10+02:00');
    await expect(status(page)).toHaveText('Lagret. Versjon 1.');
    await page.reload();
    await page.getByRole('button', { name: 'Åpne 2026-07-20 · versjon 1', exact: true }).click();
    await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('23:50');
    await expect(page.getByLabel('Sluttdato', { exact: true })).toHaveValue('2026-07-16');
  });

  test('incomplete and spring-gap input survives while both autumn occurrences require a choice', async ({ page }) => {
    await login(page);
    await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-03-29');
    await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
    await page.getByLabel('Starttid', { exact: true }).fill('02:30');
    await expect(page.getByText('Dette klokkeslettet finnes ikke i Oslo', { exact: false })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeDisabled();
    await page.getByLabel('Startdato', { exact: true }).fill('');
    await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('02:30');
    await page.evaluate(() => {
      Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
      Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
    });
    await expect(page.getByLabel('Startdato', { exact: true })).toHaveValue('');
    await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('02:30');
    await page.getByLabel('Startdato', { exact: true }).fill('2026-10-25');
    await expect(page.getByLabel('Start: forekomst', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeDisabled();
    await page.getByLabel('Start: forekomst', { exact: true }).selectOption({ label: 'Første forekomst' });
    await page.getByLabel('Sluttdato', { exact: true }).fill('2026-10-25');
    await page.getByLabel('Sluttid', { exact: true }).fill('02:30');
    await page.getByLabel('Slutt: forekomst', { exact: true }).selectOption({ label: 'Andre forekomst' });
    await page.evaluate(() => {
      Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
      Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
    });
    await expect(page.getByLabel('Start: forekomst', { exact: true })).toHaveValue('2026-10-25T02:30+02:00');
    await expect(page.getByLabel('Slutt: forekomst', { exact: true })).toHaveValue('2026-10-25T02:30+01:00');
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeEnabled();
    const result = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    const saved = await (await result).json();
    expect(saved.draft.activities[0].start).toBe('2026-10-25T02:30+02:00');
    expect(saved.draft.activities[0].end).toBe('2026-10-25T02:30+01:00');
    await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  });

  test('unavailable and stale resolution retains input and saves only the latest clock', async ({ page }) => {
    await login(page);
    await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-01-15');
    await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
    await page.route('**:8001/draft-times/resolve', route => route.abort());
    await page.getByLabel('Starttid', { exact: true }).fill('10:00');
    await expect(page.getByText('Tidspunktet kunne ikke kontrolleres.', { exact: false })).toBeVisible();
    await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('10:00');
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeDisabled();
    await page.unroute('**:8001/draft-times/resolve');
    let release!: () => void, entered!: () => void;
    const gate = new Promise<void>(resolve => { release = resolve; });
    const waiting = new Promise<void>(resolve => { entered = resolve; });
    let first = true;
    await page.route('**:8001/draft-times/resolve', async route => {
      if (!first) { await route.continue(); return; }
      first = false; const response = await route.fetch(); entered(); await gate; await route.fulfill({ response });
    });
    try {
      await page.getByRole('button', { name: 'Kontroller starttid igjen' }).click(); await waiting;
      await page.getByLabel('Starttid', { exact: true }).fill('11:00');
      release();
      const result = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
      await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
      expect((await (await result).json()).draft.activities[0].start).toBe('2026-01-15T11:00+01:00');
      await expect(status(page)).toHaveText('Lagret. Versjon 1.');
    } finally { release(); }
  });

  test('existing explicit instants and source clocks remain identical during unrelated edits', async ({ page }) => {
    await login(page);
    const proof = await (await page.request.get('http://127.0.0.1:8001/auth/csrf')).json();
    const headers = { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token };
    const operation = await (await page.request.post('http://127.0.0.1:8001/draft-operations', { headers, data: {} })).json();
    const original = await (await page.request.post('http://127.0.0.1:8001/drafts', { headers, data: { operation_id: operation.operation_id, expected_revision: 0, draft: { service_date: '2026-11-03', activities: [{ id: randomUUID(), start: '2026-10-25T02:30:15+01:00', end: '2026-10-25T02:45:16+01:00', source_start: '26:30' }] } } })).json();
    await page.getByRole('button', { name: 'Oppdater listen' }).click();
    await page.getByRole('button', { name: 'Åpne 2026-11-03 · versjon 1', exact: true }).click();
    await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('02:30:15');
    await expect(page.getByLabel('Startdato', { exact: true })).toHaveValue('2026-10-25');
    await page.getByLabel('Buss/vogn', { exact: true }).fill('manual-bus');
    const result = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts/' + original.id);
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    const updated = await (await result).json();
    expect(updated.draft.activities).toEqual(original.draft.activities);
    expect(updated.expires_at).toBe(original.expires_at);
  });

  test('clearing saved, incomplete and gap times saves null without changing other facts', async ({ page }) => {
    await login(page); await fill(page);
    const initialResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    const original = await (await initialResponse).json();
    await expect(status(page)).toHaveText('Lagret. Versjon 1.');
    await page.getByRole('button', { name: 'Start: tøm tidspunkt', exact: true }).click();
    const clearedResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts/' + original.id);
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    const cleared = await (await clearedResponse).json();
    expect(cleared.draft.activities[0]).toEqual({ ...original.draft.activities[0], start: null });
    await expect(status(page)).toHaveText('Lagret. Versjon 2.');
    await page.reload();
    await page.getByRole('button', { name: /Åpne 2026-10-24 · versjon 2/ }).first().click();
    await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('');
    await expect(page.getByLabel('Sluttid', { exact: true })).toHaveValue('02:30');
    await expect(page.getByLabel('Opprinnelig startklokke')).toHaveValue('24:00');
    await page.getByLabel('Startdato', { exact: true }).fill('2026-03-29');
    await page.getByLabel('Starttid', { exact: true }).fill('02:30');
    await expect(page.getByText('Dette klokkeslettet finnes ikke i Oslo', { exact: false })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeDisabled();
    await page.getByRole('button', { name: 'Start: tøm tidspunkt', exact: true }).click();
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeEnabled();
    await page.getByLabel('Startdato', { exact: true }).fill('');
    await page.getByLabel('Starttid', { exact: true }).fill('10:00');
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeDisabled();
    await page.getByRole('button', { name: 'Start: tøm tidspunkt', exact: true }).click();
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    await expect(status(page)).toHaveText('Lagret. Versjon 3.');
  });
});

for (const purged of [false, true]) test(`terminal lost-save lookup releases only an explicitly empty recovery (${purged})`, async ({ page }) => {
  await login(page); await fill(page);
  let accepted: any, originalBody: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    originalBody = route.request().postDataJSON(); accepted = await (await route.fetch()).json(); await route.abort();
  });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Lagring er uavklart.');
  await page.unroute('**:8001/drafts');
  python(`with database() as conn:\n conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (${JSON.stringify(accepted.id)},))\n conn.execute('UPDATE draft_operations SET expires_at=(SELECT expires_at FROM drafts WHERE id=%s) WHERE draft_id=%s', (${JSON.stringify(accepted.id)},${JSON.stringify(accepted.id)}))\n${purged ? 'from app.private_storage import cleanup\ncleanup()\n' : ''}`);
  await page.getByRole('button', { name: 'Kontroller lagringsforsøket' }).click();
  await expect(status(page)).toContainText('Lagring er ikke bekreftet.');
  await expect(status(page)).toContainText('kan ikke sendes på nytt');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-0012');
  await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('00:00');
  await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Prøv samme lagringsforsøk igjen' })).toHaveCount(0);
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: purged ? 'Nytt utkast' : 'Tilbakestill utkast', exact: true }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
  await expect(page.getByLabel('Starttid', { exact: true })).toHaveCount(0);
  const freshResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const fresh = await (await freshResponse).json();
  expect(fresh.id).not.toBe(accepted.id); expect(fresh.draft.activities).toEqual([]);
  expect(fresh.draft.physical_bus).toBeNull();
  const proof = await (await page.request.get('http://127.0.0.1:8001/auth/csrf')).json();
  expect((await page.request.post('http://127.0.0.1:8001/drafts', { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data: originalBody })).status()).toBe(purged ? 404 : 410);
});

test('negative intervals are explained before sending and generic validation uses friendly time guidance', async ({ page }) => {
  await login(page);
  await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-07-15');
  await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
  await page.getByLabel('Starttid', { exact: true }).fill('23:00');
  await page.getByLabel('Sluttid', { exact: true }).fill('01:00');
  let operations = 0;
  page.on('request', request => { if (request.url().endsWith('/draft-operations') && request.method() === 'POST') operations++; });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Aktivitet 1: Slutt er før start.');
  await expect(status(page)).toContainText('Slutt: neste dag'); expect(operations).toBe(0);
  await page.getByRole('button', { name: 'Slutt: neste dag', exact: true }).click();
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('changed');
  await page.route('**:8001/drafts/*', route => route.request().method() === 'POST' ? route.fulfill({ status: 422, json: { detail: 'Invalid synthetic value' } }) : route.continue());
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toContainText('Velg riktig kalenderdag eller neste dag');
  await expect(status(page)).not.toContainText('offset');
});

test('activity removal cancellation preserves unresolved raw input and canonical facts', async ({ page }) => {
  await login(page); await fill(page);
  const firstResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const original = await (await firstResponse).json();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.getByLabel('Sluttdato', { exact: true }).fill('');
  await page.getByLabel('Kilde / manuell rettelse').fill('unsaved provenance');
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('button', { name: 'Fjern aktivitet 1', exact: true }).click();
  await expect(page.getByLabel('Sluttdato', { exact: true })).toHaveValue('');
  await expect(page.getByLabel('Sluttid', { exact: true })).toHaveValue('02:30');
  await expect(page.getByLabel('Starttid', { exact: true })).toHaveValue('00:00');
  await expect(page.getByLabel('Kilde / manuell rettelse')).toHaveValue('unsaved provenance');
  await page.getByLabel('Sluttdato', { exact: true }).fill('2026-10-25');
  await page.getByLabel('Slutt: forekomst', { exact: true }).selectOption({ label: 'Andre forekomst' });
  const updateResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts/' + original.id);
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const updated = await (await updateResponse).json();
  expect(updated.draft.activities[0]).toEqual({ ...original.draft.activities[0], provenance: 'unsaved provenance' });
  await expect(status(page)).toHaveText('Lagret. Versjon 2.');
  await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
  let dialogs = 0;
  const rejectDialog = async (dialog: any) => { dialogs++; await dialog.dismiss(); };
  page.on('dialog', rejectDialog);
  await page.getByRole('button', { name: 'Fjern aktivitet 2', exact: true }).click();
  page.off('dialog', rejectDialog);
  expect(dialogs).toBe(0);
  await expect(page.getByLabel('Starttid', { exact: true })).toHaveCount(1);
});

test('initial failed lists and later failures never claim an acknowledged empty list', async ({ page }) => {
  await page.route('**:8001/drafts', route => route.abort());
  await login(page);
  await expect(page.getByText('Listen er utilgjengelig.', { exact: false })).toBeVisible();
  await expect(page.getByText('Ingen lagrede utkast.', { exact: true })).toHaveCount(0);
  await page.getByLabel('Buss/vogn', { exact: true }).fill('retained');
  await page.unroute('**:8001/drafts');
  await page.route('**:8001/drafts', route => route.fulfill({ json: { drafts: [] } }));
  await page.getByRole('button', { name: 'Oppdater listen' }).click();
  await expect(page.getByText('Ingen lagrede utkast.', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('retained');
  await page.unroute('**:8001/drafts');
  await page.getByLabel('Tjenestedato', { exact: true }).fill('2026-11-04');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(status(page)).toHaveText('Lagret. Versjon 1.');
  await page.route('**:8001/drafts', route => route.abort());
  await page.getByRole('button', { name: 'Oppdater listen' }).click();
  await expect(page.getByText('Listen er utilgjengelig.', { exact: false })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Åpne 2026-11-04 · versjon 1', exact: true })).toBeVisible();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('retained');
  await expect(page.getByText('Ingen lagrede utkast.', { exact: true })).toHaveCount(0);
});
