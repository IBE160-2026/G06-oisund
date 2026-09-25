---
status: approved
created: 2026-09-25
epic: E2
story: '2.5'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.1', '2.4']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice extends Story 2.4's shared import/review flow to scanned PDF and JPG/PNG screenshots/photos using the qualified OCR path. It reuses E1 persistence/access and Story 2.3 editing through 2.4; it does not introduce another review UI, final plan confirmation or timetable matching.

### Story 2.5: Review Scanned PDFs and Images Through the Shared Import Flow

As the pilot owner,
I want to import a scanned shift PDF, screenshot or photograph into the same editable review,
So that I can check and correct my shift even when its source has no usable text layer.

**Acceptance Criteria:**

**Given** permitted private access and representative scanned PDF/JPG/PNG cases qualified under Story 2.1,
**When** the owner selects an existing supported file through the shared upload entry,
**Then** the backend validates the input and uses the qualified OCR adapter behind the existing import port,
**And** selecting an existing photograph/screenshot requires no camera permission, live-camera capture, GPS or separate installed application,
**And** cancelling selection preserves the existing draft and invalid/corrupt/over-limit files produce an understandable error without a false successful import.

**Given** one shift is split across several JPG/PNG files,
**When** the driver selects the files or adds another image to the same unconfirmed draft,
**Then** show an ordered file list with clear source references and accessible controls to inspect and change the order rather than relying silently on filename or upload completion order,
**And** show the proposed combined activity sequence before applying additions, preserving existing activity identities and manual corrections,
**And** repeated selection/retry or overlapping content must not create duplicate activities; uncertain overlaps require explicit resolution rather than silently merging or dropping potentially distinct activities,
**And** adding a file cannot remove activities absent from that file, overwrite earlier corrections or become an active-plan revision,
**And** changing source order does not silently rewrite corrected activity order; any conflict remains visible for driver resolution.

**Given** a multi-image import with out-of-order files, overlapping rows, a later-added file and an already corrected activity,
**When** the driver reviews the order, applies additions, saves and reopens the draft,
**Then** the checked expected activity sequence and prior correction are retained without duplicates, with minimal file/part provenance and coverage warnings,
**And** cropped, unreadable or known missing parts remain explicitly uncertain/unknown; success on the available files is not proof the whole shift is present,
**And** only minimal source-reference/order metadata persists, not original image files or permanent thumbnails; unavailable originals must be reselected for comparison,
**And** an unreadable or cancelled individual file cannot erase successfully saved activities from the other files, and the draft remains unconfirmed regardless of OCR success.

**Given** a PDF containing scanned pages, optionally alongside usable text pages,
**When** the import adapter processes it,
**Then** every relevant scanned page is rendered and OCR-processed, with explicit per-page text/OCR/error/uncertain coverage,
**And** text and OCR paths cannot duplicate activities merely because the same page has both a text layer and image content,
**And** page continuations and source-supported activity order are preserved; neither empty text extraction nor completion of one page is evidence that the whole document was interpreted.

**Given** a screenshot/photo or an uncertain OCR result,
**When** extracted activities are prepared for review,
**Then** retain supported values with minimal source/page provenance and visible unknown/uncertain states,
**And** do not invent cropped, unreadable or missing text; identify affected pages/parts when known and explicitly mark unknown coverage where the missing extent cannot be established,
**And** common tested recognition failures in Norwegian characters, times, columns and row order are exposed for checking rather than silently normalized into confident facts,
**And** Vogn, physical bus, passenger trips and other activities keep their approved distinct meanings.

**Given** a scanned/image Friday-service entry reading 25:30, or an ambiguous recognition of it,
**When** the owner reviews/corrects, saves and reopens the draft,
**Then** supported or manually corrected Friday 25:30 retains Friday service identity and working-day position, with Saturday 01:30 used for calendar presentation,
**And** uncertainty between possible time readings remains explicit until corrected; OCR cannot infer the service date from a calendar-time rendering alone,
**And** identical display times never merge distinct activities or discard their provenance.

**Given** a transient original and an interpreted result are available,
**When** the shared review opens,
**Then** display the source PDF/image beside the interpreted activities using the same correction/add-activity controls and unknown/partial-coverage labels as Story 2.4,
**And** import and save remain unconfirmed regardless of extraction success or server acknowledgement,
**And** reopening retains editable activities, manual corrections and coverage warnings while the source area clearly requests reselection of the original for comparison,
**And** source reselection alone does not reimport, overwrite corrections, confirm work or extend retention.

**Given** a processing error, cancellation, client disconnection or interrupted OCR process,
**When** the request ends or the backend recovers,
**Then** remove uploaded originals, rendered pages and temporary preprocessing copies under the same success/failure/cancel/crash cleanup rules as Story 2.4,
**And** no raw file, rendered-page archive or raw OCR transcript persists in IndexedDB, asset caches, persistent job payloads, logs, repository or CI artifacts,
**And** retain only permissible interpreted fields/provenance within existing draft expiry, offering correction/reselection without pretending the missing result was saved,
**And** one OCR job runs at a time with tested bounded input/resource handling; waiting or interrupted work cannot create a hidden persistent original-file queue.

**Given** an OCR result is retried, arrives after a manual edit or is received during logout/expiry,
**When** the result would be applied,
**Then** reuse Story 2.4's owner/attempt/revision checks and reject silent replacement of newer edits, another draft or confirmed work,
**And** result application and its event use the existing atomic storage/synchronization path without mutating an already submitted batch,
**And** only a valid receipt matching the sent batch changes local/pending status to server-confirmed,
**And** late results cannot unlock private content, bypass unresolved revocation, reset the earliest AD-12 deadline or resurrect expired draft data.

**Given** an OCR import has partial or no usable results,
**When** the owner sees the outcome,
**Then** the review explains what was extracted and which pages/parts remain missing or uncertain, with accessible error/status labels and manual correction/another-file actions,
**And** failure does not silently substitute a fictional shift or mark an empty extraction complete,
**And** unsupported required representative cases remain reported as capability gaps requiring a solution decision, not removed from V1 merely because manual entry exists.

**Traceability:** FR-2 with the approved PDF/JPG/PNG extension; FR-3/4/5 interpretation boundaries; NFR-2/3; UX-DR4/5/38/42/44; AD-1/6 import port/backend OCR, AD-2/5 persistence, AD-10/12 access and retention, AD-13 bounded single-job processing. Carry forward the approved temporal clarification and Story 2.4 side-by-side/reselection/page-coverage behavior.

**Dependencies:** Implemented Story 2.4 and completed Story 2.1 qualification supporting the intended scanned/image cases. Their planning approval is not evidence that OCR works. The existing editor/access/sync stores are reused through 2.4's dependencies. OCR-tool adoption must follow actual qualification; materially negative findings return to the owner before silently changing tools or supported scope.

**Implementation evidence:** Checked representative scanned multipage PDFs, mixed text/scanned pages, JPG and PNG screenshots/photos, unreadable/cropped input and Norwegian text; multi-image shifts with changed file order, overlapping rows, later additions, repeated files, missing/failed parts and prior manual corrections through save/reopen; page coverage and duplicate suppression; Friday 25:30 correction/reopen; failed/cancelled/interrupted processing and restart cleanup; response-loss retry, late-result conflict, logout/expiry; retained draft without original preview. Record actual case coverage and remaining gaps, not an invented universal OCR-accuracy claim. Tests are planned, not run here.

**Size boundary:** Add one OCR adapter path and page/format dispatch to the existing flow, not a new import system or general image editor. No camera-capture UI, automatic plan activation, timetable lookup, active-day revision or mentor workflow. Detailed preprocessing choices follow the qualified evidence; additional unsupported image formats are not introduced.

**Pilot qualification:** Local integrated tests contribute to E8-D and the import portion of E8-P. Representative real-layout evidence, actual host cleanup/resource behavior and the complete driver-confirmation flow still require their respective checks. E8-E remains later actual-shift evaluation. No implementation or readiness check is performed by drafting this story.

**Approval:** Approved by the owner on 2026-09-25 with multi-JPG/PNG shifts, inspectable/controllable file order, additive import into the same unconfirmed draft without duplicates or lost corrections, and explicit uncertainty for cropped/unreadable/missing parts. OCR success is never driver confirmation. Approval concerns planning only; the approved copy in epics.md is canonical.
