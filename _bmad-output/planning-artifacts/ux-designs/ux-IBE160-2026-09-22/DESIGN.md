---
name: IBE160 Bus Driver Assistant
description: Calm operational information for bus drivers on a mounted tablet.
status: final
updated: 2026-09-22
sources:
  - ../../prds/prd-IBE160-2026-09-21/prd.md
  - ../../prds/prd-IBE160-2026-09-21/addendum.md
  - ../../briefs/brief-IBE160-2026-09-21/product-brief.md
  - ../../briefs/brief-IBE160-2026-09-21/brief.md
  - ../../briefs/brief-IBE160-2026-09-21/addendum.md
source_precedence: PRD and PRD addendum govern; briefs provide background.
colors:
  surface-base: '#FFFFFF'
  ink-primary: '#171717'
  ink-secondary: '#525252'
  critical: '#AD1717'
  attention: '#805000'
  information: '#1755A1'
  confirmed: '#17613E'
  surface-base-dark: '#101010'
  ink-primary-dark: '#EAEAEA'
  ink-secondary-dark: '#BBBBBB'
  critical-dark: '#F89696'
  attention-dark: '#EFC66C'
  information-dark: '#95BDEC'
  confirmed-dark: '#8BCDAB'
  warning-fill: '#F5C842'
  warning-ink: '#171717'
  theme-sun: '#F5C842'
  theme-moon: '#BBBBBB'
typography:
  stop-focus:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 64px
    fontWeight: '750'
    lineHeight: '1.15'
    letterSpacing: -0.025em
  stop-secondary:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 32px
    fontWeight: '550'
    lineHeight: '1.15'
  route:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 42px
    fontWeight: '750'
    lineHeight: '1.3'
  destination:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 32px
    fontWeight: '650'
  stop-role:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 18px
    fontWeight: '650'
    letterSpacing: 0.04em
  trip-meta:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.5'
  control:
    fontFamily: system-ui
    fontSize: 20px
    fontWeight: '650'
  notice-title:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 45px
    fontWeight: '700'
    lineHeight: '1.12'
    letterSpacing: -0.02em
  notice-body:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 23px
    fontWeight: '400'
    lineHeight: '1.55'
  notice-stop-focus:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 36px
    fontWeight: '750'
    lineHeight: '1.15'
    letterSpacing: -0.025em
  notice-stop-secondary:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 25px
    fontWeight: '550'
    lineHeight: '1.15'
  notice-stop-role:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: 16px
    fontWeight: '650'
    letterSpacing: 0.04em
  preparation-heading:
    fontFamily: system-ui
    fontSize: 34px
    fontWeight: '700'
  preparation-section:
    fontFamily: system-ui
    fontSize: 23px
    fontWeight: '700'
  preparation-activity:
    fontFamily: system-ui
    fontSize: 22px
    fontWeight: '650'
  preparation-time:
    fontFamily: system-ui
    fontSize: 21px
    fontWeight: '650'
  preparation-detail:
    fontFamily: system-ui
    fontSize: 18px
    fontWeight: '400'
  preparation-table:
    fontFamily: system-ui
    fontSize: 20px
    fontWeight: '400'
  preparation-source-meta:
    fontFamily: system-ui
    fontSize: 16px
    fontWeight: '400'
rounded:
  control: 8px
spacing:
  screen-inline: 30px
  screen-block: 22px
  orientation-gap: 22px
  stop-label-gap: 2px
  stop-block: 10px
  control-inline: 24px
  control-block: 10px
  control-gap: 14px
  notice-columns: 30px
  preparation-columns: 30px
  preparation-row-gap: 12px
  preparation-path-gap: 24px
  preparation-table-block: 16px
  preparation-table-inline: 12px
components:
  persistent-clock:
    fontSize: 30px
    fontWeight: '700'
    numerals: tabular-nums
  mentor-role-badge:
    borderWidth: 3px
    paddingBlock: 7px
    paddingInline: 14px
    fontWeight: '800'
    letterSpacing: 0.06em
    color: '{colors.information}'
    colorDark: '{colors.information-dark}'
  mentor-driving:
    columns: '1.15fr 1fr'
    gap: 28px
    focusSize: 48px
    secondarySize: 28px
  between-activity:
    headingSize: 54px
    lineHeight: '1.12'
  closing-message:
    headingSize: 58px
    maxWidth: 940px
  pdf-document:
    pageSize: A4
    orientation: portrait
    bodySize: 16px
    tableSize: 14px
    headingSize: 30px
  theme-toggle:
    size: 58px
    outerWidth: 152px
    outerHeight: 62px
    iconSize: 32px
    autoMinWidth: 76px
    autoInactive: '{colors.ink-secondary}'
    autoInactiveDark: '{colors.ink-secondary-dark}'
    autoActive: '{colors.confirmed}'
    autoActiveDark: '{colors.confirmed-dark}'
    borderWidth: 2px
    radius: '{rounded.control}'
    background: '{colors.surface-base}'
    backgroundDark: '{colors.surface-base-dark}'
    border: '{colors.ink-primary}'
    borderDark: '{colors.ink-secondary-dark}'
    sun: '{colors.theme-sun}'
    moon: '{colors.theme-moon}'
  driving-focus:
    fontSize: '{typography.stop-focus.fontSize}'
    railWidth: 7px
    railColor: '{colors.information}'
    railColorDark: '{colors.information-dark}'
    paddingInlineStart: 21px
    paddingBlockStart: 14px
    paddingBlockEnd: 18px
  three-stop-sequence:
    secondaryRailWidth: 3px
    secondaryPaddingInlineStart: 25px
    marginInlineStart: 10px
  driving-menu:
    minHeight: 62px
    width: 152px
    radius: '{rounded.control}'
    paddingInline: 12px
    paddingBlock: '{spacing.control-block}'
    borderWidth: 2px
    background: '{colors.surface-base}'
    backgroundDark: '{colors.surface-base-dark}'
    foreground: '{colors.ink-primary}'
    foregroundDark: '{colors.ink-primary-dark}'
  stop-warning:
    fill: '{colors.warning-fill}'
    ink: '{colors.warning-ink}'
    size: 0.8em
    minSize: 24px
    marginInlineStart: 0.2em
  notice-and-sequence:
    columns: '1.25fr 1fr'
    gap: '{spacing.notice-columns}'
    noticeRailWidth: 7px
    noticePaddingInlineStart: 26px
  import-review-editor:
    columns: '0.8fr 1.35fr'
    gap: '{spacing.preparation-columns}'
    rowColumns: '70px 1fr auto'
    rowMinHeight: 78px
    rowGap: '{spacing.preparation-row-gap}'
    rowPaddingBlock: 10px
    sourceBorderWidth: 2px
    sourceBorderStyle: dashed
    sourcePadding: 30px
  preparation-control:
    minHeight: 58px
    radius: '{rounded.control}'
    paddingInline: '{spacing.control-inline}'
    paddingBlock: '{spacing.control-block}'
    borderWidth: 2px
  shift-disruption-list:
    columns: '1fr 1.2fr'
    gap: '{spacing.preparation-columns}'
    noticeRailWidth: 5px
    noticePaddingInlineStart: 16px
    noticeMarginBlock: 20px
  shift-part-header:
    borderWidth: 2px
    paddingBlockStart: 12px
    rowMinHeight: 65px
    rowGap: 14px
    gapPaddingBlock: 15px
  shift-revision-review:
    pathColumns: '1fr 1fr'
    pathGap: '{spacing.preparation-path-gap}'
    pathRailWidth: 3px
    pathPaddingBlockStart: 20px
    cellPaddingBlock: '{spacing.preparation-table-block}'
    cellPaddingInline: '{spacing.preparation-table-inline}'
    cellBorderWidth: 1px
---

## Brand & Style

**Accepted extended coverage:** the [43-screen consolidated gallery](mockups/remaining-screens.html) covers private access, ambiguity, stop selection, between-activity states, end/abort, operative FADDER/INSTRUKTØR, the separate public PC demo and PDF. The final corrections keep `Bekreft egen tur` on one line and remove the blue rail from Bussbytte, as already done for Pilotbil and depot return. Acceptance establishes a visual reference, not implemented behavior or device validation.

A calm, professional operational instrument for a bus driver using a mounted tablet. The essential information must be understood in a one-to-two-second sideways glance while traffic, mirrors, passengers and other instruments compete for attention. Predictability and honest uncertainty matter more than decorative expression.

This specification captures the accepted Day A/Night C palettes and [vertical driving composition](mockups/driving.html). The reference's existing typography, spacing and control geometry are extracted above as implementation reference tokens. Their readability, fit and touch performance still require validation on the mounted tablet; accepting the composition does not establish device performance or implemented behavior. Unillustrated failure/responsive variants remain governed by EXPERIENCE and implementation verification. The latest user decisions recorded in `.memlog.md` extend the PRD to PDF and JPG/PNG import and establish current-stop dominance at a stop and next-stop dominance between stops.

The companion [EXPERIENCE.md](EXPERIENCE.md) owns behavior. These two spines take precedence over mocks, wireframes and imports when they conflict.

## Colors

| Semantic role | Confirmed use |
|---|---|
| Red | Critical information; the source-required end-shift action is also red. |
| Yellow or orange | Attention; internet loss specifically uses a yellow exclamation triangle with explanatory text. |
| Blue | Information. |
| Green | Confirmed or normal status, never an unsupported claim that a route is clear. |

Use a restricted, consistent palette with high contrast in both day and night modes. Status must remain understandable through text and symbols as well as color. Fresh, stale, uncertain, unavailable, manually corrected and simulated information must not share an indistinguishable appearance. Night mode must limit glare and unnecessary illumination; day mode must remain readable in direct sunlight.

The approved day palette pairs {colors.surface-base} with {colors.ink-primary} and {colors.ink-secondary}. The approved night palette pairs {colors.surface-base-dark} with {colors.ink-primary-dark} and {colors.ink-secondary-dark}. Semantic text uses the corresponding critical, attention, information and confirmed token for its mode. These colors are foregrounds on the base surface; using them as button fills requires a separately checked foreground pairing. The attention foreground is dark amber by day for readable text. The accepted stop-warning triangle uses {colors.warning-fill} with a dark {colors.warning-ink} outline and exclamation; the connectivity warning is illustrated in the accepted recovery reference.

Calculated relative-luminance contrast against the base surface is 17.93:1 for day primary text, 7.81:1 for day secondary text, 15.82:1 for night primary text and 9.91:1 for night secondary text. The warning's dark outline/exclamation contrasts 11.29:1 with its yellow fill. Yellow alone contrasts only 1.59:1 against the day base (11.98:1 against the night base), so preserve the dark outline and exclamation. These numerical pair checks do not establish complete-interface conformance, readability or glare performance on the mounted tablet. Do not apply the same text tokens to other surfaces without checking their contrast.

**Verification remaining:** complete-interface contrast, changed-notice emphasis and accepted compositions require device readability/fit checks. Base palettes and illustrated warning/control treatments are settled.

## Typography

Current stop dominates when the bus is at a stop; next stop dominates between stops. Route and destination remain clearly and persistently visible as secondary orientation. Three-stop look-ahead must remain readable without competing with the dominant fact. An approaching important disruption or necessary action may temporarily take priority; the appropriate current/next stop regains priority afterward.

Use large, clear text with a small number of visibly distinct roles. Notice headings stay visible; long detail belongs to permitted detail access. New and changed notice versions are bold until opened. Confirmed ended notices are struck through for their retained overview period. Never shrink important text simply to fit more content.

The accepted driving reference uses the system sans-serif stack. Normal stop focus is {typography.stop-focus.fontSize} at weight 750; secondary stops and destination are 32px, the route number 42px and metadata 18px. During prominent notice presentation, the notice title is 45px and the adjacent stop focus 36px. These are extracted reference values, not evidence that smaller notice-side text meets the glance goal. Where no line height is specified in a token, the reference uses the browser's normal line height. Validate available font weights, long-name wrapping and actual viewing distance on the target device. Accepted preparation references add a 34px heading, 23px section headings, 22px activity labels, 21px times, 20px comparison text and 18px detail. Multi-notice source metadata uses 16px; that reference value is not proof of device legibility. Summary and document typography follow the accepted summary/recovery and consolidated gallery references. Local paragraph/heading line heights vary between the preparation references, without defining a new global type scale.

## Layout & Spacing

Driving footer: Menu and the combined Day/Night/Auto control have equal 152px by 62px outer boxes, aligned to the same top and bottom edges with the existing 14px gap. The icon and Auto remain separate hit areas inside one outline. A newly received relevant acute notice occupies the right-hand information area, retaining stop context to the left; use an inline region, not a covering modal or moving popup.

Accepted summary and degraded-data reference: [daily summary, internet loss and GPS loss](mockups/summary-recovery.html). The GPS-loss variant includes the requested countdown beside restricted Menu/trip selection. The static countdown is an example, not a working timer or a new wait interval.

Accepted preparation references: [original beside interpreted activities](mockups/preparation.html) and [multiple notices, split parts and shift revisions](mockups/shift-updates.html). Source/review columns use 0.8fr/1.35fr; the ordinary overview uses 1.4fr/1fr. Expanded shift parts and notices use 1fr/1.2fr with a 30px gap. Update entry paths use equal columns and a 24px gap, followed by current/proposed comparison columns. The 1080px minimum width and 740px minimum height frame the static previews, not responsive product requirements. These accepted stationary compositions do not alter driving; device fit and interaction remain untested.

Tablet first, primarily landscape. The stop overview is vertical, future at the top. Three-stop baseline, top-to-bottom: at a stop, stop after next / next / CURRENT highlighted; between stops, stop after next / NEXT highlighted / departed. Previous stop is omitted while at a stop to show two upcoming stops. Four visible stops with previous always at the bottom may be explored as an alternative; it is not the selected baseline. Preparation, active driving and daily summary have distinct purposes and clearly distinguishable presentations. Active driving has one dominant information area and few secondary elements, without extensive scrolling or a grid of competing equal-weight cards. A map must not displace the main operational information.

Large forgiving touch targets support vibration, short stops and possible gloves. Necessary corrections should take one or two clear taps while stopped. The depicted driving Menu control has a 62px height, 152px width and 10px by 12px padding; glove and vibration performance still need device validation. At confirmed sequence boundaries, use an em dash with an explicit no-more/no-previous label; missing data retains its distinct unavailable state.

Accepted composition reference: [vertical driving sketch](mockups/driving.html), extracted from `.working/driving-vertical-2.html`. The earlier vertical and horizontal sketches are historical and do not govern the current stop roles or orientation. The landscape reference uses 30px horizontal and 22px vertical padding, with route/destination above the stop sequence and a footer below. The prominent-notice variant places notice and sequence side by side in a 1.25:1 ratio with a 30px gap. Its 16:10 presentation and 840px minimum preview width are mock framing, not finalized responsive breakpoints; side-scrolling belongs only to the review page. An affected stop two ahead carries a yellow triangle immediately after its name; its automatic message appears on approach from the preceding stop and stays until driving onward from the affected stop.

The [accepted consolidated gallery](mockups/remaining-screens.html) frames tablet examples at 1180 × 740px minimum, the PC simulation at 1380 × 780px minimum and PDF as two portrait A4 pages. These are reference frames, not fixed product breakpoints. Its preparation columns use 1.25fr/1fr with a 36px gap; mentor driving uses {components.mentor-driving.columns} with {components.mentor-driving.gap}. A permanent top-right clock uses tabular numerals without competing with stop focus. The operational role is a prominent text badge, never an icon-only indication.

Pilotbil, Bussbytte and the two-line `Returner til` / `Depot` are centered and have no decorative blue next-activity rail. Other activity pages preserve one dominant activity and a secondary next activity. The closing page is centered with restrained text and summary/main-menu actions. PDF uses document hierarchy, provenance and page numbering rather than a tablet screenshot. Screen 42's `Bekreft egen tur` action stays on one line, with sufficient width rather than smaller text.

## Elevation & Depth

Avoid glassmorphism, decorative depth and visual noise. No shadow or surface-elevation system has been chosen.

## Shapes

The depicted Menu control uses {rounded.control} corners and a 2px outline. Stop focus uses a 7px information-colored left rail; secondary rows use 3px secondary-ink rails. The stop-warning triangle is an outlined SVG with an exclamation, immediately after the name. No general icon family or shape system for unshown surfaces has been selected.

## Components

Meny is always visible in driving, replacing the standalone trip-choice control. During a movement restriction, show the disabled control with explicit `Meny · låst` text and a distinguishable outline; do not hide it. For GPS-outage-locked Menu, show a readable remaining-time label directly beside the controls (`Tilgjengelig om 4:12 uten GPS`). Use the existing attention and body/metadata roles, not a flashing animation. The countdown disappears when its restriction ends or reliable GPS returns; an ongoing speed restriction needs its own plain-language reason. Timer behavior is defined in EXPERIENCE.md.

Names match the behavioral component catalog in EXPERIENCE.md. Driving and preparation tokens above come from accepted references. Preparation controls use a 58px minimum height, 8px radius and 10px/24px padding; the older update working sketch used 22px inline padding, normalized in the promoted reference. Both preparation references use the approved base, text and semantic palettes. Rules for unshown components remain constraints rather than completed compositions.

| Component | Visual rules |
|---|---|
| Persistent clock | Top-right time on tablet screens; {components.persistent-clock.fontSize}, weight {components.persistent-clock.fontWeight}, tabular numerals. |
| Mentor assignment and role | Separate own-plan and linked-person panels; permanent FADDER or INSTRUKTØR badge using {components.mentor-role-badge.borderWidth}. Operational mentoring is visually distinct from simulated PC mode. Import review includes the immediate source-file deletion notice. Summary/PDF distinguish accompanied portions and their observed/uncertain outcomes from own activities and takeovers, with the own-day expiry visible. |
| Mentor driving and role switch | Preserve vertical stops and route orientation; open controls while guiding. FØRER replaces the guiding role after `Jeg kjører`; role status remains prominent. |
| Closing message | Centered `Takk for i dag`, one brief affirmation, then summary/main-menu actions; {components.closing-message.headingSize}, without scores or decorative celebration. |
| PDF document | Portrait {components.pdf-document.pageSize}, headings, outcome table, notice/evidence detail and page footer; simulation text on every demo page. Export may span more than the two example pages. |
| Access and navigation controls | Clear labelled entry points, explicit logout and no public-registration affordance. No small or hidden controls. |
| Driving menu | Always visible in the driving footer, using {components.driving-menu.minHeight}. Shows `Meny` when available and `Meny · låst` when restricted, with a distinguishable outline and accessible state. GPS-outage waiting time appears beside it. Trip selection is inside this menu, not another driving-view button. |
| Import review editor | Clearly separate interpreted, unknown and user-corrected values. Both file formats use the [same source/review presentation](mockups/preparation.html) with {components.import-review-editor.columns} and labelled activity rows. |
| Activity and trip selector | Make route, direction, service date and relevant times distinguishable; preserve passenger/non-passenger distinctions. |
| Shift overview | Make chronological activities, reporting time, known places and actual bus assignment readable before duty. |
| Driving focus | Current stop dominates at a stop; next stop between stops. Temporary important-action takeover preserves route/destination orientation. |
| Three-stop sequence | Vertical. Top-to-bottom at a stop: stop after next / next / CURRENT highlighted. Between stops: stop after next / NEXT highlighted / departed. No previous stop in the at-stop baseline. Yellow triangle immediately after an affected name, with an accessible warning label. Four-stop alternative is optional, not adopted. |
| Trip transition and correction controls | The accepted reference places always-visible `Meny` at the lower right, using {components.driving-menu.minHeight} minimum height. Trip choices are inside Menu. Automatic transition and undo compositions remain open. |
| Notice heading and detail | Moving: headings only, retaining essential data-status labels. Stationary: expandable body/source metadata and a large `Registrert` action, with optional swipe dismissal as an alternative. Visible heading, bold unseen versions, extra color treatment for changed versions, strike-through for confirmed endings. Detail distinguishes validity, source time and retrieval time. When two important disruptions approach the same stop, show both short headlines simultaneously; no automatic alternation or carousel. |
| Data status | Text/symbol plus semantic color; prominent top connectivity warning, local source failures, unmistakable simulation. Never disguise uncertainty as normal operation. |
| Stop correction controls | Large labelled previous/next controls during GPS loss and clear arbitrary-stop selection when permitted. |
| Operational-change controls | Clearly labelled choices distinguish trip interruption, physical bus replacement, next trip and shift ending. |
| Between-activity display | Legible activity label; source-required centered `Bussbytte`/`Pilotbil`; depot return uses centered `Returner til` / `Depot` on two lines. None of these three activity screens uses the decorative blue rail. |
| Theme control | Active Auto additionally has a small underline, providing a non-color selected cue; manual Auto has no underline.  One combined outlined control immediately left of Menu has two hit areas: current-mode sun/moon and `Auto`. Both remain enabled when Menu is locked. Day appearance: yellow sun, light background, dark outline. Night: gray crescent, dark background, gray outline. Icon stays visible in Auto. Auto text uses gray inactive tokens for manual and green active tokens for automatic; expose selected state accessibly. Keep the shared outer boundary and a divider, with {components.theme-toggle.size} hit height, {components.theme-toggle.iconSize} icon and {components.theme-toggle.autoMinWidth} minimum Auto width. Actual lunar phase is optional and not adopted; new moon would use a gray circular outline. |
| End-shift confirmation | Red `Avslutt skift` action and unambiguous `Er du sikker?` confirmation/cancel choices. |
| Summary and export | Distinguishable completed/skipped/aborted/uncertain outcomes, manual evidence and source failures; closing `Takk for i dag`. Simulation marking carries into demo export. |
| Instructor simulation controls | Clearly separate simulation controls and fictional data from operational information; no misleading live appearance. |
| Optional support information | Speed limit, weather and meeting buses remain subordinate to the core driving hierarchy; uncertain or unavailable support is visibly qualified. |
| Shift disruption list | Several readable notice rows with distinct titles; one shared notice names all affected lines and trip/time associations. Keep separate incidents separate, even on one line. Source and freshness remain attached to each notice. The [accepted composition](mockups/shift-updates.html) uses separate 5px attention rails, explicit affected lines/trips and attached metadata, with {components.shift-disruption-list.noticePaddingInlineStart}. |
| Shift part header | Clearly separate work parts and show each reporting time and known starting depot. Distinguish the gap between parts from ordinary trip/break rows without implying an unconfirmed transfer. |
| Shift revision review | Distinguish performed/current work from proposed future changes. Updated-file and manual-add entry points are both visible; additions, changes and unresolved matches must be distinguishable beyond color. The [accepted reference](mockups/shift-updates.html) uses two update paths, explicit file scope and current/proposed columns with {components.shift-revision-review.cellPaddingBlock}; unresolved matches have labelled alternatives and unavailable confirmation. |

## Do's and Don'ts

| Do | Don't |
|---|---|
| Highlight current stop at a stop and next stop between stops. | Make route, notices, map and optional information equal-sized competitors. |
| Distinguish observed, planned, stale, manual and simulated information. | Use visual certainty unsupported by data. |
| Use consistent restrained semantic colors with text and symbols. | Rely on color alone or repeat alarms to demand attention. |
| Keep active driving concise and predictable. | Use chatbot framing, long pages, hidden functions or precise swipes. |
| Preserve legibility across sunlight, darkness and tunnels. | Add glare, unnecessary animations, gamification or flashy AI styling. |
| Keep imported personal information out of active driving. | Expose personal shift details on a screen visible to passengers or others. |
