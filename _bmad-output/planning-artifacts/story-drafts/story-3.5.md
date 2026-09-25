---
status: approved
created: 2026-09-25
epic: E3
story: '3.5'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.3', '3.4']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice renders the adopted driving hierarchy from explicit committed operational state. Deterministic component/domain fixtures exercise at-stop/between-stop states before the subsequent progression engine supplies live evidence. Operational use never receives simulated progress as a substitute.

### Story 3.5: Read the Active Trip and Three-Stop Sequence Without False Location Claims

As the driver,
I want the relevant current or next stop to dominate a stable driving view,
So that I can understand the actual trip and supported stop context with a brief glance.

**Acceptance Criteria:**

**Given** a committed actual trip selection,
**When** its driving view opens,
**Then** persistently display its route, destination/direction and clock using the accepted DESIGN hierarchy and readable landscape-tablet layout,
**And** exclude personal imported details; physical bus, vehicle duty and passenger-trip identity remain distinct,
**And** retain the always-visible Menu with 3.2's lock/reason/countdown and its existing trip-selection and Skiftdetaljer actions,
**And** trip selection alone supplies no current-stop or passage evidence; show unknown progression until supported state exists.

**Given** explicit supported at-stop state for the selected trip,
**When** the three-stop view renders,
**Then** make the current stop dominant and show the vertical sequence top-to-bottom as stop after next, next, CURRENT highlighted,
**And** omit the previous stop from this adopted at-stop baseline; do not implement the exploratory four-stop alternative,
**And** distinguish upcoming stops from current location through text roles and hierarchy, not color alone.

**Given** explicit supported between-stop state,
**When** the view renders,
**Then** make the next stop dominant and show the vertical sequence top-to-bottom as stop after next, NEXT highlighted, departed stop,
**And** identify the departed stop as past context rather than current location,
**And** rendering the state never infers departure/passage from the clock, scheduled time or a visual animation.

**Given** a confirmed sequence boundary, short route or unusable/missing stop data,
**When** the corresponding slot renders,
**Then** use the adopted dash and explicit no-more/no-previous label where the sequence boundary is actually known,
**And** distinguish that from missing/unknown information with an unavailable-data label, retaining Stoppinformasjon mangler where applicable,
**And** never invent stops, wrap the sequence to another trip or present a next-trip stop as an available stop in the current trip.

**Given** last known progress becomes uncertain or is restored without fresh evidence,
**When** the view renders,
**Then** show retained context with explicit uncertainty/manual provenance as applicable, never claiming the bus is still at the last known stop,
**And** test that retained context under unknown progression is labelled uncertain and never presented as a new position observation; preserve the adopted ordering and visual emphasis for supported at-stop/between-stop states,
**And** distinguish selected-trip certainty from location/progress certainty; a manual trip choice does not establish current position,
**And** keep route/destination and control restrictions visible through unknown-position/offline states; connectivity alone cannot refresh position or retained data,
**And** do not implement a new quality or progression engine in the view.

**Given** several initial candidates with movement-locked selection or no actual trip yet,
**When** the entry surface renders,
**Then** retain 3.4's simple unresolved/waiting status and visible permitted route to selection,
**And** do not display any candidate as the active trip or populate its driving stop sequence before selection,
**And** no modal, focus-stealing prompt or required interaction asks the moving driver to resolve it.

**Given** long Norwegian stop names, short/terminal sequences, enlarged text and day/night design tokens,
**When** the view is inspected at the intended landscape-tablet viewport,
**Then** preserve legibility, route/direction and stop-role distinction without overlapping controls, clipped essential names or confusing rearrangement,
**And** use the accepted typography/contrast and forgiving touch-target defaults; keyboard focus and accessible role labels remain understandable,
**And** validate one-to-two-second glance readability separately on the mounted device rather than claiming screenshot tests prove it,
**And** this story tests both adopted palettes but leaves persistent theme selection/Auto behavior to its own required story.

**Given** logout, expiry, a failed state read or a restored active-trip view,
**When** rendering attempts to show private context,
**Then** honor existing access/storage locks and AD-12 checks before displaying private information, preserving the established recoverable-error behavior,
**And** render the existing committed plan/selection/progress state without creating duplicate operational events, changing revisions or resetting retention,
**And** introduce no private asset-cache copy, screenshot archive or redundant database table for presentation; retain E1/E2/E3 authoritative persistence and receipt semantics.

**Given** supported current/next/departed stop state changes or retained context becomes uncertain,
**When** the accessible view communicates that change,
**Then** expose meaningful stop-role/status changes without moving focus, announcing every sensor poll or repeating unchanged announcements,
**And** test a fresh state change, identical repeated observations and restored uncertain context separately,
**And** associated notice-warning descriptions remain required E4 integration; this view does not invent a notice or its source status.

**Traceability:** FR-7 as explicitly superseded by approved UX, display portions of FR-6/9/16; NFR-1/2/3; UX-DR10/11/12/13/23/38/40/44; DESIGN typography/layout/tokens; AD-2 committed-state rendering, AD-9 shared operational state and honest evidence, AD-10/12 access/privacy. Runtime FR-8 progression and notice-driven emphasis under E4 remain later integration.

**Dependencies:** Implemented 3.3/3.4 and their shared movement/plan foundations. At-stop/between-stop/manual/uncertain states are verified with labelled isolated test fixtures; the live operational surface remains unknown until actual progression evidence is available. No future story is required to implement and test the presentation contract.

**Implementation evidence:** At-stop and between-stop role/order assertions, first/last/one-/two-stop routes, missing list versus true boundary, long names/enlargement/palettes, manual/uncertain/restored context, locked ambiguous selection, permission/status visibility and logout/expiry/read failure. Component checks verify rendering causes no operational mutation. Device glance qualification remains outstanding; no tests are run while drafting.

**Size boundary:** Active-trip/stop presentation and existing Menu integration only. No passage detection, arbitrary/manual stop controls, final-stop timer, non-passenger transitions, theme persistence/Auto, wake lock or notice ingestion. Those remain required subsequent stories.

**Pilot qualification:** Deterministic presentation evidence contributes to E8-D. Actual mounted readability in sun/darkness, live progression and integrated notices/controls/recovery require E8-P; E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the adopted ordering and visual emphasis preserved. Retained context under unknown progression is explicitly uncertain, never a new position observation. Registration recovered after the tool interruption. The owner also approved the explicit UX-DR40 meaningful stop-state announcement and unchanged-poll suppression tests at the E3 checkpoint on 2026-09-25. Planning approval only; the approved copy in epics.md is canonical.
