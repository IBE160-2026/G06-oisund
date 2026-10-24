import { test, expect, openedPlan, API, post, randomUUID, selected, activityStatus, shiftStatus, beforeUnload, reopen, setup } from './private-activity-helpers';
import { writeFileSync } from 'node:fs';
setup();

test('direct previous next exact stable members equal times pauses gaps midnight and reload', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context);
  await expect(page.getByRole('button', { name: 'Velg en aktivitet først', exact: true })).toHaveCount(2);
  await expect(page.getByRole('button', { name: 'Velg aktivitet 1', exact: true })).toHaveText('Velg aktivitet 1');
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(activityStatus(page)).toHaveText('Aktivitetsvalget er lagret.');
  const firstChoice = page.getByRole('button', { name: 'Velg aktivitet 1', exact: true });
  await expect(firstChoice).toHaveAccessibleDescription(/Passasjertur.*Linje: 20.*Retning: Nord.*02.01.2031/);
  await expect(firstChoice).toHaveAttribute('aria-current', 'true');
  await expect(page.locator('.day-member [aria-current="true"]')).toHaveCount(1);
  await expect(activityStatus(page)).toBeFocused();
  await expect(selected(page)).toContainText('Linje: 20'); await expect(selected(page)).toContainText('Retning: Nord');
  await expect(page.getByRole('button', { name: 'Ingen forrige aktivitet', exact: true })).toBeDisabled();
  let writes = 0; page.on('request', req => { if (req.url().endsWith('/selection') && req.method() === 'POST') writes++; });
  await expect(page.getByRole('button', { name: 'Velg aktivitet 1', exact: true })).toBeDisabled(); expect(writes).toBe(0);
  for (let i = 1; i < activities.length; i++) {
    await page.getByRole('button', { name: 'Neste aktivitet', exact: true }).click();
    await expect(activityStatus(page)).toHaveText('Aktivitetsvalget er lagret.');
    expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).activity_id).toBe(activities[i].id);
  }
  await expect(selected(page)).toContainText('03.01.2031'); await expect(page.getByRole('button', { name: 'Ingen neste aktivitet', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: 'Forrige aktivitet', exact: true }).click(); await expect(selected(page)).toContainText('Matpause');
  await page.getByText('Vis 2 pauserader', { exact: true }).click();
  await expect(page.locator('[data-activity-id="' + activities[3].id + '"]').getByText('Manuelt valgt aktivitet', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Velg aktivitet 3', exact: true }).click(); await expect(selected(page)).toContainText('Kaffepause');
  await reopen(page); await expect(selected(page)).toContainText('Kaffepause');
  await page.reload(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click(); await expect(selected(page)).toContainText('Kaffepause');
  await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
});

test('identical facts equal times still identify the exact selected member ordinal', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context, false, undefined, undefined, true);
  for (const index of [0, 1]) {
    await page.getByRole('button', { name: `Velg aktivitet ${index + 1}`, exact: true }).click();
    await expect(selected(page)).toContainText(`Aktivitet ${index + 1} av 5`);
    const current = page.locator('.day-member [aria-current="true"]');
    await expect(current).toHaveCount(1); await expect(current).toHaveAccessibleName(`Velg aktivitet ${index + 1}`);
    expect(await current.evaluate(el => el.closest('[data-activity-id]')?.getAttribute('data-activity-id'))).toBe(activities[index].id);
    expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).activity_id).toBe(activities[index].id);
  }
  await reopen(page); await expect(selected(page)).toContainText('Aktivitet 2 av 5');
});

for (const resource of ['selection', 'lifecycle']) for (const phase of ['initial', 'refreshed']) test(`malformed ${phase} current ${resource} records never establish authority`, async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context);
  const path = '/workdays/' + plan.id + '/' + resource;
  await post(context, '/workdays/' + plan.id + (resource === 'selection' ? '/selection' : '/start'), {
    operation_id: randomUUID(), expected_revision: 0, ...(resource === 'selection' ? { activity_id: activities[0].id } : {}),
  });
  const original = await (await context.request.get(API + path)).json();
  const faults = [{ ...original, workday_id: randomUUID() }, { ...original, expires_at: new Date(Date.parse(original.expires_at) + 1000).toISOString() },
    ...(resource === 'selection' ? [{ ...original, activity_id: randomUUID() }, { ...original, revision: 0 }]
      : [{ ...original, state: 'confirmed' }, { ...original, started_at: null }, { ...original, started_at: 'not-a-time' }])];
  const refresh = page.getByRole('button', { name: resource === 'selection' ? 'Kontroller plantilgang og aktivitetsvalg' : 'Hent skiftstatus igjen', exact: true });
  for (const faulty of faults) {
    if (phase === 'initial') await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
    else { await refresh.click(); await expect(resource === 'selection' ? selected(page) : page.getByText('Startet manuelt', { exact: true })).toBeVisible(); }
    await page.route('**:8001' + path, route => route.fulfill({ status: 200, json: faulty }));
    if (phase === 'initial') await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
    else await refresh.click();
    if (resource === 'selection') {
      await expect(page.getByText('Lagret aktivitetsvalg kan ikke bekreftes.', { exact: true })).toBeVisible();
      await expect(selected(page)).toHaveCount(0); await expect(page.locator('.day-member [aria-current="true"]')).toHaveCount(0);
      await expect(activityStatus(page)).not.toHaveText('Aktivitetsvalget er lagret.');
    } else {
      await expect(page.getByText('Skiftstatus er ukjent / utilgjengelig', { exact: true })).toBeVisible();
      await expect(page.getByText('Startet manuelt', { exact: true })).toHaveCount(0); await expect(page.getByRole('button', { name: 'Start skift', exact: true })).toHaveCount(0);
      await expect(shiftStatus(page)).not.toHaveText('Skiftstart er lagret.');
    }
    await page.unroute('**:8001' + path);
  }
});

test('stale proposal explicit comparison and accepted older receipt preserve newer choice', async ({ page, context }) => {
  const { plan, activities } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/selection';
  await post(context, path, { operation_id: randomUUID(), expected_revision: 0, activity_id: activities[1].id });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(activityStatus(page)).toContainText('endret i et annet vindu');
  await expect(page.getByText(/^Lokalt forslag/)).toContainText('Linje: 20');
  await expect(page.getByText(/^Gjeldende lagret valg/)).toContainText('Linje: 24');
  await page.getByRole('button', { name: 'Last inn lagret aktivitetsvalg', exact: true }).click(); await expect(selected(page)).toContainText('Linje: 24');
  await expect(activityStatus(page)).toHaveText('Lagret aktivitetsvalg er lastet inn. Det lokale forslaget er fjernet.');
  await expect(activityStatus(page)).toBeFocused(); await expect(page.getByText(/^Lokalt forslag/)).toHaveCount(0);
  let original: any;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() !== 'POST') return route.continue();
    original = route.request().postDataJSON(); await route.fetch();
    await post(context, path, { operation_id: randomUUID(), expected_revision: 2, activity_id: activities[4].id });
    await route.fulfill({ status: 200, contentType: 'text/html', body: '<html>lost</html>' });
  });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true })).toBeEnabled();
  await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(true);
  await page.unroute('**:8001' + path); await page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true }).click();
  await expect(activityStatus(page)).toContainText('Forsøket ble lagret. Et nyere');
  expect((await (await context.request.get(API + path)).json()).activity_id).toBe(activities[4].id);
  await page.getByRole('button', { name: 'Last inn lagret aktivitetsvalg', exact: true }).click(); await expect(selected(page)).toContainText('03.01.2031');
  await expect(activityStatus(page)).toHaveText('Lagret aktivitetsvalg er lastet inn. Det lokale forslaget er fjernet.');
  await expect(activityStatus(page)).toBeFocused(); await expect(page.getByText(/^Lokalt forslag/)).toHaveCount(0);
  expect((await (await context.request.get(API + '/workday-selection-operations/' + original.operation_id)).json()).result.activity_id).toBe(activities[0].id);
});

test('selected non-passenger labels preserve applicable identifiers and visible grouped member identity', async ({ page, context }) => {
  await openedPlan(page, context, false, undefined, 'Sign-on');
  const signOn = page.locator('.day-member').first();
  await expect(signOn).not.toContainText(/Linje:|Tur:|Retning:/);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(selected(page)).toContainText('Oppmøte'); await expect(selected(page)).toContainText('Planlagt start:');
  await expect(selected(page)).not.toContainText(/Linje:|Tur:|Retning:/);
  await page.getByText('Vis 2 pauserader', { exact: true }).click();
  await page.getByRole('button', { name: 'Velg aktivitet 4', exact: true }).click(); await expect(selected(page)).toContainText('Matpause');
  await expect(selected(page)).not.toContainText(/Linje:|Tur:|Retning:/);
  await page.getByText('Vis 2 pauserader', { exact: true }).click();
  await expect(page.getByText('Manuelt valgt aktivitet i denne pausegruppen: aktivitet 4.', { exact: true })).toBeVisible();
});

for (const reply of ['lost', 'html', 'malformed']) test(`uncertain ${reply} choice retains original operation and aggregate bus lock`, async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/selection'; let original: any;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() !== 'POST') return route.continue(); original = route.request().postDataJSON(); await route.fetch();
    if (reply === 'lost') return route.abort();
    await route.fulfill(reply === 'html' ? { status: 200, contentType: 'text/html', body: '<html>lost</html>' } : { status: 200, json: { operation_id: original.operation_id, result: {} } });
  });
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await expect(activityStatus(page)).toContainText('uavklart');
  await expect(page.getByRole('button', { name: 'Kontroller aktivitetsvalget', exact: true })).toBeEnabled();
  await expect(selected(page)).toHaveCount(0); await expect(page.getByRole('button', { name: 'Velg aktivitet 2', exact: true })).toBeDisabled();
  const bus = page.getByRole('region', { name: 'Fysisk buss', exact: true }).getByLabel('Fysisk buss', { exact: true });
  await bus.fill('other guard'); await page.getByRole('button', { name: 'Avbryt bussendring', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Lukk planen', exact: true })).toBeDisabled(); await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(true);
  await page.unroute('**:8001' + path); let retry: any;
  page.on('request', req => { if (req.url().endsWith(path) && req.method() === 'POST') retry = req.postDataJSON(); });
  await page.getByRole('button', { name: 'Prøv samme aktivitetsvalg igjen', exact: true }).click(); await expect(selected(page)).toContainText('Linje: 20'); expect(retry).toEqual(original);
  await expect.poll(() => beforeUnload(page), { timeout: 5000 }).toBe(false);
});

test('denial in one resource cannot be unhidden by another and recovers deliberately', async ({ page, context }) => {
  const { plan } = await openedPlan(page, context); const path = '/workdays/' + plan.id + '/selection'; let denied = true;
  await page.route('**:8001' + path, async route => {
    if (route.request().method() === 'GET' && denied) return route.fulfill({ status: 404, json: { detail: 'synthetic denial' } });
    return route.continue();
  });
  await page.getByRole('button', { name: 'Kontroller plantilgang og aktivitetsvalg', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
  await page.getByRole('button', { name: 'Hent skiftstatus igjen', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toHaveCount(0);
  await expect(page.getByText('Ikke startet', { exact: true })).toHaveCount(0);
  denied = false; await page.getByRole('button', { name: 'Kontroller plantilgang og aktivitetsvalg', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
});

for (const width of [768, 1440]) for (const night of [false, true]) test(`selection start keyboard long labels enlarged ${width} ${night ? 'Night' : 'Day'}`, async ({ page, context }) => {
  await page.setViewportSize({ width, height: 1100 }); const { plan } = await openedPlan(page, context);
  if (night) await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
  await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
  const choose = page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }); await choose.focus(); await page.keyboard.press('Enter');
  await expect(selected(page)).toContainText('Linje: 20');
  await page.getByRole('button', { name: 'Start skift', exact: true }).click(); await expect(shiftStatus(page)).toHaveText('Skiftstart er lagret.');
  await expect(shiftStatus(page)).toBeFocused();
  await expect(page.getByText('Startet manuelt', { exact: true })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  const control = page.getByRole('button', { name: 'Neste aktivitet', exact: true }); await control.focus();
  expect(await control.evaluate(el => el.getBoundingClientRect().height)).toBeGreaterThanOrEqual(58);
  await page.getByRole('region', { name: 'Bekreftet plan', exact: true }).screenshot({ path: `../docs/evidence/11-1-selection-${width}-${night ? 'night' : 'day'}.png` });
  expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
});

test('rendered selector start markers boundaries and focus meet IR-01 in both themes', async ({ page, context }) => {
  await openedPlan(page, context);
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click(); await expect(selected(page)).toBeVisible();
  const measurements: object[] = [];
  for (const night of [false, true]) {
    if (night) await page.getByRole('button', { name: 'Nattmodus', exact: true }).click();
    const measured = await page.getByRole('region', { name: 'Bekreftet plan', exact: true }).evaluate(element => {
      const rgb = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number);
      const light = (v: string) => rgb(v).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((s, c, i) => s + c * [.2126, .7152, .0722][i], 0);
      const ratio = (a: string, b: string) => (Math.max(light(a), light(b)) + .05) / (Math.min(light(a), light(b)) + .05);
      const background = (el: Element): string => { const color = getComputedStyle(el).backgroundColor; return color === 'rgba(0, 0, 0, 0)' || color === 'transparent' ? el.parentElement ? background(el.parentElement) : 'rgb(255,255,255)' : color; };
      const text = [...element.querySelectorAll('.private-activity-selection p, .private-shift-start p, .activity-selection-marker, .private-activity-selection button, .private-shift-start button, .day-member button')].map(el => ratio(getComputedStyle(el).color, background(el)));
      const boundaries = [...element.querySelectorAll('.private-activity-selection, .private-shift-start, .selected-activity')].map(el => ratio(getComputedStyle(el).borderLeftColor, background(el.parentElement!)));
      const direct = [...element.querySelectorAll<HTMLButtonElement>('.day-member button')].slice(0, 2).map(el => ({ disabled: el.disabled, current: el.getAttribute('aria-current'), text: ratio(getComputedStyle(el).color, background(el)), boundary: ratio(getComputedStyle(el).borderLeftColor, background(el.parentElement!)), height: el.getBoundingClientRect().height }));
      return { text: Math.min(...text), boundary: Math.min(...boundaries), direct };
    });
    expect(measured.text).toBeGreaterThanOrEqual(4.5); expect(measured.boundary).toBeGreaterThanOrEqual(3);
    expect(measured.direct.map(v => v.disabled)).toEqual([true, false]); expect(measured.direct[0].current).toBe('true');
    for (const direct of measured.direct) { expect(direct.text).toBeGreaterThanOrEqual(4.5); expect(direct.boundary).toBeGreaterThanOrEqual(3); expect(direct.height).toBeGreaterThanOrEqual(58); }
    for (const name of ['Neste aktivitet', 'Start skift', 'Velg aktivitet 2']) {
      const button = page.getByRole('button', { name, exact: true }); await page.keyboard.press('Tab'); await button.focus();
      const focus = await button.evaluate(el => {
        const rgb = (v: string) => (v.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number);
        const light = (v: string) => rgb(v).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((s, c, i) => s + c * [.2126, .7152, .0722][i], 0);
        const style = getComputedStyle(el); let ancestor = el.parentElement!;
        while (getComputedStyle(ancestor).backgroundColor === 'rgba(0, 0, 0, 0)' && ancestor.parentElement) ancestor = ancestor.parentElement;
        const a = light(style.outlineColor), b = light(getComputedStyle(ancestor).backgroundColor);
        return { width: parseFloat(style.outlineWidth), ratio: (Math.max(a, b) + .05) / (Math.min(a, b) + .05) };
      });
      expect(focus.width).toBeGreaterThanOrEqual(2); expect(focus.ratio).toBeGreaterThanOrEqual(3);
      measurements.push({ theme: night ? 'Night' : 'Day', control: name, ...measured, focus });
      await test.info().attach(`11-1-${night ? 'night' : 'day'}-${name}`, { body: JSON.stringify({ ...measured, focus }), contentType: 'application/json' });
    }
  }
  writeFileSync('../docs/evidence/11-1-contrast.json', JSON.stringify(measurements, null, 2) + '\n');
});

test('single member has both disabled boundaries and no clock-driven selection', async ({ page, context }) => {
  await page.clock.install(); const { plan, activities } = await openedPlan(page, context, true, 30);
  await expect(page.getByText('Ingen aktivitet valgt', { exact: true })).toBeVisible(); await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
  await expect(selected(page)).toBeVisible();
  await page.clock.fastForward(120000);
  await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Ingen forrige aktivitet', exact: true })).toBeDisabled(); await expect(page.getByRole('button', { name: 'Ingen neste aktivitet', exact: true })).toBeDisabled();
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/lifecycle')).json()).state).toBe('confirmed');
  expect((await (await context.request.get(API + '/workdays/' + plan.id + '/selection')).json()).activity_id).toBe(activities[0].id);
});
