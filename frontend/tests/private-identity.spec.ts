import { preparation, editor } from './private-screen-helpers';
import { test, expect, type BrowserContext, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';

test('an obsolete unauthorized read cannot clear input after same-session revalidation', async ({ page }) => {
  await visibleWindow(page);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('Keep after revalidation');
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const waiting = new Promise<void>(resolve => { entered = resolve; });
  await page.route('**:8001/drafts', async route => {
    entered(); await gate;
    await route.fulfill({ status: 401, json: { detail: 'Synthetic delayed expiry' } });
  });
  try {
    await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
    await waiting;
    await page.evaluate(() => {
      Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' });
      document.dispatchEvent(new Event('visibilitychange'));
      Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' });
      document.dispatchEvent(new Event('visibilitychange'));
    });
    await expect(page.getByRole('status', { name: 'Tilgangsstatus' })).toHaveText('Du er logget inn.');
    const returned = page.waitForResponse(response => response.url().endsWith(':8001/drafts'));
    release(); await (await returned).finished();
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve(null)))));
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Keep after revalidation');
  } finally { release(); }
});

test('unavailable identity validation hides and then restores the same unsaved input', async ({ page }) => {
  await visibleWindow(page);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('Keep through outage');
  await page.route('**:8001/auth/session', route => route.abort());
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Private utkast' })).toBeHidden();
  await expect(page.getByRole('button', { name: 'Kontroller tilgang igjen' })).toBeEnabled();
  await page.unroute('**:8001/auth/session');
  await page.getByRole('button', { name: 'Kontroller tilgang igjen' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Keep through outage');
});

const accounts = ['a', 'b'].map(name => ({ username: `synthetic-identity-${name}-${randomUUID()}`, password: randomBytes(24).toString('hex') }));
const API = 'http://127.0.0.1:8001';

function python(program: string) {
  if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project selection required');
  return execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'], {
    cwd: '..', encoding: 'utf8', input: 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n' + program,
  });
}

test.beforeAll(() => {
  python('from app.auth import provision\n' + accounts.map(account => `provision(${JSON.stringify(account.username)}, ${JSON.stringify(account.password)})\n`).join(''));
});
test.beforeEach(() => python("with database() as conn:\n conn.execute('DELETE FROM login_limits')\n"));
test.afterAll(() => {
  for (const account of accounts) python(`with database() as conn:
 owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(account.username)},)).fetchone()['id']
 conn.execute('DELETE FROM workday_deletions WHERE owner=%s', (owner,))
 conn.execute('DELETE FROM workday_operations WHERE owner=%s', (owner,))
 conn.execute('DELETE FROM workdays WHERE owner=%s', (owner,))
 conn.execute('DELETE FROM drafts WHERE owner=%s', (owner,))
 conn.execute('DELETE FROM draft_operations WHERE owner=%s', (owner,))
 conn.execute('DELETE FROM draft_deletions WHERE owner=%s', (owner,))
 conn.execute('DELETE FROM sessions WHERE owner=%s', (owner,))
 conn.execute('DELETE FROM accounts WHERE id=%s', (owner,))
 conn.execute('DELETE FROM login_limits')
`);
});

async function visibleWindow(page: Page, suppressBroadcast = false) {
  await page.addInitScript(({ suppressBroadcast }) => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' });
    if (suppressBroadcast) {
      const NativeChannel = window.BroadcastChannel;
      window.BroadcastChannel = class extends NativeChannel {
        constructor(name: string) {
          super(name);
          // Keep the native channel and outgoing notifications; drop incoming handlers.
          Object.defineProperty(this, 'onmessage', { configurable: true, set: () => {}, get: () => null });
        }
      };
    }
  }, { suppressBroadcast });
  await page.goto('/private');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
}

async function twoLoggedOutWindows(page: Page, context: BrowserContext, suppressBroadcast = false) {
  await visibleWindow(page, suppressBroadcast);
  const other = await context.newPage();
  await visibleWindow(other);
  return other;
}

async function login(page: Page, index: number) {
  await page.getByLabel('Brukernavn', { exact: true }).fill(accounts[index].username);
  await page.getByLabel('Passord', { exact: true }).fill(accounts[index].password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
  // Finish the login's automatic list read before switching the shared account.
  // Otherwise that earlier read can correctly invalidate the old editor first,
  // before the mutation this scenario intends to exercise.
  await expect(page.getByText('Laster lagrede utkast …', { exact: true })).toHaveCount(0);
}

test('account login in another visible window promptly clears the previous editor', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('A private unsaved work');
  // A login must leave an already open, logged-out login form usable.
  await expect(other.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
  await login(other, 1);
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveCount(0);
  await other.close();
});

test('missed account broadcast cannot save a new unsaved draft under the next account', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('A must never become B work');
  await login(other, 1);
  const before = await (await context.request.get(API + '/drafts')).json();
  let posts = 0;
  page.on('request', request => {
    if (request.method() === 'POST' && ['/draft-operations', '/drafts'].includes(new URL(request.url()).pathname)) posts++;
  });
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  expect(posts).toBe(0);
  expect(await (await context.request.get(API + '/drafts')).json()).toEqual(before);
  await other.close();
});

test('missed account broadcast cannot refresh the previous workspace with the next accounts list', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('A unsaved editor');
  await login(other, 1);
  await editor(other); await other.getByLabel('Tjenestedato', { exact: true }).fill('2031-02-03');
  await editor(other); await other.getByLabel('Buss/vogn', { exact: true }).fill('B private draft');
  await editor(other); await other.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(other.getByRole('region', { name: 'Private utkast' }).getByRole('status')).toHaveText('Lagret. Versjon 1.');
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  await expect(page.getByRole('button', { name: /Åpne 2031-02-03/ })).toHaveCount(0);
  await other.close();
});

test('missed account broadcast blocks PDF upload from the previous workspace', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('A private work before import');
  await login(other, 1);
  let uploads = 0;
  page.on('request', request => {
    if (request.method() === 'POST' && new URL(request.url()).pathname === '/imports/pdf') uploads++;
  });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({
    name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.4\n%%EOF'),
  });
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  expect(uploads).toBe(0);
  await other.close();
});

test('account switch queued between draft operation and save never sends the previous accounts content', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('A content cannot cross the queued login');
  const countB = () => Number(python(`with database() as conn:
 print(conn.execute('SELECT count(*) AS n FROM drafts WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(accounts[1].username)},)).fetchone()['n'])
`).trim());
  const before = countB();
  let release!: () => void;
  let issued!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const committed = new Promise<void>(resolve => { issued = resolve; });
  let saves = 0;
  page.on('request', request => {
    if (request.method() === 'POST' && new URL(request.url()).pathname === '/drafts') saves++;
  });
  await page.route('**:8001/draft-operations', async route => {
    const response = await route.fetch();
    expect(response.status()).toBe(200);
    issued();
    await gate;
    await route.fulfill({ response });
  });
  try {
    await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
    await committed;
    await other.getByLabel('Brukernavn', { exact: true }).fill(accounts[1].username);
    await other.getByLabel('Passord', { exact: true }).fill(accounts[1].password);
    await other.getByRole('button', { name: 'Logg inn', exact: true }).click();
    await expect.poll(() => other.evaluate(async () => {
      const locks = await navigator.locks.query();
      return locks.pending?.some(lock => lock.name === 'private-auth-mutations') ?? false;
    })).toBe(true);
    release();
    await expect(other.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
    expect(saves).toBe(0);
    expect(countB()).toBe(before);
    expect((await (await context.request.get(API + '/drafts')).json()).drafts).toHaveLength(before);
  } finally {
    release();
    await other.close();
  }
});

for (const paginated of [false, true]) test(`a delayed private list is rejected after another window changes account (cursor=${paginated})`, async ({ page, context }) => {
  if (paginated) python(`from uuid import uuid4\nfrom psycopg.types.json import Jsonb\nwith database() as conn:\n owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(accounts[0].username)},)).fetchone()['id']\n for n in range(51):\n  conn.execute('INSERT INTO drafts(id,owner,revision,content) VALUES (%s,%s,1,%s)',(uuid4(),owner,Jsonb({'service_date':'2034-06-07','activities':[]})))\n`);
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('Previous account private input');
  await expect(page.getByText('Laster lagrede utkast …', { exact: true })).toHaveCount(0);
  let release!: () => void;
  let fetched!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const received = new Promise<void>(resolve => { fetched = resolve; });
  await page.route(paginated ? '**:8001/drafts?cursor=*' : '**:8001/drafts', async route => {
    const response = await route.fetch();
    expect(response.status()).toBe(200);
    fetched();
    await gate;
    await route.fulfill({ response });
  });
  try {
    await preparation(page); await page.getByRole('button', { name: paginated ? 'Vis flere utkast' : 'Oppdater listen', exact: true }).click();
    await received;
    // Reads must leave the auth lock available while waiting for their body.
    await login(other, 1);
    release();
    await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveCount(0);
    await expect(other.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
    await expect(other.getByRole('button', { name: /Åpne 2034-06-07/ })).toHaveCount(0);
  } finally {
    release();
    await other.close();
    if (paginated) python(`with database() as conn:\n conn.execute("DELETE FROM drafts WHERE owner IN (SELECT id FROM accounts WHERE username=%s) AND content->>'service_date'='2034-06-07'", (${JSON.stringify(accounts[0].username)},))\n`);
  }
});

test('missed broadcasts cannot reopen a plan from the next account', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await login(other, 1);
  let reads = 0;
  page.on('request', request => { if (new URL(request.url()).pathname === '/workdays') reads++; });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  expect(reads).toBe(0);
  await other.close();
});

test('delayed plan list cannot enter a workspace after a silent account switch', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  // Finish initial plan discovery before intercepting this explicit read.
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toHaveText('Planlisten er oppdatert.');
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const received = new Promise<void>(resolve => { entered = resolve; });
  await page.route('**:8001/workdays', async route => {
    const response = await route.fetch(); entered(); await gate;
    await route.fulfill({ response });
  });
  try {
    await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
    await received; await login(other, 1); release();
    await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
    await expect(page.getByRole('region', { name: 'Bekreft plan' })).toHaveCount(0);
  } finally { release(); await other.close(); }
});

for (const delayed of [false, true]) test(`plan deletion ${delayed ? 'delayed acknowledgement' : 'preflight'} cannot cross a silent account switch`, async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  async function post(path: string, data: object) {
    const proof = await (await context.request.get(API + '/auth/csrf')).json();
    const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data });
    expect(response.status()).toBe(200); return response.json();
  }
  const serviceDate = delayed ? '2033-02-04' : '2033-02-03';
  const draft = await post('/drafts', { operation_id: (await post('/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: serviceDate, activities: [{ id: randomUUID(), type: 'manual', start: '2033-02-03T10:00+01:00', end: '2033-02-03T11:00+01:00' }] } });
  const review = await post('/workday-reviews', { draft_id: draft.id, expected_revision: 1 });
  const plan = await post('/drafts/' + draft.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: review.unknowns.map((item: any) => item.id), classifications: {} });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan ' + serviceDate + ' · versjon 1', exact: true }).click();
  let release!: () => void, entered!: () => void, writes = 0;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const received = new Promise<void>(resolve => { entered = resolve; });
  page.on('request', request => { if (request.url().endsWith('/workdays/' + plan.id + '/delete')) writes++; });
  if (delayed) await page.route('**:8001/workdays/*/delete', async route => { const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try {
    if (!delayed) await post('/auth/login', accounts[1]);
    page.once('dialog', dialog => dialog.accept());
    await page.getByRole('button', { name: 'Slett bekreftet plan', exact: true }).click();
    if (delayed) { await received; await post('/auth/login', accounts[1]); release(); }
    await expect(page.getByRole('region', { name: 'Bekreft plan' })).toHaveCount(0);
    expect(writes).toBe(delayed ? 1 : 0);
    await post('/auth/login', accounts[0]);
    expect((await context.request.get(API + '/workdays/' + plan.id)).status()).toBe(delayed ? 404 : 200);
  } finally { release(); await other.close(); }
});

for (const delayed of [false, true, 'denied-current'] as const) test(`physical bus ${delayed === 'denied-current' ? 'denied current read' : delayed ? 'delayed reply' : 'preflight'} cannot cross a silent account switch`, async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true); await login(page, 0);
  async function post(path: string, data: object) {
    const proof = await (await context.request.get(API + '/auth/csrf')).json();
    const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data });
    expect(response.status()).toBe(200); return response.json();
  }
  const serviceDate = delayed === 'denied-current' ? '2034-01-04' : delayed ? '2034-01-03' : '2034-01-02';
  const draft = await post('/drafts', { operation_id: (await post('/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: serviceDate, activities: [{ id: randomUUID(), type: 'manual', start: '2034-01-02T10:00+01:00', end: '2034-01-02T11:00+01:00' }] } });
  const review = await post('/workday-reviews', { draft_id: draft.id, expected_revision: 1 });
  const plan = await post('/drafts/' + draft.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: review.unknowns.map((item: any) => item.id), classifications: {} });
  const path = '/workdays/' + plan.id + '/physical-bus';
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan ' + serviceDate + ' · versjon 1', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
  await page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true }).fill('0012 old account');
  let release!: () => void, entered!: () => void, writes = 0;
  const gate = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  page.on('request', request => { if (request.url().endsWith(path) && request.method() === 'POST') writes++; });
  if (delayed === true) await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET') return route.continue();
    const response = await route.fetch(); entered(); await gate; await route.fulfill({ response });
  });
  if (delayed === 'denied-current') await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'POST') return route.continue();
    entered(); await gate; await route.fulfill({ status: 404, json: { detail: 'synthetic denied current read' } });
  });
  try {
    if (!delayed) await post('/auth/login', accounts[1]);
    await page.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click();
    if (delayed) { await received; await post('/auth/login', accounts[1]); release(); }
    await expect(page.getByRole('region', { name: 'Bekreft plan' })).toHaveCount(0);
    await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
    expect(writes).toBe(delayed ? 1 : 0);
    await post('/auth/login', accounts[0]);
    const value = await (await context.request.get(API + path)).json();
    expect(value.physical_bus).toBe(delayed ? '0012 old account' : null);
    expect(value.revision).toBe(delayed ? 1 : 0);
  } finally { release(); await other.close(); }
});

for (const resource of ['selection', 'start']) for (const delayed of [false, true, 'denied-current'] as const) test(`${resource} ${delayed === 'denied-current' ? 'denied current read' : delayed ? 'delayed reply' : 'preflight'} cannot cross a silent account switch`, async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true); await login(page, 0);
  async function post(path: string, data: object) {
    const proof = await (await context.request.get(API + '/auth/csrf')).json();
    const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data });
    expect(response.status()).toBe(200); return response.json();
  }
  const serviceDate = `2035-0${resource === 'selection' ? 1 : 2}-0${delayed === 'denied-current' ? 4 : delayed ? 3 : 2}`;
  const activityId = randomUUID();
  const draft = await post('/drafts', { operation_id: (await post('/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: serviceDate, activities: [{ id: activityId, type: 'manual', start: serviceDate + 'T10:00+01:00', end: serviceDate + 'T11:00+01:00' }] } });
  const review = await post('/workday-reviews', { draft_id: draft.id, expected_revision: 1 });
  const plan = await post('/drafts/' + draft.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: [], classifications: {} });
  const path = '/workdays/' + plan.id + '/' + resource;
  const read = '/workdays/' + plan.id + '/' + (resource === 'start' ? 'lifecycle' : resource);
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan ' + serviceDate + ' · versjon 1', exact: true }).click();
  const action = page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true });
  await expect(action).toBeEnabled();
  let release!: () => void, entered!: () => void, writes = 0;
  const gate = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  page.on('request', request => { if (request.url().endsWith(path) && request.method() === 'POST') writes++; });
  if (delayed === true) await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET') return route.continue();
    const response = await route.fetch(); entered(); await gate; await route.fulfill({ response });
  });
  if (delayed === 'denied-current') await page.route('**:8001' + read, async route => {
    if (route.request().method() === 'POST') return route.continue();
    entered(); await gate; await route.fulfill({ status: 404, json: { detail: 'synthetic denied read' } });
  });
  try {
    if (!delayed) await post('/auth/login', accounts[1]);
    await action.click();
    if (delayed) { await received; await post('/auth/login', accounts[1]); release(); }
    await expect(page.getByRole('region', { name: 'Bekreft plan' })).toHaveCount(0);
    await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
    expect(writes).toBe(delayed ? 1 : 0);
    await post('/auth/login', accounts[0]);
    const value = await (await context.request.get(API + read)).json();
    expect(value.revision).toBe(delayed ? 1 : 0);
    if (resource === 'selection') expect(value.activity_id).toBe(delayed ? activityId : null);
    else expect(value.state).toBe(delayed ? 'active' : 'confirmed');
  } finally { release(); await other.close(); }
});

test('review fix delayed accepted confirmation cannot cross a silent account switch', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  async function post(path: string, data: object) {
    const proof = await (await context.request.get(API + '/auth/csrf')).json();
    const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data });
    expect(response.status()).toBe(200); return response.json();
  }
  const draft = await post('/drafts', { operation_id: (await post('/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: '2033-02-05', activities: [{ id: randomUUID(), type: 'manual', start: '2033-02-05T10:00+01:00', end: '2033-02-05T11:00+01:00' }] } });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne 2033-02-05 · versjon 1', exact: true }).click();
  await editor(page); await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
  for (const box of await page.getByRole('region', { name: 'Gjennomgått versjon' }).getByRole('checkbox').all()) await box.check();
  let release!: () => void, entered!: () => void, accepted: any, decisions: any, writes = 0;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const received = new Promise<void>(resolve => { entered = resolve; });
  await page.route('**:8001/drafts/*/confirm', async route => { writes++; decisions = route.request().postDataJSON(); const response = await route.fetch(); expect(response.status()).toBe(200); accepted = await response.json(); entered(); await gate; await route.fulfill({ response }); });
  try {
    await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
    await received; await post('/auth/login', accounts[1]); release();
    await expect(page.getByRole('region', { name: 'Bekreft plan' })).toHaveCount(0);
    expect(writes).toBe(1);
    await post('/auth/login', accounts[0]);
    expect(await (await context.request.get(API + '/workday-operations/' + decisions.operation_id)).json()).toEqual({ state: 'accepted', result: accepted });
    expect(accepted.source_draft_id).toBe(draft.id);
    expect(accepted.acknowledgements.sort()).toEqual(decisions.acknowledgements.sort());
    expect(accepted.classifications).toEqual(decisions.classifications);
  } finally { release(); await other.close(); }
});

for (const action of ['cancel', 'logout'] as const) test(`${action} cancels an import waiting for its session preflight`, async ({ page }) => {
  await visibleWindow(page);
  await login(page, 0);
  await expect(page.getByText('Laster lagrede utkast …', { exact: true })).toHaveCount(0);
  let release!: () => void;
  let started!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const entered = new Promise<void>(resolve => { started = resolve; });
  let uploads = 0;
  let proofs = 0;
  page.on('request', request => {
    const path = new URL(request.url()).pathname;
    if (request.method() === 'POST' && path === '/imports/pdf') uploads++;
    if (path === '/auth/csrf') proofs++;
  });
  await page.route('**:8001/auth/session', async route => {
    const response = await route.fetch();
    started();
    await gate;
    await route.fulfill({ response }).catch(() => {});
  });
  try {
    await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({
      name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.4\n%%EOF'),
    });
    await entered;
    expect(proofs).toBe(0);
    if (action === 'cancel') {
      await page.getByRole('button', { name: 'Avbryt import', exact: true }).click();
      await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toBeEnabled();
    } else {
      await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
      await expect(page.getByRole('status', { name: 'Tilgangsstatus' })).toHaveText('Du er logget ut.');
      await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
    }
    await expect.poll(() => page.evaluate(async () => {
      const locks = await navigator.locks.query();
      return [...(locks.held ?? []), ...(locks.pending ?? [])].some(lock => lock.name === 'private-auth-mutations');
    })).toBe(false);
    release();
    expect(uploads).toBe(0);
    // Logout obtains one proof for its own request; the upload obtains none.
    expect(proofs).toBe(action === 'logout' ? 1 : 0);
    await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toHaveCount(0);
  } finally { release(); }
});
