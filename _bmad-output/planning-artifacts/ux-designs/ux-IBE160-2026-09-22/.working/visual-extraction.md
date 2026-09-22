# Accepted driving reference extraction

Source: `driving-vertical-2.html`, accepted by the user on 2026-09-22. Promoted copy: [driving.html](../mockups/driving.html). Original working artifact retained. DESIGN.md remains draft.

| Existing reference | Extracted contract |
|---|---|
| Day A / Night C | Existing base, ink and semantic palettes retained. |
| System sans-serif; main stop 64px/750/1.15 | `typography.stop-focus`; secondary stop 32px/550, route 42px/750, destination 32px/650, role and trip metadata 18px. |
| Notice column styles | Title 45px/700/1.12, body 23px/400/1.55; adjacent focused stop 36px, secondary 25px, role 16px. Existing CSS overrides, not unused 54px event default. |
| Correction button | `components.trip-correction-control.minHeight` = 58px, `rounded.control` = 4px, 2px border, 10px/24px padding, 20px/650 label. |
| Screen and stop spacing | 22px/30px padding, 22px orientation gap, 2px label gap; exact existing focus and secondary rail offsets captured. |
| Yellow SVG marker | `colors.warning-fill` #F5C842, `colors.warning-ink` #171717; 0.8em with 24px minimum, 0.2em gap immediately after stop name. |
| Vertical sequence | Future at top; at stop: next-after-next / next / CURRENT; between stops: next-after-next / NEXT / departed. No four-stop adoption. |
| Notice/sequence composition | 1.25fr / 1fr columns, 30px gap; notice staged on approach, retained through dwell, cleared after onward progression as defined in EXPERIENCE.md. |

Relative-luminance calculations: primary/base day 17.93:1, secondary/base day 7.81:1; primary/base night 15.82:1, secondary/base night 9.91:1. Warning ink/fill 11.29:1; warning fill/day base 1.59:1, fill/night base 11.98:1. Retain dark outline and exclamation. This is pair arithmetic, not a complete accessibility or device validation result.

Still open: mounted-device viewing distance/glare/touch checks, realistic long names, normal line heights and font weight rendering, sequence endpoints, updated-notice treatment, connectivity warning composition, responsive behavior, transition/undo composition, and unshown preparation/summary surfaces. The preview page's margins, 840px minimum tablet width and horizontal review overflow are not product layout requirements. No new aesthetic values were invented for unshown surfaces; no behavior is implemented by the static HTML.
