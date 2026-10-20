# Epic 9 Context: Save a Private Working-Day Draft

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Establish a reproducible local fullstack application in which the owner can sign in and save/reopen a private working-day draft, alongside an independent, bounded experiment establishing which anonymized text-PDF layouts can be supported. Only the approved SCOPE-02 course V1 governs implementation; earlier automatic-driving, offline and mentor plans are historical. The application supports preparation and consultation while stopped and distinguishes planned, manual, unknown and fictional facts.

## Stories

- Story 9.1: Establish supported imports
- Story 9.2: Run a persisted fictional day locally
- Story 9.3: Access private work
- Story 9.4: Save and reopen a draft

## Requirements & Constraints

- **Approved fixture baseline, 2026-10-20:** Jonas approved all seven anonymized PDFs and the [independent expected facts](../../Eksempelfiler/README.md). Use these for story 9.1 and downstream import; fixture preparation is complete, but extraction qualification is unexecuted. `Vogn` means vehicle duty (vognløp), not physical bus. Preserve full `960xxx` and the three-character realtime-screen value including leading zeros; actual bus remains unknown until externally obtained and manually entered. Adjacent pause types may be displayed together: any MealBreak makes the combined interval a meal break, Coffee alone remains coffee, Split break remains a split-duty break. Preserve source rows/provenance. Include the explained paid free time in example 5 and the clarified 27-minute deadhead in example 6. See the baseline for exact times and counts; no live integration is implied.

- Deliver an actual frontend/API/PostgreSQL system with documented startup, migrations, fictional seed/reset, test commands and teardown. Verify real write/read and persistence after service restart. A static demonstration is insufficient. Bind private development endpoints to loopback by default and record executable versions.
- Use only anonymized or fictional assessment data. No live feed, GPS, paid runtime account or external owner secret is required. Keep fictional assessment storage/configuration separate from private data; reset must affect only fictional state.
- Qualify text-PDF extraction against independently checked expected facts in 3–5 anonymized fixtures. Timebox the experiment to 3–4 hours; classify supported/partial/unsupported results and report a failed useful input envelope for an explicit scope decision. Manual entry cannot count as successful extraction.
- Drafts retain ordered activities, service date, explicit calendar dates/times, uncertainty and corrections. Preserve overnight/extended-hour meaning in Europe/Oslo without inferring dates from clock order. Preserve unknown codes and places. Vehicle duty, physical bus and trip identity remain separate; no invented transfers or depot assumptions.
- Provision private access without public signup. Every private operation checks session, ownership and data expiry. Fixed session lifetime is 14 days from sign-in; draft lifetime is seven days from server creation. Viewing, editing, retry or reauthentication never extends retention. Deny expired access immediately and purge related data/idempotency records on startup and at least hourly.
- Save failures retain form input while the page remains open. Stale edits cannot overwrite newer saved work. Unknown response outcomes remain unresolved until authorized lookup/retry. Reload restores acknowledged server state only; private browser persistence and offline recovery are excluded.
- Apply privacy, validation, uncertainty and error handling when each slice introduces relevant data or controls. Record actual executed evidence and limits; planning approval and mockups are not implementation acceptance.

## Technical Decisions

- Adopt React/TypeScript, a modular Python/FastAPI backend and PostgreSQL. Verify compatible supported versions and lock actual dependencies during bootstrap. Use ordinary versioned migrations; no SQLite substitute for integration or production persistence.
- Backend owns saved drafts/plans, sessions and authoritative validation. Browser memory holds unsaved forms/presentation only. No private localStorage/IndexedDB, service worker, outbox, day grant or offline synchronization engine. A non-private manual theme preference may use localStorage.
- Use UUID record identities, server-derived ownership, UTC instants and explicit Europe/Oslo service/calendar interpretation. ImportDraft includes stable ID, owner, creation/expiry, revision, ordered typed activities and field/page uncertainty/manual corrections. Activity identity is independent of line number; optional facts remain nullable.
- Mutations atomically validate ownership/session/expiry and expected revision, apply changes and advance revision. Creation uses an operation ID established before sending; replaying the same operation/payload returns its accepted result, while a changed payload conflicts. Repeated-result lookup still checks authorization/expiry. Scope operation metadata to its owner/record and retention deadline.
- Use validated request/response schemas. Return session renewal, safe access denial, conflict, validation and owned-expiry errors distinctly; private responses use no-store. Never interpret HTML/login/error responses as successful saves.
- Retain password hashing, rate limiting, opaque server-managed sessions, host-only HttpOnly cookies, explicit SameSite, CSRF and exact-origin checks. HTTPS/Secure cookies are required beyond loopback; development configuration must not silently authorize public deployment.
- Logout clears private browser presentation and invalidates the server session. An unreachable server leaves logout explicitly unconfirmed while locking local presentation; settle it before later private traffic. Back/reload and renewed sign-in cannot reveal expired or unauthorized data.
- PDF interpretation is a small external adapter boundary. Bound size/page count/time and inspect content. Process originals transiently; clean success/failure/cancel and interrupted jobs. Never persist originals, raw extracted archives or private payload logs.

## UX & Interaction Patterns

Use Norwegian, readable tablet/PC forms with labelled controls, keyboard access, visible focus and text-based status. Draft review separates interpreted, corrected and unresolved values; cancellation preserves saved work. Source previews are transient and may require reselection after reload. Show saving/saved/unsaved/unavailable/conflict/unresolved states honestly and preserve input for comparison after a stale write. Fictional assessment displays a persistent `Fiktive demodata` label. Session expiry returns to non-private access presentation.

Use restrained system-ui/Segoe UI styling and manual Day/Night where introduced. Wrap long text; do not hide critical information. Informative text requires 4.5:1 contrast, necessary non-text 3:1 and meaningful visible keyboard focus. No color-only status or implementation identifiers in ordinary product flows. Old driving/mentor/offline/PDF-export galleries are not active navigation requirements.

## Cross-Story Dependencies

9.1 and 9.2 are independent roots. If representative PDFs are unavailable, 9.2 can proceed with fictional data. 9.3 depends on 9.2; 9.4 depends on 9.3. Later reviewed import requires both the qualified input envelope from 9.1 and persisted drafts from 9.4. Deferred GPS, automatic notices, offline execution, mentor roles, advanced active-plan revision, export and public hosting are never prerequisites.
