import { editor, preparation } from './private-screen-helpers';
import { test, expect, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
const username = 'synthetic-password-' + randomUUID();
const oldPassword = randomBytes(24).toString('hex');
const newPassword = randomBytes(24).toString('hex');
function python(program: string) {
  return execFileSync('docker', ['compose', '-f', 'compose.password-tests.yaml', 'exec', '-T', 'private-api', 'python', '-'], { cwd: '..', input: "from app import auth\nfrom app.private_storage import database\nwith database() as conn:\n auth.require_synthetic_accounts(conn)\n" + program, encoding: 'utf8' });
}
test.beforeAll(() => { if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-password-tests') throw Error('Isolated password project required'); });
test.beforeEach(() => {
  python(`auth.provision(${JSON.stringify(username)}, ${JSON.stringify(oldPassword)})\nwith database() as conn:\n conn.execute('DELETE FROM login_limits')\n`);
});
test.afterEach(() => {
  python(`with database() as conn:\n conn.execute('DELETE FROM workday_operations WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM workdays WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM drafts WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM draft_operations WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM accounts WHERE username=%s', (${JSON.stringify(username)},))\n conn.execute('DELETE FROM login_limits')\n`);
});
async function login(page: Page, password=oldPassword) {
  await page.goto('/private');
  await loginRendered(page, password);
}
async function loginRendered(page: Page, password=oldPassword) {
  await expect(page.getByLabel('Brukernavn', { exact:true })).toBeEnabled();
  await page.getByLabel('Brukernavn', { exact:true }).fill(username);
  await page.getByLabel('Passord', { exact:true }).fill(password);
  await page.getByRole('button', { name:'Logg inn', exact:true }).click();
  await expect(page.getByRole('heading', { name:'Privat arbeidsrom' })).toBeVisible();
}
async function open(page: Page) {
  await expect(page.locator('.draft-loaded-count')).toContainText('Lastet ');
  await expect(page.locator('.private-confirmation')).toHaveAttribute('aria-busy', 'false');
  await page.getByRole('button', { name:'Brukerinnstillinger', exact:true }).click();
  await expect(page.getByRole('heading', { name:'Endre passord', exact:true })).toBeFocused();
}
async function fill(page: Page, current=oldPassword) {
  await page.getByLabel('Gjeldende passord', { exact:true }).fill(current);
  await page.getByLabel('Nytt passord', { exact:true }).fill(newPassword);
  await page.getByLabel('Gjenta nytt passord', { exact:true }).fill(newPassword);
}
const submit = (page: Page) => page.getByRole('button', { name:'Endre passord og logg ut alle enheter' }).click();

test('real change, all-device revocation and same-account login', async ({page, browser, context}) => {
  const other = await browser.newContext(); const otherPage=await other.newPage();
  const sibling = await context.newPage();
  try {
    await login(page); await login(otherPage);
    await sibling.goto('/private');
    await expect(sibling.locator('.private-confirmation')).toHaveAttribute('aria-busy', 'false');
    await expect(sibling.locator('.draft-loaded-count')).toHaveText('Lastet 0 utkast.');
    let siblingRequests = 0;
    sibling.on('request', () => { siblingRequests++; });
    await open(page); await fill(page); await submit(page);
    await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
    await expect(page.getByLabel('Brukernavn', {exact:true})).toBeFocused();
    await expect(sibling.getByLabel('Brukernavn', {exact:true})).toBeVisible();
    await expect(sibling.getByRole('region', {name:'Private utkast',exact:true})).toHaveCount(0);
    expect(siblingRequests).toBe(0);
    await otherPage.evaluate(() => {
      Object.defineProperty(document, 'visibilityState', {configurable:true,get:()=> 'hidden'}); document.dispatchEvent(new Event('visibilitychange'));
      Object.defineProperty(document, 'visibilityState', {configurable:true,get:()=> 'visible'}); document.dispatchEvent(new Event('visibilitychange'));
    });
    await expect(otherPage.getByLabel('Brukernavn', {exact:true})).toBeVisible();
    await loginRendered(page,newPassword);
    expect(await page.evaluate(()=>[sessionStorage.length,localStorage.length])).toEqual([0,0]);
  } finally { await sibling.close(); await other.close(); }
});

for (const path of ['/auth/csrf', '/auth/session']) test(`password preflight ${path} failure is not sent and recoverable`, async ({page}) => {
  await login(page); await open(page);
  let posts = 0;
  page.on('request', request => { if (request.url().endsWith('/auth/password/change')) posts++; });
  await page.route('**' + path, route => route.abort());
  await fill(page); await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordendringen ble ikke sendt.');
  await expect(page.getByRole('button', {name:'Prøv utlogging igjen'})).toHaveCount(0);
  expect(posts).toBe(0);
  await page.unroute('**' + path);
  if (path === '/auth/session') await page.getByRole('button', {name:'Kontroller tilgang igjen',exact:true}).click();
  await expect(page.getByLabel('Gjeldende passord', {exact:true})).toHaveValue('');
  await expect(page.getByLabel('Nytt passord', {exact:true})).toHaveValue('');
  await expect(page.getByRole('heading', {name:'Endre passord',exact:true})).toBeVisible();
  expect(posts).toBe(0);
  await fill(page); await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
  expect(posts).toBe(1);
});

test('confirmed password outcome remains confirmed after shared logout lock', async ({page}) => {
  await login(page); await open(page); await fill(page); await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
  await page.evaluate(() => {
    document.cookie = 'private_logout_pending=1; Path=/; SameSite=Strict';
    const channel = new BroadcastChannel('private-access-security'); channel.postMessage('logout-pending'); channel.close();
  });
  await expect(page.getByRole('button',{name:'Prøv utlogging igjen'})).toBeEnabled();
  await page.getByRole('button',{name:'Prøv utlogging igjen'}).click();
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
  await expect(page.getByLabel('Tilgangsstatus')).not.toContainText('ikke bekreftet');
});
test('typed rejection clears secrets and cancel returns focus', async ({page}) => {
  await login(page); await open(page); await fill(page,'synthetic-incorrect'); await submit(page);
  await expect(page.getByText('Gjeldende passord er feil.', {exact:true})).toBeVisible();
  await expect(page.getByLabel('Gjeldende passord', {exact:true})).toHaveValue('');
  await expect(page.getByLabel('Gjeldende passord', {exact:true})).toHaveAttribute('aria-invalid', 'true');
  await expect(page.getByLabel('Gjeldende passord', {exact:true})).toHaveAttribute('aria-describedby', 'password-feedback');
  await expect(page.getByLabel('Gjeldende passord', {exact:true})).toBeFocused();
  await expect(page.getByLabel('Nytt passord', {exact:true})).toHaveValue('');
  await page.getByRole('button',{name:'Avbryt',exact:true}).click();
  await expect(page.getByRole('button',{name:'Brukerinnstillinger',exact:true})).toBeFocused();
});

test('code-point limits preserve non-BMP credentials and whitespace through login and verification', async ({page}) => {
  await login(page); await open(page); await fill(page);
  const next = ' ' + '😀'.repeat(254) + ' ';
  await page.getByLabel('Nytt passord', {exact:true}).fill('😀'.repeat(11));
  await page.getByLabel('Gjenta nytt passord', {exact:true}).fill('😀'.repeat(11));
  await submit(page);
  await expect(page.getByLabel('Nytt passord', {exact:true})).toBeFocused();
  await expect(page.getByText('Nytt passord må ha 12–256 tegn.', {exact:true})).toBeVisible();
  await page.getByLabel('Nytt passord', {exact:true}).fill(next + 'x');
  await page.getByLabel('Gjenta nytt passord', {exact:true}).fill(next + 'x');
  await submit(page);
  await expect(page.getByLabel('Nytt passord', {exact:true})).toHaveValue(next + 'x');
  await page.getByLabel('Nytt passord', {exact:true}).fill(next);
  await page.getByLabel('Gjenta nytt passord', {exact:true}).fill(next + 'x');
  // Use a valid-length mismatch to exercise its associated correction focus.
  await page.getByLabel('Gjenta nytt passord', {exact:true}).fill('😀'.repeat(256));
  await submit(page);
  await expect(page.getByLabel('Gjenta nytt passord', {exact:true})).toBeFocused();
  await expect(page.getByLabel('Gjenta nytt passord', {exact:true})).toHaveAttribute('aria-invalid', 'true');
  await page.getByLabel('Gjenta nytt passord', {exact:true}).fill(next);
  await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
  await login(page, next); await open(page); await fill(page, next); await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
  await login(page, newPassword);
});

for (const lost of [false, true]) test(`hide/show retains dispatched outcome after delayed actual commit, lost=${lost}`, async ({page}) => {
  await login(page); await open(page);
  let release!: () => void, started!: () => void, count = 0;
  const gate = new Promise<void>(r => { release = r; });
  const entered = new Promise<void>(r => { started = r; });
  await page.route('**/auth/password/change', async route => {
    count++; started(); await gate;
    const response = await route.fetch();
    if (lost) await route.abort(); else await route.fulfill({response});
  });
  await fill(page); await submit(page); await entered;
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', {configurable:true, get:()=> 'hidden'});
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByLabel('Gjeldende passord', {exact:true})).toHaveCount(0);
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', {configurable:true, get:()=> 'visible'});
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Resultatet av passordendringen er ukjent.');
  release();
  await expect(page.getByRole('button', {name:'Prøv utlogging igjen'})).toBeEnabled();
  await page.getByRole('button', {name:'Prøv utlogging igjen'}).click();
  await expect(page.getByLabel('Brukernavn', {exact:true})).toBeEnabled();
  await login(page, newPassword);
  expect(count).toBe(1);
});

test('PDF processing and unsaved review block settings until explicit cancellation or adoption', async ({page}) => {
  const pdf = Buffer.from(python('import sys, base64\nsys.path.insert(0, "/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nprint(base64.b64encode(synthetic_text_pdf()).decode())\n').trim(), 'base64');
  await login(page); await preparation(page);
  let release!: () => void, started!: () => void;
  const gate = new Promise<void>(r => { release = r; });
  const entered = new Promise<void>(r => { started = r; });
  await page.route('**/imports/pdf', async route => { const response = await route.fetch(); started(); await gate; await route.fulfill({response}); });
  const upload = () => page.getByLabel('Velg tekst-PDF', {exact:true}).setInputFiles({name:'synthetic.pdf',mimeType:'application/pdf',buffer:pdf});
  const blocked = async () => {
    await page.getByRole('button', {name:'Brukerinnstillinger',exact:true}).click();
    await expect(page.getByLabel('Tilgangsstatus')).toContainText('Lagre eller forkast');
    await expect(page.getByRole('heading', {name:'Endre passord',exact:true})).toHaveCount(0);
  };
  await upload(); await entered; await blocked();
  release();
  await expect(page.getByRole('heading', {name:'Importsammendrag',exact:true})).toBeVisible();
  await blocked();
  await page.getByRole('button', {name:'Forkast gjennomgang',exact:true}).click();
  await open(page); await page.getByRole('button', {name:'Avbryt',exact:true}).click();
  await page.unroute('**/imports/pdf'); await upload();
  await expect(page.getByRole('heading', {name:'Importsammendrag',exact:true})).toBeVisible();
  await page.getByRole('button', {name:'Rett eller legg til opplysninger',exact:true}).click();
  // Adoption transfers the guard to the unsaved draft; explicit reset releases it.
  await blocked();
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', {name:'Tilbakestill utkast',exact:true}).click();
  await open(page);
});
for (const mode of ['lost','html','malformed']) test(`uncertain ${mode} response never replays credentials`, async ({page}) => {
  await login(page); await open(page); let count=0;
  await page.route('**/auth/password/change',async route=>{count++; await route.fetch(); if(mode==='lost') await route.abort(); else await route.fulfill({status:200,contentType:mode==='html'?'text/html':'application/json',body:mode==='html'?'<html>Unavailable</html>':'{"bad":true}'});});
  await fill(page); await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Resultatet av passordendringen er ukjent.');
  await expect(page.getByLabel('Gjeldende passord', {exact:true})).toHaveCount(0);
  await page.getByRole('button',{name:'Prøv utlogging igjen',exact:true}).click();
  await login(page,newPassword); expect(count).toBe(1);
});
for (const width of [768,1440]) for(const night of [false,true]) test(`settings keyboard and 200 percent ${width} ${night?'night':'day'}`,async ({page})=>{
  await page.setViewportSize({width,height:1000}); await login(page);
  if(night) await page.getByRole('button',{name:'Nattmodus',exact:true}).click();
  await open(page); await page.evaluate(()=>{document.documentElement.style.fontSize='200%';});
  await expect(page.getByLabel('Gjeldende passord',{exact:true})).toHaveAttribute('autocomplete','current-password');
  await expect(page.getByLabel('Nytt passord',{exact:true})).toHaveAttribute('autocomplete','new-password');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  for(const field of await page.locator('section[aria-label="Brukerinnstillinger"] input').all()) expect((await field.boundingBox())!.height).toBeGreaterThanOrEqual(58);
  await page.getByLabel('Gjeldende passord',{exact:true}).focus(); await page.keyboard.press('Tab');
  await expect(page.getByLabel('Nytt passord',{exact:true})).toBeFocused();
  mkdirSync('../tmp/password-evidence',{recursive:true});
  const contrast = await page.evaluate(() => {
    const rgb=(value:string)=>value.match(/[\d.]+/g)!.slice(0,3).map(Number);
    const lum=(value:string)=>rgb(value).map(v=>{const c=v/255;return c<=0.04045?c/12.92:((c+0.055)/1.055)**2.4;}).reduce((sum,v,i)=>sum+v*[0.2126,0.7152,0.0722][i],0);
    const ratio=(a:string,b:string)=>(Math.max(lum(a),lum(b))+0.05)/(Math.min(lum(a),lum(b))+0.05);
    const main=getComputedStyle(document.querySelector('main')!);
    const field=getComputedStyle(document.querySelector('#change-new_password')!);
    const button=getComputedStyle(document.querySelector('form[aria-label="Endre passord"] button')!);
    return { text:ratio(main.color,main.backgroundColor), inputText:ratio(field.color,field.backgroundColor), inputBorder:ratio(field.borderColor,main.backgroundColor), buttonText:ratio(button.color,button.backgroundColor), focus:ratio(field.outlineColor,main.backgroundColor), focusWidth:field.outlineWidth };
  });
  expect(contrast.text).toBeGreaterThanOrEqual(4.5); expect(contrast.inputText).toBeGreaterThanOrEqual(4.5); expect(contrast.buttonText).toBeGreaterThanOrEqual(4.5);
  expect(contrast.inputBorder).toBeGreaterThanOrEqual(3); expect(contrast.focus).toBeGreaterThanOrEqual(3); expect(contrast.focusWidth).toBe('3px');
  writeFileSync(`../tmp/password-evidence/contrast-${width}-${night?'night':'day'}.json`,JSON.stringify(contrast,null,2));
  await page.screenshot({path:`../tmp/password-evidence/settings-${width}-${night?'night':'day'}-200.png`,fullPage:true});
});

test('dirty and uncertain business writes block settings without losing input',async ({page})=>{
  await login(page); await editor(page);
  await page.getByLabel('Buss/vogn',{exact:true}).fill('Synthetic-unsaved');
  await page.getByRole('button',{name:'Brukerinnstillinger',exact:true}).click();
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Lagre eller forkast');
  await expect(page.getByLabel('Buss/vogn',{exact:true})).toHaveValue('Synthetic-unsaved');
  await page.route('**/drafts',route=>route.request().method()==='POST'?route.abort():route.continue());
  await page.getByRole('button',{name:'Lagre utkast',exact:true}).click();
  await expect(page.getByRole('button',{name:'Kontroller lagringsforsøket',exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Brukerinnstillinger',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Endre passord',exact:true})).toHaveCount(0);
  await expect(page.getByLabel('Buss/vogn',{exact:true})).toHaveValue('Synthetic-unsaved');
});

test('unconfirmed decisions block settings and accepted plan releases the guard',async ({page,context})=>{
  await login(page);
  const post=async(path:string,data:object)=>{
    const csrf=await(await context.request.get('http://127.0.0.1:18441/auth/csrf')).json();
    const response=await context.request.post('http://127.0.0.1:18441'+path,{headers:{Origin:'http://127.0.0.1:15440','X-CSRF-Token':csrf.csrf_token},data});
    expect(response.status()).toBe(200);return response.json();
  };
  const op=await post('/draft-operations',{});
  await post('/drafts',{operation_id:op.operation_id,expected_revision:0,draft:{service_date:'2031-01-02',vehicle_duty:'Synthetic',physical_bus:null,activities:[{id:randomUUID(),type:null,raw_code:'Synthetic',start:'2031-01-02T10:00+01:00',end:'2031-01-02T11:00+01:00'}]}});
  await preparation(page); await page.getByRole('button',{name:'Oppdater listen',exact:true}).click();
  await page.getByRole('button',{name:'Åpne 2031-01-02 · versjon 1',exact:true}).click();
  await editor(page); await page.getByRole('button',{name:'Gjennomgå lagret utkast',exact:true}).click();
  const review=page.getByRole('region',{name:'Gjennomgått versjon',exact:true});
  await expect(review).toBeVisible();
  for(const select of await review.getByRole('combobox').all()) await select.selectOption('manual');
  for(const checkbox of await review.getByRole('checkbox').all()) await checkbox.check();
  await page.getByRole('button',{name:'Brukerinnstillinger',exact:true}).click();
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Lagre eller forkast');
  await page.getByRole('button',{name:'Bekreft gjennomgått plan',exact:true}).click();
  await expect(page.getByRole('region',{name:'Bekreftet plan',exact:true})).toBeVisible();
  await open(page); await page.getByRole('button',{name:'Avbryt',exact:true}).click();
  await expect(page.getByRole('region',{name:'Bekreftet plan',exact:true})).toBeVisible();
});
