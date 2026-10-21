import { test, expect, type BrowserContext, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';

test('an obsolete unauthorized read cannot clear input after same-session revalidation', async ({ page }) => {
  await visibleWindow(page);
  await login(page, 0);
  await page.getByLabel('Buss/vogn', { exact: true }).fill('Keep after revalidation');
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const waiting = new Promise<void>(resolve => { entered = resolve; });
  await page.route('**:8001/drafts', async route => {
    entered(); await gate;
    await route.fulfill({ status: 401, json: { detail: 'Synthetic delayed expiry' } });
  });
  try {
    await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
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
  await page.getByLabel('Buss/vogn', { exact: true }).fill('Keep through outage');
  await page.route('**:8001/auth/session', route => route.abort());
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
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
}

test('account login in another visible window promptly clears the previous editor', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context);
  await login(page, 0);
  await page.getByLabel('Buss/vogn', { exact: true }).fill('A private unsaved work');
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
  await page.getByLabel('Buss/vogn', { exact: true }).fill('A must never become B work');
  await login(other, 1);
  const before = await (await context.request.get(API + '/drafts')).json();
  let posts = 0;
  page.on('request', request => {
    if (request.method() === 'POST' && ['/draft-operations', '/drafts'].includes(new URL(request.url()).pathname)) posts++;
  });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  expect(posts).toBe(0);
  expect(await (await context.request.get(API + '/drafts')).json()).toEqual(before);
  await other.close();
});

test('missed account broadcast cannot refresh the previous workspace with the next accounts list', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await page.getByLabel('Buss/vogn', { exact: true }).fill('A unsaved editor');
  await login(other, 1);
  await other.getByLabel('Tjenestedato', { exact: true }).fill('2031-02-03');
  await other.getByLabel('Buss/vogn', { exact: true }).fill('B private draft');
  await other.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(other.getByRole('region', { name: 'Private utkast' }).getByRole('status')).toHaveText('Lagret. Versjon 1.');
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  await expect(page.getByRole('button', { name: /Åpne 2031-02-03/ })).toHaveCount(0);
  await other.close();
});

test('missed account broadcast blocks PDF upload from the previous workspace', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await page.getByLabel('Buss/vogn', { exact: true }).fill('A private work before import');
  await login(other, 1);
  let uploads = 0;
  page.on('request', request => {
    if (request.method() === 'POST' && new URL(request.url()).pathname === '/imports/pdf') uploads++;
  });
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({
    name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.4\n%%EOF'),
  });
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
  expect(uploads).toBe(0);
  await other.close();
});

test('account switch queued between draft operation and save never sends the previous accounts content', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await page.getByLabel('Buss/vogn', { exact: true }).fill('A content cannot cross the queued login');
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
    await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
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

test('a delayed private list is rejected after another window changes account', async ({ page, context }) => {
  const other = await twoLoggedOutWindows(page, context, true);
  await login(page, 0);
  await expect(page.getByText('Laster lagrede utkast …', { exact: true })).toHaveCount(0);
  let release!: () => void;
  let fetched!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const received = new Promise<void>(resolve => { fetched = resolve; });
  await page.route('**:8001/drafts', async route => {
    const response = await route.fetch();
    expect(response.status()).toBe(200);
    fetched();
    await gate;
    await route.fulfill({ response });
  });
  try {
    await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
    await received;
    // Reads must leave the auth lock available while waiting for their body.
    await login(other, 1);
    release();
    await expect(page.getByRole('heading', { name: 'Mine utkast' })).toHaveCount(0);
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveCount(0);
  } finally {
    release();
    await other.close();
  }
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
    await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({
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
