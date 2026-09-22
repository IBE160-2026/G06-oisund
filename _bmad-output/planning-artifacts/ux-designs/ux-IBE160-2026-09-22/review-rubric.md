# Spine Pair Review — IBE160

## Overall verdict

The spines preserve the established driver workflow and recent mentor-role corrections, with source journeys, concrete tokens and all five accepted visual references available to downstream consumers. Before final handoff, resolve the explicitly open linked-plan lifecycle contract and reconcile the few internal catalog/state conflicts below. Static acceptance is not device validation; deferred browser, sensing and mounted-device tests are not defects in this review.

Reviewed DESIGN.md, EXPERIENCE.md, the five accepted mockups, current memlog decisions, source extraction/coverage and reconciliation material, and the PRD journey/requirement headings. Historical working mock candidates do not govern this review.

## 1. Flow coverage — adequate

The exact source journeys UJ-1 and UJ-2 retain protagonists, numbered steps, climax and failure paths. FR-1–25 are represented across those flows and their linked behavior sections; NFR-1–4 have applicable usability, trust, privacy and environment treatment. Split work and the added UJ-3/UJ-4 address the latest own-plan/accompanied-plan decisions. Public demo without sign-in and current stop roles correctly supersede older source decisions.

### Findings

- **R1 — high — Operational linked-plan lifecycle is still a product-contract gap.** EXPERIENCE.md:266, 268, 359 and 380 explicitly defer mentor entitlements, linked-record lifecycle and export scope, while UJ-3/UJ-4 already require importing several separately confirmed persons' shifts. A consumer cannot determine which day starts deletion for each linked plan, whether ending the mentor's day affects a linked record, or what accompanied outcomes may enter the mentor's PDF. The existing single-day seven-day rule does not answer those ownership questions. *Fix:* commit a minimal UX contract for user-uploaded linked copies versus shared live records, independent end/retention boundaries and mentor-summary/export content. Preserve the existing seven-day limit and record separation; do not infer new shared access. **User/product decision needed** for any actual sharing/access or lifecycle choice not established by the upload model; storage/authentication mechanisms remain downstream.

## 2. Token completeness — adequate

Every inspected `{colors...}`, `{typography...}`, `{rounded...}`, `{spacing...}` and `{components...}` reference resolves against DESIGN frontmatter, including EXPERIENCE references. Color tokens have concrete hex values and appropriate day/night counterparts; typography and component dimensions have usable values. Document/reference sizing is explicitly separated from responsive requirements.

### Findings

- **R2 — medium — Contrast measurements are supplied without a committed acceptance floor.** DESIGN.md:278–284 reports several existing pair ratios and requires high contrast, but does not state a minimum for newly combined text, changed-notice emphasis, focus states and control boundaries. EXPERIENCE Accessibility Floor likewise has no numeric contrast target. The numerical examples alone do not constrain a consumer implementing additional states. *Fix:* add explicit text and non-text contrast targets as implementation acceptance criteria, including checks for each semantic foreground and both themes. This is a documentary accessibility default, not a claim that the complete interface or mounted viewing has passed. **No user decision needed** to make the existing high-contrast requirement testable.

## 3. Component coverage — adequate

Visual and behavioral catalogs cover access, import, trip/stop progression, notices, activity transitions, theme, summary/export and mentor extensions. Rows contain actual constraints rather than labels alone.

### Findings

- **R3 — low — One paired component name differs.** DESIGN.md:343 names `Stop Menu controls`; EXPERIENCE.md:95 names `Stop correction controls`. These are the same arbitrary-selection/GPS previous-next component but fail the advertised identical-name contract. *Fix:* use `Stop correction controls` consistently in both catalogs and references. **No user decision needed.**

## 4. State coverage — adequate

The IA destinations have state coverage in the main state table, operational-role table, recovery defaults and explicit movement policy. Offline is separated from GPS failure, uncertainty from confirmed progress, temporary takeover from planned own driving, and demonstration from operational state. Missing capability cannot manufacture progress. Authentication-copy and responsive/sensor verification are openly deferred rather than falsely asserted complete.

### Findings

- **R4 — medium — Ended-summary permissions contradict manual completion confirmation.** EXPERIENCE.md:190 says an ended combined day has a `read/export-only summary`; lines 165 and 296 require manual confirmation of uncertain activities in that summary, which follows end confirmation. Lines 52 and 298 separately apply read/export-only to reopened retained summaries. A consumer can reasonably disable the very confirmation required immediately after ending, or allow it indefinitely. *Fix:* explicitly distinguish initial post-end review from later retained-summary access, and state when manual evidence confirmation is available. Keep the shift ended and retention unchanged in either case. The existing initial-review versus reopened-summary distinction supplies a conservative resolution; **no new user choice is needed unless corrections after reopening are proposed**.

## 5. Visual reference coverage — adequate

All five files under mockups/ are linked from both spines at relevant sections: driving, preparation, shift updates, summary/recovery and the consolidated 43-screen gallery. No accepted mock orphan was found. DESIGN states spines win on conflicts. The gallery distinguishes landscape tablet, PC demonstration and portrait PDF, and keeps simulated labels. The final button/blue-rail corrections are present.

### Findings

- **R5 — medium — Primary accepted driving/recovery references omit the now-required persistent clock.** DESIGN.md:328 and EXPERIENCE.md:78 prescribe a top-right clock on tablet screens including driving. The consolidated gallery includes it, but mockups/driving.html headers (for example lines 32, 47 and 112) and the active-driving frames of mockups/summary-recovery.html still have no clock. A consumer lifting the original driving reference will omit a user-approved feature. *Fix:* add the same clock treatment to the accepted driving and degraded-data frames, then verify it fits beside route/destination and state labels; keep the simulated time explicit. **No user decision needed** because persistence was already accepted.

## 6. Bloat & overspecification — adequate

Token recipes are useful extraction from accepted visual references; explicit separation of mock framing from responsive requirements prevents accidental fixed-size implementation. Source FRs are inherited rather than copied wholesale. Some staged-notice, movement and acceptance explanations repeat across sections, but they do not introduce a separate load-bearing error. Consolidate these during the planned prose pass without removing the exact exceptions.

## 7. Inheritance discipline — adequate

All five frontmatter source paths resolve. UJ-1/UJ-2 names match the source. Own versus accompanied plans, FADDER versus INSTRUKTØR, no-login demonstration, stationary notice access, GPS five-minute access and persistent manual theme match the current decisions. Token references resolve. R3 is the component-name mismatch.

### Findings

- **R6 — medium — Superseded open-state markers contradict settled defaults.** DESIGN.md:304 says sequence-boundary empty positions remain open, whereas EXPERIENCE's final defaults prescribe an em dash with explicit boundary labels. EXPERIENCE.md:124 says layover presentation still needs definition despite the accepted Reguleringstid transition and gallery; line 127 leaves retained-summary access open despite the main-menu entry being specified at lines 52 and 298; line 125 leaves unsupported Auto fallback open despite the preservation default at the end of the document. *Fix:* replace these stale markers with references to the current decisions/defaults and leave only genuinely unresolved trigger/capability details open. Avoid sending already settled questions back to the user. **No user decision needed.**

## 8. Shape fit — strong

DESIGN follows the canonical section order. EXPERIENCE includes Foundation, IA, Voice and Tone, Component Patterns, State Patterns, Interaction Primitives, Accessibility Floor and Key Flows. Responsive & Platform and Inspiration & Anti-patterns are present where applicable. Information Trust/Privacy/Retention and the role sections earn their place through operational requirements; the remaining-verification list distinguishes future evidence from current visual acceptance.

## Mechanical notes

- Severity counts: critical 0; high 1; medium 4; low 1.
- No unresolved token reference or broken listed source path found.
- Component catalogs differ only in the stop-control name identified in R3.
- All five accepted mockups are referenced; historical `.working` candidates were excluded.
- No Mermaid syntax is used in the spine pair.
- This is document-contract validation, not implemented-product testing, live-source verification or proof of mounted-device accessibility.
