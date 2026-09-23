# DESIGN reconciliation

Verdict: consistent, with one small acceptance-gate omission. No new architecture decision is needed.

Compared the complete final `ux-IBE160-2026-09-22/DESIGN.md` against the Architecture Spine, honoring later adopted AD decisions. The spine explicitly delegates presentation to DESIGN (line 28), so its omission of individual tokens, exact layouts and component styling is appropriate. Client-owned operational state, distinct position/speed quality, version-aware notices, editable import drafts, private/demo isolation and local PDF export all support the required presentation. No technical contradiction was found.

## Actionable finding

- **Add device presentation qualification to the pilot gates.** `ARCHITECTURE-SPINE.md:254` tests GPS and operational transitions but does not mention DESIGN's explicitly outstanding full-interface contrast, changed-notice emphasis, mounted-device readability/fit, long-name wrapping, touch/glove performance or responsive behavior (`DESIGN.md:284`, `:290`, `:302`, `:304`). Extend the existing device gate with a compact reference to these DESIGN checks. This prevents the enumerated pilot gate from being treated as complete after functional GPS tests alone; the approved static compositions are not device qualification. The existing source reference already binds these requirements, so this is clarification rather than a new commitment.

## Constraints correctly delegated to DESIGN

Three-stop dominance and sequence orientation; visible locked Menu/countdown; non-color uncertainty and role indicators; keeping personal imported details out of active driving; fictional simulation markings including every exported demo PDF page; and all layout, typography and palette details remain authoritative through the explicit DESIGN reference. Do not copy the full visual specification into the short architecture document.
