import { test, expect, openedPlan, post, API, setup, randomUUID, beforeUnload, relativeInstants } from './private-activity-helpers';
setup();
const feedback = (page: any) => page.getByRole('status', { name: 'Avviksstatus', exact: true });
const retry = (page: any) => page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true });
const content = (extra = {}) => ({ title: 'Integration incident', line_tags: ['20'], valid_until: '2031-01-04T23:59:59+01:00', ...extra });
async function open(page: any) {
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await expect(feedback(page)).toHaveText('Lagrede avvik er hentet.');
}
async function create(page: any, ending = '2031-01-04T23:59:59+01:00') {
  await open(page); await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Retained integration proposal');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20');
  await page.getByLabel('Gyldig tildato', { exact: true }).fill(ending.slice(0, 10));
  await page.getByLabel('Gyldig til: klokkeslett', { exact: true }).fill(ending.slice(11, 19));
  await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
  await expect(page.getByRole('button', { name: 'Lagre avvik', exact: true })).toBeEnabled();
}

for (const code of [409, 422, 429]) test(`notice committed behind HTML ${code} and typed-looking lookup rejection retains one original effect`, async ({ page, context }) => {
  await openedPlan(page, context); await create(page); const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  const writes: any[] = [];
  await page.route('**:8001/notices', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    writes.push(route.request().postDataJSON()); await route.fetch();
    await route.fulfill({ status: code, contentType: 'text/html', body: '<html>proxy error</html>' });
  });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(retry(page)).toBeEnabled(); await expect(feedback(page)).toContainText('uavklart');
  const detail = code === 409 ? 'Lagret avvik er endret. Hent og gjennomgå på nytt.' : code === 422 ? 'Kontroller feltene.' : { code: 'notice_capacity', message: 'Registeret har allerede 200 avvik.' };
  await page.route('**:8001/workday-notice-operations/*', route => route.fulfill({ status: code, json: { detail } }));
  for (let attempt = 0; attempt < 2; attempt++) {
    await retry(page).click(); await expect(retry(page)).toBeEnabled();
    await expect(feedback(page)).toContainText('uavklart');
    await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Retained integration proposal');
    await expect(page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true })).toBeDisabled();
    expect(writes).toHaveLength(1);
  }
  await page.unroute('**:8001/workday-notice-operations/*');
  await retry(page).click(); await expect(feedback(page)).toHaveText('Avviket er lagret.');
  const records = (await (await context.request.get(API + '/notices')).json()).notices;
  expect(records).toHaveLength(1); expect(records[0].revision).toBe(1);
  const receipt = await (await context.request.get(API + '/workday-notice-operations/' + writes[0].operation_id)).json();
  expect(receipt.result).toEqual(records[0]); expect(writes).toHaveLength(1); expect(errors).toEqual([]);
});

test('unaccepted create past its ending is never dispatched again and proposal can be discarded', async ({ page, context }) => {
  test.setTimeout(45000); await openedPlan(page, context);
  const ending = relativeInstants(8)[0]; await create(page, ending);
  let writes = 0, lookups = 0, current = 0;
  await page.route('**:8001/notices', route => { if (route.request().method() === 'POST') { writes++; return route.abort(); } current++; return route.continue(); });
  await page.route('**:8001/workday-notice-operations/*', route => { lookups++; return route.continue(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(retry(page)).toBeEnabled();
  await expect.poll(() => Date.now() > Date.parse(ending), { timeout: 12000 }).toBe(true);
  await retry(page).click(); await expect(feedback(page)).toContainText('kan ikke gjenopprettes');
  expect(writes).toBe(1); expect(lookups).toBeGreaterThan(0); expect(current).toBeGreaterThan(0);
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Retained integration proposal');
  await expect(retry(page)).toHaveCount(0);
  await page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true }).click();
  expect(await beforeUnload(page)).toBe(false);
  expect((await (await context.request.get(API + '/notices')).json()).notices).toEqual([]);
});

test('lost accepted source check resolves after automatic ending without reopening writes', async ({ page, context }) => {
  test.setTimeout(45000); await openedPlan(page, context);
  const ending = relativeInstants(8)[0];
  const notice = (await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: content({ valid_until: ending }) })).result;
  await open(page); await page.locator('.notice-list summary').click(); let writes = 0;
  await page.route('**:8001/notices/' + notice.id + '/check', async route => { writes++; await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).click(); await expect(retry(page)).toBeEnabled();
  await expect.poll(() => Date.now() > Date.parse(ending), { timeout: 12000 }).toBe(true);
  await retry(page).click(); await expect(feedback(page)).toHaveText('Kildekontrollen er lagret.');
  expect(writes).toBe(1); await expect(page.locator('.notice-list summary')).toContainText('Utløpt');
  await expect(page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Rediger ' + notice.title, exact: true })).toHaveCount(0);
  const saved = await (await context.request.get(API + '/notices/' + notice.id)).json();
  expect(saved.revision).toBe(2); expect(saved.checked_revision).toBe(2); expect(saved.valid_until).toBe(ending);
});

for (const surface of ['reader', 'maintenance']) test(`held ${surface} response cannot restart already elapsed notice validity`, async ({ page, context }) => {
  test.setTimeout(45000); await openedPlan(page, context, true, -60);
  const ending = relativeInstants(5)[0];
  await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: content({ valid_until: ending }) });
  const path = surface === 'reader' ? '**:8001/workdays/*/notice-reader' : '**:8001/notices';
  let release!: () => void, received!: () => void;
  const gate = new Promise<void>(resolve => release = resolve), entered = new Promise<void>(resolve => received = resolve);
  await page.route(path, async route => { const response = await route.fetch(); received(); await gate; await route.fulfill({ response }); });
  try {
    await page.getByRole('button', { name: surface === 'reader' ? 'Les avvik for linjer og datoer' : 'Manuelt vedlikeholdte avvik', exact: true }).click();
    await entered; await expect.poll(() => Date.now() > Date.parse(ending) + 200, { timeout: 9000 }).toBe(true); release();
    if (surface === 'reader') {
      const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
      await expect(reader.getByRole('status')).toHaveText('Lagrede avvik er hentet.');
      await expect(reader.locator('summary')).toHaveCount(0, { timeout: 500 });
    } else {
      await expect(feedback(page)).toHaveText('Lagrede avvik er hentet.');
      await expect(page.locator('.notice-list summary')).toContainText('Utløpt', { timeout: 500 });
      await page.locator('.notice-list summary').click();
      await expect(page.getByRole('button', { name: 'Rediger Integration incident', exact: true })).toHaveCount(0);
    }
  } finally { release(); }
});
