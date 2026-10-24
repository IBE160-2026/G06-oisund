import { preparation, editor, planScreen } from './private-screen-helpers';
import { test, expect, type Page, type BrowserContext } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';

const account = { username: 'synthetic-bus-' + randomUUID(), password: randomBytes(24).toString('hex') };
const API = 'http://127.0.0.1:8001';
function python(program: string) {
  if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project selection required');
  return execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'], { cwd: '..', encoding: 'utf8', input: 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n' + program });
}
test.beforeAll(() => python(`from app.auth import provision\nprovision(${JSON.stringify(account.username)}, ${JSON.stringify(account.password)})\n`));
test.beforeEach(() => python(`with database() as conn:
 owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(account.username)},)).fetchone()['id']
 for table in ['workday_deletions','workday_operations','workdays','drafts','draft_operations','draft_deletions']:
  conn.execute('DELETE FROM '+table+' WHERE owner=%s',(owner,))
 conn.execute('DELETE FROM login_limits')
`));
test.afterAll(() => python(`with database() as conn:
 owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(account.username)},)).fetchone()['id']
 for table in ['workday_deletions','workday_operations','workdays','drafts','draft_operations','draft_deletions','sessions']:
  conn.execute('DELETE FROM '+table+' WHERE owner=%s',(owner,))
 conn.execute('DELETE FROM accounts WHERE id=%s',(owner,))
 conn.execute('DELETE FROM login_limits')
`));
async function login(page: Page) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
}
async function post(context: BrowserContext, path: string, body: object) {
  const proof = await (await context.request.get(API + '/auth/csrf')).json();
  const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data: body });
  expect(response.status()).toBe(200); return response.json();
}
async function seed(page: Page, context: BrowserContext, kind: string | null = null) {
  const operation = await post(context, '/draft-operations', {});
  const draft = await post(context, '/drafts', { operation_id: operation.operation_id, expected_revision: 0, draft: { service_date: '2031-01-02', vehicle_duty: 'CAR - 1', physical_bus: null, activities: [{ id: randomUUID(), type: kind, raw_code: 'Fictional code', start: '2031-01-02T10:00+01:00', end: '2031-01-02T11:00+01:00', from_place: 'Fiktivt langt oppmøtested med navn som skal brytes og være lesbart i smale vinduer', to_place: null, uncertainty: 'Fiktiv ukjent opplysning' }] } });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).first().click();
  await expect(page.getByRole('button', { name: 'Gjennomgå lagret utkast' })).toBeEnabled();
  return draft;
}
async function review(page: Page) {
  await editor(page); await page.getByRole('button', { name: 'Gjennomgå lagret utkast' }).click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
}
async function decide(page: Page) {
  const region = page.getByRole('region', { name: 'Gjennomgått versjon' });
  for (const select of await region.getByRole('combobox').all()) await select.selectOption('manual');
  for (const box of await region.getByRole('checkbox').all()) await box.check();
}
async function confirmSaved(context: BrowserContext, draft: any) {
  const reviewed = await post(context, '/workday-reviews', { draft_id: draft.id, expected_revision: draft.revision });
  return post(context, '/drafts/' + draft.id + '/confirm', { operation_id: reviewed.operation_id, expected_revision: draft.revision, acknowledgements: reviewed.unknowns.filter((item: any) => !reviewed.classifications_required.includes(item.id.split(':')[0])).map((item: any) => item.id), classifications: Object.fromEntries(reviewed.classifications_required.map((id: string) => [id, 'manual'])) });
}

async function openedPlan(page: Page, context: BrowserContext) {
  await login(page); const draft = await seed(page, context, 'trip');
  const plan = await confirmSaved(context, draft);
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
  return { draft, plan };
}

const busInput = (page: Page) => page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true });
const busStatus = (page: Page) => page.getByRole('status', { name: 'Bussstatus' });
const saveBus = (page: Page) => page.getByRole('button', { name: 'Lagre fysisk buss', exact: true });

test('feedback clear current bus is an unsaved proposal with cancel save and reopen', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  await busInput(page).fill(' 000x / 090 '); await saveBus(page).click();
  await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
  const path = API + '/workdays/' + plan.id + '/physical-bus';
  const before = await (await context.request.get(path)).json();
  await page.getByRole('button', { name: 'Tøm fysisk buss', exact: true }).click();
  await expect(busInput(page)).toHaveValue('');
  expect(await (await context.request.get(path)).json()).toEqual(before);
  await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await expect(busInput(page)).toHaveValue(' 000x / 090 ');
  await page.getByRole('button', { name: 'Tøm fysisk buss', exact: true }).click();
  await saveBus(page).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
  const cleared = await (await context.request.get(path)).json();
  expect(cleared.physical_bus).toBeNull(); expect(cleared.expires_at).toBe(plan.expires_at);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(busInput(page)).toHaveValue('');
});

for (const width of [768, 1440]) for (const night of [false, true]) test(`bus keyboard correction clearing reopening ${width} ${night ? 'Night' : 'Day'}`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: 1000 });
  const { plan, draft } = await openedPlan(page, context);
  if (night) await page.getByRole('button', { name: 'Nattmodus' }).click();
  await expect(busStatus(page)).toContainText('Ukjent');
  await busInput(page).focus(); await page.keyboard.type(' 0006 / 090 ');
  await expect(busInput(page)).toBeFocused();
  await page.getByRole('region', { name: 'Fysisk buss', exact: true }).screenshot({ path: `../docs/evidence/11-2-regression-10-4-bus-unsaved-${width}-${night ? 'night' : 'day'}.png` });
  await expect(page.getByRole('button', { name: 'Slett bekreftet plan', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeDisabled();
  await saveBus(page).focus(); await page.keyboard.press('Enter');
  await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
  await expect(busInput(page)).toBeFocused();
  await busInput(page).fill('korrigert');
  await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await expect(busInput(page)).toHaveValue(' 0006 / 090 '); await expect(busInput(page)).toBeFocused();
  const region = page.getByRole('region', { name: 'Fysisk buss', exact: true });
  await region.screenshot({ path: `../docs/evidence/11-2-regression-10-4-bus-${width}-${night ? 'night' : 'day'}.png` });
  const contrast = await region.evaluate(element => {
    function rgb(value: string) { return value.match(/[\d.]+/g)!.slice(0, 3).map(Number).map(v => { const c = v / 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0); }
    function ratio(a: string, b: string) { const x = rgb(a), y = rgb(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); }
    const field = element.querySelector('input')!, style = getComputedStyle(field);
    const background = getComputedStyle(element.closest('.private-drafts')!).backgroundColor;
    const surface = background === 'rgba(0, 0, 0, 0)' ? getComputedStyle(document.querySelector('main')!).backgroundColor : background;
    return { text: ratio(style.color, style.backgroundColor), border: ratio(style.borderColor, style.backgroundColor), focus: ratio(style.outlineColor, surface), focusWidth: parseFloat(style.outlineWidth) };
  });
  expect(contrast.text).toBeGreaterThanOrEqual(4.5); expect(contrast.border).toBeGreaterThanOrEqual(3); expect(contrast.focus).toBeGreaterThanOrEqual(3); expect(contrast.focusWidth).toBeGreaterThanOrEqual(2);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(busInput(page)).toHaveValue(' 0006 / 090 ');
  await post(context, '/workdays/' + plan.id + '/physical-bus', { operation_id: randomUUID(), expected_revision: 1, physical_bus: '0090' });
  await busInput(page).fill('mitt forslag 0006'); await saveBus(page).click(); await expect(busStatus(page)).toContainText('annet vindu');
  const reload = page.getByRole('button', { name: 'Last inn lagret buss', exact: true }); await reload.focus();
  await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab'); await expect(reload).toBeFocused();
  const recoveryContrast = await reload.evaluate(element => {
    const lum = (s: string) => s.match(/[\d.]+/g)!.slice(0, 3).map(Number).map(v => { const c = v / 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((s, c, i) => s + c * [.2126, .7152, .0722][i], 0);
    const ratio = (a: string, b: string) => (Math.max(lum(a), lum(b)) + .05) / (Math.min(lum(a), lum(b)) + .05);
    const s = getComputedStyle(element), bg = getComputedStyle(element.closest('.import-warning')!).backgroundColor;
    return { text: ratio(s.color, s.backgroundColor), boundary: ratio(s.borderColor, bg), focus: ratio(s.outlineColor, bg), focusWidth: parseFloat(s.outlineWidth) };
  });
  expect(recoveryContrast.text).toBeGreaterThanOrEqual(4.5); expect(recoveryContrast.boundary).toBeGreaterThanOrEqual(3); expect(recoveryContrast.focus).toBeGreaterThanOrEqual(3); expect(recoveryContrast.focusWidth).toBeGreaterThanOrEqual(2);
  await region.screenshot({ path: `../docs/evidence/11-2-regression-10-4-bus-conflict-${width}-${night ? 'night' : 'day'}.png` });
  await page.getByRole('button', { name: 'Last inn lagret buss', exact: true }).click();
  await expect(busInput(page)).toBeFocused();
  await busInput(page).fill(''); await saveBus(page).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
  expect(await (await context.request.get(API + '/drafts/' + draft.id)).json()).toEqual(draft);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(busInput(page)).toHaveValue('');
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0]);
  expect(await page.evaluate(async () => ({ databases: (await indexedDB.databases()).length, caches: (await caches.keys()).length }))).toEqual({ databases: 0, caches: 0 });
});

test('conflict preserves losing input until explicit reload and new revision save', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  await busInput(page).fill('mitt forslag');
  await post(context, '/workdays/' + plan.id + '/physical-bus', { operation_id: randomUUID(), expected_revision: 0, physical_bus: '0090' });
  await saveBus(page).click();
  await expect(busStatus(page)).toContainText('annet vindu');
  await expect(busInput(page)).toHaveValue('mitt forslag');
  await expect(page.getByText('Nyere lagret verdi:', { exact: false })).toContainText('0090');
  await page.getByRole('button', { name: 'Last inn lagret buss', exact: true }).click();
  await expect(busInput(page)).toHaveValue('0090');
  await busInput(page).fill('0006'); await saveBus(page).click();
  await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
});

test('lost reply uses identical operation retry and compares newer accepted state', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  const path = '/workdays/' + plan.id + '/physical-bus'; let first: any;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET') return route.continue();
    first = route.request().postDataJSON(); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost response</html>' });
  });
  await busInput(page).fill('0006'); await saveBus(page).click(); await expect(busStatus(page)).toContainText('uavklart');
  await expect(page.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true })).toBeEnabled();
  await post(context, path, { operation_id: randomUUID(), expected_revision: 1, physical_bus: '0090' });
  await page.unroute('**:8001' + path);
  let retried: any;
  page.on('request', request => { if (request.url().endsWith(path) && request.method() === 'POST') retried = request.postDataJSON(); });
  await page.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true }).click();
  await expect(busStatus(page)).toContainText('nyere registrering'); expect(retried).toEqual(first);
  await expect(busInput(page)).toHaveValue('0006');
  expect((await (await context.request.get(API + path)).json()).physical_bus).toBe('0090');
});

test('missing lookup stays uncertain; successful lookup verifies current bus', async ({ page, context }) => {
  await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  await page.route('**:8001/workdays/*/physical-bus', async route => {
    if (route.request().method() === 'GET') return route.continue();
    await route.fulfill({ status: 503, json: { detail: 'synthetic unavailable before acceptance' } });
  });
  await busInput(page).fill('0012'); await saveBus(page).click();
  await page.getByRole('button', { name: 'Kontroller busslagringen', exact: true }).click();
  await expect(busStatus(page)).toContainText('uavklart'); await expect(busInput(page)).toHaveValue('0012');
  await expect(page.getByRole('heading', { name: 'Bekreftet plan · versjon 1', exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
  await page.unroute('**:8001/workdays/*/physical-bus');
  await page.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true }).click();
  await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
});

test('malformed accepted receipt stays unresolved until guarded operation lookup', async ({ page, context }) => {
  await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  await page.route('**:8001/workdays/*/physical-bus', async route => {
    if (route.request().method() === 'GET') return route.continue();
    const response = await route.fetch(); const receipt = await response.json();
    await route.fulfill({ json: { ...receipt, result: { ...receipt.result, physical_bus: 'wrong value' } } });
  });
  await busInput(page).fill('0012'); await saveBus(page).click();
  await expect(busStatus(page)).toContainText('uavklart');
  await page.getByRole('button', { name: 'Kontroller busslagringen', exact: true }).click();
  await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.'); await expect(busInput(page)).toHaveValue('0012');
});

test('delayed parent plan response cannot replace unsaved bus input', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  let release!: () => void, started!: () => void;
  const hold = new Promise<void>(resolve => release = resolve), reached = new Promise<void>(resolve => started = resolve);
  await page.route('**:8001/workdays/' + plan.id, async route => { const response = await route.fetch(); started(); await hold; await route.fulfill({ response }); });
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await reached; await planScreen(page);
  await busInput(page).fill('behold 0006'); release();
  await expect(busInput(page)).toHaveValue('behold 0006'); await expect(saveBus(page)).toBeEnabled();
  await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeEnabled();
});

test('same plan reopen refreshes current registration and supports 100 Unicode code points', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  await post(context, '/workdays/' + plan.id + '/physical-bus', { operation_id: randomUUID(), expected_revision: 0, physical_bus: '0090' });
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(busInput(page)).toHaveValue('0090');
  const unicode = '🚍'.repeat(100);
  await busInput(page).fill(unicode); await saveBus(page).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(busInput(page)).toHaveValue(unicode);
});

test('pending plan deletion disables bus entry until its outcome is settled', async ({ page, context }) => {
  await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  let release!: () => void, entered!: () => void;
  const hold = new Promise<void>(resolve => release = resolve), reached = new Promise<void>(resolve => entered = resolve);
  await page.route('**:8001/workdays/*/delete', async route => { entered(); await hold; await route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } }); });
  page.once('dialog', dialog => dialog.accept());
  try {
    await page.getByRole('button', { name: 'Slett bekreftet plan', exact: true }).click(); await reached;
    await expect(busInput(page)).toBeDisabled(); release();
    await expect(page.getByRole('button', { name: 'Kontroller slettingen', exact: true })).toBeEnabled();
    await expect(busInput(page)).toBeDisabled();
  } finally { release(); }
});

test('remote deletion after bus acceptance hides authority and preserves the same unresolved operation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  const path = '/workdays/' + plan.id + '/physical-bus'; let original: any;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET') return route.continue();
    original = route.request().postDataJSON(); const response = await route.fetch();
    await post(context, '/workdays/' + plan.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
    await route.fulfill({ response });
  });
  await busInput(page).fill('behold lokalt 0012'); await saveBus(page).click();
  await expect(page.getByText('Planfakta er skjult til plantilgangen er kontrollert.', { exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
  await expect(page.getByRole('heading', { name: 'Bekreftet plan · versjon 1', exact: true })).toHaveCount(0);
  await expect(page.getByText(/^Lagret verdi:/)).toHaveCount(0);
  await expect(busInput(page)).toHaveValue('behold lokalt 0012');
  await expect(busStatus(page)).toContainText('uavklart');
  await page.unroute('**:8001' + path); let retry: any;
  page.on('request', request => { if (request.url().endsWith(path) && request.method() === 'POST') retry = request.postDataJSON(); });
  await page.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller busslagringen', exact: true })).toBeEnabled();
  expect(retry).toEqual(original); expect((await context.request.get(API + path)).status()).toBe(404);
  await expect(busInput(page)).toHaveValue('behold lokalt 0012');
});

test('denied current bus read hides authority until successful recovery and operation lookup', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  const path = '/workdays/' + plan.id + '/physical-bus'; let denied = true;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET' && denied) return route.fulfill({ status: 404, json: { detail: 'synthetic denial' } });
    return route.continue();
  });
  await busInput(page).fill('0012'); await saveBus(page).click();
  await expect(page.getByText('Planfakta er skjult til plantilgangen er kontrollert.', { exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
  await expect(busInput(page)).toHaveValue('0012');
  denied = false;
  await page.getByRole('button', { name: 'Kontroller plantilgangen', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Bekreftet plan · versjon 1', exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
  await expect(busStatus(page)).toContainText('fortsatt uavklart');
  await page.getByRole('button', { name: 'Kontroller busslagringen', exact: true }).click();
  await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.'); await expect(busInput(page)).toHaveValue('0012');
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
});

test('initial denied bus read recovery populates the current saved value', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  const path = '/workdays/' + plan.id + '/physical-bus';
  await post(context, path, { operation_id: randomUUID(), expected_revision: 0, physical_bus: ' 0012 ' });
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click(); let denied = true;
  await page.route('**:8001' + path, route => denied ? route.fulfill({ status: 404, json: { detail: 'synthetic denied initial read' } }) : route.continue());
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByText('Planfakta er skjult til plantilgangen er kontrollert.', { exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
  denied = false; await page.getByRole('button', { name: 'Kontroller plantilgangen', exact: true }).click();
  await expect(busInput(page)).toHaveValue(' 0012 ');
  await expect(page.getByRole('heading', { name: 'Bekreftet plan · versjon 1', exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
});

const beforeUnload = (page: Page) => page.evaluate(() => { const event = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(event); return event.defaultPrevented; });

const expectUnload = async (page: Page, blocked: boolean) => { await expect.poll(() => beforeUnload(page)).toBe(blocked); };

test('Unicode whitespace contract preserves FEFF and meaningful formatting through receipts', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  for (const [value, expected] of [['0012', '0012'], ['\u0085', null], ['\ufeff', '\ufeff'], [' \u0085A\ufeff ', ' \u0085A\ufeff ']] as const) {
    await busInput(page).fill(value); await saveBus(page).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
    expect((await (await context.request.get(API + '/workdays/' + plan.id + '/physical-bus')).json()).physical_bus).toBe(expected);
  }
});

test('oversized and NUL input explain rejection and retain invalid input for correction', async ({ page, context }) => {
  await openedPlan(page, context); await expect(busInput(page)).toBeEnabled(); await busInput(page).fill('0012');
  let writes = 0; page.on('request', req => { if (req.url().endsWith('/physical-bus') && req.method() === 'POST') writes++; });
  await busInput(page).fill('🚍'.repeat(102)); await expect(busStatus(page)).toContainText('Maksimum er 100 tegn'); await expect(busInput(page)).toHaveValue('🚍'.repeat(102));
  await expect(busInput(page)).toHaveAttribute('aria-invalid', 'true'); await expect(busInput(page)).toHaveAttribute('aria-describedby', 'physical-bus-error');
  await expect(busInput(page)).toHaveAccessibleDescription(/Maksimum er 100 tegn/);
  await expect(saveBus(page)).toBeDisabled(); expect(writes).toBe(0);
  await busInput(page).fill('A\0B'); await expect(busStatus(page)).toContainText('NUL-tegn'); await expect(busInput(page)).toHaveValue('A\0B');
  await expect(busInput(page)).toHaveAttribute('aria-invalid', 'true'); await expect(busInput(page)).toHaveAccessibleDescription(/NUL-tegn/);
  await expect(saveBus(page)).toBeDisabled(); expect(writes).toBe(0);
  await busInput(page).fill('0012');
  await expect(busInput(page)).toHaveAttribute('aria-invalid', 'false'); await expect(page.locator('#physical-bus-error')).toHaveCount(0);
  await expect(saveBus(page)).toBeEnabled(); await saveBus(page).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
});

test('returning to a normalized saved value releases bus-only guards without a write', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled(); await expectUnload(page, false);
  await busInput(page).fill('0012'); await expectUnload(page, true);
  await busInput(page).fill('\u0085'); await expect(saveBus(page)).toBeDisabled(); await expectUnload(page, false);
  await preparation(page); await expect(page.getByRole('button', { name: 'Nytt utkast', exact: true })).toBeEnabled(); await planScreen(page);
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/physical-bus')).json()).revision).toBe(0);
  await busInput(page).fill('0012'); await saveBus(page).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.');
  let writes = 0; page.on('request', req => { if (req.url().endsWith('/physical-bus') && req.method() === 'POST') writes++; });
  await busInput(page).fill('different'); await expectUnload(page, true);
  await busInput(page).fill('0012'); await expect(saveBus(page)).toBeDisabled(); await expectUnload(page, false);
  expect(writes).toBe(0); expect((await (await context.request.get(API + '/workdays/' + plan.id + '/physical-bus')).json()).revision).toBe(1);
});

test('review fixes invalid whitespace against saved-null bus remains cancellable and guarded', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  let writes = 0; page.on('request', req => { if (req.url().endsWith('/physical-bus') && req.method() === 'POST') writes++; });
  const invalid = ' '.repeat(101);
  await busInput(page).fill(invalid);
  await expect(busInput(page)).toHaveValue(invalid); await expect(saveBus(page)).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Avbryt bussendring', exact: true })).toBeEnabled();
  await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { includeHidden: true, name: 'Nytt utkast', exact: true })).toBeDisabled();
  await expectUnload(page, true);
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('link', { name: 'Åpne fiktiv demo', exact: true }).click();
  await expect(page).toHaveURL(/\/private$/); await expect(busInput(page)).toHaveValue(invalid);
  await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await expect(busInput(page)).toHaveValue(''); await expectUnload(page, false);
  expect(writes).toBe(0);
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/physical-bus')).json()).physical_bus).toBeNull();
});

test('authoritative receipt capacity rejection preserves editable input and cancellation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  const path = '/workdays/' + plan.id + '/physical-bus';
  const receipt = await post(context, path, { operation_id: randomUUID(), expected_revision: 0, physical_bus: 'base' });
  python(`from psycopg.types.json import Jsonb\nwith database() as conn:\n row=conn.execute('SELECT * FROM workday_bus_operations WHERE id=%s', (${JSON.stringify(receipt.operation_id)},)).fetchone()\n conn.execute('INSERT INTO workday_bus_operations SELECT gen_random_uuid(),owner,workday_id,payload_hash,result,expires_at FROM workday_bus_operations CROSS JOIN generate_series(1,1999) WHERE id=%s', (row['id'],))\n`);
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await expect(busInput(page)).toHaveValue('base');
  await busInput(page).fill('proposal'); await saveBus(page).click(); await expect(busStatus(page)).toContainText('grensen på 2000');
  await expect(busInput(page)).toHaveValue('proposal'); await expect(busInput(page)).toBeEnabled();
  await busInput(page).fill('editable proposal'); await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await expect(busInput(page)).toHaveValue('base'); await expectUnload(page, false);
});

for (const malformed of [false, true]) test(`accepted write followed by ${malformed ? 'malformed JSON' : 'HTML'} 429 keeps the original nonce`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled(); const path = '/workdays/' + plan.id + '/physical-bus'; let original: any;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET') return route.continue();
    original = route.request().postDataJSON(); await route.fetch();
    await route.fulfill(malformed ? { status: 429, json: { detail: { code: 'bus_receipt_capacity' } } } : { status: 429, contentType: 'text/html', body: '<html>capacity</html>' });
  });
  await busInput(page).fill('0012'); await saveBus(page).click(); await expect(page.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true })).toBeEnabled();
  await expect(busInput(page)).toBeDisabled(); await expectUnload(page, true);
  await page.unroute('**:8001' + path); let retry: any; page.on('request', req => { if (req.url().endsWith(path) && req.method() === 'POST') retry = req.postDataJSON(); });
  await page.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true }).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.'); expect(retry).toEqual(original);
});

for (const unresolved of [false, true]) test(`bus-only outer leave guards retain ${unresolved ? 'unresolved' : 'dirty'} proposals and release`, async ({ page, context }) => {
  await openedPlan(page, context); await expect(busInput(page)).toBeEnabled(); await expectUnload(page, false);
  if (unresolved) await page.route('**:8001/workdays/*/physical-bus', async route => { if (route.request().method() === 'GET') return route.continue(); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost</html>' }); });
  await busInput(page).fill('bus-only proposal');
  if (unresolved) { await saveBus(page).click(); await expect(page.getByRole('button', { name: 'Kontroller busslagringen', exact: true })).toBeEnabled(); }
  await expectUnload(page, true); await expect(page.getByRole('button', { includeHidden: true, name: 'Nytt utkast', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { includeHidden: true, name: 'Åpne 2031-01-02 · versjon 1', exact: true })).toBeDisabled();
  let prompts = 0;
  page.once('dialog', async dialog => { prompts++; expect(dialog.message()).toContain('går tapt'); await dialog.dismiss(); });
  await page.getByRole('link', { name: 'Åpne fiktiv demo', exact: true }).click(); await expect(page).toHaveURL(/\/private$/);
  page.once('dialog', async dialog => { prompts++; expect(dialog.message()).toContain('utlogging'); await dialog.dismiss(); });
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click(); expect(prompts).toBe(2); await expect(busInput(page)).toHaveValue('bus-only proposal');
  if (unresolved) { await page.unroute('**:8001/workdays/*/physical-bus'); await page.getByRole('button', { name: 'Kontroller busslagringen', exact: true }).click(); await expect(busStatus(page)).toHaveText('Fysisk buss er lagret.'); }
  else await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await preparation(page); await expectUnload(page, false); await expect(page.getByRole('button', { name: 'Nytt utkast', exact: true })).toBeEnabled(); await planScreen(page);
});

for (const unresolved of [false, true]) test(`near-expiry bus-only ${unresolved ? 'unresolved' : 'unsaved'} state clears presentation guards and late replies`, async ({ page, context }) => {
  await page.clock.install(); await login(page);
  const ending = python("from datetime import datetime,timedelta\nfrom zoneinfo import ZoneInfo\nprint((datetime.now(ZoneInfo('Europe/Oslo'))-timedelta(days=7)+timedelta(seconds=60)).replace(microsecond=0).isoformat())\n").trim();
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: ending.slice(0, 10), activities: [{ id: randomUUID(), type: 'manual', start: ending, end: ending }] } });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click(); await page.getByRole('button', { name: `Åpne ${draft.draft.service_date} · versjon 1`, exact: true }).click();
  const plan = await confirmSaved(context, draft); await page.clock.setSystemTime(new Date(Date.parse(plan.expires_at) - 5000));
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click(); await page.getByRole('button', { name: `Åpne plan ${draft.draft.service_date} · versjon 1`, exact: true }).click();
  await expect(busInput(page)).toBeEnabled(); await expectUnload(page, false);
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => release = resolve), waiting = new Promise<void>(resolve => entered = resolve);
  if (unresolved) await page.route('**:8001/workdays/' + plan.id + '/physical-bus', async route => { if (route.request().method() === 'GET') return route.continue(); const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try {
    await busInput(page).fill('near expiry'); if (unresolved) { await saveBus(page).click(); await waiting; }
    await expectUnload(page, true);
    await page.clock.fastForward(6000); await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Kontroller busslagringen', exact: true })).toHaveCount(0); await expectUnload(page, false);
  await preparation(page); await expect(page.getByRole('button', { name: 'Nytt utkast', exact: true })).toBeEnabled(); await expect(page.getByRole('button', { name: 'Oppdater planlisten', exact: true })).toBeEnabled();
    if (unresolved) { const returned = page.waitForResponse(response => response.url().endsWith('/workdays/' + plan.id + '/physical-bus') && response.request().method() === 'POST'); release(); await (await returned).finished(); }
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0); await expectUnload(page, false);
  } finally { release?.(); }
});

test('single-pane two-plan lifecycle guards bus edits and keeps confirmation snapshots independent', async ({ page, context }) => {
  const { plan: first } = await openedPlan(page, context); await expect(busInput(page)).toBeEnabled();
  const second = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: '2031-01-03', physical_bus: 'B snapshot', activities: [{ id: randomUUID(), type: 'manual', start: '2031-01-03T10:00+01:00', end: '2031-01-03T11:00+01:00' }] } });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click(); await page.getByRole('button', { name: 'Åpne 2031-01-03 · versjon 1', exact: true }).click();
  const begin = page.getByRole('button', { includeHidden: true, name: 'Gjennomgå lagret utkast', exact: true }); await expect(begin).toBeEnabled();
  await planScreen(page); await busInput(page).fill('A manual bus'); await expect(begin).toBeDisabled();
  await expect(page.getByRole('button', { includeHidden: true, name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click(); await editor(page); await expect(begin).toBeEnabled();
  await review(page); await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  await decide(page);
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon', exact: true })).toHaveCount(0); await expect(busInput(page)).toBeEnabled();
  await review(page); await decide(page); const confirm = page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }); await expect(confirm).toBeEnabled();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  let release!: () => void, entered!: () => void; const gate = new Promise<void>(resolve => release = resolve), waiting = new Promise<void>(resolve => entered = resolve);
  await page.route('**:8001/drafts/' + second.id + '/confirm', async route => { const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try {
    await confirm.click(); await waiting; await expect(busInput(page)).toHaveCount(0);
    await expect(page.getByRole('button', { includeHidden: true, name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toBeDisabled(); release();
    await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Planen er bekreftet'); await expect(busInput(page)).toHaveValue('B snapshot');
    expect((await (await context.request.get(API + '/workdays/' + first.id + '/physical-bus')).json()).physical_bus).toBe(null);
    expect((await (await context.request.get(API + '/workdays')).json()).workdays).toHaveLength(2);
  } finally { release(); }
});
