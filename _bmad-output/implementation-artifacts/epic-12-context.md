# Epic 12 Context: Verify and Deliver the Assessable Application

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Make the included course V1 application assessable through repeatable isolated fictional fullstack execution and honest, executed privacy, interface, integration and reproducibility evidence. Verify existing contracts rather than introducing deferred capabilities. Functional correctness, extraction results, automated desktop checks, actual device observations and unperformed field-benefit hypotheses are separate kinds of evidence.

## Stories

- Story 12.1: Enforce the retained-data boundary
- Story 12.2: Repeat a fictional assessment
- Story 12.3: Use the included views on tablet and PC
- Story 12.4: Verify the complete user flow
- Story 12.5: Deliver a reproducible submission

## Requirements & Constraints

The application supports reviewed text-PDF or manual preparation, explicit confirmation, chronological days, manual activity selection, physical bus entry, explicit outcomes, manual account notices, terminal end/abort and a small read-only recap. Preserve planned/manual/unknown/fictional distinctions. Selection and time never imply observed location, Start or completion; closure never completes unknown activities. Existing confirmed work survives failed/cancelled imports and separate draft creation.

Use independent fixture expectations and actual API/PostgreSQL persistence, including service restart. Supported extraction, partial results and unsupported scans/images remain distinct; manual entry does not pass extraction. Assessment must require no live feed, GPS, paid account, owner secret or real shift file. No-login fictional demo is isolated from private accounts; its reset affects only fictional state. A separate fictional fullstack environment uses actual API/PostgreSQL and locally provisioned assessment credentials.

Private operations authorize the fixed server session, account owner and data retention. Sessions expire fourteen days after authentication. Drafts expire seven days after server creation. Confirmed maximum expiry is confirmed planned-final-end plus seven days; terminal server end/abort may shorten it to the earlier end/abort plus seven days. Reads, login and retries never renew data deadlines. Deny expired authority immediately, purge at startup and at least hourly, and prevent late/stale requests from recreating expired data. Outcomes and related day-operation metadata follow day retention.

The accepted 11.5 correction overrides older per-day notice language: one account-owned incident serves all eligible days and survives original-day closure/deletion/expiry. Require a future ending date; date-only means the end of that Oslo date, while exact entered clocks remain exact. Extension is accepted only before the existing deadline. Automatic expiry and earlier manual ending are terminal and distinct from explicit source checking. Retain notice history and independent command metadata seven days after effective ending, then deny/purge. Legacy missing-end notices keep their original storage bound until explicitly completed; already-ended legacy records have the one-time migration grace. Preserve immutable receipts without treating old parent metadata as current authority.

Uploaded originals and processing copies are transient and removed after success, failure, cancellation and interrupted-process recovery. Retain interpreted fields/uncertainty, not originals or raw extraction archives. No private persistent browser storage, service worker, payload logs, repository fixtures, historical backups or permanent driver history. Ordinary database deletion is logical deletion, not forensic erasure.

## Technical Decisions

Preserve React/TypeScript, modular Python/FastAPI and real PostgreSQL. Lock executable dependencies, apply ordinary versioned migrations and test populated upgrade/restart. Backend is authoritative; browser holds transient edits/presentation only. Non-private manual-theme preference may persist locally.

Writes use stable operation IDs, expected revisions and atomic validation/application. Resolve lost responses through authorized lookup or the same command; never duplicate effects, silently overwrite newer state or mark an HTML/error response saved. Preserve unresolved proposals and honest recovery state. Private responses are no-store. Logout/session expiry clears private UI memory; Back/reload checks authorization before private display. An unreachable logout locks local presentation and honestly reports unconfirmed server logout.

Use server UTC authority and explicit Europe/Oslo service/calendar interpretation, including midnight, extended-hour notation and DST. Activity identity is independent of line; source vehicle duty is not physical bus. Notice matching uses exact selected/all-line scope and planned intervals, without inferred precise stop/trip relevance, freshness, completeness or road clearance.

Private development binds loopback by default. External tablet access requires separately verified route/origin/HTTPS/session configuration; no hosting or exposure is implicit in verification. GPS, automatic ingestion, offline private persistence, mentor roles, advanced plan revisions, export, Auto theme, wake lock and field evaluation remain deferred.

## UX & Interaction Patterns

Keep separate upload, review/editor, day, selected activity, notice reader/maintenance and terminal recap screens. Preserve unsaved proposals and reachable original-command recovery across safe navigation; warn before avoidable loss. Online reload restores server-saved state only. Manual actions and terminal read-only state remain explicit.

Verify labelled controls, reading/keyboard order, meaningful focus and dialog return, disabled boundaries, long Norwegian text, enlargement and tablet/PC layout in actual states. Both manual themes must meet IR-01: informative text 4.5:1; necessary non-text 3:1; focus equivalent to a two-CSS-pixel perimeter with required 3:1 changes/adjacency and no complete obscuring. Measure rendered composited states, not only palette values. Record actual device/browser limitations; desktop automation is not Lenovo Pad/Android/Brave qualification.

## Cross-Story Dependencies

12.1 verifies earlier import, outcome/closure and notice lifetimes against the corrected cross-day contract. 12.2 builds on outcomes, notices and recovery; its fictional reset cannot cross the private boundary. 12.3 covers theme persistence and actual included UI/device evidence. 12.4 integrates recovery plus 12.1–12.3 using independent expectations and requirement/test traceability. 12.5 follows integrated verification with a clean README setup, fictional fixtures, versioned results, limitations and AI-process reflection. Proposed retrospective remedies must be triaged by relevance; existing physical-device and remote-access obligations are not inferred passes or hidden prerequisites for isolated privacy tests.
