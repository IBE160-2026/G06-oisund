# Story 10.5 — Read the day

Implementation and owner acceptance: 24 October 2026. Jonas explicitly approved the delivery and requested commit/push, with no retrospective. Actual iPad Safari checks remain not run; the owner previously reported that the device was unavailable. No individual manual test result or tablet acceptance is inferred. The approved [specification](../../_bmad-output/implementation-artifacts/spec-10-5-read-the-day.md) governs the scope; Epic 11 navigation is excluded.

## Final technical status

**Implementation, independent review and owner acceptance complete.** Root's complete final run on the reviewed/patched code passed **236 backend/API tests (264.58s)**, exact PostgreSQL/API restart and repeated-migration equality, production build and **all 190 Playwright tests in one clean run (11.1m)**, exit 0. Five fully mocked verifier/restoration controls passed (0.133s). One additional unchanged-code contrast test passed with JSON reporting to preserve numeric measurements. Final log: ignored `tmp/10-5-root-final.log`; measurement report: ignored `tmp/10-5-render-report.json`. These final results supersede intermediate harness failures and the pre-review 236/184 run.

All three independent BMAD review layers completed before individual triage. Thirteen findings are individually recorded in the specification; nine retained patch groups are resolved and re-inspected by the same reviewers with no concrete remaining defect. The unknown confirmed service-date claim was refuted by upstream guards; the unusual three-digit CAR extension was graded low and rejected outside the qualified CAR 1–4 envelope. No retained finding was deferred. Patches preserve timed returning duty transitions, single paid-meal subtypes, visible historical uncertainty, list semantics and safe historical-source clock fallback, with stronger correction/classification/fixture/full-plan evidence.

The original operational database container and all monitored account/draft/plan/bus/operation/session/security/secret digests match the pre-test baseline. The only digest difference is three expired login-throttle rows removed by unchanged startup cleanup. Ordinary API/database are healthy, test services are stopped, and the app returns 200 serving tested `index-DgqOD_AO.js` / `index-DQsFmhCi.css`. No operational backend upgrade or migration was needed. Historical test-image churn was restored; new synthetic day/full-plan renders are retained. No product code changed after final verification. Sprint/specification and Epic 10 are done after owner acceptance; commit/push are authorized. No retrospective is started.

The confirmed and reopened plan now presents one ordered day list beside the existing physical-bus editor. The list uses confirmed calendar instants, classifications and corrected fields; historical import metadata never supplies replacement activity facts. Oppmøte comes from confirmed Sign-on, including later reporting points, with unknown places kept unknown. If Sign-on is absent, the separate source-header start is explicitly source information. The planned final activity end and fixed expiry remain distinct from the source-header end.

Touching consecutive pause rows are projected anew with MealBreak, Split break, Coffee-only and paid-meal precedence. Each member keeps its identity, confirmed details, uncertainty and effective duty; grouped warnings and duty changes remain visible. Equal starts, zero-duration CAR rows, repeated trip numbers, separate periods and explicit midnight dates remain ordered. Gaps begin after the greatest preceding end and stay unclassified; overlaps receive a neutral note. The current physical bus stays separate from historical snapshot bus and duty/CAR facts. No new persistence, API, migration, bus history or lifecycle action was added.

## Verification record

- `npm.cmd run build`: passed during implementation (TypeScript and production Vite build).
- Focused initial run: 75 passed / 11 failed in 6.8 minutes. Four existing service-date selectors needed scoping to the new visible overview; seven new cases had omitted the saved draft identity when issuing an update operation. Both test-harness issues were corrected. All 25 bus and 19 identity regressions passed. The 34-case targeted followup passed in 1.4 minutes, including all 19 projection cases, affected confirmation/denied-bus regressions and the eight day browser cases. After single-row type/time deduplication and omission of empty non-passenger identifiers, the final eight-case render rerun passed in 51.5 seconds. All eight new screenshots were regenerated from the polished production build. Implementation-agent inspection of the 768 Day and Night 200% renders found wrapping and visible warning/disclosure focus without clipping. Every runtime wrapper restored the operational API healthy in its finalizer; the disposable API/database are stopped. No historical PNG changed. `git diff --check` passes.
- Root pre-review run passed 236 backend/API tests (275.46s), exact restart/migration equality, build and all 184 browser tests (10.8m). Root read the complete tracked/untracked diff and audited every specification matrix row against executed tests.
- Review fixes passed 35 affected checks (1.3m). A strengthened six-case enlarged-control run initially passed four; two landscape measurements needed explicit scroll centering and 1px rounding tolerance, then passed 2/2 (16.2s). Product assets did not change for this measurement correction. The final complete 236/190 run above includes every corrected test together.

Only fictional synthetic accounts are used for browser save/correct/confirm/reopen checks. Pure projection tests use synthetic edge cases and the independent owner-approved anonymized example transcriptions for all nine examples, without importing operational files or modifying private records. The focused runtime wrapper restores the operational API in `finally`; no operational image upgrade is authorized.

The new browser matrix covers 768 × 1024 portrait, 1024 × 768 landscape and 1440 × 1024 desktop viewports in Day/Night, 200% root text, long place names, keyboard pause disclosures, both grouped members, explicit overnight dates, zero-preserving duties, CAR, fixed stored snapshots/deadlines and empty browser persistence. Whole-plan checks scroll to the bus field, save/cancel, historical/source disclosures and close/delete controls and verify visible bounds; screenshots cover the combined surface. Root inspected normal/enlarged Day/Night renders at several widths; warnings, dates, wrapping and disclosure focus are visible without clipping. These are automated desktop-browser checks, not actual iPad/Safari or assistive-technology qualification.

Actual computed-style measurements retained from the final code, rounded to two decimals:

| Measurement | Day | Night | Required floor |
|---|---:|---:|---:|
| Main text | 14.39:1 | 12.86:1 | 4.5:1 |
| Reporting text | 12.86:1 | 10.01:1 | 4.5:1 |
| Warning text | 11.89:1 | 11.89:1 | 4.5:1 |
| Activity boundary | 5.89:1 | 8.37:1 | 3:1 |
| Reporting boundary | 9.91:1 | 6.51:1 | 3:1 |
| Keyboard focus against adjacent surface | 21.00:1 | 11.45:1 | 3:1 |
| Focus outline | 3 CSS px | 3 CSS px | 2px-perimeter-equivalent |

These measurements cover the tested surfaces/states; they are not a complete WCAG conformance claim.

| Specification matrix row | Executed evidence |
|---|---|
| Corrected confirmed plan | Real save/correct/confirm/reopen, immutable API snapshot equality, matching-source comparison and explicit Instruktør/Sign-on decisions in `private-confirmation.spec.ts` |
| Touching pauses | 21 projection cases, all nine independent transcriptions, both singleton paid types, grouped-member disclosures and visible A → B → A boundaries |
| Gaps/overlap | Nested-overlap greatest-end regression plus independent known gaps/labels and no invented header-tail work |
| Overnight/separate parts | Example 1/4/6 expectations and browser date/reporting matrix, preserving zeros, CAR and non-driving activities |
| Denial/suspension/expiry/deletion | Complete bus/identity/confirmation regressions, including explicit overview hiding/recovery and parent-section removal/late-response guards |

## Owner walkthrough — offered checks; delivery accepted

Use http://127.0.0.1:5173/private with your existing access, reload the page and use separate anonymized/manual test plans. Do not alter genuine work to perform these checks.

1. Open a confirmed test plan. Compare reporting time, activity order, types, known places and final end against the [approved fasit](../../Eksempelfiler/README.md). Missing places remain unknown; gaps are unclassified, with no invented work or completion.
2. Check example 2 matpause 12:01–12:43 or example 7 08:52–09:28; expand both members. Check example 4's next-day dates and `090`, example 5's `006` and final explicit end instead of header end, and example 6's separated work/owner-assisted Travel to. Example 8 keeps CAR/duties separate from actual bus; example 9 keeps Fadder/Instruktør and separate Coffee periods without invented driving.
3. For a corrected imported test activity, open **Kilde og rettelser** and compare original/current fields and correction marker. Open **Bekreftede detaljer og historisk kilde** and **Bevarte kildefakta**. Historical uncertainty is labelled before correction/confirmation and never overrides confirmed facts; previously accepted source-marker warnings remain visible.
4. Enter physical bus `0012`, save, reload and reopen; correct or clear/save/reopen. Current bus changes must not alter the chronological snapshot, duty/suffix or fixed expiry. Optionally compare two windows after competing bus edits; no silent overwrite should occur.
5. On iPad, inspect portrait/landscape, Day/Night, touch controls, long names and enlarged text. On PC, use Tab/Enter for disclosures and verify visible focus. Confirm bus, history and close/delete controls remain reachable and text is not clipped. No activity Start/selection/outcome controls should have appeared.

Actual iPad Safari portrait/landscape, hardware touch and 200% text: **not run**. Owner acceptance: **accepted 2026-10-24**. The checklist records offered checks, not individually reported results. No external network exposure is authorized. Desktop screenshot evidence remains separate from actual-device verification and owner acceptance.
