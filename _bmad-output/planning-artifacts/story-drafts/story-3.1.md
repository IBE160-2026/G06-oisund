---
status: approved
created: 2026-09-25
epic: E3
story: '3.1'
type: qualification
approved: true
approvedOn: 2026-09-25
dependencies: []
---

## Epic 3: Follow and Correct the Actual Trip Safely

E3 covers FR-6–11/16, runtime missing-stop fallback under FR-3 and outcome evidence for FR-22; NFR-1/2/4, UX driving/movement requirements and AD-9 bind its implementation. The first slice is early target-device evidence, not implementation of the operational engine. Shared source, storage, access and retention foundations remain E1–2 responsibilities.

### Story 3.1: Qualify Position and Speed Observations on the Pilot Tablet

As the pilot owner,
I want evidence of the position and speed observations actually available on the intended tablet/browser,
So that driving behavior uses realistic quality rules and explicit uncertainty rather than assumed sensor capabilities.

**Acceptance Criteria:**

**Given** the actual pilot Lenovo tablet and Brave browser,
**When** a minimal foreground diagnostic probe is run in a browser context that can exercise the required permissions,
**Then** record the actual device/OS/browser versions, mount/location, permission settings, network arrangement and test conditions,
**And** distinguish unavailable hardware/browser access from permission denial, missing values, stale observations and failed acquisition,
**And** do not assume a native app, accelerometer, background operation or that a desktop simulation qualifies the tablet.

**Given** controlled stationary and moving observations with independently identified reference events,
**When** position and speed are sampled,
**Then** evaluate their quality separately, recording observed age, reported accuracy, delivery intervals and plausible sequence, including null/unknown speed versus a valid zero,
**And** report availability and observed limitations without treating a reported accuracy figure or speed value alone as proof of reliability,
**And** derive evidence-backed candidate quality/freshness rules for later AD-9 implementation, with units, rationale and unresolved cases; do not invent thresholds or change adopted movement-policy boundaries.

**Given** reproducible cases for initial acquisition, denied/revoked permission, loss after valid zero/low/moving speed, recovery, network loss and page/device interruption,
**When** the probe exercises those cases where feasible,
**Then** report which cases actually ran and what observations the browser delivered,
**And** distinguish network loss from loss of usable position/speed; retain the approved rule that unknown speed is not standstill,
**And** identify evidence needed to persist first-valid-speed history and outage timing across restart without giving a fresh startup exception,
**And** label induced or synthetic failures separately from real signal-loss evidence; untested cases remain explicitly unqualified.

**Given** a valid position and speed observation followed by at least five minutes without a new usable observation,
**When** the diagnostic probe records the outage and subsequent recovery,
**Then** document separately the last valid sample time, when position and speed each become too old under the evaluated quality rules, and what the browser actually reports throughout (including silence, errors, null values or repeated stale values),
**And** distinguish the freshness limit from the approved five-minute interaction exception; five minutes never makes the old position/speed usable again,
**And** use independently observed departures/passages as ground truth, with no driver operation while moving, to assess whether the available position evidence realistically supports progression within 100 metres after passage,
**And** report unsupported/uncertain progression during the outage explicitly, including any recovery limits; do not infer observed passage from schedule or elapsed time.

**Given** an observable route segment with independently marked actual stop departure/passage events,
**When** field sampling can be performed safely with a separate observer or unattended capture,
**Then** assess whether observed accuracy/frequency plausibly supports the later stop-progression requirement and record tested conditions and counterexamples,
**And** treat the at-most-100-m target as distance travelled after actual passage/departure, never a proximity radius proving passage,
**And** include the reported approximately 250-m stop-spacing scenario where representative conditions are available, without presenting it as a verified network minimum,
**And** make clear that this probe cannot pass the finished progression requirement: integrated state-machine/device evaluation is still required under E8-P.

**Given** a field observation involves a vehicle,
**When** the test is arranged and conducted,
**Then** it requires no driver interaction with diagnostics while moving and does not rely on an unqualified app for operational decisions,
**And** use consented, anonymized test material and avoid passenger/employee identifiers or real shift documents,
**And** keep only the minimum temporary observation data necessary for analysis, delete raw position traces after analysis and retain sanitized timing/error summaries rather than a permanent GPS track in the app, repository or CI artifacts.

**Given** collected observations and gaps,
**When** the qualification report is completed,
**Then** provide a reproducible case matrix, actual results, limitations and candidate quality rules for position and speed separately,
**And** explicitly conclude what works, what needs uncertain/manual fallback and what is currently unsupported or untested,
**And** negative evidence triggers an owner decision on the further solution; it neither silently removes V1 requirements nor changes AD-9 or the approved startup/five-minute movement policy,
**And** state which follow-up implementation/device cases are still necessary before claiming safe interaction gating or compliant stop progression.

**Traceability:** FR-6/7/8/9/16 sensing prerequisites; NFR-1/2/4; UX-DR14/15/25/44 and EXPERIENCE Responsive & Platform; AD-9 separate position/speed quality and field target, AD-12 no permanent raw GPS track. Wake lock, sound and automatic-theme capability remain separate required device checks; this focused report does not qualify them.

**Dependencies:** Actual target tablet/browser and safe test access, not a future application story. A minimal diagnostic probe may be created during implementation of this qualification task; no production progression/movement engine or service provisioning is required. If the device or safe reference observations are unavailable, report the unqualified cases and obtain the necessary evidence later rather than claiming completion of those tests.

**Evidence boundary:** A report with negative findings can complete the investigation while leaving capability qualification failed. This early E3 work informs implementation and contributes evidence to E8-P; synthetic cases may support E8-D but cannot replace actual device evidence. E8-E remains the later three-workday evaluation. No tests, probe implementation, provisioning or readiness workflow were run while drafting this story.

**Size boundary:** Position/speed acquisition quality and diagnostic evidence only. No automatic trip selection, passage detection engine, operational controls, full recovery, raw tracking feature, browser migration or assumed platform guarantees. Other device capabilities remain explicit subsequent qualification/integration work.

**Approval:** Approved by the owner on 2026-09-25 with a five-minute outage after valid position/speed, separate documentation of sample expiry and browser output, and an honest 100-m feasibility assessment against independently observed passages without driver interaction while moving. Planning approval only; the approved copy in epics.md is canonical.
