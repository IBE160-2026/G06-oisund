// Disposable copies preserve historical URLs. A manifest owns only generated
// names; unrelated files in this directory are never inferred to be disposable.
import { mkdir, readFile, readdir, writeFile, realpath, unlink, lstat } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
export async function prepare(rootPath = fileURLToPath(new URL('../', import.meta.url))) {
  const root = resolve(rootPath), destination = resolve(root, 'frontend/.story124-tests');
  if (destination !== join(root, 'frontend', '.story124-tests')) throw Error('Unexpected disposable destination');
  async function entry(path) {
    try { const value = await lstat(path); if (value.isSymbolicLink()) throw Error('Symbolic links are not disposable: ' + path); return value; }
    catch (error) { if (error.code === 'ENOENT') return null; throw error; }
  }
  await entry(destination);
  await mkdir(destination, { recursive: true });
  if (await realpath(destination) !== destination) throw Error('Disposable destination must not redirect outside workspace');
  const files = (await readdir(join(root, 'frontend/tests'), { withFileTypes: true })).filter(file => file.isFile() && file.name.endsWith('.ts')).map(file => file.name);
  // Complete the ownership/link preflight before the first write or deletion.
  for (const name of await readdir(destination)) await entry(join(destination, name));
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
  for (const name of previous) if (!files.includes(name)) {
    try { await unlink(join(destination, name)); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  for (const name of files) {
    const source = await readFile(join(root, 'frontend/tests', name), 'utf8');
    await writeFile(join(destination, name), source.replaceAll("new URL('./fixtures/pdf-upload.json', import.meta.url)", "new URL('../tests/fixtures/pdf-upload.json', import.meta.url)").replaceAll('1848[13]', '18484').replaceAll('18481', '18484').replaceAll('18483', '18484').replaceAll(':8001', ':18326').replaceAll(':8000', ':18325').replaceAll(':5173', ':15324').replaceAll(':15222', ':15324').replaceAll('ibe160-private-tests', 'ibe160-story124-tests').replaceAll('compose.private.yaml', 'compose.story124.yaml'));
  }
  await writeFile(join(destination, '.generated-manifest.json'), JSON.stringify(files, null, 2));
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  await prepare();
  console.log('Prepared isolated test copies. Use COMPOSE_PROJECT_NAME=ibe160-story124-tests and playwright.story124.config.ts.');
}
