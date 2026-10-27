import { test, expect, type Page } from '@playwright/test';
const button = (p: Page, name: string) => p.getByRole('button', { name, exact: true });
async function edit(p: Page) { await button(p, 'Åpne delvis tekst-PDF-eksempel').click(); }
async function fault(p: Page, value: string) { if (!await p.getByLabel('Utfall', { exact: true }).isVisible()) await p.getByText('Simuler feil ved neste lagring', { exact: true }).click(); await p.getByLabel('Utfall', { exact: true }).selectOption(value); }
async function start(p: Page) { await button(p, 'Lagre forslag i simuleringen').click(); await button(p, 'Se lagret dag før start').click(); await button(p, 'Bekreft plan').click(); await button(p, 'Start arbeidsdagen').click(); await button(p, 'Bekreft Start').click(); }
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('story122-sentinel', 'keep'); sessionStorage.setItem('story122-sentinel', 'keep');
    document.cookie = 'story122-sentinel=keep;path=/';
    const counts = { fetch: 0, xhr: 0, gps: 0 }; (window as any).__demoCounts = counts; const forbidden = (key: keyof typeof counts) => { counts[key]++; throw new Error('Demo attempted forbidden browser capability'); };
    window.fetch = (() => forbidden('fetch')) as typeof fetch; window.XMLHttpRequest = class { constructor() { forbidden('xhr'); } } as typeof XMLHttpRequest;
    navigator.geolocation.getCurrentPosition = () => forbidden('gps'); navigator.geolocation.watchPosition = () => forbidden('gps');
  });
  const attempted: string[] = [], errors: string[] = [];
  (page as any).__attempted = attempted; (page as any).__errors = errors;
  page.on('pageerror', e => errors.push(e.message));
  await page.route('**/*', route => {
    const url = new URL(route.request().url());
    const expected = url.origin === 'http://127.0.0.1:15222' && !url.search && (['/demo', '/demo.html'].includes(url.pathname) || /^\/assets\/(demo|FictionalAssessment|theme)-[\w-]+\.(js|css)$/.test(url.pathname));
    if (expected) return route.continue();
    attempted.push(url.href); return route.abort();
  });
  await page.goto('/demo');
  await expect(page.locator('script[type=module]')).toHaveAttribute('src', /assets\/demo-/);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
});
test.afterEach(async ({ page }) => { expect(await page.evaluate(() => (window as any).__demoCounts)).toEqual({ fetch: 0, xhr: 0, gps: 0 }); expect((page as any).__attempted).toEqual([]); expect((page as any).__errors).toEqual([]); });
test('repeat normal journey, selection, cancellation, terminal unknowns and isolation', async ({ page }) => {
  for (let repeat = 0; repeat < 2; repeat++) {
    await edit(page); await page.getByLabel('Fysisk buss').fill('Fiktiv 42'); await start(page);
    await button(page, 'Velg Linje 100 · Tur A').click(); await expect(page.getByText(/Utfall: Ikke registrert/)).toBeVisible();
    await page.getByLabel('Foreslått utfall').selectOption('Fullført manuelt'); await button(page, 'Lagre utfall').click(); await button(page, 'Til dagsoversikten').click();
    await expect(page.locator('li').filter({ has: page.getByRole('heading', { name: 'Linje 100 · Tur A', exact: true }) })).toContainText('Utfall: Fullført manuelt'); await button(page, 'Avslutt arbeidsdagen').click(); await expect(page.getByText(/Lagrede kjente utfall: 1 av 3/)).toBeVisible(); await button(page, 'Avbryt bekreftelse').click();
    await button(page, 'Avslutt arbeidsdagen').click(); await button(page, 'Bekreft avsluttet').click();
    await expect(page.getByRole('heading', { name: /skrivebeskyttet/ })).toBeVisible();
    await expect(page.getByText('Pause: Ikke registrert / ukjent', { exact: true })).toBeVisible(); await expect(page.getByText('Linje 100 · Tur A: Fullført manuelt', { exact: true })).toBeVisible();
    await expect(button(page, 'Start arbeidsdagen')).toHaveCount(0);
    await button(page, 'Nullstill simuleringen').click(); await button(page, 'Behold simuleringen').click();
    await expect(page.getByRole('heading', { name: /skrivebeskyttet/ })).toBeVisible();
    await button(page, 'Nullstill simuleringen').click(); await button(page, 'Bekreft nullstilling').click();
  }
  expect(await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage }, cookie: document.cookie }))).toEqual({ local: { 'story122-sentinel': 'keep' }, session: { 'story122-sentinel': 'keep' }, cookie: 'story122-sentinel=keep' });
});
test('unavailable, immutable reopen, conflict and unresolved receipt lookup', async ({ page }) => {
  await edit(page); await button(page, 'Lagre forslag i simuleringen').click();
  await page.getByLabel('Vognløp').fill('Forslag'); await fault(page, 'unavailable'); await button(page, 'Lagre forslag i simuleringen').click();
  await expect(page.getByRole('status')).toContainText('ikke lagret'); await expect(page.getByLabel('Vognløp')).toHaveValue('Forslag');
  await button(page, 'Åpne lagret øyeblikksbilde').click(); await button(page, 'Forkast forslag og fortsett').click(); await expect(page.getByLabel('Vognløp')).toHaveValue('F-42');
  await page.getByLabel('Vognløp').fill('Mitt forslag'); await fault(page, 'conflict'); await button(page, 'Lagre forslag i simuleringen').click();
  await expect(page.getByRole('region', { name: 'Konflikt' })).toContainText('Mitt forslag'); await expect(page.getByRole('region', { name: 'Konflikt' })).toContainText('F-99');
  await button(page, 'Avbryt konflikt').click(); await expect(page.getByLabel('Vognløp')).toHaveValue('Mitt forslag');
  await fault(page, 'normal'); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Ta i bruk gjeldende').click();
  await fault(page, 'lost'); await button(page, 'Lagre forslag i simuleringen').click();
  await expect(button(page, 'Lagre forslag i simuleringen')).toBeDisabled(); await page.getByLabel('La oppslag feile').check(); await button(page, 'Slå opp original kvittering').click();
  await expect(page.getByRole('status')).toContainText('fortsatt uavklart'); await page.getByLabel('La oppslag feile').uncheck(); await button(page, 'Slå opp original kvittering').click();
  await expect(page.getByRole('status')).toContainText('SIM-3'); await expect(page.getByRole('status')).toContainText('revisjon 3');
});
test('unsupported/manual preserves saved work; reload is volatile; abort preserves unknowns', async ({ page }) => {
  await edit(page); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Import').click();
  await button(page, 'Prøv format som ikke støttes').click(); await expect(page.getByRole('status')).toContainText('Lagret arbeid er beholdt');
  await button(page, 'Registrer manuelt').click(); await expect(page.getByLabel('Vognløp')).toHaveValue(''); await button(page, 'Åpne lagret øyeblikksbilde').click(); await button(page, 'Forkast forslag og fortsett').click(); await expect(page.getByLabel('Vognløp')).toHaveValue('F-42');
  await button(page, 'Se lagret dag før start').click(); await button(page, 'Bekreft plan').click(); await button(page, 'Start arbeidsdagen').click(); await button(page, 'Bekreft Start').click(); await button(page, 'Avbryt arbeidsdagen').click(); await button(page, 'Bekreft avbrutt').click();
  await expect(page.getByText('Linje 100 · Tur A: Ikke registrert / ukjent', { exact: true })).toBeVisible();
  await page.reload(); await expect(button(page, 'Arbeidsdag')).toBeDisabled();
});
test('notices missing source/start, required ending, scope, lost response and independent lifetime', async ({ page }) => {
  await button(page, 'Kontomeldinger').click(); await expect(page.getByText('Start: Ukjent · Kilde oppdatert: Ukjent · Kildelenke: Ukjent', { exact: true })).toBeVisible();
  await expect(page.getByRole('article')).toHaveCount(1); await button(page, 'Vedlikehold meldinger').click();
  await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('sluttid etter simulert nåtid');
  await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await page.getByLabel('Kildelenke').fill('https://example.invalid/shared');
  await fault(page, 'lost'); await button(page, 'Lagre melding i simuleringen').click(); await button(page, 'Slå opp original kvittering').click();
  await button(page, 'Les kontomeldinger').click(); await expect(page.getByRole('article')).toHaveCount(2); await page.getByLabel('Vis linje').selectOption('300'); await expect(page.getByRole('article')).toHaveCount(1);
  await page.getByLabel('Vis linje').selectOption('200'); await expect(page.getByRole('article')).toHaveCount(2);
  await button(page, 'Import').click(); await edit(page); await fault(page, 'normal'); await start(page); await button(page, 'Avslutt arbeidsdagen').click(); await button(page, 'Bekreft avsluttet').click(); await expect(page.getByText(/Lagrede kontomeldinger: 1 simulert/)).toBeVisible();
});
test('keyboard and narrow layout plus fresh evidence', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 800 });
  await expect(page.getByRole('heading', { name: '1. Velg import' })).toBeFocused(); await page.keyboard.press('Tab'); await expect(button(page, 'Åpne delvis tekst-PDF-eksempel')).toBeFocused();
  await edit(page); await page.getByLabel('Vognløp').focus(); await page.keyboard.type('X');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: `../docs/evidence/12-2-demo-narrow-editor-${Date.now()}.png`, fullPage: true });
  await start(page); await page.screenshot({ path: `../docs/evidence/12-2-demo-narrow-day-${Date.now()}.png`, fullPage: true });
});
test('confirmed plan stays fixed, pre-Start selection and Start cancellation return to selected activity', async ({ page }) => {
  await edit(page); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Se lagret dag før start').click(); await button(page, 'Bekreft plan').click();
  await button(page, 'Velg Linje 100 · Tur A').click(); await expect(button(page, 'Lagre utfall')).toBeDisabled(); await expect(button(page, 'Forrige aktivitet')).toBeDisabled();
  await button(page, 'Start arbeidsdagen').click(); await button(page, 'Avbryt Start').click(); await expect(button(page, 'Start arbeidsdagen')).toBeFocused();
  await button(page, 'Start arbeidsdagen').click(); await button(page, 'Bekreft Start').click();
  await page.getByLabel('Foreslått utfall').selectOption('Fullført manuelt'); await button(page, 'Avbryt utfallsforslag').click(); await expect(page.getByLabel('Foreslått utfall')).toHaveValue('Ikke registrert');
  await button(page, 'Neste aktivitet').click(); await button(page, 'Neste aktivitet').click(); await expect(button(page, 'Neste aktivitet')).toBeDisabled();
  await button(page, 'Utkast').click(); await page.getByLabel('Vognløp').fill('Ny plan'); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Se lagret dag før start').click();
  await expect(page.getByText(/Bekreftet vognløp: F-42/)).toBeVisible();
  await button(page, 'Velg Linje 200 · Tur B').click(); await button(page, 'Avbryt arbeidsdagen').click(); await button(page, 'Avbryt bekreftelse').click(); await expect(button(page, 'Avbryt arbeidsdagen')).toBeFocused();
  await button(page, 'Avbryt arbeidsdagen').click(); await button(page, 'Bekreft avbrutt').click(); await button(page, 'Kontomeldinger').click(); await expect(page.getByRole('article')).toHaveCount(1); await button(page, 'Vedlikehold meldinger').click(); await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('Bekreftet simulert lagring'); await button(page, 'Til oppsummeringen').click(); await expect(page.getByRole('heading', { name: /Avbrutt · skrivebeskyttet/ })).toBeVisible();
});
test('notice invalid ending/source, unavailable and conflict preserve proposals', async ({ page }) => {
  await button(page, 'Kontomeldinger').click(); await button(page, 'Vedlikehold meldinger').click();
  await page.getByLabel('Slutt (påkrevd)').fill('2026-10-25T02:00'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('sluttid etter simulert nåtid');
  await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await page.getByLabel('Kildelenke').fill('javascript:alert(1)'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('HTTP(S)'); await page.getByLabel('Kildelenke').fill('https://#'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('HTTP(S)'); await page.getByLabel('Kildelenke').fill('');
  await fault(page, 'unavailable'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('ikke lagret');
  await fault(page, 'conflict'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('region', { name: 'Konflikt' })).toContainText('Nyere simulert melding'); await button(page, 'Ta i bruk gjeldende').click(); await expect(page.getByLabel('Melding', { exact: true })).toHaveValue('Nyere simulert melding fra en annen økt');
});
test('night view and modal reset cancellation preserve state; confirmed reset clears unresolved state', async ({ page }) => {
  await button(page, 'Bytt til nattvisning').click(); await expect(page.locator('main')).toHaveClass(/demo-night/); await edit(page); await fault(page, 'lost'); await button(page, 'Lagre forslag i simuleringen').click();
  await button(page, 'Nullstill simuleringen').click(); await expect(page.getByRole('heading', { name: 'Nullstille bare denne simuleringen?' })).toBeFocused(); await page.keyboard.press('Escape'); await expect(button(page, 'Nullstill simuleringen')).toBeFocused(); await expect(button(page, 'Lagre forslag i simuleringen')).toBeDisabled();
  await button(page, 'Nullstill simuleringen').click(); await button(page, 'Bekreft nullstilling').click(); await expect(page.locator('main')).toHaveClass(/demo-night/); await edit(page); await button(page, 'Lagre forslag i simuleringen').click(); await expect(page.getByRole('status')).toContainText('SIM-1');
});
test('rendered foreground and keyboard focus contrast in both themes', async ({ page }) => {
  for (const night of [false, true]) {
    if (night) await button(page, 'Bytt til nattvisning').click();
    await page.getByRole('heading', { name: '1. Velg import' }).focus();
    await page.keyboard.press('Tab');
    const ratios = await page.evaluate(() => {
      const element = document.activeElement!;
      const css = getComputedStyle(element);
      const numbers = (s: string) => s.match(/[\d.]+/g)!.slice(0, 3).map(Number);
      const lum = (c: number[]) => c.map(n => { n /= 255; return n <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4; }).reduce((s, n, i) => s + n * [.2126, .7152, .0722][i], 0);
      let parent: Element | null = element.parentElement, background = 'rgb(255,255,255)';
      while (parent) { const c = getComputedStyle(parent).backgroundColor; if (c !== 'rgba(0, 0, 0, 0)') { background = c; break; } parent = parent.parentElement; }
      const ratio = (a: string) => { const values = [lum(numbers(a)), lum(numbers(background))].sort((a, b) => a-b); return (values[1] + .05) / (values[0] + .05); };
      const foreground = lum(numbers(css.color)), buttonBackground = lum(numbers(css.backgroundColor));
      return { text: (Math.max(foreground, buttonBackground) + .05) / (Math.min(foreground, buttonBackground) + .05), focus: ratio(css.outlineColor), visible: element.matches(':focus-visible') && css.outlineStyle !== 'none' && parseFloat(css.outlineWidth) >= 3 };
    });
    expect(ratios.text).toBeGreaterThanOrEqual(4.5); expect(ratios.focus).toBeGreaterThanOrEqual(3);
    expect(ratios.visible).toBe(true);
    await page.screenshot({ path: `../docs/evidence/12-2-demo-${night ? 'night' : 'day'}-focus-${Date.now()}.png`, fullPage: true });
  }
});

test('discard confirmation preserves draft on cancellation and outcome proposals survive navigation', async ({ page }) => {
  await edit(page); await page.getByLabel('Vognløp').fill('Mitt ulagrede forslag'); await button(page, 'Import').click(); await button(page, 'Registrer manuelt').click(); await button(page, 'Behold ulagret forslag').click(); await button(page, 'Utkast').click(); await expect(page.getByLabel('Vognløp')).toHaveValue('Mitt ulagrede forslag');
  await button(page, 'Lagre forslag i simuleringen').click(); await page.getByLabel('Vognløp').fill('Endret'); await button(page, 'Åpne lagret øyeblikksbilde').click(); await page.keyboard.press('Escape'); await expect(page.getByLabel('Vognløp')).toHaveValue('Endret'); await button(page, 'Åpne lagret øyeblikksbilde').click(); await button(page, 'Forkast forslag og fortsett').click();
  await button(page, 'Se lagret dag før start').click(); await button(page, 'Bekreft plan').click(); await button(page, 'Start arbeidsdagen').click(); await button(page, 'Bekreft Start').click(); await button(page, 'Velg Linje 100 · Tur A').click(); await page.getByLabel('Foreslått utfall').selectOption('Hoppet over'); await button(page, 'Neste aktivitet').click(); await button(page, 'Forrige aktivitet').click(); await expect(page.getByLabel('Foreslått utfall')).toHaveValue('Hoppet over'); await button(page, 'Til dagsoversikten').click(); await button(page, 'Velg Linje 100 · Tur A').click(); await expect(page.getByLabel('Foreslått utfall')).toHaveValue('Hoppet over');
  await button(page, 'Avslutt arbeidsdagen').click(); await expect(page.getByText(/Lagrede kjente utfall: 0 av 3/)).toBeVisible(); await expect(page.getByText(/Ikke registrert: Linje 100/)).toBeVisible(); await button(page, 'Bekreft avsluttet').click(); await expect(page.getByText(/Bekreftet plan: tjenestedato/)).toContainText('Mitt ulagrede forslag');
});

test('all lifecycle cancellations restore invoking day or selected-activity controls', async ({ page }) => {
  await edit(page); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Se lagret dag før start').click(); await button(page, 'Bekreft plan').click();
  await button(page, 'Start arbeidsdagen').click(); await button(page, 'Avbryt Start').click(); await expect(button(page, 'Start arbeidsdagen')).toBeFocused();
  await button(page, 'Velg Linje 100 · Tur A').click(); await expect(page.getByText(/Første aktivitet.*Neste: Pause/)).toBeVisible(); await expect(button(page, 'Forrige aktivitet')).toBeDisabled();
  await button(page, 'Start arbeidsdagen').click(); await button(page, 'Avbryt Start').click(); await expect(button(page, 'Start arbeidsdagen')).toBeFocused(); await button(page, 'Start arbeidsdagen').click(); await button(page, 'Bekreft Start').click();
  for (const screen of ['activity', 'day']) {
    if (screen === 'day') await button(page, 'Til dagsoversikten').click();
    for (const name of ['Avslutt arbeidsdagen', 'Avbryt arbeidsdagen']) { await button(page, name).click(); await button(page, 'Avbryt bekreftelse').click(); await expect(button(page, name)).toBeFocused(); }
  }
  await button(page, 'Velg Linje 200 · Tur B').click(); await expect(page.getByText(/Forrige: Pause.*Siste aktivitet/)).toBeVisible(); await expect(button(page, 'Neste aktivitet')).toBeDisabled();
});
test('reader states and known-start future exact and past boundaries', async ({ page }) => {
  await button(page, 'Kontomeldinger').click();
  for (const [state, text] of [['empty', 'Ingen meldinger er lagret'], ['filtered', 'Ingen lagrede meldinger gjelder'], ['unavailable', 'Innholdet er ukjent']]) { await page.getByLabel('Simulert lesertilstand').selectOption(state); await expect(page.getByText(new RegExp(text))).toBeVisible(); await expect(page.getByRole('article')).toHaveCount(0); }
  await page.getByLabel('Simulert lesertilstand').selectOption('normal');
  for (const [time, visible] of [['2026-10-26T23:01', false], ['2026-10-26T23:00', true], ['2026-10-26T22:59', true]] as const) {
    await button(page, 'Vedlikehold meldinger').click(); await page.getByLabel('Start (valgfri)').fill(time); await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await button(page, 'Lagre melding i simuleringen').click(); await button(page, 'Les kontomeldinger').click(); await expect(page.getByRole('heading', { name: 'Simulert lagret melding', exact: true })).toHaveCount(visible ? 1 : 0);
  }
});
test('faults are consumed by valid saves and remain available after closure', async ({ page }) => {
  await edit(page); await fault(page, 'unavailable'); await button(page, 'Lagre forslag i simuleringen').click(); await expect(page.getByLabel('Utfall', { exact: true })).toHaveValue('normal'); await start(page); await button(page, 'Avslutt arbeidsdagen').click(); await button(page, 'Bekreft avsluttet').click(); await button(page, 'Kontomeldinger').click(); await button(page, 'Vedlikehold meldinger').click();
  await fault(page, 'lost'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByLabel('Utfall', { exact: true })).toHaveValue('lost'); await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByLabel('Utfall', { exact: true })).toHaveValue('normal'); await expect(button(page, 'Lagre melding i simuleringen')).toBeDisabled(); await page.getByLabel('La oppslag feile').check(); await button(page, 'Slå opp original kvittering').click(); await expect(page.getByRole('status')).toContainText('fortsatt uavklart'); await page.getByLabel('La oppslag feile').uncheck(); await button(page, 'Slå opp original kvittering').click(); await expect(page.getByRole('status')).toContainText('SIM-2'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('SIM-3');
});
test('comparison text and focused native-dialog controls have contrast in both themes', async ({ page }) => {
  const contrast = async (selector: string, focus = false) => {
    const result = await page.locator(selector).evaluate((element, checkFocus) => {
      const css = getComputedStyle(element); const rgb = (s: string) => s.match(/[\d.]+/g)!.slice(0, 3).map(Number); const lum = (s: string) => rgb(s).map(n => { n /= 255; return n <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4; }).reduce((sum, v, i) => sum + v * [.2126, .7152, .0722][i], 0);
      const ratio = (a: string, b: string) => (Math.max(lum(a), lum(b)) + .05) / (Math.min(lum(a), lum(b)) + .05);
      let parent: Element | null = checkFocus ? element.parentElement : element; let bg = 'rgb(255,255,255)'; while (parent) { const value = getComputedStyle(parent).backgroundColor; if (value !== 'rgba(0, 0, 0, 0)') { bg = value; break; } parent = parent.parentElement; }
      return { ratio: ratio(checkFocus ? css.outlineColor : css.color, bg), visible: !checkFocus || (element.matches(':focus-visible') && css.outlineStyle !== 'none') };
    }, focus);
    expect(result.ratio).toBeGreaterThanOrEqual(focus ? 3 : 4.5); expect(result.visible).toBe(true);
  };
  await edit(page);
  for (const night of [false, true]) {
    if (night) await button(page, 'Bytt til nattvisning').click();
    await fault(page, 'conflict'); await button(page, 'Lagre forslag i simuleringen').click(); await contrast('section[aria-label="Konflikt"] pre:first-of-type'); await button(page, 'Ta i bruk gjeldende').click();
    await button(page, 'Nullstill simuleringen').click(); await page.keyboard.press('Tab'); await expect(button(page, 'Bekreft nullstilling')).toBeFocused(); await contrast('dialog[open] button:first-of-type', true); await contrast('dialog[open] p'); await page.screenshot({ path: `../docs/evidence/12-2-review-dialog-${night ? 'night' : 'day'}-${Date.now()}.png`, fullPage: true }); await button(page, 'Behold simuleringen').click();
  }
});
