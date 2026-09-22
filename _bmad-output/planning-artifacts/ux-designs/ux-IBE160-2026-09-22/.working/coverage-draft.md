# Draft source coverage — 2026-09-22

Accepted-reference extraction update: DESIGN.md now contains concrete driving typography, spacing, radius and component tokens extracted from the user-approved vertical reference, promoted to `mockups/driving.html`. EXPERIENCE.md links the same artifact and correction-control tokens. `.working/visual-extraction.md` records the CSS mapping and numerical color checks. Earlier empty-token findings are superseded for depicted driving elements only. Unshown surfaces, some behavior decisions and actual-device validation remain open. Draft keyboard and recoverable-error defaults also reduce earlier state gaps; no full reviewer gate has run.

Current correction: the user explicitly confirms vertical orientation and changes the at-stop baseline to next-after-next / next / CURRENT (top-to-bottom), omitting previous. Between stops it is next-after-next / NEXT / departed. A four-stop variant is merely permitted for exploration. Manual Day/Night persists across shifts/restarts until explicitly disabled. Current reference is `driving-vertical-2.html`; prior sketch files are visibly marked historical. This supersedes prior horizontal updates and all open manual-override lifetime items below.

Resume update: the latest explicit instruction now requests horizontal stops in Day A/Night C. The existing run continues; no sources or prior behavior were reset. `driving-horizontal-1.html` is the current candidate, with left/right mapping and dimensions awaiting assessment. `driving-layout-1.html` preserves the earlier vertical variant as history. All earlier vertical-order findings below are superseded for orientation only; current/next focus and notice timing still apply.

Latest order/clearing update: future stops are above, past stops below, with current/next focus in the middle. At a stop the top-to-bottom order is next/current/previous; between stops it is stop-after-next/next/departed. Stop-related messages remain through arrival/dwell and clear after onward departure or passage, without marking the source notice resolved. This supersedes the earlier open clearing item below.

Latest focus/timing update: the user clarified current-stop emphasis at a stop and next-stop emphasis between stops, superseding the earlier next-stop-always interpretation. The vertical sketch now illustrates that rule and a warning triangle directly after a stop name two stops ahead; automatic stop-related message display begins only on the segment from the preceding stop to the affected next stop. Message clearing remains open. Earlier snapshot references to unresolved focus placement and entirely unresolved takeover entry are superseded by these decisions.

Update after palette selection: the user selected Day A and Night C. DESIGN.md now defines 14 color tokens and EXPERIENCE.md references the approved day/night colors. All color references resolve. The original distillation findings below describe the earlier snapshot: the empty-color-group finding is superseded, while typography, geometry, component recipes and other recorded gaps remain open. The accepted palette reference is `.working/color-themes-1.html`, explicitly limited to Day A and Night C; its layout is not accepted.

Proactive Pass 1 mechanical check during distillation. This is not an opt-in reviewer report, not a conformance claim and not finalization. Read all three DESIGN examples, both EXPERIENCE examples, the local DESIGN spec and validate.md Pass 1. Source extraction and latest canonical memlog were the decision basis; PRD requirement headings were checked directly. Source refs in both spines retain all five inputs in the approved order.

## Source-requirements mapping

| Exact PRD requirement | Draft destination |
|---|---|
| FR-1 — Private access | Access and navigation controls; IA private access; UJ-1 step 1; UJ-2 step 1 |
| FR-2 — Import and confirmation | Import review editor; UJ-1 steps 1–3. Latest user override explicitly adds JPG/PNG. |
| FR-3 — Timetable completion | Activity and trip selector; state table; UJ-1 step 2 |
| FR-4 — Other activities | Import review editor/selector; UJ-1 step 2 |
| FR-5 — Day overview and assignment | Shift overview; UJ-1 step 3 |
| FR-6 — Active trip | Trip choice/correction; UJ-1 steps 4, 7 |
| FR-7 — Three-stop view | Three-stop sequence; UJ-1 step 5 |
| FR-8 — Progression accuracy and diversion recovery | Three-stop sequence; active-driving states; UJ-1 step 5 and failure path |
| FR-9 — Uncertainty and manual stop control | Stop correction controls; movement policy; UJ-1 step 7 |
| FR-10 — Between-trip displays | Between-activity transitions; UJ-1 step 8 |
| FR-11 — Operational changes | Operational-change controls; UJ-1 step 7 |
| FR-12 — Retrieval and relevance | Information Trust; notice components; UJ-1 steps 3, 6 |
| FR-13 — Provenance and freshness | Data status; Voice and Tone; Information Trust; UJ-1 step 6 |
| FR-14 — Notice lifecycle | Notice heading and detail; Information Trust; UJ-1 steps 6–7 |
| FR-15 — Audio | Interaction Primitives; UJ-1 step 6 |
| FR-16 — Movement and interaction policy | Approved movement policy; UJ-1 steps 6–7 |
| FR-17 — Internet loss | Whole-active-shift states; UJ-1 step 7 |
| FR-18 — Recovery and partial failure | Data status; whole-active-shift states; UJ-1 step 7 |
| FR-19 — No initial data | Voice and Tone; notice states; UJ-1 failure path |
| FR-20 — Active-shift recovery | Access controls; whole-active-shift states; UJ-1 step 7 |
| FR-21 — End or abort | End-shift confirmation; UJ-1 step 9 |
| FR-22 — Daily summary | Summary and export; UJ-1 step 10 |
| FR-23 — PDF export | Summary and export; UJ-1 step 10; UJ-2 step 5 |
| FR-24 — Retention | Information Trust, Privacy and Retention; UJ-1 step 11 |
| FR-25 — Repeatable desktop demo | Instructor simulation; UJ-2 |
| NFR-1 — Tablet usability | DESIGN hierarchy; Accessibility Floor; UJ-1 step 5; actual mounted verification pending |
| NFR-2 — Information integrity | Data status; Information Trust; both journeys and failure paths |
| NFR-3 — Privacy and access | Foundation; Information Trust; UJ-1 steps 1, 10–11; UJ-2 steps 1, 5 |
| NFR-4 — Target-environment reliability | Responsive & Platform; both journey failure paths; actual device verification remains downstream |

The latest user decisions additionally cover dominant next stop/temporary action, automatic and manual themes, non-passenger activity breadth, obvious trip transitions with undo, active-trip wakefulness, privacy and one/two-tap stationary correction. They appear in both spines where visual and behavioral concerns apply; unresolved mechanics remain explicit rather than invented.

## Pass 1 findings

1. **Flow coverage — adequate draft coverage.** Both exact PRD UJ names are retained, with Alex and the source-named Instructor role, numbered steps, climax and failure paths. All 25 FRs map to steps/behavior. There is no invented instructor personal name. Remaining missing load-bearing detail: transition undo after additional progress; takeover/return criteria; layover/dispatch-change behavior; summary reopening; import/export/access failure recovery. These are explicit open items, so surface closure is not yet final.
2. **Token completeness — critical gap, intentional draft.** All five token groups are empty; no unresolvable references were emitted. Exact day/night colors, typography, geometry, contrast targets and visual state recipes are not established. The spines are not ready for visual implementation. Palette candidates, if generated, are choices for the user rather than accepted tokens.
3. **Component coverage — catalog strong, recipes incomplete.** All 17 component names in the DESIGN table have identically named rows in EXPERIENCE. Visual and behavioral constraints exist; exact visual recipes and several interaction states remain open as listed in the spines.
4. **State coverage — partial.** Each IA destination has a state-table entry; offline/GPS/recovery/uncertainty/notice lifecycle/confirmation/demo distinctions are explicit. Focus, keyboard, permission/access errors, import processing/error recovery, export errors and detailed empty/loading treatments are not complete. Do not mark this category strong until those gaps close.
5. **Visual reference coverage — pending.** No accepted mocks, wireframes or supplied imports informed this draft. Any independently generated `.working` palette candidate is an unaccepted discovery artifact. Finalization must inventory accepted artifacts, promote keepers, link relevant spine sections and confirm each IA surface as mocked or spine-only.

## Remaining user-facing decisions

First resolve the user-owned visual direction and concrete palette/type/layout choices using the parent's discovery process. Next decisions concern endpoint slots, meal label, theme override behavior and visual treatment of changed/uncertain data. Behavior requiring further precision includes dominant-action takeover, undo after progress, layover/dispatch changes and minimal summary reopening. Accessibility/error-state implementation detail can be resolved without reopening already confirmed movement, retention or core-scope decisions; choices must remain labelled until captured.
