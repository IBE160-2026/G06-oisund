---
status: approved
created: 2026-09-25
epic: E2
story: '2.1'
type: qualification
approved: true
approvedOn: 2026-09-25
dependencies: []
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

The owner can import PDF/images, correct unknowns, resolve dated timetable matches, confirm own activities and physical bus, prepare available day data and review scoped revisions/split work without losing existing facts. FR-2–5 are the primary requirements; NFR-2/3, UX-DR4–8/42/43 and AD-6/7 govern import and preparation. Stories 1.1–1.4 supply the approved private draft foundation for later implementation stories.

This first E2 story is the early OCR qualification already required by AD-6, not an implemented import feature or a complete E8-P pass. It can run independently of E1 implementation; the result informs the later import adapter and review stories. Live transit-source qualification and device qualification remain separate early work, not assumed satisfied by this test.

### Story 2.1: Establish Which Import Cases the Extraction Candidates Can Support

As the pilot owner,
I want representative evidence of how PDF/image extraction handles my shift layouts and failures,
So that the import implementation exposes uncertainty and supports correction rather than relying on untested OCR assumptions.

**Acceptance Criteria:**

**Given** owner-supplied representative anonymized material is available for permitted local qualification,
**When** the qualification set is prepared,
**Then** its case inventory covers text PDF, two-column layout, multipage continuation, scanned multipage PDF, JPG/PNG screenshot/photo and poor-quality or unreadable input,
**And** the expected relevant pages, activity sequence, dates/times, Norwegian text and known ambiguous/missing fields are recorded for comparison,
**And** representative anonymized shifts have a checked answer key for dates, times, activities and ordering; the report lists the formats and failure types actually exercised, separately from planned or missing cases,
**And** missing representative categories are explicitly marked unqualified rather than replaced with fictional evidence presented as real-layout coverage,
**And** no exact operational identifiers, private original or raw OCR transcript is committed to the public repository.

**Given** a documented candidate configuration for pdfplumber and Tesseract behind the intended backend import boundary,
**When** each case is processed through a bounded local qualification harness,
**Then** text extraction is distinguished from OCR and every relevant scanned PDF page is rendered and processed,
**And** the evidence records tool versions, preprocessing, page coverage, duration and errors, with results traceable to sanitized case IDs,
**And** field/row ordering errors, mixed columns, broken Norwegian characters and omitted/duplicated activities are compared with the expected case facts rather than hidden by a successful process exit.

**Given** extracted fields are compared with expected facts,
**When** the qualification report is produced,
**Then** it distinguishes correct, incorrect, missing and uncertain values for service date, activity type, time, route/endpoints and vehicle-duty labels where supplied,
**And** it records which errors were detected by validation and which would require human correction; it does not claim unmeasured certainty or invent a previously unapproved accuracy threshold,
**And** ambiguous source codes remain unresolved, and Vogn is not interpreted as a physical bus assignment,
**And** the report identifies the minimum provenance/uncertainty information the later editable ImportDraft must expose, without making a confirmed plan from extraction alone.

**Given** unreadable input, an extraction failure, cancellation or interrupted processing,
**When** the harness exercises the failure and cleanup paths,
**Then** no output is treated as a confirmed shift and no existing confirmed plan is changed,
**And** the report identifies the direct manual-entry/correction path required by FR-2 and gaps the later review implementation must address,
**And** temporary originals, rendered pages and processing copies are removed after success/failure/cancellation and by recovery cleanup after interruption,
**And** temporary-storage/swap exposure is assessed and recorded as verified, limited or unresolved; deleting a file alone is not claimed as forensic erasure.

**Given** the accepted desktop-first constraints,
**When** representative extraction is measured with one OCR job at a time,
**Then** record processing duration and CPU/memory observations on the measured host, along with any blocking/resource issue,
**And** do not assume these measurements qualify final Docker/Windows restart behavior, acceptable desktop noise or the complete hosted processing chain,
**And** no continuous batch service, external OCR provider or source-file archive is introduced for this investigation.

**Given** all available cases have been investigated,
**When** the report concludes,
**Then** each required format/layout has a supported, conditional, unsupported or not-tested disposition with reproducible evidence and specific limitations,
**And** the conclusion explicitly separates what works, what requires the driver's checking/correction and what does not currently work; even supported extraction still requires the approved explicit driver confirmation,
**And** pdfplumber/Tesseract remain candidates unless the evidence justifies locking them for the intended import cases; partial success never certifies all formats,
**And** a material capability gap returns to the owner for an explicit decision without removing PDF/JPG/PNG from V1 or claiming manual-only input satisfies import,
**And** completing this story means completing the honest qualification result even if it is negative; passing the import gate is recorded separately and is not automatic.

**Given** qualification is complete,
**When** its retained artifacts are prepared,
**Then** keep the sanitized case inventory, expected generic/fictional examples where useful, aggregate findings, versions and reproducible procedure,
**And** retain no uploaded private originals, raw OCR archive or separate permanent anonymized operational quality dataset in the application/repository,
**And** explicitly separate source documents held by the owner from transient copies used by the harness; no deletion of the owner's external originals is implied,
**And** the report lists follow-up implementation and pilot evidence still required, without claiming import UI, driver confirmation, backend crash cleanup in production or provider handling has been implemented.

**Traceability:** FR-2 (PDF review/correction feasibility, extended to JPG/PNG by approved UX), FR-3/4/5 field interpretation boundaries, NFR-2/3; UX-DR4/42; AD-6 mandatory representative-file qualification and transient originals, AD-12 no private archive, AD-13 single OCR job/resource qualification; PRD B-2/B-5. This does not fulfill the functional import stories themselves.

**Dependencies:** No application-story prerequisite for the bounded qualification harness. Requires representative anonymized samples with enough expected facts to evaluate them and a local environment capable of running the candidate tools. Missing samples/tool access are explicit evidence gaps, not permission to mark a case passed. Subsequent import implementation consumes this report together with approved E1 access/draft storage. No real external service provisioning or Cloudflare upload is necessary.

**Evidence boundary:** Qualification is scheduled early within E2. Fictional fixtures may prove deterministic failure handling but cannot establish actual source-layout coverage. The evidence contributes only to the import portion of E8-P and supports honest demonstration claims under E8-D. Actual implemented import/confirmation/cleanup must later pass integrated checks; source coverage, tablet behavior and E8-E remain separate. No qualification work or implementation has been performed by drafting this story.

**Size boundary:** One bounded report and reproducible candidate evaluation, not construction of the complete importer, a generalized parser, an annotation platform or a new retained dataset. No estimate or delivery date is committed. If representative coverage is too broad for one development session, split case execution while preserving one explicit consolidated qualification decision rather than silently dropping cases.

**Approval:** Approved by the owner on 2026-09-25 with representative anonymized shifts and checked answer keys, actual format/failure coverage reported explicitly, and conclusions separating working behavior, required driver checking and current failures. Negative findings require an explicit further-solution decision and never automatically reduce V1. Approval is of the planned qualification story, not a test result. The approved copy in epics.md is canonical.
