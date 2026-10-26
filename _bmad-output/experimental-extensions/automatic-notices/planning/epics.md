---
stepsCompleted: [1, 2, 3, 4]
workflow: bmad-create-epics-and-stories
workflowMode: user-directed-short-brownfield-adaptation
status: planning-draft
validation: passed-as-draft
approval: not-granted
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
created: 2026-10-26
inputDocuments:
  - ../specs/spec-automatic-notices/SPEC.md
  - ../specs/spec-automatic-notices/source-lifecycle.md
  - ../specs/spec-automatic-notices/relevance-rules.md
  - ../specs/spec-automatic-notices/compatibility.md
  - ../specs/spec-automatic-notices/qualification.md
  - ../specs/spec-automatic-notices/product-decisions.md
  - ../specs/spec-automatic-notices/technical-addendum.md
  - ../research/technical-automatic-notices-2026-10-26/research.md
  - ../../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
  - ../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md
  - ../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
---

# Automatic notices — bounded pilot epic

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Overview

One short extension plan using the existing product architecture and specification. No new brief, PRD, UX or architecture workflow was run. Step completion records extraction/drafting/checks under the user's short-process instruction, not owner approval or implementation readiness. Requirements stay canonical in SPEC.md/companions; the stories below slice those requirements rather than create a second product contract.

Product baseline `aa0fcfb`, planning baseline `36bfc19`. Entur TRO SX, lines 20/24 and two representative confirmed workdays; Svipper is manual control. Actual dates, canonical mappings and full-collection proof are qualification inputs. No complete route-network dependency or live-driving permission.

## Requirements inventory

### Functional requirements

Use existing CAP IDs, qualified by SPEC-automatic-notices: CAP-1 complete/partial source view; CAP-2 exact line/planned-time possible relevance; CAP-3 stop/broad/unknown review; CAP-4 source/clocks/lifecycle evidence; CAP-5 manual preservation; CAP-6 honest health/age; CAP-7 separate overlapping contributions and reversible explicit links. Full normative behavior is in the named spec companions.

### Non-functional requirements

- AN-NFR-1: preserve owner/session/origin/CSRF checks, parent expiry and private/demo separation; no private data sent externally or persisted in browser storage.
- AN-NFR-2: bounded allowed-source XML ingestion, truthful complete/partial/unknown states, conservative documented request budget, no all-clear claim or fabricated timestamp.
- AN-NFR-3: retain stable operations/expected revisions, source-revision context and recoverable user proposals; no automatic manual overwrite, check or reopen.

### Technical additions

The code-grounded `technical-addendum.md` companion owns the component map and minimal flow. Separate normalized public source state from private review overlays and existing manual notices. Fresh full baselines first; no long-lived delta feature or new service architecture. Small K qualifications are embedded in the dependent stories.

### UX requirements

Reuse day-linked navigation, separate manual maintenance/editor, readable Day/Night, keyboard/focus and retained-input/recovery guards. Expose source, age, missing metadata and scope uncertainty; unresolved TRO items remain reachable with honest counts/paging. No driving alerts, fabricated stop/location precision or forced interaction while driving.

## Epic list

### AN-E1 — Understand possible notices for a planned workday

The driver can consult a qualified TRO source view, see explainable possible relevance for lines 20/24, review stop-only/broad/unknown items, and keep manual information and prior decisions intact through source changes or failures.

Covers SPEC-automatic-notices CAP-1–7 and AN-NFR-1–3. One cohesive extension epic; the same day/notice components are affected throughout. No external route-network epic, deferred V1 delivery, new administration system or other provider is required. This is a drafted scope under the current request, not final product approval.

### Capability coverage map

| Capability | Epic | Delivery emphasis |
|---|---|---|
| CAP-1 | AN-E1 | Complete paged baseline, bounded partial states, later periodic refresh. |
| CAP-2 | AN-E1 | Exact reviewed line/time scope and explicit private association. |
| CAP-3 | AN-E1 | Reachable stop/broad/unresolved review with reversible actions. |
| CAP-4 | AN-E1 | Source identity, missing clocks, change/close/not-seen evidence. |
| CAP-5 | AN-E1 | Manual web/SMS/corrections/check/end preservation and existing private lifetime. |
| CAP-6 | AN-E1 | Health, partial/failure, successful sync and age kept separate. |
| CAP-7 | AN-E1 | Explicit reversible manual/source link and side-by-side conflicting contributions only. |


## Epic AN-E1: Understand possible notices for a planned workday

**Outcome:** one small consultative pilot can retrieve qualified source information, explain possible workday relevance and preserve manual facts through changes and outages. No operational completeness/all-clear claim.

**Recommended order:** AN-E1-S1 → AN-E1-S2 → AN-E1-S3 → AN-E1-S4. Each story is an independently demonstrable vertical slice and depends only on previous slices. Storage/API/view work belongs inside the slice introducing its data; do not create all future entities upfront. All stories are planning drafts, not ready-for-dev or owner-accepted.

### Story AN-E1-S1: Read a qualified TRO source view

As a driver consulting the day,
I want to inspect source notices with an honest collection result,
So that I can use the retrieved information without mistaking a partial or failed fetch for complete coverage.

**Scope/value:** one allowed TRO SIRI-SX adapter, bounded paged baseline, separate normalized source state and a day-linked read-only source/health view. On-demand collection first; no workday matching or private review mutations yet. End-to-end value is readable source facts and health, not merely a database table.

**Depends on:** existing accepted private workday access/manual-notice product baseline; no later story or route-network delivery.
**Traceability:** CAP-1/4/6, manual non-interference part of CAP-5; G-1/G-2/G-4; AN-NFR-1/2/3.

**Small qualification K-1:** in the first implementation slice, use a bounded permitted provider session to establish real page continuation, declared scope, rate/cycle limits and terminal baseline proof. Retain request/response metadata and independently checked counts/IDs without private data. Research's three-record MoreData page is not a pass. A stalled/unqualifiable baseline stops completeness acceptance; do not broaden research or silently deliver a partial-only substitute.

**Acceptance criteria:**

- **S1-AC1 — Given** valid authorized workday access and K-1 evidence, **when** all pages of one TRO baseline validate, **then** the separate source view reports that declared scope/generation and complete result with observed counts, **and** no private plan/SMS/account identifiers were sent to Entur.
- **S1-AC2 — Given** MoreData, a failed middle page, repeated/stalled continuation, exhausted budget or a truncated/invalid response, **when** collection stops, **then** it reports partial/unavailable as appropriate and retains last qualified content/clocks, **and** a terminal final page cannot conceal the earlier gap or produce a false zero.
- **S1-AC3 — Given** an HTTP error, timeout, invalid XML/entity payload, valid HTTP with an unusable shell or inconsistent provider scope, **when** processing occurs, **then** no complete generation is promoted, **and** the view exposes the attempt/result without private payload logs or unsafe source HTML/links.
- **S1-AC4 — Given** simultaneous browser refreshes or multiple API workers, **when** collection is requested, **then** one source writer shares a bounded request budget across pages/attempts, **and** throttling/backoff follows documented limits without a per-browser polling fan-out.
- **S1-AC5 — Given** records with absent version/update/link, multiple validity windows and nested typed selectors, **when** displayed, **then** the original identity/text/scope and unknown values remain distinct from retrieval/response/observation times, **and** missing publisher time or a source-item URL is never fabricated.
- **S1-AC6 — Given** a complete verified empty baseline versus a partial empty attempt, **when** read, **then** only the former may say zero retrieved items in that checked scope, **and** neither says no disruptions/clear roads. Without any complete baseline, coverage remains unqualified.
- **S1-AC7 — Given** existing manual web/SMS notices and an expired/deleted/foreign workday, **when** source collection/read occurs, **then** manual rows/receipts/check/end values and existing capacity stay unchanged, **and** unauthorized private day access is denied and expiry is never extended.
- **S1-AC8 — Given** long or missing source text and keyboard/Day/Night navigation, **when** opening/returning from the source view, **then** facts/status remain readable and focus returns meaningfully, **and** existing manual editor input/selection is preserved.

**Completion evidence:** qualified real complete baseline plus labelled controlled failure examples, focused API/storage and rendered-view evidence for this slice, additive migration/data-preservation evidence if persistence is introduced, and no regression of the existing manual contract. Rights/retention check from Q-5/G-4 applies before accepting persistent storage. None has been executed by this plan.

### Story AN-E1-S2: See possible line/time relevance for the workday

As a driver preparing a confirmed day,
I want notices nominated from exact line bindings and planned intervals,
So that I can find potentially relevant information without invented trip precision.

**Scope/value:** a small reviewed dated crosswalk for lines 20/24, server-side relevance against the authorized confirmed-plan revision, and explained candidate rows in the automatic view. Reading does not save an association. No exact direction/stop/journey match or full timetable integration.

**Depends on:** AN-E1-S1.
**Traceability:** CAP-2/4/6; G-3; AN-NFR-1/2/3.

**Small qualification K-2:** select two representative permitted confirmed-day fixtures including an overnight/uncertain-time case; validate canonical line 20/24 identities and applicability dates against source evidence. Record expected classifications independently of matcher output. Printed values, codespace and operator context must be explicit; source suffixes are not an ID-generation rule. A missing binding remains a review reason, not a guessed match.

**Acceptance criteria:**

- **S2-AC1 — Given** a reviewed date-valid binding and compatible source line/validity, **when** the current authorized plan is projected, **then** its matching activity/line reasons appear as **possible relevance**, **and** no automatic nomination is labelled user/provider-confirmed applicability.
- **S2-AC2 — Given** 20, 020, X20, 20E, a different provider/operator or an expired/ambiguous binding, **when** compared, **then** only an explicitly reviewed applicable mapping can match, **and** no substring, number coercion or invented LineRef hides uncertainty.
- **S2-AC3 — Given** multiple source validity windows and separate planned activities/gaps, **when** evaluated, **then** half-open overlap uses the relevant activity's planned calendar instants; a point activity matches when validity_start <= activity_time < validity_end (where known), **and** touching endpoints alone, overnight dates and gaps have independently expected outcomes. Service date alone and actual shift start do not replace these intervals.
- **S2-AC4 — Given** missing/reversed/ambiguous date or DST information, open-ended source validity, direction text or unsupported nested stop/journey qualifiers, **when** nominated, **then** retain the uncertainty/conditional reason, **and** only a reliable explicit incompatibility may exclude it. No source field is fabricated to force a decision.
- **S2-AC5 — Given** a message matching both pilot lines or several activities, **when** listed, **then** one contribution lists all matching lines/activities with reasons, **and** separate source identities remain separate incidents.
- **S2-AC6 — Given** source collection is partial/stale/unavailable or no-line messages exist, **when** line/time candidates are read, **then** source health qualifies the result and the full source list remains reachable, **and** no-line items are not silently deleted by the line filter before S3's dedicated review flow.
- **S2-AC7 — Given** a changed/unauthorized/deleted/expired plan or a failed projection response, **when** reading candidates, **then** current owner/revision/expiry checks apply and unavailable differs from empty, **and** no selection, lifecycle, manual check/end, manual note or private deadline is mutated.

**Completion evidence:** dated binding manifest and two fixture references; independent exact-identity/time/unknown-field examples; actual API-to-view projection and focus/navigation evidence within the existing access/expiry contract. Do not require provider endorsement, all regional lines or complete routes.

### Story AN-E1-S3: Review uncertain notices while preserving manual information

As a driver reviewing the day's information,
I want reachable stop/broad/unresolved messages and explicit local review actions,
So that useful warnings are not lost and my manual knowledge remains distinguishable from source content.

**Scope/value:** grouped review inbox, inspect/associate/context/dismiss/leave-unresolved actions, local review decisions plus a simple explicit reversible link to an existing manual notice. Corrections, SMS additions and manual endings use the existing manual editor; source text remains read-only and no second correction editor is added. No automatic merge or third source integration.

**Depends on:** AN-E1-S1 and AN-E1-S2.
**Traceability:** CAP-2/3/5/7; G-3/G-4/G-5; AN-NFR-1/2/3.

**Small qualification K-3:** verify a minimal typed pilot-stop/endpoint binding set including the Giæverbukta example if still relevant to chosen fixture dates. StopPlace is not Quay. Unknown bindings remain in the unresolved group; do not acquire a full stop sequence/route geometry to make this story possible.

**Acceptance criteria:**

- **S3-AC1 — Given** mapped stop-only, compatible explicit broad scope and unknown-line/area TRO items, **when** review is opened, **then** each stays reachable in its explained group with honest observed totals/paging, **and** empty line lists do not become all-line scope. Partial-source counts are labelled observed/partial, not regional totals.
- **S3-AC2 — Given** a StopPlace/Quay distinction, nested stop restriction or a known regional non-pilot service, **when** classified, **then** qualified bindings/reliable incompatibility determine review/broad/outside scope, **and** names, proximity and free-text direction cannot invent precise trip relevance.
- **S3-AC3 — Given** an authorized mutable day and displayed source/plan revision, **when** the driver explicitly associates to a named activity or keeps day context, **then** a separate attributable private overlay records that choice and its evidence revision, **and** the action does not mark the source checked or start/select/complete an activity.
- **S3-AC4 — Given** a local dismissal or a correction/manual ending held in the existing manual editor, **when** the review decision is saved or reversed where permitted, **then** original source evidence remains inspectable and manual facts remain separately owned, **and** dismissal is plan-local, reversible and never source closure. Unfinished review remains unresolved; no second source-text editor or source-ending action is introduced.
- **S3-AC5 — Given** an existing manual web/SMS notice with text, optional link, correction, checked time or manual ending, **when** it is explicitly linked/unlinked or compared with a source contribution, **then** both contributions remain intact and conflicting facts/clocks are visible, **and** similar titles never trigger automatic merge, overwrite, check or reopen.
- **S3-AC6 — Given** a stale plan/source revision, competing tab or lost mutation response, **when** the same review operation is retried or status-checked, **then** expected-revision/operation identity prevents duplicate or stale acceptance, **and** the unsaved proposal is preserved for comparison without force overwrite.
- **S3-AC7 — Given** terminal/deleted/expired/foreign work or renewed login, **when** review is read/written, **then** authorization, read-only terminal behavior and original parent expiry apply, **and** private overlays/receipts cannot be revived or leaked by public polling. Use Q-5 bounded history and cleanup with this slice.
- **S3-AC8 — Given** navigation between review, day, source detail and manual maintenance, **when** the driver returns/cancels, **then** input/recovery/selection and focus remain intact, **and** Svipper opening is a manual control link whose check timestamp requires an explicit action.

- **S3-AC9 — Given** a malformed/lost reply, denial, validation error or receipt-capacity rejection for a private review action, **when** the view recovers, **then** unconfirmed operations retain the original identifier/body for authorized lookup/retry and no confirmed badge is invented, **and** denial hides private data while bounded known rejection remains cancellable. A valid older receipt never overwrites newer current authority.

**Completion evidence:** representative stop/broad/unknown cases, explicit-review/retry/conflict/no-overwrite demonstrations through the real private path, expiry/access evidence and a small driver walkthrough. Preserve separate contributions without a generalized grouping UI/framework.

### Story AN-E1-S4: Keep review trustworthy through changes and outages

As a driver returning to the day,
I want source changes, missed updates and my earlier choices explained,
So that I can reassess information without losing manual work or trusting stale certainty.

**Scope/value:** serialized periodic full-baseline refresh, changed-content/lifecycle comparison, retained private review context and explicit reassessment, plus the bounded two-day evaluation. Builds on earlier error/privacy protections; they are not postponed until this story. No long-lived delta feature or automatic Svipper extraction.

**Depends on:** AN-E1-S1, AN-E1-S2 and AN-E1-S3.
**Traceability:** CAP-1–7; G-1–G-5; AN-NFR-1/2/3.

**Small qualification K-4:** use actual transitions where available and clearly labelled controlled cases for older/closed/versionless/missed-close behavior. Qualify each inference separately; absent live retraction evidence never permits disappearance-as-resolution. Check restart with fresh-baseline proof rather than unqualified session continuation.

**Acceptance criteria:**

- **S4-AC1 — Given** the provisional five-minute/fifteen-minute policy, **when** repeated cycles, concurrent refreshes or throttling occur, **then** every page shares the same bounded budget and health/age uses successful complete synchronization rather than attempts, **and** incomplete/resync status appears immediately even before an age threshold is reached.
- **S4-AC2 — Given** identical records, ordered newer/older versions or versionless changed content, **when** refreshed, **then** identical observations remain one contribution, ordered regressions cannot replace newer source state and changed content retains provenance, **and** contradictory unorderable evidence is a conflict, not a fabricated publisher update or silent reopen.
- **S4-AC3 — Given** explicit validated close, expired validity, comparable complete-baseline absence or partial-cycle disappearance, **when** processed, **then** source-close, validity-expired, not-seen and observation-unknown remain different, **and** no one of them asserts road clearance or closes/reopens another/manual contribution.
- **S4-AC4 — Given** a failed middle page, outage, restart, expired cursor or missed-close window, **when** collection resumes, **then** a new complete baseline is required and previous qualified content/success clocks remain explainable, **and** omission after recovery cannot prove incident resolution.
- **S4-AC5 — Given** a material source/plan change after association, dismissal, correction or manual ending, **when** the driver reads the day, **then** show original reviewed evidence alongside the current difference and request reassessment where applicable, **and** retain old choices without silently promoting them to confirmation of the changed facts. Read-only terminal consultation stays read-only.
- **S4-AC6 — Given** parent deletion/expiry and bounded public history cleanup, **when** polling/cleanup/retry occurs, **then** all private links/notes/receipts obey the original parent lifetime and selected evidence remains available only within that lifetime, **and** no successful poll extends or resurrects private data. Verify existing manual rows/receipts and fictional isolation remain unchanged.
- **S4-AC7 — Given** the two permitted workdays and at least 30 independently labelled cases covering G-1–G-5, **when** the candidate/review flow is evaluated, **then** report raw false/missed/unknown counts, recall/precision denominators and manual review workload, **and** all truthfulness/privacy/manual-preservation invariants pass. Provisional 95%/90% targets inform owner go/no-go, not a provider SLA or automatic acceptance; zero denominator is not evaluable.
- **S4-AC8 — Given** selected source items have a Svipper counterpart, **when** manual paired checks are recorded, **then** retain URLs/facts/check times and differences without assuming synchronized publication, **and** missing counterparts remain documented. The driver distinguishes possible relevance, association, close/not-seen and stale/partial in the selected walkthrough cases.

**Completion evidence:** focused collection/review regression and recovery proof, source-revision/parent-expiry evidence, two-workday result ledger and one owner evaluation session. If completeness, exact identities or manual preservation fails, the dependent slice is not accepted; discuss a narrower first delivery rather than quietly changing it.

## Traceability and dependent qualification summary

| Specification capability | Primary stories | Supporting checks |
|---|---|---|
| CAP-1 | AN-E1-S1, AN-E1-S4 | K-1/K-4, S1-AC1–4, S4-AC1/4. |
| CAP-2 | AN-E1-S2, AN-E1-S3 | K-2, S2-AC1–7, S3-AC3/6. |
| CAP-3 | AN-E1-S3 | K-3, S3-AC1–4/8. |
| CAP-4 | AN-E1-S1, AN-E1-S4 | S1-AC5, S4-AC2/3/5. |
| CAP-5 | AN-E1-S1, AN-E1-S3, AN-E1-S4 | S1-AC7, S3-AC4–7, S4-AC5/6. |
| CAP-6 | AN-E1-S1, AN-E1-S2, AN-E1-S4 | S1-AC2/6, S2-AC6/7, S4-AC1/4. |
| CAP-7 | AN-E1-S3, AN-E1-S4 | S3-AC5, S4-AC3/5. |

Cross-cutting AN-NFR-1–3 and the inherited UX constraints apply to every slice introducing affected data/actions, not just S4. Controlled failure cases supplement live evidence; they never become claimed real provider outages/transitions.

## Before implementing the first story

Obtain separate implementation authorization and an agreed bounded qualification/effort checkpoint. Recheck the then-current accepted product baseline; no need to wait for uncommitted V1 reader/recovery work. Confirm provisional retention/access/attribution constraints before persistent integration. Start K-1 within S1; real paging/completeness is the concrete unresolved technical gate, not a reason to restart all research. K-2 fixture dates/mappings are needed for S2, not to build S1's bounded source view. No sprint-status entry or V1 dispatcher handoff is generated.
