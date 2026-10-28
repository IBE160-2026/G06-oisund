import { test, expect, API, account, setup, post } from './private-activity-helpers';
import { editor, preparation } from './private-screen-helpers';
import { readFileSync } from 'node:fs';
import type { Page, BrowserContext } from '@playwright/test';
setup();
const oracle = JSON.parse(readFileSync('../Eksempelfiler/Fasit-testskift.json', 'utf8').replace(/^\uFEFF/, '')).shifts.find((shift: any) => shift.case === 'A');
const button = (page: Page, name: string) => page.getByRole('button', { name, exact: true });
async function loginAndImport(page: Page) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await button(page, 'Logg inn').click();
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('../Eksempelfiler/Testskift-A.pdf');
  await expect(button(page, 'Alt stemmer – lagre og fortsett')).toBeVisible();
}
async function drafts(context: BrowserContext) { const response = await context.request.get(API + '/drafts'); expect(response.ok()).toBe(true); return (await response.json()).drafts; }
async function fullDraft(context: BrowserContext, id: string) { const response = await context.request.get(API + '/drafts/' + id); expect(response.ok()).toBe(true); return response.json(); }
function assertIndependentFacts(content: any) {
  expect(content.service_date).toBe(oracle.date.split('/').reverse().join('-'));
  expect(content.import_metadata.header.shift_id).toBe(oracle.shift_id);
  expect(content.vehicle_duty).toBe(oracle.events.find((event: any) => event.kind === 'vehicle').vehicle);
  const events = oracle.events.filter((event: any) => event.kind !== 'vehicle');
  expect(content.activities).toHaveLength(events.length);
  for (const [index, event] of events.entries()) {
    const row = content.activities[index];
    const start = event.kind === 'movement' ? event.stops[0].local_datetime : event.start_local;
    const end = event.kind === 'movement' ? event.stops.at(-1).local_datetime : event.end_local;
    expect(Date.parse(row.start)).toBe(Date.parse(start + ':00+01:00'));
    expect(Date.parse(row.end)).toBe(Date.parse(end + ':00+01:00'));
    if (event.kind === 'movement') expect([row.trip, row.from_place, row.to_place]).toEqual([event.trip_id, event.stops[0].name, event.stops.at(-1).name]);
  }
}
for (const width of [768, 1440]) test(`correct import saves explicitly and reaches distinct compact approval at ${width}px`, async ({ page, context }, info) => {
  await page.setViewportSize({ width, height: 1000 }); await loginAndImport(page);
  expect(await drafts(context)).toEqual([]);
  await expect(page.getByText('Importsammendrag', { exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Kildefakta fra PDF', includeHidden: true })).toBeHidden();
  await page.screenshot({ path: info.outputPath('import-summary.png'), fullPage: true });
  await button(page, 'Alt stemmer – lagre og fortsett').click();
  const review = page.getByRole('region', { name: 'Gjennomgått versjon' }); await expect(review).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Rediger utkast', exact: true })).toBeHidden();
  await expect(review.getByText('Vis alle opplysninger i lagret versjon', { exact: true })).toBeVisible();
  const saved = await fullDraft(context, (await drafts(context))[0].id); assertIndependentFacts(saved.draft); expect(saved.revision).toBe(1);
  expect(await review.getByRole('checkbox').count()).toBeGreaterThan(0);
  for (const box of await review.getByRole('checkbox').all()) await expect(box).not.toBeChecked();
  await expect(button(page, 'Bekreft gjennomgått plan')).toBeDisabled();
  await page.screenshot({ path: info.outputPath('compact-approval.png'), fullPage: true });
  await review.getByText('Vis alle opplysninger i lagret versjon', { exact: true }).click();
  await expect(review).toContainText(oracle.start_place);
  for (const select of await review.getByRole('combobox').all()) await select.selectOption('manual');
  for (const box of await review.getByRole('checkbox').all()) await box.check();
  await button(page, 'Bekreft gjennomgått plan').click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
  await expect(button(page, 'Start skift')).toBeVisible();
  const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true });
  await bus.getByLabel('Fysisk buss', { exact: true }).fill('SYN-ONLY-BUS');
  await bus.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click();
  await expect(bus.getByRole('status', { name: 'Bussstatus' })).toHaveText('Fysisk buss er lagret.');
  expect((await fullDraft(context, saved.id)).draft).toEqual(saved.draft);
  const plans = await (await context.request.get(API + '/workdays')).json();
  const persistedBus = await (await context.request.get(API + '/workdays/' + plans.workdays[0].id + '/physical-bus')).json();
  expect(persistedBus).toEqual(expect.objectContaining({ workday_id: plans.workdays[0].id, physical_bus: 'SYN-ONLY-BUS', revision: 1 }));
  await page.reload(); await button(page, `Åpne plan ${saved.draft.service_date} · versjon 1`).click();
  await expect(bus.getByLabel('Fysisk buss', { exact: true })).toHaveValue('SYN-ONLY-BUS');
  await expect(bus).toContainText('bussversjon 1');
});
test('corrections keep save position, bus refuses unrelated proposals, and time save can proceed directly', async ({ page, context }, info) => {
  await loginAndImport(page); await button(page, 'Rett eller legg til opplysninger').click();
  const destination = page.getByLabel('Til sted', { exact: true }).nth(1);
  await destination.fill('Syntetisk rettet endeholdeplass');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('SYN-42');
  await button(page, 'Lagre buss/vogn').click();
  await expect(page.getByLabel('Buss i utkast', { exact: true })).toContainText('Buss kan ikke lagres separat nå');
  expect(await drafts(context)).toEqual([]); await expect(destination).toHaveValue('Syntetisk rettet endeholdeplass');
  const save = button(page, 'Lagre utkast'); await save.scrollIntoViewIfNeeded(); await save.focus();
  const before = await page.evaluate(() => scrollY); expect(before).toBeGreaterThan(500);
  await page.keyboard.press('Enter');
  await expect(page.getByRole('status', { name: 'Lagringsstatus' })).toHaveText('Lagret. Versjon 1.');
  expect(Math.abs(await page.evaluate(() => scrollY) - before)).toBeLessThan(100); await expect(save).toBeFocused();
  await page.screenshot({ path: info.outputPath('saved-in-position.png') });
  const saved = await fullDraft(context, (await drafts(context))[0].id);
  expect(saved.draft.activities[1].to_place).toBe('Syntetisk rettet endeholdeplass'); expect(saved.draft.physical_bus).toBe('SYN-42');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('SYN-43'); await button(page, 'Lagre buss/vogn').click();
  await expect(page.getByRole('status', { name: 'Lagringsstatus' })).toHaveText('Lagret. Versjon 2.');
  const busOnly = await fullDraft(context, saved.id); expect(busOnly.draft.activities).toEqual(saved.draft.activities); expect(busOnly.draft.physical_bus).toBe('SYN-43');
  const start = page.getByLabel('Starttid', { exact: true }).first(); await start.fill('06:51');
  await expect(save).toBeEnabled(); await save.click(); await expect(page.getByRole('status', { name: 'Lagringsstatus' })).toHaveText('Lagret. Versjon 3.');
  await button(page, 'Fortsett til godkjenning').click(); await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toContainText('Lagret versjon 3');
});
test('failed direct save retains original operation and only explicit recovery advances', async ({ page, context }) => {
  await loginAndImport(page);
  await page.route('**:8001/drafts', route => route.request().method() === 'POST' ? route.abort() : route.continue());
  await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('status', { name: 'Direkte lagringsstatus' })).toContainText('Lagring er uavklart');
  await expect(page.getByRole('heading', { name: 'Gjennomgå og bekreft', exact: true })).toBeHidden(); expect(await drafts(context)).toEqual([]);
  await page.unroute('**:8001/drafts'); await button(page, 'Prøv samme lagringsforsøk igjen').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible(); expect(await drafts(context)).toHaveLength(1);
});
test('new edit invalidates saved review and unfinished time cannot bypass explicit save', async ({ page, context }) => {
  await loginAndImport(page); await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible(); await editor(page);
  await page.getByLabel('Startdato', { exact: true }).first().fill('');
  await expect(button(page, 'Lagre utkast')).toBeDisabled(); await expect(button(page, 'Til godkjenning')).toBeDisabled();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toHaveCount(0); expect((await fullDraft(context, (await drafts(context))[0].id)).revision).toBe(1);
});

test('direct saving stays compact with a prior selection and creates a separate saved identity', async ({ page, context }, info) => {
  await loginAndImport(page); await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
  const original = await fullDraft(context, (await drafts(context))[0].id);
  await preparation(page);
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('../Eksempelfiler/Testskift-C.pdf');
  await expect(button(page, 'Alt stemmer – lagre og fortsett')).toBeVisible();
  const cOracle = JSON.parse(readFileSync('../Eksempelfiler/Fasit-testskift.json', 'utf8').replace(/^\uFEFF/, '')).shifts.find((shift: any) => shift.case === 'C');
  const interval = page.locator('.import-summary-interval');
  await expect(interval).toContainText(`${cOracle.start} · ${cOracle.start_place} → ${cOracle.end} · ${cOracle.end_place}`);
  await expect(interval).toContainText(`${cOracle.events[0].start_local.slice(0, 10)} – ${cOracle.events.at(-1).end_local.slice(0, 10)}`);
  let release!: () => void, entered!: () => void;
  const held = new Promise<void>(resolve => { release = resolve; }), started = new Promise<void>(resolve => { entered = resolve; });
  const writes: any[] = [];
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    writes.push(route.request().postDataJSON()); entered(); await held; await route.continue();
  });
  try {
    await button(page, 'Alt stemmer – lagre og fortsett').click(); await started;
    await expect(page.getByRole('heading', { name: 'Lagre import og fortsett', exact: true })).toBeFocused();
    await expect(page.locator('.draft-form')).toBeHidden();
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toBeHidden();
    await page.screenshot({ path: info.outputPath('compact-saving.png') });
    expect(await drafts(context)).toHaveLength(1);
    release(); await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
    const summaries = await drafts(context); expect(summaries).toHaveLength(2);
    expect(writes).toHaveLength(1); expect(writes[0].expected_revision).toBe(0);
    const second = await fullDraft(context, summaries.find((item: any) => item.id !== original.id).id);
    const independent = JSON.parse(readFileSync('../Eksempelfiler/Fasit-testskift.json', 'utf8').replace(/^\uFEFF/, '')).shifts.find((shift: any) => shift.case === 'C');
    expect(second.draft.service_date).toBe(independent.date.split('/').reverse().join('-'));
    expect(second.draft.import_metadata.header.shift_id).toBe(independent.shift_id);
    expect(await fullDraft(context, original.id)).toEqual(original);
  } finally { release(); }
});
test('committed direct save with lost response stays compact and settles the original operation once', async ({ page, context }) => {
  await loginAndImport(page); let accepted: any, command: any, posts = 0;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    posts++; command = route.request().postDataJSON(); accepted = await (await route.fetch()).json(); await route.abort();
  });
  await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('status', { name: 'Direkte lagringsstatus' })).toContainText('Lagring er uavklart');
  await expect(page.locator('.draft-form')).toBeHidden();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toHaveCount(0);
  expect(await drafts(context)).toHaveLength(1); expect((await fullDraft(context, accepted.id)).revision).toBe(1);
  const receipt = await (await context.request.get(API + '/draft-operations/' + command.operation_id)).json();
  expect(receipt.state).toBe('accepted'); expect(receipt.result.id).toBe(accepted.id);
  await button(page, 'Kontroller lagringsforsøket').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
  expect(posts).toBe(1); expect(await fullDraft(context, accepted.id)).toEqual(accepted); expect(await drafts(context)).toHaveLength(1);
});
for (const unrelated of ['content', 'time']) test(`saved-draft bus action refuses unrelated ${unrelated} and preserves both proposals`, async ({ page, context }) => {
  await loginAndImport(page); await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible(); await editor(page);
  const original = await fullDraft(context, (await drafts(context))[0].id);
  await expect(button(page, 'Lagre buss/vogn')).toBeDisabled();
  await page.getByLabel('Buss/vogn', { exact: true }).fill('SYN-UNSAVED-BUS');
  if (unrelated === 'content') await page.getByLabel('Til sted', { exact: true }).nth(1).fill('Syntetisk ulagret sted');
  else await page.getByLabel('Startdato', { exact: true }).first().fill('');
  await button(page, 'Lagre buss/vogn').click();
  await expect(page.getByLabel('Buss i utkast', { exact: true })).toContainText('Andre opplysninger er også ulagret');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('SYN-UNSAVED-BUS');
  if (unrelated === 'content') await expect(page.getByLabel('Til sted', { exact: true }).nth(1)).toHaveValue('Syntetisk ulagret sted');
  else { await expect(page.getByLabel('Startdato', { exact: true }).first()).toHaveValue(''); await expect(button(page, 'Lagre hele utkastet med buss')).toBeDisabled(); }
  expect(await fullDraft(context, original.id)).toEqual(original);
  page.once('dialog', dialog => dialog.accept()); await button(page, 'Forkast endringer').click();
  await expect(page.getByLabel('Buss i utkast', { exact: true })).not.toContainText('Andre opplysninger er også ulagret');
  await expect(page.getByLabel('Buss i utkast', { exact: true })).toContainText('Andre opplysninger er allerede lagret');
  await expect(button(page, 'Lagre buss/vogn')).toBeDisabled();
});
test('tablet first save retains open source details, viewport and replacement time-input keyboard focus', async ({ page, context }, info) => {
  await page.setViewportSize({ width: 768, height: 1000 }); await loginAndImport(page); await button(page, 'Rett eller legg til opplysninger').click();
  const details = page.locator('details.source-disclosure'); await details.locator('summary').click();
  const time = page.getByLabel('Starttid', { exact: true }).first(); await time.fill('06:51');
  await expect(button(page, 'Lagre utkast')).toBeEnabled(); await time.focus();
  const position = await page.evaluate(() => scrollY); expect(position).toBeGreaterThan(1000);
  await page.keyboard.press('Enter');
  await expect(page.getByRole('status', { name: 'Lagringsstatus' })).toHaveText('Lagret. Versjon 1.');
  await expect(details).toHaveAttribute('open', ''); await expect(time).toBeFocused();
  expect(Math.abs(await page.evaluate(() => scrollY) - position)).toBeLessThan(100);
  await expect(time).toHaveValue(/^06:51(:00)?$/);
  const saved = await fullDraft(context, (await drafts(context))[0].id); expect(saved.draft.activities[0].start).toContain('T06:51');
  await page.screenshot({ path: info.outputPath('tablet-time-focus-after-first-save.png') });
});
for (const stage of ['review', 'confirmation']) test(`competing revision before ${stage} is rejected and current revision remains reachable`, async ({ page, context }) => {
  await loginAndImport(page); await button(page, 'Rett eller legg til opplysninger').click(); await button(page, 'Lagre utkast').click();
  await expect(page.getByRole('status', { name: 'Lagringsstatus' })).toHaveText('Lagret. Versjon 1.');
  const saved = await fullDraft(context, (await drafts(context))[0].id);
  if (stage === 'confirmation') { await button(page, 'Gjennomgå lagret utkast').click(); await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible(); }
  const operation = await post(context, '/draft-operations', { draft_id: saved.id });
  const latest = await post(context, '/drafts/' + saved.id, { operation_id: operation.operation_id, expected_revision: 1, draft: { ...saved.draft, physical_bus: 'SYN-COMPETING' } }); expect(latest.revision).toBe(2);
  if (stage === 'review') await button(page, 'Gjennomgå lagret utkast').click();
  else {
    const review = page.getByRole('region', { name: 'Gjennomgått versjon' });
    for (const select of await review.getByRole('combobox').all()) await select.selectOption('manual');
    for (const box of await review.getByRole('checkbox').all()) await box.check();
    await button(page, 'Bekreft gjennomgått plan').click();
  }
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus' })).toContainText('Utkastet er endret');
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toHaveCount(0);
  expect((await (await context.request.get(API + '/workdays')).json()).workdays).toHaveLength(0);
  await preparation(page); await button(page, 'Oppdater listen').click(); await button(page, `Åpne ${saved.draft.service_date} · versjon 2`).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('SYN-COMPETING'); await button(page, 'Gjennomgå lagret utkast').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toContainText('Lagret versjon 2');
});
test('approval navigation returns from a clean notice registry to visible saved decisions', async ({ page }) => {
  await loginAndImport(page); await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
  await button(page, 'Manuelt vedlikeholdte avvik').click();
  await expect(page.getByRole('heading', { name: 'Gjennomgå og bekreft', exact: true })).toBeHidden();
  await button(page, 'Til godkjenning').click();
  await expect(page.getByRole('heading', { name: 'Gjennomgå og bekreft', exact: true })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
  await expect(button(page, 'Prøv gjennomgang på nytt')).toHaveCount(0);
});

test('held review is deduplicated while leaving and returning to approval', async ({ page }) => {
  await loginAndImport(page); await button(page, 'Rett eller legg til opplysninger').click(); await button(page, 'Lagre utkast').click();
  await expect(page.getByRole('status', { name: 'Lagringsstatus' })).toHaveText('Lagret. Versjon 1.');
  let release!: () => void, entered!: () => void, reviews = 0;
  const held = new Promise<void>(resolve => { release = resolve; }), started = new Promise<void>(resolve => { entered = resolve; });
  await page.route('**:8001/workday-reviews', async route => { reviews++; const response = await route.fetch(); entered(); await held; await route.fulfill({ response }); });
  try {
    await button(page, 'Gjennomgå lagret utkast').click(); await started;
    await editor(page); await button(page, 'Gjennomgå lagret utkast').click();
    expect(reviews).toBe(1); release();
    await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible(); await page.waitForLoadState('networkidle');
    expect(reviews).toBe(1); await expect(button(page, 'Bekreft gjennomgått plan')).toBeDisabled();
  } finally { release(); }
});
test('classification decision exposes its source code dates times and places while full facts stay collapsed', async ({ page, context }) => {
  await loginAndImport(page);
  const operation = await post(context, '/draft-operations', {});
  const saved = await post(context, '/drafts', { operation_id: operation.operation_id, expected_revision: 0, draft: { service_date: '2030-02-08', physical_bus: null, activities: [{ id: crypto.randomUUID(), type: 'SYN-UNKNOWN', raw_code: 'SYN-CODE-REQUIRED', start: '2030-02-08T23:50:00+01:00', end: '2030-02-09T00:10:00+01:00', from_place: 'Syntetisk startsted', to_place: 'Syntetisk endested' }] } });
  await preparation(page); await button(page, 'Oppdater listen').click(); await button(page, `Åpne ${saved.draft.service_date} · versjon 1`).click(); await button(page, 'Gjennomgå lagret utkast').click();
  const decision = page.locator('.classification-decision'); await expect(decision).toBeVisible();
  for (const text of ['SYN-CODE-REQUIRED', 'SYN-UNKNOWN', '23:50', '00:10', 'Syntetisk startsted', 'Syntetisk endested']) await expect(decision).toContainText(text);
  await expect(decision).toContainText(/0?8\.0?2\.2030, 23:50/); await expect(decision).toContainText(/0?9\.0?2\.2030, 00:10/);
  await expect(decision.getByRole('combobox')).toHaveValue(''); await expect(decision.getByRole('combobox')).toHaveAttribute('aria-describedby', /classification-context-/);
  await expect(page.getByText('Vis alle opplysninger i lagret versjon', { exact: true }).locator('..')).not.toHaveAttribute('open');
  await expect(button(page, 'Bekreft gjennomgått plan')).toBeDisabled();
});
test('fresh direct terminal failure with prior selection retains imported proposals and prior saved facts', async ({ page, context }) => {
  await loginAndImport(page); await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
  const original = await fullDraft(context, (await drafts(context))[0].id); await preparation(page);
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('../Eksempelfiler/Testskift-C.pdf'); await expect(button(page, 'Alt stemmer – lagre og fortsett')).toBeVisible();
  await page.route('**:8001/drafts', route => route.request().method() === 'POST' ? route.fulfill({ status: 410, json: { detail: 'Lagringsforsøket er utløpt.' } }) : route.continue());
  await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('status', { name: 'Direkte lagringsstatus' })).toContainText('Lokale inndata er beholdt');
  await expect(page.getByRole('status', { name: 'Direkte lagringsstatus' })).not.toContainText('Private felt fra det utløpte utkastet er fjernet');
  await expect(page.locator('.draft-form')).toBeHidden(); await button(page, 'Rett eller legg til opplysninger').click();
  await expect(page.getByLabel('Tjenestedato', { exact: true })).toHaveValue('2030-02-08');
  await expect(page.getByLabel('Starttid', { exact: true }).first()).toHaveValue(/^22:10(:00)?$/);
  await expect(button(page, 'Lagre utkast')).toBeDisabled(); expect(await drafts(context)).toHaveLength(1); expect(await fullDraft(context, original.id)).toEqual(original);
});
test('disappearing occurrence selector restores focus to an input in the same saved time field', async ({ page, context }) => {
  await loginAndImport(page);
  const saved = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: '2030-10-27', physical_bus: null, activities: [{ id: crypto.randomUUID(), type: 'manual', start: '2030-10-27T01:30:00+02:00', end: '2030-10-27T03:30:00+01:00' }] } });
  await preparation(page); await button(page, 'Oppdater listen').click(); await button(page, `Åpne ${saved.draft.service_date} · versjon 1`).click();
  await page.getByLabel('Starttid', { exact: true }).fill('02:30');
  const occurrence = page.getByRole('combobox', { name: 'Start: forekomst', exact: true }); await occurrence.selectOption({ label: 'Første forekomst' });
  await expect(button(page, 'Lagre utkast')).toBeEnabled(); await occurrence.focus(); const position = await page.evaluate(() => scrollY);
  // Submit the actual form while the occurrence control owns focus. The saved
  // replacement deliberately has no occurrence selector to restore by index.
  await occurrence.evaluate((control: HTMLSelectElement) => control.form!.requestSubmit());
  await expect(page.getByRole('status', { name: 'Lagringsstatus' })).toHaveText('Lagret. Versjon 2.');
  await expect(occurrence).toHaveCount(0);
  await expect(page.locator(`[data-draft-time="${saved.draft.activities[0].id}:start"] input`).first()).toBeFocused();
  expect(Math.abs(await page.evaluate(() => scrollY) - position)).toBeLessThan(100);
  expect((await fullDraft(context, saved.id)).draft.activities[0].start).toMatch(/^2030-10-27T02:30(?::00)?\+02:00$/);
});
test('direct admission failure retains compact import before a command exists and retries explicitly once', async ({ page, context }) => {
  await loginAndImport(page); let posts = 0;
  page.on('request', request => { if (request.method() === 'POST' && request.url() === API + '/drafts') posts++; });
  await page.route('**:8001/draft-operations', route => route.abort()); await button(page, 'Alt stemmer – lagre og fortsett').click();
  await expect(page.getByRole('status', { name: 'Direkte lagringsstatus' })).toContainText('Inndata er beholdt');
  await expect(page.locator('.draft-form')).toBeHidden(); await expect(button(page, 'Kontroller lagringsforsøket')).toHaveCount(0);
  expect(await drafts(context)).toEqual([]); expect(posts).toBe(0);
  await page.unroute('**:8001/draft-operations'); await button(page, 'Lagre import og prøv igjen').click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon' })).toBeVisible();
  expect(await drafts(context)).toHaveLength(1); expect(posts).toBe(1); assertIndependentFacts((await fullDraft(context, (await drafts(context))[0].id)).draft);
});
