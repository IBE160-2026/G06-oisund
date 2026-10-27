---
title: '12.1 — Enforce the retained-data boundary'
type: bugfix
created: 2026-10-26
status: done
route: dispatch
review_loop_iteration: 0
baseline_commit: 0bae54833f38dc3dbf041d54c324c220618c21da
story_key: 12-1-enforce-the-retained-data-boundary
owner_acceptance: accepted
owner_acceptance_date: 2026-10-27
technical_status: integrated-verified
context:
  - D:/IBE160/_bmad-output/specs/spec-12-1-retained-data/implementation-plan.md
---

## Owner acceptance — 2026-10-27

Jonas explicitly approved Story 12.1 after completing the agreed manual checklist A–F without problems: “Siden dette var testene som var lagt opp til er story 12.1 godkjent.” Status is now done, owner acceptance accepted. Manual context: Jonas_desktop, Brave private window, reported reference83cdd2b; running product is62a0cf4-equivalent as verified in the current handoff. This accepts12.1 only, not12.2, later device qualification or later stories. Earlier pending-acceptance statements below describe the historical implementation/integration stages. See [manual guide](../../docs/testveiledning-12-1-deretter-12-2.md).

<frozen-after-approval reason="Owner explicitly authorizes autonomous specification, implementation, testing and review; stop before manual acceptance">

## Intent

Enforce and demonstrate the existing private retention contract across originals, drafts, confirmed work, outcomes, independent account notices and operation metadata. Close concrete resurrection and late-read gaps while preserving the accepted 11.5 cross-day model and original-command recovery.

## Boundaries & Constraints

**Always:** Draft creation+7d; confirmed min(planned-end+7d, terminal-server-end+7d); independent notices effective-ending+7d, including accepted legacy handling. Deny expired authority immediately; startup/hourly purge; no sliding renewal. Original uploads remain transient, absent from persistent browser stores/logs/repository. Preserve identity, manual actions, unknown facts and immutable receipts.

**Never:** No day-cascade deletion of account notices, indefinite payload/tombstone retention, weakened tests, ordinary data/service changes, other worktree edits, acceptance registration, commit/push/merge or next story. Work only in D:/IBE160-story-12-1. Test only synthetic accounts in a dedicated Compose project with private volumes/network and ports. Do not invoke existing verification scripts that stop ordinary services.

## I/O & Edge-Case Matrix

| Scenario | State | Required behavior | Failure handling |
|---|---|---|---|
| Creation replay | Notice ended early, row/receipt purged, original ending still future | Original create cannot recreate; genuinely new create uses server-issued live ID | Unknown/expired/foreign IDs rejected without mutation |
| Late writes | Creation admission or original notice deadline crossed inside transaction | Roll back content/revision/deadline/receipts | Reject; no renewal/resurrection |
| Late reads | Draft/notice/list/reader retained at initial read but expiry before final authorization | Exclude expired rows; detail denies; projected notices obey final server_now | No expired private presentation |
| Independent lifetimes | Two days share notice; original day deleted/expired | Shared identity survives; outcomes/day commands disappear with day; notice history/commands purge at own bound | No per-day notice copies/cascade |
| Originals | Success, failure, cancellation, interrupted worker | No raw original or extraction archive persisted; worker/admission released | Honest error, no payload logs |
| Browser boundary | Logout, expiry, Back/reload, delayed responses, slow device clock | Clear/hide private state, reauthorize; no private persistent stores; safe timer scheduling | Server access remains authoritative |

</frozen-after-approval>

## Code Map

- `backend/app/workday_notice_storage.py`: create currently accepts unknown client UUID after purge; introduce bounded payload-free server-issued admission using existing operation_id shape. Preserve lookup-first receipt compatibility and terminal guards.
- `backend/app/private_main.py`, `private_storage.py`, new migration 014: issuance endpoint, startup/hourly cleanup for pending admission; additive migration.
- `backend/app/draft_storage.py`, `workday_storage.py`, `workday_notice_storage.py`: final authorization/read expiry checks. Existing notice list test deliberately permits stale captured time; strengthen to final expiry exclusion with explicit evidence.
- `frontend/src/PrivateNotices.tsx`: obtain creation ID before constructing first command; edits/check/end retain client UUIDs. Preserve pending identity through ambiguous dispatch and no duplicate POST recovery.
- `frontend/src/PrivateAccess.tsx`, `PrivateDrafts.tsx`: clamp/recheck deadline timers rather than immediate overflow expiry.
- `backend/app/private_import.py`, `pdf_import.py`: byte-only worker and existing cancellation/finally cleanup; qualify with tests, avoid unnecessary rewrites.
- Backend tests and frontend private helpers: use issuance for valid new creates while keeping explicit invalid/replay tests. Existing independent expectations remain authoritative.

## Tasks & Acceptance

**Execution:**
- [x] `backend/migrations/private/014_*.sql`, notice storage/routes/cleanup -- live server admission for new notices, bounded no-payload metadata, rollback checks and compatible accepted receipt recovery.
- [x] `backend/app/*storage.py` -- final read-retention checks without altering independent notice ownership or operation semantics.
- [x] `frontend/src/PrivateNotices.tsx`, `PrivateAccess.tsx`, `PrivateDrafts.tsx` -- safe create issuance/recovery and timer scheduling.
- [x] `backend/tests/test_retained_data.py`, relevant existing tests, `frontend/tests/private-retention.spec.ts` and helpers -- deterministic boundary regressions, originals/browser privacy and lifecycle evidence.
- [x] `docs/evidence/12-1-retained-data.md`, isolated test runner/config and sprint/spec -- executed results, review, integration contract and manual steps.

**Acceptance Criteria:**
- Given private resources, when read/retry/login occurs, then original retention remains fixed and expired work cannot return or recreate.
- Given pending or accepted commands crossing their authority deadline, when accepted atomically, then expired attempts have no persisted effect.
- Given startup/hourly cleanup, when deadlines have passed, then all affected payload/command rows are gone while independently live account notices remain.
- Given imported originals or navigation after logout/expiry, when processing ends or access is lost, then no persistent original/private browser cache is available.

## Implementation Notes

No product-intent gaps. API admission is an implementation correction necessary to reconcile complete metadata deletion with replay denial; document the new prerequisite for 12.2. Standing owner autonomy supersedes intermediate Build approvals; explicit no-commit includes session logs.

## Spec Change Log

## Review Triage Log

| Finding | Verdict | Evidence and disposition |
| --- | --- | --- |
| B1 | medium | New-create row is None, so both original-ending guards skip it. A held create can cross its valid_until while admission remains live. Patch final future-ending validation and rollback test. |
| B2 | medium | Existing wall-clock expiry affects sessions/drafts under slow clocks; clamping fixes overflow but exposes indefinite presentation with a fixed clock. Patch existing clock authority using observable server time and monotonic elapsed time; preserve leases and accelerated-clock tests. |
| B3 | medium | stop only stops Compose and leaves the task preview PID alive. Patch scoped stop with exact process ownership validation. |
| B4 | medium | serve reports success immediately even if strictPort child exits. Patch readiness/ownership check and fail on occupied port without touching its listener. |
| B5 | medium | Manifest includes backend inputs but omits frontend package.json, tsconfig and Dockerfile. Patch source-input inventory. |
| B6 | medium | Source manifests alone do not identify loaded modules or served build. Root verifies API modules against host sources after restart and compares served JS/CSS with final dist before browser qualification. |
| B7 | medium | Single-expiry pagination case leaves 50 live rows, so empty scan continuation is not exercised. Patch existing parameterized test with all-first-page-expired and consecutive-empty-page cases. |
| B8 | medium | Changed draft/notice consumers lack executed sparse/empty-continuation browser cases. Add explicit consumer journeys. |
| B9 | medium | New admission route is covered under valid credentials only. Add missing-auth/CSRF/origin/extra-fields rejection tests with unchanged admission counts. |
| B10 | medium | Restart and final-source checks remained pending in handoff draft. Complete actual populated migration/restart evidence before final report. |
| E1 | medium | Independently confirms B1: new creation can cross original source ending; patch same final guard/test. |
| E2 | medium | Independently confirms B2: browser presentation follows slow clock after clamping. Patch server/monotonic clock use and eventual-expiry regression. |
| V1 | medium | Pre-verified gap: neither frontend consumer is tested with sparse/empty continuation, and backend-only coverage cannot kill old validator restoration. Patch browser journeys with subsequent retained rows. |
| N1 | medium | Root traced the global notice controller: the list filters expired history but editor/base/comparison can retain saved fields past expires_at. Patch retention-based clearing and late-response invalidation, retaining validity history until storage expiry and unrelated new proposals. |
| V2 | medium | Verified old private-drafts malformed cases now describe valid sparse pages; default gate omitted this suite. Preserve rejection checks with actually invalid/nonadvancing cursors and run the whole draft suite. |

| V3 | medium | Reinspection gap: old plan expiry tests advance Date.now, so reverting PrivateConfirmation clock reads could survive. Added one frozen-device-clock plan deadline test with no subsequent network/revalidation; focused case passed in17.3s. |

Patch groups: creation deadline (B1/E1), clock authority (B2/E2), task runner lifecycle/identity (B3?B6), scan continuation and stale assertions (B7/B8/V1/V2), route denial tests (B9), final evidence (B10). All demonstrate reachable states and direct corrections under the frozen existing retention/verification intent; no product-intent question, deferred feature, or API body change is required. No reviewer finding is dropped. Root completes evidence separately from product patch.

## Verification

Dedicated synthetic PostgreSQL/API full backend gate; focused browser retained-data/cross-day/recovery/import/access gate; build; populated migration/repeated restart and source identity evidence. Keep original failures and final exit codes. Review required before handoff. Physical tablet/remote testing belongs to parallel work.


### Reinspection and executed root checks

Blind and edge reviewers re-read the patched source and retained no concrete defect. Verification reviewer confirmed sparse-page/stale-test fixes and raised V3, subsequently tested successfully. Root N1 includes removal of expired saved manual/imported drafts, notice editor/comparison/original metadata, record state and reader payload/choice state; unrelated fresh proposals survive. Server Date is exposed through CORS and privateClock uses memory-only monotonic advancement.

Root actual two-startup populated 013 to 014/repeat-migration probe passed: due draft/day/outcome/receipt rows removed, live independent notice and immutable receipt rows identical, original purged create denied, expired admission purged on second startup. Root compared44 API/migration files in runtime with host SHA256, verified source predates API startup, and matched actual served index/JS/CSS with final dist; no-store and Date exposure passed. Final broad stable-source gates subsequently passed as recorded below.

### Final technical handoff - 2026-10-27

Stable gates passed:441 backend/domain/PDF tests in556.74s and all479 private Playwright cases in40.4m, exit0 and unchanged source manifests in each invocation. All eleven script controls passed. Three independent reviews/reinspections retained no finding; V3 passed in the complete gate. Root populated startup/restart, accelerated hourly scheduling, served build/runtime identity and main/historical preservation checks passed. E11-A6/A11 technically resolved; A7/A8/A12 carried into this story evidence while their broader follow-through remains tracked. Two synthetic line20 acceptance days provisioned only in the dedicated test cluster; credentials stored under ignored .private-runtime.

Keep status in-review and owner_acceptance pending under explicit owner instruction. Generic Build done/commit steps and session-log commit are superseded by the explicit no-commit/manual-acceptance boundary. No staging/commit/push/merge, external activation or further story performed. See [delivery evidence](../../docs/evidence/12-1-retained-data.md) and [machine verification](../../docs/evidence/12-1-verification.json).

## Local integration authorization — 2026-10-27

Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.

Jonas explicitly authorizes separate local commits, integration in order 12.1 then 12.2, automated verification and local main merge before manual acceptance. Earlier no-commit/no-merge instructions describe the historical run and are superseded for this integration. Status remains review/in-review. Current steps and limits: [manual checklist](../../docs/story-12-manual-testing.md).
