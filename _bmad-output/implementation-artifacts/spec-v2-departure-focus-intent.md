---
title: 'Preserve a newer focus choice during departure lookup'
type: 'bugfix'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** An accepted departure response focuses its heading even when the user has moved to a different control during the request.

**Approach:** Preserve newer focus and keep the committed heading handoff for a normal explicit selection. Browser focus falling back to the document when the select is disabled should still allow the usual heading handoff. Exercise both paths through the existing route workflow in Edge, Firefox and WebKit.

</frozen-after-approval>

## Implementation Notes

- Both route source variants reproduced the fault in Edge before the code change. The fixture held the journey response, confirmed that the user had clicked into `Buss/vogn`, then released the response. The existing build focused the heading.
- `DraftRouteReview` keeps the focus intent with the departure request generation. A later focus event on another control clears it. The normal handoff still occurs when the browser drops focus to the document because the select is disabled. The layout effect consumes the intent at the same point where it focuses the committed heading.
- The two route tests use held responses for the ordinary and competing-focus cases. They check active focus before release, preserve mouse and keyboard choices, and still exercise the route selection and uncertain save workflow.
- The first build with the correction passed 33 browser tests across Edge, Firefox and WebKit, including route, notices, stop progression and GPS speed. After review, TypeScript/Vite and all six route tests passed with the additional disabled-select and Tab assertions. The 18 deterministic motion tests passed. The browser cases use synthetic data. The page-focus check uses standard browser focus detection. [HTML focus model](https://html.spec.whatwg.org/multipage/interaction.html#dom-document-hasfocus-dev).
- Repeat the final route run from `frontend` with the opt-in browser setup recorded in [the previous focus fix](spec-v2-route-heading-focus.md) and `npx --no-install playwright test v2-route-reference -c playwright.v2.config.ts`.

## Review Triage Log

- Medium, patched. The committed heading receives focus only if the document itself still has focus. This covers the case where the response arrives while focus is outside the page.
- Low, patched. The ordinary handoff waits for a held response and confirms the disabled input, document or select focus, and absence of the heading before release.
- Medium, patched. The rechecked-source fixture uses Tab during the delayed request and verifies that the resulting enabled control still has focus after the new heading renders. The original-source fixture exercises the mouse.
