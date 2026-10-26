import { test, expect, openedPlan, API, post, randomUUID, selected, shiftStatus, beforeUnload, python, setup, dayScreen, activityScreen, account } from './private-activity-helpers';
import { writeFileSync } from 'node:fs';
setup();
const progressStatus = (page: any) => page.getByRole('status', { name: 'Aktivitetsstatus og avslutningsstatus' });
test('active multi-member local proposals are explicit on day and independently discardable', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page); let writes = 0;
  page.on('request', request => { if (request.method() === 'POST' && request.url().endsWith('/outcome')) writes++; });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
  await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed');
  await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click();
  await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('skipped'); await dayScreen(page);
  const proposals = page.getByRole('region', { name: 'Ulagrede forslag til aktivitetsstatus', exact: true });
  await expect(proposals).toContainText('Dagsoversikten viser lagrede statuser.');
  await expect(proposals.getByText('Aktivitet 1: Fullført manuelt', { exact: true })).toBeVisible();
  await expect(proposals.getByText('Aktivitet 2: Hoppet over', { exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Avslutt skift', exact: true })).toBeDisabled(); await expect.poll(() => beforeUnload(page)).toBe(true);
  await proposals.getByRole('button', { name: 'Forkast ulagret aktivitetsstatus for aktivitet 1', exact: true }).click();
  await expect(proposals.getByText('Aktivitet 1: Fullført manuelt', { exact: true })).toHaveCount(0);
  await expect(proposals.getByText('Aktivitet 2: Hoppet over', { exact: true })).toBeVisible(); await expect.poll(() => beforeUnload(page)).toBe(true);
  await proposals.getByRole('button', { name: 'Forkast ulagret aktivitetsstatus for aktivitet 2', exact: true }).click();
  await expect(proposals).toHaveCount(0); await expect.poll(() => beforeUnload(page)).toBe(false);
  await expect(page.getByRole('button', { name: 'Avslutt skift', exact: true })).toBeEnabled();
  expect(writes).toBe(0); expect((await recap(context, plan)).outcomes.outcomes.map((row: any) => row.outcome)).toEqual(Array(5).fill('unregistered'));
});

test('pending activity status describes original member and value after navigation and retries identical command', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await start(page);
  const path = '/workdays/' + plan.id + '/outcome'; let original: any, retry: any;
  await page.route('**:8001' + path, async route => { original = route.request().postDataJSON(); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost</html>' }); });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
  await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('interrupted'); await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller aktivitetsstatusen', exact: true })).toBeEnabled();
  await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click(); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[1].id);
  await expect(page.getByText('Uavklart lagringsforsøk for aktivitet 1: Avbrutt.', { exact: false })).toBeVisible();
  await expect(page.getByRole('button', { name: /Forkast ulagret aktivitetsstatus/ })).toHaveCount(0);
  await page.unroute('**:8001' + path); page.on('request', request => { if (request.url() === API + path && request.method() === 'POST') retry = request.postDataJSON(); });
  await page.getByRole('button', { name: 'Prøv samme aktivitetsstatus igjen', exact: true }).click(); await expect(progressStatus(page)).toHaveText('Aktivitetsstatusen er lagret.');
  expect(retry).toBeUndefined(); expect(original.activity_id).toBe(activities[0].id); expect(original.outcome).toBe('interrupted');
  expect((await (await context.request.get(API + '/workday-outcome-operations/' + original.operation_id)).json()).result.outcomes[0].outcome).toBe(original.outcome);
  const saved = await recap(context, plan); expect(saved.outcomes.outcomes.map((row: any) => row.outcome)).toEqual(['interrupted', 'unregistered', 'unregistered', 'unregistered', 'unregistered']);
  await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[1].id); await expect.poll(() => beforeUnload(page)).toBe(false);
});

test('current snapshot keeps acknowledged newer bus when an otherwise valid projection regresses bus revision', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page);
  await post(context, '/workdays/' + plan.id + '/physical-bus', { operation_id: randomUUID(), expected_revision: 0, physical_bus: 'Acknowledged newer bus' });
  await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  await page.getByRole('button', { name: 'Hent skift og aktivitetsstatus igjen', exact: true }).click();
  await expect(page.getByText('Fysisk buss: Acknowledged newer bus', { exact: true })).toBeVisible();
  const authority = await recap(context, plan); expect(authority.bus.revision).toBe(1);
  await page.route('**:8001/workdays/' + plan.id + '/recap', route => route.fulfill({ status: 200, json: { ...authority, bus: { ...authority.bus, revision: 0, physical_bus: null } } }));
  await page.getByRole('button', { name: 'Hent skift og aktivitetsstatus igjen', exact: true }).click();
  await expect(progressStatus(page)).toHaveText('Lagret skift og aktivitetsstatus er hentet.');
  await expect(page.getByText('Fysisk buss: Acknowledged newer bus', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Åpne oppsummering', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Oppsummering av skift', exact: true })).toContainText('Fysisk buss: Acknowledged newer bus.');
});
for (const invalid of ['wrong-workday', 'invalid-shape']) test(`malformed lifecycle ${invalid} current reply cannot shorten deadline or discard local outcome`, async ({ page, context }) => {
  await page.clock.install();
  const { plan, activities } = await openedPlan(page, context); await start(page);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
  await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed');
  await dayScreen(page);
  const deadline = await page.getByText(/^Siste aktivitetsslutt:/).innerText();
  const path = '/workdays/' + plan.id + '/lifecycle';
  const original = await (await context.request.get(API + path)).json();
  const earlier = new Date(await page.evaluate(() => Date.now()) + 5000).toISOString();
  await page.route('**:8001' + path, route => route.fulfill({ status: 200, json: { ...original, ...(invalid === 'wrong-workday' ? { workday_id: randomUUID() } : { state: 'malformed' }), expires_at: earlier } }));
  const reload = page.getByRole('button', { name: 'Hent skiftstatus igjen', exact: true });
  await reload.click();
  await expect(shiftStatus(page)).toContainText('kan ikke bekreftes');
  await page.clock.fastForward(6000);
  await expect(page.getByText(/^Siste aktivitetsslutt:/)).toHaveText(deadline);
  await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.unroute('**:8001' + path); await reload.click();
  await expect(shiftStatus(page)).toContainText('Lagret status er hentet.');
  await activityScreen(page);
  await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[0].id);
  await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveValue('completed');
  const current = await recap(context, plan);
  expect(current.plan.expires_at).toBe(plan.expires_at); expect(current.outcomes.revision).toBe(0);
  const selection = await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json();
  expect(selection.activity_id).toBe(activities[0].id); expect(selection.revision).toBe(1);
});
test('held valid old-plan lifecycle reply cannot shorten a newly opened plan', async ({ page, context }) => {
  await page.clock.install();
  const { plan } = await openedPlan(page, context); await start(page);
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { service_date: '2031-02-02', activities: [{ id: randomUUID(), type: 'trip', start: '2031-02-02T10:00+01:00', end: '2031-02-02T11:00+01:00' }] } });
  const review = await post(context, '/workday-reviews', { draft_id: draft.id, expected_revision: 1 });
  const other = await post(context, '/drafts/' + draft.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: review.unknowns.map((item: any) => item.id), classifications: {} });
  const terminal = await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  expect(Date.parse(terminal.result.expires_at)).toBeLessThan(Date.parse(other.expires_at));
  let release!: () => void, received!: () => void;
  const held = new Promise<void>(resolve => { release = resolve; }); const ready = new Promise<void>(resolve => { received = resolve; });
  await page.route('**:8001/workdays/' + plan.id + '/lifecycle', async route => { const response = await route.fetch(); received(); await held; await route.fulfill({ response }); });
  await page.getByRole('button', { name: 'Hent skiftstatus igjen', exact: true }).click(); await ready;
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne plan 2031-02-02 · versjon 1', exact: true }).click();
  await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
  await start(page); await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
  await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('skipped'); await dayScreen(page);
  const deadline = await page.getByText(/^Siste aktivitetsslutt:/).innerText(); const before = await recap(context, other);
  // The response alone precedes workspace postvalidation. Hold that auth read,
  // then queue a lock barrier behind it so the guarded read can finish while A
  // remains live. B has finished loading before the only remaining A read runs.
  await activityScreen(page); await expect(page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true })).toBeEnabled(); await dayScreen(page);
  let releaseValidation!: () => void, validating!: () => void;
  const validationHeld = new Promise<void>(resolve => { releaseValidation = resolve; });
  const validationReady = new Promise<void>(resolve => { validating = resolve; });
  await page.route('**:8001/auth/session', async route => { const response = await route.fetch(); validating(); await validationHeld; await route.fulfill({ response }); }, { times: 1 });
  release(); await validationReady;
  const barrier = page.evaluate(() => navigator.locks.request('private-auth-mutations', () => true));
  releaseValidation(); expect(await barrier).toBe(true);
  await expect(page.getByText(/^Siste aktivitetsslutt:/)).toHaveText(deadline);
  await page.clock.fastForward(Date.parse(terminal.result.expires_at) - await page.evaluate(() => Date.now()) + 1000);
  await expect(page.getByText(/^Siste aktivitetsslutt:/)).toHaveText(deadline);
  await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  await activityScreen(page); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', other.draft.activities[0].id);
  await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveValue('skipped');
  expect(await recap(context, other)).toEqual(before);
});
test('numeric bus current expiry preserves deadline and original proposal until authorized reconciliation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  const deadline = await page.getByText(/^Siste aktivitetsslutt:/).innerText();
  const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true });
  const input = bus.getByLabel('Fysisk buss', { exact: true });
  await input.fill('Recoverable numeric expiry proposal');
  const path = '/workdays/' + plan.id + '/physical-bus'; let posts = 0;
  page.on('request', request => { if (request.url() === API + path && request.method() === 'POST') posts++; });
  await page.route('**:8001' + path, async route => {
    const response = await route.fetch();
    if (route.request().method() === 'POST') return route.fulfill({ response });
    await route.fulfill({ status: 200, json: { ...await response.json(), expires_at: 2030 } });
  });
  await bus.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click();
  await expect(bus.getByRole('button', { name: 'Kontroller busslagringen', exact: true })).toBeEnabled();
  await expect(page.getByRole('status', { name: 'Bussstatus' })).toContainText('uavklart');
  await expect(input).toHaveValue('Recoverable numeric expiry proposal');
  await expect(page.getByText(/^Siste aktivitetsslutt:/)).toHaveText(deadline);
  await expect.poll(() => beforeUnload(page)).toBe(true); expect(posts).toBe(1);
  await page.unroute('**:8001' + path);
  await bus.getByRole('button', { name: 'Kontroller busslagringen', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Bussstatus' })).toHaveText('Fysisk buss er lagret.');
  await expect(input).toHaveValue('Recoverable numeric expiry proposal');
  await expect(page.getByText(/^Siste aktivitetsslutt:/)).toHaveText(deadline);
  await expect.poll(() => beforeUnload(page)).toBe(false); expect(posts).toBe(1);
  expect((await recap(context, plan)).plan.expires_at).toBe(plan.expires_at);
});
async function start(page: any) { await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.'); }
async function save(page: any, value: string) { await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption(value); await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click(); await expect(progressStatus(page)).toHaveText('Aktivitetsstatusen er lagret.'); }
async function recap(context: any, plan: any) { const response = await context.request.get(API + '/workdays/' + plan.id + '/recap'); expect(response.status()).toBe(200); return response.json(); }
async function tabTo(page: any, target: any) {
  await expect(target).toBeEnabled();
  for (let i = 0; i < 160; i++) {
    if (await target.evaluate((el: Element) => el === document.activeElement)) { await expect(target).toBeFocused(); return; }
    await page.keyboard.press('Tab');
  }
  throw Error('Control was not reached by keyboard traversal');
}
async function measure(scope: any, control: any) {
  // Measurement-only positioning; the separate journey uses Tab throughout.
  await expect(control).toBeEnabled(); await control.focus();
  await control.page().keyboard.press('Tab'); await control.page().keyboard.press('Shift+Tab'); await expect(control).toBeFocused();
  const result = await scope.evaluate((region: Element) => {
    const light = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
    const ratio = (a: string, b: string) => (Math.max(light(a), light(b)) + .05) / (Math.min(light(a), light(b)) + .05);
    const bg = (node: Element): string => { const c = getComputedStyle(node).backgroundColor; return c === 'rgba(0, 0, 0, 0)' || c === 'transparent' ? node.parentElement ? bg(node.parentElement) : 'rgb(255,255,255)' : c; };
    const visible = [...region.querySelectorAll('h2,h3,p,dt,dd,strong,button,select,summary,li')].filter(node => node.getBoundingClientRect().height > 0);
    const focused = document.activeElement!, style = getComputedStyle(focused);
    return { text: Math.min(...visible.map(node => ratio(getComputedStyle(node).color, bg(node)))), boundary: ratio(getComputedStyle(region).borderTopColor, bg(region.parentElement!)), focus: ratio(style.outlineColor, bg(focused.parentElement!)), focusWidth: parseFloat(style.outlineWidth), height: focused.getBoundingClientRect().height, controls: [...region.querySelectorAll('button,select,summary')].filter(node => node.getBoundingClientRect().height > 0).map(node => ({ disabled: (node as HTMLButtonElement).disabled, text: ratio(getComputedStyle(node).color, bg(node)), height: node.getBoundingClientRect().height })) };
  });
  expect(result.text).toBeGreaterThanOrEqual(4.5); expect(result.boundary).toBeGreaterThanOrEqual(3); expect(result.focus).toBeGreaterThanOrEqual(3); expect(result.focusWidth).toBeGreaterThanOrEqual(2); expect(result.height).toBeGreaterThanOrEqual(58);
  for (const c of result.controls) { expect(c.text).toBeGreaterThanOrEqual(4.5); expect(c.height).toBeGreaterThanOrEqual(58); }
  return result;
}

test('prestart consultation explicit outcomes correction cancel end retained read-only recap', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context);
  await expect(page.getByRole('button', { name: 'Avslutt skift', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: 'Velg aktivitet 2', exact: true }).click(); await activityScreen(page);
  await expect(page.getByText('Start skiftet før du registrerer aktivitetsstatus.', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveCount(0);
  expect((await recap(context, plan)).outcomes.outcomes.map((item: any) => item.outcome)).toEqual(Array(5).fill('unregistered'));
  await dayScreen(page); await start(page); await activityScreen(page);
  await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed');
  expect((await recap(context, plan)).outcomes.revision).toBe(0);
  await dayScreen(page); await expect(page.getByRole('button', { name: 'Avslutt skift', exact: true })).toBeDisabled();
  await activityScreen(page); await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveValue('completed');
  await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click(); await expect(progressStatus(page)).toHaveText('Aktivitetsstatusen er lagret.');
  await save(page, 'skipped'); await save(page, 'unregistered'); await save(page, 'interrupted');
  await dayScreen(page);
  const before = await recap(context, plan);
  await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  const confirmation = page.getByRole('region', { name: 'Bekreft avslutning', exact: true });
  await expect(confirmation).toContainText('Ikke registrerte aktiviteter forblir ikke registrert.');
  await confirmation.getByText('Ikke registrerte aktiviteter (4)', { exact: true }).click();
  expect(await confirmation.locator('[data-unregistered-id]').evaluateAll(nodes => nodes.map(node => node.getAttribute('data-unregistered-id')))).toEqual(activities.filter((_: any, index: number) => index !== 1).map((a: any) => a.id));
  await expect(page.getByRole('region', { name: 'Dagsoversikt' })).toBeHidden();
  await page.getByRole('button', { name: 'Tilbake uten å avslutte', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Avslutt skift', exact: true })).toBeFocused();
  expect(await recap(context, plan)).toEqual(before);
  await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible();
  const saved = await recap(context, plan);
  expect(saved.outcomes.outcomes).toEqual(activities.map((a: any, index: number) => ({ activity_id: a.id, outcome: index === 1 ? 'interrupted' : 'unregistered' })));
  expect(Date.parse(saved.plan.expires_at)).toBe(Date.parse(saved.lifecycle.ended_at) + 7 * 86400000);
  expect(saved.lifecycle.started_at).toBe(before.lifecycle.started_at);
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Start skift', exact: true })).toBeHidden();
  await page.getByRole('button', { name: 'Les aktivitet 5', exact: true }).click();
  await expect(selected(page)).toContainText('Tomkjøring');
  await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toBeHidden();
  await expect(page.getByText('Skiftet er avsluttet. Aktivitetsstatusen er skrivebeskyttet.')).toBeVisible();
  expect((await context.request.get(API + '/workdays/' + plan.id + '/selection')).ok()).toBeTruthy();
  await page.reload();
  await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible();
  expect(await recap(context, plan)).toEqual(saved);
});

test('every real pause and nonpassenger member can receive an exact saved outcome', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await start(page);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
  const values = ['completed', 'skipped', 'interrupted', 'completed', 'skipped'];
  for (let i = 0; i < values.length; i++) { await save(page, values[i]); if (i < values.length - 1) { await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click(); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[i + 1].id); } }
  expect((await recap(context, plan)).outcomes.outcomes).toEqual(activities.map((a: any, i: number) => ({ activity_id: a.id, outcome: values[i] })));
  await dayScreen(page);
  await expect(page.getByText(/Registrerte aktivitetsstatuser i pausegruppen:/)).toContainText('aktivitet 3: Avbrutt · aktivitet 4: Fullført manuelt');
  await page.getByRole('button', { name: 'Avbryt skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft avbrudd', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Skift avbrutt', exact: true })).toBeVisible();
  expect((await recap(context, plan)).outcomes.outcomes.map((item: any) => item.outcome)).toEqual(values);
});

for (const resource of ['outcome', 'close']) for (const failure of ['lost', 'html', 'malformed']) test(`${resource} ${failure} reply preserves identity and authorized recovery`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page);
  if (resource === 'outcome') { await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed'); }
  else await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  const path = '/workdays/' + plan.id + '/' + resource; let original: any;
  await page.route('**:8001' + path, async route => { original = route.request().postDataJSON(); await route.fetch(); if (failure === 'lost') return route.abort(); await route.fulfill(failure === 'html' ? { status: 200, contentType: 'text/html', body: '<html>synthetic proxy</html>' } : { status: 200, json: { operation_id: original.operation_id, result: {} } }); });
  await page.getByRole('button', { name: resource === 'outcome' ? 'Lagre aktivitetsstatus' : 'Bekreft avslutning', exact: true }).click();
  await expect(progressStatus(page)).toContainText('uavklart');
  await expect.poll(() => beforeUnload(page)).toBe(true);
  await expect(page.getByRole('button', { name: resource === 'outcome' ? 'Kontroller aktivitetsstatusen' : 'Kontroller avslutningen', exact: true })).toBeEnabled();
  await page.unroute('**:8001' + path);
  let retry: any; page.on('request', request => { if (request.url().endsWith(path) && request.method() === 'POST') retry = request.postDataJSON(); });
  await page.getByRole('button', { name: resource === 'outcome' ? 'Prøv samme aktivitetsstatus igjen' : 'Prøv samme avslutning igjen', exact: true }).click();
  await expect(progressStatus(page)).toHaveText(resource === 'outcome' ? 'Aktivitetsstatusen er lagret.' : 'Skiftet er avsluttet og skrivebeskyttet.');
  expect(retry).toBeUndefined(); expect((await (await context.request.get(API + '/workday-' + resource + '-operations/' + original.operation_id)).json()).operation_id).toBe(original.operation_id); await expect.poll(() => beforeUnload(page)).toBe(false);
});

test('changed counts reject stale confirmation and require another explicit review', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await start(page);
  await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeEnabled();
  await post(context, '/workdays/' + plan.id + '/outcome', { operation_id: randomUUID(), expected_revision: 0, expected_lifecycle_revision: 1, activity_id: activities[3].id, outcome: 'skipped' });
  await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click();
  await expect(progressStatus(page)).toContainText('ble avvist');
  await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toHaveCount(0);
  expect((await recap(context, plan)).lifecycle.state).toBe('active');
  await page.getByRole('button', { name: 'Tilbake uten å avslutte', exact: true }).click();
  await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible();
});

test('terminal state from another window blocks new writes and permits read-only consultation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page);
  const terminal = await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'aborted' });
  await page.getByRole('button', { name: 'Hent skift og aktivitetsstatus igjen', exact: true }).click();
  await expect(page.getByText('Skiftet er avbrutt. Dagen er skrivebeskyttet.')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Start skift', exact: true })).toBeHidden();
  await expect(page.getByRole('button', { name: 'Lagre fysisk buss', exact: true })).toBeHidden();
  await page.getByRole('button', { name: 'Les aktivitet 1', exact: true }).click();
  await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click();
  await expect(selected(page)).toContainText('Linje: 24');
  expect((await recap(context, plan)).lifecycle).toEqual(terminal.result);
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).revision).toBe(0);
});

test('terminal refresh keeps a known unsaved bus proposal discardable without editing or saving', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page);
  const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true });
  await bus.getByLabel('Fysisk buss', { exact: true }).fill('Known unsaved terminal proposal');
  await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  await page.getByRole('button', { name: 'Hent skift og aktivitetsstatus igjen', exact: true }).click();
  await expect(bus.getByLabel('Fysisk buss', { exact: true })).toBeDisabled();
  await expect(bus.getByRole('button', { name: 'Lagre fysisk buss', exact: true })).toHaveCount(0);
  await bus.getByRole('button', { name: 'Forkast ulagret bussendring', exact: true }).click();
  await expect(bus).toBeHidden();
  await expect.poll(() => beforeUnload(page)).toBe(false);
  expect((await recap(context, plan)).bus.physical_bus).toBeNull();
});

for (const resource of ['start', 'selection', 'physical-bus']) test(`fresh stale ${resource} rejection resolves against current terminal authority`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 });
  if (resource === 'physical-bus') await page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true }).fill('Unaccepted stale bus');
  const terminal = await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  await page.getByRole('button', { name: resource === 'start' ? 'Start skift' : resource === 'selection' ? 'Velg aktivitet 1' : 'Lagre fysisk buss', exact: true }).click(); if (resource === 'start') await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  if (resource !== 'start') {
    const status = page.getByRole('status', { name: resource === 'selection' ? 'Aktivitetsvalgstatus' : 'Bussstatus' });
    await expect(status).toContainText('ble ikke lagret');
    await page.getByRole('button', { name: resource === 'selection' ? 'Last inn lagret aktivitetsvalg' : 'Last inn lagret buss', exact: true }).click();
  }
  await expect.poll(() => beforeUnload(page)).toBe(false);
  await expect(page.getByText('Skiftet er avsluttet. Dagen er skrivebeskyttet.')).toBeVisible();
  expect((await recap(context, plan)).lifecycle).toEqual(terminal.result);
});

test('terminal pause consultation labels transient member without writing saved selection', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await start(page);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await dayScreen(page);
  await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click();
  await page.getByRole('heading', { name: 'Skift avsluttet', exact: true }).waitFor();
  let selectionWrites = 0; page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith('/selection')) selectionWrites++; });
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByText('Vis 2 pauserader', { exact: true }).click();
  await page.getByRole('button', { name: 'Les aktivitet 3', exact: true }).click();
  await expect(selected(page)).toContainText('Skrivebeskyttet konsultasjon · Aktivitet 3'); await dayScreen(page);
  await expect(page.getByText('Aktivitet i lesevisning i denne pausegruppen: aktivitet 3.', { exact: true })).toBeVisible();
  await expect(page.getByText(/Manuelt valgt aktivitet i denne pausegruppen/)).toHaveCount(0);
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).activity_id).toBe(activities[0].id);
  expect(selectionWrites).toBe(0);
});

for (const mode of ['outcome-dirty', 'outcome-pending', 'bus-pending']) test(`recap preparation navigation cannot strand ${mode} state`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page);
  const resource = mode === 'bus-pending' ? 'physical-bus' : 'outcome', path = '/workdays/' + plan.id + '/' + resource;
  let original: any;
  if (mode !== 'outcome-dirty') await page.route('**:8001' + path, async route => { original = route.request().postDataJSON(); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>synthetic lost response</html>' }); });
  if (resource === 'outcome') {
    await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
    await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('skipped');
    if (mode === 'outcome-pending') { await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click(); await expect(progressStatus(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Kontroller aktivitetsstatusen', exact: true })).toBeEnabled(); }
    await dayScreen(page);
  } else {
    await page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true }).fill('Uncertain recap bus');
    await page.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click(); await expect(page.getByRole('status', { name: 'Bussstatus' })).toContainText('uavklart'); await expect(page.getByRole('button', { name: 'Kontroller busslagringen', exact: true })).toBeEnabled();
  }
  const current = await recap(context, plan);
  await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: current.outcomes.revision, action: 'ended' });
  await page.getByRole('button', { name: 'Hent skift og aktivitetsstatus igjen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne oppsummering', exact: true }).click();
  const preparation = page.getByRole('button', { name: 'Til forberedelse og planlisten', exact: true });
  await expect(preparation).toBeDisabled(); await expect.poll(() => beforeUnload(page)).toBe(true);
  if (mode === 'outcome-dirty') {
    expect((await recap(context, plan)).outcomes.revision).toBe(0);
    await expect(page.getByText('Aktivitet 1: Hoppet over', { exact: true })).toBeVisible();
    await page.getByRole('button', { name: 'Forkast ulagret aktivitetsstatus for aktivitet 1', exact: true }).click();
  } else if (mode === 'outcome-pending') {
    await page.unroute('**:8001' + path); await page.getByRole('button', { name: 'Kontroller aktivitetsstatusen', exact: true }).click();
    await expect(progressStatus(page)).toHaveText('Aktivitetsstatusen er lagret.');
    expect((await (await context.request.get(API + '/workday-outcome-operations/' + original.operation_id)).json()).result.outcomes[0].outcome).toBe('skipped');
  } else {
    await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await page.unroute('**:8001' + path);
    await page.getByRole('button', { name: 'Kontroller busslagringen', exact: true }).click(); await expect.poll(() => beforeUnload(page)).toBe(false);
    await page.getByRole('button', { name: 'Åpne oppsummering', exact: true }).click();
    expect((await recap(context, plan)).bus.physical_bus).toBe('Uncertain recap bus');
  }
  await expect.poll(() => beforeUnload(page)).toBe(false); await expect(preparation).toBeEnabled(); await preparation.click();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
});

test('held initial current authority gates fresh bus writes without disabling later denied-save recovery', async ({ page, context }) => {
  let release!: () => void, entered!: () => void, writes = 0, operation: any;
  const held = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  await page.route('**:8001/workdays/*/recap', async route => { const response = await route.fetch(); entered(); await held; await route.fulfill({ response }); });
  page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith('/physical-bus')) writes++; });
  const opening = openedPlan(page, context);
  try {
    await received;
    const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true });
    await expect(bus.getByLabel('Fysisk buss', { exact: true })).toBeDisabled();
    await expect(bus.getByRole('button', { name: 'Lagre fysisk buss', exact: true })).toBeDisabled();
    expect(writes).toBe(0); release();
    const { plan } = await opening; await page.unroute('**:8001/workdays/*/recap');
    await expect(bus.getByLabel('Fysisk buss', { exact: true })).toBeEnabled();
    let denied = true;
    const path = '/workdays/' + plan.id + '/physical-bus';
    await page.route('**:8001' + path, async route => {
      if (route.request().method() === 'GET' && denied) return route.fulfill({ status: 404, json: { detail: 'synthetic denied current bus' } });
      if (route.request().method() === 'POST') operation = route.request().postDataJSON();
      await route.continue();
    });
    await bus.getByLabel('Fysisk buss', { exact: true }).fill('Held authority recovery bus'); await bus.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click();
    await expect(bus.getByRole('button', { name: 'Kontroller plantilgangen', exact: true })).toBeEnabled();
    await expect(bus.getByRole('button', { name: 'Prøv samme busslagring igjen', exact: true })).toBeEnabled();
    await expect(bus.getByLabel('Fysisk buss', { exact: true })).toHaveValue('Held authority recovery bus');
    denied = false; await bus.getByRole('button', { name: 'Kontroller plantilgangen', exact: true }).click();
    await expect(page.getByRole('status', { name: 'Bussstatus' })).toContainText('fortsatt uavklart');
    await bus.getByRole('button', { name: 'Kontroller busslagringen', exact: true }).click();
    await expect(page.getByRole('status', { name: 'Bussstatus' })).toHaveText('Fysisk buss er lagret.');
    expect(writes).toBe(1); expect((await (await context.request.get(API + '/workday-bus-operations/' + operation.operation_id)).json()).result.physical_bus).toBe('Held authority recovery bus');
  } finally { release(); await opening; }
});

for (const width of [768, 1024, 1440]) for (const theme of ['Dag', 'Natt']) test(`outcome closure recap ${width} ${theme} enlarged keyboard and rendered evidence`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: width === 768 ? 1024 : 768 });
  const { plan } = await openedPlan(page, context); await start(page);
  if (theme === 'Natt') await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.evaluate(() => document.documentElement.style.fontSize = '200%');
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await save(page, 'completed');
  const measures = [await measure(page.getByRole('region', { name: 'Registrert aktivitetsstatus', exact: true }), page.getByLabel('Manuell aktivitetsstatus', { exact: true }))];
  await page.screenshot({ path: `../docs/evidence/11-3-outcome-${width}-${theme === 'Dag' ? 'day' : 'night'}.png`, fullPage: true });
  await dayScreen(page); await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeEnabled();
  measures.push(await measure(page.getByRole('region', { name: 'Bekreft avslutning', exact: true }), page.getByRole('button', { name: 'Tilbake uten å avslutte', exact: true })));
  const unregistered = page.getByRole('region', { name: 'Bekreft avslutning', exact: true }).locator('summary');
  measures.push(await measure(page.getByRole('region', { name: 'Bekreft avslutning', exact: true }), unregistered));
  await page.keyboard.press('Enter');
  const remaining = page.locator('[data-unregistered-id]'); await expect(remaining).toHaveCount(4);
  for (const member of await remaining.all()) { await member.scrollIntoViewIfNeeded(); await expect(member).toBeInViewport(); expect(await member.evaluate(el => el.scrollWidth <= el.clientWidth + 1)).toBe(true); }
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  measures.push(await measure(page.getByRole('region', { name: 'Bekreft avslutning', exact: true }), unregistered));
  await page.screenshot({ path: `../docs/evidence/11-3-closure-${width}-${theme === 'Dag' ? 'day' : 'night'}.png`, fullPage: true });
  await page.getByRole('button', { name: 'Tilbake uten å avslutte', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Avslutt skift', exact: true })).toBeFocused();
  await page.keyboard.press('Enter'); await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeFocused();
  const summary = page.getByRole('region', { name: 'Oppsummering av skift', exact: true });
  await expect(summary).toContainText('Planlagt start: 02.01.2031, 23:00. Planlagt siste slutt: 03.01.2031, 00:10.');
  for (const [label, count] of [['Ikke registrert', '4'], ['Fullført manuelt', '1'], ['Hoppet over', '0'], ['Avbrutt', '0']]) await expect(summary.locator('dl > div').filter({ has: page.getByText(label, { exact: true }) }).locator('dd')).toHaveText(count);
  measures.push(await measure(summary, page.getByRole('button', { name: 'Tilbake til dagen', exact: true })));
  await page.screenshot({ path: `../docs/evidence/11-3-recap-${width}-${theme === 'Dag' ? 'day' : 'night'}.png`, fullPage: true });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBeTruthy();
  expect((await recap(context, plan)).outcomes.outcomes.filter((item: any) => item.outcome === 'unregistered')).toHaveLength(4);
  writeFileSync(`../docs/evidence/11-3-contrast-${width}-${theme === 'Dag' ? 'day' : 'night'}.json`, JSON.stringify(measures, null, 2) + '\n');
});

test('actual synthetic upload edit confirm start outcome close recap journey', async ({ page, context }) => {
  const pdf = Buffer.from(python('import sys, base64\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nprint(base64.b64encode(synthetic_text_pdf()).decode())\n').trim(), 'base64');
  await page.goto('/private'); await page.getByLabel('Brukernavn', { exact: true }).fill(account.username); await page.getByLabel('Passord', { exact: true }).fill(account.password); await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic-11-3.pdf', mimeType: 'application/pdf', buffer: pdf });
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast', exact: true }).click();
  await page.getByLabel('Fra sted', { exact: true }).first().fill('Rettet syntetisk oppmøtested 11.3');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click();
  for (const select of await page.getByRole('region', { name: 'Gjennomgått versjon', exact: true }).locator('select').all()) await select.selectOption('manual');
  for (const checkbox of await page.getByRole('checkbox').all()) await checkbox.check();
  await page.getByRole('button', { name: 'Bekreft gjennomgått plan', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible(); await start(page);
  const plans = await (await context.request.get(API + '/workdays')).json(); const plan = await (await context.request.get(API + '/workdays/' + plans.workdays[0].id)).json();
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
  await expect(selected(page)).toContainText('Rettet syntetisk oppmøtested 11.3'); await save(page, 'skipped');
  await dayScreen(page); await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible();
  const result = await recap(context, plan);
  expect(result.outcomes.outcomes).toEqual(plan.draft.activities.map((a: any, i: number) => ({ activity_id: a.id, outcome: i === 0 ? 'skipped' : 'unregistered' })));
  expect(result.plan.draft).toEqual(plan.draft);
});

test('all unknown recap preserves literal Oslo offset transition dates and exact count', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context, true, undefined, undefined, false, content => { content.service_date = '2026-10-25'; Object.assign(content.activities[0], { start: '2026-10-25T02:55+02:00', end: '2026-10-25T02:05+01:00' }); });
  await start(page); await page.getByRole('button', { name: 'Avbryt skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft avbrudd', exact: true }).click();
  const summary = page.getByRole('region', { name: 'Oppsummering av skift', exact: true });
  await expect(summary).toContainText('Planlagt start: 25.10.2026, 02:55. Planlagt siste slutt: 25.10.2026, 02:05.');
  await expect(summary.locator('dl > div').filter({ has: page.getByText('Ikke registrert', { exact: true }) }).locator('dd')).toHaveText('1');
  expect((await recap(context, plan)).outcomes.outcomes[0].outcome).toBe('unregistered');
});

test('keyboard-only outcome save closure cancel confirm and recap navigation traverses real controls', async ({ page, context }) => {
  await openedPlan(page, context);
  await tabTo(page, page.getByRole('button', { name: 'Start skift', exact: true })); await page.keyboard.press('Enter'); await expect(page.getByRole('heading', { name: 'Start skiftet?', exact: true })).toBeFocused();
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Bekreft skiftstart', exact: true })).toBeFocused(); await page.keyboard.press('Enter'); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
  await tabTo(page, page.getByRole('button', { name: 'Velg aktivitet 1', exact: true })); await page.keyboard.press('Enter'); await expect(selected(page)).toBeVisible();
  const choice = page.getByLabel('Manuell aktivitetsstatus', { exact: true }); await tabTo(page, choice);
  await page.keyboard.press('Home'); await page.keyboard.press('ArrowDown'); await expect(choice).toHaveValue('completed');
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true })).toBeFocused(); await page.keyboard.press('Enter'); await expect(progressStatus(page)).toHaveText('Aktivitetsstatusen er lagret.');
  await tabTo(page, page.getByRole('button', { name: 'Tilbake til dagen', exact: true })); await page.keyboard.press('Enter');
  const end = page.getByRole('button', { name: 'Avslutt skift', exact: true }); await tabTo(page, end); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Avslutt skift', exact: true })).toBeFocused(); await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeEnabled();
  await page.keyboard.press('Tab'); await expect(page.locator('[aria-label="Bekreft avslutning"] summary')).toBeFocused();
  await page.keyboard.press('Enter'); await expect(page.locator('[data-unregistered-id]')).toHaveCount(4);
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeFocused();
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Tilbake uten å avslutte', exact: true })).toBeFocused(); await page.keyboard.press('Enter');
  await expect(end).toBeFocused(); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Avslutt skift', exact: true })).toBeFocused(); await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeEnabled();
  await page.keyboard.press('Tab'); await expect(page.locator('[aria-label="Bekreft avslutning"] summary')).toBeFocused();
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeFocused(); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeFocused();
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Tilbake til dagen', exact: true })).toBeFocused(); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Dagen din', exact: true })).toBeFocused();
  await tabTo(page, page.getByRole('button', { name: 'Åpne oppsummering', exact: true })); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeFocused();
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Tilbake til dagen', exact: true })).toBeFocused();
  await page.keyboard.press('Tab'); await expect(page.getByRole('button', { name: 'Til forberedelse og planlisten', exact: true })).toBeFocused(); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
});

for (const resource of ['outcome', 'close']) for (const currentFacts of ['available', 'unavailable']) test(`validated ${resource} capacity rejection with ${currentFacts} facts explains wait and permits cancellation without automatic writes`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page); let posts = 0;
  await page.route('**:8001/workdays/' + plan.id + '/' + resource, route => { posts++; return route.fulfill({ status: 429, json: { detail: { code: resource + '_receipt_capacity', message: 'For mange lagringsforsøk. Vent til tidligere planer utløper.' } } }); });
  if (resource === 'outcome') { await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed'); }
  else await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  if (resource === 'close') await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeEnabled();
  if (currentFacts === 'unavailable') await page.route('**:8001/workdays/' + plan.id + '/recap', route => route.fulfill({ status: 503, json: { detail: 'synthetic unavailable after known rejection' } }));
  await page.getByRole('button', { name: resource === 'outcome' ? 'Lagre aktivitetsstatus' : 'Bekreft avslutning', exact: true }).click();
  await expect(progressStatus(page)).toContainText('Vent til tidligere planer utløper før du prøver igjen.');
  await expect(page.getByRole('button', { name: resource === 'outcome' ? 'Kontroller aktivitetsstatusen' : 'Kontroller avslutningen', exact: true })).toHaveCount(0);
  expect((await recap(context, plan)).outcomes.revision).toBe(0); expect((await recap(context, plan)).lifecycle.state).toBe('active'); expect(posts).toBe(1);
  if (resource === 'outcome') {
    await expect.poll(() => beforeUnload(page)).toBe(true);
    if (currentFacts === 'available') { await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveValue('completed'); await page.getByRole('button', { name: 'Avbryt ulagret aktivitetsstatus', exact: true }).click(); }
    else { await expect(page.getByRole('region', { name: 'Ulagrede forslag til aktivitetsstatus', exact: true })).toContainText('Fullført manuelt'); await page.getByRole('button', { name: 'Forkast ulagret aktivitetsstatus for aktivitet 1', exact: true }).click(); }
  }
  else { await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toHaveCount(0); await page.getByRole('button', { name: 'Tilbake uten å avslutte', exact: true }).click(); }
  await expect.poll(() => beforeUnload(page)).toBe(false); expect(posts).toBe(1);
});

test('lost abort response resolves exclusively through authorized close lookup with no extra POST', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page); let operation: any, posts = 0, lookups = 0;
  await page.route('**:8001/workdays/' + plan.id + '/close', async route => { operation = route.request().postDataJSON(); posts++; await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost terminal receipt</html>' }); });
  await page.getByRole('button', { name: 'Avbryt skift', exact: true }).click(); await page.getByRole('button', { name: 'Bekreft avbrudd', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller avslutningen', exact: true })).toBeEnabled();
  const terminal = (await recap(context, plan)).lifecycle;
  page.on('request', request => { if (request.url().endsWith('/workday-close-operations/' + operation.operation_id)) lookups++; });
  await page.getByRole('button', { name: 'Kontroller avslutningen', exact: true }).click(); await expect(page.getByRole('heading', { name: 'Skift avbrutt', exact: true })).toBeVisible();
  expect(posts).toBe(1); expect(lookups).toBe(1); expect((await recap(context, plan)).lifecycle).toEqual(terminal); expect(terminal.state).toBe('aborted'); await expect.poll(() => beforeUnload(page)).toBe(false);
});

test('stale outcome rejection distinguishes newer saved value and retained proposal until explicit save', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await start(page); const attempts: any[] = [];
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed');
  await post(context, '/workdays/' + plan.id + '/outcome', { operation_id: randomUUID(), expected_revision: 0, expected_lifecycle_revision: 1, activity_id: activities[0].id, outcome: 'skipped' });
  page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith('/workdays/' + plan.id + '/outcome')) attempts.push(req.postDataJSON()); });
  await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click(); await expect(progressStatus(page)).toContainText('Forsøket ble avvist.');
  await expect(page.getByRole('region', { name: 'Registrert aktivitetsstatus', exact: true })).toContainText('Lagret: Hoppet over'); await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveValue('completed');
  expect((await recap(context, plan)).outcomes.revision).toBe(1); expect(attempts).toHaveLength(1); await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click(); await expect(progressStatus(page)).toHaveText('Aktivitetsstatusen er lagret.');
  expect(attempts).toHaveLength(2); expect(attempts[1].expected_revision).toBe(1); expect(attempts[1].operation_id).not.toBe(attempts[0].operation_id); expect((await recap(context, plan)).outcomes.outcomes[0].outcome).toBe('completed');
});

for (const recovery of ['lookup', 'retry']) test(`lost accepted outcome ${recovery} preserves the proposal for comparison with a newer correction`, async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await start(page); let original: any; const writes: any[] = [];
  const path = '/workdays/' + plan.id + '/outcome';
  await page.route('**:8001' + path, async route => { original = route.request().postDataJSON(); await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost</html>' }); });
  page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith(path)) writes.push(req.postDataJSON()); });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed'); await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller aktivitetsstatusen', exact: true })).toBeEnabled(); await page.unroute('**:8001' + path);
  await post(context, path, { operation_id: randomUUID(), expected_revision: 1, expected_lifecycle_revision: 1, activity_id: activities[0].id, outcome: 'interrupted' });
  await page.getByRole('button', { name: recovery === 'lookup' ? 'Kontroller aktivitetsstatusen' : 'Prøv samme aktivitetsstatus igjen', exact: true }).click();
  await expect(progressStatus(page)).toHaveText('Aktivitetsstatusen ble lagret. En nyere lagret versjon vises; ditt forslag er beholdt hvis statusen er endret. Sammenlign før et nytt forsøk.');
  await expect(page.getByRole('region', { name: 'Registrert aktivitetsstatus', exact: true })).toContainText('Lagret: Avbrutt'); await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveValue('completed');
  expect(writes).toHaveLength(1);
  await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.getByRole('button', { name: 'Avbryt ulagret aktivitetsstatus', exact: true }).click();
  await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveValue('interrupted');
  await expect.poll(() => beforeUnload(page)).toBe(false); await dayScreen(page); await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeEnabled();
  expect((await recap(context, plan)).outcomes.revision).toBe(2);
});

for (const denial of ['unavailable', 'deleted']) test(`known unsent outcome remains locally discardable after ${denial} current facts`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page); let writes = 0;
  page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith('/outcome')) writes++; });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('skipped'); await dayScreen(page);
  if (denial === 'deleted') await post(context, '/workdays/' + plan.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
  else await page.route('**:8001/workdays/' + plan.id + '/recap', route => route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } }));
  await page.getByRole('button', { name: 'Hent skift og aktivitetsstatus igjen', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Ulagrede forslag til aktivitetsstatus', exact: true })).toContainText('lokale forslagene til aktivitetsstatus er ikke lagret');
  await expect(page.getByRole('region', { name: 'Ulagrede forslag til aktivitetsstatus', exact: true })).not.toContainText('Planlagt start:');
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0); await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.getByRole('button', { name: 'Forkast ulagret aktivitetsstatus for aktivitet 1', exact: true }).click(); await expect.poll(() => beforeUnload(page)).toBe(false); expect(writes).toBe(0);
  await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeEnabled();
});

for (const resource of ['outcome', 'close']) for (const invalidation of ['account', 'session-expired']) test(`held ${resource} receipt cannot enter ${invalidation} workspace`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await start(page);
  if (resource === 'outcome') { await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed'); }
  else await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  let release!: () => void, entered!: () => void, operation: any;
  const gate = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  const path = '/workdays/' + plan.id + '/' + resource;
  await page.route('**:8001' + path, async route => { operation = route.request().postDataJSON(); const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  const next = { username: 'synthetic-held-outcome-' + randomUUID(), password: randomUUID() };
  try {
    await page.getByRole('button', { name: resource === 'outcome' ? 'Lagre aktivitetsstatus' : 'Bekreft avslutning', exact: true }).click(); await received;
    if (invalidation === 'account') {
      python(`from app.auth import provision\nprovision(${JSON.stringify(next.username)},${JSON.stringify(next.password)})\n`);
      await post(context, '/auth/login', next);
    } else python(`with database() as conn:\n conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=(SELECT id FROM accounts WHERE username=%s)", (${JSON.stringify(account.username)},))\n`);
    const returned = page.waitForResponse(response => response.url().endsWith(path) && response.request().method() === 'POST'); release(); await (await returned).finished();
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0); await expect(selected(page)).toHaveCount(0);
    await expect(page.getByRole('region', { name: 'Oppsummering av skift', exact: true })).toHaveCount(0); await expect.poll(() => beforeUnload(page)).toBe(false);
    expect((await context.request.get(API + '/workday-' + resource + '-operations/' + operation.operation_id)).status()).toBe(invalidation === 'account' ? 404 : 401);
    if (invalidation === 'account') { await page.reload(); await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible(); await expect(page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true })).toHaveCount(0); }
    else await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  } finally {
    release();
    if (invalidation === 'account') python(`with database() as conn:\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(next.username)},))\n conn.execute('DELETE FROM accounts WHERE username=%s', (${JSON.stringify(next.username)},))\n`);
  }
});

for (const resource of ['outcome', 'close']) for (const boundary of ['deletion', 'expiry']) test(`pending held ${resource} cannot resurrect private data after ${boundary}`, async ({ page, context }) => {
  if (boundary === 'expiry') await page.clock.install();
  const { plan } = await openedPlan(page, context, boundary === 'expiry', boundary === 'expiry' ? -604830 : undefined);
  if (boundary === 'expiry') {
    // Reopen after moving wall-clock time so the plan's timeout is installed
    // against the same five-second deadline that the assertion advances.
    await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
    await page.clock.setSystemTime(new Date(Date.parse(plan.expires_at) - 5000));
    await page.getByRole('button', { name: `Åpne plan ${plan.draft.service_date} · versjon 1`, exact: true }).click();
  }
  await start(page);
  if (resource === 'outcome') { await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page); await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('completed'); }
  else await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click();
  let release!: () => void, entered!: () => void, operation: any;
  const gate = new Promise<void>(resolve => release = resolve), received = new Promise<void>(resolve => entered = resolve);
  const path = '/workdays/' + plan.id + '/' + resource;
  await page.route('**:8001' + path, async route => { operation = route.request().postDataJSON(); const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try {
    await page.getByRole('button', { name: resource === 'outcome' ? 'Lagre aktivitetsstatus' : 'Bekreft avslutning', exact: true }).click(); await received;
    if (boundary === 'deletion') await post(context, '/workdays/' + plan.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
    else {
      await page.clock.fastForward(6000); await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0); await expect.poll(() => beforeUnload(page)).toBe(false);
    }
    const returned = page.waitForResponse(response => response.url().endsWith(path) && response.request().method() === 'POST'); release(); await (await returned).finished();
    await expect(selected(page)).toHaveCount(0); await expect(page.getByRole('region', { name: 'Oppsummering av skift', exact: true })).toHaveCount(0); await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
    if (boundary === 'deletion') {
      const check = page.getByRole('button', { name: resource === 'outcome' ? 'Kontroller aktivitetsstatusen' : 'Kontroller avslutningen', exact: true }); await expect(check).toBeEnabled(); await check.click(); await expect(check).toBeEnabled();
      await expect(progressStatus(page)).toContainText('uavklart'); await expect(page.getByRole('button', { name: /Forkast ulagret aktivitetsstatus/ })).toHaveCount(0); await expect.poll(() => beforeUnload(page)).toBe(true);
      expect((await context.request.get(API + '/workday-' + resource + '-operations/' + operation.operation_id)).status()).toBe(404);
    } else { await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0); await expect.poll(() => beforeUnload(page)).toBe(false); }
  } finally { release(); }
});
