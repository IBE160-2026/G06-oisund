"""PM-E1-S3 real PostgreSQL/API, synthetic-only and secret-safe assertions."""
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from time import monotonic
from types import SimpleNamespace
import re

import httpx
import pytest
from fastapi import HTTPException
from app import auth, password_recovery as recovery
from app.private_storage import database
from test_private_access import users, client, synthetic_only, headers, login, URL, pytestmark
from test_password_change import gates, request_for

NEW = 'synthetic-recovery-new-password'
def anonymous():
    return SimpleNamespace(cookies={}, client=SimpleNamespace(host='synthetic-recovery'))
def issued(users):
    return recovery.issue(recovery.resolve(users[0][0]))
def redeem(users, code, request=None):
    return recovery.redeem(request or anonymous(), users[0][0], code, NEW, NEW)
def post(client, users, candidate, **overrides):
    body = dict(username=users[0][0], code=candidate, new_password=NEW, confirmation=NEW)
    body.update(overrides)
    return client.post('/auth/password/recover', headers=headers(client), json=body)
def outcome(function):
    try:
        function()
        return 200
    except HTTPException as error:
        return error.status_code

def test_full_recovery_preserves_data_sessions_receipts(client, users):
    from test_private_drafts import save
    from test_private_workdays import prepare, confirm
    from test_account_notices import send, command, content
    verified = login(client, users).status_code == 200
    assert verified, 'Synthetic recovery invariant failed'
    saved, body = save(client)
    record = saved.json()
    draft, _, decisions = prepare(client)
    plan = confirm(client, draft, decisions).json()
    notice_body = command(content=content())
    notice = send(client, notice_body).json()
    with httpx.Client(base_url=URL) as second, httpx.Client(base_url=URL) as other, httpx.Client(base_url=URL) as fresh:
        verified = login(second, users).status_code == 200
        assert verified, 'Synthetic recovery invariant failed'
        verified = login(other, users, 1).status_code == 200
        assert verified, 'Synthetic recovery invariant failed'
        code, proof = issued(users)
        response = post(fresh, users, code, username=' '+users[0][0].upper()+' ')
        verified = response.status_code == 200 and response.json() == {'changed': True}
        assert verified, 'Synthetic recovery invariant failed'
        verified = response.headers['cache-control'] == 'no-store'
        assert verified, 'Synthetic recovery invariant failed'
        verified = fresh.get('/auth/session').status_code == 401
        assert verified, 'Synthetic recovery invariant failed'
        for path in ['/auth/session', '/drafts', '/workdays', '/notices']:
            verified = client.get(path).status_code == second.get(path).status_code == 401
            assert verified, 'Synthetic recovery invariant failed'
        verified = other.get('/auth/session').status_code == 200
        assert verified, 'Synthetic recovery invariant failed'
        verified = login(fresh, users).status_code == 401
        assert verified, 'Synthetic recovery invariant failed'
        response = fresh.post('/auth/login', headers=headers(fresh), json={'username':users[0][0], 'password':NEW})
        verified = response.json()['account_id'] == str(users[1][0])
        assert verified, 'Synthetic recovery invariant failed'
        verified = fresh.get('/drafts/'+record['id']).json() == record
        assert verified, 'Synthetic recovery invariant failed'
        verified = fresh.get('/draft-operations/'+body['operation_id']).status_code == 200
        assert verified, 'Synthetic recovery invariant failed'
        verified = fresh.get('/workdays/'+plan['id']).json() == plan
        assert verified, 'Synthetic recovery invariant failed'
        verified = fresh.get('/workday-operations/'+decisions['operation_id']).json()['result'] == plan
        assert verified, 'Synthetic recovery invariant failed'
        verified = fresh.get('/notices/'+notice['result']['id']).json() == notice['result']
        assert verified, 'Synthetic recovery invariant failed'
        verified = fresh.get('/workday-notice-operations/'+notice_body['operation_id']).json() == notice
        assert verified, 'Synthetic recovery invariant failed'
        with database() as conn:
            verified = conn.execute('SELECT state FROM recovery_proofs WHERE id=%s', (proof['id'],)).fetchone()['state'] == 'consumed'
            assert verified, 'Synthetic recovery invariant failed'
            audit_row = conn.execute("SELECT owner,action,result,actor FROM recovery_audit WHERE action='change' AND owner=%s", (users[1][0],)).fetchall()
            verified = audit_row == [dict(owner=users[1][0], action='change', result='revoked', actor='recovery-proof:'+str(proof['id']))]
            assert verified, 'Successful recovery audit metadata mismatch'
            safe = code not in str(conn.execute('SELECT * FROM recovery_proofs').fetchall()) and code not in str(conn.execute('SELECT * FROM recovery_audit').fetchall())
            verified = safe
            assert verified, 'Plaintext recovery code persisted'

@pytest.mark.parametrize('state', ['malformed','wrong','unknown','control-name','wrong-account','expired','replaced','revoked','used'])
def test_generic_invalid_states_no_mutation(client, users, state):
    code, proof = issued(users)
    name = users[0][0]
    if state == 'malformed': code = 'invalid'
    if state == 'wrong': code = ('A' if code[0] != 'A' else 'B') + code[1:]
    if state == 'unknown': name = 'synthetic-unknown'
    if state == 'control-name': name = 'synthetic-\x00unknown'
    if state == 'wrong-account': name = users[0][1]
    if state == 'expired':
        with database() as conn:
            conn.execute("UPDATE recovery_proofs SET created_at=statement_timestamp()-interval '30 minutes',expires_at=statement_timestamp() WHERE id=%s", (proof['id'],))
    if state == 'replaced': issued(users)
    if state == 'revoked': recovery.revoke(recovery.resolve(name))
    if state == 'used': redeem(users, code)
    with database() as conn:
        before = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall(), conn.execute('SELECT * FROM sessions ORDER BY token_hash').fetchall(), conn.execute('SELECT * FROM recovery_proofs ORDER BY id').fetchall(), conn.execute('SELECT * FROM recovery_audit ORDER BY id').fetchall()
    result = post(client, users, code, username=name)
    verified = result.status_code == 400 and result.json() == {'detail': recovery.INVALID_CODE}
    assert verified, 'Synthetic recovery invariant failed'
    safe = code not in result.text and NEW not in result.text
    verified = safe
    assert verified, 'Secret in rejection'
    with database() as conn:
        after = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall(), conn.execute('SELECT * FROM sessions ORDER BY token_hash').fetchall(), conn.execute('SELECT * FROM recovery_proofs ORDER BY id').fetchall(), conn.execute('SELECT * FROM recovery_audit ORDER BY id').fetchall()
        verified = after == before
        assert verified, 'Synthetic recovery invariant failed'
        verified = conn.execute("SELECT attempts FROM login_limits WHERE bucket=%s", ('recover:user:'+auth.digest(name),)).fetchone()['attempts'] >= 1
        assert verified, 'Synthetic recovery invariant failed'

def test_boundaries_and_live_other_session(client, users):
    code, _ = issued(users)
    verified = login(client, users, 1).status_code == 200
    assert verified, 'Synthetic recovery invariant failed'
    before = client.get('/auth/session').json()
    verified = post(client, users, code).status_code == 409
    assert verified, 'Synthetic recovery invariant failed'
    verified = client.get('/auth/session').json() == before
    assert verified, 'Synthetic recovery invariant failed'
    client.post('/auth/logout', headers=headers(client))
    for overrides in [dict(extra='forbidden'),dict(new_password='short'),dict(confirmation='mismatch-password'),dict(code=12)]:
        result = post(client, users, code, **overrides)
        verified = result.status_code == 422
        assert verified, 'Synthetic recovery invariant failed'
        safe = code not in result.text and NEW not in result.text
        verified = safe
        assert verified, 'Secret in validation'
    for proof in [{}, {'Origin':'https://foreign.invalid'}, {'Origin':__import__('os').environ['PRIVATE_TEST_ORIGIN'],'X-CSRF-Token':'forged'}]:
        verified = client.post('/auth/password/recover', headers=proof, json={}).status_code == 403
        assert verified, 'Synthetic recovery invariant failed'
    verified = client.post('/auth/password/recover', headers=headers(client), content=b'x'*4097).status_code == 413
    assert verified, 'Synthetic recovery invariant failed'
    verified = client.get('/drafts').status_code == 401
    assert verified, 'Synthetic recovery invariant failed'
    verified = post(client, users, code).status_code == 200
    assert verified, 'Synthetic recovery invariant failed'

def test_expired_cookie_has_no_authority(client, users):
    verified = login(client, users, 1).status_code == 200
    assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '15 days',expires_at=statement_timestamp()-interval '1 day'")
    code, _ = issued(users)
    verified = post(client, users, code).status_code == 200
    assert verified, 'Synthetic recovery invariant failed'
    verified = client.get('/auth/session').status_code == 401
    assert verified, 'Synthetic recovery invariant failed'

def test_expiry_while_hashing(users, monkeypatch):
    code, proof = issued(users)
    with database() as conn:
        conn.execute("UPDATE recovery_proofs SET expires_at=clock_timestamp()+interval '0.1 second' WHERE id=%s", (proof['id'],))
    original = auth.password_hash
    def hash_then_expire(password, salt=None):
        value = original(password, salt)
        with database() as conn:
            conn.execute('SELECT pg_sleep(0.2)')
        return value
    monkeypatch.setattr(auth, 'password_hash', hash_then_expire)
    verified = outcome(lambda: redeem(users, code)) == 400
    assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        verified = conn.execute('SELECT state FROM recovery_proofs WHERE id=%s', (proof['id'],)).fetchone()['state'] == 'active'
        assert verified, 'Synthetic recovery invariant failed'

@pytest.mark.parametrize('competitor',['redeem','issue','revoke','change','login'])
def test_true_database_contention(users, monkeypatch, gates, competitor):
    code, _ = issued(users)
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-before')
    entered, release = Event(), Event()
    original = auth.password_hash
    def hold(password, salt=None):
        if password == NEW and not entered.is_set():
            entered.set()
            verified = release.wait(10)
            assert verified, 'Gate release timeout'
        return original(password, salt)
    monkeypatch.setattr(auth, 'password_hash', hold)
    actions = {'redeem':lambda:redeem(users,code), 'issue':lambda:issued(users), 'revoke':lambda:recovery.revoke(recovery.resolve(users[0][0])), 'change':lambda:auth.change_password(request_for(token),users[2],NEW,NEW), 'login':lambda:auth.authenticate(users[0][0],users[2],'synthetic-after')}
    with ThreadPoolExecutor(max_workers=2) as pool:
        winner = pool.submit(gates.run, 'winner', lambda:outcome(lambda:redeem(users,code)))
        verified = entered.wait(5)
        assert verified, 'Synthetic recovery invariant failed'
        loser = pool.submit(gates.run, 'competitor', lambda:outcome(actions[competitor]))
        try: gates.blocked('competitor','winner')
        finally: release.set()
        verified = winner.result() == 200
        assert verified, 'Synthetic recovery invariant failed'
        verified = loser.result() == {'redeem':400,'issue':200,'revoke':200,'change':401,'login':401}[competitor]
        assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        verified = not conn.execute('SELECT 1 FROM sessions WHERE owner=%s',(users[1][0],)).fetchone()
        assert verified, 'Synthetic recovery invariant failed'

def test_rollback_after_partial_replacement(users,monkeypatch):
    code, proof = issued(users)
    for i in range(2): auth.authenticate(users[0][0],users[2],str(i))
    with database() as conn:
        before=conn.execute('SELECT * FROM accounts ORDER BY id').fetchall(),conn.execute('SELECT * FROM sessions ORDER BY token_hash').fetchall(), conn.execute('SELECT * FROM recovery_proofs ORDER BY id').fetchall(), conn.execute('SELECT * FROM recovery_audit ORDER BY id').fetchall()
    original=auth.replace_password
    def fail(conn,owner,replacement,actor):
        original(conn,owner,replacement,actor)
        conn.execute('SELECT missing_synthetic_recovery_column')
    monkeypatch.setattr(auth,'replace_password',fail)
    with pytest.raises(Exception): redeem(users,code)
    with database() as conn:
        verified = (conn.execute('SELECT * FROM accounts ORDER BY id').fetchall(),conn.execute('SELECT * FROM sessions ORDER BY token_hash').fetchall(), conn.execute('SELECT * FROM recovery_proofs ORDER BY id').fetchall(), conn.execute('SELECT * FROM recovery_audit ORDER BY id').fetchall()) == before
        assert verified, 'Synthetic recovery invariant failed'
        verified = conn.execute('SELECT state FROM recovery_proofs WHERE id=%s',(proof['id'],)).fetchone()['state']=='active'
        assert verified, 'Synthetic recovery invariant failed'
        verified = conn.execute("SELECT attempts FROM login_limits WHERE bucket LIKE 'recover:user:%%'").fetchone()['attempts']==1
        assert verified, 'Synthetic recovery invariant failed'

def test_persistent_parallel_budget_and_expiry(users):
    with ThreadPoolExecutor(max_workers=8) as pool:
        results=list(pool.map(lambda _:outcome(lambda:redeem(users,'invalid')),range(8)))
    verified = results.count(400)==5 and results.count(429)==3
    assert verified, 'Synthetic recovery invariant failed'
    verified = outcome(lambda:auth.authenticate(users[0][0],users[2],'synthetic-login'))==200
    assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        verified = conn.execute("SELECT attempts FROM login_limits WHERE bucket LIKE 'recover:user:%%'").fetchone()['attempts']==8
        assert verified, 'Synthetic recovery invariant failed'
        conn.execute("UPDATE login_limits SET expires_at=clock_timestamp()-interval '1 second' WHERE bucket LIKE 'recover:%%'")
    verified = outcome(lambda:redeem(users,'invalid'))==400
    assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        verified = conn.execute("SELECT attempts FROM login_limits WHERE bucket LIKE 'recover:user:%%'").fetchone()['attempts']==1
        assert verified, 'Synthetic recovery invariant failed'

def test_global_and_proxy_precede_bounded_unknown_buckets(users):
    for i in range(20): recovery.admission('unknown'+str(i),'same-proxy')
    verified = outcome(lambda:recovery.admission('new-name','same-proxy'))==429
    assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        verified = conn.execute("SELECT count(*) AS n FROM login_limits WHERE bucket LIKE 'recover:user:%%'").fetchone()['n']==20
        assert verified, 'Synthetic recovery invariant failed'
    for i in range(79): recovery.admission('distributed'+str(i),'proxy'+str(i))
    verified = outcome(lambda:recovery.admission('beyond-global','new-proxy'))==429
    assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        verified = conn.execute("SELECT count(*) AS n FROM login_limits WHERE bucket LIKE 'recover:user:%%'").fetchone()['n']==99
        assert verified, 'Synthetic recovery invariant failed'

def test_controlled_failure_processing(users,monkeypatch):
    code,_=issued(users)
    original=auth.password_hash
    counts=[]
    def counted(password,salt=None):
        counts.append(1)
        return original(password,salt)
    monkeypatch.setattr(auth,'password_hash',counted)
    timings=[]
    for name,candidate in [(users[0][0],'malformed'),(users[0][1],code),('synthetic-unknown',code)] * 3:
        start=monotonic()
        verified = outcome(lambda:recovery.redeem(anonymous(),name,candidate,NEW,NEW))==400
        assert verified, 'Synthetic recovery invariant failed'
        timings.append(monotonic()-start)
    verified = len(counts)==9
    assert verified, 'Synthetic recovery invariant failed'
    groups=[sorted(timings[i::3])[1] for i in range(3)]
    verified = max(groups)<min(groups)*3
    assert verified, 'Controlled invalid-proof median work diverged'

def test_operator_terminal_to_app_own_account_without_app_password(client,users):
    from test_password_recovery_operator import cli
    name=users[0][0]
    status,captured=cli(name,[(b'bekrefte',name),(b'TRYGT:','TRYGT'),(b'SENDT','SENDT')])
    verified = status==0
    assert verified, 'Synthetic recovery invariant failed'
    match=re.search(rb'Engangskode: ([A-HJKM-Z2-9]{4}(?:-[A-HJKM-Z2-9]{4}){4})',captured)
    verified = match is not None
    assert verified, 'Synthetic terminal code missing'
    code=match.group(1).decode()
    verified = client.get('/auth/session').status_code==401
    assert verified, 'Synthetic recovery invariant failed'
    result=post(client,users,code)
    verified = result.status_code==200
    assert verified, 'Synthetic operator-to-app redemption failed'
    result=client.post('/auth/login',headers=headers(client),json={'username':name,'password':NEW})
    verified = result.status_code==200
    assert verified, 'Synthetic recovery invariant failed'

@pytest.mark.parametrize('operation',['issue','revoke','change'])
def test_obsolete_code_waits_for_preceding_mutation(users,gates,operation,monkeypatch):
    code,_=issued(users)
    token,_=auth.authenticate(users[0][0],users[2],'synthetic-before')
    entered,release=Event(),Event()
    original_confirmed=recovery.confirmed
    original_hash=auth.password_hash
    def pause():
        if not entered.is_set():
            entered.set()
            verified = release.wait(10)
            assert verified, 'Mutation release timeout'
    def confirmed(conn,target):
        original_confirmed(conn,target)
        pause()
    def hashed(password,salt=None):
        if password==users[2]:pause()
        return original_hash(password,salt)
    if operation=='change':monkeypatch.setattr(auth,'password_hash',hashed)
    else:monkeypatch.setattr(recovery,'confirmed',confirmed)
    actions={'issue':lambda:issued(users),'revoke':lambda:recovery.revoke(recovery.resolve(users[0][0])),
             'change':lambda:auth.change_password(request_for(token),users[2],NEW,NEW)}
    with ThreadPoolExecutor(max_workers=2) as pool:
        first=pool.submit(gates.run,'mutation',lambda:outcome(actions[operation]))
        verified = entered.wait(5)
        assert verified, 'Synthetic recovery invariant failed'
        second=pool.submit(gates.run,'redeemer',lambda:outcome(lambda:redeem(users,code)))
        try:gates.blocked('redeemer','mutation')
        finally:release.set()
        verified = first.result()==200
        assert verified, 'Synthetic recovery invariant failed'
        verified = second.result()==400
        assert verified, 'Synthetic recovery invariant failed'

def test_login_committed_before_recovery_is_revoked(users,monkeypatch,gates):
    code,_=issued(users)
    entered,release=Event(),Event()
    original=auth.password_hash
    def hold(password,salt=None):
        if password==users[2]:
            entered.set()
            verified = release.wait(10)
            assert verified, 'Login release timeout'
        return original(password,salt)
    monkeypatch.setattr(auth,'password_hash',hold)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first=pool.submit(gates.run,'login',auth.authenticate,users[0][0],users[2],'synthetic-before')
        verified = entered.wait(5)
        assert verified, 'Synthetic recovery invariant failed'
        second=pool.submit(gates.run,'redeemer',lambda:outcome(lambda:redeem(users,code)))
        try:gates.blocked('redeemer','login')
        finally:release.set()
        token,_=first.result()
        verified = second.result()==200
        assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        verified = outcome(lambda:auth.session(conn,request_for(token)))==401
        assert verified, 'Synthetic recovery invariant failed'

@pytest.mark.parametrize('field',['username','code','new_password'])
def test_escaped_surrogate_is_bounded_safe_api_rejection(client,users,field):
    import json
    body=dict(username=users[0][0],code='invalid',new_password=NEW,confirmation=NEW)
    body[field]='\ud800' if field!='new_password' else '\ud800'*12
    if field=='new_password':body['confirmation']=body[field]
    result=client.post('/auth/password/recover',headers={**headers(client),'Content-Type':'application/json'},content=json.dumps(body))
    verified = result.status_code == 422
    assert verified, 'Malformed Unicode must reject without server error'
    verified = result.json() == {'detail':'Kontroller feltene.'}
    assert verified, 'Synthetic recovery invariant failed'
    with database() as conn:
        bounded = conn.execute("SELECT count(*) AS n FROM login_limits WHERE bucket LIKE 'recover:%%'").fetchone()['n'] == 0
        assert bounded, 'Invalid Unicode is rejected before recovery admission'
        verified = not conn.execute('SELECT 1 FROM sessions WHERE owner=ANY(%s)',(users[1],)).fetchone()
        assert verified, 'Synthetic recovery invariant failed'


@pytest.mark.parametrize('style', ['compact', 'lower', 'hyphens', 'spaces', 'legacy-length'])
def test_readable_code_variants(client, users, style):
    code, _ = issued(users)
    shaped = len(code) == 20 and all(c in recovery.CODE_ALPHABET for c in code)
    assert shaped, 'Invalid generated recovery shape'
    candidate = {'compact': code, 'lower': code.lower(),
                 'hyphens': recovery.display_code(code),
                 'spaces': recovery.display_code(code).lower().replace('-', ' '),
                 'legacy-length': code + '-' * 23}[style]
    result = post(client, users, candidate)
    assert result.status_code == 200, 'Readable code redemption failed'
    assert post(client, users, candidate).status_code == 400, 'Code replay accepted'


def test_readable_code_ascii_normalization_and_entropy():
    assert len(recovery.CODE_ALPHABET) == len(set(recovery.CODE_ALPHABET)) == 32
    assert not set('01IL') & set(recovery.CODE_ALPHABET)
    assert 'O' in recovery.CODE_ALPHABET
    example = 'ABCD' * 5
    assert recovery.canonical_code('abcd-abcd abcd-abcd-abcd') == example
    for malformed in ['0' + example[1:], 'I' + example[1:], 'l' + example[1:],
                      'ß' + example[2:], 'Ａ' + example[1:], example + '\n',
                      example + '\t', example + '\u00a0', example[:-1], example + 'A',
                      ' ' * 257 + example]:
        assert recovery.canonical_code(malformed) is None, 'Malformed code accepted'


@pytest.mark.parametrize('ambiguous', [False, True])
def test_legacy_code_exact_and_case_sensitive(client, users, ambiguous):
    import secrets
    code, proof = issued(users)
    legacy = ('ABCD' * 5 + '-' * 23) if ambiguous else secrets.token_urlsafe(32)
    with database() as conn:
        conn.execute('UPDATE recovery_proofs SET digest=%s WHERE id=%s', (auth.digest(legacy), proof['id']))
    changed = legacy.swapcase()
    assert changed != legacy, 'Legacy test needs an alphabetic character'
    assert post(client, users, changed).status_code == 400, 'Legacy case altered'
    assert post(client, users, ' ' + legacy).status_code == 400, 'Legacy spacing altered'
    assert post(client, users, legacy).status_code == 200, 'Legacy proof lost compatibility'


def test_malformed_readable_codes_consume_admission(client, users):
    code, _ = issued(users)
    for _ in range(5):
        assert post(client, users, '0' + code[1:]).status_code == 400
    assert post(client, users, code).status_code == 429, 'Malformed attempts bypassed admission'



def test_generation_uses_twenty_independent_choices(users, monkeypatch):
    calls = []
    def choose(alphabet):
        calls.append(alphabet)
        return alphabet[(len(calls) - 1) % len(alphabet)]
    monkeypatch.setattr(recovery.secrets, 'choice', choose)
    code, _ = issued(users)
    valid = len(calls) == 20 and all(a == recovery.CODE_ALPHABET for a in calls)
    assert valid, 'Generator must make twenty independent CSPRNG selections'
    matches = code == recovery.CODE_ALPHABET[:20]
    assert matches, 'Generator must preserve each independent selection'
