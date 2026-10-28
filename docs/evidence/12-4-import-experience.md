# Story12.4: owner-directed shift preparation correction

## Owner result and scope

On28October2026 Jonas confirmed all six guided physical Lenovo/Brave tests passed, including logout, empty secondary account and reopening the primary account's saved terminal plan and notice. He explicitly **did not approve Story12.4**. These checks qualify the earlier implementation `5ca3f7df73f4cf49f5244dbc97a0a3ebb8de9891`, not the subsequent correction.

The requested correction belongs to12.4: remove repeated compulsory document-detail review, allow a correct import to continue without editing, require an explicit choice to correct/add information, provide dedicated adjacent bus-save actions, and preserve the working position after saving an edited draft. The owner accepted either a separate approval page or a direct route to approval; the implementation specification chooses the separate view.

[Follow-up specification](../../_bmad-output/implementation-artifacts/spec-12-4-import-experience.md) records behavior and invariants. [Original handoff](12-4-handoff.md) and [physical report](12-4-device-testing-2026-10-28.md) retain their original source/build/test limits. Prior passing counts are not new executions of this correction.

## Isolation and qualification

Work continues in `D:/IBE160/tmp/story-12-4` on `story/12-4-complete-user-flow`, from follow-up baseline `c884ade743edcc3739086703748ac22d45d2a695`. Use only compose project `ibe160-story124-tests`, frontend15324, fictional API18325 and private API18326. Automated regression accounts are separate from the two physical/manual test accounts. No private original PDF, operational data, active gateway or tunnel is part of the correction.

The following checkpoints retain their original source limits. Later results below supersede earlier in-progress statements; none grants owner acceptance.

## Executed development checkpoints

These checkpoints precede review corrections; they do not qualify a later source snapshot.

| Record | Actual result | Qualification |
|---|---|---|
| `12-4-build-20261028T134152720164Z-0425fa6c.json`, `12-4-build-20261028T134357031444Z-a464e0f8.json` | Build passed | Implementation-agent builds; local browser attempt was denied by Docker sandbox guard before tests launched. Local stop-preview was also denied Get-CimInstance. Root subsequently ran both with the necessary elevated tooling. |
| `12-4-browser-20261028T134545577922Z-bb35d137.json` | First new direct-flow test failed; four did not run; gate2 | Direct save did not display review. Source selectors also changed across this first gate, so it is explicitly unqualified. Corrected waiting for parent save to become clean and effect ordering (invalidate epoch before beginning review). |
| `12-4-browser-20261028T134732462277Z-3f43ed26.json` | 5/5 passed,38.8seconds; stable source/build/API identity | Actual API/PostgreSQL: direct summary/approval at768/1440, independently authored synthetic A oracle, explicit unchecked unknowns, confirmed bus independence, correction/position/bus scope/time save, failed direct-save recovery and invalidated review. Screenshots were visually inspected by root. This still precedes subsequent review corrections. |
| `12-4-browser-20261028T134921459395Z-68b5099b.json` | Deliberately interrupted; exit1; no final browser summary | Selected326 cases, reached logged case57 when review established changes were necessary. Stopped only verified own npx PID14092/tree (matching parent45796, exact command and creation time14:49:26). Source and executed inputs were unchanged until collection. Never report326 passed or infer all begun cases passed. Original log/bundle retained. |

All records and byte-preserving per-entry archive indexes are in this directory and `12-4-bundles/`. The original successful five-case build used `main-BRCwnSA6.js`. Review identified further presentation and verification gaps, individually triaged in the follow-up spec. Re-derivation preserves the working behavior while adding compact in-flight save/recovery, stable disclosure/time focus, unchanged-bus refusal, notice-to-approval navigation and stronger actual integration tests. Post-review verification remains pending at this checkpoint.

## Review corrections and focused final-source verification

Both rounds used three independent reviewers (blind/edge/verification), launched before results were handled. Every finding, including rejected findings and evidence, is retained in the specification. The second edge and verification reviewers reported no further findings/gaps. Retained second-round patches prevent overlapping same-version review requests, keep classification-specific source/time/place context visible, bind terminal failures to the actual create/update target, derive current bus-scope feedback, restore focus when an occurrence selector disappears, cover failed operation admission and expose source dates/places for overnight import identity.

| Final-source record | Actual result | Expected versus observed |
|---|---|---|
| `12-4-browser-20261028T141350083644Z-01e4534d.json` | 21 passed,2 failed,0 skipped/flaky;170.97seconds | Selected18 new cases plus5 existing independent synthetic A–E imports. Two new assertions incorrectly demanded zero-padded nb-NO dates and explicit zero seconds; rendered dates and saved minute-precision timestamps were semantically correct. Product behavior/focus assertions otherwise passed up to those assertions. The failed result is retained. |
| `12-4-browser-20261028T141728244776Z-3872dba1.json` | 2 passed,0 skipped/flaky;17.31seconds | The two affected cases reran fully. Date assertions independently require8/9February2030 and23:50/00:10 with only optional leading zeros; occurrence assertion independently anchors first Oslo occurrence `2030-10-27T02:30+02:00`, accepting only optional zero seconds. |
| `12-4-build-20261028T141842488213Z-626354e3.json` | TypeScript/Vite build passed | Final desktop product asset `main-DbTshW9R.js`, freshly configured for actual APIs18325/18326. |

The two browser records have unchanged source/executed inputs, matching build/current source and expected API settings. Root compared every frontend/backend product-source hash between them: identical. This is21 unchanged passing cases plus2 corrected passing cases, **not** a claimed single23/23 run. No product code changed for formatting corrections. The final326-case affected regression is running separately and is not yet claimed passed here. Backend implementation and transport/session authority were not changed by this follow-up.

| Follow-up scenario | Executed targeted coverage |
|---|---|
| Correct import without editing | Two widths, no draft before explicit action, independent A facts, untouched unknown acknowledgements and separate compact approval; prior-selected A followed by C creates a new identity and preserves A. |
| Corrected import | Explicit correction, preserved original facts in existing A–E cases, retained viewport/focus after save, first-save open source disclosure and resolved-time save, direct access to current-revision approval. |
| Minimal approval | Optional full facts; visible required classification context; stale saved revision before review and before confirmation cannot create work; held review request is deduplicated; notice-list navigation returns to visible decisions. |
| Draft bus | First draft requires explicit whole-draft save; clean saved draft supports independent bus change; unchanged bus action disabled; unrelated content and dirty time refuse bus-only persistence and retain proposals. |
| Confirmed bus | Actual independent bus endpoint shows value/revision1 after save; reload/reopen retains it; source draft is unchanged. |
| Failure and recovery | Unsent POST, accepted/lost POST, failed operation admission and terminal fresh-create failure; compact proposals retained, original operation explicitly reconciled, no duplicate draft/effect or prior-draft overwrite. |
| Time/viewport | Tablet viewport retains first-save source disclosure and replacement time-input focus; disappearing DST occurrence selector falls back within the same activity/time field, with unchanged scroll and exact first Oslo offset. |

These are automated desktop-browser tests, including viewport emulation, against actual APIs/PostgreSQL. Controlled transport failures and delayed responses are labelled test injections; successful operations still reach the actual service. They are not new physical device or personal acceptance tests. Existing mobile boundary checks use intentional API doubles; final-source mobile verification follows the broader regression.

Root visually inspected the development screenshots: [compact import768](12-4-import-experience-import-768.png), [approval768](12-4-import-experience-approval-768.png), [saving a second document](12-4-import-experience-saving.png), [retained save position](12-4-import-experience-saved-position.png). Their current copied-run identity is recorded in the final checkpoint below. Original bytes also remain in each run's verified archive.

## Broad regression and final narrow corrections

`12-4-browser-20261028T141845088376Z-a0cfe7e7.json` completed with **317 passed,5 failed,4 not run**,35.4minutes, exit1 and stable source/inputs. It was not326/326. Preliminary chat updates based on log tails missed earlier failures; these final counts supersede those updates.

Two keyboard import cases used an unscoped text locator that became ambiguous when save feedback was intentionally repeated next to the bus action. The corrected locator targets the authoritative `Lagringsstatus` status region, preserving unknown-save/recovery assertions. A503 fixture expected a parser error; it now checks the existing service-unavailable category, unchanged input/focus and retained error on return, and excludes parser/adoption success. Product error mapping was unchanged.

Both768px themes also failed the existing planned-start placement bound:480.56px against <450px. The first hypothesis that the new approval navigation wrapped was disproved by the trace: consultation already hides that navigation. A read-only comparison with historical `c884ade` showed the same top notice-entry placement; no baseline runtime rerun is claimed. The minimal correction moves the same notice-reader button below activity facts only during consultation, retaining its ref, access guards and ordinary day placement. No geometry, contrast, enlargement or focus threshold was loosened.

The exact-five rerun `12-4-browser-20261028T145858001741Z-047aa4e1.json` passed the three import/error cases and still failed both geometry cases. After the proven placement correction, `12-4-browser-20261028T150418027996Z-d11be58e.json` passed both themes; build `80bf4be6` passed. Final product asset is `main-BRJ12oLt.js`. The earlier317 passing cases qualify their earlier captured snapshot; final affected-suite qualification is recorded separately below.

## Final affected-source qualification and access

| Record | Actual result | Scope |
|---|---|---|
| `12-4-browser-20261028T150525812602Z-427d7a87.json` | **64/64 passed**,0 skipped/flaky/unexpected;523.77seconds | Full affected import and selected-activity suites, all18 new preparation cases and both complete actual API/PostgreSQL journeys. Includes all five prior failures and four previously unrun geometry cases. |
| `12-4-tablet-browser-20261028T151438853623Z-f3e6ccfa.json` | **32/32 passed**,0 skipped/flaky/unexpected;39.7seconds | Fresh mobile byte/access/error/session boundaries with intentional API doubles; not a physical-device test and not a substitute for the actual integration journeys. |
| `12-4-build-20261028T151533859483Z-f92bb74f.json` | TypeScript/Vite build passed; preview36388 ready | Fresh desktop build `main-BRJ12oLt.js`, SHA256 `86df9a48bc01673b421f5f925ac6335793468a966e54df19ff93cdb88ea784b3`, actual APIs18325/18326. |

Both final browser gates prove stable source/executed inputs, tested build matching current source and expected API configuration. Product source is unchanged between the final64-case and32-case executions and the served build. The64 is a distinct final affected gate, not a relabelled326/326 broad run; the earlier317/5/4 record remains intact. Backend implementation was unchanged and its earlier455/74 results were not rerun for this UI correction.

Root copied and visually inspected the four linked screenshots from the final64/64 record, preserving exact bytes: compact summary/approval at768px, compact second-document saving and retained editing/save position. Measurements for the full affected geometry suite are archived with that run; thresholds remain unchanged.

Environment: Windows, Node24.19.0, host Python3.12.10, Playwright1.64.1, actually loaded Edge156.0.4314.50, Docker29.7.2 and Compose5.5.1. The owned-browser loaded-module observation is in `12-4-import-experience-environment.json`; runtime/API/PostgreSQL identity is recorded by the final served audit. These are desktop tests and viewport emulation. The earlier physical Lenovo results remain historical; the new UI has no new owner/device acceptance. USB connectivity was checked28October at15:54 local, with existing reverse ports15324/18325/18326 and no cloudflared process; this is connectivity evidence only.

The isolated preview is `http://127.0.0.1:15324/private` on the PC and the connected tablet through the existing USB reverse. Reload to replace the old in-memory app. It is separate from the active website/gateway18081; no tunnel, deployment or operational-data change was made. A fresh dedicated synthetic manual account was additively provisioned for the four-point retest. Its credentials exist only in ignored `.private-runtime/story124-experience-manual.json`; no login was submitted and both prior manual/device accounts and records remain untouched. Do not publish credentials or reuse automated regression accounts for owner acceptance.

## Focused owner retest after technical verification

1. Import synthetic A. Before an explicit save action, there must be no new saved draft. Choose the correct-as-is action; reach approval directly, without a mandatory editor or full repeated document list. Inspect required unknown decisions and optionally open the full details.
2. Import a separate synthetic document and explicitly choose correction/addition. Change a destination and save from that working position. The saved message must be nearby; saving must not return to the page top. Reach approval directly and check that corrected and source facts remain distinguishable.
3. Use the dedicated bus-save action in a draft and on an open confirmed day. Confirm its scope is clear, saved value survives reopening, unrelated edits cannot be silently saved/lost, and ended work remains read-only.
4. Assess the overall number of steps and scrolling on the physical tablet, then explicitly approve or reject Story12.4. Passing individual automated or manual checks is not approval.

## Committed-source runtime audit

Product/tests/specification/evidence commit: `5ee35ef` (`fix: streamline story12.4 shift preparation and approval`). Final test records captured the preceding HEAD9be6278 plus exact uncommitted source hashes; all98 frontend/backend product hashes were checked against this committed source and are identical across the final64-case gate,32-case gate and served build. Subsequent documentation/log commits do not change those product bytes.

`12-4-runtime-20261028T151727047995Z.json` passed all38 checks after the product commit: exact served frontend bytes/API settings/current source, both API containers' mounted backend bytes and restart ordering, health, unauthenticated401/no-store and preservation of all23 pre-existing container IDs/images/ports. Runtime PostgreSQL17.11 and API Python3.13.16 are recorded with dependency versions. Preview15324 remains available; no active-site deployment or tunnel was started.

Technical correction is review-ready. No retained technical finding remains open; the owner-directed four-point retest and explicit acceptance decision remain pending. Story12.4 stays in review/explicitly-not-approved and12.5 remains backlog.
