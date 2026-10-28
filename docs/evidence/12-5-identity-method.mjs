// Read-only identity capture, run from the clean checkout after recipe checks.
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
const run = (command, args) => execFileSync(command, args, { encoding: 'utf8' }).trim();
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const project = 'ibe160-submission';
const ids = run('docker', ['ps', '-aq', '--filter', 'label=com.docker.compose.project=' + project]).split(/\s+/);
const containers = JSON.parse(run('docker', ['inspect', ...ids])).map(c => ({
  id: c.Id, name: c.Name, imageId: c.Image, image: c.Config.Image, startedAt: c.State.StartedAt,
  state: c.State.Status, health: c.State.Health?.Status,
  project: c.Config.Labels['com.docker.compose.project'],
  root: c.Config.Labels['com.docker.compose.project.working_dir'],
  config: c.Config.Labels['com.docker.compose.project.config_files'],
  ports: c.NetworkSettings.Ports, networks: Object.keys(c.NetworkSettings.Networks),
  mounts: c.Mounts.map(m => ({type:m.Type, name:m.Name, source:m.Source, destination:m.Destination, readWrite:m.RW})),
}));
const files = run('git', ['ls-files']).split(/\r?\n/).filter(p =>
  p.startsWith('backend/') || p.startsWith('frontend/src/') || p.startsWith('frontend/submission-tests/')
  || p.startsWith('deploy/submission/') || p.startsWith('scripts/submission') || p === 'scripts/verify-submission-runtime.mjs'
  || ['README.md', '.dockerignore', 'compose.submission.yaml', 'frontend/package.json', 'frontend/package-lock.json', 'frontend/tsconfig.json', 'frontend/vite.config.ts', 'frontend/playwright.submission.config.ts'].includes(p)
  || /^Eksempelfiler\/(Testskift-[A-E]\.pdf|Fasit-testskift\.json)$/.test(p));
const html = await (await fetch('http://127.0.0.1:15325/private')).text();
const assets = [...html.matchAll(/(?:src|href)="([^"?]+\.(?:js|css))"/g)].map(m => m[1]);
const served = [];
for (const asset of assets) {
  if (!/^\/assets\/[\w.-]+\.(js|css)$/.test(asset)) throw Error('Unexpected served asset');
  const bytes = new Uint8Array(await (await fetch('http://127.0.0.1:15325' + asset)).arrayBuffer());
  const imageHash = run('docker', ['exec', project + '-frontend-1', 'node', '-e', "process.stdout.write(require('crypto').createHash('sha256').update(require('fs').readFileSync(" + JSON.stringify('/app/dist' + asset) + ")).digest('hex'))"]);
  const sha256 = hash(bytes);
  if (imageHash !== sha256) throw Error('Served asset differs from built image');
  served.push({asset, bytes:bytes.length, sha256, equalsBuiltImage:true});
}
const result = {
  capturedAt:new Date().toISOString(), source:run('git',['rev-parse','HEAD']),
  clean:run('git',['status','--porcelain']) === '', root:process.cwd(),
  host:{platform:os.platform(), release:os.release(), arch:os.arch(), node:process.version},
  docker:run('docker',['version','--format','{{.Server.Version}}']), compose:run('docker',['compose','version']),
  containers, served, sourceFileSha256:Object.fromEntries(files.map(p => [p,hash(readFileSync(p))])),
  privateHealth:await (await fetch('http://127.0.0.1:18328/health')).json(),
  fictionalHealth:await (await fetch('http://127.0.0.1:18327/health')).json(),
};
writeFileSync('tmp/submission-identity.json', JSON.stringify(result,null,2));
console.log(JSON.stringify({source:result.source,clean:result.clean,containers:containers.length,sourceFiles:files.length,servedAssets:served.length}));
