import { preparation, editor } from './private-screen-helpers';
import { test, expect, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';
import { resolve } from 'node:path';

const username = 'synthetic-import-browser-' + randomUUID();
const password = randomBytes(24).toString('hex');
function python(program: string) {
  if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project required');
  return execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'], { cwd: '..', input: 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n' + program, encoding: 'utf8' });
}
let pdf: Buffer;
let partialPdf: Buffer;
let dutyPdf: Buffer;
test.beforeAll(() => {
  python(`from app.auth import provision\nprovision(${JSON.stringify(username)}, ${JSON.stringify(password)})\n`);
  pdf = Buffer.from(python('import sys, base64\nsys.path.insert(0, "/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nprint(base64.b64encode(synthetic_text_pdf()).decode())\n').trim(), 'base64');
  partialPdf = Buffer.from(python(`import sys, base64
sys.path.insert(0, '/app/tests')
from test_pdf_import import pdf_bytes
lines=[(810,'Synthetic Employer - Origin Skift: PARTIAL'),(790,'Date: 01/01/2030 Tue Synthetic Driver'),(770,'Division: Example'),(750,'Skift start: 15:00 Origin Arb.tid: 1h10 Utstrekk: 1h10'),(738,'Skift slutt: 16:10 Destination Tillegg: 25,00%0h00'),(720,'Sign-on 15:00 15:01'),(700,'Travel to 16:00'),(680,'Sign-off 16:00 16:10')]
content='\\n'.join(f'BT /F1 9 Tf 20 {y} Td ({text}) Tj ET' for y,text in lines).encode()
data=pdf_bytes([b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Count 1 /Kids [3 0 R] >>',b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 841] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',f'<< /Length {len(content)} >>\\nstream\\n'.encode()+content+b'\\nendstream'])
print(base64.b64encode(data).decode())
`).trim(), 'base64');
  dutyPdf = Buffer.from(python(`import sys, base64
sys.path.insert(0, '/app/tests')
from test_pdf_import import pdf_bytes
lines=[(810,'Synthetic Employer - Origin Skift: DUTIES'),(790,'Date: 02/01/2030 Wed Synthetic Driver'),(770,'Division: Example'),(750,'Skift start: 15:00 Origin Arb.tid: 1h10 Utstrekk: 1h10'),(738,'Skift slutt: 16:10 Destination Tillegg: 25,00%0h00'),(720,'Sign-on 15:00 15:01'),(705,'Vogn 960181'),(690,'tom / 99 Origin 15:02'),(675,'Destination 15:03'),(660,'Vogn 960176'),(645,'Travel to 16:00'),(630,'Sign-off 16:00 16:10')]
content='\\n'.join(f'BT /F1 9 Tf 20 {y} Td ({text}) Tj ET' for y,text in lines).encode()
data=pdf_bytes([b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Count 1 /Kids [3 0 R] >>',b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 841] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',f'<< /Length {len(content)} >>\\nstream\\n'.encode()+content+b'\\nendstream'])
print(base64.b64encode(data).decode())
`).trim(), 'base64');
});
test.beforeEach(() => python(`with database() as conn:\n owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(username)},)).fetchone()['id']\n conn.execute('DELETE FROM drafts WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM draft_operations WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM draft_deletions WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM login_limits')\n`));
test.afterAll(() => python(`with database() as conn:\n owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(username)},)).fetchone()['id']\n conn.execute('DELETE FROM drafts WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM draft_operations WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM draft_deletions WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM sessions WHERE owner=%s',(owner,))\n conn.execute('DELETE FROM accounts WHERE id=%s',(owner,))\n conn.execute('DELETE FROM login_limits')\n`));
async function login(page: Page) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(username);
  await page.getByLabel('Passord', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
}
async function upload(page: Page) {
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: pdf });
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toBeVisible();
}

for (const width of [768, 1440]) test(`corrections structure legacy duties cancel and reopen at ${width}px`, async ({ page }) => {
  await page.setViewportSize({ width, height: 1100 });
  await login(page);
  let source: any;
  await page.route('**:8001/imports/pdf', async route => {
    const value = await (await route.fetch()).json(); delete value.vehicle_duty_changes;
    source = structuredClone(value.import_metadata); await route.fulfill({ json: value });
  });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'corrections.pdf', mimeType: 'application/pdf', buffer: dutyPdf });
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).click();
  const row = () => page.locator('#activity-' + source.activities[2].activity_id);
  await expect(page.locator('.correction-marker')).toHaveCount(0);
  const first = page.locator('#activity-' + source.activities[0].activity_id);
  await first.getByLabel('Opprinnelig startklokke', { exact: true }).fill('15:00:00');
  await first.getByLabel('Starttid', { exact: true }).fill('15:00');
  await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeEnabled();
  await expect(first.locator('.correction-marker')).toHaveCount(0);
  await first.locator('summary').click();
  for (const [input, field, clock] of [['Starttid', 'Start med dato', '15:00'], ['Sluttid', 'Slutt med dato', '15:01']]) {
    const fact = first.locator('.comparison-fact').filter({ has: page.locator('dt').filter({ hasText: field }) });
    await first.getByLabel(input, { exact: true }).fill('');
    await expect(first.locator('.pending-time')).toContainText('er uavklart');
    await expect(fact).toContainText('Gjeldende: Inntastet tidspunkt er uavklart');
    await expect(fact).toContainText('Opprinnelig: 2030-01-02T');
    await expect(fact.locator('.correction-marker')).toHaveCount(0);
    await expect(first.locator('.correction-marker')).toHaveCount(0);
    await expect(first.locator('.current-unknown')).not.toContainText(input === 'Starttid' ? 'start' : 'slutt');
    await expect(first.getByLabel(input, { exact: true })).toHaveValue('');
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeDisabled();
    await first.getByLabel(input, { exact: true }).fill(clock);
    await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeEnabled();
    await expect(first.locator('.pending-time')).toHaveCount(0);
  }
  await first.getByLabel('Starttid', { exact: true }).fill('15:00:30');
  await expect(page.getByRole('button', { name: 'Lagre utkast', exact: true })).toBeEnabled();
  await expect(first.getByText('Manuelt rettet fra opprinnelig tolkning.', { exact: false })).toBeVisible();
  await expect(row()).toContainText('Gjeldende ukjente fakta: aktivitetstype, start, fra sted, til sted');
  await row().getByLabel('Aktivitetstype', { exact: true }).fill('deadhead');
  await row().getByLabel('Fra sted', { exact: true }).fill('Manuelt sted med langt navn for kontroll av linjebryting');
  await row().getByLabel('Turnummer', { exact: true }).fill('Manual-09');
  async function assertPlaceTripAndRestoration() {
    const fact = (label: string) => row().locator('.comparison-fact').filter({ has: page.locator('dt').filter({ hasText: new RegExp('^' + label) }) });
    for (const [label, value] of [['Fra sted', 'Manuelt sted med langt navn for kontroll av linjebryting'], ['Turnummer', 'Manual-09']]) {
      await expect(fact(label)).toContainText('Opprinnelig: Ukjent');
      await expect(fact(label)).toContainText('Gjeldende: ' + value);
      await expect(fact(label).locator('.correction-marker')).toHaveCount(1);
      await row().getByLabel(label, { exact: true }).fill('');
      await expect(fact(label).locator('.correction-marker')).toHaveCount(0);
      await expect(fact(label)).toContainText('Gjeldende: Ukjent');
      await expect(fact(label === 'Fra sted' ? 'Turnummer' : 'Fra sted').locator('.correction-marker')).toHaveCount(1);
      await expect(fact('Aktivitetstype').locator('.correction-marker')).toHaveCount(1);
      await row().getByLabel(label, { exact: true }).fill(value);
      await expect(fact(label).locator('.correction-marker')).toHaveCount(1);
    }
  }
  await assertPlaceTripAndRestoration();
  await row().getByRole('button', { name: 'Flytt opp', exact: true }).click();
  await expect(row().getByLabel('Vognløp fra aktivitet 2', { exact: true })).toHaveValue('960176');
  await expect(row()).toContainText('Manuelt rettet fra opprinnelig tolkning');
  await row().getByRole('button', { name: 'Flytt opp', exact: true }).click();
  await expect(row().getByRole('button', { name: 'Flytt opp', exact: true })).toBeDisabled();
  await editor(page); await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
  const manual = page.getByRole('group', { name: 'Aktivitet 5', exact: true });
  await expect(manual).toContainText('Manuell aktivitet');
  await manual.getByLabel('Aktivitetstype', { exact: true }).fill('Manuelt arbeid');
  await manual.getByRole('button', { name: 'Flytt opp', exact: true }).click();
  const response = page.waitForResponse(r => r.request().method() === 'POST' && new URL(r.url()).pathname === '/drafts');
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const saved = await (await response).json();
  expect(saved.draft.import_metadata).toEqual(source);
  expect(saved.draft.activities.find((activity: any) => activity.id === source.activities[0].activity_id).start).toBe('2030-01-02T15:00:30+01:00');
  expect(saved.draft.vehicle_duty_changes[0].from_activity_id).toBe(source.activities[2].activity_id);
  await row().getByLabel('Aktivitetstype', { exact: true }).fill('cancel-me');
  await page.getByRole('group', { name: 'Aktivitet 2', exact: true }).getByRole('button', { name: 'Flytt opp', exact: true }).click();
  await editor(page); await page.getByRole('button', { name: 'Legg til aktivitet' }).click();
  page.once('dialog', d => d.dismiss()); await editor(page); await page.getByRole('button', { name: 'Forkast endringer' }).click();
  await expect(row().getByLabel('Aktivitetstype', { exact: true })).toHaveValue('cancel-me');
  await expect(page.getByLabel('Aktivitetstype', { exact: true })).toHaveCount(6);
  page.once('dialog', d => d.accept()); await editor(page); await page.getByRole('button', { name: 'Forkast endringer' }).click();
  await expect(page.getByLabel('Aktivitetstype', { exact: true })).toHaveCount(5);
  await expect(row().getByLabel('Vognløp fra aktivitet 1', { exact: true })).toHaveValue('960176');
  expect(await (await page.request.get('http://127.0.0.1:8001/drafts/' + saved.id)).json()).toEqual(saved);
  await page.reload(); await preparation(page); await page.getByRole('button', { name: /Åpne 2030-01-02/ }).first().click();
  await expect(first.getByLabel('Starttid', { exact: true })).toHaveValue('15:00:30');
  await expect(first.getByText('Manuelt rettet fra opprinnelig tolkning.', { exact: false })).toBeVisible();
  await expect(row().getByLabel('Aktivitetstype', { exact: true })).toHaveValue('deadhead');
  await row().locator('summary').focus(); await page.keyboard.press('Enter');
  await expect(row().locator('summary')).toBeFocused();
  await expect(row()).toContainText('Opprinnelig: Ukjent');
  await expect(row()).toContainText('Gjeldende: deadhead');
  await assertPlaceTripAndRestoration();
  await row().getByLabel('Aktivitetstype', { exact: true }).fill('');
  await expect(row().locator('.comparison-fact').filter({ has: page.locator('dt:text-is("Aktivitetstype")') })).not.toContainText('Manuelt rettet');
  await row().getByLabel('Aktivitetstype', { exact: true }).fill('deadhead');
  for (const night of [false, true]) {
    const toggle = page.getByRole('button', { name: 'Nattmodus' });
    if ((await toggle.getAttribute('aria-pressed') === 'true') !== night) await toggle.click();
    for (const control of [row().locator('summary'), page.getByRole('region', { name: 'Usikkerheter fra importen' }).getByRole('button').first(), row().getByLabel('Usikkerhet / ukjente fakta', { exact: true })]) {
      await control.focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab');
      await expect(control).toBeFocused();
      await expect(control).toHaveCSS('outline-width', '3px');
      const lightPanel = await control.evaluate(element => !!element.closest('.import-warning, .current-unknown'));
      await expect(control).toHaveCSS('outline-color', night && !lightPanel ? 'rgb(255, 227, 155)' : 'rgb(0, 0, 0)');
    }
  }
  if (width === 1440) await page.getByRole('button', { name: 'Nattmodus' }).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await row().locator('summary').focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab');
  await expect(row().locator('summary')).toBeFocused();
  await row().scrollIntoViewIfNeeded();
  await page.screenshot({ path: `../docs/evidence/11-2-regression-10-2-${width}.png` });
  expect(await page.evaluate(async () => [localStorage.length, sessionStorage.length, (await indexedDB.databases()).length])).toEqual([0, 0, 0]);
  page.once('dialog', d => d.accept()); await row().getByRole('button', { name: 'Fjern aktivitet 1', exact: true }).click();
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByText('Lagret. Versjon 2.', { exact: true })).toBeVisible();
  const removed = await (await page.request.get('http://127.0.0.1:8001/drafts/' + saved.id)).json();
  expect(removed.draft.import_metadata).toEqual(source);
  expect(removed.draft.vehicle_duty_changes).toEqual([]);
});

for (const number of [8, 9]) test(`approved example ${number} preserves work and vehicle changes through save and reopen`, async ({ page }) => {
  await login(page);
  let facts: any;
  // Read genuine API bodies in the pass-through handler. Edge can evict the
  // inspector response cache after a real PDF upload, before Response.json().
  await page.route('**:8001/imports/pdf', async route => {
    const response = await route.fetch(); facts = await response.json(); await route.fulfill({ response });
  });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles(resolve(`../Eksempelfiler/Eksempel-${number}-anonymisert.pdf`));
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toBeVisible();
  const count = number === 8 ? 23 : 8;
  expect(facts.activities).toHaveLength(count);
  expect(facts.import_metadata.unresolved).toEqual([]);
  const source = page.getByRole('region', { name: 'Kildefakta fra PDF' });
  if (number === 8) {
    await expect(source).toContainText('CAR - 1');
    await expect(source).toContainText('Tomkjøring med CAR');
    await expect(source).not.toContainText('deadhead_car');
    expect(facts.vehicle_duty_changes.map((c: any) => [c.vehicle_duty, c.realtime_duty])).toEqual([['960176', '176'], ['CAR - 1', null]]);
  } else {
    await expect(source).toContainText('Fadder'); await expect(source).toContainText('Instruktør');
    expect(facts.activities.map((a: any) => a.type)).toEqual(['Sign-on', 'Fadder', 'Coffee', 'Fadder', 'Coffee', 'Fadder', 'Coffee', 'Instruktør']);
  }
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).click();
  const checkEditor = async () => {
    await expect(page.locator('.correction-marker')).toHaveCount(0);
    await expect(page.getByLabel('Aktivitetstype', { exact: true })).toHaveCount(count);
    await expect(page.locator('details.source-disclosure')).not.toHaveAttribute('open');
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
    if (number === 8) {
      await expect(page.getByLabel('Vognløp fra aktivitet 14', { exact: true })).toHaveValue('960176');
      await expect(page.getByLabel('Vognløp fra aktivitet 21', { exact: true })).toHaveValue('CAR - 1');
      await expect(page.getByLabel('Aktivitetstype', { exact: true }).nth(20)).toHaveValue('CAR');
      await expect(page.getByLabel('Aktivitetstype', { exact: true }).nth(21)).toHaveValue('Tomkjøring med CAR');
    } else {
      await expect(page.getByLabel('Aktivitetstype', { exact: true }).nth(1)).toHaveValue('Fadder');
      await expect(page.getByLabel('Aktivitetstype', { exact: true }).nth(7)).toHaveValue('Instruktør');
    }
  };
  await checkEditor();
  let saved: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    const response = await route.fetch(); saved = await response.json(); await route.fulfill({ response });
  });
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByText('Lagret. Versjon 1.', { exact: true })).toBeVisible();
  expect(saved.draft).toEqual(facts);
  await page.reload();
  await page.getByRole('button', { name: new RegExp(`Åpne 2030-01-${number === 8 ? '10' : '14'}`) }).first().click();
  await checkEditor();
  expect(await (await page.request.get('http://127.0.0.1:8001/drafts/' + saved.id)).json()).toEqual(saved);
  await page.getByRole('group', { name: `Aktivitet ${number === 8 ? 22 : 2}`, exact: true }).screenshot({ path: `../docs/evidence/11-2-regression-10-1-example-${number}-activity.png` });
});
for (const width of [768, 1440]) test(`keyboard review separate adoption save recovery reopen at ${width}px`, async ({ page }) => {
  await page.setViewportSize({ width, height: 1100 });
  await login(page); await upload(page);
  const facts = page.getByRole('region', { name: 'Kildefakta fra PDF' });
  await expect(facts).toContainText('Kildestart');
  await expect(facts).toContainText('N (side 1, kolonne 1, linje 3)');
  await expect(facts).toContainText('side 1, overskrift, felt Tjenestedato');
  await expect(facts).toContainText('Avledningsgrunnlag per kalenderfelt');
  await expect(facts).toContainText('aktivitet 1: Startklokke, overskrift: Tjenestedato');
  await expect(facts).toContainText('entydig tidspunkt innenfor oppgitt skiftintervall');
  await expect(facts).not.toContainText('Synthetic Driver');
  expect(await page.getByLabel('Velg tekst-PDF', { exact: true }).inputValue()).toBe('');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: `../docs/evidence/11-2-regression-10-1-${width}.png`, fullPage: true });
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).focus(); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Nytt manuelt utkast' })).toBeFocused();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
  let accepted: any;
  await page.route('**:8001/drafts', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    accepted = await (await route.fetch()).json(); await route.abort();
  });
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByText('Lagring er uavklart.', { exact: false })).toBeVisible();
  await page.unroute('**:8001/drafts');
  await page.getByRole('button', { name: 'Kontroller lagringsforsøket' }).click();
  await expect(page.getByText('Lagret. Versjon 1.', { exact: true })).toBeVisible();
  await page.getByLabel('Vognløp', { exact: true }).fill('0007');
  page.once('dialog', d => d.accept()); await editor(page); await page.getByRole('button', { name: 'Forkast endringer' }).click();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('');
  await page.reload();
  await preparation(page); await page.getByRole('button', { name: /Åpne 2030-01-01/ }).first().click();
  expect(await (await page.request.get('http://127.0.0.1:8001/drafts/' + accepted.id)).json()).toEqual(accepted);
  await expect(page.locator('details.source-disclosure')).not.toHaveAttribute('open');
  await page.getByText('Vis kildefakta fra PDF', { exact: true }).click();
  await expect(page.getByRole('region', { name: 'Kildefakta fra PDF' })).toContainText('Kildestart');
  expect(await page.evaluate(async () => [localStorage.length, sessionStorage.length, (await indexedDB.databases()).length])).toEqual([0, 0, 0]);
});

test('failed review keeps editor and edit protection guards separate adoption', async ({ page }) => {
  await login(page);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('Earlier-001');
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'broken.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-corrupt') });
  await expect(page.getByText('PDF-en kunne ikke tolkes.', { exact: false })).toBeVisible();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Earlier-001');
  await page.screenshot({ path: '../docs/evidence/11-2-regression-10-1-error.png', fullPage: true });
  await upload(page);
  page.once('dialog', d => d.dismiss()); await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Earlier-001');
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toBeVisible();
  page.once('dialog', d => d.accept()); await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).click();
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('');
});

test('cancel and logout discard late replies and raw selection', async ({ page }) => {
  await login(page);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('Earlier');
  let release!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  await page.route('**:8001/imports/pdf', async route => { const response = await route.fetch(); await gate; await route.fulfill({ response }).catch(() => {}); });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: pdf });
  await page.getByRole('button', { name: 'Avbryt import' }).click(); release();
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toHaveCount(0);
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Earlier');
  await page.unroute('**:8001/imports/pdf'); await upload(page);
  page.once('dialog', d => d.accept()); await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Kildefakta fra PDF' })).toHaveCount(0);
  await expect(page.getByLabel('Velg tekst-PDF', { exact: true })).toHaveCount(0);
});

test('invalid metadata or HTML cannot become a review', async ({ page }) => {
  await login(page);
  await page.route('**:8001/imports/pdf', route => route.fulfill({ contentType: 'text/html', body: '<html>login</html>' }));
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: pdf });
  await expect(page.getByText('PDF-en kunne ikke tolkes.', { exact: false })).toBeVisible();
  await page.unroute('**:8001/imports/pdf');
  await page.route('**:8001/imports/pdf', async route => { const value = await (await route.fetch()).json(); value.import_metadata.header.driver = 'forbidden'; await route.fulfill({ json: value }); });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: pdf });
  await expect(page.getByText('PDF-en kunne ikke tolkes.', { exact: false })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toHaveCount(0);
});

test('unknown uncertainty references keep code field column and line', async ({ page }) => {
  await login(page);
  await page.route('**:8001/imports/pdf', async route => {
    const value = await (await route.fetch()).json();
    value.import_metadata.unresolved.push({ code: 'future_source_issue', field: 'unknown_field', activity: 2, provenance: { page: 1, column: 2, line: 9, region: null, field: null } });
    await route.fulfill({ json: value });
  });
  await upload(page);
  await expect(page.getByRole('region', { name: 'Kildefakta fra PDF' })).toContainText('Aktivitet 2: Ukjent kildeusikkerhet (future_source_issue) (unknown_field) · side 1, kolonne 2, linje 9');
});

for (const state of ['hidden', 'expired']) test(`delayed import is discarded after ${state} access revalidation`, async ({ page }) => {
  await login(page);
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('Earlier-private');
  let release!: () => void, started!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const accepted = new Promise<void>(resolve => { started = resolve; });
  await page.route('**:8001/imports/pdf', async route => { const response = await route.fetch(); started(); await gate; await route.fulfill({ response }).catch(() => {}); });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: pdf });
  await accepted;
  if (state === 'expired') python(`with database() as conn:\n conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner IN (SELECT id FROM accounts WHERE username=%s)", (${JSON.stringify(username)},))\n`);
  else await page.route('**:8001/auth/session', route => route.abort());
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange'));
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange'));
  });
  if (state === 'expired') await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  else await expect(page.getByRole('button', { name: 'Kontroller tilgang igjen' })).toBeEnabled();
  release();
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toHaveCount(0);
  await expect(page.getByRole('region', { name: 'Kildefakta fra PDF' })).toHaveCount(0);
  if (state === 'expired') await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveCount(0);
  else {
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toBeHidden();
    await page.unroute('**:8001/auth/session');
    await page.getByRole('button', { name: 'Kontroller tilgang igjen' }).click();
    await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Earlier-private');
    await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toHaveCount(0);
  }
});

test('partial fictional Travel to preserves known end and unresolved facts through save reopen', async ({ page }) => {
  await login(page);
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'partial-fictional.pdf', mimeType: 'application/pdf', buffer: partialPdf });
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toBeVisible();
  async function assertPartial() {
    const facts = page.getByRole('region', { name: 'Kildefakta fra PDF' });
    await expect(facts).toContainText('Delvis tolkning');
    const row = facts.getByRole('listitem').filter({ has: page.getByRole('heading', { name: '2. Travel to · side 1', exact: true }) });
    await expect(row.locator('dt:text-is("Kildeslutt") + dd')).toContainText('16:00');
    await expect(row.locator('dt:text-is("Kildestart") + dd')).toContainText('Ukjent / uavklart');
    await expect(row.locator('dt:text-is("Fra") + dd')).toContainText('Ukjent / uavklart');
    await expect(row.locator('dt:text-is("Til") + dd')).toContainText('Ukjent / uavklart');
    await expect(row.locator('dt:text-is("Tolket type") + dd')).toContainText('Ukjent / uavklart');
    await expect(row).not.toContainText('deadhead');
  }
  await assertPartial();
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).click();
  await expect(page.getByLabel('Starttid', { exact: true }).nth(1)).toHaveValue('');
  await expect(page.getByLabel('Sluttid', { exact: true }).nth(1)).toHaveValue('16:00:00');
  await expect(page.getByLabel('Aktivitetstype', { exact: true }).nth(1)).toHaveValue('');
  await expect(page.getByLabel('Fra sted', { exact: true }).nth(1)).toHaveValue('');
  await expect(page.getByLabel('Til sted', { exact: true }).nth(1)).toHaveValue('');
  const savedResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/drafts');
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  const saved = await (await savedResponse).json();
  expect(saved.draft.activities[1]).toEqual(expect.objectContaining({ raw_code: 'Travel to', source_end: '16:00', start: null, type: null, from_place: null, to_place: null }));
  await page.reload();
  await preparation(page); await page.getByRole('button', { name: /Åpne 2030-01-01/ }).first().click();
  await expect(page.locator('details.source-disclosure')).not.toHaveAttribute('open');
  await page.getByText('Vis kildefakta fra PDF', { exact: true }).click();
  await assertPartial();
  expect(await (await page.request.get('http://127.0.0.1:8001/drafts/' + saved.id)).json()).toEqual(saved);
});

test('duty changes, readable uncertainty and collapsed facts survive editing and reopen', async ({ page }) => {
  await login(page);
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'fictional-duty-changes.pdf', mimeType: 'application/pdf', buffer: dutyPdf });
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toBeVisible();
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).click();
  await expect(page.locator('details.source-disclosure')).not.toHaveAttribute('open');
  await expect(page.getByRole('region', { name: 'Kildefakta fra PDF', includeHidden: true })).toBeHidden();
  await expect(page.getByLabel('Vognløp', { exact: true })).toHaveValue('960181');
  await expect(page.getByLabel('Vognløp fra aktivitet 3', { exact: true })).toHaveValue('960176');
  const third = page.getByRole('group', { name: 'Aktivitet 3', exact: true });
  const fourth = page.getByRole('group', { name: 'Aktivitet 4', exact: true });
  await expect(third).toContainText('Gjeldende vognløp: 960176 · sanntidsverdi 176');
  await expect(fourth).toContainText('Gjeldende vognløp: 960176 · sanntidsverdi 176');
  await expect(page.getByRole('region', { name: 'Usikkerheter fra importen' })).toContainText('Kontroller start');
  await expect(page.getByLabel('Usikkerhet / ukjente fakta', { exact: true }).nth(2)).toHaveValue(/Kontroller start.*Travel to/);
  await page.getByRole('button', { name: 'Se aktivitet 3', exact: true }).first().click();
  await expect(third).toBeFocused();
  await editor(page); await page.getByLabel('Buss/vogn', { exact: true }).fill('Bus-42');
  await page.getByLabel('Vognløp fra aktivitet 3', { exact: true }).fill('960006');
  await page.getByRole('button', { name: 'Bytt vognløp fra aktivitet 2', exact: true }).click();
  await page.getByLabel('Vognløp fra aktivitet 2', { exact: true }).fill('960090');
  await expect(fourth).toContainText('Gjeldende vognløp: 960006 · sanntidsverdi 006');
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByText('Lagret. Versjon 1.', { exact: true })).toBeVisible();
  await page.reload();
  await preparation(page); await page.getByRole('button', { name: /Åpne 2030-01-02/ }).first().click();
  await expect(page.getByLabel('Vognløp fra aktivitet 2', { exact: true })).toHaveValue('960090');
  await expect(page.getByLabel('Vognløp fra aktivitet 3', { exact: true })).toHaveValue('960006');
  await expect(page.getByLabel('Buss/vogn', { exact: true })).toHaveValue('Bus-42');
  await expect(page.locator('details.source-disclosure')).not.toHaveAttribute('open');
  await expect(page.getByRole('region', { name: 'Usikkerheter fra importen' })).toContainText('Aktivitetstypen er uavklart');
  await page.screenshot({ path: '../docs/evidence/11-2-regression-10-1-amended-editor.png', fullPage: true });
  await page.getByRole('button', { name: 'Fjern vognløpsbytte fra aktivitet 3', exact: true }).click();
  await expect(fourth).toContainText('Gjeldende vognløp: 960090 · sanntidsverdi 090');
  await page.getByRole('button', { name: 'Fjern vognløpsbytte fra aktivitet 2', exact: true }).click();
  await expect(fourth).toContainText('Gjeldende vognløp: 960181 · sanntidsverdi 181');
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByText('Lagret. Versjon 2.', { exact: true })).toBeVisible();
  await page.reload();
  await preparation(page); await page.getByRole('button', { name: /Åpne 2030-01-02/ }).first().click();
  await expect(page.getByLabel(/^Vognløp fra aktivitet/)).toHaveCount(0);
  await expect(fourth).toContainText('Gjeldende vognløp: 960181 · sanntidsverdi 181');
});

test('legacy imported duty occurrences remain editable without rewriting original metadata', async ({ page }) => {
  await login(page);
  await page.route('**:8001/imports/pdf', async route => {
    const value = await (await route.fetch()).json();
    delete value.vehicle_duty_changes;
    for (const activity of value.activities) activity.uncertainty = null;
    await route.fulfill({ json: value });
  });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'legacy-fictional.pdf', mimeType: 'application/pdf', buffer: dutyPdf });
  await page.getByRole('button', { name: 'Bruk som separat nytt utkast' }).click();
  await expect(page.getByLabel('Vognløp fra aktivitet 3', { exact: true })).toHaveValue('960176');
  await expect(page.getByRole('region', { name: 'Usikkerheter fra importen' })).toContainText('Kontroller start');
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByText('Lagret. Versjon 1.', { exact: true })).toBeVisible();
  await page.reload();
  await preparation(page); await page.getByRole('button', { name: /Åpne 2030-01-02/ }).first().click();
  await expect(page.getByLabel('Vognløp fra aktivitet 3', { exact: true })).toHaveValue('960176');
  await page.getByRole('button', { name: 'Fjern vognløpsbytte fra aktivitet 3', exact: true }).click();
  await editor(page); await page.getByRole('button', { name: 'Lagre utkast', exact: true }).click();
  await expect(page.getByText('Lagret. Versjon 2.', { exact: true })).toBeVisible();
  await page.reload();
  await preparation(page); await page.getByRole('button', { name: /Åpne 2030-01-02/ }).first().click();
  await expect(page.getByLabel(/^Vognløp fra aktivitet/)).toHaveCount(0);
});

test('upload holds the mutation lock from rotating proof through cancellation', async ({ page }) => {
  await login(page);
  let release!: () => void, started!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const proofStarted = new Promise<void>(resolve => { started = resolve; });
  await page.route('**:8001/auth/csrf', async route => { const response = await route.fetch(); started(); await gate; await route.fulfill({ response }).catch(() => {}); });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: pdf });
  await proofStarted;
  await page.evaluate(() => {
    (window as any).competingMutationEntered = false;
    void navigator.locks.request('private-auth-mutations', async () => { (window as any).competingMutationEntered = true; });
  });
  expect(await page.evaluate(() => (window as any).competingMutationEntered)).toBe(false);
  await page.getByRole('button', { name: 'Avbryt import' }).click();
  await expect.poll(() => page.evaluate(() => (window as any).competingMutationEntered)).toBe(true);
  release();
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toHaveCount(0);
});

test('logout promptly cancels an import holding the mutation lock', async ({ page }) => {
  await login(page);
  let release!: () => void, started!: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  const accepted = new Promise<void>(resolve => { started = resolve; });
  await page.route('**:8001/imports/pdf', async route => { const response = await route.fetch(); started(); await gate; await route.fulfill({ response }).catch(() => {}); });
  await preparation(page); await page.getByLabel('Velg tekst-PDF', { exact: true }).setInputFiles({ name: 'synthetic.pdf', mimeType: 'application/pdf', buffer: pdf });
  await accepted;
  await page.getByRole('button', { name: 'Logg ut', exact: true }).click();
  await expect(page.getByRole('status', { name: 'Tilgangsstatus' })).toHaveText('Du er logget ut.');
  await expect(page.getByLabel('Brukernavn', { exact: true })).toBeVisible();
  release();
  await expect(page.getByRole('button', { name: 'Bruk som separat nytt utkast' })).toHaveCount(0);
});
