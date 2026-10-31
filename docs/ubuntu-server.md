# Ubuntu-server for Bussassistent

Gjeldende 31.10.2026: serverintegrasjonen og driftsoverleveringen er fullført og inngår i V1 etter Jonas sin avklaring. Tidligere bonus/v1.0.1-avgrensning er erstattet; [samlet omfang, status og versjonstilknytning](submission/v1-scope-and-operations.md). Sensor bruker den selvstendige [lokale oppskriften](../README.md) og trenger ikke server, eierkonto, private data eller Cloudflare-tilgang.

Integrasjonen tok inn main-grunnlaget 64f91a7 i 6f845fa før testing. Backend, frontend og tablet-gate ble bevart. Publisert main var 5dc6400 ved dokumentkontrollen; siste dokumenterte deploy er addd27b14fe4b26ef24d488d847d1c0d59a98946, med eierbekreftet innlogging/lagring 31.10.2026. Publisering av dokumentasjon deployer ikke ny release. Ferdig integrerte serverbrancher er ryddet etter kontroll, se driftsloggen. Opprinnelig plan godkjent 29.10.2026. Langtidsstabilitet observeres videre. Lesende sluttkontroll31.10 bekreftet fortsatt addd27b og healthy API/database/aktiv tunnel. En reboot-required-markør for libc6 er registrert som videre vedlikehold; ingen omstart/oppdatering ble utført. [Avgrensede resultater og åpne O3–O6 etter V1](evidence/v1-final-control-20261031.md).

## Publisert og deployet V1 — 31.10.2026 kl.03:21

Etter ny uttrykkelig bestilling er [GitHub-release v1.0.0](https://github.com/IBE160-2026/G06-oisund/releases/tag/v1.0.0) publisert, og nøyaktig **d367a0e47198aeecc52358258cb6825eecdc8c4a** er aktiv på Ubuntu. Taggen er ikke flyttet. [Faktisk backup, deploy, etterkontroll og eierteststatus](evidence/v1-release-deploy-20261031.md). Dette erstatter addd27b som aktiv release; avsnittet ovenfor er førhistorikken. `previous` beholder addd27b som dokumentert tilbakevei med identiske private migreringer. Nyere dokumentasjonscommits i main er ikke deployet automatisk.

Windows-backup er SHA256-verifisert, og en separat fersk backup bestod isolert restore med alle tabellfingeravtrykk like. Eksisterende deployverktøy fullførte med exit0; API/DB healthy, tunnelready200/4 forbindelser, backup-timer active og ingen failed units. Jonas bekreftet deretter innlogging, lagring og gjenåpning på d367a0e: «Alle tre bestod uten feil». Siste lesende kontroll kl.03:30 bestod på samme release. Ingen maskinomstart eller produksjonsrestore/reset ble utført. O3–O6 og libc6-/stabilitetsoppfølging er fortsatt åpne.

## Server og drift

SSH: jonas@192.168.1.139 fra Windows på samme lokalnett.
Lenovo Y520-15IKBN, Ubuntu26.04.1, kernel7.0.0-42-generic.
Gammel kernel7.0.0-30 er markert manuelt installert og beholdes.
GRUB viser meny; tilbakevei er Advanced options for Ubuntu -> 7.0.0-30-generic.
Fire oppstarter med ny kernel bestod. Tidligere frys er ikke sikkert årsaksforklart;
videre stabilitet observeres uten automatisk BIOS-/driverendring.

App, Cloudflare Tunnel og backup-timer starter automatisk uten lokal innlogging.
Lokk ignoreres på ekstern strøm; batteridrift er ikke kvalifisert.
Wi-Fi/Ethernet-venting godtar et rutbart IPv4-grensesnitt.
Bare SSH og loopback-app/metrics er publisert; database/API har ingen vertsporter.

- /opt/bussassistent/releases/<full-SHA>: kilde og bygggrunnlag.
- /opt/bussassistent/current og previous: valgte releaser.
- /etc/bussassistent/server.env: TABLET_HOST=app.bussassistent.com.
- /etc/bussassistent/secrets/: app-/databaselegitimasjon, mappe0700.
- /etc/bussassistent/tunnel-token: root0600, systemd LoadCredential.
- Docker-volum bussassistent_private_pg: beholdes mellom releaser.
- /var/backups/bussassistent: databasebackuper, root:jonas, 0750/0640.

Containerfilene i secrets-mappen er0444 for avgrensede ikke-root-containere;
beskyttelsen på verten er den overordnede0700-mappen. Ikke åpne denne mappen.
Avgrenset sudo til bussassistentctl er en administratorrolle som kan deploye kode.

## Oppdatering fra Windows

Arbeid på egen branch, test og commit endringene. Velg en eksplisitt commit som
inneholder deploy/ubuntu. Etter godkjent integrering kan testet main brukes.
Skriptet deployer committede filer; det gjør ikke git pull, merge eller push.

Kjør i PowerShell fra D:\IBE160, én kommando om gangen. Stopp ved feil.

~~~powershell
.\scripts\server.ps1 -Action Status
.\scripts\server.ps1 -Action Check
.\scripts\server.ps1 -Action Backup
$revision = git rev-parse HEAD
.\scripts\server.ps1 -Action Deploy -Revision $revision
.\scripts\server.ps1 -Action Check
.\scripts\server.ps1 -Action Status
~~~

Kontroller deretter innlogging, lagring og gjenåpning i nettleseren.
Vanlig appdeploy krever ikke maskinomstart. Gjør dette i vedlikeholdstid:
tunnelen og skriverne stoppes kort under byttet.

Deploy arkiverer backend/frontend/deploy, kontrollerer SHA256 og avviser
arkivlenker/path traversal. Bygg utføres før avbruddet. Driftsverktøy installeres,
serverbackup tas, release byttes og Compose/apphelse kontrolleres.
Windows Backup henter en separat verifisert kopi før deploy.
Ved feil etter mulig migrering forblir tunnelen stoppet; gammel kode startes
ikke blindt mot en mulig nyere database.

~~~powershell
.\scripts\server.ps1 -Action Logs
.\scripts\server.ps1 -Action Rollback -Revision <full-SHA-til-tidligere-installert-release>
~~~

Rollback krever identiske private migreringsfiler og allerede bygde images.
Ved schemaendring kreves egen vurdering av restore og data skrevet etter backup.
Ingen down -v, volume prune eller generell Docker-opprydding inngår.
Ta vare på aktuell og tidligere verifisert release.

## Backup og restore

Ubuntu-timer: daglig03:15 Europe/Oslo, persistent.
Windows-oppgave Bussassistent-Backup: daglig04:00 og ved innlogging, bare når
Jonas er innlogget. StartWhenAvailable og tre nye forsøk med fem minutters
mellomrom ved feil. PC-en behøver ikke være på for at appen skal kjøre,
men lokale backupkopier krever at Windows-oppgaven faktisk kan kjøre.

Windows-kopier ligger i %LOCALAPPDATA%\BussassistentServer\backups.
Overføringen SHA256-verifiseres og mappen beskyttes med ACL.
Oppbevaring48t ryddes ved neste vellykkede kjøring, ikke som en absolutt frist
mens maskinen er avslått. Backup kan inneholde rader som senere er slettet.
Ved produksjonsrestore må opprydding/utløpsregler kjøres før ekstern åpning.

Installer/oppdater Windows-oppgaven med scripts/install-server-backup.ps1.
Oppgaven bruker en fast kopi av administrasjonsskriptet i brukerøkten.
SSH-nøkkelen er separat; ingen passord eller token legges i oppgaveargumentene.

Isolert verifikasjon av fersk backup, uten å erstatte produksjonsdata:

~~~powershell
ssh -i "$env:USERPROFILE\.ssh\ibe160_server_ed25519" jonas@192.168.1.139 "sudo -n /usr/local/sbin/bussassistentctl verify-restore"
~~~

Denne kommandoen sammenligner før-/etterfingeravtrykk, gjenoppretter dumpen i
en unik PostgreSQL-container uten nettverk eller vertsporter, kun tmpfs-data,
og sammenligner alle tabeller. Container og midlertidig volum slettes etterpå.
Kjør i rolig periode: samtidige skriv gjør at sammenligningen avvises.
Dette er en restore-prøve, ikke kommando for produksjonsrestore.
Førstegangskommandoen restore-initial avviser allerede deployet/ikke-tom database.

## Vedlikehold og dokumentert testdekning

Ubuntu-sikkerhetsoppdateringer er automatisert; automatisk reboot er avslått.
Docker/cloudflared og appimages oppdateres kontrollert i vedlikeholdstid.
Kontroller diskplass, backupresultat og reboot-required regelmessig.
Gammel kernel beholdes til stabiliteten er avklart.

Bestått29.10:
- Initial faktisk restore,25 tabeller sammenlignet med originalen.
- Fire oppstarter med kernel7.0.0-42 og automatisk app/tunnel/backup-timer.
- Kontrollerte API-/DB-/tunnelkrasj; automatisk recovery og uendrede tabeller.
- Faktisk Windows-backup, også etter Windows-av-prøven.
- Lokk lukket på ekstern strøm; SSH/app/tunnel fortsatte å fungere.
- Wi-Fi ned/opp; samme boot og tunnelprosess, automatisk gjenoppkobling.
- Eierbekreftet innlogging/lagring, reload/ny innlogging og mobilnett.
- Eierbekreftet innlogging/lagring mens Windows var avslått.
- Fersk isolert backuprestore med full tabellfingeravtrykk-sammenligning.

Senere integrasjon/deploy/rollback og nøyaktige releaser registreres i
[driftsloggen](../.logs/jonas-oisund/990-2026-10-29-18-30-00-ubuntu-server.md).
Historiske feil og avgrensninger bevares der. Eier bekreftet31.10.2026 at innlogging/lagringstesten også bestod på integrert release addd27b. De øvrige manuelle testene ovenfor gjelder
releasen som var aktiv da de ble gjennomført; de er ikke ny eieraksept av senere kode.

Tester ved integrasjon:12 driftstester (chown mockes i ikke-root-testkjøringen),
23 gate-tester,4 cleanup-tester, frontend TypeScript/Vite-bygg, Windows-parser og
faktiske Docker-bygg. Ingen produksjonshemmeligheter inngår i Git eller testoutput.
Originalt Windows-databasevolum og verifiserte backupkopier beholdes.
