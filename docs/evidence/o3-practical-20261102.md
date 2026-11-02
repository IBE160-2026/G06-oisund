# O3 praktiske eksterne kontroller — pågår

Grunnlag: aktiv produksjon7921eb5, senest lesende bekreftet ved start av denne økten. Eieren bruker Desktop/Brave/Wi-Fi og det syntetiske testutkastet fra O5. Bildenes klienthint viser Windows og Chromium/Brave-brandmajor156; full nettleserversjon, Windows-versjon og individuelle handlingstidspunkt er ikke oppgitt. Tidligere gyldig isolert evidens og bestått O5-flyt gjenbrukes.

| Kontroll | Observasjon | Avgrenset status |
|---|---|---|
| Autentisert GET `/private-api/auth/session` | Eier rapporterer sju forespørsler, alle200OK/Cache-Control:no-store/CF-Cache-Status:DYNAMIC | Bestått for akkurat disse rapporterte svarfeltene. Ingen full cache-/feilmatrise utledes. |
| Nettleserens memory/disk-cachekilde | Size er valgt, men kolonnen er ikke synlig | Uavklart; DYNAMIC ogno-store alene brukes ikke som bevis for denne separate visningen. |
| Appcookieflagg | Eier bekrefter Secure/HttpOnly/SameSite=Strict for både private_session/private_csrf | Bestått for de to appcookienes rapporterte flagg. [Resultat](o3-practical-20261102/app-cookie-flags.json). Ingen verdier samlet. |
| Normal ekstern lagring | Eier bekrefter lagring i appen,200/no-store, korrekt Request-Origin og CSRF-header til stede | Bestått for én normal syntetisk lagring. [Resultat](o3-practical-20261102/normal-save.json). Dette beviser ikke avslag ved feil Origin/CSRF. |
| DevTools Offline: tilgang og tilbakekomst | Eier presiserer at Lagre utkast ble trykket mens Offline var aktivt; innholdet ble skjult umiddelbart etter klikket. Etter Online/tilgangskontroll kom privat innhold og testendringen tilbake; ny session200 | Bestått avgrenset tilgangsreaksjon, gjenoppretting og synlig bevaring. [Frakobling](o3-practical-20261102/offline-access-suspension.json), [avklaring/recovery](o3-practical-20261102/offline-access-recovery.json). Ny varig lagring/gjenåpning avventes. Ingen etter-commit/tapt-kvittering-konklusjon. |
| Videre ekstern Origin/CSRF, cache/error, skriveresultat/kvittering/replay og fysisk klientnett | Ingen nye observasjoner i denne delen av økten | Fortsatt åpne; reelle skift/avvik skal ikke brukes. |

[Ordrett avgrensede baselinefelt og mottakstid](o3-practical-20261102/session-baseline.json). Ingen cookie-/tokenverdier, private svarbodyer eller HAR er samlet. Kun DevTools Offline i klientfanen er brukt; ingen server-/DNS-/tunnel-/produksjonskodeendring eller fysisk Wi-Fi-prøve er dokumentert. O3, O4 og O6 forblir åpne; O5-status er uendret.
