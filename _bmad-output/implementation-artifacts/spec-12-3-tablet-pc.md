---
title: '12.3 — Use included views on tablet and PC'
type: feature
created: 2026-10-27
status: in-progress
route: dispatch
review_loop_iteration: 0
baseline_commit: ce0669f6f75f337a2df9471860be1b66efb171f0
story_key: 12-3-use-the-included-views-on-tablet-and-pc
owner_acceptance: pending
context: []
---

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
- [ ] Add shared safe theme preference and connect every included entry/view; style actual states, controls and reflow. Fix concrete keyboard/focus defects encountered within this outcome.
- [ ] Add meaningful browser cases covering matrix including denied/corrupt storage, reload, cross-route/login/logout/reset isolation and full rendered-state measurement in both themes. Use independent literal expectations and actual private API data for private screens.
- [ ] Add isolated reproducible verification/setup with frontend15323, fictional18323, private18324, Compose project `ibe160-story123-tests`, separate volumes and ignored credentials. Root coordinates execution; never start/stop other environments. Existing npm dependencies are installed in this worktree.
- [ ] Record AC-to-behavior/evidence mapping, exact commands/build/source identities, failures/limits and short manual checklist at `docs/story-12-3-manual-testing.md`; update own story/sprint to review, never done or accepted.

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
