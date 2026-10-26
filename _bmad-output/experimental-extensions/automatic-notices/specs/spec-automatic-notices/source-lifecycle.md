# Source collection and lifecycle

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Draft behavior for CAP-1,4,6. D = documented in adopted research, O = observed there, P = proposed product behavior, U = unresolved. Draft requirements are not provider guarantees.

## Evidence boundary

D: Entur documents TRO SIRI-SX, application identification, four GET requests/minute, full versus requestor-session updates and MoreData paging. O: the three-record page had MoreData=true; no complete snapshot, continuation cursor or recovery was qualified. Version/VersionedAtTime were absent. D: profile describes explicit open/closed and validity; actual TRO closure/retraction was not observed. Research and entur-r1 digest retain URLs/access dates.

## Complete collection and recovery

P: Complete means all pages for declared provider/dataset, filters, mode and observation window have been parsed and validated, no MoreData remains, and no unresolved truncation, session loss or scope mismatch exists. A terminal page cannot hide prior failure. Repeated/stalled pages, budget exhaustion, malformed responses and expired continuation produce partial status, not success.

P: Retain attempt/result, declared scope, page progress, baseline/session continuity, response time, last complete baseline and last successful synchronization with record counts. A zero result requires a qualified complete cycle and means zero candidates within that scope, never no disruptions or road clear.

P: Qualify baseline and delta continuity separately. A no-change delta is not a new baseline. A valid continuous delta session can advance successful-sync time while baseline age stays distinct. Restart without proven continuity, session expiry, missed-close window, parser/schema change or unknown cursor requires complete resynchronization. Until then retain known content with partial/unavailable/needs-resync labels and do not infer absence.

P: Valid records from partial collections may be shown with a partial label; they cannot promote the whole view to complete. A validated newer explicit close can update that source record even during a partial cycle. Other records retain their uncertainty. Without defensible update ordering, preserve conflict rather than silently reopening/replacing known state.

## Fields, identity and clocks

P: Preserve provider/dataset, participant/source situation identity, optional version, summary/body/advice, original source link if present, typed affected entities and nested qualifiers, validity windows, original temporal wording and source status. Unknown fields remain null/unknown. A provider reference page is distinct from a missing item URL. Preserve original content beside local interpretation.

P: Distinguish source creation, publisher update/version time, response time, fetch/first-seen/last-seen, complete baseline, successful synchronization, explicit user check and user-association time. Fetch never fills unknown publisher-update or manual-check time. Old creation alone does not stale an actively observed open notice. Versionless changes are observed changes with publisher time unknown.

P: Repeated identical records are one contribution. Updates keep source identity; retain earlier user-referenced content and explain material changes. Older ordered versions cannot replace newer state. Versionless contradictory content remains a conflict when ordering is not defensible. No database/schema or fingerprint algorithm is selected here.

## Separate lifecycle dimensions

| Meaning | Trigger | Required behavior |
|---|---|---|
|Source open| Explicit source status | Relevance still depends on time/scope/health |
|Not seen| Absent from complete comparable baseline | Preserve last observation; never infer closed |
|Observation unknown| Partial, failure or delta gap | No absence inference |
|Expired validity| Known end passed with no later applicable window | Leave current-time candidates with accessible expiry reason; no road-reopening claim |
|Source closed| Explicit validated close for same identity | Stop active source candidates; retain evidence; do not close manual contributions |
|User ended| Explicit user action | Remains independent of source updates |
|Source retracted| Explicit qualified retraction evidence | Never derive from disappearance; use not-seen/unknown until semantics qualified |

P: Search-result disappearance or filter exit is not comparable-baseline absence. A source closure ends that source's statement, not the real-world incident or every grouped contribution. Reappearance can clear not-seen on a valid observation but cannot undo manual ending. A source-closed record can coexist with expired validity and a manually open supplementary record.

D: The cited profile redistributes a close until EndTime at least five hours ahead. P: Recovery must tolerate missing this window; omission after resync still does not establish incident resolution.

## Health and local reference checks

P: Show never-qualified, collecting/partial, complete-current, unavailable and needs-resync; age is independent. Keep last attempt, last successful sync and baseline age distinct. Retained records stay readable with last known content, warning and source link. No first complete baseline means coverage unknown despite individual observed records. Unknown observation stays visible even if a stale-age threshold has not elapsed.

P/Q-3: Five-minute refresh target and fifteen-minute age warning are proposals, not SLA. All paging/retry/recovery shares the documented rate budget; backoff/throttling cannot masquerade as a met cadence. Provider publication latency remains unknown. Failed attempts do not erase prior success clocks.

P: Svipper is manually opened for selected local checks. Keep URL, explicit observed facts and check time; opening a link alone is not a completed check. No automatic scraping or presentation-API dependence. Contact a provider only when documentation and bounded permitted qualification cannot resolve a specific blocking ambiguity.

## First-epic collection choice

For AN-E1, use fresh complete paged baselines; no long-lived delta mode is delivered. Requestor/session identity is used only if K-1 qualifies its page-continuation semantics within a cycle. A restart or expired/unknown cursor requires a new full baseline; partial-only operation is not an accepted substitute. The earlier delta discussion remains a future-mode constraint, not an additional first-epic feature. Provisional Q-3 timing and Q-5 retention are classified in product-decisions.md; technical-addendum.md locates the bounded implementation responsibilities.
