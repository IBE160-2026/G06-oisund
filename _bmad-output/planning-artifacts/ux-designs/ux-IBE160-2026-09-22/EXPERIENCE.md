---
name: IBE160 — Experience Spine
status: approved
decision: SCOPE-02
updated: 2026-10-25
---

# Experience Spine — Course V1

## Authority and purpose

[Approved SCOPE-02](../../sprint-change-proposal-2026-10-19.md) and the [current PRD](../../prds/prd-IBE160-2026-09-21/prd.md) replace the old automatic driving/offline/mentor experience. [DESIGN](DESIGN.md) governs appearance. The original 43-screen gallery remains a historical/future reference, not active V1 coverage. The [mockup index](mockups/README.md) identifies reusable preparation compositions.

V1 supports preparation and consultation while stopped. It neither measures movement nor certifies standstill. No interaction is required while driving. Planned and manually selected information must not look GPS-confirmed.

## Information architecture and flows

**Owner clarification, 2026-10-24 (11.2):** Upload, interpretation control/editing, confirmed day and selected activity are separate screens with clear navigation, not consecutive sections of one long page. Flow: upload → inspect/edit/confirm → open day → select/open activity → return to day with registered data and saved choice intact. Day may scroll; selected activity prioritizes only its own facts and previous/next, allowing long/enlarged content to scroll. Preserve unsaved input and unresolved commands across safe internal navigation; keep recovery reachable and existing loss/access guards effective. Navigation never starts a shift or records an outcome. Existing explicit Start and bus controls belong with the day. Future notices have a secondary day-linked destination (11.4/11.5); end/abort/recap belongs in day/shift navigation (11.3), without implementing them in 11.2. Intermediate-stop extraction/display is post-V1; expansion of the limited working demo remains later planned work.

| Surface | Entry and actions | Exit / failure |
|---|---|---|
| Access / main menu | Private sign-in, saved drafts/days, separate clearly fictional demo entry, logout. | Session expiry requires sign-in; no private view before authorization. |
| Import and draft review | Select text PDF or manual entry; inspect source beside interpreted fields, page/field uncertainty; edit/add/remove/reorder activities. | Confirm explicitly or save draft. Invalid/unsupported input permits manual entry; cancellation preserves saved/confirmed work. |
| Confirmed day overview | Reporting time, chronological activities, dates, gaps/known parts, physical bus distinct from duty; line/date notice list. | Explicit Start activates saved plan; select activity. A new import creates a separate draft, never replaces this day. |
| Selected activity | Route, direction/destination and planned dates/times, or non-passenger type/place; selected activity is labelled manual. | Previous/next/direct choice, bus correction, explicit outcome or return to day. Selection does not complete anything. |
| Notice reader / maintenance / editor | Separate day-linked reader with line/calendar-date filters and complete source facts; unfiltered maintenance/editor retain proposals and pending recovery. Optional source link/description, short/deep text, explicit selected/all-line scope, validity/source-update time and separate entered/checked time. | Reader/day/maintenance navigation preserves selected activity and input. Save/cancel edit stays in maintenance; no sound, staged stop warning or acknowledgement lifecycle. |
| End/abort confirmation and recap | Review outcomes, explicitly end normally or abort; cancel is clear. | Saved terminal recap is read-only. Unknown work stays unknown; no resume or PDF action. |
| Fictional assessment | Resettable fictional day and import/manual-navigation/notice/save-error examples. | Reset only fictional state; failures never fall back to private records. |

**UJ-1:** sign in → import/manual draft → review/correct → confirm → enter bus/read day and notices → Start/select activity → record outcomes while stopped → confirm end/abort → read recap.

**UJ-2:** local README setup → fictional fullstack seeded environment → repeat the same included flow → inspect controlled failures → reset. Public no-login demo and locally provisioned fictional fullstack credentials are distinct from private owner access.

## Components and behavior

**Draft review:** show interpreted, user-corrected and unresolved values distinctly with text/symbols. Keep page/section provenance when known; unknown coverage is stated. Source preview is transient and may require reselection after reload. Explain unsupported scan/image input without treating manual fallback as successful extraction. Required date/type errors block confirmation visibly. No AI correction/chat interface.

**Date/order:** show service date and explicit calendar times across midnight. Preserve extended-hour meaning in review. Do not infer that a later work part starts at the first part's depot. Known gaps, breaks, vehicle duty and bus changes retain their distinct meaning.

**Day overview:** one chronological list and a secondary notice region; readable reporting time and bus field. Missing bus is visibly unassigned; Vogn never fills it automatically. A confirmed day can be consulted before Start. Once active, plan structure is fixed; explain that in-day revised-file reconciliation is deferred rather than presenting a nonfunctional control.

**Activity selection:** direct selection list identifies route, direction/destination and departure/date; line number alone is insufficient. Previous/next includes non-passenger activities and is disabled with a clear boundary label at the ends. The prominent label is `Valgt tur` or `Valgt aktivitet`, with `Manuelt valgt`. Do not show `Du er her`, current/next stop, GPS marker or arrival timer. Scheduled time cannot change selection.

**Outcomes:** default `Ikke registrert`; explicit `Fullført manuelt`, `Hoppet over`, `Avbrutt`. Owner clarification, 2026-10-25: registration requires an explicitly started active shift. Before Start, day reading, activity selection and details remain available; selection never Starts or records outcomes. Change outcomes before closure, including explicit return to unregistered; use a separately labelled area and explicit Save. Show saved counts and remaining unregistered members on a separate day-linked confirmation screen. `Avslutt skift` / `Avbryt skift` → confirmation/cancel with return focus. The separate read-only recap shows the saved plan and manual/unknown outcomes, with expiry. Terminal consultation never writes another selection. Keep proposals and recovery reachable across navigation; known-unsent proposals may be discarded locally when current facts are unavailable, while uncertain commands retain checking/retry. A neutral `Takk for i dag` is sufficient; no inferred success or scores.

**Notice reader:** heading `Avvik for linjer og datoer`; separate from `Manuelt vedlikeholdte avvik` maintenance/editor. Each item carries all saved explanations and optional source description/link, explicit scope and metadata. Shared multi-line notice appears once listing all matched lines; separate incidents remain separate. Exact line identifiers preserve leading zeros/case; copied route headings are not parsed. Match day lines independently of the union of explicit planned intervals, with Oslo calendar-date filters, midnight/DST and gaps. Fully known validity excludes non-overlap; unknown/partial validity remains labelled uncertain. Explicit all-line notices remain candidates when plan lines are absent. Describe line-free activities neutrally and explain unmatched tags/possible coverage gaps. Empty stored, empty filtered and unavailable states stay distinct. Use `Kildens oppdateringstid er ukjent` for a null source time, and separate `Registrert` / `Sist kontrollert` timestamps. Reading/editing does not automatically update checked time; an explicit source-check action does. `Avsluttet manuelt` never establishes road clearance. No precise trip/stop match or automatic coverage claim. Preserve maintenance proposals and reachable original-command recovery across reader navigation.

**Save feedback:** show saving, saved, unsaved, unavailable, conflict and unresolved response honestly. Keep form input after request failure while the page remains open. A lost response leads to status lookup/retry using the same command; no duplicate day or end. A stale tab offers reload and preserves current input for comparison, without automatic force overwrite. Warn before avoidable navigation with unsaved edits; page closure can lose them. Successful online reload restores server-saved state only.

**Access:** clear private presentation on logout/session expiry, guard Back/reload, and preserve saved server data only until its own deadline. Server-unreachable logout reports unconfirmed server logout and locks local presentation; no offline private recovery. All private endpoints still authorize access. Demo remains clearly fictional and isolated.

**Theme:** manual Day/Night toggle persists as a non-private preference until changed. Use text/icon and selected state. No Auto button, ambient sensor dependency or wake-lock claim.

## Required visible states and copy

| Condition | Treatment |
|---|---|
| Unsupported/scanned PDF | `Denne PDF-en støttes ikke. Legg inn aktivitetene manuelt eller velg en tekstbasert PDF.` |
| Unknown import fields/coverage | Mark affected fields/pages; do not say the day is complete. |
| No registered notices | `Ingen avvik er registrert her. Kontroller originalkilden.` |
| List unavailable | `Avvikslisten er utilgjengelig. Prøv igjen eller kontroller originalkilden.` |
| Unknown start / legacy ending / check | Qualify a missing start as partial validity. Legacy `Mangler sluttdato` stays in maintenance until explicitly completed; exclude it from active reading. `Ikke kontrollert` is separate; never imply freshness. |
| Server unavailable | `Kan ikke lagre nå. Endringene er ikke bekreftet lagret.` |
| Lost save response | `Lagring er uavklart. Kontrollerer lagret versjon.` then resolved result or actionable retry; never indefinite checking. |
| Stale revision | Explain newer saved version; preserve unsaved input and offer reload. |
| Expired session/data | Non-private sign-in/expired surface. Reauthentication cannot revive expired data. |
| Demo | Persistent `Fiktive demodata` label; fictional failures remain inside that context. |

## Accessibility and verification

Keyboard order follows reading order; controls have action labels, visible selected/disabled state and meaningful focus. Dialog focus returns to its invoking control; cancellation changes nothing. No color-only status, hover-only essential action or required swipe. Do not announce every refresh; announce meaningful save/failure transitions. Long Norwegian place names and enlarged text must wrap without hiding controls or critical information.

Use manual Day/Night and applicable IR-01 values from DESIGN. Test actual rendered forms, warnings, dialog, disabled boundaries and focus; tablet/PC fit requires observations. No previous mock acceptance proves these implemented states. Deferred UJ-3/UJ-4, sensor locks, offline/transfer, plan-revision and export flows are historical and must not remain as active navigation.

## Owner activity-flow refinement — 2026-10-25

Use Aktivitetsstatus for the user-facing outcome concept and retain Fullført manuelt. Activity selection still opens consultation without starting or recording anything. Provide Start and End/Abort directly from the selected activity, with explicit confirmation/cancel and current lifecycle context, reusing one lifecycle authority. Cancel returns to the exact originating activity and invoking control. The day entry points have consistent Start confirmation; accepted closure retains the approved separate read-only recap. Keep unsaved/pending/current-authority protections and long/enlarged Day/Night navigation. The owner reports the recap and other exercised behavior good; final story acceptance remains pending.

Owner acceptance, 2026-10-25: Jonas accepted the implemented activity-flow refinement and authorized commit/push. Existing later tablet/theme obligations remain separate; no next story is started.
## Owner notice-lifecycle correction — 2026-10-26

The owner rejected registering the same notice for every scanned day. Replace the per-day scope with one account register, consulted automatically by every eligible day. Keep separate reader/management/editor views and retain unsaved proposals/original recovery across plan switches or parent expiry. Management remains available independently of a live shift. Require an ending date when registering; date-only means the end of that Oslo date, clearly stated, while an explicit ending clock is preserved. Show when the notice will expire. Allow manual earlier ending and extension only before the existing deadline. At expiry show `Utløpt`, distinct from `Avsluttet manuelt` and source-check time. Neither proves road clearance. Ended/expired incidents leave the active reader and remain read-only history for seven days; no reopening or post-expiry extension. Legacy missing endings are shown as `Mangler sluttdato` for explicit completion, with no fabricated date or active-relevance claim. Deleting/ending the original shift must not delete a still-valid account notice. Keep shared incidents single and separately entered incidents separate; no guessed deduplication.
