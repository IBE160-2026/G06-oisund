---
status: done
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-13
epic: 11
story: '11.4'
dependencies: [V1-03]
implementationStarted: true
owner_acceptance: accepted
accepted_on: 2026-10-25
---

### Story 11.4: Maintain a planned notice

**Stable alias:** V1-13. **Status:** done; Jonas accepted the corrected SMS/text/all-lines delivery on 2026-10-25 and authorized commit/push. Final 61 notice API / 49 browser passes and local rollout/data preservation verified. The original 393 API / 395 browser gate is historical. See [delivery evidence](../../../docs/evidence/11-4-manual-notices.md).
**Depends on:** V1-03.
**Traceability:** FR-12/13/14/24; AC-04/09; SCOPE-02.

**User outcome:** private editor stores title, short and detailed explanations, explicit selected/all-line scope, optional source description/URL, nullable source update/validity and separate entered/checked-at time; SMS-only sources need no URL; demo uses fictional records.

**Acceptance criteria:**
- Owner correction on 2026-10-25: require title and explicit selected/all-line scope. Selected scope requires tags; all-lines is an explicit choice, never inferred. Support short/deep explanation text and optional source description/link, including SMS-only notices. Validate any supplied link as HTTP(S); no website address is mandatory. Workday ownership/expiry applies. Source-update and validity are nullable; entry/edit time is not source check. Only an explicit check action sets checked-at. Fictional records remain isolated. See the corrective dispatch specification for current implementation/verification status.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
