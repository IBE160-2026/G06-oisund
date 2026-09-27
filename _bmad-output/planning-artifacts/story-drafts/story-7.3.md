---
status: approved
created: 2026-09-26
epic: E7
story: '7.3'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['7.1', '7.2', '4.8', '6.10']
---

### Story 7.3: Inspect One Daily Summary with Distinct Outcomes and Evidence

As the pilot owner reviewing an ended or aborted day,
I want one readable summary of my activities, actually accompanied portions, displayed notices, corrections and source problems,
So that I can understand what was recorded without confusing planned work, manual statements and observed facts.

**Acceptance Criteria:**

**Given** an ended/aborted combined own day with an authorized retained result from 7.1,
**When** the owner opens its summary,
**Then** compose one summary from a coherent retained revision, identifying the own day and its normal/aborted end status, including all own work parts and their reporting/depot context where retained,
**And** distinguish completed, skipped, aborted, uncertain and manually confirmed outcomes using existing E3/E6/7.2 evidence rules. Planned time, position, elapsed time or closing the day cannot manufacture physical completion,
**And** passenger completion still requires the adopted registered-final-stop basis and respects explicit abort; registered manual progression remains manual evidence, not GPS evidence,
**And** preserve the service date and order through midnight while displaying calendar dates where needed: Friday 25:30 belongs to Friday's day and is Saturday 01:30 in calendar presentation,
**And** show unknown physical bus numbers, times and missing facts as unknown; distinguish physical bus, duty and trip identity. Known occurrence times and registration times remain separate, including late bus-change reports and unverifiable offline end time.

**Given** the day contains own work, accompanying periods, own driving or an acute FADDER takeover,
**When** these outcomes are presented together,
**Then** visibly separate own planned activities and driving, actually accompanied portions and manually reported takeover segments; a reviewed copy of another person's plan is not that person's confirmation,
**And** preserve separate A–B–A periods, their actual observed scope, observation gaps and the exact plan revisions underlying them. A newer linked plan cannot replace historical evidence or resolve an unresolved link,
**And** a partial accompanied trip does not become a whole completed trip or own driving. A later recovered stop cannot prove that the 100-metre goal was met during an observation gap,
**And** exclude discarded/unaccompanied remainder under AD-12. Missing evidence stays visible as missing rather than being filled from the other person's full plan or a newly fetched source.

**Given** retained notice-display records, manual corrections and source-problem records exist,
**When** the summary composes its evidence sections,
**Then** include relevant notices actually displayed, linked to their exact source version, day/context and recorded presentation kind; distinguish preview from actual-trip context and heading presentation from displayed detail where the evidence supports it,
**And** fetching, queuing, an attempted rejected view or an audio attempt alone cannot establish displayed content. Seen, Registrert and manually hidden statuses remain separate version-specific driver states and do not prove understanding or change source facts,
**And** preserve retained source identity, validity/update information and known gaps. Do not present a fetch time as a source publication time, or a failed/partial source response as proof that no notices existed,
**And** present manual corrections and source problems with their retained context and provenance, without turning corrections into source/GPS evidence or assigning earlier observations to a guessed bus/person,
**And** summary reading does not change historical operational seen/registered states, replay sound, restart notice timers or fetch a newer notice version to silently replace what was displayed then.

**Given** the retained result includes locally saved confirmations or unresolved synchronization,
**When** the summary loads, refreshes or recovers offline,
**Then** use the existing owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL result contracts to read one consistent permitted basis, extending only fields/projections needed for this summary,
**And** display locally saved, server-confirmed and unresolved receipt/conflict status accurately. Only the existing matching-receipt rules establish server confirmation; network availability alone does not,
**And** a failed/partial load cannot erase available results or mix incompatible revisions into an apparently complete summary. Identify unavailable sections or retain the last coherent authorized view with its revision/status visibly stated,
**And** integrate a newly accepted review event coherently while preserving its manual provenance; a delayed older response cannot overwrite it. Do not create a new evidence collector, separate history database or independent synchronization protocol,
**And** render the summary offline from permitted retained data without needing the original import files or fresh source access. Absent local data remains unavailable, not reconstructed by guessing.

**Given** the initial review is still open, explicitly finished, or its phase is unresolved,
**When** the owner uses the summary and available review entry,
**Then** permit eligible editing only through 7.2 while its durable current phase and authority allow it. Summary navigation, Back, closing the tab or restart alone never consumes review continuation,
**And** explicit review completion first shows remaining uncertain activities and follows 7.2's guarded confirmation. Thereafter the summary is read-only; unresolved phase restricts editing until resolved, without claiming that navigation closed it,
**And** summary rendering never resumes the ended day, starts another day, changes end time, extends a deadline or resolves unknown physical role. Existing interaction restrictions still apply,
**And** use the adopted readable tablet-landscape/PC summary layout with textual outcome/provenance labels rather than colour alone, accessible keyboard/focus behavior and clearly associated local/server and missing-data messages. PDF, closing affirmation and the retained-day selection browser are separate later slices.

**Given** summary data is read, cached, refreshed or expires,
**When** client/backend enforce access and lifecycle,
**Then** authorize owner/day scope, enforce logout and pending-revocation locks, and apply the existing AD-10/12 limits to result and any derived summary copy; show applicable expiry without starting a fresh clock,
**And** unverifiable local end time cannot extend retention/access; the earliest applicable deadline continues to apply under 7.1. TIME-01 implementation and role-uncertainty rules remain unresolved by presentation,
**And** expiry/terminal guards prevent an old tab, cached response or older local snapshot restoring deleted content. No raw source file, extra movement archive, private historical backup, driver score or cross-account summary is introduced,
**And** private operational summaries remain separate from fictional/anonymized demonstration data.

**Given** fictional/anonymized mixed days, browser clients and real PostgreSQL,
**When** this slice is verified against a known retained-result fixture,
**Then** compare every summary section with the fixture for normal and aborted days, split work parts crossing midnight, unknown bus/time, uncertain and manually confirmed non-passenger activities, skipped/aborted passenger trips and known final-stop outcomes,
**And** test A–B–A, partial accompaniment, own driving/takeover segments, observation gaps and old-active/new-linked revision history; prove that neither whole-trip completion nor unaccompanied remainder is invented,
**And** test two displayed versions of one notice, heading-only versus detail, preview versus actual context, fetched-but-never-displayed notices, unknown metadata and partial/failed sources. Reopening the summary must neither play sound nor alter historical driver statuses,
**And** test pending manual confirmation, lost receipt, partial load, delayed old response, offline restart, explicit review completion versus interruption, wrong owner, pending logout and expiry across simultaneous tabs,
**And** inspect local/server data for coherent revision/provenance and cleanup, and verify readable textual states and keyboard navigation. Record controlled evidence for E8-D without claiming actual device/source qualification.

**Traceability:** Summary composition portion of FR-22; offline/recovery FR-17/20, bounded FR-1/24 and retained FR-21 terminal outcome. NFR-1–4; UX-DR23/31/32/33/36/38/39/44. EXPERIENCE summary permissions, outcome uncertainty and accompanied-only evidence; DESIGN summary layout and distinct states. Owner clarification in 7.2 governs explicit review completion. AD-2/4/5 local/server evidence, AD-7/8 source/display provenance, AD-9 outcome/context invariants, AD-10/11 bounded access and explicit conflicts, AD-12 trimmed retention and AD-14 compatible data. AD-1–AD-14 remain unchanged.

**Dependencies:** 7.1 retained terminal result, 7.2 review-phase/manual confirmation, existing E3/E4 evidence through 4.8, E5 settlement contracts and E6 scoped evidence through 6.10. Works using already available records and a direct ended-day entry; no future PDF, closing screen or retained-day browser is needed.

**Size boundary:** One daily-summary read model and screen over existing evidence, with coherent local/server rendering and access/expiry integration. No new operational engine, source adapter, generic editor, PDF generator, affirmation bank, historical browser or permanent archive. Implement only the database projection/query changes this view needs.

**Pilot qualification:** Controlled coherent-summary, provenance, offline, access and lifecycle cases contribute to E8-D. E8-P still requires actual Lenovo/Brave readability and integrated end/review/summary/export/expiry checks; source and observation coverage cannot be inferred from a correct renderer. E8-E remains real-workday evaluation. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. The owner affirmed distinct planned facts, observations, manual confirmations and uncertainty; only actually recorded notice presentation is represented as displayed, and summary reading does not close initial review. Planning approval only; the approved copy in epics.md is canonical.

**TIME-01 amendment (owner, 2026-09-27):** The ordinary retained daily summary for a day approved before E remains viewable after E only for its owner/day within the grant, effective D and earlier access caps after trusted time/status control. Show activation approval, offline closure settlement and summary receipt states separately; a server-approved start alone does not confirm later results. An unresolved or rejected local start is not a server-approved summary. After rejection, only a distinct still-permitted local-result review under 7.4 may be offered following fresh same-owner login and trusted checks. Test list/detail labels and blocked unknown-time/expired states.
