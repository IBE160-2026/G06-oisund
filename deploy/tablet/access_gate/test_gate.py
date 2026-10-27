import copy
import json
import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from gate import Admission

POLICY = {'team': 'synthetic-team', 'audience': '1' * 64, 'owner_email': 'owner@owner-domain.no'}


def synthetic_fixture():
    admission = Admission(POLICY)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    jwk.update(kid='synthetic-key', alg='RS256', use='sig')
    admission.keys.fetch_data = lambda: {'keys': [jwk]}
    now = int(time.time())
    claims = {'iss': admission.issuer, 'aud': [POLICY['audience']], 'email': POLICY['owner_email'],
              'sub': 'synthetic-owner-id', 'type': 'app', 'iat': now - 10, 'exp': now + 300}

    def token(change=None, remove=None, signing_key=key, headers=None):
        body = {**claims, **(change or {})}
        if remove:
            body.pop(remove)
        return jwt.encode(body, signing_key, algorithm='RS256', headers={'kid': 'synthetic-key', **(headers or {})})

    variants = {
        'valid': token(), 'malformed': 'not.a.jwt',
        'bad-signature': token(signing_key=other), 'expired': token({'exp': now - 1}),
        'wrong-issuer': token({'iss': 'https://other.cloudflareaccess.com'}),
        'issuer-prefix': token({'iss': 'https://synthetic-team.cloudflareaccess.com.evil.no'}),
        'wrong-audience': token({'aud': ['2' * 64]}),
        'other-identity': token({'email': 'other@owner-domain.no'}),
        'service-token': token({'type': 'service'}), 'future-iat': token({'iat': now + 60}),
        'future-nbf': token({'nbf': now + 60}), 'unknown-kid': token(headers={'kid': 'unknown'}),
        'none-alg': jwt.encode(claims, None, algorithm='none', headers={'kid': 'synthetic-key'}),
        'hs256': jwt.encode(claims, 'synthetic-' * 8, algorithm='HS256', headers={'kid': 'synthetic-key'}),
        'critical-header': token(headers={'crit': ['unknown'], 'unknown': True}),
        'empty-sub': token({'sub': ''}), 'text-exp': token({'exp': str(now + 300)}),
    }
    for name in claims:
        variants['missing-' + name] = token(remove=name)
    return admission, variants, token, jwk


@pytest.fixture
def fixture():
    return synthetic_fixture()


def test_accepts_only_approved_signed_app_token(fixture):
    admission, tokens, *_ = fixture
    assert admission.allows(tokens['valid'])
    for name, token in tokens.items():
        if name != 'valid':
            assert not admission.allows(token), name
    assert not admission.allows(None)
    assert not admission.allows('')
    assert not admission.allows('x' * 16385)


def test_public_key_failure_is_closed(fixture, monkeypatch):
    admission, tokens, *_ = fixture
    def unavailable():
        raise jwt.PyJWKClientError('synthetic outage')
    monkeypatch.setattr(admission.keys, 'fetch_data', unavailable)
    assert not admission.allows(tokens['valid'])


def test_cached_public_key_is_bounded(fixture, monkeypatch):
    admission, tokens, *_ = fixture
    assert admission.allows(tokens['valid'])
    def unavailable():
        raise jwt.PyJWKClientError('synthetic outage')
    monkeypatch.setattr(admission.keys, 'fetch_data', unavailable)
    assert admission.allows(tokens['valid'])  # Verified cached public key, not cached authorization.
    admission.keys.jwk_set_cache.put(None)  # Represents the end of the configured 300-second cache.
    assert not admission.allows(tokens['valid'])


def test_token_urls_cannot_choose_jwks(fixture):
    admission, _, token, _ = fixture
    expected = admission.issuer + '/cdn-cgi/access/certs'
    assert admission.keys.uri == expected
    assert admission.allows(token(headers={'jku': 'http://evil.invalid/key', 'x5u': 'http://evil.invalid/cert'}))
    assert admission.keys.uri == expected


def test_key_rotation_fixture(fixture, monkeypatch):
    admission, _, token, jwk = fixture
    replacement = copy.deepcopy(jwk)
    replacement['kid'] = 'rotated-synthetic-key'
    monkeypatch.setattr(admission.keys, 'fetch_data', lambda: {'keys': [replacement]})
    assert admission.allows(token(headers={'kid': replacement['kid']}))
    assert not admission.allows(token())


@pytest.mark.parametrize('change', [
    {'owner_email': '*@owner-domain.no'}, {'owner_email': 'owner@owner-domain.no,other@owner-domain.no'},
    {'audience': '0' * 64}, {'team': 'https://evil.no'}, {'owner_email': 'owner@identity.invalid'},
    {'owner_email': ['owner@owner-domain.no']}, {'bypass': True},
])
def test_invalid_or_broad_policy_refused(change):
    with pytest.raises(ValueError):
        Admission({**POLICY, **change})


def test_changing_approved_owner_denies_old_token(fixture):
    _, tokens, _, jwk = fixture
    changed = Admission({**POLICY, 'owner_email': 'replacement@owner-domain.no'})
    changed.keys.fetch_data = lambda: {'keys': [jwk]}
    assert not changed.allows(tokens['valid'])
