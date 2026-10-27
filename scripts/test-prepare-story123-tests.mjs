import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdir, mkdtemp, writeFile, readFile, readdir, unlink } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { prepare } from './prepare-story123-tests.mjs';

test('prunes only obsolete manifest-owned test copies and preserves unrelated files', async () => {
  const base = resolve('tmp/story123-prepare-tests'); await mkdir(base, { recursive: true });
  const root = await mkdtemp(join(base, 'run-'));
  await mkdir(join(root, 'frontend/tests'), { recursive: true });
  await writeFile(join(root, 'frontend/tests/old.ts'), "const url = ':8001';");
  await prepare(root);
  await writeFile(join(root, 'frontend/.story123-tests/unrelated.ts'), 'keep typescript');
  await writeFile(join(root, 'frontend/.story123-tests/unrelated.txt'), 'keep text');
  await unlink(join(root, 'frontend/tests/old.ts'));
  await writeFile(join(root, 'frontend/tests/renamed.ts'), "const url = ':8001';");
  await prepare(root);
  assert(!(await readdir(join(root, 'frontend/.story123-tests'))).includes('old.ts'));
  assert.equal(await readFile(join(root, 'frontend/.story123-tests/renamed.ts'), 'utf8'), "const url = ':18324';");
  assert.equal(await readFile(join(root, 'frontend/.story123-tests/unrelated.ts'), 'utf8'), 'keep typescript');
  assert.equal(await readFile(join(root, 'frontend/.story123-tests/unrelated.txt'), 'utf8'), 'keep text');
});
