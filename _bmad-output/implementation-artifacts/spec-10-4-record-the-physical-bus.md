---
title: '10.4 — Record the physical bus'
type: feature
created: 2026-10-22
status: done
owner_acceptance: accepted
accepted_on: 2026-10-24
approved_on: 2026-10-23
route: dispatch
epic: 10
story: '10.4'
alias: V1-08
story_key: 10-4-record-the-physical-bus
baseline_commit: 6d07f74c4e4d2b172ef2e248ae8b3d54d1e64d77
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
---

<frozen-after-approval reason="human-owned intent — changes require human approval">

## Intent

**Problem:** A confirmed private plan cannot independently retain the driver's actual physical bus or a correction to it.

**Approach:** Add explicit manual bus entry, save, correction and reopening to the opened confirmed plan. Keep this current manual value separate from the immutable reviewed snapshot.

## Boundaries & Constraints

**Always:** Label **Fysisk buss**, with unknown/manual/saved/unsaved states. Preserve text formatting and leading zeros, maximum 100 characters; empty/whitespace-only means unknown. Initially use any manually entered snapshot bus; otherwise unknown. Explicit clearing survives reopening. Distinguish current registration from historical confirmation facts/acknowledgements.

Vognløp collects trips; its final three digits, including `006`/`090`, are the realtime-screen value. Import, duty changes and CAR never establish actual bus/replacement. Bus edits leave snapshot, source draft, routes, activity identities/order/times, duty anchors, decisions and deadlines unchanged. Retention remains final-end + seven days.

Use existing identity guards, CSRF/origin, no-store and transactional revisions. Retain failed input in memory; uncertain writes use identical-operation retry/lookup. Conflicts require comparison/reload. Reject stale presentation and deleted/expired resurrection. Protect unsaved/unresolved edits against navigation, plan replacement and deletion. Preserve logout/account-switch clearing and unavailable-revalidation hiding.

**Never:** Add activity-linked bus-change history, automatic/live lookup, activation, outcomes, parser expansion, the 10.5 overview or unrelated retrospective repairs. No ordinary-account tests, private resets, secret/volume replacement, persistent browser content, private payload logs or commit/push before owner acceptance. Tests use disposable synthetic storage.

## I/O & Edge-Case Matrix

| Scenario | Input/state | Result | Failure handling |
|---|---|---|---|
| Initial | Imported/manual confirmed plan | Manual snapshot bus or unknown; independent bus revision | No inferred duty/bus mapping |
| Save/correct/clear | Text or unknown, expected revision | Reopen same current bus; snapshot unchanged | Invalid input writes nothing |
| Retry | Duplicate/lost/malformed reply | Same operation resolves once | Changed payload conflicts; keep uncertain state |
| Concurrent edit | Two windows, same revision | One accepted update | Preserve losing input and show saved comparison |
| Boundary race | Identity change, deletion, expiry | Authorized live acceptance only | Clear/deny; no resurrection or stale display |

</frozen-after-approval>

## Code Map

- `backend/app/workday_storage.py`: reuse `owned`, `presentation`, deletion locking; keep confirmation responses immutable. `draft_storage.py`: reuse `authorized`/fingerprint.
- `frontend/src/PrivateConfirmation.tsx`: reuse validation, expiry/generation/leave guards. `PrivateAccess.tsx` supplies session-bound props/Web Locks; all new traffic uses them, including post-write verification.
- `scripts/verify-private-drafts.py`: synthetic-only guard, sequential verification and operational restoration.

## Tasks & Acceptance

**Execution:**
- [x] New `backend/migrations/private/006_workday_bus.sql`, `backend/app/workday_bus_domain.py`, `workday_bus_storage.py`: separate bus resource with revision initially zero, snapshot fallback, fixed-expiry idempotent receipts and save/read/lookup. Reuse existing plan locks; atomically check live plan/session/revision; cascade deletion/expiry. Replay preserves accepted revision without reverting newer state.
- [x] `backend/app/private_main.py`, `private_storage.py`: strict owner-scoped routes, additive migration/cleanup and input/admission bounds.
- [x] New `frontend/src/PrivateBus.tsx`; `PrivateConfirmation.tsx`, `PrivateDrafts.tsx`, `style.css`: entry/save/cancel, historical/current labels, response validation, retry/lookup, conflict comparison and leave/deletion guards.
- [x] New `backend/tests/test_private_bus.py`, `frontend/tests/private-bus.spec.ts`; `frontend/tests/private-identity.spec.ts`: matrix coverage, immutable facts, formatting, silent account switches, delayed parent reads/replies, retry after newer writes and atomic expiry; synthetic teardown.
- [x] `scripts/verify-private-drafts.py`, `scripts/test_verify_private_drafts.py`: include bus suites, exact restart/migration bus/receipt/deadline equality and failure restoration.
- [x] New `Docs/evidence/10-4-physical-bus.md`; `Docs/development-log.md`, `README.md`, sprint status: executed evidence, review dispositions and owner walkthrough; acceptance before done/publication.

**Acceptance Criteria:**
- Given a confirmed plan, when a bus is saved, corrected, cleared and reopened, then only current manual bus state/revision changes and formatting survives.
- Given duties `960006`, `960090` or `CAR - 1`, when bus is unknown or corrected, then duty/realtime/activity identities remain independent and import never invents bus.
- Given concurrent writes, uncertain replies or changed identity, when saving/retrying, then no silent overwrite, cross-account mutation or false saved status occurs.
- Given expiry/deletion, when a late read/write/retry arrives, then neither private storage nor presentation resurrects the plan.
- Given keyboard use at 768/1440px in Day/Night, when entering/recovering/cancelling, then labels, focus, wrapping and applicable contrast remain usable.

## Implementation Notes

- Owner acceptance, 2026-10-24: Jonas reports, "Test viser at det fungerer som ønsket." This accepts the delivered 10.4 walkthrough. Sprint 10.4 moves from review to done; earlier pending-acceptance notes are historical. No individual manual scenario beyond this reported result is invented. Product code and recorded verification are unchanged. No commit/push or 10.5 start accompanies this documentation closure.

- Final root result, 2026-10-24: **236 backend/API tests (272.31s)** and **all 157 browser tests in one run (10.2m)** passed, exit 0. Exact current-bus/receipt/plan/source/decision/deadline equality survived repeated migrations and PostgreSQL/API restart; production bundle `index-FOJ_MQro.js` passed. Five fully mocked verifier controls passed in 0.143s. Log: ignored `tmp/10-4-root-final.log`. This supersedes all intermediate partial/fixture failures below. All matrix rows have executed evidence. Root re-inspected final saved/conflict Day/Night renders, restored generated historical screenshots and retained new synthetic evidence.
- All three BMAD review layers completed; all retained findings are fixed and re-inspected. Chronological UUID ordering proposal rejected with rationale; root simultaneous-pane claim refuted and its temporary expansion reverted. Original single-pane lifecycle retained and independently re-inspected. No retained finding deferred. Only owner acceptance remains open.
- Local operational API upgraded after the final pass. Test/operational filesystem layers match; additive migration 006 applied. Existing table/secret digests exactly match pre-test baseline and original database container retained. API/app return 200, tested bundle served, unauthenticated new bus/operation routes return 401. Disposable services stopped; ordinary API/database/frontend healthy. No ordinary login/test, volume/secret replacement or private payload output.
- Implementation is technically done; sprint 10.4 is `review` for owner walkthrough. E9-A2–A5 technical evidence also passes this combined run; human action closure remains pending and historical retro verdict unchanged. HEAD remains `6d07f74c4e4d2b172ef2e248ae8b3d54d1e64d77`; no staging, commit, push or 10.5 start. Approved no-publication-before-acceptance overrides generic BMAD local commit.

- 2026-10-24 root implementation audit: complete combined verifier on final worker code passed 229 backend/API tests (255.48s), exact PostgreSQL/API restart and migration equality for bus/receipts/snapshots/deadlines, production build and all 146 browser tests (9.2m), exit 0. Four mocked verifier controls passed (0.116s). Every matrix row has executed coverage. Root read code/tests and inspected final saved/conflict Day/Night renders at 768/1440; historical tracked PNG churn restored. Early Unicode/parent-operation/same-ID/label/receipt-expiry/focus audit issues were corrected and covered before this run. Independent BMAD review follows; no local 10.4 rollout or owner acceptance yet.

- 2026-10-24: Re-read approved specification from disk; frozen intent unchanged. Owner authorized implementation and routine minor refinements without another checkpoint. E9 technical gate passed: 219 backend/API and 129 browser tests, restart/migration equality, build and three mocked controls; all review fixes resolved. Current authorized local E9/spec/log/evidence changes must be preserved. Root matched operational API layers to tested code and verified existing data/secret hashes and database-container identity. No human acceptance or 10.5 start.
- Coordination: implementer owns isolated synthetic implementation verification and restoration through handback. Root owns independent BMAD reviews, final combined verification/documentation and operational API rollout after review. Do not upgrade ordinary runtime, use ordinary accounts, commit/push or record owner acceptance. Append actual test evidence here and report remaining coordinator work.

## Spec Change Log

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| Root implementation audit: Unicode bound | medium / patch | New JS length/maxLength used UTF-16 units while existing draft/backend contracts allow 100 code points, so a valid existing manual bus could be rejected. Align bounding/validation and add Unicode roundtrip evidence. |
| Root implementation audit: parent operation coordination | medium / patch | Bus edits could invalidate an older parent's finally without releasing busy, and controls remained usable during pending confirmation/deletion. A later parent response could discard edits or leave locks stuck. Coordinate disabling, epoch/generation and busy release; exercise these races. |
| Root implementation audit: same-ID reopen | medium / patch | Bus key/effect depended only on unchanged plan ID; reopening that plan would retain a stale bus after another window's correction. Refresh bus state on explicit successful reopen while protecting dirty edits. |
| Root implementation audit: historical label in unconfirmed review | low / patch | Shared Facts unconditionally labelled a not-yet-confirmed bus historical. Make the label context-dependent and correct the literal encoding typo. |
| Root/implementer audit: receipt deadline before cleanup | medium / patch | Initial lookup/replay checked the parent deadline but not receipt expires_at. Align explicit operation expiry checks/cleanup and prove an expired receipt is denied while the parent remains live, without changing current bus/plan. |
| Root implementation audit: keyboard recovery focus | medium / patch | Comparison reload attempted focus before React enabled the input; successful save disabled the active button without transferring focus. Restore input focus after commit and assert both recovery/success paths. |
| Root/implementer audit: denied authoritative presentation | medium / patch, resolved | A denied current resource read originally left saved bus/plan facts visible. Guarded denial now revalidates identity, hides authoritative facts and preserves local text/nonce; live recovery/remote deletion/silent identity cases passed the root combined run. |
| Implementer render audit: Night warning recovery contrast | medium / patch, resolved | Light recovery-control boundary on yellow failed the intended distinction. Scoped dark control palette and actual keyboard text/boundary/focus assertions passed in all four width/theme combinations. |
| Blind 1: Unicode whitespace normalization mismatch | medium / patch | JS trim preserves U+0085 but Python strip clears it; an accepted save then fails exact receipt matching indefinitely. Define consistent client/server normalization and exercise Unicode whitespace. |
| Blind 2: capacity rejection leaves permanent pending state | medium / patch | At 2,000 live receipts, valid API 429 creates no receipt, but the UI locks editing/cancellation behind nonexistent-operation lookup. Distinguish a validated authoritative rejection from malformed/uncertain responses and preserve editable input after identity revalidation. |
| Blind 3: oversized paste silently ignored | low / patch | The length guard returns without status feedback. Add accessible feedback identifying that the field was not changed; retain the previous valid proposal. |
| Blind 4: returning to saved value stays dirty | low / patch | change always sets editing/lock true, even after restoring the saved value. Compare normalized current input to saved state and release semantic no-op edits without spending a receipt. |
| Blind 5: UUID order replaces newest-first | low / reject | Every accepted record remains reachable and the current saved draft stays open after acknowledgement. The E9 contract deliberately reuses stable UUID pagination; chronological compound cursors add public contract/validation complexity for the less common large/multiple-draft selection workflow. No data is hidden or lost. Human acceptance remains pending. |
| Blind 6: concurrent bus save/plan delete untested | medium / patch | Sequential cascade tests do not prove contention in both lock orderings. Add deterministic real-PostgreSQL save-first/delete-first races, checking no orphan/resurrection and unchanged unrelated/source facts. |
| Blind 7: browser expiry with dirty/pending bus untested | medium / patch | Parent expiry clears plan and child lock, but new bus-only states do not exercise that timer. Test unsaved and unresolved cases, cleared presentation/guards and ignored late replies. |
| Blind 8: receipt capacity excludes foreign/expired untested | medium / patch | Populated-cap test proves 429 but not scoped eligibility or exact receipt-row immutability. Add foreign/expired rows without prior cleanup, successful admission and full no-mutation comparison at the bound. |
| Blind 9: new routes absent from fictional denial probes | medium / patch | Verifier checks old plan routes only. Add physical-bus GET/POST and bus-operation lookup denial on the fictional API using an otherwise valid request origin. |
| Blind 10: accepted nonce reused on another own plan untested | medium / patch | Target binding is implemented but only changed content is tested. Verify target reuse conflicts and preserves both plans, bus revisions and original receipt. |
| Edge 1: U+0085 mismatch | medium / patch | Independently confirms Blind 1; shared normalization root cause. |
| Edge 2: definitive 429 lock | medium / patch | Independently confirms Blind 2; shared rejection-resolution root cause. |
| Edge 3: NUL accepted before PostgreSQL failure | medium / patch | The current string model permits NUL, which PostgreSQL cannot persist; UI would hold an uncorrectable uncertain attempt. Reject unrepresentable input before writes, with client feedback and no mutation. |
| Verification 1: bus-only outer leave guards untested | medium / patch | Pre-verified gap: removing busLocked from parent lock propagation leaves local close/delete tests passing while beforeunload/navigation/logout and draft replacement lose protection. Add otherwise-clean-draft dirty/pending cases, dismissed prompts, preserved proposals and guard release after cancellation/resolution. |
| Root final audit: initial confirm button during another plan's bus edit | refuted / retain lifecycle | Source reinspection shows begin clears the opened plan and reopen clears review; the proposed simultaneous-pane state was unreachable. Keep the harmless defensive busLocked disabled condition, but preserve existing single-pane transitions. The replacement regression checks bus-edit transition blocking, cancellation, review of another plan, pending confirmation and its independent bus snapshot. A temporary patch removed pane clearing to construct the original test; root caught and requested reversal before broad verification because it would introduce mixed retention deadlines. |

## Design Notes

### Review patch reinspection — 2026-10-24

The same implementer applied the retained fix groups. Root read the affected normalization/storage/error-handling and regression changes. The original blind and edge reviewers independently re-inspected their retained claims and reported no concrete remaining defect; the verification reviewer confirmed that the two otherwise-clean bus-only outer-guard cases now detect removal of parent bus-lock propagation. These were read-only inspections, not executed-test claims. The low-impact UUID chronological-order proposal remains rejected; the extra root simultaneous-pane claim is refuted and its temporary lifecycle expansion is being reversed, as individually recorded above. Focused execution and root complete verification are recorded separately when finished; no retained finding is deferred and no human acceptance is implied.

Final lifecycle reinspection: the blind reviewer confirmed restored single-pane begin/reopen transitions and disabled plan reopening during pending confirmation. Plan A cannot remain mounted while B's confirmation is pending, so A's expiry cannot clear B through the shared deadline. The replacement regression covers these transitions and independent bus snapshots. The restoration's scoped production build and browser test passed; the complete root verifier is running on this restored source.

Medium persistence/API/UI change. Separate bus metadata preserves confirmation hashes/unknowns and retention. No remaining intent gaps. Migration/runtime upgrade only after implementation approval and disposable testing.

Use a separate `/workdays/{id}/physical-bus` resource and accepted-operation lookup; preserve exact immutable plan response keys. Guarded post-write reads must validate identity/current revision before claiming saved. An old accepted receipt must not overwrite a newer current bus. Missing operation lookup stays uncertain until retry/live-plan resolution. Parent plan-read generations and leave/deletion guards must include bus edits/pending writes; do not let a delayed plan response unmount unsaved bus input. Reuse existing Web Locks. Preserve the authorized E9 pagination/expiry changes and all local work. These are implementation refinements within the owner-approved scope, not new features.

Receipt admission is bounded at 2,000 unexpired accepted bus receipts per owner. Identical accepted retries remain available at that bound; expiry cleanup releases retained metadata. Rejected admission leaves current state unchanged. The bound and the existing operation-identity rules are covered by synthetic backend tests.

## Verification

Final root sequential run in progress on restored/reviewed source (`tmp/10-4-root-final.log`): **236 backend/API tests passed in 272.31s**, exact restart/migration bus/receipt/plan/source/decision/deadline equality passed, production bundle `index-FOJ_MQro.js` built. Five fully mocked verifier controls passed separately in 0.143s. The 157-case browser phase and final runtime preservation/availability checks remain pending at this entry.

Run `scripts/verify-private-drafts.py` with `COMPOSE_PROJECT_NAME=ibe160-private-tests`: new suites, full regressions, restart/migration equality, production build. Run restoration tests and `git diff --check`. Inspect Day/Night renders and browser-storage absence. Complete independent BMAD review layers, triage/fix/retest. Preserve ordinary data/account/secret, restore availability and prepare tested runtime/owner checks. No tests/runtime changes during planning.

## E10-A1–A3 maintenance follow-up — 2026-10-24

The approved draft-contracts bundle preserves the normalized original import baseline (including absence for manual drafts), shares fresh-write physical-bus semantics, and pins review policy to issued operations and confirmed plans. Missing deadhead/CAR trip numbers remain visible as unknown without a separate acknowledgement; passenger direction joins the draft unknown display. Historical acceptance above remains unchanged. See [the maintenance evidence](../../docs/evidence/epic-10-draft-contracts.md). Implementation checks and owner acceptance for this follow-up are tracked separately; E10-A1–A3 remain in-progress.

## Owner review amendment — 2026-10-24

The approved `spec-epic-10-review-feedback.md` adds explicit clear buttons beside draft and current bus inputs. Clear creates an unsaved empty proposal; save, cancel, retry, conflict and reopen retain existing semantics and fixed expiry. Fresh invalid saves are disabled/grey, with input and associated errors preserved; already pending retry identities remain available. Existing Unicode White_Space, 100-code-point/NUL rules, leading zeros (including 000x) and meaningful spaces are unchanged. Original story acceptance is historical; amendment owner acceptance remains pending.
