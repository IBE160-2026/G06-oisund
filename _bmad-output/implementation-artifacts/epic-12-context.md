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

Retain labelled forgiving controls, keyboard navigation, visible focus, meaningful screen-transition focus, long Norwegian text wrapping and enlargement. Manual Day/Night only. Verify actual text contrast of at least 4.5:1, necessary non-text contrast 3:1 and IR-01 focus requirements in included rendered states; colors alone convey no meaning.

## Cross-Story Dependencies

12.2 builds on the accepted closure, account notice and recovery contracts of 11.3/11.5/11.6. The accepted 11.5 account model overrides older per-workday wording. 12.1 owns retention/deletion enforcement; 12.3 owns broader device/theme evidence. 12.4 combines completed included slices into actual end-to-end verification, followed by 12.5 clean reproducible delivery. Do not implement deferred GPS, automatic sources, private offline storage, advanced revisions, mentor workflows, PDF export or public hosting as prerequisites.

Current integration: 12.1 uses server-issued live notice creation IDs via POST /notice-operations. Unknown, expired, deleted or foreign IDs are rejected; original accepted-command recovery remains supported through lookup-first same-ID retry. Both implementations are locally integrated under explicit owner authorization before acceptance testing. Fresh API/PostgreSQL and browser evidence lives in docs/evidence/12-integrated-handoff.md. No technical result implies Jonas has accepted either story; both remain review/in-review pending manual/physical testing.