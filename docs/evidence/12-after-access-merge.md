# Story 12.1/12.2 — ny regresjon etter tilgangsmerge

Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.

Jonas sin manuelle/fysiske akseptansetest av Story 12.1 og 12.2 gjenstår. Automatiske tester innebærer ikke brukeraksept.

## Siste versjonsavklaring og overlevering — 27. oktober 2026

| Grunnlag | Kontrollert versjon |
|---|---|
| Main før denne dokumentasjonspubliseringen | `83cdd2b344aa8ec717d42cd3ecd055daad97a222` |
| Kjørende isolert Story12-bygg og siste regresjonskjøring | `62a0cf4f67f2ce1ea2b0da78c76858a10d7adf11` |
| Produkt-/konfigurasjons-/testforskjell mellom disse | Ingen |
| Senere commits | `40bd15d`, `c4813f6`, `3c6282d`, `83cdd2b`: bare dokumentasjon og logger |

`git diff --name-only 62a0cf4..83cdd2b` viser kun de to sesjonsloggene, issues.md, docs/tablet-main-review.md, docs/tablet-pilot-result.md og docs/tablet-tunnel-setup.md. Dermed beholdes regresjonsevidensen nedenfor som gyldig også for produktet i gjeldende main; endret commit-ID alene krever ikke ny kjøring. Dokumentasjonspubliseringen i denne økten endrer heller ikke produktet.

**Nye kontroller i denne økten:** Alle kildeinnganger i de seks regresjonsrapportene (build/checks/backend/fictional/demo/browser) er hashkontrollert mot arbeidskopien; rålogg-hash og genererte kjørte tester er også kontrollert. Begge API-ers 67 backendfiler og tidligere serverte filhash matcher siste runtime-evidens. Alle seks bygde frontendfiler er hentet over HTTP og matcher dist. Begge API-er er friske. De bekreftede testdatoene 2./3. januar 2031 finnes, kontrollert med en skrivebeskyttet databasetransaksjon. Alle 23 containere har uendret ID, image, oppstartstid, restartteller og labels gjennom kontrollen. [Versjons-/miljøevidens](12-current-main-readiness.json), [ny runtimekontroll](12-current-main-runtime.json).

Det midlertidige lesekontrollskriptet stoppet først fordi forventet antall regresjonsrapporter feilaktig var satt til sju. Dette ble korrigert til eksplisitt kontroll av de seks modusene ovenfor; den komplette kontrollen bestod. Ingen produktkode, testpåstand eller historisk evidens ble endret. Skriptet kjøres som `& $py tmp/story12-refresh/reconcile.py`; dets kilde følger [evidensen](12-after-access-logs/reconcile.py) for etterprøvbarhet.

**Beslutning:** Ingen ombygging og ingen ny kjøring av funksjonsregresjonene var nødvendig. De siste faktiske regresjonsresultatene er fortsatt 455 private backendtester, 86 private nettlesertilfeller, 19 fiktive API-tester, 27 demo/fiktive nettlesertilfeller, 73 faktiske API-/PostgreSQL-kontroller, 29 verktøykontroller og tre tablet-transporttester, alle bestått på 62a0cf4. De er ikke rapportert som kjørt på nytt i denne økten. Tidligere feil og begrensninger står nedenfor. Rålogger fra siste kjøring er bevart under [12-after-access-logs](12-after-access-logs/), med opprinnelige hash i JSON-evidensen.

**Bruk dette miljøet:** `ibe160-story12-integration`, <http://127.0.0.1:15312/private> for 12.1, deretter `/demo` og `/` på samme port for 12.2. API-er 18312/18313. Ikke bruk 15323/18323/18324, som tilhører separat 12.3, eller den tidligere tilgangspiloten/gateway18081. Ingen eksponering, tilgangsregel, privat datagrunnlag, ordinær tjeneste eller annet testmiljø er endret. Ingen 12.3-fletting eller oppstart av 12.4.

Veiledningen er kontrollert mot identiske produktkilder og kjørende bygg. **Første manuelle steg:** Åpne nytt InPrivate-vindu på PC-en, gå til <http://127.0.0.1:15312/private>, logg inn med den syntetiske kontoen fra `.private-runtime/story12-manual-credentials.json`, og åpne 2. januar 2031-planen. Følg deretter [12.1 A–F og stoppunktet](../testveiledning-12-1-deretter-12-2.md). Start 12.2 bare hvis 12.1 ikke krever rettinger eller har uavklarte resultater.

Ferdige veiledninger, denne rapporten, relevant JSON-/rålogevidens og separat sesjonsdokumentasjon publiseres nå på main etter uttrykkelig autorisasjon. Produktgrunnlaget forblir 62a0cf4-ekvivalent. Nye commitreferanser og kontroll av origin dokumenteres i sesjonsloggen og sluttmeldingen.

## Historisk regresjonsøkt fra 62a0cf4

Arbeidsgrunnlag: lokal `main`, `62a0cf4f67f2ce1ea2b0da78c76858a10d7adf11`, kontrollert 27. oktober 2026. De to lokale testveiledningene fra forrige økt er bevart. Ingen produktkode er endret i denne regresjonsøkten. Senere lokal loggcommit endrer ikke det testede produktgrunnlaget. [Testveiledning: 12.1 først, deretter 12.2](../testveiledning-12-1-deretter-12-2.md).

## Avgrensning og miljø

Kun `ibe160-story12-integration` bygges og brukes til faktiske database-/API-/nettlesertester. Frontend 15312, fiktiv API 18312, privat API 18313, egne eksisterende syntetiske volumer og testkontoer. Den faktiske integrasjonsverifikasjonen nullstiller bare dette miljøets fiktive database og starter egne API-er/databaser på nytt. Private manuelle testdata bevares; forberedelsen er additiv. Ingen ordinær migrering, tunnelendring eller pilotutrulling.

Det nye tilgangsarbeidet berører autentiseringskonfigurasjon, cookieflagg, tillit til proxy-headere og frontendens API-adressevalg. Derfor kjøres både Story12-flytene og transportregresjonen. Tabletvarianten bygges separat under ignorert `frontend/tmp/tablet-refresh-dist`; uendrede transporttester bruker simulerte API-er og egen preview på 18481. Dette kvalifiserer ikke faktisk Cloudflare-/nettbrettdrift av den nye kombinasjonen.

## Kommandoer og nye resultater

Kjørt fra `D:\IBE160`, med `$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'`. Rålogger og tidsstemplede JSON-filer er nye resultater fra denne økten; tidligere 12-integrated-handoff-resultater gjelder tidligere grunnlag.

```powershell
& $py scripts/verify-story12-integration.py up
& $py scripts/verify-story12-checks.py checks
& $py scripts/verify-story12-checks.py stop-preview
& $py scripts/verify-story12-checks.py build
& $py scripts/verify-story12-integration.py verify
& $py scripts/verify-story12-checks.py serve
& $py scripts/verify-story12-checks.py backend
& $py scripts/verify-story12-checks.py fictional
& $py scripts/verify-story12-checks.py demo
& $py scripts/verify-story12-checks.py browser private-access.spec.ts private-retention.spec.ts private-recovery.spec.ts private-notice-recovery-integration.spec.ts private-crossday-notices.spec.ts private-notice-reader.spec.ts
& $py scripts/verify-story12-integration.py prepare
```

| Kontroll | Ferskt resultat / evidens |
|---|---|
| Bygg av isolerte tjenester | Bestod; `12-integration-real-20261027T151253469417Z-daaaf59e5d02.json` |
| TypeScript/Vite produksjonsbygg | Bestod; `12-integrated-build-20261027T151322415424Z-51ec5875.json` |
| Verktøyenes avvisning/feil/evidens | 29 bestod; `12-integrated-checks-20261027T151314848823Z-71a6a1c2.json` |
| Faktisk HTTP/PostgreSQL-integrasjon | 73 kontroller bestod, opprydding bestod; `12-integration-real-20261027T151337711402Z-6a081a1e1299.json` |
| Privat backend inkl. ny transport | 455 bestod, én kjent Starlette TestClient-deprecation, 605,74 s; `12-integrated-backend-20261027T151434577486Z-367d8c98.json` |
| Faktisk fiktiv API | 19 bestod; `12-integrated-fictional-20261027T151446666486Z-22d2b33a.json` |
| Demo + faktisk fiktiv nettleserflyt | 27 bestod; `12-integrated-demo-20261027T151450064458Z-a3c6c73e.json` |
| Berørte private nettleserpakker | 86 bestod i 9,1 min, exit 0 og uendrede kilde-/kjørte testfiler; `12-integrated-browser-20261027T152516149301Z-40082d4a.json` |
| Relativ tablet-API, logout/reload, skjerming, serverklokke | 3 bestod; [kommandoer og hash](12-after-access-tablet.json), rålogg `tmp/story12-refresh/tablet-browser.log` |
| Kilde-/serverte filhash og helse | Bestod; [runtime-evidens](12-after-access-runtime.json) |
| Additiv klargjøring av manuell testkonto | Bestod; `12-integration-real-20261027T153457287239Z-bb3ab058cc61.json` |

Alle ovennevnte verktøykjøringer bestod med uendrede kildeinnganger. Den private nettleserkjøringen omfatter hele de seks navngitte pakkene, inkludert reelle API-stopp/start og retensjon med fast/treg enhetsklokke. Det er ikke en ny full 479-tilfellers kjøring. Ingen produktretting var nødvendig.

Sluttkontrollen etter alle tester/klargjøring bekrefter at begge API-ers backendfiler matcher hosthash, servert HTML og refererte JS/CSS matcher `dist`, og begge API-er er friske. Preview 15312 står klart med det isolerte bygget. Docker-metadata før/etter ligger i ignorert `tmp/story12-refresh/baseline.txt` og `final.txt`: alle 19 containere utenfor integrasjonsprosjektet har identisk ID, image, StartedAt, restartteller og labels. Ordinære tjenester, andre storymiljøer og tilgangspiloten er bevart.

Rapport, testveiledninger og JSON-evidens er lagret lokalt. Bare sesjonslogg og oppdatert issues-fil committes lokalt etter beståtte kontroller, i tråd med prosjektets loggoppskrift. Ingen push er utført i denne økten.

Den faktiske integrasjonsverifikasjonen dekker avviksopprettelse, serverutstedt original-ID, samme-ID-gjentakelse, konflikt/utløp/eierskap, tapt akseptert svar og oppslag, uavhengighet fra slettet dag, restart, retensjon/purge og fiktiv reset uten endring av private tabeller.

Transporttesten feilet først 3/3 fordi miljøvariabler ble satt ved preview-oppstart, mens `npm run start` serverer et allerede kompilert loopbackbygg. Ingen produktfeil er utledet av dette. En separat tabletbuild med `VITE_PRIVATE_API_BASE=/private-api` og alternativ `VITE_PRIVATE_API=http://127.0.0.1:18313` ble deretter laget. Første oppstart av den midlertidige preview-konfigurasjonen hadde feil relativ arbeidsmappe og ble avvist før testkjøring. Med eksplisitt `cwd=D:/IBE160/frontend` bestod alle tre uendrede tester. Original feil finnes under `tmp/tablet-main-browser-results`, oppstartsfeilen i `tmp/story12-refresh/tablet-browser-startup-failure.log`. Ingen påstander ble svekket, og Story12-dist ble ikke erstattet av tabletvarianten.

## Manuell aksept og begrensninger

Begge storyene beholder `review` / `in-review`, med eieraksept ventende. Test 12.1 først; ved feil, endringsbehov eller uavklart resultat stopper 12.2. Se [testveiledningen](../testveiledning-12-1-deretter-12-2.md).

Den kjørende tilgangspiloten bruker fortsatt sitt tidligere image. Denne økten deployer ikke Story12-bygget til pilotadressen. Naturlig Access-utløp, faktisk ny fysisk enhetskvalifikasjon og allerede åpne senere storypunkter er ikke løst av automatiske tester. Simuleringens faste aktiviteter/lesetid og manglende reell PDF-tolking er fortsatt dokumenterte begrensninger.
