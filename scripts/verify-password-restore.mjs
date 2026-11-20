// Real disposable PostgreSQL/image journey; mocked host lifecycle tested separately.
import {spawn,spawnSync} from 'node:child_process';
import {randomBytes, createHash} from 'node:crypto';
import {mkdirSync, writeFileSync, readFileSync} from 'node:fs';
import {resolve} from 'node:path';
const root=process.cwd(), id='ibe160-pm-restore-'+randomBytes(6).toString('hex');
const temp=resolve(root,'tmp',id), slash=p=>p.replaceAll('\\','/');
mkdirSync(temp,{recursive:true});
const diagnostics=[];
function run(cmd,args,opts={}) {
  const r=spawnSync(cmd,args,{cwd:root,maxBuffer:64*1024*1024,...opts});
  diagnostics.push(r.stderr??Buffer.alloc(0));
  if(!args.includes('pg_dump') && !args.includes('pg_restore'))diagnostics.push(r.stdout??Buffer.alloc(0));
  if(r.status!==0) {
    const safe=(r.stderr?.toString()??'').split('\n').filter(line=>/^(FAILED \(|Ran \d+ tests|FAIL restore invariant|ERROR: test_[a-z_]+ |FAIL: test_[a-z_]+ )/.test(line));
    for(const line of safe)console.error(line);
    throw new Error(`Restore qualification failed (${cmd}, exit ${r.status}); raw diagnostics withheld`);
  }
  return r.stdout;
}
for(const name of ['bootstrap','password'])writeFileSync(resolve(temp,name),randomBytes(32).toString('hex'),{flag:'wx'});
const compose={services:{
  'private-db':{image:id+'-postgres',build:{context:root,dockerfile:'deploy/ubuntu/Dockerfile.postgres'},user:'postgres',read_only:true,cap_drop:['ALL'],security_opt:['no-new-privileges:true'],pids_limit:128,tmpfs:['/tmp:mode=1777','/var/run/postgresql:mode=1777'],environment:{POSTGRES_DB:'private_work',POSTGRES_USER:'tablet_bootstrap',POSTGRES_PASSWORD_FILE:'/run/secrets/bootstrap'},secrets:['bootstrap','tablet_postgres_password'],volumes:['data:/var/lib/postgresql/data',slash(resolve(root,'deploy/tablet/init-private-role.sql'))+':/docker-entrypoint-initdb.d/010-private-role.sql:ro'],healthcheck:{test:['CMD','pg_isready','-U','private_work','-d','private_work'],interval:'2s',retries:30}},
  'private-api':{image:id+'-api',build:resolve(root,'backend'),user:'10001:10001',read_only:true,cap_drop:['ALL'],security_opt:['no-new-privileges:true'],pids_limit:128,tmpfs:['/tmp:size=128m,mode=1777'],environment:{APP_MODE:'private-local',PRIVATE_DATABASE_URL:'postgresql://private_work@private-db/private_work',PRIVATE_DATABASE_PASSWORD_FILE:'/run/secrets/tablet_postgres_password',PRIVATE_ORIGIN:'http://127.0.0.1:15440',PRIVATE_LOOPBACK_DEVELOPMENT:'1',PRIVATE_TEST_PROJECT:'ibe160-private-tests',PRIVATE_TEST_ORIGIN:'http://127.0.0.1:15440',PYTHONPATH:'/app:/app/tests'},secrets:['tablet_postgres_password'],volumes:[slash(resolve(root,'scripts'))+':/probe:ro',slash(resolve(root,'deploy/ubuntu'))+':/host-tests:ro',slash(temp)+':/state'],depends_on:{'private-db':{condition:'service_healthy'}},healthcheck:{test:['CMD','python','-c',"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"],interval:'2s',retries:30}}
},networks:{default:{internal:true,ipam:{config:[{subnet:`10.247.${randomBytes(1)[0]}.0/28`}]}}},volumes:{data:{}},secrets:{bootstrap:{file:resolve(temp,'bootstrap')},tablet_postgres_password:{file:resolve(temp,'password')}}};
const file=resolve(temp,'compose.json');writeFileSync(file,JSON.stringify(compose));
const dc=(...args)=>run('docker',['compose','-p',id,'-f',file,...args]);
const offline=(...args)=>dc('run','--rm','--no-deps','-T','private-api',...args);
const probe=phase=>process.stdout.write(offline('python','/probe/password-restore-probe.py',phase));
const sql=text=>run('docker',['compose','-p',id,'-f',file,'exec','-T','private-db','psql','-X','-U','tablet_bootstrap','-d','private_work','-v','ON_ERROR_STOP=1'],{input:text});
const dump=name=>{const value=dc('exec','-T','private-db','pg_dump','-U','tablet_bootstrap','-d','private_work','-Fc','--no-owner','--no-acl');writeFileSync(resolve(temp,name+'.dump'),value);return value;};
function replacement(archive) {
  const base=['compose','-p',id,'-f',file,'exec','-T','private-db','pg_restore'];
  const toc=run('docker',[...base,'--list'],{input:archive}).toString();
  const body=run('docker',[...base,'--no-owner','--no-privileges','--file=-'],{input:archive});
  writeFileSync(resolve(temp,'toc.txt'),toc);writeFileSync(resolve(temp,'archive.sql'),body);
  offline('python','/probe/password-restore-helper.py');
  return readFileSync(resolve(temp,'replacement.sql'));
}
console.log('Restore qualification project '+id);
try {
  dc('up','-d','--build','--wait','--wait-timeout','120');
  // Real DB transaction rollback/recovery/migration tests; stdout contains only test counts.
  process.stdout.write(dc('exec','-T','private-api','python','-m','pytest','-q','--tb=no','tests/test_password_restore.py'));
  dc('run','--rm','--no-deps','-T','--user','0:0','private-api','python','-m','unittest','discover','-s','/host-tests','-p','test*py');
  console.log('PASS mocked Linux host suites');
  probe('seed');
  probe('guards');probe('unsupported');
  dc('stop','private-api');
  const current=dump('current');
  const blocker=spawn('docker',['compose','-p',id,'-f',file,'exec','-T','-e','PGAPPNAME=synthetic-restore-blocker','private-db','psql','-U','tablet_bootstrap','-d','private_work','-c','BEGIN; LOCK TABLE accounts IN ACCESS EXCLUSIVE MODE; SELECT pg_sleep(20); COMMIT;'],{stdio:'ignore'});
  try {
    let locked=false;
    for(let n=0;n<50;n++) {
      locked=dc('exec','-T','private-db','psql','-U','tablet_bootstrap','-d','private_work','-Atc',"SELECT count(*) FROM pg_locks WHERE relation='accounts'::regclass AND mode='AccessExclusiveLock' AND granted").toString().trim()==='1';
      if(locked)break;
      await new Promise(resolve=>setTimeout(resolve,100));
    }
    if(!locked)throw new Error('Synthetic lock setup failed');
    const bounded=replacement(current), started=Date.now();
    const rejected=spawnSync('docker',['compose','-p',id,'-f',file,'exec','-T','private-db','psql','-X','-U','tablet_bootstrap','-d','private_work','-v','ON_ERROR_STOP=1'],{input:bounded});
    diagnostics.push(rejected.stderr??Buffer.alloc(0));
    if(rejected.status===0 || Date.now()-started<4500 || Date.now()-started>10000)throw new Error('Generated restore lock timeout failed');
    console.log('PASS generated SQL real five-second lock timeout');
  } finally {
    sql("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE application_name='synthetic-restore-blocker'");
    await new Promise(resolve=>{if(blocker.exitCode!==null)resolve();else blocker.once('exit',resolve)});
  }
  sql('DROP INDEX sessions_expiry; ALTER TABLE accounts DROP CONSTRAINT accounts_username_key;');
  dump('malformed');
  sql('CREATE INDEX sessions_expiry ON sessions(expires_at); ALTER TABLE accounts ADD CONSTRAINT accounts_username_key UNIQUE(username);');
  probe('pre015'); const prior=dump('pre015');
  const evidence={project:id,source:run('git',['rev-parse','HEAD']).toString().trim(),images:JSON.parse(dc('images','--format','json').toString()),archives:{},checks:[]};
  for(const [name,archive] of [['pre015',prior],['current',current]]) {
    // A newer unknown table must disappear with schema replacement.
    sql('CREATE TABLE synthetic_leftover(id integer); INSERT INTO synthetic_leftover VALUES(1);');
    const transaction=replacement(archive);
    const before=dc('exec','-T','private-db','pg_dump','-U','tablet_bootstrap','-d','private_work','--data-only','--no-owner','--no-acl').toString().replace(/^\\(?:un)?restrict .*$/gm,'');
    const bad=Buffer.from(transaction.toString().replace(/COMMIT;\s*$/,'SELECT missing_synthetic_restore_column;\nCOMMIT;'));
    const failed=spawnSync('docker',['compose','-p',id,'-f',file,'exec','-T','private-db','psql','-X','-U','tablet_bootstrap','-d','private_work','-v','ON_ERROR_STOP=1'],{input:bad});
    if(failed.status===0)throw new Error('Failed replacement unexpectedly committed');
    const after=dc('exec','-T','private-db','pg_dump','-U','tablet_bootstrap','-d','private_work','--data-only','--no-owner','--no-acl').toString().replace(/^\\(?:un)?restrict .*$/gm,'');
    if(before!==after)throw new Error('Failed replacement changed data');
    sql(transaction);
    const leftover=dc('exec','-T','private-db','psql','-U','tablet_bootstrap','-d','private_work','-Atc',"SELECT count(*) FROM pg_tables WHERE tablename='synthetic_leftover'").toString().trim();
    if(leftover!=='0')throw new Error('Replacement retained newer table');
    probe('journey');
    dc('up','-d','--wait','--wait-timeout','120','private-api');
    dc('restart','private-api');dc('up','-d','--wait','--wait-timeout','120','private-api');
    probe('ordinary-restart');dc('stop','private-api');
    evidence.archives[name]={sha256:createHash('sha256').update(archive).digest('hex'),bytes:archive.length};
    evidence.checks.push(name+': atomic failed replacement rollback, no leftover table, migration business equality, all old passwords/sessions/proofs rejected, independent A/B recovery, ordinary migration preserves credentials');
  }
  const logs=Buffer.concat([dc('logs','--no-color'),...diagnostics]);
  process.stdout.write(run('docker',['compose','-p',id,'-f',file,'run','--rm','--no-deps','-T','private-api','python','/probe/password-restore-probe.py','scan'],{input:logs}));
  evidence.fingerprints={};
  for(const p of ['backend/app/restore.py','backend/app/manage.py','deploy/ubuntu/bussassistentctl.py','deploy/ubuntu/compose.yaml','scripts/verify-password-restore.mjs','scripts/password-restore-probe.py'])evidence.fingerprints[p]=createHash('sha256').update(readFileSync(resolve(root,p))).digest('hex');
  writeFileSync(resolve(temp,'evidence.json'),JSON.stringify(evidence,null,2));
  console.log('PASS restore qualification; sanitized evidence '+resolve(temp,'evidence.json'));
} finally {dc('stop');}
