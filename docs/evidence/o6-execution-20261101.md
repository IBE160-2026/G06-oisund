# O6 gjennomføring — 1. november 2026

## Faktisk status ved kontrollpunktet

Ny uttrykkelig vedlikeholdsautorisasjon er mottatt. Produksjonen er kontrollert før arbeid: aktiv release **93ee582b1a71a3f7552da1894b570366b89afee1**, gatewayrettelsen fra tidligere kjøring er aktiv. API/gate/PG, systemd259.5-0ubuntu3.4, cloudflared2026.10.6, kernel7.0.0-42 og boot44c550dc er uendret. API/database healthy, tunnelready200/fire forbindelser, origin uten assertion403, backup-timer aktiv og ingen failed units. [Førkontroll](o6-execution-20261101/before.txt), [etter staging](o6-execution-20261101/after-staging.txt).

## Gjennomført

- Ny Windows-backup med verifisert overføringshash: `20261101T203510Z-93ee582b1a71a3f7552da1894b570366b89afee1.dump`, SHA256 **04ff0a8e8b6741c377996ef276b859dccb5c744697fc20de4aebaa0c25f65195**. Backupbyte ligger privat utenfor Git. Separat fersk serverdump20:35:13UTC ble gjenopprettet isolert uten produksjonsvolum; alle tabellfingeravtrykk like. [Backup](o6-execution-20261101/backup-windows.txt), [restore](o6-execution-20261101/backup-restore.txt).
- Selektiv integrering av kvalifiserte Python3.13.18/pip-fjerning, PG17.11/gosu1.20 og all-image-forkontroll fra bevart kvalifiseringsbranch. Nyere gatewayguard/tilbakevei er bevart. Arbeidscommit **e0ad930**, integrert og pushet i main som **5e521cbc658594a47c4568d352a50e46309573c4**. ACL-/FTS5-analysen er også integrert. Ingen passordfunksjonalitet, låse-/migrerings-/appkode-/refleksjonsendring.
- Samlet integrasjonskontroll: **20 Linux-driftstester bestod**. Fast lesende database-summary er utvidet med PG-versjon/kollasjon/extensions; SQL prøvd i egen disponibel PG/tmpfs og deretter faktisk produksjon. Ingen privat rad-/konto-/sesjonsverdi leses ut.
- Releasen5e521cb er **bygget/staget, ikke aktivert**, med eksisterende GatewayStage som bare bygger og installerer driftsverktøy. Denne actionens navn innebærer ingen gatewayaktivering. Driftsverktøy/unitfiler er installert med daemon-reload; ingen container/tjeneste eller maskin er restartet. [Full kvittering](o6-execution-20261101/stage-only.txt).
- Faktisk database: **PG17.11**, provider c, en_US.utf8, både lagret/aktuell kollasjonsversjon null; bare plpgsql1.0. 14 migreringer. Dette erstatter tidligere manglende produksjonsmetadata, men er ikke full kvalifikasjon av alle mulige kollasjons-/extensionscenarioer. [Lesende metadata](o6-execution-20261101/production-db-metadata.txt).
- Vertens nåværende apt-lister tilbyr de kvalifiserte ti systemdpakkene259.9-0ubuntu0.1. Lesende apt-simulering: **10 oppgraderinger, ingen nye/fjernede pakker**. Ingen apt-update/install utført.20 lokalt bevarte gamle/nye deb-er er hashkontrollert mot kvalifiseringen. De er ennå ikke overført til konsolltilgjengelig gjenopprettingssted, og privat OS-konfigbackup gjenstår før OS-endring.
- Trivy-databaseoppfriskning og ny skanning av **bevarte lokale kvalifiserte kandidater**, ikke de nye serverbyggene: API/gate46high, ingencritical; PG1critical/25high/30medium. Samme sentrale resttall som før, med tidligere konkrete Debian-/Go-disponeringer; ingen ignoreliste. Skannerens ArtifactID er ikke automatisk samme identifikator som Docker-inspect/OCI-index-ID. Dette er ikke etter-deploy-skanning. Rårapporter er komprimert og sammendrag merket med riktig miljø.
- [Produksjonsidentiteter etter staging](o6-execution-20261101/staged-and-active-identities.txt) viser samme fire aktive container-ID/image/PID/start/restart og tunnel som før. Det nye staged gatewayimaget er et annet artefakt; det er ikke erklært lik den kvalifiserte aktive gatewayen.

## Stoppporter og minste neste handling

Den tidligere [vedlikeholdsplanen](https://github.com/IBE160-2026/G06-oisund/blob/841fbbe337860d06456abf21c6cd0e5501ad5ffc/docs/evidence/o6-maintenance-ready-20261101.md) krever D1 før Python/imageaktivering og fysisk konsoll/tilbakevei før systemd/nett/tunnel/omstart. Ny generell vedlikeholdsautorisasjon er **ikke risikoaksept**. Én samlet eierforespørsel er sendt om midlertidig avgrenset restfare og faktisk konsoll-/administratorberedskap; svar er ikke mottatt ved dette kontrollpunktet.

1. **Eierbeslutning D1/D2:** velg midlertidig videreføring med dokumenterte barrierer for util-linux/ncurses/installerte ACL-/FTS5-biblioteker og fortsatt kerneloppfølging, eller fortsatt utsett berørte trinn. ACL/FTS5 er verifisert utenfor kartlagte normale appflyter, ikke rettet i imagene. Risikoaksept registreres først ved uttrykkelig beslutning.
2. **Praktisk gjenopprettingstilgang:** eieren må bekrefte prøvd lokal administratorinnlogging, skjerm/tastatur/strøm og GRUB-tilgang før OS-/tunnel-/boottrinn. Generell sudo krever fortsatt interaktiv administratoreksport/betjening; passord skal ikke sendes i chat. Privat OS-konfigbackup og tilgjengelige gamle pakker må verifiseres før endring.
3. **Tekniske aktiveringsporter består:** bind faktisk staged imageinnhold til kvalifisering før aktivering; nye artefaktavvik må vurderes/skannes/testes etter behov. Ny frisk backup/restore ved senere vindu hvis dagens resultat er blitt utdatert. Aktiver i planens rekkefølge med helse, tilgang/tunnel, personlig lagring/gjenåpning og relevant faktisk etter-skanning før neste trinn. Ved feil: dokumentert retur; ingen blind databaseoverskriving.
4. Ingen dokumentert støttet rettet kernel er etablert. Omstart med42 aktiverer ikke en kernel-CVE-rettelse. Påkrevd ny boot-/nett-/tunnelkontroll og videre stabilitetsobservasjon er **ikke utført eller lukket**. Ingen observasjonstid er oppfunnet som et fullført krav.

**O6 er fortsatt åpen:** kvalifiserte rettelser er integrert/staget, men øvrige runtime-/vertsrettelser, eierporter, faktisk etterkontroll og stabilitetsoppfølging er ufullførte. Gatewaydelen er allerede fullført historisk. O3–O5 spores separat. v1.0.0 beholdes på d367a0e; ingen ny tag/release. Andre branches, kvalifiserte kandidater og eksisterende miljøer er bevart. [Evidensindeks](o6-execution-20261101/index.json).

## Etterfølgende uttrykkelig eierbeslutning

Jonas har nå akseptert midlertidig restfare for util-linux, ncurses, ACL/FTS5 og kernel med dokumenterte barrierer, og bekreftet prøvd lokal administratorinnlogging samt fysisk strøm/skjerm/tastatur/GRUB-beredskap. [Ordrett beslutning](o6-execution-20261101/owner-decision.json). D1/D2 og bekreftelsen av konsollberedskap er dermed gitt; de historiske ventepunktene over beskriver forrige kontrollpunkt. Dette er ingen påstand om rettede biblioteker/kernel eller lukket O6. Generell sudo krever fortsatt eierens interaktive terminalbetjening.

Fersk lesende kontroll ved gjenopptakelse bestod på samme93ee582. Komplett fire-image eksportfunksjon er prøvd lokalt og fjernet etter testen; hashkontrollert preflightskript er klargjort for eierkjøring. Det skal eksportere faktiske serverimages og lage root-beskyttet systemkonfigbackup uten aktivering. Resultat registreres først etter innhenting og kontroll.

De22 gamle/nye systemd-/cloudflared-debene er nå overført til den private arbeidsmappen på serveren; alle overføringshasher er kontrollert. Ingen installasjon utført. Flytting til root-beskyttet konsolltilbakevei og endelig hashkontroll skal gjøres før OS-trinnet. [Overføringskontroll](o6-execution-20261101/recovery-package-transfer.json).

## Utført containeraktivering — 1. november kl.22:30 Oslo

**Aktiv serverrelease er nå5e521cbc658594a47c4568d352a50e46309573c4**, med ny Python3.13.18/pip-fjerning og PG17.11/gosu1.20. Tidligere93ee582 er dokumentert tilbakevei; migreringene er uendret. Historiske avsnitt ovenfor beskriver før-/stagingpunktene. Senere dokumentasjonscommits er ikke deployet.

Administratoreksporten er fullført: alle fire eksporterte image-ID-er/rootfs-lag stemmer mellom server og lokal Docker etter hashkontrollert overføring. Beskyttet systembackup `/var/backups/bussassistent/o6-pre-5e521cbc/host-config.tar` har SHA25686e3fd3246c6ab65d1d3ba0021f1831cd7cd34c7be4b45c939105aa2a075bc87, kontrollert arkivliste og0600/root-eierskap i0700-mappe. Ingen privat arkivbyte er hentet til Git. [Kvittering](o6-execution-20261101/admin-preflight-result.json).

| Faktisk kjørende rolle | Eksakt eksportert/testet image-ID |
|---|---|
| api | `sha256:65b4f7dd8e336198175fdbc10e0a3ed2ba68118426ab54d36e751cded7173bdf` |
| access-gate | `sha256:f9c4a48c92b644c638359573dd44a8b5f55c79cb018e0c3c544748cb55cd3aa5` |
| postgres | `sha256:c078a9092712e11deb68fa2b3ee7ce0f5c59cb0b76ffac8f9c7022580a5ef806` |
| gateway | `sha256:b37608187e86507cefc1d79995fdfd631cae3e3f9490dc96d0fea89e996bcb75` |

Full lokal filesystem-sammenligning av aldri startede egne containere: PG/gateway identiske i filinnhold og valgte rettigheter/linker. API-avvik1345=1276bytekodehoder+69mode755→644; gate120=118bytekodehoder+2mode755→644. Alle kompilerte payloads etter16bytehode er identiske (1436/280pyc kontrollert). Alle øvrige filbytes, native biblioteker, eiere og linker er like; kildefiler/migreringer er fortsatt lesbare av uid10001. Docker-genererte hosts/hostname/resolv.conf og virtuelle dev/proc/sys er avgrenset bort. Ingen runtime-/produksjonsvolum er eksportert. [Forskjeller](o6-execution-20261101/staged-filesystem-comparison.json), [bytekodebinding](o6-execution-20261101/pyc-payload-binding.json).

Ny faktisk-serverimage-skanning: gateway0treff, API/gate46high utencritical, PG1critical/25high/30medium. Samme sentrale restfunn som de kvalifiserte kandidatene, med eksisterende konkrete Debian/Go-disponeringer og eierens uttrykkelige midlertidige risikoaksept. Ingen ignoreliste eller generell sikkerhetsgodkjenning. Førskanningens artefakter er nå bundet til faktisk aktive ID-er; den er ikke relabellet som en uavhengig runtime-forensisk skanning.

Fordi filrettigheter/byggartefakter var forskjellige, ble relevante kontroller kjørt på de faktiske serverimagene før aktivering: isolert Uvicorn/PG15familier og75Origin/CSRF-negative kontroller, svar-tap/oppslag/replay; faktisk innlogget HTTP-PDF200, ikke-PDF422, utenøkt401, utenCSRF403; gate26negative JWT-varianter/25HTTP-kall. Alle bestod, med null ACL/SQLite-events i instrumenterte flyter. Tidligere komplette327/private/PDF- og øvrige kvalifiseringer gjenbrukes på det dokumenterte identiske kode-/native grunnlaget, ikke som ny fulltestkjøring.

Fersk Windows-backup20261101T212947Z-93ee582b1a71a3f7552da1894b570366b89afee1.dump SHA2562135c3479094ecd668e0ed39f10cef9248f1abd4292e33cf93b9ae55287a1743 og ny separat isolert restore bestod umiddelbart før deploy. Eksisterende deployverktøy tok også backup med skriverne stoppet. Deploy exit0; alle25tabellfingeravtrykk før/etter er identiske, alle fire kjørende image-ID-er matcher de kontrollerte artefaktene, ingen tilbakeføring nødvendig. API/database healthy, origin uten assertion403, tunnelready200/fire forbindelser, timer aktiv, ingen failed units. Ny tunnelPID2749754 etter autorisert full appdeploy; boot/kernel/vertsversjoner er uendret. [Aktivering](o6-execution-20261101/activate-container-release.txt), [samlet verifikasjon](o6-execution-20261101/container-activation-verification.json), [helse](o6-execution-20261101/after-container-activation.txt).

Personlig innlogging/visning/lagring/gjenåpning er etterspurt på denne nye releasen; resultat **avventes** før neste trinn. Systemd259.9/cloudflared2026.10.7 er ennå ikke installert. Énfase-hjelperen er klargjort/hashkontrollert på serveren med innebygde22pakkehasher, beskyttet pakkekopi/tilbakevei, backuphashkontroll, strengt simulert ti-pakkesett, unit-/helsekrav og kontrollert gammelpakkeretur ved feil. Pakkeløsningens negative stoppkontroller bestod; dette er ikke en påstand om allerede utført vertsvedlikehold. Sudo-betjening gjenstår når brukerflytporten består. Kernel-/libc6-boot og faktisk stabilitetsobservasjon forblir åpne. O6 er fortsatt åpen; O3–O5 separat.

## Container-eiertest bestått; systemd-kjøring klargjort

Jonas bekreftet **«bestått»** på den etterspurte nye private Cloudflare-/appinnloggingen, normal visning, ufarlig egen utkastlagring og refresh/gjenåpning på5e521cb. [Eierresultat](o6-execution-20261101/container-owner-test.json). Dette lukker den personlige kontrollporten for containertrinnet, ikke heleO6.

Ny faktisk førkontroll bestod på samme aktive5e521cb med uendret boot/vertsversjoner, friske tjenester, tunnelready200/fire forbindelser og tilgangsnekt uten assertion. Fersk Windows-backup og separat fersk isolert restore bestod også etter eiertestens lagring. Hashen til den klargjorte systemdhjelperen er fortsatt identisk lokalt/server: e53c6401a243ea21bc7e4eb6aa4f0159467e9e0189b3c4b5c537c66dba2fb05e.

Fordi generell sudo fortsatt krever interaktiv administratorbetjening, har Jonas fått den konkrete kommandoen `sudo python3 /tmp/ibe160-o6-window.uNfjQHcy/host-step.py systemd` for **lokal terminal på Ubuntu**, slik at SSH-brudd ikke avbryter kjøringen. Denne er den allerede autoriserte ti-pakkeoppdateringen med backup-/tilbakevei-/helseporter; ingen ny vedlikeholds- eller risikoaksept etterspørres. Resultatkvitteringen må hentes og kontrolleres før systemd erklæres utført og før cloudflared-trinnet. Ved dette dokumentasjonspunktet er kjøringen **forespurt, ikke verifisert fullført**. Ingen maskinomstart eller kerneloppdatering er utført.

## Systemd-forsøk: ventende lesende førkontroll, ikke oppdatert

Etter eierens «kjørt ferdig» manglet `systemd-result.json`; første innhenting feilet derfor og er beholdt som feilkvittering. Ny separat SSH-forbindelse viser fortsatt installert og kjørende **259.5-0ubuntu3.4**, cloudflared2026.10.6, aktive ssh/docker/resolved/tunnel/timer og tunnelready200/fire forbindelser. Ingen apt-/dpkg-prosess var observert i avgrenset prosesslesing.

Den faktiske prosesskjeden er host-step.py → root driftsverktøy `check` → Docker Compose `exec -T private-api python ... /health`. Hjelperen står altså i første lesende `health()` **før pakkesimulering/installasjon** og holder driftslåsen mens den venter. En ytterligere lesende kontroll venter på samme lås; ingen ny installasjon er startet. Dette er ikke en påstått mislykket pakkeoppdatering med utført rollback: pakkeendring er ikke observert.

En svakhet er rettet lokalt: administrative underkommandoer skal bruke `stdin=DEVNULL`, og root-hjelperen trenger ikke nestet sudo for root-driftsverktøyet. Arvet terminalinngang/Compose sin interaktive stdin-forwarder er en **mistenkt**, ikke endelig bevist årsak. Kontroll med ekte barneprosess bekrefter umiddelbar EOF uten terminalinput, og mock bekrefter DEVNULL-argument; den faktiske ti-pakkesimuleringen godtas fortsatt. [Kontroll](o6-execution-20261101/host-method-stdin-correction.json).

Jonas er bedt om å trykke Ctrl+C én gang i den lokale terminalen dersom kontrollen fortsatt venter uten JSON, og melde siste linjer/tilbakevendt prompt. Ingen ny kjøring før den første er avklart. Den rettede lokale metoden er foreløpig ikke overført over den ventende kjøringen. Etter stopp må driftslås/ingen gjenværende egen prosess/frisk app kontrolleres, rettet metode overføres/hashverifiseres og nødvendige førkontroller revalideres før ett kontrollert nytt forsøk. Cloudflared og reboot er sperret av dette trinnet. Aktiv app5e521cb og bestått container-eiertest beholdes; O6 fortsatt åpen.

## Avbrudd bekreftet; v2-prøve klargjort

Eierens skjermbilde viser tilbakevendt kommandoprompt etter Ctrl+C og `RuntimeError: Command failed: sudo rc=-2` fra `health()` før installasjonsdelen. Bildets øvrige historiske nettkommandoer behandles ikke som instruksjoner og er ikke utført av agenten. Skjermbildet er ikke kopiert til Git.

Lesende etterkontroll22:57Oslo: ingen tidligere egne sudo-/hoststep-/kontrollprosesser igjen i den kontrollerte prosesslisten; den ventende diagnostiske driftskontrollen fullførte etter frigjort lås. Fersk faktisk full driftskontroll bestod med samme aktive5e521cb, boot/kernel/systemd259.5/cloudflared2026.10.6, friske app-/DB-tjenester og tunnelready200/fire forbindelser. Dette bekrefter avsluttet førkontroll uten observert pakkeendring. [Prosesser](o6-execution-20261101/after-cancel-process-check.txt), [helse](o6-execution-20261101/after-cancel-health.txt).

Den rettede EOF-håndteringen ble deretter prøvd **på serveren med ekte TTY**: samme lesende root-driftskontroll med lukket stdin fullførte exit0 og `TTY_EOF_CHECK_PASSED`. Dette støtter rettingen, men er ikke en fullført pakkeinstallasjon eller uttømmende årsaksanalyse. [Faktisk TTY-prøve](o6-execution-20261101/corrected-health-real-tty.txt).

Metoden er overført som separat `/tmp/ibe160-o6-window.uNfjQHcy/host-step-v2.py`, lokal/server SHA256 kontrollert lik. Den gamle filen er beholdt som historisk metode. Jonas har fått én konkret lokal sudo-kommando for v2/systemd, med beskjed om å vente på JSON og prompt og holde nettforbindelsen uendret. [Binding og metodehash](o6-execution-20261101/host-method-v2-prepared.json). Resultat av det nye forsøket avventes; ingen systemd-/cloudflared-/boot-endring erklæres fullført her. O6 er fortsatt åpen.

## Systemd v2: forsøk feilet, frisk gammel tilstand kontrollert

Eierens rapport er avstemt med faktisk [v2-resultat](o6-execution-20261101/systemd-v2-result.txt):passed=false,rollback_used=true,rollback_health_passed=true,unit_hashes_preserved=true. Alle22returpakker og systembackuphash ble verifisert. RuntimeError mangler opprinnelig kommandoutskrift i v2, så kvitteringen identifiserer ikke alene den konkrete feilen. Returflagget betyr at gammelpakke-/helsekommandoene bestod; det beviser ikke at nye pakker faktisk rakk å bli installert.

Separat etterkontroll23:01Oslo bekrefter **alle ti pakker og kjørende PID1 på259.5-0ubuntu3.4**, ingen dpkg-auditfeil, ny SSH fungerer, fem nødvendige tjenester aktive, standardrute og faktisk navneoppslag fungerer. App5e521cb/API/database er friske, tunnelready200/fire forbindelser og prosjektets fire unit-hasher er uendret. Kernel/boot/cloudflared er uendret. [Pakker/PID1/nett](o6-execution-20261101/systemd-v2-package-manager-check.txt), [full helse](o6-execution-20261101/after-systemd-v2-return.txt). Ingen neste fase startet på grunnlag av dette feilresultatet.

### Isolert reproduksjon og cache-retting

Samme APT-installasjonsform ble prøvd i disponibel Ubuntu-testcontainer med network=none, identiske deb-er og privat0700-katalog/0600-filer. Første test traff testimagets Python-entrypoint i stedet for shell; korrigert prøve er bevart separat. Korrigert opprinnelig `--no-download`-form feilet med exit100/«Unable to fetch some archives». En avklaringsprøve uten denne flaggen viste Permission denied for filene i privat katalog og forsøkt fallback til Ubuntu-arkivet, som var utilgjengelig i det frakoblede miljøet. Prøven forklarer en konkret feil i den nye installeringshjelperen; opprinnelig vertsstderr er ikke bevart, så identisk vertsårsak kan ikke påstås direkte observert.

Når kun de verifiserte **offentlige deb-ene** legges i standard APT-arkivcache, består samme frakoblede installasjon. Hjelperen er derfor rettet til å hashkontrollere og kopiere kun de valgte offentlige pakkene til `/var/cache/apt/archives`, med hash-/symlinkkontroll og uten overskriving av andre cachefiler. Private konfigbackuper/returkataloger åpnes ikke. APT beholder `--no-download`; ekstra uventede pakker avvises fortsatt i forkant.

Den faktiske rettede `install()`-funksjonen er prøvd **gammel→ny→gammel**, alle ti pakker kontrollert etter hver fase, med network=none. Alle tre faser bestod, privat backupkatalog beholdt0700. Dette er pakke-/returkvalifisering, ikke en ekte PID1-/SSH-/Lenovo-oppstartstest. [Full prøve](o6-execution-20261101/systemd-corrected-cache-roundtrip.txt), [metode](o6-execution-20261101/cache-roundtrip-method.py). Hjelperen lagrer nå full kommandoutskrift i root-beskyttet forsøkslogg og returnerer sikker failure_message/loggsti i feilkvitteringen; private logger lastes ikke automatisk til Git.

Ny separat `host-step-v3.py` er overført og hashkontrollert, frisk faktisk gammel tilstand bekreftet igjen. [Metodebinding](o6-execution-20261101/host-method-v3-prepared.json). Jonas er guidet til én lokal v3/systemd-kjøring, ikke bedt om ny risiko-/vedlikeholdsaksept. Resultatet avventes. Ingen systemd-retting, cloudflared-oppdatering eller omstart erklæres fullført i dette kontrollpunktet; O6 forblir åpen og O3–O5 separat.
