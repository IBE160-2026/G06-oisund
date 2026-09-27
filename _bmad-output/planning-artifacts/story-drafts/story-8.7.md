---
status: approved
created: 2026-09-27
epic: E8
story: '8.7'
type: qualification
approved: true
approvedOn: 2026-09-27
dependencies: ['2.1', '2.2', '2.7', '2.8', '4.1', '4.2', '4.3', '4.4', '8.4', '8.5']
---

### Story 8.7: Qualify the Implemented Import and Source Chain for the Pilot Cases

As the pilot owner,
I want a reproducible report showing which representative imports, dated trips and original-source notices the implemented release actually handles,
So that the import/source portion of the pilot decision rests on observed capability and explicit gaps rather than successful fixtures or early candidate investigations alone.

**Acceptance Criteria:**

**Given** the early reports from 2.1, 2.2 and 4.1 and the implemented import, timetable and notice adapters,
**When** the bounded qualification inventory is prepared,
**Then** identify the tested release, adapter/tool versions, configuration, source endpoints/observation dates and sanitized reference cases, linking reusable prior evidence and checking whether it still applies,
**And** cover representative text/two-column/multipage/scanned PDFs, ordered JPG/PNG groups, poor or incomplete inputs, dated trips for lines 20/24/28/42 and the required notice categories from 4.1. List missing cases rather than silently narrowing the inventory,
**And** use independently checked expected dates, times, activities, order and source references; an output produced by the system under test is not its own answer key,
**And** separate actual source/layout observations, historical evidence, labelled synthetic edge cases and untested cases. The early investigations remain early work; this story reuses them and checks the implemented chain rather than postponing or repeating all discovery.

**Given** representative anonymized files with checked expected facts and a permitted processing environment,
**When** they pass through the actual private UI, backend extraction/OCR and persisted draft/review flow,
**Then** compare extracted fields and activity/page order against the reference and report correct, incorrect, missing and uncertain values, including errors only the driver can detect; do not invent an unapproved accuracy threshold,
**And** test all relevant scanned pages, missing/truncated parts and several ordered JPG/PNG files added to one draft without duplicates or loss of corrections. A successful OCR process cannot imply a complete or confirmed plan,
**And** verify side-by-side PDF review while the original is available, preserved edits after reopening with a clear request to select the original again, visible unknowns, and explicit confirmation of only the revision actually reviewed. A concurrent draft change requires renewed review,
**And** exercise failed/cancelled/interrupted extraction and recovery cleanup in the packaged implementation. Known drafts/confirmed plans survive; temporary originals/renderings/processing copies are removed as required by AD-6, with storage/swap limitations reported honestly and no originals in persistent browser caches, logs or queues,
**And** document provider handling under 8.5 before routing real shift files through external ingress. Local success or anonymization alone is not proof of provider handling, and real operational files are not needed for this bounded qualification.

**Given** checked representative trip facts and the adopted targeted Entur queries,
**When** the implemented matcher prepares the whole working day, including later trips and separate work parts,
**Then** compare actual returned identifiers, route/direction, endpoints, ordered stops and date/time evidence against the reference; document the fields and their observed/documented meaning rather than assume a service-date field exists,
**And** test Friday 25:30 as Saturday 01:30 while preserving Friday service date and working-day order through correction, saving and reopening. Include several Saturday 01:30 candidates and require evidence-supported identity or explicit ambiguity rather than choosing by displayed time alone,
**And** distinguish unique match, multiple candidates, successful no match, incomplete response and source failure. Preserve manual corrections when a new or delayed result disagrees, showing source values and the difference instead of silently replacing edits,
**And** verify per-trip preparation coverage and missing stop information across the whole day. Partial coverage never becomes whole-day-ready; a driver-confirmed unmatched trip remains missing source/stop facts, with no fabricated progression or verified physical bus number,
**And** include repeated-stop occurrences in the checked identity cases. A name or proximity alone cannot identify the intended occurrence; source updates cannot silently alter the confirmed plan or active trip context.

**Given** the actual automatic notice adapter and suitable Svipper originals during a stated observation period,
**When** the implemented retrieval/normalization/relevance chain is compared with those originals,
**Then** record coverage separately for each pilot line and available categories, tracing original source to incident identity, version/status, applicability and actual client presentation. Neither a matching headline nor a successful empty fetch proves coverage,
**And** verify full/delta baseline, pagination, stable IDs, supplied validity/update metadata, relevant line/direction/stop references and source access using the qualified semantics from 4.1. Missing update time remains unknown and separate from successful retrieval time,
**And** measure observed fetch intervals and available source freshness evidence separately; central polling targets about two minutes within provider limits, without a two-minute publication-to-display guarantee,
**And** verify updates, explicit endings and uncertain disappearance against available source evidence, plus repeated/out-of-order/partial/failed responses. Retained information is not erased or falsely closed, and fetch time/content hashes do not manufacture source ordering,
**And** where a notice can concern several occurrences of one stop, select a particular occurrence only with documented time or other source evidence; otherwise retain uncertain applicability. General diversion text cannot create a replacement stop sequence,
**And** distinguish an actually verified absence of relevant notices from no suitable observation opportunity. Missing live update/ending/category examples remain unqualified even when labelled fixtures demonstrate correct application behavior; planned-notice coverage does not establish acute or road-by-road deadhead coverage.

**Given** actual adapters and the existing failure contracts,
**When** a bounded set of source timeouts, access/rate-limit failures, malformed/partial responses and delayed responses is exercised safely,
**Then** record which failures were observed and which were induced at the adapter boundary; do not deliberately overload a provider or present injected responses as actual source observations,
**And** check that source-specific status distinguishes no initial data, retained potentially stale data, network recovery awaiting a valid fetch and failed refresh. A successful source fetch is not a server-storage receipt,
**And** report the tested sample, durations and limitations, including unavailable cases. This is not the full-day offline/device/host test campaign and cannot claim those gates passed.

**Given** the case results and reproducible evidence,
**When** the consolidated import/source report is completed,
**Then** give passed, failed, blocked or not-run outcomes per case with expected versus observed result, input provenance and evidence reference, and conclude what works, what requires driver checking/correction and what currently does not work,
**And** map each gap to its requirement and owning implementation story, distinguish a finished investigation from a passed import/source gate, and provide explicit blockers/next decisions for E8-P. Completing an honest negative report does not qualify the capability,
**And** raise inadequate import, timetable or notice coverage for a separate owner solution decision. Do not remove V1 requirements, substitute manual/demo data for automatic capability, choose a new provider/OCR stack independently or introduce bulk NeTEx/GTFS without the AD-7 decision,
**And** retain only sanitized case IDs, minimum dated public-source evidence, aggregate findings and reproducible generic/fictional fixtures. Do not create a permanent private or anonymized operational quality archive, raw OCR/GPS record or retention exception; transient associations follow AD-6/12,
**And** identify which release/configuration the conclusion qualifies and which changes require affected checks to be repeated. E8-D status can reference these findings, but E8-P still requires the separate device, durability, access/deployment and release gates; E8-E remains later actual-shift evaluation.

**Traceability:** E8-P import/source gate; FR-2–5, FR-12–14/18/19 and source prerequisites for FR-15/17/20; NFR-2/3/4; UX-DR4–9/19–21/23/42–44. AD-6 reviewed import/transient originals, AD-7 qualified dated matching and automatic source coverage, AD-8 source lifecycle, AD-5 identity/provenance, AD-12 private evidence limits and AD-13 deployed import/provider boundaries. All AD-1–AD-14 remain unchanged. No sensor accuracy, audio or mounted-readability result is claimed here.

**Dependencies:** Executed 2.1/2.2/4.1 investigations, implemented E2 import/review/matching/day preparation and E4 retrieval/lifecycle/relevance, plus 8.4 packaged runtime and the applicable 8.5 provider/access evidence. Requires representative anonymized references and permitted source access. Missing inputs/evidence are explicit blockers, not fabricated passes. No future E8 story or actual working-shift pilot is needed to complete this bounded report.

**Size boundary:** One consolidated import/source evidence report with targeted integration checks reusing existing harnesses, reference cases and reports. No new production importer/source architecture, all-E2/E4 regression rewrite, unlimited live observation or automatic remediation. Predetermine a bounded case inventory/observation window; if execution needs splitting, preserve every required case and the consolidated decision, with missing evidence visibly incomplete. Functional repairs stay with their owning stories and require rechecking the affected evidence.

**Qualification boundary:** Supplies only import/source evidence for E8-P, never pilot permission by itself. TIME-01 policy is adopted; its implementation/evidence and other E8 gates remain open. This is story planning; no source research, uploads, queries, implementation, actual tests, provisioning, deployment or readiness/final-validation workflow is executed now.

**Approval:** Approved by the owner on 2026-09-27 as scoped: the report must distinguish actually observed source/import coverage from synthetic tests and untested cases. Negative findings require a separate solution decision before they can be considered resolved. Planning approval only; the approved copy in epics.md is canonical.
