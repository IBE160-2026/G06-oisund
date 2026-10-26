---
title: '11.5 — Reuse notices across days until explicit expiry'
type: feature
created: 2026-10-26
status: done
route: dispatch
review_loop_iteration: 0
baseline_commit: aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed
story: '11.5'
story_key: 11-5-read-line-date-notices
owner_acceptance: accepted
owner_accepted_on: 2026-10-26
context:
  - D:/IBE160/_bmad-output/specs/spec-11-5-cross-day-notice-register/implementation-plan.md
---

<frozen-after-approval reason="Owner rejects per-shift notices and explicitly defines cross-day expiry/extension rules on 2026-10-26; standing autonomous implementation authorization">

## Intent

Register a traffic notice once for the signed-in account and automatically consult it on every eligible imported/confirmed day, without re-entry. A required ending date controls automatic expiry. Manual earlier ending is allowed; extension must be accepted before expiry. An expired or manually ended notice cannot be revived or extended.

## Boundaries & Constraints

**Always:** One account-owned incident identity, independent of original shift closure/deletion/expiry. Reuse exact-line/all-line and planned-interval filtering with honest uncertainty/coverage warnings. A notice is active until the server ending instant, or earlier explicit manual ending. Show `Utløpt` separately from `Avsluttet manuelt`; neither means verified road clearance or source checking. Hide both from the active reader; management exposes them as read-only history. Require a future ending date for new registrations. Preserve a precise entered ending clock when provided; date-only ending means the end of that Oslo calendar day, clearly stated. Extend only while still registered and before the existing deadline, with an atomic server check; reject stale/lost retries after expiry without resurrection. Source check remains explicit and separate.

Keep ended/expired notices for seven days after their effective ending, then deny/purge notices and associated command metadata on startup/hourly. No read/login/retry extends retention. Existing unknown-ending notices remain visible as `Mangler sluttdato` in maintenance, excluded from the active reader until explicitly completed; keep their original storage deadline, without inventing source validity. Existing dated notices/IDs/content/timestamps/check state and immutable receipts survive migration; allow a one-time seven-day migration grace for already ended legacy records so rollout does not silently delete them.

Preserve every existing 11.5/11.6 dirty-tree change and original-command recovery, proposal/comparison, navigation, selected activity, access/session isolation and no-store behavior. Keep unsaved registry input/recovery alive independently of plan switches/expiry. Ordinary owner records are never test fixtures. Stop before staging/commit/push or starting any further story. No manual acceptance.

**Never:** No per-day copies, title/text-based incident merging, automatic source fetch, private browser persistence, inferred source verification, extending expired notices or silently converting existing unknown validity to a date. No unrelated 11.6 redesign.

## I/O & Edge-Case Matrix

| Scenario | State/input | Required behavior | Failure handling |
|---|---|---|---|
| Cross-day | One notice, days A/B with 20/24 | Same ID automatically relevant in both; edits/check visible once across days | Foreign account cannot see/use it |
| Parent removal | Original day closes/deletes/expires | Independent notice remains through its own deadline | No original-shift dependency |
| Ending | Required date, optional exact clock | Explicit Oslo deadline; automatic expiry, separate manual earlier ending | Missing/past deadline blocked with retained input |
| Extension race | Before/at/after deadline, concurrent edit/retry | Only accepted pre-deadline extension succeeds once | No receipt-based resurrection or force overwrite |
| Legacy migration | Existing notices/receipts, unknown end | Preserve fields/IDs; unknown end qualified for completion | No fabricated date or silent merging/deletion |
| Recovery/navigation | Lost save/check/end, plan switch, identity loss | Original identity/status-first recovery retained across screens | Session/ownership/lifecycle authority wins |

</frozen-after-approval>

## Code Map

- `backend/app/workday_notice_storage.py`, `workday_notice_domain.py`, migrations 011/012: current parent ownership/cascade/receipt coupling; evolve additively or introduce a single canonical account registry with a compatibility adapter.
- `backend/app/workday_outcome_storage.py`, `private_storage.py`: closure shortens old notice receipts; cleanup cascades through workdays. Separate global commands and retention from these paths while preserving legacy receipts.
- `backend/app/notice_reader_domain.py`, `private_main.py`: project one owner registry against an authorized displayed plan; plan read lease and notice retention are distinct.
- `frontend/src/PrivateNotices.tsx`, `PrivateNoticeReader.tsx`: currently validate current workday/expiry and lifecycle; replace with account notice contracts, separate effective status and timers.
- `PrivateDrafts.tsx`, `PrivateConfirmation.tsx`, `PrivateWorkdayView.tsx`: mount registry state above plan replacement/expiry, preserve current navigation/locks and avoid hidden duplicate screens.
- `recoverOperation.ts`: delivered 11.6 behavior; reuse unchanged where possible. Registry callbacks must no longer require original shift authority.
- Notice/reader/recovery tests and `scripts/verify-private-drafts.py`: update only superseded notice contracts; retain unrelated guards and historical evidence.

## Tasks & Acceptance

- [x] `backend/migrations/private/013_*.sql`, notice domain/storage/routes/cleanup — independent owner registry, atomic deadline rules, compatible old receipts and safe upgrade.
- [x] `frontend/src/PrivateNotices.tsx`, reader and retained workspace integration — shared management, required ending/date-only semantics, expiry/history and intact recovery.
- [x] Backend/browser notice/reader/recovery tests and verifier — real cross-day persistence, original-day purge, boundary/extension/ownership races, legacy migration/restart, rendered Day/Night and preserved state.
- [x] Active planning, specification/log/sprint/evidence — record rejected prior contract, actual execution/results and owner steps; keep 11.6 local work intact.

Given a saved account notice, when another confirmed day matches its lines/date before expiry, then the same incident appears without copying or re-entry. Given original-shift removal, when another authorized day opens, then the independent notice remains available. Given an expired/manual-ended notice, when edited or retried, then no extension/resurrection occurs and historical check/status facts remain separate.

## Implementation Notes

Owner clarified required ending and pre-expiry extension; no open intent question remains. Significant schema/API/retention/UI footprint requires dispatch. Root preserved 914 existing tracked/untracked files in `tmp/11-5-crossday-initial`, including complete 11.6 work. Root owns documentation/final review/ordinary rollout; worker owns scoped implementation and focused synthetic tests, restoring services. No nested Build workflow. Read the companion implementation plan fully.

## Spec Change Log

## Review Triage Log

All three independent review layers returned before triage on 2026-10-26. Each finding is recorded separately before grouping.

| ID | Verdict | Evidence and disposition |
|---|---|---|
| Blind-1 | medium | Same-revision receipt equality normalizes retention but not nullable original-day provenance. Migration's SET NULL is reachable after parent deletion; patch receipt comparison to ignore only documented mutable provenance/retention metadata. |
| Blind-2 | medium | Receipt recovery checks immutable historical expires_at against device time even though server receipt authority now follows the notice; patch by relying on authorized lookup/current record, preserving immutable result validation. |
| Blind-3 | medium | Legacy per-day capacity can aggregate above 200; SQL LIMIT 201 plus frontend total cap denies both reader and maintenance. Patch existing collection bounds/reading to preserve full legacy discovery without silent truncation; retain new-registration cap. |
| Blind-4 | false | This is intentional broad planned-day matching, not a claim of precise trip relevance. The retained test_line_matching_is_independent_of_which_activity_supplies_time_overlap explicitly requires this result; frozen intent reuses these existing planned-interval rules. No change. |
| Blind-5 | medium | Authoritative expiry/absence after retention leaves original.current and pending set forever. Patch existing denial branch to allow abandoning an unrecoverable command after verified session and authoritative absence, preserving proposal and never reporting successful saving. Transport/proxy failure must stay unresolved. |
| Blind-6 | medium | terminal derives from original base while refresh never offers a current active replacement unless conflict already set; comparison acknowledgement is itself disabled by stale base. Patch refresh/comparison guards to allow explicit review of current active revision with proposal intact. |
| Blind-7 | medium | The shared 2,000-receipt check executes before end, so exhausted normal capacity blocks early manual ending. Patch to exempt the one terminal ending per existing incident; retries remain idempotent and other operations bounded. |
| Blind-8 | medium | Separate now readings can include a candidate already expired relative to returned server_now and cause frontend rejection. Patch projection to use one captured instant and cover boundary. |
| Blind-9 | low | History already distinguishes manual ending, entered source validity and expiry, but omits the exact manual-ending instant. Existing explicit status fulfills the owner's distinction; adding a new API field/history surface for timestamp detail is more than a direct correction. Reject this low-impact enhancement in this correction; no fabricated legacy timestamp. |
| Blind-10 | medium | Migration test uses partial receipt JSON; separate deployed-shape recovery test inserts post-migration rows, leaving serialization/provenance integration unproven. Patch realistic receipt fixture and persisted isolated/synthetic recovery coverage. |
| Edge-1 | medium | readerOpen survives top navigation while registryOpen lacks screen guard, hiding preparation/editor. Patch registry visibility to follow actual visible plan reader and cover navigation. |
| Edge-2 | medium | Independently confirms Blind-1 through SET NULL provenance and immutable receipt equality. Patch with Blind-1. |
| Verification-1 | medium | Pre-verified regression gap: populated migration lacks registered notice expired more than seven days ago. Patch fixture/grace assertions and cleanup survival for notice and immutable receipt. |

Patch groups: immutable recovery (Blind-1/2, Edge-2), legacy collection compatibility (Blind-3), terminal recovery (Blind-5), stale proposal review (Blind-6), terminal capacity (Blind-7), projection clock (Blind-8), migrated receipt/grace verification (Blind-10, Verification-1), reader navigation (Edge-1). These correct demonstrated states through existing endpoints and controls; no new workflow or owner-intent question is needed. Blind-4 is refuted; Blind-9 is rejected under the low-impact complexity rule.

Reinspection: the original blind reviewer found every retained finding resolved and withdrew Blind-4 under the established contract; the original edge reviewer verified both visibility/provenance patches and found no concrete regression; the original verification reviewer confirmed removing the expired-registered migration grace would now fail the populated HTTP/migration test. These were independent source/test inspections, not additional test runs. Focused patch verification: five backend cases passed; ten unique browser cases passed across the initial seven passes and four affected reruns after fixing asynchronous test waits; build passed. No retained correction finding is deferred. The separate unchanged access-clock limitation is recorded in deferred-work.md.

## Verification

Build; real synthetic PostgreSQL/API tests for all matrix rows, populated additive migration/repeated restart and immutable receipts; browser cross-day/expiry/recovery/navigation and enlarged Day/Night evidence. Preserve ordinary rows/secret/database and all original evidence. Relevant broad regression after focused review fixes; report executed scope and failures honestly. Physical Lenovo Pad/Android/Brave/mobile-network qualification remains separate.

Final root gate exited 0: **420 backend tests passed in 516.21s; all 472 browser cases passed in one invocation (37.4m)**. Populated restart, repeated migrations, exact state/receipt/deadline/session preservation and build passed. One TestClient dependency deprecation warning remains informational. Raw log: `tmp/11-5-crossday-root-full-gate.log`; [delivery evidence and owner steps](../../docs/evidence/11-5-crossday-register.md).

All 112 source/test/migration/verifier hashes match the gate baseline. All 914 initial files remain; 309 historical evidence files restored byte-for-byte (111 fresh rerenders archived separately), 24 original fixtures and 25 historical frozen blocks preserved. Generic delivered 11.6 recovery is unchanged. Migration 013 is now applied locally: original fields of all 23 ordinary tables, original database/secret and 12 immutable legacy receipt/identity hashes are preserved. Only approved independent receipt-retention metadata and schema additions changed; normal expired login-throttle cleanup is separately documented. Tested HTML/JS/CSS and 43 runtime Python/migration files match the served version. Ordinary services are healthy, synthetic services stopped.

Specification stays in-review, canonical story/sprint review, owner acceptance pending. Existing 11.6 remains review; no further story/epic, staging, commit or push. The owner's request overrides generic Build completion/commit defaults. Physical device/mobile-network testing is not claimed.

## Owner acceptance — 2026-10-26

Jonas explicitly replied `Godkjent.` to the corrected delivery report. Story 11.5, its active specification and sprint tracking are now done with owner acceptance accepted. This accepts the corrected account-owned cross-day/expiry delivery, not the rejected historical per-shift contract. Technical evidence remains 420 backend and 472 browser passes; this message adds no test execution or physical-device qualification. Existing 11.6 remains review, and Epic 11 remains in-progress. Commit/push and further work remain outside the authorization.
