// Disposable copies preserve historical URLs. A manifest owns only generated
// names; unrelated files in this directory are never inferred to be disposable.
import { mkdir, readFile, readdir, writeFile, realpath, unlink } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
export async function prepare(rootPath = fileURLToPath(new URL('../', import.meta.url))) {
  const root = resolve(rootPath), destination = resolve(root, 'frontend/.story123-tests');
  if (destination !== join(root, 'frontend', '.story123-tests')) throw Error('Unexpected disposable destination');
  await mkdir(destination, { recursive: true });
  if (await realpath(destination) !== destination) throw Error('Disposable destination must not redirect outside workspace');
  const files = (await readdir(join(root, 'frontend/tests'), { withFileTypes: true })).filter(file => file.isFile() && file.name.endsWith('.ts')).map(file => file.name);
  let previous = [];
  try { previous = JSON.parse(await readFile(join(destination, '.generated-manifest.json'), 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  if (!Array.isArray(previous) || previous.some(name => typeof name !== 'string' || name !== name.replaceAll(/[/\\]/g, '') || !name.endsWith('.ts'))) throw Error('Invalid generated-file manifest');
  for (const name of previous) if (!files.includes(name)) {
    try { await unlink(join(destination, name)); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  for (const name of files) {
    const source = await readFile(join(root, 'frontend/tests', name), 'utf8');
    await writeFile(join(destination, name), source.replaceAll(':8001', ':18324').replaceAll(':8000', ':18323').replaceAll(':5173', ':15323').replaceAll(':15222', ':15323').replaceAll('ibe160-private-tests', 'ibe160-story123-tests').replaceAll('compose.private.yaml', 'compose.story123.yaml'));
  }
  await writeFile(join(destination, '.generated-manifest.json'), JSON.stringify(files, null, 2));
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  await prepare();
  console.log('Prepared isolated test copies. Use COMPOSE_PROJECT_NAME=ibe160-story123-tests and playwright.story123.config.ts.');
}
