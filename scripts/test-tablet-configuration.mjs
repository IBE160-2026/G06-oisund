// Evaluate the actual configuration prelude after TypeScript transpilation.
// No network, cookies or app state is involved in this fail-closed boundary test.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { stripTypeScriptTypes } from 'node:module';
const source = readFileSync(new URL('../frontend/src/PrivateAccess.tsx', import.meta.url), 'utf8');
const prelude = source.slice(source.indexOf('const apiEnvironment'), source.indexOf('// Only a logout lock'));
function api(env) {
  const js = stripTypeScriptTypes(prelude.replaceAll('import.meta', JSON.stringify({ env })) + '\nAPI;');
  return vm.runInNewContext(js);
}
test('explicit relative tablet base overrides legacy; invalid explicit bases fail closed', () => {
  assert.equal(api({ VITE_PRIVATE_API_BASE: '/private-api', VITE_PRIVATE_API: 'https://legacy.invalid' }), '/private-api');
  assert.equal(api({ VITE_PRIVATE_API: 'http://127.0.0.1:18324' }), 'http://127.0.0.1:18324');
  for (const value of ['', '/private-api/', '//evil.invalid', 'https://evil.invalid', ' /private-api', '/private-api?x=1']) {
    assert.throws(() => api({ VITE_PRIVATE_API_BASE: value }), /Invalid private API configuration/);
  }
});
