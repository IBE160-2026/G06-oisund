---
status: approved
created: 2026-09-25
epic: E2
story: '2.4'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['1.1', '1.2', '1.3', '1.4', '2.1', '2.3']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice imports a supported text-based PDF into the existing unconfirmed review editor. It consumes the text-PDF findings from Story 2.1, preserves original-file transience and enables manual correction through Story 2.3. Scanned PDF/JPG/PNG remains required V1 work in a subsequent slice; timetable matching and final driver confirmation remain separate.

### Story 2.4: Review a Text-PDF Shift as an Editable Unconfirmed Draft

As the pilot owner,
I want to upload a text-based shift PDF and inspect its interpreted activities beside the source,
So that I can identify errors and missing work before any interpretation becomes my confirmed plan.

**Acceptance Criteria:**

**Given** permitted private application access and the preparation entry,
**When** the owner selects a supported text-based PDF for a new import,
**Then** the authenticated backend validates the upload against documented type/size/processing limits and invokes the import adapter qualified by Story 2.1,
**And** it creates an owner-scoped unconfirmed import attempt/draft, not an active day or confirmed plan,
**And** cancelling file selection returns to the preceding state without altering another draft or confirmed work,
**And** unsupported, corrupt or over-limit input produces an understandable failure without a false successful import or exposure to another owner.

**Given** a qualified text PDF with multiple columns or page continuations,
**When** interpretation completes,
**Then** process all relevant pages and produce editable known fields and activities in source-supported order,
**And** preserve minimal page/field provenance, missing/uncertain markers and unexplained source codes without retaining a raw OCR/text archive,
**And** Vogn is not treated as a physical bus number, and Travel to is not automatically classified as pilot-car transport,
**And** incomplete extraction identifies the specific missing/unreadable pages or parts using available page/section references; when the extent cannot be established it explicitly says coverage is unknown rather than presenting a complete plan,
**And** this coverage status is retained with the draft so it survives saving/reopening; unsupported portions never silently disappear from the review.

**Given** a Friday-service entry containing 25:30 and neighboring activities,
**When** extracted data is shown, corrected, saved and reopened,
**Then** retain the source Friday service date, extended time and activity identity/order, deriving Saturday 01:30 only for calendar-date presentation,
**And** do not merge it with another same-display-time activity or infer an Entur service-date match,
**And** missing source date/time or ambiguous ordering stays visible for correction instead of invented midnight rollover or silently assigning today's date.

**Given** a completed or partially interpreted unconfirmed draft,
**When** the shared review screen opens,
**Then** the PDF and interpreted activities are shown side by side in the approved source/review composition while the transient original is available,
**And** the driver can use Story 2.3's direct field correction and missing-activity addition, with extracted/manual/unknown facts distinguishable,
**And** saving or server acknowledgement does not confirm the plan or enable an active trip,
**And** processing/layout failures retain available interpreted facts as unconfirmed and expose another-file/manual-correction paths rather than inventing a complete shift.

**Given** an unexpired interpreted draft is reopened after its transient original preview has been released,
**When** the shared review screen is displayed under permitted access,
**Then** the saved editable activities, manual corrections and page/part coverage warnings remain available,
**And** the source area explicitly states that the original PDF must be selected again to compare with it, with a labelled file-selection action rather than an empty or apparently loading preview,
**And** reselecting a file for comparison does not silently reimport it, overwrite corrections, confirm the plan or reset expiry,
**And** tests cover side-by-side review before closure, source-unavailable messaging after reopening and retained warnings identifying missing pages/parts.

**Given** an upload/interpretation attempt is retried or its response is lost,
**When** the owner resumes that same authorized unexpired attempt,
**Then** a stable attempt identity permits recovery of any persisted interpreted result without producing duplicate activities/drafts or reusing a changed payload under the same identity,
**And** retry cannot require the backend to retain the original after processing has ended,
**And** if no interpreted result survived, the UI explains that the file must be selected again; a new attempt is explicit,
**And** late or cancelled results never overwrite intervening manual corrections, another draft or confirmed work; mismatched revisions are preserved as a visible conflict rather than silently applied.

**Given** interpretation finishes, fails or is cancelled,
**When** processing cleanup runs,
**Then** backend originals and processing copies are deleted on each outcome, with interrupted-process cleanup verified on restart,
**And** originals never enter IndexedDB, service-worker caches, persistent job payloads, logs, repository or CI artifacts,
**And** the browser preview remains transient for the current review, is released on leaving/cancelling the review, logout or expiry, and is unavailable after reload unless the owner selects the source again,
**And** only necessary interpreted fields/provenance/corrections remain under the existing draft retention boundary; the UI explains the distinction between the transient file and retained interpreted information.

**Given** interpreted data is committed and manually corrected,
**When** local persistence, synchronization or reopening occurs,
**Then** reuse the approved atomic state/event and immutable batch/receipt behavior, preserving field provenance, activity IDs/order and unresolved values,
**And** clearly distinguish local saving from server confirmation; an extraction response alone is not a matching SyncReceipt,
**And** draft expiry is non-sliding from draft creation or an earlier applicable associated-day deadline, not completion/retry time,
**And** every introduced interpreted result, import-attempt private association, pending payload and receipt is included in ownership checks and expiry cleanup.

**Given** logout, unreliable local lock storage, permission loss or expiry occurs during upload or interpretation,
**When** the browser receives a late response or reopens the application,
**Then** private source previews and interpreted contents remain hidden until the applicable Story 1.2/AD-10 recovery conditions are met,
**And** no late result renews retention, bypasses pending revocation or resurrects an expired draft,
**And** server processing still cleans transient originals even when the client disconnects; disconnection is not permission to retain private files indefinitely.

**Given** the import/review UI,
**When** it is used with touch, keyboard or enlarged text,
**Then** upload progress, failure, partial-page coverage, unknown values and save states are clearly labelled with focus/error handling and the approved preparation tokens,
**And** no camera/GPS permission, AI correction interpreter or precise gesture is required,
**And** scanned/image-only input is explicitly identified as requiring the later OCR path rather than represented as a successful empty text import; V1 support for that path remains mandatory.

**Traceability:** FR-2, FR-3/4/5 interpretation and identity boundaries, NFR-2/3; UX-DR2/4/5/38/39/42; AD-1 import boundary, AD-2/5 persistence, AD-6 backend interpretation/transient originals, AD-10 access, AD-12 retention and AD-13 bounded processing/private no-store handling. Preserve the approved service-date/extended-time clarification from Stories 2.2/2.3.

**Dependencies:** Approved implementation Stories 1.1–1.4 and 2.3, plus completed Story 2.1 evidence supporting the intended text-PDF cases. Story 2.1's approval as a plan is not passing extraction evidence; a material negative qualification result requires the owner's further-solution decision before locking a parser. No timetable integration from 2.2 is required to review known extracted fields. Exact processing limits are documented/tested implementation choices, not a silent reduction of supported representative V1 inputs.

**Implementation evidence:** Representative qualified text fixtures with checked dates/times/activities/order; multipage/column coverage; Friday 25:30 correction/reopen; missing-field/code cases; invalid/oversized/cancelled file selection; partial extraction, crash cleanup, duplicate retry/lost response and late-result/manual-edit conflict; source-preview loss after reload; logout/expiry while processing; local/PostgreSQL fault cases and owner isolation. Test private sample handling without publishing operational originals. These checks are proposed, not executed here.

**Size boundary:** New unconfirmed text-PDF import into one shared editor, not replacement of an active plan, scoped day revisions, OCR, timetable matching or final plan confirmation. Build only the import attempt/result handling needed for this path. Existing drafts remain intact when another file is selected; no silent merge/overwrite is introduced.

**Pilot qualification:** Implemented fixture evidence contributes to E8-D and the text-import portion of E8-P. Actual hosted handling/cleanup, remaining PDF/image formats and end-to-end driver confirmation still require their own integration evidence; this story cannot establish the whole pilot gate or E8-E. No implementation or readiness workflow is started by this draft.

**Approval:** Approved by the owner on 2026-09-25 with side-by-side PDF/activity review while the transient original is available, preserved editable draft and explicit original-reselection guidance on reopening, and specific missing-page/part warnings for incomplete extraction. Import remains unconfirmed. Approval concerns planning only; the approved copy in epics.md is canonical.
