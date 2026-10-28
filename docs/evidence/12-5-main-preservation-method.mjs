import {execFileSync} from 'node:child_process';
import {writeFileSync,readFileSync} from 'node:fs';
const run=(exe,args,cwd='D:/IBE160')=>execFileSync(exe,args,{cwd,encoding:'utf8'}).trim();
const git=(...args)=>run('git',args);
const paths=git('worktree','list','--porcelain').split('\n').filter(x=>x.startsWith('worktree ')).map(x=>x.slice(9));
const worktrees=paths.map(path=>({path,head:run('git',['rev-parse','HEAD'],path),status:run('git',['status','--porcelain'],path)}));
const ids=run('docker',['ps','-aq']).split(/\s+/).filter(Boolean);
const containers=JSON.parse(run('docker',['inspect',...ids])).map(c=>({id:c.Id,name:c.Name,image:c.Image,started:c.State.StartedAt,status:c.State.Status,restarts:c.RestartCount,ports:c.HostConfig.PortBindings,mounts:c.Mounts.map(m=>({type:m.Type,name:m.Name,source:m.Source,destination:m.Destination,rw:m.RW})).sort((a,b)=>a.destination.localeCompare(b.destination))})).sort((a,b)=>a.id.localeCompare(b.id));
const names=run('docker',['volume','ls','-q']).split(/\s+/).filter(Boolean);
const volumes=JSON.parse(run('docker',['volume','inspect',...names])).map(v=>({name:v.Name,created:v.CreatedAt,driver:v.Driver,mountpoint:v.Mountpoint})).sort((a,b)=>a.name.localeCompare(b.name));
const record={at:new Date().toISOString(),worktrees,containers,volumes};
if(process.argv[2]==='before')writeFileSync('D:/IBE160/tmp/125-before.json',JSON.stringify(record,null,2)+'\n');
else {
 const before=JSON.parse(readFileSync('D:/IBE160/tmp/125-before.json','utf8'));
 if(JSON.stringify(before.containers)!==JSON.stringify(containers)||JSON.stringify(before.volumes)!==JSON.stringify(volumes))throw Error('Runtime metadata changed');
 for(const old of before.worktrees.filter(w=>w.path!=='D:/IBE160')){
  const now=worktrees.find(w=>w.path===old.path);
  if(!now||now.head!==old.head||now.status!==old.status)throw Error('Worktree changed: '+old.path);
 }
 writeFileSync('D:/IBE160/docs/evidence/12-5-main-preservation.json',JSON.stringify({before,after:record,result:'passed'},null,2)+'\n');
}
console.log(JSON.stringify({worktrees:worktrees.map(w=>({path:w.path,head:w.head,dirtyEntries:w.status?w.status.split('\n').length:0})),containers:containers.length,volumes:volumes.length}));
