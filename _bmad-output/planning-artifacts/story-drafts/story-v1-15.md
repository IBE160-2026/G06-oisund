---
status: done
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-15
epic: 11
story: '11.6'
dependencies: [V1-04, V1-12, V1-14]
implementationStarted: true
ownerAcceptance: accepted
ownerAcceptedOn: 2026-10-26
---

### Story 11.6: Recover from an unavailable server

**Stable alias:** V1-15. **Status:** done; Jonas explicitly accepted the integrated delivery on 2026-10-26. Fresh final gate: 421 backend tests and all 479 browser cases passed; source manifest recorded. See the [execution specification](../../implementation-artifacts/spec-11-6-recover-from-an-unavailable-server.md) and [delivery evidence](../../../docs/evidence/11-6-server-recovery.md). No commit/push, retrospective or next epic is included.
**Depends on:** V1-04, V1-12, V1-14.
**Traceability:** FR-17/18/20; NFR-2; AC-07; SCOPE-02.

**User outcome:** show unsaved/unavailable status, preserve current form input while the page remains open, reconcile a retry with server state and reopen the last saved revision when connected. No offline restart guarantee or silent lost-save claim.

**Acceptance criteria:**
- Exercise timeout before commit, lost response after commit, stale revision and backend unavailable on save. Resolve stable operation ID/status before retrying; no duplicates or force overwrite. Keep form input while open and warn before avoidable loss; online reopen recovers last server-saved revision, never an invented offline copy.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.


## Owner acceptance - 2026-10-26

Jonas explicitly approved the integrated 11.6 delivery and instructed completion of the Epic 11 retrospective, including the preliminary work from the other chat. The accepted source manifest remains unchanged. Selected manual environment was local desktop browser; detailed scenario results/browser version were not supplied and are not invented. No physical Lenovo/Android/Brave/mobile-network test is inferred. Remote access is scheduled between Epic 11 and Epic 12. No commit/push or Epic 12 implementation is authorized. Earlier pending statements remain historical.
