# Gjeldende fjernmiljø: godkjent main med 12.4

Oppdatert 28. oktober 2026. Adresse: https://app.bussassistent.com/private.
Denne veiledningen erstatter historiske oppstarts-/stoppstatus i tablet-local-pilot.md,
tablet-tunnel-setup.md og tablet-pilot-result.md. De rapportene beholdes som historikk.
Godkjenningsgrunnlag: [12.4-integrasjon](evidence/12-4-main-integration.md) og
[eieraksept](evidence/12-4-owner-acceptance-2026-10-28.md).

## Kilde og faktisk drift

Fersk fetch bekreftet ren lokal main og origin/main lik
`a48f2132fd0059b21b9581bf27d337cb1561d55b` før bygg. Både akseptert 12.4 og
mobilretting c0e809f er inkludert. Senere commits i denne økten endrer bare drift og
dokumentasjon, ikke deployet produkt. Ingen 12.5 eller nye produktfunksjoner.

| Del | Aktiv identitet |
|---|---|
| API | `ibe160-tablet-api:main-a48f213`, `sha256:26ee88cb518aefb2b2733b6f96fec909c061fe58becd42981ebaf251e134ac12` |
| Gateway/frontend | `ibe160-tablet-gateway:main-a48f213`, `sha256:50242b65f742441d0928d00775640715ce4748b4420519fbca9ece5b54253bfe` |
| JavaScript | `index-DOc41X9S.js`, SHA256 `2d4ecd349dfd74f077210bc32d9b5e385c878c007b4111d45252642f09e54602` |
| API/gateway OCI revision | `a48f2132fd0059b21b9581bf27d337cb1561d55b` |
| Database | Eksisterende `ibe160-tablet-prep_tablet_pg`; PostgreSQL-image og rollemodell bevart |
| Skjema | 001–014; ordinær idempotent migrering ved API-oppstart, ingen nye migreringer nødvendig |
| Access-gate | Eksisterende `ibe160-tablet-access-gate:11-6`, image `25e40c61e6a734c2b19daaeb5c3eb7230f424a917992f3f33e100a2e309484c2` |

Fjernmiljøets eksisterende kontoer, passordhash, senere endringer og alle tabellrader
ble bevart. Ingen gammel kontokopi ble importert. Miljøene synkroniseres fortsatt ikke.

## Stabil lokal driftsmappe

`C:/Users/Jonas/.codex/.chatgpt-projects/g-p-6ab6b4c1c6888191a96d3242fab912b4/operations`
er privat og utenfor applikasjonsrepoet, ACL-begrenset til eier og SYSTEM.

- `compose.yaml`, `.env.tablet`, `build-identity.json`: aktiv konfigurasjon og låste image-ID-er.
- `runtime/tablet/`: bare `postgres-password`, `bootstrap-password` og `access-policy.json`.
- `releases/a48f2132fd0059b21b9581bf27d337cb1561d55b/`: eksport av verifisert Git-main. Ordinære bygg ble gjort før isolerte testadaptere ble lagt til. Ingen aktiv kildekodemontasje til API.
- `archived-config/`: tidligere override, byggmetadata og pilotinnlogging, bevart privat og ikke aktiv.
- `backups/20261028-pre-a48f213/`: database/config/source/containerbaseline, restorebevis, stashreferanse og kontrollert fullarkiv av gammelt worktree. Innholdet skal ikke publiseres eller dumpes til logger.
- `verification.json`, `browser-report-39.json`, `browser-report-18.json`: lokale sluttresultater. Tilgjengelige mislykkede testadapterforsøk er bevart separat.
- `deploy.py`, `check-server.cjs`: denne øktens private metode og syntetiske testadapter. `deploy.py prepare/configure/test-prepare/cleanup-old` er engangssteg og skal ikke gjenkjøres som ordinær oppstart.
- `tunnel.pid`, `tunnel.stdout.log`, `tunnel.stderr.log`: lokal prosessinformasjon. Ikke publiser hele tunnel-/containerlogger eller konfigurasjon.

Alle fire produksjonstjenestene bruker nå compose fra operations. Database/API/gate
monterer bare stabile operations-filer, ikke gamle worktrees. Prosjektnavn og datavolum
er bevisst beholdt. Bare gateway er publisert, på `127.0.0.1:18081`; API/DB/gate har ingen vertsporter.
API kjører eksplisitt HTTPS-modus for app.bussassistent.com. Frontend er bygget med
`VITE_PRIVATE_API_BASE=/private-api` og Nginx videresender dette til privat API.

## Start og stopp

Fra et oppdatert repo, med Docker Desktop i gang:

```powershell
$runtime = 'C:/Users/Jonas/.codex/.chatgpt-projects/g-p-6ab6b4c1c6888191a96d3242fab912b4/operations'
./scripts/start-tablet-production.ps1 -RuntimeRoot $runtime
```

Skriptet kontrollerer eksakte image-ID-er/revision, bruker bare lokal compose uten
nybygg, venter på tjenester og starter eksisterende tunnel skjult som selvstendig
prosess. Gjentatt kjøring gjenbruker en kontrollert eksisterende connector. Det er
ikke installert Windows-tjeneste, planlagt oppgave eller autostart. Docker, PC,
nettverk og connector må fortsatt kjøre; etter omstart brukes kommandoen over.

Eksisterende signert cloudflared 2026.10.4 og tokenfil beholdes under
`C:/Users/Jonas/AppData/Local/BussassistentTabletPilot`. Tunnel-ID
`4aecb83e-cf83-4112-8f76-9a564252e1fe`, metrics bare `127.0.0.1:18083`.
Ingen tokenverdi i argumenter/logger. Ingen DNS-, hostname-, Access-, MFA- eller
cachepolicy ble endret. Connectoren kjører videre etter denne økten.

Ved stopp: identifiser prosessen fra `tunnel.pid`, kontroller at ExecutablePath er
den dokumenterte cloudflared-filen og at CommandLine inneholder denne tunnel-ID-en,
og stopp bare den prosessen. For å stenge inngangen uten datatap:

```powershell
docker compose --env-file "$runtime/.env.tablet" -f "$runtime/compose.yaml" --profile tablet stop gateway
```

Ingen `-v`, prune, reset eller sletting av datavolum/passord. Tokenrotasjon og
Access-tilbakekalling er ulike operasjoner; ingen rotasjon ble gjort her.

## Backup og tilbakerulling

`backups/20261028-pre-a48f213/private_work.dump` er full pg_dump custom-format av
fjernmiljøets nåværende database, 92037 byte, SHA256
`26deeea831b50c69b8f37d5faa6912bd5b1851597da0d608dff87b4b01075a99`.
Backupen ble faktisk pg_restore-testet i egen PostgreSQL-container med `--network none`,
ingen vertsporter og tmpfs. Alle offentlige tabellrader ble sammenlignet deterministisk
med fjernmiljøets førtilstand og var identiske. Engangscontaineren er fjernet.
Config, tre aktive secrets/policy, opprinnelig runtime, tunnelcredentials og
kildearkiv er privat sikret samme sted. Fingeravtrykk av private tabeller publiseres ikke.

| Førtilstand/rollback | Image-ID |
|---|---|
| `ibe160-tablet-private-api:rollback-20261028` | `sha256:a585b56ed625132e277353fa57241d9ffa5e340ef7e15ff819b9980bc709c92e` |
| `ibe160-tablet-gateway:rollback-20261028` | `sha256:980c6b662cb29b04e7305d1fa9b0912979651aaf8d1edfb02c10340c99956352` |

Tidligere API var main-2dd1b11, gateway pdf-upload-20261027. De er beholdt lokalt
med rollback-tags. Ingen imagepruning er gjort. `compose.rollback.yaml` bruker de
gamle appimagene med stabile lokale filer og samme database. Nåværende og tidligere
API har samme 14 migreringer; ved behov kan akkurat disse appdelene tilbakeføres:

```powershell
docker compose --env-file "$runtime/.env.tablet" -f "$runtime/compose.rollback.yaml" --profile tablet up -d --no-build --no-deps private-api gateway
```

Kontroller deretter helse, mounts, adgangsnekt og byggidentitet. Ikke bruk vanlig
oppstartsskript etter rollback før aktiv compose/build-identity bevisst er satt til
ønsket versjon. Denne rollbacken skal ikke blindt gjenbrukes etter fremtidige
skjemamigreringer. Databaserestore var ikke nødvendig og er ikke utført i drift.
Ved eventuell katastrofegjenoppretting: restore først til nytt isolert volum med
private_work-rolle, sammenlign, og planlegg eksplisitt overgang; aldri overskriv
det nåværende datavolumet eller importer den eldre originalkontoen.

## Utførte kontroller og bevisgrenser

- 39/39: to komplette API/PostgreSQL-brukerflyter med eksakte PDF-byte, korrigering,
  godkjenning, avslutning/avbrudd og gjenåpning; fem A–E-importer; 32 kontrollerte
  mobilgrensetester. Komplett A-flyt inkluderte database-/API-omstart med persistens.
- 18/18: faktisk API/PostgreSQL for direkte import, valgfri korrigering, minimal
  godkjenning, busslagring på utkast og bekreftet plan, viewport/fokus og eksplisitt
  gjenoppretting/konflikter. To skjermbredder er nettleseremulering.
- 14/14: produksjonsimagets HTTPS-/Secure-cookie-/Origin-/CSRF-kontrakt, nettverksløst
  med syntetiske testdobler. Én eksisterende Starlette TestClient-deprecation-advarsel.
- Produksjonens API-filer er hashkontrollert mot main. Gatewayens HTML/JS/CSS er
  identisk med ferdigbygde filer som de 57 nettlesertestene brukte. API/gateway har
  korrekt OCI revision, faktisk kjørende API/DB er healthy.
- Alle fjernmiljøets tabellrader, inkludert konto/passordhash og senere data,
  var uendret etter oppstart. Alle øvrige opprinnelige container-ID-er/images/starttider
  var uendret. Produksjonsdatabasen ble aldri brukt til funksjonstestenes skriving.
- 15 lokale 403/no-store-prøver på side/asset/API med manglende, malformed og alg-none
  JWT; tre offentlige side/API-kall ga 302 til forventet Access. Direkte API ga 401
  uten appøkt og POST uten gyldig Origin/CSRF ga 403, begge no-store.
- Tunnel-ready 200 og fire aktive forbindelser. Faktisk nedlastet tunnelkonfigurasjon har bare riktig hostname, loopback18081, Access required, bevart team og AUD lik lokal gate, og avsluttende 404. Ingen nye DNS-/Access-/MFA-valg. Oppstartsskriptet er også kontrollert ved gjentatt kjøring uten ny connector.

Tilpasningsforsøkene av gammel testharness feilet først på sandboxnettverk,
historisk demo.html-fane (privatbygget inneholder korrekt ingen demo), tmpfs-persistens
under restart, manglende API-remigrering etter bytte av testvolum og feil arbeidsmappe.
Adapterne ble rettet uten produktendring. Første etterkontroll hadde feil lokal backendsti;
Python-standardklienten fikk også edge-403. Vanlig klientidentitet ga Access-302.
Disse forsøkene er ikke presentert som beståtte produktkjøringer.

Ingen ny innlogget Cloudflare/MFA-økt eller fysisk Pixel/Lenovo-prøve ble gjennomført
av agenten på dette offentlige bygget. Gyldig Access etterfølges fortsatt av appens
innlogging; jonas og eksisterende passordhash er bevart. Eier kan nå åpne samme
HTTPS-adresse, laste siden på nytt og prøve mobil/native filvelger, valgfri korrigering,
godkjenning og busslagring. Dette er en ny driftskontroll, ikke ny Story12.4-aksept.
Tidligere godkjenning og fysisk evidens er beholdt. [Maskinlesbar rapport](evidence/tablet-production-2026-10-28.json).

## Opprydding og konkret beholdt innhold

`tablet-remote-access` hadde 16 statusoppføringer, utvidet til 29 filer. Alle stier
finnes i main; 16 er identiske etter LF/CRLF-normalisering. Tilgangsfunksjonene i
de fire endrede produktfilene er integrert; main inneholder nyere funksjonell utvikling
i PrivateAccess/private_main. Docker-/Compose-/oppstartsforskjellene er historiske
versjoner som main har videreutviklet. Transporttester, gate/proxytester, eksempler
og historisk dokumentasjon finnes også i main. Ingen gammel produktfil ble kopiert
over godkjent main.

Hele gammelt worktree, inkludert nyttig dokumentasjon/testarbeid og ignorerte
fixture-/ACL-/hjul-/probe-kataloger, er bevart privat i
`backups/20261028-pre-a48f213/tablet-remote-access-full.tar`: 906 filer bytekontrollert
mot arkivet før fjerning. SHA256
`88955f6927e9cb9305d31a18cc0e5438a6874064096f33030c330cc3961bb89d`.
Ukommittert arbeid er i tillegg bevart i navngitt lokal Git-stash, referanse i privat
backup. Ignorert tmp-innhold er flyttet til backup, ikke slettet. Ingen container
refererte worktreet. Deretter normal `git worktree remove` og `git branch -d`
på fullt integrert `setup/tablet-remote-access`, uten force. Ingen tilsvarende
origin-branch fantes. Historien er fortsatt tilgjengelig fra main og privat stash/arkiv.

`tablet-access-11-6` beholdes konkret: seks egne loggcommits etter main-linjen,
privat historisk runtime og testuttrekk, installerte frontendavhengigheter. Etter
konsolideringen refererer ingen aktiv produksjonsmount eller compose-arbeidsmappe dit.
Branchen `setup/tablet-remote-access-11-6` er ikke fullt integrert; den slettes ikke.
Ikke bruk dens gamle oppstart/override som gjeldende drift. D:/IBE160/tmp/story-12-3
og story-12-4 beholdes som før for eksisterende test-/previewmiljøer og privat tilstand;
øvrige worktrees er utenfor denne oppryddingen. Ingen aktiv katalog ble fjernet.

Det nye syntetiske prosjektet ibe160-deploy-check er stoppet/fjernet, testserveren
stoppet og engangs restore-/transportcontainere fjernet. Det separate syntetiske
testvolumet check_pg er beholdt uten aktiv container; produksjonsvolumet er urørt.
