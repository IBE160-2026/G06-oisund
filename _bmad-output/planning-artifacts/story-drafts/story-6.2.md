---
status: approved
created: 2026-09-26
epic: E6
story: '6.2'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.1', '2.3', '2.4', '2.5', '2.6', '2.7', '5.13']
---

### Story 6.2: Review and Confirm a Separate Private Copy of an Accompanied Person's Shift

As the pilot owner preparing FADDER or INSTRUKTØR work,
I want to import, correct and separately confirm the intended person's shift within my own working day,
So that I can prepare the necessary route context without replacing my own plan or claiming that accompaniment has begun.

**Acceptance Criteria:**

**Given** an accessible, unexpired own working day with its own mentor plan reviewed and confirmed through 6.1,
**When** the owner starts preparation of another person's shift,
**Then** create a separately identified imported-plan draft associated with that own day and the explicitly identified intended person, with the target visible throughout import, editing and confirmation,
**And** show separate Egen arbeidsplan and accompanied-person plan panels; use only the person information needed to distinguish the imported contexts, without a permanent person directory or another account's identity/permissions,
**And** an unknown or ambiguous intended-person association remains visibly unresolved and cannot silently be assigned to an existing person by similar name, route or time,
**And** selecting a file is neither confirmation of its person/contents nor linking it to an accompaniment block; an instructor day without accompaniment still needs no imported person plan.

**Given** a PDF, one or several JPG/PNG files, or a manually entered plan for this target,
**When** the shared E2 import/editor interprets and displays the result,
**Then** retain editable extracted activities, source/manual provenance, uncertainty and visible missing pages/parts; extraction/OCR success is not confirmation,
**And** reuse multi-image ordering and correction-preservation rules, preventing repeated processing/retries from duplicating activities or dropping prior edits,
**And** preserve service date and extended time separately from calendar display: Friday 25:30 remains Friday's shift activity and displays as Saturday 01:30 where calendar time is used, in the correct sequence after save/reopen,
**And** preserve reporting/depot/work-part details and physical bus versus vehicle-duty identity; unknown data remains unknown and failed extraction still permits manual entry/correction,
**And** source matching uses the applicable trip identity and service date, retaining manual corrections and distinguishing no match, ambiguity and retrieval failure; no match copies a trip from another private plan.

**Given** a source file is being processed or compared with the interpreted draft,
**When** processing finishes, fails, is cancelled or is interrupted, or the review is reopened,
**Then** apply AD-6 transient-original handling: delete backend originals and processing copies after interpretation/failure/cancellation, with interrupted-process cleanup; do not retain originals in IndexedDB, Service Worker caches, logs or persistent queues,
**And** while a selected original is still transiently available in the browser, permit the existing side-by-side source comparison; after reopening explain that the original must be selected again while interpreted data and manual corrections are preserved,
**And** explain the deletion rule during import review; retaining the necessary interpreted information does not authorize a raw OCR archive or permanent source-file copy,
**And** cancelling this import leaves own and previously confirmed person plans intact, with any retained unconfirmed draft clearly identified and subject to its original expiry.

**Given** the owner has reviewed the intended person, target plan and corrected draft revision,
**When** the owner explicitly confirms that person's imported plan,
**Then** confirm only the exact revision reviewed, with the E2 requirements for service date, order and planned end satisfied; require a new review if the draft or relevant target/day basis changes,
**And** label and persist confirmation as the FADDER/INSTRUKTØR owner having reviewed this private imported copy and its exact revision; do not imply that the accompanied person confirmed, approved or authenticated the plan. Preserve this attribution through reopen, synchronization and downstream plan references,
**And** permit reviewed trips without a source match under 2.7's rules, retaining missing-stop/missing-bus/unknown-source status rather than marking these fields verified,
**And** atomically store the separate confirmed plan and required outbox event, removing redundant draft copies only after successful local confirmation,
**And** do not modify the own plan, its planned own trips, active trip/pin, actual role, accompaniment state or performed evidence; this action grants no guiding exception and does not declare any work performed,
**And** show separate statuses for person-plan confirmation, still-pending accompaniment linking and actual data coverage; confirmed contents alone cannot claim the whole mentor day is ready.

**Given** two imported plans have overlapping routes/times or the same person will be accompanied again later,
**When** plans are listed, reopened or selected for preparation,
**Then** preserve stable person/plan/revision identities within this owner and own day, showing enough context to distinguish them without merging by route/time/name similarity,
**And** expose an already confirmed copy for later explicit reuse rather than requiring a duplicate import; no reuse automatically creates an accompaniment block or carries completion/manual pin evidence,
**And** an attempt to replace an existing confirmed copy cannot silently run as a new import or overwrite it; use the subsequent explicit linked-revision review/repair flow, while this slice can independently create, review and reopen new copies,
**And** a forged target or correction cannot turn this person's trip into planned own driving or change another stored plan.

**Given** this private imported data is saved, synchronized, reopened or becomes due for deletion,
**When** browser and backend process it,
**Then** extend the existing owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL contracts with only the person/plan/draft identity and fields this slice needs; enforce scope and confirmation rules on both client and server,
**And** local failure never reports saved/confirmed state; a missing or mismatched receipt leaves server status unconfirmed and stable retries do not duplicate the imported plan. Expired access, pending logout, stale revision or obsolete writer authority cannot bypass E1/E5 guards,
**And** use the unconfirmed draft's fixed creation-plus-seven-days deadline or an earlier associated-own-day deadline under AD-12; confirmation removes redundant drafts and associates needed extracted data with that own combined day's existing retention rules, without resetting a clock or extending an earlier binding deadline,
**And** the imported person's planned/actual shift ending never starts a separate retention clock or changes the mentor's own-day end or authority,
**And** register this new data type in the existing all-copy expiry and 5.13 closure/retirement guards now: without actual accompanied evidence, linked operational content is not retained after own-day closure; delayed responses, stale tabs or pending batches cannot restore prohibited content. Fixture-based closure is sufficient here, without a future summary screen,
**And** importing provides no access to another person's account or original records; private imported data is unavailable to public fictional demo access, public logs or assessment artifacts, and personal source fields do not enter the active driving view.

**Given** representative anonymized/fictional own and person shifts, the shared import engines and real PostgreSQL,
**When** this slice is verified,
**Then** test PDF, ordered multi-image input and manual fallback; identify the tested formats and failure cases without treating these tests as new OCR/source qualification,
**And** test partial extraction, retained correction across retry/reopen, Friday 25:30 and two candidate trips showing Saturday 01:30, identical-looking own/person trips and two distinct imported-person contexts,
**And** test confirmation attribution in the review, reopened plan and stored/API result: the mentor is the reviewer, the accompanied person is the subject of the imported copy, and no label or record claims their approval,
**And** test separate confirmations, changed review revision, cancel, wrong target/owner, local failure, lost/mismatched receipt, logout, expiry and interrupted-original cleanup,
**And** test own-day closure with no accompanied evidence, pending imported-plan work, stale tab/delayed response and earlier draft/day expiry, verifying all relevant client/server copies against the existing deletion protocol,
**And** prove that import/confirmation/reopening never changes operative role, selects an active linked trip, manufactures accompaniment evidence or copies a trip into own driving.

**Traceability:** FR-2/3/4/5 imported-plan preparation and FR-6 ownership boundary, shared FR-1/16/20/24, under UX UJ-3/4. NFR-1–4; UX-DR4/5/6/7/8/26/27/28/36/38/39/43/44. EXPERIENCE assignment scope, revision ownership and Accompanied-person imports and summary scope; DESIGN separate own/linked panels and source-deletion notice. AD-2/4/5 atomic storage/receipts, AD-6 shared interpretation/transient originals, AD-9 no implicit role/context transition, AD-10/11 authority and AD-12 all-copy retention. All AD-1–AD-14 remain unchanged.

**Dependencies:** Approved 6.1 own-plan preparation, E2 shared import/edit/matching/confirmation and E1/E5 access, persistence and expiry/settlement through 5.13. Tests may invoke existing terminal commands with no-accompaniment fixtures. No later block-linking, operational mentoring, linked-revision repair or E7 summary screen is needed to complete this import slice.

**Size boundary:** Adapt the existing reviewed import flow to a separately identified private person-plan copy, including target visibility, confirmation, persistence and lifecycle integration. No second OCR engine, person directory, cross-account integration, actual accompaniment selection, operational role switch, linked-plan revision/repair UI or summary/PDF renderer. Later E6 stories explicitly link confirmed plans and establish observed portions.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL import and deletion cases contribute to E8-D. E8-P still requires actual representative formats, qualified extraction/source coverage, tablet review usability and verified temporary/provider handling before real files. E8-E remains field evaluation. None is claimed executed or passed by this planning story.

**Approval:** Approved by the owner on 2026-09-26 with explicit confirmation attribution: confirmed means that the FADDER/INSTRUKTØR has reviewed their private copy of the other person's shift, never that the other person has confirmed the plan. Planning approval only; the approved copy in epics.md is canonical.
