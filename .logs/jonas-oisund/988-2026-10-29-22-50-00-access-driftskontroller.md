# Access-driftskontroller

## 2026-10-29 kl. 22:50 — Jonas Øisund

### Oppgave

Veilede og dokumentere to gjenværende kontroller av eksisterende Cloudflare-fjernaksess: annen faktisk medlemsidentitet mot eksakt e-postregel og ekte signert token replayet etter faktisk utløp. Bevare jonas, data, Access/MFA og eieradgang; ingen deploy, serverflytting eller bred sikkerhetsrevisjon. Commit/push uttrykkelig bestilt.

### Plan

- Lese AGENTS/CLAUDE, sesjonslogg-oppskrift, kvalifikasjonslogg, pilot-/driftsrapporter og faktisk status.
- Guide eieren trinnvis med separat B-profil, laveste medlemsrolle, negativ side/API-prøve og opprydding.
- Forberede skjult lokal DPAPI-lagring, signatur-/tjeneste-/førkontroll, faktisk venting og eksakt-token-replay uten fornyelse/redirects/appcookies.
- Dokumentere sanitert evidens, versjonsgrenser, feilforsøk, opprydding og eierens tunnelvalg.

### Resultat

Arbeid committet i `b6a98e0`: [full rapport](../../docs/evidence/access-operations-20261029.md), Capture/Replay/runner-JSON, konkret ventemetode og gjenbrukbar PowerShell-hjelper. Bare O1/O2-delen av leveranseregisteret og kvalifikasjonstillegget oppdatert; produktkode og V1-/Epic12-status urørt. Git diff --check, sanitiseringskontroll, JSON-parsing, skriptsyntaks/base64url/SHA256/klientkonstruksjon og faktisk før/etter-prøve bestod. Ingen token/cookieverdier, privat svarinnhold eller e-postadresse publisert.

Windows-driftscontainerne var stoppet. Eksisterende Ubuntu-release eb0eee3496d8999fb28615b49d4bf60124b6158f ble identifisert fra live status/current/release-identity og image-tags. Dette kvalifiserer ikke nyere integrert C1/D1–D3-kode. Image-digester/JS-bytebinding er ikke påstått; direkte Docker-lesing/generell sudo var utilgjengelig. Ingen ekstra privilegier ble gitt. Tidlige sandboxlesinger feilet og nødvendige lesekontroller ble gjentatt med verktøyets godkjente eskalering.

B ble Active med bare Minimal Account Access, nektet ved Cloudflare på side/API og fjernet igjen. Eier endret selv teamdomene under en etterspurt avlesing; dette er dokumentert, og medlemsprøven ble gjentatt på endelig bussassistent.cloudflareaccess.com med samme nekt og full opprydding. Første etter-endring-forløp uten observert MFA er beholdt; ny ren gjesteøkt krevde faktisk Authenticator. Eieradgang etter begge fjerninger bestod.

Tokenets signatur/issuer/AUD ble faktisk kontrollert. Førkontroll20:46:31–32UTC ga200/app-shell og401 uten appøkt. Ekte exp21:42:29UTC; samme token sendt21:42:50UTC ga302 til Cloudflare Access på begge mål uten privat respons. Ingen redirectfølging, tokenfornyelse eller klokkeendring. Dette er edge-evidens, ikke separat lokal gate-replay. Hjelpernes linjeskift-/dato-parsingsfeil før replay er rettet og bevart i rapporten. Gjestevinduet ble lukket under ventingen; lagret kopi muliggjorde fortsatt replay.

Token/binding/testmappe er slettet og runner avsluttet, begge kontrollert. B er fjernet. Eier bekreftet etter replay ny2FA og normal jonas-adgang. Tunnelen beholdes aktiv etter uttrykkelig beskjed, for separat Windows-av-prøve. Ingen passord/data/volum-/tjenesteendring utført av denne oppgaven. Dokumentasjon/logg publiseres med normal push; ingen force, tag, release eller kursinnlevering.

### Åpne punkter

- Ingen gjenstående arbeid innen de to bestilte testmålene. Det eksisterende sammensatte issues-punktet og O3–O6 står fortsatt åpne for øvrige Origin/CSRF/cache/timing/WAN/IPv6/DNS/OS-bevisgrenser; de er ikke prøvd eller godkjent utsatt her. Rapporten bevarer begrensningene om lokal gate, versjonsbinding og MFA-matrise.

## 2026-11-01 kl. 18:22 — Jonas Øisund

### Oppgave

Gjennomføre bare teknisk klart O6-gatewaytrinn med nødvendig integrering/push/deploy, verifisert backup/tilbakevei/etterkontroll og personlig brukerprøve. Bevare passordarbeid, alle øvrige komponenter/miljøer og V1-tag; presentere konkrete resterende risikovalg, tilgang og praktiske kontroller uten å godkjenne restfare.

### Plan

- Lese instruksjoner, [kvalifisert gateway og siste plan](../../docs/evidence/o6-gateway-deploy-20261101.md), fersk origin/main og faktisk produksjon.
- Integrere bare identisk gateway-FROM og nødvendig avgrenset driftsmodus: standarddeploy stopper ellers API/gate/tunnel.
- Ta fersk privat backup/Windows-hash og isolert fullrestore, stage uten aktivering, hente/hashbinde og kvalifisere faktisk serverimage.
- Bytte bare gateway med kilde-/Compose-/forventet SHA/image- og lifecycle-porter, kontrollert gatewaytilbakevei og faktiske tekniske/eieretterprøver.
- Dokumentere faktisk versjon/image, bevaring og resterende O6-valg; publisere dokumentasjon og egen loggcommit.

### Resultat

Fersk main5cee9e0 og ren kontrollcheckout. Ny arbeidsbranch maintenance/gateway-o6-20261101 fra origin/main; andre lokale/remote kvalifiseringsbrancher og checkoutmiljøer beholdt. Produktendring er bare runtime-FROM identisk med kvalifisert5333138/nginx1.30.6-slim/dede8895…. Backend/frontend/gate/PG-Compose/låser/migreringer/refleksjon er uendret og passordarbeid ikke med. Arbeidscommit82a4b68 er integrert i main med **93ee582b1a71a3f7552da1894b570366b89afee1**, pushet før staging. Serverdeploy er denne eksakte SHA-en, ikke senere dokumentcommits.

Driftsverktøyets GatewayStage/GatewaySwitch tillater avgrenset utrulling. Eksisterende stage bygde/cachet hele releasen, men midlertidige appbuilds ble aldri startet. Switch binder nye API/gate-aliaser til eksakt aktive V1-image-ID-er før kun gateway up --no-deps/--no-build/--pull never. Kilde/Compose utenom gateway skal være identisk; full forventet current-SHA og kvalifisert image-ID må stemme. Non-gateway container-ID/image/PID/start/restarts, tunnel og boot sammenlignes. Feil gir bare gatewaytilbakeføring, ingen blind DB-restore.18isolerte Linux-driftstester bestod. Etterpå ble lokal Windows-GatewayStage sperret på aktiv SHA før nytt bygg; forventet avvisning faktisk prøvd lesende. Ingen ny runtime-deploy av denne Windows-sperren.

Fersk Windows-backup66495byte, SHA256 **5bf90e546527d6edad7ef06a2f15e89089afb38a23da794361e66bef70edfd05**, overføringshash/ACL verifisert. Separat fersk dump bestod network-none/tmpfs-restore med alle tabellfingeravtrykk like; ingen produksjonsrestore eller backupbyte i Git. Switch tok ytterligere serverbackup umiddelbart før byttet.

Faktisk serverbygget gateway **sha256:18f942c0107fa36b2fff8e11759d64ee08244fe115195e8e89bab03f4fc984c0** er annet artifact enn bevart lokal3cae…. Derfor eksportert offentlig gatewayimage, overføringshash4c738c72… og lokal/server-ID/rootfs-layers like, så ny kvalifikasjon før aktivering. Fem stier×24syntetiske JWT-varianter/cookies/header/OriginCSRF/no-store/gate-down, statiske appbyte/faktisk JS-CSS-levering, nginx-syntaks, ti upstreamfeil og egen API-down bestod. SammeTrivy0.76.1/DB1.11 kl13:02: 0treff i21runtimepakker. Ingen ny generisk sikkerhetsgodkjenning.

GatewaySwitch exit0; gateway startet **1.11 kl.18:09:21 Oslo**, containerd4c19704…, aktiv release93ee582 og image18f942c0…. Previous er d367a0e og gammel gateway78e1858a…; ingen rollback nødvendig/utført. API/gate/DB har eksakt tidligere containere, images37b767ba/6bba55ec/b0f9560a, PIDs1154760/1154662/1154582, start31.10 og restart0. TunnelMainPID1155012/start31.10/NRestarts0 er uendret; ready200/fire forbindelser. Samme boot44c550dc, kernel42/libc/systemd259.5/cloudflared2026.10.6 og fire unit-/cloudflared-hasher. Bare driftsverktøy installert med daemon-reload, ingen pakkeoppdatering eller annen tjenesteomstart. App/DB healthy, ingen failed units, backup-timer aktiv,83GB ledig.

Ti direkte origin-GET-er uten/med ugyldig syntetisk assertion ga403/no-store; tre uautentiserte eksterne HTTPS-kall ga403/no-store. Ekte ny privat Cloudflare-/appinnlogging, visning/knapper, ufarlig egen testutkastendring/lagring og refresh/gjenåpning ble personlig gjennomført; Jonas bekreftet **«Alle fire bestod uten feil»**. Funksjonsaksepten er ikke restfareaksept. Etter eiertesten bestod siste lesende status på samme93ee582/18f942c0.

Et ekstra cat-forsøk på root0600-kvittering ble korrekt nektet; ingen tilgang endret. Switchens allerede returnerte JSON-kvittering gir samme nødvendige før/etterevidens. En lokal kontroll leste først kun stdout for forventet PowerShell-avvisning, så ble korrekt stderr-kvittering avstemt; ingen ny serverstaging utført. Rå feilforsøk beholdes.

Alle81eksisterende lokale containere/31volumer og de fire tidligere kvalifiserte imagealiasene er bevart. Ingen gjenværende egne probecontainere/nett; offentlig serverimage/cache beholdes. [Full rapport og beslutningstabell](../../docs/evidence/o6-gateway-deploy-20261101.md),55evidensfiler inkl.indeks, syntaks/JSON/lenker/høysignalhemmelighetssøk/diff --check kontrollert. Dokumentasjon/Windows-sperre **f8184cb2fbd8c887a49ab715c379c67132b4a2b8** er pushet og remoteverifisert. Main-dokumentasjon er nyere enn aktiv serverrelease. Gatewaybranch5333138 og øvrig kvalifiseringsbranch841fbbe er urørt. V1-tagobjekt38bfb0d… og mål d367a0e er uendret; ingen ny tag/release/kursinnlevering.

### Åpne punkter

- O6: util-linux/ncurses/ACL/SQLiteFTS5 har konkrete midlertidige restfare-/reachabilityvalg som må tas av Jonas. Ingen aksept er registrert. Kernel har fortsatt ingen etablert støttet rettet kandidat; midlertidig driftsrisiko og videre leverandør-/kvalifikasjonsoppfølging er separate valg.
- Python/pip/gosu-kandidater og senere PG-metadata/restore før eventuell oppdatering krever eget avgrenset løp; ingen av dem ble deployet her. systemd/cloudflared/libc6-aktivering trenger senere bestilling, privat backup/pakke-/konfigtilbakevei, administratorbetjening/lokal konsoll og faktiske nett/SSH/tunnel/boot/eiertester.
- O3–O5 beholder separat ekstern/WAN/DNS-oppfølging; libc6-markør og langtidsstabilitet beholdes i sine eksisterende punkter. Ingen O6-lukking av gatewaykvalifikasjon eller positiv eiertest.
