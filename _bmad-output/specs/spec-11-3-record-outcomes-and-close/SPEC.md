---
id: SPEC-11-3-record-outcomes-and-close
status: done
approved_on: 2026-10-25
created: 2026-10-25
story: '11.3'
story_key: 11-3-record-outcomes-and-close
alias: V1-12
implementationStarted: true
owner_acceptance: accepted
owner_accepted_on: 2026-10-25
baseline_commit: b42f1e8fa66ad5026f1751f31ddad50c3acbc7d6
companions:
  - implementation-plan.md
  - ../../implementation-artifacts/epic-11-context.md
  - ../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
  - ../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md
  - ../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
  - ../../planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md
sources: []
---

# Story 11.3 — Record outcomes and close

## Why

The driver can select and consult activities and explicitly start a shift, but cannot yet record what happened or close it. Extend the accepted 11.2 flow with explicit outcomes and terminal closure, preserving unknown information and a small retained recap. Jonas approved this plan and implementation on 2026-10-25, with active-only outcome registration.

## Capabilities

- **CAP-1** — **intent:** Record a manual outcome for an exact activity. **success:** An acknowledged action changes only that stable activity ID to completed, skipped, interrupted or explicitly unregistered; every actual non-passenger and pause member is supported.
- **CAP-2** — **intent:** Correct outcomes before closure. **success:** Corrections persist after authorized reload; selection, navigation, scheduled time and Start never alter outcomes, and failed/stale proposals remain distinguishable from saved state.
- **CAP-3** — **intent:** End or abort a started shift through explicit confirmation. **success:** Cancel leaves saved state unchanged; confirmation atomically saves one terminal state, first server ending time and non-extending expiry, without completing unknown activities or permitting resumption.
- **CAP-4** — **intent:** Consult a read-only recap within retention. **success:** After closure/reload, the recap shows the saved plan, explicit manual/unknown outcomes, terminal status, separate planned/actual times and expiry; no editing or restart is offered.
- **CAP-5** — **intent:** Resolve uncertain or conflicting saves without losing intent. **success:** Authorized lookup/same-command retry resolves the accepted effect once; stale proposals cannot overwrite newer outcomes, old receipts cannot reopen terminal work, and expired/deleted data cannot reappear.

## Constraints

- Follow SCOPE-02 and active Epic 11.3 (FR-11/21/22/24, AC-08). Reuse 11.1 Start and its original server timestamp; activity choice, Start, outcomes and closure remain distinct actions.
- Outcome registration and closure require an explicitly started active shift. Before Start, the day, activity selection and details remain available. Selection never starts the shift or records outcomes. This is the owner's explicit 2026-10-25 decision.
- Preserve 11.2 separate primary screens and clear keyboard/touch navigation, focus, retained unsaved input and reachable recovery. Selection detail hosts a separately labelled outcome area; closure confirmation and recap have their own day-linked screens.
- Unknown is `Ikke registrert`, never assumed completed. Normal end and abort are separate terminal reasons. No clock, inferred movement, depot arrival or selected member determines an outcome.
- The server owns state, UUID membership, ownership, session checks, revisions and atomic acceptance. Terminal guards cover bus, saved selection, Start and outcomes. Read-only consultation remains available within expiry.
- Closure expiry is the earlier of the existing deadline, planned final end + seven days and first server ending + seven days. Retrying, reading and signing in never extend it. Deny immediately at expiry; purge associated state/receipts at startup/hourly. Preserve historical confirmed facts and accepted receipts separately from current authority.
- Keep browser proposals in memory only; no private persistent cache/outbox. Validate responses, bind requests to displayed identity and preserve the existing no-store/access/deletion protections.
- Verify rendered Day/Night, keyboard, long content and 200% text at 768/1024/1440px against IR-01. Distinguish actual-device evidence from emulation and owner acceptance.

## Non-goals

- No notices implementation (11.4/11.5), integrated recovery redesign (11.6), automatic completion/progression, GPS/stops, offline private persistence, export, scoring, post-end editing, resumption or replacement Start.
- No demo expansion, theme-persistence completion or claim of actual iPad/Safari qualification; later stories retain those obligations.

## Success signal

A synthetic real-API/browser flow starts explicitly, records and corrects exact-member outcomes, cancels closure without mutation, then ends or aborts once and reloads the same read-only recap with unregistered members unchanged. Race, lost-response, identity and expiry cases prove no later mutation, duplicate end or deadline extension.

Implementation stops in review for owner testing, before commit, push or the next story. No unresolved product questions remain.

## Delivery — 2026-10-25

Implemented and independently reviewed. See the [execution specification](../../implementation-artifacts/spec-11-3-record-outcomes-and-close.md) and [executed evidence](../../../docs/evidence/11-3-outcomes-and-close.md) for exact results, intermediate failures and remaining device obligations. Owner acceptance is pending; implementation remains in-review before commit/push/next story.

## Owner feedback delivered in review — 2026-10-25

The owner requests Aktivitetsstatus terminology (retain Fullført manuelt) and confirmed Start/End directly from the activity. Recap and the remaining tested behavior were reported good; full story acceptance remains pending. The [feedback specification](../../implementation-artifacts/spec-11-3-owner-feedback.md) records execution and verification. The existing generated A–E import correction is delivered and verified without changing PDFs/fasit. B’s real unknown time and D’s note warnings remain explicit.

The owner explicitly authorized extending bounded import to the existing generated Testskift A–D, including E and all nine originals in regression. This follow-up preserves source files/fasit, real source uncertainty, endpoint/provenance rules and all privacy constraints; no runtime oracle or intermediate-stop feature is introduced. See the feedback specification for this authorized scope amendment.

Final review/gate/runtime evidence: [owner-feedback delivery report](../../../docs/evidence/11-3-owner-feedback.md). Root final verification: **119 affected PDF/import tests passed in 13.01s**, **all 351 browser tests passed in one complete invocation (27.3m)**, six isolated verifier/restoration controls passed (0.288s), and the production TypeScript/Vite build passed. The 119-test result is reused with exact backend application/test/migration hashes unchanged; only the reviewed identity-test entry point changed before the final browser run. All nine original independent fixtures and all 65 A–E source activities / 34 movements are covered; actual A–E upload/adoption/save/reopen verifies source rows, endpoints, calendar dates, expected uncertainty and duty/CAR anchors. New actual keyboard journeys cover activity Start cancel/confirm, status Save, End/Abort cancel/confirm, exact member identity, request counts, terminal consultation and cross-window recovery.

Owner acceptance remains pending. B intentionally retains its unclassified 16:20 Travel to (start/end/type unknown); D retains two unstructured source-note warnings while all 16 activities/endpoints are imported. A/C/E have bounded-layout qualification with no unresolved source lines. The nine original interpretations retain their source uncertainties, including Example 6. Physical iPad/Safari, touch hardware, assistive technology and browser chrome zoom remain untested; viewport/keyboard/200% root-text evidence does not replace those later 12.3/12.4 obligations. No staging, commit, push or next story. Story 11.3 finishes in review for the owner.

## Owner acceptance and publication authorization — 2026-10-25

Jonas explicitly accepted story 11.3, including the activity-status/shift-action and generated-PDF owner-feedback corrections, on 2026-10-25 and instructed commit and push. Owner acceptance is accepted; implementation is done. The earlier pending/review/stop-before-publication statements are historical checkpoints superseded by this instruction. Stories 11.4 onward remain backlog and no next story is started. Publication is authorized; actual commit/push results are checked through Git after execution.
