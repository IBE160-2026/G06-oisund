import { test, expect, openedPlan, post, API, setup, python, randomUUID, beforeUnload } from './private-activity-helpers';
import { editor } from './private-screen-helpers';
import { writeFileSync } from 'node:fs';
setup();
test.use({ actionTimeout: 15000 });
const feedback = (page: any) => page.getByRole('status', { name: 'Avviksstatus', exact: true });
const examples = [
  { title: 'Syntetisk SMS om midlertidig holdeplass', summary: 'Bruk midlertidig holdeplass ved kaia.', description: '2. januar 2031: Linje 20 mot nord bruker kaia.\n3. januar 2031: Linje 24 mot sør bruker biblioteket.\nDette er et uavhengig syntetisk aksepteksempel.', source_note: 'Syntetisk SMS fra trafikkleder; ingen nettadresse.', source_url: null, line_scope: 'selected', line_tags: ['20', '24'] },
  { title: 'Syntetisk delt lenke med lang instruksjon', summary: 'Felles melding for alle linjer.', description: Array(24).fill('Uavhengig skrevet norsk instruksjon: gå gjennom skilting mens bussen står stille.').join('\n'), source_note: 'Syntetisk eksempel med delt lenke.', source_url: 'https://example.invalid/delt-melding', line_scope: 'all', line_tags: [] },
];
async function open(page: any) {
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Hent lagrede avvik', exact: true })).toBeEnabled();
}
async function fill(page: any, item: typeof examples[number]) {
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04');
  await page.getByLabel('Tittel', { exact: true }).fill(item.title);
  await page.getByLabel('Kort forklaring', { exact: true }).fill(item.summary);
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill(item.description);
  await page.getByLabel('Kildebeskrivelse', { exact: true }).fill(item.source_note);
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill(item.source_url ?? '');
  await page.getByLabel('Linjeomfang', { exact: true }).selectOption(item.line_scope);
  if (item.line_scope === 'selected') await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill(item.line_tags.join(', '));
}

test('D2 A7 independent synthetic source shapes survive cross-day reading and parent removal/expiry', async ({ page, context }, testInfo) => {
  const { plan: a } = await openedPlan(page, context);
  const original = await (await context.request.get(API + '/drafts/' + a.source_draft_id)).json();
  const content = structuredClone(original.draft); content.service_date = '2031-01-03';
  for (const activity of content.activities) for (const field of ['start', 'end']) activity[field] = activity[field].replace('2031-01-03', '2031-01-04').replace('2031-01-02', '2031-01-03');
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: content });
  const review = await post(context, '/workday-reviews', { draft_id: draft.id, expected_revision: 1 });
  const b = await post(context, '/drafts/' + draft.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: review.unknowns.map((u: any) => u.id), classifications: {} });
  const commands: any[] = [];
  page.on('request', request => { if (request.method() === 'POST' && new URL(request.url()).pathname === '/notices') commands.push(request.postDataJSON()); });
  await open(page);
  for (const item of examples) {
    await fill(page, item);
    const response = page.waitForResponse(reply => reply.request().method() === 'POST' && new URL(reply.url()).pathname === '/notices' && reply.status() === 200);
    await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await response;
    await expect(feedback(page)).toHaveText('Avviket er lagret.');
    await expect(page.getByRole('button', { name: 'Registrer avvik', exact: true })).toBeEnabled();
  }
  const saved = (await (await context.request.get(API + '/notices')).json()).notices;
  for (const item of examples) {
    const row = saved.find((n: any) => n.title === item.title);
    expect(row).toMatchObject({ ...item, valid_from: null, source_updated_at: null, checked_at: null, workday_id: null, revision: 1, valid_until: '2031-01-04T23:59:59+01:00' });
  }
  const receipts = await Promise.all(commands.map(async command => (await context.request.get(API + '/workday-notice-operations/' + command.operation_id)).json()));
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne plan 2031-01-03 · versjon 1', exact: true }).click();
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
  await expect(reader.locator('summary')).toHaveCount(2);
  for (const item of examples) await expect(reader).toContainText(item.title);
  for (const item of await reader.locator('summary').all()) await item.click();
  await page.screenshot({ path: testInfo.outputPath('a7-independent-synthetic-examples.png'), fullPage: true });
  await post(context, '/workdays/' + a.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
  expect((await (await context.request.get(API + '/notices')).json()).notices).toEqual(saved);
  // Controlled expiry changes only this synthetic parent; notices/receipts are independent.
  python(`with database() as conn:\n conn.execute("UPDATE workdays SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (${JSON.stringify(b.id)},))\n`);
  expect([404, 410]).toContain((await context.request.get(API + '/workdays/' + b.id)).status());
  expect((await (await context.request.get(API + '/notices')).json()).notices).toEqual(saved);
  for (let i = 0; i < commands.length; i++) expect(await (await context.request.get(API + '/workday-notice-operations/' + commands[i].operation_id)).json()).toEqual(receipts[i]);
  writeFileSync(testInfo.outputPath('a7-result.json'), JSON.stringify({ synthetic: true, examples, parentADeleted: a.id, parentBControlledExpiry: b.id, saved, receipts }, null, 2));
});

for (const concurrent of [false, true]) test(`D2 A8 accepted notice update retains identity through proxy and failed lookup concurrent=${concurrent}`, async ({ page, context }) => {
  await openedPlan(page, context);
  const item = examples[0];
  const initial = await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { ...item, valid_until: '2031-01-04T23:59:59+01:00', source_updated_at: null, valid_from: null } });
  await open(page); await page.locator('.notice-list summary').click();
  await page.getByRole('button', { name: 'Rediger ' + item.title, exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Syntetisk endret etter faktisk lagring');
  const writes: any[] = [];
  await page.route('**:8001/notices/' + initial.result.id, async route => { if (route.request().method() !== 'POST') return route.continue(); writes.push(route.request().postDataJSON()); await route.fetch(); await route.fulfill({ status: 502, contentType: 'text/html', body: '<html>synthetic lost accepted update</html>' }); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(feedback(page)).toContainText('uavklart');
  await page.route('**:8001/workday-notice-operations/*', route => route.fulfill({ status: 503, json: { detail: 'Synthetic lookup unavailable' } }));
  const failedLookup = page.waitForResponse(reply => new URL(reply.url()).pathname.startsWith('/workday-notice-operations/') && reply.status() === 503);
  await page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }).click(); await failedLookup;
  await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toBeEnabled();
  await expect(feedback(page)).toContainText('uavklart'); expect(writes).toHaveLength(1);
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Syntetisk endret etter faktisk lagring');
  const third = concurrent ? await post(context, '/notices/' + initial.result.id, { operation_id: randomUUID(), expected_revision: 2, content: { ...item, title: 'Nyere uavhengig endring i annet vindu', valid_until: '2031-01-04T23:59:59+01:00', source_updated_at: null, valid_from: null } }) : null;
  await page.unroute('**:8001/workday-notice-operations/*');
  await page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true }).click();
  if (concurrent) {
    await expect(feedback(page)).toContainText('Et nyere avvik finnes.');
    await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Syntetisk endret etter faktisk lagring');
    await expect(page.getByText('Nyere lagret avvik', { exact: true })).toBeVisible();
  } else await expect(feedback(page)).toHaveText('Avviket er lagret.');
  expect(writes).toHaveLength(1);
  const current = await (await context.request.get(API + '/notices/' + initial.result.id)).json();
  expect(current.revision).toBe(concurrent ? 3 : 2); expect(current.title).toBe(concurrent ? 'Nyere uavhengig endring i annet vindu' : 'Syntetisk endret etter faktisk lagring');
  if (concurrent) expect(current).toEqual(third.result);
  const receipt = await (await context.request.get(API + '/workday-notice-operations/' + writes[0].operation_id)).json();
  expect(receipt.result.revision).toBe(2); expect(receipt.result.title).toBe('Syntetisk endret etter faktisk lagring');
  if (!concurrent) expect(receipt.result).toEqual(current);
  expect(receipt.operation_id).toBe(writes[0].operation_id);
});

for (const [code, detail] of [[409, 'Slettingsforsøket har annet innhold.'], [410, 'Slettingsforsøket er utløpt.']] as const) test(`D2 A8 accepted draft deletion lookup ${code} is not a mutation rejection`, async ({ page, context }) => {
  const { draft } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click(); await editor(page);
  const writes: any[] = [];
  await page.route('**:8001/drafts/' + draft.id + '/delete', async route => { writes.push(route.request().postDataJSON()); await route.fetch(); await route.abort(); });
  page.once('dialog', dialog => dialog.accept()); await page.getByRole('button', { name: 'Slett utkast', exact: true }).click();
  const status = page.getByRole('status', { name: 'Lagringsstatus', exact: true });
  await expect(status).toContainText('Sletting er ikke bekreftet.');
  await page.route('**:8001/draft-deletions/*', route => route.fulfill({ status: code, json: { detail } }));
  await page.getByRole('button', { name: 'Kontroller slettingen', exact: true }).click();
  await expect(status).toContainText('Sletting er ikke bekreftet.');
  await expect(page.getByRole('button', { name: 'Kontroller slettingen', exact: true })).toBeEnabled();
  await expect.poll(() => beforeUnload(page)).toBe(true); expect(writes).toHaveLength(1);
  await page.unroute('**:8001/draft-deletions/*');
  await page.getByRole('button', { name: 'Kontroller slettingen', exact: true }).click();
  await expect(status).toHaveText('Utkastet er slettet.'); expect(writes).toHaveLength(1);
  expect(await (await context.request.get(API + '/draft-deletions/' + writes[0].operation_id)).json()).toEqual({ deleted_id: draft.id });
});
