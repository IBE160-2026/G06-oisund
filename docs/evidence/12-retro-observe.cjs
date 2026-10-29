const { chromium, expect } = require('../../frontend/node_modules/@playwright/test');
const fs = require('node:fs');
const crypto = require('node:crypto');
const http = require('node:http');
const path = require('node:path');
const out = { date: new Date().toISOString(), source: '62ac07586681b22812a633c676e2f18ba49c7489', observations: [], requests: [], errors: [] };
(async () => {
  const root = path.resolve('tmp/epic12-retro/dist');
  const server = http.createServer((req,res) => {
    const filename = path.resolve(root, '.' + new URL(req.url, 'http://localhost').pathname);
    if (!filename.startsWith(root + path.sep) || !fs.existsSync(filename)) {res.writeHead(404).end();return;}
    res.setHeader('Content-Type', filename.endsWith('.js') ? 'application/javascript' : filename.endsWith('.css') ? 'text/css' : 'text/html');
    res.end(fs.readFileSync(filename));
  });
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  const origin = 'http://127.0.0.1:' + server.address().port;
  out.origin = origin;
  out.method = 'Fresh static Vite build; isolated in-memory demo, no API/PostgreSQL exercised';
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    page.on('pageerror', e => out.errors.push(e.message));
    page.on('request', r => out.requests.push({ method: r.method(), url: r.url() }));
    await page.route('**/*', r => {
      const u = new URL(r.request().url());
      if (u.origin === origin && (u.pathname === '/demo.html' || u.pathname.startsWith('/assets/'))) return r.continue();
      return r.abort();
    });
    await page.goto(origin + '/demo.html');
    const b = n => page.getByRole('button', { name: n, exact: true });
    await expect(page.getByRole('heading', { name: '1. Velg import' })).toBeVisible();
    await b('Åpne delvis tekst-PDF-eksempel').click();
    await b('Lagre forslag i simuleringen').click();
    await b('Se lagret dag før start').click();
    await b('Bekreft plan').click();
    await b('Velg Linje 100 · Tur A').click();
    await expect(b('Lagre aktivitetsstatus')).toBeDisabled();
    out.observations.push('Selection before explicit Start cannot save an outcome.');
    await b('Start arbeidsdagen').click();
    await b('Bekreft Start').click();
    await page.getByLabel('Manuell aktivitetsstatus').selectOption('Fullført manuelt');
    await b('Lagre aktivitetsstatus').click();
    await b('Til dagsoversikten').click();
    await b('Avslutt arbeidsdagen').click();
    await b('Bekreft avsluttet').click();
    await expect(page.getByRole('heading', { name: /skrivebeskyttet/ })).toBeVisible();
    await expect(page.getByText('Pause: Ikke registrert / ukjent', { exact: true })).toBeVisible();
    await expect(page.getByText('Linje 100 · Tur A: Fullført manuelt', { exact: true })).toBeVisible();
    await expect(b('Start arbeidsdagen')).toHaveCount(0);
    out.observations.push('Explicit Start/outcome/end produces read-only fictional recap; untouched outcomes stay unknown.');
    const assets = await page.locator('script[src],link[rel=stylesheet]').evaluateAll(es => es.map(e => e.src || e.href));
    out.assets = [];
    for (const url of assets) { const r = await fetch(url); const bytes = Buffer.from(await r.arrayBuffer()); out.assets.push({ url, status:r.status, sha256:crypto.createHash('sha256').update(bytes).digest('hex') }); }
    await page.reload();
    await expect(b('Arbeidsdag')).toBeDisabled();
    out.observations.push('Reload discards only this fresh context\'s in-memory simulation. No reset/lifecycle/private mutation issued.');
    out.storage = await page.evaluate(async () => ({ local: {...localStorage}, session: {...sessionStorage}, serviceWorkers: (await navigator.serviceWorker.getRegistrations()).length }));
    if (out.errors.length || out.requests.some(r => r.method !== 'GET')) throw Error('Unexpected page error or mutation');
    out.ok = true;
  } finally { await browser.close(); await new Promise(resolve => server.close(resolve)); }
})().catch(e => {out.ok=false;out.failure=String(e);process.exitCode=1;}).finally(() => fs.writeFileSync('tmp/epic12-retro/observation.json', JSON.stringify(out,null,2)+'\n'));
