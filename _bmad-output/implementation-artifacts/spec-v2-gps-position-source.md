---
title: 'Display qualified GPS speed from one shared foreground position source'
type: 'feature'
created: '2026-11-20'
status: 'in-review'
route: 'dispatch'
baseline_commit: '755b6f9c43c13bcad1eef5555d9672c8f9f50456'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Show own measured GPS speed independently of route and road datasets. Share the same opt-in location watch with the later stop and road consumers.

## Boundaries & Constraints

Use `D:/IBE160-plan-gps-speed` at `e2468abb8bf492007d9f9437698c80d88e9ca280`, in particular GPS-LAB-1, V01–V12, and explicit shared behavior in dependencies.md. Use navigator.geolocation feature detection, without browser allowlists. React owns the resource inside the selected authorized private context. No geolocation data outside bounded browser RAM or in test logs. Use synthetic measurements only. Edit only this V2 worktree. Do not stage or commit.

| Scenario | Expected behavior |
| --- | --- |
| Opt-in and supported acquisition | One watch while visible and explicitly authorized. Pause/Off or context/authority loss clears it immediately. Speed can start without a stop anchor. |
| Native speed and timing | Strict acquisition timestamp, monotonic age and two coherent native samples. Only actual native zero renders 0. Missing/invalid/old is unknown, small valid positive value renders &lt;1. Apply the planned 3000 ms and 10 s boundaries. |
| Unsupported or interrupted | Informative status for unsupported/insecure origin, denial, unavailable service or timeout, stale, low accuracy and clock jumps. Hidden/BFCache/pagehide and loss of session/workday require explicit resume. Old callbacks and old data have no effects. |
| Shared consumers | A typed local position subscription exposes fix metadata and generation; road and progression use independent profiles. Starting speed does not activate another consumer, mutate progress, or require a road limit. |

</frozen-after-approval>

## Code Map

- `PrivateAccess.tsx` owns the validated session and suspension. `PrivateConfirmation.tsx` keys `PrivateWorkdayView.tsx` by workday. Mount the shared region under the acknowledged selection in `PrivateActivitySelection.tsx`, respecting visible/available/expired/terminal state. Design a wrapper slot so route, road and progression mount as children later.
- Use `privateNow` for workday/session expiry and native acquisition/wall time plus `performance.now` for browser timing. Implement testable clock and geolocation boundaries.

## Tasks & Acceptance

- [x] Add the shared TypeScript foreground controller, speed evaluator and explicit Norwegian UI.
- [x] Add deterministic and synthetic Edge coverage at the usual private entry.
- [ ] Record physical Lenovo Brave and Chrome performance, permission behavior and owner acceptance.

## Implementation Notes

Keep public interfaces typed and iterate with parent on planned progression/road consumers. Do not edit unrelated shared components; coordinate before editing a shared line. The V2 test stack and Playwright adapter use loopback 19651–19653.

## Spec Change Log

- Validate live workday selection and lifecycle in addition to browser session. The same coordinator supplies independent stop and road consumers.

## Review Triage Log

- Patched position acquisition while the account settings hide the plan and missing scope revalidation. Registered the Node controls under `test:v2-motion`. No browser allowlist or raw-position persistence was introduced.
