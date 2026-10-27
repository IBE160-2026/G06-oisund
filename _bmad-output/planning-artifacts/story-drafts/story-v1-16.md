---
status: review
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-16
epic: 12
story: '12.1'
dependencies: [V1-05, V1-12, V1-13]
implementationStarted: true
technicallyReadyOn: 2026-10-27
ownerAcceptance: pending
---

### Story 12.1: Enforce the retained-data boundary

**Stable alias:** V1-16. **Status:** review; technically verified in isolated worktree, owner manual acceptance pending.
**Depends on:** V1-05, V1-12, V1-13.
**Traceability:** FR-1/2/24; NFR-3; AC-06/09; SCOPE-02.

**User outcome:** end-to-end expiry and deletion across drafts, plans, outcomes and associated private notices; no uploaded originals in logs/caches/repository. Late/stale requests cannot recreate expired work.

**Acceptance criteria:**
- Verify draft creation+7d and confirmed min(planned-end+7d, server-end+7d) deadlines without sliding renewal. Deny immediately, purge at startup/hourly, remove associated outcomes/notices/operation metadata and prevent late recreation. Inspect original cleanup, private no-store/back behavior and absence of private persistent browser/log/repository data.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.

## Local integration authorization — 2026-10-27

Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.

Jonas explicitly authorizes separate local commits, integration in order 12.1 then 12.2, automated verification and local main merge before manual acceptance. Earlier no-commit/no-merge instructions describe the historical run and are superseded for this integration. Status remains review/in-review. Current steps and limits: [manual checklist](../../../docs/story-12-manual-testing.md).
