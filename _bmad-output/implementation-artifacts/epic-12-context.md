# Epic 12 Context: Verify and Deliver the Assessable Application

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Make the included application assessable through a repeatable isolated fictional journey, executed privacy and integration checks, usable tablet/PC views and reproducible local delivery. Evidence must distinguish simulated demonstrations, actual API/PostgreSQL behavior and unperformed device or field evaluation. The application supports preparation and consultation while stopped; it does not certify standstill, road clearance, source completeness or real-world benefit.

## Stories

- Story 12.1: Enforce the retained-data boundary
- Story 12.2: Repeat a fictional assessment
- Story 12.3: Use the included views on tablet and PC
- Story 12.4: Verify the complete user flow
- Story 12.5: Deliver a reproducible submission

## Requirements & Constraints

- Keep fictional records and resets isolated from private accounts and data. A no-login demo cannot authenticate to the private API. Provide a separate actual fullstack evidence path using locally provisioned fictional assessment credentials; simulated save errors cannot demonstrate PostgreSQL correctness.
- Repeat supported import/correction, manual navigation, notice consultation, explicit outcomes and terminal closure, including unsupported input, uncertain fields/coverage, missing notice metadata, server unavailable, stale revision and lost response. No GPS, live feed, paid account, real owner credentials or real shift file is required at demo runtime. Setup may download dependencies.
- Unsupported/scanned input offers manual entry without claiming successful extraction. A new or failed import does not replace confirmed work. Expected fixture facts must be checked independently from parser output. Preserve service date, explicit calendar dates across midnight, unknown activity codes and the distinction between vehicle duty and physical bus.
- Distinguish planned, manual, unknown, fictional, unsaved and confirmed saved facts. Selection/navigation/time passage never starts a shift or records completion. Only explicit active-shift actions record outcomes; unregistered outcomes stay unknown after ending. Terminal recap is read-only and cannot resume the shift.
- Every private operation enforces session, owner and retention. Drafts expire seven days after creation; confirmed work expires at the earlier applicable fixed planned-end/server-closure bound plus seven days. Deny expired access immediately and purge on startup and at least hourly; retry/read/login cannot renew retention or recreate expired work.
- Accepted account notices have their own lifetime, independent of the original day. Original-shift closure, deletion or expiry cannot remove a still-valid notice. Required ending, pre-expiry extension only, earlier manual ending and bounded post-ending retention remain authoritative. Unknown source update/start/check facts are not invented; legacy missing-ending records require explicit completion and remain excluded from active reading.
- Originals and processing copies are transient, including failure/cancel/interruption cleanup. No private persistent browser store, service worker, payload logging, operational repository fixtures or historical private archive. Private responses are no-store; logout/session expiry clears private presentation and guards Back/reload.
- Execute and record meaningful tests, failures, limits and exact build identity. README reproduction, extraction, functional integration and rendered UI evidence are separate. No mockup or fictional result establishes field time savings, notice coverage or actual tablet usability.

## Technical Decisions

Use the adopted React/TypeScript frontend, Python/FastAPI backend and real PostgreSQL for integration; no SQLite substitute. Server state is authoritative for saved records, revisions, outcomes, sessions and account notices. Browser memory holds current edits/presentation; only the non-private manual theme preference may persist locally.

Commands use stable operation identity, expected revision and atomic validation/application. Retrying the same accepted operation/payload resolves its original result; altered content under the same identity conflicts. Stale writes preserve the proposal for comparison and never force overwrite. Lost responses remain unresolved until authorized lookup or the original retry establishes saved state. Authorization and expiry apply before replaying receipts. No HTML/login/error response means saved.

Use server UTC authority with explicit Europe/Oslo service/calendar interpretation. Ordinary versioned migrations preserve data and immutable historical receipts. Independently retained notice command metadata follows the notice's lifetime. Notice matching uses explicit line scope and planned intervals, qualifies partial validity, deduplicates one multi-line incident and preserves separately entered incidents.

Fictional and private execution use separate origin/runtime configuration and isolated storage. Demo adapters may reuse UI logic but receive no private credentials or credentialed cross-origin access. Development endpoints bind to loopback. Tests use isolated project names, ports, databases and volumes without touching ordinary services or parallel work. External activation and public exposure require separate authorization.

## UX & Interaction Patterns

Keep upload, interpretation review, day overview, selected activity, notice reader/maintenance/editor, closure confirmation and recap as distinct navigable screens. Preserve selected identity, unsaved proposals and reachable original-command recovery across safe internal navigation. Show persistent `Fiktive demodata` identification and scope reset visibly to fictional state.

Show field/page uncertainty; do not imply complete coverage. Day reading and manual selection remain available before explicit Start. Selected activity prioritizes its own planned facts and labelled previous/next boundaries. Outcome controls remain separate from selection. End/abort has explicit confirmation/cancel, saved counts and unregistered members; cancel returns focus to the originating control.

Use honest saving/saved/unsaved/unavailable/conflict/unresolved states. Preserve form input while open after failure and warn before avoidable loss; no offline restart guarantee. Notice reader separates empty stored, empty filtered and unavailable states. Entry/edit time never means source check; expiry/manual ending never proves road clearance.

Retain labelled forgiving controls, keyboard order matching reading order, meaningful screen-transition focus, long Norwegian text wrapping and enlargement without losing controls or critical information. Dialog cancellation changes nothing and returns focus to its invoking control. No essential hover-only action or required swipe. Announce meaningful save/failure changes without announcing every refresh. Selection, disabled boundaries and status need understandable labels; color alone conveys no meaning.

Manual Day/Night persists only a non-private preference. Measure all informative text, including large text, at least 4.5:1 against its actual background; necessary non-text information needs 3:1. Focus requires an area equivalent to a 2 CSS-pixel perimeter, 3:1 change on the same pixels between focused/unfocused states, and 3:1 against necessary adjacent colors; it cannot be entirely obscured. Verify actual rendered default, focused, selected, warning, error, unavailable and disabled states in both themes, including compositing, overlays and semantic icon outlines. Palette calculations alone are insufficient. Record raw ratios, environment and passed/failed/not-measured results. Browser viewport checks and static designs do not establish physical tablet usability or overall WCAG AAA conformance. No Auto, wake, GPS or PDF pass is inferred.

## Cross-Story Dependencies

12.2 builds on the accepted closure, account notice and recovery contracts of 11.3/11.5/11.6. The accepted 11.5 account model overrides older per-workday wording. 12.1 owns retention/deletion enforcement. 12.3 depends on 10.5/11.2/11.5 and owns broader device/theme evidence; pending manual acceptance of 12.1/12.2 does not block its implementation. 12.4 depends on the combined 12.1–12.3 delivery plus 11.6 and owns complete end-to-end verification, followed by 12.5 clean reproducible delivery. Do not implement deferred GPS, automatic sources, private offline storage, advanced revisions, mentor workflows, PDF export or public hosting as prerequisites.

Current integration: 12.1/12.2 are integrated in local main through f13d289. Both remain review/in-review; Jonas has not performed manual/physical acceptance of either. Their synthetic assessment environment on port 15312 must stay undisturbed by later development, which uses separate ports/data. Evidence lives in docs/evidence/12-integrated-handoff.md: its broad browser run was 477/479, followed by successful affected checks after corrections, not a newly passed complete broad run. Keep historical results distinct from new story evidence. No technical result establishes user acceptance, including for 12.3.

12.3 delivery checkpoint (27 October 2026): implementation is isolated on `story/12-3-tablet-pc-accessibility` in `D:/IBE160/tmp/story-12-3`, with synthetic frontend 15323/APIs 18323/18324. [Specification](spec-12-3-tablet-pc.md), [actual execution/review report](../../docs/evidence/12-3-handoff.md) and [manual checklist](../../docs/story-12-3-manual-testing.md) carry the technical outcome. Keep 12.3 in review pending Jonas; physical Lenovo Pad/Android/Brave and unmeasured native icon/picker/zoom/assistive-technology checks remain distinct. 12.4 remains backlog.
