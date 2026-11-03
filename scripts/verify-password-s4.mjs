// Isolated synthetic qualification. Qualified on Windows Docker Desktop with Node 24.
// Native Linux needs a separately reviewed UID10001-writable task state mount;
// never make the secret-bearing scratch directory world-writable.
import {spawnSync} from 'node:child_process';
import {randomBytes, createHash} from 'node:crypto';
import {mkdirSync, writeFileSync, readFileSync, readdirSync} from 'node:fs';
import {resolve} from 'node:path';
import net from 'node:net';
if(process.platform!=='win32') throw new Error('S4 runner qualified only on Windows Docker Desktop; native state mount ownership is not qualified');
const root=process.cwd(), id='ibe160-pm-s4-'+randomBytes(6).toString('hex');
const temp=resolve(root,'tmp',id), prior='15011042b1fe093becbe68177e6396e456b1f35f';
mkdirSync(temp,{recursive:true}); mkdirSync(resolve(temp,'prior'));
function run(cmd,args,options={}) {
  const r=spawnSync(cmd,args,{cwd:root,encoding:null,maxBuffer:32*1024*1024,...options});
  if(r.status!==0) {
    const safe=r.stderr?.toString().split('\n').find(line=>/^FAIL (S4 invariant failed: [a-zA-Z0-9 /_-]+|[A-Za-z]+)$/.test(line));
    if(safe) console.error(safe);
    throw new Error(`Qualification command failed: ${cmd} ${args.slice(0,3).join(' ')}; diagnostics withheld (exit ${r.status})`);
  }
  return r.stdout;
}
writeFileSync(resolve(temp,'bootstrap-password'),randomBytes(32).toString('hex'),{flag:'wx'});
writeFileSync(resolve(temp,'password'),randomBytes(32).toString('hex'),{flag:'wx'});
const server=net.createServer();
await new Promise((ok,bad)=>{server.once('error',bad);server.listen(0,'127.0.0.1',ok)});
const port=server.address().port; await new Promise(ok=>server.close(ok));
writeFileSync(resolve(temp,'prior.tar'),run('git',['archive',prior,'backend']));
run('tar',['-xf',resolve(temp,'prior.tar'),'-C',resolve(temp,'prior')]);
const slash=p=>p.replaceAll('\\','/');
const compose=`services:
  private-db:
    image: ${id}-postgres
    build:
      context: ${slash(root)}
      dockerfile: deploy/ubuntu/Dockerfile.postgres
    user: postgres
    read_only: true
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    pids_limit: 128
    tmpfs: [/tmp:mode=1777, /var/run/postgresql:mode=1777]
    environment:
      POSTGRES_DB: private_work
      POSTGRES_USER: tablet_bootstrap
      POSTGRES_PASSWORD_FILE: /run/secrets/bootstrap_password
    secrets: [bootstrap_password, tablet_postgres_password]
    volumes:
      - data:/var/lib/postgresql/data
      - ${slash(resolve(root,"deploy/tablet/init-private-role.sql"))}:/docker-entrypoint-initdb.d/010-private-role.sql:ro
    healthcheck:
      test: [CMD, pg_isready, -U, private_work, -d, private_work]
      interval: 2s
      retries: 30
  private-api:
    image: ${id}-api
    build: ${slash(resolve(root,'backend'))}
    user: '10001:10001'
    read_only: true
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    pids_limit: 128
    tmpfs: ['/tmp:size=128m,mode=1777']
    environment: &environment
      APP_MODE: private-local
      PRIVATE_DATABASE_URL: postgresql://private_work@private-db/private_work
      PRIVATE_DATABASE_PASSWORD_FILE: /run/secrets/db_password
      PRIVATE_ORIGIN: https://bus.owner-domain.no
      PRIVATE_HTTPS_DEPLOYMENT: '1'
      PRIVATE_TEST_PROJECT: ibe160-private-tests
      PRIVATE_TEST_ORIGIN: https://bus.owner-domain.no
      PYTHONPATH: /app:/app/tests
    secrets: [db_password]
    volumes:
      - ${slash(resolve(root,'scripts'))}:/probe:ro
      - ${slash(temp)}:/state
    healthcheck:
      test: [CMD, python, -c, "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 2s
      retries: 30
    depends_on:
      private-db: {condition: service_healthy}
  access-gate:
    image: ${id}-gate
    user: '10001:10001'
    read_only: true
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    pids_limit: 32
    tmpfs: ['/tmp:size=1m,mode=1777']
    command: [python, /probe/password-s4-gate.py]
    environment: {PYTHONPATH: /gate-test}
    volumes:
      - ${slash(resolve(root,'scripts'))}:/probe:ro
      - ${slash(resolve(root,'deploy/tablet/access_gate'))}:/gate-test:ro
  gateway:
    image: ${id}-gateway
    build:
      context: ${slash(root)}
      dockerfile: deploy/tablet/Dockerfile
    environment: {TABLET_HOST: bus.owner-domain.no}
    ports: ['127.0.0.1:${port}:8080']
    user: '101:101'
    read_only: true
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    pids_limit: 64
    tmpfs: ['/tmp:size=32m,mode=1777']
    depends_on:
      private-api: {condition: service_healthy}
      access-gate: {condition: service_started}
  prior:
    image: ${id}-api
    profiles: [compatibility]
    user: '10001:10001'
    read_only: true
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    pids_limit: 128
    tmpfs: ['/tmp:size=128m,mode=1777']
    environment: *environment
    secrets: [db_password]
    volumes:
      - ${slash(resolve(temp,'prior/backend'))}:/app:ro
      - ${slash(resolve(root,'scripts'))}:/probe:ro
      - ${slash(temp)}:/state
    command: [python, /probe/password-s4-probe.py, prior]
networks:
  default: {internal: true}
volumes:
  data:
secrets:
  bootstrap_password:
    file: ${slash(resolve(temp,'bootstrap-password'))}
  tablet_postgres_password:
    file: ${slash(resolve(temp,'password'))}
  db_password:
    file: ${slash(resolve(temp,'password'))}
`;
const file=resolve(temp,'compose.yaml');writeFileSync(file,compose);
const fingerprints={};
function fingerprint(path) {
  for(const entry of readdirSync(resolve(root,path),{withFileTypes:true})) {
    if(['__pycache__','node_modules','.pytest_cache'].includes(entry.name))continue;
    const name=path+'/'+entry.name;
    if(entry.isDirectory())fingerprint(name);
    else fingerprints[name]=createHash('sha256').update(readFileSync(resolve(root,name))).digest('hex');
  }
}
for(const path of ['backend','frontend/src','deploy/tablet','deploy/ubuntu'])fingerprint(path);
for(const name of ['scripts/verify-password-s4.mjs','scripts/password-s4-probe.py','scripts/password-s4-gate.py','frontend/package-lock.json','frontend/package.json','frontend/tsconfig.json','.dockerignore'])fingerprints[name]=createHash('sha256').update(readFileSync(resolve(root,name))).digest('hex');
const dc=(...args)=>run('docker',['compose','-p',id,'-f',file,...args]);
const probe=phase=>{const out=dc('exec','-T','private-api','python','/probe/password-s4-probe.py',phase);process.stdout.write(out)};
const dump=name=>writeFileSync(resolve(temp,name+'.dump'),dc('exec','-T','private-db','pg_dump','-U','private_work','-d','private_work','-Fc'));
const restore=name=>run('docker',['compose','-p',id,'-f',file,'exec','-T','private-db','pg_restore','-U','private_work','-d','private_work','--clean','--if-exists','--exit-on-error'],{input:readFileSync(resolve(temp,name+'.dump'))});
console.log(`S4 project ${id}; loopback ${port}; ignored artifacts ${temp}`);
try {
  run('docker',['build','-t',id+'-gate-runtime','-f','deploy/tablet/access_gate/Dockerfile','.']);
  run('docker',['build','-t',id+'-gate','--build-arg','GATE_IMAGE='+id+'-gate-runtime','-f','deploy/tablet/access_gate/Dockerfile.test','.']);
  const gateBuild={runtimeImage:run('docker',['image','inspect','--format','{{.Id}}',id+'-gate-runtime']).toString().trim(),runtimeTag:id+'-gate-runtime',testedOverlayImage:run('docker',['image','inspect','--format','{{.Id}}',id+'-gate']).toString().trim(),testDockerfile:'deploy/tablet/access_gate/Dockerfile.test',buildArg:'GATE_IMAGE='+id+'-gate-runtime'};
  dc('up','-d','--build','--wait','--wait-timeout','120');
  const runtime={};
  for(const [service,user] of Object.entries({'private-db':'postgres','private-api':'10001:10001','gateway':'101:101','access-gate':'10001:10001'})) {
    const info=JSON.parse(run('docker',['inspect',dc('ps','-q',service).toString().trim()]).toString())[0];
    const h=info.HostConfig;
    const expectedPids={'private-db':128,'private-api':128,'gateway':64,'access-gate':32}[service];
    if(h.PidsLimit!==expectedPids || info.Config.User!==user || !h.ReadonlyRootfs || !h.CapDrop.includes('ALL') || !h.SecurityOpt.includes('no-new-privileges:true') || h.Privileged) throw new Error('Runtime restriction assertion failed');
    runtime[service]={user:info.Config.User,readOnly:h.ReadonlyRootfs,capDrop:h.CapDrop,securityOpt:h.SecurityOpt,pidsLimit:h.PidsLimit,privileged:h.Privileged,image:info.Image};
  }
  probe('role');
  probe('seed');
  dc('stop','gateway','private-api');
  process.stdout.write(dc('run','--rm','--no-deps','private-api','python','/probe/password-s4-probe.py','pre-schema'));
  dc('up','-d','--wait','private-api','gateway');probe('upgrade');dump('pre');
  probe('journeys'); dump('post');
  dc('restart','private-api'); dc('up','-d','--wait','--wait-timeout','120','private-api'); probe('restart');
  // No HTTP traffic during restore; invalidation happens before either service restarts.
  probe('scan-db'); dc('stop','gateway','private-api');
  restore('pre');
  process.stdout.write(dc('run','--rm','--no-deps','private-api','python','/probe/password-s4-probe.py','invalidate-pre'));
  process.stdout.write(dc('run','--rm','--no-deps','prior'));
  process.stdout.write(dc('run','--rm','--no-deps','private-api','python','/probe/password-s4-probe.py','settle'));
  dc('up','-d','--wait','private-api','gateway'); probe('restored');
  probe('scan-db'); dc('stop','gateway','private-api'); restore('post');
  process.stdout.write(dc('run','--rm','--no-deps','private-api','python','/probe/password-s4-probe.py','invalidate-post'));
  process.stdout.write(dc('run','--rm','--no-deps','prior'));
  dc('up','-d','--wait','private-api','gateway'); probe('post-restored');
  for(const service of ['private-api','gateway','access-gate','private-db']) {
    const logs=dc('logs','--no-color',service);
    // Scan inside container without emitting marker values or raw logs.
    run('docker',['compose','-p',id,'-f',file,'exec','-T','private-api','python','/probe/password-s4-probe.py','scan'],{input:logs});
  }
  const evidence={project:id,port,source:run('git',['rev-parse','HEAD']).toString().trim(),prior,
    docker:run('docker',['version','--format','{{.Server.Version}}']).toString().trim(),node:process.version,
    fingerprints,runtime,gateBuild,images:JSON.parse(dc('images','--format','json').toString()),
    results:JSON.parse(readFileSync(resolve(temp,'results.json')))};
  writeFileSync(resolve(temp,'evidence.json'),JSON.stringify(evidence,null,2));
  console.log('PASS S4 combined qualification; sanitized evidence.json saved; synthetic volumes retained.');
} finally {
  dc('stop');
}
