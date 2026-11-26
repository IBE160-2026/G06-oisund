---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories, step-04-final-validation]
status: draft
workflow_status: document-validation-complete
implementation_readiness: gated
approval: not-approved
version_target: V1.3.0
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
inputDocuments:
  - scope.md
  - specs/spec-position-progression/SPEC.md
  - specs/spec-position-progression/behavior.md
  - specs/spec-position-progression/route-interface.md
  - specs/spec-position-progression/fictional-example.md
  - specs/spec-position-progression/decisions.md
  - specs/spec-position-progression/technical-addendum.md
  - research/technical-position-progression-2026-10-26/research.md
  - ../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
referenceRouteCommit: 7cada9d2e66af9806358f582bc8ea459321a6563
---

# Position and stop progression / V1.3.0 - Epic Breakdown

## Overview

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

One bounded planning epic derived from the existing SPEC package and latest user-set decisions PP-D1–D4. The existing specification substitutes for a new PRD; current architecture and established UI patterns are reused. No new brief/full PRD/UX/architecture round. Stories are proposed delivery slices, not implementation authorization or test evidence.

Implementation is gated on completed/tested V1, the required route function and separate authorization. The route function is a dependency, not part of this epic. Story qualification tasks occur only after that gate. No GPS suitability has been demonstrated.

## Requirements Inventory

### Functional Requirements

- PP-FR1 (CAP-1/6): consume a user-confirmed compatible dated route, selected inclusive range and ordered distinct occurrences; qualify NSR Quay coordinates through ID/source/version/validity mapping. Missing data keeps the affected portion manual.
- PP-FR2 (CAP-1): select the relevant driven occurrence for initial or mid-trip start, never hardcode full-pattern index one.
- PP-FR3 (CAP-2): opt in to visible-page assistance and estimate ordinary progression without collapsing repeated stops or changing activity/outcome/lifecycle.
- PP-FR4 (CAP-4): protect a fresh manual correction, then allow coherent reliable subsequent evidence to revise its estimate without per-stop confirmation; age alone is insufficient.
- PP-FR5 (CAP-3): stop on interruption and require manual occurrence selection plus fresh acquisition on resume; manual choice may skip stops without fabricated observations. Automatic multi-stop reacquisition stays later.
- PP-FR6 (CAP-5): save bounded latest-stop context/time/origin and propose a correctly remapped occurrence for the next confirmed trip in the same workday, including midnight crossing. Missing/ambiguous match requires manual clarification.
- PP-FR7 (CAP-6): show route-data defects separately from denied/unavailable/stale/uncertain measurements; both can coexist.
- PP-FR8 (CAP-2/4/5): respect explicit Pause/Off, clear transient state and stale callbacks, preserve existing saved data and fixed lifecycle/deletion rules.

### NonFunctional Requirements

- PP-NFR1: reuse authenticated online authority, owner/session binding, strict schemas, revision conflicts and stable-operation recovery; no private data in public coordinate requests.
- PP-NFR2: one bounded server anchor per workday, bounded receipts and transient samples; no full GPS trail, analytics coordinates or private persistent browser cache. Parent expiry/deletion/closure shortening cannot be extended.
- PP-NFR3: preserve frozen route/import/manual facts, stable IDs, activity outcomes, bus assignment, user-driven lifecycle and private/demo isolation.
- PP-NFR4: qualify actual device/browser/origin, measurement quality and tuning separately; synthetic fixtures never demonstrate GPS suitability. Unsupported cases remain manual.
- PP-NFR5: generation/context guards reject late callbacks/responses; unavailable/uncertain saves never claim acknowledgement or silently overwrite newer work.

### Additional Requirements

- Reuse React/TypeScript, FastAPI and PostgreSQL; no starter template, new service or route catalogue. Proposed surfaces and contract additions: [technical addendum](specs/spec-position-progression/technical-addendum.md).
- Route prerequisite: compatible frozen dated association, ordered occurrences, selected range and preparation/carry-forward extension point. Add coordinate binding locally; do not implement route discovery/review again.
- Server authority and fixed workday expiry apply from the first persistent slice; necessary additive migrations belong to that slice and must preserve saved data.
- No actual implementation or qualification executes in this planning run.

### UX Design Requirements

No new UX contract was commissioned. Carry these concrete existing-pattern requirements into the extension:
- PP-UX1: labelled start/anchor/correction/Pause/Resume/Off controls and textual status/origin/evidence age; no permission prompt before explicit Start and no control use required while moving.
- PP-UX2: independent route-health and measurement-health messages; preserve the manual stop list, distinguish estimate from served/observed stops, and distinguish saved/unconfirmed anchor state.
- PP-UX3: use existing Day/Night, narrow/enlarged layout, keyboard/focus and safe access-suspension patterns; new state indications cannot rely on color alone.

### FR Coverage Map

| Requirement | Epic / proposed slice |
|---|---|
| PP-FR1, PP-FR2 | PP-E1 — route eligibility and relevant start anchor |
| PP-FR3, PP-FR4, PP-FR7 | PP-E1 — foreground following, advisory correction and uncertainty |
| PP-FR5 | PP-E1 — interruption and manual recovery |
| PP-FR6 | PP-E1 — saved same-workday anchor and next-trip remapping |
| PP-FR8 | PP-E1 — safe controls from sensing onward; lifecycle/cleanup throughout |

## Epic List

**PP-E1 — Follow the selected trip and retain useful stop context within a shift.**

The driver can start from the relevant stop, follow qualified foreground estimates, correct them, manually recover after a gap and reuse a bounded stop proposal for a later trip in the same workday, including across midnight. Coverage: PP-FR1–8, PP-NFR1–5 and PP-UX1–3.

One epic as requested; each slice delivers a driver-visible outcome. Dependency: completed/tested V1 and the necessary route handoff (see technical addendum), not a future position epic. Automatic multi-stop reacquisition, cross-workday reuse and background tracking are excluded. No V1 backlog item is created.

## Epic PP-E1: Follow the selected trip within one workday

Deliver the first-delivery branch of the [fictional scenario](specs/spec-position-progression/fictional-example.md), including the midnight handoff, while preserving all existing manual workday authority. Recommended order: **PP-E1-S1 → PP-E1-S2 → PP-E1-S3 → PP-E1-S4**. Each slice builds only on earlier slices and the external route prerequisite. No later position story is required for an earlier slice's stated value.

All acceptance criteria below describe future observable behavior, not checks executed in this task. The epic remains draft and gated; the four slices together form the proposed first delivery.

### Story PP-E1-S1: Inspect the usable stop sequence and choose the starting occurrence

As a driver,
I want to see the dated trip's usable stop occurrences and select the first stop I will drive,
So that assistance starts from an explainable reference rather than a guessed route origin.

**Scope and value:** one selected confirmed trip/range, read-only route/coordinate health and a transient manual start marker. Add the narrow NSR coordinate binding/consumer required by the position interface. The manual list remains useful without sensing.

**Dependencies:** completed/tested V1; delivered route function with frozen dated association and a compatible preparation/carry-forward hook; separate implementation authorization. No dependency on S2–S4. No route discovery, matching workflow, regional catalogue, background refresh or saved-anchor resource.

**Requirements:** PP-FR1/2/7; PP-NFR1/3/4; PP-UX1/2/3.

**Acceptance Criteria:**

- **PP-S1-AC1 — Given** a confirmed compatible dated journey and selected range, **when** the panel opens, **then** it shows operating date and explicit call dates/times, source/mapping version, range and ordered unique occurrence keys; **and** repeated Quay visits remain separate (A-o2 and A-o5).
- **PP-S1-AC2 — Given** range A-o2..A-o8, **when** the user chooses A-o2 or a relevant later occurrence, **then** that occurrence becomes the transient manual start assertion with time/origin; **and** A-o1 or an occurrence from another trip/version is rejected without changing prior state.
- **PP-S1-AC3 — Given** a scheduled StopPlace/Quay and explicit mapping, **when** the NSR binding is prepared, **then** the consumer retains separate parent/platform IDs, WGS84 kind/coordinates, object/snapshot/mapping versions, source metadata and validity at the dated call; **and** name equality or a parent centroid cannot substitute for the scheduled Quay.
- **PP-S1-AC4 — Given** missing/invalid coordinates, ambiguous mapping, unresolved date/range or a known incompatible association, **when** eligibility is evaluated, **then** the affected portion is labelled manual-only with its route-data reason; **and** an unverified source choice stays labelled unverified, precise fixes cannot repair it, and no false “no stops” result hides unavailable data.
- **PP-S1-AC5 — Given** a source update or failed public request, **when** the panel is opened/refreshed, **then** the frozen reviewed facts and user start choice are preserved or explicitly marked incompatible; **and** no active-plan rewrite or unqualified new coordinate version is silently adopted. Only allowlisted bounded public stop/validity facts leave the private boundary.
- **PP-S1-AC6 — Given** a suspended/denied/expired private context or a terminal workday, **when** the panel would activate, **then** private presentation follows existing access gates and no new assistance is enabled; **and** manual outcomes, activity selection, plan, bus assignment and lifecycle remain unchanged.
- **PP-S1-AC7 — Given** the manual-only panel, **when** using keyboard, enlarged/narrow layout and Day/Night, **then** occurrence selection, date/version warnings and focus are usable and status is textual; **and** no geolocation permission prompt occurs.

**Small qualification tasks:** qualify one bounded prerequisite route handoff and NSR response/mapping on the selected pilot scope, with independent expected dated occurrences and missing/wrong-Quay/version cases. Record exact source validity/attribution/limits and any unsupported fields; block only the affected automatic-support claim. Use synthetic date/loop cases where needed and label them. Check new panel states on the actual target layout later; no location capture is needed for this story.

### Story PP-E1-S2: Follow ordinary progress and correct an advisory estimate

As a driver,
I want voluntary foreground stop estimates that respect my correction and later reliable evidence,
So that I can follow the trip without confirming every stop or trusting an isolated GPS error.

**Scope and value:** one visible selected trip, opt-in watch, bounded candidate evaluator and transient estimate/correction UI. Safe stopping is included now. No persisted anchor or automatic recovery across gaps.

**Dependencies:** S1's qualified route binding and manual start selection; actual-device secure-origin/access prerequisites. S1 remains usable if device qualification fails. No dependency on S3/S4; before S3, a stopped session can be started anew by explicit Start and manual selection.

**Requirements:** PP-FR2/3/4/7/8; PP-NFR1/2/3/4/5; PP-UX1/2/3.

**Acceptance Criteria:**

- **PP-S2-AC1 — Given** an authorized visible page, eligible route and selected start occurrence, **when** the user explicitly starts, **then** permission is requested and only a watch bound to that context may contribute evidence; **and** denied/unavailable/timeout/unsupported or insecure-context results leave the manual list usable with a distinct measurement reason and no repeated prompt loop.
- **PP-S2-AC2 — Given** qualified temporally distinct approach/departure evidence for the supported next occurrence, **when** the evaluator advances, **then** only the estimate changes (A-o2→A-o3); **and** repeated Quays retain occurrence order, range end does not select another trip, and no served/observed outcome or lifecycle transition is created.
- **PP-S2-AC3 — Given** a new manual correction at A-o6, **when** an immediate contradictory F fix arrives, **then** the selected estimate is protected and old accumulated evidence is discarded; **and** later post-assertion coherent reliable evidence may support ordinary A-o6→A-o7 without another manual confirmation. The manual assertion/time remains distinct from the revised estimate.
- **PP-S2-AC4 — Given** an aged manual anchor, **when** only protection time has elapsed or fixes are stale, duplicate, future/out-of-order, implausible, poor or ambiguous, **then** no override follows from age alone; **and** show uncertainty and retain correction controls. A far/backward contradiction requests re-anchoring rather than arbitrary multi-stop relocation.
- **PP-S2-AC5 — Given** good route data and stale fixes, or missing route data and good fixes, **when** statuses render, **then** each dimension reports its own condition, origin and evidence age; **and** both can be shown together without a fabricated current stop.
- **PP-S2-AC6 — Given** a running or pending watch, **when** Pause, Off, hidden page, material gap, trip change, access loss, unmount or terminal closure occurs, **then** sensing stops, the generation is invalidated and raw samples are cleared; **and** late permission grants/callbacks cannot restart it. Pause/Off is never reversed merely by becoming visible; Start/Resume requires explicit action and a manual occurrence.
- **PP-S2-AC7 — Given** any estimated or manually corrected stop, **when** state changes, **then** no raw positions enter persistence/logs/analytics/public requests, the sample buffer stays within the declared bound, and existing saved user data/outcomes are unchanged; **and** readable labelled controls and focus remain usable without color-only certainty.

**Small qualification tasks:** identify Lenovo model/SKU and Android build; separately record Brave/Chrome versions, trusted HTTPS and permission/OS-location behavior. Use a small controlled fixture set for repeat/nearby Quays, stationary drift, jumps and correlated error; then, only under later authorization, compare representative device measurements against independently known positions. Qualify or reject the illustrative age/radius/coherence/protection/hysteresis values; record supported layouts and failure reasons, not a blanket GPS guarantee. No full raw-track archive or standalone research epic.

### Story PP-E1-S3: Resume safely after an interruption

As a driver,
I want to restore assistance at the relevant stop after a gap,
So that missed stops do not force catch-up clicks or become invented observations.

**Scope and value:** a clear stale/interrupted state and explicit manual recovery within the current selected range. Builds on S2's immediate safe stop; adds the contextual Resume path across hidden/locked/reloaded sessions. Automatic multi-stop reacquisition remains outside scope.

**Dependencies:** S1 and S2. S4 is not required; after reload this story can recover through existing authorized route loading and manual occurrence selection.

**Requirements:** PP-FR5/7/8; PP-NFR1/2/3/4/5; PP-UX1/2/3.

**Acceptance Criteria:**

- **PP-S3-AC1 — Given** an estimate A-o3 before the page hides/locks or measurements materially stop, **when** the user returns, **then** an authorized view identifies the old estimate and its evidence time as stale; **and** it requests a manual occurrence rather than continuing automatically from new fixes.
- **PP-S3-AC2 — Given** a gap during which the fictional vehicle passed A-o4/A-o5, **when** the user chooses A-o6 and explicitly resumes, **then** a new manual assertion and new watch generation start at A-o6; **and** no one-at-a-time catch-up or observed-passage events are generated for A-o4/A-o5. Fresh reliable fixes are still required for GPS-derived following.
- **PP-S3-AC3 — Given** a canceled choice, out-of-range occurrence or changed/incompatible trip/reference, **when** Resume is attempted, **then** no watch starts for the stale selection and no old sequence is transferred; **and** cancellation preserves manual work and offers current-route clarification.
- **PP-S3-AC4 — Given** explicit Pause/Off, **when** visibility/access returns or fresh callbacks arrive, **then** the user's stopped intent remains in force; **and** only explicit Resume/Start with a relevant occurrence can proceed. Failed access or location permission checks cannot silently reactivate support.
- **PP-S3-AC5 — Given** reload, discard, session change, expiry or terminal closure, **when** recovery is attempted, **then** authorization and route context are revalidated before private display/use; **and** prior raw samples/watch handles never survive as fresh evidence. Denied/terminal contexts cannot resume, while saved plan/manual outcomes remain untouched.
- **PP-S3-AC6 — Given** successful manual recovery, **when** ordinary fresh evidence subsequently supports the next occurrence, **then** S2's advisory-anchor protection/reassessment applies without manual approval at every stop; **and** the interruption is not treated as permission for automatic multi-stop recovery.

**Small qualification tasks:** on each supported target browser, exercise a bounded matrix of tab switch, screen lock, power-saving gap, denied revalidation and reload. Record watch invalidation, stale presentation, canceled recovery and manual 3→6 behavior using synthetic movement first. Qualify the material-gap rule and clock-change handling. Distinguish actual lifecycle observations from injected gaps; this story does not claim background tracking.

### Story PP-E1-S4: Reuse the last stop on another trip in the same workday

As a driver,
I want my last saved stop offered at the correct occurrence on the next trip in this shift,
So that I can restart with less manual lookup even when the shift crosses midnight.

**Scope and value:** one bounded online anchor, next-trip remapping/acceptance and complete persistence cleanup. Add only the resource/migration/receipts this slice needs. No cross-workday copy, raw trajectory, persistent browser queue or route reconstruction.

**Dependencies:** S1–S3, existing owner-scoped online storage and workday deletion/expiry lifecycle. No future story dependency.

**Requirements:** PP-FR6/8 plus PP-FR1/4/7 at handoff; PP-NFR1/2/3/4/5; PP-UX1/2/3.

**Acceptance Criteria:**

- **PP-S4-AC1 — Given** an enabled, authorized, nonterminal context and an explicit manual anchor or supported stop change, **when** its save is acknowledged, **then** exactly one latest workday-owned stop record contains StopPlace/Quay, trip/date/pattern/occurrence and source/coordinate revisions, original evidence/assertion time, manual/GPS origin, savedAt and fixed expiry; **and** no raw coordinates or stop history are stored as anchors.
- **PP-S4-AC2 — Given** the acknowledged A-o8/Q:G anchor at 2026-11-02T23:48:00+01:00 in W1, **when** the user selects confirmed B in W1 at 2026-11-03T00:08:00+01:00, **then** Q:G uniquely proposes B-o3 in range3..5 with its old GPS time/origin and age20min; **and** explicit acceptance creates a new manual assertion, never a fresh GPS fix, index8 or the old journey's operating date.
- **PP-S4-AC3 — Given** no matching occurrence, multiple occurrences, different Quay under the same StopPlace or invalid/new mapping, **when** a proposal is requested, **then** explain the mismatch/alternatives and require manual clarification; **and** never match by name, old sequence or nearest time. Cancel leaves sensing off and preserves prior saved data.
- **PP-S4-AC4 — Given** the same workday across midnight or a different workday on the same calendar date, **when** reuse is evaluated, **then** the first passes the workday-identity gate while the second cannot inherit the anchor; **and** terminal, denied, deleted or expired contexts cannot activate assistance. Midnight alone neither deletes nor refreshes a record.
- **PP-S4-AC5 — Given** an uncertain/lost/malformed acknowledgement, **when** the user checks or retries, **then** reuse the exact operation/payload and show unconfirmed status until authoritative resolution; **and** reload offers only acknowledged server state. Offline/unavailable service cannot claim durable recovery.
- **PP-S4-AC6 — Given** concurrent tabs, a delayed older save or a reused operation ID with changed payload, **when** persistence is attempted/resolved, **then** stale revisions/conflicting payloads are rejected and a newer anchor is not overwritten or silently rebased; **and** an old accepted receipt is checked against current authority before presentation. Bounded/coalesced writes and receipt capacity failures preserve an explainable manual path.
- **PP-S4-AC7 — Given** Pause/Off or a trip change while an anchor save is in flight, **when** a reply arrives, **then** no sensing resumes and no further automatic save is issued from the old context; **and** a possible prior commit is reconciled without claiming cancellation or deleting the existing anchor. Raw buffers/estimates are cleared as specified.
- **PP-S4-AC8 — Given** parent closure shortening, deletion or expiry, **when** an anchor/receipt is read, written, retried or cleaned up, **then** existing authority/deadline rules deny invalid access and purge anchor-related data on the established schedule; **and** login, midnight, reuse and retries cannot extend or resurrect it. Unrelated drafts/plans/notices/bus/outcomes and private/demo isolation remain intact.
- **PP-S4-AC9 — Given** accepted/unconfirmed/stale anchor states, **when** the handoff UI is used in Day/Night and narrow/enlarged keyboard layouts, **then** origin/time, selected occurrence and acceptance/cancel controls remain readable with predictable focus; **and** an old proposal is never styled or labelled as measured current position.

**Small qualification tasks:** use synthetic owner/workday identities for overnight/different-workday mapping, retention shortening, two-tab race, lost reply and deletion/retry cases. Choose and record bounded save cadence, receipt admission/expiry and payload limits; verify zero sensitive payload logging and zero raw-location persistence. Qualify only the handoff UI/device behavior newly added here; do not repeat S2's full measurement work. Persistence checks later use isolated synthetic data and preserve existing real records.

## Coverage and completion boundary

| Contract / requirement | Story evidence to prepare later |
|---|---|
| CAP-1; PP-FR1/2 | S1-AC1–5; S2-AC1; S3-AC2 |
| CAP-2; PP-FR3 | S2-AC2/7; S3-AC6 |
| CAP-3; PP-FR5; PP-D1 | S3-AC1–6 |
| CAP-4; PP-FR4; PP-D3 | S2-AC3/4/6; S3-AC4/6 |
| CAP-5; PP-FR6; PP-D2/4 | S4-AC1–8 |
| CAP-6; PP-FR7 | S1-AC3–5; S2-AC1/5; S4-AC3 |
| PP-FR8 | S2-AC6/7; S3-AC4/5; S4-AC7/8 |
| PP-NFR1/3 | S1-AC5/6; S2-AC2/6/7; S3-AC5; S4-AC5/6/8 |
| PP-NFR2/5 | S2-AC6/7; S3-AC5; S4-AC1/5–8 |
| PP-NFR4 | Each story's small qualification tasks; all findings remain unexecuted |
| PP-UX1/2/3 | S1-AC7; S2-AC1/5/7; S3-AC1/3/4; S4-AC3/9 |

The inherited CAP IDs are local to this specification; PP-E1 and PP-E1-S1–S4 are extension IDs and do not renumber V1 stories. All four stories remain proposed. Document coherence is not implementation readiness, GPS suitability or user acceptance. No new material product choice is unresolved; qualification failures may require a later concrete scope decision.
