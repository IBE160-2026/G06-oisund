---
status: superseded-draft
superseded_by: technical-addendum.md
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
---

> Preserved working draft, not an active specification companion. Use [technical-addendum.md](technical-addendum.md) and [product-decisions.md](product-decisions.md). Earlier AN-1/TQ allocation and idle-view-only retention alternative below are superseded by AN-E1/K-1–K-4 and the canonical Q-5 register. No final owner approval is recorded.

# Short technical supplement — automatic-notice pilot

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Planning proposals,not an architecture workflow or accepted implementation design. Reuse the existing React/TypeScript → FastAPI modular monolith → PostgreSQL and private-local runtime. No greenfield bootstrap,new service,route-network pipeline or public deployment. Product rules stay in SPEC and existing companions; this file assigns responsibilities and qualification gates.

## Read-only code evidence and compatibility

Inspected26 October2026 at extension planning commit36bfc196dba1c885b3fcda19b79a64ab86746ee6; product code remains aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed. Main HEAD still aa0fcfb with uncommitted11.5/11.6 changes; none adopted/copied. Before AN-1.2 inspect any newly accepted committed baseline and reconcile affected files; no automatic main-worktree import is assumed.

| Existing component | Observed responsibility | Proposed change boundary |
|---|---|---|
|backend/app/private_main.py| Private route registration,lifespan maintenance task; no source collector | New read-only source/day-candidate resources and collector lifecycle integration in same runtime,feature disabled by default. Source I/O outside private request locks. |
|backend/app/workday_storage.py| owned() enforces owner/live expiry with row lock;require_mutable() rejects ended/aborted writes | Reuse guards for day reads/decisions. Match read from confirmed content and source_revision; never rewrite plan. Consultation on closed days stays read-only. |
|backend/app/workday_notice_storage.py and workday_notice_domain.py| Manual saves/check/end with expected revisions/lifecycle,operation receipts,200-notice limit and fixed parent expiry | Do not import automatic records through manual save/check/end paths or consume manual capacity. Explicit manual additions continue through current editor. |
|backend/app/private_storage.py; backend/migrations/private/011_manual_notices.sql,012_real_notice_sources.sql| Private DB/cleanup; existing manually entered source fields | Add only story-needed source-generation/health and later private-decision records with versioned additive migration,not all future tables. No alteration of manual semantics or identity. |
|frontend/src/PrivateWorkdayView.tsx| Composes day/activity screens and notice controller,passed authorized request/mutation callbacks | Secondary Automatic candidates entry beside manual notices; keep activity/start/lifecycle behavior untouched. |
|frontend/src/PrivateNotices.tsx;useWorkdayResource.ts| Manual controller,retained proposals and uncertain commands; identity/access handling | Reuse UI tokens,authorized transport and pending/error patterns. Automatic viewer has its own source result shape; do not make manual validator accept synthetic automatic notices. |

## Adapter,refresh and bounded state

A narrow backend-only Entur TRO SX adapter returns source identities/text,typed selectors,original validity/status/optional fields and collection-health evidence. It sends an honest application header,requests a documented dataset scope and enforces documented rate/size/time bounds. Reject external entities/unsafe XML expansion,oversize/malformed responses and unbounded paging; expose partial/error rather than treating rejection as empty. Keep provider URL allowlisted; never server-fetch arbitrary notice links. No private plan/notes/SMS in provider requests or collector logs.

Provisional simplification: each scheduled refresh establishes a new full comparable baseline,not a long-lived cross-cycle delta session. Qualify page/session continuation within that cycle and finish every MoreData page before committing a complete generation. A failed budget/session/page keeps the previous complete generation with truthful health; valid partial observations may appear separately marked. Single-flight/DB lease prevents overlapping cycles and multiplied worker traffic; releasing/expiry and restart cause clean full resync. Qualification decides the small runner/lease details,not a new infrastructure project.

Reuse same private-API process lifecycle and database connection pattern,with start/stop cancellation,timeout/backoff and no blocking external I/O inside owner transactions. Collector disabled in demo and by default until explicitly enabled for the authorized private-local pilot. Unavailable network/DB cannot break manual notice use or fake completeness. Refresh target5min/age15min are provisional,not an SLA. A caller cannot trigger extra network polls for each user/day; manual refresh joins/schedules the shared bounded cycle.

Logical data responsibilities: current public-source generation and previous last-complete state during refresh; attempt/page/last-success health; canonical source identity/revision including observed-content change without fabricated publisher time. At most one candidate generation in flight and one complete publication; bounded unreferenced staging is discarded. Only source revisions referenced by private decisions need additional retention. No historical raw XML archive. Q-5 proposes seven-day idle public-view expiry; private references/receipts expire with their plan and never revive it. Exact columns/endpoints are implementation detail,not predetermined future schema.

## Workday matching and future route boundary

Compute candidates server-side from authorized confirmed plan snapshot,its source_revision,source generation and dated line-crosswalk version. Plan source_revision is not an editable-plan version engine: confirmed plans here are immutable; replacement/deletion/expiry invalidates old associations. Lifecycle/source-content revisions remain separate. AN-1.1 qualifies20/24 IDs and two independent plan fixtures. No numeric-ID concatenation; no service-date-only comparison; unsupported direction/stop restrictions remain conditional. A small typed resolver returns resolved/ambiguous/unavailable with provenance and date range. It can later be supplied by the separately planned route-network extension without making full routes prerequisite.

## Minimal user flow and source/manual separation

Open confirmed day → Automatic candidates → grouped possible line/time matches plus Requires review/broad/unknown-scope groups → inspect source text/link,clocks,qualifiers and health → optionally associate with activity,keep day context or dismiss for this plan. Show source closed/not seen/expired distinctly and provide return to manual notices. Keyboard,focus,narrow screens,Day/Night and text-based status follow existing UI; no driving alerts,new theme system or sensor interactions.

Persist user decisions only when added by their story,with operation identity,expected decision/source/plan/lifecycle context,receipt lookup and current-authority reread. Lost/malformed reply keeps original intent for lookup/retry; stale409 preserves proposal for comparison; denial hides private result; capacity/validation rejection is distinct from uncertain mutation. Terminal days may be read but not mutated. Source updates never mark manual checked or reopen manual ends.

For local text corrections/SMS use existing manual editor as a separately owned contribution. A later explicit reversible link can relate it to a source identity/revision; no automatic copying into manual records or fuzzy cross-source merge. Source changes surface Changed since review; old local correction/association remains inspectable and needs reassessment. Dedup repeated observations by source identity,not title; no second automatically scraped source in this epic.

## Small blocking qualification tasks

TQ-1 in AN-1.1: one permitted complete TRO baseline and actual page-continuation/cycle-budget proof; bounded incomplete/expired-cursor cases and read-only report. Existing three MoreData records are insufficient. If cursor/size bounds cannot produce qualified full scope,stop dependent collector story and return explicit alternative to owner.

TQ-2 in AN-1.1: reviewed dated20/24 bindings and two synthetic/approved-redacted day shapes with independent expected outcomes,including overnight/unknown direction and the stop-only426 pattern. No route-network import or private provider upload. Unknown per-departure/direction bindings stay review reasons.

TQ-3 at AN-1.2 start: qualify the existing runtime's single-flight/start/stop/lease and additive migration/cleanup boundary with a focused implementation check. Code already has lifespan maintenance,but no adapter; this is not evidence a collector exists. Stop if it requires deployment expansion or new service. Actual close/retraction examples may use current official semantics plus controlled cases without pretending observed TRO coverage.
