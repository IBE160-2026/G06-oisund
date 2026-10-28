// Audit changed/versioned submission files; never print generated secret values.
import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync, existsSync, writeFileSync } from 'node:fs';
const git = args => execFileSync('git', args, { encoding:'utf8' }).trim().split(/\r?\n/).filter(Boolean);
const paths = [...new Set([...git(['diff','--name-only','99c272b09abaa5ffecf3286b406fbf065a445c7c']), ...git(['ls-files','--others','--exclude-standard'])])].sort();
const tracked = git(['ls-files']);
const forbiddenTracked = tracked.filter(p => /(^|\/)(node_modules|\.private-runtime)(\/|$)/.test(p) || /(^|\/)\.env(?:\.|$)/.test(p) && !p.endsWith('.example'));
const secrets = [];
for (const directory of ['D:/IBE160/tmp/submission-clean-20261028/.private-runtime/submission','D:/IBE160/tmp/submission-clean-20261028/tmp/failed-initial-runtime','D:/IBE160/tmp/submission-clean-20261028/tmp/failed-second-runtime']) {
  if (!existsSync(directory)) continue;
  const passwordPath = directory + '/postgres-password', accountPath = directory + '/account.json';
  if (existsSync(passwordPath)) secrets.push(readFileSync(passwordPath,'utf8').trim());
  if (existsSync(accountPath)) secrets.push(JSON.parse(readFileSync(accountPath,'utf8')).password);
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
