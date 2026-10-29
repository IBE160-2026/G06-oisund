const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),crypto=require('node:crypto'),readline=require('node:readline');
const root=process.cwd(),API='http://127.0.0.1:18330',origin='http://127.0.0.1:15326';
const {chromium,expect}=require(path.join(root,'frontend/node_modules/@playwright/test'));
const device=JSON.parse(fs.readFileSync('.private-runtime/v1-acceptance-device.json','utf8'));
const credentialsPath=path.join(root,'.private-runtime/v1-acceptance-manual-credentials.json');
const statePath=path.join(root,'.private-runtime/v1-acceptance-manual-state.json');
const out=path.join(root,'docs/evidence/v1-acceptance-device');fs.mkdirSync(out,{recursive:true});
function py(program){return cp.execFileSync('docker',['compose','-p','ibe160-v1followup-tests','-f','compose.v1followup.yaml','exec','-T','private-api','python','-'],{cwd:root,encoding:'utf8',input:'from app.auth import require_synthetic_accounts,provision\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n'+program});}
if(!fs.existsSync(credentialsPath)){
 const credentials={username:'synthetic-v1-acceptance-'+crypto.randomUUID(),password:crypto.randomBytes(32).toString('hex'),project:'ibe160-v1followup-tests',origin};
 fs.writeFileSync(credentialsPath,JSON.stringify(credentials,null,2),{flag:'wx'});
 py(`provision(${JSON.stringify(credentials.username)},${JSON.stringify(credentials.password)})\n`);
}
const credentials=JSON.parse(fs.readFileSync(credentialsPath,'utf8'));
if(credentials.project!=='ibe160-v1followup-tests'||credentials.origin!==origin)throw Error('Wrong synthetic credentials');
let browser,context,page,scene={},state=fs.existsSync(statePath)?JSON.parse(fs.readFileSync(statePath,'utf8')):{plans:{}};
const save=()=>fs.writeFileSync(statePath,JSON.stringify(state,null,2));
const button=name=>page.getByRole('button',{name,exact:true});
async function get(route){const r=await context.request.get(API+route);expect(r.ok()).toBe(true);return r.json();}
async function post(route,data){const proof=await get('/auth/csrf');const r=await context.request.post(API+route,{headers:{Origin:origin,'X-CSRF-Token':proof.csrf_token},data});expect(r.status()).toBe(200);return r.json();}
async function plan(key,day,fold=false){
 if(state.plans[key])return state.plans[key];
 const draft=await post('/drafts',{operation_id:(await post('/draft-operations',{})).operation_id,expected_revision:0,draft:{service_date:day,vehicle_duty:'Syntetisk V1-kontroll',activities:[{id:crypto.randomUUID(),type:'trip',line:'20',direction:'Nord',from_place:'Syntetisk start',to_place:'Syntetisk slutt',start:day+(fold?'T02:00:00+02:00':'T10:00:00+01:00'),end:day+(fold?'T03:00:00+01:00':'T11:00:00+01:00')}]}});
 const review=await post('/workday-reviews',{draft_id:draft.id,expected_revision:1});
 const p=await post('/drafts/'+draft.id+'/confirm',{operation_id:review.operation_id,expected_revision:1,acknowledgements:review.unknowns.map(x=>x.id),classifications:{}});
 state.plans[key]=p;save();return p;
}
async function open(p){
 if(await button('Lukk planen').isVisible()) {await expect(button('Lukk planen')).toBeEnabled();await button('Lukk planen').click();}
 const preparation=button('Forberedelse og planlister');if(await preparation.isVisible())await preparation.click();
 await button('Oppdater planlisten').click();await button('Åpne plan '+p.draft.service_date+' · versjon 1').click();
 await expect(page.getByText('Ikke startet',{exact:true})).toBeVisible();
}
async function prepare(resource){
 await page.unrouteAll({behavior:'wait'});
 const p=await plan(resource,resource==='selection'?'2031-01-05':'2031-01-06');await open(p);
 const current='/workdays/'+p.id+'/'+(resource==='start'?'lifecycle':'selection'),mutation='/workdays/'+p.id+'/'+resource;
 scene={kind:'rejection',resource,plan:p,writes:0};
 await page.route('**:18330'+mutation,route=>{
  if(route.request().method()==='POST'){scene.writes++;return route.fulfill({status:429,json:{detail:{code:resource+'_receipt_capacity',message:'For mange lagringsforsøk. Vent til tidligere planer utløper.'}}});}
  return route.fulfill({status:503,json:{detail:'Tjenesten er utilgjengelig.'}});
 });
 if(current!==mutation)await page.route('**:18330'+current,route=>route.fulfill({status:503,json:{detail:'Tjenesten er utilgjengelig.'}}));
 return {scene:resource,ready:true,controlledFault:'canonical mutation429 + unavailable current503; no server write'};
}
async function seed(){
 if(state.noticesSeeded)return;
 const examples=[{title:'Syntetisk SMS om midlertidig holdeplass',summary:'Bruk midlertidig holdeplass ved kaia.',description:'2. januar 2031: Linje 20 mot nord bruker kaia.\n3. januar 2031: Linje 24 mot sør bruker biblioteket.\nDette er et uavhengig syntetisk aksepteksempel.',source_note:'Syntetisk SMS fra trafikkleder; ingen nettadresse.',source_url:null,line_scope:'selected',line_tags:['20','24']},{title:'Syntetisk delt lenke med lang instruksjon',summary:'Felles melding for alle linjer.',description:Array(24).fill('Uavhengig skrevet norsk instruksjon: gå gjennom skilting mens bussen står stille.').join('\n'),source_note:'Syntetisk eksempel med delt lenke.',source_url:'https://example.invalid/delt-melding',line_scope:'all',line_tags:[]}];
 for(const example of examples)await post('/notices',{operation_id:(await post('/notice-operations',{})).operation_id,expected_revision:0,content:{...example,source_updated_at:null,valid_from:null,valid_until:'2031-01-04T23:59:59+01:00'}});
 for(const [offset,title] of [['+02:00','Første 02:30 – syntetisk'],['+01:00','Andre 02:30 – syntetisk']])await post('/notices',{operation_id:(await post('/notice-operations',{})).operation_id,expected_revision:0,content:{title,line_scope:'all',line_tags:[],source_url:null,source_updated_at:'2030-10-27T02:30:00'+offset,valid_from:'2030-10-27T02:30:00+02:00',valid_until:'2030-10-27T02:30:00+01:00'}});
 state.noticesSeeded=true;save();
}
async function action(command){
 if(command==='selection'||command==='start')return prepare(command);
 if(command==='status')return {scene:scene.kind,resource:scene.resource,writes:scene.writes,guard:await page.evaluate(()=>{const e=new Event('beforeunload',{cancelable:true});window.dispatchEvent(e);return e.defaultPrevented;}),messages:await page.getByRole('status').allTextContents(),viewport:await page.evaluate(()=>({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scale:visualViewport.scale,orientation:screen.orientation.type,theme:document.documentElement.dataset.theme}))};
 if(command==='abandon'){
  await page.unrouteAll({behavior:'wait'});const p=await plan('abandon','2031-01-07');await open(p);scene={kind:'abandon',plan:p,writes:0};
  await page.route('**:18330/workdays/'+p.id+'/selection',async route=>{if(route.request().method()!=='POST')return route.continue();scene.writes++;scene.operation=route.request().postDataJSON().operation_id;await route.fetch();await route.abort();});return {ready:true,scene:'abandon',controlledFault:'actual accepted selection, reply loss only'};
 }
 if(command==='remove-plan'){await post('/workdays/'+scene.plan.id+'/delete',{operation_id:crypto.randomUUID(),source_revision:1});return {deletedSyntheticParent:true,originalSelectionWrites:scene.writes};}
 if(command==='folds'||command==='examples'){
  await page.unrouteAll({behavior:'wait'});const p=await plan(command,command==='folds'?'2030-10-27':'2031-01-03',command==='folds');await open(p);await button('Les avvik for linjer og datoer').click();scene={kind:command};return {ready:true,scene:command,candidates:await page.locator('.notice-list summary').count()};
 }
 if(command==='capture') {const info=await action('status');const name=new Date().toISOString().replaceAll(/[:.]/g,'-');await page.screenshot({path:path.join(out,name+'-'+scene.kind+'.png'),fullPage:true});fs.appendFileSync(path.join(out,'observations.ndjson'),JSON.stringify({time:new Date().toISOString(),...info,method:'passive metadata and screenshot of own synthetic scene; human outcome recorded separately'})+'\n');return info;}
 if(command==='close'){await context.close();await browser.close();return {closedOnlyOwnContext:true};}
 throw Error('Unknown command');
}
(async()=>{
 browser=await chromium.connectOverCDP(device.endpoint);context=await browser.newContext({viewport:null});page=await context.newPage();await page.bringToFront();page.setDefaultTimeout(15000);
 const cdp=await context.newCDPSession(page);state.target=(await cdp.send('Target.getTargetInfo')).targetInfo.targetId;save();
 await page.goto(origin+'/private');await page.getByLabel('Brukernavn',{exact:true}).fill(credentials.username);await page.getByLabel('Passord',{exact:true}).fill(credentials.password);await button('Logg inn').click();await expect(page.getByRole('heading',{name:'Mine utkast',exact:true})).toBeVisible();
 await seed();await action('selection');
 const identity={time:new Date().toISOString(),product:'3c2287ed68d0cbb1923439fc6ee00254395072a4',browser:browser.version(),target:state.target,model:device.model,android:device.android,method:'actual USB Lenovo browser; separate context, viewport:null; no device metrics emulation',ui:await page.evaluate(()=>({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,ua:navigator.userAgent,orientation:screen.orientation.type})),assets:await page.locator('script[src]').evaluateAll(nodes=>nodes.map(n=>new URL(n.src).pathname))};fs.writeFileSync(path.join(out,'manual-device-identity.json'),JSON.stringify(identity,null,2));console.log('READY '+JSON.stringify(identity));
 const lines=readline.createInterface({input:process.stdin});let queue=Promise.resolve();lines.on('line',line=>{queue=queue.then(async()=>{try{const result=await action(line.trim());console.log('RESULT '+JSON.stringify(result));if(line.trim()==='close')process.exit(0);}catch(e){let message=e.message;for(const value of [credentials.username,credentials.password])message=message.split(value).join('[REDACTED]');console.log('ERROR '+message);}});});
})().catch(e=>{let message=e.stack||e.message;for(const value of [credentials.username,credentials.password])message=message.split(value).join('[REDACTED]');console.log('ERROR '+message);process.exit(1)});
