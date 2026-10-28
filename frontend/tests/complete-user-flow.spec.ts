import { test, expect, API, account, setup, dayScreen, activityScreen, selected, shiftStatus } from './private-activity-helpers';
import { readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import type { Page, BrowserContext } from '@playwright/test';

setup();
// Headed desktop automation proves real tab focus. Visibility lifecycle is
// exercised separately: this runtime keeps background tabs visible.
test.use({ headless: false, actionTimeout: 15000, navigationTimeout: 30000 });
// Authored independently of the parser. Never regenerate these facts from an import.
const oracle = JSON.parse(readFileSync('../Eksempelfiler/Fasit-testskift.json', 'utf8').replace(/^\uFEFF/, '')).shifts;
const button = (page: Page, name: string) => page.getByRole('button', { name, exact: true });
function assertWinterInstant(actual: string | null, local: string | null) {
  if (local === null) { expect(actual).toBeNull(); return; }
  // These independent fixtures are in February, explicitly UTC+01:00 in Oslo.
  // Do not let host timezone or the parser supply the expected UTC instant.
  expect(actual).toMatch(/(?:Z|[+-]\d{2}:\d{2})$/);
  expect(Date.parse(actual!)).toBe(Date.parse(local + ':00+01:00'));
}
async function json(context: BrowserContext, path: string) {
  const response = await context.request.get(API + path); expect(response.status()).toBe(200); return response.json();
}
async function login(page: Page) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await button(page, 'Logg inn').click();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
}
async function importAndSave(page: Page, context: BrowserContext, name: string) {
  const expected = oracle.find((value: any) => value.case === name);
  const events = expected.events.filter((value: any) => value.kind !== 'vehicle');
  const response = page.waitForResponse(r => r.url() === API + '/imports/pdf' && r.request().method() === 'POST');
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('../Eksempelfiler/Testskift-' + name + '.pdf');
  const result = await response; expect(result.status()).toBe(200);
  const pdfBytes = readFileSync('../Eksempelfiler/Testskift-' + name + '.pdf');
  expect(result.request().postDataBuffer()).toEqual(pdfBytes);
  const imported = await result.json();
  const serviceDate = expected.date.split('/').reverse().join('-');
  expect(imported.service_date).toBe(serviceDate);
  expect(imported.import_metadata.header.service_date).toBe(serviceDate);
  expect(imported.import_metadata.header.shift_id).toBe(expected.shift_id);
  await expect(button(page, 'Rett eller legg til opplysninger')).toBeVisible();
  expect((await json(context, '/drafts')).drafts).toHaveLength(name === 'A' ? 0 : 1);
  expect(imported.activities).toHaveLength(events.length);
  for (let i = 0; i < events.length; i++) {
    const row = imported.activities[i], event = events[i];
    if (event.kind === 'movement') {
      expect([row.trip, row.line, row.from_place, row.to_place]).toEqual([event.trip_id, ['tom', 'CAR'].includes(event.line) ? null : event.line, event.stops[0].name, event.stops.at(-1).name]);
      expect(row.start.slice(0, 16)).toBe(event.stops[0].local_datetime);
      expect(row.end.slice(0, 16)).toBe(event.stops.at(-1).local_datetime);
      assertWinterInstant(row.start, event.stops[0].local_datetime);
      assertWinterInstant(row.end, event.stops.at(-1).local_datetime);
    } else {
      expect(row.raw_code).toBe(event.label);
      expect(row.start?.slice(0, 16) ?? null).toBe(event.start_local);
      expect(row.end?.slice(0, 16) ?? null).toBe(event.end_local);
      assertWinterInstant(row.start, event.start_local);
      assertWinterInstant(row.end, event.end_local);
    }
  }
  expect(imported.vehicle_duty).toBe(expected.events.find((event: any) => event.kind === 'vehicle').vehicle);
  expect(imported.physical_bus).toBeNull();
  await button(page, 'Rett eller legg til opplysninger').click();
  const tripIndex = events.findIndex((event: any) => event.passenger_service);
  const trip = page.locator('#activity-' + imported.activities[tripIndex].id);
  await trip.getByLabel('Til sted', { exact: true }).fill('Syntetisk manuelt korrigert endeholdeplass');
  await trip.getByLabel('Kilde / manuell rettelse', { exact: true }).fill('Manuelt kontrollert mot syntetisk oppgave');
  await page.getByLabel('Buss/vogn', { exact: true }).fill('SYN-124');
  const savedReply = page.waitForResponse(r => r.url() === API + '/drafts' && r.request().method() === 'POST');
  await button(page, 'Lagre utkast').click();
  const savedResponse = await savedReply; expect(savedResponse.status()).toBe(200); const saved = await savedResponse.json();
  expect(saved.draft.activities[tripIndex].to_place).toBe('Syntetisk manuelt korrigert endeholdeplass');
  expect(saved.draft.activities[tripIndex].provenance).toBe('Manuelt kontrollert mot syntetisk oppgave');
  expect(saved.draft.activities[tripIndex].direction).toBeNull();
  expect(saved.draft.import_metadata).toEqual(imported.import_metadata);
  expect(saved.draft.physical_bus).toBe('SYN-124');
  return { saved, imported, expected, tripIndex, uploadedBytes: pdfBytes.length };
}

for (const [name, action] of [['A', 'ended'], ['C', 'aborted']] as const) {
  test(`real two-document journey ${name}: explicit correction notice tab restore and ${action} recap`, async ({ page, context, browser }) => {
    test.setTimeout(240000);
    await test.step('Log in to the synthetic account', () => login(page));
    const a = await test.step('Import A with exact bytes, independent facts and explicit save', () => importAndSave(page, context, 'A'));
    await button(page, 'Forberedelse og planlister').click();
    const c = await test.step('Import C with midnight facts and a separate saved identity', () => importAndSave(page, context, 'C'));
    expect(c.saved.id).not.toBe(a.saved.id);
    expect(c.imported.activities.some((row: any) => row.end?.startsWith('2030-02-09'))).toBe(true);
    expect((await json(context, '/drafts')).drafts).toHaveLength(2);
    const chosen = name === 'A' ? a : c;
    await page.reload();
    await button(page, `Åpne ${chosen.saved.draft.service_date} · versjon 1`).click();
    const reopened = await json(context, '/drafts/' + chosen.saved.id); expect(reopened).toEqual(chosen.saved);
    await page.getByText('Vis kildefakta fra PDF', { exact: true }).click();
    await expect(page.getByRole('region', { name: 'Kildefakta fra PDF', exact: true })).toContainText(chosen.expected.shift_id);
    await button(page, 'Gjennomgå lagret utkast').click();
    const review = page.getByRole('region', { name: 'Gjennomgått versjon', exact: true });
    await expect(review).toBeVisible();
    await expect(button(page, 'Bekreft gjennomgått plan')).toBeDisabled();
    for (const checkbox of await review.getByRole('checkbox').all()) await checkbox.check();
    const confirmation = page.waitForResponse(r => r.url().endsWith('/confirm') && r.request().method() === 'POST');
    await button(page, 'Bekreft gjennomgått plan').click();
    const confirmedResponse = await confirmation; expect(confirmedResponse.status()).toBe(200); const plan = await confirmedResponse.json();
    expect(plan.source_draft_id).toBe(chosen.saved.id);
    expect(plan.draft.import_metadata).toEqual(chosen.imported.import_metadata);
    expect(plan.unknowns.some((unknown: any) => unknown.id.endsWith(':direction'))).toBe(true);
    await expect(page.getByText('Ingen aktivitet valgt', { exact: true })).toBeVisible();
    await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();

    await button(page, 'Manuelt vedlikeholdte avvik').click();
    await expect(button(page, 'Registrer avvik')).toBeEnabled(); await button(page, 'Registrer avvik').click();
    const title = 'Syntetisk flerlinjeavvik 12.4 ' + name;
    const description = 'Første tidsvindu: omkjøring ved Måneglimt.\nAndre tidsvindu: bruk midlertidig holdeplass.';
    await page.getByLabel('Tittel', { exact: true }).fill(title);
    await page.getByLabel('Detaljert forklaring', { exact: true }).fill(description);
    await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill('731, 81');
    await page.getByLabel('Gyldig tildato', { exact: true }).fill('2030-02-10');
    await expect(page.getByRole('region', { name: 'Lagringskrav' })).not.toContainText('ufullstendig');
    // Remove Playwright's focus override, then exercise an actual browser tab.
    // No API response or native focus/blur event is fabricated.
    const focusSession = await context.newCDPSession(page);
    await focusSession.send('Emulation.setFocusEmulationEnabled', { enabled: false });
    await page.evaluate(() => {
      (window as any).__story124Visibility = [];
      (window as any).__story124Focus = [];
      document.addEventListener('visibilitychange', () => (window as any).__story124Visibility.push(document.visibilityState));
      window.addEventListener('blur', () => (window as any).__story124Focus.push('blur'));
      window.addEventListener('focus', () => (window as any).__story124Focus.push('focus'));
    });
    const other = await context.newPage(); await other.goto('/demo.html');
    const otherFocusSession = await context.newCDPSession(other);
    await otherFocusSession.send('Emulation.setFocusEmulationEnabled', { enabled: false });
    await test.step('Switch actual browser tabs and observe native focus', async () => {
      await other.bringToFront();
      await expect.poll(() => page.evaluate(() => document.hasFocus())).toBe(false);
      await page.bringToFront();
      await expect.poll(() => page.evaluate(() => document.hasFocus())).toBe(true);
    });
    const visibility = await page.evaluate(() => (window as any).__story124Visibility);
    const focus = await page.evaluate(() => (window as any).__story124Focus);
    expect(focus).toContain('blur'); expect(focus).toContain('focus');
    await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue(title);
    await expect(page.getByLabel('Detaljert forklaring', { exact: true })).toHaveValue(description);
    // Separate lifecycle fault injection: tab switching above does not emit
    // hidden/visible in this runtime. Session restoration still uses the real API.
    if (name === 'C') {
      const originalSession = await json(context, '/auth/session');
      await test.step('Inject hidden lifecycle while preserving the dirty editor', async () => {
        await page.evaluate(() => {
          const descriptor = Object.getOwnPropertyDescriptor(document, 'visibilityState');
          (window as any).__story124RestoreVisibility = () => {
            if (descriptor) Object.defineProperty(document, 'visibilityState', descriptor);
            else delete (document as any).visibilityState;
            document.dispatchEvent(new Event('visibilitychange'));
          };
          Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' });
          document.dispatchEvent(new Event('visibilitychange'));
        });
        await expect(page.getByLabel('Tittel', { exact: true })).toBeHidden();
      });
      await test.step('Restore original authorization without saving the proposal', async () => {
        const restored = page.waitForResponse(r => r.url() === API + '/auth/session');
        await page.evaluate(() => (window as any).__story124RestoreVisibility());
        const restoredResponse = await restored; expect(restoredResponse.status()).toBe(200);
        expect(await restoredResponse.json()).toEqual(originalSession);
        await expect(page.getByRole('status', { name: 'Tilgangsstatus', exact: true })).toHaveText('Du er logget inn.');
        await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue(title);
        await expect(page.getByLabel('Detaljert forklaring', { exact: true })).toHaveValue(description);
        expect((await json(context, '/notices')).notices).toHaveLength(0);
      });
    }
    expect((await json(context, '/notices')).notices).toHaveLength(0);
    await other.close();
    await button(page, 'Tilbake til avvik').click(); await button(page, 'Tilbake til ulagret avvik').click();
    await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue(title);
    await button(page, 'Lagre avvik').click();
    await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toHaveText('Avviket er lagret.');
    const notices = (await json(context, '/notices')).notices;
    expect(notices).toHaveLength(1);
    expect(notices[0]).toMatchObject({ title, description, line_tags: ['731', '81'], valid_from: null, source_updated_at: null, checked_at: null, valid_until: '2030-02-10T23:59:59+01:00' });
    await button(page, 'Tilbake til dagen').click();
    // The injected hide can interrupt the focus-triggered current read. Recover
    // authority through the offered explicit read before opening dependent views.
    if (name === 'C') await test.step('Recover current day authority after lifecycle interruption', async () => {
      await button(page, 'Hent skift og aktivitetsstatus igjen').click();
      await expect(page.getByRole('status', { name: 'Aktivitetsstatus og avslutningsstatus' })).toHaveText('Lagret skift og aktivitetsstatus er hentet.');
    });
    await button(page, 'Les avvik for linjer og datoer').click();
    const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
    await reader.getByLabel('Bekreftet linje', { exact: true }).selectOption(name === 'A' ? '731' : '81');
    await reader.getByLabel('Planlagt kalenderdato (Oslo)', { exact: true }).selectOption(chosen.saved.draft.service_date);
    await expect(reader.locator('.notice-list summary')).toContainText(title);
    await reader.locator('.notice-list summary').click();
    await expect(reader).toContainText('Delvis kjent gyldighet');
    await expect(reader).toContainText('Kildens oppdateringstid er ukjent');
    await expect(reader).toContainText('Ikke kontrollert');
    await reader.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
    await button(page, 'Velg aktivitet ' + (chosen.tripIndex + 1)).click(); await activityScreen(page);
    await expect(selected(page)).toContainText('Syntetisk manuelt korrigert endeholdeplass');
    const selection = await json(context, '/workdays/' + plan.id + '/selection');
    expect(selection.activity_id).toBe(chosen.saved.draft.activities[chosen.tripIndex].id);
    expect(selection.revision).toBe(1);
    await dayScreen(page); await button(page, 'Start skift').click(); await button(page, 'Bekreft skiftstart').click();
    await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
    await activityScreen(page);
    await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption(action === 'ended' ? 'completed' : 'interrupted');
    await button(page, 'Lagre aktivitetsstatus').click();
    await expect(page.getByRole('status', { name: 'Aktivitetsstatus og avslutningsstatus' })).toHaveText('Aktivitetsstatusen er lagret.');
    await dayScreen(page); await button(page, action === 'ended' ? 'Avslutt skift' : 'Avbryt skift').click();
    await button(page, action === 'ended' ? 'Bekreft avslutning' : 'Bekreft avbrudd').click();
    await expect(page.getByRole('heading', { name: action === 'ended' ? 'Skift avsluttet' : 'Skift avbrutt', exact: true })).toBeVisible();
    const recapUI = page.getByRole('region', { name: 'Oppsummering av skift', exact: true });
    await expect(recapUI.locator('dt:text-is("Ikke registrert") + dd')).toHaveText(String(chosen.saved.draft.activities.length - 1));
    await expect(recapUI.locator(`dt:text-is("${action === 'ended' ? 'Fullført manuelt' : 'Avbrutt'}") + dd`)).toHaveText('1');
    const recap = await json(context, '/workdays/' + plan.id + '/recap');
    expect(recap.lifecycle.state).toBe(action);
    expect(recap.plan.source_draft_id).toBe(chosen.saved.id);
    expect(recap.plan.draft).toEqual(chosen.saved.draft);
    expect(recap.outcomes.outcomes.map((row: any) => row.outcome)).toEqual(chosen.saved.draft.activities.map((_: any, i: number) => i === chosen.tripIndex ? action === 'ended' ? 'completed' : 'interrupted' : 'unregistered'));
    expect(recap.bus.physical_bus).toBe('SYN-124');
    if (name === 'A') {
      if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project selection required');
      await test.step('Restart actual database and API and verify fixed records', async () => {
        const compose = ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml'];
        for (const service of ['private-db', 'private-api']) {
          execFileSync('docker', [...compose, 'restart', service], { cwd: '..', timeout: 30000 });
          execFileSync('docker', [...compose, 'start', '--wait', '--wait-timeout', '45', service], { cwd: '..', timeout: 60000 });
        }
        expect(await json(context, '/workdays/' + plan.id + '/recap')).toEqual(recap);
        expect(await json(context, '/workdays/' + plan.id + '/selection')).toEqual({ ...selection, expires_at: recap.plan.expires_at });
      });
    }
    await page.reload(); await button(page, `Åpne plan ${chosen.saved.draft.service_date} · versjon 1`).click();
    await expect(page.getByRole('heading', { name: action === 'ended' ? 'Skift avsluttet' : 'Skift avbrutt', exact: true })).toBeVisible();
    await expect(button(page, 'Start skift')).toBeHidden();
    await expect(button(page, 'Bekreft skiftstart')).toBeHidden();
    expect(await json(context, '/workdays/' + plan.id + '/recap')).toEqual(recap);
    expect(await json(context, '/workdays/' + plan.id + '/selection')).toEqual({ ...selection, expires_at: recap.plan.expires_at });
    expect((await json(context, '/notices')).notices).toEqual(notices);
    const storage = await page.evaluate(async () => ({ local: Object.keys(localStorage), session: Object.keys(sessionStorage), databases: (await indexedDB.databases()).length, caches: (await caches.keys()).length, workers: (await navigator.serviceWorker.getRegistrations()).length }));
    expect(storage.local.filter(key => key !== 'ibe160-theme')).toEqual([]);
    expect(storage).toMatchObject({ session: [], databases: 0, caches: 0, workers: 0 });
    await page.screenshot({ path: `../docs/evidence/12-4-journey-${name}.png`, fullPage: true });
    const browserRuntime = { version: browser.version(), viewport: page.viewportSize(), platform: process.platform, userAgent: await page.evaluate(() => navigator.userAgent) };
    writeFileSync(`../docs/evidence/12-4-journey-${name}.json`, JSON.stringify({ synthetic: true, mockedApi: false, browserRuntime, case: name, action, databaseAndApiRestart: name === 'A', nativeVisibilityEvents: visibility, nativeFocusEvents: focus, lifecycleEmulation: name === 'C', exactUploadedBytes: [a.uploadedBytes, c.uploadedBytes], draftIds: [a.saved.id, c.saved.id], planId: plan.id, selection, recap, notices }, null, 2));
  });
}
