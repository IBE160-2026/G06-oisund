import { test, expect, openedPlan, API, post, randomUUID, beforeUnload, setup, activityStatus, shiftStatus, activityScreen, python } from './private-activity-helpers';
import { editor } from './private-screen-helpers';
setup();

async function uncertainCommand(page: any, context: any, resource: 'selection' | 'start' | 'physical-bus' | 'outcome') {
  const { plan } = await openedPlan(page, context);
  if (resource === 'outcome') {
    await page.getByRole('button', { name: 'Start skift', exact: true }).click();
    await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
    await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
    await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
    await activityScreen(page);
  }
  const path = '/workdays/' + plan.id + '/' + resource;
  let original: any, writes = 0;
  await page.route('**:8001' + path, async (route: any) => {
    if (route.request().method() !== 'POST') return route.continue();
    writes++; original = route.request().postDataJSON(); await route.fetch(); await route.abort();
  });
  if (resource === 'physical-bus') {
    await page.getByRole('textbox', { name: 'Fysisk buss', exact: true }).fill('Synthetic uncertain bus');
    await page.getByRole('button', { name: 'Lagre fysisk buss', exact: true }).click();
  } else if (resource === 'outcome') {
    await page.getByLabel('Manuell aktivitetsstatus', { exact: true }).selectOption('interrupted');
    await page.getByRole('button', { name: 'Lagre aktivitetsstatus', exact: true }).click();
  } else {
    await page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true }).click();
    if (resource === 'start') await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  }
  const check = page.getByRole('button', { name: { selection: 'Kontroller aktivitetsvalget', start: 'Kontroller skiftstarten', 'physical-bus': 'Kontroller busslagringen', outcome: 'Kontroller aktivitetsstatusen' }[resource], exact: true });
  await expect(check).toBeEnabled();
  return { plan, check, original, writes: () => writes, lookup: '/workday-' + (resource === 'physical-bus' ? 'bus' : resource) + '-operations/' + original.operation_id };
}

for (const resource of ['selection', 'start']) for (const automaticRead of ['failed', 'successful']) test(`D1 canonical ${resource} rejection retains cancellation through repeated failed refreshes after ${automaticRead} automatic read`, async ({ page, context }, testInfo) => {
  const { plan } = await openedPlan(page, context);
  const path = '/workdays/' + plan.id + '/' + resource;
  const read = '/workdays/' + plan.id + '/' + (resource === 'start' ? 'lifecycle' : resource);
  let writes = 0, failCurrent = automaticRead === 'failed';
  await page.route('**:8001' + path, route => {
    if (route.request().method() !== 'POST') return failCurrent ? route.fulfill({ status: 503, json: { detail: 'Tjenesten er utilgjengelig.' } }) : route.continue();
    writes++; return route.fulfill({ status: 429, json: { detail: { code: resource + '_receipt_capacity', message: 'For mange lagringsforsøk. Vent til tidligere planer utløper.' } } });
  });
  if (resource === 'start') await page.route('**:8001' + read, route => failCurrent ? route.fulfill({ status: 503, json: { detail: 'Tjenesten er utilgjengelig.' } }) : route.continue());
  await page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true }).click();
  if (resource === 'start') await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  const status = resource === 'selection' ? activityStatus(page) : shiftStatus(page);
  await expect(status).toContainText('avvist');
  await expect(page.getByRole('button', { name: resource === 'selection' ? 'Kontroller aktivitetsvalget' : 'Kontroller skiftstarten', exact: true })).toHaveCount(0);
  const cancel = page.getByRole('button', { name: resource === 'selection' ? 'Avbryt avvist aktivitetsvalg' : 'Avbryt avvist skiftstart', exact: true });
  const retry = page.getByRole('button', { name: resource === 'selection' ? 'Prøv avvist aktivitetsvalg igjen' : 'Prøv avvist skiftstart igjen', exact: true });
  const refresh = page.getByRole('button', { name: resource === 'selection' ? 'Kontroller plantilgang og aktivitetsvalg' : 'Hent skiftstatus igjen', exact: true });
  await expect(cancel).toBeEnabled();
  failCurrent = true;
  for (let attempt = 0; attempt < 2; attempt++) {
    const response = page.waitForResponse(reply => reply.url().endsWith(read) && reply.request().method() === 'GET');
    await refresh.click(); await (await response).finished(); await expect(refresh).toBeEnabled();
    await expect(cancel).toBeEnabled(); await expect(retry).toBeDisabled();
    await expect(page.getByText(resource === 'selection' ? 'Lagret aktivitetsvalg kan ikke bekreftes.' : 'Skiftstatus er ukjent / utilgjengelig', { exact: true })).toBeVisible();
    await expect.poll(() => beforeUnload(page)).toBe(true);
  }
  await page.screenshot({ path: testInfo.outputPath(resource + '-rejected-unavailable.png'), fullPage: true });
  failCurrent = false;
  await refresh.click(); await expect(status).toContainText('Det avviste forslaget er beholdt');
  await expect(cancel).toBeEnabled(); await expect.poll(() => beforeUnload(page)).toBe(true);
  if (resource === 'selection') await expect(page.getByText(/^Lokalt forslag/)).toBeVisible();
  await cancel.click();
  await expect.poll(() => beforeUnload(page)).toBe(false); expect(writes).toBe(1);
});

for (const resource of ['selection', 'start']) for (const refusal of [429, 409]) test(`D1 accepted ${resource} lost reply retains original after typed lookup ${refusal}`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context);
  const path = '/workdays/' + plan.id + '/' + resource;
  let original: any, writes = 0;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() !== 'POST') return route.continue();
    writes++; original = route.request().postDataJSON(); await route.fetch(); await route.abort();
  });
  await page.getByRole('button', { name: resource === 'selection' ? 'Velg aktivitet 1' : 'Start skift', exact: true }).click();
  if (resource === 'start') await page.getByRole('button', { name: 'Bekreft skiftstart', exact: true }).click();
  const check = page.getByRole('button', { name: resource === 'selection' ? 'Kontroller aktivitetsvalget' : 'Kontroller skiftstarten', exact: true });
  await expect(check).toBeEnabled();
  const lookupPath = '/workday-' + resource + '-operations/' + original.operation_id;
  await page.route('**:8001' + lookupPath, route => route.fulfill({ status: refusal, json: { detail: refusal === 429
    ? { code: resource + '_receipt_capacity', message: 'For mange lagringsforsøk. Vent til tidligere planer utløper.' }
    : resource === 'selection' ? 'Aktivitetsvalget er endret. Sammenlign med lagret verdi.' : 'Skiftstatusen er endret. Last inn lagret status.' } }));
  const lookup = page.waitForResponse(reply => reply.url().endsWith(lookupPath));
  await page.getByRole('button', { name: resource === 'selection' ? 'Prøv samme aktivitetsvalg igjen' : 'Prøv samme skiftstart igjen', exact: true }).click();
  await (await lookup).finished(); await expect(check).toBeEnabled();
  await expect(page.getByRole('button', { name: resource === 'selection' ? 'Avbryt avvist aktivitetsvalg' : 'Avbryt avvist skiftstart', exact: true })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Last inn lagret aktivitetsvalg', exact: true })).toHaveCount(0);
  await expect.poll(() => beforeUnload(page)).toBe(true); expect(writes).toBe(1);
  await page.unroute('**:8001' + lookupPath);
  const recovered = page.waitForRequest(request => request.url().endsWith(lookupPath));
  await check.click(); await recovered;
  await expect(resource === 'selection' ? activityStatus(page) : shiftStatus(page)).toHaveText(resource === 'selection' ? 'Aktivitetsvalget er lagret.' : 'Skiftstart er lagret.');
  await expect.poll(() => beforeUnload(page)).toBe(false); expect(writes).toBe(1);
  expect((await (await context.request.get(API + lookupPath)).json()).operation_id).toBe(original.operation_id);
});

test('D1 wrong identity conflict comparison preserves local proposal without B facts', async ({ page, context }) => {
  const { draft } = await openedPlan(page, context);
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await page.getByRole('button', { name: 'Oppdater listen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne 2031-01-02 · versjon 1', exact: true }).click(); await editor(page);
  await page.getByLabel('Vognløp', { exact: true }).fill('local-proposal-A');
  const path = '/drafts/' + draft.id;
  await page.route('**:8001' + path, route => route.request().method() === 'POST'
    ? route.fulfill({ status: 409, json: { detail: 'Utkastet er endret. Sammenlign med lagret versjon før du fortsetter.' } })
    : route.fulfill({ status: 200, json: { ...draft, id: randomUUID(), revision: 2, draft: { ...draft.draft, vehicle_duty: 'PRIVATE-B-FACT' } } }));
  await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Lagringsstatus', exact: true })).toContainText('Konflikt');
  await expect(page.getByText('PRIVATE-B-FACT', { exact: true })).toHaveCount(0);
  await expect(page.getByRole('region', { name: 'Sammenlign versjoner' })).toHaveCount(0);
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('local-proposal-A');
});

test('D1 source folds display authoritative supplied offsets', async ({ page, context }, testInfo) => {
  await openedPlan(page, context, false, undefined, undefined, false, content => {
    content.service_date = '2030-10-27';
    content.activities = [{ ...content.activities[0], start: '2030-10-27T02:00:00+02:00', end: '2030-10-27T03:00:00+01:00' }];
  });
  const originals: any[] = [];
  for (const [offset, title] of [['+02:00', 'First fold'], ['+01:00', 'Second fold']]) {
    const operation = (await post(context, '/notice-operations', {})).operation_id;
    const receipt = await post(context, '/notices', { operation_id: operation, expected_revision: 0,
      content: { title, line_scope: 'all', line_tags: [], source_updated_at: '2030-10-27T02:30:00' + offset, valid_from: '2030-10-27T02:30:00+02:00', valid_until: '2030-10-27T02:30:00+01:00', source_url: null } });
    originals.push({ operation, receipt });
  }
  await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
  for (const view of ['maintenance', 'reader']) {
    if (view === 'reader') {
      await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
      await page.getByRole('button', { name: 'Les avvik for linjer og datoer', exact: true }).click();
    }
    for (const [offset, title] of [['+02:00', 'First fold'], ['+01:00', 'Second fold']]) {
      const item = page.locator('.notice-list li:visible').filter({ hasText: title }); await item.locator('summary').click();
      await expect(item).toContainText('Kilden oppdatert: 27.10.2030, 02:30:00 (UTC' + offset + ')');
      await expect(item).toContainText('Gyldighet: fra 27.10.2030, 02:30:00 (UTC+02:00) til 27.10.2030, 02:30:00 (UTC+01:00)');
    }
    await page.screenshot({ path: testInfo.outputPath('folds-' + view + '.png'), fullPage: true });
  }
  for (const { operation, receipt } of originals) {
    expect(await (await context.request.get(API + '/notices/' + receipt.result.id)).json()).toEqual(receipt.result);
    expect(await (await context.request.get(API + '/workday-notice-operations/' + operation)).json()).toEqual(receipt);
  }
});

test('D1 explicit abandonment checks disappearance and preserves account notices', async ({ page, context }, testInfo) => {
  const { plan } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/selection'; let writes = 0, original: any;
  await post(context, '/notices', { operation_id: (await post(context, '/notice-operations', {})).operation_id, expected_revision: 0,
    content: { title: 'Independent retained notice', line_scope: 'all', line_tags: [], source_updated_at: null, valid_from: null, valid_until: '2031-01-04T23:59:59+01:00', source_url: null } });
  await page.route('**:8001' + path, async route => { if (route.request().method() !== 'POST') return route.continue(); writes++; original = route.request().postDataJSON(); await route.fetch(); await route.abort(); });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true })).toBeEnabled();
  const abandon = page.getByRole('button', { name: 'Oppgi uavklart forsøk og lukk planen', exact: true });
  let prematureDialogs = 0;
  const denyDialog = async (dialog: any) => { prematureDialogs++; await dialog.dismiss(); };
  page.on('dialog', denyDialog);
  // A transient current read must retain the uncertain operation and locks.
  for (const response of [
    { status: 503, json: { detail: 'Tjenesten er utilgjengelig.' } },
    { status: 200, contentType: 'text/html', body: '<html>unavailable</html>' },
    { status: 404, contentType: 'text/html', body: '<html>unavailable</html>' },
    { status: 404, json: { detail: 'wrong detail' } },
  ]) {
    await page.route('**:8001/workdays/' + plan.id, route => route.fulfill(response));
    const refused = page.waitForResponse(reply => reply.url().endsWith('/workdays/' + plan.id));
    await abandon.click(); await (await refused).finished();
    await expect(abandon).toBeEnabled();
    await expect.poll(() => beforeUnload(page)).toBe(true);
    await expect(page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true })).toBeEnabled();
    await page.unroute('**:8001/workdays/' + plan.id);
    expect(prematureDialogs).toBe(0);
  }
  page.off('dialog', denyDialog);
  await post(context, '/workdays/' + plan.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
  const dismissDialog = page.waitForEvent('dialog');
  const dismissAttempt = abandon.click();
  await (await dismissDialog).dismiss(); await dismissAttempt;
  await expect(abandon).toBeEnabled();
  await expect.poll(() => beforeUnload(page)).toBe(true);
  await page.screenshot({ path: testInfo.outputPath('abandonment-before-confirmation.png'), fullPage: true });
  const lookup = page.waitForRequest(request => request.url().endsWith('/workday-selection-operations/' + original.operation_id));
  await page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true }).click(); await lookup;
  await expect(page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true })).toBeEnabled();
  const acceptDialog = page.waitForEvent('dialog');
  const acceptAttempt = abandon.click();
  await (await acceptDialog).accept(); await acceptAttempt;
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  await expect.poll(() => beforeUnload(page)).toBe(false); expect(writes).toBe(1);
  await page.screenshot({ path: testInfo.outputPath('abandonment-after-confirmation.png'), fullPage: true });
  expect((await (await context.request.get(API + '/notices')).json()).notices.map((n: any) => n.title)).toContain('Independent retained notice');
});

for (const fault of ['second-read', 'second-session-503', 'second-session-401']) test(`D1 abandonment ${fault} cannot pass the post-confirmation safeguard`, async ({ page, context }) => {
  const command = await uncertainCommand(page, context, 'selection');
  await post(context, '/workdays/' + command.plan.id + '/delete', { operation_id: randomUUID(), source_revision: 1 });
  let reads = 0, failSession = false;
  await page.route('**:8001/workdays/' + command.plan.id, route => {
    reads++;
    if (reads === 2 && fault === 'second-read') return route.fulfill({ status: 503, json: { detail: 'Tjenesten er utilgjengelig.' } });
    if (reads === 2) failSession = true;
    return route.fulfill({ status: 404, json: { detail: 'Tilgangen ble avvist.' } });
  });
  if (fault !== 'second-read') await page.route('**:8001/auth/session', route => failSession
    ? route.fulfill({ status: fault === 'second-session-401' ? 401 : 503, json: { detail: 'Tjenesten er utilgjengelig.' } }) : route.continue());
  const abandon = page.getByRole('button', { name: 'Oppgi uavklart forsøk og lukk planen', exact: true });
  const dialog = page.waitForEvent('dialog'), action = abandon.click();
  await (await dialog).accept(); await action;
  if (fault === 'second-session-401') {
    await expect(page.getByRole('heading', { name: 'Logg inn', exact: true })).toBeVisible();
    await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
    await expect.poll(() => beforeUnload(page)).toBe(false);
  } else {
    if (fault === 'second-session-503') {
      const restore = page.getByRole('button', { name: 'Kontroller tilgang igjen', exact: true });
      await expect(restore).toBeEnabled();
      await expect.poll(() => beforeUnload(page)).toBe(true);
      await page.unroute('**:8001/auth/session');
      await restore.click();
    }
    await expect(abandon).toBeEnabled();
    await expect.poll(() => beforeUnload(page)).toBe(true);
    await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeDisabled();
    await expect(command.check).toBeEnabled();
    const lookup = page.waitForResponse(response => response.url().endsWith(command.lookup));
    await command.check.click(); await (await lookup).finished(); await expect(command.check).toBeEnabled();
    await expect.poll(() => beforeUnload(page)).toBe(true);
  }
  expect(reads).toBeGreaterThanOrEqual(2); expect(command.writes()).toBe(1);
  await expect(page.getByText('Den bortfalte planen er lukket. Lokale planforsøk er oppgitt uten bekreftet lagring. Avviksregisteret er beholdt.', { exact: true })).toHaveCount(0);
});

for (const resource of ['physical-bus', 'start', 'outcome'] as const) test(`D1 server410 abandonment releases distinct ${resource} parent lock without another write`, async ({ page, context }) => {
  const command = await uncertainCommand(page, context, resource);
  await expect.poll(() => beforeUnload(page)).toBe(true);
  python(`with database() as conn:\n conn.execute("UPDATE workdays SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (${JSON.stringify(command.plan.id)},))\n`);
  const abandon = page.getByRole('button', { name: 'Oppgi uavklart forsøk og lukk planen', exact: true });
  const firstDenial = page.waitForResponse(response => response.url().endsWith('/workdays/' + command.plan.id) && response.status() === 410);
  const dialog = page.waitForEvent('dialog'), action = abandon.click();
  await firstDenial; await (await dialog).accept(); await action;
  await expect(page.getByRole('region', { name: 'Bekreftet plan', exact: true })).toHaveCount(0);
  await expect.poll(() => beforeUnload(page)).toBe(false); expect(command.writes()).toBe(1);
  await expect(page.getByRole('status', { name: 'Bekreftelsesstatus', exact: true })).toContainText('uten bekreftet lagring');
});
