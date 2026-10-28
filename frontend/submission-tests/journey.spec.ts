import { test, expect, type Page, type BrowserContext } from '@playwright/test';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const API = 'http://127.0.0.1:18328';
const account = JSON.parse(readFileSync('../.private-runtime/submission/account.json', 'utf8'));
if (account.username !== 'synthetic-submission') throw Error('Only isolated submission credentials are permitted');
const oracle = JSON.parse(readFileSync('../Eksempelfiler/Fasit-testskift.json', 'utf8').replace(/^\uFEFF/, '')).shifts;
const button = (page: Page, name: string) => page.getByRole('button', { name, exact: true });
async function get(context: BrowserContext, path: string) {
  const response = await context.request.get(API + path);
  expect(response.status()).toBe(200);
  expect(response.headers()['cache-control']).toBe('no-store');
  return response.json();
}
function winterInstant(actual: string | null, local: string | null) {
  if (local === null) { expect(actual).toBeNull(); return; }
  expect(actual).toMatch(/(?:Z|[+-]\d{2}:\d{2})$/);
  expect(Date.parse(actual!)).toBe(Date.parse(local + ':00+01:00'));
}

for (const [name, action] of [['A', 'ended'], ['C', 'aborted']] as const) {
  test(`submission actual API/PostgreSQL journey ${name}: import correct save confirm use ${action} reopen`, async ({ page, context, browser }) => {
    const requestedOrigins = new Set<string>();
    page.on('request', request => requestedOrigins.add(new URL(request.url()).origin));
    // All writes go to the separately guarded submission runtime; no API routes are mocked.
    execFileSync(process.execPath, ['scripts/submission.mjs', 'status'], { cwd: '..', timeout: 30000 });
    await page.goto('/private');
    await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
    await page.getByLabel('Passord', { exact: true }).fill(account.password);
    await button(page, 'Logg inn').click();
    await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
    const originalDrafts = (await get(context, '/drafts')).drafts.length;
    const expected = oracle.find((entry: any) => entry.case === name);
    const events = expected.events.filter((entry: any) => entry.kind !== 'vehicle');
    const importedReply = page.waitForResponse(r => r.url() === API + '/imports/pdf' && r.request().method() === 'POST');
    await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('../Eksempelfiler/Testskift-' + name + '.pdf');
    const response = await importedReply;
    expect(response.status()).toBe(200);
    const bytes = readFileSync('../Eksempelfiler/Testskift-' + name + '.pdf');
    expect(response.request().postDataBuffer()).toEqual(bytes);
    const imported = await response.json();
    expect(imported.service_date).toBe(expected.date.split('/').reverse().join('-'));
    expect(imported.import_metadata.header.shift_id).toBe(expected.shift_id);
    expect(imported.physical_bus).toBeNull();
    expect(imported.vehicle_duty).toBe(expected.events.find((entry: any) => entry.kind === 'vehicle').vehicle);
    expect(imported.activities).toHaveLength(events.length);
    for (let i = 0; i < events.length; i++) {
      const row = imported.activities[i], event = events[i];
      if (event.kind === 'movement') {
        expect([row.trip, row.line, row.from_place, row.to_place]).toEqual([event.trip_id, ['tom', 'CAR'].includes(event.line) ? null : event.line, event.stops[0].name, event.stops.at(-1).name]);
        winterInstant(row.start, event.stops[0].local_datetime);
        winterInstant(row.end, event.stops.at(-1).local_datetime);
      } else {
        expect(row.raw_code).toBe(event.label);
        winterInstant(row.start, event.start_local);
        winterInstant(row.end, event.end_local);
      }
    }
    expect((await get(context, '/drafts')).drafts).toHaveLength(originalDrafts);
    await button(page, 'Rett eller legg til opplysninger').click();
    const index = events.findIndex((entry: any) => entry.passenger_service);
    const trip = page.locator('#activity-' + imported.activities[index].id);
    await trip.getByLabel('Til sted', { exact: true }).fill('Syntetisk korrigert endeholdeplass 12.5');
    await trip.getByLabel('Kilde / manuell rettelse', { exact: true }).fill('Manuelt valgt i reproduksjonsprøven');
    await page.getByLabel('Buss/vogn', { exact: true }).fill('SYN-125');
    const savedReply = page.waitForResponse(r => r.url() === API + '/drafts' && r.request().method() === 'POST');
    await button(page, 'Lagre utkast').click();
    const savedResponse = await savedReply;
    expect(savedResponse.status()).toBe(200);
    const saved = await savedResponse.json();
    expect(saved.draft.import_metadata).toEqual(imported.import_metadata);
    expect(saved.draft.activities[index].to_place).toBe('Syntetisk korrigert endeholdeplass 12.5');
    expect(saved.draft.activities[index].provenance).toBe('Manuelt valgt i reproduksjonsprøven');
    expect(saved.draft.physical_bus).toBe('SYN-125');
    await page.reload();
    await button(page, `Åpne ${saved.draft.service_date} · versjon 1`).click();
    expect(await get(context, '/drafts/' + saved.id)).toEqual(saved);
    await button(page, 'Gjennomgå lagret utkast').click();
    const review = page.getByRole('region', { name: 'Gjennomgått versjon', exact: true });
    await expect(review).toBeVisible();
    await expect(button(page, 'Bekreft gjennomgått plan')).toBeDisabled();
    for (const checkbox of await review.getByRole('checkbox').all()) await checkbox.check();
    const confirmedReply = page.waitForResponse(r => r.url().endsWith('/confirm') && r.request().method() === 'POST');
    await button(page, 'Bekreft gjennomgått plan').click();
    const confirmedResponse = await confirmedReply;
    expect(confirmedResponse.status()).toBe(200);
    const plan = await confirmedResponse.json();
    expect(plan.source_draft_id).toBe(saved.id);
    expect(plan.draft).toEqual(saved.draft);
    await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
    await expect(page.getByText('Ingen aktivitet valgt', { exact: true })).toBeVisible();
    await button(page, 'Manuelt vedlikeholdte avvik').click();
    await button(page, 'Registrer avvik').click();
    const title = 'Fiktivt avvik reproduksjon 12.5 ' + name;
    await page.getByLabel('Tittel', { exact: true }).fill(title);
    await page.getByLabel('Detaljert forklaring', { exact: true }).fill('Syntetisk manuell registrering; ingen sanntidskilde.');
    await page.getByLabel('Linjer fra kilden (kommaseparert)', { exact: true }).fill(name === 'A' ? '731' : '81');
    await page.getByLabel('Gyldig tildato', { exact: true }).fill('2030-02-10');
    await button(page, 'Lagre avvik').click();
    await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toHaveText('Avviket er lagret.');
    await button(page, 'Tilbake til dagen').click();
    await button(page, 'Les avvik for linjer og datoer').click();
    const reader = page.getByRole('region', { name: 'Avvik for linjer og datoer', exact: true });
    await reader.getByLabel('Bekreftet linje', { exact: true }).selectOption(name === 'A' ? '731' : '81');
    await reader.getByLabel('Planlagt kalenderdato (Oslo)', { exact: true }).selectOption(saved.draft.service_date);
    await expect(reader.locator('.notice-list summary')).toContainText(title);
    await reader.locator('.notice-list summary').click();
    await expect(reader).toContainText('Kildens oppdateringstid er ukjent');
    await expect(reader).toContainText('Ikke kontrollert');
    await reader.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
    await button(page, 'Velg aktivitet ' + (index + 1)).click();
    await expect(page.locator('.selected-activity')).toContainText('Syntetisk korrigert endeholdeplass 12.5');
    await button(page, 'Tilbake til dagen').click();
    await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
    await button(page, 'Start skift').click();
    await button(page, 'Bekreft skiftstart').click();
    await expect(page.getByRole('status', { name: 'Skiftstatus', exact: true })).toHaveText('Skiftstart er lagret.');
    await button(page, 'Åpne valgt aktivitet').click();
    await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption(action === 'ended' ? 'completed' : 'interrupted');
    await button(page, 'Lagre aktivitetsstatus').click();
    await expect(page.getByRole('status', { name: 'Aktivitetsstatus og avslutningsstatus', exact: true })).toHaveText('Aktivitetsstatusen er lagret.');
    await button(page, 'Tilbake til dagen').click();
    await button(page, action === 'ended' ? 'Avslutt skift' : 'Avbryt skift').click();
    await button(page, action === 'ended' ? 'Bekreft avslutning' : 'Bekreft avbrudd').click();
    const heading = action === 'ended' ? 'Skift avsluttet' : 'Skift avbrutt';
    await expect(page.getByRole('heading', { name: heading, exact: true })).toBeVisible();
    const recap = await get(context, '/workdays/' + plan.id + '/recap');
    const session = await get(context, '/auth/session');
    expect(recap.lifecycle.state).toBe(action);
    expect(recap.plan.draft).toEqual(saved.draft);
    expect(recap.outcomes.outcomes.map((entry: any) => entry.outcome)).toEqual(saved.draft.activities.map((_: any, i: number) => i === index ? action === 'ended' ? 'completed' : 'interrupted' : 'unregistered'));
    expect(recap.bus.physical_bus).toBe('SYN-125');
    if (name === 'A') {
      execFileSync(process.execPath, ['scripts/submission.mjs', 'restart'], { cwd: '..', timeout: 120000 });
      expect(await get(context, '/workdays/' + plan.id + '/recap')).toEqual(recap);
      expect(await get(context, '/auth/session')).toEqual(session);
      expect(await get(context, '/drafts/' + saved.id)).toEqual(saved);
    }
    await page.reload();
    await button(page, `Åpne plan ${saved.draft.service_date} · versjon 1`).click();
    await expect(page.getByRole('heading', { name: heading, exact: true })).toBeVisible();
    await expect(button(page, 'Start skift')).toBeHidden();
    expect(await get(context, '/workdays/' + plan.id + '/recap')).toEqual(recap);
    const storage = await page.evaluate(async () => ({ local: Object.keys(localStorage).filter(key => key !== 'ibe160-theme'), session: Object.keys(sessionStorage), databases: (await indexedDB.databases()).length, caches: (await caches.keys()).length, workers: (await navigator.serviceWorker.getRegistrations()).length }));
    expect(storage).toEqual({ local: [], session: [], databases: 0, caches: 0, workers: 0 });
    mkdirSync('../tmp/submission-browser-results', { recursive: true });
    await page.screenshot({ path: `../tmp/submission-browser-results/journey-${name}.png`, fullPage: true });
    // Synthetic records only; no cookies, token or generated password is recorded.
    expect([...requestedOrigins].every(origin => ['http://127.0.0.1:15325', API].includes(origin))).toBe(true);
    writeFileSync(`../tmp/submission-browser-results/journey-${name}.json`, JSON.stringify({ synthetic: true, mockedApi: false, browser: browser.version(), viewport: page.viewportSize(), requestedOrigins: [...requestedOrigins], exactUploadedBytes: bytes.length, case: name, saved, recap, restartPreserved: name === 'A', storage }, null, 2));
  });
}

test('submission correct import B saves directly into distinct saved-version approval', async ({ page, context }) => {
  execFileSync(process.execPath, ['scripts/submission.mjs', 'status'], { cwd: '..', timeout: 30000 });
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await button(page, 'Logg inn').click();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
  const before = (await get(context, '/drafts')).drafts.length;
  const reply = page.waitForResponse(r => r.url() === API + '/imports/pdf' && r.request().method() === 'POST');
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('../Eksempelfiler/Testskift-B.pdf');
  const imported = await (await reply).json();
  const expected = oracle.find((entry: any) => entry.case === 'B');
  expect(imported.service_date).toBe(expected.date.split('/').reverse().join('-'));
  expect(imported.import_metadata.header.shift_id).toBe(expected.shift_id);
  expect((await get(context, '/drafts')).drafts).toHaveLength(before);
  const savedReply = page.waitForResponse(r => r.url() === API + '/drafts' && r.request().method() === 'POST');
  await button(page, 'Alt stemmer – lagre og fortsett').click();
  const response = await savedReply;
  expect(response.status()).toBe(200);
  const saved = await response.json();
  expect(saved.draft).toEqual(imported);
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon', exact: true })).toBeVisible();
  expect(await get(context, '/drafts/' + saved.id)).toEqual(saved);
  expect((await get(context, '/drafts')).drafts).toHaveLength(before + 1);
});
