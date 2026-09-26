---
status: approved
created: 2026-09-26
epic: E7
story: '7.4'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['7.3', '5.2', '5.12']
---

### Story 7.4: Export the Daily Summary as a Private Local PDF Offline

As the pilot owner reviewing an ended or aborted day,
I want to explicitly export its summary as a readable local PDF, including while offline,
So that I can keep a user-controlled copy with the same evidence and uncertainty as the summary.

**Acceptance Criteria:**

**Given** a permitted retained daily summary from 7.3 and the required verified application assets are available,
**When** the owner explicitly requests PDF export,
**Then** generate the PDF locally from one coherent summary revision without requiring a live server, source lookup, external fonts or a remote conversion service,
**And** use the existing authorized local result, or existing authenticated FastAPI/PostgreSQL summary retrieval when needed and available, without adding a server PDF store or export archive. A missing local result remains unavailable offline rather than being invented,
**And** export remains optional for the user; day completion, initial-review completion and return navigation cannot trigger automatic export or require it,
**And** include the PDF generation resources in existing asset readiness and compatible-update checks. Missing/incompatible resources produce a recoverable error, not a claim that PDF export works offline.

**Given** the selected summary revision contains own work, accompanied portions, takeovers, displayed notices, corrections and source problems,
**When** the PDF content is composed,
**Then** preserve the same permitted content and distinctions as 7.3: planned versus observed facts, completed/skipped/aborted/uncertain/manual outcomes, exact actually displayed notice versions, source attribution and missing evidence,
**And** keep own activities and driving separate from actually accompanied portions and manual takeover events. Exclude the other person's unaccompanied remainder and deleted source originals; do not reconstruct either from newer source data,
**And** identify the combined own day, service date, relevant calendar dates, summary revision and export-generation time, distinguishing that time from actual event times and verifiable timing evidence. Unknown occurrence times remain unknown,
**And** show the snapshot's local/server receipt status, unresolved source/data gaps and applicable own-day expiry. A locally saved result may be exported with its pending status; export does not certify server acceptance or missing physical evidence,
**And** if required summary sections cannot be read consistently, explain the failure and preserve retry. Known gaps already represented as uncertainty in a coherent summary remain exportable and visibly incomplete in the same way as that summary; a rendering/load failure cannot silently omit a section.

**Given** a short or long summary and the adopted document design,
**When** pages are laid out,
**Then** produce a portrait A4 document with readable headings, outcome table, notice/evidence detail and numbered page footers, following DESIGN's PDF hierarchy and type references rather than capturing the tablet screen,
**And** paginate all permitted content across as many pages as needed; the two-page mockup is not a limit. Keep headings, continued rows/sections and provenance understandable across page breaks,
**And** retain Norwegian characters, long stop/source names, multiline notices and readable textual outcome labels. No clipped or silently truncated evidence, unreadably shrunk type or colour-only uncertainty indication is acceptable,
**And** keep text selectable and in a sensible document reading order; inspect the rendered pages as well as extracted text when verifying export.

**Given** export starts while review is open or saved summary data can change,
**When** generation and browser handoff occur,
**Then** bind the export to the exact coherent revision selected at the request, without mixing subsequent confirmations, receipts or corrections into its pages,
**And** if a newer result becomes available, keep the export's revision/status explicit and allow a new user-initiated export; do not silently label the older file current or modify a file already handed to the user,
**And** generation, download initiation, cancelling a file dialog and reading the PDF cannot complete the initial review, close editing, resume operations or alter original end/retention times. 7.2's explicit review-completion boundary remains controlling,
**And** repeated explicit exports may create separate user-held files but do not create operational events, duplicate manual confirmations or change notice seen/registered state.

**Given** the owner starts, cancels or retries export,
**When** the app generates the file and hands it to the browser's supported local-file mechanism,
**Then** provide accessible progress, error and retry feedback while preserving the ended day, its summary and review phase,
**And** distinguish PDF generation from browser handoff and confirmed saving. Claim a saved file only when the chosen mechanism supplies reliable confirmation; otherwise report the observed handoff and let the user locate/check the downloaded file,
**And** handle cancellation, generation failure, denied/unavailable file capability, storage failure and an interrupted tab without claiming success or automatically replaying a download on restart,
**And** retry uses an explicitly selected currently permitted summary revision and current access checks; failure does not resume the day, discard valid work, reset expiry or require a network-only workaround for the offline requirement.

**Given** a private export request or an in-flight export,
**When** data is read and immediately before a new browser handoff,
**Then** enforce current owner/day access, logout/pending-revocation lock, applicable interaction restrictions and AD-10/12 expiry; an ended day does not prove standstill or resolve unknown role,
**And** cancel undelivered private output and release app-managed temporary data when a known lock/deletion/expiry invalidates access. Old tabs, delayed completion callbacks and stale snapshots cannot hand off a newly prohibited export or restore deleted content,
**And** keep generated private PDF buffers temporary and outside permanent caches, backend storage, logs, repository and CI artifacts. No automatic upload, publication or sharing is performed,
**And** explain before handoff that a user-held PDF can contain actual operational identifiers and lies outside automatic app cleanup. Once handed off, the app does not claim it can revoke or delete that external copy; showing app-data expiry must not imply expiry of the exported file,
**And** export never extends authority or the data clock. Unverifiable offline end time follows 7.1's earliest-applicable-limit rule; this story does not resolve the 5.4 timing-evidence decision.

**Given** an explicitly fictional/demo summary supplied through the isolated demo contract,
**When** the same PDF renderer is used,
**Then** visibly mark every page as demo/simulation, including overflow pages, and preserve simulated evidence labels,
**And** permit only fictional/anonymized demo inputs and never load private credentials, operational records or a private fallback. Private actual identifiers must not enter assessment artifacts,
**And** verify the renderer boundary with fixtures now; integration with the full public demo remains E8 work and is not a prerequisite for private export.

**Given** anonymized/fictional fixtures, the prepared client and existing backend/summary contracts,
**When** the story is verified,
**Then** export offline after restart with the server and external resources unavailable; check a short summary and a document longer than two pages against the exact selected summary revision,
**And** render and inspect every page for long Norwegian names, multiline notice versions, cross-midnight dates, uncertain/manual outcomes, source gaps, pending receipts and own/accompanied/takeover separation; compare extracted content to the fixture to detect omitted or duplicated evidence,
**And** test an open review with a concurrent correction/receipt, explicit review completion, cancelled or failed handoff, blocked file capability, retry and tab interruption; verify no false saved status, lost review opportunity or replayed download,
**And** test logout, pending revocation and expiry during generation, including another tab and a delayed callback, plus cleanup of app-owned temporary output. An already user-held file is explicitly outside that cleanup claim,
**And** verify every page of a multipage demo export is marked and contains no real identifiers. Use controlled browser evidence for E8-D; qualify actual offline generation, download/opening and readability on Lenovo/Brave before E8-P approval.

**Traceability:** Primary FR-23; exported FR-22 evidence, offline FR-17, bounded FR-1/20/24 and demo-export boundary FR-25. NFR-1–4; UX-DR23/33/35/36/38/39/44. EXPERIENCE PDF document, recoverable export failures and accompanied-only evidence; DESIGN portrait A4 document, hierarchy and page numbering. AD-2 offline assets/data, AD-3/4 existing fullstack summary contracts, AD-5 accurate receipt status, AD-8 source/version evidence, AD-9 terminal/review semantics, AD-10 access, AD-12 temporary copies and user-held-PDF exception, AD-13 demo isolation and AD-14 compatible assets. All AD-1–AD-14 remain unchanged.

**Dependencies:** 7.3 coherent summary read model and its inherited 7.1/7.2 access/review boundaries; verified assets and compatible builds through 5.2/5.12. Uses existing FastAPI/PostgreSQL data contracts; introduce no tables unless this bounded export behavior actually needs them. Public-demo integration, retained-day browser and closing affirmation are later independent slices.

**Size boundary:** One local PDF renderer and explicit browser export flow, with pagination, revision binding, offline assets, access/error handling and isolated demo labelling. No CSV, generic report designer, remote converter, automatic sharing, PDF archive or new evidence collection. CSV remains optional outside required V1 scope; required PDF behavior is not removed if qualification fails.

**Pilot qualification:** E8-D can demonstrate correctly rendered fictional fixtures and controlled failures. E8-P requires actual Lenovo/Brave offline export and file retrieval/opening, lifecycle/race and readability evidence; unsupported capability becomes a separate solution decision, not a silent V1 exception. E8-E remains field evaluation. No implementation, actual PDF generation or device tests occur during story planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. The owner affirmed one-revision offline PDF generation, preserved uncertainty and receipt status, no unsupported claim that browser handoff confirms saving, and the necessary explanation that a downloaded PDF is outside app cleanup. Planning approval only; the approved copy in epics.md is canonical.
