---
title: 'Review and preserve dated line 20 route evidence'
type: 'feature'
created: '2026-11-20'
status: 'in-review'
route: 'dispatch'
baseline_commit: '755b6f9c43c13bcad1eef5555d9672c8f9f50456'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Present bounded, dated public departures when a driver inspects a saved draft. Preserve an expressly selected departure/occurrence range at overall confirmation, with imported and manual facts preserved.

## Boundaries & Constraints

Use CRN-E1-S1–S4, QC01–12 and the source contracts under `D:/IBE160-plan-complete-route-network/_bmad-output/experimental-extensions/complete-route-network` at `7cada9d2e66af9806358f582bc8ea459321a6563`. Implement line 20, both directions and variants, for the explicitly qualified 2026-11-23–29 window. Keep the original October/November casebook as historical replay. Enrichment may use no private or location input in public requests. Only edit the V2 worktree and do not stage, deploy or commit.

| Scenario | Expected behavior |
| --- | --- |
| Qualified dated scope | Return bounded complete/partial/unavailable coverage independently of found candidates. Keep stored date, raw local time/day offset, UTC interpretation, namespaced journey, pattern and ordered calls. |
| Matching alternatives | Explicit candidate selection, neither route number, unsupported code, nearest time nor an empty service query establishes a unique match or absence. |
| Draft and confirmation | Saved draft revision and a versioned route decision remain explicit. Freeze the acknowledged selection in the existing workday confirmation transaction; retries do not recompute or update it. |
| Source change and manual continuity | A stale, cancelled or changed source does not overwrite a confirmed reference or any imported/manual fact. Keep offline, expired, legacy, repeated stop, cross-midnight and DST cases truthful. |

</frozen-after-approval>

## Code Map

- `backend/app/workday_storage.py` review and confirm hold the existing draft lock; extend the exact stored review/operation boundary with a bound route revision. Keep the accepted legacy retry hash and strict DTOs compatible. `draft_storage.py` owns session and draft authorization.
- Migration `017_route_reference.sql` stores authorized route decisions and frozen references in separate tables with parent FK cascade. Read through an explicit private subresource. The existing FastAPI app middleware supplies private Origin/CSRF and no-store.
- `frontend/src/PrivateDrafts.tsx` clean saved draft and `PrivateActivitySelection.tsx` acknowledged selection are the normal review and frozen displays. Retain manual alternatives and current activity semantics.
- Public read-only evidence: Troms NeTEx generation `1795129398375617`, ETag `5d5e931e207e5ccfc8b6dd2cae6314f8`, SHA-256 `03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9`. 7,225,724 compressed bytes, 171 flat members; exact line 20 XML and shared XML. Cross-check source-generated active counts (136×4, 143, 109, 64) and retain provenance. Empty dated API results are insufficient. Use public archive with bounded download and XML/ZIP limits. Preserve exact NSR Quay identifiers for the later versioned coordinate sidecar.

## Tasks & Acceptance

- [x] Implement bounded source preparation and normalize the P1 service calendar and ordered call facts.
- [x] Implement private draft references and explicit review. Freeze in the confirmation transaction and preserve legacy operations and deadlines.
- [x] Exercise additive migration, calendar and repeated stop controls, review races, operation replay, authorization and source loss.
- [ ] Complete the independently labelled actual shift/departure ledger using a qualified current version, followed by personal acceptance.

## Implementation Notes

Keep a separate launch-time qualified public reference rather than fetching for every query. Coordinate mutations to shared `private_main.py` with the parent. Only the owner sandbox may load the public live source. Complete-network P2 and automatically inferred road identity are outside this increment.

## Spec Change Log

- Fixed an actual acquisition clock to the archived digest and added a path through configured startup for closed dated evidence.

## Review Triage Log

- Verified the public pin, repeated Quay controls and transactional freeze against independent synthetic inputs. The missing real-shift oracle and refresh timing remain named qualification gates. [Pilot source and scope](../../docs/v2-route-p1.md).
