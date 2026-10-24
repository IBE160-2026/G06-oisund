---
title: '10.5 — Read the day'
type: feature
created: 2026-10-24
status: done
approved_on: 2026-10-24
owner_acceptance: accepted
accepted_on: 2026-10-24
implementation_status: complete
route: dispatch
epic: 10
story: '10.5'
alias: V1-09
story_key: 10-5-read-the-day
baseline_commit: 3a101981775dba203c59bcc64979dbab9f3ce53d
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
  - D:/IBE160/Eksempelfiler/README.md
---

<frozen-after-approval reason="human-owned intent — changes require human approval">

## Intent

**Problem:** Confirmed plans show detailed facts, but lack a readable day overview.

**Approach:** One chronological list after confirmation/reopening, alongside the existing bus editor. SCOPE-02/V1-09, FR-4/5, AC-02 govern; AC-03 navigation belongs to Epic 11.

## Boundaries & Constraints

**Always:** Show service date, Europe/Oslo calendar dates/times, planned final end and fixed expiry. Prominent `Oppmøte` uses confirmed Sign-on facts; retain subsequent reporting points. If absent, say unknown; an available source header start is separately labelled source information. Header end never replaces confirmed final end. Show type, line/trip/direction, known endpoints, effective duty/full suffix (`006`, `090`) and visible unknown/uncertainty labels. Source/correction details remain expandable. Preserve confirmed order and stable IDs, including equal starts and zero-duration activities.

Keep current physical bus separate from snapshot bus and activities/duties. CAR/duty changes never establish bus changes. Preserve explicit transfer/bus-change classification/raw text; current bus edits create no history. Missing places never inherit depots.

**Never:** Add Start/activation, selectable/current activity, previous/next, outcomes, closure, notices, GPS, offline support, parser expansion or general refactoring. Preserve account/session binding, suspension, generation/expiry guards, bus concurrency/retry/leave protection and no-store. No private browser persistence or payload logs; use synthetic tests only.

## I/O & Edge-Case Matrix

| Input/state | Presentation | Guard |
|---|---|---|
| Corrected confirmed plan | Current confirmed facts/classifications | Original metadata cannot override corrections |
| Consecutive touching pauses | MealBreak wins; otherwise Split break, Coffee-only, then paid meal | Derive anew; retain member IDs/details; do not hide duty boundaries |
| Gap/overlap | Neutral unclassified interval/overlap note | Gap starts after greatest preceding end; never invent work/pay/transfer |
| Overnight/separate parts | Explicit dates and known reporting points | No clock-based date guessing |
| Denied/suspended/expired/deleted | Existing hidden/cleared presentation and recovery | Late responses cannot restore facts |

</frozen-after-approval>

## Code Map

- `frontend/src/PrivateConfirmation.tsx`: validated Plan, `planAvailable`, `planOpen`, expiry and parent locks; retain review `Facts`, move confirmed detail behind disclosure.
- `frontend/src/PrivateBus.tsx`, `PrivateAccess.tsx`: reuse current bus and guarded requests unchanged.
- `frontend/src/draftInterpretation.ts`: reuse `effectiveDuty`, `dutySuffix`, correction/provenance helpers. `backend/app/pdf_import.py:175` supplies pause rules; metadata pause_groups is historical.
- `backend/app/workday_domain.py`, `workday_storage.py`, `draft_domain.py`: existing snapshot, classifications, source facts and fixed retention suffice. No schema, API or migration expected.

## Tasks & Acceptance

**Execution:**
- [x] New `frontend/src/dayOverview.ts`: pure immutable projection for grouping, gaps and reporting; preserve source/member identity.
- [x] New `frontend/src/PrivateDayOverview.tsx`; `PrivateConfirmation.tsx`, `style.css`: integrate readable list under existing availability gate; scoped Day/Night styles, wrapped names and accessible disclosures. Keep one bus editor and existing lifecycle.
- [x] `frontend/src/PrivateImport.tsx`: contextual historical-source heading for confirmed detail, preserving unconfirmed review wording.
- [x] New `frontend/tests/private-day.spec.ts`: table-driven projection and real synthetic save/confirm/reopen/browser checks; extend `private-identity.spec.ts` for new presentation guard assertions.
- [x] `Docs/evidence/10-5-day-overview.md`, `Docs/development-log.md`, `README.md`, sprint status: actual evidence and owner walkthrough after authorized implementation.

**Acceptance Criteria:**
- Given corrected saved activities, when confirmed/reopened, then order, reporting, types, places and dates match independent expected facts; viewing changes no record/deadline.
- Given examples 2/7, when displayed, then matpause is 12:01–12:43 / 08:52–09:28 with both member rows accessible; separated/non-touching pauses remain separate.
- Given examples 1/4–9 and synthetic overlaps/repeated turn numbers, when read, then split parts, midnight, `006`/`090`, assisted facts, CAR and non-driving work retain distinct meaning without invented work, bus history or completion.
- Given two windows, bus edits or access/deletion/expiry races, when reading/reopening, then existing isolation, conflict, uncertain-retry and clearing protections still hold.
- Given iPad-sized portrait/landscape and PC, when using both themes, keyboard and enlarged text, then dates, long places, warnings and controls remain readable without clipping or color-only meaning.

## Implementation Notes

- Owner acceptance/publication, 2026-10-24: Jonas explicitly states "Jeg godkjenner. Commit og push. Ingen retrospektiv." Story/specification are accepted and done; publication is authorized. Actual iPad/Safari testing remains not run, as Jonas previously reported the device was unavailable. Do not infer individual manual scenarios or tablet acceptance from this approval. Earlier pending/no-publication notes are historical and superseded for this accepted delivery; the no-retrospective instruction remains. Product code and recorded final verification are unchanged.

- Final root gate on reviewed/patched code: **236 backend/API tests (264.58s)**, exact PostgreSQL/API restart/migration/session/plan/bus/receipt/source/deadline equality, production build and **all 190 browser tests in one run (11.1m)** passed, exit 0. Log: ignored `tmp/10-5-root-final.log`. Five mocked restoration controls passed (0.133s); one additional unchanged-code JSON-report contrast case passed to retain actual measured values. No product code changed afterward. All matrix rows retain executed coverage, including new historical warnings, classification/correction disclosures, returning duty boundaries and malformed source clocks.
- Operational API/database are healthy; disposable services stopped. Existing account/draft/plan/bus/operation/session/security/secret digests equal baseline, except three expired login-throttle rows removed by unchanged startup cleanup. Original database container retained; app returns 200 and serves tested `index-DgqOD_AO.js` / `index-DQsFmhCi.css`. Historical screenshot churn restored; new synthetic day/full-plan evidence retained. Actual iPad/Safari and owner acceptance remain pending. The owner's explicit instruction overrides generic step-05 done/commit actions: specification stays in-review, sprint stays review, no staging/commit/push/retrospective.

- Review corrections: all three original reviewers re-inspected their retained findings against the patched diff/source/tests and confirmed resolution without a remaining concrete defect. Nine patch groups resolved all retained rows; no finding deferred. Scoped checks passed 35/35 (1.3m), followed by all six strengthened enlarged-control combinations (four passed initially; two landscape reruns passed after explicit scroll centering/1px measurement tolerance, 16.2s). This was a test measurement correction; product assets remained `index-DgqOD_AO.js` / `index-DQsFmhCi.css`. Final root complete verifier follows; the earlier 236/184 pass is pre-review evidence, not the final patched pass.

- Root pre-review gate passed: 236 backend/API tests (275.46s), exact restart/migration/plan/bus/session/deadline equality, production build and all 184 browser tests in one run (10.8m), exit 0. Five fully mocked verifier controls passed (0.133s). Log: ignored `tmp/10-5-root-combined.log`. Root read the complete tracked/untracked diff without staging and inspected Day/Night/enlarged renders. Matrix audit: corrected facts/classifications and source separation covered by day/confirmation cases; pause rules/member IDs by 19 projection cases and browser disclosures; greatest-end gaps/overlaps by projection; overnight/separate reporting by nine-example projection/browser matrix; denial/deletion/suspension/expiry/late replies by bus, identity and confirmation regressions. Every matrix row has executed passing coverage. Existing data fingerprints match except three expired login_limits rows removed by unchanged startup cleanup; no account/plan/bus/session/secret changes. Independent review follows.

- 2026-10-24: Jonas approved this specification and authorized implementation, tests, independent BMAD reviews and routine fixes through manual-review handoff. Preserve existing data/services; no commit, push or retrospective. Sprint must remain review pending final owner acceptance. Re-read approved file from disk; frozen intent unchanged. Initial Git contains only the authorized preparation spec/log at the recorded baseline.
- Coordination: implementer may run isolated synthetic verification sequentially and must restore affected services before handback. Do not upgrade the operational API or use ordinary accounts/data for tests. Root owns independent reviews, final combined verification and any final serving of verified assets. Read-only operational table/secret fingerprints were captured in ignored `tmp/10-5-operational-baseline.json`; preserve them for comparison. Do not stage, commit or push. Document exact executed evidence and incomplete checks; do not claim actual iPad hardware testing.

## Spec Change Log

## Review Triage Log

All three independent layers completed before triage. Thirteen individual findings are recorded below; nine retained patch groups follow. No intent change or public contract expansion is required.

| Finding | Verdict / route | Evidence and disposition |
|---|---|---|
| Blind 1: null confirmed service date | false / reject | `validPlan` explicitly requires draft.service_date, and backend assessment blocks confirmation without it. An acknowledged unknown service date cannot reach this component. |
| Blind 2: A → B → A duty summary | medium / patch | Global Set deduplication hides the return transition in a valid touching pause group. Retain consecutive transitions with member start times; test visible sequence. |
| Blind 3: single paid-meal subtype disappears | low / patch | A manual single Paid meal before/after row with no raw code becomes generic Betalt matpause. Directly retain its specific single-row label; test both types. |
| Blind 4: source uncertainty hidden | medium / patch | New primary list shows activity uncertainty but source-level unresolved issues/annotations remain in collapsed historical detail. Reuse existing importIssues; label them as original-source uncertainty, attach known matches to visible rows and show unmatched issues globally, without undoing corrections/classification. |
| Blind 5: three-digit CAR suffix | low / reject | Accepted pilot-car codes are CAR - 1 through CAR - 4; all retain null suffix through the reused rule. CAR - 100 is outside that recognized envelope and not produced by supported fixtures. Expanding CAR-prefix classification/guards for an unusual manual identifier adds a branch beyond the qualified cases; ordinary accepted CAR handling is unchanged. |
| Blind 6: list semantics with list-style none | medium / patch | New primary list removes markers and has no explicit role. WebKit documents this accessibility heuristic; add role=list and an accessible-structure assertion. Actual Safari/VoiceOver remains untested. Primary evidence: [WebKit 170179](https://bugs.webkit.org/show_bug.cgi?id=170179). |
| Blind 7: rendered classification gap | medium / patch | Helper classification is tested, but browser day seeds use empty decisions and the instructor test checks storage only. Assert original/confirmed classification in the day immediately and after reopen. Shares fix with Gap 2. |
| Blind 8: example semantic expectations incomplete | medium / patch | Member-equality tests do not independently check all duty boundary positions; only selected suffixes/labels are asserted. Add explicit known duty transitions and independently chosen gap/label expectations from the fasit; keep existing preservation checks. |
| Blind 9: enlarged combined plan coverage | low / patch | Whole-document overflow and post-enlargement close already run, but screenshots cover only the new list and do not assert bus/disclosure/control bounds at 200%. Add direct combined-plan visibility/bounds checks and synthetic full-plan evidence. |
| Edge 1: malformed source header instant | medium / patch | Existing metadata schema allows nullable bounded strings, while the new no-Sign-on branch sends nonempty header.start_instant directly to Intl. A valid-shaped retained plan can throw RangeError. Check parseability and fall back to labelled raw source start; test a real saved malformed-source-header plan without changing authoritative activity dates. |
| Edge 2: returning duty boundary lost | medium / patch | Independently confirms Blind 2: Set removes a later repeated duty although member details retain it. Same defect/fix; retain this individual disposition. |
| Gap 1: activity correction disclosure | medium / patch | Pre-verified: new browser seeds have no matching original activity IDs, and the imported correction regression opens only the separate historical Facts view. Extend it to open the new row disclosure and assert original/current values plus correction marker. |
| Gap 2: classification integration | medium / patch | Pre-verified: replacing classifications prop with an empty map would pass the current browser assertions. Extend real confirmation/reopen assertions, sharing Blind 7's fix. |

## Verification

Run focused Playwright checks, then `$env:COMPOSE_PROJECT_NAME='ibe160-private-tests'`; `uv run --no-project python scripts/verify-private-drafts.py`: PostgreSQL/API regressions, restart/migration equality, build and all browser suites. Run `uv run --no-project python scripts/test_verify_private_drafts.py` and `git diff --check`. Preserve operational restoration and historical screenshots.

Manual: compare examples 2/4/6/8/9 against the fasit, plus corrected/manual and unknown-bus plans; save/correct/clear/reopen bus; inspect source details, gaps and midnight. Check iPad Safari portrait/landscape, 768/1024/1440 browser widths, 200% text, keyboard/disclosure focus and Day/Night. Measure actual text ≥4.5:1, necessary boundaries ≥3:1, focus ≥2px-equivalent area and applicable ≥3:1 contrast. Record hardware checks separately as pass/fail/not-run; no network exposure is authorized by this spec.
