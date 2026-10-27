# Lokal isolert pilot – trinn 1

Dato: 2026-10-26. Eier har uttrykkelig godkjent lokal isolert pilot med bare fiktive data, uten ekstern publisering, DNS-endring eller tunnelstart. **Trinn 1 er gjennomført. De fire lokale pilotcontainerne kjører; trinn 2 er ikke godkjent eller startet.**

Worktree: `C:\Users\Jonas\.codex\.chatgpt-projects\g-p-6ab6b4c1c6888191a96d3242fab912b4\tablet-access-11-6`.
Branch: `setup/tablet-remote-access-11-6`, base `f5ffa4bf64696b8e1abf910ccd8ac106663d30a9`.

## Kjører lokalt

Prosjektet er utelukkende `ibe160-tablet-prep` fra den selvstendige `compose.tablet.yaml`, profil `tablet`. Ingen ordinær Compose-fil er kombinert inn.

| Tjeneste | Tilstand | Eksponering |
|---|---|---|
| private-db | running / healthy | Eget interne storage-nett og volum `ibe160-tablet-prep_tablet_pg`; ingen hostport |
| private-api | running / healthy | Interne app/storage-nett; ingen hostport |
| access-gate | running, svarte med nekt i live-prøve | app-nett og eget keys-nett for offentlig JWKS; ingen hostport |
| gateway | running | Bare `127.0.0.1:18081 → 8080/tcp`; app-nett og eget front-bro-nett |

Alle fire: ikke root, read-only rootfilsystem, cap_drop ALL, no-new-privileges, restartpolicy `no`. Ingen Windows-tjeneste eller autostart er installert. Bare pilotgatewayen er publisert. Docker Engine er 29.7.2 i dette snapshotet.

Front-nettet er nødvendig for faktisk hostpublisering i dette Docker-oppsettet. Bare gatewayen er tilkoblet; IPv6 er av og nettets standard hostbinding er 127.0.0.1, i tillegg til eksplisitt loopback-binding på porten. Gateway og gate har nå hvert sitt ikke-interne bro-nett; dette er ikke en fullstendig egress-brannmur eller domenebegrensning. API/DB beholder intern nettverksisolasjon. Ingen direkte ruting, nat-unprotected, host-network, Docker-socket eller Windows-/ruterbrannmurendring er innført. Se [Docker nettverksoversikt](https://docs.docker.com/engine/network/) og [portpublisering](https://docs.docker.com/engine/network/port-publishing/).

## Lokale filer og fiktive data

prepare-tablet-files.ps1 har fått en eksplisitt `-LocalOnly`-modus. Den krever ikke tunnel-ID/credential-sti, nekter å kombinere LocalOnly med slike argumenter, og lager ingen cloudflared.yml. Eksisterende konfigurasjoner og passord overskrives ikke. Faktisk repetert kjøring ble avvist og bytekontroll viste alle eksisterende filer uendret.

Lokalt opprettet, ignorert av Git:

- `.env.tablet`: kun vertsnavnet app.bussassistent.com.
- `.private-runtime/tablet/access-policy.json`: ett eksplisitt godkjent email, faktisk team og app-AUD fra tidligere godkjent oppsett. Ingen bred identitet/bypass.
- `.private-runtime/tablet/postgres-password` og `bootstrap-password`: uavhengige kryptografisk tilfeldige passord. Bootstrap-passord er bare montert i DB, ikke API.
- `.private-runtime/tablet/pilot-login.json`: brukernavn `tablet-provebruker` og et separat tilfeldig passord. Ikke åpne denne filen i chat, logger, skjermbilder eller delte forhåndsvisninger. Eier kan lese den lokalt ved senere godkjent innlogging; ingen hemmelighet skal limes inn i chat.

Runtime-mappen fikk begrenset ACL før passord ble skrevet. Mappe/filer tillater bare nåværende Windows-bruker og SYSTEM; ACL og Git-ignorering er kontrollert. Lokal administrator eller kompromittert eierkonto kan fortsatt få tilgang. Ingen tunnellegitimasjon, admin-cert.pem eller tunnelkonfigurasjon er laget.

Den nye databasen har 13 migreringer, én fiktiv bruker og ett tydelig merket fiktivt utkast med tjenestedato 2031-01-02 og ingen aktiviteter. Ingen ordinære data eller kontoer er kopiert. Seed-skriptet krever en tom konto-/utkastdatabase og korrekt prosjektmarkør/origin/DB før opprettelse; ikke kjør det på nytt, og ikke nullstill databasen for å få det til å passere. Lokalt tilfeldig generert prøvepassord ble montert read-only bare i en midlertidig klientcontainer; klienten er fjernet. Ingen passord, cookie eller token ble skrevet til chat/logg.

## Utført kontroll

- Faktisk runtime-inspeksjon: riktige containernavn/prosjekt, read-only/caps/no-new-privileges/restartpolicy, egne nett/volum og ingen hostporter for API/DB/gate. DB/API healthy.
- Bare én hostlytter på pilotporten, `127.0.0.1:18081`. Ingen IPv6-loopback-lytter på denne porten. Faktisk Docker NetworkSettings.Ports samsvarer med ønsket loopback-publisering.
- 18 live HTTP-forsøk mot localhost: rot, /private, faktisk bygget JavaScript-asset, API auth/session GET, API drafts GET og POST × manglende, malformed og alg-none JWT. Alle returnerte 403 og no-store. Feil Host lukket forbindelsen, og den interne auth-ruten ga 404 ved direkte kall. Ingen gyldig Access-token er konstruert eller brukt.
- Ekte pilot-DB/API: 13 migreringer, approlle uten SUPERUSER/CREATEDB/CREATEROLE/REPLICATION, innlogging med Secure/HttpOnly/SameSite Strict, CSRF-nekt, fiktiv lagring/gjenåpning og utlogging bestod. Dette brukte FastAPI TestClient med HTTPS-base og ekte pilotdatabase; det er ikke et faktisk TLS-/nettleser-/Cloudflare-bevis.
- Etter avvisningsprøvene: fortsatt én bruker/ett utkast, og null aktive appøkter.
- Fem ordinære containere: samme ID, StartedAt, RestartCount og image før/etter. Ingen stop/restart/rebuild utført på dem. Hovedarbeidsmappens index og de fire berørte produktfilenes bytehash er uendret. Ingen ordinær DB ble åpnet av pilotkontrollene; ingen påstand om full råtabellhash av ordinære data fremsettes.
- Ingen cloudflared-prosess. Ingen kommando som oppretter tunnel, DNS eller publisering er kjørt.

Reproduserbar, ikke-muterende lokal kontroll fra denne worktree-mappen:

~~~powershell
./scripts/test-tablet-config.ps1
./scripts/test-tablet-local-pilot.ps1
~~~

En nettleser uten Access-token skal ikke vise appen via denne HTTP-porten. 403 er forventet. Ikke åpne en LAN-port eller legg inn bypass for å få en innloggingsside i lokalpiloten.

### Feil og rettelser under oppstart

Første kontroll av Git-ignorering brukte git check-ignore --quiet med flere filnavn, som Git avviser. Kontrollen ble korrigert til ett filnavn per kall; filer/passord ble ikke regenerert. Første seed-klient manglet PYTHONPATH=/app og stoppet før auth-import eller DB-operasjon; korrekt modulbane løste feilen. Én kjent TestClient-deprecation-advarsel gjenstår.

Første Compose-oppstart av API stoppet fordi usiterte komma i YAMLs tmpfs-liste ble tolket som et ekstra mountnavn. API/gateway-verdiene er sitert, og konfigurasjonskontrollen avviser nå relative tmpfs-navn og feil antall mounts. Bare pilotressurser var opprettet.

Den første gatewayen hadde ønsket port i HostConfig, men ingen faktisk portbinding i NetworkSettings fordi den bare var tilkoblet et internt nett. Localhost-kallet feilet. Et eget front-bro-nett ble lagt til, bare pilotgatewayen ble gjenskapt, og faktisk localhost-port og 18 nektprøver bestod. De tidligere syntetiske proxytestene brukte container-internt nett og kunne ikke oppdage hostpubliseringsfeilen. Ny runtime-test kontrollerer faktisk binding og HTTP-svar, slik at bare en gyldig Compose-konfigurasjon ikke lenger teller som publiseringsbevis.

## Stoppe eller senere fortsette

For å stenge bare lokalpilotens inngang:

~~~powershell
docker compose --env-file .env.tablet -f compose.tablet.yaml --profile tablet stop gateway
~~~

For å stoppe alle fire pilottjenester og beholde fiktive data/passord:

~~~powershell
docker compose --env-file .env.tablet -f compose.tablet.yaml --profile tablet stop
~~~

Bruk bare disse kommandoene fra denne worktree-mappen, aldri ordinære Compose-filer eller prune/reset/-v. Ingen stopp er utført ved leveransen; lokalpiloten kjører uten autostart.

Ekstern testing krever fortsatt egen godkjenning av trinn 2: kontrollert portabel cloudflared, navngitt tunnel og lokal legitimasjon, konkret DNS-rute for app.bussassistent.com og manuell tunnelstart. Dette er ikke godkjent av trinn 1. Før dette må eksisterende Access/MFA/cache-valg leses tilbake, eventuelle nye kontoforhold vurderes og oppdaterte binær-/avhengighetskontroller gjennomføres. Tidligere ruterkontroll er eiers opplysning, ikke teknisk bevist WAN-policy; samlet alternativ-rute-verifikasjon må dokumenteres ved publiseringsbeslutningen.

Gjenstår fysisk/eksternt: tvungen MFA for akkurat appen, korrekt Access-signert token/signatur/issuer/AUD/exp, nekt for uinnlogget og feil identitet på side og API, utløp/tilbakekalling, faktisk HTTPS/cookies/cache, rask tunnelstenging og Lenovo/Android/Brave på hjemmenett og mobilnett, inkludert lagring og forbindelsesbrudd. Full browserregresjon og fysisk test er ikke utført i denne fasen. Se også sikkerhetsrapportens aktiveringsmatrise.
