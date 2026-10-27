import { test, expect, openedPlan, setup, python, API, post } from './private-activity-helpers';
setup();
const feedback = (page: any) => page.getByRole('status', { name: 'Avviksstatus', exact: true });
async function proposal(page: any, context: any) {
  await openedPlan(page, context);
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Synthetic retained proposal');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20');
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04');
  await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
}

test('lost issuance response retains proposal and sends no create until explicit retry', async ({ page, context }) => {
  await proposal(page, context);
  let creates = 0;
  page.on('request', r => { if (r.method() === 'POST' && r.url() === API + '/notices') creates++; });
  await page.route('**:8001/notice-operations', async route => { await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(feedback(page)).toContainText('Forslaget er beholdt.');
  expect(creates).toBe(0);
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Synthetic retained proposal');
  await page.unroute('**:8001/notice-operations');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(feedback(page)).toHaveText('Avviket er lagret.');
  expect(creates).toBe(1);
});

test('expired creation admission rejects without receipt and releases retained proposal', async ({ page, context }) => {
  await proposal(page, context);
  await page.route('**:8001/notice-operations', async route => {
    const response = await route.fetch(); const issued = await response.json();
    python(`with database() as conn:\n conn.execute("UPDATE notice_creation_admissions SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (${JSON.stringify(issued.operation_id)},))\n`);
    await route.fulfill({ response });
  });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(feedback(page)).toContainText('Et lokalt forslag er beholdt');
  await expect(page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true })).toHaveCount(0);
  expect((await (await context.request.get(API + '/notices')).json()).notices).toEqual([]);
  await page.unroute('**:8001/notice-operations');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(feedback(page)).toHaveText('Avviket er lagret.');
});

test('extremely slow device clock does not overflow session or draft expiry timers', async ({ page, context }) => {
  await page.clock.setFixedTime(new Date('2000-01-01T00:00:00Z'));
  await openedPlan(page, context);
  await page.waitForTimeout(100);
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: /^Åpne 2031-01-02/ }).click();
  await page.waitForTimeout(100);
  await expect(page.getByText('Utkastet er utløpt.', { exact: false })).toHaveCount(0);
  expect(await page.evaluate(() => ({ local: localStorage.length, session: sessionStorage.length }))).toEqual({ local: 0, session: 0 });
});


test('fixed device clock clears a short real server session deadline without revalidation', async ({ page, context }) => {
  await page.clock.setFixedTime(new Date('2000-01-01T00:00:00Z'));
  await openedPlan(page, context);
  const session = await (await context.request.get(API + '/auth/session')).json();
  python(`with database() as conn:\n conn.execute("UPDATE sessions SET expires_at=statement_timestamp()+interval '5 seconds',created_at=statement_timestamp()+interval '5 seconds'-interval '14 days' WHERE owner=%s", (${JSON.stringify(session.account_id)},))\n`);
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom', exact: true })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom', exact: true })).toHaveCount(0, { timeout: 8000 });
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  await expect.poll(async () => (await context.request.get(API + '/auth/session')).status()).toBe(401);
  expect(await page.evaluate(() => [localStorage.length, sessionStorage.length])).toEqual([0, 0]);
});

for (const imported of [false, true]) test(`fixed device clock clears expired saved ${imported ? 'imported' : 'manual'} draft fields`, async ({ page, context }) => {
  await page.clock.setFixedTime(new Date('2000-01-01T00:00:00Z'));
  await openedPlan(page, context);
  let content: any = { activities: [], vehicle_duty: null, realtime_duty: null };
  if (imported) {
    const pdf = Buffer.from(python(`import sys,base64\nsys.path.insert(0,'/app/tests')\nfrom test_pdf_import import synthetic_text_pdf\nprint(base64.b64encode(synthetic_text_pdf()).decode())\n`).trim(), 'base64');
    const proof = await (await context.request.get(API + '/auth/csrf')).json();
    const response = await context.request.post(API + '/imports/pdf', { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token, 'Content-Type': 'application/pdf' }, data: pdf });
    expect(response.status()).toBe(200);
    content = await response.json();
  }
  Object.assign(content, { service_date: '2032-02-03', physical_bus: 'Synthetic retained field' });
  const saved = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: content });
  python(`with database() as conn:\n conn.execute("UPDATE drafts SET expires_at=statement_timestamp()+interval '5 seconds',created_at=statement_timestamp()+interval '5 seconds'-interval '7 days' WHERE id=%s", (${JSON.stringify(saved.id)},))\n`);
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: /^\u00c5pne 2032-02-03/ }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Synthetic retained field');
  if (imported) await expect(page.locator('.source-disclosure')).toHaveCount(1);
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('', { timeout: 8000 });
  await expect(page.locator('.source-disclosure')).toHaveCount(0);
  await expect(page.getByLabel('Starttid', { exact: true })).toHaveCount(0);
  // Retention loss clears this saved presentation, then a fresh unrelated
  // unsaved proposal remains available under the still-live account session.
  await page.getByLabel('Buss/vogn', { exact: true }).fill('Fresh unrelated proposal');
  await page.waitForTimeout(1200);
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Fresh unrelated proposal');
});


for (const editor of [false, true]) test(`fixed device clock removes notice ${editor ? 'editor' : 'readable history'} only at storage retention`, async ({ page, context }) => {
  await page.clock.setFixedTime(new Date('2000-01-01T00:00:00Z'));
  await openedPlan(page, context);
  const created = await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { title: 'Synthetic expiring notice', line_tags: ['20'], valid_until: '2031-01-04', description: 'Private retained description' } });
  // History remains readable until its own bound; selected days/sessions stay live.
  python(`with database() as conn:\n conn.execute("UPDATE workday_notices SET expires_at=statement_timestamp()+interval '6 seconds'${editor ? '' : ",valid_until=statement_timestamp()-interval '1 second'"} WHERE id=%s", (${JSON.stringify(created.result.id)},))\n`);
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await page.locator('.notice-list summary').click();
  await expect(page.locator('.notice-list')).toContainText('Private retained description');
  if (editor) {
    await page.getByRole('button', { name: 'Rediger Synthetic expiring notice', exact: true }).click();
    await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Synthetic expiring notice');
  }
  await expect(page.locator('.notice-list summary')).toHaveCount(0, { timeout: 9000 });
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveCount(0);
  await expect(page.getByText('Private retained description', { exact: false })).toHaveCount(0);
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom', exact: true })).toBeVisible();
  // A fresh unsaved proposal has no association to the expired saved notice.
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Fresh unrelated notice proposal');
  await page.waitForTimeout(1200);
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Fresh unrelated notice proposal');
});


test('fixed device clock removes reader payload at independent notice storage retention', async ({ page, context }) => {
  await page.clock.setFixedTime(new Date('2000-01-01T00:00:00Z'));
  await openedPlan(page, context);
  const created = await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { title: 'Synthetic expiring reader notice', line_tags: ['20'], valid_until: '2031-01-04', description: 'Private reader description' } });
  python(`with database() as conn:\n conn.execute("UPDATE workday_notices SET expires_at=statement_timestamp()+interval '6 seconds' WHERE id=%s", (${JSON.stringify(created.result.id)},))\n`);
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
  await expect(reader.locator('summary')).toHaveCount(1);
  await reader.locator('summary').click();
  await expect(reader).toContainText('Private reader description');
  await expect(reader.locator('summary')).toHaveCount(0, { timeout: 9000 });
  await expect(reader).not.toContainText('Private reader description');
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom', exact: true })).toBeVisible();
});


test('fixed device clock clears a confirmed plan at its known server deadline without revalidation', async ({ page, context }) => {
  const frozen = '2000-01-01T00:00:00Z';
  await page.clock.setFixedTime(new Date(frozen));
  const { plan } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  const deadline = python(`with database() as conn:\n row=conn.execute("UPDATE workdays SET expires_at=statement_timestamp()+interval '8 seconds' WHERE id=%s RETURNING expires_at", (${JSON.stringify(plan.id)},)).fetchone()\n print(row['expires_at'].isoformat())\n`).trim();
  // Establish the shortened authority once. From the settled open response
  // onward, no refresh, request or revalidation may cause the disappearance.
  await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  const opened = page.waitForResponse(response => response.url() === API + '/workdays/' + plan.id && response.request().method() === 'GET');
  await page.getByRole('button', { name: /^\u00c5pne plan 2031-01-02/ }).click();
  expect(Date.parse((await (await opened).json()).expires_at)).toBe(Date.parse(deadline));
  const presentation = page.getByRole('region', { name: 'Bekreftet plan', exact: true });
  await expect(presentation).toBeVisible();
  await page.waitForLoadState('networkidle');
  // Prevent queued child-resource loads from obtaining any further authority.
  // A pending transport cannot hide/unmount the plan through an error reply;
  // only the established in-memory retention deadline can remove it.
  await page.evaluate(() => { window.fetch = () => new Promise<Response>(() => {}); });
  const requests: string[] = [];
  const observe = (request: any) => requests.push(request.url());
  page.on('request', observe);
  await expect(presentation).toHaveCount(0, { timeout: 11000 });
  page.off('request', observe);
  expect(requests).toEqual([]);
  expect(await page.evaluate(() => Date.now())).toBe(Date.parse(frozen));
  await expect(page.getByRole('heading', { name: 'Privat arbeidsrom', exact: true })).toBeVisible();
  expect((await context.request.get(API + '/auth/session')).status()).toBe(200);
});
