---
title: '12.3 — Use included views on tablet and PC'
type: feature
created: 2026-10-27
status: done
route: dispatch
review_loop_iteration: 0
baseline_commit: ce0669f6f75f337a2df9471860be1b66efb171f0
story_key: 12-3-use-the-included-views-on-tablet-and-pc
owner_acceptance: accepted
accepted_on: 2026-10-27
acceptance_evidence: ../../docs/evidence/12-3-device-acceptance-2026-10-27.md
context: []
---

> Publication follow-up,27 October2026: Jonas has now explicitly authorized committing/pushing the completed documentation and evidence, then merging12.3 into main after identity/final checks and pushing main. Earlier no-commit/no-push/no-merge statements describe the previous checkpoint.12.4 remains backlog.


> Final owner decision, 27 October 2026: **done/accepted**. Jonas approved personal Lenovo/Brave readability and touch comfort and conditionally granted overall acceptance. All remaining required checks passed; see [final device acceptance](../../docs/evidence/12-3-device-acceptance-2026-10-27.md). Earlier frozen scope/pending statements below are historical. His latest no-commit/no-push instruction overrides earlier publication permissions; no main merge or12.4 work.


> Current-main update, 27 October 2026: this document retains the original approved checkpoint and historical verification. The [current reconciliation spec](spec-12-3-current-main-sync.md) supersedes its old no-main-integration restriction and pending 12.1/12.2 assertions: both dependencies are now done/accepted by Jonas. It authorizes full main integration and root commits/push on the existing story branch. Story 12.3 remains review/pending; use the [new handoff](../../docs/evidence/12-3-main-sync-handoff.md) for fresh integrated-build evidence. Previous runs and physical pilot observations do not qualify this version.


<frozen-after-approval reason="Owner explicitly requests autonomous implementation, verification and isolated local commits, without stopping after a plan">

## Intent

Make all included views readable and operable on PC and tablet layouts with labelled controls, visible keyboard focus, manual Day/Night and enlarged text. Persist only the non-private theme preference. Record actual measurements, failures and device limitations.

## Boundaries & Constraints

**Always:** Work only in `D:/IBE160/tmp/story-12-3`, branch `story/12-3-tablet-pc-accessibility`, based on clean local main containing 12.1/12.2. Preserve their contracts, historical evidence and pending Jonas acceptance. IR-01: informative text >=4.5:1, necessary non-text >=3:1, focus >=2px perimeter area and >=3:1 change/adjacent contrast, unobscured. Forgiving labelled controls, 58px preparation control floor, wrapping Norwegian text and keyboard dialog focus/return. Theme remains available before login and across included screens/reload, with explicit current state. Only an allowlisted theme value may persist; private content remains volatile. Blocked/corrupt storage cannot prevent operation. Preserve manual, unknown, fictional and owner distinctions.

**Never:** No Auto, wake, GPS, offline private persistence, parser expansion, external activation, main merge or push. Do not touch the 12.1/12.2 environment15312/18312/18313 or ordinary services. Do not expand to 12.4 complete-system qualification or claim actual hardware/owner acceptance from emulation.

## I/O & Edge-Case Matrix

| State/action | Expected behavior | Failure boundary |
|---|---|---|
| First visit / explicit theme toggle / reload / route change | Deterministic Day default, current label/pressed cue, retained explicit Day/Night on all included views | No OS Auto; no private values stored |
| Invalid or denied localStorage | Day fallback or in-memory chosen theme, usable controls | No crash or deletion of unrelated keys |
| Logout, demo reset and reopen | Theme retained; private/demo state boundaries unchanged | Theme never implies restored private session or data |
| Keyboard navigation/dialog cancel | Labelled controls, meaningful screen focus, visible indicator, return to actual visible invoker | No hidden focus target or focus escape from native modal |
| Default/selected/warning/error/unavailable/conflict/disabled | Actual computed text/background/boundary/focus meet IR-01 in both themes | Measure actual surfaces, including bright warning on Night |
| Long Norwegian text at tablet/PC and 200% text | Wrap/reflow; controls and details reachable | No clipped content/horizontal page overflow |

</frozen-after-approval>

## Code Map

- `frontend/src/main.tsx`, `demo.tsx`: separate production entries; `/demo` remains private-module-free.
- `PrivateDrafts.tsx`: local Night state and `Nattmodus` button; replace state with shared theme while retaining familiar button semantics.
- `FictionalAssessment.tsx`: local Night, reset forces Day; share preference and preserve it across reset. Keep demo-only imports isolated.
- `PrivateAccess.tsx`: auth shell/login presently not themed; add theme access outside private session.
- `style.css`, `fictional-assessment.css`: actual palettes; private Night pre/link/auth shell and demo Night form surfaces need inspection. Preserve black focus on bright warnings.
- `frontend/tests/private-activity-helpers.ts` and existing private-* specs: real API fixtures, accessible journeys and measurement patterns; hardcoded8001/5173/project require disposable copies for12.3.
- `frontend/tests/fictional-assessment.spec.ts`: no-network demo and contrast/dialog tests; update intentional reset expectation and asset allowlist if shared theme creates a new chunk, retaining no-private-network boundary.

## Tasks & Acceptance

**Execution:**
- [x] Add shared safe theme preference and connect every included entry/view; style actual states, controls and reflow. Fix concrete keyboard/focus defects encountered within this outcome.
- [x] Add meaningful browser cases covering matrix including denied/corrupt storage, reload, cross-route/login/logout/reset isolation and full rendered-state measurement in both themes. Use independent literal expectations and actual private API data for private screens.
- [x] Add isolated reproducible verification/setup with frontend15323, fictional18323, private18324, Compose project `ibe160-story123-tests`, separate volumes and ignored credentials. Root coordinates execution; never start/stop other environments. Existing npm dependencies are installed in this worktree.
- [x] Record AC-to-behavior/evidence mapping, exact commands/build/source identities, failures/limits and short manual checklist at `docs/story-12-3-manual-testing.md`; update own story/sprint to review, never done or accepted.

**Acceptance Criteria:**
- Given each included access/editor/confirmation/bus/day/activity/outcome/notice/conflict/closure/recap/demo state, when inspected in both themes with keyboard, then rendered informative text, boundaries and focus satisfy IR-01 with readable labels and return focus.
- Given long Norwegian values and200% text on narrow tablet and wide PC layouts, when traversing the included views, then content and controls remain readable/reachable without page overflow.
- Given manual theme choice, when navigating/reloading/resetting/logging out, then only the allowlisted non-private preference persists and private/demo boundaries remain intact.
- Given automated desktop evidence, when handing off, then actual Lenovo Pad/Android/Brave and manual Jonas acceptance remain explicitly pending;12.1/12.2 acceptance and historical477/479 results are unchanged.

## Implementation Notes

No unresolved product intent gap. No irreversible migration/external action. Implementation agent must not spawn agents or run a nested Build. Root owns final review, commits and Norwegian session logging; agent may edit product/tests/setup/docs only in this worktree. User authorization overrides intermediate plan approval pause. Keep bounded implementation decisions here.

## Spec Change Log

## Review Triage Log

## Verification

TypeScript/Vite production build; isolated real-API private browser checks and no-backend demo regression; task browser matrix for themes/storage/contrast/focus/reflow. Preserve raw UTF-8 outputs and failed attempts; record exact passed counts, no extrapolated complete broad pass. Root independently inspects diff and screenshots, runs three review layers and verifies fixes.

### Pre-review root verification checkpoint — 2026-10-27

Full29-case task matrix passed with stable source, actual executed inputs and current built artifacts: `12-3-browser-20261027T085409659655Z-0057a88f.json`.312 measured states cover25,216 text observations,6,720 boundaries,6,000 keyboard stops and80 distinct checked/unchecked native indicator samples (160 emitted individual/aggregate observations). Minima: text6.126:1, necessary boundary4.781:1, focus5.987:1 /3px. Actual100%/200% root text is16px/32px. Edge156 desktop only; hardware/owner acceptance remain pending. Root independently read code/test changes and inspected actual modal/recap/checkbox renders. Original failures and bounds remain in the handoff report. Regression and independent review results are appended after completion.

### Independent review triage — 2026-10-27

All three layers reported before triage. Each finding is judged individually before grouping. Corrections remain inside existing intent; no backend contract or12.4 goal is introduced.

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| B1 focus pixels | medium / patch | Focused styles do not compare the same pixels before focus; permanent matching outlines can pass. Add actual before/after comparisons and a negative probe. |
| B2 alpha surfaces | medium / patch | RGB-only background logic can misreport alpha layers and modal backdrop content. Composite supported layers and explicitly scope/record unsupported or inactive surfaces. |
| B3 native glyph | medium / patch | Arbitrary maximum interior contrast does not identify glyph/fill. Use checked fill/glyph evidence, exclude the boundary and reject a missing-glyph probe. |
| B4 inner clipping | medium / patch | Document width misses clipped critical labels/content in fixed containers. Check meaningful critical content while retaining intentional input/dialog scrolling. |
| B5 reading order | false / reject | Existing private-access tests assert username to password to login; fictional-day explicitly asserts theme to load to save; owner-feedback asserts Start/end confirmation order. These representative literal tests run in the184-case regression. |
| B6 native icon limits | low / patch | Checkbox pixels are measured; calendar/select/disclosure pixels are not. State this explicitly in summary/checklist rather than implying universal non-text qualification. |
| B7 private focus states | medium / patch | Start, saved outcome, reader and recap need complete focus traversal in addition to text measurements. Extend the actual journey. |
| B8 stale copied tests | low / patch | Deleted source tests remain generated. Remove obsolete generated .ts files and verify unrelated files survive. |
| B9 storage clear | low / patch | Cross-tab listener ignores key=null clear events; normalize this event and test two tabs. |
| B10 durable evidence | medium / patch | Ignored logs disappear on cleanup; older copied tests share an overwritten directory. Preserve available raw results/final actual inputs durably and disclose exploratory-copy limits. |
| V1 same-pixel change | medium / patch | Independent duplicate of B1: focused-only assertions cannot reject an unchanged permanent outline. Share correction/negative probe, retaining this separate row. |
| E1 timeout children | medium / patch | A subprocess timeout kills the immediate launcher, leaving owned descendants able to retain15323. Terminate/await the owned tree, retain cleanup evidence and test an actual owned child. |

B1/V1 share a cause; all other retained items have separate causes/corrections. B5 is refuted by the named literal tests. No frozen-intent change or deferral is required.

## Bounded implementation / verification notes — 2026-10-27

These patches implement the retained review items without changing the frozen intent, environments, acceptance owner or historical12.1/12.2 evidence.

- B1/V1: real keyboard traversal remains census-based. Every visited host is actually blurred, its unfocused computed style/ancestor surface signature checked, and focus restored with keyboard navigation. Unique style/geometry/surface pairs capture actual focused/unfocused PNGs; cached results are explicitly labelled representative. Count only same-position pixels outside the host border with >=3:1 change, requiring >=2px perimeter area. A positive focus-only probe and identical permanent-outline negative probe share a test/cache and reject unchanged rings. The stronger measure found the next opaque private-confirmation button covering part of a ring; vertical button spacing fixes the actual rendering without lowering the threshold.
- B2/B4: supported RGB/RGBA backgrounds and foreground alpha are composited. Active native-modal measurements exclude the underlying page/backdrop. Unsupported group opacity, filters, images/blending and translucent modal backgrounds are recorded as unmeasured and fail normal positive product measurements. Critical text/action bounds are checked against clipping ancestors, while native field content and intentional vertical native-dialog scrolling remain reachable. The disabled native form palette now explicitly uses opacity1. Independent alpha, opacity, clipping and modal-scrolling probes exercise these boundaries.
- B3: checked fill is the actual dominant interior pixel population (including UA hover treatment), then a connected non-boundary checkmark component must contrast >=3:1 against that fill. The author boundary plus antialiasing is excluded. PNG/palette/component evidence is attached before assertions. A checked appearance:none fill with no glyph is rejected.
- B7/B9: start confirmation, saved outcome, notice reader, recap and saved/reopened/unavailable API assessment states now have full focus traversal. Storage clear events use deterministic Day; two actual tabs verify the event and reload behavior.
- B8: generated-copy ownership is recorded in a manifest. Only obsolete manifest-owned .ts copies in the verified real disposable directory are removed; unrelated .ts/text files survive. Unknown pre-manifest files are never guessed to be disposable. The rename/stale-removal/preservation self-test passes1/1.
- E1/B10: timed-out commands terminate and await only their owned PID tree/session and preserve the original124 failure plus cleanup outcome. Actual-child timeout and UTF-8 failed-command/archive self-tests pass2/2. Inputs are snapshotted before launch; available raw logs/reports/results and executed-input copies are compressed into a unique durable tar.gz with a per-entry hash index. Every archived entry is re-read and verified before only the verified owned staging directory is removed. Older exploratory inputs are not invented or rewritten.

Targeted evidence (root owns final/full verification):

- Stable production build: `docs/evidence/12-3-build-20261027T093222536295Z-f97c2469.json`, gate0.
- Five helper/theme positive/negative probes plus three representative actual private/demo/API journeys:8/8 passed, gate0, `docs/evidence/12-3-browser-20261027T093241559270Z-3dea4d0a.json`. The39 measured positive product states have an empty unmeasured list. The opacity negative probe deliberately records one unsupported opacity0.5 paragraph.
- Actual owned-child timeout record: `docs/evidence/12-3-probe-timeout-20261027T092636431373Z-71245256.json` retains exit124 and confirms observed child/root processes exited. Actual UTF-8 command failure: `docs/evidence/12-3-probe-failed-20261027T092636431373Z-71245256.json` retains exit7. The self-test asserts these expected failures and the durable input/log hashes; it does not relabel the commands successful.
- Failed attempts remain available: first tooling archive validation rejected Windows separator mismatches (original archives/staging retained); first browser probe set4/5 failed a CSS-accent equality assumption because UA hover darkens the actual fill; first product representatives1/3 exposed covered focus pixels and translucent disabled select. Subsequent corrections use actual rendering and keep the original failures.

This remains desktop automation. Native calendar/select/disclosure icon pixels, actual Lenovo/Android/Brave and Jonas acceptance remain outside the qualified evidence. Root owns final report/checklist, commits and Norwegian session logging.

### Reinspection triage — 2026-10-27

All three original layers reported before this triage. B1/B2/B3/B6/B7/B8/B9/B10/V1 are fixed; B5 remains rejected on its recorded refutation. E1 covers the tested living-parent case but has a residual race.

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| B4-R1 clipped field host | medium / patch | The native-content early return also bypasses a field host rectangle in boundary checks. Apply the exemption only to internal field content, and reject an input host clipped by an ancestor. |
| E1-R1 parent-exit race | medium / patch | The observed children are only awaited if the parent exits between process snapshot and taskkill. Retain owned process handles, terminate surviving observed children safely and test a parent exit during cleanup. |

Root intentionally interrupted only the verified owned Playwright launcher tree to apply these corrections. `12-3-browser-20261027T093740410315Z-828acca6.json` retains exit1 and partial raw results; this is an interrupted attempt, not a completed 34-case result. The first ownership guard refused an insufficient direct-child proof; a recursive verified worktree descendant proof succeeded. No unrelated runtime was stopped.

Final reinspection: all three original layers returned before closure. Blind confirmed B4-R1 fixed with no new issue; edge confirmed E1-R1 fixed with no new issue; verification confirmed no new gap and V1 remains fixed. Root read the revised host-boundary condition, creation-time/handle cleanup and actual negative probes. No retained technical review finding is deferred. Final full executed gates are recorded in the handoff.

### Final technical checkpoint — 2026-10-27

Final revision 9329311: complete task matrix 34/34 passed, selected post-review regression 37/37 passed, actual HTTP/PostgreSQL 74/74 passed, TypeScript/Vite build passed. Root tooling 3/3 and unchanged generator 1/1 passed. Final preparation and runtime verification are recorded in the handoff; all three reviewers closed their retained findings. The earlier 184/184 regression and historical 477/479 are separate. E10-A4 theme persistence and E11-A4 visible-invoker focus are technically resolved; device qualification and Jonas acceptance remain pending. Keep story review/in-review and 12.4 backlog.
