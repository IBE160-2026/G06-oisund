# Sluttresultat: isolert nettbrettpilot, 27. oktober 2026

## Resultat og sluttstatus

Den fiktive piloten er praktisk testet fra Lenovo Pad med Android/Brave på hjemmets Wi-Fi og via telefonens hotspot med mobildata. Access/MFA, appens egen innlogging, lagring/gjenåpning, observert nettbrudd, tilbakekalling og naturlig cookie-/øktutløp ga forventet oppførsel i forløpene nedenfor. Dette er avgrenset pilotevidens, ikke en generell sikkerhetsgaranti eller godkjenning av Story 12.

Eier bekreftet til slutt ny MFA, bevart sist lagret fiktiv verdi, utlogging fra appen og tunnelstopp med Ctrl+C. Agentens etterkontroll fant **null cloudflared-prosesser og null lyttere på metrics-port 18083**. De fire pilotcontainerne kjører fortsatt lokalt; API/DB er healthy. Eneste publiserte pilotport er fortsatt **127.0.0.1:18081**. Database/API/gate har ingen publiserte hostporter; Docker-visning av 5432/tcp er ikke en hostpublisering.

Den godkjente DNS-posten og publiserte ruten er ikke fjernet: app.bussassistent.com → navngitt tunnel 4aecb83e-cf83-4112-8f76-9a564252e1fe → lokal gateway. Ingen connector kjører ved sluttkontrollen. Cloudflares innloggingsside kan fortsatt være offentlig tilgjengelig; det betyr ikke at lokalappen nås. Ingen Windows-tjeneste eller autostart er installert. Apputlogging er ikke en påstand om at alle gjenværende Access-/administratorsesjoner er avsluttet.

## Fysisk og ekstern evidens

| Prøve | Observert resultat og avgrensning |
|---|---|
| Uinnlogget nettside | Privat desktop-Brave og Lenovo viste Access før appen. |
| Direkte API uten gyldig Access | Ni eksterne GET-kall mot side og to API-adresser med manglende/malformed/alg-none assertion ga 302 til forventet HTTPS Access-innlogging, uten redirect-følging eller dataskriving. Dette er ikke en faktisk prøve med signert utløpt JWT. |
| Feil identitet | Annen, ikke innmeldt Cloudflare-konto ble avvist med medlemsbegrensningsmelding før appinnlogging. Direkte API-adresse førte til Access uten data. Eksakt e-post-policy mot et annet kontomedlem er ikke isolert prøvd; ingen ekstra medlem ble lagt til. |
| MFA og appinnlogging | Eier måtte gjennom både Cloudflare-kontoens MFA og separat Access-MFA, deretter pilotens egen appinnlogging. På Lenovo ble MFA og pilotinnlogging bekreftet på både Wi-Fi og mobilnett. |
| Lagring/gjenåpning | Fiktive testverdier ble bekreftet lagret og stod etter oppdatering/gjenåpning på desktop og Lenovo, både Wi-Fi og mobilnett. Ingen ordinære data ble brukt. |
| Nettbrudd | Tunnelstopp på desktop og fysisk nettbrudd på Lenovo medførte skjerming ved ubekreftet tilgang og ingen falsk lagringsbekreftelse. Inndata kom tilbake etter gjenoppkobling; ny eksplisitt lagring og gjenåpning beholdt verdien. Alle timingvinduer for et tvetydig serverfullført skriveforsøk er ikke fysisk fremprovosert. |
| Apputlogging | Bekreftet, vedvarte etter refresh og tilbake/fram uten privat plan. Direkte API viste Logg inn på nytt uten utkast; HTTP-status ble ikke avlest i det skjermbildet. |
| Faktiske cookieflagg | Eier kontrollerte private_session/private_csrf i desktop-Brave: Secure, HttpOnly, SameSite Strict, Path /. Verdiene ble ikke delt. |
| Faktisk privat cache-respons | Autentisert GET /private-api/drafts: 200 OK, Cache-Control no-store, CF-Cache-Status DYNAMIC, ingen Age. Ikke en full kontroll av alle svar-/feilvarianter. |
| Faktisk CSRF-nekt | Autentisert POST /private-api/drafts med ufullstendig JSON uten X-CSRF-Token: 403 og forventet generisk nekt. Ingen gyldig skrivepayload eller hemmelige verdier ble vist. |
| Access-tilbakekalling | Eier valgte sin bruker → Revoke sessions. Etter ett minutt skjulte neste leseforsøk på Lenovo innholdet. Direkte API krevde Access uten utkast. Ny MFA lot eier hente sist lagret verdi igjen. Ingen permanent identitetssperre eller eksakt tilbakekallingslatens er bevist. |
| Naturlig cookie-/øktutløp | Oppgitt CF_Authorization-expiry var 2026-10-27T15:27:06.168Z, tilsvarende 16:27:06 Oslo. Ved retur 16:33 viste appen privat innhold skjult; direkte API krevde Access uten utkast. Ny MFA ble krevd, sist lagret verdi var bevart. Eksakt tidspunkt/årsak til første skjerming ble ikke observert. Dette er et forventet praktisk utløpsforløp, ikke isolert avvisning av en fortsatt innsendt, signert utløpt JWT. |
| Rask stenging | Eier stoppet manuelt med Ctrl+C flere ganger. Endelig prosess-/metrics-kontroll bekrefter stopp, uten å stoppe ordinære tjenester. |

Fysiske nettleserresultater er eiers rapporter/skjermbilder; agentens automatiserte kontroller er eksplisitt skilt ut. Ingen passord, tunnel-token, JWT eller cookieverdier er lest inn for å dokumentere resultatene.

## Kildeversjon og isolerte tester

Den fysisk testede piloten kjører fortsatt images bygd fra godkjent Epic 11, base **f5ffa4b**, med de forberedte tilgangsendringene. Senere main-endringer er ikke satt i drift i piloten.

Tilgangskoden ble committet som 35c4548, kombinert med nyere main i merge-commit ca1d647 og flettet inn lokalt i main. Sluttdokumentasjon/logg fulgte til 62a0cf4. Senere lokal main-loggcommit 40bd15d er hentet inn i tilgangs-worktree-et før denne sluttrapporten; den andre chattens åpne punkter er bevart. Ingen push er utført av tilgangsarbeidet.

Den kombinerte kildekandidaten bestod 14 nettverksløse transporttester, en ekte API/DB-prøve med 14 migreringer bare i engangs-tmpfs-database, 120 proxyavvisninger/fail-closed, tre fokuserte Edge-regresjoner samt frontend-/privat gatewaybygg og standalone Compose-kontroll. Gatewaybygget er verifisert uten demo.html og med relativ /private-api. Tidligere JWT-tester med fiktive RSA-nøkler dekket blant annet signatur, issuer, audience og exp; det er syntetisk evidens. Detaljer/oppstartsfeil og rettelser er dokumentert i [integreringsrapporten](tablet-main-review.md).

Ved kodeintegreringen ble de to daværende lokale dokumentasjonsendringene i D:\IBE160 bevart byte for byte. Alle 23 baseline-containere var uendret i ID/StartedAt/restartteller/image etter test/merge. Ingen ordinære data ble migrert, og ingen eksisterende container ble stoppet/startet/ombygd av integreringen. Ingen story-/retrostatus er satt av tilgangsarbeidet.

## Gjenværende arbeid og begrensninger

1. **Ny kombinert versjon er ikke fysisk testet eller deployet.** Relevant isolert integrasjon bestod, men full manuell 12.1/12.2/12.3-aksept og tester i den andre chatten må knyttes til riktig kilde-/imageversjon. Tilgangspiloten gir ingen slik storyaksept. Overgang til nyere images eller ordinære data er separat arbeid; denne sluttrapporten starter ingen tjenester eller migreringer.
2. **Faktisk signert utløpt Access-JWT er ikke replay-testet eksternt.** Syntetisk exp-validering, praktisk naturlig cookie-/øktutløp og tilbakekalling har forskjellig bevisverdi. Ingen ekte JWT er samlet inn for å lukke dette punktet.
3. **Eksponeringskontrollen har grenser.** Observerte appporter er loopback, DB er upublisert, og tunneloppsettet har ingen private LAN-ruter. Ruterens UPnP/DMZ/IPv6-policy er eiers/farens opplysning, ikke avlest konfigurasjon; full uavhengig IPv4/IPv6-portskanning er ikke gjort. Ingen ruter-/brannmurendring er utført.
4. **Enkelte sikkerhetsforløp er bare isolert testet.** Faktisk feil identitet ble stoppet ved medlemsbegrensningen; alle e-post-/origin-/CSRF-/cache-/utløpsvarianter er ikke fysisk testet. Avhengighetskontroller uten kjente funn ved klargjøringen og gyldig binærsignatur er ikke en full OS-/supply-chain-/penetrasjonstest.
5. **Varig drift er ikke satt opp.** Ingen autostart, tjenesteinstallasjon eller ordinær datatilgang er levert som aktiv drift. Tunnel-token forblir lokalt utenfor Git; pilotens øvrige runtime-filer er Git-ignorert og tilgangsbegrenset. Sikre senere rotasjon, sikkerhetskopi og en eksplisitt deploybeslutning før eventuell ordinær bruk.

## Senere start og tilbakeføring

Ingen ny aktivering er utført ved avslutningen. Eksakt foreground-kommando og tilhørende team/AUD står i [tunnelveiledningen](tablet-tunnel-setup.md); senere operatør må kontrollere at kilde, images og fiktive/ordinære data er de avtalte før oppstart.

Rask stenging er Ctrl+C i den ene foreground-terminalen; ved uventet innhold kan bare pilotgatewayen stoppes med den prosjektavgrensede Compose-kommandoen i [lokalpilotrapporten](tablet-local-pilot.md). Full tilbakeføring fjerner den ene publiserte ruten og tilhørende CNAME etter separat beslutning, mens Access-beskyttelsen beholdes. Ikke slett databasevolumer eller kjør prune. Ved tokenkompromiss kreves både rotasjon og frakobling av eksisterende connectors; vanlig økttilbakekalling er ikke permanent sperring av en fortsatt tillatt identitet.
