# 12.2 implementation and verification handoff

Baseline: `0bae54833f38dc3dbf041d54c324c220618c21da`. All changes remain uncommitted in this worktree. Independent root review is complete; owner acceptance and 12.1-dependent integration remain pending. See [final handoff](12-2-final-review.md). No other story status is changed by this implementation.

Implemented a separate volatile simulation entry, adapter and Norwegian screens, independent fault scenarios, proposal/receipt distinction, source uncertainty, frozen confirmed plan, explicit whole-day Start and outcome save/cancel, terminal recap, independent account notices and confirmed reset. Existing actual assessment/private entry paths are retained. Product coordination/API dependency details are documented rather than exposed in the UI.

## Matrix coverage

| Matrix | Browser evidence | Actual evidence |
|---|---|---|
| Import | Partial text-PDF unknown facts; scanned/unsupported to manual; saved snapshot survives | Not claimed; fixture endpoint only |
| Save | Edited proposal, explicit simulated receipt, immutable reopen, unavailable retention | Fixed fixture persisted/reopened in PostgreSQL |
| Conflict | Current/proposed comparison, cancel/adopt; both resources | Changed fixed-fixture replay rejected 409, original unchanged |
| Lost response | Original unresolved identity, failed/successful nonmutating lookup, save/nav disabled | Caller-discarded accepted response then same-operation replay only; no network drop/private notice claim |
| Notices | Missing start/source, future required ending/URL checks, legacy exclusion, line scope, multiline/link, independent post-closure editing | Creation/retry/lost reply pending stable 12.1 contract |
| Activity/closure | Confirm plan vs Start, selection before Start, outcome proposal/save/cancel, previous/next, end/abort cancel, terminal unknowns | Existing private semantics reused as examples only, no private mutation |
| Reset/isolation | Repeat twice, sentinel cookies/storage unchanged, zero fetch/XHR/GPS/post-load requests/pageerrors, modal cancel/Escape, reload, theme | Guarded fictional reset/reseed, populated private synthetic account/sentinel fingerprint unchanged |

## Executed evidence

- `12-2-real-20261026T214831Z.json`: first independent actual verifier, exit 0; save/replay/conflict/restart/reset and private unauthenticated denial.
- `12-2-real-20261026T215053Z.json`: strengthened actual verifier, exit 0, 18 assessment pytest cases, empty project/volume preflight and populated private synthetic reset-isolation fingerprint proof. Own containers retained for inspection.
- `12-2-frontend-20261026T215232Z.json`: production build exit 0; Windows console cp1252 printing the build checkmark failed before browser execution. Runner corrected to UTF-8; original artifact retained.
- `12-2-frontend-20261026T215243Z.json`: production build exit 0, nine task-only browser tests passed. Exact source and build hashes included. Later refinement runs retain fresh per-run evidence.
- `12-2-frontend-20261026T215347Z.json`: dedicated alias entry and genuinely keyboard-visible focus/text contrast, build plus nine browser cases passed.
- `12-2-frontend-20261026T215559Z.json`: final implementation build and ten browser cases passed, including explicit dirty-proposal discard/cancel, preserved member proposals, closure count/list, plan recap and no demo links to ordinary/private services. This is the final implementation source/build identity for root review.

Earlier interactive browser runs exposed exact-label ambiguity in fault selection/notice textarea and reset Escape focus being attempted before the modal stopped making the page inert. Explicit accessible labels and closing the native dialog before focus return fixed these; repeat checks passed. Initial sandbox npm install failed DNS and build lacked dependencies; narrow escalated locked install succeeded. Browser launch needed narrow escalation. No security settings were changed.

Fresh narrow and day/night screenshots accompany each later run; historical non-12.2 captures are untouched. Local rendered captures were inspected for readable wrapping/layout. Physical tablet, private notice admission/recovery integration and owner acceptance are not claimed.

## Post-review closure

All retained review corrections were independently reinspected. Final root build and fourteen browser cases passed; the final source/build and actual-container identity audit is in [final audit](12-2-final-audit.json). Earlier implementation runs above are historical checkpoints, not the final source identity. No private notice admission/recovery API qualification is claimed.
