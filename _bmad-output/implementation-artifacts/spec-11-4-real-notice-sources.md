---
title: '11.4 — Record real traffic notices from the web or SMS'
type: bugfix
created: 2026-10-25
status: done
owner_acceptance: accepted
accepted_on: 2026-10-25
route: dispatch
baseline_commit: cdcf2816b86772e559f33ded5807e8cb5a4473bc
story: '11.4'
story_key: 11-4-maintain-a-planned-notice
---

<frozen-after-approval reason="Standing implementation authorization and explicit owner SMS/text/all-lines directions on 2026-10-25; do not request repeat permission">

## Intent

The owner cannot record useful real traffic notices. The earlier validation-copy fix was insufficient. Isolated Edge inspection of Svipper's rendered widget and four expanded notices confirms place-based entries, long route headings, operational time windows, expandable instructions and no individual links in the inspected entries. The owner requires SMS sources without URLs, title/short/detailed explanations, and an explicit all-lines choice.

Provide a required title, optional short explanation and multiline detailed explanation, optional source description, optional HTTP(S) link, and required line scope: specific explicitly entered lines or “Alle linjer”. Never infer all-lines from empty input. Preserve complete operational wording without forcing it into tags or invented dates. Optional timestamps remain unknown when empty.

## Boundaries & Constraints

Always preserve records, immutable receipts, metadata, expiry, account isolation, revision conflicts, original-command recovery, separate screens, activity selection and raw unsaved proposals. Source check and manual ending remain separate explicit actions. All-lines is a recorded user choice. Existing notices default to specific-line scope and retain titles/tags.

No automatic web/SMS import, sending, GPS or filtering; relevance remains 11.5. Do not rewrite migration 011, historical receipts or old approved intent. Stop before staging, commit, push or next story. Tests use disposable synthetic accounts; preserve ordinary data/services.

## I/O & Edge-Case Matrix

| Scenario | Required behavior |
|---|---|
| SMS, no URL | Save title/text/source description and chosen scope without a fake URL. |
| Specific lines | Require an explicit tag; preserve copied route headings up to 300 characters each. No silent number extraction. |
| All lines | Save explicit all-line scope without tags; display “Alle linjer”. Toggling retains the in-memory specific-line proposal but sends only chosen scope. |
| Empty specific lines | Explain missing lines and offer all-lines; never silently convert scope. |
| Shared web overview | Accept Svipper overview URL without demanding an individual link; validate nonempty URLs. |
| Detailed/time-window text | Preserve multiline instructions; never invent continuous structured validity from separate windows. |
| Old receipts/lost reply/stale edit | Preserve identity/results, recover one accepted effect and retain comparison proposals. |

</frozen-after-approval>

## Code Map

- frontend/src/PrivateNotices.tsx: content/receipt validation, equivalence, pending commands, editor and saved facts; retain reconciliation/navigation.
- backend/app/workday_notice_domain.py and workday_notice_storage.py: fields/serializers, SQL/fingerprints; retain authorization/lifecycle.
- backend/migrations/private/011_manual_notices.sql: deployed required-URL/nonempty-line constraints; use a new migration.
- backend/tests/test_private_notices.py and frontend/tests/private-notices.spec.ts: existing synthetic fixtures/failure coverage.
- scripts/verify-private-drafts.py: disposable migration/restart and preservation checks.

## Tasks & Acceptance

**Execution:**

- [x] New migration/domain/storage: nullable summary (1000 characters), description (5000, multiline), source_note (500), nullable source_url, line_scope (selected/all; old rows selected). Empty tags only for all-lines; retain 50-tag bound, raise per-tag bound to 300. Preserve old operation fingerprints/results and same-command retry without receipt rewriting.
- [x] Editor: title, short explanation, detailed textarea, source description, optional link and explicit scope selector. Retain specific-line input across toggles/navigation. Render complete saved text/source/scope. Exact field/CSV/clock errors beside fields and saving; blank optional strings become null without discarding raw proposals.
- [x] Tests: SMS/no URL, overview, selected/all, long heading, missing tags, multiline text, toggle/navigation/reload, old receipts and uncertain writes. Recheck manual actions, terminal state, ownership/expiry and metadata. Verify migration/restart and preserved old rows.
- [x] Update active specification/plan/context/logs to supersede URL-only rules and record actual results. Preserve historical evidence and pending owner acceptance.

**Acceptance Criteria:**

- Given SMS/web text, when saved/reopened, then title, short/deep explanations, source and scope survive without mandatory URL.
- Given scope changes/navigation, when returning, then text and specific-line proposal survive; all-lines is never inferred.
- Given old notices/receipts, when upgraded and retried/looked up, then business content and accepted-effect identity remain compatible.
- Given invalid fields/blocked lifecycle, when saving, then the exact cause is visible and input remains available.

## Implementation Notes

Initial planning checkpoint: no product code, migration or ordinary data had changed yet. Dirty tree was the authorized uncommitted 11.4 baseline. Exact owner line input remains unknown: do not claim reproduction of that specific rejection. Independently observed source mismatches and explicit new requirements justify correction; executed implementation/results follow below.

Route: product choices are settled; schema migration and cross-layer receipt compatibility require dispatch. Standing owner implementation authorization plus explicit SMS/text/all-lines directions authorize this correction; the concrete contract was summarized before dispatch without asking repeat permission. The earlier optional/unknown-line proposal is superseded by explicit selected/all scope.

Parent owns the BMAD workflow, review and canonical memlog; do not invoke another Build workflow or edit the memlog. Coordinate before changing shared services. Ordinary owner data must never be test targets; the parent captures a fresh baseline before dispatch. Existing tmp/11-4-feedback-preservation.py and tmp/11-4-check-served.py illustrate read-only preservation/served checks; never overwrite an old baseline. Current ordinary project is ibe160-private-work; disposable tests use ibe160-private-tests (API port 8001). Frontend is ibe160-fictional-assessment on port 5173. Existing notice fixtures enforce synthetic account selection. Do not stage/commit/push even if generic workflow defaults suggest it. Preserve existing evidence before any test overwrites it; use new evidence filenames.

## Verification

TypeScript/Vite build, meaningful notice API/PostgreSQL/browser regressions, old-receipt retry/lookup, repeated migration/restart and ordinary-data preservation. Inspect both themes/narrow editor and saved views. Restore ordinary services; verify served assets. State untested hardware limitations.

Source: [Svipper traffic messages](https://svipper.no/meny/reise/trafikkmeldinger/trafikkmeldinger/), rendered widget and four expanded entries inspected 2026-10-25. Plain text fetch misses the widget. Scratch evidence: tmp/11-4-svipper-expanded.log and tmp/11-4-svipper-site.png.

## Review Triage Log

All three required layers ran; none skipped. The two instructed reviewers initially hit the known generated-snapshot read restriction, then successfully retried using authorized read-only escalation. Edge-case review returned no findings. Scoped diff uses the captured authorized dirty-source baseline, rather than re-reviewing the earlier 11.4 delivery; full canonical Git HEAD remains recorded above. No index staging.

| ID | Verdict / route | Evidence and resolution |
|---|---|---|
| Blind 1 | low / patch | Field error paragraphs exist but inputs lack aria-invalid/describedby, so focused controls do not expose their reason programmatically. Add direct associations. |
| Blind 2 | low / patch | Client plain/multiline allow lone UTF-16 surrogates rejected as Cs by the backend. Align the existing character check, retaining valid astral text. |
| Blind 3 | low / patch | The first intro paragraph still directs event text only into title and lines into the tag input. Update it to match short/deep text and explicit all-line choice. |
| Blind 4 | medium / patch | Legacy replay test proves identity compatibility but lacks a reused-operation rejection assertion for changed new nondefault fields/scope. Add targeted conflict/no-second-effect coverage. |
| Blind 5 | medium / patch | SMS content persists through create/edit/replay, but separate check/end assertions do not compare every new content field. Extend the API regression. |
| Blind 6 | medium / patch | Existing browser conflict compares a changed title, leaving new text/source/scope presentation without direct assertions. Extend the same comparison flow. |
| Blind 7 | low / patch | Enlarged Day/Night tests measure the new control but leave its text blank; exercise maximum new text bounds in those existing cases. |
| Blind 8 | low / patch | Canonical SPEC, plan override, epic/story acceptance and README already superseded the old requirement, but older active-plan paragraphs and the cache lead still repeated it. Root updated those active summaries and added a correction pointer outside the old execution spec's frozen block. Preserve the explicitly historical original contract/test gates rather than rewriting approved history. |
| Verification 1 | medium / patch | Pre-verified regression gap: removing the three new NoticeFacts paragraphs would preserve API/editor assertions. Add visible saved summary/source and full multiline description assertions, including textContent and pre-wrap style. |
| Root 1 | low / patch | The textarea-inclusive measurement selected a visible but intentionally disabled textarea in the unavailable state; six layout cases failed to focus it while both editable SMS cases passed. Select the textarea only when visible and enabled, otherwise use reachable Back; keep disabled control layout/contrast measurements. |

Patch findings were checked against callers/tests and sent together to the original implementation agent. No intent gap or new public surface is needed; the changes directly correct markup/copy/character validation or add assertions for already implemented behavior. No deferral.



## Final correction verification — 2026-10-25

Root re-inspected the patched source, tests and rendering. All ten retained review/root findings are fixed; none deferred. Final source remains unchanged through verification/rollout: 95 source/test/migration SHA-256 values match. Actual final full notice runs: **61 API/PostgreSQL tests passed in 82.55s** (`tmp/11-4-real-root-current-api.log`) and **49 browser tests passed in 4.1m** (`tmp/11-4-real-root-final-browser.log`). Production TypeScript/Vite build passed. Earlier failed label/measurement runs remain recorded rather than presented as final successes. Root first found a stale container copy of the test file (55 tests); copied the current file and reran the entire current 61-case suite. All 41 runtime backend/migration files equal current workspace content.

Matrix audit: SMS/all scope/text uses API `test_sms_explicit_scope_multiline_and_new_limits` and both Day/Night SMS browser cases; copied selected headings/overview/limits use that API test plus quoted-CSV browser edit; empty selected scope uses API rejection and SMS/associated-error tests; multiline consultation uses `textFacts` visibility/textContent/pre-wrap assertions; legacy compatibility uses the legacy fingerprint test, populated 011→012 upgrade test and dedicated repeated-migration/database/API restart check; lost SMS responses use lookup/retry browser cases, and richer stale comparison shows all new facts. All covering cases ran in the final complete suites.

Restart/repeated migrations preserve exact SMS/legacy rows, metadata, immutable receipt payloads/hashes and accepted retry/lookup. Seven verifier control-flow tests pass. Final 24 measured enlarged states cover 486 controls: text min 6.126:1, boundary min 4.391:1, focus min 11.450:1/3px, controls min 77.56px, no overflow or obscured focus. New textarea is included. Day/Night 390px SMS editor/saved states also pass; root visually inspected final narrow editor and saved multiline source facts. Physical iPad/Safari, touch/assistive-tech and browser chrome zoom remain untested existing follow-up obligations.

Ordinary local migration 012 is applied and services healthy. Projected read-only preservation proves every original business/account/session/security/notice/receipt field and the original secret/database identity unchanged: only migration 012 and nullable/default-selected columns were added. No ordinary account was a test target. All 226 pre-existing render/measurement files match baseline byte-for-byte; new real-source artifacts remain. Synthetic services are stopped. Served HTML/assets match tested dist: index-CpzA4ip2.js and index-8lnBnkIq.css. Git HEAD/index unchanged; no staging, commit, push or next story. Overall 11.4 remains review pending owner acceptance.

## Owner acceptance and publication authorization — 2026-10-25

Jonas explicitly approved the corrected story 11.4 delivery, then instructed commit and push. Owner acceptance is accepted and story/sprint status is done. The technical final gate remains 61 API/PostgreSQL and 49 browser passes with verified migration/restart/data preservation. Earlier pending-acceptance and stop-before-publication statements are historical and superseded by these owner messages. Record the accepted work in Git and push to origin/main; do not start 11.5 or any other story.
