import { test, expect, API, account, setup } from './private-activity-helpers';
import { readFileSync, writeFileSync } from 'node:fs';
setup();
const shifts = JSON.parse(readFileSync('../Eksempelfiler/Fasit-testskift.json', 'utf8').replace(/^\uFEFF/, '')).shifts;
for (const name of ['A', 'B', 'C', 'D', 'E']) test(`generated ${name} real upload full source rows adopt save and reopen`, async ({ page, context }) => {
  test.setTimeout(60000);
  const expected = shifts.find((shift: any) => shift.case === name), events = expected.events.filter((event: any) => event.kind !== 'vehicle');
  const suffix = (value: string | null) => value?.match(/\d{3}$/)?.[0] ?? null;
  const duties: { value: string; suffix: string | null; after_activity: number }[] = [];
  let ordinal = 0;
  for (const event of expected.events) {
    if (event.kind === 'vehicle') duties.push({ value: event.vehicle, suffix: suffix(event.vehicle), after_activity: ordinal });
    else ordinal++;
  }
  const initialDuty = duties[0]?.value ?? null;
  const changes: { index: number; vehicle_duty: string; realtime_duty: string | null }[] = [];
  let previousDuty = initialDuty;
  for (const duty of duties) if (duty.value !== previousDuty && duty.after_activity < events.length) { changes.push({ index: duty.after_activity, vehicle_duty: duty.value, realtime_duty: suffix(duty.value) }); previousDuty = duty.value; }
  function assertIndependentImport(content: any) {
    const metadata = content.import_metadata;
    expect(metadata.qualification).toBe(['B', 'D'].includes(name) ? 'partial' : 'bounded-layout');
    expect(metadata.unresolved.map((issue: any) => issue.code).sort()).toEqual(name === 'B' ? ['unclassified_time', 'unresolved_time', 'unresolved_time'] : name === 'D' ? ['unrecognized_source_line', 'unrecognized_source_line'] : []);
    if (name === 'B') {
      const member = events.findIndex((event: any) => event.unclassified_time) + 1;
      expect(metadata.unresolved.every((issue: any) => issue.activity === member)).toBe(true);
      expect(metadata.unresolved.filter((issue: any) => issue.code === 'unresolved_time').map((issue: any) => issue.field).sort()).toEqual(['end', 'start']);
    }
    expect(metadata.duties.map(({ value, suffix, after_activity }: any) => ({ value, suffix, after_activity }))).toEqual(duties);
    expect(content.vehicle_duty).toBe(initialDuty); expect(content.realtime_duty).toBe(suffix(initialDuty));
    expect(content.vehicle_duty_changes ?? []).toEqual(changes.map(change => ({ from_activity_id: content.activities[change.index].id, vehicle_duty: change.vehicle_duty, realtime_duty: change.realtime_duty })));
    for (let index = 0; index < events.length; index++) {
      const last = [...changes].reverse().find(change => change.index <= index), effective = last?.vehicle_duty ?? initialDuty;
      const activity = content.activities[index];
      if (events[index].kind === 'movement' && events[index].line === 'CAR') expect(activity.type).toBe('CAR');
      if (events[index].kind === 'movement' && events[index].line === 'tom') expect(activity.type).toBe(effective?.startsWith('CAR') ? 'Tomkjøring med CAR' : 'deadhead');
    }
  }
  async function assertAdoptedUI(content: any) {
    await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue(initialDuty ?? '');
    for (let index = 0; index < events.length; index++) {
      const last = [...changes].reverse().find(change => change.index <= index), effective = last?.vehicle_duty ?? initialDuty;
      await expect(page.locator('#activity-' + content.activities[index].id)).toContainText(`Gjeldende vognløp: ${effective ?? 'ukjent'} · sanntidsverdi ${suffix(effective) ?? 'ukjent'}.`);
    }
    if (name === 'B') {
      const warnings = page.getByRole('region', { name: 'Usikkerheter fra importen', exact: true });
      await expect(warnings).toContainText('Ett klokkeslett står i første tidskolonne. Kontroller om det er start eller slutt; begge er uavklart.');
      await expect(warnings).not.toContainText('Ukjent kildeusikkerhet'); await expect(warnings).not.toContainText('unclassified_time');
    }
  }
  await page.goto('/private'); await page.getByLabel('Brukernavn', { exact: true }).fill(account.username); await page.getByLabel('Passord', { exact: true }).fill(account.password); await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast', exact: true })).toBeVisible();
  let imported: any;
  await page.route('**:8001/imports/pdf', async route => { const response = await route.fetch(); expect(response.status()).toBe(200); imported = await response.json(); await route.fulfill({ response, json: imported }); });
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('../Eksempelfiler/Testskift-' + name + '.pdf');
  await expect(page.getByRole('button', { name: 'Rett eller legg til opplysninger', exact: true })).toBeVisible();
  expect(imported.activities).toHaveLength(events.length);
  assertIndependentImport(imported);
  expect(events.length).toBe(({ A: 5, B: 21, C: 15, D: 16, E: 8 } as Record<string, number>)[name]);
  for (let index = 0; index < events.length; index++) {
    const event = events[index], row = imported.activities[index];
    if (event.kind === 'movement') {
      const first = event.stops[0], last = event.stops.at(-1);
      expect([row.trip, row.line, row.from_place, row.to_place]).toEqual([event.trip_id, ['tom', 'CAR'].includes(event.line) ? null : event.line, first.name, last.name]);
      expect(row.start.slice(0, 16)).toBe(first.local_datetime); expect(row.end.slice(0, 16)).toBe(last.local_datetime);
    } else {
      expect(row.raw_code).toBe(event.label); expect(row.start?.slice(0, 16) ?? null).toBe(event.start_local); expect(row.end?.slice(0, 16) ?? null).toBe(event.end_local);
    }
  }
  await page.getByText('Vis alle kildefakta fra PDF', { exact: true }).click();
  const facts = page.getByRole('region', { name: 'Kildefakta fra PDF', exact: true });
  await expect(facts.locator(':scope > ol > li')).toHaveCount(events.length);
  await expect(facts).toContainText(expected.shift_id); await expect(facts).toContainText(expected.end);
  for (const index of [0, events.length - 1]) {
    const row = facts.locator(':scope > ol > li').nth(index); await row.scrollIntoViewIfNeeded(); await expect(row).toBeInViewport();
    const event = events[index]; await expect(row).toContainText(event.label ?? event.trip_id);
  }
  if (name === 'B') {
    await expect(facts).toContainText('Travel to 16:20 · første tidskolonne');
    const travelIndex = events.findIndex((event: any) => event.unclassified_time);
    await expect(facts.locator(':scope > ol > li').nth(travelIndex).locator('dt:text-is("Kildestart") + dd')).toContainText('Ukjent');
    await expect(facts.locator(':scope > ol > li').nth(travelIndex).locator('dt:text-is("Kildeslutt") + dd')).toContainText('Ukjent');
  }
  if (name === 'C') expect(imported.activities.at(-1).end.slice(0, 10)).toBe('2030-02-09');
  if (name === 'D') expect(imported.activities.at(-2).type).toBe('Tomkjøring med CAR');
  await page.getByRole('button', { name: 'Rett eller legg til opplysninger', exact: true }).click();
  await expect(page.getByLabel('Aktivitetstype', { exact: true })).toHaveCount(events.length);
  await assertAdoptedUI(imported);
  const saving = page.waitForResponse(r => r.url() === API + '/drafts' && r.request().method() === 'POST');
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click(); const savedResponse = await saving; expect(savedResponse.status()).toBe(200); const saved = await savedResponse.json();
  expect(saved.draft.activities).toEqual(imported.activities); expect(saved.draft.import_metadata).toEqual(imported.import_metadata);
  assertIndependentImport(saved.draft);
  await page.reload(); await page.getByRole('button', { name: `Åpne ${imported.service_date} · versjon 1`, exact: true }).click();
  await expect(page.getByLabel('Aktivitetstype', { exact: true })).toHaveCount(events.length);
  await assertAdoptedUI(saved.draft);
  await page.getByText('Vis kildefakta fra PDF', { exact: true }).click(); await expect(facts.locator(':scope > ol > li')).toHaveCount(events.length);
  const reopened = await (await context.request.get(API + '/drafts/' + saved.id)).json(); expect(reopened).toEqual(saved); assertIndependentImport(reopened.draft);
  await page.screenshot({ path: `../docs/evidence/11-3-feedback-import-${name}.png`, fullPage: true });
  writeFileSync(`../docs/evidence/11-3-feedback-import-${name}.json`, JSON.stringify({ case: name, activities: events.length, movements: events.filter((event: any) => event.kind === 'movement').length, savedAndReopened: true, qualification: imported.import_metadata.qualification, unknowns: imported.import_metadata.unresolved.map((item: any) => item.code) }, null, 2));
});
