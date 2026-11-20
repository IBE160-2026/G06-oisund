---
title: 'Provide exact manual stop anchors throughout the line 20 pilot'
type: 'bugfix'
created: '2026-11-20'
status: 'done'
route: 'dispatch'
baseline_commit: '7a8949b3c120a597c29fb48dbe0d768c6391dc31'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Manual stop anchors in real line 20 pilot routes need exact parent StopPlace identities. The regional NSR export has all 120 mapped Quays. The current three-row sidecar and 32-row guard leave otherwise valid manual anchors unavailable. Supply the complete bounded pilot mapping for new reviews while preserving prior references.

## Boundaries & Constraints

**Always:** Use only the two pinned public archives already present. Keep the current route observation timestamp, immutable coordinate selection and private operation rules. Coordinates missing dated validity are unavailable for GPS and cross-trip proposals. No product geolocation, new network call, migration, deployment, private data or signing changes. Edit only this V2 worktree and leave commits to the coordinator.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| New exact pilot reference | Reviewed explicit route decision under the original timetable digest | Save and freeze the current manual mapping revision; preserve receipt and route-review semantics | A different timetable digest does not acquire this mapping |
| Prior reference | Persisted implicit v1, explicit v1, or explicit null | Preserve historical v1 mapping and fingerprint; explicit null stays unmapped | Unknown revisions stay unavailable |
| Real manual mapping | Exact Quay among the 120 expected pilot identities | Present exact StopPlace and permit the existing manual save with null coordinate revision | No invented date, no GPS permission or positive coordinate qualification |
| Duplicate, mismatched, or malformed evidence | Conflicting Quay or incorrect parent or archive | Preserve explicit unavailability | Fail closed without replacing older accepted authority |

</frozen-after-approval>

## Code Map

- `backend/app/route_source.py` qualifies the pinned regional timetable. `.private-runtime/route/troms-netex-1795129398375617.zip` is SHA-256 `03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9`. The known seven-day coverage contains 120 unique Quays. The pinned NSR export `.private-runtime/route/troms-nsr-1795125615869698.zip` is SHA-256 `2c224106067c28de88b6e67e04d3a33c527ae629ee6b3103dcb309e430d8427a`, 1,980,625 bytes, with one member `tiamat-export-55_Troms-202611192300011691.xml`, 31,423,981 bytes. Local acquisition metadata is 2026-11-20 01:14:33 UTC. StopPlace and nested Quay exact IDs and source versions are available. Individual Quay validity is absent. Entur's current open-data publication is `https://developer.entur.no/open-data/stops`.
- `backend/app/position_coordinates.py` binds old references by raw digest and handles exact parent and eligibility. Preserve v1 bytes; add a separately pinned manual sidecar with size/count bounds for 120 records. `backend/app/route_reference_storage.py` `save` constructs the newly reviewed copy after replay and before freeze; bind the new revision there only for the known timetable SHA. Preserve request DTO/hash and legacy read fallback. The anchor API already accepts manual null coordinate revision with an exact parent.
- `frontend/src/positionAnchorClient.ts` allowlists the old REST docs URL. Accept the exact official NSR archive documentation URL for the new source. Keep pending receipts and user-selected activation behavior unchanged.

## Tasks & Acceptance

- [x] Reconcile the public pinned archives offline. Keep only the exact scheduled 120 mappings, verified identities/version/centroid, explicit unknown validity, NLOD, original generation/digests, and documented reproducibility. The extraction can be a one-off under ignored `tmp` when the checked-in data and evidence are sufficient to audit it.
- [x] Implement current/legacy mapping selection and official v2 source link through the existing DTOs. Keep old records and missing/manual-only modes.
- [x] Cover pinned membership, new pin through real route HTTP save/replay/confirmation, legacy/explicit null, manual API with real mapping and GPS rejection, and frontend projection acceptance.

## Implementation Notes

Use existing stopped V2 Docker images for read-only offline work if Windows Python lacks IANA tzdata. Coordinate before starting the shared V2 test project. The source acquisition methodology and live version probe will be documented by the coordinator.

The 120-row artifact pins its serialized SHA-256 under the exact `eol=lf` rule. The current digest is associated with new decisions, while existing JSON fingerprints are left unmodified. Both archived data membership and private receipt verification passed against the current V2 fixture project.

## Verification

The targeted PostgreSQL and API suite passed 31 tests and the restore suite passed four. The TypeScript/Vite build, 18 deterministic motion tests and seven Edge cases passed. The isolated live API replay used the archived 80-call public journey and a disposable account, froze the route receipt, saved a manual anchor at call 80 and rejected the corresponding GPS write.

## Spec Change Log

## Review Triage Log

| Layer and finding | Verdict | Evidence and action |
| --- | --- | --- |
| Blind · source age before the operating dates | Medium | The archived observation expires earlier. Documented effective preparation window and requalification condition. |
| Blind · new pin with unavailable artifact | Medium | A damaged package could reduce manual coverage on a newly saved decision. Validate at selection and preserve a known same-source legacy fallback. |
| Blind · historical reader depends on the new writer selector | Medium | A later writer change would misclassify the old v2 release. Separate stable historical binding from writer choice. |
| Blind · existing scheduled parent with explicit null | Low | The old scheduled parent remains available independently of lookup. Clarified in evidence and added a populated control. |
| Blind · all-row runtime projection | Medium | The archive test can skip and checks source fields separately from runtime projection. Added a packaged-data control for all rows. |
| Blind · manual-only v2 browser flow | Medium | The previous browser control sends an eligible coordinate revision. Added the null-coordinate, no-watch control. |
| Blind · server handoff with missing dated coordinates | Medium | Frontend rejection alone would miss a server regression. Added an authenticated control for the manual-only mapping. |
| Blind · v1 bytes could be edited by an operator | Low | The shipped v1 bytes are unchanged and app code has no writer for the packaged file. A new checksum policy for historical product assets is outside this coverage fix. |
| Blind · moving source URL in release metadata | Low | A latest URL could resolve to a different archive later. Pin the original object generation in metadata. |
| Blind · truncated observation precision | Low | Use the complete observation from the launcher in the extract and fixture. |
| Edge · DST in test sign-off | Medium | Wall arithmetic can form an invalid local offset at a spring transition. Do duration arithmetic in UTC. |
| Edge · operating window claim | Medium | Distinguish pre-pilot review from the later period that requires checked fresh source data. |
| Verification · no-archive positive API control | Medium | A clean checkout otherwise skips the positive reference-write case. Supply an archive-independent control against packaged v2 data. |
| Verification · accepted duplicate ambiguity | Medium | The tampered artifact was rejected before reaching lookup. Exercise a digest-accepted duplicate of the queried ID as a separate fixture. |
