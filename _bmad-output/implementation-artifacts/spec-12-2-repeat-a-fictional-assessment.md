---
title: '12.2 — Repeat a fictional assessment'
type: feature
created: 2026-10-26
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: 0bae54833f38dc3dbf041d54c324c220618c21da
story_key: 12-2-repeat-a-fictional-assessment
owner_acceptance: pending
integration_status: pending-12-1-contract
technical_status: independent-scope-verified
context:
  - C:/Users/Jonas/.codex/.chatgpt-projects/g-p-6ab6b4c1c6888191a96d3242fab912b4/story-12-2/_bmad-output/specs/spec-12-2-fictional-assessment/implementation-plan.md
---

<frozen-after-approval reason="Owner authorizes autonomous planning, implementation, testing and review; latest instruction defers final notice API verification until 12.1 contract stabilizes">

## Intent

Extend the limited fictional assessment into a repeatable, clearly simulated walkthrough of included import, draft, day, activity, notice, recovery and closure flows. Keep the real API/PostgreSQL assessment separately reachable and documented. Simulation cannot establish real database or private API success.

## Boundaries & Constraints

**Always:** Separate understandable screens; Norwegian UI; explicit manual Start, selection, outcomes and terminal confirmation. Unknown facts remain unknown. Distinguish unsaved proposals, unresolved replies and confirmed simulated storage. Reset/reload touches fictional in-memory state only. Use a demo-only entry/runtime without private credentials, authenticated calls, GPS, source fetching or browser persistence. Retain accepted Epic 11 semantics: selection never completes/starts work; closure preserves unknown outcomes; notices are account-wide with independent lifetimes.

**Never:** No edits outside this worktree, ordinary services/data, staging/commit/push/merge/deployment, imported unfinished branches, global environment/security changes or 12.1 expiry/deletion work. Do not run existing verification orchestrators that stop ordinary services. Real notice creation/retry/lost-reply verification remains explicitly pending stable 12.1 admission contract; implement independent simulations now without claiming API equivalence.

## I/O & Edge-Case Matrix

| Scenario | Input/state | Required result | Failure handling |
|---|---|---|---|
| Import | Fictional partial or unsupported sample | Source uncertainty remains explicit; unsupported offers manual entry | No file upload or private request; current saved work survives |
| Save | Edited fictional proposal | Explicit save receipt in demo adapter; reopening restores that snapshot | Unavailable retains proposal, never says saved |
| Conflict | Newer simulated revision | Show current versus proposed facts | No overwrite; explicit fresh adoption or cancellation |
| Lost response | Accepted simulated command, missing acknowledgement | Unresolved pending identity; lookup resolves original receipt | No second mutation/duplicate; failed lookup retains uncertainty |
| Notices | Missing start/source time; legacy missing ending | Unknown is labelled; legacy row excluded from active reader | Required ending before new save; no inferred source check |
| Activity/closure | Selected member, unregistered outcomes, end/abort | Explicit Start/outcomes; confirmation cancel; terminal read-only recap | No inferred completion or resume |
| Reset/isolation | Modified demo and unrelated browser sentinel | Confirmation resets only demo adapter, fixture and screen | No API/network/storage mutation or private fallback |

</frozen-after-approval>

## Code Map

- `frontend/src/main.tsx`: existing fictional API/PostgreSQL slice and `/private` dispatch; add `/demo` entry and link, retain old paths. Keep shared edits minimal.
- `frontend/src/FictionalAssessment.tsx`, `fictionalAssessmentModel.ts`, `fictional-assessment.css`: new separate screens and pure in-memory fixture/receipt adapter. Reuse existing visual tokens and literal independent examples rather than private controllers with auth dependencies.
- `backend/app/manage.py`, `storage.py`: existing fictional-only guarded reset; no product rewrite required. Verify actual reset against own isolated database.
- `frontend/tests/fictional-assessment.spec.ts`, task-specific Playwright config: network-denial, repeatability, normal/failure journeys and keyboard/layout tests.
- `compose.story122.yaml`, `scripts/verify-story122.py`: isolated synthetic real API/PostgreSQL verification; avoid existing service-stopping scripts.

## Tasks & Acceptance

**Execution:**
- [x] Implement demo adapter and separate import/editor/preparation/day/activity/notice/recap screens, explicit fault controls, cancellation and confirmed reset.
- [x] Add browser tests covering every matrix row, no fetch/private calls/persistent storage, deterministic repeated scenarios and narrow layout.
- [x] Add isolated real fullstack/reset verifier, build and executed evidence; keep simulated and actual results separate.
- [x] Document 12.1 contract dependency, retrospective routing, manual steps and review evidence; update only own sprint key/status.

**Acceptance Criteria:**
- Given no backend or login, when the assessor repeats included normal/failure flows and resets, then the labelled simulation works without GPS/live feeds and private access.
- Given own isolated API/PostgreSQL, when actual persistence/retry/reset checks run, then results are documented independently from simulation and ordinary data remains untouched.
- Given pending 12.1 notice admission, when reporting completion, then notice creation/retry/lost-response API integration is explicitly pending, never marked passed or owner accepted.

## Implementation Notes

No product questions remain for independent work. User authorizes continuing despite existing session-log changes and no commits. Boundaries apply to all delegated work. Root owns final review/log; implementation agent may implement/tests/docs but must not launch a nested Build, new agents or other stories. Use process-scoped writable tmp for uv/Python.

## Spec Change Log

## Review Triage Log
Root verified/classified every finding before grouping. User autonomy applies to bounded corrections; no product-intent change or external action is required.

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| B1 night comparison | medium / patch | Inherited pre background is light while demo-night section text is near-white; add themed pre styles and rendered comparison checks. |
| B2 night dialog focus | medium / patch | Native dialog stays white while night focus is pale yellow; theme native dialogs and test focused controls. |
| B3 hidden terminal fault | medium / patch | Fault control is hidden by terminal while independent notice save still consumes fault; keep it reachable for notice maintenance. |
| B4 manual fixture clarity | medium / patch | Manual action edits duty/bus but activities are fixed; explicitly label fixed sample scope instead of implying complete manual entry. Full activity authoring need not be duplicated. |
| B5 invoking focus | medium / patch | Cancellation focuses heading rather than actual Start/end/abort invoker; retain and restore invoking control, preserving exact screen/member. |
| B6 startup monitoring | medium / patch | Pageerror and request observers are installed after goto; monitor before navigation and permit only entry/build assets. Retain fetch/XHR/GPS counters and sentinel assertions. |
| B7 source identity | medium / patch | Manifests omit build/test/config inputs, relevant for uncommitted tree; hash backend tests/migrations/dependencies/Dockerfile and frontend package/config plus executed tests. |
| B8 reader empty/unavailable | medium / patch | Fixed all-line article makes empty/unavailable states unreachable; add controlled fictional reader states and distinct assertions without network fallback. |
| B9 neighbour boundaries | low / patch | Count and disabled buttons exist but explicit first/last and neighbouring labels are a direct clarity correction; add labels without changing selection semantics. |
| B10 legacy completion | low / reject | Missing-ending example is explicitly excluded and described as illustrative; no completed migration/legacy editing is claimed. 12.2 requires missing metadata and isolation, not every legacy maintenance operation. Adding a legacy completion record/command model is more than a direct correction; document this demonstration limit. Actual notice API verification remains pending 12.1. |
| E1 loopback | medium / patch | npm start inherits --host0.0.0.0; use explicit --host127.0.0.1 in task test/manual commands and verify configuration. No global host changes. |
| E2 malformed HTTP URL | medium / patch | Regex accepts https://# without hostname; validate URL parsing/protocol/hostname before simulated acknowledgement and test malformed HTTP form. |
| E3 repeated next-save fault | low / patch | Label says next save but state persists; consume selected fault once on valid save, retaining pending command/recovery. |
| E4 evidence collision | low / patch | Seconds-only timestamps can overwrite run JSON; use subsecond/random suffixes for both runners. |
| V1 saved outcome proof | medium / patch | Pre-verified gap: removing saved outcome mutation passes existing assertions; assert exact completed member in overview/recap and nonzero saved closure count. |
| V2 notice start proof | medium / patch | Pre-verified gap: every existing notice has empty start; assert future-start exclusion and equal/past-boundary inclusion for saved text. |

## Verification

Production TypeScript/Vite build; task-only Playwright browser gate; real PostgreSQL fixture/save/replay/restart/reset and private unauthenticated denial in unique Compose project. Record exit codes, failures, exact source/build identity, fresh captures and pending contract checks. Root independently reviews before handoff. No physical tablet qualification claimed.

## Final root verification — 2026-10-26

All retained findings were patched and reinspected by their original reviewers. Root production build and fourteen Edge cases passed in 12-2-frontend-20261026T220411706929Z-a5bf80782560.json. Actual eighteen-test/API/PostgreSQL evidence is retained separately; sixty-two running backend input files match worktree bytes, with no backend changes. All414 historical evidence hashes match. See [final handoff](../../docs/evidence/12-2-final-review.md) and [audit](../../docs/evidence/12-2-final-audit.json). Owner acceptance and actual12.1-dependent notice verification remain pending; user instruction overrides automatic done/commit workflow steps. No further story begins.
