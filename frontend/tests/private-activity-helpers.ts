import { test, expect, type Page, type BrowserContext } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';
import type { Content } from '../src/PrivateDrafts';
export { test, expect, randomUUID };
export const API = 'http://127.0.0.1:8001';
export const account = { username: 'synthetic-activity-' + randomUUID(), password: randomBytes(24).toString('hex') };
export function python(program: string) {
  if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project selection required');
  return execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'], { cwd: '..', encoding: 'utf8', input: 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n' + program });
}
export function setup() {
test.beforeAll(() => python(`from app.auth import provision\nprovision(${JSON.stringify(account.username)}, ${JSON.stringify(account.password)})\n`));
test.beforeEach(() => python(`with database() as conn:
 owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(account.username)},)).fetchone()['id']
 for table in ['workday_deletions','workday_operations','workdays','drafts','draft_operations','draft_deletions']:
  conn.execute('DELETE FROM '+table+' WHERE owner=%s',(owner,))
 conn.execute('DELETE FROM login_limits')
`));
test.afterAll(() => python(`with database() as conn:
 owner=conn.execute('SELECT id FROM accounts WHERE username=%s', (${JSON.stringify(account.username)},)).fetchone()['id']
 for table in ['workday_deletions','workday_operations','workdays','drafts','draft_operations','draft_deletions','sessions']:
  conn.execute('DELETE FROM '+table+' WHERE owner=%s',(owner,))
 conn.execute('DELETE FROM accounts WHERE id=%s',(owner,))
 conn.execute('DELETE FROM login_limits')
`));
}
export async function post(context: BrowserContext, path: string, body: object) {
  const proof = await (await context.request.get(API + '/auth/csrf')).json();
  const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data: body });
  expect(response.status()).toBe(200); return response.json();
}
export function relativeInstants(seconds: number, anchor?: string): [string, string] {
  // Retention and request deadlines are elapsed durations. Do arithmetic in UTC
  // and serialize each endpoint separately so a DST change cannot add an hour.
  const now = anchor ? `datetime.fromisoformat(${JSON.stringify(anchor)}).astimezone(timezone.utc)` : 'datetime.now(timezone.utc)';
  return JSON.parse(python(`from datetime import datetime,timedelta,timezone\nfrom zoneinfo import ZoneInfo\nimport json\nstart=${now}.replace(microsecond=0)+timedelta(seconds=${seconds})\nend=start+timedelta(minutes=1)\nprint(json.dumps([instant.astimezone(ZoneInfo('Europe/Oslo')).isoformat() for instant in [start,end]]))\n`));
}
export async function openedPlan(page: Page, context: BrowserContext, single = false, relativeStart?: number, firstType?: string, identicalMembers = false, customize?: (content: Content) => void, classifications: Record<string, string> = {}) {
  await page.goto('/private');
  await page.getByLabel('Brukernavn', { exact: true }).fill(account.username);
  await page.getByLabel('Passord', { exact: true }).fill(account.password);
  await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
  const activities = [
    ['trip', '20', 'Nord', '2031-01-02T23:00+01:00', '2031-01-02T23:10+01:00'],
    ['trip', '24', 'Sør', '2031-01-02T23:00+01:00', '2031-01-02T23:10+01:00'],
    ['Coffee', null, null, '2031-01-02T23:10+01:00', '2031-01-02T23:20+01:00'],
    ['MealBreak', null, null, '2031-01-02T23:20+01:00', '2031-01-02T23:30+01:00'],
    ['deadhead', '20', 'Sør', '2031-01-03T00:00+01:00', '2031-01-03T00:10+01:00'],
  ].slice(0, single ? 1 : undefined).map(([type, line, direction, start, end]) => ({ id: randomUUID(), type, line, direction, start, end, to_place: 'Fiktivt langt destinasjonsnavn med mange ord som skal brytes ved forstørring' }));
  if (firstType) { activities[0].type = firstType; activities[0].line = null; activities[0].direction = null; }
  if (identicalMembers) activities[1] = { ...activities[0], id: activities[1].id };
  if (relativeStart !== undefined) {
    const times = relativeInstants(relativeStart);
    activities[0].start = times[0]; activities[0].end = times[1];
  }
  const serviceDate = activities[0].start!.slice(0, 10);
  const content = { service_date: serviceDate, activities, vehicle_duty: null, realtime_duty: null, physical_bus: null } as Content;
  customize?.(content);
  const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: content });
  const review = await post(context, '/workday-reviews', { draft_id: draft.id, expected_revision: 1 });
  const decided = Object.fromEntries(Object.entries(classifications).map(([index, kind]) => [content.activities[Number(index)].id, kind]));
  const plan = await post(context, '/drafts/' + draft.id + '/confirm', { operation_id: review.operation_id, expected_revision: 1, acknowledgements: review.unknowns.filter((item: any) => { const activity = content.activities.find(a => item.id.startsWith(a.id + ':')); return activity && (decided[activity.id] ?? activity.type) === 'trip'; }).map((item: any) => item.id), classifications: decided });
  await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
  await page.getByRole('button', { name: `Åpne plan ${content.service_date} · versjon 1`, exact: true }).click();
  await expect(page.getByText('Ingen aktivitet valgt', { exact: true })).toBeVisible();
  await expect(page.getByText('Ikke startet', { exact: true })).toBeVisible();
  return { draft, plan, activities };
}
export const selected = (page: Page) => page.locator('.selected-activity');
export const activityStatus = (page: Page) => page.getByRole('status', { name: 'Aktivitetsvalgstatus' });
export const shiftStatus = (page: Page) => page.getByRole('status', { name: 'Skiftstatus' });
export const beforeUnload = (page: Page) => page.evaluate(() => { const e = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(e); return e.defaultPrevented; });
export async function dayScreen(page: Page) { if (await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).isVisible()) await page.getByRole('button', { name: 'Tilbake til dagen', exact: true }).click(); }
export async function activityScreen(page: Page) { const open = page.getByRole('button', { name: 'Åpne valgt aktivitet', exact: true }); await expect(selected(page).or(open)).toBeVisible(); if (await open.isVisible()) await open.click(); }
export async function reopen(page: Page) {
  await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
  await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 1', exact: true }).click();
}
