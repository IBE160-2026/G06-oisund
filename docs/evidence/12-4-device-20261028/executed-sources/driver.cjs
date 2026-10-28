const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {chromium,expect}=require('../../frontend/node_modules/@playwright/test');
const out=path.resolve('docs/evidence/12-4-device-20261028');fs.mkdirSync(out,{recursive:true});
const statePath=path.resolve('.private-runtime/story124-device.json');
const adb='C:/Users/Jonas/.codex/.chatgpt-projects/g-p-6ab6b4c1c6888191a96d3242fab912b4/local-tools/android/platform-tools/adb.exe';
const API='http://127.0.0.1:18326';
function device(...args){return cp.execFileSync(adb,['-s','HA2BN9HR',...args],{encoding:'utf8',maxBuffer:8*1024*1024});}
function state(){return JSON.parse(fs.readFileSync(statePath,'utf8'));}
async function connect(){const browser=await chromium.connectOverCDP('http://127.0.0.1:50924');const s=state();let page,cdp;for(const candidate of browser.contexts().flatMap(c=>c.pages()).filter(p=>p.url().startsWith('http://127.0.0.1:15324/'))){const session=await candidate.context().newCDPSession(candidate);if((await session.send('Target.getTargetInfo')).targetInfo.targetId===s.target){page=candidate;cdp=session;break;}}if(!page)throw Error('Exact own12.4 target missing');page.setDefaultTimeout(12000);return{browser,page,cdp,s};}
async function tap(page,cdp,locator){await expect(locator).toBeEnabled();await locator.scrollIntoViewIfNeeded();await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const b=await locator.boundingBox();if(!b)throw Error('Touch target missing');await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:b.x+b.width/2,y:b.y+b.height/2}]});await new Promise(r=>setTimeout(r,90));await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
const button=(p,name)=>p.getByRole('button',{name,exact:true});
async function get(page,url){return page.evaluate(async url=>{const r=await fetch(url,{credentials:'include',cache:'no-store'});if(!r.ok)throw Error('HTTP'+r.status);return r.json();},API+url);}
function write(name,data){fs.writeFileSync(path.join(out,name),JSON.stringify(data,null,2));}
async function record(name,run){const row={name,time:new Date().toISOString()};try{row.result=await run();row.passed=true;}catch(e){let error=e.stack||String(e);const s=state();for(const key of ['username','password'])error=error.split(s[key]).join('[REDACTED]');row.passed=false;row.error=error;}fs.appendFileSync(path.join(out,'checks.ndjson'),JSON.stringify(row)+'\n');console.log(name+': '+(row.passed?'PASS':'FAIL'));if(!row.passed)throw Error('Recorded failure: '+name);return row;}
module.exports={fs,path,crypto,cp,chromium,expect,out,statePath,adb,API,device,state,connect,tap,button,get,write,record};
