---
status: approved
created: 2026-09-26
epic: E4
story: '4.1'
type: qualification
approved: true
approvedOn: 2026-09-26
dependencies: []
---

## Epic 4: Understand Relevant Notices and Their Sources

E4 delivers automatic source-backed notices, relevance, metadata, version lifecycle, safe presentation/acknowledgement and audio, with honest initial/partial failures. It covers FR-12–15/19, source-refresh FR-18 and shared FR-16; NFR-1–4, UX-DR9/14/19–22/23/25/38–41/44 and AD-7/8 govern the applicable slices. E2 supplies dated day/trip identity; E3 supplies actual context, progression and the shared movement policy. E8 qualifies the integrated result; it does not supply a missing production adapter.

### Story 4.1: Qualify Automatic Svipper Notice Coverage and Source Semantics

As the pilot owner,
I want documented evidence of the notices and metadata the candidate source actually supplies for the pilot lines,
So that automatic retrieval can be built on verified source behavior without promising unsupported coverage or freshness.

**Acceptance Criteria:**

**Given** the adopted Entur SIRI SX/TRO candidate and pilot lines 20, 24, 28 and 42,
**When** the qualification investigation examines current official documentation and actual responses,
**Then** identify the exact tested endpoint/dataset, provider namespace, access conditions, request scope, timestamps and reproducible query method,
**And** verify provider identification and line/stop references rather than assuming the TRO label or a successful response proves Svipper coverage,
**And** distinguish documented provider guarantees, actual observations, inferences and unresolved assumptions; do not introduce a new source architecture independently.

**Given** representative Svipper originals for planned works, closures, diversions or moved stops,
**When** actual candidate responses are compared with the original source over a stated observation period,
**Then** record a reference matrix with original link/identifier, affected line(s), direction/stops/area and validity where supplied, candidate match or absence, and the evidence supporting that comparison,
**And** report results separately for the four pilot lines and tested notice categories, including overlapping 20/24 and multi-line incidents where examples are available,
**And** an empty observation period or absence of a suitable example means untested coverage, not proof of complete coverage; explicitly identify unavailable cases,
**And** label fixtures, historical examples and induced failures separately from observed live notices; a matching headline alone is not proof of incident identity.

**Given** source notice identity, references, timestamps and validity fields,
**When** their meaning and mapping are examined,
**Then** document stable source-namespaced incident IDs, version/order evidence, original-source access, source update time, retrieval time and all supplied validity periods as separate facts,
**And** document calendar dates/timezones and overnight validity rather than treating display time as trip service-date identity; cross-reference qualified E2 identity mapping when available,
**And** missing source update time remains unknown, with the required Kildens oppdateringstid er ukjent behavior alongside last successful retrieval; fetching cannot manufacture update time,
**And** document how source references support route/direction/stop/area applicability and where they do not; roadworks text alone cannot establish road-trajectory precision or a replacement stop sequence.

**Given** documented and observed full/delta responses, pagination and source cursor/baseline behavior,
**When** retrieval is repeated and interruption/restart scenarios are investigated,
**Then** distinguish empty changes, complete confirmed absence of active notices, partial results and failed retrieval,
**And** identify how to establish/resume the baseline and finish pagination before claiming completeness, with examples or explicitly untested cases,
**And** document timeout, access failure, throttling and malformed/partial response handling needed by the adapter; none establishes all-clear conditions or erases retained notices,
**And** verify limits relevant to central source/area polling around two minutes, including feasible retry/backoff behavior; do not multiply requests per driver or exceed provider limits to test a target.

**Given** notice updates, endings, expired validity, disappearance and repeated or out-of-order records,
**When** actual source evidence and labelled controlled examples are examined,
**Then** report which fields establish identity, meaningful change, ordering and explicit closure, including sparse closure messages and multiple validity periods,
**And** distinguish confirmed closure, expired validity and uncertain disappearance; absence from an incomplete response is never closure,
**And** neither a new fetch timestamp nor a content fingerprint proves source version ordering; document the handling/decision needed when ordering cannot be established,
**And** preserve the AD-8 responsibility split: backend source facts versus client day/version-specific seen, registered and hidden state. This report does not implement that lifecycle.

**Given** time-correlated observations of the original and candidate source,
**When** polling and freshness feasibility are assessed,
**Then** distinguish requested polling interval, observed successful fetch interval, provider update cadence and any measurable original-to-candidate delay,
**And** report tested duration, missed observations, uncertainty and limits rather than claiming a two-minute end-to-end freshness guarantee from a two-minute poll,
**And** planned-notice coverage does not imply complete acute-event, congestion, cancellation or road-by-road deadhead coverage; unsupported acute delivery remains unknown even though the approved UX can present such a notice if supplied.

**Given** the investigation finishes with positive, negative or incomplete evidence,
**When** its report is reviewed,
**Then** conclude what automatic retrieval and metadata mapping demonstrably support, what requires original-source checking or explicitly uncertain presentation, and what currently fails or remains untested,
**And** list blocking gaps and the next concrete evidence/solution decision; negative findings cannot silently remove V1 requirements or replace automatic retrieval with manual/demo notices,
**And** distinguish a completed investigation from passed source qualification; do not certify E8-P from the report alone or choose a replacement provider independently.

**Given** queries, examples and evidence are retained for reproducibility,
**When** artifacts are written,
**Then** use public source notices and anonymized reference cases without private shifts, account credentials, tokens or raw GPS traces,
**And** retain only the minimum dated source excerpts/metadata needed to substantiate findings, with origin and observation time; no permanent private pilot archive or unrelated application database is introduced,
**And** any temporary probe is limited to this qualification task, with no service provisioning, production scheduler or operational app flow required.

**Traceability:** Qualification prerequisites for FR-12/13/14/18/19 and FR-15 source identity/newness; NFR-2/3/4; UX-DR9/19/20/21/23/44; PRD B-1 and the approved Early Qualification Queue. AD-7 source coverage/relevance/central polling and AD-8 identity/version/closure are primary; AD-1 adapter boundaries, AD-5 identity separation and AD-12 evidence privacy remain applicable. All AD-1–AD-14 remain unchanged.

**Dependencies:** Source documentation/access and suitable Svipper reference examples, not a future E4 implementation. Reuse 2.2 transit-identity findings if available; missing mappings are explicit evidence gaps, not guessed identifiers. A minimal diagnostic query/probe may be used when this story is executed, without the finished application. Lack of live updates/closures during the observation period leaves those cases unqualified; use labelled supporting cases and record the remaining live check.

**Evidence boundary:** A dated source-qualification report, comparison matrix and minimal reproducible requests/examples. Report exact cases actually tested and separate documented semantics from observed behavior and fixtures. No source research or tests are executed during this story-drafting step.

**Size boundary:** One focused source qualification investigation only. No production adapter, persistent polling service, notice database/lifecycle implementation, relevance engine, UI, audio, source replacement or new external service. Later implementation slices own those outcomes and their fullstack persistence/access/failure/privacy behavior.

**Pilot qualification:** Labelled source fixtures can support later E8-D behavior demonstrations but do not prove live coverage. Actual source evidence contributes to E8-P together with the implemented adapter and integrated target-environment behavior. E8-E remains the subsequent three-workday field evaluation. Investigation completion is not pilot permission.

**Approval:** Approved by the owner on 2026-09-26 with the stated scope and explicit distinction between documented coverage, missing metadata, retrieval failure and actual absence of notices. Negative findings require a separate solution decision. Planning approval only; the approved copy in epics.md is canonical.
