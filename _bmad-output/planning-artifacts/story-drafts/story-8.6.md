---
status: approved
created: 2026-09-27
epic: E8
story: '8.6'
type: qualification
approved: true
approvedOn: 2026-09-27
dependencies: ['8.1', '8.2', '8.3', '8.4', '8.5']
---

### Story 8.6: Assemble the Assessable IBE160 Delivery and Record the E8-D Checkpoint

As the project owner preparing assessment,
I want a versioned delivery package with repeatable demonstrations, traceable evidence and an honest requirement-status report,
So that the assessor can inspect the implemented work and its limitations without being given private access or a false claim of pilot readiness.

**Acceptance Criteria:**

**Given** the implemented release and evidence produced by the owning stories and 8.1–8.5,
**When** the delivery package is assembled,
**Then** identify the code revision, application/build/schema and fixture versions, public demo entry, setup/run instructions, test/evidence locations and the known limitations of that exact release,
**And** provide a concise ordinary-PC walkthrough for the basic fictional day, notice/network/position/speed scenarios, explicit restart and labelled PDF, with expected observations and recovery from a failed demo load,
**And** link separately to the private fullstack evidence from 8.3 and reproducible authorized test-environment instructions. Public static demo success must not stand in for React/FastAPI/PostgreSQL evidence,
**And** keep assessor use possible without pilot-owner credentials, operational files or physical GPS. An authorized developer's private-stack reproduction procedure is distinct from the public assessor walkthrough,
**And** record when evidence was produced and which release it applies to. Changed contracts/builds require targeted revalidation; an old passing report is not automatically valid for the packaged release.

**Given** FR-1–25, NFR-1–4, approved UX requirements and AD-1–AD-14,
**When** delivery status is mapped to evidence,
**Then** include every requirement with its owning story, implementation status, evidence reference, tested environment/input type and any unresolved limitation or decision,
**And** distinguish implementation from verification, and verification outcomes as passed, failed, blocked or not run. Mark fictional source/sensor inputs, controlled faults and actual observations explicitly,
**And** preserve the specific limits of each result: available source coverage is not all-clear, a single successful OCR fixture is not representative format qualification, browser simulation is not Lenovo evidence, a functioning Access route is not provider approval, and source success is not confirmed server saving,
**And** include the open 5.4/7.1 time-basis decision and its enforced restrictions, plus any source/device/provider/role/recovery blockers. Do not resolve them by wording, change V1 scope, or present a manual/demo substitute as the required automatic capability,
**And** retain coverage of E6 mentor paths and the E7 complete lifecycle in the evidence index, even where the public demo exposes only a bounded subset. Missing evidence remains visible rather than being omitted from the matrix.

**Given** the saved development log, adopted decisions, actual code changes and test records,
**When** the AI-use and reflection material is prepared,
**Then** describe the tools/workflows used, human decisions and review, observed defects/corrections, quality-assurance methods and their limitations, with traceable examples drawn from the real project record,
**And** cover the process, challenges, chosen solutions and relevant ethical/technical consequences without inventing hours, pilot results, independent reviews or successful checks that did not occur,
**And** separate approved planning from implemented behavior and executed evidence; an approved story or architecture decision is not a passed test,
**And** identify unresolved course-format/submission instructions and use owner-confirmed applicable requirements before final handoff. Historical date references in the brief are not a confirmed deadline, and the old 40–160-hour range is not an available budget,
**And** preserve private information boundaries when selecting examples. Do not publish raw operational records, tokens, private identity/configuration, uploaded originals or unrestricted conversation/log extracts merely to document AI use.

**Given** the separate public demo and the course's assessment-access requirement,
**When** the owner prepares the availability plan,
**Then** record the agreed assessment period including the applicable Christmas period, responsible operator, intended PC browser/environment and a procedure for reporting/recovering access failures. Exact dates/environment must come from owner/course clarification, not an invented deadline,
**And** test a fresh external ordinary-PC browser session without pilot login against the actual demo link, including the documented scenario/restart/export path and separation from the private route,
**And** document the 8.4 Windows restart/sign-in/Docker startup interruption and its effect on demo availability, with recovery responsibilities. An untested uptime promise is not an availability plan,
**And** keep scheduling unknowns marked unresolved and the affected acceptance incomplete until clarified. They do not block preparation of other package contents or justify publishing private access,
**And** no automated course message, credential handoff or submission is implied by this story plan; the user supplies/authorizes external coordination when needed during execution.

**Given** report text, screenshots, PDFs, logs and source/run artifacts intended for assessment,
**When** the shareable package is checked,
**Then** verify that public examples and demonstration data are fictional or appropriately anonymized, with explicit simulation labels and no exact private operational identifiers or secrets,
**And** preserve the distinction between a private user-held PDF and a shareable assessment PDF. The private export exception does not authorize identifiable publication,
**And** link to sanitized evidence rather than archiving private database dumps, originals, raw movement tracks or hidden private copies. Documentation does not create an exception to AD-12 expiry,
**And** check links, version references and run instructions by following the documented paths against the release. Record broken links, non-reproducible cases and missing prerequisites as findings rather than marking the package complete from file presence alone,
**And** keep source/OCR/device/provider evidence provenance intact when summarizing it; do not strip limitations to produce a stronger delivery claim.

**Given** the versioned package, requirement matrix and observed demonstration/fullstack results,
**When** the E8-D checkpoint is presented for owner review,
**Then** state whether the running delivery and its evidence meet the demonstrability boundary, what remains pending/blocked and which specific failures prevent an affirmative E8-D outcome,
**And** require actual repeatable public demo and real private fullstack/database evidence for an affirmative demonstrability claim; screenshots, prepared documents or a deployed URL alone are insufficient,
**And** distinguish a demonstrable delivery with explicitly recorded operational limitations from a fully satisfied V1. An unresolved required feature remains unresolved even if the course demonstration can run,
**And** record the owner-reviewed E8-D outcome and evidence version separately from E8-P and E8-E. A negative or incomplete E8-D result remains so until the relevant findings are resolved and checked,
**And** no E8-D decision authorizes real shifts. E8-P still requires the actual source/import/device/access/host/recovery/release gates, and E8-E still requires the later three-workday evaluation. Neither is marked passed by assembling this package,
**And** preserve capacity/delivery uncertainty and escalate any requested scope change to its own explicit decision. Do not turn missing time into silent removal of requirements.

**Traceability:** E8-D approved delivery boundary; FR-25 ordinary-PC assessment and SM-5, explicit fullstack/database requirement and integrated FR-1–24 evidence; NFR-1–4 with actual limits retained. UX-DR35/37/38/44 and relevant evidence for the remaining approved UX inventory; adopted AD-1–AD-14 remain unchanged. Product Brief addendum records AI-use/quality-assurance and reflection obligations; PRD C-2/C-3 identify assessment-period/environment clarification. This story packages existing evidence and records demonstrability, not a new product capability or replacement pilot gate.

**Dependencies:** Implemented 8.1/8.2 demo, 8.3 private fullstack evidence, 8.4 reproducible runtime and 8.5 protected/private versus public access evidence, plus existing feature/qualification records. Later source/device/integration reports may still be pending and must be listed honestly; they are not a hidden future-story dependency for recording an E8-D outcome. Unknown assessment dates/browser block only the affected availability acceptance until clarified.

**Size boundary:** One versioned delivery/evidence index, concise walkthrough/run references, requirement-status matrix, grounded AI-use/reflection material and explicit E8-D decision record. Reuse existing reports/runbooks rather than recreate all tests or write a second architecture. No new application feature, full E8-P test campaign, real-shift evaluation, automatic external submission or new private archive. This story cannot be marked fully delivered while its own required availability/evidence checks remain unresolved.

**Qualification boundary:** E8-D assesses demonstrability only. Actual import/source consolidation, target-device qualification, integrated host/offline/recovery/releases, the E8-P decision and E8-E field evaluation remain subsequent separate work. The 5.4/7.1 time basis stays open until its explicit solution decision. This is story planning: no package is submitted, no E8-D outcome is issued and no implementation, tests, provisioning, deployment or readiness/final-validation workflow is started now.

**Approval:** Approved by the owner on 2026-09-27 as scoped: E8-D requires a functioning demonstration and documented fullstack testing, with explicit failed, blocked and not-run requirement status. It does not authorize actual shifts. Planning approval only; the approved copy in epics.md is canonical.
