# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fictional-assessment.spec.ts >> night view and modal reset cancellation preserve state; confirmed reset clears unresolved state
- Location: tests\fictional-assessment.spec.ts:94:1

# Error details

```
Error: expect(locator).toBeFocused() failed

Locator:  getByRole('button', { name: 'Nullstill simuleringen', exact: true })
Expected: focused
Received: inactive
Timeout:  5000ms

Call log:
  - Expect "toBeFocused" getByRole('button', { name: 'Nullstill simuleringen', exact: true }) with timeout 5000ms
  - waiting for getByRole('button', { name: 'Nullstill simuleringen', exact: true })
    14 × locator resolved to <button>Nullstill simuleringen</button>
       - unexpected value "inactive"

```

```yaml
- button "Nullstill simuleringen"
```

# Test source

```ts
  1  | import { test, expect, type Page } from '@playwright/test';
  2  | const button = (p: Page, name: string) => p.getByRole('button', { name, exact: true });
  3  | async function edit(p: Page) { await button(p, 'Åpne delvis tekst-PDF-eksempel').click(); }
  4  | async function fault(p: Page, value: string) { if (!await p.getByLabel('Utfall', { exact: true }).isVisible()) await p.getByText('Simuler feil ved neste lagring', { exact: true }).click(); await p.getByLabel('Utfall', { exact: true }).selectOption(value); }
  5  | async function start(p: Page) { await button(p, 'Lagre forslag i simuleringen').click(); await button(p, 'Se lagret dag før start').click(); await button(p, 'Bekreft plan').click(); await button(p, 'Start arbeidsdagen').click(); await button(p, 'Bekreft Start').click(); }
  6  | test.beforeEach(async ({ page }) => {
  7  |   await page.addInitScript(() => {
  8  |     localStorage.setItem('story122-sentinel', 'keep'); sessionStorage.setItem('story122-sentinel', 'keep');
  9  |     document.cookie = 'story122-sentinel=keep;path=/';
  10 |     const counts = { fetch: 0, xhr: 0, gps: 0 }; (window as any).__demoCounts = counts; const forbidden = (key: keyof typeof counts) => { counts[key]++; throw new Error('Demo attempted forbidden browser capability'); };
  11 |     window.fetch = (() => forbidden('fetch')) as typeof fetch; window.XMLHttpRequest = class { constructor() { forbidden('xhr'); } } as typeof XMLHttpRequest;
  12 |     navigator.geolocation.getCurrentPosition = () => forbidden('gps'); navigator.geolocation.watchPosition = () => forbidden('gps');
  13 |   });
  14 |   await page.goto('/demo.html');
  15 |   await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  16 |   const attempted: string[] = []; const errors: string[] = []; (page as any).__attempted = attempted; (page as any).__errors = errors; page.on('pageerror', e => errors.push(e.message)); await page.route('**/*', r => { attempted.push(r.request().url()); return r.abort(); });
  17 | });
  18 | test.afterEach(async ({ page }) => { expect(await page.evaluate(() => (window as any).__demoCounts)).toEqual({ fetch: 0, xhr: 0, gps: 0 }); expect((page as any).__attempted).toEqual([]); expect((page as any).__errors).toEqual([]); });
  19 | test('repeat normal journey, selection, cancellation, terminal unknowns and isolation', async ({ page }) => {
  20 |   for (let repeat = 0; repeat < 2; repeat++) {
  21 |     await edit(page); await page.getByLabel('Fysisk buss').fill('Fiktiv 42'); await start(page);
  22 |     await button(page, 'Velg Linje 100 · Tur A').click(); await expect(page.getByText(/Utfall: Ikke registrert/)).toBeVisible();
  23 |     await page.getByLabel('Foreslått utfall').selectOption('Fullført manuelt'); await button(page, 'Lagre utfall').click(); await button(page, 'Til dagsoversikten').click();
  24 |     await button(page, 'Avslutt arbeidsdagen').click(); await button(page, 'Avbryt bekreftelse').click();
  25 |     await button(page, 'Avslutt arbeidsdagen').click(); await button(page, 'Bekreft avsluttet').click();
  26 |     await expect(page.getByRole('heading', { name: /skrivebeskyttet/ })).toBeVisible();
  27 |     await expect(page.getByText('Pause: Ikke registrert / ukjent', { exact: true })).toBeVisible();
  28 |     await expect(button(page, 'Start arbeidsdagen')).toHaveCount(0);
  29 |     await button(page, 'Nullstill simuleringen').click(); await button(page, 'Behold simuleringen').click();
  30 |     await expect(page.getByRole('heading', { name: /skrivebeskyttet/ })).toBeVisible();
  31 |     await button(page, 'Nullstill simuleringen').click(); await button(page, 'Bekreft nullstilling').click();
  32 |   }
  33 |   expect(await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage }, cookie: document.cookie }))).toEqual({ local: { 'story122-sentinel': 'keep' }, session: { 'story122-sentinel': 'keep' }, cookie: 'story122-sentinel=keep' });
  34 | });
  35 | test('unavailable, immutable reopen, conflict and unresolved receipt lookup', async ({ page }) => {
  36 |   await edit(page); await button(page, 'Lagre forslag i simuleringen').click();
  37 |   await page.getByLabel('Vognløp').fill('Forslag'); await fault(page, 'unavailable'); await button(page, 'Lagre forslag i simuleringen').click();
  38 |   await expect(page.getByRole('status')).toContainText('ikke lagret'); await expect(page.getByLabel('Vognløp')).toHaveValue('Forslag');
  39 |   await button(page, 'Åpne lagret øyeblikksbilde').click(); await expect(page.getByLabel('Vognløp')).toHaveValue('F-42');
  40 |   await page.getByLabel('Vognløp').fill('Mitt forslag'); await fault(page, 'conflict'); await button(page, 'Lagre forslag i simuleringen').click();
  41 |   await expect(page.getByRole('region', { name: 'Konflikt' })).toContainText('Mitt forslag'); await expect(page.getByRole('region', { name: 'Konflikt' })).toContainText('F-99');
  42 |   await button(page, 'Avbryt konflikt').click(); await expect(page.getByLabel('Vognløp')).toHaveValue('Mitt forslag');
  43 |   await fault(page, 'normal'); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Ta i bruk gjeldende').click();
  44 |   await fault(page, 'lost'); await button(page, 'Lagre forslag i simuleringen').click();
  45 |   await expect(button(page, 'Lagre forslag i simuleringen')).toBeDisabled(); await page.getByLabel('La oppslag feile').check(); await button(page, 'Slå opp original kvittering').click();
  46 |   await expect(page.getByRole('status')).toContainText('fortsatt uavklart'); await page.getByLabel('La oppslag feile').uncheck(); await button(page, 'Slå opp original kvittering').click();
  47 |   await expect(page.getByRole('status')).toContainText('SIM-3'); await expect(page.getByRole('status')).toContainText('revisjon 3');
  48 | });
  49 | test('unsupported/manual preserves saved work; reload is volatile; abort preserves unknowns', async ({ page }) => {
  50 |   await edit(page); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Import').click();
  51 |   await button(page, 'Prøv format som ikke støttes').click(); await expect(page.getByRole('status')).toContainText('Lagret arbeid er beholdt');
  52 |   await button(page, 'Registrer manuelt').click(); await expect(page.getByLabel('Vognløp')).toHaveValue(''); await button(page, 'Åpne lagret øyeblikksbilde').click(); await expect(page.getByLabel('Vognløp')).toHaveValue('F-42');
  53 |   await button(page, 'Se lagret dag før start').click(); await button(page, 'Bekreft plan').click(); await button(page, 'Start arbeidsdagen').click(); await button(page, 'Bekreft Start').click(); await button(page, 'Avbryt arbeidsdagen').click(); await button(page, 'Bekreft avbrutt').click();
  54 |   await expect(page.getByText('Linje 100 · Tur A: Ikke registrert / ukjent', { exact: true })).toBeVisible();
  55 |   await page.unroute('**/*'); await page.reload(); await expect(button(page, 'Arbeidsdag')).toBeDisabled();
  56 | });
  57 | test('notices missing source/start, required ending, scope, lost response and independent lifetime', async ({ page }) => {
  58 |   await button(page, 'Kontomeldinger').click(); await expect(page.getByText('Start: Ukjent · Kilde oppdatert: Ukjent · Kildelenke: Ukjent', { exact: true })).toBeVisible();
  59 |   await expect(page.getByRole('article')).toHaveCount(1); await button(page, 'Vedlikehold meldinger').click();
  60 |   await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('sluttid etter simulert nåtid');
  61 |   await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await page.getByLabel('Kildelenke').fill('https://example.invalid/shared');
  62 |   await fault(page, 'lost'); await button(page, 'Lagre melding i simuleringen').click(); await button(page, 'Slå opp original kvittering').click();
  63 |   await button(page, 'Les kontomeldinger').click(); await expect(page.getByRole('article')).toHaveCount(2); await page.getByLabel('Vis linje').selectOption('300'); await expect(page.getByRole('article')).toHaveCount(1);
  64 |   await page.getByLabel('Vis linje').selectOption('200'); await expect(page.getByRole('article')).toHaveCount(2);
  65 |   await button(page, 'Import').click(); await edit(page); await fault(page, 'normal'); await start(page); await button(page, 'Avslutt arbeidsdagen').click(); await button(page, 'Bekreft avsluttet').click(); await expect(page.getByText(/Lagrede kontomeldinger: 1 simulert/)).toBeVisible();
  66 | });
  67 | test('keyboard and narrow layout plus fresh evidence', async ({ page }) => {
  68 |   await page.setViewportSize({ width: 360, height: 800 });
  69 |   await expect(page.getByRole('heading', { name: '1. Velg import' })).toBeFocused(); await page.keyboard.press('Tab'); await expect(button(page, 'Åpne delvis tekst-PDF-eksempel')).toBeFocused();
  70 |   await edit(page); await page.getByLabel('Vognløp').focus(); await page.keyboard.type('X');
  71 |   expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  72 |   await page.screenshot({ path: `../docs/evidence/12-2-demo-narrow-editor-${Date.now()}.png`, fullPage: true });
  73 |   await start(page); await page.screenshot({ path: `../docs/evidence/12-2-demo-narrow-day-${Date.now()}.png`, fullPage: true });
  74 | });
  75 | test('confirmed plan stays fixed, pre-Start selection and Start cancellation return to selected activity', async ({ page }) => {
  76 |   await edit(page); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Se lagret dag før start').click(); await button(page, 'Bekreft plan').click();
  77 |   await button(page, 'Velg Linje 100 · Tur A').click(); await expect(button(page, 'Lagre utfall')).toBeDisabled(); await expect(button(page, 'Forrige aktivitet')).toBeDisabled();
  78 |   await button(page, 'Start arbeidsdagen').click(); await button(page, 'Avbryt Start').click(); await expect(page.getByRole('heading', { name: /Valgt aktivitet: Linje 100/ })).toBeFocused();
  79 |   await button(page, 'Start arbeidsdagen').click(); await button(page, 'Bekreft Start').click();
  80 |   await page.getByLabel('Foreslått utfall').selectOption('Fullført manuelt'); await button(page, 'Avbryt utfallsforslag').click(); await expect(page.getByLabel('Foreslått utfall')).toHaveValue('Ikke registrert');
  81 |   await button(page, 'Neste aktivitet').click(); await button(page, 'Neste aktivitet').click(); await expect(button(page, 'Neste aktivitet')).toBeDisabled();
  82 |   await button(page, 'Utkast').click(); await page.getByLabel('Vognløp').fill('Ny plan'); await button(page, 'Lagre forslag i simuleringen').click(); await button(page, 'Se lagret dag før start').click();
  83 |   await expect(page.getByText(/Bekreftet vognløp: F-42/)).toBeVisible();
  84 |   await button(page, 'Velg Linje 200 · Tur B').click(); await button(page, 'Avbryt arbeidsdagen').click(); await button(page, 'Avbryt bekreftelse').click(); await expect(page.getByRole('heading', { name: /Valgt aktivitet: Linje 200/ })).toBeFocused();
  85 |   await button(page, 'Avbryt arbeidsdagen').click(); await button(page, 'Bekreft avbrutt').click(); await button(page, 'Kontomeldinger').click(); await expect(page.getByRole('article')).toHaveCount(1); await button(page, 'Vedlikehold meldinger').click(); await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('Bekreftet simulert lagring'); await button(page, 'Til oppsummeringen').click(); await expect(page.getByRole('heading', { name: /Avbrutt · skrivebeskyttet/ })).toBeVisible();
  86 | });
  87 | test('notice invalid ending/source, unavailable and conflict preserve proposals', async ({ page }) => {
  88 |   await button(page, 'Kontomeldinger').click(); await button(page, 'Vedlikehold meldinger').click();
  89 |   await page.getByLabel('Slutt (påkrevd)').fill('2026-10-25T02:00'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('sluttid etter simulert nåtid');
  90 |   await page.getByLabel('Slutt (påkrevd)').fill('2026-10-27T02:00'); await page.getByLabel('Kildelenke').fill('javascript:alert(1)'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('HTTP(S)'); await page.getByLabel('Kildelenke').fill('');
  91 |   await fault(page, 'unavailable'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('status')).toContainText('ikke lagret');
  92 |   await fault(page, 'conflict'); await button(page, 'Lagre melding i simuleringen').click(); await expect(page.getByRole('region', { name: 'Konflikt' })).toContainText('Nyere simulert melding'); await button(page, 'Ta i bruk gjeldende').click(); await expect(page.getByLabel('Melding', { exact: true })).toHaveValue('Nyere simulert melding fra en annen økt');
  93 | });
  94 | test('night view and modal reset cancellation preserve state; confirmed reset clears unresolved state', async ({ page }) => {
  95 |   await button(page, 'Bytt til nattvisning').click(); await expect(page.locator('main')).toHaveClass(/demo-night/); await edit(page); await fault(page, 'lost'); await button(page, 'Lagre forslag i simuleringen').click();
> 96 |   await button(page, 'Nullstill simuleringen').click(); await expect(page.getByRole('heading', { name: 'Nullstille bare denne simuleringen?' })).toBeFocused(); await page.keyboard.press('Escape'); await expect(button(page, 'Nullstill simuleringen')).toBeFocused(); await expect(button(page, 'Lagre forslag i simuleringen')).toBeDisabled();
     |                                                                                                                                                                                                                                                           ^ Error: expect(locator).toBeFocused() failed
  97 |   await button(page, 'Nullstill simuleringen').click(); await button(page, 'Bekreft nullstilling').click(); await expect(page.locator('main')).not.toHaveClass(/demo-night/); await edit(page); await button(page, 'Lagre forslag i simuleringen').click(); await expect(page.getByRole('status')).toContainText('SIM-1');
  98 | });
  99 | 
```