import { test, expect, openedPlan, post, API, setup, python, randomUUID, beforeUnload, relativeInstants } from './private-activity-helpers';
import { writeFileSync } from 'node:fs';
setup();
const management = (page: any) => page.getByRole('region', { name: 'Avviksvedlikehold', exact: true });
const feedback = (page: any) => page.getByRole('status', { name: 'Avviksstatus', exact: true });
async function open(page: any) { await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeVisible(); await expect(page.getByRole('button', { name: 'Hent lagrede avvik', exact: true })).toBeEnabled(); }
async function fill(page: any, title: string) {
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill(title);
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20, 24');
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04');
  await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
}
async function second(context: any, original: any) {
  const draft = structuredClone(original.draft); draft.service_date = '2031-01-03';
  for (const a of draft.activities) { a.start = a.start.replace('2031-01-03', '2031-01-04').replace('2031-01-02', '2031-01-03'); a.end = a.end.replace('2031-01-03', '2031-01-04').replace('2031-01-02', '2031-01-03'); }
  const saved = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft });
  const review = await post(context, '/workday-reviews', { draft_id: saved.id, expected_revision: 1 });
  return post(context, '/drafts/' + saved.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: review.unknowns.map((u: any) => u.id), classifications: {} });
}
async function navigateSecond(page: any) {
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne plan 2031-01-03 · versjon 1', exact: true }).click();
  await expect(page.getByText('Ingen aktivitet valgt', { exact: true })).toBeVisible();
}

test('one account incident appears on two days and survives original parent purge', async ({ page, context }) => {
  const { plan: a } = await openedPlan(page, context); const b = await second(context, a);
  await open(page); await fill(page, 'One shared incident');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(feedback(page)).toHaveText('Avviket er lagret.');
  const notice = (await (await context.request.get(API + '/notices')).json()).notices[0];
  expect(notice.valid_until).toBe('2031-01-04T23:59:59+01:00'); expect(notice.workday_id).toBeNull();
  await navigateSecond(page);
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
  await expect(reader.locator('summary')).toHaveCount(1); await expect(reader).toContainText('One shared incident');
  await reader.getByRole('button', { name: 'Til avviksvedlikehold', exact: true }).click();
  if (!await page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).isVisible()) await management(page).locator('summary').click();
  await page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).click(); await expect(feedback(page)).toHaveText('Kildekontrollen er lagret.');
  await page.getByRole('button', { name: 'Rediger One shared incident', exact: true }).click();
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-05');
  await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(feedback(page)).toHaveText('Avviket er lagret.');
  await expect(management(page)).toContainText('Kontrollert før siste endring:');
  for (const id of [a.id, b.id]) {
    const shared = (await (await context.request.get(API + '/workdays/' + id + '/notice-reader')).json()).candidates[0].notice;
    expect(shared.id).toBe(notice.id); expect(shared.valid_until).toBe('2031-01-05T23:59:59+01:00');
    expect(shared.expires_at).toBe('2031-01-12T22:59:59Z'); expect(shared.checked_revision).toBe(2); expect(shared.revision).toBe(3);
  }
  expect((await (await context.request.get(API + '/notices')).json()).notices).toHaveLength(1);
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  python(`with database() as conn:\n conn.execute('DELETE FROM workdays WHERE id=%s', (${JSON.stringify(a.id)},))\n`);
  await reader.getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click(); await expect(reader.locator('summary')).toHaveCount(1);
  for (const id of [b.id]) expect((await (await context.request.get(API + '/workdays/' + id + '/notice-reader')).json()).candidates[0].notice.id).toBe(notice.id);
  expect((await (await context.request.get(API + '/workdays/' + b.id + '/notice-reader')).json()).candidates[0].notice.checked_revision).toBe(2);
});

test('unsaved proposal and lost accepted original command survive changing days and original day expiry', async ({ page, context }) => {
  const { plan: a } = await openedPlan(page, context); await second(context, a);
  await open(page); await fill(page, 'Retained across days'); expect(await beforeUnload(page)).toBe(true);
  await navigateSecond(page); await open(page);
  await page.getByRole('button', { name: 'Tilbake til ulagret avvik', exact: true }).click();
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Retained across days');
  let writes = 0;
  await page.route('**:8001/notices', async route => { if (route.request().method() !== 'POST') { await route.continue(); return; } writes++; await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(feedback(page)).toContainText('uavklart');
  python(`with database() as conn:\n conn.execute('UPDATE workdays SET expires_at=clock_timestamp() WHERE id=%s', (${JSON.stringify(a.id)},))\n`);
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await open(page);
  await page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }).click(); await expect(feedback(page)).toHaveText('Avviket er lagret.');
  expect(writes).toBe(1); expect((await (await context.request.get(API + '/notices')).json()).notices).toHaveLength(1);
});

test('open reader automatically hides expiry and maintenance exposes distinct read-only history', async ({ page, context }) => {
  await page.addInitScript(() => { const original = Date.now; Date.now = () => original() - 2 * 3600000; });
  await openedPlan(page, context, true, -60);
  const ending = relativeInstants(6)[0];
  const receipt = await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { title: 'Short active incident', line_tags: ['20'], valid_until: ending } });
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
  await expect(reader.locator('summary')).toHaveCount(1);
  await page.evaluate(() => { const original = Date.now; Date.now = () => original() - 86400000; });
  await expect(reader.locator('summary')).toHaveCount(0, { timeout: 10000 });
  await reader.getByRole('button', { name: 'Til avviksvedlikehold', exact: true }).click();
  await expect(management(page).locator('summary')).toContainText('Utløpt'); await management(page).locator('summary').click();
  await expect(management(page).getByRole('button', { name: 'Rediger Short active incident', exact: true })).toHaveCount(0);
  const saved = (await (await context.request.get(API + '/notices/' + receipt.result.id)).json()); expect(saved.status).toBe('registered'); expect(saved.checked_at).toBeNull();
});

test('pending original notice recovery remains mounted when the displayed plan expires', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await fill(page, 'Retained after displayed plan expiry');
  let writes = 0;
  await page.route('**:8001/notices', async route => { if (route.request().method() !== 'POST') { await route.continue(); return; } writes++; await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(feedback(page)).toContainText('uavklart');
  python(`with database() as conn:\n conn.execute("UPDATE workdays SET expires_at=clock_timestamp()+interval '4 seconds' WHERE id=%s", (${JSON.stringify(plan.id)},))\n`);
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByRole('button', { name: 'Hent skift og aktivitetsstatus igjen', exact: true }).click();
  await open(page); await page.getByRole('button', { name: 'Tilbake til ulagret avvik', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0, { timeout: 10000 });
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Retained after displayed plan expiry'); expect(await beforeUnload(page)).toBe(true);
  await page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }).click(); await expect(feedback(page)).toHaveText('Avviket er lagret.');
  expect(writes).toBe(1); expect((await (await context.request.get(API + '/notices')).json()).notices).toHaveLength(1);
});

for (const night of [false, true]) test(`enlarged ${night ? 'Night' : 'Day'} account register ending feedback is readable`, async ({ page, context }) => {
  await openedPlan(page, context); await page.setViewportSize({ width: 390, height: 844 });
  await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
  if (night) await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await open(page); await fill(page, 'Langt kildevarsel ved et svært langt norsk stedsnavn');
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill('Første tidsvindu\nAndre tidsvindu\nBehold hele kildeinstruksjonen.');
  await expect(management(page)).toContainText('23:59:59'); await expect(management(page)).toContainText('Felles avviksregister');
  const control = page.getByRole('button', { name: 'Lagre avvik', exact: true }); await control.focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab'); await expect(control).toBeFocused(); await control.scrollIntoViewIfNeeded();
  const metrics = await control.evaluate((node: HTMLElement) => ({ overflow: document.documentElement.scrollWidth > innerWidth, height: node.getBoundingClientRect().height, focusWidth: parseFloat(getComputedStyle(node).outlineWidth), focusVisible: node.matches(':focus-visible') }));
  expect(metrics.overflow).toBe(false); expect(metrics.height).toBeGreaterThanOrEqual(58); expect(metrics.focusWidth).toBeGreaterThanOrEqual(2); expect(metrics.focusVisible).toBe(true);
  const prefix = '../docs/evidence/11-5-crossday-register-390-' + (night ? 'night' : 'day');
  await page.screenshot({ path: prefix + '.png', fullPage: true }); writeFileSync(prefix + '.json', JSON.stringify(metrics, null, 2));
});
