# Story 10.2 draft corrections — 22 October 2026

The editor compares current persisted activity facts with the original interpretation by activity UUID. Corrected values, original values and manual additions have text labels. Equivalent instants, source clocks with optional zero seconds and the mapped CAR type do not create false correction markers. Restoring an original value removes its marker. Source warnings remain historical; current missing type, times, places and required trip facts are listed separately. Missing facts remain saveable; invalid entered times and negative intervals remain blocked. No confirmation is implemented.

Reorder/add/remove materializes legacy duty boundaries against activity IDs before changing structure. Deleting an anchor deletes its duty boundary; original metadata remains intact. Raw local time controls stay keyed to activity IDs. Day/Night is an in-memory preference.

## Independent A–E comparison and import limits

Examples 1–9 remain the primary realistic-upload regression set; A–E supplement it. The 167-test full backend run included `test_all_actual_fixtures_compare_every_required_fact`, all-seven independent import facts/provenance and save/reopen checks, and the separate examples 8–9 assertions. Browser regressions also import, save and reopen examples 8–9. These checks retain the original partial status for example 6; new synthetic layouts do not replace the approved historical fixtures. Jonas explicitly reaffirmed checking both sets during implementation.

Expected facts come from `Eksempelfiler/Fasit-testskift.json`, not adapter output. Initial full guarded verification deliberately compared every activity endpoint and failed four cases: **162 passed, 4 failed** (112.54 seconds). No parser contract was changed to make these layouts qualify.

| Case | Observed result | Bounded assertion / limitation |
| --- | --- | --- |
| A | Partial, 2 of 5 rows | Both explicit work rows match independent times. Three movement rows are missing. Header 08:50 and final Sign-off 08:28 remain distinct; no gap row invented. |
| B | Rejected: `conflicting_headers` | Not qualified. Fasit contains partial Travel to, gaps, repeated turnumbers and zero-duration movement; these cannot be claimed tested through this PDF. Existing valid fictional partial-Travel-to and zero-duration fixtures provide bounded regression coverage. |
| C | Partial, 6 of 15 rows | Six work/pause rows match independent clocks and calendar dates including overnight. Nine movements are missing. No claim to its full overnight movement extraction. |
| D | Rejected: `conflicting_headers` | Not qualified. CAR transfer/return cannot be claimed through this PDF. Existing qualified example 8 and fictional CAR variants remain the bounded mapping/return regressions. |
| E | Eight work rows | Work-only facts match independent JSON, including Fadder/Instruktør, separate Coffee and no invented final Sign-off, trip or bus. |

Final A–E regression assertions record these exact partial/rejected outcomes and compare only supported rows with independent expectations. A–D are **not qualified**. Intermediate-stop duplication, distance and arbitrary layouts remain unqualified. The JSON is an independent test oracle, never a runtime oracle; this is not a full-fasit claim.

## Verification and walkthrough handoff

Correction integration uses valid fictional PDFs, with a legacy metadata-only duty boundary. It checks corrections/addition/reorder, manual origin, source retention, unknowns, discarded and dismissed edits, revision/content preservation, save/reopen and removal of a duty anchor. Additional API coverage combines corrections, added incomplete activity, order and fixed expiry. Existing suite retains invalid/overnight clocks, replay/conflict/recovery and account/session isolation coverage.

The second guarded run passed **167 backend/API/PostgreSQL tests (116.74s)**, real restart/migration replay/state/deadline checks and the TypeScript/Vite build. Its broad browser run passed **80 of 82 cases (4.9m)**, including both new correction cases. Two test issues were identified: a new exact seconds expectation rejected equivalent `00:00`, and an existing account-switch case allowed the initial automatic list read to invalidate its editor before its intended save. The tests now accept equivalent zero seconds and wait for initial list completion respectively; no identity product code changed. These historical counts are superseded by the later verification below.

Pre-review focused verification passed **5 A–E cases (1.87s)** and **59 affected browser cases (3.9m)**. Actual different-time correction (15:00 → 15:00:30), save/reopen, equivalent-time/CAR markers, structural discard and missing-line feedback are covered. An earlier interrupted invocation supplied no result and is not counted.

Three independent review layers ran. Six fixes addressed light-panel Night focus contrast, imported-note attribution, unresolved entered times versus unknown facts, supported-row mapped-type assertions, independent place/trip comparison/restoration checks, and both modes at both widths. One cosmetic helper-extraction suggestion was rejected; no review finding was deferred. Targeted post-review checks passed 5 A–E cases (1.85s), both correction browser cases (20.7s) and builds.

**Final post-review full verification: 167 backend/API/PostgreSQL tests passed (112.70s), real restart/migration replay with identical account/session/draft/operation/deadline and cleanup passed, production build passed, and all 82 browser cases passed in one run (4.8m).** This includes examples 1–9, bounded A–E assertions, every correction matrix row and the identity regressions. A later owner-requested wording-only amendment clarifies that discard covers field edits, activity additions/removals and reordering, while retaining the last saved version. Its TypeScript/Vite build passed; existing discard behavior was unchanged and the full suite was not repeated for that copy change.

Root inspected regenerated screenshots `10-2-768.png` and `10-2-1440.png`: readable correction comparison, unknowns and wrapping without overflow, with visible keyboard focus in both modes. Narrow mode uses Night and wide mode uses Day; browser tests exercise both modes at both widths. CSS contrast calculations: Day text 14.39:1, Night text 12.86:1, Night fields 10.01:1, unknown banner 11.89:1; Night control borders 6.51:1 and focus on dark surfaces 11.45:1. Pale warning panels use a black focus override. Focus outlines are 3px.

The final guarded script exited 0, stopped disposable services and restored the operational API to healthy. The human walkthrough covered correction clarity, reopen, discard, known/unknown distinctions and readability. Jonas requested clearer discard scope, then explicitly approved story 10.2 on 22 October 2026 after that wording amendment. Sprint 10.2 is done. He subsequently authorized commit and push of the completed work, including the development log. No deployment or ordinary-account test is included; A–D import limits remain unchanged.
