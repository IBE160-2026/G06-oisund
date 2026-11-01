# O6: avgrenset gatewayvedlikehold 1. november 2026

Jonas har bestilt integrering og deploy av bare den kvalifiserte gatewayrettelsen.
Ingen passordfunksjonalitet, Python/API/gate-/PostgreSQL-/vertsoppdatering inngår.
V1-taggen skal forbli på d367a0e47198aeecc52358258cb6825eecdc8c4a; ingen ny tag/release.

## Kvalifisert grunnlag og nødvendige driftsgrenser

[Gatewaykvalifikasjonen](https://github.com/IBE160-2026/G06-oisund/blob/533313873c49317a958dc9a2407fad32f916d19f/docs/evidence/o6-gateway-candidate-20261101.md)
og [samlet vedlikeholdsplan](https://github.com/IBE160-2026/G06-oisund/blob/841fbbe337860d06456abf21c6cd0e5501ad5ffc/docs/evidence/o6-maintenance-ready-20261101.md)
beholdes med sine faktiske versjonsgrenser. Produktendringen er identisk runtime-FROM
til nginx1.30.6-alpine-slim/indexdede8895648b461178c3bc604f7eed4423efe5220b2c4d839f5eb3d34ac3f8f7.
Tidligere kvalifisert lokalt image3cae8303e4976d3515db8d515e0d41f53c5a51884a8bc444dfb1046187a65c6a
bevares. Nyeste origin/main ved start er5cee9e03d03d2c9c165c7f8fec64aa3e146959ab.

Standarddeployen stopper også API/gate og tunnelen. Ny `GatewayStage` stopper
derfor før aktivering; `GatewaySwitch` aktiverer kun gateway med --no-deps/--no-build/
--pull never. Gammel stage bygger hele pakken som tidligere; eventuelle nye midlertidige
API/gate-builds blir aldri kjørt. Før gatewaybyttet bindes nye releasealiases til
de eksakte aktive API/gate-image-ID-ene. Dette bevarer også riktige appbyte ved en
senere autostart. Ingen app-/DB-migrering eller restart bestilles.

Gatewaymodusen avviser endringer i backend, frontend, gate, Nginx-mal/hovedkonfig
og løst Compose-oppsett utover releasealias. Den krever forventet aktiv SHA og
eksakt kvalifisert gatewayimage. API/gate/DB-container-ID/image/PID/oppstart/restartteller,
tunnelprosess og boot-ID sammenlignes før/etter. Ved feil returneres bare gatewayen
til gammel release før operasjonen avvises. 18 isolerte Linux-driftstester bestod,
inkludert kilde-/DB-grenser, feil image, selektivt bytte og gatewaytilbakevei.

## Gjennomføring

Historisk førkontroll: produksjonen var frisk på d367a0e;
83GB ledig, ingen failed units, tunnelready200, backup-timer aktiv og boot-ID
44c550dc-d3b9-4222-8f6c-e0dcdac1a991. Dette var kontrollpunktet før inngrep.

## Faktisk integrering, backup og deploy

Arbeidscommit **82a4b68** er integrert i main med mergecommit
**93ee582b1a71a3f7552da1894b570366b89afee1** og pushet før staging. Ingen backend-,
frontend-, gate-, PG-/Compose-/låsefil-/migrerings- eller passordendring inngår.
[Inngangshasher og omfang](o6-gateway-deploy-20261101/source-scope.json).

Windows-kopien av fersk backup er **66495 byte**, SHA256
**5bf90e546527d6edad7ef06a2f15e89089afb38a23da794361e66bef70edfd05**.
Den ligger bare i eksisterende ACL-beskyttet privat backupområde. Serverens
pg_restore-list og overføringshash bestod. En separat fersk dump bestod full isolert
network-none/tmpfs-restore med alle tabellfingeravtrykk like. Bare prosjektets egne
restore-fixtures ble fjernet; ingen produksjonsrestore/dataendring.
[Backupkvittering](o6-gateway-deploy-20261101/backup-verification.json),
[restore](o6-gateway-deploy-20261101/backup-restore.txt).

Releasen ble bygget med eksisterende stage-/install-tools-løp uten aktivering.
Enhetenes fire filer og cloudflared-binæren har samme hash før/etter; daemon-reload
installerte driftsverktøyet uten pakkeoppdatering eller tjenesteomstart. Midlertidige
API/gate-builds i stage ble ikke kjørt; nye releasealiases er bundet tilbake til
eksakt aktive V1-image-ID-er før gatewaybyttet.

Serverbygget fikk **sha256:18f942c0107fa36b2fff8e11759d64ee08244fe115195e8e89bab03f4fc984c0**,
som er en annen identitet enn den bevarte opprinnelige lokale kandidaten3cae8303….
Serverartefakten ble derfor eksportert, SHA256-verifisert ved overføring
(arkiv **4c738c724d1b2054e7c8b8f9c731ce25b0417dee4ad4ff1ed7dbcf12f263b84b**),
lastet under et ledig lokalt releasenavn og kvalifisert på nytt før aktivering.
Server/lokal image-ID og alle rootfs-layers er like.
[Binding](o6-gateway-deploy-20261101/artifact-binding.json).

Serverartefakten bestod fem beskyttede stier×24 syntetiske tokenvarianter,
cookie-/header-/Origin/CSRF-/no-store-grenser og gate-nede. Ekstraserien bestod
nginx-syntaks, faktisk levering av appskall/JS/CSS, ti upstream-feilstatuser og
API-nede med fortsatt aktiv gate. Appens index/assets er byteidentiske med det
tidligere kvalifiserte appgrunnlaget. Trivy0.76.1 med den låste1.11-databasen ga
**0 advisorytreff i21 runtimepakker** (Alpine3.24.3/Nginx1.30.6/OpenSSL3.5.9).
Dette er avgrenset pakke-/atferdskvalifikasjon, ingen generell sikkerhetsgaranti.
[Proxy](o6-gateway-deploy-20261101/proxy-regression.txt),
[ekstra runtime](o6-gateway-deploy-20261101/extra-runtime.json),
[skann](o6-gateway-deploy-20261101/gateway-qualification.json).

**GatewaySwitch fullførte med exit0; aktiv gateway startet1.11 kl.18:09:21 Oslo.**
Aktiv release er **93ee582b1a71a3f7552da1894b570366b89afee1**, gatewayimage er
**sha256:18f942c0107fa36b2fff8e11759d64ee08244fe115195e8e89bab03f4fc984c0**.
Gatewaycontainer **d4c197048bb79a6a6fa181094faeeb182be8c996a162b67e8cb766662f48377a**
erstatter den gamle gatewayen. Ny privat serverbackup ble tatt av switch før byttet.
Ingen tilbakeføring var nødvendig eller utført; previous er den umiddelbare
førversjonen **d367a0e47198aeecc52358258cb6825eecdc8c4a** med gammel gateway78e1858a….
[Deploykvittering](o6-gateway-deploy-20261101/deploy-receipt.json).

| Bevaringskontroll | Faktisk etter deploy |
|---|---|
| API | Samme containerb4eaf0a7…, image37b767ba…, PID1154760, oppstart31.10 og restartteller0. |
| Gate | Samme container2dd7409f…, image6bba55ec…, PID1154662, oppstart31.10 og restartteller0. |
| PostgreSQL | Samme container18203c23…, imageb0f9560a…, PID1154582, oppstart31.10 og restartteller0. Ingen ny PG-base/gosu eller migrering. |
| Tunnel | Samme MainPID1155012, ActiveEnterTimestamp31.10 og NRestarts0; ready200/fire forbindelser. |
| Vert | Samme boot-ID/kernel7.0.0-42/libc6/systemd259.5/cloudflared2026.10.6 og unit-/cloudflared-hasher. Ingen failed units, timer aktiv, fortsatt83GB ledig. |

API/DB healthy, aktiv Nginx-syntaks og origin-nekt bestod. Ti faktiske
origin-GET-er (fem stier uten assertion/med ugyldig syntetisk assertion) ga403/no-store.
Tre uautentiserte eksterne HTTPS-kall ga403 med no-store; dette kvalifiserer nekt,
ikke ny positiv MFA-/Access-matrise. Ingen token/cookie eller privat responsinnhold ble hentet.
[Etterstatus](o6-gateway-deploy-20261101/after.txt),
[origin](o6-gateway-deploy-20261101/origin-live-controls.json),
[eksterne nekt](o6-gateway-deploy-20261101/edge-live-controls.json).

En ekstra forsøk på å lese root-eid gateway-maintenance.json direkte som SSH-bruker
ble nektet. Tilgangsreglene ble bevart. Den identiske strukturerte kvitteringen var
allerede returnert av den autoriserte switch-handlingen og er brukt som evidens;
dette påvirket ikke deploy/etterkontroll. [Bevart lesefeil](o6-gateway-deploy-20261101/active-maintenance-receipt.txt).

Jonas gjennomførte ny privat nettleserøkt med Cloudflare-/appinnlogging, normal
visning/knapper, ufarlig endring i eget testutkast, lagring og oppdatering/gjenåpning.
Han bekreftet **«Alle fire bestod uten feil»** på den aktive gatewayreleasen.
Dette er funksjonsevidens, ingen aksept av resterende O6-risiko. Ingen tidligere
eierprøve er relabellet som denne prøven.

Windows-verktøyet nekter ny GatewayStage av allerede aktiv SHA før arkiv/bygg.
Dette beskytter de bevarte appimage-aliasene fra å bli overskrevet ved en utilsiktet
gjentakelse; stoppgrensen er prøvd lesende mot aktiv93ee582. Denne senere lokale
verktøy-/dokumentoppfølgingen endrer ikke deployet servercommit eller runtimeimages.

## Tilbakevei for dette trinnet

Ved gatewayfeil brukes `GatewaySwitch` til den eksisterende førreleasen
d367a0e47198aeecc52358258cb6825eecdc8c4a med forventet nåværende93ee582… og gammel
eksakt gatewayimage **sha256:78e1858a3c91b5f041230b979b1a6268f5578c155f7252eea15d95b95dcfa91f**.
Den samme kilde-/Compose-/livssyklusgrensen kontrolleres. Bare gatewayen returneres;
API/gate/DB/tunnel stoppes ikke. Ingen gammel dump gjenopprettes over nye skriv.
Eksisterende generell fullrelease-rollback er fortsatt tilgjengelig for separat
autorisert appvedlikehold; den er ikke brukt i dette avgrensede trinnet.

## Gjenstående O6-valg — ingen risikoaksept registrert

Detaljene/versjonene i [planens fire Debian-grupper og øvrige porter](https://github.com/IBE160-2026/G06-oisund/blob/841fbbe337860d06456abf21c6cd0e5501ad5ffc/docs/evidence/o6-maintenance-ready-20261101.md)
gjelder fortsatt. Gatewayutbedringen verken godkjenner eller lukker resten.

| Type / punkt | Betydning for denne serveren, tiltak og anbefaling | Konkret fra Jonas |
|---|---|---|
| **Risikovalg: util-linux** | Fire CVE-er krever privilegert mount/fstab/nsenter-bruk som dagens webtjenester ikke gjør. Ikke-root/read-only/cap_drop og tom fstab begrenser banen. Bevar disse og unngå privilegert diagnostikk på ubetrodde mål mens støttet Debian-rettelse mangler. | Ta stilling til midlertidig videre drift med disse grensene, eller be om mer avklaring før andre image-trinn. Ingen aksept er antatt. |
| **Risikovalg: ncurses** | Feilen ligger i infocmp med ubetrodd terminfo. Webflyten kjører ikke verktøyet, men det ligger i imaget. Anbefaling: ikke bruk det på fremmede data; følg stabil rettelse. | Samme avgrensede, midlertidige driftsvalg; eventuell fjerning av verktøy krever egen kvalifisering. |
| **Risikovalg/avklaring: ACL og SQLiteFTS5** | Bibliotekene finnes. ACL krever privilegert behandling av angriperkontrollerte stier; SQLite-feilen krever særskilt FTS5-SQL som appen ikke eksponerer (lageret er PostgreSQL). Hele native kallkjeden er ikke bevist utilgjengelig. Anbefaling: bevar sperrene og følg støttet rettelse; ikke bland ustøttede distro-pakker. Videre kilde-/reachabilitygransking er et alternativ til midlertidig aksept. [ACL](https://security-tracker.debian.org/tracker/CVE-2026-54369), [SQLite](https://security-tracker.debian.org/tracker/CVE-2026-119373). | Eksplisitt valg mellom midlertidig avgrenset restfare og videre analyse først. Aksept betyr ikke at funnene er rettet eller bestått. |
| **Risikovalg: kernel** | Kjente kernelproblemer består; noen lokale angrepsflater er relevante, andre kritiske triggere er ikke observert aktive. Siste isolerte pakkekontroll etablerte ingen støttet rettet målversjon. Anbefaling: følg Ubuntu og kvalifiser rettet kernel/konkrete tiltak før endring; fortsatt containerbegrensning erstatter ikke kernelrettelse. | Avklar midlertidig driftsrisiko mens rettet støttet mål mangler. Ingen kernel-/sysctl-/modulendring bestilles av dette valget alene. |
| **Neste rettelser: Python/pip og gosu** | De aktive V1-images har fortsatt gamle verktøykopier. Kvalifisert Python3.13.18/pip-fjerning og gosu1.20 finnes på kvalifiseringsbranchen. Gosus brukerparserfeil har avgrenset trigger i normal ikke-root-DB-start; de26 Go-standardbibliotektreffene er konkret avklart for den kontrollerte binæren. Anbefaling: eget kontrollert imagetrinn, etter Debian-disponeringen og faktisk PG-kollasjon/extensions/backup/restore. | Separat bestilling på de rettelsene; ingen generell aksept av scannerantall. Tekniske PG-forutsetninger skal kontrolleres før bytte. |
| **Tilgang og praktiske kontroller: systemd/cloudflared/libc6** | Isolerte pakke-/retur-/kildetester er bestått; fysisk boot/nett/SSH/PAM/NSS, autentisert tunnel og libc6-aktivering gjenstår. Oppdateringene retter ikke automatisk kernelrestene. Anbefaling: separate rolige vinduer med privat konfig-/pakke-/DB-backup og konsolltilbakevei. | Avtal når du kan være ved serveren med skjerm/tastatur og administratorinnlogging. Eventuelt sudo-passord skrives kun i din terminal. Det er ingen manglende tilgang som hindret dagens gatewaytrinn. |

Etterfølgende [isolert ACL-/FTS5-analyse](o6-acl-fts5-20261101.md) supplerer den
historiske tabellraden over: de kartlagte app-/gateflytene når ikke de berørte
funksjonene, med direkte produksjonsbinding av Python-/native filer. Bibliotekene
er fortsatt berørte. Administrativ bruk/annen kodekjøring og fremtidige endringer
er utenfor beviset; ingen midlertidig restfareaksept er registrert. Øvrige valg og
vedlikeholdsporter er uendret.

**O6 er fortsatt åpen. O3–O5 spores separat** på oppfølgingsbranchen med sine
opprinnelige eksterne/WAN/DNS-grenser. Ingen av disse lukkes av gatewaydeployen.
Full OS-/supply-chain-/firmwaredekning er ikke oppnådd eller erstattet med blank risikoaksept.

Alle81eksisterende lokale containere og31volumer er bevart i kontrollerte lifecycle-/image-/mount-felt. Alle tidligere kvalifiserte gateway/API/gate/PG-kandidatnavn peker fortsatt på sine eksakte gamle image-ID-er. Egne proxy-fixtures/nett er ryddet; nytt serverimage og offentlige artefakt-/skannercacher beholdes. [Bevaring](o6-gateway-deploy-20261101/preservation.json). Siste lesende sluttkontroll etter eiertesten bestod på samme93ee582/18f942c0…; [sluttstatus](o6-gateway-deploy-20261101/final.txt).
