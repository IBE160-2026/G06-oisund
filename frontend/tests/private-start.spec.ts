import { test, expect, openedPlan, API, post, randomUUID, selected, shiftStatus, beforeUnload, reopen, python, setup, relativeInstants, dayScreen, activityScreen } from './private-activity-helpers';
setup();
const oslo = (value: string) => new Intl.DateTimeFormat('nb-NO', { timeZone: 'Europe/Oslo', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(new Date(value));

test('relative fixture uses elapsed UTC durations across the Oslo autumn transition', () => {
  for (const anchor of ['2026-10-25T01:30:00+02:00', '2026-10-25T02:30:00+01:00', '2026-10-26T00:00:00+01:00']) {
    const [start, end] = relativeInstants(-604830, anchor);
    expect(Date.parse(start) - Date.parse(anchor)).toBe(-604830000);
    expect(Date.parse(end) - Date.parse(start)).toBe(60000);
    expect(Date.parse(end) + 7 * 86400000 - Date.parse(anchor)).toBe(30000);
  }
  const [start, end] = relativeInstants(-30, '2026-10-25T02:59:45+02:00');
  expect(start).toBe('2026-10-25T02:59:15+02:00');
  expect(end).toBe('2026-10-25T02:00:15+01:00');
  expect(Date.parse(end) - Date.parse(start)).toBe(60000);
});

test('independent explicit start without selection reopen reload and unchanged planned snapshot', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
  await expect(page.getByText('Ingen aktivitet valgt', { exact: true })).toBeVisible();
  await expect(page.getByText(/^Planlagt start:/)).toContainText('02.01.2031');
  const actual = await (await context.request.get(API + '/workdays/' + plan.id + '/lifecycle')).json();
  const timestamps = async () => {
    await expect(page.getByText(/^Planlagt start:/)).toHaveText(`Planlagt start: ${oslo(plan.draft.activities[0].start)}. Dette er første bekreftede aktivitetsstart.`);
    await expect(page.getByText(/^Faktisk start \(lagret av serveren\):/)).toHaveText(`Faktisk start (lagret av serveren): ${oslo(actual.started_at)}`);
    expect(oslo(actual.started_at)).not.toBe(oslo(plan.draft.activities[0].start));
  };
  await timestamps();
  await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Velg aktivitet 2', exact: true }).click(); await activityScreen(page); await expect(selected(page)).toContainText('Linje: 24');
  await dayScreen(page); await reopen(page); await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  await timestamps();
  await page.reload(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible(); await activityScreen(page); await expect(selected(page)).toContainText('Linje: 24');
  await dayScreen(page); await timestamps();
  expect(await (await context.request.get(API + '/workdays/' + plan.id + '/lifecycle')).json()).toEqual(actual);
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
});

test('explicit start after planned departure preserves its distinct authoritative actual time', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context, true, -120);
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
  const actual = await (await context.request.get(API + '/workdays/' + plan.id + '/lifecycle')).json();
  expect(Date.parse(actual.started_at)).toBeGreaterThan(Date.parse(activities[0].start!));
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
});

for (const reply of ['lost', 'html', 'malformed']) test(`uncertain ${reply} start retains same operation and never guesses success`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/start'; let original: any;
  await page.route('**:8001' + path, async route => {
    original = route.request().postDataJSON(); await route.fetch();
    if (reply === 'lost') return route.abort();
    await route.fulfill(reply === 'html' ? { status: 200, contentType: 'text/html', body: '<html>lost</html>' } : { status: 200, json: { operation_id: original.operation_id, result: {} } });
  });
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await expect(shiftStatus(page)).toContainText('uavklart');
  await expect(page.getByRole('button', { name: 'Kontroller skiftstarten', exact: true })).toBeEnabled();
  await expect(page.getByText('Startet manuelt', { exact: true })).toHaveCount(0); await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(true);
  // The day keeps unresolved start recovery reachable before another activity can open.
  await expect(page.getByRole('button', { name: 'Velg aktivitet 1', exact: true })).toBeDisabled();
  await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeDisabled();
  await page.unroute('**:8001' + path); let retry: any; page.on('request', req => { if (req.url().endsWith(path) && req.method() === 'POST') retry = req.postDataJSON(); });
  await page.getByRole('button', { name: 'Prøv samme skiftstart igjen', exact: true }).click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.'); expect(retry).toBeUndefined();
  expect((await (await context.request.get(API + '/workday-start-operations/' + original.operation_id)).json()).result.revision).toBe(original.expected_revision + 1);
  const lifecycle = await (await context.request.get(API + '/workdays/' + plan.id + '/lifecycle')).json();
  expect((await post(context, path, { operation_id: randomUUID(), expected_revision: 0 })).result).toEqual(lifecycle);
  await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(false);
});

test('another window start read and missing lifecycle remain truthful', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/lifecycle';
  const actual = (await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 })).result;
  await page.getByRole('button', { name: 'Hent skiftstatus igjen', exact: true }).click(); await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  await page.route('**:8001' + path, route => route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } }));
  await page.getByRole('button', { name: 'Hent skiftstatus igjen', exact: true }).click();
  await expect(page.getByText('Skiftstatus er ukjent / utilgjengelig', { exact: true })).toBeVisible(); await expect(page.getByRole('button', { name: 'Start skift', exact: true })).toHaveCount(0);
  await page.unroute('**:8001' + path); await page.getByRole('button', { name: 'Hent skiftstatus igjen', exact: true }).click();
  await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  expect(await (await context.request.get(API + path)).json()).toEqual(actual);
});

for (const resource of ['selection', 'start']) test(`validated ${resource} capacity rejection retains cancellable proposal`, async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/' + resource;
  const receipt = await post(context, path, { operation_id: randomUUID(), expected_revision: 0, ...(resource === 'selection' ? { activity_id: activities[1].id } : {}) });
  python(`with database() as conn:\n conn.execute('INSERT INTO workday_${resource}_operations SELECT gen_random_uuid(),owner,workday_id,payload_hash,result,expires_at FROM workday_${resource}_operations CROSS JOIN generate_series(1,1999) WHERE id=%s', (${JSON.stringify(receipt.operation_id)},))\n`);
  // UI still holds revision zero: selection needs fresh state to hit admission.
  if (resource === 'selection') await page.getByRole('button', { name: 'Kontroller plantilgang og aktivitetsvalg', exact: true }).click();
  await page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true }).click(); if (resource === 'start') await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  const status = resource === 'selection' ? page.getByRole('status', { name: 'Aktivitetsvalgstatus' }) : shiftStatus(page);
  await expect(status).toContainText('grensen på 2000'); await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(true);
  await page.getByRole('button', { name: resource === 'selection' ? 'Avbryt avvist aktivitetsvalg' : 'Avbryt avvist skiftstart', exact: true }).click();
  await expect(status).toHaveText(resource === 'selection' ? 'Avvist aktivitetsvalg er avbrutt. Lagret valg er uendret.' : 'Avvist skiftstart er avbrutt. Lagret skiftstatus er uendret.');
  await expect(status).toBeFocused();
  await expect(page.getByText(/^Lokalt forslag/)).toHaveCount(0);
  await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(false);
});

for (const resource of ['selection', 'start']) test(`${resource} late accepted reply cannot restore an expired plan`, async ({ page, context }) => {
  await page.clock.install(); const { plan } = await openedPlan(page, context, true, -604830);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await page.clock.setSystemTime(new Date(Date.parse(plan.expires_at) - 5000));
  await page.getByRole('button', { name: `Åpne plan ${plan.draft.service_date} · versjon 1`, exact: true }).click();
  await expect(page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true })).toBeEnabled();
  const path = '/workdays/' + plan.id + '/' + resource;
  let release!: () => void, entered!: () => void;
  const gate = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  await page.route('**:8001' + path, async route => {
    if (route.request().method() !== 'POST') return route.continue();
    const response = await route.fetch(); entered(); await gate; await route.fulfill({ response });
  });
  try {
    await page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true }).click(); if (resource === 'start') await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await received;
    await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(true);
    await page.clock.fastForward(6000);
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(false);
    const returned = page.waitForResponse(response => response.url().endsWith(path) && response.request().method() === 'POST');
    release(); await (await returned).finished();
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(false);
  } finally { release(); }
});

for (const resource of ['selection', 'start']) test(`${resource} deleted plan hides authority and retains unresolved original attempt`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/' + resource; let original: any;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() !== 'POST') return route.continue();
    original = route.request().postDataJSON(); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost</html>' });
  });
  await page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true }).click(); if (resource === 'start') await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  const check = page.getByRole('button', { name: resource === 'selection' ? 'Kontroller aktivitetsvalget' : 'Kontroller skiftstarten', exact: true });
  await expect(check).toBeEnabled(); await page.unroute('**:8001' + path);
  await post(context, '/workdays/' + plan.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
  let retry: any; page.on('request', req => { if (req.url().endsWith(path) && req.method() === 'POST') retry = req.postDataJSON(); });
  await page.getByRole('button', { name: resource === 'selection' ? 'Prøv samme aktivitetsvalg igjen' : 'Prøv samme skiftstart igjen', exact: true }).click();
  await expect(page.getByText('Planfakta er skjult til plantilgangen er kontrollert.', { exact: true })).toBeVisible();
  expect(retry).toBeUndefined(); expect(original.operation_id).toBeTruthy(); await expect(selected(page)).toHaveCount(0); await expect(page.getByText('Startet manuelt', { exact: true })).toHaveCount(0);
  await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(true);
});
