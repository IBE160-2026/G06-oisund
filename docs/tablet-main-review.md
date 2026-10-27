# Integreringskontroll for nettbrettilgang, 2026-10-27

Senere sluttresultat for den faktiske f5-piloten: [tablet-pilot-result.md](tablet-pilot-result.md). Praktisk naturlig cookie-/øktutløp, ny MFA og bevart verdi er nå observert, og tunnelen er stoppet. Nedenstående integreringshistorikk skal ikke leses som deploy av den kombinerte main-versjonen.

## Oppdatert: godkjent commit/merge og testet kombinasjon

**Utført:** Merge-commit `ca1d6470fcab636fe9c754f02d78990e418f0cca` er ferdigstilt i tilgangsbranchen og lokal main er fast-forwardet til den etter eiers uttrykkelige godkjenning. Ingen push. De to opprinnelige lokale dokumentasjonsfilene i D:\IBE160 er bevart byte for byte og fortsatt henholdsvis endret/utracket. Hovedindex har ingen stagede filer. Alle 23 baseline-containere har uendret ID, StartedAt, restartteller og image; engangstestcontainere og preview-port 18481 er ryddet. Tunnelen er ikke startet/stoppet av merge-operasjonen. Kjørende fysisk pilot bruker fortsatt f5-baserte images; deploy av de kombinerte image-versjonene er en separat operasjon og ikke utført. Ingen ordinær migrering eller storyaksept er gjort.

Eier godkjente senere uttrykkelig commit og deretter merge, uten push. Tilgangsarbeidet ble committet som `35c4548`, og sesjonsloggen separat som `252616b`. Main på d5bf85d er nå kombinert i tilgangs-worktree-et før endelig commit/innfletting. Konflikten i PrivateAccess er løst ved at validert VITE_PRIVATE_API_BASE prioriteres for nettbrett, mens nyere mains VITE_PRIVATE_API og eksisterende loopback-default beholdes. PrivateClock/Date-observasjon, fristtimer, nye API-ruter og Date/CORS er beholdt. Ingen storyaksept er gitt av dette.

Det første gatewaybygget avslørte at parent-unntak i root-.dockerignore også slapp inn nye mains demo/Vite-konfigurasjon og lokale node_modules. Allowlisten er rettet ved å ekskludere innhold igjen før de eksplisitte unntakene. Dockerfile kopierer nå bare packagefiler, tsconfig og src eksplisitt, med separat privat index. Det korrigerte bygget er kontrollert uten demo.html og med relativ /private-api. Det første testimaget ble aldri satt i drift; ingen kjørende images/containere er erstattet.

| Ny kontroll av kombinert kandidat | Resultat |
|---|---|
| API-build, eget image main-review-d5 | Bestod |
| HTTPS/cookie/CSRF, nettverksløse testdobler | 14 bestod; kjent Starlette TestClient-deprecation |
| Ekte API/PostgreSQL i engangs-tmpfs på eget internt nett | 14 migreringer, gjentatt migrering, rollebegrensning, HTTPS-cookies/CSRF/feil origin/eierskap, samme-ID-replay/gjenåpning/utlogging bestod; ikke ekte TLS |
| Standard frontend TypeScript/Vite-build | Bestod med både tablet-base og alternativ legacy-API konfigurert |
| Ny isolert headless Edge-regresjon på 127.0.0.1:18481 | 3 bestod: relativ API prioritet og logout/reload, skjerming og bevart forslag ved suspensjon, serverklokkeutløp fra nyere main. Alle API-kall simulert og andre nettmål blokkert. Ingen ordinære API-er/DB-er brukt. |
| Privat gatewaybuild og innhold | Bestod, egen privat inngang uten demo og med /private-api |
| Ekte Nginx/proxy med syntetisk upstream/gate | 120 avvisninger med null avviste kall til upstream, gyldig identitet/Origin/CSRF/cookies/no-store/CSP og gate-nede fail-closed bestod |
| Standalone Compose | Bestod uten oppstart av tjenester |

Browserregresjonens første klokketest slo ut fordi en innledende API-respons allerede utløste forventet skjerming før klikket. Testen ventet deretter på ferdige innledende nettlesinger før klokkeendringen, og alle tre bestod. Produktets klokkevern ble ikke svekket. Ingen full Story 12-regresjon eller ny faktisk nettbrettprøve av kombinasjonen er påstått. Fysisk pilot kjører fortsatt f5-images; mergeresultat starter ikke tunnel/containere eller migrerer data. Naturlig Access-utløpsprøve etter Oslo 16:28 står separat åpen.

Planen nedenfor beskriver den opprinnelige lesekontrollen. Kombinasjons- og testpunktene ovenfor erstatter den tidligere opplysningen om at ingen samlet kandidat var laget.

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

Konflikten er løst, den kombinerte kandidaten er bygd og relevant isolert regresjon bestod som angitt øverst. Lokal main-integrering er gjennomført etter senere uttrykkelig commit-/merge-godkjenning; push er ikke godkjent eller utført. Kjørende pilot er fortsatt f5, og tilgangsdata/hemmeligheter følger ikke med Git. Naturlig Access-utløp og eksakt faktisk signert utløpt token er fortsatt separate, ikke praktisk verifiserte tilfeller. Dette er ingen generell påstand om risikofri drift eller full Story 12-godkjenning.
