import { preparation, editor, planScreen } from './private-screen-helpers';
import { test, expect, type Page, type BrowserContext } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';

const account = { username: 'synthetic-confirm-' + randomUUID(), password: randomBytes(24).toString('hex') };
const API = 'http://127.0.0.1:8001';
function python(program: string) {
  if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project selection required');
  return execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'], { cwd: '..', encoding: 'utf8', input: 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n' + program });
}
test.beforeAll(() => python(`from app.auth import provision\nprovision(${JSON.stringify(account.username)}, ${JSON.stringify(account.password)})\n`));
test.beforeEach(() => python(`with database() as conn:
 owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(account.username)},)).fetchone()['id']
 for table in ['workday_deletions','workday_operations','workdays','drafts','draft_operations','draft_deletions']:
  conn.execute('DELETE FROM '+table+' WHERE owner=%s',(owner,))
 conn.execute('DELETE FROM login_limits')
`));
test.afterAll(() => python(`with database() as conn:
 owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(account.username)},)).fetchone()['id']
 for table in ['workday_deletions','workday_operations','workdays','drafts','draft_operations','draft_deletions','sessions']:
  conn.execute('DELETE FROM '+table+' WHERE owner=%s',(owner,))
 conn.execute('DELETE FROM accounts WHERE id=%s',(owner,))
 conn.execute('DELETE FROM login_limits')
`));
async function login(page: Page) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
}
async function post(context: BrowserContext, path: string, body: object) {
  const proof = await (await context.request.get(API + '/auth/csrf')).json();
  const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data: body });
  expect(response.status()).toBe(200); return response.json();
}
async function seed(page: Page, context: BrowserContext, kind: string | null = null, extra: Record<string, string | null> = {}) {
  const operation = await post(context, '/draft-operations', {});
  const draft = await post(context, '/drafts', { operation_id: operation.operation_id, expected_revision: 0, draft: { service_date: '2031-01-02', vehicle_duty: 'CAR - 1', physical_bus: null, activities: [{ id: randomUUID(), type: kind, raw_code: 'Fictional code', start: '2031-01-02T10:00+01:00', end: '2031-01-02T11:00+01:00', from_place: 'Fiktivt langt oppmøtested med navn som skal brytes og være lesbart i smale vinduer', to_place: null, uncertainty: 'Fiktiv ukjent opplysning', ...extra }] } });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).first().click();
  await expect(page.getByRole('button', { name: 'Gjennomgå lagret utkast' })).toBeEnabled();
  return draft;
}
async function review(page: Page) {
  await editor(page); await page.getByRole('button', { name: 'Gjennomgå lagret utkast' }).click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
}
async function decide(page: Page) {
  const region = page.getByRole('region', { name: 'Gjennomgått versjon' });
  for (const select of await region.getByRole('combobox').all()) await select.selectOption('manual');
  for (const box of await region.getByRole('checkbox').all()) await box.check();
}
async function confirmSaved(context: BrowserContext, draft: any) {
  const reviewed = await post(context, '/workday-reviews', { draft_id: draft.id, expected_revision: draft.revision });
  return post(context, '/drafts/' + draft.id + '/confirm', { operation_id: reviewed.operation_id, expected_revision: draft.revision, acknowledgements: reviewed.unknowns.filter((item: any) => !reviewed.classifications_required.includes(item.id.split(':')[0])).map((item: any) => item.id), classifications: Object.fromEntries(reviewed.classifications_required.map((id: string) => [id, 'manual'])) });
}

function syntheticImport() {
  const imported = JSON.parse(python('import sys\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nfrom app.pdf_import import parse_document\nfrom app.private_import import interpret\nprint(interpret(parse_document(synthetic_text_pdf())).model_dump_json())\n'));
  imported.service_date = '2031-01-02';
  imported.activities.forEach((activity: any, index: number) => { activity.start = `2031-01-02T10:0${index}+01:00`; activity.end = activity.start; activity.type = index === 0 ? 'trip' : 'manual'; });
  imported.import_metadata.annotations = [{ value: 't', meaning: null, provenance: { page: 1, column: null, line: null } }];
  imported.activities[0].uncertainty = '  Kildemerket t har ukjent betydning (side 1). Concrete manual note.  ';
  return imported;
}

test('review fixes legacy mixed note survives unrelated draft save and reopen exactly', async ({ page, context }) => {
  await login(page); const imported = syntheticImport();
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: imported });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click();
  const note = page.getByLabel('Usikkerhet / ukjente fakta', { exact: true }).first();
  await expect(note).toHaveValue('   Concrete manual note.  ');
  await page.getByLabel('Vognløp', { exact: true }).fill('0007');
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Private utkast' }).getByRole('status')).toHaveText('Lagret. Versjon 2.');
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 2', exact: true }).click();
  await expect(note).toHaveValue('   Concrete manual note.  ');
  const stored = await (await context.request.get(API + '/drafts/' + draft.id)).json();
  expect(stored.draft.activities).toEqual(draft.draft.activities);
  expect(stored.draft.import_metadata).toEqual(draft.draft.import_metadata);
});

for (const policy of [1, 2]) test(`review fixes real legacy policy ${policy} reopens exact facts decisions and expiry`, async ({ page, context }) => {
  await login(page); const imported = syntheticImport();
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: imported });
  const issued = await post(context, '/workday-reviews', { draft_id: draft.id, expected_revision: 1 });
  const unknowns = JSON.parse(python(`from app.draft_domain import DraftContent\nfrom app.workday_domain import assessment\nimport json\nwith database() as conn:\n conn.execute('UPDATE workday_operations SET assessment_policy_version=%s WHERE id=%s', (${policy}, ${JSON.stringify(issued.operation_id)}))\n content=conn.execute('SELECT content FROM drafts WHERE id=%s', (${JSON.stringify(draft.id)},)).fetchone()['content']\nprint(json.dumps(assessment(DraftContent.model_validate(content), policy_version=${policy})['unknowns']))\n`));
  const decisions = { operation_id: issued.operation_id, expected_revision: 1, acknowledgements: unknowns.map((item: any) => item.id), classifications: {} };
  const plan = await post(context, '/drafts/' + draft.id + '/confirm', decisions);
  expect(plan.draft).toEqual(draft.draft); expect(plan.unknowns).toEqual(unknowns);
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  for (let opened = 0; opened < 2; opened++) {
    await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
    const confirmed = page.getByRole('region', { name: 'Bekreftet plan', exact: true });
    const current = confirmed.getByRole('region', { name: 'Dagsoversikt', exact: true }).locator(`[data-activity-id="${draft.draft.activities[0].id}"]`);
    await expect(current.locator('.day-uncertainty')).toHaveText('Usikkerhet: Concrete manual note.');
    await confirmed.getByText('Bekreftede detaljer og historisk kilde', { exact: true }).click();
    const rawNote = confirmed.locator('.day-confirmed-details .fact').filter({ has: page.locator('dt', { hasText: 'Usikkerhet / ukjente fakta' }) }).locator('dd').first();
    expect(await rawNote.textContent()).toBe(imported.activities[0].uncertainty);
    await expect(rawNote).toBeVisible();
    await expect(rawNote.locator('.day-uncertainty')).toHaveCount(0);
    expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
    expect(await (await context.request.get(API + '/workday-operations/' + issued.operation_id)).json()).toEqual({ state: 'accepted', result: plan });
    await planScreen(page); await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  }
  expect(await post(context, '/drafts/' + draft.id + '/confirm', decisions)).toEqual(plan);
});

for (const tamper of ['swapped', 'misleading']) test(`review fixes reject ${tamper} candidate labels before consent`, async ({ page, context }) => {
  await login(page); await seed(page, context, 'trip');
  let confirmations = 0;
  page.on('request', request => { if (request.method() === 'POST' && request.url().endsWith('/confirm')) confirmations++; });
  await page.route('**/workday-reviews', async route => {
    const response = await route.fetch(); const value = await response.json();
    if (tamper === 'swapped') [value.unknowns[0].label, value.unknowns[1].label] = [value.unknowns[1].label, value.unknowns[0].label];
    else value.unknowns[0].label = 'Everything is complete. No missing fact.';
    await route.fulfill({ response, json: value });
  });
  await editor(page); await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Tjenesten kunne ikke bekrefte svaret');
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toHaveCount(0);
  expect(confirmations).toBe(0);
});

test('feedback classification switching prunes decisions and frozen lost response settles non-trip', async ({ page, context }) => {
  await login(page); const draft = await seed(page, context);
  await review(page);
  const region = page.getByRole('region', { name: 'Gjennomgått versjon' });
  const classification = region.getByRole('combobox');
  await expect(region.getByRole('checkbox')).toHaveCount(0);
  await classification.selectOption('trip');
  await expect(region.getByRole('checkbox')).toHaveCount(5);
  for (const box of await region.getByRole('checkbox').all()) await box.check();
  await classification.selectOption('manual');
  await expect(region.getByRole('checkbox')).toHaveCount(0);
  await classification.selectOption('trip');
  for (const box of await region.getByRole('checkbox').all()) await expect(box).not.toBeChecked();
  await expect(region.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true })).toBeDisabled();
  await classification.selectOption('Coffee');
  let submitted: any;
  await page.route('**/drafts/' + draft.id + '/confirm', async route => {
    submitted = route.request().postDataJSON();
    const response = await route.fetch(); expect(response.status()).toBe(200);
    await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost reply</html>' });
  });
  await region.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true })).toBeVisible();
  await expect.poll(() => submitted).toBeTruthy();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Bekreftelsen er uavklart.');
  expect(submitted.acknowledgements).toEqual([]);
  expect(submitted.classifications).toEqual({ [draft.draft.activities[0].id]: 'Coffee' });
  await expect(classification).toBeDisabled();
  await page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
});

for (const malformed of ['unassociated', 'non-trip', 'invented-field']) test(`feedback rejects malformed review candidate ${malformed}`, async ({ page, context }) => {
  await login(page); const draft = await seed(page, context, malformed === 'non-trip' ? 'Coffee' : 'trip');
  await page.route('**/workday-reviews', async route => {
    const response = await route.fetch(); const value = await response.json();
    value.unknowns.push({ id: malformed === 'unassociated' ? randomUUID() + ':line' : draft.draft.activities[0].id + ':' + (malformed === 'invented-field' ? 'raw_code' : 'line'), label: 'Malformed candidate' });
    await route.fulfill({ response, json: value });
  });
  await editor(page); await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Tjenesten kunne ikke bekrefte svaret');
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toHaveCount(0);
});

for (const kind of ['trip', 'deadhead', 'CAR']) test(`review unknown contract and passenger direction for ${kind}`, async ({ page, context }) => {
  await login(page); await seed(page, context, kind);
  const currentUnknowns = page.getByText(/Gjeldende ukjente fakta:/);
  if (kind === 'trip') await expect(currentUnknowns).toContainText('retning');
  await review(page);
  const region = page.getByRole('region', { name: 'Gjennomgått versjon' });
  await expect(region).toContainText('Godta manglende turinformasjon');
  await expect(region.getByRole('checkbox', { name: /turnummer er ukjent/ })).toHaveCount(kind === 'trip' ? 1 : 0);
  await expect(region.getByRole('checkbox', { name: /retning er ukjent/ })).toHaveCount(kind === 'trip' ? 1 : 0);
  await decide(page);
  await region.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
});

for (const [kind, field, value, missing] of [
  ['trip', 'direction', '\ufeff', false],
  ['trip', 'direction', '\u001c', true],
  ['deadhead', 'trip', '', true],
  ['CAR', 'trip', ' \u0085\u001c ', true],
] as const) test(`activity absence presentation ${kind} ${field} ${JSON.stringify(value)}`, async ({ page, context }) => {
  await login(page); const saved = await seed(page, context, kind, { [field]: value });
  const label = field === 'direction' ? 'retning' : 'turnummer';
  const unknown = page.getByText(/Gjeldende ukjente fakta:/);
  if (kind === 'trip' && missing) await expect(unknown).toContainText(label); else await expect(unknown).not.toContainText(label);
  await review(page);
  const region = page.getByRole('region', { name: 'Gjennomgått versjon' });
  const fact = region.locator('.fact').filter({ has: page.locator('dt', { hasText: field === 'direction' ? /^Retning$/ : /^Turnummer$/ }) }).locator('dd');
  expect(await fact.textContent()).toBe(missing ? 'Ukjent' : value);
  await expect(region.getByRole('checkbox', { name: new RegExp(label + ' er ukjent') })).toHaveCount(kind === 'trip' && missing ? 1 : 0);
  await decide(page); await region.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
  const member = day.locator('[data-activity-id="' + saved.draft.activities[0].id + '"]');
  if (kind === 'trip' && missing) await expect(member.locator('p').filter({ hasText: /^Ukjent:/ })).toContainText(label);
  else if (kind === 'trip') expect(await member.textContent()).toContain('Retning: ' + value);
  else await expect(member.locator('p').filter({ hasText: /^Ukjent:/ })).not.toContainText(label);
  expect((await (await context.request.get(API + '/drafts/' + saved.id)).json()).draft.activities[0][field]).toBe(value);
});

async function openedPlan(page: Page, context: BrowserContext) {
  await login(page); const draft = await seed(page, context, 'trip');
  const plan = await confirmSaved(context, draft);
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
  return { draft, plan };
}

for (const width of [768, 1440]) for (const night of [false, true]) test(`plan deletion popup cancel accept reload at ${width}px ${night ? 'Night' : 'Day'}`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: 1000 });
  const { draft, plan } = await openedPlan(page, context);
  if (night) await page.getByRole('button', { name: 'Nattmodus' }).click();
  let requests = 0;
  page.on('request', request => { if (request.url().endsWith('/delete')) requests++; });
  page.once('dialog', async dialog => { expect(dialog.type()).toBe('confirm'); expect(dialog.message()).toContain('Dette kan ikke angres. Kildeutkastet beholdes.'); await dialog.dismiss(); });
  const remove = page.getByRole('button', { name: 'Slett bekreftet plan', exact: true });
  await expect(remove).toBeEnabled(); await remove.focus(); await page.keyboard.press('Enter');
  await expect(remove).toBeFocused(); expect(requests).toBe(0);
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
  page.once('dialog', dialog => dialog.accept());
  await page.keyboard.press('Enter');
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Den bekreftede planen er slettet.');
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeFocused();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  await page.getByRole('region', { name: 'Bekreft plan', exact: true }).screenshot({ path: `../docs/evidence/11-2-regression-10-3-deleted-${width}-${night ? 'night' : 'day'}.png` });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.reload(); await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toHaveCount(0);
  expect((await context.request.get(API + '/workdays/' + plan.id)).status()).toBe(404);
  expect(await (await context.request.get(API + '/drafts/' + draft.id)).json()).toEqual(draft);
});

for (const reply of ['html', 'html404', 'wrong', 'network', 'unsent']) test(`plan deletion ${reply} reply stays uncertain and identical retry or lookup settles`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  let original = '';
  await page.route('**:8001/workdays/*/delete', async route => {
    original = route.request().postData()!;
    if (reply === 'unsent') { await route.abort(); return; }
    await route.fetch();
    if (reply === 'network') await route.abort();
    else if (reply === 'html' || reply === 'html404') await route.fulfill({ status: reply === 'html404' ? 404 : 200, contentType: 'text/html', body: '<html>login</html>' });
    else await route.fulfill({ json: { operation_id: randomUUID(), deleted_id: plan.id, source_revision: 1 } });
  });
  page.once('dialog', dialog => dialog.accept());
  await planScreen(page); await page.getByRole('button', { name: 'Slett bekreftet plan', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Slettingen er uavklart. Behold siden åpen');
  await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { includeHidden: true, name: 'Oppdater planlisten', exact: true })).toBeDisabled();
  await expect(page.getByLabel('Vognløp', { exact: true })).toBeDisabled();
  expect(await page.evaluate(() => { const event = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(event); return event.defaultPrevented; })).toBe(true);
  page.once('dialog', async dialog => { expect(dialog.type()).toBe('confirm'); await dialog.dismiss(); });
  await page.getByRole('link', { name: 'Åpne fiktiv demo', exact: true }).click();
  await page.unroute('**:8001/workdays/*/delete');
  if (reply === 'wrong' || reply === 'unsent') {
    if (reply === 'unsent') {
      await page.getByRole('button', { name: 'Kontroller slettingen', exact: true }).click();
      await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Slettingen er uavklart.');
    }
    await page.route('**:8001/workdays/*/delete', async route => { expect(route.request().postData()).toBe(original); await route.continue(); });
    await page.getByRole('button', { name: 'Prøv samme sletting igjen', exact: true }).click();
  } else await page.getByRole('button', { name: 'Kontroller slettingen', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Den bekreftede planen er slettet.');
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
});

for (const read of ['list', 'plan']) test(`plan deletion discards delayed ${read} response`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const waiting = new Promise<void>(resolve => { entered = resolve; });
  const path = read === 'list' ? '**:8001/workdays' : '**:8001/workdays/' + plan.id;
  await page.route(path, async route => { const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try {
    await preparation(page); await page.getByRole('button', { name: read === 'list' ? 'Oppdater planlisten' : 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
    await waiting;
    page.once('dialog', dialog => dialog.accept()); await planScreen(page); await page.getByRole('button', { name: 'Slett bekreftet plan', exact: true }).click();
    await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Den bekreftede planen er slettet.');
    const returned = page.waitForResponse(response => response.url().endsWith(read === 'list' ? ':8001/workdays' : '/workdays/' + plan.id));
    release(); await (await returned).finished();
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toHaveCount(0);
  } finally { release(); }
});
test('review fix preserves later-page discovery after deleting the last first-page summary', async ({ page, context }) => {
  const { draft, plan } = await openedPlan(page, context);
  const laterDraft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { ...draft.draft, service_date: '2032-02-03' } });
  const later = await confirmSaved(context, laterDraft);
  const summary = (value: any) => ({ id: value.id, source_draft_id: value.source_draft_id, source_revision: value.source_revision, service_date: value.draft.service_date, expires_at: value.expires_at });
  await page.route('**:8001/workdays', route => route.fulfill({ json: { workdays: [summary(plan)], next_cursor: plan.id } }));
  let cursor: string | null = null;
  await page.route('**:8001/workdays?*', async route => { cursor = new URL(route.request().url()).searchParams.get('cursor'); await route.fulfill({ json: { workdays: [summary(later)], next_cursor: null } }); });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Last flere planer', exact: true })).toBeEnabled();
  page.once('dialog', dialog => dialog.accept()); await planScreen(page); await page.getByRole('button', { name: 'Slett bekreftet plan', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Den bekreftede planen er slettet.');
  await preparation(page); await page.getByRole('button', { name: 'Last flere planer', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2032-02-03 · versjon 1', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true }).getByRole('region', { name: 'Dagsoversikt', exact: true }).getByText('2032-02-03', { exact: true })).toBeVisible();
  expect(cursor).toBe(plan.id);
});

for (const status of [404, 410]) test(`review fix clears only the denied same-ID snapshot on ${status}`, async ({ page, context }) => {
  const { draft, plan } = await openedPlan(page, context);
  const otherDraft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { ...draft.draft, service_date: '2032-02-03' } });
  await confirmSaved(context, otherDraft);
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await page.route('**:8001/workdays/' + plan.id, route => route.fulfill({ status, json: { detail: 'Synthetic denial' } }));
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toHaveText('Tilgangen ble avvist eller fristen er utløpt.');
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2032-02-03 · versjon 1', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toHaveText('Tilgangen ble avvist eller fristen er utløpt.');
  await planScreen(page); await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true }).getByRole('region', { name: 'Dagsoversikt', exact: true }).getByText('2032-02-03', { exact: true })).toBeVisible();
});

for (const held of ['deletion', 'read']) test(`review fix expiry clears busy and leave locks during held ${held}`, async ({ page, context }) => {
  await page.clock.install(); await login(page);
  const ending = python("from datetime import datetime,timedelta,timezone\nfrom zoneinfo import ZoneInfo\nprint((datetime.now(timezone.utc)-timedelta(days=7)+timedelta(seconds=60)).replace(microsecond=0).astimezone(ZoneInfo('Europe/Oslo')).isoformat())\n").trim();
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: ending.slice(0, 10), activities: [{ id: randomUUID(), type: 'manual', start: ending, end: ending }] } });
  const plan = await confirmSaved(context, draft);
  // Schedule retention timers near the deadline so expiry precedes the
  // independent ten-second transport timeout of the held request.
  await page.clock.setSystemTime(new Date(Date.parse(plan.expires_at) - 5000));
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  const open = page.getByRole('button', { name: `Åpne plan ${draft.draft.service_date} · versjon 1`, exact: true });
  await open.click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const waiting = new Promise<void>(resolve => { entered = resolve; });
  const path = held === 'deletion' ? '**:8001/workday-deletions/*' : '**:8001/workdays/' + plan.id;
  await page.route(path, async route => { const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try {
    if (held === 'deletion') { page.once('dialog', dialog => dialog.accept()); await planScreen(page); await page.getByRole('button', { name: 'Slett bekreftet plan', exact: true }).click(); }
    else { await preparation(page); await open.click(); }
    await waiting;
    await expect(page.getByRole('button', { includeHidden: true, name: 'Oppdater planlisten', exact: true })).toBeDisabled();
    if (held === 'deletion') expect(await page.evaluate(() => { const event = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(event); return event.defaultPrevented; })).toBe(true);
    await page.clock.fastForward(Date.parse(plan.expires_at) - await page.evaluate(() => Date.now()) + 1000);
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Kontroller slettingen', exact: true })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Prøv samme sletting igjen', exact: true })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Oppdater planlisten', exact: true })).toBeEnabled();
    await expect(page.getByLabel('Vognløp', { exact: true })).toBeEnabled();
    expect(await page.evaluate(() => { const event = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(event); return event.defaultPrevented; })).toBe(false);
    const returned = page.waitForResponse(response => response.url().includes(held === 'deletion' ? '/workday-deletions/' : '/workdays/' + plan.id));
    release(); await (await returned).finished();
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Oppdater planlisten', exact: true })).toBeEnabled();
  } finally { release(); }
});

for (const reply of ['failed', 'malformed', 'mismatched', 'delayed']) test(`review fix mandatory deletion receipt ${reply} retains identity until matching recovery`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  let body: any, receiptPath = '', release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const waiting = new Promise<void>(resolve => { entered = resolve; });
  await page.route('**:8001/workdays/*/delete', async route => { body = route.request().postDataJSON(); await route.continue(); });
  await page.route('**:8001/workday-deletions/*', async route => {
    receiptPath = new URL(route.request().url()).pathname;
    if (reply === 'failed') await route.abort();
    else if (reply === 'malformed') await route.fulfill({ contentType: 'application/json', body: '{' });
    else if (reply === 'mismatched') await route.fulfill({ json: { deleted_id: plan.id, source_revision: 1, operation_id: randomUUID() } });
    else { const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); }
  });
  try {
    page.once('dialog', dialog => dialog.accept()); await planScreen(page); await page.getByRole('button', { name: 'Slett bekreftet plan', exact: true }).click();
    if (reply === 'delayed') await waiting;
    else await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Slettingen er uavklart. Behold siden åpen');
    expect(receiptPath).toBe('/workday-deletions/' + body.operation_id);
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeDisabled();
    await expect(page.getByRole('button', { includeHidden: true, name: 'Oppdater planlisten', exact: true })).toBeDisabled();
    await expect(page.getByLabel('Vognløp', { exact: true })).toBeDisabled();
    expect(await page.evaluate(() => { const event = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(event); return event.defaultPrevented; })).toBe(true);
    page.once('dialog', dialog => dialog.dismiss()); await page.getByRole('link', { name: 'Åpne fiktiv demo', exact: true }).click();
    if (reply === 'delayed') release();
    else {
      await page.unroute('**:8001/workday-deletions/*');
      await page.route('**:8001/workdays/*/delete', async route => { expect(route.request().postDataJSON()).toEqual(body); await route.continue(); });
      await page.getByRole('button', { name: 'Prøv samme sletting igjen', exact: true }).click();
    }
    await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Den bekreftede planen er slettet.');
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  } finally { release?.(); }
});

test('saved revision review cancels unchanged, editing invalidates, unknowns and classification gate confirmation', async ({ page, context }) => {
  await login(page); const draft = await seed(page, context);
  await review(page);
  await expect(page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: 'Avbryt gjennomgang' }).click();
  expect(await (await context.request.get(API + '/drafts/' + draft.id)).json()).toEqual(draft);
  await review(page);
  await page.getByLabel('Vognløp', { exact: true }).fill('0007');
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Gjennomgå lagret utkast' })).toBeDisabled();
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Gjennomgå lagret utkast' })).toBeEnabled();
  await review(page); await decide(page);
  await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  const plan = page.getByRole('region', { name: 'Bekreftet plan', exact: true });
  await expect(plan).toBeVisible();
  await expect(plan.getByRole('heading', { name: 'Bekreftet plan · versjon 2' })).toBeVisible();
  await plan.getByText('Godtatte ukjente fakta', { exact: true }).click();
  await expect(plan.getByText('Buss/vogn er ukjent.', { exact: true })).toHaveCount(0);
  await expect(plan.getByText(/from_place|source_start|operation_id/)).toHaveCount(0);
  expect(await page.evaluate(async () => ({ local: Object.keys(localStorage), session: Object.keys(sessionStorage), databases: (await indexedDB.databases()).map(d => d.name) })) ).toEqual({ local: [], session: [], databases: [] });
});

test('accepted confirmation with invalid reply stays uncertain and resolves through authorized lookup', async ({ page, context }) => {
  await page.clock.install();
  await login(page); await seed(page, context, 'trip'); await review(page); await decide(page);
  await page.route('**:8001/drafts/*/confirm', async route => {
    const response = await route.fetch(); expect(response.status()).toBe(200);
    await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>synthetic lost acknowledgement</html>' });
  });
  await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toHaveText('Bekreftelsen er uavklart. Behold siden åpen og kontroller eller prøv samme bekreftelse igjen.');
  await expect(page.getByLabel('Vognløp', { exact: true })).toBeDisabled();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  expect(await page.evaluate(() => { const event = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(event); return event.defaultPrevented; })).toBe(true);
  page.once('dialog', async dialog => { expect(dialog.type()).toBe('confirm'); await dialog.dismiss(); });
  await page.getByRole('link', { name: 'Åpne fiktiv demo', exact: true }).click();
  await expect(page).toHaveURL(/\/private$/);
  await expect(page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true })).toBeEnabled();
  // The accepted snapshot/operation can outlive the source's seven-day clock.
  // Keep the unresolved identity even though the original draft now expires.
  await page.clock.fastForward(7 * 86400000 + 10000);
  await expect(page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true })).toBeEnabled();
  await page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
  await expect(page.getByLabel('Vognløp', { exact: true })).toBeDisabled();
});

for (const [classification, label] of [['Instruktør', 'Instruktør'], ['Sign-on', 'Oppmøte']]) test(`advertised ${classification} classification preserves source facts and accepted plans refresh discovery`, async ({ page, context }) => {
  await login(page); const draft = await seed(page, context, 'Fiktiv ukjent type'); await review(page);
  await page.getByRole('combobox').selectOption({ label });
  for (const box of await page.getByRole('region', { name: 'Gjennomgått versjon' }).getByRole('checkbox').all()) await box.check();
  await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
  await preparation(page); await expect(page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toBeVisible(); await planScreen(page);
  const plans = await (await context.request.get(API + '/workdays')).json();
  const plan = await (await context.request.get(API + '/workdays/' + plans.workdays[0].id)).json();
  expect(plan.draft).toEqual(draft.draft);
  expect(plan.classifications).toEqual({ [draft.draft.activities[0].id]: classification });
  const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
  for (const reopened of [false, true]) {
    if (reopened) { await preparation(page); await planScreen(page); await page.getByRole('button', { name: 'Lukk planen', exact: true }).click(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); }
    await expect(day).toContainText(`Oppgitt type: Fiktiv ukjent type · Bekreftet klassifisering: ${label}`);
    await expect(day.locator('.day-activity').getByRole('heading', { name: label, exact: true })).toBeVisible();
    if (classification === 'Sign-on') { await expect(day.locator('.day-reporting')).toContainText('02.01.2031, 10:00'); await expect(day).not.toContainText('ingen bekreftet Sign-on'); }
    else await expect(day).toContainText('Ukjent · ingen bekreftet Sign-on');
  }
});

test('accepted plan remains visible when automatic discovery refresh fails', async ({ page, context }) => {
  await login(page); await seed(page, context); await review(page); await decide(page);
  await page.route('**:8001/workdays', route => route.abort());
  await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Planen er bekreftet. Planlisten kunne ikke oppdateres.');
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true })).toHaveCount(0);
});

test('reopening rejects a snapshot that omits required classification decisions', async ({ page, context }) => {
  await login(page); const draft = await seed(page, context);
  const plan = await confirmSaved(context, draft);
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await page.route('**:8001/workdays/' + plan.id, route => route.fulfill({ json: { ...plan, classifications: {} } }));
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('kunne ikke bekrefte');
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
});

test('two-page discovery retains earlier summaries and reopens a later-page plan using its cursor', async ({ page, context }) => {
  await login(page); const firstDraft = await seed(page, context, 'trip');
  const first = await confirmSaved(context, firstDraft);
  const secondDraft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { ...firstDraft.draft, service_date: '2032-02-03' } });
  const second = await confirmSaved(context, secondDraft);
  const summary = (plan: any) => ({ id: plan.id, source_draft_id: plan.source_draft_id, source_revision: plan.source_revision, service_date: plan.draft.service_date, expires_at: plan.expires_at });
  const cursors: (string | null)[] = [];
  await page.route('**:8001/workdays?*', async route => {
    const cursor = new URL(route.request().url()).searchParams.get('cursor'); cursors.push(cursor);
    await route.fulfill({ json: { workdays: [summary(second)], next_cursor: null } });
  });
  await page.route('**:8001/workdays', route => route.fulfill({ json: { workdays: [summary(first)], next_cursor: first.id } }));
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toBeVisible();
  await preparation(page); await page.getByRole('button', { name: 'Last flere planer', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Åpne plan 2032-02-03 · versjon 1', exact: true })).toBeVisible();
  expect(cursors).toEqual([first.id]);
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2032-02-03 · versjon 1', exact: true }).click();
  const reopened = page.getByRole('region', { name: 'Bekreftet plan', exact: true });
  await expect(reopened).toBeVisible(); await expect(reopened.getByRole('region', { name: 'Dagsoversikt', exact: true }).getByText('2032-02-03', { exact: true })).toBeVisible();
});

test('corrected imported draft retains readable original source facts in review and reopened plan', async ({ page, context }) => {
  await login(page);
  const imported = JSON.parse(python('import sys\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nfrom app.pdf_import import parse_document\nfrom app.private_import import interpret\nprint(interpret(parse_document(synthetic_text_pdf())).model_dump_json())\n'));
  const source = structuredClone(imported.import_metadata);
  imported.service_date = '2031-01-02';
  imported.activities.forEach((activity: any, i: number) => { activity.start = `2031-01-02T10:0${i}+01:00`; activity.end = activity.start; });
  imported.activities[0].from_place = 'Manuelt rettet sted';
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: imported });
  await preparation(page); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click();
  await review(page);
  const reviewed = page.getByRole('region', { name: 'Gjennomgått versjon' });
  await expect(reviewed.getByText('Manuelt rettet sted', { exact: true })).toBeVisible();
  await reviewed.getByText('Bevarte kildefakta', { exact: true }).click();
  await expect(reviewed.getByRole('region', { name: 'Kildefakta fra PDF', exact: true }).getByText(/^2030-01-01/).first()).toBeVisible();
  await decide(page); await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  const confirmed = page.getByRole('region', { name: 'Bekreftet plan', exact: true });
  await expect(confirmed).toBeVisible(); await planScreen(page); await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  const row = confirmed.getByRole('region', { name: 'Dagsoversikt', exact: true }).locator(`[data-activity-id="${draft.draft.activities[0].id}"]`);
  await row.getByText('Kilde og rettelser · aktivitet 1', { exact: true }).click();
  await expect(row.getByText('Fra sted · rettet', { exact: true })).toBeVisible();
  await expect(row).toContainText(`Bekreftet: Manuelt rettet sted · Opprinnelig: ${source.activities[0].origin ?? 'Ukjent'}`);
  await expect(row.getByText('Rettet fra opprinnelig tolkning.', { exact: true })).toBeVisible();
  await confirmed.getByText('Bekreftede detaljer og historisk kilde', { exact: true }).click();
  await expect(confirmed.getByText('Manuelt rettet sted', { exact: true })).toBeVisible();
  await confirmed.getByText('Bevarte kildefakta', { exact: true }).click();
  await expect(confirmed.getByRole('region', { name: 'Kildefakta fra PDF', exact: true }).getByText(/^2030-01-01/).first()).toBeVisible();
  const plans = await (await context.request.get(API + '/workdays')).json();
  const stored = await (await context.request.get(API + '/workdays/' + plans.workdays[0].id)).json();
  expect(stored.draft).toEqual(draft.draft); expect(stored.draft.import_metadata).toEqual(source);
});

test('expired plan summaries are removed and delayed expired lists cannot repopulate them', async ({ page }) => {
  await page.clock.install(); await login(page);
  const summary = { id: randomUUID(), source_draft_id: randomUUID(), source_revision: 1, service_date: '2032-02-03', expires_at: new Date(Date.now() + 3000).toISOString() };
  await page.route('**:8001/workdays', route => route.fulfill({ json: { workdays: [summary], next_cursor: null } }));
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Åpne plan 2032-02-03 · versjon 1', exact: true })).toBeVisible();
  await page.clock.fastForward(4000);
  await expect(page.getByRole('button', { name: 'Åpne plan 2032-02-03 · versjon 1', exact: true })).toHaveCount(0);
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('kunne ikke bekrefte');
  await expect(page.getByRole('button', { name: 'Åpne plan 2032-02-03 · versjon 1', exact: true })).toHaveCount(0);
});

test('wrong snapshot acknowledgement is rejected and identical retry settles the same operation', async ({ page, context }) => {
  await login(page); const draft = await seed(page, context, 'trip'); await review(page); await decide(page);
  let planId = '';
  await page.route('**:8001/drafts/*/confirm', async route => {
    const response = await route.fetch(); const value = await response.json(); planId = value.id;
    await route.fulfill({ json: { ...value, source_draft_id: randomUUID() } });
  });
  await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toHaveText('Bekreftelsen er uavklart. Behold siden åpen og kontroller eller prøv samme bekreftelse igjen.');
  await page.unroute('**:8001/drafts/*/confirm');
  await page.getByRole('button', { name: 'Prøv samme bekreftelse igjen', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toBeVisible();
  const plans = await (await context.request.get(API + '/workdays')).json();
  expect(plans.workdays.filter((v: any) => v.source_draft_id === draft.id).map((v: any) => v.id)).toEqual([planId]);
});

for (const width of [768, 1440]) for (const night of [false, true]) test(`review and reopen at ${width}px ${night ? 'Night' : 'Day'}`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: 1000 });
  await login(page); await seed(page, context); if (night) await page.getByRole('button', { name: 'Nattmodus' }).click();
  await review(page);
  await expect(page.getByRole('heading', { name: 'Gjennomgå og bekreft' })).toBeFocused();
  const region = page.getByRole('region', { name: 'Gjennomgått versjon' });
  await region.screenshot({ path: `../docs/evidence/11-2-regression-10-3-review-${width}-${night ? 'night' : 'day'}.png` });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  const select = region.getByRole('combobox'); await select.focus(); await page.keyboard.press('m'); await page.keyboard.press('Tab');
  await decide(page); await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  const confirmed = page.getByRole('region', { name: 'Bekreftet plan', exact: true });
  await expect(confirmed).toBeVisible(); await confirmed.getByText('Godtatte ukjente fakta', { exact: true }).click();
  await confirmed.screenshot({ path: `../docs/evidence/11-2-regression-10-3-confirmed-${width}-${night ? 'night' : 'day'}.png` });
  await planScreen(page); await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await preparation(page); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).last().click();
  await expect(confirmed).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
