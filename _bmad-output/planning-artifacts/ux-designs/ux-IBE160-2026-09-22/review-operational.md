# Operational UX validation

Reviewed 22 September 2026 against the current DESIGN.md, EXPERIENCE.md, latest memlog decisions and accepted 43-screen `mockups/remaining-screens.html`. Latest explicit user decisions govern. This is a document/visual-contract review, not an implemented-system test. Other review findings were not consulted.

## O1 — High — A revision has a file scope but no explicit plan owner

- **Location:** EXPERIENCE.md:155–161, “Split shifts and revisions during the day”; :339, separate own/linked plans. Accepted gallery `#mentor-driver-instructor` and `#instructor-day`.
- **Trigger:** The instructor has an own shift plus person A and B loaded and imports a partial revision for A. A trip has the same date, route, direction and departure in more than one retained plan, or a revision changes a trip referenced by two accompaniment blocks.
- **Consequence:** The documented matching keys do not identify which plan may change. A plausible implementation can reconcile into the active/own plan, detach a later accompaniment block, or treat another person's records as duplicate activities. The ordinary single-plan reconciliation rule does not specify this multi-plan boundary.
- **Concrete fix:** Before file scope/matching, name the target own or linked plan and retain that target throughout preview and confirmation. Match only inside it. Show affected accompaniment links when an accepted revision removes/changes their referenced trip/portion; retain unresolved links for explicit repair rather than silently selecting replacement work. Preserve active trip/manual evidence and all other plans. This extends the existing separate-record and explicit-review rules, not the ability to share records.
- **Needs user choice:** **No** for target-scoped review and preserving unresolved links; derive these from approved separate plans and non-destructive revision requirements.

## O2 — High — Restart recovery omits the role that determines whether controls are restricted

- **Location:** EXPERIENCE.md:123, whole-active-shift recovery; :225–227, preserved outage timer; :346–348, acute takeover. Accepted gallery `#fadder-takeover` and `#fadder-acute-driving`.
- **Trigger:** A fadder presses `Jeg kjører`, then the browser restarts offline before or during the unplanned takeover. The original assignment still says FADDER and the active trip still belongs to the accompanied person's plan.
- **Consequence:** Recovery explicitly lists bus/trip/corrections/seen state, but does not say to restore the current operational role, actual driver-change event, own/linked plan identity and accompaniment block. Rebuilding the view from the assignment label can reopen unrestricted mentor controls even though no explicit return to guiding occurred. Preserving the GPS timer alone does not prevent that error.
- **Concrete fix:** Extend recovery to persist and restore current driver/guiding role, assignment role, plan/block identity, active trip pin and actual takeover/return events together. A recovered acute takeover remains FØRER until explicit permitted return; a preserved GPS outage does not become a fresh startup exception. Show last-confirmed context when recovery is incomplete rather than deriving an unrestricted role from FADDER/INSTRUKTØR in the plan. Keep the already approved five-minute and genuine first-start exceptions unchanged.
- **Needs user choice:** **No**; this is required by existing “explicit return only”, preserved recovery and timer rules.

## O3 — Medium — A pinned trip has no stated precedence at an explicitly ended partial accompaniment

- **Location:** EXPERIENCE.md:202, manual selection until actual completion; :339–341, limited accompaniment and person change. Accepted gallery `#instructor-select`, `#mentor-instructor-controls`, `#instructor-day`.
- **Trigger:** The instructor manually selects a trip, accompanies only part of it and explicitly ends that block before its final stop. Later the instructor returns to the same person in a different block. The gallery explicitly permits partial-trip accompaniment, while its selector says the selected trip remains until finished.
- **Consequence:** It is unclear whether the old pin prevents leaving the block, continues tracking the unaccompanied remainder, or becomes active again when the same person is relinked. Merely preventing the previous *other person's* pin from transferring does not resolve return to the same person. It can also falsely complete a trip whose remainder was not observed.
- **Concrete fix:** Scope the active manual pin to the active tracking context. An explicit confirmed block/person/activity change exits that context without declaring the unfinished passenger trip complete or aborted. Preserve historical correction evidence, but establish the actual trip afresh when entering a later block—even for the same person. Time/proximity alone must still never release a pin within an unchanged active block. Spell this precedence out next to the pin rule and the accompaniment-boundary rule.
- **Needs user choice:** **No** for this reconciliation of accepted partial-trip scope and explicit context changes. If a different cross-block pin behavior is wanted, that would require a new decision.

## O4 — High — Linked-plan retention and export remain a user-visible unresolved contract

- **Location:** EXPERIENCE.md:266–268, privacy/retention; :339, linked full plans; :359 and :380, acknowledged entitlement/lifecycle/export deferral. Accepted gallery `#mentor-driver-instructor`, `#instructor-select` and `#pdf`.
- **Trigger:** An instructor imports a person's whole shift but accompanies one portion; their own working day ends earlier/later than that person's shift, then exports the instructor's daily summary or reopens it six days later.
- **Consequence:** “Delete all shift-associated data seven days after completion” has multiple possible completion owners. The UX does not establish which expiry the instructor sees, whether an imported linked copy is retained with the instructor's assignment, or whether a PDF contains only accompanied evidence versus the entire other person's day. The docs explicitly defer this, so a final handoff cannot yet promise a clear deletion date/export scope for mentor records. No shared-account access should be inferred from upload.
- **Concrete fix:** Define the user-visible lifecycle and export boundary for the mentor's imported copies and observed evidence; state the controlling expiry and show it in mentor retained-summary/export UI. Keep own activities, observed accompaniment and acute-takeover events distinct; do not present unobserved parts as performed work. Clarify whether these are private imported copies only or any cross-account record links before defining access behavior. Architecture can implement the resulting rule but cannot choose the product scope implicitly.
- **Needs user choice:** **Yes**, a narrow choice about imported linked-record scope/expiry and mentor export scope if not settled elsewhere. The currently supplied decisions do not settle it. Do not ask again about the already decided seven-day duration.

## Boundaries that are sufficiently clear

- FADDER full-single-person accompaniment and INSTRUKTØR multi-block/person/classroom/office ownership are separated; planned own trips are not copied from linked plans.
- Acute takeover immediately applies driver restrictions and retains current linked progress. Returning to guiding is explicit; scheduled time is not a role change.
- Notice acknowledgement is per version, retained across restart, distinct from seen/resolved state and individual when two notices are present. Planned stop clearing and route-wide acute lifecycle are distinguished.
- GPS loss retains the approved five-minute exception/countdown, reliable recovery restores speed rules, and an established timer does not restart on view/restart.
- The public fictional demo is explicitly isolated from operational records and exported evidence. No authentication requirement has been reintroduced for it.

**Result:** 4 findings: 3 high, 1 medium. O1–O3 can be resolved by making existing decisions operationally explicit. O4 needs the stated product boundary resolved before claiming the mentor lifecycle/export contract complete.
