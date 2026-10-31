// Isolated synthetic qualification. Run from repository root with Node 24.
import {spawnSync} from 'node:child_process';
import {randomBytes, createHash} from 'node:crypto';
import {mkdirSync, writeFileSync, readFileSync, readdirSync} from 'node:fs';
import {resolve} from 'node:path';
import net from 'node:net';
const root=process.cwd(), id='ibe160-pm-s4-'+randomBytes(6).toString('hex');
const temp=resolve(root,'tmp',id), prior='5cee9e03d03d2c9c165c7f8fec64aa3e146959ab';
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
writeFileSync(resolve(temp,'password'),randomBytes(32).toString('hex'),{flag:'wx'});
const server=net.createServer();
await new Promise((ok,bad)=>{server.once('error',bad);server.listen(0,'127.0.0.1',ok)});
const port=server.address().port; await new Promise(ok=>server.close(ok));
writeFileSync(resolve(temp,'prior.tar'),run('git',['archive',prior,'backend']));
run('tar',['-xf',resolve(temp,'prior.tar'),'-C',resolve(temp,'prior')]);
const slash=p=>p.replaceAll('\\','/');
// Compose the existing pinned runtime and test dependency recipes, without
// depending on the historical locally prepared base tag in Dockerfile.test.
const gateDockerfile=readFileSync(resolve(root,'deploy/tablet/access_gate/Dockerfile'),'utf8')+'\n'+
  readFileSync(resolve(root,'deploy/tablet/access_gate/Dockerfile.test'),'utf8').split(/\r?\n/).filter(line=>!line.startsWith('FROM ')).join('\n');
const compose=`services:
  private-db:
    image: postgres:17-alpine@sha256:b0f9560a2de083e2cc7382e75f808c7381a32852a7ec49117deedb300e552b24
    environment:
      POSTGRES_DB: private_work
      POSTGRES_USER: private_work
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets: [db_password]
    volumes: [data:/var/lib/postgresql/data]
    healthcheck:
      test: [CMD, pg_isready, -U, private_work, -d, private_work]
      interval: 2s
      retries: 30
  private-api:
    image: ${id}-api
    build: ${slash(resolve(root,'backend'))}
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
    build:
      context: ${slash(root)}
      dockerfile_inline: |
${gateDockerfile.split(/\r?\n/).map(line=>'        '+line).join('\n')}
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
    read_only: true
    tmpfs: ['/tmp:mode=1777']
    depends_on:
      private-api: {condition: service_healthy}
      access-gate: {condition: service_started}
  prior:
    image: ${id}-api
    profiles: [compatibility]
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
for(const path of ['backend','frontend/src','deploy/tablet'])fingerprint(path);
for(const name of ['scripts/verify-password-s4.mjs','scripts/password-s4-probe.py','scripts/password-s4-gate.py','frontend/package-lock.json','frontend/package.json','frontend/tsconfig.json','.dockerignore'])fingerprints[name]=createHash('sha256').update(readFileSync(resolve(root,name))).digest('hex');
const dc=(...args)=>run('docker',['compose','-p',id,'-f',file,...args]);
const probe=phase=>{const out=dc('exec','-T','private-api','python','/probe/password-s4-probe.py',phase);process.stdout.write(out)};
const dump=name=>writeFileSync(resolve(temp,name+'.dump'),dc('exec','-T','private-db','pg_dump','-U','private_work','-d','private_work','-Fc'));
const restore=name=>run('docker',['compose','-p',id,'-f',file,'exec','-T','private-db','pg_restore','-U','private_work','-d','private_work','--clean','--if-exists','--exit-on-error'],{input:readFileSync(resolve(temp,name+'.dump'))});
console.log(`S4 project ${id}; loopback ${port}; ignored artifacts ${temp}`);
try {
  dc('up','-d','--build','--wait','--wait-timeout','120');
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
    fingerprints,images:JSON.parse(dc('images','--format','json').toString()),
    results:JSON.parse(readFileSync(resolve(temp,'results.json')))};
  writeFileSync(resolve(temp,'evidence.json'),JSON.stringify(evidence,null,2));
  console.log('PASS S4 combined qualification; sanitized evidence.json saved; synthetic volumes retained.');
} finally {
  dc('stop');
}
