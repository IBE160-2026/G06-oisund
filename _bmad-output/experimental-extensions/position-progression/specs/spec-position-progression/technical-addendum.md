# Technical addition — foreground stop assistance

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Short extension proposal, 2026-10-26. Source inspection is not implementation or test evidence. Reuse React/TypeScript → FastAPI → PostgreSQL from the [V1 architecture spine](../../../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md). GPS and structured stops are extension-only deviations from V1's exclusions. Reinspect the completed V1 baseline before execution; no framework/service replacement or full architecture round.

## Reuse and narrow additions

| Existing surface, inspected read-only | Proposed extension responsibility |
|---|---|
| frontend/src/PrivateWorkdayView.tsx and PrivateActivitySelection.tsx | Put a small optional stop-assistance panel under the explicitly selected activity. Consume authorized frozen route facts; never change the selected activity, confirmed plan or outcomes from position. Hide private facts with the existing suspension/access gates. |
| frontend/src/PrivateAccess.tsx and useWorkdayResource.ts | Reuse session-bound request/mutation wrappers, visibility revalidation, generation guards and unresolved-operation comparison semantics. The existing resource hook only supports selection/start; add a narrow anchor client rather than passing an unsupported resource string or widening authority accidentally. |
| backend/app/private_main.py, workday_storage.py and workday_lifecycle_storage.py | Add an owner-scoped anchor resource using existing session, CSRF/origin, parent lock, expected revision, no-store and deadline checks. Lock/validate the parent before accepting a stop save; ended/aborted days are read-only. |
| backend/app/private_storage.py and existing migrations/cleanup | Add only the latest anchor and bounded operation receipts when PP-E1-S4 needs persistence. Parent deletion/expiry and closure shortening must reach both. Preserve unrelated saved plans, drafts, notices, bus assignments and outcomes. No raw GPS table. |

New logical pieces: a typed read-only route/coordinate binding; a small foreground controller and pure candidate evaluator; a latest-stop resource. These are modular additions, not a general location engine or duplicate route catalogue.

## Route and NSR boundary

[route-interface.md](route-interface.md) is the proposed contract v0. The prerequisite route function supplies the confirmed dated journey, ordered distinct occurrences, chosen range, source versions and frozen association. It is not implemented by this epic. PP-E1-S1 adds only the position consumer and missing coordinate qualification/binding.

Prefer attaching a bounded, versioned NSR coordinate sidecar during route preparation/confirmation through the existing route extension point. It binds StopPlace/Quay IDs and ScheduledStopPoint mapping, coordinate kind/WGS84, source/fetch/update metadata, validity, NSR object versions and mapping/snapshot revision to the selected route snapshot. Missing source-version metadata stays unknown and may block qualification; do not manufacture freshness. Frozen active route facts are never re-enriched silently. If the prerequisite lacks a preparation/carry-forward hook, record the needed contract addition here and block the affected integration rather than recreating route review.

NSR acquisition belongs behind a narrow adapter in the existing backend; use only bounded public stop IDs and relevant validity context, no private owner/workday/activity or GPS values. Verify supported response/version semantics, attribution and limits in PP-E1-S1 before retention. No arbitrary source-URL fetch, polling per fix, regional download or new service. Coordinate drift/mapping changes require explicit preparation/review and a new binding, not replacement of an active snapshot.

Eligibility validates dated identity/calendar, range/order and coordinate coverage separately from measurement availability. Partial coverage leaves the unsupported part manual. Wrong/missing Quay, unknown validity, a StopPlace centroid or incompatible mapping mode cannot be repaired by a precise GPS fix. No geometry is required for the first supported cases; ambiguous layouts remain manual.

## Foreground controller and evidence

Proposed states: Off → manual-start-needed → acquiring → following/uncertain; Pause or interruption → manual-resume-needed. Access suspension hides private state; terminal/denied/expired context disables assistance. Visibility return alone never starts sensing. Keep explicit user intent separate from browser lifecycle.

Bind each watch generation to session, workday, activity, dated trip/reference version and manual assertion. Stop/invalidate on Pause, Off, hidden page, material gap, context change, access loss or closure; late permission grants/callbacks cannot revive it. Keep only the bounded transient sample window. Timing gates use acquisition age plus monotonic elapsed protection; clock anomalies invalidate the sequence and require manual recovery.

Manual choice resets evidence, protects the new occurrence and remains a separately timestamped assertion. After protection, fresh coherent measurements and unique route-order support can revise the estimate to the next occurrence without per-stop confirmation. A timer, nearest point, repeated Quay or one contradictory sample never suffices. A far/backward contradiction requests manual re-anchoring; automatic multi-stop relocation is deferred. Use the unqualified seeds in [behavior.md](behavior.md) only as later experiment inputs.

## Latest-anchor transaction and recovery

Conceptual fields are in the route contract; no wire endpoint name is promised. Store one latest stop-context record per owner/workday with anchor revision, source trip/occurrence/version, original evidence/assertion timestamp and origin, server savedAt and parent expiresAt. No fix coordinates, trail, persistent client queue or public export. Minimize receipts to operation/payload digest, accepted anchor revision, server time and expiry; do not retain a full stop payload per receipt as a hidden stop history. Read the current anchor separately after acknowledgement.

Save explicit manual anchors and supported stop changes only while authorized, nonterminal and enabled. Serialize one pending save per controller; coalesce a newer candidate in memory, bound request/receipt count and bytes, and qualify practical cadence in PP-E1-S4. Do not mint endless retries. Expected revision rejects another tab's stale write; a delayed older candidate must not be rebased automatically over a newer anchor. Lost/malformed acknowledgements retain the same operation/payload for lookup or exact retry. Re-read current authority after a receipt; never present an old accepted result as latest.

Off prevents new saves and clears sensing memory. An in-flight save may already have committed; reconcile it without resuming sensing. Keep an acknowledged anchor under ordinary workday expiry, not an Off-triggered deletion of user data. On unavailable authority hide private display; on logout/expiry clear it. Existing parent deletion/cleanup removes anchor/receipts without changing unrelated records or extending any deadline.

Next-trip selection first checks identical workday identity, then maps stop IDs to the new confirmed dated trip's selected range. Same workday across midnight passes this scope check; another workday does not. A unique proposal needs explicit acceptance, creating a new manual assertion while retaining the old observation's provenance. Ambiguous/absent/different-Quay matches remain manual.

## Qualification tasks, not demonstrated behavior

PP-E1-S1 qualifies the dated handoff and NSR binding. PP-E1-S2 qualifies the actual Lenovo model, Android/build, Brave and Chrome separately, trusted HTTPS, permission behavior, fix quality and conservative thresholds. PP-E1-S3 qualifies visibility, lock, gaps, reload and explicit Pause/Off. PP-E1-S4 qualifies persistence races, bounded receipts and overnight identity/retention. Each story starts with synthetic cases; controlled device observation requires later authorization and records limitations separately. No GPS suitability, accuracy or battery result exists yet. A failure keeps the affected case manual or blocks its pilot claim.
