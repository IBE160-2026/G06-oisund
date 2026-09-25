---
status: approved
created: 2026-09-25
epic: E3
story: '3.6'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.1', '3.5']
---

## Epic 3: Follow and Correct the Actual Trip Safely

Recovered from the story presented and approved in conversation after the tool interruption. This records normal-route progression, not a claim that implementation or qualification has occurred.

### Story 3.6: Advance the Stop Sequence from Qualified Actual Movement

As the driver,
I want the stop display to follow actual arrival, departure and passage within my selected trip,
So that it remains useful during delays and when passing without stopping.

**Acceptance Criteria:**

**Given** an active trip with a supported stop sequence,
**When** observations are evaluated,
**Then** use the actual quality limits established in 3.1 within the shared AD-9 state machine,
**And** scheduled time or proximity alone never proves arrival, departure or passage; position and speed quality remain distinct.

**Given** observations support actual arrival or departure within the selected trip,
**When** progression is committed,
**Then** update the state consumed by 3.5 with supported stop identity and observed provenance,
**And** preserve the adopted at-stop/between-stop hierarchy without making an upcoming stop a confirmed current location.

**Given** passage without stopping is supported by qualified observations,
**When** progression advances,
**Then** do not require a zero-speed observation or invent dwell,
**And** remain within the supported sequence of the selected trip without fabricating boundary stops.

**Given** independently observed actual departure or passage, including passage without stopping,
**When** the implemented progression is measured on the target device,
**Then** measure distance travelled from that reference event to the updated display and test the at-most-100-m requirement,
**And** use a separate observer or unattended capture without driver operation while moving; neither proximity nor the algorithm's own detection serves as independent ground truth,
**And** record tested conditions, actual distances and deviations; if the target is not achieved, document the failure and do not mark the requirement fulfilled,
**And** actual qualification remains an E8-P obligation, distinct from deterministic logic tests and planning approval.

**Given** stale measurements, position jumps, noisy or otherwise insufficient evidence,
**When** progression cannot be established,
**Then** retain the last committed stop context explicitly uncertain rather than guessing advancement,
**And** retained context is not a new observation, and noise/repeated observations must not produce false advancement or duplicate events.

**Given** an active trip selected automatically or manually,
**When** delays, other departure times or nearby lines occur,
**Then** keep progression within that trip and preserve the manual choice,
**And** reject stale results evaluated for a superseded trip/context rather than transferring its stop index to the current trip.

**Given** a supported progression change,
**When** local storage and rendering occur,
**Then** atomically save state and its necessary event before showing the new progression,
**And** a failed local write cannot appear as successful advancement; retain committed context with explicit failure/uncertainty,
**And** reopening restores context without renewing observation freshness or retention, preserving movement history and access locks.

**Given** committed progress is synchronized,
**When** the backend accepts a batch or its response is lost,
**Then** reuse the inherited authenticated FastAPI/PostgreSQL ownership/revision checks, atomic receipt handling and immutable retries,
**And** only a valid matching receipt changes server-confirmation status; server/network failure does not discard locally committed progress,
**And** preserve minimal necessary evidence under AD-12 without a permanent raw GPS track; downloaded data supports local operation without implying new source retrieval.

**Traceability:** FR-7/8 normal progression, foundational FR-9 uncertainty and FR-6 active-trip authority; NFR-1/2/4; UX-DR10/11/15/16; AD-2/3/5 committed local state and fullstack persistence, AD-9 qualified shared state machine, AD-10/12 access/privacy. All adopted decisions remain binding.

**Dependencies:** Implemented 3.5 with its trip/permission/data prerequisites and actual quality evidence from 3.1. Story approval is not proof of qualified sensor behavior. Deterministic normal-route progression is independently testable before the later fallback/transition stories.

**Implementation evidence:** Supported arrival/departure and passage without stopping, delays and adjacent lines, stale/noisy/jumping observations, duplicate samples, trip-context changes, failed writes/receipts and uncertain reopen. Independently observed field passages/departures measure the 100-m outcome and explicitly record failures. No tests were performed during drafting.

**Size boundary:** Normal supported progression within the selected trip. Manual stop correction, diversion recovery and final-stop/same-route-return transitions remain subsequent required stories; no requirement is removed or marked implemented by this approval.

**Pilot qualification:** Repeatable logic contributes to E8-D. Actual 100-m performance requires E8-P evidence against independent observations, with failure recorded honestly. E8-E remains subsequent actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the presented scope/criteria and explicit independent-ground-truth testing including nonstopping passage; missed 100-m targets must be documented, never marked fulfilled. Registration recovered after the tool interruption. Planning approval only; the approved copy in epics.md is canonical.
