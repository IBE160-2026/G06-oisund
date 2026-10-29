---
title: V1 D1 D2 D3 bounded remediation and qualification
type: bugfix
created: 2026-10-29
status: done
route: dispatch
review_loop_iteration: 0
baseline_commit: 6d1259628c5fc7cec2d649e4097331d1606d9574
owner_acceptance: accepted
context: []
---

**Owner decision:** Jonas explicitly accepted C1/local V1 with “Jeg godkjenner kandidaten og V1-grunnlaget” after all personal controls. Integration/closure authority below has been executed with passing final checks; Epic12/local V1 are complete. [Integration record](../../docs/evidence/v1-main-integration-20261029.md).

**Later continuation authority (29October):** Jonas requests completion through V1 closure. Server setup is separate bonus work, excluded from V1/prerequisites. After explicit C1 candidate approval and fulfilled actual criteria, main integration/checks/push, Epic12/V1 closure and safe deletion of the fully integrated follow-up branch are authorized without another merge question. Production operations, server move, release/tag, coursework and extensions remain excluded. The frozen implementation boundary below records the earlier authorization; this explicit later instruction supersedes its no-merge/no-closure restriction only under those conditions. [Current execution/owner record](../../docs/evidence/v1-acceptance-2026-10-29.md).

<frozen-after-approval reason="Explicit owner instruction authorizes implementation through review and branch publication; early UX direction confirmed separately">

## Intent

Resolve the named D1 defects, complete A7/A8 qualification and bounded B6–B10 maintenance before reconsidering V1 closure. Preserve historical c067fdb evidence; publish a new precise candidate, never infer acceptance. The owner explicitly keeps all these goals together and requests execution, overriding intermediate scope/plan approval pauses.

## Boundaries & Constraints

**Always:** Work only on `followup/v1-d1-d2-d3` in `D:/IBE160/tmp/v1-remediation`, from fresh main6d12596. Keep independent owner/session/expiry/revision/operation guards, original receipts, explicit manual actions and independent notice retention. Use synthetic data, controlled dates, new project/ports/volumes and payload-free evidence. Early E12-A2 direction confirmed: explicit abandon/confirm, known rejection versus unavailable read, authoritative UTC offsets. Actual product acceptance remains pending. Owner separately authorized starting Docker Desktop after being informed existing restart policies can resume containers.

**Never:** Merge main, close Epic12, deploy production, change production data/accounts/passwords/volumes/tunnel/Access/MFA, create tags/releases, submit coursework or start extensions. Do not present synthetic JWT/device controls as external Cloudflare observations. Do not blanket-rerun historical tests without relevant risk.

## I/O & Edge-Case Matrix

| Case | Expected result | Denial boundary |
|---|---|---|
| Known plan disappears with uncertain command | Fresh same-session authority checks permit explicit confirmed abandonment; navigation unlocks; no saved claim, resend or notice loss | Transient/HTML/malformed/auth failures do not qualify disappearance |
| Canonical selection/Start capacity rejection then failed current read | Known rejected attempt settles; proposal cancellable, current facts unavailable | HTML/wrong/incomplete error remains uncertain |
| Two Oslo02:30 folds | Distinct supplied UTC+02/+01 display; stored instants/receipts unchanged | Unknowns and historical offsets preserved |
| Cleanup fails then recovers | Fixed payload-free events and bounded cleanup status distinct from DB connectivity; hourly retry/startup semantics preserved | No SQL/exception/private text in events |
| Wrong-ID draft comparison | Requested identity/generation checked before display/adoption; proposal retained | No B facts or requests under A comparison |
| A7/A8 actual qualification | Independent synthetic source/lifetime examples and per-family fault/assertion/executed-result matrix | Missing/unexecuted work remains explicit |
| Gate/cache/proxy load | Fail-closed validation, bounded refresh/concurrency, minimized cookies, recovery without restart | No unbounded threads/queue or unverified token acceptance |

</frozen-after-approval>

## Code Map

- `frontend/src/PrivateConfirmation.tsx`: parent plan mount/child locks; abandonment belongs here, preserving independent notice controller. `useWorkdayResource.ts`, `PrivateActivitySelection.tsx`, `PrivateShiftStart.tsx`, `PrivateBus.tsx`: rejection/proposal and unavailable authority.
- `PrivateNotices.tsx`: source/validity offset display. `PrivateDrafts.tsx`: comparison identity and deletion recovery protocols. Reuse existing guards, no general rewrite.
- `backend/app/private_main.py`: scheduled cleanup/lifespan/health; introduce only bounded payload-free observable metadata, preserving connectivity contract.
- `scripts/prepare-tablet-files.ps1`, `deploy/tablet/access_gate/gate.py`, gate tests, nginx templates and proxy probes: preparation/admission parity and bounded JWT/cookie behavior. Existing verification uses UUID internal networks and synthetic services; new image tags only.
- Existing recovery/draft/confirmation/bus/selection/start/outcome/notice/crossday tests and `test_account_notices.py`/`test_retained_data.py`: reuse exact coverage and recorded results. `private-recovery.spec.ts:116` covers draft **creation**, correcting the earlier closeout's update description.
- `compose.story124.yaml`, qualified runner/copy infrastructure: adapt into separately named candidate namespace, frontend15326/fictional18329/private18330, never use retained story/submission environments.
- `docs/submission`, new evidence/report and `HANDOFF.md`: updated recipe, new candidate identity, honest per-item status and final grouped owner checklist.

## Tasks & Acceptance

- [x] D1 frontend/backend: add independent baseline regressions before patches; implement five bounded fixes with unchanged safety invariants.
- [x] A7 technical qualification: define literal synthetic SMS/noURL and long shared-link examples, selected/all-line scope, controlled two-day/original-day removal/expiry and legacy completion; link existing exact evidence and execute missing composite journey. Subjective owner acceptance remains pending.
- [x] A8: enumerate each mutation family and distinct issuance/receipt protocol, fault, assertion and executed result; add genuinely missing tests (including typed-looking deletion-lookup refusals if reproduced), preserve original failures.
- [x] D3: fix preparation parity before writes; implement measurable budgets below; qualify signed JWT errors, cookie/Origin/CSRF/cache/write timing in isolated probes; enumerate real-access blockers without altering live rules.
- [x] Implementation verification phase: install locked dependencies, record source/build/exit/hash, execute targeted red/green and relevant integrated regressions sequentially. Results: backend48, host25, preparation/proxy/API0, browser85/86 with corrected-expectation19/19 and remaining-deletion4/4; all original failures retained.
- [x] Document E12-A2 adopted practice (future runs not already executed), current decisions, candidate reproduction, exact point status and pending owner acceptance.
- [x] Independent review/reinspection and retained fixes; final preservation/source binding; immutable local source candidate `3c2287ed68d0cbb1923439fc6ee00254395072a4`. Associated documentation/evidence and separate session-log publication follow the explicit owner instruction, with actual push results recorded in the log. Build completion does not grant owner acceptance, merge, deployment or Epic12 closure.

**Acceptance criteria:** Given the named baseline defects, when independently specified regression expectations execute, then failures are retained and corrected candidate passes the same expectations. Given accepted or denied commands, when replies/lookup/current authority fail, then per-family original identity, no extra accepted write, honest state and owner/expiry gates hold. Given synthetic input/lifetime examples, when the complete journey executes, then independent facts and unknowns survive without dependence on a real-day wait. Given the new candidate, when the recipe is followed in its own isolated runtime, then actual API/PostgreSQL and browser evidence identifies exact tested source; prior evidence is not relabelled.

## Design Notes

D3 initial measurable envelope: team1–63 lowercase bounded rule and ASCII owner parity before file creation; four admission handlers, no unbounded waiting; one concurrent JWKS fetch and one attempt per5s window, verified key cache at most300s, remote deadline3s. A cached valid token during stalled refresh completes within500ms in isolated local probe; cold/unknown completes fail-closed within4s, overload within500ms. Exact cache/cooldown boundaries use fake monotonic time; actual synthetic HTTP establishes transport/concurrency. Rotation recovers after cooldown plus a successful fetch without restart. Upstream cookies allow only `private_session`/`private_csrf`; duplicate names fail closed. These are bounded single-user application budgets, not a general internet-scale service promise. Reconcile a measured environment/contract conflict explicitly rather than weakening assertions silently.

## Implementation Notes

No outstanding product-intent gap. Authorized irreversibles are follow-up branch publication and isolated synthetic mutations only. User permits all named goals in one run; specification length/scope splitting is not a reason to defer requested work. Root owns environment operations/review/log; implementers cannot operate production or spawn nested agents. Early UX confirmation and Docker-start approval are recorded in chat; neither is product acceptance.

Dispatch execution: root already activated and owns the rendered Build workflow at `D:/IBE160/_bmad/render/bmad-build/ibe160-fab92315c642/bd3f3f6671b7dbda68f8`. An implementation subagent is executing that workflow's Step3 handoff, not a new user Build invocation. Do not invoke another skill/bootstrap/workflow; implement directly from this specification and report to root. Root handles A7/A8 added tests/integration and environment; the implementer handles D1/D3 code and tests. Write D1 regression tests first and send root exact selectors, waiting for pristine red evidence before corresponding product patches. D3 independent red unit checks can run without runtime operations. Preserve outputs.

## Spec Change Log

## Review Triage Log

Three context-free required layers reviewed the unified baseline diff (including untracked evidence),2709064bytes. All layers reported before triage. Blind finding floor was10; evidence-hash volume is not ten independently proven defects. Each filed finding receives its own verdict below before grouping. `B`=blind, `E`=edge, `V`=verification-gap. Same model capability; no reviewer changed files.

| Finding | Verdict / route | Verified evidence and disposition |
|---|---|---|
| B1 lookup429 treated as dispatch rejection | high / patch P1 | `recoverOperation()` throws lookup errors directly while the caller's `lookup` argument remains false. The new429 branch can clear an accepted uncertain operation without a mutation rejection. Track actual dispatch refusal; qualify both resource protocols. |
| B2 rejected refresh loses cancellation | medium / patch P2 | Canonical refusal sets `unresolved=false`; `load()` clears saved on503; both components require `rejected && saved` for cancel. Preserve rejected saved/proposal state while hiding unavailable current facts. |
| B3 slow header monopolizes hard pool | medium / patch P3 | Per-read5s inactivity permits indefinitely repeated partial headers. The newly bounded four-handler pool exposes a recoverable-capacity obligation; add a small absolute header deadline and a real socket regression. No public route/policy change or external exploit claim. |
| B4 unsupported mobile/tablet modes | medium / patch P4 | Shared substitutions refer to nonexistent isolated Vite/Playwright tablet configs. Directly remove unqualified modes; no mobile execution is claimed. |
| B5 parent-link preflight after mkdir | medium / patch P5 | An exported preparer invoked on a redirected `frontend` can create `.v1followup-tests` outside lexical root before realpath refusal. Existing parent ancestry must be checked before mutation. |
| B6 interrupted generation ownership | medium / patch P5 | New collision refusal plus ownership manifest written last means a first-run interruption leaves intended generated files unowned on retry. Preflight-approved ownership must be atomically recorded before file writes; preserve unrelated files. |
| B7 serve skips runtime guard | medium / patch P4 | Browser/backend guard metadata but manual serve does not. Reuse the same guard before preview, keeping stop independent of API availability. |
| B8 abandonment coverage branches | medium / patch P6 | Selection/deleted-plan test exercises common parent path, but not server410, failed same-session check or second post-confirmation failure. Add bounded branch checks; invalidated session401 must still clear private presentation. Representative other child locks qualify aggregate parent wiring without claiming every combination. |
| B9 cleanup tests allegedly leave failed state | false / reject | Read all four test endings: hourly second tick succeeds; event test succeeds; counter test restores cleanup and runs it; health-separation test does likewise. Every successful test leaves statusok/counter0. The filed assertion that one leaves failed is false; reordered successful cases do not expose the claimed counter assumption. |
| B10 immutable binding not yet recorded | false / reject as current defect | The work/ledger explicitly says in-progress/in-review, binding/publication pending and owner acceptance pending. No completed publication is claimed. Final binding remains an authorized workflow deliverable and will be completed before publication, not silently omitted or graded as already done. |
| E1 rejected refresh loses cancellation | medium / patch P2 | Independently filed same causal state transition asB2; verified against catch and both rendering guards. |
| E2 lookup429 provenance | high / patch P1 | Independently filed same lookup/dispatch ambiguity asB1; matching receipt identity must remain reachable with zero resend. |
| V1 successful refresh coverage gap | medium / patch P2 | Pre-verified gap: immediate-cancel tests would pass if `|| rejected` preservation were removed. Add successful explicit refresh and verify proposal/guard survive until explicit cancellation/retry. |
| V2 second post-confirmation safeguard gap | medium / patch P6 | Pre-verified gap: current accepted-confirmation test gets identical absence/session outcomes twice. Force second-check failure and preserve original intent. |
| V3 repeated failure clears saved | medium / patch P2 | Same verified defect asB2/E1; preserves distinct filed provenance, grouped only after verdict. |
| Root P3 timer turnover resource bound | medium / patch P3 | A cancelled Timer can outlive a finished handler briefly. Cancel and join before slot release; focused actual ten-request resource regression and final host gate pass. This is root post-patch inspection, not an additional independent-reviewer finding. |

P1–P6 are retained small corrections to demonstrated state/ownership/capacity boundaries, without adding public APIs or changing accepted intent. The original implementation agent is re-engaged with the exact Step4 patch instruction. No finding is approved for deferral. Patches require focused checks followed by root affected qualification; final outcomes will be appended here. Candidate identity/publication and subjective/external limits remain separate.

Patch inspection: actual mutation-refusal flag gates429 and409; failed loads retain rejected intent but explicitly revoke current-fact availability.17D1 cases now assert repeated failed/successful refresh, typed-looking lookup409/429 after accepted writes, second-read/session503/401 and server410 with bus/start/outcome locks. Four bounded daemon header timers enforce a3s absolute request-line/header deadline; actual four-client trickle test recovers all slots without fixture release/restart. Unsupported tablet modes removed; serve uses existing runtime guard; stop remains independent. Parent ancestry checks precede mkdir, and preflight-approved ownership is atomically reserved before generated writes. Root read the patches and focused tests. Independent verification reviewer re-read the frontend patch/tests and confirmed closure of all its filed findings, without edits or runtime operations. Root review-host30passed and review-preparer3passed; final browser/image qualification pending below. No retained finding deferred.

## Verification

Later explicit metadata exception: a separate session had mistakenly marked Epic12 done on main. Jonas clarified that only12.5 was to be marked done, then explicitly authorized only the prepared eight-file tracking correction to main. Published metadata26b9e25 plus separate log6f641d7 restore Epic12 in-progress, preserve12.5/retrospective done and all action items, and have zero product/test/tooling/deployment diff. This does not merge or accept candidate3c2287e. The original checkout's concurrent Ubuntu setup work was preserved by using another worktree. Actual scope/push proof is in the qualification ledger.

Final outcome: host31/31, finalD1/D2 browser23/23, actual final-r1 proxy exit0, final guarded manual preview exit0. The preceding affected73-case run retains72passes plus one ambiguous bus test selector failure; it stopped before dispatch, was corrected to textbox role and passes in23/23. No frontend product source changed after that72/73 run.229 actually captured inputs bind to the immutable candidate commit; actual API/gate/proxy image bytes and every served static asset match the recorded source/build. Other12worktrees/35containers/16volumes and1519historical evidence files are preserved (120text files differ from main only by initialCRLF checkout representation). All retained findings resolved, none deferred. Source/evidence details and pending grouped owner checks are in `docs/submission/v1-followup-qualification.md`; owner_acceptance stays pending and Epic12 stays in-progress.

Use targeted frontend/browser, backend/cleanup, gate/PowerShell/proxy checks plus affected fullstack journeys, recording actual commands, literal expectations, failures, source/build and preservation. Security probe results must separate isolated signed fixtures from genuine Cloudflare/MFA/device access. Subjective owner checks are grouped before final acceptance; unavailable external checks remain open.

Implementation-phase matrix audit: missing-plan, canonical refusal, two folds and wrong-ID rows all execute in final19/19 (20261029T162628095551Z-e4669ac5); cleanup row executes in host25/25 and backend48/48; A7/A8 executes in19/19 plus exact historical family mapping and legacy backend case; gate/cache/proxy row executes in host25/25 and actual proxy/API exit0. Captured sources/builds and unchanged-input checks are in the linked qualification ledger. The sole85/86 failure was an obsolete exact display label; the independently specified1894+00:43 expectation passes in19/19. Subsequent adapter-only preview work addresses missing Windows TCP PID metadata; no product source changed. Owner usability and genuine external access observations are not marked passed.
