# Integreringskontroll for nettbrettilgang, 2026-10-27

## Faktisk base og ny main

Den kjørende fiktive piloten og dette worktree-ets HEAD bygger på godkjent Epic 11: `f5ffa4bf64696b8e1abf910ccd8ac106663d30a9`. Ingen commit er laget i tilgangsarbeidet.

Lokal main ble ved ny lesekontroll funnet på `d5bf85d81b813e040bd718504d6edbddc5ae70ac`, og lokal origin/main på `ce0669f6f75f337a2df9471860be1b66efb171f0`. Ingen fetch er gjort i denne kontrollen, så dette er lokale ref-observasjoner, ikke ny GitHub-verifikasjon. Main inneholder tekniske Story 12.1/12.2-endringer som ikke fantes i tidligere docs-/logg-only main. Eier bekrefter at 12.1–12.3 ikke er godkjent; de avventer mens tilgangsarbeidet fullføres. Tilgangsprøvene godkjenner ikke disse storyene. Ingen story-/retrostatus endres her.

## Isolert sammenslåingsprøve

`git merge-file -p` er brukt bare på midlertidige tekstfiler under Git-ignorert `tmp/tablet-main-review`, med f5 som base og den fryste d5-main som mål. Ingen Git-merge/rebase, index-, ref- eller produktfilendring inngikk. Ingen ordinary database/container ble brukt. Første forsøk med python.exe lot seg ikke starte; samme kontroll ble deretter fullført med PowerShell/Git.

| Fil | Tekstlig treveiskontroll |
|---|---|
| backend/app/auth.py | Uten konflikt |
| backend/app/private_main.py | Uten konflikt |
| backend/app/run.py | Uten konflikt |
| backend/requirements.lock | Uten konflikt |
| frontend/src/PrivateAccess.tsx | Én konfliktblokk ved API-konfigurasjon |
| .logs/jonas-oisund/issues.md | Uten konflikt; senere main-punkter må bevares |

37 daværende nye filer ble sjekket mot main; ingen hadde samme sti som en sporet main-fil. Denne nye rapporten kommer i tillegg. Dette er ikke en full Git-merge eller semantisk regresjonstest. Faktisk index er fortsatt uten stagede filer; git diff --check bestod.

## Konkret kombinasjon som må gjennomføres før merge

1. Behold oppdatert main som grunnlag for en isolert samlet kandidat; bruk bare tilgangsdifferansen fra f5, ikke komplette gamle produktfiler. Piloten og dens fiktive volum/passord skal forbli urørt under dette.
2. I PrivateAccess må nyere mains privateClock-import, serverens Date-observasjon og fristtimer bevares. Kombiner ny mains VITE_PRIVATE_API-konfigurasjon for eksisterende oppsett med tilgangskandidatens eksplisitte VITE_PRIVATE_API_BASE=/private-api i nettbrettbygget. En definert, ugyldig tablet-base må fortsatt stoppe bygg/runtime; på HTTPS skal logout-markøren fortsatt være Secure. Ikke løs konflikten ved å velge hele én sides fil.
3. Behold nyere mains CORS Date-expose og nye notice-operations-rute når Secure-cookieendringene anvendes. Migrering 014 i nyere main skal ikke kjøres mot pilotens nåværende eller ordinære data. Ny samlet kandidat må bruke egen tom testdatabase og egne ressurser.
4. Root-.dockerignore påvirker ikke ordinære frontend-/backendbygg, som har egne ./frontend og ./backend som kontekst. Nettbrettets root-kontekst er eksplisitt allowlistet og privat inngang brukes. Ny mains vite.config.ts/demo.html er ikke med i denne allowlisten; det private bygget må fortsatt verifiseres som separat privat inngang uten fiktiv demo og med riktig relativ API-base. Ikke importer ukritisk den nye flersidekonfigurasjonen inn i nettbrettbygget.
5. Behold alle eksisterende main-logg-/issuepunkter og senere tekniske endringer. Dette worktree-et skal ikke gjeninnføre gamle åpne/lukkede statuser fra f5 over nyere main.
6. Kontroller gate-JWT, HTTPS-cookie/CSRF, proxy/fail-closed og ny faktisk API/DB-integrasjon på den samlede kandidaten. Utfør passende eksisterende frontend-/retensjons-/utloggingsregresjon isolert for det berørte felleslaget. Historiske 11.6-tester og fysisk f5-pilot teller ikke som gjennomført regresjon av den nye kombinasjonen.
7. Presenter endelig diff, testresultater, fryst målhode og eventuelle rester for eier før commit/merge/push. Revider hvis main flytter seg. Merge må ikke medføre tunnelstart, DNS-operasjon eller serviceinstallasjon. Ingen startup-hooks eller standard Compose-tunnel er innført i tilgangskandidaten.

## Avgrensning

Konflikten er identifisert og løsningsplanen konkretisert, men en samlet kandidat mot d5-main er ennå ikke laget, bygget eller testet. Ingen påstand om ferdig main-integrering fremsettes. Kjørende pilot er fortsatt f5; tilgansdata/hemmeligheter følger ikke med noen patch. Ekstern publisering/testing er separat godkjent av eier, og gir ingen commit-/merge-/push-godkjenning.
