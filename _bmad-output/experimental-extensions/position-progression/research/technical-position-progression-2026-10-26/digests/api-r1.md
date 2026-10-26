# API/privacy — acquisition digest

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Source: https://www.w3.org/TR/geolocation/ — W3C, Candidate Recommendation Snapshot, published 2026-03-26, accessed 2026-10-26. Class: API contract; confidence medium/single authoritative specification, not device compatibility evidence.

Retrieved sections 3, 6–9: secure context and user permission gate location; watch delivery is restricted to fully active visible documents. Timestamp is acquisition time, accuracy is a reported 95%-confidence radius in metres; high accuracy is a hint with possible power/latency cost. maximumAge controls accepted cached age; timeout excludes waiting for visibility/permission. Updates have implementation-defined significance/rate. Privacy guidance favours purpose limitation and disposal. No suitable tablet GNSS, measurement cadence, stop identity or background continuity is proved.

Leads: cross-check lifecycle in Chrome docs, actual Android permission/source availability, and permission UX in Brave. Bound: specification semantics can be documented now; actual device behavior remains an explicit future qualification.
