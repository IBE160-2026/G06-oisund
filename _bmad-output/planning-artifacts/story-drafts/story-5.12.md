---
status: approved
created: 2026-09-26
epic: E5
story: '5.12'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.11', '5.2', '5.3', '5.10']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice adds controlled owner-accepted activation of a completely staged successor and versioned local storage migration between working days. It reuses 5.2's complete assets/coherent boot and 5.11's required backend compatibility. It does not deploy a release or implement the later AD-12 terminal settlement flow.

### Story 5.12: Accept an App Update Between Days Without Losing Retained Work

As the pilot owner,
I want to activate a verified app update between working days with retained work safely carried forward,
So that updating or recovering from a failed update cannot interrupt an active day, lose pending changes or bypass access rules.

**Acceptance Criteria:**

**Given** a successor application build is available,
**When** its assets are downloaded/staged,
**Then** reuse 5.2's complete integrity-checked app-file set and preserve the selected build and retained private data until activation prerequisites are satisfied,
**And** distinguish download, verification, update available, blocked, migrating and activation complete; downloading or a new Service Worker becoming active is not owner acceptance or permission to migrate,
**And** bind any activation choice to the specific verified build and applicable storage transition, not an indefinite agreement to install whatever becomes available next,
**And** reject missing/wrong-build/login-page assets and failed staging without pruning the build still needed by an active day or retained work.

**Given** the owner is between working days and chooses to activate the staged build,
**When** the app checks the update preconditions,
**Then** verify no active day is using the affected store/build, including coordinated tabs, and inspect retained drafts, prepared days, pending batches, conflicts, review intake/dispositions, handover state and pending logout,
**And** verify a supported migration path and 5.11 backend compatibility for all retained contracts before activation; inability to establish compatibility leaves activation blocked rather than assuming the newest code is safe,
**And** pending work need not be deleted or falsely acknowledged to permit updating: migrate it only through a proven preserving path; unresolved authority/transfer or unsafe storage conditions block activation where consistency cannot be established,
**And** explain blockers in ordinary Norwegian and allow postponement; postpone/cancel before migration leaves the selected build and work intact,
**And** a new-client requirement may block authorizing a new day, but does not revoke an existing active day's continuation, erase retained work or manufacture a new sign-in/grant,
**And** an active day in any affected context blocks the ordinary app/schema switch even if another tab displays the main menu or the planned finishing time has passed.

**Given** an owner-approved update passes preconditions,
**When** the migration/activation begins,
**Then** coordinate tabs and workers using the established locking/version scheme, rechecking active-day and storage state at the commit boundary so racing operations cannot mutate an obsolete schema,
**And** blocked database upgrades or uncooperative tabs give a visible pending/blocked result, not destructive database deletion or silent forced activation,
**And** use versioned transactional local migrations where possible; for necessary multi-step transitions document the recoverable states and test interruption at each persistent boundary,
**And** preserve a coherent boot decision across the non-atomic boundaries between asset cache, private IndexedDB and build-selection metadata; never publish a ready marker for a partially migrated or incompatible combination,
**And** a second updater or delayed callback cannot select another build or run a completed migration twice; persisted transition state supports restart without guessing.

**Given** retained private E1–E5 records are migrated,
**When** the new local schema is committed,
**Then** preserve owner/day/plan/context identities, service dates, manual trip pins and stop corrections, bus-change provenance, notice identities/version states, audio-attempt outcomes, movement history/outage timing and unknown values,
**And** preserve writer epochs, original access/data deadlines, lock/pending-revocation state, unsynchronized events and batches, receipts, conflicts and review/handover states without converting pending or received-for-review into accepted,
**And** immutable outbox IDs/payloads and their integrity basis remain unchanged for retry under the original supported event schema; migrating local indexes/wrappers is not permission to rewrite event content or reset sequence/revision meaning,
**And** retain manual theme preferences and the operational context contract that E6/E7 will extend; current fixtures do not imply those later features are implemented,
**And** migration changes representation only, never marks a draft confirmed, a prepared day active, an uncertain action observed or a terminal day resumed,
**And** demonstrate equality of required preserved facts and original immutable batch representations before/after the concrete transition, rather than merely checking that the new screen loads.

**Given** all browser tabs close while a successor worker/update is waiting, or an activation is interrupted,
**When** the app reopens online, offline or with Access expired,
**Then** an active day still boots its required coherent build through 5.2 without accepting the waiting successor or starting migration,
**And** an interrupted between-day migration resumes or recovers only through its validated state transition and compatible code/storage combination; closing/reopening is not fresh consent for a different update,
**And** run private lock/authority/expiry checks before rendering or sending retained work; no stale history page or late update callback may expose locked content,
**And** original data expiry still applies during migration and on return: delete expired private copies before use rather than extending their lifetime for recovery,
**And** retain the actual observation gap and movement history; update/restart is not a new measurement or a new first-start exemption.

**Given** migration, validation or post-migration opening fails,
**When** recovery is offered,
**Then** report the failed/blocked transition and preserve permitted data plus any still-usable compatible build; no clear-storage repair, random old/new mixture, silent field dropping or recreated outbox identity is allowed,
**And** reactivate older code only if it is proven compatible with the current stored schema and retained contracts; an irreversible schema transition cannot be undone by selecting an older bundle,
**And** when no compatible executable path remains, stop activation and offer explicit non-destructive recovery rather than claiming successful rollback or promising an unavailable offline recovery screen,
**And** any temporary migration staging is bounded recovery state under the same privacy/expiry rules, cleaned when no longer required; it is not a historical private snapshot/archive or a new disaster-recovery feature,
**And** distinguish browser eviction/actual missing data from recoverable migration failure, without claiming to restore information that no longer exists.

**Given** logout, revocation or an expired application session overlaps an update,
**When** activation, recovery or a server request is attempted,
**Then** preserve 1.2/5.5 local locking and pending-revocation priority; updating is never a prerequisite for using the retained supported logout/revocation path,
**And** Access renewal or new app code alone cannot unlock retained private work, discard unresolved revocation or renew ordinary/day authority,
**And** current access guards remain effective if the migration is blocked, and late callbacks cannot apply a different owner/day's private state,
**And** local migration completion is not server confirmation: any required authenticated private metadata synchronization uses existing matching receipts, while the ordinary operational outbox remains unchanged,
**And** reject demo/private storage or credential mixing; no credentials/private payloads appear in release artifacts, logs or test publications.

**Given** activation succeeded and obsolete assets/staging may be cleaned up,
**When** pruning checks run,
**Then** retain files/formats actually required by active or unexpired retained work and pending compatible recovery, following 5.2/5.11 rather than release count or deployment age alone,
**And** keep one selected build and one staged successor as the normal V1 case, with additional nonpersonal code only for a demonstrated retained-work need,
**And** remove redundant permitted migration copies after validated completion and original expiry as applicable; code retention cannot hide expired private associations,
**And** show activated only after the selected app can open its migrated guarded state coherently, preserving readable status, keyboard focus and non-color feedback without forcing update interaction during driving.

**Given** an actual retained client/storage fixture and a concrete compatible successor,
**When** browser integration and real backend receipt checks run,
**Then** test accepted/postponed update, incomplete staged files, pending work with a supported path, unsafe transition, active day in another tab, a blocked database upgrade and simultaneous updaters,
**And** close/reopen with an update waiting during an active day both offline and Access-expired; verify no app/schema switch,
**And** interrupt every persisted migration/selection boundary, inject quota/read/write failures and test compatible rollback versus blocked destructive downgrade,
**And** include an immutable accepted-but-unacknowledged batch, pending logout, manual corrections, exact notice/audio state, review intake, handover ambiguity and original expiry during closure; verify retries against PostgreSQL retain the original meaning and no duplicated effects,
**And** distinguish actual stored-format migration evidence from backend-only compatibility tests; E6/E7 must later extend preservation tests for their added state.

**Traceability:** Controlled client-update continuity FR-1/17/18/20/24 and retained E1–E4 behavior; NFR-1–4; UX-DR3/14/16/19/23/24/38/39/44. AD-2 local transactions/assets, AD-3 coherent client engine, AD-5 immutable event contracts, AD-8 notice version preservation, AD-9 context/movement, AD-10/11 access and writer authority, AD-12 original expiry/no private historical backup, AD-13 Access separation and AD-14 staged accepted activation, migration and storage-compatible rollback.

**Dependencies:** Implemented 5.2 complete assets/boot routing, 5.11 backend compatibility and existing E1–E5 stored state through 5.10. Use a concrete old/new local schema transition and controlled terminal fixtures where needed without requiring future E7 screens. No future settlement or mentor feature is needed to prove this update path; later consumers extend its preservation contract.

**Size boundary:** One controlled owner-accepted app/local-schema transition and its failure recovery, using existing assets/version and backend contracts. No deployment, generic release platform, new features, private backup system, historical data restoration or E7 closing protocol.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL interruption cases contribute to E8-D. E8-P requires actual Lenovo/Brave multi-tab/worker/IndexedDB lifecycle, close/restart with a waiting update, storage failures and integrated Access/offline behavior. E8-E remains later field evaluation. No implementation, migration, deployment or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with downloaded/staged updates distinct from actual build activation, preserving active days, pending work and access rules through migration/restart. Planning approval only; the approved copy in epics.md is canonical.
