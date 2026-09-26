---
status: approved
created: 2026-09-26
epic: E5
story: '5.6'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.5', '5.4', '4.2', '4.8', '1.4']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice integrates reconnect detection, automatic source refresh and normal resumption of existing operational submissions. It keeps transport availability, source retrieval and operational acknowledgements independently observable. Conflict detection preserves work and stops affected submission; explicit resolution and writer transfer remain later E5 slices.

### Story 5.6: Refresh After Reconnection Without Hiding Missing Updates or Pending Work

As the driver continuing a working day,
I want the app to refresh automatically when usable connectivity returns and show what has actually recovered,
So that I can continue without mistaking a restored network connection for current source information or confirmed server storage.

**Acceptance Criteria:**

**Given** a permitted day running locally through a connection/update failure,
**When** browser connectivity hints, foreground return or a bounded retry suggest reconnection,
**Then** automatically attempt recovery through the existing private backend without requiring driver interaction,
**And** treat a browser online flag as a hint, not proof that the backend, Access gate or provider is reachable; show checking/unavailable status until the relevant response supports stronger wording,
**And** check local locks, pending revocation, day authority and expiry before private traffic; pending logout follows 1.2/5.5 before other requests,
**And** known revocation locks locally, while outer Access failure uses 5.5's separate classification/renewal path without forced login navigation while driving,
**And** keep existing permitted local operation and the active trip/manual choices throughout recovery; reconnect creates no movement evidence, new day, access extension or release activation.

**Given** actual backend connectivity is restored but source refresh or operational submission is outstanding,
**When** the top status is updated,
**Then** show connection restored with synchronization/updates pending and retain the prominent yellow-triangle missing-update warning until required retrieval succeeds,
**And** separately expose source-update state and locally saved work awaiting server confirmation, using concise text/symbols rather than technical queue/cursor identifiers,
**And** source success with a pending/failed outbox does not mean all work is synchronized; an acknowledged outbox with failed source retrieval does not clear the missing-update warning,
**And** do not present a failed/timed-out attempt as indefinitely in progress; identify pending, retry delayed, failed, access blocked or conflict requiring review where supported,
**And** when there are no pending operational events, do not invent a synchronization task or treat an empty queue as evidence that source retrieval succeeded.

**Given** restored authorized connectivity for the current source/day scope,
**When** automatic source recovery starts,
**Then** initiate or join 4.2's central per-source/pilot-area retrieval, respecting qualified cadence/provider limits and existing cursor/baseline recovery; multiple tabs/clients cannot multiply provider requests,
**And** accept a qualifying shared retrieval that covers the recovery need, with committed source generation/scope evidence, without forcing a duplicate provider fetch for each reconnect,
**And** an old pre-failure success, unchanged cached status, successful API health check, source request initiation or first page of a partial response cannot satisfy that need,
**And** define and test the recovery basis using source generation/scope and accepted request/result state rather than client-clock order alone, including a backend retrieval completed while this browser was disconnected,
**And** retain prior useful notices and source metadata while collection fails or remains partial; no response absence alone proves closure or an empty road network.

**Given** a required source retrieval completes according to its qualified protocol,
**When** validated results/status are committed on the backend and successfully applied to the current client context,
**Then** clear only the corresponding missing-update condition; do not clear it solely because the backend reports success if the client could not receive or commit the applicable result,
**And** failed sources/scopes retain visible local warnings; the overall missing-update warning remains while a required update is unresolved, without falsely describing the healthy sources as failed,
**And** successful retrieval means that retrieval completed, not that source content is fresh, metadata is complete or all real disruptions are covered; retain original source update time, last source success and client receipt time separately,
**And** an empty delta is no change; a complete empty result establishes only its qualified source scope/time, and never a general all-clear,
**And** refresh never changes confirmed plans, manual times/stops, actual trip/progress or driver notice state by treating source data as operational authority,
**And** reuse E4 lifecycle/relevance/seen/hidden/audio rules: unchanged/replayed notices and updates remain silent as specified; any genuinely new eligible receipt uses 4.8's policy rather than reconnect itself becoming an audio trigger.

**Given** committed local operational events or an immutable in-flight batch awaiting confirmation,
**When** usable access and current writer authority permit normal resubmission,
**Then** resume the existing AD-5 submission path in order, with one stable batch in flight per day and unchanged batch/event identity and payload after an uncertain response,
**And** only a valid matching receipt marks its accepted events confirmed in the local transaction; HTTP success, source retrieval or a read of server state cannot substitute for it,
**And** preserve locally committed changes made during the request and pending events outside the acknowledged batch; an acknowledgement cannot replace the whole local view with the submitted snapshot,
**And** a valid delayed receipt remains processable after a reconnect-generation change under current access/expiry rules, whereas stale source-status callbacks cannot regress newer source state; these different ordering rules must be tested separately,
**And** retry a lost acceptance response without duplicating PostgreSQL effects; failure to save the receipt locally retains the immutable batch for safe retry,
**And** 5.4 activation delivered after ordinary expiry remains unresolved without its required verifiable timing basis; reconnect or a fresh Access credential cannot manufacture that evidence.

**Given** source throttling/timeouts, repeated network flapping or concurrent recovery triggers,
**When** attempts are scheduled and completed,
**Then** coalesce duplicate triggers, use bounded documented retry/backoff consistent with provider rules and terminate each attempt with an honest result,
**And** ensure a stale failure cannot replace a later successful generation or clear a newer failure for another scope; pending timestamps do not reset forever on every online event,
**And** a failure of one independent source/submission path does not block unrelated authorized paths, subject to global access/revocation and causal event-order constraints,
**And** tab coordination prevents duplicate operational senders; source refresh stays centrally coordinated and does not increment operational server revisions,
**And** offer a movement-permitted retry where useful without demanding it during driving, stealing focus, opening detail or repeatedly announcing unchanged status; provide accessible focus handling for any invoked feedback surface.

**Given** a revision/writer conflict, invalid payload/schema, terminal/expired day or learned authority change,
**When** an attempted submission or response reports that condition,
**Then** stop incompatible retries for the affected work and preserve permitted local events and their original identities for explicit resolution; never silently overwrite, change epochs, mint substitute batches or take over by timeout,
**And** an old client stops acting as writer once it learns of transfer; retained changes remain identifiable for later review and are not auto-submitted under the new epoch,
**And** apply access/data expiry before read/send/application of late responses; expired work cannot be re-uploaded or given a new grace period to finish recovery,
**And** preserve retirement-versus-acknowledgement distinctions for any existing retired batch; this slice does not implement E7 terminal trimming/settlement,
**And** expose bounded recovery status and existing safe local/read-only behavior as applicable; explicit conflict-resolution and planned/emergency transfer UI remain subsequent stories, not a prerequisite for detecting/protecting these cases.

**Given** status/recovery metadata and actual synchronized data are persisted,
**When** storage, logout or privacy checks run,
**Then** reuse IndexedDB and authenticated FastAPI/PostgreSQL contracts, adding only necessary current recovery scope/generation/status metadata,
**And** failed local/backend writes cannot be shown as saved/applied; retain prior usable permitted state and retry non-destructively,
**And** private associations, outboxes and receipts retain original AD-12 deadlines; no permanent attempt history, raw response archive, credentials or GPS tracks are introduced,
**And** private/demo separation and authenticated scope checks remain effective for refresh triggers/status and receipt retrieval; responses arriving after logout or a different owner/day cannot expose private content.

**Given** a controlled E1–E5 day with retained notices and pending local corrections,
**When** recovery tests run,
**Then** cover the cross-product of source success/failure and outbox accepted/pending/failure, plus no pending events, first-ever source failure, multiple source scopes, partial pages and valid empty delta,
**And** cover online-with-unreachable-backend, Access HTML, source outage with healthy backend, network flapping, restart during retry, concurrent tabs, stale callbacks and valid late matching receipts,
**And** inject database/local acknowledgement failure, lost acceptance response, edits during submission, logout/revocation, original expiry, writer conflict and unresolved 5.4 timing evidence,
**And** verify real PostgreSQL receipt/revision effects separately from source generations and inspect client warnings at each transition; neither path's success may conceal the other's unresolved outcome.

**Traceability:** Primary FR-18 and shared FR-12/13/17/19/20, FR-1/16 access and safe presentation, FR-24 retention. NFR-1–4; UX-DR14/19/22/23/38/39/44; AD-2 retained local authority, AD-4/5 atomic receipts and independent source state, AD-7 central qualified retrieval, AD-8 notice identity, AD-9 unchanged actual context, AD-10/11 authority/conflict gates, AD-12 original expiry, AD-13 gate failures and AD-14 compatible client contract. No successful reconnect certifies live coverage or pilot readiness.

**Dependencies:** Implemented 5.5 access handling, 5.1–5.4 continuity/activation, 4.2 qualified source retrieval/status, E4 lifecycle through 4.8 and existing E1–E4 immutable submission/receipt handlers. This integrates those paths and protects conflicts; it does not depend on a future conflict UI or transfer implementation to demonstrate normal recovery and rejection handling.

**Size boundary:** Reconnect coordinator and shared status, using existing source and submission mechanisms. No new adapter, generic synchronization framework, conflict-resolution UI, writer transfer, terminal settlement, migrations or E6/E7 functionality. Actual source qualification remains 4.1/4.2 evidence and E8-P integration.

**Pilot qualification:** Repeatable browser/FastAPI/PostgreSQL fault scenarios contribute to E8-D. E8-P must qualify actual tethering, host/home-network and Access/source failure/recovery on Lenovo/Brave, with retained driving context and readable warnings. E8-E remains later field evaluation. Tests are specified, not run in planning.

**Approval:** Approved by the owner on 2026-09-26 with restored connectivity, validated source updates and confirmed server storage remaining separate statuses. Pending revocation is processed first; conflicts and lost receipts cannot cause silent overwrite. Planning approval only; the approved copy in epics.md is canonical.
