<!-- scope-02-historical -->
> **Historical baseline — superseded for active V1 on 2026-10-19.** Jonas approved [SCOPE-02](../../../sprint-change-proposal-2026-10-19.md). The [current backlog](../../../epics.md), PRD and UX/architecture spines govern. Earlier approvals, mandatory language, unresolved questions and test plans below describe the previous scope; they neither reactivate deferred features nor establish current test results. The proposal maps every old story to rewritten or deferred responsibilities. TIME-01's offline mechanisms are deferred; applicable IR-01 UI criteria remain.
<!-- /scope-02-historical -->

# Product Brief reconciliation

Verdict: **Pass with two small clarifications.** No unhandled architectural dimension or contradiction with the effective brief scope was found. Later PRD/UX and adopted architecture decisions correctly supersede the brief's original speed-limit ambition, Selfservice-PDF wording and older raw-file retention assumptions.

Reviewed inputs: `briefs/brief-IBE160-2026-09-21/product-brief.md` and `addendum.md`, against the draft Architecture Spine. Selected later PRD/UX wording was checked to avoid reviving superseded requirements.

## Actionable clarifications

1. **Make retrieval failure behavior explicit across the source/UI boundary.** AD-7 (spine lines 68–72) distinguishes fetch failures and AD-8 prevents false closure, but neither directly requires the existing notices to remain displayed as retained, potentially stale data after a fetch failure. The brief's “Trust and failure behavior” and addendum's “Operational information and trust” explicitly require this. One sentence in AD-7 can bind retaining the last successful notice set with a freshness warning and treating a never-successful fetch as unknown coverage, never a reassuring empty set. This is a clarification of adopted behavior, not a new decision.

2. **Carry the original-source link through the notice contract.** AD-7 mentions source references and the `NoticeVersion / SourceStatus` row mentions evidence, but does not expressly retain an original source URL for the UX source action. The brief requires access to the original source, and EXPERIENCE.md line 306 carries that requirement forward. State that source-provided original links/identifiers and nullable source metadata survive normalization; unavailable links remain explicitly unavailable. Detailed DTO fields can remain deferred.

## Coverage confirmed

- Full-stack web client/backend/PostgreSQL, generic reviewed shift import, actual-progress tracking, manual authority and explicit uncertainty.
- Distinct workday/shift/trip/vehicle duty/physical bus, pilot configuration independent of the domain and future operator integrations outside V1.
- Qualified automatic planned-notice ingestion, actual pilot-data checks, fictional demo isolation and no claim that simulation proves real operation.
- Offline operation, retained work, privacy/deletion and bounded host/access assumptions.
- Explicit feasibility gates and delivery-capacity uncertainty. The three-workday evaluation and recalled-baseline time-saving target remain product acceptance criteria in the authoritative brief/PRD; they need not be duplicated in the architecture spine. Pre-pilot technical qualification is correctly not represented as completed product evaluation.

No spine edits were made by this reconciliation.
