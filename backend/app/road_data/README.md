# Road snapshot boundary

The current public corpus records the historical Polaria to Flyplassvegen chain from 27 October 2026. It has 139 contiguous source segments, four source-bound roundabout arcs and recorded type 105 limits. The 70→50 change after the fourth roundabout is 218.448 m forward in the documented 200 m approach scenario. This evidence preserves the original topology calculation. It does not supply current temporary regulation, complete bus turn and lane eligibility or a physically qualified error model.

On 20 November 2026, five scoped repeat requests returned HTTP 200 for segment 1126506, the segmentized R4 sequence 1125950, the R4 surface exit, and two targeted type 105 queries. The returned R4 objects were 1019488950 v1 at 70 km/h and 1019488951 v1 at 50 km/h. Three responses exposed continuation links. This was a scoped source recheck. Complete current interval coverage, turn restrictions and temporary regulation remain open.

The private route projection only returns a matching packaged `v2-approved.json` with the exact dated, frozen journey, occurrence range, versioned road packages and supporting direction, coverage, topology, source and error-model evidence. No such operational package is bundled. The technical controls use two explicitly synthetic manifests and the same runtime matcher. A simulated browser or a reachable NVDB endpoint cannot close the physical pilot gates.

- Source pilot specification and evidence are pinned on `codex/plan-speed-limits` at `5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c`.
- [NVDB Les](https://nvdbapiles.atlas.vegvesen.no/) supplies public road topology and type 105 records under NLOD.
- Original sign evidence and licensing are stored in [the asset manifest](../../../frontend/public/assets/road-signs/source.json).
