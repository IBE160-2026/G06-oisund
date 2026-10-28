// Executed recipe checks. This deliberately resets ONLY the guarded submission data.
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash, randomUUID } from 'node:crypto';
import { ROOT, PROJECT } from './submission.mjs';

const docker = args => execFileSync('docker', args, { cwd: ROOT, encoding: 'utf8', timeout: 180000 });
const compose = ['compose', '--project-directory', ROOT, '-p', PROJECT, '-f', ROOT + '/compose.submission.yaml'];
const action = name => execFileSync(process.execPath, ['scripts/submission.mjs', name], { cwd: ROOT, encoding: 'utf8', timeout: 180000 });
const python = (service, program) => execFileSync('docker', [...compose, 'exec', '-T', service, 'python', '-'], { cwd: ROOT, encoding: 'utf8', input: program, timeout: 30000 });
const protectedContainers = () => {
  const ids = docker(['ps', '-aq']).trim().split(/\s+/).filter(Boolean);
  return ids.length ? JSON.parse(docker(['inspect', ...ids])).filter(c => c.Config.Labels?.['com.docker.compose.project'] !== PROJECT).map(c => ({ id: c.Id, image: c.Image, started: c.State.StartedAt, state: c.State.Status, volumes:c.Mounts.filter(m=>m.Type==='volume').map(m=>({name:m.Name,destination:m.Destination})).sort((a,b)=>a.name.localeCompare(b.name)) })).sort((a,b) => a.id.localeCompare(b.id)) : [];
};
const protectedVolumes = () => {
  const names = docker(['volume','ls','-q']).trim().split(/\s+/).filter(Boolean);
  return names.length ? JSON.parse(docker(['volume','inspect',...names])).filter(v=>v.Labels?.['com.docker.compose.project']!==PROJECT).map(v=>({name:v.Name,driver:v.Driver,scope:v.Scope,createdAt:v.CreatedAt})).sort((a,b)=>a.name.localeCompare(b.name)) : [];
};
const privatePrefix = 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\n';
const fictionalPrefix = `import os\nfrom pathlib import Path\nfrom urllib.parse import quote\nassert os.environ['SUBMISSION_PROJECT']=='ibe160-submission'\nos.environ['DATABASE_URL']='postgresql://fictional:'+quote(Path('/run/secrets/submission_password').read_text().strip(),safe='')+'@db/fictional_assessment'\nfrom app.storage import database\n`;
function snapshot(service, guardUsername = null) {
  const prefix = service === 'private-api' ? privatePrefix : fictionalPrefix;
  const privateGuard = guardUsername ? `assert conn.execute("SELECT username FROM accounts WHERE username NOT LIKE 'synthetic-%%'").fetchall()==[{'username':${JSON.stringify(guardUsername)}}]` : 'require_synthetic_accounts(conn)';
  return JSON.parse(python(service, prefix + `import json,hashlib\nfrom psycopg import sql\nresult={}\nwith database() as conn:\n ${service === 'private-api' ? privateGuard : "assert conn.execute('SELECT current_database() AS n').fetchone()['n']=='fictional_assessment'"}\n for table in conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename").fetchall():\n  rows=conn.execute(sql.SQL('SELECT row_to_json(t) AS row FROM {} t').format(sql.Identifier(table['tablename']))).fetchall()\n  encoded=sorted(json.dumps(row['row'],sort_keys=True) for row in rows)\n  result[table['tablename']]={'count':len(rows),'hash':hashlib.sha256(json.dumps(encoded).encode()).hexdigest()}\nprint(json.dumps(result))\n`));
}
const secretHashes = () => ['postgres-password', 'account.json'].map(name => createHash('sha256').update(readFileSync(ROOT + '/.private-runtime/submission/' + name)).digest('hex'));

const result = { source: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: ROOT, encoding: 'utf8' }).trim(), started: new Date().toISOString(), checks: [] };
mkdirSync(ROOT + '/tmp', { recursive: true });
try {
  action('status');
  const protectedBefore = protectedContainers(), volumesBefore = protectedVolumes(), secretsBefore = secretHashes();
  const guardId = randomUUID(), guardUsername = 'operator-submission-guard-' + guardId, bucket = 'submission-guard-' + guardId;
  python('private-api', privatePrefix + `from app.auth import DUMMY,digest\nfrom uuid import UUID\nwith database() as conn:\n conn.execute('LOCK TABLE accounts IN ACCESS EXCLUSIVE MODE')\n require_synthetic_accounts(conn)\n conn.execute('INSERT INTO accounts VALUES (%s,%s,%s)',(UUID(${JSON.stringify(guardId)}),${JSON.stringify(guardUsername)},DUMMY))\n conn.execute('INSERT INTO sessions(token_hash,owner) VALUES (%s,%s)',(digest(${JSON.stringify(guardId)}),UUID(${JSON.stringify(guardId)})))\n conn.execute("INSERT INTO login_limits VALUES (%s,7,clock_timestamp()+interval '5 minutes')",(${JSON.stringify(bucket)},))\n`);
  try {
    const privateBefore = snapshot('private-api', guardUsername), fictionalBefore = snapshot('api');
    const refused = spawnSync(process.execPath, ['scripts/submission.mjs','reset'], {cwd:ROOT,encoding:'utf8',timeout:30000});
    assert.equal(refused.status,1);
    assert.match(refused.stderr,/disposable synthetic-only private database/);
    assert.deepEqual(snapshot('private-api', guardUsername),privateBefore);
    assert.deepEqual(snapshot('api'),fictionalBefore);
    result.ordinaryAccountRefusal = {exitCode:refused.status,privateUnchanged:true,fictionalUnchanged:true};
    result.checks.push('Whole Node reset command refuses an ordinary guard account before either database changes.');
  } finally {
    python('private-api', privatePrefix + `from uuid import UUID\nwith database() as conn:\n conn.execute('DELETE FROM sessions WHERE owner=%s',(UUID(${JSON.stringify(guardId)}),))\n conn.execute('DELETE FROM accounts WHERE id=%s AND username=%s',(UUID(${JSON.stringify(guardId)}),${JSON.stringify(guardUsername)}))\n conn.execute('DELETE FROM login_limits WHERE bucket=%s',(${JSON.stringify(bucket)},))\n`);
  }
  // Remove expired leftovers from other disposable suites before measuring
  // preservation of newly acknowledged, unexpired state.
  action('reset');
  // Populate acknowledged synthetic state through the actual HTTP API, not SQL fixtures.
  python('private-api', `import json,uuid,httpx
from pathlib import Path
account=json.loads(Path('/run/secrets/submission_account').read_text())
with httpx.Client(base_url='http://127.0.0.1:8000') as client:
 def post(path,body):
  proof=client.get('/auth/csrf').json()['csrf_token']
  response=client.post(path,headers={'Origin':'http://127.0.0.1:15325','X-CSRF-Token':proof},json=body)
  assert response.status_code==200,(path,response.status_code)
  return response.json()
 post('/auth/login',account)
 member=str(uuid.uuid4())
 operation=post('/draft-operations',{})
 draft=post('/drafts',{'operation_id':operation['operation_id'],'expected_revision':0,'draft':{'service_date':'2030-03-01','activities':[{'id':member,'type':'trip','trip':'SYN-501','line':'731','direction':'Nord','from_place':'Fiktiv start','to_place':'Fiktiv slutt','start':'2030-03-01T08:00+01:00','end':'2030-03-01T08:15+01:00'}]}})
 review=post('/workday-reviews',{'draft_id':draft['id'],'expected_revision':1})
 plan=post('/drafts/'+draft['id']+'/confirm',{'operation_id':review['operation_id'],'expected_revision':1,'acknowledgements':[u['id'] for u in review['unknowns']],'classifications':{}})
 base='/workdays/'+plan['id']
 def command(**values): return {'operation_id':str(uuid.uuid4()),'expected_revision':0,**values}
 post(base+'/selection',command(activity_id=member))
 post(base+'/physical-bus',command(physical_bus='RUNTIME-125'))
 post(base+'/start',command())
 post(base+'/outcome',command(expected_lifecycle_revision=1,activity_id=member,outcome='completed'))
 issued=post('/notice-operations',{})
 post('/notices',{'operation_id':issued['operation_id'],'expected_revision':0,'content':{'title':'Syntetisk varighetsprove','line_tags':['731'],'source_note':'Fiktiv oppgavekilde','valid_until':'2030-03-03'}})
 post(base+'/close',{'operation_id':str(uuid.uuid4()),'expected_revision':1,'expected_outcome_revision':1,'action':'ended'})
print('Acknowledged synthetic draft, plan, bus, selection, start, outcome, notice, closure and receipts created through HTTP.')
`);
  const before = snapshot('private-api'), fictionalBefore = snapshot('api');
  assert(before.drafts.count >= 1 && before.sessions.count >= 1);
  for (const table of ['workdays','workday_lifecycles','workday_buses','workday_selections','workday_outcomes','workday_start_operations','workday_outcome_operations','workday_close_operations','workday_notices','account_notice_operations']) assert(before[table].count>0,table+' must be populated');
  action('stop'); action('start');
  assert.deepEqual(snapshot('private-api'), before);
  assert.deepEqual(snapshot('api'), fictionalBefore);
  result.checks.push('Stop/start and repeated migrations/initialization preserve every private and fictional table row, including fixed deadlines.');
  action('restart');
  assert.deepEqual(snapshot('private-api'), before);
  assert.deepEqual(snapshot('api'), fictionalBefore);
  result.checks.push('Restart preserves every private and fictional table row.');
  action('reset');
  const after = snapshot('private-api'), fictionalAfter = snapshot('api');
  for (const [name, value] of Object.entries(after)) {
    if (name === 'accounts') assert.equal(value.count, 1);
    else if (['private_migrations', 'security_settings'].includes(name)) assert.deepEqual(value, before[name]);
    else assert.equal(value.count, 0, name + ' must be empty after reset');
  }
  assert.equal(fictionalAfter.fictional_days.count, 1);
  assert.equal(fictionalAfter.creation_operations.count, 1);
  assert.notEqual(fictionalAfter.fictional_days.hash, fictionalBefore.fictional_days.hash);
  assert.deepEqual(secretHashes(), secretsBefore);
  assert.deepEqual(protectedContainers(), protectedBefore);
  assert.deepEqual(protectedVolumes(), volumesBefore);
  result.privateCountsBefore = Object.fromEntries(Object.entries(before).map(([key,value]) => [key,value.count]));
  result.privateCountsAfter = Object.fromEntries(Object.entries(after).map(([key,value]) => [key,value.count]));
  result.protectedContainerCount = protectedBefore.length;
  result.protectedVolumeCount = volumesBefore.length;
  result.checks.push('Reset removes synthetic business data/sessions, keeps migration/security settings and generated secrets, reprovisions one account and reseeds exactly one fictional day.');
  result.checks.push('All unrelated container IDs/images/start times/states, volume identities/creation times and container-volume mount relationships remain identical.');
  result.passed = true;
} catch (error) {
  result.passed = false; result.error = error.message; process.exitCode = 1;
} finally {
  result.finished = new Date().toISOString();
  writeFileSync(ROOT + '/tmp/submission-runtime-check.json', JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
}
