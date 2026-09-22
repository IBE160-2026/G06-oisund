# PRD input reconciliation

Compared `DESIGN.md`, `EXPERIENCE.md` and `.memlog.md` with [the approved PRD](../../prds/prd-IBE160-2026-09-21/prd.md). This is source reconciliation, not a reviewer gate or implementation verification. Explicit later user decisions take precedence.

## Retained coverage

- **PRD §§2–4, UJ-1/UJ-2:** mounted-tablet website, separate fictional PC assessment, preparation/driving/summary journey, actual physical bus versus vehicle duty, service date and direction remain explicit. The source pseudonym is preserved.
- **§6.1, FR-1–6:** private access and 14-day remembered sign-in without expiry interrupting active work; review/correction/confirmation; timetable ambiguity, failure and missing-stop fallback; actual bus entry; actual-trip selection and correction remain covered.
- **§6.2, FR-7–11:** actual movement rather than schedule governs progression, including passage without stopping and the 100-metre criterion. Uncertainty, supported diversion recovery, manual GPS-loss controls, ten-second non-return transitions, separate return-trip trigger and operational corrections remain covered.
- **§6.3–6.5, FR-12–20:** automatic Svipper retrieval, two-minute target, actual-trip relevance, provenance, unknown timestamps, version-specific seen state, disappearance/removal behavior, restricted chime, movement thresholds and timer cancellation are retained. Whole loaded-shift offline use and restart recovery preserve uncertainty; connectivity restoration does not imply successful synchronization.
- **§6.6–6.7, FR-21–25:** confirmed normal/aborted ending, cancellation, no ended-shift resumption, differentiated summary outcomes, manual uncertainty confirmation, private user-initiated PDF, seven-day cleanup and isolated repeatable simulation remain covered.
- **§7, NFR-1–4:** glanceability, large targets, non-color status cues, honest data states, anonymized published evidence and actual-device validation remain explicit. Source/device feasibility and architecture choices remain downstream; static compositions are not validation evidence. Optional support does not become MVP acceptance scope.

## Intentional overrides and additions

- FR-2's PDF-only import expands to PDF plus JPG/PNG, including photos/screenshots, with one confirmation flow.
- FR-7's at-stop previous/current/next becomes future-first stop-after-next/next/current, omitting previous. Current dominates at a stop; next dominates between stops. Four stops remain unadopted.
- User decisions add staged stop-warning/message timing, simultaneous short headings without rotation, persistent manual theme choice, manual-trip authority until completion and the GPS-outage countdown without changing its five-minute exception.
- Preparation expands to split parts within one day/summary and both revised-file/manual overtime entry. Accepted scope review protects performed/current work; partial uploads cannot imply removal.

## Dropped or insufficiently carried detail

**PRD §6.6, FR-22:** summary outcomes are retained, but the spines do not explicitly restate the completion predicates: passenger trip completes at registered final-stop arrival unless manually aborted; other activities require position and timing together, never scheduled end alone. These remain inherited requirements, not authorized removals. Carry them explicitly into the behavioral contract before finalization.

No other genuinely dropped qualitative/behavioral requirement identified. PRD §9 acceptance targets and §10 validation ownership remain source-owned rather than duplicated UX requirements.

Resolution: the completion predicates above are now explicit in EXPERIENCE.md, Between-activity transitions, including preservation of manual evidence and uncertain completion.
