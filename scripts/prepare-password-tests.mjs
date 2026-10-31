// Disposable copies preserve historical URLs. A manifest owns only generated
// names; unrelated files in this directory are never inferred to be disposable.
import { mkdir, readFile, readdir, writeFile, realpath, unlink, lstat, rename } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { resolve, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
export async function prepare(rootPath = fileURLToPath(new URL('../', import.meta.url)), writeGenerated = writeFile) {
  const root = resolve(rootPath), destination = resolve(root, 'frontend/.password-regression-tests');
  if (destination !== join(root, 'frontend', '.password-regression-tests')) throw Error('Unexpected disposable destination');
  async function entry(path) {
    try { const value = await lstat(path); if (value.isSymbolicLink()) throw Error('Symbolic links are not disposable: ' + path); return value; }
    catch (error) { if (error.code === 'ENOENT') return null; throw error; }
  }
  for (const path of [root, join(root, 'frontend'), join(root, 'frontend/tests')]) {
    const info = await entry(path);
    if (!info?.isDirectory() || await realpath(path) !== path) throw Error('Disposable parent ancestry must not redirect: ' + path);
  }
  const destinationEntry = await entry(destination);
  if (destinationEntry && (!destinationEntry.isDirectory() || await realpath(destination) !== destination)) throw Error('Disposable destination must not redirect outside workspace');
  const files = (await readdir(join(root, 'frontend/tests'), { withFileTypes: true })).filter(file => file.isFile() && file.name.endsWith('.ts')).map(file => file.name);
  // Complete the ownership/link preflight before the first write or deletion.
  for (const name of destinationEntry ? await readdir(destination) : []) await entry(join(destination, name));
  const manifest = join(destination, '.generated-manifest.json');
  const manifestEntry = await entry(manifest);
  if (manifestEntry && !manifestEntry.isFile()) throw Error('Manifest must be a regular file');
  let previous = [];
  try { previous = JSON.parse(await readFile(manifest, 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  if (!Array.isArray(previous) || new Set(previous).size !== previous.length || previous.some(name => typeof name !== 'string' || name !== name.replaceAll(/[/\\]/g, '') || !name.endsWith('.ts'))) throw Error('Invalid generated-file manifest');
  for (const name of new Set([...previous, ...files])) {
    const existing = await entry(join(destination, name));
    if (existing && !previous.includes(name)) throw Error('Refusing unowned generated-name collision: ' + name);
    if (existing && !existing.isFile()) throw Error('Generated entry must be a regular file: ' + name);
  }
  await mkdir(destination, { recursive: true });
  async function recordOwnership(names) {
    const temporary = join(destination, '.ownership-' + randomUUID() + '.tmp');
    try {
      await writeFile(temporary, JSON.stringify(names, null, 2), { flag: 'wx' });
      await rename(temporary, manifest);
    } finally {
      try { await unlink(temporary); } catch (error) { if (error.code !== 'ENOENT') throw error; }
    }
  }
  // Reserve only preflight-approved planned names before generated writes.
  // An interrupted first run can recover its partial copies on the next run.
  await recordOwnership([...new Set([...previous, ...files])]);
  for (const name of previous) if (!files.includes(name)) {
    try { await unlink(join(destination, name)); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  for (const name of files) {
    const source = await readFile(join(root, 'frontend/tests', name), 'utf8');
    await writeGenerated(join(destination, name), source.replaceAll('../docs/evidence/', '../tmp/password-regression-evidence/').replaceAll("new URL('./fixtures/pdf-upload.json', import.meta.url)", "new URL('../tests/fixtures/pdf-upload.json', import.meta.url)").replaceAll('1848[13]', '18489').replaceAll('18481', '18489').replaceAll('18483', '18489').replaceAll(':8001', ':18441').replaceAll(':8000', ':18440').replaceAll(':5173', ':15440').replaceAll(':15222', ':15440').replaceAll('ibe160-private-tests', 'ibe160-password-tests').replaceAll('compose.private.yaml', 'compose.password-tests.yaml'));
  }
  await recordOwnership(files);
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  await prepare();
  console.log('Prepared isolated test copies. Use COMPOSE_PROJECT_NAME=ibe160-password-tests and playwright.password-regression.config.ts.');
}
