---
id: SPEC-automatic-notices
status: draft
approval: not-granted
updated: 2026-10-26
created: 2026-10-26
planning_stage: epic-draft
companions:
  - source-lifecycle.md
  - relevance-rules.md
  - compatibility.md
  - qualification.md
  - product-decisions.md
  - technical-addendum.md
  - ../../research/technical-automatic-notices-2026-10-26/research.md
sources:
  - ../../scope.md
---

# Automatisk avviksinnhenting — first pilot draft

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

This draft and its companions define the specification for review, not approved implementation requirements. The user supplied the first-epic planning boundary; remaining product choices use explicitly provisional defaults in product-decisions.md. The research companion supplies evidence; its blanket recommendations do not override this draft's explicitly scoped qualification gates.

## Why

An opportunity to reduce repeated source checking for drivers: qualify a small automatic passenger-notice view against planned workdays while preserving manual information and explicit uncertainty alongside approved V1.

## Capabilities

- **CAP-1**
  - **intent:** Maintain a qualified source view through complete collection, updates and recovery.
  - **success:** G-1/G-2 demonstrate every page and continuity; partial/failure/recovery never becomes false complete or zero.

- **CAP-2**
  - **intent:** Identify possible notice relevance to the confirmed workday using exact line identities and planned validity.
  - **success:** Independent cases preserve identity/time qualifiers and uncertainty; explicit user association differs from automatic nomination.

- **CAP-3**
  - **intent:** Review stop-only, broad and unresolved-scope notices without losing them through line filtering.
  - **success:** G-5 cases show reachable items/reasons/counts and reversible associate/context/dismiss/unresolved actions.

- **CAP-4**
  - **intent:** Distinguish source content, clocks, updates and lifecycle evidence.
  - **success:** Cases keep not-seen, unknown observation, expired validity and explicit source close distinct without fabricated fields or all-clear.

- **CAP-5**
  - **intent:** Preserve manual notices, SMS, corrections and manual lifecycle actions alongside automatic sources.
  - **success:** G-4 preserves original content/check/end/ownership/expiry through updates and plan changes; no automatic overwrite or reopen.

- **CAP-6**
  - **intent:** Judge whether the available source view is complete, partial, unavailable or old.
  - **success:** Failure cases retain qualified last-success/attempt/baseline ages; zero candidates is stated only within qualified successful scope.

- **CAP-7**
  - **intent:** Inspect overlapping/conflicting source contributions without losing provenance.
  - **success:** Cases retain contributions/disagreements and reversible links; similar titles or newer fetches do not establish truth.

## Constraints

- First draft outside approved V1. Companion behavior is proposed contract for review, not implementation authorization.
- Entur TRO SIRI-SX is proposed primary; Svipper is a manually checked local reference. No automatic operational-applicability or all-clear claim.
- Use authorized confirmed-plan facts and reviewed dated bindings; retain unknown fields, failed continuity and source conflicts.
- Source contributions, user notes, manual check/end and plan associations remain separate; preserve privacy, authority, expiry and isolation.
- Qualification is scoped to the chosen pilot; provider contact and full regional coverage are not blanket gates.

## Non-goals

- Product implementation/tests/services, full architecture/UX workflows, V1 changes or Git publication in this planning run; extension epic/story planning is authorized.
- GPS, automatic stop progression, complete route datasets, vehicle tracking, offline guarantees, dispatch authority and real-driving deployment.
- Automatic Svipper extraction, ET/VM/GTFS-alert expansion or Vegvesen integration in the first slice.

## Success signal

A bounded demonstration nominates explainable possible relevance, keeps stop-only/broad messages reviewable and preserves manual facts through source faults and lifecycle changes. Every invariant case passes; trial size, percentages, workload and refresh targets in Q-1–Q-7 remain proposals requiring owner agreement before pilot acceptance.

## Assumptions

- Current planning basis is 20/24, two representative workdays and manual Svipper checks. Other defaults remain provisional; implementation/pilot acceptance is not authorized.
- A small reviewed mapping set plus explicit review can evaluate line/time relevance without complete routes; usefulness remains unproven.

## Open Questions

- Q-1–Q-7 in product-decisions.md: pilot scope, no-line inbox, refresh/age, interval/association semantics, retention, acceptance targets and effort/go-no-go. See product-decisions.md for supplied planning basis, provisional defaults and later checkpoints; no inferred final approval.
