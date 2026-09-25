---
status: approved
created: 2026-09-25
epic: E2
story: '2.12'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.10', '2.11']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice applies an explicitly reviewed own-plan file revision using the existing revision transaction. Story 2.11 supplies comparison; this story adds replacement/removal commit guards and recovery. Operational movement integration remains E3, linked-person effects E6.

### Story 2.12: Confirm and Atomically Apply a Scoped Own-Plan Revision

As the pilot owner,
I want to explicitly confirm the reviewed changes to my own plan,
So that the intended remaining work becomes authoritative without partial replacement, lost evidence or an unintended change of active trip.

**Acceptance Criteria:**

**Given** an owned, unexpired proposal with stored target, scope and base revision,
**When** final review opens or resumes,
**Then** display that comparison basis, additions, changed before/after values, proposed removals and unchanged work with affected parts' reporting times/depots,
**And** check that the base revision is still current; a stale proposal cannot be confirmed until it has been compared and reviewed again,
**And** changed proposal content, scope or target invalidates the review rather than silently retaining confirmation eligibility.

**Given** the proposal contains ambiguity, missing source coverage or a proposed removal,
**When** the driver prepares to confirm,
**Then** require resolution of identity, scope and temporal ambiguity necessary to apply the changes safely,
**And** unknown source matches/stops/bus remain permitted with explicit missing labels once blocking ambiguity is resolved; confirmation is not source verification,
**And** require explicit confirmation of the displayed removals within the established replacement scope; additions-only cannot remove anything and absence from a partial file alone never authorizes removal,
**And** keep the current confirmed plan in force if required resolution or confirmation is missing.

**Given** a current, resolved, reviewed proposal,
**When** the driver explicitly confirms it,
**Then** validate the exact target, base and proposal revisions and protected activity state inside the local commit boundary,
**And** atomically apply only the reviewed in-scope future changes, advance the plan revision and persist the typed revision event before showing local success,
**And** retain identity for matched existing activities and assign stable identities only to actual additions; preserve manual/source provenance of explicitly accepted field changes,
**And** no failure may leave some proposed replacements/removals applied and others unapplied; cancellation and failed local commit preserve the prior plan.

**Given** performed work, active trip/pin/progression, manual corrections or out-of-scope plans/activities,
**When** confirmation runs, including after operational state changed since review,
**Then** recheck protection and preserve those facts and active context; a formerly future activity that is now active/performed cannot be silently replaced or removed,
**And** require fresh comparison for affected conflicts rather than silently skipping protected changes while claiming the whole reviewed proposal was applied,
**And** only explicitly reviewed changes to eligible future fields may replace their prior values; refresh or matching alone never overrides manual corrections,
**And** a missing active trip in the uploaded source cannot switch the selected trip or falsify completed/aborted work; tests use protected-state fixtures before E3 integration.

**Given** duplicate confirmation, repeated upload or an uncertain response,
**When** application/synchronization is retried,
**Then** use stable proposal/application and immutable event/batch identities so the revision and its effects occur once,
**And** reopening distinguishes a committed local revision awaiting server acknowledgement from an unapplied proposal; do not apply an already committed revision again,
**And** authenticated FastAPI/PostgreSQL acceptance atomically validates ownership, writer authority and expected server revision with domain changes, deduplication and matching receipt under AD-5,
**And** a matching receipt alone marks server confirmation; backend conflicts preserve permitted local work for explicit resolution without partial backend writes, silent rollback or blind overwrite.

**Given** a revision changes remaining work,
**When** coverage is updated,
**Then** publish the new plan and its honest coverage relationship consistently, preserving still-applicable data while invalidating changed/removed associations for current-plan use,
**And** identify added/changed trips needing downloads; an old complete manifest cannot make the revised day complete,
**And** offline confirmation is possible only with permitted access and sufficient reviewed local facts; missing external data remains missing and cannot be fetched by implication,
**And** record the applied revision and necessary before/after provenance for later summary and notice-relevance integration without creating source notices or resetting unchanged notice-version states.

**Given** a proposed change affects the combined planned final end,
**When** the revision is confirmed,
**Then** use Story 2.10's exact AD-12 criteria: only a confirmed revision changes a never-ended day's planned-end reference; no seven-day clock starts at revision time,
**And** fixed draft creation deadlines and any earlier applicable limits remain enforced; no expired data can be revived under fresh identities and redundant proposal/draft copies are removed under AD-12,
**And** actual end/abort overrides planned end, terminal days cannot be revised, and old revisions/events/receipts share their applicable day deadline rather than independent new lifetimes,
**And** no retention change automatically extends AD-10 access/grant authority; late responses, logout and storage failures cannot bypass lock/expiry checks.

**Given** final review is operated by touch, keyboard or enlarged text,
**When** the driver inspects and confirms/cancels,
**Then** clearly identify the target, scope, removals, changed values, final-end effects, local/server status and recoverable errors with accessible labels and focus,
**And** before enabling use during an actual shift, E3 must connect both entry and confirmation to the shared movement permission, cancelling/preventing an uncommitted action when permission is lost; no second movement engine is introduced.

**Traceability:** FR-2/4/5 and preservation aspects of FR-6/17/20/24; NFR-2/3; UX-DR7/8/38/42/43 and revision ownership; AD-2/4/5 atomic changes/receipts, AD-6 explicit confirmation, AD-7 no silent plan change, AD-10/11 authority/conflicts, AD-12 cleanup/expiry. E3 retains runtime permission/progression, E4 relevance, E5 full conflict recovery, E6 linked plans, E7 summary rendering.

**Dependencies:** Implemented 2.10 revision application foundation and 2.11 persisted comparison, including their prerequisites. Preparation UI and domain fixtures demonstrate this slice without a future story. Operational driving and linked-plan integrations remain separately required before those uses are available.

**Implementation evidence:** Whole-day/part replacement and additions-only; explicit removal, partial-file omission rejection, stale proposal/base/scope, activity becoming active/performed during review, preserved pin/progression; partial-write fault injection, duplicate tap/retry/reupload, lost receipt, backend conflict, reopen of unapplied versus locally applied proposal; changed data coverage, offline missing facts, final-end/old-draft expiry and terminal/owner/logout rejection. PostgreSQL integration evidence is required; no tests run during planning.

**Size boundary:** Extend the existing revision transaction to reviewed eligible replacements/removals and their commit-time checks. No new importer, general merge/conflict-resolution UI, runtime movement engine, linked-plan repair or summary UI. These remain assigned V1 obligations, not deferred requirements.

**Pilot qualification:** Repeatable end-to-end own-plan revision supports E8-D. E8-P still requires actual file/layout coverage, mounted-device movement restrictions and integrated recovery, relevance and summary/retention checks. E8-E remains subsequent actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the described result, scope and acceptance criteria. The owner requested continuation to the next individual story. Planning approval only; the approved copy in epics.md is canonical.
