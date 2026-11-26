# Route/vehicle — acquisition digest

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Publisher Entur; all accessed 2026-10-26; medium/single-publisher documentation, no live feed or device observation.

- https://developer.entur.no/docs/open-services/vehicle-positions (updated 2026-07-15): GraphQL HTTP and WebSocket vehicle positions; example includes vehicleId, lastUpdated, location; maxDataAge filter documented. Does not establish TRO coverage, unique mapping to the selected dated journey, user's physical bus, or sensor accuracy. Class compatibility.
- https://developer.entur.no/apis/stop-place-v1-read (date unknown): stop places, quays, scheduled-stop-point mappings and versions are exposed with location information. Class data interface. Does not prove every chosen occurrence has a usable quay coordinate or correct historical version.
- https://developer.entur.org/pages-real-time-intro/ (date unknown; legacy portal directs to developer.entur.no): SIRI VM is vehicle-position information; SIRI ET is timetable estimates; these are different streams. Class pattern. Provider coverage must be rechecked; no coverage-table icon inference made.

Leads/limits: qualify exact physical-bus↔dated-journey↔vehicle linkage and source age before any future supplement. Current documentation alone cannot supply that private operational connection. First delivery does not need this integration. Coordinate provenance and occurrence-order requirements are project proposals, not claims that the route extension already delivers them.
