import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdir, mkdtemp, writeFile, readFile, readdir, symlink } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { prepare } from './prepare-v1followup-tests.mjs';

async function fixture() {
  const base = resolve('tmp/v1followup-preparer-unit');
  await mkdir(base, { recursive: true });
  return mkdtemp(join(base, 'case-'));
}

for (const parent of ['root', 'frontend']) test(`redirected ${parent} is refused before destination mkdir`, async () => {
  const base = await fixture(), external = join(base, 'external');
  await mkdir(join(external, 'frontend/tests'), { recursive: true });
  await mkdir(join(external, 'tests'), { recursive: true });
  const root = join(base, 'root');
  if (parent === 'root') await symlink(external, root, process.platform === 'win32' ? 'junction' : 'dir');
  else {
    await mkdir(root);
    await symlink(external, join(root, 'frontend'), process.platform === 'win32' ? 'junction' : 'dir');
  }
  const before = await readdir(external);
  await assert.rejects(prepare(root), /Symbolic links|ancestry/);
  assert.deepEqual(await readdir(external), before);
  assert(!(await readdir(join(external, 'frontend'))).includes('.v1followup-tests'));
});

test('partial first generation recovers only preflight-owned copies and preserves unrelated files', async () => {
  const root = await fixture(), source = join(root, 'frontend/tests');
  await mkdir(source, { recursive: true });
  await writeFile(join(source, 'a.ts'), ':8001 ibe160-private-tests');
  await writeFile(join(source, 'b.ts'), ':5173 compose.private.yaml');
  const destination = join(root, 'frontend/.v1followup-tests');
  await mkdir(destination);
  await writeFile(join(destination, 'unowned.ts'), 'never overwrite');
  let writes = 0;
  await assert.rejects(prepare(root, async (path, content) => {
    // Ownership must already include every planned output before the first
    // generated write. Simulate interruption after a partial second copy.
    assert.deepEqual(JSON.parse(await readFile(join(destination, '.generated-manifest.json'), 'utf8')), ['a.ts', 'b.ts']);
    writes++;
    await writeFile(path, writes === 2 ? 'partial' : content);
    if (writes === 2) throw Error('simulated interruption');
  }), /simulated interruption/);
  assert.equal(await readFile(join(destination, 'b.ts'), 'utf8'), 'partial');
  await prepare(root);
  assert.equal(await readFile(join(destination, 'a.ts'), 'utf8'), ':18330 ibe160-v1followup-tests');
  assert.equal(await readFile(join(destination, 'b.ts'), 'utf8'), ':15326 compose.v1followup.yaml');
  assert.equal(await readFile(join(destination, 'unowned.ts'), 'utf8'), 'never overwrite');
  await writeFile(join(source, 'unowned.ts'), 'collision');
  await assert.rejects(prepare(root), /unowned.*collision/);
  assert.equal(await readFile(join(destination, 'unowned.ts'), 'utf8'), 'never overwrite');
});
