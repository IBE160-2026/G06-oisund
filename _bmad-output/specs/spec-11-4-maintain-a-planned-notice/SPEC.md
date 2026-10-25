---
id: SPEC-11-4-maintain-a-planned-notice
status: done
approved_on: 2026-10-25
created: 2026-10-25
story: '11.4'
story_key: 11-4-maintain-a-planned-notice
alias: V1-13
implementationStarted: true
owner_acceptance: accepted
accepted_on: 2026-10-25
baseline_commit: cdcf2816b86772e559f33ded5807e8cb5a4473bc
companions:
  - implementation-plan.md
  - ../../implementation-artifacts/epic-11-context.md
  - ../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
  - ../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md
  - ../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
  - ../../planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md
sources:
  - ../../planning-artifacts/story-drafts/story-v1-13.md
---

# Story 11.4 — Maintain a planned notice

## Why

The delivered 11.3 flow lacked manual maintenance of source-linked notices. This change adds that maintenance while preserving separate screens, saved choices and unsaved proposals. Jonas approved the complete plan and authorized implementation, testing and browser verification on 2026-10-25.

## Capabilities

- **CAP-1** — **intent:** Register a manually maintained notice for a confirmed workday, including SMS-only sources. **success:** Explicit save and authorized reopen retain one stable notice ID, title, short/deep explanations, optional source description/link, explicitly selected specific/all-line scope, nullable source update/validity and initial `Registrert` status without changing the plan, bus, activity selection or activity statuses.
- **CAP-2** — **intent:** Maintain an existing notice and explicitly end it manually. **success:** Revisioned edits change exactly the intended notice; a separate deliberate action changes `Registrert` to `Avsluttet manuelt`. Time, source disappearance, navigation and edits never infer ending.
- **CAP-3** — **intent:** Distinguish recorded metadata from an explicit source check. **success:** Server registration/edit times remain separate from nullable source-update time, validity and checked-at; only the explicit check action records checked-at for the saved revision. A later edit visibly qualifies any earlier check.
- **CAP-4** — **intent:** Maintain notices through clear screens without losing other work. **success:** Day → notice management → new/edit → save/cancel → notice management → day preserves saved activity choice and other registered data, retains unsaved input across safe navigation, returns meaningful focus and keeps unresolved-command recovery reachable.
- **CAP-5** — **intent:** Recover from failed or conflicting notice writes without inventing success. **success:** Authorized lookup/same-command retry resolves one accepted effect; stale proposals remain available for comparison. Account changes, terminal closure, deletion and expiry cannot enable unauthorized writes or resurrect work.

## Constraints

- Apply Story 11.4/V1-13, FR-12/13/14/24, AC-04/09 and SCOPE-02. The management list identifies records belonging to this day; line/date relevance filtering and multi-line matching belong to 11.5.
- The owner's 2026-10-25 correction supersedes the earlier URL-only contract: require a nonblank title and explicit specific/all-line scope. Specific scope requires entered tags; all-line scope is a user choice, never inferred from missing tags. Short/deep text and source description are supported; URL is optional, including for SMS-only notices. Any entered URL must be HTTP(S). Render plain text and an optional normal link; do not fetch sources. Unknown source times and unknown/partial validity remain explicit. No road-clearance, complete-coverage or current-trip/stop claim.
- Jonas approved `Registrert` / `Avsluttet manuelt` and deliberate manual ending during this planning run. Do not introduce a seen/hidden/versioned or automatically ended lifecycle.
- Preserve one primary screen at a time, 11.3 `Aktivitetsstatus` / `Fullført manuelt`, confirmed Start/End from the activity, read-only recap and existing navigation/access/loss guards. Notice actions never Start, select, complete or close work.
- Reuse server ownership, parent-workday locking, revisions, typed responses and stable bounded operation receipts. Browser private proposals stay in memory only. Workday expiry and terminal authority apply to notices, checks, retries and receipts; reads/sign-in/edits never extend retention.
- Add schema through a new migration; preserve existing data and historical receipts. Closure shortening, immediate denial, parent deletion and startup/hourly purge cover the new records and operation metadata.
- Verify real synthetic API/PostgreSQL/restart behavior and rendered Day/Night keyboard/long-content/200% text at 768/1024/1440px against IR-01. Device observations and owner acceptance remain separate from emulation and historical 11.3 results.

## Non-goals

- No 11.5 filtered reader, automatic ingestion, source crawling, source-history engine, notice deletion/reopening workflow, trip/stop matching, GPS, sound or inferred resolution.
- No integrated 11.6 recovery redesign, parser/demo expansion, private offline cache, export, theme-persistence completion or actual iPad/Safari qualification. Fictional examples remain isolated; later assessment work retains its scope.
- No staging, commit, push or next story in this implementation run; stop in review for owner testing.

## Success signal

A later synthetic real-API/browser journey creates and reopens a source-linked notice, edits it without asserting source verification, explicitly checks it and manually ends it, then returns to the same day/activity. Lost replies, stale revisions, cross-window closure, deletion and expiry demonstrate one accepted effect, preserved proposals, no unauthorized mutation and no extended retention.

## Assumptions

- Preparation permits creation/edit/check/manual ending before Start and while active; ended/aborted workdays permit only reading within retention. This follows the current preparation and terminal contracts, rather than the active-only activity-status rule.
- A check applies to saved content. Later edits retain its timestamp with a visible earlier-revision qualification until another explicit check; an edit does not silently set or erase source-check time.

## Open Questions

No unresolved product blocker remains. The complete plan is approved; implement and verify the technical contracts, then stop for owner testing before publication.

## Owner-directed contract correction — 2026-10-25

The owner reported that saving real notices remained unusable and explicitly requires SMS without a website address, title/short/deep explanation fields and specific-line or “Alle linjer” selection. Rendered Svipper inspection confirmed expanded operational text, place notices, longer route headings and shared rather than individual links. The [corrective dispatch specification](../../implementation-artifacts/spec-11-4-real-notice-sources.md) records the active implementation, compatibility and verification requirements. The earlier feedback-only change and complete-gate results below are historical evidence, not verification of this correction. Retain separate screens, original-command recovery and manual check/ending. Filtering remains 11.5; no publication is authorized.

## Implementation and independent review checkpoint — 2026-10-25

CAP-1–5 are implemented. The [execution specification](../../implementation-artifacts/spec-11-4-maintain-a-planned-notice.md) records every independent review finding and reinspection; the [evidence](../../../docs/evidence/11-4-manual-notices.md) distinguishes actual results and intermediate failures. Every retained finding is fixed, with no deferral. Source instants now retain server-authoritative Oslo calendar fields, including historical offsets; raw older UTC receipt JSON remains unchanged. Explicit tag boundaries survive quoted comma entry, and comparison/denial/load/validation feedback is covered by new regressions.

The first complete gate passed 384 API tests, all 377 browser tests, populated restart/repeated migration preservation and build. After review corrections, the final complete gate passed **393 API tests and all 395 browser tests**, including all 53 notice API cases and 44 notice browser cases, plus populated restart/repeated migration/raw-state preservation, build and seven verifier controls. The tested local version is served with additive migration 011, unchanged original rows/secret/database identity and two empty notice tables. The only original-baseline maintenance difference is three expired login-throttle rows removed by unchanged startup cleanup; later comparisons preserve the resulting baseline. Root source hashes and served-asset equality are verified. Owner acceptance remains pending; stop in review with no staging, commit, push or next story.

## Real-source correction final checkpoint — 2026-10-25

The owner's SMS-without-URL, short/deep text and explicit all-lines requirements are implemented and independently reviewed. Final root checks passed 61 notice API/PostgreSQL tests and all 49 notice browser tests, production build, populated upgrade/repeated migration/database/API restart preservation and seven verifier controls. Every retained review/root finding is fixed; none deferred. Migration 012/local rollout and original data/secret/database preservation are verified; tested assets are served. This correction supersedes the old URL/nonempty-tag-only contract, while the original full gate below/above remains historical. Overall owner acceptance stays pending; no staging/commit/push or next story. See the corrective dispatch specification and latest evidence for precise results and owner walkthrough.

## Owner acceptance and publication authorization — 2026-10-25

Jonas explicitly approved the corrected story 11.4 delivery, then instructed commit and push. Owner acceptance is accepted and story/sprint status is done. The technical final gate remains 61 API/PostgreSQL and 49 browser passes with verified migration/restart/data preservation. Earlier pending-acceptance and stop-before-publication statements are historical and superseded by these owner messages. Record the accepted work in Git and push to origin/main; do not start 11.5 or any other story.
