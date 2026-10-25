import { test, expect, API, setup, openedPlan, selected, activityStatus, dayScreen, activityScreen, account, python, post, randomUUID, beforeUnload } from './private-activity-helpers';
import { writeFileSync } from 'node:fs';

setup();
const fact = (page: Parameters<typeof selected>[0], name: string) => selected(page).locator('.selected-facts > div').filter({ has: page.getByText(name + ':', { exact: true }) }).locator('dd');

test('literal Oslo offset transition and passenger unknown rows remain independent', async ({ page, context }) => {
  await openedPlan(page, context, true, undefined, undefined, false, content => {
    content.service_date = '2026-10-25'; Object.assign(content.activities[0], { start: '2026-10-25T02:55+02:00', end: '2026-10-25T02:05+01:00', line: null, trip: null, direction: ' ' });
  });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(fact(page, 'Planlagt start')).toHaveText('25.10.2026, 02:55');
  await expect(fact(page, 'Planlagt slutt')).toHaveText('25.10.2026, 02:05');
  for (const field of ['Linje', 'Turnummer', 'Retning']) await expect(fact(page, field)).toHaveText('Ukjent');
});

test('Back cancels held next auto-open while preserving the acknowledged selection', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await expect(selected(page)).toBeVisible();
  let release!: () => void, entered!: () => void; const held = new Promise<void>(r => release = r), received = new Promise<void>(r => entered = r);
  await page.route('**:8001/workdays/' + plan.id + '/selection', async route => { if (route.request().method() === 'GET') return route.continue(); const response = await route.fetch(); entered(); await held; await route.fulfill({ response }); });
  try {
    await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click(); await received;
    await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
    await expect(page.getByRole('button', { name: 'Åpne aktivitet 1', exact: true })).toBeFocused(); release();
    await expect(activityStatus(page)).toHaveText('Aktivitetsvalget er lagret.'); await expect(selected(page)).toHaveCount(0);
    expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).activity_id).toBe(activities[1].id);
    await page.getByRole('button', { name: 'Åpne aktivitet 2', exact: true }).click(); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[1].id);
  } finally { release(); }
});

test('loading and failed next choice preserve focused Back and recovery controls', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await expect(selected(page)).toBeVisible();
  let release!: () => void, entered!: () => void; const held = new Promise<void>(r => release = r), received = new Promise<void>(r => entered = r);
  await page.route('**:8001/workdays/' + plan.id + '/selection', async route => { if (route.request().method() === 'GET') return route.continue(); entered(); await held; await route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } }); });
  try {
    await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click(); await received;
    const back = page.getByRole('button', { name: 'Tilbake til dagen', exact: true }); await back.focus(); release();
    await expect(activityStatus(page)).toHaveText('Forsøket er uavklart. Kontroller eller prøv samme forsøk.'); await expect(back).toBeFocused();
    const retry = page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true }); await retry.focus(); await expect(retry).toBeFocused();
  } finally { release(); }
});

test('long day grouped pause Back restores selected Open and consultation writes nothing', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context, false, undefined, undefined, false, content => { content.activities[0].from_place = 'Lang syntetisk forklaring '.repeat(10); });
  await page.getByRole('button', { name: 'Velg aktivitet 2', exact: true }).click(); await expect(selected(page)).toBeVisible();
  await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click(); await expect(selected(page)).toContainText('Kaffepause');
  await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click(); await expect(selected(page)).toContainText('Matpause');
  let writes = 0; page.on('request', request => { if (request.method() === 'POST' && request.url().includes('/workdays/')) writes++; });
  await dayScreen(page); const open = page.getByRole('button', { name: 'Åpne aktivitet 4', exact: true }); await expect(open).toBeFocused(); await expect(open).toBeInViewport();
  await expect(page.getByRole('button', { name: 'Velg aktivitet 4', exact: true })).toBeDisabled(); await open.click(); await expect(selected(page)).toContainText('Matpause');
  await dayScreen(page); await expect(open).toBeFocused(); expect(writes).toBe(0);
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).activity_id).toBe(plan.draft.activities[3].id);
});

test('different pending confirmation survives retained old plan expiry and resolves its original operation', async ({ page, context }) => {
  await page.clock.install(); const { plan } = await openedPlan(page, context, true, -604795);
  await page.clock.setSystemTime(new Date(Date.parse(plan.expires_at) - 15000));
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await page.getByRole('button', { name: `Åpne plan ${plan.draft.service_date} · versjon 1`, exact: true }).click(); await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
  const source = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: '2031-01-02', activities: [{ id: randomUUID(), type: 'manual', start: '2031-01-02T12:00+01:00', end: '2031-01-02T13:00+01:00' }] } });
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click(); await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click(); await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true })).toBeEnabled();
  let operation = '', accepted: any;
  await page.route('**:8001/drafts/' + source.id + '/confirm', async route => { operation = route.request().postDataJSON().operation_id; accepted = await (await route.fetch()).json(); await route.abort(); });
    await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
    await expect(page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true })).toBeEnabled();
    await page.clock.fastForward(20000);
    await expect(page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true })).toBeEnabled();
    expect(await beforeUnload(page)).toBe(true); await expect(page.getByRole('region', { name: 'Gjennomgått versjon', exact: true })).toBeVisible();
    await page.unroute('**:8001/drafts/' + source.id + '/confirm');
    const lookup = page.waitForRequest(request => request.url().endsWith('/workday-operations/' + operation));
    await page.getByRole('button', { name: 'Kontroller bekreftelsen', exact: true }).click(); await lookup;
    await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible(); expect(accepted.id).not.toBe(plan.id);
    expect(await (await context.request.get(API + '/workdays/' + accepted.id)).json()).toEqual(accepted);
    expect(await beforeUnload(page)).toBe(false);
});

test('delayed same-plan denial clears orphaned activity mode and exposes preparation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await expect(selected(page)).toBeVisible(); await dayScreen(page);
  let release!: () => void, entered!: () => void; const held = new Promise<void>(r => release = r), received = new Promise<void>(r => entered = r);
  await page.route('**:8001/workdays/' + plan.id, async route => { entered(); await held; await route.fulfill({ status: 404, json: { detail: 'synthetic denial' } }); });
  try {
    await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await received;
    await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click(); await activityScreen(page); release();
    await expect(selected(page)).toHaveCount(0); await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true })).toBeEnabled();
    await expect(page.getByRole('status', { name: 'Bekreftelsesstatus', exact: true })).toContainText('Tilgangen ble avvist');
  } finally { release(); }
});

test('delayed upload failure leaves edited draft and focus intact', async ({ page, context }) => {
  await openedPlan(page, context); let release!: () => void, entered!: () => void;
  const held = new Promise<void>(r => release = r), received = new Promise<void>(r => entered = r);
  await page.route('**:8001/imports/pdf', async route => { entered(); await held; await route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } }); });
  try {
    await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click(); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-synthetic') }); await received;
    await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click(); const input = page.getByLabel('Vognløp', { exact: true }); await input.fill('Behold etter feil'); release();
    await expect(page.getByRole('region', { name: 'Importer tekst-PDF', exact: true, includeHidden: true })).toContainText('PDF-en kunne ikke tolkes');
    await expect(input).toBeFocused(); await expect(input).toHaveValue('Behold etter feil');
    await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click(); await expect(page.getByText('PDF-en kunne ikke tolkes.', { exact: false })).toBeVisible();
  } finally { release(); }
});
test('exact acknowledged member dates, opposite directions, identical members and pause members survive consultation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context, false, undefined, undefined, false, content => {
    content.activities[1].line = '20';
    content.activities[4].source_start = '24:00'; content.activities[4].source_end = '24:10';
  });
  let writes = 0;
  page.on('request', req => { if (req.method() === 'POST' && /\/workdays\//.test(req.url())) writes++; });
  const before = await Promise.all(['', '/selection', '/lifecycle', '/physical-bus'].map(async path => { const response = await context.request.get(API + '/workdays/' + plan.id + path); expect(response.status()).toBe(200); return response.json(); }));
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  for (let i = 0; i < plan.draft.activities.length; i++) {
    const activity = plan.draft.activities[i];
    await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activity.id);
    await expect(selected(page)).toContainText(`Manuelt valgt · Aktivitet ${i + 1} av 5`);
    await expect(fact(page, 'Planlagt start')).toHaveText(['02.01.2031, 23:00', '02.01.2031, 23:00', '02.01.2031, 23:10', '02.01.2031, 23:20', '03.01.2031, 00:00'][i]);
    await expect(fact(page, 'Planlagt slutt')).toHaveText(['02.01.2031, 23:10', '02.01.2031, 23:10', '02.01.2031, 23:20', '02.01.2031, 23:30', '03.01.2031, 00:10'][i]);
    await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeHidden();
    await expect(page.getByRole('region', { name: 'Fysisk buss', exact: true })).toBeHidden();
    await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toBeHidden();
    await expect(page.getByText('Stoppdata er ikke tilgjengelig i denne visningen.', { exact: true })).toBeVisible();
    if (i === 0) { await expect(fact(page, 'Retning')).toHaveText('Nord'); await expect(page.getByRole('button', { name: 'Ingen forrige aktivitet', exact: true })).toBeDisabled(); }
    if (i === 1) await expect(fact(page, 'Retning')).toHaveText('Sør');
    if (i < 4) await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click();
  }
  await expect(page.getByRole('button', { name: 'Ingen neste aktivitet', exact: true })).toBeDisabled();
  const savedSelection = await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json();
  const count = writes;
  await dayScreen(page); await expect(page.getByRole('button', { name: 'Åpne aktivitet 5', exact: true })).toBeFocused();
  await activityScreen(page); await expect(activityStatus(page)).toBeFocused();
  await dayScreen(page);
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click(); await activityScreen(page);
  expect(writes).toBe(count);
  const after = await Promise.all(['', '/selection', '/lifecycle', '/physical-bus'].map(async path => { const response = await context.request.get(API + '/workdays/' + plan.id + path); expect(response.status()).toBe(200); return response.json(); }));
  expect(after).toEqual([before[0], savedSelection, before[2], before[3]]);
  await page.reload(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await activityScreen(page);
  await expect(selected(page)).toHaveAttribute('data-selected-activity-id', plan.draft.activities[4].id);
});

test('identical facts retain member ordinal and saved identity', async ({ page, context }) => {
  const { activities } = await openedPlan(page, context, false, undefined, undefined, true);
  for (const i of [0, 1]) {
    await dayScreen(page); await page.getByRole('button', { name: `Velg aktivitet ${i + 1}`, exact: true }).click();
    await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[i].id);
    await expect(selected(page)).toContainText(`Aktivitet ${i + 1} av 5`);
  }
});

for (const kind of ['deadhead', 'CAR', 'Travel to', 'Sign-on']) test(`missing ${kind} places and irrelevant fields remain neutral`, async ({ page, context }) => {
  await openedPlan(page, context, true, undefined, kind, false, content => { Object.assign(content.activities[0], { from_place: '  ', to_place: null, trip: null, uncertainty: 'Kontroller sted med kilden' }); });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(fact(page, 'Fra')).toHaveText('Ukjent'); await expect(fact(page, 'Til')).toHaveText('Ukjent');
  await expect(selected(page).getByText('Linje:', { exact: true })).toHaveCount(0); await expect(selected(page).getByText('Retning:', { exact: true })).toHaveCount(0);
  if (['deadhead', 'CAR'].includes(kind)) await expect(fact(page, 'Turnummer')).toHaveText('Ukjent');
  else await expect(selected(page).getByText('Turnummer:', { exact: true })).toHaveCount(0);
  if (kind === 'Travel to') { await expect(fact(page, 'Aktivitetstype')).toHaveText('Reise til'); await expect(selected(page)).not.toContainText('CAR'); }
  await expect(selected(page)).toContainText('Gjeldende usikkerhet: Kontroller sted med kilden');
  await expect(page.getByRole('button', { name: 'Ingen forrige aktivitet', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Ingen neste aktivitet', exact: true })).toBeDisabled();
});

test('confirmed classification determines selected labels without new acknowledgement', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context, true, undefined, undefined, false, content => { content.activities[0].type = 'CUSTOM'; }, { '0': 'Travel to' });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(fact(page, 'Aktivitetstype')).toHaveText('Reise til');
  await expect(selected(page)).toContainText('Valgt aktivitet'); await expect(fact(page, 'Linje')).toHaveText('20');
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
});

test('current uncertainty and located neutral markers stay separate from historical and unlocated source issues', async ({ page, context }) => {
  const imported = JSON.parse(python('import sys\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nfrom app.pdf_import import parse_document\nfrom app.private_import import interpret\nprint(interpret(parse_document(synthetic_text_pdf())).model_dump_json())\n'));
  await openedPlan(page, context, true, undefined, undefined, false, content => {
    const metadata = imported.import_metadata;
    const source = metadata.activities[0]; source.activity_id = content.activities[0].id;
    for (const points of Object.values(source.provenance)) if (Array.isArray(points)) for (const point of points) Object.assign(point, { page: 1, column: 1, line: 1 });
    metadata.annotations = [{ value: 'A', meaning: null, provenance: { page: 1, column: 1, line: 1 } }, { value: 'U', meaning: null, provenance: { page: 1, column: null, line: null } }];
    metadata.unresolved = [{ code: 'missing_endpoint', activity: source.source_order, field: 'destination', provenance: { page: 1, column: 1, line: 1 } }];
    content.import_metadata = metadata;
    content.activities[0].uncertainty = 'Gjeldende notat. Kildemerket A har ukjent betydning (side 1). Kildemerket U har ukjent betydning (side 1).';
    content.activities[0].to_place = 'Rettet bekreftet sted';
  });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(selected(page)).toContainText('Gjeldende usikkerhet: Gjeldende notat.');
  await expect(selected(page)).toContainText('Kildemerke: A (side 1).');
  await expect(selected(page)).not.toContainText('Kildemerke: U');
  await expect(selected(page)).not.toContainText('Endested mangler');
  await expect(fact(page, 'Til')).toHaveText('Rettet bekreftet sted');
  await dayScreen(page);
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toContainText('Opprinnelig kildeusikkerhet');
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toContainText('Endested mangler');
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toContainText('Kildemerke: U (side 1).');
});

test('uploaded synthetic document passes separate interpretation editor confirmation day and activity screens', async ({ page, context }) => {
  const pdf = Buffer.from(python('import sys, base64\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nprint(base64.b64encode(synthetic_text_pdf()).decode())\n').trim(), 'base64');
  await page.goto('/private'); await page.getByLabel('Brukernavn', { exact: true }).fill(account.username); await page.getByLabel('Passord', { exact: true }).fill(account.password); await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic-11-2.pdf', mimeType: 'application/pdf', buffer: pdf });
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast', exact: true })).toBeVisible();
  await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toBeHidden();
  await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeHidden();
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Nytt manuelt utkast', exact: true })).toBeFocused();
  await expect(page.getByRole('region', { name: 'Importer tekst-PDF', exact: true })).toBeHidden();
  await page.getByLabel('Fra sted', { exact: true }).first().fill('Rettet syntetisk oppmøtested');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true })).toBeEnabled();
  await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click();
  for (const select of await page.getByRole('region', { name: 'Gjennomgått versjon', exact: true }).locator('select').all()) await select.selectOption('manual');
  for (const checkbox of await page.getByRole('checkbox').all()) await checkbox.check();
  await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeHidden();
  const plans = await (await context.request.get(API + '/workdays')).json(); const plan = await (await context.request.get(API + '/workdays/' + plans.workdays[0].id)).json();
  const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true });
  await bus.fill('SYNTHETIC-11-2'); await page.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bussstatus', exact: true })).toContainText('lagret');
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  const before = await Promise.all(['/physical-bus', '/lifecycle'].map(async path => { const response = await context.request.get(API + '/workdays/' + plan.id + path); expect(response.status()).toBe(200); return response.json(); }));
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(fact(page, 'Fra')).toHaveText('Rettet syntetisk oppmøtested');
  await dayScreen(page); await expect(bus).toHaveValue('SYNTHETIC-11-2');
  await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
  const after = await Promise.all(['/physical-bus', '/lifecycle'].map(async path => { const response = await context.request.get(API + '/workdays/' + plan.id + path); expect(response.status()).toBe(200); return response.json(); })); expect(after).toEqual(before);
  await page.reload(); await page.getByRole('button', { name: `Åpne plan ${plan.draft.service_date} · versjon 1`, exact: true }).click(); await activityScreen(page); await expect(fact(page, 'Fra')).toHaveText('Rettet syntetisk oppmøtested');
});

test('unsaved draft time input survives preparation and plan navigation; bus and start recovery stay reachable', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click();
  await page.getByRole('button', { name: 'Legg til aktivitet', exact: true }).click();
  const clock = page.getByLabel('Starttid', { exact: true });
  await clock.fill('12:34');
  await page.getByLabel('Fra sted', { exact: true }).fill('Ulagret sted');
  await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click();
  await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click();
  await expect(clock).toHaveValue('12:34'); await expect(page.getByLabel('Fra sted', { exact: true })).toHaveValue('Ulagret sted');
  await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click();
  const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true });
  await bus.fill('Ulagret buss');
  await expect(page.getByRole('button', { name: 'Forberedelse og planlister', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Velg aktivitet 1', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  const path = '/workdays/' + plan.id + '/start';
  await page.route('**:8001' + path, async route => { await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller skiftstarten', exact: true })).toBeEnabled();
  await expect(page.getByRole('button', { name: 'Forberedelse og planlister', exact: true })).toBeDisabled();
  await page.unroute('**:8001' + path); await page.getByRole('button', { name: 'Kontroller skiftstarten', exact: true }).click();
  const selectionPath = '/workdays/' + plan.id + '/selection';
  await page.route('**:8001' + selectionPath, async route => { if (route.request().method() === 'GET') return route.continue(); await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true })).toBeEnabled();
  await expect(page.getByRole('button', { name: 'Forberedelse og planlister', exact: true })).toBeDisabled();
  await expect(selected(page)).toHaveCount(0);
  await page.unroute('**:8001' + selectionPath); await page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true }).click();
  await expect(selected(page)).toBeVisible();
  await dayScreen(page); await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
});

test('expired draft keeps preparation and an explicit empty recovery reachable', async ({ page, context }) => {
  await page.clock.install(); const { draft, plan } = await openedPlan(page, context);
  python(`with database() as conn:\n conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days'+interval '2 minutes',expires_at=statement_timestamp()+interval '2 minutes' WHERE id=%s", (${JSON.stringify(draft.id)},))\n`);
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Rediger utkast', exact: true })).toBeVisible();
  await page.clock.fastForward(180000);
  await expect(page.getByRole('region', { name: 'Private utkast', exact: true }).getByRole('status')).toContainText('Utkastet er utløpt.');
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Nytt utkast', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeEnabled();
  await expect(page.getByLabel('Starttid', { exact: true })).toHaveCount(0);
  await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
});

test('held selection acknowledgement cannot hide a bus proposal created while saving', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  let release!: () => void, entered!: () => void;
  const held = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  await page.route('**:8001/workdays/' + plan.id + '/selection', async route => {
    if (route.request().method() === 'GET') return route.continue();
    const response = await route.fetch(); entered(); await held; await route.fulfill({ response });
  });
  try {
    await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await received;
    const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true });
    await bus.fill('Behold bussforslaget'); await expect(bus).toBeFocused(); release();
    await expect(activityStatus(page)).toHaveText('Aktivitetsvalget er lagret.');
    await expect(selected(page)).toHaveCount(0); await expect(bus).toBeVisible(); await expect(bus).toHaveValue('Behold bussforslaget'); await expect(bus).toBeFocused();
    await expect(page.getByRole('button', { name: 'Åpne valgt aktivitet', exact: true })).toBeDisabled();
    await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
    await activityScreen(page); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', plan.draft.activities[0].id);
  } finally { release(); }
});

test('held upload completion retains edited draft and offers an explicit return to interpretation', async ({ page, context }) => {
  await openedPlan(page, context);
  const pdf = Buffer.from(python('import sys, base64\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nprint(base64.b64encode(synthetic_text_pdf()).decode())\n').trim(), 'base64');
  let release!: () => void, entered!: () => void;
  const held = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  await page.route('**:8001/imports/pdf', async route => { const response = await route.fetch(); entered(); await held; await route.fulfill({ response }); });
  try {
    await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
    await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'held-synthetic.pdf', mimeType: 'application/pdf', buffer: pdf }); await received;
    await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click();
    await page.getByLabel('Vognløp', { exact: true }).fill('Behold dette forslaget');
    release(); await expect(page.getByRole('button', { name: 'Fortsett importgjennomgang', exact: true, includeHidden: true })).toHaveCount(1);
    await expect(page.getByRole('heading', { name: 'Nytt manuelt utkast', exact: true })).toBeVisible();
    await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('Behold dette forslaget');
    await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
    await page.getByRole('button', { name: 'Fortsett importgjennomgang', exact: true }).click();
    await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast', exact: true })).toBeVisible();
    await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click();
    await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('Behold dette forslaget');
  } finally { release(); }
});

test('held parent plan read cannot pull the user away from an edited draft', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  let release!: () => void, entered!: () => void;
  const held = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  await page.route('**:8001/workdays/' + plan.id, async route => { const response = await route.fetch(); entered(); await held; await route.fulfill({ response }); });
  try {
    await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
    await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await received;
    await page.getByRole('button', { name: 'Kontroller og rediger utkast', exact: true }).click();
    await page.getByLabel('Vognløp', { exact: true }).fill('Ikke flytt dette utkastet'); release();
    await expect(page.locator('.private-confirmation')).toHaveAttribute('aria-busy', 'false');
    await expect(page.getByRole('heading', { name: 'Nytt manuelt utkast', exact: true })).toBeVisible();
    await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('Ikke flytt dette utkastet');
    await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeHidden();
  } finally { release(); }
});

for (const width of [768, 1024, 1440]) for (const night of [false, true]) test(`activity facts keyboard and enlargement ${width} ${night ? 'Night' : 'Day'}`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: width === 1024 ? 768 : 1100 }); await openedPlan(page, context);
  if (night) await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).focus(); await page.keyboard.press('Enter');
  await expect(selected(page)).toBeVisible(); await expect(activityStatus(page)).toBeFocused();
  await expect(fact(page, 'Til')).toContainText('Fiktivt langt destinasjonsnavn');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  const measurements: object[] = [];
  for (const name of ['Neste aktivitet', 'Tilbake til dagen']) {
    const button = page.getByRole('button', { name, exact: true }); await button.focus(); await expect(button).toBeFocused();
    expect(await button.evaluate(el => el.getBoundingClientRect().height)).toBeGreaterThanOrEqual(58);
    const measured = await button.evaluate(el => {
      const light = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
      const ratio = (a: string, b: string) => (Math.max(light(a), light(b)) + .05) / (Math.min(light(a), light(b)) + .05);
      const bg = (node: Element): string => { const c = getComputedStyle(node).backgroundColor; return c === 'rgba(0, 0, 0, 0)' || c === 'transparent' ? node.parentElement ? bg(node.parentElement) : 'rgb(255,255,255)' : c; };
      const style = getComputedStyle(el);
      const detail = document.querySelector('.selected-activity')!;
      const text = [...detail.querySelectorAll('h3,p,dt,dd')].map(node => ratio(getComputedStyle(node).color, bg(node)));
      return { text: Math.min(...text), boundary: ratio(getComputedStyle(detail).borderInlineStartColor, bg(detail.parentElement!)), focus: ratio(style.outlineColor, bg(el.parentElement!)), focusWidth: parseFloat(style.outlineWidth) };
    });
    expect(measured.text).toBeGreaterThanOrEqual(4.5); expect(measured.boundary).toBeGreaterThanOrEqual(3);
    expect(measured.focus).toBeGreaterThanOrEqual(3); expect(measured.focusWidth).toBeGreaterThanOrEqual(2);
    measurements.push({ control: name, ...measured });
    await test.info().attach(`11-2-${width}-${night ? 'night' : 'day'}-${name}`, { body: JSON.stringify(measured), contentType: 'application/json' });
  }
  await page.getByRole('region', { name: 'Bekreftet plan', exact: true }).screenshot({ path: `../docs/evidence/11-2-activity-${width}-${night ? 'night' : 'day'}.png` });
  for (const control of [fact(page, 'Planlagt slutt'), fact(page, 'Til'), page.getByRole('button', { name: 'Kontroller plantilgang og aktivitetsvalg', exact: true }), page.getByRole('button', { name: 'Tilbake til dagen', exact: true })]) { await control.scrollIntoViewIfNeeded(); await expect(control).toBeInViewport(); }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: `../docs/evidence/11-2-activity-viewport-enlarged-${width}-${night ? 'night' : 'day'}.png` });
  await page.setViewportSize({ width, height: width === 1024 ? 768 : 1100 });
  await page.evaluate(() => { document.documentElement.style.fontSize = ''; window.scrollTo(0, 0); });
  expect(await fact(page, 'Planlagt start').evaluate(el => el.getBoundingClientRect().top)).toBeLessThan(450);
  if (width === 1024) for (const endpoint of ['Fra', 'Til']) expect(await fact(page, endpoint).evaluate(el => el.getBoundingClientRect().bottom)).toBeLessThanOrEqual(768);
  await page.screenshot({ path: `../docs/evidence/11-2-activity-viewport-${width}-${night ? 'night' : 'day'}.png` });
  writeFileSync(`../docs/evidence/11-2-contrast-${width}-${night ? 'night' : 'day'}.json`, JSON.stringify(measurements, null, 2) + '\n');
});
