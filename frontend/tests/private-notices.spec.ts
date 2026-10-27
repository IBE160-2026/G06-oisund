import { test, expect, openedPlan, API, post, randomUUID, beforeUnload, setup, dayScreen, activityScreen, selected, python, account } from './private-activity-helpers';
import { writeFileSync } from 'node:fs';
setup();
const status = (page: any) => page.getByRole('status', { name: 'Avviksstatus', exact: true });
const fields = { title: 'Fiktivt veiarbeid ved svært langt norsk stedsnavn', line_tags: ['020', '24'], source_url: 'https://example.org/originalkilde', source_updated_at: null, valid_from: null, valid_until: '2031-01-04T23:59:59+01:00' };
async function open(page: any) { await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeVisible(); await expect(page.getByRole('button', { name: 'Hent lagrede avvik', exact: true })).toBeEnabled(); }
async function newNotice(page: any, title = fields.title) {
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Rediger avvik', exact: true })).toBeFocused();
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig'); await page.getByLabel('Tittel', { exact: true }).fill(title); await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('020, 24, 020'); await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill(fields.source_url);
}
async function save(page: any) { if (!await page.getByLabel('Gyldig tildato', { exact: true }).inputValue()) { await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig'); } await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.'); }
async function list(context: any, plan: any) { return (await context.request.get(API + '/notices')).json(); }
async function seed(context: any, plan: any, title = fields.title) { return (await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { ...fields, title } })).result; }

async function textFacts(scope: any, summary: string, description: string, sourceNote: string) {
  await expect(scope.getByText('Kort forklaring: ' + summary, { exact: true })).toBeVisible();
  const detail = scope.locator('p').filter({ hasText: 'Detaljert forklaring:' });
  await expect(detail).toBeVisible();
  await expect(detail).toHaveJSProperty('textContent', 'Detaljert forklaring: ' + description);
  await expect(detail).toHaveCSS('white-space', 'pre-wrap');
  await expect(scope.getByText('Kildebeskrivelse: ' + sourceNote, { exact: true })).toBeVisible();
}

test('notice feedback explains invalid optional source URL beside save and preserves the correction through navigation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page, 'Omkjøring');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('24');
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('svipper.no');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(status(page)).toContainText('Ikke lagret. Kildelenken må være');
  await expect(page.getByRole('region', { name: 'Lagringskrav' })).toContainText('https://svipper.no/');
  expect((await list(context, plan)).notices).toHaveLength(0);
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('https://example.org/ugyldig lenke');
  await expect(status(page)).toContainText('uten mellomrom');
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('svipper.no');
  await page.getByRole('button', { name: 'Tilbake til avvik', exact: true }).click();
  await page.getByRole('button', { name: 'Tilbake til ulagret avvik', exact: true }).click();
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Omkjøring');
  await expect(page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true })).toHaveValue('svipper.no');
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('https://example.org/trafikkmelding');
  await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('Kildelenken må være');
  await expect(status(page)).not.toContainText('Kildelenken må være');
  await save(page); const saved = (await list(context, plan)).notices;
  expect(saved).toHaveLength(1); expect(saved[0].line_tags).toEqual(['24']); expect(saved[0].valid_from).toBeNull(); expect(saved[0].valid_until).toBe('2031-01-04T23:59:59+01:00');
});

test('notice feedback names incomplete optional clock beside disabled save and clears when emptied', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page);
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  const requirements = page.getByRole('region', { name: 'Lagringskrav' });
  await expect(requirements).toContainText('Tittel er påkrevd'); await expect(requirements).toContainText('Linjer er påkrevd');
  await page.getByLabel('Tittel', { exact: true }).fill('Flyttet holdeplass');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('24');
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill(fields.source_url);
  await page.getByLabel('Gyldig fradato', { exact: true }).fill('2031-01-02');
  await expect(requirements).toContainText('Gyldig fra er ufullstendig eller uavklart');
  await expect(page.getByRole('button', { name: 'Lagre avvik', exact: true })).toBeDisabled();
  expect((await list(context, plan)).notices).toHaveLength(0);
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).scrollIntoViewIfNeeded();
  await page.screenshot({ path: '../docs/evidence/11-5-crossday-real-feedback-required.png', fullPage: true });
  await page.getByLabel('Gyldig fradato', { exact: true }).fill('');
  await expect(requirements).not.toContainText('ufullstendig'); await save(page);
});

test('historical source clock roundtrip uses authoritative Oslo facts rather than browser historical rules', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  const source = '1894-01-01T12:00+00:43';
  const n = (await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { ...fields, source_updated_at: source, valid_from: source, valid_until: fields.valid_until } })).result;
  await open(page); await page.locator('.notice-list summary').click(); await page.getByRole('button', { name: 'Rediger ' + n.title, exact: true }).click();
  await expect(page.getByLabel('Kilden oppdatert: klokkeslett', { exact: true })).toHaveValue('12:00:00');
  await page.route('**:8001/notices/' + n.id, async route => {
    const response = await route.fetch(), value = await response.json();
    for (const field of ['source_updated_at', 'valid_from', 'valid_until']) value.result[field] = new Date(value.result[field]).toISOString();
    await route.fulfill({ json: value }); // An older accepted UTC representation must still reconcile.
  });
  await page.getByLabel('Tittel', { exact: true }).fill('Historisk klokkeslett beholdt'); await save(page);
  const saved = (await list(context, plan)).notices[0]; expect(Date.parse(saved.source_updated_at)).toBe(Date.parse(source)); expect(Date.parse(saved.valid_from)).toBe(Date.parse(source)); expect(Date.parse(saved.valid_until)).toBe(Date.parse(fields.valid_until));
  await expect(page.getByText('Kilden oppdatert: 01.01.1894, 12:00:00 (Oslo-tid)', { exact: true })).toBeVisible();
});

test('quoted CSV tags preserve exact API tag boundaries on title-only edit', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const tags = ['020', '20,24', 'Route "A"', 'a,"b,c"', 'H'.repeat(300)];
  const n = (await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { ...fields, line_tags: tags } })).result;
  await open(page); await page.locator('.notice-list summary').click(); await page.getByRole('button', { name: 'Rediger ' + n.title, exact: true }).click();
  await expect(page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true })).toHaveValue('020, "20,24", "Route ""A""", "a,""b,c""", ' + 'H'.repeat(300));
  await page.getByLabel('Tittel', { exact: true }).fill('Bare tittel endret'); await save(page); expect((await list(context, plan)).notices[0].line_tags).toEqual(tags);
  await page.getByRole('button', { name: 'Rediger Bare tittel endret', exact: true }).click(); await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20, "unfinished'); await expect(page.getByRole('alert')).toContainText('mangler avsluttende anførselstegn'); await expect(page.getByRole('button', { name: 'Lagre avvik', exact: true })).toBeDisabled();
});

test('reversed known validity gives a relation error, preserves clocks and makes no request until corrected', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page); let posts = 0;
  page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith('/notices')) posts++; });
  await page.getByLabel('Gyldig fradato', { exact: true }).fill('2031-01-02'); await page.getByLabel('Gyldig fra: klokkeslett', { exact: true }).fill('12:00'); await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-02'); await page.getByLabel('Gyldig til: klokkeslett', { exact: true }).fill('11:00');
  await expect(page.getByRole('alert')).toContainText('Gyldig til må være samtidig med eller etter Gyldig fra.'); await expect(page.getByRole('button', { name: 'Lagre avvik', exact: true })).toBeDisabled(); expect(posts).toBe(0); expect((await list(context, plan)).notices).toHaveLength(0); await expect(page.getByLabel('Gyldig fra: klokkeslett', { exact: true })).toHaveValue('12:00');
  await page.getByLabel('Gyldig til: klokkeslett', { exact: true }).fill('13:00'); await expect(page.getByRole('alert')).toHaveCount(0); await save(page); expect(posts).toBe(1);
});

for (const code of ['notice_capacity', 'notice_receipt_capacity']) test(`known ${code} rejection retains specific guidance and the cancellable proposal`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page);
  const message = code === 'notice_capacity' ? 'Registeret har allerede 200 avvik.' : 'For mange lagringsforsøk. Vent til tidligere avvik utløper.';
  await page.route('**:8001/notices', route => route.request().method() === 'POST' ? route.fulfill({ status: 429, json: { detail: { code, message } } }) : route.continue());
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText(message); await expect(status(page)).not.toContainText('sammenlign'); await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue(fields.title); expect((await list(context, plan)).notices).toHaveLength(0); await page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true }).click(); await expect.poll(() => beforeUnload(page)).toBe(false);
});

for (const oldReply of ['success', 'unavailable']) test(`held superseded ${oldReply} load cannot overwrite newer success`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await seed(context, plan); let release!: () => void, received!: () => void, count = 0;
  const gate = new Promise<void>(r => release = r), entered = new Promise<void>(r => received = r);
  await page.route('**:8001/notices', async route => { count++; if (count !== 1) return route.continue(); const response = await route.fetch(); received(); await gate; if (oldReply === 'success') await route.fulfill({ response }); else await route.fulfill({ status: 503, json: { detail: 'superseded unavailable' } }); });
  try {
    await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await entered; await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await open(page); await expect(status(page)).toHaveText('Lagrede avvik er hentet.');
    const returned = page.waitForResponse(r => r.url().endsWith('/notices')); release(); await (await returned).finished(); await expect(status(page)).toHaveText('Lagrede avvik er hentet.'); await expect(page.getByRole('button', { name: 'Registrer avvik', exact: true })).toBeEnabled(); await expect(page.locator('.notice-list summary')).toHaveCount(1);
  } finally { release(); }
});

for (const surface of ['current', 'acknowledgement']) for (const invalid of ['2031-01-02T12:00:00', '2031-02-30T12:00:00Z']) test(`${surface} rejects non-explicit or normalized-invalid timestamp ${invalid}`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  if (surface === 'current') {
    await seed(context, plan); await page.route('**:8001/notices', async route => { const response = await route.fetch(), value = await response.json(); value.notices[0].source_updated_at = invalid; await route.fulfill({ json: value }); });
    await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await expect(status(page)).toContainText('Avvikslisten er utilgjengelig.'); await expect(page.locator('.notice-list summary')).toHaveCount(0); await expect(page.getByRole('button', { name: 'Registrer avvik', exact: true })).toBeDisabled();
  } else {
    await open(page); await newNotice(page); await page.route('**:8001/notices', async route => { if (route.request().method() !== 'POST') return route.continue(); const response = await route.fetch(), value = await response.json(); value.result.source_updated_at = invalid; await route.fulfill({ json: value }); });
    await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true })).toBeEnabled(); await expect(status(page)).toContainText('uavklart'); await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue(fields.title); await page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.');
  }
});

test('complete multipage controller keeps all51 discoverable, edits page2, and rejects partial later-page success', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const n = await seed(context, plan);
  python(`with database() as conn:\n conn.execute("INSERT INTO workday_notices(id,workday_id,revision,title,line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision,summary,description,source_note,line_scope,owner,expires_at,ended_at) SELECT gen_random_uuid(),workday_id,revision,'Syntetisk avvik '||g.n,title_tags.line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision,summary,description,source_note,line_scope,owner,expires_at,ended_at FROM workday_notices title_tags CROSS JOIN generate_series(1,50) g(n) WHERE id=%s", (${JSON.stringify(n.id)},))\n`);
  const first = await list(context, plan); const second = await (await context.request.get(API + '/notices?cursor=' + first.next_cursor)).json(); expect(second.notices).toHaveLength(1); const target = second.notices[0];
  await page.route('**:8001/notices?cursor=*', route => route.fulfill({ status: 503, json: { detail: 'synthetic page2 unavailable' } })); await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await expect(status(page)).toContainText('Avvikslisten er utilgjengelig.'); await expect(page.locator('.notice-list summary')).toHaveCount(0); await expect(page.getByRole('button', { name: 'Registrer avvik', exact: true })).toBeDisabled();
  await page.unroute('**:8001/notices?cursor=*'); await page.getByRole('button', { name: 'Hent lagrede avvik', exact: true }).click(); await expect(status(page)).toHaveText('Lagrede avvik er hentet.'); await expect(page.locator('.notice-list summary')).toHaveCount(51); await page.locator('.notice-list summary').filter({ hasText: target.title + ' ·' }).click(); await page.getByRole('button', { name: 'Rediger ' + target.title, exact: true }).click(); await page.getByLabel('Tittel', { exact: true }).fill('Endret avvik fra side2'); await save(page); await expect(page.locator('.notice-list summary')).toHaveCount(51);
  const saved = await (await context.request.get(API + '/notices/' + target.id)).json(); expect(saved.title).toBe('Endret avvik fra side2'); expect(saved.revision).toBe(2);
});

for (const kind of ['check', 'end']) for (const recovery of ['lookup', 'retry']) test(`lost accepted ${kind} ${recovery} retains original action through day navigation with one effect`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const n = await seed(context, plan); await open(page); await page.locator('.notice-list summary').click(); const path = '/notices/' + n.id + '/' + kind; const writes: any[] = [];
  await page.route('**:8001' + path, async route => { writes.push(route.request().postDataJSON()); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost action</html>' }); });
  if (kind === 'end') page.once('dialog', d => d.accept()); await page.getByRole('button', { name: kind === 'check' ? 'Kontrollerte kilden nå' : 'Avslutt avvik manuelt', exact: true }).click(); await expect(page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true })).toBeEnabled(); const accepted = (await list(context, plan)).notices[0]; expect(accepted.revision).toBe(2);
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeEnabled(); await open(page); await page.unroute('**:8001' + path); page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith(path)) writes.push(req.postDataJSON()); });
  await page.getByRole('button', { name: recovery === 'lookup' ? 'Kontroller avvikslagringen' : 'Prøv samme avvikslagring igjen', exact: true }).click(); await expect(status(page)).toHaveText(kind === 'check' ? 'Kildekontrollen er lagret.' : 'Avviket er avsluttet manuelt.'); expect((await list(context, plan)).notices).toEqual([accepted]); expect(writes).toHaveLength(1); await expect.poll(() => beforeUnload(page)).toBe(false);
});

for (const boundary of ['deleted', 'expired']) test(`notice ${boundary} after known rejection preserves proposal without exposing historical facts as active`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const n = await seed(context, plan); await open(page); await page.locator('.notice-list summary').click();
  await page.getByRole('button', { name: 'Rediger ' + n.title, exact: true }).click(); await page.getByLabel('Tittel', { exact: true }).fill('Beholdt lokalt forslag');
  await page.route('**:8001/notices/' + n.id, async route => {
    python(`with database() as conn:\n conn.execute(${JSON.stringify(boundary === 'deleted' ? 'DELETE FROM workday_notices WHERE id=%s' : 'UPDATE workday_notices SET expires_at=clock_timestamp() WHERE id=%s')}, (${JSON.stringify(n.id)},))\n`);
    await route.fulfill({ status: 409, json: { detail: 'Lagret avvik er endret. Hent og gjennomgå på nytt.' } });
  });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText('Forsøket ble avvist.');
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Beholdt lokalt forslag'); expect(await beforeUnload(page)).toBe(true);
  await page.getByRole('button', { name: 'Tilbake til avvik', exact: true }).click(); await expect(page.locator('.notice-list summary')).toHaveCount(0);
  await page.getByRole('button', { name: 'Tilbake til ulagret avvik', exact: true }).click(); await page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true }).click();
  await expect.poll(() => beforeUnload(page)).toBe(false);
});
async function measure(page: any) {
  const scope = page.getByRole('region', { name: 'Avviksvedlikehold', exact: true });
  const detail = scope.getByLabel('Detaljert forklaring', { exact: true });
  const control = await detail.isVisible() && await detail.isEnabled() ? detail : scope.getByRole('button', { name: 'Tilbake til dagen', exact: true }); await control.focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab'); await expect(control).toBeFocused(); await control.scrollIntoViewIfNeeded();
  const metrics = await scope.evaluate((region: Element) => {
    const light = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
    const ratio = (a: string, b: string) => (Math.max(light(a), light(b)) + .05) / (Math.min(light(a), light(b)) + .05);
    const bg = (node: Element): string => { const value = getComputedStyle(node).backgroundColor; return value === 'rgba(0, 0, 0, 0)' || value === 'transparent' ? node.parentElement ? bg(node.parentElement) : 'rgb(255,255,255)' : value; };
    const visible = [...region.querySelectorAll('h2,h3,p,label,legend,a,button,input,textarea,select,summary')].filter(node => node.getBoundingClientRect().height > 0);
    const focused = document.activeElement!, style = getComputedStyle(focused), rect = focused.getBoundingClientRect();
    const controls = visible.filter(node => ['BUTTON', 'INPUT', 'TEXTAREA', 'SELECT', 'SUMMARY'].includes(node.tagName)).map(node => { const s = getComputedStyle(node); return { tag: node.tagName, disabled: (node as HTMLInputElement).disabled, height: node.getBoundingClientRect().height, text: ratio(s.color, bg(node)), boundary: ratio(s.borderTopColor, bg(node.parentElement!)) }; });
    return { overflow: document.documentElement.scrollWidth > innerWidth, text: Math.min(...visible.map(node => ratio(getComputedStyle(node).color, bg(node)))), focus: ratio(style.outlineColor, bg(focused.parentElement!)), focusWidth: parseFloat(style.outlineWidth), focusVisible: focused.matches(':focus-visible'), focusNotObscured: rect.bottom > 0 && rect.top < innerHeight && focused.contains(document.elementFromPoint(Math.max(1, Math.min(innerWidth - 1, rect.x + rect.width / 2)), Math.max(1, Math.min(innerHeight - 1, rect.y + rect.height / 2)))) , controls };
  });
  expect(metrics.overflow).toBe(false); expect(metrics.text).toBeGreaterThanOrEqual(4.5); expect(metrics.focus).toBeGreaterThanOrEqual(3); expect(metrics.focusWidth).toBeGreaterThanOrEqual(2); expect(metrics.focusVisible).toBe(true); expect(metrics.focusNotObscured).toBe(true);
  for (const c of metrics.controls) { expect(c.height).toBeGreaterThanOrEqual(58); expect(c.text).toBeGreaterThanOrEqual(4.5); expect(c.boundary).toBeGreaterThanOrEqual(3); }
  return metrics;
}

test('source-linked prestart journey saves exact stable metadata, checks explicitly, qualifies edit, ends deliberately and retains selection', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Velg aktivitet 2', exact: true }).click(); await activityScreen(page); await dayScreen(page);
  const initial = await (await context.request.get(API + '/workdays/' + plan.id + '/recap')).json(); let selections = 0, starts = 0, checks = 0, ends = 0;
  page.on('request', req => { if (req.method() === 'POST') { if (req.url().endsWith('/selection')) selections++; if (req.url().endsWith('/start')) starts++; if (req.url().endsWith('/check')) checks++; if (req.url().endsWith('/end')) ends++; } });
  await open(page); await expect(page.getByText('Ingen avvik er registrert her. Kontroller originalkilden.', { exact: true })).toBeVisible();
  await newNotice(page); await save(page); const first = (await list(context, plan)).notices[0];
  expect(first.line_tags).toEqual(['020', '24']); expect(first.checked_at).toBeNull(); expect(first.status).toBe('registered'); expect(first.valid_from).toBeNull();
  await expect(page.getByText('Ikke kontrollert', { exact: true })).toBeVisible(); await expect(page.getByText(/^Delvis kjent gyldighet:/)).toBeVisible();
  expect(await page.getByRole('link', { name: fields.source_url, exact: true }).getAttribute('rel')).toBe('noopener noreferrer'); expect(checks).toBe(0);
  await page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).click(); await expect(status(page)).toHaveText('Kildekontrollen er lagret.');
  const checked = (await list(context, plan)).notices[0]; expect(checked.checked_revision).toBe(checked.revision); expect(checked.edited_at).toBe(first.edited_at);
  await page.getByRole('button', { name: 'Rediger ' + fields.title, exact: true }).click(); await page.getByLabel('Tittel', { exact: true }).fill('Endret kildeopplysning'); await save(page);
  await expect(page.getByText(/^Kontrollert før siste endring:/)).toBeVisible(); const edited = (await list(context, plan)).notices[0]; expect(edited.id).toBe(first.id); expect(edited.checked_at).toBe(checked.checked_at);
  page.once('dialog', dialog => dialog.dismiss()); await page.getByRole('button', { name: 'Avslutt avvik manuelt', exact: true }).click(); expect(ends).toBe(0);
  page.once('dialog', dialog => dialog.accept()); await page.getByRole('button', { name: 'Avslutt avvik manuelt', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er avsluttet manuelt.'); expect(ends).toBe(1);
  await expect(page.getByRole('button', { name: 'Rediger Endret kildeopplysning', exact: true })).toHaveCount(0);
  const ended = (await list(context, plan)).notices[0]; expect(ended.status).toBe('ended_manually'); expect(ended.checked_at).toBe(checked.checked_at);
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await page.getByRole('button', { name: 'Åpne valgt aktivitet', exact: true }).click(); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[1].id);
  expect(selections).toBe(0); expect(starts).toBe(0); expect(checks).toBe(1); expect((await (await context.request.get(API + '/workdays/' + plan.id + '/recap')).json())).toEqual(initial);
  await dayScreen(page); await page.getByRole('button', { name: 'Lukk planen', exact: true }).click(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await open(page); if (!await page.getByText('Status: Avsluttet manuelt', { exact: true }).isVisible()) await page.locator('.notice-list summary').click();
  await expect(page.getByText('Status: Avsluttet manuelt', { exact: true })).toBeVisible(); expect((await list(context, plan)).notices).toEqual([ended]);
});

test('actual synthetic PDF upload correction confirmation notice and terminal recap journey', async ({ page, context }) => {
  const pdf = Buffer.from(python('import sys, base64\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nprint(base64.b64encode(synthetic_text_pdf()).decode())\n').trim(), 'base64');
  await page.goto('/private'); await page.getByLabel('Brukernavn', { exact: true }).fill(account.username); await page.getByLabel('Passord', { exact: true }).fill(account.password); await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic-11-4.pdf', mimeType: 'application/pdf', buffer: pdf }); await page.getByRole('button', { name: 'Bruk som separat nytt utkast', exact: true }).click(); await page.getByLabel('Fra sted', { exact: true }).first().fill('Rettet syntetisk oppmøtested 11.4');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click(); await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click(); for (const select of await page.getByRole('region', { name: 'Gjennomgått versjon', exact: true }).locator('select').all()) await select.selectOption('manual'); for (const checkbox of await page.getByRole('checkbox').all()) await checkbox.check(); await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible(); await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await expect(selected(page)).toContainText('Rettet syntetisk oppmøtested 11.4'); await dayScreen(page);
  await open(page); await newNotice(page, 'Fiktivt avvik etter PDF-bekreftelse'); await save(page); await page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).click(); await expect(status(page)).toHaveText('Kildekontrollen er lagret.'); await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await expect(page.getByRole('status', { name: 'Skiftstatus', exact: true })).toHaveText('Skiftstart er lagret.'); await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await expect(page.getByText(/^Sist kontrollert:/)).toBeVisible(); await expect(page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true })).toBeEnabled();
});

test('dirty notice retains raw optional time, independent bus and activity proposal through safe day and activity navigation', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await dayScreen(page);
  await page.getByRole('textbox', { name: 'Fysisk buss', exact: true }).fill('Ulagret buss'); await open(page); await newNotice(page, 'Beholdt forslag');
  await page.getByLabel('Gyldig fradato', { exact: true }).fill('2026-10-25'); await page.getByLabel('Gyldig fra: klokkeslett', { exact: true }).fill('02:30');
  await expect(page.getByLabel('Gyldig fra: forekomst', { exact: true })).toBeVisible(); await expect(page.getByRole('button', { name: 'Lagre avvik', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await expect(page.getByRole('textbox', { name: 'Fysisk buss', exact: true })).toHaveValue('Ulagret buss');
  // Existing bus proposals guard selection changes; pure consultation is enabled after cancelling only that independent proposal.
  await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne valgt aktivitet', exact: true }).click(); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[0].id); await dayScreen(page);
  await open(page); await page.getByRole('button', { name: 'Tilbake til ulagret avvik', exact: true }).click(); await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Beholdt forslag'); await expect(page.getByLabel('Gyldig fra: klokkeslett', { exact: true })).toHaveValue('02:30');
  await page.getByLabel('Gyldig fra: forekomst', { exact: true }).selectOption({ label: 'Andre forekomst' }); await save(page); expect((await list(context, plan)).notices[0].valid_from).toBe('2026-10-25T02:30:00+01:00'); await expect.poll(() => beforeUnload(page)).toBe(false);
  await page.getByRole('button', { name: 'Rediger Beholdt forslag', exact: true }).click(); await expect(page.getByLabel('Gyldig fra: klokkeslett', { exact: true })).toHaveValue('02:30:00'); await expect(page.getByLabel('Gyldig fradato', { exact: true })).toHaveValue('2026-10-25');
  await page.getByLabel('Tittel', { exact: true }).fill('Samme lagrede Oslo-tid'); await save(page); expect((await list(context, plan)).notices[0].valid_from).toBe('2026-10-25T02:30:00+01:00');
});

for (const recovery of ['lookup', 'retry']) test(`lost accepted create ${recovery} preserves exact original command through navigation and creates one row`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page);
  await page.getByLabel('Kort forklaring', { exact: true }).fill('SMS summary');
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill('First window\nSecond window');
  await page.getByLabel('Kildebeskrivelse', { exact: true }).fill('SMS');
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('');
  await page.getByLabel('Linjeomfang', { exact: true }).selectOption('all');
  let original: any; const writes: any[] = [];
  const path = '/notices';
  await page.route('**:8001' + path, async route => { if (route.request().method() !== 'POST') return route.continue(); original = route.request().postDataJSON(); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost reply</html>' }); });
  page.on('request', req => { if (req.method() === 'POST' && req.url() === API + path) writes.push(req.postDataJSON()); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true })).toBeEnabled();
  await expect(page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true })).toBeDisabled(); await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeEnabled(); await open(page); await page.unroute('**:8001' + path);
  await page.getByRole('button', { name: recovery === 'lookup' ? 'Kontroller avvikslagringen' : 'Prøv samme avvikslagring igjen', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.');
  expect(writes).toHaveLength(1); expect((await list(context, plan)).notices).toHaveLength(1); await expect.poll(() => beforeUnload(page)).toBe(false);
});

test('stale edit requires comparison and a new explicit save without overwriting newer metadata silently', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const initial = await seed(context, plan); await open(page); await page.locator('.notice-list summary').click(); await page.getByRole('button', { name: 'Rediger ' + fields.title, exact: true }).click(); await page.getByLabel('Tittel', { exact: true }).fill('Mitt beholdte forslag');
  const competing = { ...fields, title: 'En annen lagret tittel', summary: 'Competing summary', description: 'Competing first window\nCompeting second window', source_note: 'Competing SMS source', source_url: null, line_scope: 'all', line_tags: [] };
  await post(context, '/notices/' + initial.id, { operation_id: randomUUID(), expected_revision: 1, content: competing });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText('Forsøket ble avvist.'); await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Mitt beholdte forslag'); await expect(page.getByRole('button', { name: 'Lagre avvik', exact: true })).toBeDisabled();
  await expect(page.locator('.private-notices .import-warning').getByText('Tittel: En annen lagret tittel', { exact: true })).toBeVisible();
  const comparisonFacts = page.locator('.private-notices .import-warning .notice-facts');
  await textFacts(comparisonFacts, competing.summary, competing.description, competing.source_note);
  await expect(comparisonFacts.getByText('Linjer fra kilden: Alle linjer', { exact: true })).toBeVisible();
  await expect(comparisonFacts.getByRole('link')).toHaveCount(0);
  await expect(page.getByText('Nyere lagret avvik', { exact: true })).toBeVisible(); expect((await list(context, plan)).notices[0].title).toBe('En annen lagret tittel');
  await page.getByRole('button', { name: 'Jeg har sammenlignet; behold mitt forslag', exact: true }).click(); await save(page); expect((await list(context, plan)).notices[0].title).toBe('Mitt beholdte forslag'); expect((await list(context, plan)).notices[0].revision).toBe(3);
});

test('Start in another window does not change account notice authority', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page);
  await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 });
  await save(page); expect((await list(context, plan)).notices).toHaveLength(1);
  await expect(page.getByRole('region', { name: 'Lagret skiftstatus for sammenligning', exact: true })).toHaveCount(0);
});

test('terminal recap remains initial on reopen and independent notice management remains writable', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const n = await seed(context, plan); await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 }); await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  await page.reload(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible(); await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click(); await page.locator('.notice-list summary').click(); await expect(page.getByRole('link', { name: n.source_url, exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Registrer avvik', exact: true })).toBeEnabled(); await expect(page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true })).toBeEnabled(); await expect(page.getByRole('button', { name: 'Avslutt avvik manuelt', exact: true })).toBeEnabled();
});

test('original day deletion preserves account notice facts and explicit check', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const n = await seed(context, plan); await open(page); await page.locator('.notice-list summary').click();
  await post(context, '/workdays/' + plan.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
  await page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true }).click(); await expect(status(page)).toHaveText('Kildekontrollen er lagret.');
  await expect(page.getByRole('link', { name: n.source_url, exact: true })).toBeVisible();
  expect((await list(context, plan)).notices[0].id).toBe(n.id); await expect.poll(() => beforeUnload(page)).toBe(false);
});

test('transient unavailable retains qualified known source links and disables fresh commands', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const n = await seed(context, plan); await open(page); await page.locator('.notice-list summary').click();
  await page.route('**:8001/notices', route => route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } })); await page.getByRole('button', { name: 'Hent lagrede avvik', exact: true }).click(); await expect(status(page)).toContainText('Avvikslisten er utilgjengelig.');
  await expect(page.getByText('Eventuelle tidligere viste opplysninger er ikke oppdatert.', { exact: true })).toBeVisible(); await expect(page.getByRole('link', { name: n.source_url, exact: true })).toBeVisible(); await expect(page.getByRole('button', { name: 'Kontrollerte kilden nå', exact: true })).toBeDisabled(); await expect(page.getByText('Ingen avvik er registrert her. Kontroller originalkilden.', { exact: true })).toHaveCount(0);
  const stores = await page.evaluate(() => JSON.stringify({ local: { ...localStorage }, session: { ...sessionStorage } })); expect(stores).not.toContain(n.title); expect(stores).not.toContain(n.source_url);
});

for (const corruption of ['wrong-parent', 'wrong-content', 'missing-field', 'bad-time', 'HTML']) test(`malformed ${corruption} acknowledgement never establishes save and authorized lookup resolves one effect`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page);
  await page.route('**:8001/notices', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    const response = await route.fetch(), value = await response.json();
    if (corruption === 'HTML') return route.fulfill({ status: 200, contentType: 'text/html', body: '<html>proxy</html>' });
    if (corruption === 'wrong-parent') value.result.workday_id = randomUUID();
    if (corruption === 'wrong-content') value.result.title = 'Wrong accepted content';
    if (corruption === 'missing-field') delete value.result.checked_revision;
    if (corruption === 'bad-time') value.result.entered_at = 'not a timestamp';
    await route.fulfill({ status: 200, json: value });
  });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(status(page)).toContainText('uavklart'); await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue(fields.title);
  await expect(page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true })).toBeEnabled();
  expect((await list(context, plan)).notices).toHaveLength(1); await page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true }).click(); await expect(status(page)).toHaveText('Avviket er lagret.'); expect((await list(context, plan)).notices).toHaveLength(1);
});

test('a delayed accepted reply keeps the subsequently chosen day screen and reachable recovery', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page);
  let release!: () => void, received!: () => void; const gate = new Promise<void>(r => release = r), entered = new Promise<void>(r => received = r);
  await page.route('**:8001/notices', async route => { if (route.request().method() !== 'POST') return route.continue(); const response = await route.fetch(); received(); await gate; await route.fulfill({ response }); });
  try { await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await entered; await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); release(); await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeEnabled(); await expect(page.getByRole('heading', { name: 'Dagen din', exact: true })).toBeVisible(); await expect(page.getByRole('heading', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeHidden(); expect((await list(context, plan)).notices).toHaveLength(1); }
  finally { release(); }
});

test('held initial parent authority does not disable independent account registry entry', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await seed(context, plan);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click(); await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 }); await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  let release!: () => void, received!: () => void; const gate = new Promise<void>(r => release = r), entered = new Promise<void>(r => received = r);
  await page.route('**:8001/workdays/' + plan.id + '/recap', async route => { const response = await route.fetch(); received(); await gate; await route.fulfill({ response }); });
  try { await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await entered; await expect(page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeEnabled(); release(); await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible(); }
  finally { release(); }
});

test('a dirty account notice remains explicitly saveable when the original shift closes elsewhere', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page, 'Ulagret ved avslutning');
  await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 });
  await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  await save(page); expect((await list(context, plan)).notices[0].title).toBe('Ulagret ved avslutning');
  await expect.poll(() => beforeUnload(page)).toBe(false);
});

for (const invalidation of ['account', 'session']) test(`held accepted notice response cannot restore ${invalidation} private presentation`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await newNotice(page);
  let release!: () => void, received!: () => void; const gate = new Promise<void>(r => release = r), entered = new Promise<void>(r => received = r);
  await page.route('**:8001/notices', async route => { if (route.request().method() !== 'POST') return route.continue(); const response = await route.fetch(); received(); await gate; await route.fulfill({ response }); });
  const next = { username: 'synthetic-held-notice-' + randomUUID(), password: randomUUID() };
  try {
    await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await entered;
    if (invalidation === 'account') { python(`from app.auth import provision\nprovision(${JSON.stringify(next.username)},${JSON.stringify(next.password)})\n`); await post(context, '/auth/login', next); }
    else python(`with database() as conn:\n conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=(SELECT id FROM accounts WHERE username=%s)", (${JSON.stringify(account.username)},))\n`);
    release(); await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0); await expect.poll(() => beforeUnload(page)).toBe(false);
  } finally { release(); if (invalidation === 'account') python(`with database() as conn:\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(next.username)},))\n conn.execute('DELETE FROM accounts WHERE username=%s', (${JSON.stringify(next.username)},))\n`); }
});

for (const theme of ['Day', 'Night']) for (const width of [768, 1024, 1440]) test(`${theme} ${width} enlarged notice editor and saved long content remain readable, focusable and unclipped`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: width === 768 ? 600 : 768 }); const { plan } = await openedPlan(page, context); if (theme === 'Night') await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.evaluate(() => document.documentElement.style.fontSize = '200%'); await open(page); await newNotice(page, 'Fiktivt veiarbeid ved et svært langt norsk stedsnavn '.repeat(5));
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('https://example.org/' + 'lang-opprinnelig-kildeadresse-'.repeat(50));
  const summary = 'S'.repeat(1000), description = 'D'.repeat(2499) + '\n' + 'E'.repeat(2500), sourceNote = 'N'.repeat(500);
  await page.getByLabel('Kort forklaring', { exact: true }).fill(summary);
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill(description);
  await page.getByLabel('Kildebeskrivelse', { exact: true }).fill(sourceNote);
  const editor = await measure(page); await page.screenshot({ path: '../docs/evidence/11-5-crossday-real-notice-editor-' + theme.toLowerCase() + '-' + width + '.png', fullPage: true });
  await save(page); await expect(page.getByRole('heading', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeFocused();
  await expect(page.getByText('Kildens oppdateringstid er ukjent', { exact: true })).toBeVisible(); expect((await list(context, plan)).notices).toHaveLength(1);
  await textFacts(page.locator('.notice-list .notice-facts'), summary, description, sourceNote);
  const saved = await measure(page); await page.screenshot({ path: '../docs/evidence/11-5-crossday-real-notice-saved-' + theme.toLowerCase() + '-' + width + '.png', fullPage: true });
  const n = (await list(context, plan)).notices[0]; await page.getByRole('button', { name: 'Rediger ' + n.title, exact: true }).click(); await page.getByLabel('Tittel', { exact: true }).fill('Mitt forslag ved konflikt');
  await post(context, '/notices/' + n.id, { operation_id: randomUUID(), expected_revision: 1, content: { ...fields, title: 'Annen lagret tittel for sammenligning' } });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(page.getByText('Nyere lagret avvik', { exact: true })).toBeVisible(); const conflict = await measure(page); await page.screenshot({ path: '../docs/evidence/11-5-crossday-real-notice-conflict-' + theme.toLowerCase() + '-' + width + '.png', fullPage: true });
  await page.route('**:8001/notices', route => route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } })); await page.getByRole('button', { name: 'Hent lagrede avvik', exact: true }).click(); await expect(status(page)).toContainText('Avvikslisten er utilgjengelig.'); const unavailable = await measure(page);
  await page.screenshot({ path: '../docs/evidence/11-5-crossday-real-notice-unavailable-' + theme.toLowerCase() + '-' + width + '.png', fullPage: true }); writeFileSync('../docs/evidence/11-5-crossday-real-notice-' + theme.toLowerCase() + '-' + width + '.json', JSON.stringify({ editor, saved, conflict, unavailable }, null, 2));
});


for (const theme of ['Day', 'Night']) test(theme + ' SMS scope proposal survives navigation and saved text reloads', async ({ page, context }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const { plan } = await openedPlan(page, context); if (theme === 'Night') await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await dayScreen(page);
  await open(page); await newNotice(page, 'SMS traffic notice');
  const heading = 'Copied route heading ' + 'x'.repeat(279);
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill(heading);
  await page.getByLabel('Kort forklaring', { exact: true }).fill('Temporary stop');
  const detail = 'Monday 06-08\nTuesday 16-18\nUse temporary stop; keep complete operational instructions.';
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill(detail);
  await page.getByLabel('Kildebeskrivelse', { exact: true }).fill('SMS from traffic control');
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('');
  await page.getByLabel('Linjeomfang', { exact: true }).selectOption('all');
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await activityScreen(page); await dayScreen(page); await open(page);
  await page.getByRole('button', { name: 'Tilbake til ulagret avvik', exact: true }).click();
  await expect(page.getByLabel('Linjeomfang', { exact: true })).toHaveValue('all');
  await page.getByLabel('Linjeomfang', { exact: true }).selectOption('selected');
  await expect(page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true })).toHaveValue(heading);
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('');
  await expect(page.getByRole('region', { name: 'Lagringskrav' })).toContainText('eller velg Alle linjer');
  await page.getByLabel('Linjeomfang', { exact: true }).selectOption('all');
  await measure(page);
  await page.screenshot({ path: '../docs/evidence/11-5-crossday-real-sms-editor-' + theme.toLowerCase() + '-390.png', fullPage: true });
  await save(page); const n = (await list(context, plan)).notices[0];
  expect(n.line_scope).toBe('all'); expect(n.line_tags).toEqual([]); expect(n.source_url).toBeNull(); expect(n.description).toBe(detail); expect(n.valid_from).toBeNull(); expect(n.valid_until).toBe('2031-01-04T23:59:59+01:00');
  await expect(page.getByText('Linjer fra kilden: Alle linjer', { exact: true })).toBeVisible();
  await textFacts(page.locator('.notice-list .notice-facts'), 'Temporary stop', detail, 'SMS from traffic control');
  await measure(page);
  await page.screenshot({ path: '../docs/evidence/11-5-crossday-real-sms-saved-' + theme.toLowerCase() + '-390.png', fullPage: true });
  await page.reload(); await page.getByRole('button', { name: /Åpne plan 2031-01-02/ }).click(); await open(page); await page.locator('.notice-list summary').click();
  await textFacts(page.locator('.notice-list .notice-facts'), 'Temporary stop', detail, 'SMS from traffic control');
  await page.getByRole('button', { name: 'Rediger SMS traffic notice', exact: true }).click();
  await expect(page.getByLabel('Detaljert forklaring', { exact: true })).toHaveValue(detail);
  await expect(page.getByLabel('Kort forklaring', { exact: true })).toHaveValue('Temporary stop');
  await expect(page.getByLabel('Kildebeskrivelse', { exact: true })).toHaveValue('SMS from traffic control');
});


test('notice field errors have stable unique associations and clear when corrected', async ({ page, context }) => {
  await openedPlan(page, context); await open(page); await newNotice(page);
  await page.getByLabel('Tittel', { exact: true }).fill('');
  await page.getByLabel('Kort forklaring', { exact: true }).fill('S'.repeat(1001));
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill('D'.repeat(5001));
  await page.getByLabel('Kildebeskrivelse', { exact: true }).fill('N'.repeat(501));
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('invalid');
  await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('');
  for (const [label, field] of [['Tittel','title'],['Kort forklaring','summary'],['Detaljert forklaring','description'],['Kildebeskrivelse','source_note'],['Originalkilde (HTTP eller HTTPS)','source_url'],['Linjer fra kilden (kommaseparert)','line_tags'],['Linjeomfang','line_tags']]) {
    const control = page.getByLabel(label, { exact: true });
    await expect(control).toHaveAttribute('aria-invalid', 'true');
    await expect(control).toHaveAttribute('aria-describedby', 'notice-' + field + '-error');
    await expect(page.locator('#notice-' + field + '-error')).toHaveCount(1);
  }
  await page.getByLabel('Tittel', { exact: true }).fill('Valid title');
  await page.getByLabel('Kort forklaring', { exact: true }).fill('');
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill('');
  await page.getByLabel('Kildebeskrivelse', { exact: true }).fill('');
  await page.getByLabel('Originalkilde (HTTP eller HTTPS)', { exact: true }).fill('');
  await page.getByLabel('Linjeomfang', { exact: true }).selectOption('all');
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveAttribute('aria-invalid', 'false');
  await expect(page.locator('[id^="notice-"][id$="-error"]')).toHaveCount(0);
});


test('sparse notice pages and consecutive empty scans reach a later retained incident', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  const a = await seed(context, plan, 'First retained incident');
  const b = await seed(context, plan, 'Later retained incident');
  const id = (n: number) => '00000000-0000-4000-8000-' + n.toString(16).padStart(12, '0');
  const scanned: string[] = [];
  const envelope = (notices: any[], next_cursor: string | null) => ({ notices, next_cursor, server_now: new Date().toISOString() });
  await page.route('**:8001/notices', route => route.fulfill({ json: envelope([{ ...a, id: id(1) }], id(51)) }));
  await page.route('**:8001/notices?cursor=*', route => {
    const cursor = new URL(route.request().url()).searchParams.get('cursor')!; scanned.push(cursor);
    return route.fulfill({ json: cursor === id(51) ? envelope([], id(102)) : cursor === id(102) ? envelope([], id(153)) : envelope([{ ...b, id: id(154) }], null) });
  });
  await open(page);
  await expect(page.locator('.notice-list summary')).toHaveCount(2);
  await expect(page.locator('.notice-list')).toContainText('Later retained incident');
  expect(scanned).toEqual([id(51), id(102), id(153)]);
});

test('nonadvancing notice scan cursor is rejected without presenting partial private rows', async ({ page, context }) => {
  await openedPlan(page, context);
  const cursor = '00000000-0000-4000-8000-000000000051';
  await page.route('**:8001/notices', route => route.fulfill({ json: { notices: [], next_cursor: cursor, server_now: new Date().toISOString() } }));
  await page.route('**:8001/notices?cursor=*', route => route.fulfill({ json: { notices: [], next_cursor: cursor, server_now: new Date().toISOString() } }));
  await open(page);
  await expect(status(page)).toContainText('Avvikslisten er utilgjengelig.');
  await expect(page.locator('.notice-list summary')).toHaveCount(0);
});
