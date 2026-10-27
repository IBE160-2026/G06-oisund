---
title: '12.3 — Reconcile accepted current main and tablet entry'
type: chore
created: 2026-10-27
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: df840655ec0a9c9666b59d6fd4981e7f0ffc3585
main_target: 74849ff21bee108fe9cff93d740a96a6c6d2d7c5
story_key: 12-3-use-the-included-views-on-tablet-and-pc
technical_status: integrated-verified
owner_acceptance: pending
context: []
---

<frozen-after-approval reason="User explicitly authorizes main integration, necessary adaptation, verification, commits and push on the existing story branch">

## Intent

Update Story12.3 to work with current accepted main before further owner testing. Merge origin/main into its existing branch, preserve accepted remote transport and manual-feedback corrections, integrate12.3 themes/accessibility into every entry, and provide fresh isolated evidence and a current checklist.

## Boundaries & Constraints

**Always:** Work in D:/IBE160/tmp/story-12-3 on story/12-3-tablet-pc-accessibility. Merge full main74849ff21bee108fe9cff93d740a96a6c6d2d7c5; do not cherry-pick partial files. Preserve both histories.12.1/12.2 are done/accepted by Jonas;12.3 remains review/pending. Keep explicit relative /private-api priority/validation, HTTPS Secure cookies/logout marker, server Date/clock and no-store/CSRF/owner/retention contracts. Preserve accepted local feedback, readonly proposals, labelled conflict comparisons, original receipt recovery and activity terminology. Retain shared allowlisted theme only, theme across reset/reload/logout, IR-01 actual text/boundary/focus, negative measurement probes and meaningful enlargement/reflow. Add provider to dedicated private tablet entry. Preserve every historical evidence record; new results distinguish former runs and physical qualification.

**Never:** No merge of story into main, rebase/force-push, tunnel activation, DNS/access-policy changes, ordinary/pilot data mutation or12.4 expansion. Use only own project ibe160-story123-tests, ports15323/18323/18324 and a separately owned loopback tablet preview18483. Preserve all other current containers, preview15312 and manual plans. Do not read tunnel tokens. Root alone performs final full gates, local commits, session logging and authorized push.

## I/O & Edge-Case Matrix

| Scenario | Expected behavior / evidence |
|---|---|
| Dedicated tablet entry / reload / logout | Theme button actually changes presentation and persists only preference; private input remains protected, relative API wins over legacy configuration |
| Normal local build after inherited tablet env | Still targets own18324 API; no accidental /private-api without proxy |
| Demo save / conflict / lost acknowledgement | Accepted local feedback remains reachable, forms readable/readonly, labelled comparison and original lookup work; Night/reset semantics retained |
| Narrow/wide100/200% text and both themes | New feedback/comparison surfaces meet existing IR-01 checks; keyboard return/negative probes still pass |
| Current status / preserved runtime | Main acceptance not regressed;12.3 still review; other environments unchanged |

</frozen-after-approval>

## Code Map

- Main source delta from ce0669f is transport35c4548/ca1d647 plus accepted feedback8367121; other commits mostly docs/logs. Main is clean and equals fetched origin/main.
- frontend/src/tablet.tsx lacks ThemeProvider; main PrivateAccess adds validated VITE_PRIVATE_API_BASE and Secure marker. .dockerignore already permits src/**; deploy/tablet/index.html and Dockerfile retain a private-only build without demo/Vite multipage config.
- FictionalAssessment.tsx and fictional-assessment.css: combine main ComparisonFields/comparisonTime/announce/feedback/recovery/readonly and scoped comparison CSS with12.3 useTheme/ThemeControl/storage disclosure/reset retention.
- frontend/tests/fictional-assessment.spec.ts: retain main390/1440 feedback matrix and12.3 theme asset allowlist/reset expectations. tablet-pc.spec.ts has obsolete fault/activity labels; update selectors to accepted visible wording without weakening outcomes.
- frontend/tests/tablet-transport.spec.ts is hardcoded18481; own separate tablet config/build must use18483 and actual tablet.tsx. Add actual toggle/reload and invalid API-base checks where practical.
- scripts/verify-story123.py: clear inherited VITE_PRIVATE_API_BASE for standard build; extend hashed inputs to deploy/.dockerignore/tablet compose. Add isolated tablet build/browser/backend-transport modes reusing durable executor, preserving existing dist and runtime guards.
- .logs/jonas-oisund/issues.md, sprint-status.yaml: reconcile accepted main closures with12.3 technical E10-A4/E11-A4 closures; preserve existing other open issues and all histories. Root adds new session entry at finish.
- README.md, story12.3 planning copy, original specification, epic12 context, manual checklist and handoff contain stale pending12.1/12.2 assertions. Mark previous checkpoints historical; update active guidance, accepted statuses and new remote/build limitations. Do not rewrite old raw evidence or pretend the old physical pilot qualifies this version.

## Tasks & Acceptance

- [x] Merge origin/main without committing; resolve conflicts by integrating behavior, not taking whole product files. Resolve issues with main acceptance plus story improvements. Do not create/update session logs.
- [x] Adapt tablet provider, theme/feedback merge, accepted test selectors and environment isolation. Add focused regression for actual dedicated entry; preserve secure transport unchanged.
- [x] Provide reproducible separate tablet build/test and affected backend transport command, durable records, hash inputs and invalid-env checks. Small targeted self-tests only where changed behavior warrants.
- [x] Update current documentation and original spec/context to accepted main; preserve historical notes. Create docs/evidence/12-3-main-sync-handoff.md with concrete overlap/decisions and bounded verification notes. Root completes final results.

**Acceptance:** Given current main, when merged, then its full ancestry and accepted UI/transport remain with working12.3 theme on all entries. Given isolated environments, when updated/tested, then own build/API/browser run current sources and others stay unchanged. Given final handoff, when read, then12.1/12.2 accepted and12.3 pending are unambiguous, with fresh evidence and exact limitations.

## Implementation Notes

No unresolved product choice. Work is reversible except explicitly authorized Git push, which root performs last. User scope authorizes integration directly; no intermediate approval. Agent may merge/resolve/edit code, test tooling and current docs, but must not run full matrix or mutate other runtimes. Report conflict decisions and exact commands. Root verifies and commits.

## Spec Change Log

## Review Triage Log

## Verification

Root: own runtime up/build/verify/prepare, complete12.3 matrix+negative/theme probes; accepted demo regression plus affected access/retention/recovery/notice suites; own tablet build/browser with mocked transport and actual tablet entry; backend transport tests; generator/tooling self-tests if changed; dedicated gateway build/config checks where relevant. Final served asset/API/source audit and unchanged-other-container metadata. No new physical/Cloudflare acceptance inferred. Record failures, actual counts and hashes; no old pass relabelled as fresh.

### Review triage — 27 October 2026

All three layers reported before triage. Incoming main deployment code was compared with origin/main and is byte-identical; those inherited limitations do not undo owner acceptance or become new12.3 prerequisites.

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| B1 build settings | low / patch | Dist hashes distinguish different compiled bytes, but the actual API build settings are not explicit in records/identity. Record allowlisted effective settings so reproduction is direct. |
| B2 tablet type check | medium / patch | Standalone tablet-build invokes Vite without the ordinary TypeScript gate. Use the same checked build command with the dedicated config. |
| B3 failed tablet logout | medium / patch | Existing private-access covers failure on legacy API; dedicated relative API/theme test covers success only. Add failed logout/reload/check settlement to prove the merged boundary. |
| B4 complete storage assertion | low / patch | New dedicated privacy assertion omits Cache Storage and Service Workers. Add explicit empty assertions to bound its only-preference claim. |
| B5 extraction markers | false / reject | A missing/reordered marker yields empty/invalid source; the first successful API assertion throws ReferenceError/syntax failure. It cannot falsely pass all valid/invalid cases. Diagnostic marker assertions are cosmetic, not a demonstrated bad outcome. |
| B6 team preparation | low / defer | Unchanged main prep uses case-insensitive unbounded team regex, while gate requires bounded lower-case non-trailing-hyphen. Invalid operator input can create unusable policy; gate fails closed. |
| B7 email preparation | low / defer | Unchanged main prep permits non-ASCII lower-case email while gate rejects it. Invalid operator input can fail later startup. |
| B8 serial admission | medium / defer | Unchanged main HTTPServer serializes admissions; a cold/slow JWKS request occupies it until the existing3s timeout. Availability limitation, not a demonstrated authorization bypass. |
| B9 unknown-key refresh | medium / defer | Unchanged PyJWKClient can refresh for each unknown key. Bound retry behavior before ordinary deployment; external exploitability through Cloudflare admission has not been established. |
| B10 forwarded Access cookie | medium / defer | Unchanged nginx strips assertion header but forwards original Cookie. Application can receive outer Access cookie along with its session cookies. Minimize credentials across that boundary in separate transport work; no disclosure or bypass is claimed here. |
| E1 dual port fixture | medium / patch | Changed fixture hardcodes18483, but retained main config uses18481. Derive allowed origin from each configured base URL and run both configurations with the same dedicated build. |
| V1 dual port fixture | medium / patch | Independent duplicate verified by source/test config; retain this separate row and share E1 correction. |

E1/V1 share one root cause; other findings are separate. Root intentionally interrupted only its verified own launcher before changing source. The interrupted34-case attempt remains exit1 (`12-3-browser-20261027T185055155765Z-2e19f0f8.json`), not a completed pass. An already exited descendant made taskkill return1 while the owned root/tree were terminated; wrapper retained its interruption evidence.

All three original reviewers reinspected the bounded corrections. B1–B4 and E1/V1 are fixed; no concrete new findings. B5 remains rejected and B6–B10 remain separately deferred. Checked build, allowlisted configuration identity, both loopback ports, failure/reload/retry shielding and complete storage checks are retained. Root committed corrections as `8ca318b55b98eb34de54f29ecab038322e3ccab6` before final verification. The first restricted tablet startup remains exit1 (`12-3-tablet-browser-20261027T185700217739Z-6588456d.json`); its verified owned children were cleaned before successful escalated checks. This is not counted as a product pass.

### Final root verification

At8ca318b all final gates passed: checked standard/tablet builds; actual API/PostgreSQL74/74; accepted demo/fictitious assessment37/37; dedicated tablet5/5 on each18483/18481; backend transport14/14; complete12.3 matrix34/34 with negative probes and cross-tab clear; selected private regression86/86; Python tooling7/7 and Node2/2; current gateway image/config, access gate13/13 and120 rejected proxy variants plus valid/fail-closed cases. No skipped/flaky/unexpected browser case. Final additive manual preparation17/17 and runtime61/61;22 other containers and7 accepted15312 HTTP byte hashes unchanged. Original failed/interrupted commands and the first60/61 runtime audit are preserved and explained. See [current handoff](../../docs/evidence/12-3-main-sync-handoff.md) and its unique manifests. User instruction keeps both spec/story in review/in-review, owner_acceptance pending, despite technical completion; it explicitly authorizes this branch's push. No story-to-main merge or12.4 expansion.
