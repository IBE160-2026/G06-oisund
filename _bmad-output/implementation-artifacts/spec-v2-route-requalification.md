---
title: 'Requalify an unchanged line 20 timetable for the owner trial'
type: 'feature'
created: '2026-11-20'
status: 'done'
route: 'dispatch'
baseline_commit: '73d07a9ce859dc629598f685733971487949a2aa'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

The initial source observation expires before the owner trial dates. Provide an explicit Owner recheck that accepts the current public archive when it preserves the fully qualified seven service dates and the exact dated line 20 facts, including all departures, patterns and calls. Preserve the new archive's own provenance and the original workday and receipt data.

## Boundaries & Constraints

Use the fixed Entur Troms archive over TLS, one bounded request with no redirects per explicit check and no private input. Compare against the original hash-pinned complete seven-day corpus. Compare the entire normalized day objects, including versions, calendars, pattern IDs, ranges, ordered Quays, clocks and coverage. Changes or partial coverage require a separately reviewed pin. The 24-hour clock uses the real recheck observation, with acquisition and provider clocks distinct. Never use a local clock to relabel old data. Keep normal starts, Test, and HTTP requests offline for this source. No change to window, expiry, migrations, OS/server or service scope.

| Case | Expected behavior |
| --- | --- |
| Same current bytes or byte-distinct equivalent archive | Both yield a fresh actual observation while valid. New bytes own a distinct client-visible SHA. The rechecked source continues to support v2 manual anchors only. |
| Changed calls with same counts, incomplete archive, invalid transport or corrupt local receipt | Reject and report. No previously qualified receipt is overwritten on check failure. Startup uses the original known observation when local recheck evidence cannot be validated. |
| Replay and frozen selection | Existing route decisions and saved operation receipts are untouched. A basis from an earlier archive cannot be used to save a new decision against different current bytes. |

</frozen-after-approval>

## Code Map

- `backend/app/route_source.py` owns the existing download bounds, XML allowlist, seven dates and expected counts, parser, lookup clock and provenance. Keep original `load(path,timestamp)` and default exact archive pin behaviors backward compatible while reusing normalization for the successor.
- Keep the refreshed archive and metadata in one bounded, atomically published local bundle inside the existing ignored `/reference` mount. The explicit writer may use a one-off Owner container with that directory writable; regular API mounts stay read-only. Record SHA, size, generation, ETag and checked UTC. At launch rehash and compare complete day facts again. Network errors surface in the explicit invocation and do not delete the prior receipt.
- `scripts/v2-local.ps1` and `compose.v2.yaml` supply an explicit `-RecheckRouteSource` switch only in Owner startup. Use separate one-off process with no API ports. Reuse the existing launch environment. Normal mode automatically consumes retained qualified evidence offline. Rechecking should report why it failed and allow later ordinary launch.
- `backend/app/route_reference_storage.py` keeps actual digest authoring and provenance/frozen receipts. `backend/app/position_coordinates.py` may use a server-proven original basis for explicit v2 on equivalent new bytes. Never widen implicit v1 or fall back to v1 on successor bytes. Treat a same-digest fresh observation as the same source version. Frontend already accepts additional provenance fields.

## Tasks & Acceptance

- [x] Implement bounded qualification and frozen provenance without making old evidence look current.
- [x] Wire the explicit Owner launcher option and document actual supported conditions and failure behavior in `docs/v2-route-p1.md` and `docs/v2-handoff.md`.
- [x] Extend `backend/tests/test_route_source.py` and position/reference tests for seven-day equality, changed results with the same counts, partial / bad metadata / corruption, original compatibility, and fresh/expiry semantics. Include positive equivalents using byte-distinct synthetic data. Exercise the isolated launcher with the original public archive.

## Implementation Notes

- The one-off Owner service makes one unconditional GET to the fixed public TLS URL. The source retains the local check, HTTP Date, cache Age and both XML publication clocks separately. The earliest of HTTP Date and local check minus cache Age controls the original 24-hour interval.
- A byte-distinct archive qualifies only when the same seven complete day objects and their in-domain availability and calendar rules match the original. Dates outside the pilot window are excluded from date-range comparisons. The retained archive and checksummed receipt share one atomic bundle, and normal startup validates it offline with the original pin as fallback.
- New decisions bind to the actual current archive digest. A qualified recheck permits only an explicit v2 manual coordinate pin, while existing saved decisions and receipts retain their frozen provenance and coordinate binding.

## Spec Change Log

## Review Triage Log

| Layer and finding | Verdict | Evidence and action |
| --- | --- | --- |
| Blind · versioned NeTEx references | Medium | The baseline's versioned pattern and occurrence references resolve exactly. Check the referenced versions before an archive can qualify. |
| Blind · duplicate field values | Medium | Single-value readers used only the first match. Reject duplicate values, including conflicting departure clocks. |
| Blind · unsupported ZIP decoder | Medium | An LZMA decoder failure could bypass fallback. Support the shipped stored and deflated formats. |
| Blind · older publication | Medium | Lock the bundle writer and keep the newer effective observation. |
| Blind · body transfer extends freshness | Medium | Take the local clock when the response headers arrive. Test a simulated 20-second body transfer. |
| Blind · displayed check and freshness clocks | Medium | The UI now shows each clock for rechecks and keeps the original display for historical provenance. |
| Blind · downloader service network | Medium | Use the default egress bridge without membership in the private Compose network. Drop capabilities and enable a read-only root filesystem. |
| Blind · portability of alarm | Low | The Linux container uses the process alarm. The bounded reader remains callable by mocked checks on Windows. |
| Blind · restart failure and bundle identity | Medium | The retained bundle hash now participates in Owner API configuration, so a subsequent ordinary launch picks up a changed receipt. |
| Blind · original generation could identify different bytes | Medium | Require the original digest, size and ETag whenever the original generation is reported. |
| Edge · native recheck exit on Windows PowerShell 7.2 | Medium | Check the Docker exit code explicitly before starting services. |
| Edge · XML decoder and ZIP fallback | Medium | Catch unknown XML encodings and reject unapproved ZIP compression before decoding. |
| Edge · concurrent recheck | Medium | The same nonblocking file lock and observation ordering protect the retained bundle. |
| Edge · wrong JourneyPatternRef version | Medium | A fixture with an unresolved asserted version now fails before equivalence. |
| Verification · running API reload and failed acquisition | Medium | A launcher check simulates active services and failure. The final API reads the retained proof, with the bundle hash included in the service configuration. |
| Verification · third independent reviewer | Low | The agent thread limit prevented dispatch. The coordinator ran the verification-gap lens and inspected the launcher, database, parser and browser assertions. |

## Verification

- Networkless Docker controls for route source and position coverage passed 60 tests. They covered same bytes, byte-distinct equivalent, same-count changes, partial coverage, transport and corrupt receipt rejection, fallback, and the 24-hour boundary.
- The isolated live Owner launcher accepted all seven dates using the original public generation and digest. The local check at `2026-11-20T03:18:08.537204Z` retained the HTTP response date `2026-11-20T03:14:38Z` and reported cache age `208` seconds. This receipt expires at `2026-11-21T03:14:38Z`. Ordinary launch consumed it offline and the API reference mount was read-only. The Test launcher rejected the switch.
- The broad private run before the review fixes passed 605 tests, with six gated submission-only skips. After the fixes, 83 targeted backend tests, including private HTTP and PostgreSQL, and all eight Edge cases passed. TypeScript/Vite built successfully. Both provenance clock displays were checked in Edge.
- The final isolated downloader reached Entur with one HEAD and wrote a tested bundle using the original bytes offline. Its mount and network checks, final API offline validation of the live receipt, and three byte-distinct variants built from the actual archive passed. No different live generation was available during this check.
