---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-13
epic: 11
story: '11.4'
dependencies: [V1-03]
implementationStarted: false
---

### Story 11.4: Maintain a planned notice

**Stable alias:** V1-13. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-03.
**Traceability:** FR-12/13/14/24; AC-04/09; SCOPE-02.

**User outcome:** private editor stores title, explicit line tags, source URL, nullable source update/validity and separate entered/checked-at time; demo uses fictional records.

**Acceptance criteria:**
- Require title, explicit line tags and an HTTP(S) original-source link for real notices. Workday ownership/expiry applies. Source-update and validity are nullable; entry/edit time is not source check. Only an explicit check action sets checked-at. Fictional records remain isolated.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
