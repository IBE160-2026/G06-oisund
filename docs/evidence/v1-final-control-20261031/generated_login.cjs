// Uses only this new recipe instance and its ignored generated synthetic account.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../../..');
const instance = path.join(root, 'tmp/recipe');
const { chromium } = require(path.join(instance, 'frontend/node_modules/playwright'));
(async () => {
  const account = JSON.parse(fs.readFileSync(path.join(instance, '.private-runtime/submission/account.json'), 'utf8'));
  assert.equal(account.username, 'synthetic-submission');
  const browser = await chromium.launch({ headless: true, channel: 'chromium' });
  try {
    const context = await browser.newContext();
    const page = await context.newPage();
    const origins = new Set();
    page.on('request', r => origins.add(new URL(r.url()).origin));
    await page.goto('http://127.0.0.1:15335/private');
    await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
    await page.getByLabel('Passord', { exact: true }).fill(account.password);
    await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
    await page.getByRole('heading', { name: 'Mine utkast', exact: true }).waitFor();
    const imported = page.waitForResponse(r => r.url().endsWith('/imports/pdf') && r.request().method() === 'POST');
    await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles(path.join(instance, 'Eksempelfiler/Testskift-B.pdf'));
    assert.equal((await imported).status(), 200);
    const saved = page.waitForResponse(r => r.url() === 'http://127.0.0.1:18338/drafts' && r.request().method() === 'POST');
    await page.getByRole('button', { name: 'Alt stemmer – lagre og fortsett', exact: true }).click();
    const reply = await saved;
    assert.equal(reply.status(), 200);
    assert.equal(reply.headers()['cache-control'], 'no-store');
    const data = await reply.json();
    await page.reload();
    await page.getByRole('button', { name: `Åpne ${data.draft.service_date} · versjon 1`, exact: true }).click();
    const current = await context.request.get('http://127.0.0.1:18338/drafts/' + data.id);
    assert.equal(current.status(), 200);
    assert.deepEqual(await current.json(), data);
    assert([...origins].every(o => ['http://127.0.0.1:15335','http://127.0.0.1:18338'].includes(o)));
    const result = {at_utc:new Date().toISOString(), browser:browser.version(), synthetic:true, generated_account_login:true, import_B:true, save:true, reload_reopen_exact_saved_draft:true, response_no_store:true, requested_origins:[...origins], no_restart_or_reset:true};
    fs.writeFileSync(path.join(__dirname, 'generated-login.json'), JSON.stringify(result,null,2)+'\n');
    console.log('PASS generated synthetic login, B import/save/reload/reopen; loopback only');
  } finally { await browser.close(); }
})().catch(error => { console.error(error.name + ': generated-login fixture failed; inspect locally'); process.exitCode=1; });
