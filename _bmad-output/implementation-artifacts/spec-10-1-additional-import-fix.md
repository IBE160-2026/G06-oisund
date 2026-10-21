---
title: '10.1 — Preserve work-only shifts and CAR imports'
type: bugfix
created: 2026-10-21
status: done
route: oneshot
epic: 10
story: '10.1'
story_key: 10-1-review-a-text-pdf
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The additional approved examples fail owner walkthrough: example 9 drops Fadder/Instruktør work, while example 8 loses its CAR designation and incorrectly carries the previous bus duty into the return. Owner cannot accept 10.1 with these gaps.

**Approach:** Preserve Fadder and Instruktør as timed activities with their source labels. Recognize CAR designations and CAR transfer rows; display CAR/pilot-car use without an invented numeric realtime value or physical bus. The owner explicitly accepts a simple CAR representation; no new mentor feature or vehicle model is needed. Preserve the existing numeric duty change, all source rows, zero-duration transfer, pause grouping, uncertainty and collapsed source facts. Verify both examples through real import/save/reopen, update the already-authorized local app and preserve its account/data. Story acceptance remains pending.

</frozen-after-approval>

## Implementation Notes

- Owner accepted the 10.1 walkthrough on 2026-10-21 and authorized commit/push with devlog. Accepted known limitation: false t-marker warning on example 8 activity 13, caused by column cropping of tom / 76567; left unchanged at the owner's direction. This supersedes earlier pending-acceptance/no-publication notes below. Sprint 10.1 is done; 10.2 remains backlog and is not started.

- Planning: no unresolved intent choice; no migration, data deletion or external publication. Local service replacement is reversible and already authorized. Existing staged 10.1 work and added fixture documentation belong to this ongoing walkthrough and are retained without commit/push. Baseline HEAD: 5eaaac25a79fff18020f9716bea4c2692a6d5a45.
- Footprint: bounded parser labels/CAR matching in `backend/app/pdf_import.py`, nullable source duty suffix in `backend/app/draft_domain.py`, matching frontend metadata validation/presentation in `frontend/src/PrivateImport.tsx`; existing duty-change model and editor already support nonnumeric duties. Add focused parser/mapping/API/browser regressions and update qualification evidence. Keep source CAR - N designation verbatim while presenting CAR meaning; never derive a numeric suffix for it.
- Verification: independent 23/8-row expectations, numeric and CAR duty anchors/suffixes, typed metadata, real API storage/replay and browser review/adopt/save/reopen. Run existing guarded disposable verification and production build; local rollout must retain operational database container/volume/secret and before/after read-only state digests.
- Implemented explicit Fadder/Instruktør labels, preserved CAR designations with nullable source suffix, CAR transfer and pilot-car deadhead classification, and readable source-review text. Existing generic activity/duty storage needs no migration. Independent new fixture expectations were transcribed from approved Markdown tables, not extraction output. Preserved the exact original seven-fixture README from Git with its existing SHA-256 so additions do not rewrite the older approval.
- Review: the one-shot workflow activates Blind Hunter only; dispatch-specific edge-case/verification-gap layers are not active for this route. The independent reviewer returned four findings, all patched below. Initial added provenance assertion compared typed locations against dictionaries missing nullable fields; corrected the test to compare page/column/line explicitly, without product changes.
- Final verification: 161 backend/API/PostgreSQL tests (107.74s), real database/API restart and migration replay with exact synthetic state/deadline equality, production build, 2 focused browser examples (15.3s), and all 69 browser tests (3.0m). Final parser/mapping regression run separately passed 96 (15.97s). Initial full browser run passed 67 but failed both new tests due to Edge inspector response-cache eviction; corrected the real-response pass-through harness, without product changes. Root inspected reopened Fadder/CAR renders. All four review findings patched, none deferred.
- Local rollout verified: operational account/data/settings/migrations checksums and counts unchanged; database container/volume/secret preserved. Live backend source hashes equal verified code, API/page200 and final bundle checked; disposable services stopped. Restored generated older-story screenshots. No application changes after final tests, no operational test mutations, migration, commit or push. Existing human-owned 10.1 spec forbids commit/push; this overrides the skill's generic commit step. Implementation done here does not approve the story: sprint remains review awaiting owner acceptance.

## Review Triage Log

| Finding | Verdict / route | Evidence |
| --- | --- | --- |
| Nullable suffix makes unknown Vogn UNKNOWN look fully recognized | medium / patch | Confirmed generic duty regex can reach this case. Preserve unknown designation but add unrecognized-source-line warning; regression requires partial. CAR/CAR - 1 through CAR - 4 remain recognized. |
| Exploratory probe still expects CAR as route line | medium / patch | Confirmed probe reported line CAR whereas the approved interpretation uses CAR as vehicle/transition. Updated its independent expected mapping to null route line. |
| Additional regressions omit complete header/provenance checks | medium / patch | Added complete independent header values, all source row locations/calendar derivations and exact three duty locations/anchors. |
| Source review leaks deadhead_car internal name | low / patch | Confirmed rendered source-kind expression used raw internal string; display Tomkjøring med CAR as in adopted editor. |
