---
status: approved
created: 2026-09-26
epic: E7
story: '7.5'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['7.2', '7.3', '7.4', '5.6']
---

### Story 7.5: Reopen Retained Daily Summaries from the Main Menu Within Existing Limits

As the pilot owner,
I want to find an ended day's retained summary from the main menu and read or export it while authorized,
So that I can inspect recent results without resuming ended work or creating a permanent history.

**Acceptance Criteria:**

**Given** the owner opens the retained-summary entry from the main menu,
**When** authorized local data and any available authorized server results are listed,
**Then** identify each eligible ended/aborted combined own day once, with its service date, terminal status, applicable data expiry, local availability and local/server status; use sufficient retained identity to distinguish different days sharing a date,
**And** parts of a split day and linked-person plans do not appear as separate completed own days. Prepared, active and never-ended days are not silently converted to completed summaries because a planned end time passed,
**And** show whether initial review is explicitly complete, still open or unresolved. The list itself does not close review, end a day, acknowledge pending work or confirm an outcome,
**And** provide clear loading, empty, partial/unavailable and access-required states. A failed server listing cannot erase local pending summaries or claim that no retained results exist,
**And** use readable dates, expiry and textual status labels with keyboard/focus support, following the adopted tablet-landscape/PC summary and menu presentation.

**Given** an authorized retained day is selected,
**When** its summary is opened,
**Then** resolve its stable own-day identity and one coherent permitted revision through the existing 7.3 view; do not select the most recent day or a linked person's plan merely because names/dates match,
**And** expose the existing 7.4 user-initiated PDF export when its data, assets, access and interaction prerequisites hold, retaining exact revision/provenance, uncertainty and file-handoff semantics,
**And** after explicitly completed review, provide reading/export only, with no resume-day action or renewed edit permission. Back/history navigation, direct links, refresh, another tab and stale open dialogs obey the same boundary,
**And** preserve notice-display history, manual origin, gaps and pending receipt status. Opening a summary cannot replay notice audio, mark historical versions seen, refresh their evidence or turn local saving into server confirmation,
**And** returning to the menu neither activates a prepared day nor changes another currently active day, its role, trip, progression, writer authority or retention clock. Summary viewing is not an operational context switch.

**Given** the selected ended day has an interrupted initial review,
**When** the current durable review phase is established,
**Then** offer a clearly labelled continuation of initial review only while that phase is still open and all existing 7.2 authority, writer and interaction checks permit it; ordinary summary reading remains a separate action,
**And** Back, accidental navigation, tab closure, crash or previous summary reading cannot be used as proof that review was finished. Only the explicit 7.2 completion confirmation closes it,
**And** if phase data is missing, inconsistent or an explicit completion commit is unresolved, show that uncertainty and restrict editing until resolved. An older open copy cannot override a known completion, and an unresolved phase cannot be presented as definitely completed,
**And** recovered open review remains subject to the original expiry and current permissions. This entry cannot reopen explicitly completed review or resume the ended day's operations.

**Given** the app is offline, the server is unavailable or local storage has lost data,
**When** the list or a selected summary is opened or retried,
**Then** list and read the authorized summaries actually retained locally without depending on a source refresh; expose missing local content and unavailable server verification separately,
**And** preserve existing coherent local results during partial loads, delayed responses and retries. Reconcile one day by its identity/revision and existing receipt/conflict rules, not by arrival order or an apparent newer client timestamp,
**And** if the data exists only on the server, retrieve it only through existing authenticated, unexpired summary contracts when connected. Until retrieval succeeds, do not suggest that opening/export is available offline,
**And** distinguish inaccessible or unavailable data from known expired/deleted data where the current evidence permits; do not promise recovery after browser eviction or device/volume loss,
**And** restarting the app cannot silently finish a review, replay an export or auto-start another day. Any required login/recovery uses existing E1/E5 rules, preserving unresolved revocation and permitted pending work.

**Given** a summary list, detail request or export entry is accessed,
**When** the client and backend evaluate permissions,
**Then** enforce owner and concrete-day scope for both list metadata and content. A bounded grant for one day does not authorize listing or reading other days; possession of a local record or URL is not authority,
**And** distinguish data retention from access validity. Seven-day retention does not guarantee seven days of unrestricted login; valid renewed same-owner authorization may restore access only to data that has not expired, without restarting its retention clock,
**And** pending logout/revocation locks private rows and details immediately under the existing rules. Server failure cannot silently bypass access checks, and a stale response cannot redisplay locked content,
**And** apply existing movement/actual-role rules to summary selection, review and export, including restrictions while another day is active. An ended summary or a recovered server role does not prove standstill or resolve role uncertainty,
**And** use owner-scoped IndexedDB data and authenticated FastAPI/PostgreSQL listing/detail queries over existing retained results; add only indexes/fields needed for this entry, not a second history database or new writer-transfer protocol.

**Given** a listed or open summary reaches a binding data deadline or an earlier deadline becomes known,
**When** startup, resume, running expiry checks or reconnect processes the state,
**Then** remove expired private list metadata and content through the existing AD-12 cleanup and deny further read/export independently of backend purge timing. An open summary becomes a nonprivate unavailable/expired state before further use,
**And** invalidate stale list/detail results and temporary references so that another tab, Back/history navigation or a delayed response cannot restore deleted data. Do not retain a private tombstone archive just to populate the list,
**And** enforce the original combined-day clock and any earlier applicable limit; browsing, fetching, re-login and exporting never reset it. Unverifiable end time follows 7.1's earliest-applicable-limit rule; review-open or unsynchronized status does not suspend expiry,
**And** acknowledge that a closed browser can only clean up on return, before use; do not claim exact-time deletion while it is not running. A downloaded user-held PDF remains outside app cleanup as explained in 7.4,
**And** no extra raw tracking, linked-person remainder, permanent driver history, private backups or pilot archive is introduced. The public demo remains isolated from private list/detail data.

**Given** fictional/anonymized retained days, browser clients and real PostgreSQL,
**When** the story is verified,
**Then** test multiple ended and aborted days, two identities sharing a service date, a split day crossing midnight, linked-person context and a never-ended day; list each eligible own day once without invented completion,
**And** test completed review versus interrupted open review after Back, tab closure and crash, an unresolved completion commit, concurrent completion in another tab and a stale editing link. Only a genuinely permitted open review can continue,
**And** open an older summary while a different day is active and verify unchanged actual role, trip, progression, writer authority and clocks; verify applicable interaction restrictions,
**And** test local-only pending results, partial/failed server listing, server-only results while offline, local eviction, delayed older responses, wrong owner, day-only access versus broader valid login and pending logout,
**And** test expiry while list/detail is open, startup after expiry, reconnect revealing an earlier deadline, concurrent tabs and delayed data/export callbacks. Verify cleanup in local storage and PostgreSQL and absence of expired metadata/content revival,
**And** verify readable date/status/expiry labels, keyboard focus, 7.3 evidence fidelity and 7.4 export access. These controlled cases contribute to E8-D; actual device/offline recovery and safe navigation remain E8-P qualification.

**Traceability:** Retained read/export access under FR-22/23/24, offline/recovery FR-17/20, bounded FR-1 and terminal FR-21. NFR-1–4; UX-DR23/32/33/35/36/38/39/44. EXPERIENCE retained summaries from the main menu, date/expiry and no operational resumption, as explicitly amended by the owner's 7.2 completion rule; DESIGN distinct summary/menu presentation. AD-2 local data, AD-3/4/5 existing fullstack result/revision contracts, AD-9 terminal/context boundaries, AD-10/11 access versus writer authority, AD-12 fixed retention/all-copy deletion, AD-13 demo isolation and AD-14 compatible recovery. All AD-1–AD-14 remain unchanged.

**Dependencies:** 7.2 explicit review phase, 7.3 coherent summary, 7.4 local export and existing E1/E5 access/recovery/cleanup including 5.6. Existing E3/E6 interaction and role guards remain controlling. No later closing message or full demo is required to demonstrate the main-menu entry.

**Size boundary:** One bounded retained-summary list and selection/navigation flow, with current scope/phase checks and integration of existing read/export/cleanup contracts. No new summary renderer, editor, synchronization engine, archive, search/reporting suite or day-resumption mechanism. The closing message and remaining lifecycle coverage are separate E7 work.

**Pilot qualification:** Controlled list/read/export/access/recovery cases contribute to E8-D. E8-P requires actual Lenovo/Brave navigation, offline restart, lock/expiry behavior and integrated role/lifecycle checks; E8-E remains field evaluation. The 5.4 timing-evidence decision, 7.1 ending-time uncertainty and recovered-role restrictions remain open test/decision points. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. The owner affirmed distinct own-day identities sharing a date, preservation of an open initial review, no cross-day metadata access under a single-day grant, and expiry enforcement while a summary is open. Planning approval only; the approved copy in epics.md is canonical.
