---
status: approved
created: 2026-09-26
epic: E6
story: '6.9'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['2.11', '2.12', '6.2', '6.3', '6.8', '5.7', '5.13']
---

### Story 6.9: Revise the Intended Linked Plan and Explicitly Repair Affected Accompaniment Links

As the pilot owner preparing or using FADDER/INSTRUKTØR plans,
I want to review a revision of the intended private person-plan copy and explicitly repair affected accompaniment links,
So that changed future work becomes usable without mixing people's plans, moving the active trip or rewriting observed work.

**Acceptance Criteria:**

**Given** accessible unexpired own and imported-person plans,
**When** the owner starts a file or manual revision,
**Then** require an explicit target own plan or named imported copy and retain that owner/person/plan identity visibly throughout input, scope selection, comparison and confirmation,
**And** reuse E2's shared PDF/image/manual revision flow with whole-plan, selected-part and additions-only scope; persist the exact target, base revision, input/proposal revision and selected scope so reopening shows what was compared,
**And** match existing activities only within that target plan using supported identity/service-date evidence. Another person's or own-plan trip is never a match merely because line, time or stops are identical,
**And** retain manual correction/source provenance, unknown data and temporal uncertainty, including extended service-date times; no fresh extraction or matching answer silently replaces an existing correction,
**And** follow AD-6 original/processing cleanup and reopen-with-reselected-original behavior. This remains the mentor's private copy and review, never approval by or editing of the other person's account.

**Given** a scoped linked-plan proposal is compared with its saved base,
**When** the owner reviews changes,
**Then** show added, changed, proposed-removed and unchanged eligible activities, with before/after values and a list of accompaniment links whose person/trip/portion/boundaries are affected,
**And** distinguish future planned links from active tracking context and historical observed periods; show the effect on whole-shift FADDER scope and each affected INSTRUKTØR block, including later returns to the same person,
**And** a partial file's omission is not enough to propose deletion, additions-only removes nothing, and actual removals require explicit review within the established replacement scope,
**And** blocking identity/date/order/scope ambiguity must be resolved before confirmation; source no-match/missing stops/bus may remain visibly unknown under E2 rules,
**And** a changed base, target, scope or proposal invalidates the previous review and requires comparison again rather than retaining confirmation eligibility.

**Given** a current resolved revision proposal is explicitly confirmed,
**When** local application commits,
**Then** atomically apply only the reviewed eligible changes to that target, advance its revision, persist the revision event and mark affected accompaniment links unresolved with their former reference/scope and the reason for repair,
**And** preserve stable identities for supported existing matches and create identities only for genuine additions; never remap a removed trip or interval to a similar trip automatically,
**And** preserve other plans, performed evidence, active trip/direction/progression/pin and actual role, including an ongoing FADDER takeover. An activity that became active/performed during review is protected and requires fresh comparison instead of partial application claimed as complete,
**And** a valid revision may remain locally confirmed while affected planned links await repair; show those separate statuses. Unresolved links cannot start a new accompaniment context or silently extend/change its scope,
**And** if revision affects an active accompaniment link, keep the ongoing tracking context explicitly bound to the exact plan revision on which it was established, with the affected link visibly unresolved. Persist and render the active revision separately from the newer confirmed plan revision; neither revision application, reopen, synchronization nor a late source response may silently substitute the newer revision into the active trip,
**And** retain the necessary active-revision facts within existing AD-12 limits; further use of the changed link requires explicit current-basis review/repair. Even repaired planned links do not silently rebind the active context: any actual context change still uses the explicit permitted transition and preserves earlier evidence,
**And** unchanged references in the revised copy retain their identity and original review provenance, but a newer plan revision is not silently claimed reviewed for a new context. Revalidate and explicitly review the applicable link against the current revision before new use. Unrelated plans/links are not invalidated by association alone.

**Given** a link is unresolved after a linked-plan revision or an accepted own-plan change to its referenced assignment/activity,
**When** the owner opens link repair,
**Then** show its previous person/plan/revision/scope beside the current target and explain the changed or missing reference, preserving the old basis until explicit resolution,
**And** permit deliberate selection of a valid current portion and confirmation through 6.3's rules, or explicit removal of a no-longer-needed planned link without deleting its historical observed periods; cancellation leaves the unresolved link intact,
**And** keep FADDER tied to the same person's whole shift and INSTRUKTØR blocks explicitly bounded; known missing sections, conflicting boundaries, repeated stop occurrences or ambiguous overnight trips cannot be repaired by guessing,
**And** target-plan repair cannot silently select a different person. A needed person/assignment change follows the existing explicit plan/link path and still creates no actual operational switch,
**And** recheck exact own/linked plan revisions, target identity/scope and current role/access at repair commit. Save the newly reviewed link basis/provenance atomically; intervening changes require a new review,
**And** integrating own-plan revisions uses the existing E2 commit path with link invalidation in the same transaction; no interval may expose a changed activity with a falsely valid old link.

**Given** a repaired link is saved while old operational observations or callbacks still exist,
**When** the link is used, reopened or a delayed result arrives,
**Then** retain repair as a planned association distinct from the active and historical context. Actual person/block entry or change still requires 6.4/6.5 and current permissions,
**And** never move the active manual pin to the repaired trip, retroactively attribute earlier observations to the new portion/person, turn a manual field into source/GPS evidence or infer completion of removed work,
**And** E4 relevance and retained source/seen state remain tied to the actual supported context; a revised plan or repaired link is not a new notice receipt and cannot replay old sound,
**And** invalidate stale confirmations/gestures at commit after Jeg kjører, access loss or context/revision changes, retaining 6.7's restrictive recovery. A delayed receipt for an already committed revision confirms only that original revision, not a new repair or role change,
**And** preserve per-trip data coverage honestly after revision; new/changed trip data is not automatically downloaded or verified. Partial coverage cannot be labelled whole-day ready.

**Given** revision/repair persistence, synchronization or recovery fails,
**When** browser and backend process or reopen the work,
**Then** reuse owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL revision/outbox contracts, extending only necessary link-impact and repair state; validate target ownership, writer authority, expected revision and protected operational facts server-side,
**And** local failure/cancel leaves the prior committed plan and links intact; a committed local revision with unresolved links remains distinguishable from an unapplied proposal and from completed repair,
**And** stable proposal/application/event identities prevent duplicate revision or repair on retry, with only matching receipts establishing server confirmation. Conflicts preserve permitted proposals/evidence for 5.7 review without silent rollback or partial backend writes,
**And** recover revisions, unresolved reasons and original/current link bases together; no crash or stale tab may show a half-applied revision or falsely repaired link,
**And** obey AD-12 draft/own-day deadlines, logout/expiry and 5.13 terminal guards across proposals, old revisions, conflicts, outboxes and checkpoints. A linked person's changed final end does not change the mentor's own-day end, access grant or retention clock; only an applicable confirmed own-plan revision may affect own planned end under the exact existing AD-12 rules,
**And** keep only required interpreted private data, preserve permitted observed evidence and remove the unaccompanied remainder at own-day closure without resurrection by pending revisions/responses; no permanent source/history archive or cross-account rights are added.

**Given** anonymized/fictional own and linked plans, browser clients and real PostgreSQL,
**When** the slice is verified,
**Then** test file/manual changes to one of two identical-looking person plans, whole/part/additions scope, partial-file omission, explicitly removed future trip and retained manual correction,
**And** test a FADDER whole-shift boundary change and incomplete replacement, INSTRUKTØR A–B–A with only A links affected, a repaired interval with repeated stop occurrences and Friday 25:30/calendar-date ambiguity,
**And** test a trip becoming active/performed while review is open, ongoing takeover with pinned active trip preserved, an own activity changed with atomic invalidation of its links and prior observed periods remaining unchanged,
**And** keep an active context on revision R1 while confirming R2 that affects its link: verify visible unresolved status and R1-bound trip/stops/pin after reload, delayed R2 responses and synchronization; repair alone cannot swap the active basis, and use of the changed link requires explicit review and permitted transition,
**And** test revision saved but repair pending, cancelled repair, stale base during both reviews, no automatic similar-trip/person substitution and explicit new-context entry after repair without inherited evidence,
**And** test role change before commit, failure before/after revision and repair transactions, restart, duplicate actions, lost/mismatched receipts, wrong target/owner/writer, conflict, logout, expiry and terminal cleanup with delayed old proposals,
**And** verify that changing the linked plan's end time does not extend own-day retention/access and that updated data coverage is distinct from confirmation. No future report screen is required to verify these contracts.

**Traceability:** UX UJ-3/4 extensions of FR-2/3/4/5 and FR-6/9/16/20 preservation, FR-22/24 provenance/retention. NFR-1–4; UX-DR4/5/7/8/16/26/27/28/30/31/36/38/39/43/44. EXPERIENCE Revision ownership and linked contexts, explicit scope and actual-versus-planned context; DESIGN separate own/linked review panels. AD-2/4/5 atomic revisions/receipts, AD-6 shared import/transient originals, AD-7/8 source/notice boundaries, AD-9 active context/pin, AD-10/11 authority and AD-12 deadlines/all-copy cleanup. All AD-1–AD-14 remain unchanged.

**Dependencies:** E2 comparison/application through 2.11–2.12, 6.2 reviewed private copy, 6.3 links, 6.4–6.8 operational roles/contexts and E5 conflict/closure infrastructure through 5.13. Uses existing E2 machinery and scoped repair rather than a new general merge engine; no later full cross-device mentor recovery or E7 renderer is required.

**Size boundary:** Adapt the existing revision transaction to named linked copies, atomically invalidate impacted links and repair their explicit planned references. Active/historical context is protected rather than edited. No new importer/matching engine, arbitrary history rewrite, automatic person switch, cross-account editing or summary/PDF UI. General device-transfer recovery remains a separate E6 integration slice.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL revision/repair and race cases contribute to E8-D. E8-P still needs representative actual updates, mounted review usability and integrated role/recovery/closure behavior. E8-E remains field evaluation; approving a copied plan revision verifies neither source coverage nor the other person's performance. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with active-revision binding: when revision affects an active accompaniment link, its ongoing trip remains bound to the revision it was established on with visibly unresolved linking; no silent newer-revision substitution, and further use of the changed link requires explicit review. Planning approval only; the approved copy in epics.md is canonical.
