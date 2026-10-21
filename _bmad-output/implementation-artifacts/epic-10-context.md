# Epic 10 Context: Review and Confirm a Supported Shift

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Let the driver import a qualified text PDF into a private, unconfirmed draft, inspect uncertainty, correct the activities, explicitly confirm the reviewed plan, enter the actual bus and read a chronological day. This is preparation and consultation while stopped; planned information never establishes observed location or completed work. The approved Course V1 scope governs; archived automatic driving, offline, mentor and export plans are historical.

## Stories

- Story 10.1: Review a text PDF
- Story 10.2: Correct the draft
- Story 10.3: Confirm the reviewed plan
- Story 10.4: Record the physical bus
- Story 10.5: Read the day

## Requirements & Constraints

- **Fixture extension, 2026-10-21:** Examples 8 and 9 were added during testing of story 10.1; see the [extended fasit](../../Eksempelfiler/README.md). Their 31 additional source rows were independently transcribed and approved by Jonas on 2026-10-21; see the [dated handoff](../../docs/evidence/10-1-additional-fixtures.md). The original seven-fixture test results do not qualify these additions. Preserve example 8 duty changes, owner-clarified CAR - 1 through CAR - 4 pilot-car codes (handover row and pilot-car return on deadhead 76567), final rather than intermediate Wi-To endpoints and notes-only second page. Preserve the distinction between PDF location Wi-To and the owner-supplied explanation of the Sentrum regulation point; do not derive a bus or ordinary realtime suffix from CAR. Preserve example 9 Fadder/Instruktør and Coffee without inventing trips, duty, bus, Sign-off or mentor features. Review source facts/unknown mappings before qualifying these inputs.

- Import remains unconfirmed until explicit human review. Preserve page/field uncertainty, unknown codes and source order/provenance; do not discard unreadable pages or invent missing activities, locations, transfers or classifications. Unsupported/scanned input offers manual entry without claiming successful extraction. Cancellation/failure leaves saved and confirmed work unchanged; another import creates a separate draft.
- The accepted qualification covers seven anonymized PDFs and ten pages: examples 1–5 and 7 support automatic extraction of the checked source facts; example 6 remains partial. Its Travel to row does not provide the owner's completed start, endpoints and deadhead classification. Keep that assistance distinct from extraction and never apply its interpretation to unrelated Travel to rows. Other layouts, OCR, DST import behavior, extended header clocks and intermediate-stop completeness are unqualified.
- Vogn is vehicle duty, separate from physical bus. Preserve the full duty and its final three-character realtime-screen value, including leading zeros. Actual bus is absent from all fixtures and stays unknown until manual entry. A changed duty does not prove a bus change. Preserve bus identifier formatting and activity identity through corrections.
- Preserve source pause rows even when contiguous intervals are grouped. A group containing MealBreak is matpause; Coffee alone is kaffepause; Split break is deltskiftpause. Separated intervals remain separate. Reporting/header end may differ from the final explicit activity: owner-explained paid free time must not become an invented extracted row.
- Service date and explicit Europe/Oslo calendar dates/times are distinct. Preserve overnight dates, source clocks and extended-hour meaning; never derive dates solely from descending clocks. Keep separate work periods and known reporting locations without inventing later depots or gap activities. Unknown nonessential facts remain visible.
- Confirmation requires service date, ordered activities, explicit times establishing planned final end, and resolved required trip/type facts. Unknown source types require correction or explicit classification. Show the reviewed version and fixed expiry before confirmation; duplicate clicks cannot create multiple plans or silently replace an existing day. Plan structure freezes on activation.
- Retain interpreted facts, corrections and uncertainty only. Original/processing copies and previews are transient; clean success, failure, cancellation and interrupted work. No raw-text archives, private payload logs, persistent browser store or operational repository fixtures. Private responses use no-store. Draft retention is creation + seven days; confirmation fixes planned-final-end + seven days. Access/retry never extends retention.

## Technical Decisions

- Use React/TypeScript, FastAPI and PostgreSQL with backend authority for saved private records and browser memory for unsaved edits. PDF interpretation stays behind a bounded adapter, with content validation and explicit unsupported/error results; do not introduce deferred transit/GPS/OCR integrations.
- Import drafts need stable owner-scoped identity/revision, creation/expiry, service/calendar dates, ordered typed activities, field/page uncertainty and corrections. Activity identity is independent of line/trip number; source order distinguishes repeated identifiers. Keep extracted, derived, owner-assisted, manual and unresolved facts distinguishable.
- Every private operation enforces server-derived owner, valid session and retention. Mutations check expected revision transactionally. Creation/confirmation use stable operation IDs; identical retries return the accepted result and changed payloads conflict. Authorize and check expiry before replay. Operation metadata expires with its private data.
- Failed saves preserve current form input. Stale writes expose conflict for comparison/reload without force overwrite. A lost response stays unresolved until authorized lookup or the same retry settles it. Never display saved status for an HTML/login/error response. No expired/deleted record may be recreated by a late request.
- Preserve existing private authentication, CSRF/origin protections, logout/session-expiry clearing, isolated fictional assessment and additive migrations. Tests use disposable fictional storage, never ordinary private records.

## UX & Interaction Patterns

Show source preview beside interpreted fields when space allows, stacked in reading order on narrow screens. Preview lasts only for the current selection; reopening may require selecting the source again. Distinguish source, corrected and unresolved values with text/symbols. Provide labelled unsupported, processing, cancellation and save/error states without a completeness claim. Use ordinary Oslo date/time controls and explicit overnight dates rather than requiring UTC offsets.

The overview is one chronological list with clear reporting time, dates, known parts/gaps and a separate unassigned/manual physical bus field. Keep duty and bus visibly distinct. Use readable Norwegian labels, wrapping long names, labelled touch controls, keyboard focus and manual Day/Night. Informative text requires 4.5:1 contrast; necessary non-text 3:1; focus needs a 2 CSS-pixel-perimeter-equivalent area and applicable 3:1 contrast. Actual rendered states require verification; historical mock acceptance is not implementation evidence.

## Cross-Story Dependencies

Story 10.1 depends on the accepted 9.1 qualification and 9.4 private draft persistence. Build on their bounded import envelope and authorized save/reopen, fixed expiry, stable revisions, replay handling and friendly time-entry contracts. Qualification is evidence for extraction, not acceptance of application import.

Story 10.2 builds correction on imported/private drafts; 10.3 confirms the corrected revision; 10.4 assigns actual bus after confirmation; 10.5 combines the confirmed plan and bus into the day overview. Later activity navigation, outcomes, notices, terminal closure and whole-flow verification consume these contracts, but are not prerequisites or substitutes for acceptance of this epic.
