# Story 10.3 — Confirm the reviewed plan

Implementation, final verification and all three independent BMAD review layers are complete. Owner acceptance and publication remain pending. The approved [specification](../../_bmad-output/implementation-artifacts/spec-10-3-confirm-the-reviewed-plan.md) defines scope; confirmation never activates or completes work.

The additive private schema separates confirmed retention from disposable drafts. Review binds a server-issued operation to one saved revision. Confirmation requires resolved Oslo intervals, chronological starts, explicit unknown-type classifications and individual acknowledgements, and validates source/operation/plan/session deadlines at transactional acceptance. Snapshots retain the exact content, source facts/corrections, IDs and duty anchors. A retained source marker prevents a second snapshot even after the first plan expires. Accepted retries use the live plan, independent of source deletion/expiry.

The UI shows complete readable facts, fixed expiry, correction guidance and revision-bound decisions. Editing invalidates review; cancelling changes no saved work. Uncertain replies lock replacement/editing and preserve the original operation for lookup or identical retry. Minimal plan discovery uses owner-scoped 50-item pages. Reopening retains the snapshot state and deadline. Source/plan facts stay in browser memory and guarded no-store responses.

| Contract | Executed coverage |
| --- | --- |
| Exact manual/imported snapshot, CAR/duty anchors, overnight dates, nullable bus/places | `test_exact_snapshot_replay_decisions_and_independent_source_retention`, imported fixtures 1/8/9 regression |
| Missing date/activity/times, unordered starts, expired final end, missing/duplicate decisions | Direct invalid confirmation parameter matrix |
| Overlaps/gaps/zero transfers/latest end | Latest-end and separate-draft regression |
| Retry, changed decisions, one snapshot, stale revision/delete | Replay and concurrent-operation matrix |
| Atomic admission and fixed deadlines | 200 unused-operation cap; accepted/expired exclusion; controlled final-acceptance source/operation/plan expiry |
| Ownership/session/CSRF/origin/no-store/request bounds | Route matrix and blocked-row session expiry |
| Discovery beyond old limits | 201 live plans, five pages, every owned ID exactly once |
| Maximum decision envelope | 2,802 acknowledgements including unknown duty anchors, plus 200 classifications within bounded request |
| Lost/invalid response and changed identity | Browser invalid HTML/wrong snapshot/retry/lookup, suppressed broadcasts and delayed plan-list response |
| Day/Night, keyboard, wrapping, review/confirmed/reopen | Actual 768/1440px browser cases and story-labelled screenshots |
| Persistence | Sequential PostgreSQL/API restart, migration replay, exact snapshot/decisions/operation/deadline comparisons |

Intermediate verification run 1 passed 186 backend tests in 170.60s, restart/migration/state comparisons and the production build. Its earlier browser image exposed a future-deadline timer overflow and ambiguous nested status region; that browser run was stopped after reaching test 81/91. The verifier restored the operational private API and PostgreSQL, both verified healthy. Those failures were fixed before run 2. This intermediate run does not establish final verification of the subsequently expanded matrix.

Run 2 executed the full current product sequentially via `scripts/verify-private-drafts.py` with `COMPOSE_PROJECT_NAME=ibe160-private-tests`: **195 backend/API tests passed (164.31s)**, complete plan/operation-row and deadline comparisons passed across migration replay and PostgreSQL/API restart, and the production TypeScript/Vite build passed. The full browser run passed **90/92 (5.5m)**. Both remaining failures were new test assertions: one incorrectly expected a source-expired editor to become editable after accepted-plan recovery; one matched the initial sending message and removed response interception before the uncertain reply settled. Those assertions were corrected; no product code changed after run 2 began. The complete confirmation/identity files then passed **20/20 (1.3m)**, including both corrected cases. All 92 browser scenarios have passing evidence across these runs; no single clean 92-case run is claimed. Synthetic output is retained locally at `tmp/10-3-verification-run-2.log` and `tmp/10-3-browser-focused.log`. `git diff --check` passed, and generated prior-story screenshots were restored.

Independent review produced thirteen patch findings grouped into eleven fixes: unresolved-navigation protection, consistent supported classifications, refreshed discovery, early already-confirmed rejection, exact reopened classification keys, browser pagination, identical concurrent retries, post-purge source markers, imported source rendering, unknown duty acknowledgements and verifier-control fixtures. Two low-impact proposals were rejected with reasons in the spec; none deferred. Edge and verification reviewers re-inspected the affected patches and confirmed resolution. Targeted evidence: 40 backend tests, all 13 confirmation browser cases across a run and one source-date locator correction, and two mocked verifier tests passed.

Final root verification supersedes the intermediate totals: **207 backend/API tests passed (179.37s)**, full restart/migration/record/operation/decision/deadline comparisons passed, production TypeScript/Vite build passed, and **all 97 browser tests passed in one full run (5.2m)**. Synthetic log: `tmp/10-3-final-verification.log`. No product changes after this run. Root read the complete diff and patched code; all matrix rows have executed passing coverage. Generated prior-story screenshots were restored.

Inspected actual Day/Night review and confirmed renders at 768/1440px: Norwegian labels, long place names, explicit manual classification, readable accepted uncertainty labels and fixed deadlines wrap correctly without debug payloads/UUIDs. The four Day/Night width cases asserted keyboard focus and successful reopening. No actual-tablet or comprehensive accessibility qualification is claimed. No ordinary-account tests, private reset, publication or implementation commit/push has occurred.

After verification and review, the local private API was upgraded additively for owner walkthrough at **http://127.0.0.1:5173/private**. Read-only before/after hashes matched for existing accounts, drafts (excluding the new false-default marker), draft operations/deletions, sessions, security settings, throttle metadata and the secret. The original database container/volume remains; only migration `004_workdays.sql` was added. Operational API filesystem layers match the tested image. Frontend bundle, private health and unauthenticated workday denial passed. The initial bundle probe used unescaped Norwegian strings; matching route strings in the minified bundle corrected that probe without product changes. Disposable services are stopped. No owner-private rows or credentials were emitted or archived. Earlier runtime-pending statements are superseded.

Owner walkthrough after verification:

1. Reload the local private workspace and use your existing account. Save a corrected manual/imported draft; open **Gjennomgå lagret utkast**. Use valid activity dates whose final end + seven days is still in the future; old January examples require explicit corrections, while their source facts remain unchanged. Check revision, corrected/current/source facts, duty/CAR distinction, unknowns, latest activity end and expiry.
2. Cancel; check saved work is unchanged. Edit a field; check the old review disappears and save is required before reviewing again.
3. Leave an acknowledgement or unknown-type classification unset; confirmation must remain unavailable. Resolve blockers, acknowledge permitted unknowns and explicitly confirm.
4. Check the separate plan says **bekreftet**, retains facts/deadline, and shows no Start/outcome workflow. Refresh the plan list and reopen it.
5. Check 768/1440px Day/Night with keyboard focus, long place names and wrapped uncertainty labels. Lost-response and cross-account races are covered by synthetic tests; no ordinary private records need manipulation.

Historical import qualification limits and open Epic 9 retrospective actions remain unchanged. Bus workflows and the complete day overview remain stories 10.4 and 10.5.

Owner walkthrough feedback, 2026-10-22: Jonas reports steps 1–5 work as expected and requests a way to delete a confirmed plan with an explicit warning popup. The [deletion amendment](../../_bmad-output/implementation-artifacts/spec-10-3-delete-confirmed-plan.md) records that new requirement for approval. No deletion feature, new test result or final story acceptance is inferred. Existing code/runtime/private data are unchanged during this planning follow-up.

## Approved deletion amendment — implementation handoff

Jonas approved the amendment and requested continuing on 2026-10-22. The opened plan now offers **Slett bekreftet plan**, with a native confirmation popup: “Slette denne bekreftede planen? Dette kan ikke angres. Kildeutkastet beholdes.” Cancellation sends no deletion request. Explicit acceptance binds a stable operation to the selected plan ID and source revision. Owner serialization, session checks and live deadline predicates atomically insert a content-free receipt and delete the snapshot; accepted confirmation metadata cascades with it. The source and its confirmed marker remain, so a fresh plan requires a separate draft. Receipts expire at the original plan deadline and contain no plan facts.

The browser retains unresolved deletion identity through network/HTML/malformed or mismatched replies and unknown lookup results. It locks editing/replacement and warns on navigation. Only an exact matching acknowledgement clears the open snapshot and its summary. Deletion invalidates older list/read/confirmation generations. Receipt lookup and identical retry remain server-owned and use guarded no-store traffic. Synthetic teardown also removes receipts.

Focused implementation verification: three backend deletion cases passed (7.28s), including identical concurrent requests, owner/origin/CSRF/version/target denial, unchanged source/other records, receipt retention/cleanup, old confirmation rejection and atomic session/plan expiry rollback. Two mocked verifier restoration tests passed (0.126s). Production TypeScript/Vite build passed. The sequential verifier now compares deletion receipts and source markers across real restart/migration replay; execution of that expanded full verifier remains for the coordinator after independent review. Earlier 207/97 totals do not verify this amendment.

Browser deletion cases cover warning/cancel/accept/reload and keyboard focus at 768/1440px Day/Night; HTML (including HTTP 404), wrong JSON, lost and unsent replies; unchanged-operation retry/lookup; leave/replacement guards; delayed list/read replies and silent account changes before traffic/after acceptance. Actual result renders are saved as `10-3-deleted-{768,1440}-{day,night}.png`. The native popup text and acceptance/cancellation are asserted through Playwright dialog events; the result screenshots show the restored heading focus and wrapped guidance. No actual-tablet qualification is claimed.

Final focused browser run on the final rebuilt code: **13 passed (1.0m)**. The earlier harness iterations exposed a synthetic same-date selection ambiguity and intentionally bypassed mutation-lock orchestration; distinct labels/direct synthetic login make those race scenarios deterministic. The delayed identity case also motivated the guarded matching receipt read before accepting the mutation reply. Final source includes stale-error/finally generation guards. Exact synthetic output: system-temp `ibe160-deletion-browser.log` and `ibe160-deletion-backend.log`. Inspected 768 Night and 1440 Day result images; no clipping/debug facts. All amendment matrix rows have focused executed coverage; full regression/restart replay remains for coordinator.

Owner amendment walkthrough, after coordinator verification/runtime handoff:

1. Open a confirmed plan intended for deletion and select **Slett bekreftet plan**. Check the irreversible-action warning and source-preservation text; cancel. The open facts and plan list must remain unchanged.
2. Request deletion again and explicitly accept. Check the plan closes, its summary disappears and the source-preservation/new-draft guidance appears. Reload and check the plan remains absent, while its source draft and unrelated records remain available.
3. Check keyboard focus, cancellation and acceptance at 768/1440px in Day/Night. Synthetic tests cover lost replies and identity races; ordinary private records are never automated test targets.

Independent amendment review, final broad verification, controlled runtime handoff and Jonas's acceptance remain with the coordinator. No commit/push or story 10.4 work.

## Final deletion amendment verification and local handoff

All three independent BMAD review layers completed. Seven patch groups were fixed and the affected reviewers confirmed resolution; no finding deferred. Final root sequential run passed **213 backend/API tests (198.92s)**, real PostgreSQL/API restart/repeated migration state equality, production build and **all 120 browser tests in one run (7.6m)**. Two mocked restoration tests passed separately (0.094s). The full log is local ignored `tmp/10-3-deletion-final-verification.log`. These results supersede intermediate focused totals and pending-review/runtime notes above.

Root inspected all four deletion result renders. Popup text/cancel/accept are asserted through native dialog events; keyboard focus, wrapping, lost and invalid replies, receipt-read failures, expiry release, delayed traffic, pagination, missing source and silent account-switch behavior have passing execution evidence. No actual-tablet qualification is claimed.

The local walkthrough is ready at http://127.0.0.1:5173/private. Ordinary account/draft/plan/operation/deletion/session/security and secret hashes were unchanged before/after tests and upgrade. Only three expired login-throttle rows were removed by routine startup cleanup. The same database container remains, migration 005 is additive, tested/operational API layers match, and disposable services are stopped. Health, bundle and unauthenticated receipt denial passed without an ordinary-account test.

Reload the app, then use the three amendment walkthrough steps above: cancel first; explicitly delete only a plan you intend to remove; reload and check absence plus retained source/unrelated work. Previously confirmed source drafts require a separate new draft for a new plan. Implementation is complete; story 10.3 remains review pending Jonas's final acceptance. No commit/push or next-story work.

## Owner acceptance — 2026-10-22

Jonas confirms deletion walkthrough steps 1–4 work as expected and explicitly approves story 10.3. Original-flow steps 1–5 had already passed. Both the confirmation feature and deletion amendment are accepted; sprint 10.3 is done. Earlier owner-acceptance-pending notes are superseded. This records acceptance only; implementation and existing verification results are unchanged.
