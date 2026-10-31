// Bounded negative controls in the new synthetic instance; no production route.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../../..'),instance=path.join(root,'tmp/recipe');
const {chromium}=require(path.join(instance,'frontend/node_modules/playwright'));
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chromium'});
 try {
  const context=await browser.newContext(),page=await context.newPage();
  const account=JSON.parse(fs.readFileSync(path.join(instance,'.private-runtime/submission/account.json'),'utf8'));
  const api='http://127.0.0.1:18338',origin='http://127.0.0.1:15335';
  await page.goto(origin+'/private');
  await page.getByLabel('Brukernavn',{exact:true}).fill(account.username);
  await page.getByLabel('Passord',{exact:true}).fill(account.password);
  await page.getByRole('button',{name:'Logg inn',exact:true}).click();
  await page.getByRole('heading',{name:'Mine utkast',exact:true}).waitFor();
  const before=await (await context.request.get(api+'/drafts')).json();
  const cookies=await context.cookies(),csrf=cookies.find(c=>c.name==='private_csrf');assert(csrf);
  const cases=[];
  for(const [name,headers] of [
   ['foreign-origin-valid-csrf',{'Origin':'https://untrusted.example.invalid','X-CSRF-Token':csrf.value}],
   ['same-origin-missing-csrf',{'Origin':origin}],
   ['same-origin-wrong-csrf',{'Origin':origin,'X-CSRF-Token':'synthetic-invalid-proof'}],
  ]){
   const response=await context.request.post(api+'/drafts',{headers,data:{}});
   assert.equal(response.status(),403);assert.equal(response.headers()['cache-control'],'no-store');
   cases.push({name,status:response.status(),no_store:true});
  }
  const after=await (await context.request.get(api+'/drafts')).json();assert.deepEqual(after,before);
  const result={at_utc:new Date().toISOString(),browser:browser.version(),mode:'private-local loopback HTTP',cases,drafts_unchanged:true,cookies:cookies.map(({name,httpOnly,secure,sameSite,path})=>({name,httpOnly,secure,sameSite,path})),limit:'No HTTPS cookie qualification, real Cloudflare session, physical network-loss timing or exhaustive mutation-family coverage.'};
  fs.writeFileSync(path.join(__dirname,'local-origin-csrf.json'),JSON.stringify(result,null,2)+'\n');console.log('PASS three local refusals/no-store and unchanged draft state');
 }finally{await browser.close();}
})().catch(error=>{console.error(error.name+': local Origin/CSRF fixture failed');process.exitCode=1;});
