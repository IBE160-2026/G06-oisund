# Epic 11 Context: Consult Activities and Manually Maintained Notices

<!-- Compiled from planning artifacts on 2026-10-24. Edit freely. Regenerate with compile-epic-context if planning docs change. Sources: active epics.md; current product brief, PRD, ARCHITECTURE-SPINE, EXPERIENCE and DESIGN; current sprint status and accepted Epic 10 retrospective follow-up for continuity. -->

## Goal

Let the driver consult the intended activity, explicitly record outcomes, maintain source-linked notices and recover honestly from failed online saves. The website supports preparation and consultation while stopped; it neither senses movement nor provides live driving guidance. Preserve the approved Course V1 scope and distinguish planning requirements from executed delivery evidence.

## Stories

- Story 11.1: Choose the intended activity
- Story 11.2: Understand the selected activity
- Story 11.3: Record outcomes and close
- Story 11.4: Maintain a planned notice
- Story 11.5: Read line/date notices
- Story 11.6: Recover from an unavailable server

## Requirements & Constraints

Identify activities by stable activity ID, independently of line number. Direct and previous/next selection must distinguish route, direction/destination and explicit departure date/time, including adjacent lines 20/24 and midnight. Include non-passenger activities in navigation. Restore the last acknowledged server selection after authorized online reload. Schedule time, proximity, navigation and selection never infer location, activation, arrival or completion.

Preserve planned service date separately from explicit calendar instants in Europe/Oslo. Unknown places and missing facts remain unknown; do not fabricate stops, transfers or a later work period's depot. Physical bus, vehicle duty and passenger trip remain separate identities. Selection and bus changes do not rewrite confirmed source facts.

Outcomes remain unregistered until an explicit manual action records completion, skipping or interruption. End/abort requires confirmation with clear cancellation; atomically record terminal status/server time/deadline once, never silently complete remaining activities, and never resume or edit after closure. Recap remains read-only within retention.

Notices belong to a workday. Real entries require a title, explicit line tags and an HTTP(S) original-source link. Source-update time and validity may be unknown. Entry/edit time is separate from source check; only an explicit check action sets checked-at. Match lines against the confirmed day and known validity against its planned intervals. Exclude known non-overlap; retain unknown/partial validity as a qualified candidate. Show a shared notice once with all matching lines, while separate incidents stay separate. Empty, unavailable and unchecked states must not imply clear roads, complete coverage or precise current-trip/stop relevance.

No GPS/stop progression, automatic sources, movement locks, private offline persistence, mentor flow, advanced plan revision, export, sound, Auto theme or wake lock is prerequisite work. Meaningful API/database, failure and rendered-browser evidence is required; fictional examples and device limitations must be explicit.

## Technical Decisions

Retain React/TypeScript, modular FastAPI and PostgreSQL with ordinary versioned migrations. The backend owns saved state; browser memory holds current presentation and unsaved proposals only. Do not persist private content in localStorage, sessionStorage, IndexedDB, a service worker or recovery queue. A theme preference may be persisted only as non-private data.

Use server-derived ownership, UUIDs, typed request/response validation, expected revisions and atomic mutation checks. Check session, ownership and expiry before accepting writes or returning prior accepted effects. Stable operation identities and authorized status lookup/same-payload retry resolve uncertain responses; different content with an accepted identity conflicts. Stale writes preserve the proposal and offer explicit reload/comparison without force overwrite or automatic merge. HTML, malformed or lost responses never establish success.

Use meaningful unauthorized, denied, conflict, validation, expired and unavailable responses; private responses are no-store. Bind requests to the displayed account/session and discard stale replies after identity changes. Logout/session expiry clears private presentation; Back/reload revalidates. An unreachable-server logout stays explicitly unconfirmed and locks local presentation. No-login fictional data remains isolated from private API/storage.

Confirmed retention is bounded by planned final end plus seven days; terminal end/abort can shorten it to the earlier server-end-plus-seven-days bound. Reads, edits, retry and sign-in never extend expiry. Deny immediately at expiry and purge related mutable state and operation metadata on startup/hourly. Late requests cannot recreate deleted or expired work. Preserve existing saved records with additive migrations and test actual PostgreSQL/API restart behavior.

## UX & Interaction Patterns

Owner refinement for 11.2, 2026-10-24: separate upload, control/edit, confirmed day and selected activity screens with clear forward/back navigation. Day may scroll; activity shows only its relevant facts and previous/next, with accessible long/enlarged content. Preserve registered data, saved selection, unsaved input and reachable unresolved-command recovery across safe internal navigation. Keep existing security/loss guards. Start/bus stay naturally day-accessible; navigation never starts/completes work. Future notices are day-linked (11.4/11.5), end/abort/recap belongs in day/shift navigation (11.3); do not implement those destinations yet. Intermediate stops are post-V1 and demo expansion stays later planned work. Canonical epics, V1-11 and UX spines record the same refinement.

Keep one chronological day list and one prominent selected activity; notices are secondary. Label the selection `Valgt tur` or `Valgt aktivitet` and `Manuelt valgt`. Show clear direct-choice and previous/next actions with explicit disabled boundary labels. Line number alone is insufficient. No current/next stop, location marker, GPS timer or implied road confirmation. Separate selection from outcome actions and keep internal operation/revision details out of ordinary copy.

Show saving, saved, unsaved, unavailable, conflict and unresolved states honestly. Preserve input while the page remains open after failure, offer bounded actionable checking/retry and warn before avoidable loss; no offline restart guarantee. Cancellation preserves saved data. Use labelled keyboard/touch controls, meaningful focus, non-color selected/disabled cues, long-name wrapping and enlargement without hiding critical information. Start with 58px control height, 8px corners and 2px borders; verify actual layout.

Apply manual Day/Night and measure rendered text at least 4.5:1, necessary non-text at least 3:1, and visible focus equivalent to a 2px perimeter with 3:1 focused/unfocused and necessary adjacent contrast. Record actual-device evidence separately from viewport emulation and owner acceptance.

## Cross-Story Dependencies

Owner decision, 2026-10-24: 11.1 owns explicit `Start skift`, persisted server start status/time and idempotent recovery, independently of selection. Activities may be consulted/selected before start. Selection never starts or completes work. Planned start and actual first server-accepted manual start remain separate. 11.2 reuses selection/lifecycle; 11.3 extends that lifecycle for outcomes/terminal closure/recap without duplicating Start. 11.6 adds integrated recovery while basic write integrity belongs to 11.1 now. See the approved 11.1 specification for executable scope. Jonas explicitly accepted 11.1 on 2026-10-24 and subsequently authorized commit/push; later stories were backlog at that acceptance checkpoint.

Current 11.2 execution, 2026-10-24: separate preparation/import review/editor/day/activity screens and expanded selected facts are technically complete and independently reviewed. Root verification passed 302 API tests, exact restart/migration preservation, build, all 284 browser tests and five verifier controls. Retained findings are fixed, including independent retained-plan/new-confirmation expiry and reachable asynchronous navigation recovery. Jonas explicitly accepted 11.2 on 2026-10-25, reporting that it works well and is much clearer. Specification and sprint story are done; Jonas subsequently authorized commit/push on 2026-10-25; the next story remains unstarted. Later stories stay backlog and are not started. See [11.2 specification](spec-11-2-understand-the-selected-activity.md) and [executed evidence](../../docs/evidence/11-2-selected-activity.md). Actual iPad/Safari/theme-persistence obligations remain in 12.3/12.4.

This allocation is also recorded in canonical `planning-artifacts/epics.md` and the V1-10 planning copy; other story scope and start status remain unchanged.

11.1 follows the accepted 10.5 confirmed day overview; 11.2 builds on selection; 11.3 builds on selected-activity consultation. 11.4 needs private access from 9.3; 11.5 needs 10.5 and 11.4. 11.6 integrates recovery across drafts, outcomes/closure and notices. Integrity, access and truthful failure handling apply when each write is introduced, even before the integrated recovery story.

Epic 10 and its amended A1–A3 follow-up are accepted: preserve frozen imported baselines, common bus representability, passenger-only fresh review decisions, legacy receipt/policy compatibility and neutral source markers. Do not reopen these decisions or broaden parser qualification. Theme persistence and actual iPad/Safari verification remain open obligations under 12.3/12.4. Cross-window identity and transaction boundaries remain regression priorities; shared service/restart/browser verification runs sequentially against synthetic disposable data, preserving ordinary accounts, database volume and secrets.
