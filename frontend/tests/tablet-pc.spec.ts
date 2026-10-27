import { measureChoices } from './tablet-pc-native';
import { test, expect, type Page } from '@playwright/test';
import { measure, measureFocus } from './tablet-pc-measurements';
const button = (p: Page, name: string) => p.getByRole('button', { name, exact: true });

test('deterministic manual preference crosses entry/reload/reset without private data', async ({ page }) => {
  await page.goto('/demo');
  await expect(page.getByText('Visning: Dag', { exact: true })).toBeVisible();
  await button(page, 'Bytt til nattvisning').click();
  await expect(button(page, 'Bytt til dagvisning')).toHaveAttribute('aria-pressed', 'true');
  await button(page, 'Åpne delvis tekst-PDF-eksempel').click();
  await page.getByLabel('Vognløp', { exact: true }).fill('Privatliknende verdi skal aldri lagres');
  await button(page, 'Lagre forslag i simuleringen').click();
  await button(page, 'Nullstill simuleringen').click(); await button(page, 'Bekreft nullstilling').click();
  await expect(page.getByText('Visning: Natt', { exact: true })).toBeVisible();
  await page.reload(); await button(page, 'Åpne delvis tekst-PDF-eksempel').click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('F-42');
  await page.goto('/private'); await expect(button(page, 'Nattmodus')).toHaveAttribute('aria-pressed', 'true');
  await button(page, 'Nattmodus').click(); await page.goto('/');
  await expect(page.getByText('Visning: Dag', { exact: true })).toBeVisible();
  expect(await page.evaluate(async () => ({ local: { ...localStorage }, session: { ...sessionStorage }, databases: await indexedDB.databases() }))).toEqual({ local: { 'ibe160-theme': 'day' }, session: {}, databases: [] });
});

for (const storage of ['denied', 'corrupt'] as const) test(storage + ' storage leaves all theme controls usable', async ({ page }) => {
  await page.addInitScript(mode => {
    if (mode === 'denied') Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('Denied', 'SecurityError'); } });
    else { localStorage.setItem('ibe160-theme', '{"private":"not a theme"}'); localStorage.setItem('unrelated-sentinel', 'keep'); }
  }, storage);
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/demo'); await expect(page.getByText('Visning: Dag', { exact: true })).toBeVisible();
  await button(page, 'Bytt til nattvisning').click(); await expect(page.getByText('Visning: Natt', { exact: true })).toBeVisible();
  await button(page, 'Åpne delvis tekst-PDF-eksempel').click(); await expect(page.getByLabel('Vognløp', { exact: true })).toBeEditable();
  if (storage === 'corrupt') expect(await page.evaluate(() => ({ ...localStorage }))).toEqual({ 'ibe160-theme': 'night', 'unrelated-sentinel': 'keep' });
  expect(errors).toEqual([]);
});

for (const scale of [100, 200]) for (const night of [false, true]) for (const width of [800, 1440]) test(`rendered demo states ${night ? 'Night' : 'Day'} ${width}px ${scale}% text`, async ({ page }, info) => {
  await page.setViewportSize({ width, height: 1000 }); await page.goto('/demo');
  if (night) await button(page, 'Bytt til nattvisning').click();
  await page.addStyleTag({ content: `:root { font-size: ${scale}%; }` });
  const check = async (state: string) => { await measure(page, info, state); await measureFocus(page, info, state); };
  await check('import'); await measureFocus(page, info, 'import');
  await button(page, 'Åpne delvis tekst-PDF-eksempel').click();
  await page.getByLabel('Vognløp', { exact: true }).fill('Et svært langt norsk vognløpsnavn med æ ø å og mange ord '.repeat(8));
  await check('editor');
  await page.getByText('Simuler feil ved neste lagring', { exact: true }).click();
  await page.getByLabel('Utfall', { exact: true }).selectOption('unavailable'); await button(page, 'Lagre forslag i simuleringen').click(); await check('unavailable');
  await page.getByLabel('Utfall', { exact: true }).selectOption('conflict'); await button(page, 'Lagre forslag i simuleringen').click(); await check('conflict');
  await button(page, 'Ta i bruk gjeldende').click();
  await page.getByLabel('Utfall', { exact: true }).selectOption('lost'); await button(page, 'Lagre forslag i simuleringen').click();
  await check('pending'); await measureChoices(page, info, 'pending');
  await button(page, 'Slå opp original kvittering').click(); await button(page, 'Lagre forslag i simuleringen').click();
  await button(page, 'Se lagret dag før start').click(); await check('confirmation'); await button(page, 'Bekreft plan').click(); await check('day');
  await button(page, 'Velg Linje 100 · Tur A').click(); await check('activity-disabled');
  await button(page, 'Start arbeidsdagen').click(); await check('start'); await button(page, 'Avbryt Start').click(); await expect(button(page, 'Start arbeidsdagen')).toBeFocused();
  await button(page, 'Start arbeidsdagen').click(); await button(page, 'Bekreft Start').click();
  await page.getByLabel('Foreslått utfall').selectOption('Hoppet over'); await button(page, 'Lagre utfall').click(); await check('outcome');
  await button(page, 'Avslutt arbeidsdagen').click(); await check('closure'); await button(page, 'Bekreft avsluttet').click(); await check('recap');
  await button(page, 'Kontomeldinger').click(); await check('notice-reader'); await button(page, 'Vedlikehold meldinger').click();
  await page.getByLabel('Melding', { exact: true }).fill('Lang norsk melding som må kunne brytes og leses ved forstørring. '.repeat(12));
  await check('notice-editor'); await button(page, 'Lagre melding i simuleringen').click(); await check('notice-error');
  await button(page, 'Nullstill simuleringen').click(); await check('native-modal'); await measureFocus(page, info, 'native-modal');
  await page.screenshot({ path: info.outputPath('modal.png'), fullPage: true });
  await page.keyboard.press('Escape'); await expect(button(page, 'Nullstill simuleringen')).toBeFocused();
});

for (const scale of [100, 200]) for (const night of [false, true]) for (const width of [800, 1440]) test(`rendered API assessment ${night ? 'Night' : 'Day'} ${width}px ${scale}% text`, async ({ page }, info) => {
  await page.setViewportSize({ width, height: 1000 }); await page.goto('/');
  await expect(page.getByRole('status')).toContainText('Ikke lagret');
  if (night) await button(page, 'Nattmodus').click();
  await page.addStyleTag({ content: `:root { font-size: ${scale}%; }` });
  await measure(page, info, 'api-assessment-day'); await measureFocus(page, info, 'api-assessment-day');
  await button(page, 'Lagre fiktiv dag').click(); await expect(page.getByRole('status')).toHaveText('Lagret og bekreftet av tjenesten.');
  await measure(page, info, 'api-assessment-saved'); await measureFocus(page, info, 'api-assessment-saved');
  await page.reload(); await expect(page.getByRole('status')).toHaveText('Lagret eksempel er hentet fra tjenesten.');
  await page.addStyleTag({ content: `:root { font-size: ${scale}%; }` });
  await expect(button(page, 'Nattmodus')).toHaveAttribute('aria-pressed', String(night));
  await measure(page, info, 'api-assessment-reopened'); await measureFocus(page, info, 'api-assessment-reopened');
  await page.route('**:8000/fixture', route => route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } }));
  await button(page, 'Last inn nytt fiktivt eksempel').click(); await expect(page.getByRole('status')).toContainText('Utilgjengelig');
  await measure(page, info, 'api-assessment-unavailable'); await measureFocus(page, info, 'api-assessment-unavailable');
});
