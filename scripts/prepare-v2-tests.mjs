import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';
import { prepare } from './prepare-password-tests.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));

await prepare(root, async (file, source) => {
  const isolated = source
    .replaceAll('ibe160-password-tests', 'ibe160-v2-tests')
    .replaceAll('compose.password-tests.yaml', 'compose.v2.yaml')
    .replaceAll(':15440', ':19651')
    .replaceAll(':18440', ':19652')
    .replaceAll(':18441', ':19653')
    .replaceAll('18489', '19654')
    .replaceAll('../tmp/password-regression-evidence/', '../tmp/v2-regression-evidence/');
  await writeFile(file, isolated);
}, 'v2');

const relative = 'frontend/.v2-tests/.generated-manifest.json';
const generated = JSON.parse(await readFile(join(root, relative), 'utf8'));
console.log(`Prepared ${generated.length} local V2 browser inputs.`);
