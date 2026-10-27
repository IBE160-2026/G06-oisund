import { measureChoices } from './tablet-pc-native';
import { test, expect, openedPlan, setup, account, activityScreen, dayScreen, post } from './private-activity-helpers';
import { measure, measureFocus } from './tablet-pc-measurements';
setup();
test.use({ actionTimeout: 10000 });
for (const scale of [100, 200]) for (const night of [false, true]) for (const width of [800, 1440]) test(`real private surfaces ${night ? 'Night' : 'Day'} ${width}px ${scale}% text`, async ({ page, context }, info) => {
  await page.setViewportSize({ width, height: 1000 }); await page.goto('/private');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEditable();
  if (night) await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.addStyleTag({ content: `:root { font-size: ${scale}%; }` });
  await measure(page, info, 'access'); await measureFocus(page, info, 'access');
  // openedPlan uses actual API operations, review and confirmation; no mock data.
  const { draft } = await openedPlan(page, context, false, undefined, undefined, false, content => {
    content.activities[0].to_place = 'Langt norsk destinasjonsnavn med æ ø å og mange ord '.repeat(5);
  });
  // A navigation replaces the temporary stylesheet, so reapply text enlargement.
  await page.addStyleTag({ content: `:root { font-size: ${scale}%; }` });
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Rediger utkast', exact: true })).toBeFocused();
  await measure(page, info, 'draft-editor'); await measureFocus(page, info, 'draft-editor');
  await page.getByLabel('Vognløp', { exact: true }).fill('Mitt manuelle forslag');
  await post(context, '/drafts/' + draft.id, { operation_id: (await post(context, '/draft-operations', { draft_id: draft.id })).operation_id, expected_revision: 1, draft: { ...draft.draft, vehicle_duty: 'Nyere manuelt forslag', realtime_duty: null } });
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Sammenlign versjoner', exact: true })).toBeVisible();
  await measure(page, info, 'private-conflict'); await measureFocus(page, info, 'private-conflict');
  page.once('dialog', d => d.accept()); await page.getByRole('button', { name: 'Last inn lagret versjon', exact: true }).click();
  // A confirmed source draft cannot be reviewed again, even after editing.
  // Create a separate real draft for the review/acknowledgement surface.
  await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: { ...draft.draft, service_date: '2031-01-03', activities: draft.draft.activities.map((a: any) => ({ ...a, start: a.start?.replace('2031-01-03', '2031-01-04').replace('2031-01-02', '2031-01-03') ?? null, end: a.end?.replace('2031-01-03', '2031-01-04').replace('2031-01-02', '2031-01-03') ?? null })) } });
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne 2031-01-03 · versjon 1', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Rediger utkast', exact: true })).toBeFocused();
  await page.getByRole('button', { name: 'Gjennomgå lagret utkast', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Gjennomgått versjon', exact: true })).toBeVisible();
  await measureChoices(page, info, 'draft-review'); await measure(page, info, 'draft-review'); await measureFocus(page, info, 'draft-review');
  await page.getByRole('button', { name: 'Avbryt gjennomgang', exact: true }).click();
  await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click();
  await measure(page, info, 'day'); await measureFocus(page, info, 'day');
  await page.getByText('Vis 2 pauserader', { exact: true }).click();
  await measure(page, info, 'day-expanded-pauses'); await measureFocus(page, info, 'day-expanded-pauses');
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await activityScreen(page);
  await measure(page, info, 'selected-activity'); await measureFocus(page, info, 'selected-activity');
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await expect(page.getByRole('button', { name: 'Bekreft skiftstart', exact: true })).toBeEnabled(); await measure(page, info, 'start-confirmation'); await measureFocus(page, info, 'start-confirmation');
  await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Skiftstatus', exact: true })).toHaveText('Skiftstart er lagret.');
  await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('skipped');
  await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Aktivitetsstatus og avslutningsstatus', exact: true })).toHaveText('Aktivitetsstatusen er lagret.');
  await measure(page, info, 'outcome'); await measureFocus(page, info, 'outcome'); await dayScreen(page);
  await page.getByRole('button', { name: 'Forberedelse og planlister', exact: true }).click();
  await measure(page, info, 'preparation-with-plan');
  // Regression: the original day button is hidden while preparation is visible.
  const invoker = page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true });
  await invoker.click(); await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toHaveText('Lagrede avvik er hentet.'); await measure(page, info, 'notice-list');
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await expect(invoker).toBeFocused();
  await page.route('**:8001/notices', route => route.fulfill({ status: 503, json: { detail: 'synthetic unavailable' } }));
  await invoker.click(); await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toContainText('utilgjengelig'); await measure(page, info, 'private-unavailable');
  await page.unroute('**:8001/notices'); await page.getByRole('button', { name: 'Hent lagrede avvik', exact: true }).click();
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('En lang norsk melding '.repeat(12));
  await page.getByLabel('Detaljert forklaring', { exact: true }).fill('Lang beskrivelse med mange ord og linjeskift.\n'.repeat(30));
  await measure(page, info, 'notice-editor'); await measureFocus(page, info, 'notice-editor');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click(); await measure(page, info, 'notice-validation');
  page.once('dialog', d => d.accept()); await page.getByRole('button', { name: 'Forkast ulagrede endringer', exact: true }).click();
  await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
  await page.getByLabel('Tittel', { exact: true }).fill('Lagret norsk melding'); await page.getByLabel('Linjeomfang', { exact: true }).selectOption('all');
  await page.getByLabel('Gyldig tildato', { exact: true }).fill('2031-01-04');
  await page.getByRole('button', { name: 'Lagre avvik', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Avviksstatus', exact: true })).toHaveText('Avviket er lagret.'); await measure(page, info, 'notice-saved');
  await expect(page.locator('.notice-list details[open]:visible')).toHaveCount(1); await measure(page, info, 'notice-details');
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByRole('button', { name: 'Til den åpne planen', exact: true }).click();
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  await expect(page.getByText('Lagrede avvik er hentet.', { exact: true })).toBeVisible();
  await page.locator('.notice-list summary:visible').first().click(); await measure(page, info, 'notice-reader'); await measureFocus(page, info, 'notice-reader');
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await page.getByRole('button', { name: 'Avslutt skift', exact: true }).click(); await expect(page.getByRole('button', { name: 'Bekreft avslutning', exact: true })).toBeVisible(); await measure(page, info, 'closure'); await measureFocus(page, info, 'closure');
  await page.getByRole('button', { name: 'Bekreft avslutning', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Oppsummering av skift', exact: true })).toBeVisible(); await measure(page, info, 'recap'); await measureFocus(page, info, 'recap');
  await page.screenshot({ path: info.outputPath('private-recap.png'), fullPage: true });
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeEditable();
  await expect(page.getByRole('button', { name: 'Nattmodus', exact: true })).toHaveAttribute('aria-pressed', String(night));
  expect(await page.evaluate(() => ({ ...localStorage }))).toEqual(night ? { 'ibe160-theme': 'night' } : {});
});

test('notice maintenance returns focus to preparation invoker without an open plan', async ({ page }) => {
  await page.goto('/private'); await page.getByLabel('Brukernavn', { exact: true }).fill(account.username); await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  const invoker = page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true });
  await invoker.click(); await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); await expect(invoker).toBeFocused();
});
test('notice reader maintenance returns focus to visible day entry', async ({ page, context }) => {
  await openedPlan(page, context);
  await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Avvik for linjer og datoer', exact: true })).toBeFocused();
  await page.getByRole('button', { name: 'Til avviksvedlikehold', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeFocused();
  await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true })).toBeFocused();
});
