const d=require('./driver.cjs');const {expect}=d;const {readFileSync,writeFileSync}=d.fs;const {execFileSync}=d.cp;const API=d.API;const account=d.state();const cases=[];function test(name,fn){cases.push({name,fn})};test.use=()=>{};test.setTimeout=()=>{};test.step=(name,fn)=>d.record('Physical journey A: '+name,fn).then(row=>row.result);const selected=p=>p.locator('.selected-activity');const shiftStatus=p=>p.getByRole('status',{name:'Skiftstatus'});async function dayScreen(p){const b=p.getByRole('button',{name:'Tilbake til dagen',exact:true});if(await b.isVisible())await b.click();}async function activityScreen(p){if(!await selected(p).isVisible())await p.getByRole('button',{name:'Åpne valgt aktivitet',exact:true}).click();await expect(selected(p)).toBeVisible();}



                                                             


// Headed desktop automation proves real tab focus. Visibility lifecycle is
// exercised separately: this runtime keeps background tabs visible.

// Authored independently of the parser. Never regenerate these facts from an import.
const oracle = JSON.parse(readFileSync('Eksempelfiler/Fasit-testskift.json', 'utf8').replace(/^\uFEFF/, '')).shifts;
const button = (page      , name        ) => page.getByRole('button', { name, exact: true });
function assertWinterInstant(actual               , local               ) {
  if (local === null) { expect(actual).toBeNull(); return; }
  // These independent fixtures are in February, explicitly UTC+01:00 in Oslo.
  // Do not let host timezone or the parser supply the expected UTC instant.
  expect(actual).toMatch(/(?:Z|[+-]\d{2}:\d{2})$/);
  expect(Date.parse(actual )).toBe(Date.parse(local + ':00+01:00'));
}
async function json(context                , path        ) {
  const response = await context.request.get(API + path); expect(response.status()).toBe(200); return response.json();
}
async function login(page) { await expect(button(page,'Bruk som separat nytt utkast')).toBeVisible(); }
async function importAndSave(page      , context                , name        ) {
  const expected = oracle.find((value     ) => value.case === name);
  const events = expected.events.filter((value     ) => value.kind !== 'vehicle');
  const pdfBytes = readFileSync('Eksempelfiler/Testskift-' + name + '.pdf');
  let imported;
  if(name === 'A') imported=JSON.parse(readFileSync('docs/evidence/12-4-device-20261028/import-A.json','utf8'));
  else {
  const response = page.waitForResponse(r => r.url() === API + '/imports/pdf' && r.request().method() === 'POST');
  await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles('Eksempelfiler/Testskift-' + name + '.pdf');
  const result = await response; expect(result.status()).toBe(200);

  expect(result.request().postDataBuffer()).toEqual(pdfBytes);
  imported = await result.json();
  }
  const serviceDate = expected.date.split('/').reverse().join('-');
  expect(imported.service_date).toBe(serviceDate);
  expect(imported.import_metadata.header.service_date).toBe(serviceDate);
  expect(imported.import_metadata.header.shift_id).toBe(expected.shift_id);
  await expect(button(page, 'Bruk som separat nytt utkast')).toBeVisible();
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
  expect(imported.vehicle_duty).toBe(expected.events.find((event     ) => event.kind === 'vehicle').vehicle);
  expect(imported.physical_bus).toBeNull();
  await button(page, 'Bruk som separat nytt utkast').click();
  const tripIndex = events.findIndex((event     ) => event.passenger_service);
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


(async()=>{const{page,browser}=await d.connect();const real=page.context();const context={newPage:()=>real.newPage(),newCDPSession:p=>real.newCDPSession(p),request:{get:async url=>{const value=await page.evaluate(async url=>{const r=await fetch(url,{credentials:'include',cache:'no-store'});return{status:r.status,body:await r.json()};},url);return{status:()=>value.status,json:async()=>value.body};}}};const rows=d.fs.readFileSync(d.path.join(d.out,'checks.ndjson'),'utf8').trim().split('\n').map(JSON.parse);const a=rows.find(r=>r.passed&&r.name.includes('Import A with exact bytes')).result;const c=rows.find(r=>r.passed&&r.name.includes('Import C with midnight facts')).result;const chosen=a,name='A',action='ended';const item=(await d.get(page,'/workdays')).workdays.find(p=>p.source_draft_id===a.saved.id);const plan=await d.get(page,'/workdays/'+item.id);const notices=(await d.get(page,'/notices')).notices;const visibility=await page.evaluate(()=>window.__story124Visibility),focus=await page.evaluate(()=>window.__story124Focus);await d.expect(selected(page)).toBeVisible();await d.expect(selected(page)).toContainText('Syntetisk manuelt korrigert endeholdeplass');process.env.COMPOSE_PROJECT_NAME='ibe160-story124-tests';await d.record('Physical A continuation: explicit start outcome end database restart and saved recap reload',async()=>{
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
    expect(recap.outcomes.outcomes.map((row     ) => row.outcome)).toEqual(chosen.saved.draft.activities.map((_     , i        ) => i === chosen.tripIndex ? action === 'ended' ? 'completed' : 'interrupted' : 'unregistered'));
    expect(recap.bus.physical_bus).toBe('SYN-124');
    if (name === 'A') {
      if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-story124-tests') throw Error('Disposable project selection required');
      await test.step('Restart actual database and API and verify fixed records', async () => {
        const compose = ['compose', '-p', 'ibe160-story124-tests', '-f', 'compose.story124.yaml'];
        for (const service of ['private-db', 'private-api']) {
          execFileSync('docker', [...compose, 'restart', service], { cwd: '.', timeout: 30000 });
          execFileSync('docker', [...compose, 'start', '--wait', '--wait-timeout', '45', service], { cwd: '.', timeout: 60000 });
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
    await page.screenshot({ path: `docs/evidence/12-4-device-20261028/physical-journey-${name}.png`, fullPage: true });
    const browserRuntime = { version: browser.version(), viewport: page.viewportSize(), platform: process.platform, userAgent: await page.evaluate(() => navigator.userAgent) };
    writeFileSync(`docs/evidence/12-4-device-20261028/physical-journey-${name}.json`, JSON.stringify({ synthetic: true, mockedApi: false, browserRuntime, case: name, action, databaseAndApiRestart: name === 'A', nativeVisibilityEvents: visibility, nativeFocusEvents: focus, lifecycleEmulation: name === 'C', exactUploadedBytes: [a.uploadedBytes, c.uploadedBytes], draftIds: [a.saved.id, c.saved.id], planId: plan.id, selection, recap, notices }, null, 2));
});process.exit(0)})().catch(e=>{console.error(e.message);process.exit(1)});