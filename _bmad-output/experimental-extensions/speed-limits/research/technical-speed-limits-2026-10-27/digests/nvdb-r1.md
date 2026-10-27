# NVDB source digest, round 1

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Accessed 2026-10-27. Publisher Statens vegvesen; publication dates unknown unless response metadata says otherwise. Single-publisher confidence medium, not independent verification.

- Dataset https://dataut.vegvesen.no/dataset/nasjonal-vegdatabank documents network geometry/topology and speed limits on additional road categories. It does not prove complete Tromsø coverage.
- V4 docs https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Vegnett/ document bounded geographic filters and segment/node/length/geometry fields.
- https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Posisjon/ locates a single point on roads; no trajectory confidence guarantee is documented.
- https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Vegobjekter/ describes version history/time filtering. https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Endringer/ describes change pagination; aggregation can return fewer records than requested.
- https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/introduksjon/retning-pa-vegsystemreferanse/ distinguishes link direction from road-reference metre direction.
- https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Rute/ documents beta network routing. A route between endpoints does not prove intended bus path.
- Observed: imports/tromso-sample.json, one request with kommune=5501, antall=3; IDs 91467734/91467735/91467736, versions 5/5/3, limits 60/60/50. Includes county/municipal roads and a roundabout, linear locations and metadata. Not a random or representative sample. No next page followed. No complete coverage, physical signs, adjacency between examples, or live variable state demonstrated.

Technical recommendation (not source claim): local bounded multi-fix matching plus qualified directed corridor; uncertainty hides current/preview values. Open: intended-path qualification, variable/temporary coverage, complete pilot interval/direction coverage.
