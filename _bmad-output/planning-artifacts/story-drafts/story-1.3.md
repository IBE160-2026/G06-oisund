---
status: approved
created: 2026-09-25
epic: E1
story: '1.3'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['1.1', '1.2']
---

## Epic 1: Access and Recover a Private Working-Day Draft

This slice gives the owner a real, recoverable local draft while proving the already-approved access lock against actual private records. It introduces only an unconfirmed draft shell and its pending local event. Server synchronization will be a subsequent E1 slice; import, activity editing and confirmation remain E2.

### Story 1.3: Create and Reopen a Protected Local Working-Day Draft

As the pilot owner,
I want to create a dated working-day draft and reopen it without re-entering its saved details,
So that I have a private, recoverable starting point for preparing my day.

**Acceptance Criteria:**

**Given** a valid ordinary application session from Story 1.1 and no unresolved lock/revocation or access-storage error from Story 1.2,
**When** the owner opens Forbered neste skift, enters a valid service date and saves the initial draft,
**Then** the app creates an owner-scoped unconfirmed draft with a stable opaque UUID, service date, applicable IANA timezone, creation time, fixed expiry and schema identity,
**And** ownership comes from authenticated identity, not a user-editable owner field,
**And** no passenger trip, physical bus, location, confirmed plan or active-day grant is invented or activated; import and activity editing are not presented as implemented features.

**Given** the initial draft is ready to save,
**When** local persistence succeeds,
**Then** IndexedDB commits the draft and its pending typed creation event in one transaction before the UI reports saved state,
**And** the event has a stable identity and payload sufficient for subsequent synchronization without requiring future import/activity records,
**And** the UI explicitly says the draft is saved on this device and not synchronized; it never claims a PostgreSQL copy, whole-day offline readiness or backup exists,
**And** repeated submission while the save is in progress cannot create duplicate drafts/events for the same action.

**Given** an invalid or missing service date, unavailable local storage, insufficient storage space or injected transaction abort,
**When** the owner attempts to save,
**Then** an understandable error is shown, no successful save is announced and entered values remain available in the current view for correction/retry,
**And** a failed transaction leaves neither a draft without its event nor an event without its draft,
**And** retry after failure produces one committed draft/event, not a silent duplicate,
**And** the failure does not clear other local records, locks or pending revocations.

**Given** an unexpired saved local draft and valid application access for its owner,
**When** the owner reloads or closes/reopens the application and selects that draft,
**Then** the same draft UUID, service date, timezone, creation time, expiry and pending event are restored from committed storage,
**And** the initial list/detail shows unconfirmed and locally unsynchronized status plus expiry; reopening creates no extra creation event and does not extend retention,
**And** absent or unreadable data is shown as unavailable rather than replaced with an invented recovered draft,
**And** this slice does not claim offline cold-start assets or full-day recovery; browser/device qualification remains separate.

**Given** one or more local private drafts, including unsynchronized work,
**When** the owner logs out, encounters known revocation, or resumes with uncertain lock/intent storage,
**Then** Story 1.2 hides/locks draft lists and details before rendering and preserves permitted unexpired draft/event data within its existing deadline,
**And** a new login cannot discard or bypass unresolved revocation,
**And** after authoritative settlement only fresh application login by the same owner allows those drafts to be read again,
**And** another authenticated owner cannot list/read/relabel/adopt them, including by changing a draft ID or owner field in a request/action; fictional second-owner tests do not add multi-driver product scope.

**Given** an unconfirmed draft with no associated confirmed day,
**When** seven days from its original creation are reached,
**Then** the draft and its associated event/payload copies are inaccessible and deleted under the non-sliding draft-expiry rule,
**And** checks run before displaying or queuing its data at startup/resume and while the app is running; a closed browser deletes expired content before use when reopened,
**And** viewing, retrying a save, logging in or later preparing synchronization does not restart this deadline,
**And** expiry of unsynchronized work is visible in advance and expiry never marks work confirmed/completed or recreates an expired draft under a new identity.

**Given** the draft is associated with a day whose applicable AD-12 expiry is earlier than draft creation plus seven days,
**When** the effective deadline is calculated or rechecked before display, reopening or synchronization,
**Then** use the earlier deadline for the draft and all its associated payload/event copies,
**And** derive day expiry from confirmed actual end/abort or, for a never-ended day, its established planned final end interpreted with service date, timezone and explicit overnight dates,
**And** a service date alone does not justify inventing an unknown final-end timestamp; unresolved source facts stay explicit,
**And** reopening never restarts either clock and knowledge of an earlier day expiry creates no new grace period,
**And** controlled-clock tests cover the earlier-day deadline, the standalone seven-day deadline and reopening immediately before/at/after each; linked-day cases use fixtures until a real day association is introduced in E2.

**Given** two same-origin tabs saving or reopening drafts and a logout or expiry occurring concurrently,
**When** an operation resumes after a competing access/lifecycle change,
**Then** it rechecks applicable ownership, lock and expiry before exposing or committing private state,
**And** draft/event writes are atomic, identities are not reused for different content, and late UI responses do not resurrect expired data or unlock a logged-out view,
**And** this does not implement multi-device writer transfer or merge conflicts belonging to E5.

**Given** the preparation entry, draft list and draft detail,
**When** the owner uses touch, keyboard or enlarged text,
**Then** labels, focus order, pending/disabled states and validation errors follow the approved access/preparation visual and accessibility rules,
**And** unknown, unconfirmed and unsynchronized information is explicit through text rather than color alone,
**And** only interpreted/manual draft fields and access metadata are stored in IndexedDB; no source file, raw OCR, credentials or private payload appears in application-asset caches, URLs, logs or test artifacts.

**Traceability:** E1's approved minimal draft outcome; FR-1, foundational FR-2/20/24 portions, NFR-2/3; UX-DR2/3/4 (minimal unconfirmed draft subset), UX-DR23/38. AD-2 atomic local state/event, AD-5 identity/event conventions, AD-6 resumable draft fields, AD-10 ownership/logout recovery, AD-12 seven-day draft expiry and AD-14 schema identity. No claim of completed import review, full active-day recovery or complete V1 retention coverage.

**Dependencies:** Approved Stories 1.1 and 1.2. Create only the local unconfirmed draft/event stores needed for this result; no future trip/notice/mentor tables or generic event-sourcing framework. This is the minimal manually initiated unconfirmed draft supported by E1, not a seventh system-wide architecture contract. Existing authenticated server identity is used; no backend draft replica or sync receipt is claimed until the subsequent synchronization story. Local creation/reopening is independently demonstrable now.

**Implementation evidence:** Browser create/reopen/reload tests; IndexedDB transaction-abort/quota fault injection; repeated-save and two-tab cases; logout/failed lock reads/same-owner versus other-owner recovery with actual fictional draft payloads; controlled-clock tests immediately before/at/after draft expiry, including unsynchronized events and closed-browser return. Verify no unauthorized first-frame rendering and no deadline renewal. No tests are run as part of writing this draft.

**Remaining E1 and integration coverage:** A subsequent E1 story will deliver the first authenticated PostgreSQL draft synchronization with matching durable acknowledgement, retry and expiry protection; the current story remains explicitly local-only. E2 adds editable trips/activities, imported content and explicit plan confirmation. E5 expands full-day recovery and active-day authority. When a draft is associated with a day, earlier day expiry also bounds it under AD-12. This slice creates no confirmed day and does not alter that rule.

**Pilot qualification:** Local fixture evidence contributes to E8-D. It is not proof of device storage durability, whole-day offline operation, OCR accuracy or real-shift readiness. Those remain E8-P qualification, with E8-E after pilot readiness. Browser eviction can destroy unsynchronized local data; the app must not imply guaranteed durability or a server backup.

**Approval:** Approved by the owner on 2026-09-25, preserving the described scope and criteria and clarifying that the earlier applicable AD-12 day deadline takes precedence over draft creation plus seven days. Service-date interpretation must preserve known final-end facts rather than inventing an end time. Reopening never renews retention. Approval concerns planning only; the approved copy in epics.md is canonical.
