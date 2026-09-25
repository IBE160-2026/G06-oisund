---
status: approved
created: 2026-09-25
epic: E2
story: '2.9'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.3', '2.7', '2.8']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice adds explicit work parts to initial own-day preparation and the confirmed overview. It does not revise an already active plan or implement operational progression/end/summary screens.

### Story 2.9: Prepare Split Work as One Combined Day

As the pilot owner,
I want to review each work part with its own reporting time and depot within one combined day,
So that I can prepare for later work without treating the intervening gap as a completed day or an invented transfer.

**Acceptance Criteria:**

**Given** an owned, unexpired draft contains split work,
**When** the driver reviews or corrects its work parts before initial confirmation,
**Then** allow activities to be assigned to explicit ordered parts with stable identities within the same own plan/workday,
**And** each part exposes its own reporting time and known reporting location/depot for checking and correction,
**And** a time gap or separate source file alone does not silently create a part boundary; source-supported interpretations remain reviewable and ambiguous grouping requires driver resolution,
**And** regrouping existing activities does not duplicate them, discard corrections or change their service-date/source identities.

**Given** two parts have different depots, or the later reporting location is unknown,
**When** the combined overview is displayed,
**Then** show each part's own reporting time and depot separately, leaving the unknown location explicitly unknown,
**And** show the interval between parts and the next reporting information without inventing travel, rest, meal or paid/unpaid classification,
**And** retain explicitly entered or source-supported transfers and other activities instead of replacing them with a generic gap,
**And** do not imply that the same physical bus continues into the next part merely because the plan or vehicle duty is shared.

**Given** a later part or activity crosses calendar midnight,
**When** the driver reviews, confirms, saves and reopens the combined plan,
**Then** preserve the confirmed service date and activity order with explicit calendar dates where needed,
**And** test Friday 25:30 displayed as Saturday 01:30 within its correct part without moving it to another working day,
**And** temporal/grouping ambiguity that prevents a correct sequence or planned final end requires correction before confirmation; unknown depot, bus or source match alone does not require guessed values.

**Given** the driver reviews the complete split-day draft,
**When** initial confirmation is requested,
**Then** use Story 2.7's explicit reviewed-revision confirmation for the combined plan, preserving all parts and their activities,
**And** keep every part's reporting time and depot visible in the review while confirmation, day-data coverage and the expiry deadline apply to the combined working day,
**And** a change to a part, reporting detail or activity during review requires a new review before confirmation,
**And** cancellation preserves the unconfirmed draft, and failed confirmation leaves no partially confirmed collection of parts,
**And** a confirmed unmatched trip remains permitted with its missing-data labels; confirmation cannot verify unknown facts.

**Given** the combined plan contains multiple parts,
**When** Story 2.8 prepares its data and renders coverage,
**Then** include every part's trips in the same revisioned day manifest and show coverage per trip within each part,
**And** successfully downloading the first part cannot mark the whole day prepared if a later part lacks required data,
**And** retained available data and part/reporting information can be inspected without new requests in the already available compatible application, with explicit missing/stale states.

**Given** the plan includes an intermediate depot return or the interval before a later part,
**When** preparation/overview evaluates the combined-day structure and planned end,
**Then** that boundary is not a terminal workday state, does not mark later work complete and does not start a separate completed-day retention clock,
**And** derive the never-ended day's planned final end from the final activity of the reviewed combined plan, not the first part's end,
**And** expose one workday identity for the later final end/abort and daily summary; no summary or actual completion is fabricated here,
**And** runtime entry into the gap and final end/abort behavior remain E3/E7 integration obligations, not functionality claimed by this preparation slice.

**Given** a part edit, initial confirmation or retry,
**When** local storage and server synchronization occur,
**Then** atomically persist the affected grouping/reporting facts and event using the existing local storage and authenticated PostgreSQL path,
**And** preserve stable identities through retry/reopen; only a matching valid receipt changes synchronization status to server-confirmed,
**And** test failed local writes and lost responses without duplicate parts or lost activities,
**And** apply ownership, pending-logout/storage locks and AD-12 expiry to every private part/association/event; regrouping or reopening never resets retention or revives expired data.

**Given** the split-day review and overview,
**When** used with touch, keyboard or enlarged text,
**Then** part headings, reporting times/locations, gaps and per-trip warnings remain distinguishable with accessible text and focus handling,
**And** moving an activity between parts is possible without drag-only controls,
**And** the overview retains the approved persistent clock and separates confirmed-plan, local-data and app-asset status.

**Traceability:** FR-2/4/5; preparation portions of FR-17/20/24; UX-DR6/7/12/38 and the split-day ownership boundary of UX-DR8; approved UJ-1 split-work extension; AD-2/4/5 persistence/identities, AD-6 reviewed plan changes, AD-7 whole-day data, AD-10 access and AD-12 one combined-day deadline. E3/E7 retain actual transitions, final end and summary behavior.

**Dependencies:** Implemented Stories 2.3, 2.7 and 2.8 with their prerequisites. Manual split-day entry demonstrates this independently; existing import paths feed the same editable grouping. No future revision editor, operational progression or summary implementation is required to test the initial confirmed split plan and complete manifest enumeration.

**Implementation evidence:** Two parts with different depots; unknown later depot; explicit transfer versus unclassified interval; source-file boundaries that do not equal work-part boundaries; regrouping without duplicates/lost corrections; Friday 25:30; stale-review rejection; first-part-only download; save/reopen, failed write/lost receipt, ownership/logout/expiry and accessible grouping. Check the combined planned final end and absence of intermediate terminal state in domain fixtures. Tests are specified, not run.

**Size boundary:** Initial own-day part composition and overview, reusing editor, confirmation and manifest. No active-day revision, new import engine, payroll/rest-rule inference, physical transfer verification, live progression, mentor plans or summary generation. All later V1 obligations remain assigned, with no capacity estimate or deferral implied.

**Pilot qualification:** Repeatable preparation contributes to E8-D. E8-P must integrate actual later-part continuation, offline restart, final end/retention and one combined summary on the target device before actual-shift use. E8-E remains separate field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with each part's reporting time and depot visible during review, while confirmation, data coverage and expiry apply to the combined working day. Planning approval only; the approved copy in epics.md is canonical.
