# 11.5 corrective cross-day register execution

The owner rejected per-workday notice ownership. This correction keeps one
account-owned incident and consults it against each authorized displayed plan.
No title/text deduplication or per-day copies are introduced.

## Implemented

- Migration 013 backfills owner and independent retention on canonical rows,
  preserves IDs/content/source times/check facts, and makes original workday
  provenance nullable with `ON DELETE SET NULL`. Unknown endings keep their
  existing storage deadline. Already ended legacy rows receive one migration
  grace period; no legacy manual-ending instant is fabricated.
- New `/notices` account routes use account-serialized revisions, required future
  endings, exact Oslo clocks or date-only 23:59:59, terminal manual ending, and
  checks before and after writes against the original server deadline. Ended and
  expired notices cannot be edited, checked, extended or resurrected.
- Account operation receipts follow incident retention. Historical receipt JSON
  and fingerprints remain immutable. Legacy replay reconstructs the deployed
  fingerprint and checks original parent/action/target/payload. Status lookup
  survives parent removal while requiring current account/resource retention.
  Legacy receipt `expires_at` metadata intentionally follows canonical incident
  retention; this is distinct from immutable historical JSON.
- Startup/hourly cleanup independently purges incidents and associated command
  metadata after retention. Manual ending cannot lengthen an unknown legacy
  notice's original storage lease. Reads/login/retries do not extend retention.
- The retained account controller lives above plan replacement/expiry. Dirty
  input and original pending commands survive consulting, switching days and
  displayed-plan expiry. Workspace loss/session guards remain active, and
  account registry proposals do not block safe day navigation.
- Reader and maintenance use server timestamps plus monotonic elapsed time.
  Active reading excludes unknown-ending, manually ended and expired rows;
  maintenance distinguishes `Mangler sluttdato`, `Utløpt` and `Avsluttet manuelt`.
  Source checking remains explicit and separate.

## Executed verification

- Frontend TypeScript/Vite build passed after the final source changes.
- Real guarded synthetic HTTP/PostgreSQL notice/reader suite: **77 passed** in
  106.12 seconds. Raw final output: `tmp/11-5-crossday-api-final.log`.
- This includes cross-day identity/edit/check, original-day close/delete,
  ownership/privacy/no-store, exact-line/all-line and interval filtering,
  pagination/capacities, required/date-only/exact/DST endings, near-deadline
  extension and held-lock expiry rejection, revision races, immutable receipts,
  isolated populated 012→013 migration, unknown-ending completion/manual end,
  independent retention/purge and repeated migration calls.
- Browser regression: **94 passed, 2 failed** in the initial corrected 96-case
  run. Both failures were retained assertions superseded by the new contract:
  opening an already retained expanded history detail and expecting a manually
  ended incident in the active reader. Both were corrected and rerun together
  with the positive extension case: **3 passed** in 32 seconds. Logs:
  `tmp/11-5-crossday-browser-rerun.log` and
  `tmp/11-5-crossday-browser-affected.log`.
- An additional displayed-plan-expiry/original-command recovery browser test
  passed: `tmp/11-5-crossday-displayed-expiry.log`.
- Browser coverage includes real controls for extension with the same incident
  ID and deadline on both days, retained check qualification, actual parent purge,
  dirty/pending navigation, source/status-first lost save/check/manual-end
  recovery, malformed replies, owner/session/plan invalidation, unavailable and
  late/filter-race reads, live expiry with device skew/wall-clock jump, selected
  activity and unrelated original-command recovery regressions.
- Enlarged Day/Night evidence covers register/editor/history/recovery and reader
  at narrow and wider viewports, with overflow/contrast/control/focus assertions.
  New evidence names begin `11-5-crossday-`. Historical PNG/JSON evidence was
  restored byte-for-byte from the initial archive; six newly rendered unchanged
  11.6 regression PNGs were retained under `11-5-crossday-regression-*`.
- Verifier control-flow/restoration suite: **7 passed**. Backend source syntax
  check passed. The verifier now includes independent notice/receipt snapshots
  and the new account notice suite while retaining other resource guards.

## Boundaries

Only `ibe160-private-tests` synthetic accounts were used as fixtures. At the
worker checkpoint, the ordinary API was restored healthy without building or
migrating its image; the completed root rollout is recorded below. No files
were staged, committed or pushed. No manual owner acceptance was recorded.
Physical Lenovo Pad/Android/Brave/mobile-network qualification remains separate.

An unrelated existing access timer overflows its browser timeout range if a
device clock is more than about eleven days slow at login. Notice skew coverage
uses a two-hour initial skew and a one-day subsequent backward jump, proving
notice expiry is monotonic without changing that separate access behavior.

## Final root review, verification and local rollout

Three independent BMAD review layers completed. Every retained correction finding was fixed by the original implementation worker and reinspected by the original reviewers. The broad planned-day line/time contract was retained deliberately; an optional exact manual-ending timestamp surface was rejected as a low-impact enhancement. No retained correction finding remains deferred. The unchanged extreme device-clock/session timer limitation above is recorded separately in deferred-work.md.

Focused patch checks passed five backend cases and ten unique browser cases across the initial seven passes and four affected reruns. The three initial browser failures were premature waits on the initial `uavklart` message; the corrected tests wait for completed original/lookup requests. This initial invocation is not relabelled green.

Root started one full guarded invocation at 14:26 UTC. It exited **0**: **420 backend tests passed in 516.21s** with one TestClient dependency deprecation warning, and **all 472 browser cases in 19 files passed in one invocation (37.4m)**. Populated restart, repeated migrations, exact state/receipt/deadline/session preservation, cleanup and production build passed. Raw log: `tmp/11-5-crossday-root-full-gate.log`. The earlier focused invocations and their timing failures remain recorded above; they are not relabelled.

Before the gate, root froze 112 implementation/test/migration/verifier hashes; all match after the gate. Preservation checks confirmed 914 initial files retained, 309 historical evidence files, 24 original fixtures and 25 historical frozen contract blocks byte-preserved; generic delivered 11.6 recovery is unchanged. The full gate rerendered 111 historical artifacts: these fresh copies are archived separately in ignored scratch and historical bytes restored. Root also inspected narrow Day/Night register/reader renders; automated geometry, overflow, focus and contrast assertions remain distinct from physical qualification.

Ordinary comparison after focused tests found only three new login throttle rows from one failed login; all original business fields were unchanged. These short-lived rows were left to normal expiry/unchanged cleanup, with no baseline reset or forced deletion. The full gate restored ordinary services; the final strict comparison passed, allowing only expired startup throttle cleanup.

Root then built the ordinary private API and applied additive migration **013**. Post-rollout checks preserve original fields of **all 23 ordinary tables**, the original database and secret, and **12 immutable legacy receipt/identity hashes**. Legacy receipt retention metadata intentionally follows the independently retained incident; JSON results and payload hashes are unchanged. The new account operation table is a schema addition. Ordinary services are healthy and synthetic services stopped. Served private HTML and both assets match the tested distribution (`index-Dm8Epahj.js`, `index-8lnBnkIq.css`); all **43 runtime Python/migration files** match tested source.

Story 11.5 and sprint status are **review**, specification **in-review**, manual acceptance **pending**. Existing 11.6 stays in its prior review state. HEAD remains `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed`; nothing is staged, committed or pushed and no further story/epic is started. Physical Lenovo Pad/Android/Brave/mobile-network qualification and the separate unchanged extreme-clock access limitation remain open.

## Owner test steps

1. Preserve any unsaved text in an existing tab before refreshing to the corrected build. Use the existing private address on the tablet; localhost addresses refer to the desktop server, not the tablet.
2. Open **Manuelt vedlikeholdte avvik**. Register one notice for a line present in two scanned/confirmed days. Enter **Gyldig til** after both days; leaving the optional clock empty explicitly means 23:59:59 on that Oslo date. Save once.
3. Open **Les avvik for linjer og datoer** for each day. The same notice should appear automatically where its lines and planned interval match. Change the line/date filters and return to the day; the selected activity should be unchanged. Do not register a second copy.
4. Before the existing deadline, edit that notice and save a later ending. Check both days again: both consult the same updated entry. Merely typing a later date does not extend it; saving must succeed before the old deadline.
5. For a separate short-lived test entry, supply an exact ending clock a few minutes ahead. To test disappearance from the reader, use a confirmed day whose planned interval overlaps this validity window; a future-dated example plan will correctly not match a notice ending today. Otherwise test the deadline in maintenance: after it passes, fetch again and verify **Utløpt**. It cannot be extended or revived. History is retained for seven days after effective ending.
6. For another entry, choose **Avslutt avvik manuelt** and confirm. It becomes **Avsluttet manuelt**, disappears from the active reader and cannot be reopened. Source-check status remains a separate fact; none of these states certifies road clearance.
7. Existing **Mangler sluttdato** entries need a future ending before they can be reused. Older separately entered duplicates remain separate; review and manually end unnecessary active copies rather than assuming automatic merging. Empty results mean no matching registered entry, not that no traffic disruption exists.

Manual owner acceptance has not been recorded. Desktop automation does not qualify the physical Lenovo Pad/Android/Brave/mobile-network setup.

## Owner acceptance ? 2026-10-26

Jonas explicitly replied `Godkjent.` to the corrected 11.5 delivery report. Story 11.5 and its active specification/sprint tracking are done with owner acceptance accepted. Existing 11.6 remains review and Epic 11 remains in-progress. No new tests or physical-device qualification are inferred. The earlier stop before staging/commit/push and further work remains in effect; no such action was taken.


## 11.6 integration follow-up — 2026-10-26

Corrected 11.5 remains explicitly accepted by Jonas. A fresh 11.6 integration review repaired proxy-error recovery classification, elapsed validity during delayed replies and maintenance list timestamp consistency. These are changes to failure/latency behavior in already accepted 11.5; manual regression of the affected behavior is requested as part of 11.6, not accepted on the owner's behalf. Full updated evidence and desktop-local startup/test steps are in [the current integrated 11.6 delivery](11-6-server-recovery.md#current-integrated-delivery--26-october-2026). Historical 11.5 results above remain unchanged.
