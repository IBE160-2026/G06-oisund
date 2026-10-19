---
name: IBE160 — Design Spine
status: approved
decision: SCOPE-02
updated: 2026-10-19
---

# Design Spine — Course V1

## Authority and visual direction

[Approved SCOPE-02](../../sprint-change-proposal-2026-10-19.md) reduces the interface to preparation, manual consultation, notices and a small recap. [EXPERIENCE](EXPERIENCE.md) defines behavior. Preserve the restrained, readable tablet-first identity and the useful accepted preparation layout. The old driving/mentor/offline/PDF gallery is a historical reference; its 43-screen acceptance is not acceptance of this smaller implementation.

Use a clear chronological day and one prominent selected activity, with notices secondary. No map, chatbot, competing card grid, animated alerts, decorative effects or implied live location. The UI describes user-relevant state; internal revisions, operation IDs and database details stay out of ordinary flows.

## Palette and typography

| Token | Day | Night |
|---|---|---|
| Base | #FFFFFF | #101010 |
| Primary text | #171717 | #EAEAEA |
| Secondary text | #525252 | #BBBBBB |
| Critical | #AD1717 | #F89696 |
| Attention | #805000 | #EFC66C |
| Information | #1755A1 | #95BDEC |
| Confirmed | #17613E | #8BCDAB |

Use system-ui/Segoe UI sans-serif. Reuse preparation reference values as starting points: 34px main heading, 23px section, 22px activity, 21px time, 18px detail and 20px controls. Selected route/destination may use the earlier 42px/32px hierarchy, with a readable `Manuelt valgt` label. These are initial CSS values, not measured readability guarantees. Preserve critical long names through wrapping rather than shrinking/truncating.

Yellow #F5C842 needs the dark #171717 outline/symbol on day white; yellow fill alone is insufficient. All states also use text or a distinguishable shape. Green means saved/confirmed data only, never verified road clearance or physical completion.

## Layout and controls

Landscape tablet and ordinary PC are primary. A narrow layout stacks columns in reading order; exact breakpoints are implementation choices tested against long content and text enlargement. Static mock minimum widths are not product requirements.

Draft review: source preview and editable activities side by side where space allows, otherwise stacked. Day overview: chronological activity list with notice region secondary. Selected activity: route/destination or activity type and known planned dates/times, followed by visible previous/next/direct-selection controls. Keep selection distinct from outcome controls. No stop rail/current-location marker/GPS countdown.

Use forgiving labelled touch controls, starting from the accepted preparation minimum height of 58px, 8px corners and 2px border. No precision gesture required. Manual Day/Night shows its current state through label/icon and a non-color selected cue; omit Auto. Menu and primary actions remain discoverable without relying on the old locked driving footer.

Notice rows show title, matched lines, manual-maintenance label and source/validity/update/check metadata. Long detail can expand without taking over the selected-activity meaning. No chime/staged approach warning. End/abort actions are visually distinct with explicit confirmation and clear cancel; read-only recap shows manual/unknown outcomes and expiry.

## IR-01 acceptance floor retained

All informative text, including large text, must reach 4.5:1 against the actual background. Necessary non-text information must reach 3:1. Keyboard focus must have at least the area of a 2 CSS-pixel perimeter, a 3:1 change between focused/unfocused pixels and 3:1 against necessary adjacent colors; it must not be entirely obscured. No meaning depends only on color.

Measure actual rendered default/focus/selected/warning/error/unavailable/disabled states in both manual themes, including overlays, icon outlines and compositing. A base-palette calculation does not pass a different surface or an implemented interface. No Auto/PDF measurements are required because those features are deferred. Do not claim overall WCAG AAA conformance.

## Included components and verification

Private access, draft editor, confirmation, bus field, day list, activity selector, explicit outcomes, manual notice editor/list/detail, save/error/conflict status, end/abort dialog, recap and fictional demo label/reset all need real keyboard/readability/contrast checks.

Record measured ratios and actual browser/device observations as pass/fail/not-run. Check long Norwegian labels, midnight dates, multiple notices, unknown fields, error recovery and enlarged text. Reuse [preparation.html](mockups/preparation.html) only with the current scope overlay in the [mockup index](mockups/README.md); reference images do not establish implementation behavior or target-device acceptance.
