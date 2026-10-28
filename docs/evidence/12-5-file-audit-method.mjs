// Audit changed/versioned submission files; never print generated secret values.
// Usage: node docs/evidence/12-5-file-audit-method.mjs <ignored-runtime> [earlier-ignored-runtimes...]
import { execFileSync } from 'node:child_process';
import { readFileSync, existsSync, writeFileSync } from 'node:fs';
const git = args => execFileSync('git', args, { encoding:'utf8' }).trim().split(/\r?\n/).filter(Boolean);
const paths = [...new Set([...git(['diff','--name-only','99c272b09abaa5ffecf3286b406fbf065a445c7c']), ...git(['ls-files','--others','--exclude-standard'])])].sort();
const tracked = git(['ls-files']);
const forbiddenTracked = tracked.filter(p => /(^|\/)(node_modules|\.private-runtime)(\/|$)/.test(p) || /(^|\/)\.env(?:\.|$)/.test(p) && !p.endsWith('.example'));
const secrets = [];
const directories = process.argv.slice(2);
if (!directories.length) throw Error('Pass explicit ignored submission runtime directories to audit; no secret audit without inputs');
for (const directory of directories) {
  const passwordPath = directory + '/postgres-password', accountPath = directory + '/account.json';
  if (!existsSync(passwordPath) || !existsSync(accountPath)) throw Error('Required synthetic secret inputs are missing');
  const password=readFileSync(passwordPath,'utf8').trim(),account=JSON.parse(readFileSync(accountPath,'utf8'));
  if (password.length<32 || account.username!=='synthetic-submission' || typeof account.password!=='string' || account.password.length<32) throw Error('Expected generated synthetic secret inputs');
  secrets.push(password,account.password);
}
const matches = [];
for (const path of paths) {
  const bytes = readFileSync(path);
  if (secrets.some(secret => bytes.includes(Buffer.from(secret)) || bytes.includes(Buffer.from(secret,'utf16le')))) matches.push(path);
}
const result = {capturedAt:new Date().toISOString(),source:git(['rev-parse','HEAD'])[0],checkedPaths:paths,forbiddenTracked,generatedSecretValuesChecked:secrets.length,generatedSecretMatches:matches,newArchives:paths.filter(p=>/\.(zip|tar|gz|dump|bak)$/i.test(p)),passed:forbiddenTracked.length===0&&matches.length===0};
writeFileSync('docs/evidence/12-5-file-audit.json',JSON.stringify(result,null,2));
console.log(JSON.stringify({passed:result.passed,files:paths.length,secretsChecked:secrets.length,newArchives:result.newArchives}));
if (!result.passed) process.exitCode=1;
