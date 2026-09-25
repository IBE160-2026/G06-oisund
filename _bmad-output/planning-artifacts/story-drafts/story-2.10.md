---
status: approved
created: 2026-09-25
epic: E2
story: '2.10'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.3', '2.6', '2.7', '2.8', '2.9']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice delivers a reviewed, additions-only manual revision of the confirmed own plan. It is independently demonstrable before active driving exists; preservation of operational state is tested with domain fixtures. E3 later integrates the same revision action with its movement policy and active driving, without introducing a second revision engine.

### Story 2.10: Review and Confirm Manual Extra Work in the Existing Own Day

As the pilot owner,
I want to add extra trips or activities through an explicit comparison with my confirmed plan,
So that additional work joins the correct day without replacing existing work or silently changing my active trip.

**Acceptance Criteria:**

**Given** an owned, unexpired, nonterminal confirmed own plan and permitted access,
**When** the owner opens manual extra-work entry from the shift overview,
**Then** show the target own day/plan and an additions-only scope throughout editing, comparison and confirmation,
**And** create a separate unconfirmed revision draft against its base plan revision, using existing activity fields and stable proposed identities,
**And** never create a new workday merely because work is added later or to another part; unrelated plans remain untouched.

**Given** proposed additional trips or other activities,
**When** the driver edits and reviews them,
**Then** preserve service date, explicit overnight representation, placement in the combined day and intended work part,
**And** use the existing matching and unknown-data rules: retain manual corrections and source discrepancies, allow reviewed unmatched trips and never fabricate stops, locations or physical bus,
**And** resolve ambiguity preventing correct identity, sequence or planned final end before confirmation,
**And** show possible overlap with an existing activity for explicit resolution rather than silently duplicating or merging it; equal line number/time alone cannot prove identity.

**Given** a manual additions draft ready for comparison,
**When** the driver opens review,
**Then** clearly distinguish added activities from unchanged existing activities and show their placement with each affected part's reporting time/depot,
**And** this additions-only operation cannot propose removals or silently modify existing activities, reporting facts, manual corrections or performed evidence,
**And** show any proposed change to the combined planned final end and resulting never-ended-day expiry before confirmation,
**And** cancel or failed matching leaves the currently confirmed plan in force and the driver's permitted draft recoverable.

**Given** the driver has reviewed the additions against a specific base plan revision,
**When** explicit confirmation occurs,
**Then** atomically apply only the reviewed additions, increment the plan revision and persist the typed revision event with its provenance before showing local success,
**And** if the proposal or relevant base plan changes during review, require a new comparison/review; no last-write-wins replacement,
**And** repeated confirmation/retry uses stable identities and cannot apply the additions twice,
**And** rejection or failed local commit leaves the prior confirmed plan intact.

**Given** an operational-state fixture with performed activities and a manually selected active trip,
**When** the revision is applied,
**Then** preserve performed evidence, active activity/tracking identity, manual pin, progression and corrections; adding an earlier scheduled trip is not an automatic context switch,
**And** no added activity is marked performed merely because its scheduled time has passed,
**And** terminal or expired days reject additions without resurrecting the day,
**And** operational entry and confirmation must ultimately use E3's shared movement permission; no UI path may bypass it. Before that integration exists, demonstrate this slice in preparation and domain fixtures, not as a qualified in-vakt feature.

**Given** the new revision is locally confirmed,
**When** data coverage is displayed or refreshed,
**Then** bind coverage to the new plan revision, preserve still-valid downloaded data for unchanged activities and expose missing data for additions,
**And** previous whole-day coverage cannot remain complete merely because the old revision was prepared,
**And** offline manual additions can be saved when existing access permits, but never-downloaded source data stays missing; source retrieval waits for connectivity,
**And** expose the revision for later notice-relevance integration without fabricating notices or resetting unchanged source-version acknowledgement state.

**Given** local confirmation, synchronization and reopening,
**When** the existing authenticated FastAPI/PostgreSQL path accepts or rejects the revision batch,
**Then** enforce owner, writer authority, expected server revision and atomic domain/event/receipt updates under AD-5,
**And** distinguish local confirmation from server confirmation; only a matching valid receipt acknowledges the immutable batch,
**And** lost responses retry unchanged identities/payload; conflicts preserve permitted local work for explicit resolution rather than overwriting server state,
**And** reopen preserves the revision, draft or pending state that actually committed, including local storage-failure and pending-logout protections.

**Given** a pending or confirmed addition affects the last planned activity,
**When** retention is evaluated,
**Then** apply AD-12 exactly: derived day data expires seven days after confirmed actual end/abort, or seven days after planned final end if the day is never ended; only a confirmed plan revision may change that unended day's planned final end,
**And** never calculate expiry as seven days from addition, confirmation, retry or synchronization time; a revised planned end changes only the permitted day-level reference, not the retention duration or an independent fixed draft deadline,
**And** each unconfirmed revision/import draft expires at the earlier of its original creation plus seven days and the associated day's applicable expiry; reopening, editing, copying old work into a revision or confirming another revision cannot reset that creation time or renew an already applicable earlier fixed deadline,
**And** an unconfirmed proposal or a change not affecting the final planned end cannot move day expiry; confirmed actual end/abort takes precedence over planned end and does not acquire a new grace period when learned on reconnect,
**And** check existing expiry before accepting the revision, so already expired data cannot be revived by a later proposed end; confirmation removes redundant draft copies and all older private revisions/events/receipts remain governed by the same applicable AD-12 day deadline, not new per-revision lifetimes,
**And** plan revision never automatically extends AD-10 access authority or an active-day grant; expired authority follows its separate authorization rules.

**Given** late-in-shift additions, an older unconfirmed draft and retained earlier plan data,
**When** the addition is proposed, confirmed, retried and reopened near the applicable deadlines,
**Then** tests verify the original draft-creation deadline remains fixed, any earlier applicable deadline wins and expired draft/day data cannot reappear under fresh identities,
**And** test a confirmed later final end, a confirmed earlier final end, an unchanged final end and an actual end learned on reconnect against AD-12's respective reference times; the later-end case must not reset draft age or start a seven-day clock from revision time,
**And** active trip, manual pin, performed work and progression are unchanged in every accepted addition case.

**Given** the manual revision surface,
**When** used by touch, keyboard or enlarged text,
**Then** target plan, additions, unchanged work, uncertainties, changed final end and confirm/cancel actions have clear accessible labels and visible focus,
**And** no distinction relies on color alone or requires drag-only ordering.

**Traceability:** FR-2/3/4/5; preparation portions of FR-17/20/24; UX-DR7/8/38/43 and approved split-work/revision ownership extension; FR-6/16 preservation and integration boundary; AD-2/4/5 atomic revisions, AD-6 explicit review, AD-7 no silent plan change, AD-10/11 authority and conflict boundaries, AD-12 retention. E3 owns live movement/progression, E4 notice relevance, E5 complete conflict recovery, E7 final summaries.

**Dependencies:** Implemented Stories 2.3, 2.6, 2.7, 2.8 and 2.9 with inherited foundations. No future story is required to demonstrate additions to a confirmed plan, honest coverage and preservation invariants. Active-driving integration is separately required in E3 before this entry is enabled operationally; source matching remains qualified under 2.2.

**Implementation evidence:** Extra passenger/non-passenger activity in the same day and a later part; Friday 25:30; unmatched addition, duplicate/ambiguous candidate, cancellation, stale base/proposal, concurrent revision rejection, double confirmation, lost response and local write failure; immutable active-pin/performed-state fixtures; partial data after additions; changed final activity/deadline versus unconfirmed proposal and unchanged intermediate parts; closed/expired/unauthorized rejection. Tests are planned, not executed.

**Size boundary:** Additions-only revision transaction and review using existing editors. No file reconciliation, replacement/deletion of existing activities, general conflict-resolution UI, movement engine, linked-person revision or summary rendering. These remain required later scopes; no V1 reduction or capacity commitment.

**Pilot qualification:** Demonstrable revision/preservation evidence contributes to E8-D. E8-P still requires real mounted-device operation through E3's movement policy, offline recovery/sync, notice relevance and final summary/retention integration. E8-E remains actual-shift evaluation. Planning approval does not qualify live updates during a shift.

**Approval:** Approved by the owner on 2026-09-25 with the exact AD-12 retention distinction and late-addition tests: a confirmed revision may change the unended day's planned final end, but cannot restart retention from revision time, renew an earlier fixed draft deadline or resurrect expired/old data under new identities. Active trip, performed work and progression remain unchanged. Planning approval only; the approved copy in epics.md is canonical.
