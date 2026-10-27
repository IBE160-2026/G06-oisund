import { test, expect, openedPlan, post, API, setup, python, randomUUID, beforeUnload, relativeInstants, account } from './private-activity-helpers';
setup();
const status = (page: any) => page.getByRole('status', { name: 'Avviksstatus', exact: true });
const noticeContent = (extra = {}) => ({ title: 'Review incident', line_tags: ['20'], valid_until: '2031-01-04T23:59:59+01:00', ...extra });
async function seed(context: any, extra = {}) { return (await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: noticeContent(extra) })).result; }
async function open(page: any) { await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await expect(status(page)).toHaveText('Lagrede avvik er hentet.'); }
async function edit(page: any, notice: any, title = 'Retained local proposal') {
  await open(page); await page.locator('.notice-list summary').click();
  await page.getByRole('button', { name: 'Rediger ' + notice.title, exact: true }).click(); await page.getByLabel('Tittel', { exact: true }).fill(title);
}

test('historical legacy recovery accepts past receipt lease and SET NULL provenance after original parent deletion', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const notice = await seed(context);
  python(`with database() as conn:\n conn.execute("UPDATE workday_notices SET workday_id=%s,entered_at='2019-01-01',edited_at='2019-01-01' WHERE id=%s", (${JSON.stringify(plan.id)},${JSON.stringify(notice.id)}))\n`);
  await edit(page, notice, 'Recovered legacy edit'); let writes = 0, operation = '';
  await page.route('**:8001/notices/' + notice.id, async route => {
    if (route.request().method() !== 'POST') { await route.continue(); return; }
    writes++; const body = route.request().postDataJSON(); operation = body.operation_id;
    // Model the pre-migration accepted edit: complete deployed receipt JSON,
    // immutable old lease, independently extended live metadata, then SET NULL.
    python(`import json\nfrom app.workday_notice_domain import NoticeRecord,SaveNotice\nfrom app.draft_storage import fingerprint\nfrom psycopg.types.json import Jsonb\nbody=json.loads(${JSON.stringify(JSON.stringify(body))})\nwith database() as conn:\n row=conn.execute("UPDATE workday_notices SET title=%s,revision=2,edited_at='2019-01-02' WHERE id=%s RETURNING *", (body['content']['title'],${JSON.stringify(notice.id)})).fetchone()\n result=NoticeRecord(**{key:row[key] for key in NoticeRecord.model_fields}).model_dump(mode='json')\n result['expires_at']='2020-01-10T00:00:00Z'\n legacy=SaveNotice(**body,expected_lifecycle_revision=0).model_dump(mode='json',exclude={'content':{'summary','description','source_note','line_scope'}})\n digest=fingerprint(row['workday_id'],{'action':'save','notice_id':str(row['id']),**legacy})\n conn.execute('INSERT INTO workday_notice_operations VALUES(%s,%s,%s,%s,%s,%s)',(body['operation_id'],row['owner'],row['workday_id'],digest,Jsonb(result),row['expires_at']))\n conn.execute('DELETE FROM workdays WHERE id=%s',(${JSON.stringify(plan.id)},))\n`);
    await route.abort();
  });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toBeEnabled();
  const historical = await (await context.request.get(API + '/workday-notice-operations/' + operation)).json();
  expect(historical.result.expires_at).toBe('2020-01-10T00:00:00Z'); expect(historical.result.workday_id).toBe(plan.id);
  await page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.');
  expect(writes).toBe(1); expect(await beforeUnload(page)).toBe(false);
  const current = await (await context.request.get(API + '/notices/' + notice.id)).json();
  expect(current.workday_id).toBeNull(); expect(current.revision).toBe(2); expect(current.title).toBe('Recovered legacy edit');
  expect(await (await context.request.get(API + '/workday-notice-operations/' + operation)).json()).toEqual(historical);
});

test('different non-null provenance in a recovered receipt never establishes acceptance', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const notice = await seed(context);
  python(`with database() as conn:\n conn.execute('UPDATE workday_notices SET workday_id=%s WHERE id=%s',(${JSON.stringify(plan.id)},${JSON.stringify(notice.id)}))\n`);
  await edit(page, notice);
  await page.route('**:8001/notices/' + notice.id, async route => { await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toBeEnabled();
  await page.route('**:8001/workday-notice-operations/*', async route => { const response = await route.fetch(), value = await response.json(); value.result.workday_id = randomUUID(); await route.fulfill({ json: value }); });
  await page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true }).click(); await expect(status(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toBeEnabled();
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Retained local proposal');
  await page.unroute('**:8001/workday-notice-operations/*');
  await page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.');
});

test('more than 200 retained legacy incidents remain completely maintainable and readable', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  const draft = structuredClone(plan.draft); draft.service_date = '2031-01-03';
  for (const a of draft.activities) { a.start = a.start.replace('2031-01-03', '2031-01-04').replace('2031-01-02', '2031-01-03'); a.end = a.end.replace('2031-01-03', '2031-01-04').replace('2031-01-02', '2031-01-03'); }
  const saved = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft });
  const review = await post(context, '/workday-reviews', { draft_id: saved.id, expected_revision: 1 });
  const second = await post(context, '/drafts/' + saved.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: review.unknowns.map((u: any) => u.id), classifications: {} });
  python(`with database() as conn:\n for index,plan in enumerate([${JSON.stringify(plan.id)},${JSON.stringify(second.id)}]):\n  conn.execute("INSERT INTO workday_notices(id,owner,workday_id,revision,title,line_tags,valid_until,status,entered_at,edited_at,expires_at) SELECT gen_random_uuid(),owner,id,1,%s||g.n,jsonb_build_array('20','Legacy heading'),'2031-01-04T23:59:59+01:00','registered',clock_timestamp(),clock_timestamp(),'2031-01-11T23:59:59+01:00' FROM workdays CROSS JOIN generate_series(1,125) g(n) WHERE id=%s",('Legacy '+str(index)+'-',plan))\n`);
  await open(page); await expect(page.locator('.notice-list summary')).toHaveCount(250);
  await page.locator('.notice-list summary').last().click(); const detail = page.locator('.notice-list li').last();
  await detail.getByRole('button', { name: /^Rediger / }).click(); await page.getByLabel('Tittel', { exact: true }).fill('Maintained legacy incident');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.');
  await expect(page.locator('.notice-list summary')).toHaveCount(250);
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
  await expect(reader.locator('summary')).toHaveCount(250); await expect(reader).toContainText('uten eksakt samsvar: 250');
});

for (const cause of ['gone', 'retention', 'proxy', 'malformed-current']) test(`pending original ${cause} recovery requires authoritative terminal proof and retains proposal`, async ({ page, context }) => {
  await openedPlan(page, context); const notice = await seed(context); await edit(page, notice); let writes = 0;
  await page.route('**:8001/notices/' + notice.id, async route => { writes++; await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toBeEnabled();
  if (cause === 'retention') python(`with database() as conn:\n conn.execute('UPDATE workday_notices SET expires_at=clock_timestamp() WHERE id=%s',(${JSON.stringify(notice.id)},))\n`);
  if (cause === 'gone' || cause === 'malformed-current') python(`with database() as conn:\n conn.execute('DELETE FROM workday_notices WHERE id=%s',(${JSON.stringify(notice.id)},))\n`);
  if (cause === 'proxy') await page.route('**:8001/workday-notice-operations/*', route => route.fulfill({ status: 404, contentType: 'text/html', body: '<html>proxy not found</html>' }));
  if (cause === 'malformed-current') await page.route('**:8001/notices', route => route.fulfill({ json: { notices: [] } }));
  await page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }).click();
  if (cause === 'proxy' || cause === 'malformed-current') {
    await expect(status(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toBeEnabled(); await expect(page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true })).toBeDisabled();
    expect(writes).toBe(1);
    return;
  }
  await expect(status(page)).toContainText('kan ikke gjenopprettes');
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Retained local proposal');
  await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true })).toBeEnabled(); expect(writes).toBe(1);
  await page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true }).click(); expect(await beforeUnload(page)).toBe(false);
});

test('absent unaccepted create receipt still permits explicit original retry before its deadline', async ({ page, context }) => {
  await openedPlan(page, context); await open(page); await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Unaccepted create'); await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20');
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
  const bodies: any[] = []; await page.route('**:8001/notices', route => { if (route.request().method() !== 'POST') return route.continue(); bodies.push(route.request().postDataJSON()); return route.abort(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true })).toBeEnabled();
  await page.unroute('**:8001/notices'); page.on('request', request => { if (request.method() === 'POST' && request.url() === API + '/notices') bodies.push(request.postDataJSON()); });
  await page.getByRole('button', { name: 'Prøv samme avvikslagring igjen', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.');
  expect(bodies).toHaveLength(2); expect(bodies[1]).toEqual(bodies[0]); expect((await (await context.request.get(API + '/notices')).json()).notices).toHaveLength(1);
});

test('refresh after old deadline permits explicit comparison of another session live extension', async ({ page, context, browser }) => {
  test.setTimeout(45000); await openedPlan(page, context);
  const ending = relativeInstants(10)[0]; const notice = await seed(context, { valid_until: ending });
  await edit(page, notice, 'Proposal retained across another extension');
  const other = await browser.newContext(); await post(other, '/auth/login', account);
  await post(other, '/notices/' + notice.id, { operation_id: randomUUID(), expected_revision: 1, content: noticeContent({ valid_until: '2031-01-05T23:59:59+01:00' }) }); await other.close();
  await expect.poll(() => Date.now() >= Date.parse(ending), { timeout: 15000 }).toBe(true);
  await page.getByRole('button', { name: 'Hent lagrede avvik', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Jeg har sammenlignet; behold mitt forslag', exact: true })).toBeEnabled();
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Proposal retained across another extension');
  await page.getByRole('button', { name: 'Jeg har sammenlignet; behold mitt forslag', exact: true }).click();
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2032-01-01'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.');
  const saved = await (await context.request.get(API + '/notices/' + notice.id)).json();
  expect(saved.revision).toBe(3); expect(saved.title).toBe('Proposal retained across another extension'); expect(saved.valid_until.startsWith('2032-01-01T')).toBe(true);
});

test('retained reader does not hide preparation editor or account maintenance after top navigation', async ({ page, context }) => {
  await openedPlan(page, context); await seed(context);
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
  await expect(reader.locator('summary')).toHaveCount(1); await reader.getByLabel('Bekreftet linje', { exact: true }).selectOption('20');
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
  await open(page); await expect(page.getByRole('heading', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeVisible(); await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Nytt manuelt utkast', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click(); await expect(reader).toBeVisible(); await expect(reader.getByLabel('Bekreftet linje', { exact: true })).toHaveValue('20');
});
