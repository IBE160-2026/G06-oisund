import { editor } from './private-screen-helpers';
import { test, expect, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
const username='synthetic-recovery-'+randomUUID();
const oldPassword=randomBytes(24).toString('hex'), newPassword=randomBytes(24).toString('hex');
let code='';
function python(program:string) {
  return execFileSync('docker',['compose','-f','compose.password-tests.yaml','-p','ibe160-password-tests','exec','-T','private-api','python','-'],{cwd:'..',input:"from app import auth, password_recovery as recovery\nfrom app.private_storage import database\nwith database() as conn:\n auth.require_synthetic_accounts(conn)\n"+program,encoding:'utf8'});
}
test.beforeAll(()=>{if(process.env.COMPOSE_PROJECT_NAME!=='ibe160-password-tests') throw Error('Isolated password project required');});
test.beforeEach(()=>{
  code=python(`auth.provision(${JSON.stringify(username)},${JSON.stringify(oldPassword)})\nwith database() as conn:\n conn.execute('DELETE FROM login_limits')\ncode,_=recovery.issue(recovery.resolve(${JSON.stringify(username)}))\nprint(code)\n`).trim();
});
test.afterEach(()=>{
  code='';
  python(`with database() as conn:\n conn.execute('DELETE FROM workday_operations WHERE owner IN (SELECT id FROM accounts WHERE username=%s)',(${JSON.stringify(username)},))\n conn.execute('DELETE FROM workdays WHERE owner IN (SELECT id FROM accounts WHERE username=%s)',(${JSON.stringify(username)},))\n conn.execute('DELETE FROM drafts WHERE owner IN (SELECT id FROM accounts WHERE username=%s)',(${JSON.stringify(username)},))\n conn.execute('DELETE FROM draft_operations WHERE owner IN (SELECT id FROM accounts WHERE username=%s)',(${JSON.stringify(username)},))\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)',(${JSON.stringify(username)},))\n conn.execute('DELETE FROM accounts WHERE username=%s',(${JSON.stringify(username)},))\n conn.execute('DELETE FROM login_limits')\n`);
});
async function open(page:Page) {
  await page.goto('/private');
  await page.getByRole('button',{name:'Glemt passord?',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Glemt passord?',exact:true})).toBeFocused();
}
async function fill(page:Page, candidate=code, password=newPassword) {
  await page.getByLabel('Brukernavn',{exact:true}).fill(username);
  await page.getByLabel('Engangskode',{exact:true}).fill(candidate);
  await page.getByLabel('Nytt passord',{exact:true}).fill(password);
  await page.getByLabel('Gjenta nytt passord',{exact:true}).fill(password);
}
const submit=(page:Page)=>page.getByRole('button',{name:'Lagre nytt passord og logg ut alle enheter'}).click();
async function login(page:Page,password=oldPassword) {
  await page.getByLabel('Brukernavn',{exact:true}).fill(username);
  await page.getByLabel('Passord',{exact:true}).fill(password);
  await page.getByRole('button',{name:'Logg inn',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Privat arbeidsrom',exact:true})).toBeVisible();
}
async function visibility(page:Page) {
  await page.evaluate(()=>{
    Object.defineProperty(document,'visibilityState',{configurable:true,get:()=> 'hidden'});document.dispatchEvent(new Event('visibilitychange'));
    Object.defineProperty(document,'visibilityState',{configurable:true,get:()=> 'visible'});document.dispatchEvent(new Event('visibilitychange'));
  });
}
test('operator terminal to app, separate login and other device revocation',async({page,browser})=>{
  // Synthetic PTY capture stays in process memory; no trace or report disclosure.
  code=python(`import sys,re\nsys.path.insert(0,'tests')\nfrom test_password_recovery_operator import cli\nname=${JSON.stringify(username)}\nstatus,captured=cli(name,[(b'bekrefte',name),(b'TRYGT:','TRYGT'),(b'MOTTATT','MOTTATT')])\nif status != 0: raise RuntimeError('Synthetic terminal issuance failed')\nmatch=re.search(rb'Engangskode: ([A-Za-z0-9_-]{43})',captured)\nif not match: raise RuntimeError('Synthetic terminal code missing')\nprint(match.group(1).decode())\n`).trim();
  const other=await browser.newContext();const remote=await other.newPage();
  try {
    await remote.goto('/private');await login(remote);
    await open(page);await fill(page);await submit(page);
    await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
    await expect(page.getByRole('heading',{name:'Privat arbeidsrom',exact:true})).toHaveCount(0);
    await visibility(remote);
    await expect(remote.getByRole('form',{name:'Innlogging'})).toBeVisible();
    await login(page,newPassword);
    expect(await page.evaluate(()=>[localStorage.length,sessionStorage.length])).toEqual([0,0]);
    const logs=execFileSync('docker',['compose','-f','compose.password-tests.yaml','-p','ibe160-password-tests','logs','--no-color','private-api'],{cwd:'..',encoding:'utf8',maxBuffer:8*1024*1024});
    const safeLogs=![code,oldPassword,newPassword].some(secret=>logs.includes(secret));
    expect(safeLogs,'No synthetic recovery secrets in service logs').toBe(true);
  } finally {await other.close();}
});
test('invalid code associated error, clear secrets, cancel focus',async({page})=>{
  await open(page);await fill(page,'invalid');await submit(page);
  await expect(page.getByLabel('Engangskode',{exact:true})).toHaveAttribute('aria-describedby','recovery-feedback');
  await expect.poll(async()=> (await page.getByLabel('Engangskode',{exact:true}).inputValue()) === '', {message:'Recovery secret field is empty'}).toBe(true);
  await expect.poll(async()=> (await page.getByLabel('Nytt passord',{exact:true}).inputValue()) === '', {message:'Recovery secret field is empty'}).toBe(true);
  await expect(page.getByLabel('Brukernavn',{exact:true})).toBeFocused();
  await expect(page.getByRole('status').filter({hasText:'Alle feltene er tømt'})).toBeVisible();
  await page.getByLabel('Engangskode',{exact:true}).fill('corrected-invalid-code');
  await expect(page.locator('input[aria-invalid="true"]')).toHaveCount(0);
  await expect(page.getByLabel('Engangskode',{exact:true})).not.toHaveAttribute('aria-describedby','recovery-feedback');
  await page.getByRole('button',{name:'Avbryt',exact:true}).click();
  await expect(page.getByRole('button',{name:'Glemt passord?',exact:true})).toBeFocused();
});
for(const kind of ['lost','html','malformed','timeout','hide-lost','unrelated400']) test(`uncertain ${kind} never replays and new login resolves`,async({page})=>{
  await open(page);let posts=0;
  page.on('request',request=>{if(request.url().endsWith('/auth/password/recover'))posts++;});
  await page.route('**/auth/password/recover',async route=>{
    await route.fetch();
    if(kind==='hide-lost')await visibility(page);
    if(kind==='unrelated400') await route.fulfill({status:400,contentType:'application/json',body:JSON.stringify({detail:'Unrelated proxy rejection'})});
    else if(kind==='timeout') {await new Promise(resolve=>setTimeout(resolve,11000));await route.abort();}
    else if(kind==='lost'||kind==='hide-lost')await route.abort();
    else await route.fulfill({status:200,contentType:kind==='html'?'text/html':'application/json',body:kind==='html'?'<html>Unavailable</html>':'{"unexpected":true}'});
  });
  await fill(page);await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('ukjent',{timeout:15000});
  await expect(page.getByLabel('Engangskode',{exact:true})).toHaveCount(0);
  await visibility(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('ukjent');
  expect(posts).toBe(1);
  await page.getByRole('button',{name:'Prøv utlogging igjen'}).click();
  await login(page,newPassword);expect(posts).toBe(1);
});
test('hide before submit clears secrets without sending; BFCache rechecks',async({page})=>{
  await open(page);await fill(page);let posts=0;
  page.on('request',request=>{if(request.url().endsWith('/auth/password/recover'))posts++;});
  await visibility(page);
  await page.getByRole('button',{name:'Glemt passord?',exact:true}).click();
  await expect.poll(async()=> (await page.getByLabel('Engangskode',{exact:true}).inputValue()) === '', {message:'Recovery secret field is empty'}).toBe(true);
  await expect.poll(async()=> (await page.getByLabel('Nytt passord',{exact:true}).inputValue()) === '', {message:'Recovery secret field is empty'}).toBe(true);
  await page.evaluate(()=>{window.dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}));window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}));});
  await expect(page.getByRole('form',{name:'Innlogging'})).toBeVisible();expect(posts).toBe(0);
});
test('code point validation and preserved whitespace',async({page})=>{
  await open(page);await fill(page,code,'😀'.repeat(11));await submit(page);
  await expect(page.getByLabel('Nytt passord',{exact:true})).toBeFocused();
  await expect(page.getByLabel('Nytt passord',{exact:true})).toHaveAttribute('aria-invalid','true');
  await page.getByLabel('Nytt passord',{exact:true}).fill('😀'.repeat(12));
  await expect(page.locator('input[aria-invalid="true"]')).toHaveCount(0);
  await fill(page,code,' '+'😀'.repeat(254)+' ');await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
  await login(page,' '+'😀'.repeat(254)+' ');
});
test('signed in workspace must explicitly logout with dirty guard',async({page})=>{
  const otherName=username+'-other';
  python(`auth.provision(${JSON.stringify(otherName)},${JSON.stringify(oldPassword)})\n`);
  await page.goto('/private');
  await page.getByLabel('Brukernavn',{exact:true}).fill(otherName);
  await page.getByLabel('Passord',{exact:true}).fill(oldPassword);
  await page.getByRole('button',{name:'Logg inn',exact:true}).click();
  await expect(page.getByRole('button',{name:'Glemt passord?',exact:true})).toHaveCount(0);
  await expect(page.locator('.private-confirmation')).toHaveAttribute('aria-busy','false');
  await editor(page);
  await page.getByLabel('Buss/vogn',{exact:true}).fill('synthetic unsaved');
  page.once('dialog',dialog=>dialog.dismiss());
  await page.getByRole('button',{name:'Logg ut',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Privat arbeidsrom',exact:true})).toBeVisible();
  page.once('dialog',dialog=>dialog.accept());
  await page.getByRole('button',{name:'Logg ut',exact:true}).click();
  await page.getByRole('button',{name:'Glemt passord?',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Glemt passord?',exact:true})).toBeVisible();
  python(`with database() as conn:\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)',(${JSON.stringify(otherName)},))\n conn.execute('DELETE FROM accounts WHERE username=%s',(${JSON.stringify(otherName)},))\n`);
});
test('blank recovery form tablet PC themes and enlarged text',async({page})=>{
  await open(page);mkdirSync('../tmp/password-recovery-evidence',{recursive:true});
  for(const width of [800,1280])for(const theme of ['day','night']) {
    await page.setViewportSize({width,height:1100});
    const toggle=page.getByRole('button',{name:'Nattmodus',exact:true});
    if((await toggle.getAttribute('aria-pressed')==='true') !== (theme==='night'))await toggle.click();
    await page.evaluate(()=>{document.documentElement.style.fontSize='200%';});
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
    const bounds=await page.getByRole('button',{name:'Lagre nytt passord og logg ut alle enheter'}).boundingBox();
    expect(bounds!.height).toBeGreaterThanOrEqual(58);
    await page.getByLabel('Nytt passord',{exact:true}).focus();
  const contrast = await page.evaluate(() => {
    const rgb=(value:string)=>value.match(/[\d.]+/g)!.slice(0,3).map(Number);
    const lum=(value:string)=>rgb(value).map(v=>{const c=v/255;return c<=0.04045?c/12.92:((c+0.055)/1.055)**2.4;}).reduce((sum,v,i)=>sum+v*[0.2126,0.7152,0.0722][i],0);
    const ratio=(a:string,b:string)=>(Math.max(lum(a),lum(b))+0.05)/(Math.min(lum(a),lum(b))+0.05);
    const main=getComputedStyle(document.querySelector('main')!);
    const field=getComputedStyle(document.querySelector('#recover-new_password')!);
    const button=getComputedStyle(document.querySelector('form[aria-label="Gjenopprett tilgang"] button')!);
    return { text:ratio(main.color,main.backgroundColor), inputText:ratio(field.color,field.backgroundColor), inputBorder:ratio(field.borderColor,main.backgroundColor), buttonText:ratio(button.color,button.backgroundColor), focus:ratio(field.outlineColor,main.backgroundColor), focusWidth:field.outlineWidth };
  });
  expect(contrast.text).toBeGreaterThanOrEqual(4.5); expect(contrast.inputText).toBeGreaterThanOrEqual(4.5); expect(contrast.buttonText).toBeGreaterThanOrEqual(4.5);
  expect(contrast.inputBorder).toBeGreaterThanOrEqual(3); expect(contrast.focus).toBeGreaterThanOrEqual(3); expect(contrast.focusWidth).toBe('3px');
  writeFileSync(`../tmp/password-recovery-evidence/contrast-${width}-${theme}.json`,JSON.stringify(contrast,null,2));
    await page.screenshot({path:`../tmp/password-recovery-evidence/blank-${theme}-${width}.png`,fullPage:true});
  }
});

test('offline preflight clears secrets without replay',async({page,context})=>{
  await open(page);await fill(page);let posts=0;
  page.on('request',request=>{if(request.url().endsWith('/auth/password/recover'))posts++;});
  await context.setOffline(true);await submit(page);
  await expect(page.getByRole('status').filter({hasText:'ble ikke sendt'})).toBeVisible();
  await expect.poll(async()=> (await page.getByLabel('Engangskode',{exact:true}).inputValue()) === '', {message:'Recovery secret field is empty'}).toBe(true);
  await expect.poll(async()=> (await page.getByLabel('Nytt passord',{exact:true}).inputValue()) === '', {message:'Recovery secret field is empty'}).toBe(true);
  await expect(page.locator('input[aria-invalid="true"]')).toHaveCount(0);
  await expect(page.getByLabel('Brukernavn',{exact:true})).toBeFocused();
  await context.setOffline(false);expect(posts).toBe(0);
  await fill(page);await submit(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');expect(posts).toBe(1);
});

test('another tab login clears obsolete recovery form',async({page,context})=>{
  await open(page);await fill(page);
  const other=await context.newPage();
  try{
    await other.goto('/private');await login(other);
    await expect(page.getByLabel('Engangskode',{exact:true})).toHaveCount(0);
    await expect(page.getByLabel('Tilgangsstatus')).toContainText('annet vindu');
    await visibility(page);
    await expect(page.getByRole('heading',{name:'Privat arbeidsrom',exact:true})).toBeVisible();
    await expect(page.getByRole('button',{name:'Glemt passord?',exact:true})).toHaveCount(0);
  }finally{await other.close();}
});

test('delayed confirmed recovery keeps shared logout lock and guides explicit logout',async({page})=>{
  await open(page);
  let release!:()=>void, committed!:()=>void;
  const held=new Promise<void>(resolve=>{release=resolve;});
  const accepted=new Promise<void>(resolve=>{committed=resolve;});
  await page.route('**/auth/password/recover',async route=>{
    const response=await route.fetch();committed();await held;await route.fulfill({response});
  });
  await fill(page);await submit(page);await accepted;await visibility(page);
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('ukjent');
  release();
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret. Fullfør utlogging');
  await expect(page.getByRole('form',{name:'Innlogging'})).toHaveCount(0);
  const sharedLock=await page.evaluate(()=>document.cookie.includes('private_logout_pending=1'));
  expect(sharedLock).toBe(true);
  await page.getByRole('button',{name:'Prøv utlogging igjen'}).click();
  await expect(page.getByLabel('Tilgangsstatus')).toContainText('Passordet er endret.');
  await login(page,newPassword);
});

test('missed broadcast live B cookie receives real409 and preserves target',async({page,context})=>{
  const otherName=username+'-conflict';
  python(`auth.provision(${JSON.stringify(otherName)},${JSON.stringify(oldPassword)})\n`);
  try {
    await open(page);await fill(page);
    const csrf=await(await context.request.get('http://127.0.0.1:18441/auth/csrf')).json();
    const b=await context.request.post('http://127.0.0.1:18441/auth/login',{headers:{Origin:'http://127.0.0.1:15440','X-CSRF-Token':csrf.csrf_token},data:{username:otherName,password:oldPassword}});
    expect(b.status()).toBe(200);const bId=(await b.json()).account_id;
    const conflict=page.waitForResponse(r=>r.url().endsWith('/auth/password/recover'));
    await submit(page);expect((await conflict).status()).toBe(409);
    await expect(page.getByRole('heading',{name:'Privat arbeidsrom',exact:true})).toBeVisible();
    await expect(page.getByRole('button',{name:'Glemt passord?',exact:true})).toHaveCount(0);
    const current=await(await context.request.get('http://127.0.0.1:18441/auth/session')).json();
    expect(current.account_id===bId).toBe(true);
    const intact=python(`with database() as conn:\n row=conn.execute('SELECT id,password_hash FROM accounts WHERE username=%s',(${JSON.stringify(username)},)).fetchone()\n proof=conn.execute("SELECT digest,state FROM recovery_proofs WHERE owner=%s",(row['id'],)).fetchone()\n intact=auth.password_hash(${JSON.stringify(oldPassword)},row['password_hash'].split(':')[0])==row['password_hash'] and proof['state']=='active' and proof['digest']==auth.digest(${JSON.stringify(code)})\n print('intact' if intact else 'changed')\n`).trim()==='intact';
    expect(intact,'Target password and active proof remain unchanged').toBe(true);
    await page.getByRole('button',{name:'Logg ut',exact:true}).click();
    await page.getByRole('button',{name:'Glemt passord?',exact:true}).click();
    await expect(page.getByRole('heading',{name:'Glemt passord?',exact:true})).toBeVisible();
  } finally {
    python(`with database() as conn:\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)',(${JSON.stringify(otherName)},))\n conn.execute('DELETE FROM accounts WHERE username=%s',(${JSON.stringify(otherName)},))\n`);
  }
});

test('real recovery429 keeps form with wait guidance and no false field error',async({page,context})=>{
  await open(page);
  for(let attempt=0;attempt<5;attempt++) {
    const csrf=await(await context.request.get('http://127.0.0.1:18441/auth/csrf')).json();
    const response=await context.request.post('http://127.0.0.1:18441/auth/password/recover',{headers:{Origin:'http://127.0.0.1:15440','X-CSRF-Token':csrf.csrf_token},data:{username,code:'invalid',new_password:newPassword,confirmation:newPassword}});
    expect(response.status()).toBe(400);
  }
  await fill(page);const limited=page.waitForResponse(r=>r.url().endsWith('/auth/password/recover'));await submit(page);
  expect((await limited).status()).toBe(429);
  await expect(page.getByRole('form',{name:'Gjenopprett tilgang'})).toBeVisible();
  await expect(page.getByRole('status').filter({hasText:'Vent 15 minutter'})).toBeVisible();
  for(const label of ['Engangskode','Nytt passord','Gjenta nytt passord'])await expect.poll(async()=> (await page.getByLabel(label,{exact:true}).inputValue())==='',{message:'Recovery secret field cleared'}).toBe(true);
  await expect(page.locator('input[aria-invalid="true"]')).toHaveCount(0);
  await expect(page.getByLabel('Brukernavn',{exact:true})).toBeFocused();
  await expect(page.getByLabel('Tilgangsstatus')).not.toContainText('ukjent');
  await expect(page.getByRole('button',{name:'Prøv utlogging igjen'})).toHaveCount(0);
});
