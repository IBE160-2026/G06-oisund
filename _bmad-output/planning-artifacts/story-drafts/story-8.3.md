---
status: approved
created: 2026-09-27
epic: E8
story: '8.3'
type: qualification
approved: true
approvedOn: 2026-09-27
dependencies: ['2.12', '4.8', '5.13', '6.10', '7.6', '8.2']
---

### Story 8.3: Produce Reproducible Evidence of the Private Fullstack Day Lifecycle

As the project owner preparing the IBE160 delivery,
I want a repeatable verification of the actual private React/FastAPI/PostgreSQL flow with wholly fictional data,
So that fullstack persistence, recovery and lifecycle claims are supported by observed results rather than the public static demo.

**Acceptance Criteria:**

**Given** the implemented E1–E7 application and an isolated qualification environment,
**When** the evidence run is prepared,
**Then** use the actual private frontend, Python/FastAPI validation/authentication and PostgreSQL 18 with the application's migrations and contracts; neither SQLite, an in-memory server store nor a mocked success response can substitute for persistence evidence,
**And** identify the code/build, schema/API versions, configuration, browser, fixture versions and commands necessary to reproduce the run. Document environment prerequisites and stop clearly when they are missing,
**And** provision only fictional test identities/data in this isolated environment through controlled setup; run user actions through ordinary private sign-in and authorization, not a bypassed production login or public-demo endpoint,
**And** make environment checks prevent fixture seeding, fault injection, clock controls or cleanup against the pilot database/host. Test helpers are not published in the private production or public demo runtime,
**And** record which external inputs are fictional adapters, which import components actually execute and which layers are real. Simulated source/sensor inputs do not turn this run into Entur/OCR-layout/Lenovo qualification.

**Given** a versioned fictional fixture set with expected dates, ordering, plan revisions, identities and outcome provenance,
**When** the operator follows the documented lifecycle procedure,
**Then** exercise one own-day path and one mentor path using existing application actions: import through the real backend interpreter, inspect uncertain fields, manually correct, explicitly confirm, prepare available data, start within valid ordinary authorization, perform permitted fictional-input operations, end/abort, review, read summary and export PDF,
**And** use one defined text-PDF import case plus a bounded image/scanned case through the implemented OCR path, documenting the exact formats/cases actually run and known failures. A directly seeded confirmed plan cannot count as tested import/review; representative real-layout coverage still comes from 2.1 and later E8-P qualification,
**And** include service/calendar dates crossing midnight and a manual correction that differs from the fictional route source. Preserve the correction, day ordering, explicit confirmed revision and uncertainty through persistence and recovery,
**And** the mentor path includes separate own work and only partially accompanied evidence, with known unaccompanied remainder that must be removed on own-day closure. Reuse E6's fixtures/contracts; do not invent new role or attribution rules,
**And** preserve actual displayed notice versions and source/manual/unknown status in the summary and the revision-bound local PDF. All retained/exported evidence in this run is labelled as fictional qualification data,
**And** exercise normal ending in one path and explicit abort in the other; neither terminal choice certifies uncertain physical activity. Initial review ends only through its explicit confirmation, and retained entry is read/export-only afterward.

**Given** a representative confirmed plan change, operational correction and terminal/review event in these paths,
**When** each passes from the client to the backend,
**Then** correlate the visible local/pending/server-confirmed state with committed IndexedDB state/outbox, the authenticated request and matching receipt, and independently read the expected PostgreSQL records/revision,
**And** verify ownership, event/batch identity, expected revision and domain effects with sanitized test identifiers; an HTTP success, screenshot, empty queue or client cache is not sufficient evidence of database commitment,
**And** demonstrate database-backed recovery after restarting the application services while retaining the test database volume, then loading the result in an authorized clean browser context without its former local data. No automatic writer transfer or revival of an ended day is permitted,
**And** verify that requests with no authority, another test owner or only a different concrete-day scope cannot read private metadata/content or apply changes. Rejected writes leave the database unchanged,
**And** inspect private source-file cleanup after interpretation and end-of-day linked-plan trimming, without copying original uploads, secrets or raw GPS tracks into the evidence report.

**Given** existing E1/E5/E7 fault hooks and test procedures scoped to the isolated environment,
**When** controlled failures are injected into the same actual stack,
**Then** demonstrate a local transaction failure before completion, a PostgreSQL transaction failure, and a server commit whose response is lost. Show their different visible and durable outcomes,
**And** retry the lost-response operation with the identical immutable batch and verify one domain effect, one accepted receipt identity and no extra revision increment from retry. A mismatched receipt must not mark the client work confirmed,
**And** interrupt actual client access to the test backend while retaining local data, make a permitted correction, restart the client with prepared assets, then restore connectivity and verify preservation and reconciliation. A browser online flag alone is not proof of backend/source recovery,
**And** use the existing stale-writer/revision cases to prove rejection without silent overwrite. Preserve permitted pending work for explicit handling rather than automatically taking authority or rewriting old batches,
**And** test old-request versus closure ordering through the real 5.13 PostgreSQL transaction/fence contract, with an actual E6 retained projection. Distinguish retired-original outcome, local closure and the new closure receipt; old payloads cannot restore discarded linked data,
**And** reuse relevant existing automated evidence where its build/contracts/fixture conditions match; execute the composed path and its necessary integration gaps rather than duplicating every feature test or claiming old results validate changed code.

**Given** the composed day has retained results, pending events, review state, PDF temporary data and summary/greeting metadata,
**When** logout, terminal cleanup and the fixed data deadline are tested,
**Then** check current access and deletion behavior in client, backend and PostgreSQL, including another tab, delayed response and a restart before private display,
**And** verify removal of all applicable private copies under the existing AD-12 inventory, plus rejection of late reads/writes independently of asynchronous purge. Preserve unrelated test-day/public-source data; do not claim deletion just from a hidden screen,
**And** include a never-ended fixture expiring from planned final end without becoming completed, and an ended fixture retaining an earlier binding limit despite retries/review/export,
**And** distinguish a downloaded user-held PDF from app-managed buffers/copies; do not claim the app deletes external files. Evidence must not introduce a permanent private backup or pilot archive,
**And** any accelerated test clock or fault injection is explicitly labelled as a test mechanism. It cannot establish TIME-01 server acceptance or Tg/D behavior on the real candidate; late activation is rejected and uncertain-time cases remain restricted pending actual evidence.

**Given** observed results from the repeatable procedures,
**When** the evidence report is assembled,
**Then** list each case with requirement/story reference, starting conditions, expected result, actual result, execution identity and supporting sanitized UI/API/database observations,
**And** distinguish passed, failed, not run and blocked cases; separately state whether the feature is implemented and what was actually verified. Do not substitute a planned test or fixture expectation for an observed pass,
**And** provide reproducible run/reset instructions scoped to the fictional test environment, a concise sequence for inspecting frontend/backend/database behavior, and evidence location/version references. Another authorized developer must be able to repeat the procedure from documented prerequisites,
**And** check the report, screenshots, PDFs and diagnostic excerpts for real operational identifiers, credentials, cookies, tokens and private payloads before using them in assessment material. Use wholly fictional fixtures for shareable artifacts; no uncontrolled database dumps,
**And** report failure and limitation ownership without automatically changing V1 or architecture. Fixes remain the responsibility of the owning E1–E7 feature stories; this evidence slice is not permission to replace missing behavior with a demonstration stub,
**And** keep this report separate from the later complete delivery/reflection/AI-use package and formal E8-D decision. It contributes the private fullstack evidence but does not itself pass E8-D, E8-P or E8-E.

**Traceability:** Explicit PRD fullstack/database obligation and E8-D private end-to-end evidence; selected integrated FR-1–5/9/14/17–24, UX-DR23/31–36/38/44 and NFR-2/3, with controlled NFR-1/4 observations limited to the stated environment. Shared import, role, notice and lifecycle criteria remain in their owning E1–E7 stories. AD-1 actual adapters with declared fixture boundaries, AD-2 client transactions/assets, AD-3 real React/FastAPI, AD-4 PostgreSQL 18, AD-5 immutable batches/receipts/atomicity, AD-6 transient import originals, AD-8 provenance, AD-9 terminal/role rules, AD-10/11 authority, AD-12 cleanup, AD-13 separated test/private/demo environments and AD-14 versioned evidence. All AD-1–AD-14 remain unchanged.

**Dependencies:** Implemented relevant E1–E7 slices through 7.6, including E2 extraction/review, E5 recovery/settlement and E6 mentor projections. 8.1/8.2 establish the public-demo evidence boundary; this story uses a separate private test environment. Local isolated deployment of the actual application suffices; public hostname/tunnel/assessment hosting and future E8 stories are not prerequisites. Missing implementation or representative evidence is reported blocked/unverified, not silently supplied by this qualification story.

**Size boundary:** One bounded own-day/mentor lifecycle evidence pack and selected persistence/fault/expiry cases, reusing existing test infrastructure. Not a new application implementation, complete security audit, all-feature regression rewrite, live-source/device qualification, production provisioning, publication or final readiness review. Full target-environment gates, delivery documentation and field evaluation remain later E8 work.

**Qualification boundary:** Real local fullstack/database evidence contributes to E8-D. Fictional source/sensor inputs and a controlled desktop environment cannot pass E8-P's actual source/OCR/device/access/host requirements. E8-E follows E8-P with three actual workdays. TIME-01 policy is adopted but untested; capacity/delivery remain unresolved. This story is being planned only: no tests, application changes, provisioning or deployment are executed now.

**Approval:** Approved by the owner on 2026-09-27 as scoped. Tests must demonstrate the actual client-to-PostgreSQL chain and report passed, failed, blocked and not-run cases distinctly. The evidence contributes to E8-D and does not replace E8-P. Planning approval only; the approved copy in epics.md is canonical.
