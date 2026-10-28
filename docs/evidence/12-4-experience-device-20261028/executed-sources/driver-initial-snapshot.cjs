const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {chromium,expect}=require('../../frontend/node_modules/@playwright/test');
const out=path.resolve('docs/evidence/12-4-experience-device-20261028');fs.mkdirSync(out,{recursive:true});
const statePath=path.resolve('.private-runtime/story124-experience-device.json');
const adb='C:/Users/Jonas/.codex/.chatgpt-projects/g-p-6ab6b4c1c6888191a96d3242fab912b4/local-tools/android/platform-tools/adb.exe';
const API='http://127.0.0.1:18326';
const device=(...args)=>cp.execFileSync(adb,['-s','HA2BN9HR',...args],{encoding:'utf8',maxBuffer:8*1024*1024});
const state=()=>JSON.parse(fs.readFileSync(statePath,'utf8'));
async function connect(){const browser=await chromium.connectOverCDP('http://127.0.0.1:50924');const s=state();for(const page of browser.contexts().flatMap(c=>c.pages()).filter(p=>p.url().startsWith('http://127.0.0.1:15324/'))){const cdp=await page.context().newCDPSession(page);if((await cdp.send('Target.getTargetInfo')).targetInfo.targetId===s.target){page.setDefaultTimeout(15000);return{browser,page,cdp,s};}}throw Error('Exact own experience target missing');}
async function tap(page,cdp,locator){await expect(locator).toBeEnabled();await locator.scrollIntoViewIfNeeded();await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const b=await locator.boundingBox();if(!b)throw Error('Touch target missing');await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:b.x+b.width/2,y:b.y+b.height/2}]});await new Promise(r=>setTimeout(r,90));await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
const button=(p,name)=>p.getByRole('button',{name,exact:true});
async function get(page,url){return page.evaluate(async url=>{const r=await fetch(url,{credentials:'include',cache:'no-store'});if(!r.ok)throw Error('HTTP'+r.status);return r.json();},API+url);}
function write(name,data){fs.writeFileSync(path.join(out,name),JSON.stringify(data,null,2));}
async function record(name,run){const row={name,time:new Date().toISOString()};try{row.result=await run();row.passed=true;}catch(e){let error=e.stack||String(e);if(fs.existsSync(statePath)){const s=state();for(const k of ['username','password'])error=error.split(s[k]).join('[REDACTED]');}row.passed=false;row.error=error;}fs.appendFileSync(path.join(out,'checks.ndjson'),JSON.stringify(row)+'\n');console.log(name+': '+(row.passed?'PASS':'FAIL'));if(!row.passed)throw Error('Recorded failure: '+name);return row;}
function nodes(){device('shell','uiautomator','dump','/sdcard/ibe160-story124-experience-ui.xml');return[...device('exec-out','cat','/sdcard/ibe160-story124-experience-ui.xml').matchAll(/<node\s+([^>]+)>?/g)].map(m=>Object.fromEntries([...m[1].matchAll(/([\w-]+)="([^"]*)"/g)].map(x=>[x[1],x[2]])));}
function nativeTap(n){if(!n)throw Error('Required observed native control missing');const b=n.bounds.match(/\d+/g).map(Number);device('shell','input','tap',String((b[0]+b[2])/2),String((b[1]+b[3])/2));}
module.exports={fs,path,crypto,cp,chromium,expect,out,statePath,adb,API,device,state,connect,tap,button,get,write,record,nodes,nativeTap};
