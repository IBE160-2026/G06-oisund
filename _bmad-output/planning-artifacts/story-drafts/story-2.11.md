---
status: approved
created: 2026-09-25
epic: E2
story: '2.11'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.4', '2.5', '2.6', '2.9', '2.10']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice builds a scoped, reviewable change proposal from an updated own-shift file. It deliberately stops before applying replacement/removal: that atomic confirmation slice follows separately. The current plan remains authoritative throughout this independently testable comparison flow.

### Story 2.11: Compare an Updated Shift File Within an Explicit Scope

As the pilot owner,
I want to compare an updated shift file with the correct plan and explicitly chosen scope,
So that I can see additions, changes and possible removals without losing existing work or mistaking a partial file for a complete replacement.

**Acceptance Criteria:**

**Given** an owned, unexpired, nonterminal confirmed own plan and permitted access,
**When** an updated PDF/JPG/PNG is selected from the shift overview,
**Then** visibly identify the target own workday/plan and its base revision, keeping that target visible through import, scope selection and comparison,
**And** require explicit whole-day replacement, replacement of selected work part(s), or additions-only scope before producing removal proposals,
**And** do not infer whole-day replacement from filename, file count or apparent extraction success; other plans remain untouched.

**Given** text/scanned PDFs or a shift spread over several JPG/PNG files,
**When** the updated source is interpreted,
**Then** reuse the qualified shared import/editor flow, transient originals and side-by-side comparison while originals are available,
**And** preserve controllable file order, prior manual draft corrections and duplicate protection when files are added or retried,
**And** expose missing/unreadable/cropped pages or parts and unknown coverage; success on available pages does not establish complete replacement evidence,
**And** incomplete or unknown coverage cannot silently turn unseen activities into proposed removals; show the affected reconciliation as unresolved until explicitly clarified.

**Given** interpreted activities and the selected target scope,
**When** matching them to the confirmed plan,
**Then** use supported activity/source identity, service date, direction, departure and existing provenance, not line number/clock time alone,
**And** preserve Friday 25:30 versus Saturday 01:30 and working-day ordering,
**And** present ambiguous matches for explicit selection, keeping genuinely distinct same-time activities separate,
**And** retain driver corrections and visibly compare source values; no new or delayed result silently overwrites a correction or establishes an unsupported unique match.

**Given** a comparison proposal,
**When** the driver reviews it,
**Then** distinguish added, changed, proposed-removed and unchanged future activities with before/after values and uncertainty,
**And** show affected parts' reporting times/depots, the target scope and any proposed final-end/AD-12 deadline effect,
**And** additions-only never proposes removals; selected-part replacement cannot propose changes/removals outside those parts,
**And** absence from a partial file is not deletion evidence; removal can only be proposed within an explicitly established replacement scope after coverage ambiguity is resolved,
**And** a repeated upload reconciles against existing identities rather than automatically proposing duplicate trips.

**Given** performed work, a manually selected active trip or activities outside the chosen scope,
**When** comparison runs,
**Then** preserve performed evidence, active trip/pin/progression, corrections and out-of-scope activities exactly,
**And** distinguish source disagreement from an authorized change; a source's omission cannot erase performed work or replace the active context,
**And** proposals that would affect protected active/performed state remain visibly unresolved rather than silently applied or reassigned to a similar activity,
**And** all comparisons remain non-operational proposals, with no plan revision or activity-completion event emitted.

**Given** a pending import/match or an existing saved proposal,
**When** the target plan or proposal changes, a response arrives late, or the view is reopened,
**Then** check owner/day/target/base revision and attempt/input identity before using the result,
**And** mark stale comparisons for new reconciliation and review rather than displaying them as current,
**And** save/reopen retains permissible interpreted fields, chosen scope, corrections and unresolved matches, while explaining that originals must be selected again for source comparison,
**And** persist the selected scope, target plan identity and exact compared base plan revision together with the proposal, and display them on reopening so the comparison basis remains explicit,
**And** if the current base plan has since changed, label the proposal stale and prohibit its use until comparison and review against the current plan are repeated; do not silently rebind its stored base revision,
**And** cancellation/failure leaves the confirmed plan in force; no automatic activation or implicit confirmation is offered by this slice.

**Given** proposal persistence and cleanup,
**When** local storage, synchronization, retry, logout or expiry occurs,
**Then** atomically store draft changes/events, use the inherited authenticated PostgreSQL path and acknowledge only matching immutable batch receipts,
**And** retain recoverable input on permissible failures without reporting a failed save as successful,
**And** enforce ownership, pending-revocation locks and the earlier applicable AD-12 draft/day deadline from Story 2.10; proposed later final ends cannot extend the draft or current day deadline,
**And** delete transient originals on success/failure/cancel/interrupted processing and remove redundant/expired private copies without resurrecting them through retry.

**Given** target, scope and comparison controls,
**When** used with touch, keyboard or enlarged text,
**Then** added/changed/removed/unchanged states have explicit labels, readable before/after values and accessible focus/error handling,
**And** target/scope changes visibly invalidate affected comparison results and require re-review,
**And** operational entry later uses E3's shared movement policy; until integrated, demonstrate in preparation and protected-state fixtures rather than claiming safe live-shift use.

**Traceability:** FR-2/3/4/5; NFR-2/3; UX-DR4/7/8/38/42/43 and revision ownership; AD-1/6 import boundary/transient files, AD-2/4/5 protected persistence/identities, AD-7 qualified matching, AD-10/12 access/retention. Preserves FR-6/20 operational-context boundaries without implementing live progression or full recovery.

**Dependencies:** Implemented 2.4/2.5 import, 2.6 matching, 2.9 part identity and 2.10 revision-draft/comparison foundations with their qualifications. Applying replacements/removals is not needed to demonstrate a correct, saved scoped proposal and is deliberately excluded here; it remains required in the subsequent E2 story.

**Implementation evidence:** Whole-day/selected-part/additions scope; incomplete and unknown source coverage; multi-image overlap/retry; same-line/time distinct journeys; manual/source disagreement; repeated upload; changed/removed/unchanged future activities; immutable performed/active/out-of-scope fixtures; stale base/late responses, cancel, reload/reselection, receipt/write faults and expiry. Tests are planned, not run.

**Size boundary:** Scoped comparison and recoverable proposal only, reusing existing extraction/matching/editor code. No replacement/removal commit, linked-person revisions, general merge engine, movement engine or automatic operational changes. The next slice supplies explicit confirmation and atomic application; no V1 requirement is removed.

**Pilot qualification:** Repeatable comparison contributes to E8-D. E8-P requires subsequent apply/preservation integration, actual import layouts and real tablet/movement/offline behavior before use during actual shifts. E8-E remains separate evaluation.

**Approval:** Approved by the owner on 2026-09-25 with scope and compared base revision persisted/displayed with the proposal. A changed base plan makes the proposal stale and requires fresh comparison before use. Absence from a partial file alone never justifies proposed deletion. Planning approval only; the approved copy in epics.md is canonical.
