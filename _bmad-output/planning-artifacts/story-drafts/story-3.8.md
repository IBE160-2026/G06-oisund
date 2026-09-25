---
status: approved
created: 2026-09-25
epic: E3
story: '3.8'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.7', '2.6', '2.8']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice handles supported diversion sequences and qualified re-acquisition farther along the selected trip. Missing-list manual completion and terminal/return transitions remain separate required slices.

### Story 3.8: Recover Stop Progress Within the Selected Trip After a Diversion or Gap

As the driver,
I want the assistant to use supported diversion stops or recognize a later stop on my current trip,
So that progression recovers without inventing a route, switching lines or treating unobserved stops as visited.

**Acceptance Criteria:**

**Given** a selected trip and available evidence for an alternate stop sequence,
**When** the transit adapter evaluates that sequence,
**Then** verify source identity, applicable service date/direction, validity and its supported association with the selected trip using existing qualified contracts,
**And** keep source/version/fetch provenance and unknown metadata explicit,
**And** a general disruption text, nearby line or inferred road path alone cannot establish replacement stops; source failure cannot create a supported diversion.

**Given** a supported applicable alternate sequence,
**When** it is adopted for operational stop tracking,
**Then** retain the confirmed plan/activity identity, active trip and manual trip pin while updating the applicable source-backed stop sequence,
**And** keep the distinction between operational source sequence and a confirmed plan revision; do not rewrite driver-entered facts or confirmed activity scope through a source refresh,
**And** map existing progress only where evidence supports correspondence; ambiguous mapping preserves manual correction/context as uncertain instead of silently selecting a new stop,
**And** feed supported sequence/progress to the existing 3.5/3.6 engine and view, without a second progression engine.

**Given** no supported alternate sequence, or an interval with unobserved progression,
**When** fresh qualified evidence identifies a later stop of the same selected trip,
**Then** permit re-acquisition beyond the immediately next stop, explicitly testing two and ten stops ahead,
**And** use the actual 3.1 quality rules and plausible direction/sequence evidence; proximity or scheduled time alone is insufficient,
**And** resolve repeated stop occurrences, loops and shared/opposite-direction stops using trip/sequence identity rather than names alone,
**And** test a trip that visits the same physical stop multiple times: unambiguous recognition must identify the correct occurrence in the selected trip's sequence; name, stop identifier or proximity alone is insufficient when multiple occurrences remain plausible,
**And** do not require the driver to press through every intervening stop when recovery is unambiguous.

**Given** a supported later-stop recovery,
**When** it commits,
**Then** record the observed recovery and preserve the earlier observed/manual history,
**And** do not backfill skipped-over stops as GPS-observed visits, infer dwell or manufacture completed work during the gap,
**And** display the newly supported context and any remaining uncertainty without erasing prior manual provenance,
**And** visibly indicate the observation gap even after a later stop is recognized, retaining minimal gap/recovery evidence through save/reopen without inventing exact boundaries where unknown,
**And** a jump to a later stop is not evidence that the 100-m target was met for unobserved departures/passages; test two-/ten-stop recovery with gap visibility and no backfilled compliance claim,
**And** automatic evidence-based recovery may span multiple stops, while each direct manual arrow press still obeys 3.7's at-most-one-stop rule.

**Given** fresh but ambiguous observations, an implausible jump, stale source data or conflicting candidates,
**When** recovery cannot establish a supported same-trip location,
**Then** retain the selected trip and the previous context explicitly uncertain; do not pick the nearest stop/line or silently overwrite a manual correction,
**And** keep 3.7's permitted manual path available according to its qualified signal state and 3.2 movement rules, without demanding interaction during motion,
**And** distinguish source-data uncertainty from actual GPS loss: unknown speed or network failure alone never exposes direct GPS-loss arrows.

**Given** the device is offline or a source update fails,
**When** diversion/recovery is evaluated,
**Then** use only available downloaded sequences with honest provenance/freshness and preserve usable prior data,
**And** do not fabricate an alternate sequence or claim a fresh verification; a later recognized stop may still support local recovery on the selected known sequence,
**And** no usable stop list keeps automatic progression disabled with Stoppinformasjon mangler; manual outcome fallback remains a separate required slice.

**Given** source/observation processing overlaps a new manual correction, trip choice or plan change,
**When** an update would commit,
**Then** revalidate current trip/context/sequence revision and qualified evidence against the latest committed state,
**And** a delayed computation cannot overwrite newer manual work or apply to another trip; recompute against current context where supported,
**And** apply sequence/progress changes and necessary events atomically without duplicate recovery effects or partial identity mapping.

**Given** committed recovery and synchronization/reopen,
**When** storage or transport fails,
**Then** inherit local atomic state/event writes, authenticated FastAPI/PostgreSQL ownership/revision checks and immutable matching-receipt retries,
**And** failed local writes leave the prior committed context with explicit uncertainty/error; lost server responses do not discard locally committed recovery,
**And** separate source version updates from operational revisions; source polling alone does not advance the latter,
**And** persist minimal evidence under access/logout and AD-12 expiry rules, never a permanent raw GPS track; reopening does not refresh evidence or restart movement timers.

**Given** recovery reaches a sequence boundary or data ceases to support the selected trip,
**When** the result is presented,
**Then** preserve honest boundary/missing-data states and never switch to another trip as a recovery shortcut,
**And** final-stop completion and same-route-return triggers remain the separately required transition behavior; this slice must not invent them.

**Traceability:** FR-8 diversion/later-stop recovery, FR-9 uncertainty/manual evidence, FR-6 selected-trip authority, FR-3 source/missing-list boundary; NFR-1/2/4; UX-DR11/15/16/23/38/43/44; AD-1/7 qualified source boundary, AD-2/5 atomic state and source separation, AD-9 evidence-based single engine, AD-10/12 access/retention.

**Dependencies:** Implemented 3.7 and its progression/quality foundations plus 2.6/2.8 qualified transit data. Supported alternate-sequence availability must be evidenced through the existing adapter; a fixture demonstrates logic but does not establish real source coverage. Missing provider support returns a documented solution decision without removing V1 scope or adopting bulk ingestion independently. No future notice-ingestion story is required: notice text is not sequence evidence.

**Implementation evidence:** Supported/unsupported alternate sequence; two-/ten-stop recovery, loops/repeated names/shared directions, manual correction versus ambiguous return, source and GPS failures separately, offline known sequence, stale update races, atomic write/receipt faults, reopen/expiry. Use checked reference cases and actual source/device evidence for qualification. The existing 100-m target remains measured against independently observed passage/departure under reliable positioning; unexplained gaps do not justify fabricated compliance. Tests are planned, not run.

**Size boundary:** Selected-trip sequence validation and re-acquisition using existing adapter/state engine. No general road routing/map-matching service, notice-text route inference, new source pipeline, trip switching, manual missing-list outcomes or final-stop transitions.

**Pilot qualification:** Repeatable recovery cases contribute to E8-D. Actual alternate-sequence source support and observed recovery accuracy/latency require E8-P evidence; failures remain recorded gaps rather than passed requirements. E8-E remains subsequent actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with correct stop-occurrence identity required for repeated visits and a visible retained observation gap. Later-stop recovery does not establish 100-m compliance for unobserved departures/passages. Planning approval only; the approved copy in epics.md is canonical.
