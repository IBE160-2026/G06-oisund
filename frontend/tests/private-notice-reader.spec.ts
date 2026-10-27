import { test, expect, openedPlan, API, post, randomUUID, setup, beforeUnload, python, account } from './private-activity-helpers';
import { writeFileSync } from 'node:fs';
setup();
async function measure(page: any) {
  const scope = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
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
  const reachable = scope.locator('button:not(:disabled),select:not(:disabled),summary,a[href]');
  const focusTargets = [];
  for (let index = 0; index < await reachable.count(); index++) {
    if (index > 0) await page.keyboard.press('Tab');
    const target = reachable.nth(index); await expect(target).toBeFocused(); await target.scrollIntoViewIfNeeded();
    const focus = await target.evaluate((node: Element) => {
      const light = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
      const bg = (element: Element): string => { const value = getComputedStyle(element).backgroundColor; return value === 'rgba(0, 0, 0, 0)' || value === 'transparent' ? element.parentElement ? bg(element.parentElement) : 'rgb(255,255,255)' : value; };
      const s = getComputedStyle(node), rect = node.getBoundingClientRect(), a = light(s.outlineColor), b = light(bg(node.parentElement!));
      // Inline source links have separate painted fragments; the union box can
      // have its center in the unpainted line-height gap. Hit-test every visible
      // fragment instead of mistaking that gap for an obscuring element.
      const fragments = [...node.getClientRects()].filter(r => r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth).map(r => {
        const x = (Math.max(0, r.left) + Math.min(innerWidth, r.right)) / 2, y = (Math.max(0, r.top) + Math.min(innerHeight, r.bottom)) / 2;
        const hit = document.elementFromPoint(x, y);
        return { rect: r.toJSON(), hit: hit?.tagName, unobscured: !!hit && node.contains(hit) };
      });
      return { tag: node.tagName, name: node.getAttribute('aria-label') || node.textContent?.slice(0, 80), contrast: (Math.max(a, b) + .05) / (Math.min(a, b) + .05), width: parseFloat(s.outlineWidth), visible: node.matches(':focus-visible'), unobscured: fragments.length > 0 && fragments.every(f => f.unobscured), rect: rect.toJSON(), fragments };
    });
    expect(focus.contrast).toBeGreaterThanOrEqual(3); expect(focus.width).toBeGreaterThanOrEqual(2); expect(focus.visible).toBe(true); expect(focus.unobscured, JSON.stringify(focus)).toBe(true); focusTargets.push(focus);
  }
  return { ...metrics, focusTargets };
}


const region = (page: any) => page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
async function open(page: any) { await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click(); await expect(region(page).getByRole('status')).toHaveText('Lagrede avvik er hentet.'); }
async function seed(context: any, plan: any, title: string, extra = {}) { return (await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0, content: { title, line_tags: ['20', '24'], source_url: null, source_updated_at: null, valid_from: null, valid_until: '2031-01-04T23:59:59+01:00', ...extra } })).result; }
async function snapshot(context: any, plan: any) { return Promise.all(['', '/notices', '/selection', '/lifecycle', '/recap'].map(async suffix => (await context.request.get(API + '/workdays/' + plan.id + suffix)).json())); }

test('shared and independent candidates filter exact lines and calendar gaps without changing saved state', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  await seed(context, plan, 'Shared'); await seed(context, plan, 'Separate 20', { line_tags: ['20'] });
  await seed(context, plan, 'Midnight 24', { line_tags: ['24'], valid_from: '2031-01-03T00:00+01:00', valid_until: '2031-01-03T00:00+01:00' });
  await seed(context, plan, 'Gap', { valid_from: '2031-01-02T23:40+01:00', valid_until: '2031-01-02T23:50+01:00' });
  await seed(context, plan, 'Heading', { line_tags: ['20 heading'] });
  await seed(context, plan, 'Partial', { valid_from: null });
  await seed(context, plan, 'Mixed', { line_tags: ['20', 'Copied heading'] });
  const before = await snapshot(context, plan); await open(page); const r = region(page);
  await expect(r.locator('summary')).toHaveCount(5); await r.getByText('Shared · Registrert', { exact: true }).click();
  await expect(r.locator('details[open]').getByText('Samsvarende bekreftede linjer: 20, 24', { exact: true })).toBeVisible();
  await expect(r).toContainText('uten eksakt samsvar: 2');
  // A mixed source tag list remains one candidate with a specific warning.
  await r.getByText('Mixed · Registrert', { exact: true }).click();
  const mixed = r.locator('details').filter({ hasText: 'Mixed · Registrert' });
  await expect(mixed.getByText('Samsvarende bekreftede linjer: 20', { exact: true })).toBeVisible();
  await expect(mixed).toContainText('uten eksakt samsvar: Copied heading');
  const mixedApi = await (await context.request.get(API + '/workdays/' + plan.id + '/notice-reader')).json();
  expect(mixedApi.candidates.find((c: any) => c.notice.title === 'Mixed')).toMatchObject({ matching_lines: ['20'], unmatched_tags: ['Copied heading'], line_uncertain: true });
  await r.getByLabel('Bekreftet linje', { exact: true }).selectOption('24'); await expect(r.locator('summary')).toHaveCount(3);
  await r.getByLabel('Planlagt kalenderdato (Oslo)', { exact: true }).selectOption('2031-01-02'); await expect(r.locator('summary')).toHaveCount(2);
  await r.getByText('Partial · Registrert', { exact: true }).click(); await expect(r).toContainText('tidsmessig samsvar er ikke bekreftet');
  await r.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await expect(page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true })).toBeFocused();
  await open(page); await expect(r.getByLabel('Bekreftet linje', { exact: true })).toHaveValue('24');
  expect(await snapshot(context, plan)).toEqual(before);
});

test('saved all-lines notice remains visible with no known plan lines', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context, false, undefined, undefined, false, content => { for (const a of content.activities) a.line = null; });
  await seed(context, plan, 'All lines without known lines', { line_scope: 'all', line_tags: [] });
  const before = await snapshot(context, plan); await open(page); const r = region(page);
  await expect(r).toContainText('Aktiviteter uten oppgitt linje: 5');
  await expect(r).toContainText('Ingen linje utledes'); await expect(r.locator('summary')).toHaveCount(1);
  await expect(r.locator('summary')).toContainText('Alle linjer; ingen kjente i planen');
  await r.locator('summary').click(); await expect(r).toContainText('Samsvarende bekreftede linjer: Ingen kjente');
  await expect(r).toContainText('Linjer fra kilden: Alle linjer'); await expect(r).toContainText('tidsmessig samsvar er ikke bekreftet');
  const reply = await (await context.request.get(API + '/workdays/' + plan.id + '/notice-reader')).json();
  expect(reply.available_lines).toEqual([]); expect(reply.candidates[0].matching_lines).toEqual([]); expect(await snapshot(context, plan)).toEqual(before);
});

for (const contradiction of ['empty-selected', 'requested-line-absent', 'extra-match', 'missing-unmatched', 'false-uncertainty', 'all-scope-unmatched']) test(`complete contradictory ${contradiction} payload hides prior reader results`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await seed(context, plan, 'Prior valid', { line_tags: ['20', 'Copied heading'] }); await open(page);
  await region(page).getByLabel('Bekreftet linje', { exact: true }).selectOption('20'); await expect(region(page).locator('summary')).toHaveCount(1);
  await page.route('**/notice-reader*', async route => {
    const response = await route.fetch(), value = await response.json(), c = value.candidates[0];
    if (contradiction === 'empty-selected') c.matching_lines = [];
    if (contradiction === 'requested-line-absent') { c.notice.line_tags = ['24', 'Copied heading']; c.matching_lines = ['24']; }
    if (contradiction === 'extra-match') c.matching_lines = ['20', '24'];
    if (contradiction === 'missing-unmatched') c.unmatched_tags = [];
    if (contradiction === 'false-uncertainty') c.line_uncertain = false;
    if (contradiction === 'all-scope-unmatched') { c.notice.line_scope = 'all'; c.notice.line_tags = []; c.matching_lines = ['20', '24']; }
    await route.fulfill({ json: value });
  });
  await region(page).getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click();
  await expect(region(page).getByRole('status')).toContainText('utilgjengelig'); await expect(region(page).locator('summary')).toHaveCount(0);
  await expect(region(page)).not.toContainText('Ingen lagrede avvik samsvarer');
});

test('dirty editor and chosen activity survive reader navigation', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click(); await page.getByLabel('Tittel', { exact: true }).fill('Unchanged proposal');
  await open(page); await region(page).getByRole('button', { name: 'Til avviksvedlikehold', exact: true }).click();
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Unchanged proposal'); expect(await beforeUnload(page)).toBe(true);
  const chosen = await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json(); expect(chosen.activity_id).toBe(plan.draft.activities[0].id);
});

test('zero matching differs from zero stored and terminal reader remains read only', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await seed(context, plan, 'Other line', { line_tags: ['99'] }); await open(page);
  await expect(region(page)).toContainText('Ingen lagrede avvik samsvarer med valget.');
  await region(page).getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await seed(context, plan, 'All lines', { line_scope: 'all', line_tags: [] });
  await post(context, '/workdays/' + plan.id + '/start', { operation_id: randomUUID(), expected_revision: 0 });
  await post(context, '/workdays/' + plan.id + '/close', { operation_id: randomUUID(), expected_revision: 1, expected_outcome_revision: 0, action: 'ended' });
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Skift avsluttet', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await open(page);
  await expect(region(page).locator('summary')).toHaveCount(1); await expect(region(page).getByRole('button', { name: /Lagre|Kontrollerte|Avslutt avvik/ })).toHaveCount(0);
});

test('pending maintenance command survives consulting and original recovery remains reachable', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click(); await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04'); await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig'); await page.getByLabel('Tittel', { exact: true }).fill('Pending'); await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('20');
  await page.route('**:8001/notices', async route => { if (route.request().method() !== 'POST') return route.continue(); await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await expect(page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true })).toBeEnabled();
  await open(page); await expect(region(page).locator('summary')).toHaveCount(1); await region(page).getByRole('button', { name: 'Til avviksvedlikehold', exact: true }).click();
  await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Pending'); await page.getByRole('button', { name: 'Kontroller avvikslagringen', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toHaveText('Avviket er lagret.');
});

for (const invalidation of ['account', 'session', 'plan']) test(`held reader success cannot restore ${invalidation} private facts`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await seed(context, plan, 'Private saved');
  let release!: () => void, entered!: () => void; const gate = new Promise<void>(r => release = r), started = new Promise<void>(r => entered = r);
  let first = true;
  await page.route('**/notice-reader*', async route => { if (!first) return route.continue(); first = false; const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  const next = { username: 'synthetic-reader-' + randomUUID(), password: randomUUID() };
  try {
    await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click(); await started;
    if (invalidation === 'account') { python(`from app.auth import provision\nprovision(${JSON.stringify(next.username)},${JSON.stringify(next.password)})\n`); await post(context, '/auth/login', next); }
    else if (invalidation === 'session') python(`with database() as conn:\n conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=(SELECT id FROM accounts WHERE username=%s)", (${JSON.stringify(account.username)},))\n`);
    else {
      await region(page).getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
      python(`with database() as conn:\n conn.execute('UPDATE workdays SET expires_at=clock_timestamp() WHERE id=%s', (${JSON.stringify(plan.id)},))\n`);
      await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
      await expect(region(page).getByRole('status')).toContainText('utilgjengelig');
    }
    release();
    if (invalidation !== 'plan') await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect(region(page).locator('summary')).toHaveCount(0);
  } finally { release(); if (invalidation === 'account') python(`with database() as conn:\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(next.username)},))\n conn.execute('DELETE FROM accounts WHERE username=%s', (${JSON.stringify(next.username)},))\n`); }
});

test('bounded late read becomes unavailable and cannot publish its late success', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await seed(context, plan, 'Late saved');
  let release!: () => void, entered!: () => void; const gate = new Promise<void>(r => release = r), started = new Promise<void>(r => entered = r);
  await page.route('**/notice-reader*', async route => { const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try { await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click(); await started; await expect(region(page).getByRole('status')).toContainText('utilgjengelig', { timeout: 18000 }); release(); await expect(region(page).locator('summary')).toHaveCount(0); }
  finally { release(); }
});

for (const failure of ['503', 'malformed']) test(failure + ' hides successful results, distinguishes empty and recovers', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await open(page); await expect(region(page)).toContainText('Ingen avvik er lagret i registeret.');
  await seed(context, plan, 'Saved'); await region(page).getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click(); await expect(region(page).locator('summary')).toHaveCount(1);
  await page.route('**/notice-reader*', route => route.fulfill({ status: failure === '503' ? 503 : 200, json: failure === '503' ? { detail: 'Synthetic unavailable' } : { candidates: [] } }));
  await region(page).getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click(); await expect(region(page).getByRole('status')).toContainText('utilgjengelig'); await expect(region(page).locator('summary')).toHaveCount(0);
  await expect(region(page)).not.toContainText('Ingen avvik er lagret'); await page.unroute('**/notice-reader*'); await region(page).getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click(); await expect(region(page).locator('summary')).toHaveCount(1);
});

test('superseded filter replies cannot replace current results', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); await seed(context, plan, 'Only 20', { line_tags: ['20'] }); await seed(context, plan, 'Only 24', { line_tags: ['24'] }); await open(page);
  let release!: () => void, entered!: () => void; const gate = new Promise<void>(r => release = r), started = new Promise<void>(r => entered = r);
  await page.route('**/notice-reader?line=20', async route => { const response = await route.fetch(); entered(); await gate; await route.fulfill({ response }); });
  try {
    await region(page).getByLabel('Bekreftet linje', { exact: true }).selectOption('20', { noWaitAfter: true }); await started;
    await expect(region(page).locator('summary')).toHaveCount(0); await region(page).getByLabel('Bekreftet linje', { exact: true }).selectOption('24');
    await expect(region(page).getByText('Only 24 · Registrert', { exact: true })).toBeVisible(); release(); await expect(region(page).getByText('Only 20 · Registrert', { exact: true })).toHaveCount(0);
  } finally { release(); }
});

for (const theme of ['Day', 'Night']) for (const width of [390, 768, 1024, 1440]) test(`${theme} ${width} enlarged reader keyboard and complete facts`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: 840 }); const { plan } = await openedPlan(page, context);
  const n = await seed(context, plan, 'Langt norsk stedsnavn og trafikkmelding '.repeat(5), { summary: 'Oppsummering', description: 'Mandag 06–08\nTirsdag 16–18\n' + 'Lang instruksjon '.repeat(35), source_note: 'SMS fra trafikkleder', source_url: 'https://example.org/' + 'lang-kilde-'.repeat(15) });
  await post(context, '/notices/' + n.id + '/check', { operation_id: randomUUID(), expected_revision: 1 });
  if (theme === 'Night') await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.evaluate(() => document.documentElement.style.fontSize = '200%'); const before = await snapshot(context, plan); await open(page);
  await expect(region(page).getByRole('heading')).toBeFocused(); await page.keyboard.press('Tab'); await expect(region(page).getByRole('button', { name: 'Tilbake til dagen', exact: true })).toBeFocused();
  await region(page).locator('summary').focus(); await page.keyboard.press('Enter'); await expect(region(page)).toContainText('Sist kontrollert:'); await expect(region(page)).toContainText('Registrert'); await expect(region(page)).toContainText('SMS fra trafikkleder');
  const metrics = await measure(page);
  await page.screenshot({ path: `../docs/evidence/11-5-crossday-reader-${theme.toLowerCase()}-${width}.png`, fullPage: true }); writeFileSync(`../docs/evidence/11-5-crossday-reader-${theme.toLowerCase()}-${width}.json`, JSON.stringify(metrics, null, 2));
  expect(await snapshot(context, plan)).toEqual(before);
  await page.route('**/notice-reader*', route => route.fulfill({ status: 404, json: { detail: 'Synthetic unavailable plan' } }));
  await region(page).getByRole('button', { name: 'Hent avvik på nytt', exact: true }).click();
  await expect(region(page).getByRole('status')).toContainText('utilgjengelig');
  await expect(region(page).getByLabel('Bekreftet linje', { exact: true })).toBeDisabled();
  const unavailable = await measure(page);
  await page.screenshot({ path: `../docs/evidence/11-5-crossday-reader-unavailable-${theme.toLowerCase()}-${width}.png`, fullPage: true });
  writeFileSync(`../docs/evidence/11-5-crossday-reader-unavailable-${theme.toLowerCase()}-${width}.json`, JSON.stringify(unavailable, null, 2));
});
