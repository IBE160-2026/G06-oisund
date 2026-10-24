import { test, expect, type BrowserContext, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { randomUUID, randomBytes } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { projectDay, osloDateTime } from '../src/dayOverview';
import type { Content } from '../src/PrivateDrafts';

const activity = (type: string, start: string, end: string, extra: Record<string, string | null> = {}) => ({ id: randomUUID(), type, start: `2031-01-02T${start}+01:00`, end: `2031-01-02T${end}+01:00`, ...extra });
const content = (activities: Content['activities'], extra: Partial<Content> = {}): Content => ({ service_date: '2031-01-02', vehicle_duty: '960006', realtime_duty: '006', physical_bus: null, activities, ...extra });
for (const [name, kinds, expected] of [
  ['example 2', ['MealBreak', 'Paid meal before'], 'Matpause'],
  ['example 7', ['Paid meal after', 'MealBreak'], 'Matpause'],
  ['meal precedence', ['Split break', 'MealBreak'], 'Matpause'],
  ['split precedence', ['Coffee', 'Split break'], 'Deltskiftpause'],
  ['coffee only', ['Coffee', 'Coffee'], 'Kaffepause'],
  ['paid mixed', ['Coffee', 'Paid meal after'], 'Betalt matpause'],
] as const) test(`projection ${name} recomputes touching pause classification`, () => {
  const starts = name === 'example 7' ? ['08:52', '08:58', '09:28'] : ['12:01', '12:31', '12:43'];
  const input = content([activity(kinds[0], starts[0], starts[1]), activity(kinds[1], starts[1], starts[2])]);
  const before = structuredClone(input);
  Object.freeze(input.activities); input.activities.forEach(Object.freeze); Object.freeze(input);
  const result = projectDay(input).rows;
  expect(result).toHaveLength(1);
  expect(result[0]).toMatchObject({ label: expected, start: before.activities[0].start, end: before.activities[1].end });
  if (result[0].type !== 'activity') throw Error();
  expect(result[0].members.map(member => member.activity.id)).toEqual(before.activities.map(a => a.id));
  expect(input).toEqual(before);
});
for (const [type, label] of [['Paid meal before', 'Betalt matpause før'], ['Paid meal after', 'Betalt matpause etter']]) test(`projection preserves single ${type} without raw code`, () => {
  expect(projectDay(content([activity(type, '08:00', '08:10')])).rows[0]).toMatchObject({ label });
});

test('projection retains separate pauses, equal starts, zero intervals and repeated trip IDs', () => {
  const input = content([activity('Coffee', '08:00', '08:10'), activity('trip', '08:10', '09:00', { trip: '1001' }), activity('Coffee', '09:00', '09:05'), activity('CAR', '09:05', '09:05', { trip: '1001' }), activity('deadhead_car', '09:05', '09:20', { trip: '1001' }), activity('Coffee', '09:21', '09:30')]);
  const rows = projectDay(input).rows;
  expect(rows.filter(row => row.type === 'activity').map(row => row.id)).toEqual(input.activities.map(a => a.id));
  expect(rows.filter(row => row.type === 'gap')).toHaveLength(1);
  expect(rows[3]).toMatchObject({ label: 'CAR', start: input.activities[3].start, end: input.activities[3].end });
});

test('projection gap follows greatest preceding end across nested overlaps', () => {
  const rows = projectDay(content([activity('manual', '08:00', '10:00'), activity('manual', '08:30', '09:00'), activity('manual', '09:15', '09:30'), activity('manual', '10:30', '11:00')])).rows;
  expect(rows.filter(row => row.type === 'activity').map(row => row.overlap)).toEqual([false, true, true, false]);
  expect(rows.filter(row => row.type === 'gap')).toEqual([{ type: 'gap', id: 'gap-before-' + rows.at(-1)!.id, start: '2031-01-02T10:00+01:00', end: '2031-01-02T10:30+01:00' }]);
});

test('projection uses corrected classifications and dates, reporting and duty anchors', () => {
  const a = activity('legacy', '22:36', '22:39');
  const b = activity('trip', '23:50', '23:59', { end: '2031-01-03T00:35+01:00', trip: '6072' });
  const c = activity('Sign-on', '01:15', '01:17', { start: '2031-01-03T01:15+01:00', end: '2031-01-03T01:17+01:00' });
  const d = activity('deadhead_car', '01:17', '01:30', { start: '2031-01-03T01:17+01:00', end: '2031-01-03T01:30+01:00' });
  const result = projectDay(content([a, b, c, d], { vehicle_duty_changes: [{ from_activity_id: c.id, vehicle_duty: '960090', realtime_duty: '090' }, { from_activity_id: d.id, vehicle_duty: 'CAR - 1', realtime_duty: null }] }), { [a.id]: 'Sign-on' });
  expect(result.reporting.map(m => m.activity.id)).toEqual([a.id, c.id]);
  expect(result.rows.filter(row => row.type === 'activity').flatMap(row => row.members.map(member => [member.duty, member.suffix]))).toEqual([['960006', '006'], ['960006', '006'], ['960090', '090'], ['CAR - 1', null]]);
  expect(osloDateTime(b.end!)).toBe('03.01.2031, 00:35');
});

test('projection retains boundaries within grouped pauses and ignores historical metadata groups', () => {
  const a = activity('MealBreak', '08:52', '08:58'), b = activity('Paid meal after', '08:58', '09:28');
  const input = content([a, b], { vehicle_duty_changes: [{ from_activity_id: b.id, vehicle_duty: '960090', realtime_duty: '090' }], import_metadata: { activities: [], duties: [], pause_groups: [{ rows: [1, 2], kind: 'coffee' }] } as any });
  const row = projectDay(input).rows[0];
  expect(row).toMatchObject({ label: 'Matpause' });
  if (row.type !== 'activity') throw Error();
  expect(row.members.map(m => m.duty)).toEqual(['960006', '960090']);
  a.type = 'manual';
  expect(projectDay(input).rows.filter(row => row.type === 'activity').map(row => row.label)).toEqual(['Manuelt klassifisert arbeid', 'Betalt matpause etter']);
});

// Independent, owner-approved source transcriptions, not adapter output. These
// tests exercise presentation of confirmed facts without importing real files.
const fixtureCases = [
  ...JSON.parse(readFileSync(new URL('../../backend/tests/fixtures/import_expected.json', import.meta.url), 'utf8').replace(/^\uFEFF/, '')).fixtures,
  ...JSON.parse(readFileSync(new URL('../../backend/tests/fixtures/import_additional_expected.json', import.meta.url), 'utf8').replace(/^\uFEFF/, '')).fixtures,
];
for (const [index, fixture] of fixtureCases.entries()) test(`projection independent example ${index + 1} preserves every confirmed source member`, () => {
  const number = index + 1;
  const serviceDate = fixture.header?.service_date ?? `2030-01-${number === 8 ? '10' : '14'}`;
  const instant = (clock: string, day: number) => new Date(Date.parse(serviceDate + 'T00:00Z') + day * 86400000).toISOString().slice(0, 10) + 'T' + clock + '+01:00';
  const activities = fixture.activities.map((row: any, i: number) => ({
    id: 'fixture-' + number + '-' + i,
    type: row.kind ?? (row.line ? 'trip' : row.label === 'tom' ? number === 8 && i === 21 ? 'deadhead_car' : 'deadhead' : row.label),
    raw_code: row.label, start: instant(row.start, row.start_day ?? 0), end: instant(row.end, row.end_day ?? 0),
    from_place: row.origin, to_place: row.destination, line: row.line, trip: row.trip_id,
    provenance: row.owner_fields?.length ? 'Avklart av prosjekteier' : 'Kilde',
  }));
  const duties = fixture.duties ?? (number === 8 ? ['960181', '960176', 'CAR - 1'] : []);
  const anchors = fixture.duty_after_activities ?? (number === 8 ? [1, 13, 20] : []);
  const input = content(activities, { service_date: serviceDate, vehicle_duty: duties[0] ?? null, vehicle_duty_changes: duties.slice(1).map((duty: string, i: number) => ({ from_activity_id: activities[anchors[i + 1]].id, vehicle_duty: duty, realtime_duty: /^\d+$/.test(duty) ? duty.slice(-3) : null })) });
  const result = projectDay(input);
  const rows = result.rows.filter(row => row.type === 'activity');
  expect(rows).toHaveLength([33, 15, 6, 16, 5, 16, 20, 22, 8][index]);
  expect(rows.flatMap(row => row.members.map(member => member.activity))).toEqual(activities);
  const flattened = rows.flatMap(row => row.members);
  const transitions = flattened.filter((member, i) => i === 0 || member.duty !== flattened[i - 1].duty).map(member => [member.index + 1, member.activity.start!.slice(11, 16), member.duty]);
  expect(transitions).toEqual([
    [[1, '06:08', '960300'], [27, '15:10', '960301']], [[1, '07:51', '960146']], [[1, '06:51', '960127']],
    [[1, '22:36', '960090']], [[1, '06:51', '960006']], [[1, '04:50', '960078'], [11, '15:06', '960109']],
    [[1, '04:49', '960077'], [18, '14:39', '960110']], [[1, '06:17', '960181'], [14, '10:30', '960176'], [21, '14:58', 'CAR - 1']], [[1, '04:40', null]],
  ][index]);
  const gaps = result.rows.filter(row => row.type === 'gap').map(row => [row.start.slice(11, 16), row.end.slice(11, 16)]);
  if (number === 1) { expect(rows.find(row => row.start.slice(11, 16) === '10:50')).toMatchObject({ label: 'Deltskiftpause' }); expect(gaps).toContainEqual(['06:11', '06:18']); }
  if (number === 2) expect(gaps).toContainEqual(['09:59', '10:25']);
  if (number === 4) expect(rows.find(row => row.start.slice(11, 16) === '00:45')).toMatchObject({ label: 'Matpause' });
  if (number === 5 || number === 9) expect(gaps).not.toContainEqual(['08:29', '08:51']);
  if (number === 6) { expect(rows.find(row => row.start.slice(11, 16) === '09:10')).toMatchObject({ label: 'Deltskiftpause', end: '2030-01-07T15:00+01:00' }); expect(gaps).not.toContainEqual(['15:33', '16:00']); }
  if (number === 7) expect(rows.filter(row => row.label === 'Kaffepause').map(row => [row.start.slice(11, 16), row.end.slice(11, 16)])).toEqual([['11:40', '12:02'], ['14:13', '14:39']]);
  if (number === 8) { expect(gaps).toContainEqual(['14:56', '14:58']); expect(rows.at(-3)!.label).toBe('CAR'); }
  if (number === 9) expect(gaps).toEqual([]);
  expect(result.reporting.map(member => member.activity.start)).toEqual(activities.filter((row: any) => row.type === 'Sign-on').map((row: any) => row.start));
  const meal = rows.filter(row => row.label === 'Matpause');
  if ([2, 7, 8].includes(number)) {
    expect(meal).toHaveLength(1);
    expect([meal[0].start.slice(11, 16), meal[0].end.slice(11, 16), meal[0].members.length]).toEqual(number === 2 ? ['12:01', '12:43', 2] : number === 7 ? ['08:52', '09:28', 2] : ['09:38', '10:23', 2]);
  }
  if (number === 4) { expect(rows[3].end.slice(0, 16)).toBe('2030-01-06T00:35'); expect(rows[0].members[0].suffix).toBe('090'); }
  if (number === 5) { expect(rows.at(-1)!.end.slice(11, 16)).toBe('08:29'); expect(fixture.header.end).toBe('08:51'); expect(rows[0].members[0].suffix).toBe('006'); }
  if (number === 6) { expect(rows[12].members[0].activity).toMatchObject({ type: 'deadhead', raw_code: 'Travel to', from_place: 'Skoglyst', to_place: 'Breivika', trip: null }); expect(rows[12].end.slice(11, 16)).toBe('16:00'); }
  if (number === 8) { expect(rows.at(-2)!.members[0]).toMatchObject({ kind: 'deadhead_car', duty: 'CAR - 1', suffix: null }); expect(rows.at(-3)!.start).toBe(rows.at(-3)!.end); }
  if (number === 9) { expect(rows.filter(row => row.label === 'Kaffepause')).toHaveLength(3); expect(rows.at(-1)!.label).toBe('Instruktør'); expect(rows.every(row => row.members.every(member => member.duty === null && member.activity.from_place === null))).toBe(true); }
});

const account = { username: 'synthetic-day-' + randomUUID(), password: randomBytes(24).toString('hex') };
const API = 'http://127.0.0.1:8001';
function python(program: string) {
  if (process.env.COMPOSE_PROJECT_NAME !== 'ibe160-private-tests') throw Error('Disposable project required');
  return execFileSync('docker', ['compose', '-p', 'ibe160-private-tests', '-f', 'compose.private.yaml', 'exec', '-T', 'private-api', 'python', '-'], { cwd: '..', encoding: 'utf8', input: 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n' + program });
}
test.describe('synthetic day browser', () => {
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
  async function login(page: Page) {
    python("with database() as conn:\n conn.execute('DELETE FROM login_limits')\n");
    await page.goto('/private'); await page.getByLabel('Brukernavn', { exact: true }).fill(account.username); await page.getByLabel('Passord', { exact: true }).fill(account.password); await page.getByRole('button', { name: 'Logg inn', exact: true }).click();
    await expect(page.getByRole('heading', { name: 'Mine utkast' })).toBeVisible();
  }
  async function post(context: BrowserContext, path: string, data: object) {
    const proof = await (await context.request.get(API + '/auth/csrf')).json();
    const response = await context.request.post(API + path, { headers: { Origin: 'http://127.0.0.1:5173', 'X-CSRF-Token': proof.csrf_token }, data });
    expect(response.status()).toBe(200); expect(response.headers()['cache-control']).toBe('no-store'); return response.json();
  }
  async function prepare(page: Page, context: BrowserContext, reporting = true, customize?: (input: Content) => void) {
    await login(page);
    const imported = JSON.parse(python('import sys\nsys.path.insert(0,"/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nfrom app.pdf_import import parse_document\nfrom app.private_import import interpret\nprint(interpret(parse_document(synthetic_text_pdf())).model_dump_json())\n'));
    const a = activity(reporting ? 'Sign-on' : 'Fadder', '07:51', '07:54', { from_place: 'Fiktivt oppmøtested med et svært langt navn som må brytes uten klipping' });
    const b = activity('MealBreak', '12:01', '12:31', { uncertainty: 'Syntetisk usikkerhet beholdes' });
    const c = activity('Paid meal before', '12:31', '12:43');
    const d = activity('Sign-on', '12:43', '12:45');
    const e = activity('trip', '23:50', '23:59', { end: '2031-01-03T00:35+01:00', line: 'X43', trip: '1001', direction: 'Mot fiktivt sentrum', from_place: 'Fiktiv start', to_place: 'Fiktivt sluttsted' });
    const f = activity('CAR', '00:35', '00:35', { start: '2031-01-03T00:35+01:00', end: '2031-01-03T00:35+01:00', raw_code: 'CAR / 76566' });
    const input = content([a, b, c, ...(reporting ? [d] : []), e, f], { import_metadata: imported.import_metadata, vehicle_duty_changes: [{ from_activity_id: e.id, vehicle_duty: '960090', realtime_duty: '090' }, { from_activity_id: f.id, vehicle_duty: 'CAR - 1', realtime_duty: null }] });
    customize?.(input);
    // Save a real revision correction; stale original grouping/header remain historical.
    const draft = await post(context, '/drafts', { operation_id: (await post(context, '/draft-operations', {})).operation_id, expected_revision: 0, draft: input });
    const corrected = structuredClone(draft.draft); (corrected.activities.find((a: any) => a.type === 'trip') ?? corrected.activities[0]).to_place = 'Rettet fiktivt sluttsted';
    const saved = await post(context, '/drafts/' + draft.id, { operation_id: (await post(context, '/draft-operations', { draft_id: draft.id })).operation_id, expected_revision: draft.revision, draft: corrected });
    const review = await post(context, '/workday-reviews', { draft_id: saved.id, expected_revision: saved.revision });
    const plan = await post(context, '/drafts/' + saved.id + '/confirm', { operation_id: review.operation_id, expected_revision: saved.revision, acknowledgements: review.unknowns.map((item: any) => item.id), classifications: {} });
    await page.getByRole('button', { name: 'Oppdater planlisten', exact: true }).click();
    await page.getByRole('button', { name: `Åpne plan 2031-01-02 · versjon 2`, exact: true }).last().click();
    await expect(page.getByRole('region', { name: 'Dagsoversikt', exact: true })).toBeVisible();
    return { plan, saved };
  }
  for (const width of [768, 1024, 1440]) for (const night of [false, true]) test(`read corrected day ${width}px ${night ? 'Night' : 'Day'} with keyboard and enlarged text`, async ({ page, context }) => {
    await page.setViewportSize({ width, height: width === 1024 ? 768 : 1024 });
    const { plan, saved } = await prepare(page, context);
    if (night) await page.getByRole('button', { name: 'Nattmodus' }).click();
    const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
    await expect(day).toContainText('02.01.2031, 07:51'); await expect(day).toContainText('Senere oppmøte: 02.01.2031, 12:43');
    await expect(day).toContainText('12:01 – 02.01.2031, 12:43'); await expect(day).toContainText('Usikkerhet: Syntetisk usikkerhet beholdes');
    await expect(day).toContainText('03.01.2031, 00:35'); await expect(day).toContainText('Rettet fiktivt sluttsted');
    await expect(day).toContainText('Sanntidsverdi: 006'); await expect(day).toContainText('Sanntidsverdi: 090'); await expect(day).toContainText('Ikke utledet for CAR');
    const firstRow = day.locator('.day-activity').first();
    const list = day.getByRole('list', { name: 'Planlagte aktiviteter og tidsrom' });
    await expect(list).toBeVisible(); await expect(list.getByRole('listitem')).toHaveCount(7);
    await expect(firstRow.getByText('Oppmøte', { exact: true })).toHaveCount(1);
    await expect(firstRow).not.toContainText('Linje:'); await expect(firstRow).not.toContainText('Tur:'); await expect(firstRow).not.toContainText('Retning:');
    const summary = day.getByText('Vis 2 pauserader', { exact: true }); await summary.focus(); await page.keyboard.press('Enter');
    await expect(day.locator('[data-activity-id="' + saved.draft.activities[1].id + '"]')).toBeVisible();
    await expect(day.locator('[data-activity-id="' + saved.draft.activities[2].id + '"]')).toBeVisible();
    await expect(page.getByRole('region', { name: 'Fysisk buss', exact: true })).toHaveCount(1);
    expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
    expect(await (await context.request.get(API + '/drafts/' + saved.id)).json()).toEqual(saved);
    await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
    const confirmed = page.getByRole('region', { name: 'Bekreftet plan', exact: true });
    const bus = confirmed.getByRole('region', { name: 'Fysisk buss', exact: true });
    const controls = [bus, bus.getByLabel('Fysisk buss', { exact: true }), bus.getByRole('button', { name: 'Lagre fysisk buss', exact: true }), bus.getByRole('button', { name: 'Avbryt bussendring', exact: true }), confirmed.getByText('Bekreftede detaljer og historisk kilde', { exact: true }), confirmed.getByRole('button', { name: 'Lukk planen', exact: true }), confirmed.getByRole('button', { name: 'Slett bekreftet plan', exact: true })];
    for (const control of controls) {
      await control.scrollIntoViewIfNeeded(); await expect(control).toBeVisible();
      await control.evaluate(element => element.scrollIntoView({ block: 'center', inline: 'nearest' }));
      const bounds = await control.evaluate(element => { const r = element.getBoundingClientRect(); return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, height: r.height, viewportHeight: innerHeight, visible: r.left >= 0 && r.right <= innerWidth && r.width > 0 && (r.height > innerHeight || r.top >= -1 && r.bottom <= innerHeight + 1) }; });
      expect(bounds).toMatchObject({ visible: true });
    }
    const historical = confirmed.getByText('Bekreftede detaljer og historisk kilde', { exact: true });
    await historical.click(); await expect(confirmed.getByText('Fysisk buss ved bekreftelse (historisk)', { exact: true })).toBeVisible();
    const source = confirmed.getByText('Bevarte kildefakta', { exact: true }); await source.scrollIntoViewIfNeeded(); await expect(source).toBeVisible();
    await source.click(); await expect(confirmed.getByRole('heading', { name: 'Historiske kildefakta fra PDF · før rettelser og bekreftelse', exact: true })).toBeVisible(); await source.click(); await historical.click();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await day.screenshot({ path: `../docs/evidence/10-5-day-${width}-${night ? 'night' : 'day'}-200.png` });
    await confirmed.screenshot({ path: `../docs/evidence/10-5-full-plan-${width}-${night ? 'night' : 'day'}-200.png` });
    await page.getByRole('button', { name: 'Lukk planen', exact: true }).click();
    await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 2', exact: true }).last().click();
    await expect(day).toContainText('Rettet fiktivt sluttsted');
    expect(await page.evaluate(async () => ({ local: Object.keys(localStorage), session: Object.keys(sessionStorage), databases: (await indexedDB.databases()).map(d => d.name) }))).toEqual({ local: [], session: [], databases: [] });
  });
  test('missing reporting stays unknown with source header separately labelled', async ({ page, context }) => {
    await prepare(page, context, false);
    const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
    await expect(day).toContainText('Ukjent · ingen bekreftet Sign-on'); await expect(day).toContainText('Kildeinformasjon · start i overskriften');
    await expect(day).toContainText('Fadder'); await expect(day).toContainText('Planlagt siste aktivitetsslutt: 03.01.2031, 00:35');
  });
  test('grouped pause visibly retains timed return duty boundaries A to B to A', async ({ page, context }) => {
    await prepare(page, context, false, input => {
      const rows = [activity('MealBreak', '08:00', '08:10'), activity('Paid meal before', '08:10', '08:20'), activity('Paid meal after', '08:20', '08:30')];
      input.activities = rows;
      input.vehicle_duty_changes = [{ from_activity_id: rows[1].id, vehicle_duty: '960090', realtime_duty: '090' }, { from_activity_id: rows[2].id, vehicle_duty: '960006', realtime_duty: '006' }];
    });
    const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
    await expect(day.getByText(/3 sammenhengende pauserader/)).toHaveText('3 sammenhengende pauserader. Vognløp: 02.01.2031, 08:00: 960006 (sanntidsverdi 006) → 02.01.2031, 08:10: 960090 (sanntidsverdi 090) → 02.01.2031, 08:20: 960006 (sanntidsverdi 006). Hver del vises i detaljene.');
    expect(await day.locator('details').first().evaluate(element => (element as HTMLDetailsElement).open)).toBe(false);
  });
  for (const note of ['', 'Concrete manual note.']) test(`feedback generated markers stay neutral with note ${JSON.stringify(note)}`, async ({ page, context }) => {
    const { saved } = await prepare(page, context, true, input => {
      const source = input.import_metadata!.activities[0];
      const target = input.activities.find(activity => activity.type === 'trip')!;
      source.activity_id = target.id;
      const point = source.provenance.label[0];
      input.import_metadata!.annotations = [{ value: 't', meaning: null, provenance: point }];
      target.raw_code = 'Trip';
      target.uncertainty = `Kildemerket t har ukjent betydning (side ${point.page}). ${note}`;
    });
    const target = saved.draft.activities.find((activity: any) => activity.type === 'trip');
    const member = page.getByRole('region', { name: 'Dagsoversikt', exact: true }).locator(`[data-activity-id="${target.id}"]`);
    await expect(member).toContainText('Kildemerke: t');
    await expect(member).toContainText('Kode: tur');
    await expect(member.locator('.day-uncertainty')).toHaveCount(note ? 1 : 0);
    if (note) await expect(member.locator('.day-uncertainty')).toHaveText('Usikkerhet: ' + note);
    await member.getByText('Kilde og rettelser', { exact: false }).click();
    await expect(member).not.toContainText('Trip');
    const persisted = await (await context.request.get(API + '/drafts/' + saved.id)).json();
    expect(persisted.draft.activities.find((activity: any) => activity.id === target.id).uncertainty).toBe(target.uncertainty);
  });

  for (const remainder of ['', 'Concrete manual note.', 'Kildemerket other har ukjent betydning (side 1).']) test(`feedback unknown marker position stays neutral and unassociated with ${JSON.stringify(remainder)}`, async ({ page, context }) => {
    const { saved } = await prepare(page, context, true, input => {
      input.import_metadata!.annotations = [{ value: 't', meaning: null, provenance: { page: 1, column: null, line: null } }];
      input.activities.find(activity => activity.type === 'trip')!.uncertainty = 'Kildemerket t har ukjent betydning (side 1). ' + remainder;
    });
    const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
    await expect(day.getByText('Kildemerke: t (side 1).', { exact: true })).toBeVisible();
    await expect(day.locator('[data-activity-id]').filter({ hasText: 'Kildemerke: t' })).toHaveCount(0);
    const target = saved.draft.activities.find((activity: any) => activity.type === 'trip');
    const member = day.locator(`[data-activity-id="${target.id}"]`);
    await expect(member.locator('.day-uncertainty')).toHaveCount(remainder ? 1 : 0);
    if (remainder) await expect(member.locator('.day-uncertainty')).toHaveText('Usikkerhet: ' + remainder);
    const persisted = await (await context.request.get(API + '/drafts/' + saved.id)).json();
    expect(persisted.draft.activities.find((activity: any) => activity.id === target.id).uncertainty).toBe(target.uncertainty);
  });

  test('original source issues remain visible on matched rows and globally without overriding corrections', async ({ page, context }) => {
    const { saved } = await prepare(page, context, true, input => {
      const metadata = input.import_metadata!;
      const source = metadata.activities[0]; source.activity_id = input.activities[1].id;
      const point = source.provenance.label[0];
      metadata.unresolved = [{ code: 'missing_endpoint', activity: source.source_order, field: 'origin', provenance: point }, { code: 'unrecognized_source_line', activity: null, field: null, provenance: null }];
      metadata.annotations = [{ value: 'synthetic-marker', meaning: null, provenance: point }];
    });
    const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
    const pause = day.locator(`[data-day-row="${saved.draft.activities[1].id}"]`);
    await expect(pause).toContainText('Opprinnelig kildeusikkerhet (før rettelser og bekreftelse): Endested mangler');
    await expect(pause).toContainText('Kildemerke: synthetic-marker');
    await expect(pause).toContainText('Bekreftede fakta i oversikten gjelder.');
    await expect(pause.getByRole('heading', { name: 'Matpause', exact: true })).toBeVisible();
    await expect(day.getByText(/Opprinnelig kildeusikkerhet.*En kilderad kunne ikke tolkes/)).toBeVisible();
    await expect(day).toContainText('Rettet fiktivt sluttsted');
    await expect(day.locator('.day-source-information').filter({ hasText: 'Endested mangler' })).toBeVisible();
    await expect(day.locator('.day-uncertainty').filter({ hasText: 'Opprinnelig kildeusikkerhet' })).toHaveCount(0);
    await expect(pause.locator('.day-uncertainty').filter({ hasText: 'Syntetisk usikkerhet beholdes' }).first()).toBeVisible();
    expect(await pause.locator('details').first().evaluate(element => (element as HTMLDetailsElement).open)).toBe(false);
  });

  for (const kind of ['deadhead', 'deadhead_car', 'Tomkjøring med CAR', 'CAR']) test(`review fixes movement ${kind} missing trip remains a neutral visible fact`, async ({ page, context }) => {
    const { saved } = await prepare(page, context, false, input => {
      input.activities = [activity(kind, '08:00', '08:10', { trip: null, from_place: 'Origin', to_place: 'Destination' })];
      input.vehicle_duty_changes = [];
    });
    const member = page.getByRole('region', { name: 'Dagsoversikt', exact: true }).locator(`[data-activity-id="${saved.draft.activities[0].id}"]`);
    await expect(member.getByText('Tur: Ukjent', { exact: true })).toBeVisible();
    await expect(member.locator('.day-uncertainty')).toHaveCount(0);
    await expect(member.getByRole('checkbox')).toHaveCount(0);
  });
  test('invalid historical source start falls back to raw source clock after real save confirm and reopen', async ({ page, context }) => {
    const { saved, plan } = await prepare(page, context, false, input => { input.import_metadata!.header.start_instant = 'not-an-instant'; });
    const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
    for (const reopened of [false, true]) {
      if (reopened) { await page.getByRole('button', { name: 'Lukk planen', exact: true }).click(); await page.getByRole('button', { name: 'Åpne plan 2031-01-02 · versjon 2', exact: true }).click(); }
      await expect(day).toContainText(`Kildeinformasjon · start i overskriften: ${saved.draft.import_metadata.header.start}. Dette er ikke et bekreftet oppmøte.`);
      await expect(day).toContainText('Ukjent · ingen bekreftet Sign-on'); await expect(day).toContainText('Planlagt siste aktivitetsslutt: 03.01.2031, 00:35');
    }
    expect(await (await context.request.get(API + '/workdays/' + plan.id)).json()).toEqual(plan);
  });
  test('rendered day text, boundaries and keyboard focus meet contrast requirements in both themes', async ({ page, context }) => {
    await prepare(page, context);
    const day = page.getByRole('region', { name: 'Dagsoversikt', exact: true });
    for (const night of [false, true]) {
      if (night) await page.getByRole('button', { name: 'Nattmodus' }).click();
      const summary = day.getByText('Vis 2 pauserader', { exact: true });
      await page.keyboard.press('Tab');
      await summary.focus();
      const measured = await day.evaluate(element => {
        const rgb = (value: string) => (value.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number);
        const luminance = (value: string) => rgb(value).map(c => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }).reduce((sum, c, i) => sum + c * [.2126, .7152, .0722][i], 0);
        const ratio = (a: string, b: string) => (Math.max(luminance(a), luminance(b)) + .05) / (Math.min(luminance(a), luminance(b)) + .05);
        const style = getComputedStyle(element);
        const reporting = getComputedStyle(element.querySelector('.day-reporting')!);
        const warning = getComputedStyle(element.querySelector('.day-uncertainty')!);
        const row = getComputedStyle(element.querySelector('.day-activity')!);
        const focus = getComputedStyle(document.activeElement!);
        return { text: ratio(style.color, style.backgroundColor), reporting: ratio(reporting.color, reporting.backgroundColor), warning: ratio(warning.color, warning.backgroundColor), boundary: ratio(row.borderColor, style.backgroundColor), reportingBoundary: ratio(reporting.borderLeftColor, reporting.backgroundColor), focus: ratio(focus.outlineColor, style.backgroundColor), focusWidth: parseFloat(focus.outlineWidth) };
      });
      expect(measured.text).toBeGreaterThanOrEqual(4.5); expect(measured.reporting).toBeGreaterThanOrEqual(4.5); expect(measured.warning).toBeGreaterThanOrEqual(4.5);
      expect(measured.boundary).toBeGreaterThanOrEqual(3); expect(measured.reportingBoundary).toBeGreaterThanOrEqual(3); expect(measured.focus).toBeGreaterThanOrEqual(3); expect(measured.focusWidth).toBeGreaterThanOrEqual(2);
      await test.info().attach(`day-overview-contrast-${night ? 'night' : 'day'}`, { body: JSON.stringify(measured), contentType: 'application/json' });
      await page.keyboard.press('Enter');
      await expect(summary).toBeFocused();
      await day.screenshot({ path: `../docs/evidence/10-5-day-contrast-${night ? 'night' : 'day'}.png` });
      await page.keyboard.press('Enter');
    }
  });
});
