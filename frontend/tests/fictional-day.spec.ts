import { test, expect } from '@playwright/test';
import type { Page } from '@playwright/test';

async function assertOvernight(page: Page) {
  await expect(page.getByRole('heading', { name: 'Tjenestedato 2026-10-19' })).toBeVisible();
  await expect(page.getByText('Europe/Oslo', { exact: true })).toBeVisible();
  const trip = page.locator('li').first();
  await expect(trip).toContainText(/19\.10\.(?:20)?26\s*,?\s*23:30\s*–\s*20\.10\.(?:20)?26\s*,?\s*00:15/);
}

for (const width of [1440, 768]) {
  test(`keyboard save and real reload at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 1200 });
    await page.goto('/');
    await expect(page.getByRole('status')).toContainText('Ikke lagret');
    await expect(page.getByText('Fiktive demodata', { exact: true })).toBeVisible();
    await expect(page.getByText('Fysisk buss')).toBeVisible();
    await assertOvernight(page);
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Last inn nytt' })).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Lagre fiktiv dag', exact: true })).toBeFocused();
    const outline = await page.locator(':focus').evaluate(el => getComputedStyle(el).outlineWidth);
    expect(parseFloat(outline)).toBeGreaterThanOrEqual(3);
    await page.keyboard.press('Enter');
    await expect(page.getByRole('status')).toHaveText('Lagret og bekreftet av tjenesten.');
    const url = page.url();
    await page.reload();
    await expect(page.getByRole('status')).toHaveText('Lagret eksempel er hentet fra tjenesten.');
    expect(page.url()).toBe(url);
    await assertOvernight(page);
    await expect(page.getByText('Eksempelbyen', { exact: false })).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
    expect(await page.evaluate(() => localStorage.length)).toBe(0);
    await page.screenshot({ path: `../Docs/evidence/9-2-${width}.png`, fullPage: true });
  });
}

test('lost acknowledgement after commit preserves stable retry; unavailable reopen', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('status')).toContainText('Ikke lagret');
  let firstOperation = '';
  let accepted: { id: string; created_at: string } | undefined;
  await page.route('**/days', async route => {
    firstOperation = route.request().postDataJSON().operation_id;
    const response = await route.fetch();
    expect(response.status()).toBe(200);
    accepted = await response.json();
    await route.abort('failed'); // The actual API committed; only the acknowledgement is lost.
  });
  await page.getByRole('button', { name: 'Lagre fiktiv dag', exact: true }).click();
  await expect(page.getByRole('status')).toContainText('Lagring er ikke bekreftet');
  await expect(page.getByText('Eksempelbyen', { exact: false })).toBeVisible();
  await page.unroute('**/days');
  await page.route('**/days', async route => {
    expect(route.request().postDataJSON().operation_id).toBe(firstOperation);
    const response = await route.fetch();
    expect(response.status()).toBe(200);
    const replayed = await response.json();
    expect(replayed).toEqual(accepted); // Same record, creation time and fixed deadline, no second creation.
    await route.fulfill({ response });
  });
  await page.getByRole('button', { name: 'Lagre fiktiv dag', exact: true }).click();
  await expect(page.getByRole('status')).toHaveText('Lagret og bekreftet av tjenesten.');
  expect(new URL(page.url()).searchParams.get('day')).toBe(accepted?.id);
  await page.route('**/days/*', route => route.abort('failed'));
  await page.getByRole('button', { name: 'Åpne lagret dag på nytt' }).click();
  await expect(page.getByRole('status')).toContainText('Henting er ikke bekreftet');
  await expect(page.getByText('Bekreftet lagret', { exact: false })).toBeVisible();
  await expect(page.getByText('Eksempelbyen', { exact: false })).toBeVisible();
});

test('HTML and malformed JSON never count as a saved acknowledgement', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('status')).toContainText('Ikke lagret');
  for (const contentType of ['text/html', 'application/json']) {
    await page.route('**/days', route => route.fulfill({ status: 200, contentType,
      body: contentType === 'text/html' ? '<h1>Login</h1>' : '{"id":"invalid"}' }));
    await page.getByRole('button', { name: 'Lagre fiktiv dag', exact: true }).click();
    await expect(page.getByRole('status')).toContainText('Lagring er ikke bekreftet');
    expect(new URL(page.url()).searchParams.get('day')).toBeNull();
    await page.unroute('**/days');
  }
});

for (const invalid of ['future-created', 'reversed', 'expired', 'invalid-lifetime', 'nonsense', 'impossible-date', 'wrong-id']) {
  test(`reopen rejects ${invalid} response`, async ({ page, request }) => {
    const day = await (await request.get('http://127.0.0.1:8000/fixture')).json();
    const operation = await (await request.post('http://127.0.0.1:8000/operations')).json();
    const saved = await (await request.post('http://127.0.0.1:8000/days', { data: { operation_id: operation.operation_id, day } })).json();
    const now = Date.now();
    const invalidSaved = { ...saved };
    if (invalid === 'future-created') invalidSaved.created_at = new Date(now + 3600000).toISOString();
    if (invalid === 'reversed') invalidSaved.expires_at = new Date(Date.parse(saved.created_at) - 1000).toISOString();
    if (invalid === 'expired') { invalidSaved.created_at = new Date(now - 2000).toISOString(); invalidSaved.expires_at = new Date(now - 1000).toISOString(); }
    if (invalid === 'invalid-lifetime') invalidSaved.expires_at = new Date(Date.parse(saved.created_at) + 365 * 86400000).toISOString();
    if (invalid === 'nonsense') invalidSaved.created_at = 'not-a-date';
    if (invalid === 'impossible-date') invalidSaved.created_at = '2026-02-30T12:00:00Z';
    if (invalid === 'wrong-id') invalidSaved.id = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
    await page.route('**/days/*', route => route.fulfill({ json: invalidSaved }));
    await page.goto('/?day=' + saved.id);
    await expect(page.getByRole('status')).toContainText('Henting er ikke bekreftet');
    await expect(page.locator('section')).toHaveCount(0);
    await expect(page.getByText('Bekreftet lagret', { exact: false })).toHaveCount(0);
    expect(new URL(page.url()).searchParams.get('day')).toBe(saved.id);
  });
}

test('410 clears previously acknowledged state and permits new example', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('status')).toContainText('Ikke lagret');
  await page.getByRole('button', { name: 'Lagre fiktiv dag', exact: true }).click();
  await expect(page.getByRole('status')).toHaveText('Lagret og bekreftet av tjenesten.');
  await page.route('**/days/*', route => route.fulfill({ status: 410, json: { detail: 'expired' } }));
  await page.getByRole('button', { name: 'Åpne lagret dag på nytt' }).click();
  await expect(page.getByRole('status')).toContainText('Utløpt eller ukjent');
  await expect(page.locator('section')).toHaveCount(0);
  await expect(page.getByText('Bekreftet lagret', { exact: false })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Åpne lagret dag på nytt' })).toBeDisabled();
  expect(new URL(page.url()).searchParams.get('day')).toBeNull();
  await page.getByRole('button', { name: 'Last inn nytt' }).click();
  await expect(page.getByRole('status')).toContainText('Ikke lagret');
});

test('known expiry clears displayed day without another request', async ({ page }) => {
  await page.clock.install();
  await page.goto('/');
  await expect(page.getByRole('status')).toContainText('Ikke lagret');
  await page.route('**/days', async route => {
    const response = await route.fetch();
    const result = await response.json();
    result.expires_at = new Date(Date.now() + 60000).toISOString();
    result.created_at = new Date(Date.parse(result.expires_at) - 7 * 86400000).toISOString();
    await route.fulfill({ json: result });
  });
  await page.getByRole('button', { name: 'Lagre fiktiv dag', exact: true }).click();
  await expect(page.getByRole('status')).toHaveText('Lagret og bekreftet av tjenesten.');
  await page.clock.fastForward(61000);
  await expect(page.getByRole('status')).toContainText('Utløpt eller ukjent');
  await expect(page.locator('section')).toHaveCount(0);
  await expect(page.getByText('Bekreftet lagret', { exact: false })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Åpne lagret dag på nytt' })).toBeDisabled();
  expect(new URL(page.url()).searchParams.get('day')).toBeNull();
});
