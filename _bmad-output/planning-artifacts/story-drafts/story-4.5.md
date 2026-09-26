---
status: approved
created: 2026-09-26
epic: E4
story: '4.5'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['4.4', '3.2']
---

## Epic 4: Understand Relevant Notices and Their Sources

This slice delivers the combined-day notice overview, permitted detail/original-source access, exact-version seen state and confirmed-closure retention in that overview. It uses the already implemented source lifecycle and relevance contracts. Prominent driving warnings, Registrert/dismissal, manual removal of uncertain notices and sound remain separate required slices.

### Story 4.5: Review Whole-Day Notices with Source Metadata and Persistent Version State

As the driver,
I want to review the distinct notices for my confirmed working day, open their details when permitted and retain which versions I have opened,
So that source facts, changes and confirmed endings remain understandable through repeated retrieval and reopening.

**Acceptance Criteria:**

**Given** an authorized confirmed combined working day and 4.4's relevance results,
**When** its shift overview/Skiftdetaljer is opened under the shared movement policy,
**Then** show a readable heading for each distinct applicable or explicitly uncertain day-related incident, including several separate notices on one line,
**And** show one shared incident once with all supported line/trip/time associations across work parts; preserve separate incidents even when titles are similar,
**And** retain uncertainty about date, direction, repeated stop occurrence or coverage beside the relevant association; do not promote it to a verified match through presentation,
**And** use the adopted overview composition, persistent clock, Day/Night tokens and text/symbol status rather than hiding source/relevance limits behind color alone,
**And** no unconfirmed plan or raw unfiltered regional source list is presented as confirmed-day notices.

**Given** a new, unchanged or materially updated version of an incident,
**When** the list renders from committed day-specific version state,
**Then** new and changed versions are bold until that exact version has had its content actually displayed with valid access and its seen state successfully recorded; changed versions also use the adopted semantic color treatment and an explicit changed cue,
**And** after the actual authorized content display is successfully recorded for that exact version, remove its unseen bold emphasis without declaring understanding, source confirmation or acknowledgement,
**And** identical polls, changed retrieval time, plan/context switches and restarting the app do not turn an unchanged previously seen version into unseen/new,
**And** a genuinely changed version is separately unseen even when an earlier version was seen; preparing the same day and later starting it do not reset its notice state,
**And** repeated presentation is not a new source receipt or a sound trigger.

**Given** a heading whose detail is opened,
**When** the exact displayed version and its applicability are presented,
**Then** show the source body safely as data, original source/link or identifier, validity periods, nullable source update time and last successful retrieval with distinct labels,
**And** show Kildens oppdateringstid er ukjent when absent, and leave other missing facts visibly unknown; never replace source time with fetch time,
**And** distinguish source lifecycle, match uncertainty, stale retained content and retrieval/processing failure; neither opening nor refreshing detail certifies current real-world conditions,
**And** source-link actions use validated URLs and existing movement permission; a missing or unreachable original stays unavailable rather than silently linking to an unrelated notice,
**And** opening detail does not register, hide or dismiss a warning and does not modify the source incident.

**Given** a detail action for version A while version B arrives, a plan/context changes or movement begins,
**When** the action renders or its seen-state write commits,
**Then** recheck permission and owner/day/version context so only the exact version whose content was actually displayed with valid access can be marked seen,
**And** do not silently replace the opened content and mark an unseen newer version seen; indicate that an update is available while preserving which version was reviewed,
**And** a newer version remains unseen until separately opened, and a delayed action cannot mark every version of the incident seen,
**And** motion closes restricted content immediately, cancels uncommitted actions and returns focus to an appropriate visible control without undoing already committed seen evidence,
**And** source refresh cannot reopen collapsed detail, steal focus or require a response while moving.

**Given** a request to open a notice version is rejected, loses access, fails to load/render its content or is closed before the content is displayed,
**When** the action or a delayed display callback is processed,
**Then** do not mark that version seen; a click, loading shell or heading alone is not actual content display,
**And** test a movement-rejected click, access rejection, closure before content appears and version A replaced by B before display: record seen only for an exact version actually displayed with valid access,
**And** a late callback from hidden/closed or unauthorized content cannot manufacture seen evidence; preserve the existing unsaved-status behavior if a valid display occurs but its persistence fails.

**Given** the client first accepts a source-confirmed closure for an incident retained in the day,
**When** that closure transition is durably registered,
**Then** atomically preserve its stable source transition identity and first client registration time, immediately remove active-warning eligibility, and show the overview entry struck through with an explicit ended label,
**And** keep it in the overview for ten minutes from that first persisted client registration, then remove it from the overview while retaining required day evidence for the later summary,
**And** source closure time, backend receipt, opening the overview or repeat polling do not replace that first registration time,
**And** duplicate closure delivery and reload do not restart the interval; test just before/at/after ten minutes, suspended/reopened views and repeated closure messages,
**And** use trustworthy elapsed-time handling across restart/clock changes; if timing cannot be established, show the uncertainty rather than inventing an expiry or starting another ten-minute period,
**And** valid newer source reopening uses 4.3's supported new state; an old timer cannot remove a reopened or otherwise superseding version.

**Given** expired validity, uncertain disappearance or failed/partial source retrieval without confirmed closure,
**When** the overview updates,
**Then** do not apply confirmed-ended strike-through/removal merely because validity elapsed or the incident was absent from a fetch,
**And** retain unexplained disappearance with Status usikker – sjekk originalkilden and permitted source access; missing data/failure cannot erase earlier information,
**And** before any usable source data show Avviksinformasjon utilgjengelig – sjekk originalkilden rather than an empty all-clear list,
**And** a complete valid query with no matching notices may report that scoped result with coverage/time limits, never a clear-road or complete real-world-coverage claim,
**And** a failed source/processing area cannot erase unaffected notices or remain indefinitely marked as loading; future manual removal remains a separate explicit action, not implemented here.

**Given** receipt, overview display, detail opening or closure registration changes private day evidence,
**When** the client saves that change,
**Then** persist the necessary exact notice version/snapshot, first receipt, actual display/opening evidence and closure registration with stable identities, separately from source facts,
**And** distinguish received data from actually displayed/opened data; downloading a notice cannot fabricate that the driver saw it or that it was shown during a trip,
**And** commit the local state and required outbox event atomically before claiming the associated status saved; no per-poll/per-render event spam or duplicate first-receipt/closure events,
**And** local failure shows unsaved status and retry without falsely clearing durable unseen state or claiming retained evidence is safe,
**And** use inherited authenticated FastAPI/PostgreSQL owner/day/revision checks and immutable retries; only a valid receipt matching the sent batch marks server confirmation,
**And** server/network failure does not discard a successful local commit, and source polling cannot overwrite local exact-version interaction state.

**Given** the list/detail is reopened from locally retained data during a network outage or after compatible restart,
**When** existing authority permits access,
**Then** restore the same day-specific seen state, retained notice versions and original closure deadline without making old data fresh,
**And** distinguish known retained content, unavailable detail and stale source status; never require a new fetch merely to read already retained permitted content,
**And** if a required private state read fails, report the failure rather than resetting the notice to new/unseen or inventing a saved closure time,
**And** logout, known revocation and existing expiry/storage locks prevent private rendering; full offline application boot and active-day authority qualification remain E5,
**And** reusing the cache cannot reset the movement startup/outage history or silently start a completed day.

**Given** all list/detail/source actions and dynamic status changes,
**When** tested with touch, keyboard, enlarged text and assistive technology,
**Then** keep long titles, multiple associations and source/status labels readable in the adopted tablet layout without shrinking essential text to fit,
**And** follow 3.2's reliable-standstill and separately labelled startup/outage exceptions; source access has no bypass and this story does not implement mentor exceptions,
**And** focus enters detail, returns on closure/cancellation and never remains in hidden content after motion; labels expose expanded, seen/unseen, changed, ended and uncertain states without color alone,
**And** announce meaningful changes without every poll/countdown repetition, automatic scrolling, modal intrusion, focus theft or audio,
**And** keep the whole-day overview distinct from the later headings-only active-driving presentation.

**Given** retained source snapshots, interaction evidence or a source-cache prune,
**When** cleanup/access checks occur,
**Then** protect all private day associations and evidence with the existing ownership and AD-12 expiry, including local and PostgreSQL copies and pending payloads,
**And** neither reading, new retrieval nor ten-minute overview removal extends the private-day retention clock; overview removal is not summary-evidence deletion,
**And** preserve exact versions already needed by the unexpired day even when public source cache changes, without a permanent in-app notice/driver archive,
**And** retain the minimum evidence needed for E7 to describe what was displayed/opened and its source/provenance; no proof of reading comprehension or raw movement trace is inferred,
**And** no private payload, credential or operational identifier leaks to the fictional demo, public assets or published test evidence.

**Traceability:** FR-12 preparation/whole-day overview; FR-13 source metadata; FR-14 heading/detail, exact-version seen and confirmed-ended overview lifecycle; FR-16 movement restrictions; bounded FR-17/18/19/20 retained/failure behavior and FR-22 origin-time evidence. NFR-1–4; UX-DR1/9/12/14/19/23/38/39/40/41/44; adopted DESIGN notice/overview treatments. AD-2/4/5 local atomic state, PostgreSQL and matching receipts; AD-7/8 source versus client state; AD-9 shared permission/context; AD-10/12 access/retention; AD-14 compatible recovery. Registrert/manual hiding and audio remain separate requirements.

**Dependencies:** Implemented 4.4 with its qualified 4.1–4.3 data/identity/lifecycle foundations and E2 overview, plus 3.2 movement/focus policy and inherited E1 persistence/access. No future driving-warning, acknowledgement/audio or E7 report screen is needed to demonstrate this overview and persisted evidence; E7 consumes it later.

**Implementation evidence:** Multi-line shared notice plus distinct same-line incidents, uncertainty including repeated stop occurrence, new/seen/updated versions, immutable A-open/B-arrives race, safe source display/link failures, standstill/moving/startup/outage interactions and focus; closure ten-minute boundaries/reload/clock uncertainty/reopening versus stale timer; validity expiry versus uncertain disappearance versus confirmed closure; first-fetch failure and partial recovery; atomic local/outbox failure, lost/mismatched receipt, duplicate deliveries, offline view reopen, private access and expiry. Use real PostgreSQL integration and labelled source cases; actual mounted readability remains qualification. Tests are planned, not run.

**Size boundary:** The existing combined-day overview's notice list/detail, exact-version seen state, confirmed-ended ten-minute retention and their required evidence/persistence. No prominent active-driving warning layout/approach triggers, Registrert/swipe acknowledgement, manual hiding of uncertain notices, sound, mentor interface, full offline shell or summary/PDF UI. Those remain subsequent required slices rather than controls falsely shown as implemented.

**Pilot qualification:** Repeatable overview/persistence/failure behavior supports E8-D. E8-P additionally requires actual source/device readability, source access under movement rules and integration with full offline/authority and driving notice behavior. E8-E remains subsequent real-shift evaluation. Planning approval does not establish tested usability or source coverage.

**Approval:** Approved by the owner on 2026-09-26 with seen status requiring actual display of that exact version content with valid access. Rejected presses and views closed before content appears do not mark it seen. Planning approval only; the approved copy in epics.md is canonical.
