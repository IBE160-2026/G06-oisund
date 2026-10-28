// Fixed project/file/ports: never inherit an operational Compose selection.
import { spawnSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { mkdirSync, existsSync, writeFileSync, readFileSync, lstatSync, realpathSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { resolve, join } from 'node:path';
export const ROOT = realpathSync(fileURLToPath(new URL('../', import.meta.url)));
export const PROJECT = 'ibe160-submission';
const CONFIG = join(ROOT, 'compose.submission.yaml');
const runtime = join(ROOT, '.private-runtime', 'submission');
function run(command, args, options = {}) {
  const result = spawnSync(command, args, { cwd: ROOT, stdio: 'inherit', ...options });
  if (result.error) throw result.error;
  if (result.status !== 0) throw Error(`${command} exited ${result.status}`);
  return result.stdout;
}
function compose(args, capture = false) {
  const env = Object.fromEntries(Object.entries(process.env).filter(([key]) => !key.startsWith('COMPOSE_')));
  return run('docker', ['compose', '--project-directory', ROOT, '-p', PROJECT, '-f', CONFIG, ...args], { env, ...(capture ? { stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' } : {}) });
}
export function validateConfig(config) {
  const services = config.services;
  if (config.name !== PROJECT || Object.keys(services).sort().join() !== 'api,db,frontend,private-api,private-db') throw Error('Wrong submission project/services');
  for (const [name, port] of [['frontend', 15325], ['api', 18327], ['private-api', 18328]]) {
    const ports = services[name].ports;
    if (ports?.length !== 1 || ports[0].host_ip !== '127.0.0.1' || Number(ports[0].published) !== port) throw Error('Wrong submission loopback ports');
  }
  for (const [service, volume] of [['db', 'submission_fictional'], ['private-db', 'submission_private']]) {
    const mounts = services[service].volumes;
    if (services[service].ports?.length || mounts?.length !== 1 || mounts[0].type !== 'volume' || mounts[0].source !== volume || config.volumes[volume]?.name !== `${PROJECT}_${volume}` || config.volumes[volume]?.external) throw Error('Wrong submission storage');
  }
  const api = services['private-api'].environment;
  if (api.SUBMISSION_PROJECT !== PROJECT || api.PRIVATE_DATABASE_URL !== 'postgresql://private_work@private-db/private_work' || api.PRIVATE_DATABASE_PASSWORD_FILE !== '/run/secrets/submission_password' || api.PRIVATE_ORIGIN !== 'http://127.0.0.1:15325' || api.PRIVATE_TEST_PROJECT !== 'ibe160-private-tests') throw Error('Wrong private submission configuration');
}
export function validateContainer(container, service, volume) {
  const labels = container.Config.Labels;
  if (labels['com.docker.compose.project'] !== PROJECT || labels['com.docker.compose.service'] !== service
      || Object.keys(container.NetworkSettings.Networks).join() !== `${PROJECT}_default`) throw Error('Running container is outside isolated submission project/network');
  if (volume) {
    const mounts = container.Mounts.filter(mount => mount.Destination === '/var/lib/postgresql/data');
    if (mounts.length !== 1 || mounts[0].Type !== 'volume' || mounts[0].Name !== `${PROJECT}_${volume}`) throw Error('Running storage is not the isolated submission volume');
  }
  if (service === 'private-api') {
    const env = Object.fromEntries(container.Config.Env.map(value => { const at = value.indexOf('='); return [value.slice(0, at), value.slice(at + 1)]; }));
    if (env.SUBMISSION_PROJECT !== PROJECT || env.PRIVATE_DATABASE_URL !== 'postgresql://private_work@private-db/private_work' || env.PRIVATE_DATABASE_PASSWORD_FILE !== '/run/secrets/submission_password') throw Error('Running API targets wrong private storage');
  }
}
export function validateOwnership(container, root = ROOT) {
  const normalize = path => path.replaceAll('\\', '/').toLowerCase().replace(/\/$/, '');
  const labels = container.Config.Labels;
  if (labels['com.docker.compose.project'] !== PROJECT
      || normalize(labels['com.docker.compose.project.working_dir'] ?? '') !== normalize(root)
      || normalize(labels['com.docker.compose.project.config_files'] ?? '') !== normalize(join(root, 'compose.submission.yaml'))) throw Error('Submission project already belongs to another checkout/configuration; leave it unchanged');
}
function checkOwnership() {
  const ids = run('docker', ['ps', '-aq', '--filter', `label=com.docker.compose.project=${PROJECT}`], { stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' }).trim().split(/\s+/).filter(Boolean);
  if (!ids.length) return;
  const containers = JSON.parse(run('docker', ['inspect', ...ids], { stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' }));
  for (const container of containers) validateOwnership(container);
}
function preflight() { validateConfig(JSON.parse(compose(['config', '--format', 'json'], true))); }
function safePath(path) {
  if (existsSync(path) && lstatSync(path).isSymbolicLink()) throw Error('Submission runtime must not use symbolic links');
  if (existsSync(path) && realpathSync(path) !== resolve(path)) throw Error('Submission runtime path redirected');
}
function generate() {
  for (const path of [join(ROOT, '.private-runtime'), runtime]) { safePath(path); mkdirSync(path, { recursive: true }); }
  const files = [['postgres-password', () => randomBytes(32).toString('hex')], ['account.json', () => JSON.stringify({ username: 'synthetic-submission', password: randomBytes(32).toString('hex') }, null, 2)]];
  // Never replace secrets belonging to an existing persistent volume.
  for (const [name, value] of files) {
    const path = join(runtime, name); safePath(path);
    if (!existsSync(path)) {
      const volumes = run('docker', ['volume', 'ls', '--filter', `label=com.docker.compose.project=${PROJECT}`, '--format', '{{.Name}}'], { stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' });
      if (volumes.trim()) throw Error('Submission volume exists: restore original ignored secrets before continuing');
      writeFileSync(path, value(), { flag: 'wx', mode: 0o600 });
    }
  }
}
function verifyRunningStorage() {
  for (const [service, volume] of [['db', 'submission_fictional'], ['private-db', 'submission_private'], ['private-api', null], ['api', null]]) {
    const id = compose(['ps', '-q', service], true).trim();
    if (!id || id.includes('\n')) throw Error('Exactly one running submission database required');
    const [container] = JSON.parse(run('docker', ['inspect', id], { stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' }));
    validateContainer(container, service, volume);
  }
}
const privateManage = action => compose(['exec', '-T', 'private-api', 'python', '/submission/manage.py', action]);
const fictional = arguments_ => compose(['exec', '-T', 'api', 'python', '/submission/fictional.py', ...arguments_]);
function initialize() {
  compose(['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'migrate']);
  privateManage('init');
  fictional(['app.manage', 'migrate']);
  fictional(['app.manage', 'seed']);
}
export function main(action) {
  if (!['init', 'start', 'status', 'stop', 'restart', 'reset', 'test-backend', 'install-browser', 'test-browser'].includes(action)) throw Error('Use init | start | status | stop | restart | reset | test-backend | install-browser | test-browser');
  if (action === 'install-browser') {
    const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
    const npx = process.platform === 'win32' ? 'npx.cmd' : 'npx';
    // cmd.exe is necessary to launch npm.cmd on Windows; all args are fixed.
    const invoke = (command, args) => run(command, args, { cwd: join(ROOT, 'frontend'), shell: process.platform === 'win32' });
    invoke(npm, ['ci']); invoke(npx, ['playwright', 'install', 'chromium']);
    return;
  }
  checkOwnership();
  if (action === 'init') generate();
  preflight();
  if (action === 'init') compose(['build', '--pull', '--no-cache']);
  if (action === 'init' || action === 'start') { compose(['up', '-d', ...(action === 'start' ? ['--build'] : []), '--wait', '--wait-timeout', '180']); initialize(); }
  if (['status', 'test-browser', 'test-backend'].includes(action)) { verifyRunningStorage(); privateManage('check'); }
  if (action === 'status') compose(['ps']);
  if (action === 'stop') compose(['stop']);
  if (action === 'restart') { compose(['restart']); compose(['up', '-d', '--wait', '--wait-timeout', '180']); }
  if (action === 'reset') {
    verifyRunningStorage();
    // Private non-synthetic refusal must precede ANY mutation, including fictional seed.
    privateManage('reset');
    fictional(['app.manage', 'reset', '--fictional-only']);
  }
  if (action === 'test-backend') {
    compose(['exec', '-T', 'private-api', 'python', '-m', 'pytest', '-q']);
    fictional(['pytest', '-q']);
  }
  if (action === 'test-browser') {
    run(process.platform === 'win32' ? 'npx.cmd' : 'npx', ['playwright', 'test', '--config', 'playwright.submission.config.ts'], { cwd: join(ROOT, 'frontend'), shell: process.platform === 'win32' });
  }
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  try { main(process.argv.length === 3 ? process.argv[2] : ''); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
