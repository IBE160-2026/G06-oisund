# Accepted preparation extraction

Sources: preparation-1.html and preparation-2.html, accepted in the memlog. Copies promoted to ../mockups/preparation.html and ../mockups/shift-updates.html; working originals preserved. Documents remain draft. Static references do not implement behavior or establish device usability.

| Existing CSS | DESIGN mapping |
|---|---|
| `.top h2` 34px; `h3` 23px | typography.preparation-heading / preparation-section |
| `.title` 22px/650; `.time` 21px/650 | preparation-activity / preparation-time |
| detail 18px; review 20px; multi-notice source 16px | preparation-detail / preparation-table / preparation-source-meta |
| review split .8fr/1.35fr, gap 30px; rows 70px/1fr/auto, min 78px | components.import-review-editor |
| multi-notice split 1fr/1.2fr; 5px rail, 16px inset, 20px margin | components.shift-disruption-list |
| part 2px rule/12px inset, 65px rows, 15px gap padding | components.shift-part-header |
| paths 1fr/1fr, 24px gap, 3px rail; cells 16px/12px | components.shift-revision-review |
| buttons min 58px, 4px radius, 2px border | preparation-control reuses accepted control geometry |

Preparation-1 control padding is 10px/24px; preparation-2 had 10px/22px. Promoted references share approved 10px/24px; working originals unchanged. Day A/Night C foregrounds and base surfaces match approved tokens; no new product color/fill is introduced. Existing base-pair contrast arithmetic in DESIGN applies to these same pairs only. Gray review-page surround is presentation chrome, not a product token.

Gaps: source preview is a disclosed placeholder. No responsive breakpoints or upload/keyboard behavior proven; 1080px/740px bounds are preview framing. Source metadata at 16px, local paragraph/heading line heights, long content, full-shift length and touch performance need actual tablet checks. No broad review or acceptance of unseen editing/detail states is implied.
