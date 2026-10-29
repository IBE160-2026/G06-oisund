# Ubuntu-server for Bussassistent

Godkjent plan: 2026-10-29. Arbeidsbranch: setup/ubuntu-server.
Status: SSH-nøkkeltilgang verifisert, kildebackup tatt med uendrede radfingeravtrykk, driftsfiler lokalt testet; installasjon,
dataflytting, nettverksretting og oppstartstester på Ubuntu er ikke utført.

## Maskin og eksisterende drift

Server: jonas@192.168.1.139, Ubuntu 26.04.1 LTS x86_64, 7,1 GiB RAM,
86 GB ledig på /. Wi-Fi og SSH er brukerbekreftet tilgjengelig etter omstart.
systemd-networkd-wait-online feiler etter omtrent 120 sekunder.
Undersøk nettverkskort og oppstart -2 før endring; det er ikke bevist at
ventefeilen forklarer den kortvarige oppstarten. Ikke deaktiver venting blindt.
Kontroller ssh.socket; ssh.service disabled er ikke i seg selv bevis på manglende autostart.

Windows-produksjonen er stoppet og bruker main-a48f213. main ved branchopprettelse
var 9677eba. En separat oppfølgingsbranch/teststack er aktiv og skal ikke berøres.
Ingen produksjonsdata skal resettes, ingen volum skal slettes.

## Oppsett

- /opt/bussassistent/releases/<40-tegn-commit>: immutable kilde og bygggrunnlag.
- /opt/bussassistent/current og previous: valgte releaser.
- /etc/bussassistent/server.env: TABLET_HOST=app.bussassistent.com.
- /etc/bussassistent/secrets/: bootstrap-password, postgres-password, access-policy.json.
- /etc/bussassistent/tunnel-token: eksisterende tunnellegitimasjon, root 0600.
- Docker-volum bussassistent_private_pg: beholdes mellom releaser.
- /var/backups/bussassistent: postgres custom-format, root:jonas, 0750/0640.

Secrets-mappen er root 0700. De tre containerfilene må være lesbare av de
ikke-root-brukerne inne i containeren, normalt 0444 på selve filen, beskyttet av
0700 på vertsmappen. Ikke sett hele secrets-mappen offentlig lesbar.
Tokenet brukes gjennom systemd LoadCredential; aldri token i argumenter, chat eller Git.

Compose er frittstående. Ikke kombiner med demo-, test- eller tablet-Compose.
Bare gateway har vertsnettbinding, 127.0.0.1:18081. Database og API har ingen
vertsporter. Origin-JWT-gate, appinnlogging, CSRF, HTTPS-cookies og no-store beholdes.
Ingen innkommende webporter eller Docker TCP-API åpnes.

## Første installasjon (ikke utført)

1. Bekreft fungerende SSH-nøkkel fra Windows. Passord tastes bare i eierens terminal.
2. Les probe.sh og kjør den på serveren. Undersøk nettverksventing og kort oppstart.
   Ha fysisk tilgang og tilbakeføring ved enhver Netplan-endring.
3. Kopier deploy/ubuntu til serveren og kjør bootstrap.sh med sudo i egen terminal.
   Det installerer offisielle Docker/Cloudflare-pakker og tjenestefiler, men starter
   ikke app eller tunnel. Ingen nettverks-/brannmurendring utføres av skriptet.
   Avgrenset sudo gis til root-eid bussassistentctl. Dette er en administratorrolle:
   den kan deploye kjørbar kode og er derfor ikke en lavprivilegert sluttbrukerkonto.
4. Overfør godkjente secrets direkte over SSH uten å skrive innhold i terminal/logger.
   Etabler server.env, filrettigheter og riktig tunnelpolicy.
5. Lag lokal commit med verifiserte driftsfiler. Velg eksplisitt release-SHA.
   Stage laster opp et git-arkiv med bare backend/frontend/deploy og kontrollerer
   SHA256 før utpakking. Bygg skjer før produksjonen stoppes.
6. Start bare den eksisterende Windows-produksjonsdatabasen for en konsistent
   pg_dump, uten å starte app/tunnel. Behold originalvolumet.
7. Start bare Ubuntu-databasen med prepare-db SHA. Gjenopprett backupen mens
   app/tunnel er stoppet. Verifiser skjema, konto-/databevaring og rolle/eierskap
   uten å vise private rader. Etabler root-eid /etc/bussassistent/data-ready
   først etter vellykket kontroll. Førstegangsdeploy avvises ellers.
8. Deploy valgt SHA. API kjører eksisterende migreringer ved start. Kontroller
   helse og 403 fra origin uten Access-assertion. Kontroller at Windows-tunnelen er stoppet.
9. Aktiver bussassistent.service, cloudflared.service og bussassistent-backup.timer
   etter kontrollert første oppstart. Verifiser offentlig Access/MFA og appinnlogging.
10. Gjennomfør to planlagte omstarter uten lokal innlogging, lokkprøve på strøm,
    nettbrudd, prosessfeil og database-/API-restart med fiktiv kontrollhandling.
    Bekreft drift med Windows avslått. Ikke påstå fysisk brukeraksept fra automatiske tester.

## Oppstart og oppdatering

systemd starter Docker og kjører Compose up --no-build --pull never --wait.
Containerne bruker on-failure for prosessfeil. Ved oppstart er det systemd som
starter stacken i Compose-rekkefølge; Docker skal ikke starte gamle containere
uavhengig av denne rekkefølgen. Et unhealthy-merke alene utløser ikke automatisk
containerrestart. Check/status brukes til kontroll; full gjenoppretting må prøves.

Cloudflared er egen systembruker, restart always, loopback metrics 18083.
Tunnelen prøver igjen ved nettbrudd og krever ikke lokal brukerinnlogging.
Lokk på ekstern strøm settes til ignore; endringen tas i bruk ved planlagt omstart.
Det gjøres ingen BIOS-endring eller diskutvidelse som del av oppsettet.

Windows, fra prosjektroten:
~~~powershell
.\scripts\server.ps1 -Action Status
.\scripts\server.ps1 -Action Logs
.\scripts\server.ps1 -Action Check
.\scripts\server.ps1 -Action Backup
.\scripts\server.ps1 -Action Deploy -Revision <full-commit-SHA>
.\scripts\server.ps1 -Action Rollback -Revision <full-commit-SHA>
~~~

Deploy arkiverer bare committede filer; ingen automatisk git pull eller push.
Full commit-SHA kreves. Stage gjenbruker en eksisterende release bare når
arkividentiteten stemmer. Ved deploy stoppes tunnelen og skriverne, backup tas,
release byttes og helse kontrolleres. Feil etter migrering lar tunnelen være stoppet.
Gammel kode startes ikke automatisk mot en mulig nyere database.

Rollback tillates bare med identiske private migreringsfiler. Ved skjemaendring
kreves separat kontrollert databasegjenoppretting og vurdering av nyere skrivinger.
Ingen down -v, volume prune eller generell Docker-opprydding inngår.

## Backup og oppdateringsrutine

Daglig backup 03:15 Europe/Oslo, persistent timer. Maksimal oppbevaring 48 timer
ved vellykkede backupkjøringer. Windows Backup kopierer via SCP, verifiserer SHA256
og beskytter lokal mappe med ACL. Lokale kopier eldre enn 48 timer fjernes ved
neste vellykkede kjøring. Dette er ikke en uavhengig fristgaranti når maskinen er av.

Av-maskin-kopiering må kjøres fra Windows når den er på; automatisk Windows-task
er ennå ikke installert. Behold minst én verifisert kopi av serveren før overgang.
Backup inneholder private data og kan inneholde rader som senere er slettet.
Ved restore skal appens opprydding/utløpsregler kjøres før ekstern åpning.
Tilbakeføring av gamle data må ikke forlenge deres opprinnelige frister.

Ubuntu-sikkerhetsoppdateringer automatiseres med unattended-upgrades;
automatisk omstart er avslått. Docker/cloudflared fra tredjepartskilder og
appimages oppdateres kontrollert i vedlikeholdstid. Gjennomgå reboot-required.
Planlegg logg-/diskkontroll og regelmessig faktisk restore-prøve.

## Utførte lokale kontroller

- 11 isolerte Linux/Python-tester: sti-/SHA-validering, arkivhash, path traversal,
  symlink, ufullstendig release, uendret releaseidentitet ved retry,
  avbrutt dump og rollback med ulikt skjema.
- bash -n for bootstrap.sh.
- PowerShell-parser for scripts/server.ps1.
- Docker Compose-parsing og kontroll av loopback-port/faste volum.

Ingen av disse beviser faktisk systemd-drift, datamigrering, Cloudflare-tilgang
eller gjenoppkobling etter reboot/nettbrudd. Det gjenstår på Ubuntu.

Kilder: https://docs.docker.com/engine/install/ubuntu/
https://pkg.cloudflare.com/
https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/run-parameters/

Diagnose 29.10: ventetjenestens genererte kommando venter bare på enp4s0, som har no-carrier. wlp3s0 er routable. ssh.socket er enabled/active. Bootstrap legger inn en egen drop-in som godtar enten Ethernet eller Wi-Fi med IPv4, uten å endre interface-konfigurasjon. Den korte oppstarten -2 slutter uten en avsluttende årsak i journalen; årsaken er fortsatt ukjent.
