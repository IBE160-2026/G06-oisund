import { test, expect, openedPlan, API, python, setup, activityScreen, dayScreen, post, randomUUID } from './private-activity-helpers';

setup();

function controlledSource(mode: 'seed' | 'update' | 'clear', pilot = false) {
  return python(`import os
from uuid import uuid4
from app.automatic_notice_source import MAX_ID,SITUATION_PREFIX
mode=${JSON.stringify(mode)}
pilot=${pilot ? 'True' : 'False'}
name='ø'+chr(10)+'🚌'*(MAX_ID-len(SITUATION_PREFIX)-2)
if os.getenv('PRIVATE_TEST_ORIGIN') != 'http://127.0.0.1:19651' or os.getenv('V2_NOTICE_REFRESH') != 'off':
 raise RuntimeError('Only the isolated V2 test sandbox may run this controlled example')
with database() as conn:
 require_synthetic_accounts(conn)
 conn.execute('SELECT id FROM automatic_notice_feed FOR UPDATE')
 if mode == 'clear':
  conn.execute('DELETE FROM automatic_notice_sources WHERE situation=%s',(SITUATION_PREFIX+name,))
  conn.execute('DELETE FROM automatic_notice_identities WHERE situation=%s',(SITUATION_PREFIX+name,))
  conn.execute('DELETE FROM automatic_notice_feed')
  conn.execute('INSERT INTO automatic_notice_feed DEFAULT VALUES')
 else:
  if mode == 'seed':
   assert not conn.execute("SELECT 1 FROM automatic_notice_feed WHERE status!='never-qualified'").fetchone()
  import sys
  sys.path.insert(0,'tests')
  from test_automatic_notice_rules import STOP,page,situation
  from app.automatic_notice_ingestion import finish
  version,title=('1','Syntetisk stoppmelding &lt;script&gt;') if mode=='seed' else ('2','Oppdatert stoppmelding')
  window=('2026-11-23T16:00+01:00' if pilot else '2026-11-23T22:00+01:00',None)
  observed=page(situation(name,STOP,windows=(window,),version=version,text='<Summary>'+title+'</Summary>'))
  fetched=conn.execute("UPDATE automatic_notice_feed SET attempt_at=clock_timestamp(),status='collecting' RETURNING attempt_at").fetchone()['attempt_at']
  conn.commit()
  finish(conn,uuid4(),[observed.response_at],[(observed.items[0],fetched,observed.response_at)],None)
`);
}

test('normal private view preserves activity and manual input and recovers a lost review reply', async ({ page, context }) => {
  controlledSource('seed');
  try {
    const { plan } = await openedPlan(page, context);
    await page.getByRole('button', { name: 'Velg aktivitet 1', exact: true }).click();
    await activityScreen(page);
    await dayScreen(page);
    await page.getByRole('button', { name: 'Manuelt vedlikeholdte avvik', exact: true }).click();
    await page.getByRole('button', { name: 'Registrer avvik', exact: true }).click();
    await page.getByLabel('Tittel', { exact: true }).fill('Ulagret manuelt forslag');
    const entry = page.getByRole('button', { name: 'Automatiske avvik', exact: true });
    await entry.click();
    const area = page.getByRole('region', { name: 'Automatiske avvik', exact: true });
    await expect(area.getByRole('heading', { name: 'Automatiske avvik', exact: true })).toBeFocused();
    await expect(area).toContainText('Kontrollerte testdata');
    await expect(area).toContainText('Komplett innsamling for TRO');
    await area.getByRole('button', { name: 'Syntetisk stoppmelding <script>', exact: true }).click();
    await expect(area.getByRole('heading', { name: 'Avvik fra Entur', exact: true })).toBeVisible();
    await expect(area.getByLabel('Valg', { exact: true })).toHaveCount(0);
    await area.getByRole('button', { name: 'Gjennomgå kildegrunnlaget (valgfritt)', exact: true }).click();
    await expect(area).toContainText('Koblingen til planens stopp er uavklart.');
    await expect(area.locator('script')).toHaveCount(0);
    await area.getByLabel('Valg', { exact: true }).selectOption('day-context');
    const savePath = '**/automatic-notices/review';
    await page.route(savePath, async route => {
      await route.fetch();
      await route.abort();
    });
    await area.getByRole('button', { name: 'Lagre gjennomgang', exact: true }).click();
    await expect(area).toContainText('Lagringen er uavklart.');
    await page.unroute(savePath);
    await area.getByRole('button', { name: 'Kontroller lagringsforsøk', exact: true }).click();
    await expect(area).toContainText('Privat valg · Beholdt som dagskontekst');
    const original = await (await context.request.get(`${API}/workdays/${plan.id}/selection`)).json();
    expect(original.activity_id).toBe(plan.draft.activities[0].id);
    await area.getByRole('button', { name: 'Tilbake til planen', exact: true }).click();
    await expect(page.getByRole('heading', { name: 'Rediger avvik', exact: true })).toBeFocused();
    await expect(page.getByLabel('Tittel', { exact: true })).toHaveValue('Ulagret manuelt forslag');
    await page.getByRole('region', { name: 'Avviksvedlikehold', exact: true }).getByRole('button', { name: 'Tilbake til dagen', exact: true }).click();
    await entry.click();
    await area.getByRole('button', { name: 'Tilbake til planen', exact: true }).click();
    await expect(entry).toBeFocused();
  } finally {
    controlledSource('clear');
  }
});

test('a dated pilot stop has its own review group without a suggested activity', async ({ page, context }) => {
  controlledSource('seed', true);
  try {
    const { plan } = await openedPlan(page, context, true, 24 * 60 * 60, undefined, false, content => {
      content.activities[0].line = '24';
    });
    // Keep the authorized workday current while testing the historical pilot dates.
    python(`from psycopg.types.json import Jsonb
with database() as conn:
 require_synthetic_accounts(conn)
 key=${JSON.stringify(plan.id)}
 facts=conn.execute('SELECT content FROM workdays WHERE id=%s',(key,)).fetchone()['content']
 facts['service_date']='2026-11-23'
 facts['activities'][0].update(start='2026-11-23T16:10+01:00',end='2026-11-23T16:20+01:00')
 conn.execute('UPDATE workdays SET content=%s WHERE id=%s',(Jsonb(facts),key))`);
    await page.getByRole('button', { name: 'Automatiske avvik', exact: true }).click();
    const group = page.getByRole('region', { name: 'Pilotstopp til gjennomgang', exact: true });
    await expect(group.getByRole('heading')).toHaveText('Pilotstopp til gjennomgang');
    await expect(group).toContainText('Vurder om meldingen gjelder avgangen din.');
    await group.getByRole('button', { name: 'Syntetisk stoppmelding <script>', exact: true }).click();
    await page.getByRole('button', { name: 'Gjennomgå kildegrunnlaget (valgfritt)', exact: true }).click();
    await expect(page.getByRole('list', { name: 'Mulig relevante planaktiviteter' })).toHaveCount(0);
    await expect(page.getByLabel('Valg', { exact: true })).toHaveValue('unresolved');
    await page.getByLabel('Valg', { exact: true }).selectOption('day-context');
    await page.getByRole('button', { name: 'Lagre gjennomgang', exact: true }).click();
    await expect(group).toContainText('Privat valg · Beholdt som dagskontekst');
    const selection = await (await context.request.get(`${API}/workdays/${plan.id}/selection`)).json();
    expect(selection.activity_id).toBeNull();
  } finally {
    controlledSource('clear');
  }
});

test('source, concurrent review and workday boundary changes require explicit comparison before saving', async ({ page, context }) => {
  controlledSource('seed');
  try {
    const { plan } = await openedPlan(page, context);
    const path = `/workdays/${plan.id}/automatic-notices`;
    const projection = async () => (await context.request.get(API + path)).json();
    await page.getByRole('button', { name: 'Automatiske avvik', exact: true }).click();
    const view = page.getByRole('region', { name: 'Automatiske avvik', exact: true });
    await view.getByRole('button', { name: 'Syntetisk stoppmelding <script>', exact: true }).click();
    await view.getByRole('button', { name: 'Gjennomgå kildegrunnlaget (valgfritt)', exact: true }).click();
    const save = view.getByRole('button', { name: 'Lagre gjennomgang', exact: true });
    const compare = view.getByRole('button', { name: 'Sammenlignet. Behold forslaget', exact: true });
    const refresh = view.getByRole('button', { name: 'Hent status', exact: true });
    const choices = view.getByLabel('Valg', { exact: true });
    const reason = view.getByLabel('Grunn til å legge bort', { exact: true });
    await choices.selectOption('dismiss');
    await reason.fill('Mitt valg på vist grunnlag');
    await expect(save).toBeEnabled();
    controlledSource('update');
    await refresh.click();
    await expect(view.getByRole('button', { name: 'Oppdatert stoppmelding', exact: true })).toBeVisible();
    await expect(save).toBeDisabled();
    await expect(reason).toHaveValue('Mitt valg på vist grunnlag');
    await view.getByText('Kildeopplysninger da forslaget ble startet', { exact: true }).click();
    await expect(view.locator('details[open]')).toContainText('Syntetisk stoppmelding <script>');
    expect((await projection()).entries[0].decision).toBeNull();
    await compare.click();
    await save.click();
    await expect(view.getByRole('status')).toHaveText('Gjennomgangen er lagret.');
    let active = await projection();
    expect(active.entries[0].decision).toMatchObject({ action: 'dismiss', reason: 'Mitt valg på vist grunnlag', source_basis: active.entries[0].source.basis });

    await view.getByRole('button', { name: 'Gjennomgå kildegrunnlaget (valgfritt)', exact: true }).click();
    await choices.selectOption('day-context');
    const entry = active.entries[0];
    await post(context, path + '/review', { operation_id: randomUUID(), situation: entry.situation, expected_revision: entry.review_revision,
      expected_plan_revision: active.plan_revision, expected_lifecycle_revision: active.lifecycle.revision, expected_source_basis: entry.source.basis,
      action: 'unresolved' });
    await refresh.click();
    await expect(compare).toBeEnabled();
    await expect(save).toBeDisabled();
    await expect(choices).toHaveValue('day-context');
    await compare.click();
    await expect(save).toBeEnabled();

    await post(context, `/workdays/${plan.id}/start`, { operation_id: randomUUID(), expected_revision: 0 });
    await refresh.click();
    await expect(compare).toBeEnabled();
    await expect(save).toBeDisabled();
    await compare.click();
    await save.click();
    await expect(view.getByRole('status')).toHaveText('Gjennomgangen er lagret.');
    active = await projection();
    expect(active.entries[0]).toMatchObject({ review_revision: 3, decision: { action: 'day-context' } });
  } finally {
    controlledSource('clear');
  }
});

test('a delayed acknowledgement after leaving and reopening keeps the original retry body', async ({ page, context }) => {
  controlledSource('seed');
  let release = () => {};
  try {
    await openedPlan(page, context);
    const entry = page.getByRole('button', { name: 'Automatiske avvik', exact: true });
    await entry.click();
    const view = page.getByRole('region', { name: 'Automatiske avvik', exact: true });
    await view.getByRole('button', { name: 'Syntetisk stoppmelding <script>', exact: true }).click();
    await view.getByRole('button', { name: 'Gjennomgå kildegrunnlaget (valgfritt)', exact: true }).click();
    await view.getByLabel('Valg', { exact: true }).selectOption('day-context');
    const gate = new Promise<void>(resolve => { release = resolve; });
    const savePath = '**/automatic-notices/review';
    let original: string | null = null;
    let committed = false;
    await page.route(savePath, async route => {
      original = route.request().postData();
      const response = await route.fetch();
      committed = response.ok();
      await gate;
      await route.fulfill({ response });
    });
    await view.getByRole('button', { name: 'Lagre gjennomgang', exact: true }).click();
    await expect.poll(() => committed).toBe(true);
    await view.getByRole('button', { name: 'Tilbake til planen', exact: true }).click();
    await entry.click();
    const retry = view.getByRole('button', { name: 'Send opprinnelig forslag på nytt', exact: true });
    await expect(retry).toBeDisabled();
    // The reopened session read waits for the already submitted writer's Web Lock.
    release();
    await expect(view).toContainText('Privat valg · Beholdt som dagskontekst');
    await expect(retry).toBeEnabled();
    await expect(view.getByRole('status')).not.toContainText('Gjennomgangen er lagret.');
    await page.unroute(savePath);
    let resent: string | null = null;
    await page.route(savePath, async route => { resent = route.request().postData(); await route.continue(); });
    await retry.click();
    await expect(view.getByRole('status')).toHaveText('Gjennomgangen er lagret.');
    expect(resent).toBe(original);
  } finally {
    release();
    controlledSource('clear');
  }
});
