# Mounted-tablet readability and interaction review

Reviewed: 2026-09-22. Lens selected by the user. Scope: updated DESIGN.md and EXPERIENCE.md, latest recorded overrides, accepted HTML references (especially driving, recovery and the consolidated gallery). Inspected the earlier instructor-night screenshot for composition, checking current HTML for subsequent changes. This is a static contract/reference review, not mounted-device, driving, assistive-technology or standards certification.

## Findings

### A1 — Medium — Persistent clock is absent from the primary driving and recovery references

- **Location:** `mockups/driving.html`, all seven tablet frames; `mockups/summary-recovery.html`, the internet-loss and GPS-loss driving frames. Compare EXPERIENCE Component Patterns → Persistent clock and DESIGN Layout & Spacing → permanent top-right clock.
- **Evidence:** The consolidated gallery provides `time.clock` in its tablet headers. The primary driving and recovery HTML has no current-time element. Scheduled trip times and the GPS countdown are different information and cannot substitute for it.
- **Consequence:** An implementer using the explicitly accepted main driving/recovery references can omit the clock precisely during normal driving or an outage, despite the latest persistent-clock decision. The variation also weakens the predictable placement expected for a short side glance.
- **Concrete fix:** Add the same persistent top-right clock to the existing primary driving and degraded-data frames, maintaining route/destination and the current/next stop hierarchy. Use the existing 30px/tabular-numeral token and an unmistakably simulated current time. Check the existing header fit rather than shrinking stop text.
- **User decision:** None; this synchronizes references with an accepted requirement.

### A2 — Low — Auto selection is visually color-only in the main driving reference

- **Location:** `mockups/driving.html` and `mockups/summary-recovery.html`, `.auto-toggle[aria-pressed="true"]`; DESIGN Components → Theme control; EXPERIENCE Accessibility Floor.
- **Evidence:** Both states render the identical visible word `Auto` with identical geometry and weight; the selected rule changes only gray to green. `aria-pressed` and accessible names correctly distinguish the states for assistive technology. The consolidated gallery separately labels its header Auto/Manuell, but the primary driving and recovery frames do not.
- **Consequence:** A sighted user who cannot reliably distinguish gray from green cannot verify whether the persistent manual preference or Auto is active from those driving frames. The approved green/gray treatment remains valid, but alone does not meet the document's own non-color-only distinction rule.
- **Concrete fix:** Preserve the approved colors, two hit areas, dimensions and icon. Add one consistent non-color selected cue or a concise visible mode label, then reflect that choice in both references and the component description. Do not solve this through hover-only text or a menu visit.
- **User decision:** Review the small visible cue if introduced; no need to reopen Auto semantics or palette. This is a refinement, not a reason to redesign the control.

### A3 — Low — Night gallery keyboard focus uses the day blue instead of the night information color

- **Location:** `mockups/remaining-screens.html`, global `a:focus-visible,button:focus-visible` declaration; night frame `#mentor-instructor` buttons, among others.
- **Evidence:** The global outline is hard-coded `#1755A1`. Night content otherwise uses `--info:#95BDEC`, and `.stop-link:focus-visible` already uses that mode-dependent variable. Thus adjacent keyboard-operable controls in the same night screen have inconsistent focus visibility.
- **Consequence:** Keyboard focus on the dark surface is noticeably less clear for ordinary buttons than for the stop entry. The PC/keyboard accessibility contract should not inherit this avoidable inconsistency.
- **Concrete fix:** Within tablet/PC content, use `var(--info)` for the focus outline, retaining a suitable fixed fallback for the surrounding light gallery navigation. Preserve outline thickness/offset. Verify keyboard traversal after changing the selector.
- **User decision:** None; applies the already approved mode-specific information colors.

## Accepted behavior retained

- Vertical future-at-top stops and explicit current/next/departed labels support the agreed hierarchy; no horizontal redesign is warranted.
- Motion locks retain a labelled Menu, while both theme targets stay enabled. GPS countdown text has an explicit non-repetitive announcement rule and a defined unlock transition.
- Notice detail and acknowledgement follow the latest standstill/five-minute exception. A large Registrert action complements the swipe; no precise gesture is required.
- Operative mentor role labels are prominent text, with FØRER replacing the guiding state during takeover. Open mentor controls are an explicit approved exception, not a defect to remove.
- Simulation labelling, stale/last-confirmed wording and stop-role labels provide meaningful non-color cues. The described refresh/focus rules avoid poll-driven focus theft.
- The last requested button no-wrap and removal of the bus-change rail are present in the current HTML.

## Verification limits to carry forward

Real mounted-tablet glance comprehension, sunlight/night glare, glove/vibration touch performance, two simultaneous long notice headings and long stop names still require device checks. These limits are already identified in the spines; they are not new generic blockers or proof that the accepted visual choices fail. Static gallery framing and its surrounding review-page scrolling must not be mistaken for the production viewport.

Summary: 0 critical/high findings; 1 medium reference-consistency issue; 2 low accessibility refinements. No new safety restriction or role model is proposed.
