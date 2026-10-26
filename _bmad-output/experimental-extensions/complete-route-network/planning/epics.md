---
stepsCompleted: [1, 2, 3, 4]
validation: pass-as-planning-draft
workflow: bmad-create-epics-and-stories
workflowMode: user-directed-short-brownfield-draft
status: planning-draft
approval: not-approved
implementation: deferred-until-V1-complete-and-tested
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
inputDocuments:
  - ../specs/spec-complete-route-network/SPEC.md
  - ../specs/spec-complete-route-network/coverage.md
  - ../specs/spec-complete-route-network/matching.md
  - ../specs/spec-complete-route-network/data-contract.md
  - ../specs/spec-complete-route-network/qualification.md
  - ../specs/spec-complete-route-network/decisions.md
  - ../specs/spec-complete-route-network/pilot-manifest.md
  - ../specs/spec-complete-route-network/technical-addendum.md
  - ../research/technical-complete-route-network-2026-10-26/research.md
  - ../../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
  - ../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md
  - ../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
---

# Complete route network — P1 epic breakdown

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Overview

One short brownfield draft for line20 over seven literal service dates, draft association and planned reference carry-forward. Existing SPEC/companions own behavior; stories are delivery slices, not duplicated product requirements. P2/full regional import, GPS/progression and notices are excluded. Implementation is deferred until V1 is complete and has been tested for a while, then requires owner go-ahead; no calendar duration or completed V1 is implied.

## Requirements Inventory

### Functional Requirements

SPEC-complete-route-network CAP-1 scoped overview/coverage; CAP-2 dated candidate outcomes; CAP-3 explicit review/correction; CAP-4 actual ordered pattern/range/destination display; CAP-5 service-date/time/calendar semantics; CAP-6 preserved evidence through refresh; CAP-7 conceptual namespaced identity handoff. Normative details stay in named companions. P2 complete-catalogue success and QF-08 external integration are explicitly deferred.

### NonFunctional Requirements

- CRN-NFR-1: owner/session/origin/CSRF, fixed expiry and private/demo separation; no private PDF/identifiers to Entur, payload logs or private browser archive.
- CRN-NFR-2: bounded API requests/quota/backoff and result validation; closure required before unique/checked-absence, no invented dates/IDs/metadata/position.
- CRN-NFR-3: stable activity identity and immutable import metadata, separate source/manual choices, revisions/original operation recovery, no silent overwrite or expiry extension.

### Additional Requirements

Reuse modular React/FastAPI/PostgreSQL and exact draft/confirmation contracts. Add only slice-needed typed route resources; no greenfield starter, all-future tables or source framework. See technical-addendum.md. No unresolved V1 work or other extension becomes a prerequisite beyond the explicit completed/tested V1 execution gate.

### UX Design Requirements

- CRN-UX-1: draft-linked lookup/detail and return preserve manual edits/pending commands; explicit field comparison/keep/correct/cancel.
- CRN-UX-2: textual states/source age/date and evidence distinguish unique, alternatives, checked absence, insufficient data, unavailable/stale and explicit user confirmation. No first-result confirmation.
- CRN-UX-3: planned ordered stops/headsign differ from end-place and actual position; reuse Day/Night, keyboard, meaningful focus return and wrapping long names. Apply inherited IR-01 rendered text4.5:1, necessary non-text3:1 and2CSS-pixel-equivalent focus/3:1 criteria, enlarged/narrow layouts and no color-only meaning to introduced views.

### FR Coverage Map

| Capability | CRN-E1 coverage | Explicit later boundary |
|---|---|---|
| CAP-1 | S1 named line/date scope and partial/unknown evidence; S4 retained validity | P2 exhaustive catalogue is not delivered |
| CAP-2 | S2 four candidate outcomes; S3 explicit dated association | No unqualified privateCode join |
| CAP-3 | S3 field decisions/manual fallback; S4 reassessment | No confirmed/active/terminal re-enrichment |
| CAP-4 | S1 planned calls; S2 range ambiguity; S3 review | Unsupported loop/variant cases safely unresolved |
| CAP-5 | S1 raw service/calendar time; S2 qualified semantics | Unqualified DST/calendar cases unresolved |
| CAP-6 | S1 health/provenance; S3 frozen choice; S4 comparisons | No regional acquisition or realtime guarantee |
| CAP-7 | S3 selected namespaced reference; S4 privacy check | QF-08 external notice API/join deferred |

## Epic List

### CRN-E1 — Review an imported trip against a dated public departure

The driver can inspect line20 planned facts in the seven-date manifest, distinguish possible departures and evidence gaps, explicitly confirm/correct direction, destination and ordered stops in a draft, then retain that reviewed reference without losing manual values through source changes. Covers the P1 portions of CAP-1–7, CRN-NFR-1–3 and CRN-UX-1–3. Complete network coverage is a later, separately measurable goal, not this epic's label.

## Epic CRN-E1: Review an imported trip against a dated public departure

**Status:** planning draft, neither implemented nor accepted. **Order:** CRN-E1-S1 → CRN-E1-S2 → CRN-E1-S3 → CRN-E1-S4. Each slice includes only its needed source/API/storage/view behavior; no all-future schema or layer-only stories. Implementation of every story waits for completed V1, an owner-assessed period of testing, reinspection of the accepted code baseline and separate authorization. Existing V1 completion/testing is a deliberate execution gate; full route network, automatic notices and regional import are not story dependencies.

### Story CRN-E1-S1: Inspect planned services on a named operating date

As a driver reviewing an imported draft,
I want a bounded source view of planned departures and calls for a pilot date,
So that I can inspect public facts with clear limits before trusting a suggested match.

**Value/scope:** draft-linked read-only lookup/detail for configured line20 and the seven-date manifest, with planned ordered calls, source identity and health. No candidate matching, private association save, regional importer or geometry yet. Public lookup never changes the draft.

**Depends on:** accepted existing import/draft/private-access baseline after the V1 execution gate; no later story.
**Traceability:** CAP-1/4/5/6; QF-07/09; CRN-NFR-1–3; CRN-UX-1–3.
**Bounded qualification:** QF-09 verifies the actual planned-service query, result truncation/pagination/date membership and declared operator scope. Retained research queries are leads; empty datedServiceJourneys is counter-evidence to treating it as exhaustive. QF-07 checks meaningful client identification, allowed access/attribution and bounded public storage before persistence. Record request bounds/response metadata and independently checked IDs; no broad new research. If closure is unavailable, source inspection remains explicitly partial, not a qualified matching collector.

**Acceptance Criteria:**

- **R1-AC1 — Given** an authorized live draft and one literal manifest date, **When** the configured public lookup succeeds, **Then** display namespaced line/journey and date-qualified planned calls, original source clocks/day offsets, timezone evidence and source/observation times, **And** the draft/manual values, activity selection and lifecycle remain unchanged.
- **R1-AC2 — Given** bounded results with unresolved pages, missing calendar/order/identity references or an unchecked operator subset, **When** shown, **Then** expose the checked scope and partial/unknown reason, **And** neither one record nor an empty preferred-trip/dated-journey response establishes an exhaustive list, absence or network completeness.
- **R1-AC3 — Given** failed HTTP, timeout,429, GraphQL errors with HTTP200 or malformed/partial data, **When** processed, **Then** show unavailable/partial as appropriate and retain earlier qualified facts with their original clocks, **And** bounded retries/backoff share request admission rather than create a browser/field polling loop or false empty success.
- **R1-AC4 — Given** outbound/inbound, changed destination, short-origin or repeated-stop data, **When** inspected, **Then** preserve the actual journey's ordered occurrence positions, StopPlace versus Quay and per-occurrence destination display, **And** endpoint names, headsign and source direction remain distinct; no reversing/deduplication or geometry/location claim.
- **R1-AC5 — Given** after-midnight calls, a date outside source coverage or unresolved DST/calendar evidence, **When** displayed, **Then** retain service date versus derived calendar instants and explicitly unresolved conversions, **And** calls belonging to the final manifest date can extend beyond its midnight without silently changing operating date.
- **R1-AC6 — Given** external requests, foreign/expired/deleted drafts or the fictional demo, **When** lookup/read occurs, **Then** enforce existing access/expiry/demo isolation and send only minimum public parameters, **And** no PDF, internal shift number, account/workday/activity identifier or private notes enter provider requests/logs/public caches; expiry is not extended.
- **R1-AC7 — Given** keyboard/Day-Night navigation, long source text or a cancelled detail view, **When** returning to draft review, **Then** labels/status remain readable and focus returns meaningfully, **And** unsaved input and unresolved existing save commands remain intact. Unknown evidence stays textually visible, not color-only.

**Completion evidence:** source scope/query/limits record; real permitted selected-source responses plus independently labelled invalid/truncated/error controls; source-to-view evidence and existing private/manual non-interference. These are future checks. Every seven-date cell retains its own status; live historical availability is not promised. If source rights/size/idle-retention limits cannot be qualified, persistent acceptance stops, not manual draft use.

### Story CRN-E1-S2: Compare a draft trip with dated departure candidates

As a driver preparing a passenger trip,
I want explained candidate outcomes based on the current draft facts,
So that I can distinguish one possible departure, alternatives, no checked match and insufficient evidence.

**Value/scope:** compare one stable passenger activity against S1's scoped dated facts; display candidate journey/range and proposed direction/headsign/stops. No persistence or automatic confirmation yet. Breaks/private deadheads/duties are not forced into public trips; no fuzzy ranking or internal-number join.

**Depends on:** CRN-E1-S1.
**Traceability:** CAP-2/4/5; QF-02/04/05/09, QF-03 optional only for a future number rule; CRN-NFR-1–3; CRN-UX-1–3.
**Bounded qualification:** QF-02 obtains permitted minimized actual-date imported-trip/public pairs with expected outcomes independently checked from matcher output. Include ordinary both directions, ambiguity/absence and the observed night pattern; clearly separate constructed controls. QF-04 checks source-shift service-time/calendar semantics for supported examples. QF-05 checks the supported occurrence/headsign/range cases. Unqualified DST/loop cases stay unresolved and do not require an all-format parser. Shifted2030 fixtures cannot prove current public matching.

**Acceptance Criteria:**

- **R2-AC1 — Given** a saved draft/activity revision, reviewed namespaced line/date mapping, reliable known planned times/occurrences and closed candidate scope, **When** exactly one journey plus range satisfies the qualified evidence, **Then** show one possible proposal with reasons and proposed facts, **And** it remains unconfirmed until S3's explicit user action.
- **R2-AC2 — Given** two compatible journeys/variants or multiple repeated-stop subranges, **When** compared, **Then** show alternatives with distinguishing date/time/occurrence/headsign facts, **And** the first/nearest result is not preconfirmed and the driver can leave the result unresolved.
- **R2-AC3 — Given** no compatible candidate, **When** scope/calendar enumeration is adequate versus truncated/missing/unknown, **Then** return not-found-within-that-scope versus insufficient-data respectively, **And** one result from incomplete coverage remains insufficient rather than unique. Source failure/staleness is explicit alongside the outcome, never checked absence.
- **R2-AC4 — Given** equal internal turnummer/privateCode/ID suffix or a nearest clock time but insufficient independent date/occurrence evidence, **When** searched, **Then** retain these as separate unqualified facts, **And** none alone establishes uniqueness/confirmation. Preserve leading zeros, namespace and operator distinctions rather than numeric coercion.
- **R2-AC5 — Given** a partial journey with repeated platforms and changing headsigns, **When** proposing a range, **Then** use positions within the selected actual full pattern and source headsign at relevant occurrences, **And** do not collapse visits, substitute a line-wide stop union or equate the local segment end to the onward destination.
- **R2-AC6 — Given**25:30/dayOffset1, no-service/calendar exception or ambiguous DST/shift-source date semantics, **When** matching, **Then** derive instants only with qualified service-day/timezone evidence and check eligible service dates, **And** unresolved/missing offsets never become guessed calendar dates or a compatible match. Aim times, not live estimates, drive comparison.
- **R2-AC7 — Given** an unsaved/match-driving edit, changed source scope/revision or removed/reordered activity, **When** a response returns, **Then** bind it to the original stable activity and draft evidence revision or discard/invalidate it visibly, **And** it cannot overwrite manual input, attach to a list index or keep a fresh unique badge on stale facts.
- **R2-AC8 — Given** no match, unsupported activity or missing number crosswalk, **When** the driver continues, **Then** retain manual editing and normal V1 confirmation subject only to existing validations, **And** lookup does not start/complete work, manufacture physical position or block all preparation pending P2/provider contact.

**Completion evidence:** independent dated-pair manifest, scoped expected classifications and actual UI/API comparisons; real versus constructed evidence and unsupported cases explicit. Positive automatic matching acceptance is blocked only for cases lacking QF-02 or necessary QF-04/05/09 evidence; source inspection/manual reference remains useful. No QF-03 join rule is introduced.

### Story CRN-E1-S3: Confirm or correct a route reference without losing manual facts

As a driver reviewing a trip in draft,
I want to explicitly save my departure/range and field decisions,
So that destination and ordered stops help preparation while my corrections remain attributable.

**Value/scope:** a small separate typed route-review resource/view for the existing draft/activity, field-level keep/use/correct/unknown decisions, saved reference and atomic carry-forward at overall confirmation. Reuse the existing manual editor and operation patterns; no active-plan revision system, generic provenance editor or second import workflow.

**Depends on:** CRN-E1-S1 and CRN-E1-S2.
**Traceability:** CAP-2/3/4/6/7; QF-05/07; CRN-NFR-1–3; CRN-UX-1–3.
**Bounded qualification:** verify strict existing draft/confirmation DTO integration, shared lock/revision ordering and receipt recovery against the then-accepted V1 baseline. QF-07 settles actual public bounded retention and selected private evidence cleanup before durable acceptance. QF-05 qualifies explicit range choice; unsupported ranges remain manual/unverified. No database/API schema is prescribed in advance beyond these observable boundaries.

**Acceptance Criteria:**

- **R3-AC1 — Given** a unique proposal or chosen alternative, **When** the driver inspects and explicitly saves it, **Then** record dated journey, source evidence, occurrence range, reviewed draft/source revision, user/time and selection mode separately, **And** a successful lookup or opening a row alone never confirms it or asserts independently proven trip-number equivalence.
- **R3-AC2 — Given** imported/manual direction, endpoint, destination or stops and an external difference, **When** reviewing field decisions, **Then** show original/external/manual values distinctly and require explicit keep/replace/correct decisions, **And** raw import metadata and existing manual values survive; headsign is not silently written into the endpoint field or provenance text.
- **R3-AC3 — Given** insufficient coverage or a known calendar/time/occurrence contradiction, **When** the user selects a reference manually, **Then** store an explicitly unverified or incompatible reference as appropriate, **And** no user-confirmed label hides that contradiction or promotes it to verified automatic matching. Normal manual preparation remains possible.
- **R3-AC4 — Given** reject/cancel/undo-before-save or navigation back to the draft, **When** leaving review, **Then** saved facts and pending proposals remain consistent with existing loss/recovery guards and focus returns, **And** no implicit association, activity selection, shift start or outcome is recorded.
- **R3-AC5 — Given** a stale draft/source/overlay revision, competing tab or removed activity, **When** saving, **Then** serialize against current owner/parent revision and return comparison/conflict rather than stale acceptance, **And** preserve the driver's proposal and manual edits without forced overwrite. A match-driving edit invalidates the affected prior review.
- **R3-AC6 — Given** a lost/malformed save reply versus validation/capacity rejection, denial or expired data, **When** recovering, **Then** original operation identity/body supports authorized lookup/retry with one accepted effect and explicit rejection states, **And** no false saved badge or new-operation duplicate occurs; old receipts cannot overwrite newer authority and denial hides private data.
- **R3-AC7 — Given** overall plan confirmation racing a route-review save/edit, **When** one is accepted, **Then** the transaction binds exactly the saved draft and association-set revisions and freezes selected evidence together, **And** stale/late mutations fail visibly. Existing required/unknown acknowledgements still apply; an unmatched trip alone adds no blocker.
- **R3-AC8 — Given** a confirmed/active/terminal plan or deleted/expired parent, **When** consulting or attempting enrichment, **Then** the frozen planned reference is read-only where access remains valid and mutation is rejected, **And** selected source copies/overlays/receipts follow the original parent expiry/deletion with no poll/retry/login extension or resurrection.
- **R3-AC9 — Given** a conceptual identity reference used in the saved review, **When** inspected, **Then** preserve namespaced line, typed stop/platform, journey+operating date and optional occurrence/source revision, **And** no private shift/driver/account fields enter the public vocabulary; no notice consumer or exact disruption join is created.

**Completion evidence:** source-to-draft-to-confirmed-day demonstration, manual preservation/strict DTO compatibility, concurrent confirmation/retry/expiry evidence and readable/focus-preserving review. Only needed additive resources are introduced in this story; the original draft/import/manual contracts remain valid.

### Story CRN-E1-S4: Reassess changed source evidence and qualify the P1 outcome

As a driver reopening preparation or a reviewed day,
I want changed/unavailable source facts distinguished from my saved choices,
So that I can reassess uncertainty without losing corrections or trusting a stale replacement.

**Value/scope:** explicit preparation-time refresh/comparison, honest staleness/failure and preserved frozen reference, plus the existing twelve-case P1 ledger. No background regional job, live cancellation stream, automatic remapping, P2 parser or notice ingestion. Earlier privacy/error/correction safeguards apply from their first slice, not only here.

**Depends on:** CRN-E1-S1, CRN-E1-S2 and CRN-E1-S3.
**Traceability:** CAP-1–7 within P1; QF-06/09 and QC-01–12; CRN-NFR-1–3; CRN-UX-1–3.
**Bounded qualification:** QF-06 compares two public versions where available; clearly labelled controlled cases cover rare removals/calendar/platform/headsign changes without pretending live observation. Recheck API schema/access only as needed after the V1 waiting gate. No repeat of the full research or mandatory supplier contact for cases with sufficient evidence.

**Acceptance Criteria:**

- **R4-AC1 — Given** newer source content, removed/replaced journey ID, changed calendar/platform/pattern/headsign or unchanged bytes, **When** preparation refresh occurs, **Then** show a semantic comparison/no-change result with version/hash/provenance, **And** changed/removed evidence never silently replaces an association, reopens manual choices or fabricates provider update time.
- **R4-AC2 — Given** source outage/429/partial response or24h without successful scope check, **When** reading the result, **Then** show attempt versus last successful check, original provider age/validity and stale/unavailable qualifications, **And** retained evidence is not presented as freshly published or no-service/all-clear. Known validity gaps override age sooner.
- **R4-AC3 — Given** a reviewed draft whose source/input facts changed, **When** comparing, **Then** keep old manual corrections and reviewed evidence inspectable and request new explicit action for changed facts, **And** confirmed/active/terminal work keeps its frozen read-only reference rather than receiving new enrichment.
- **R4-AC4 — Given** current+prior public results rotate or parent/private operation data expires, **When** cleanup/read/retry occurs, **Then** bounded public retention and selected private-copy lifetime remain separate, **And** expired private work cannot be reconstructed from public caches; no private browser archive, raw original retention or lifetime extension is introduced.
- **R4-AC5 — Given** the seven-date manifest and independently expected QC-01–12 cases, **When** evaluating, **Then** record expected/actual outcome, checked scope and real/constructed/not-run status for every case, **And** zero unsupported automatic associations, lost manual corrections or privacy breaches is required. Unsupported advanced cases may pass safe-unresolved handling only, not positive matching qualification.
- **R4-AC6 — Given** historical retained evidence versus a later live pilot window, **When** preparing acceptance inputs after V1, **Then** retain the original manifest revision and explicitly record any new seven literal dates, coverage and independently dated pairs, **And** no shifted2030 fixture, missing day or min/max range is reported as complete real-source coverage. Historical replay cannot weaken production expiry rules.
- **R4-AC7 — Given** candidate/detail/comparison and manual fallback flows, **When** the small preparation walkthrough is performed, **Then** the driver can distinguish possible/alternative/no checked match/insufficient, source stale/unavailable, user confirmation and planned versus actual position, **And** results/limits are presented for later owner go/no-go without declaring P2 coverage, implementation acceptance or driving readiness.

**Completion evidence:** twelve-case result ledger with raw expected/actual evidence and explicit unsupported/not-run cells, comparison/recovery/expiry demonstrations and one bounded owner preparation review. No promised accuracy percentage or benefit result; no provider/source qualification has been run during this document task.

## Qualification and acceptance handoff

| Task | First dependent slice | Later scope excluded |
|---|---|---|
| QF-07/09 minimum disclosure/access,query closure/errors | S1 | No full-feed collection |
| QF-02 independent dated pairs; QF-04 time semantics | S2 | Unsupported advanced cases stay unresolved |
| QF-05 actual occurrence/range/headsign cases | S1 inspection; S2 nomination; S3 selected range | No geometry or full NSR ingestion |
| QF-07 persistent review/expiry and confirmation contract | S3 | No active-plan re-enrichment |
| QF-06 two-version comparison; QC-01–12 | S4 | No silent replacement or success invented from samples |
| QF-03 number crosswalk | Only if a future join rule is proposed | Not required for evidence-based/manual P1 |
| QF-01 complete manifest/P2; QF-08 notice mapping | Deferred | No regional completeness or notice dependency |

**Before any implementation:** completed V1 plus a period of testing judged sufficient by the owner, explicit go-ahead/effort checkpoint, then reinspection of accepted code and actual output paths. No fixed waiting duration or current completion asserted. Routine CE completion does not trigger help/architecture/sprint/build. No V1 sprint/story IDs or dispatcher file are created. Remaining dates/retention/threshold choices are provisional in decisions.md, not hidden approvals.
