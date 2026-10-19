---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-17
epic: 12
story: '12.2'
dependencies: [V1-12, V1-14, V1-15]
implementationStarted: false
---

### Story 12.2: Repeat a fictional assessment

**Stable alias:** V1-17. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-12, V1-14, V1-15.
**Traceability:** FR-25; NFR-2/3; AC-11; SCOPE-02.

**User outcome:** reset fictional data and exercise import uncertainty, missing metadata and failed save without network services or geolocation. Reset cannot affect private data.

**Acceptance criteria:**
- Exercise included failures only: unsupported import, unknown notice metadata, unavailable/stale/lost save and terminal closure. Demo reset affects only fictional configuration/store. No GPS/live feed required; no-login demo cannot authenticate to private API. Keep a separate documented actual fullstack evidence path.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
