# Technical addition for the first automatic-notices epic

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Planning-only addition to the existing product, 2026-10-26. Proposed implementation boundaries, not a new architecture/UX workflow or permission to change services. Behavior remains owned by SPEC.md and its existing companions; this file locates the changes needed for AN-E1.

## Existing components inspected

Product baseline is `aa0fcfb`; planning branch HEAD before this task is `36bfc19`. Read-only main inspection found the same product HEAD with uncommitted 11.5/11.6 work, so none of that work is assumed accepted or copied.

| Existing code | Observed behavior / extension consequence |
|---|---|
| `backend/app/private_main.py`, notice routes 323–355 | Workday-bound manual read/create/edit/check/end and operation lookup. Add a separate automatic projection/review surface using the same private authorization/origin/CSRF protections. Do not reinterpret manual endpoints. |
| `backend/app/workday_notice_domain.py` | Strict manual DTO with exact tags/all-line scope, optional web/SMS metadata, nullable source time and manual registered/ended state. Cannot represent all typed SX qualifiers/windows/health. Keep the automatic DTO separate. |
| `backend/app/workday_notice_storage.py` | Owner and live-parent checks, lifecycle/notice revision checks, serialized commands/receipts, 200-notice manual limit and 50-item pages. Automatic sources must not consume manual capacity, overwrite source-check times or bypass revision/receipt rules. |
| `backend/migrations/private/011_manual_notices.sql`, `012_real_notice_sources.sql` | Accepted manual records and compatible receipts. Future additive extension migration must preserve all rows/receipts; no rewrite of historical migrations. No SQL is authored now. |
| `backend/app/private_storage.py`, `private_main.py` lifespan | Existing PostgreSQL connection/migration boundary and startup/hourly cleanup. Reuse it for bounded reference state and private overlay cleanup; no new service stack. |
| `frontend/src/PrivateNotices.tsx` | Exact response-key/ownership/expiry guards, separate maintenance/editor, retained proposals and original-operation recovery. Automatic content needs its own validator/view; adding fields to manual payloads would break strict guards. |
| `frontend/src/PrivateWorkdayView.tsx` | Day-linked manual notice controller and activity/lifecycle navigation. Add a secondary automatic-candidates destination; preserve selected activity, manual draft state and focus/recovery on return. No dependency on the uncommitted reader/recovery screens. |

Reuse the existing React/TypeScript → FastAPI → PostgreSQL flow. New small adapter/domain/storage modules may live beside the existing notice modules; exact file/table/endpoint names are implementation details. No event bus, separate microservice, generic source framework, full route catalogue or new administration product is needed.

## Source boundary and collection state

A server-side adapter uses the documented Entur TRO SX endpoint, meaningful client identification and a fixed allowed provider scope. It sends no private plan, SMS, notes, account or workday identifiers externally. Keep XML handling bounded in bytes/depth/records/time, reject unsafe entity/DTD expansion, treat source text as text and allow only safe HTTP(S) links. Malformed selectors, source identity collisions and parse failures cannot disappear behind a success response.

**First-epic proposal:** collect fresh full baselines, with pagination, on demand first and later on the five-minute target. Do not implement a long-lived delta subscription/session in this epic. A requestor token may be needed for paging; K-1 must qualify the real provider semantics. A terminal page alone is insufficient: every page must belong to the declared TRO cycle with no gap, stalled/repeated page, budget exhaustion or scope mismatch. If complete collection cannot be established, S1 is not accepted as a complete collector; a partial-only product requires a separate scope decision.

One server coordinator serializes the provider fetch and shares the rate budget across pages, manual refreshes and scheduled cycles. In a multi-process runtime, use the existing PostgreSQL coordination boundary for one active source writer; browser visits must not start competing collectors. Keep within the stricter documented four GETs/minute until qualified otherwise; respect actual throttling/backoff. Bound each cycle and surface partial state if limits prevent completion. Scheduling never converts missed targets into successful sync.

Preserve valid partial observations separately. Publish a new complete generation atomically only after its proof is satisfied; retain the earlier complete generation/clocks through faults. Without one, label coverage never-qualified/partial. Partial/newer explicitly ordered close records may update their own source contribution while others remain uncertain; without defensible ordering, expose conflict. First implementation may conservatively retain ambiguous updates rather than resolve them.

## Persistence, linkage and refresh

Separate three logical resources: public source contributions/revisions, collection health/generation, and owner-scoped workday review overlays. This is a responsibility split, not a DDL schema. Source identity includes provider/participant/situation ID; content/version evidence and clocks remain separate. Serial fetch time can label an observed change but cannot fabricate publisher time or prove that a versionless contradiction is authoritative.

An authorized read projects the current confirmed plan revision plus reviewed dated canonical bindings into candidates. No invented `TRO:Line` formula or trip-number join. Multiple source windows and nested line/stop/journey constraints remain structured; missing bindings/offsets stay uncertain. No full stop sequence is presumed.

Review actions store the source revision/generation, plan revision, activity where relevant, action and actor/time separately from source content. Reuse session-bound mutation wrappers, expected revisions and original operation/receipt reconciliation. A stale source/plan basis conflicts visibly; an accepted retry has one effect. Reading, fetching or associating does not mark a manual record checked or start/complete a shift. Terminal days permit consultation only; overlays and manual facts are not editable after closure.

Provisional Q-5 retention: current source view plus seven days of unreferenced superseded/not-seen evidence; source evidence referenced by a live private association remains explainable only until that parent's existing deadline. Keep any necessary selected copy under that same private lifetime, release references on parent deletion/expiry, and never extend private expiry. Retention duration/rights remain a pre-persistence check, not owner-approved policy. Do not persist raw XML archives or private payload logs. Public retrieval may continue independently, but expired/deleted/foreign workdays cannot expose private links or be recreated by polling.

Source close, expired validity, not-seen in a comparable complete baseline, observation-unknown after a fault, and user-ended remain independent. Polling never reopens a user-ended contribution; disappearance never resolves a real-world incident. A material source change produces a comparison/reassessment badge; prior local corrections/dismissals remain visible, not silently carried onto changed facts.

## Minimal user flow

Day → **Automatic notice candidates** → source/health summary and possible line/time candidates → **Needs review** group for mapped-stop, broad and unresolved TRO messages → inspect source/scope/time → associate, keep day context, dismiss reversibly or leave unresolved → return to day/manual maintenance.

Show source identity/link, nullable publisher-update time, response/last observation and last complete sync separately. Use “possible relevance”, explicit nested-qualifier reasons, collection-state/age labels and honest counts/paging. No entries means no candidates in the qualified scope, never clear roads. Opening Svipper is a manual control link; record a check only through an explicit check action. Existing manual web/SMS editor stays intact and independent.

Reuse parent Day/Night styling, keyboard focus/labelled controls, readable long text and navigation recovery. A reversible explicit link between an existing manual contribution and one source contribution suffices for overlap comparison; display conflicting facts side by side. No automatic merge/deduplication or multi-provider ingestion is included.

## Small technical qualifications

K-1 in S1: one permitted complete TRO baseline with page/cycle proof and bounded timeout/stall/empty/error controls. K-2 in S2: reviewed canonical line 20/24 bindings and two permitted representative workday fixtures. K-3 in S3: typed StopPlace/Quay mapping for the pilot; unknowns enter review without geospatial inference. K-4 in S4: ordered and versionless updates, close/missed-close/resync examples, with controlled cases labelled controlled when real transitions are unavailable. These tasks resolve dependent stories; none repeats the full research or makes all future enhancements prerequisites.
