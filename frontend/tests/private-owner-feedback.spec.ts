import { test, expect, openedPlan, API, selected, shiftStatus, beforeUnload, setup, dayScreen, activityScreen, post, randomUUID } from './private-activity-helpers';
import { writeFileSync } from 'node:fs';
setup();
const button = (page: any, name: string) => page.getByRole('button', { name, exact: true });
const status = (page: any) => page.getByRole('status', { name: 'Aktivitetsstatus og avslutningsstatus' });
async function tabTo(page: any, target: any, direction = 'Tab') {
  await expect(target).toBeEnabled();
  for (let i = 0; i < 180; i++) { if (await target.evaluate((el: Element) => el === document.activeElement)) { await expect(target).toBeFocused(); return; } await page.keyboard.press(direction); }
  throw Error('Keyboard traversal did not reach the requested control');
}
async function keyboardActivate(page: any, target: any) { await tabTo(page, target); await page.keyboard.press('Enter'); }
async function current(context: any, id: string) { return (await context.request.get(API + '/workdays/' + id + '/recap')).json(); }
async function choose(page: any) { await button(page, 'Velg aktivitet 1').click(); await activityScreen(page); }

for (const action of ['Avslutt skift', 'Avbryt skift']) test(`activity keyboard confirmed Start cancel status save and ${action} cancel confirm`, async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context);
  const counts: Record<string, number> = { selection: 0, start: 0, outcome: 0, close: 0 };
  page.on('request', request => { if (request.method() === 'POST') for (const key of Object.keys(counts)) if (request.url() === API + '/workdays/' + plan.id + '/' + key) counts[key]++; });
  await keyboardActivate(page, button(page, 'Velg aktivitet 1')); await expect(selected(page)).toBeVisible();
  await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[0].id);
  await expect(page.locator('.private-shift-start')).toHaveCount(1);
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeHidden();
  await expect(page.getByLabel('Manuell aktivitetsstatus', { exact: true })).toHaveCount(0);
  const start = button(page, 'Start skift'); await keyboardActivate(page, start);
  await expect(page.getByRole('heading', { name: 'Start skiftet?', exact: true })).toBeFocused();
  await expect(selected(page)).toBeHidden(); expect(counts.start).toBe(0);
  await page.keyboard.press('Tab'); await expect(button(page, 'Bekreft skiftstart')).toBeFocused();
  await page.keyboard.press('Tab'); await expect(button(page, 'Tilbake uten å starte')).toBeFocused(); await page.keyboard.press('Enter');
  await expect(start).toBeFocused(); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[0].id);
  expect((await current(context, plan.id)).lifecycle.state).toBe('confirmed'); expect(counts.start).toBe(0);
  await page.keyboard.press('Enter'); await expect(page.getByRole('heading', { name: 'Start skiftet?', exact: true })).toBeFocused();
  await page.keyboard.press('Tab'); await expect(button(page, 'Bekreft skiftstart')).toBeFocused(); await page.keyboard.press('Enter');
  await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.'); await expect(selected(page)).toBeVisible();
  expect(counts).toEqual({ selection: 1, start: 1, outcome: 0, close: 0 });
  const firstStart = (await current(context, plan.id)).lifecycle.started_at;
  const choice = page.getByLabel('Manuell aktivitetsstatus', { exact: true }); await tabTo(page, choice, 'Shift+Tab');
  await page.keyboard.press('Home'); await page.keyboard.press('ArrowDown'); await expect(choice).toHaveValue('completed');
  await expect(button(page, action)).toBeDisabled();
  await page.keyboard.press('Tab'); await expect(button(page, 'Lagre aktivitetsstatus')).toBeFocused(); await page.keyboard.press('Enter');
  await expect(status(page)).toHaveText('Aktivitetsstatusen er lagret.');
  const before = await current(context, plan.id); expect(before.lifecycle.started_at).toBe(firstStart);
  const end = button(page, action); await keyboardActivate(page, end);
  await expect(page.getByRole('heading', { name: action, exact: true })).toBeFocused(); await expect(selected(page)).toBeHidden();
  const confirm = button(page, action === 'Avslutt skift' ? 'Bekreft avslutning' : 'Bekreft avbrudd'); await expect(confirm).toBeEnabled();
  await page.keyboard.press('Tab'); await expect(page.locator('[aria-label="Bekreft avslutning"] summary')).toBeFocused();
  await page.keyboard.press('Tab'); await expect(confirm).toBeFocused();
  await page.keyboard.press('Tab'); await expect(button(page, 'Tilbake uten å avslutte')).toBeFocused(); await page.keyboard.press('Enter');
  await expect(end).toBeFocused(); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[0].id);
  expect(await current(context, plan.id)).toEqual(before); expect(counts.close).toBe(0);
  await page.keyboard.press('Enter'); await expect(confirm).toBeEnabled(); await keyboardActivate(page, confirm);
  await expect(page.getByRole('heading', { name: action === 'Avslutt skift' ? 'Skift avsluttet' : 'Skift avbrutt', exact: true })).toBeFocused();
  expect(counts).toEqual({ selection: 1, start: 1, outcome: 1, close: 1 });
  const closed = await current(context, plan.id); expect(closed.lifecycle.started_at).toBe(firstStart);
  expect(closed.outcomes.outcomes.map((row: any) => row.outcome)).toEqual(['completed', 'unregistered', 'unregistered', 'unregistered', 'unregistered']);
  await keyboardActivate(page, button(page, 'Tilbake til dagen')); await keyboardActivate(page, button(page, 'Les aktivitet 2'));
  await expect(selected(page)).toContainText('Skrivebeskyttet konsultasjon');
  await expect(button(page, 'Start skift')).toHaveCount(0); await expect(button(page, 'Lagre aktivitetsstatus')).toHaveCount(0);
  expect(counts).toEqual({ selection: 1, start: 1, outcome: 1, close: 1 });
});

test('activity pending Start and failed lookup keep one original operation and reachable recovery', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await choose(page);
  const path = '/workdays/' + plan.id + '/start'; let original: any, retry: any, posts = 0;
  await page.route('**:8001' + path, async route => { original = route.request().postDataJSON(); posts++; await route.fetch(); await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost</html>' }); });
  await button(page, 'Start skift').click(); await button(page, 'Bekreft skiftstart').click();
  const check = button(page, 'Kontroller skiftstarten'); await expect(check).toBeEnabled();
  await expect(button(page, 'Avslutt skift')).toBeDisabled(); await expect(button(page, 'Lagre aktivitetsstatus')).toBeDisabled();
  await expect(button(page, 'Neste aktivitet')).toBeDisabled(); await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.route('**:8001/workday-start-operations/*', route => route.fulfill({ status: 503, json: { detail: 'Synthetic unavailable lookup' } }));
  await check.click(); await expect(check).toBeEnabled(); await expect(shiftStatus(page)).toContainText('uavklart');
  await dayScreen(page); await expect(button(page, 'Kontroller skiftstarten')).toBeEnabled(); await expect(button(page, 'Lukk planen')).toBeDisabled();
  await page.unroute('**:8001' + path); page.on('request', request => { if (request.url() === API + path && request.method() === 'POST') { retry = request.postDataJSON(); posts++; } });
  await button(page, 'Prøv samme skiftstart igjen').click(); await expect(check).toBeEnabled(); await expect(shiftStatus(page)).toContainText('uavklart');
  expect(retry).toBeUndefined(); expect(posts).toBe(1); await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.unroute('**:8001/workday-start-operations/*');
  await button(page, 'Prøv samme skiftstart igjen').click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
  expect(retry).toBeUndefined(); expect(posts).toBe(1); await expect.poll(() => beforeUnload(page)).toBe(false);
  expect((await (await context.request.get(API + '/workday-start-operations/' + original.operation_id)).json()).operation_id).toBe(original.operation_id);
  await activityScreen(page); await expect(selected(page)).toHaveAttribute('data-selected-activity-id', activities[0].id);
  const saved = await current(context, plan.id); expect(saved.outcomes.revision).toBe(0); expect(saved.lifecycle.revision).toBe(1);
});

test('day bus proposal and unavailable authority cannot be bypassed by activity shift actions', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await choose(page); await dayScreen(page);
  const input = page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true });
  await input.fill('Preserved bus proposal'); await expect(button(page, 'Start skift')).toBeDisabled();
  await expect(button(page, 'Åpne valgt aktivitet')).toBeDisabled();
  await button(page, 'Avbryt bussendring').click(); await activityScreen(page);
  await page.route('**:8001/workdays/' + plan.id + '/recap', route => route.fulfill({ status: 503, json: { detail: 'Synthetic unavailable facts' } }));
  await dayScreen(page); await button(page, 'Hent skift og aktivitetsstatus igjen').click();
  await expect(status(page)).toContainText('kan ikke bekreftes'); await expect(button(page, 'Start skift')).toHaveCount(0);
  await expect(button(page, 'Avslutt skift')).toBeDisabled();
  await page.unroute('**:8001/workdays/' + plan.id + '/recap'); await button(page, 'Hent skift og aktivitetsstatus igjen').click();
  await activityScreen(page); await expect(button(page, 'Start skift')).toBeEnabled();
  expect((await current(context, plan.id)).lifecycle.state).toBe('confirmed');
});

test('current terminal refresh during Start review opens authoritative recap without a new Start', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); await choose(page);
  let starts = 0; page.on('request', request => { if (request.method() === 'POST' && request.url() === API + '/workdays/' + plan.id + '/start') starts++; });
  await button(page, 'Start skift').click(); await expect(page.getByRole('heading', { name: 'Start skiftet?', exact: true })).toBeFocused();
  await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 });
  const terminal = await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  await page.evaluate(() => window.dispatchEvent(new Event('focus')));
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeFocused();
  await expect(button(page, 'Bekreft skiftstart')).toHaveCount(0); expect(starts).toBe(0);
  expect((await current(context, plan.id)).lifecycle).toEqual(terminal.result);
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).activity_id).toBe(activities[0].id);
});

async function measure(region: any, control: any) {
  await expect(control).toBeEnabled(); await control.focus(); await control.page().keyboard.press('Tab'); await control.page().keyboard.press('Shift+Tab'); await expect(control).toBeFocused();
  const result = await region.evaluate((root: Element) => {
    const l = (s: string) => (s.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map(c => (c /= 255) <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
    const ratio = (a: string, b: string) => (Math.max(l(a), l(b)) + .05) / (Math.min(l(a), l(b)) + .05);
    const bg = (e: Element): string => { const c = getComputedStyle(e).backgroundColor; return ['rgba(0, 0, 0, 0)', 'transparent'].includes(c) ? e.parentElement ? bg(e.parentElement) : 'rgb(255,255,255)' : c; };
    const nodes = [...root.querySelectorAll('h2,h3,p,label,button,select,strong')].filter(e => e.getBoundingClientRect().height > 0), focused = document.activeElement!, style = getComputedStyle(focused);
    return { text: Math.min(...nodes.map(e => ratio(getComputedStyle(e).color, bg(e)))), boundary: ratio(getComputedStyle(root).borderTopColor, bg(root.parentElement!)), focus: ratio(style.outlineColor, bg(focused.parentElement!)), focusWidth: parseFloat(style.outlineWidth), height: focused.getBoundingClientRect().height, controls: [...root.querySelectorAll('button,select')].filter(e => e.getBoundingClientRect().height > 0).map(e => ({ disabled: (e as HTMLButtonElement).disabled, text: ratio(getComputedStyle(e).color, bg(e)), height: e.getBoundingClientRect().height })), overflow: document.documentElement.scrollWidth > innerWidth + 1 };
  });
  expect(result.text).toBeGreaterThanOrEqual(4.5); expect(result.boundary).toBeGreaterThanOrEqual(3); expect(result.focus).toBeGreaterThanOrEqual(3); expect(result.focusWidth).toBeGreaterThanOrEqual(2); expect(result.height).toBeGreaterThanOrEqual(58); for (const control of result.controls) { expect(control.text).toBeGreaterThanOrEqual(4.5); expect(control.height).toBeGreaterThanOrEqual(58); } expect(result.overflow).toBe(false); return result;
}
for (const width of [768, 1440]) for (const night of [false, true]) test(`activity shift actions enlarged ${width} ${night ? 'night' : 'day'}`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: 900 }); await openedPlan(page, context); await choose(page);
  if (night) await button(page, 'Nattmodus').click(); await page.addStyleTag({ content: 'html { font-size: 200% !important; }' });
  const suffix = `${width}-${night ? 'night' : 'day'}`, results: any = {};
  await button(page, 'Start skift').click(); const review = page.getByRole('region', { name: 'Bekreft skiftstart', exact: true });
  results.start = await measure(review, button(page, 'Tilbake uten å starte')); await page.screenshot({ path: `../docs/evidence/11-3-feedback-start-${suffix}.png`, fullPage: true });
  await button(page, 'Tilbake uten å starte').click(); await expect(button(page, 'Start skift')).toBeFocused();
  await button(page, 'Start skift').click(); await button(page, 'Bekreft skiftstart').click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
  const choice = page.getByLabel('Manuell aktivitetsstatus', { exact: true }); await choice.selectOption('completed');
  results.activity = await measure(page.getByRole('region', { name: 'Registrert aktivitetsstatus', exact: true }), button(page, 'Lagre aktivitetsstatus'));
  await page.screenshot({ path: `../docs/evidence/11-3-feedback-activity-${suffix}.png`, fullPage: true });
  await button(page, 'Lagre aktivitetsstatus').click(); await expect(status(page)).toHaveText('Aktivitetsstatusen er lagret.');
  await button(page, 'Avslutt skift').click(); const close = page.getByRole('region', { name: 'Bekreft avslutning', exact: true });
  await expect(button(page, 'Bekreft avslutning')).toBeEnabled(); results.close = await measure(close, button(page, 'Tilbake uten å avslutte'));
  await page.screenshot({ path: `../docs/evidence/11-3-feedback-close-${suffix}.png`, fullPage: true });
  await button(page, 'Tilbake uten å avslutte').click(); await expect(button(page, 'Avslutt skift')).toBeFocused(); await expect(selected(page)).toBeVisible();
  writeFileSync(`../docs/evidence/11-3-feedback-contrast-${suffix}.json`, JSON.stringify(results, null, 2));
});
