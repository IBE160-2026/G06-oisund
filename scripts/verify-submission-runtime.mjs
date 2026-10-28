// Executed recipe checks. This deliberately resets ONLY the guarded submission data.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { ROOT, PROJECT } from './submission.mjs';

const docker = args => execFileSync('docker', args, { cwd: ROOT, encoding: 'utf8', timeout: 180000 });
const compose = ['compose', '--project-directory', ROOT, '-p', PROJECT, '-f', ROOT + '/compose.submission.yaml'];
const action = name => execFileSync(process.execPath, ['scripts/submission.mjs', name], { cwd: ROOT, encoding: 'utf8', timeout: 180000 });
const python = (service, program) => execFileSync('docker', [...compose, 'exec', '-T', service, 'python', '-'], { cwd: ROOT, encoding: 'utf8', input: program, timeout: 30000 });
const protectedContainers = () => {
  const ids = docker(['ps', '-aq']).trim().split(/\s+/).filter(Boolean);
  return ids.length ? JSON.parse(docker(['inspect', ...ids])).filter(c => c.Config.Labels?.['com.docker.compose.project'] !== PROJECT).map(c => ({ id: c.Id, image: c.Image, started: c.State.StartedAt, state: c.State.Status })).sort((a,b) => a.id.localeCompare(b.id)) : [];
};
const privatePrefix = 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\n';
const fictionalPrefix = `import os\nfrom pathlib import Path\nfrom urllib.parse import quote\nassert os.environ['SUBMISSION_PROJECT']=='ibe160-submission'\nos.environ['DATABASE_URL']='postgresql://fictional:'+quote(Path('/run/secrets/submission_password').read_text().strip(),safe='')+'@db/fictional_assessment'\nfrom app.storage import database\n`;
function snapshot(service) {
  const prefix = service === 'private-api' ? privatePrefix : fictionalPrefix;
  return JSON.parse(python(service, prefix + `import json,hashlib\nfrom psycopg import sql\nresult={}\nwith database() as conn:\n ${service === 'private-api' ? 'require_synthetic_accounts(conn)' : "assert conn.execute('SELECT current_database() AS n').fetchone()['n']=='fictional_assessment'"}\n for table in conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename").fetchall():\n  rows=conn.execute(sql.SQL('SELECT row_to_json(t) AS row FROM {} t').format(sql.Identifier(table['tablename']))).fetchall()\n  encoded=sorted(json.dumps(row['row'],sort_keys=True) for row in rows)\n  result[table['tablename']]={'count':len(rows),'hash':hashlib.sha256(json.dumps(encoded).encode()).hexdigest()}\nprint(json.dumps(result))\n`));
}
const secretHashes = () => ['postgres-password', 'account.json'].map(name => createHash('sha256').update(readFileSync(ROOT + '/.private-runtime/submission/' + name)).digest('hex'));

const result = { source: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: ROOT, encoding: 'utf8' }).trim(), started: new Date().toISOString(), checks: [] };
mkdirSync(ROOT + '/tmp', { recursive: true });
try {
  action('status');
  const protectedBefore = protectedContainers(), secretsBefore = secretHashes();
  // Populate acknowledged synthetic state through the actual HTTP API, not SQL fixtures.
  python('private-api', `import json,uuid,httpx\nfrom pathlib import Path\naccount=json.loads(Path('/run/secrets/submission_account').read_text())\nwith httpx.Client(base_url='http://127.0.0.1:8000') as client:\n def post(path,body):\n  proof=client.get('/auth/csrf').json()['csrf_token']\n  response=client.post(path,headers={'Origin':'http://127.0.0.1:15325','X-CSRF-Token':proof},json=body)\n  assert response.status_code==200,(path,response.status_code)\n  return response.json()\n post('/auth/login',account)\n operation=post('/draft-operations',{})\n post('/drafts',{'operation_id':operation['operation_id'],'expected_revision':0,'draft':{'service_date':'2030-03-01','activities':[{'id':str(uuid.uuid4()),'type':'Coffee','start':'2030-03-01T08:00+01:00','end':'2030-03-01T08:15+01:00'}]}})\nprint('Acknowledged synthetic draft and session created through HTTP.')\n`);
  const before = snapshot('private-api'), fictionalBefore = snapshot('api');
  assert(before.drafts.count >= 1 && before.sessions.count >= 1);
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
  result.privateCountsBefore = Object.fromEntries(Object.entries(before).map(([key,value]) => [key,value.count]));
  result.privateCountsAfter = Object.fromEntries(Object.entries(after).map(([key,value]) => [key,value.count]));
  result.protectedContainerCount = protectedBefore.length;
  result.checks.push('Reset removes synthetic business data/sessions, keeps migration/security settings and generated secrets, reprovisions one account and reseeds exactly one fictional day.');
  result.checks.push('All unrelated container IDs, images, start times and states remain identical.');
  result.passed = true;
} catch (error) {
  result.passed = false; result.error = error.message; process.exitCode = 1;
} finally {
  result.finished = new Date().toISOString();
  writeFileSync(ROOT + '/tmp/submission-runtime-check.json', JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
}
