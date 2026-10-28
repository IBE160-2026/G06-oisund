import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdir, mkdtemp, writeFile, readFile, readdir, unlink, symlink, lstat } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { prepare } from './prepare-story124-tests.mjs';

test('translates isolated endpoints and tracked synthetic fixture while preserving unrelated files', async () => {
  const base = resolve('tmp/story124-prepare-tests');
  await mkdir(base, { recursive: true });
  const root = await mkdtemp(join(base, 'run-'));
  await mkdir(join(root, 'frontend/tests/fixtures'), { recursive: true });
  const fixture = join(root, 'frontend/tests/fixtures/pdf-upload.json');
  await writeFile(fixture, '{"synthetic":true}');
  await writeFile(join(root, 'frontend/tests/old.ts'), 'old generated copy');
  await prepare(root);
  const destination = join(root, 'frontend/.story124-tests');
  await writeFile(join(destination, 'unrelated.ts'), 'keep typescript');
  await writeFile(join(destination, 'unrelated.txt'), 'keep text');
  await unlink(join(root, 'frontend/tests/old.ts'));
  const source = "new URL('./fixtures/pdf-upload.json', import.meta.url); :8001 :8000 :5173 :15222 18481 18483 1848[13] ibe160-private-tests compose.private.yaml";
  await writeFile(join(root, 'frontend/tests/mobile.ts'), source);
  await prepare(root);
  assert.equal(await readFile(join(destination, 'mobile.ts'), 'utf8'), "new URL('../tests/fixtures/pdf-upload.json', import.meta.url); :18326 :18325 :15324 :15324 18484 18484 18484 ibe160-story124-tests compose.story124.yaml");
  const resolvedFixture = new URL('../tests/fixtures/pdf-upload.json', pathToFileURL(join(destination, 'mobile.ts')));
  assert.equal(await readFile(resolvedFixture, 'utf8'), '{"synthetic":true}');
  assert(!(await readdir(destination)).includes('old.ts'));
  assert.equal(await readFile(join(destination, 'unrelated.ts'), 'utf8'), 'keep typescript');
  assert.equal(await readFile(join(destination, 'unrelated.txt'), 'utf8'), 'keep text');
  assert.equal(await readFile(join(root, 'frontend/tests/mobile.ts'), 'utf8'), source);
});

for (const defect of ['unowned collision', 'owned file link', 'obsolete file link', 'manifest link']) {
  test(`refuses ${defect} before overwriting or deleting any entry`, async t => {
    const base = resolve('tmp/story124-prepare-tests');
    await mkdir(base, { recursive: true });
    const root = await mkdtemp(join(base, 'refusal-'));
    const source = join(root, 'frontend/tests');
    await mkdir(source, { recursive: true });
    await writeFile(join(source, 'owned.ts'), 'original generated');
    await writeFile(join(source, 'obsolete.ts'), 'preserve before refused deletion');
    await prepare(root);
    const destination = join(root, 'frontend/.story124-tests');
    const manifest = join(destination, '.generated-manifest.json');
    const originalManifest = await readFile(manifest, 'utf8');
    await unlink(join(source, 'obsolete.ts'));
    await writeFile(join(source, 'owned.ts'), 'new source must not be written');
    const external = join(root, 'external-target.txt');
    const externalValue = defect === 'manifest link' ? originalManifest : 'external target must survive';
    await writeFile(external, externalValue);
    let junctionSentinel;
    let linked;
    if (defect === 'unowned collision') {
      await writeFile(join(source, 'new.ts'), 'would overwrite unowned');
      await writeFile(join(destination, 'new.ts'), 'unowned must survive');
    } else {
      linked = defect === 'manifest link' ? manifest : join(destination, defect === 'owned file link' ? 'owned.ts' : 'obsolete.ts');
      await unlink(linked);
      try { await symlink(external, linked, 'file'); }
      catch (error) {
        if (process.platform !== 'win32' || error.code !== 'EPERM') throw error;
        // Non-admin Windows cannot create file symlinks. A real junction at
        // the same owned filename exercises the same reparse-point refusal.
        const externalDirectory = join(root, 'external-directory');
        await mkdir(externalDirectory);
        junctionSentinel = join(externalDirectory, 'sentinel.txt');
        await writeFile(junctionSentinel, externalValue);
        await symlink(externalDirectory, linked, 'junction');
        t.diagnostic('Windows file-symlink privilege unavailable; exercised real junction refusal');
      }
    }
    await assert.rejects(prepare(root), /unowned.*collision|Symbolic links/);
    assert.equal(await readFile(external, 'utf8'), externalValue);
    if (junctionSentinel) assert.equal(await readFile(junctionSentinel, 'utf8'), externalValue);
    if (linked) assert((await lstat(linked)).isSymbolicLink());
    if (defect !== 'owned file link') assert.equal(await readFile(join(destination, 'owned.ts'), 'utf8'), 'original generated');
    if (defect !== 'obsolete file link') assert.equal(await readFile(join(destination, 'obsolete.ts'), 'utf8'), 'preserve before refused deletion');
    if (defect !== 'manifest link') assert.equal(await readFile(manifest, 'utf8'), originalManifest);
    if (defect === 'unowned collision') assert.equal(await readFile(join(destination, 'new.ts'), 'utf8'), 'unowned must survive');
  });
}
