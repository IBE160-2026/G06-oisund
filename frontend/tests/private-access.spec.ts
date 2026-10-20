import { test, expect, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';

const username = 'synthetic-browser-' + randomUUID();
const password = randomBytes(24).toString('hex');
function python(program: string) {
  program = "from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n" + program;
  return execFileSync('docker', ['compose', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'],
    { cwd: '..', input: program, encoding: 'utf8' });
}
test.beforeAll(() => {
  python(`from app.auth import provision, require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\nprovision(${JSON.stringify(username)}, ${JSON.stringify(password)})\nwith database() as conn:\n require_synthetic_accounts(conn)\n conn.execute('DELETE FROM login_limits')\n`);
});
test.afterAll(() => {
  python(`from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM accounts WHERE username=%s', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM login_limits')\n`);
});
async function login(page: Page) {
  await page.goto('/private');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
  await page.getByLabel('Brukernavn', { exact: true }).fill(username);
  await page.getByLabel('Passord', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toBeVisible();
}

for (const width of [768, 1440]) {
  test(`keyboard login, ownership presentation and logout at ${width}px`, async ({ page, context }) => {
    await page.setViewportSize({ width, height: 1000 });
    await page.goto('/private');
    const name = page.getByLabel('Brukernavn', { exact: true });
    await expect(name).toBeEnabled();
    await name.focus();
    await page.keyboard.type(username);
    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Passord', { exact: true })).toBeFocused();
    await page.keyboard.type(password);
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Logg inn', exact: true })).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toBeFocused();
    await expect(page.getByText('Arbeidsrommet er tomt.', { exact: false })).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0]);
    const cookies = await context.cookies();
    const session = cookies.find(cookie => cookie.name === 'private_session');
    expect(session?.httpOnly).toBe(true);
    expect(session?.sameSite).toBe('Strict');
    await page.screenshot({ path: `../Docs/evidence/9-3-${width}.png`, fullPage: true });
    await page.reload();
    await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toBeVisible();
    await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
    await expect(page.getByRole('status')).toHaveText('Du er logget ut.');
    await expect(name).toBeFocused();
    await page.reload();
    await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
    await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toHaveCount(0);
    await page.goto('/');
    await expect(page.getByText('Fiktive demodata', { exact: true })).toBeVisible();
    await page.goBack();
    await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toHaveCount(0);
  });
}

test('unreachable logout locks immediately, survives reload and settles before reads', async ({ page, context }) => {
  await login(page);
  await page.route('**:8001/auth/logout', route => route.abort());
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByRole('status')).toContainText('Utlogging er ikke bekreftet.');
  const marker = (await context.cookies()).find(cookie => cookie.name === 'private_logout_pending');
  expect(marker?.expires).toBeGreaterThan(Date.now() / 1000 + 14 * 86400 - 10);
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toHaveCount(0);
  const paths: string[] = [];
  page.on('request', request => { if (request.url().includes(':8001/')) paths.push(new URL(request.url()).pathname); });
  await page.reload();
  await expect(page.getByRole('button', { name: 'Prøv utlogging igjen' })).toBeEnabled();
  expect(paths).not.toContain('/auth/session');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toHaveCount(0);
  await page.unroute('**:8001/auth/logout');
  await page.getByRole('button', { name: 'Prøv utlogging igjen' }).click();
  await expect(page.getByRole('status')).toHaveText('Du er logget ut.');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
});

test('lost logout acknowledgement retries an already revoked session', async ({ page }) => {
  await login(page);
  await page.route('**:8001/auth/logout', async route => { await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Prøv utlogging igjen' })).toBeEnabled();
  await page.unroute('**:8001/auth/logout');
  await page.reload();
  await expect(page.getByRole('status')).toHaveText('Du er logget ut.');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
});

test('server expiry removes presentation on revalidation', async ({ page }) => {
  await login(page);
  python(`from app.private_storage import database\nwith database() as conn:\n conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '15 days', expires_at=statement_timestamp()-interval '1 day' WHERE owner IN (SELECT id FROM accounts WHERE username=%s)", (${JSON.stringify(username)},))\n`);
  await page.reload();
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toHaveCount(0);
});

test('confirmed logout clears another open tab immediately', async ({ page, context }) => {
  await login(page);
  const other = await context.newPage();
  await other.goto('/private');
  await expect(other.getByRole('heading', { name: 'Privat arbeidsrom' })).toBeVisible();
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByRole('status')).toHaveText('Du er logget ut.');
  await expect(other.getByRole('heading', { name: 'Privat arbeidsrom' })).toHaveCount(0);
  await expect(other.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
  await other.close();
});

test('known fixed deadline clears in-memory presentation', async ({ page }) => {
  const deadline = Date.now() + 3000;
  await page.route('**:8001/auth/session', route => route.fulfill({ json: {
    account_id: randomUUID(), expires_at: new Date(deadline).toISOString(), created_at: new Date(deadline - 14 * 86400000).toISOString(),
  } }));
  await page.goto('/private');
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toBeVisible();
  await expect(page.getByRole('status')).toHaveText('Økten er utløpt. Logg inn på nytt.', { timeout: 6000 });
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeFocused();
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toHaveCount(0);
});

test('late login response cannot restore a locked presentation', async ({ page }) => {
  let release!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  await page.route('**:8001/auth/login', async route => { const response = await route.fetch(); await gate; await route.fulfill({ response }); });
  await page.goto('/private');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
  await page.getByLabel('Brukernavn', { exact: true }).fill(username);
  await page.getByLabel('Passord', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await page.evaluate(() => { document.cookie = 'private_logout_pending=1; Path=/; SameSite=Strict'; });
  await expect(page.getByRole('button', { name: 'Prøv utlogging igjen' })).toBeEnabled();
  release();
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toHaveCount(0);
  await page.getByRole('button', { name: 'Prøv utlogging igjen' }).click();
  await expect(page.getByRole('status')).toHaveText('Du er logget ut.');
});

test('committed delayed login settles before another tab can confirm logout', async ({ page, context }) => {
  await login(page);
  const other = await context.newPage();
  await other.route('**:8001/auth/session', route => route.fulfill({ status: 401, json: { detail: 'Logg inn på nytt.' } }));
  await other.goto('/private');
  await expect(other.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
  let release!: () => void;
  let committed!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const accepted = new Promise<void>(resolve => { committed = resolve; });
  let logoutSent = false;
  page.on('request', request => { if (request.url().endsWith('/auth/logout')) logoutSent = true; });
  await other.route('**:8001/auth/login', async route => {
    const response = await route.fetch();
    expect(response.status()).toBe(200);
    committed(); await gate; await route.fulfill({ response });
  });
  try {
    await other.getByLabel('Brukernavn', { exact: true }).fill(username);
    await other.getByLabel('Passord', { exact: true }).fill(password);
    await other.getByRole('button', { name: 'Logg inn', exact: true }).click();
    await accepted;
    await page.bringToFront();
    await expect(page.getByRole('heading', { name: 'Privat arbeidsrom' })).toBeVisible();
    await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
    await expect(page.getByRole('status')).toContainText('Utlogging er ikke bekreftet.');
    expect(logoutSent).toBe(false);
    release();
    await expect(page.getByRole('status')).toHaveText('Du er logget ut.');
    await other.unroute('**:8001/auth/session');
    await other.reload();
    await expect(other.getByLabel('Brukernavn', { exact: true })).toBeEnabled();
    expect((await context.request.get('http://127.0.0.1:8001/auth/session')).status()).toBe(401);
  } finally { release(); await other.close(); }
});

test('window switching preserves unfinished login input', async ({ page }) => {
  await page.goto('/private');
  const name = page.getByLabel('Brukernavn', { exact: true });
  const secret = page.getByLabel('Passord', { exact: true });
  await expect(name).toBeEnabled();
  await name.fill(username); await secret.fill(password);
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' });
    document.dispatchEvent(new Event('visibilitychange'));
    window.dispatchEvent(new Event('pagehide'));
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(name).toBeEnabled();
  await expect(name).toHaveValue(username); await expect(secret).toHaveValue(password);
});
