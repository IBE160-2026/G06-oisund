# Nettbrettilgang integrert med godkjent Epic 11

**Senere oppdatering 2026-10-27:** Eier har nå godkjent commit/merge uten push. Kombinasjonen med nyere main og den løste API-konfigurasjonskonflikten er bygd og testet isolert, inkludert 14 transporttester, 14 migreringer i engangs-DB, 120 proxynektprøver og 3 fokuserte browserregresjoner. Se siste avsnitt øverst i tablet-main-review.md. Ingen kjørende pilot/ordinære tjenester er oppdatert av Git-arbeidet; fysisk pilot er fortsatt den godkjente f5-baserte versjonen. Ingen ny storyaksept er gitt.

**Ny integreringsstatus 2026-10-27:** Piloten bygger fortsatt på f5ffa4b, men main har senere fått tekniske Story 12-endringer i annen chat. Én faktisk tekstkonflikt er funnet i PrivateAccess.tsx. Se [ny main-kontroll og konkret integreringsplan](tablet-main-review.md). Den nedenstående statusen er historikk, ikke bevis for at tilgangskandidaten er ferdig kombinert med ny main. Gjeldende godkjent pilotpublisering og eksterne/fysiske prøver står i tablet-tunnel-setup.md.

Senere status: eier har godkjent lokalpilotens trinn 1. Den kjører nå uten tunnel/DNS; se [utført lokalpilot](tablet-local-pilot.md) for runtime-kontroller, oppstartsrettelser og stoppkommandoer. Denne rapportens tidligere «ingen oppstart»-status er integreringshistorikk, ikke nåværende driftstilstand.

Dato: 2026-10-26. Status: lokal, uprøvd ekstern integreringskandidat. Ingen publisering, commit, staging, merge eller push.

## Kilde og isolasjon

Eier bekrefter at 11.6 og retrospektivet er godkjent og pushet. Lokal main og origin/main peker på `f5ffa4bf64696b8e1abf910ccd8ac106663d30a9`. Dette er kandidatens eksakte base. Implementeringscommit er `81075941241d004ff2a61ee858ccd1201ffd33a3`; godkjenning/retrospektiv er dokumentert i `55578eca9146d3fb7124223c9ab0ebb65259754b`. Ingen ny fetch eller uavhengig avlesning av GitHub er nødvendiggjort eller utført; remote-tracking-ref og brukerbekreftelse er grunnlaget for publiseringsstatus.

Ny branch: `setup/tablet-remote-access-11-6`.
Worktree: `C:\Users\Jonas\.codex\.chatgpt-projects\g-p-6ab6b4c1c6888191a96d3242fab912b4\tablet-access-11-6`.

Opprinnelig `setup/tablet-remote-access` på 11.4 er beholdt med sine ukommitterte forberedelser. Desktop-verktøyet for worktree kunne ikke finne repository fra prosjektmappen; derfor ble vanlig git worktree add brukt, med tillatelse til nødvendige delte Git-metadata. Dette bytter ikke branch eller index i D:\IBE160. Ingen checkout eller filendring i hovedarbeidsmappen, og ingen ordinær container-/databaseoperasjon, er utført.

## Overføring og gjennomgang

Bare de fire eksplisitte tilgangspatchene ble anvendt med git apply uten --index og uten konflikt:

- auth.py: eksplisitt HTTPS-modus og kanonisk origin, ellers eksisterende loopback-modus.
- private_main.py: Secure for auth-/CSRF-cookie og sletting.
- run.py: ingen tillit til proxy-headere.
- PrivateAccess.tsx: kun godkjent relativ API-base og Secure logout-markør på HTTPS.

Øvrige nye deploy-/test-/skript-/dokumentasjonsfiler ble overført fra en eksplisitt liste. Ingen runtime-filer, hemmeligheter, ordinære data eller ukommittert produktkode fra hovedarbeidsmappen ble kopiert. 11.5-ruter, migration 013, 11.6-recovery, epoch/generasjonsvern og status-før-retry er bevart fra den godkjente basen. Bare de fire nevnte sporede produktfilene har differanse mot base; ingen story-/retrostatus eller Epic 12 er endret.

Cloudflare-valgene og brukerbekreftelsene, team/hostname/AUD og de gjenværende sikkerhetsgrensene står i tablet-access-security.md. Maler har fortsatt plassholdere. Ingen faktisk runtime-konfigurasjon eller tunnellegitimasjon er opprettet.

## Utført mot denne kandidaten

| Kontroll | Resultat / avgrensning |
|---|---|
| Produksjonsbygg | TypeScript/Vite privat inngang og nytt Nginx-image `ibe160-tablet-gateway:11-6` bestod. Nytt API-image `ibe160-tablet-api:11-6` bestod. Låste, tidligere installerte avhengighetslag ble gjenbrukt fra Docker-cache; dette var ikke ny avhengighets-/sårbarhetsrevisjon. Ordinære images ble ikke bygget om. |
| HTTPS/cookies/CSRF | 14 tester bestod i eget nettverksløst, rootløst, read-only API-image med testdobler for auth/DB. Én kjent TestClient-deprecation-advarsel. |
| JWT | 13 tester bestod med ekte RSA/PyJWT, fiktive nøkler og ingen ekstern nettforbindelse. |
| Proxy/gate | Ny gateway fra 11.6: 5 beskyttede side-/asset-/API-tilfeller × 24 manglende/ugyldige tokenvarianter ble nektet; null avviste kall nådde syntetisk upstream. Gyldig identitet, Origin/CSRF/cookies, Host/stier, no-store/CSP og gate-nede fail-closed bestod. |
| Ekte API/PostgreSQL | verify-tablet-api.ps1 bestod: 13 migreringer og gjentatt migrering, approlle uten SUPERUSER/CREATEDB/CREATEROLE/REPLICATION, HTTPS-modus login, CSRF-/feil-origin-nekt, kontooverskridende nekt, lagring/reåpning, kvitteringsoppslag, samme operasjon uten duplikat og logout-nekt. Ny minnebasert DB på eget internt nett, ingen hostporter/datavolumer, bare nye synthetic-kontoer. FastAPI TestClient, ikke faktisk TLS/nettleser. Den disponible testdatabasen bruker én tilfeldig testhemmelighet til bootstrap/approlle; produksjonsmalen beholder separate hemmeligheter som tidligere isolert testet. |
| Testoppsettfeil | Første minne-DB-prøve fikk readiness-timeout; containeren hadde stoppet og ble fjernet før logger kunne avleses, så eksakt intern feil er ikke bevist. Etter tmpfs-eierskap til låst images postgres UID/GID 70 kom en PowerShell-siteringsfeil ved kommaseparert mountvalg. Siteringen ble rettet, og hele API/DB-prøven bestod. Ingen produktkode eller runtime-sikkerhet ble svekket. |
| Compose og opprydding | test-tablet-config.ps1 bestod mot eksempelmiljø uten tjenesteoppstart. Egne proxy-/DB-testcontainere og testnett fjernet; minne-DB forsvant med containeren. Midlertidig testpassordfil fjernet. Nye lokale test-images beholdes. git diff --check bestod. |

Reproduser fra denne checkouten etter bygg av de to egne kandidatimages:

~~~powershell
./scripts/test-tablet-config.ps1 -EnvironmentFile deploy/tablet/.env.tablet.example
./scripts/verify-tablet-proxy.ps1 -GatewayImage ibe160-tablet-gateway:11-6
./scripts/verify-tablet-api.ps1 -ApiImage ibe160-tablet-api:11-6
~~~

Disse skriptene oppretter bare egne engangstester. Ikke bruk prosjektets ordinære private-verifikator til denne kontrollen; eksisterende browser-fixtures har faste porter/prosjektnavn og kan operere et annet miljø. Den godkjente 421 backend-/479 browser-regresjonen er historisk dokumentasjon fra 11.6, ikke en ny test av denne kandidaten. Ingen påstand om ny full browserregresjon fremsettes.

## Gjenstående før aktivering

### Oppfølgende eksponeringskontroll, 2026-10-26

Eier opplyser at husets ruter administreres av faren, som er utvikler og prioriterer sikkerhet; GlobalConnect er leverandør. Eier er trygg på at sikkerhetsfunksjoner er aktivert og utilsiktede åpninger unngått. Dette registreres som eiers opplysning, ikke avlest ruterpolicy. Ingen rutertilgang eller endring er utført. Cloudflare Tunnel bruker utgående forbindelse; ruterinnlogging eller endring av portvideresending er ikke i seg selv et teknisk krav. Tidligere formulering om at hele muligheten var avhengig av ruterkontroll var for kategorisk. Vi fortsetter uavhengige lokale kontroller uten ruterinnlogging; dette er ikke ny godkjenning til aktivering eller en påstand om verifisert WAN-beskyttelse.

Ny lesekontroll på desktop viste TCP 5173/8000/8001 bare på 127.0.0.1. Ingen lyttende TCP-porter i det kontrollerte øvrige settet 22/80/443/2375/2376/3389/5432/5985/5986/18081/18083. Docker viste samme loopback-bindinger og begge PostgreSQL-containere uten publiserte hostporter (5432/tcp alene er ikke en hostpublisering). TermService og WinRM var stoppet; netsh portproxy-listen var tom. Alle tre Windows-brannmurprofiler var ON med effektiv standardpolicy BlockInbound,AllowOutbound. Første PowerShell-profilavlesning viste NotConfigured; effektiv policy ble derfor lest separat med netsh.

Aktive innkommende tillatelsesregler ble inventert. Den brede tabellvisningen skjulte vilkår og teller ikke som full regelrevisjon. Etterfølgende strukturert utvalg for Docker/Node/Python-programmer viste to Node.js-regler: Public-profil, TCP henholdsvis UDP, alle lokale porter, alle fjernadresser, program C:\program files\nodejs\node.exe. Ingen Docker-/Python-programregel ble returnert av akkurat dette utvalget. Eksisterende øvrige program-/tjeneste-/pakkeregler er ikke fullstendig vurdert. Node-reglene endrer ikke loopback-bindingen til de observerte appportene; de må tas med ved eventuell senere tjeneste som lytter på LAN/wildcard. Ingen brannmurregel, tjeneste eller container ble endret. Uavhengig prøve fra mobilnett og samlet IPv4/IPv6-/alternativ-rute-verifikasjon gjenstår før en dokumentert publiseringsbeslutning. Ikke utled at alle innkommende tjenester er blokkert bare fra standardpolicyen.

Integreringsavhengigheten til godkjent 11.6 er nå løst for den separate kandidaten. Hovedarbeidsmappen trenger fortsatt ingen endring. Velg denne kandidatens reviewede filer og base for en eventuell senere leveranse; ikke erstatt 11.6 med gamle 11.4-filer. Ingen Git-integrering/commit til main er godkjent her.

Følg resten av aktiveringsplanen, tilbakeføringen og Lenovo-matrisen i tablet-access-security.md. Første faktiske pilot skal ha egne fiktive data. Krever fortsatt konkret godkjenning av pilotoppstart, tunnelopprettelse/legitimasjon, eventuell installasjon av cloudflared, DNS-rute og manuell tunnelstart. Ingen vedvarende tjeneste er godkjent.

Før publisering gjenstår ruter/UPnP/DMZ/IPv6 og alternative eksterne ruter; oppdatert avhengighets-/binærkontroll; faktisk lokale credentials/ACL; les-tilbake av cacheuttrykk/regelrekkefølge; og isolert pilot med faktisk gateway/API/DB. Ekte Cloudflare-MFA/JWT/TLS, uinnlogget/feil identitet, ugyldig/utløpt token på side og API, tilbakekalling/rask stenging og Lenovo/Android/Brave hjemme/mobil må dokumenteres ved kontrollert aktivering. Intet av dette kan regnes som bestått av de lokale prøvene.
