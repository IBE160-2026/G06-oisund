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
const publishedPorts = { frontend: [15325, 15325], api: [8000, 18327], 'private-api': [8000, 18328] };
const databaseVolumes = { db: 'submission_fictional', 'private-db': 'submission_private' };
const privateEnvironment = {
  APP_MODE: 'private-local', PRIVATE_LOOPBACK_DEVELOPMENT: '1', SUBMISSION_PROJECT: PROJECT,
  PRIVATE_DATABASE_URL: 'postgresql://private_work@private-db/private_work',
  PRIVATE_DATABASE_PASSWORD_FILE: '/run/secrets/submission_password',
  PRIVATE_ORIGIN: 'http://127.0.0.1:15325', PRIVATE_TEST_PROJECT: 'ibe160-private-tests',
  PRIVATE_TEST_API: 'http://private-api:8000', PRIVATE_TEST_ORIGIN: 'http://127.0.0.1:15325',
};
function validatePrivateEnvironment(environment) {
  if (Object.entries(privateEnvironment).some(([key, value]) => environment?.[key] !== value)) throw Error('Wrong private submission configuration/storage/test endpoint');
}
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
  for (const [name, [target, port]] of Object.entries(publishedPorts)) {
    const ports = services[name].ports;
    if (ports?.length !== 1 || ports[0].host_ip !== '127.0.0.1' || Number(ports[0].published) !== port || Number(ports[0].target) !== target || ports[0].protocol !== 'tcp') throw Error('Wrong submission loopback ports');
  }
  for (const [service, volume] of [['db', 'submission_fictional'], ['private-db', 'submission_private']]) {
    const mounts = services[service].volumes;
    if (services[service].ports?.length || mounts?.length !== 1 || mounts[0].type !== 'volume' || mounts[0].target !== '/var/lib/postgresql/data' || mounts[0].source !== volume || config.volumes[volume]?.name !== `${PROJECT}_${volume}` || config.volumes[volume]?.external) throw Error('Wrong submission storage');
  }
  validatePrivateEnvironment(services['private-api'].environment);
}
export function validateContainer(container, service, volume) {
  if (!(service in publishedPorts) && !(service in databaseVolumes)) throw Error('Unknown submission service');
  if (!container?.State?.Running || container.State.Status !== 'running' || container.State.Health?.Status !== 'healthy') throw Error('Every submission service must be running and healthy');
  const labels = container.Config.Labels;
  if (labels['com.docker.compose.project'] !== PROJECT || labels['com.docker.compose.service'] !== service
      || Object.keys(container.NetworkSettings.Networks).join() !== `${PROJECT}_default`) throw Error('Running container is outside isolated submission project/network');
  const bindings = Object.entries(container.NetworkSettings.Ports ?? {}).flatMap(([target, values]) => (values ?? []).map(value => ({ target, ...value })));
  if (service in publishedPorts) {
    const [target, port] = publishedPorts[service];
    if (bindings.length !== 1 || bindings[0].target !== `${target}/tcp` || bindings[0].HostIp !== '127.0.0.1' || bindings[0].HostPort !== String(port)) throw Error('Running submission publishes wrong ports');
  } else if (bindings.length) throw Error('Submission database must not publish a port');
  if (volume) {
    const mounts = container.Mounts.filter(mount => mount.Destination === '/var/lib/postgresql/data');
    if (mounts.length !== 1 || mounts[0].Type !== 'volume' || mounts[0].Name !== `${PROJECT}_${volume}`) throw Error('Running storage is not the isolated submission volume');
  }
  if (service === 'private-api') {
    const env = Object.fromEntries(container.Config.Env.map(value => { const at = value.indexOf('='); return [value.slice(0, at), value.slice(at + 1)]; }));
    validatePrivateEnvironment(env);
  }
}
export function validateRuntime(containers) {
  const services = [...Object.keys(publishedPorts), ...Object.keys(databaseVolumes)];
  if (containers.length !== services.length) throw Error('Exactly five submission services required');
  for (const service of services) {
    const matches = containers.filter(container => container.Config.Labels['com.docker.compose.service'] === service);
    if (matches.length !== 1) throw Error('Exactly one of each submission service required');
    validateContainer(matches[0], service, databaseVolumes[service]);
  }
}
export function validateOwnership(container, root = ROOT) {
  const normalize = path => {
    const normalized = path.replaceAll('\\', '/').replace(/\/$/, '');
    return process.platform === 'win32' ? normalized.toLowerCase() : normalized;
  };
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
  const ids = compose(['ps', '-a', '-q'], true).trim().split(/\s+/).filter(Boolean);
  if (!ids.length) throw Error('Exactly five submission services required');
  validateRuntime(JSON.parse(run('docker', ['inspect', ...ids], { stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' })));
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
  if (action === 'init' || action === 'start') { compose(['up', '-d', ...(action === 'start' ? ['--no-build', '--pull', 'never'] : []), '--wait', '--wait-timeout', '180']); initialize(); }
  if (['status', 'test-browser', 'test-backend'].includes(action)) { verifyRunningStorage(); privateManage('check'); }
  if (action === 'status') compose(['ps']);
  if (action === 'stop') compose(['stop']);
  if (action === 'restart') { compose(['restart']); compose(['up', '-d', '--no-build', '--pull', 'never', '--wait', '--wait-timeout', '180']); }
  if (action === 'reset') {
    verifyRunningStorage();
    // Private non-synthetic refusal must precede ANY mutation, including fictional seed.
    privateManage('reset');
    fictional(['app.manage', 'reset', '--fictional-only']);
  }
  if (action === 'test-backend') {
    compose(['exec', '-T', 'private-api', 'python', '-m', 'pytest', '-q', '--ignore=tests/test_assessment.py', '--ignore=tests/test_pdf_import.py']);
    fictional(['pytest', '-q', 'tests/test_assessment.py', 'tests/test_pdf_import.py']);
  }
  if (action === 'test-browser') {
    run(process.platform === 'win32' ? 'npx.cmd' : 'npx', ['playwright', 'test', '--config', 'playwright.submission.config.ts'], { cwd: join(ROOT, 'frontend'), shell: process.platform === 'win32' });
  }
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  try { main(process.argv.length === 3 ? process.argv[2] : ''); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
