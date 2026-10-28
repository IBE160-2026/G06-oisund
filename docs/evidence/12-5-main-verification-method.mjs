// Read-only source, documentation and live demo identity check for this integration.
import {execFileSync} from 'node:child_process';
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const run=(cmd,args)=>execFileSync(cmd,args,{encoding:'utf8'}).trim();
const git=(...args)=>run('git',args);
const assert=(v,message)=>{if(!v)throw Error(message);};
const snapshot='c067fdbb20150219c041588ed4e990e7b0ef6b94';
const accepted='330d5a21bc38decc95bbd5332edee2acf08e4faa';
const merge='dbdbd1813e29c02913b72e15a24f0a3321565d95';
for(const c of [snapshot,accepted,'12c847555be40c7ec603c0ca4e72e38adc7e9181',merge])git('merge-base','--is-ancestor',c,'HEAD');
const tree=git('rev-parse',merge+'^{tree}');
assert(tree===git('rev-parse',accepted+'^{tree}'),'Accepted tree mismatch');
const executable=['backend','frontend','scripts','deploy','compose.submission.yaml','.dockerignore','.gitattributes','Eksempelfiler'];
git('diff','--exit-code',snapshot,'HEAD','--',...executable);
assert(readFileSync('README.md','utf8').includes('git clone --branch main '),'README must use surviving main ref');
assert(readFileSync('README.md','utf8').includes(snapshot),'Immutable pin lost');
assert(/epic-12: in-progress/.test(readFileSync('_bmad-output/implementation-artifacts/sprint-status.yaml','utf8')),'Epic must stay open');
const docs=['README.md',...git('ls-files','docs/submission').split('\n').filter(p=>p.endsWith('.md')),'docs/evidence/12-5-reproduction.md','docs/evidence/12-5-owner-acceptance-2026-10-28.md','docs/evidence/12-5-main-integration.md'];
let localLinks=0,lineBounds=0;
for(const file of docs){
 for(const m of readFileSync(file,'utf8').matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  let target=m[1].replace(/^<|>$/g,'');
  if(/^(https?:|mailto:|#)/.test(target))continue;
  const [name,fragment]=target.split('#');
  const resolved=path.resolve(path.dirname(file),decodeURIComponent(name));
  // This method writes its own linked result only after all checks succeed.
  assert(existsSync(resolved)||resolved===path.resolve('docs/evidence/12-5-main-verification.json'),file+' missing '+target);localLinks++;
  if(/^L\d+$/.test(fragment??'')){
   const n=Number(fragment.slice(1));
   assert(n>0&&n<=readFileSync(resolved,'utf8').split('\n').length,file+' line out of bounds '+target);lineBounds++;
  }
 }
}
const cleanRoot='D:/IBE160/tmp/submission-clean-20261028';
assert(run('git',['-C',cleanRoot,'rev-parse','HEAD'])===snapshot,'Demo checkout moved');
assert(run('git',['-C',cleanRoot,'status','--porcelain'])==='','Demo checkout dirty');
const prior=JSON.parse(readFileSync('docs/evidence/12-5-identity-review.json','utf8'));
const assets=[];
for(const item of prior.served){
 const response=await fetch('http://127.0.0.1:15325'+item.asset);
 assert(response.ok,'Asset HTTP failure');
 const bytes=new Uint8Array(await response.arrayBuffer());
 const hash=createHash('sha256').update(bytes).digest('hex');
 assert(hash===item.sha256,'Served asset changed');
 const built=readFileSync('tmp/integration-125-fresh-frontend/frontend/dist'+item.asset);
 assert(createHash('sha256').update(built).digest('hex')===hash,'Fresh build differs from served asset');
 assets.push({asset:item.asset,sha256:hash,equalsFreshBuild:true});
}
const health=[];
for(const port of [18327,18328]){
 const response=await fetch('http://127.0.0.1:'+port+'/health');
 assert(response.ok,'API unhealthy');health.push({port,status:response.status,body:await response.json()});
}
const result={at:new Date().toISOString(),checkedHead:git('rev-parse','HEAD'),merge,accepted,snapshot,acceptedAndMergeTree:tree,allAncestors:true,executablePaths:executable,executableDiffFromSnapshot:'empty',localLinks,lineBounds,demoSource:snapshot,demoClean:true,assets,health,result:'passed'};
writeFileSync('docs/evidence/12-5-main-verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
