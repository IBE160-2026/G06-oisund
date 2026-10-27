# Sikkerhetsgjennomgang for nettbrettilgang

Gjeldende tunnelarbeidsflyt: eier ber nå om klargjøring av trinn 2. Piloten bruker videre en navngitt dashboardstyrt tunnel med token-fil, ikke det eldre lokale CLI-/cert.pem-utkastet nedenfor. Se [tunneloppsett og konkret publiseringsgrense](tablet-tunnel-setup.md). Ingen tunnel-ID/token, DNS-rute eller kjørende tunnel er etablert av agenten på dette tidspunktet; publisering avventer uttrykkelig godkjenning.

Gjeldende driftsstatus: eier har nå godkjent trinn 1, og den isolerte lokalpiloten kjører med bare fiktive data. Se [lokalpilotens resultat og stoppkommandoer](tablet-local-pilot.md). Ingen ekstern publisering, DNS-endring eller tunnelstart er godkjent eller utført. De opprinnelige forberedelsesstatusene og aktiveringsplanen nedenfor må leses sammen med denne senere, konkrete statusen.

Oppdatering 2026-10-26: 11.6 og retrospektivet er godkjent. Forberedelsene er overført til en separat kandidat på `f5ffa4bf64696b8e1abf910ccd8ac106663d30a9`, branch setup/tablet-remote-access-11-6. Se [gjeldende integreringsresultat](tablet-11-6-integration.md). Base/worktree og formuleringer om ventende 11.6 nedenfor beskriver opprinnelig forberedelse; nye kontroller og avgrensninger står i integreringsrapporten. Aktivering er fortsatt ikke godkjent eller utført.

Status 2026-10-26: lokalt forberedt og isolert testet. Ingen ekstern tilgang aktivert. Dette er gjeldende plan; den første rapporten i tablet-remote-access.md er historisk.

Branch: setup/tablet-remote-access. Base: aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed (11.4).
Worktree: C:\Users\Jonas\.codex\.chatgpt-projects\g-p-6ab6b4c1c6888191a96d3242fab912b4\tablet-remote-access.

## Avklarte forhold og grenser

- Eier har nå selv opprettet Cloudflare-konto og Cloudflare One Free, samt registrert bussassistent.com. Konto-/domeneoppsettet er brukerutført; det innebærer ingen tillatelse til DNS-rute, tunnelstart eller pilotoppstart. Se status nedenfor.
- Det finnes ingen Cloudflare-connector i tilgjengelig plugin-søk. Kontogjennomgangen bygger på eiers opplysninger og skjermbilder, ikke direkte API-/dashboard-avlesning. Ingen passord, koder, nøkler, token eller recovery-koder ble bedt om eller lest av agenten. Ingen eksterne kontoendringer er utført av agenten.
- Alt eget arbeid er i worktreet. Ingen produktkode fra det ukommitterte 11.5/11.6-arbeidet er kopiert. Ingen integrering, staging, commit, merge, push eller story-/retrostatusendring er gjort. Ingen ordinær container, database, brannmur, ruter eller DNS er operert av denne oppgaven. Den andre chatten kan samtidig endre sitt miljø; ingen påstand om globalt uendret miljø fremsettes.
- Før aktivering må godkjent 11.6 integreres og prøves særskilt. Et vellykket testbygg fra denne basen er ikke en godkjent 11.6-leveranse.

## Nåværende utforming

### Brukerutført Cloudflare-oppsett – rapportert 2026-10-26

- Registrar: Cloudflare; bussassistent.com rapportert Active, utløp 2027-10-26. Oppgitt fornyelse USD 10.46/år med automatisk fornyelse 2027-09-26. Ingen senere pris eller endelig NOK-/avgiftsbelastning er verifisert.
- Administrator: eget passord opprettet etter Google-registrering. Eier bekrefter vellykket innlogging med 2FA via Microsoft Authenticator. Recovery-koder er lagret som passordbeskyttet secure note i Dashlane, tilgjengelig på PC og telefon; opprinnelig lokal fil rapportert slettet. Google-kontoens egen MFA, medlemmer, aktive økter og audit er ikke fullstendig kontrollert.
- Teamdomene: bussassistent.cloudflareaccess.com. Forventet issuer: https://bussassistent.cloudflareaccess.com.
- App: app.bussassistent.com, tomt Path-felt (hele vertsnavnet). AUD oppgitt av eier: `11605406740b9e66f584e9bfc11d3db52f18585de0708c6d5b2741d0268fbbfa`. Dette er en offentlig identifikator, ikke et token. Verdien er registrert, men ikke kontrollert mot et ekte signert Access-token. Ved sletting/gjenoppretting av appen må AUD leses på nytt.
- Én Allow-policy «Kun meg – Bussassistent»: Include Emails kun eiers uttrykkelig valgte kontoidentitet, Require Login Methods Cloudflare. Den konkrete adressen fylles lokalt ved runtime-forberedelse. Ingen brede tillatelser er godkjent. Cloudflare-provider har Restrict to account members på ifølge eier.
- Policy-skjermbildet viser 1h økt og eksplisitt independent MFA: bare Authenticator application, Prompt for MFA on every log in. Eier valgte denne metoden fordi han ikke har sikkerhetsnøkkel. Eier rapporterer separat Authenticator-registrering via App Launcher Account; faktisk tvungen MFA for denne appen er ennå ikke bevist.
- App Launcher-innlogging er rapportert vellykket; NoApps-siden under oppsett var ikke en prøve av appens tilgangskontroll. Eier rapporterer at appinnstillinger er valgt og lagret etter gjennomgang. Cloudflare er eneste tilgjengelige IdP; grensesnittet viser da Select all ved valg av den ene metoden. Dette må vurderes på nytt hvis flere IdP-er legges til.
- Policytester: skjermbildet viser «1 user (100%) is approved». Eier utvidet resultatet og bekreftet at kun hans godkjente adresse var listet. Dette beviser policytreff for den kjente identiteten, ikke nekt for vilkårlige andre brukere eller faktisk MFA-håndheving.
- Kontosperre: eier bekrefter at kontoen bare brukes til Bussassistent, uten andre nettsteder/tjenester. Deretter er Block traffic to all domains in this account (Require Access protection) rapportert på og lagret, med tom Hostnames to Exempt. Dette er brukerbekreftet innstilling; faktisk blokkering ved edge er ikke prøvd.
- DNS-inventering: skjermbildet viser 0 av 200 DNS-poster; eier bekrefter tom liste. Ingen A/AAAA/CNAME-/wildcard-rute er registrert i denne sonen i dette snapshotet. Dette beviser ikke fravær av andre domener, direkte IP-tilgang, ruteråpninger eller tunneler.
- Kontomedlemmer: eier rapporterer kun egen konto, Super Administrator, status Active, 2FA On og API access Default. Ingen andre medlemmer eller ventende invitasjoner rapportert. Default-feltet beviser ikke fravær av utstedte bruker-/kontotoken. Tokenoversikt, aktive økter og Google-kontoens MFA gjenstår å kontrollere; ingen tokenverdier skal vises.
- API-tokeninventering: eier har nå kontrollert både Account API tokens og My Profile → API Tokens og rapporterer begge lister tomme. Global API Key er skjult og urørt. Dette er brukerbekreftet status; ingen nøkkel er lest, opprettet eller tilbakekalt av agenten. Aktive administratorøkter og Google-kontoens MFA gjenstår.
- Etterfølgende kontokontroll: eier rapporterer at My Profile → Sessions bare viser hans aktive økt, og at 2FA er aktiv på Google-kontoen brukt til Cloudflare-innlogging. Disse kontrollpunktene er dermed brukerbekreftet; ingen hemmeligheter er mottatt. Audit-logg, faktisk app-MFA og avvisningsprøver er fortsatt ikke verifisert.
- Audit-gjennomgang: eier rapporterer bare egne gjenkjente endringer og systemhendelser som samsvarer med oppsettet. Ingen ukjent aktivitet rapportert ved denne manuelle gjennomgangen. Ingen loggeksport eller rålogg er mottatt; dette er ikke en uavhengig fullstendighetskontroll av Cloudflares logging. Faktisk app-MFA, negativ tilgangstest og tunnelinventering gjenstår.
- Tunnelinventering: eier har åpnet tunneloversikten og bekrefter at den er helt tom. Ingen tunnel-ID eller tunnellegitimasjon finnes for denne oppgaven, og ingen tunnel skal opprettes/startes som neste automatiske steg. Konto-/Access-forberedelsene er nå registrert; videre integrering avventer godkjent 11.6 og aktivering krever særskilt godkjenning etter de resterende kontrollene under.
- Cache: eier bekrefter at regelen «Privat app – ingen cache» er lagret med Ignore and deploy rule anyway, uten opprettelse av DNS-post. Skjermbildet viser Bypass cache og advarsel om manglende proxied DNS for app.bussassistent.com. Faktisk cache-/headeradferd er ikke prøvd; les tilbake hele matchuttrykket og kontroller regelrekkefølge før publisering.
- Gjenstår: påkrevd MFA i faktisk appflyt, nekt for andre identiteter, cache-regelens faktiske effekt, DNS-/ruterkontroll og hele aktiveringsmatrisen. Ingen ekte runtime-konfigurasjon eller tunnellegitimasjon er generert; tunnel-ID mangler. Ingen DNS-endring eller tunneloppstart er utført i denne oppgaven.

Lenovo/Android/Brave → én offentlig HTTPS-origin → Cloudflare Access → navngitt tunnel med Access-validering → loopback 127.0.0.1:18081 → Nginx → lokal JWT-gate → privat API → separat PostgreSQL.

Samme HTTPS-adresse brukes hjemme og på mobilnett. Ingen VPN-klient, portvideresending eller egen API-origin inngår. Cloudflare avslutter klientens TLS og behandler trafikken. Det er et tillitsvalg eier må godkjenne. Transport til desktop går i kryptert tunnel; siste strekning er lokal HTTP på loopback/internt Docker-nett. Det er ikke ende-til-ende-kryptering som skjuler HTTP-innhold for Cloudflare.

Cloudflare Access er ytre innlogging. Appens brukernavn/passord, faste 14-dagersøkt, eierskap og CSRF består uavhengig. Gate gjør ikke en Access-identitet til en appkonto. Ingen fiktiv demo publiseres; privat frontend har egen inngang uten demo/API-kobling. En senere demo må ha eget hostname, API, database, volum og separat vurdering.

### Access og nøyaktig identitet

Forberedt review-utkast: deploy/tablet/access-plan.example.json. Det er **ikke et API-payload eller en anvendt policy**. Det krever:

1. Én Self-hosted-app for hele eksakte hostname, uten path-avgrensning. Ingen mer spesifikk underapp må kunne svekke beskyttelsen. Sider, rot, assets, helse/API og opplasting er omfattet.
2. Én Allow-policy: Include → Emails → kun den ene eksplisitt godkjente e-postadressen. Require → Login Methods → bare eksplisitt godkjent IdP. Ingen domenemønstre, ekstra Include-regler, Everyone, Bypass, Service Auth, service-token eller IP-/hjemmenett-unntak. Andre identiteter avvises ved standardnekt; en bred Block-regel er ikke nødvendig.
3. Påkrevd independent MFA på app/policy, eiers valgte Authenticator application. MFA ved hver ny Access-innlogging; ingen automatisk aksept av uprøvde IdP-AMR-verdier. E-postkode alene teller ikke som MFA. Faktisk håndheving og støtte på Lenovo/Android/Brave må prøves. TOTP er ikke phishing-resistent. Ikke legg inn en svakere fallback uten ny uttrykkelig godkjenning.
4. Registrer MFA-enhetene under eiers kontroll før publisering. Beskytt også IdP og gjenopprettings-e-posten. Førstegangsregistrering av MFA må ikke etterlates som et ubeskyttet bootstrap-vindu.
5. Forslag: app-/policyøkt 1 time under første sikkerhetsprøve, kortere midlertidig prøve for utløp. Dette erstatter tidligere forslag om 24 timer. Global Access-/IdP-økt og MFA-cache må registreres hver for seg. Ingen langvarig økt eller offline-unntak er godkjent.
6. I en ny dedikert konto: vurder og aktiver Require Access protection etter inventering, før publisering. Denne kontoinnstillingen avviser hostname uten Access-app, men kan påvirke andre nettsteder og skal ikke endres blindt i en senere delt konto.

### Administrator og registrar

Administratorens passord, Authenticator-2FA og gjenoppretting er bekreftet av eier som beskrevet over. Ingen sikkerhetsnøkkel er tilgjengelig; Authenticator er valgt. Recovery-koder skal fortsatt holdes utenfor chat, repo og skjermbilder. Unngå delt administratorkonto, kontroller medlemsliste og minst nødvendige roller, aktive økter og audit-logg. Aktiver 2FA Enforcement for medlemmer når kontoen er inventert. Kontroller også Google-/gjenopprettingskontoens MFA. Ingen Global API Key eller administrasjons-token trengs i app eller gate.

### Lokal JWT-gate

deploy/tablet/access_gate/gate.py brukes av Nginx auth_request før rot, privat side, assets og API. Den kontrollerer:

- Bare Cf-Access-Jwt-Assertion-header; ingen cookie-fallback eller påstand basert på headerens eksistens. Manglende, dobbelt/ugyldig eller for langt token avvises.
- Kun RS256 med signatur kontrollert av PyJWT 2.15.1/cryptography. HS256/none og ukjente kritiske headere avvises.
- Eksakt issuer https://DET-GODKJENTE-TEAMET.cloudflareaccess.com, forventet applikasjons-AUD, påkrevd utløp og utstedelsestid, og eventuell nbf. Ingen klokkeslakk. Serverklokken må derfor være korrekt.
- Påkrevd type=app, ikke-tom sub og eksakt, kanonisk e-post fra lokalt godkjent policy. Service-token, feil identitet og manglende claims avvises. Identitetsleverandøren begrenses i Access-policyen; gate erstatter ikke denne kontrollen.
- Kun operatørens faste HTTPS-JWKS-adresse. Tokenets iss/jku/x5u velger ikke nøkkelkilde. Sertifikatkontroll slås ikke av. Offentlige nøkler kan caches i inntil 300 sekunder; bibliotekets refresh/cooldown brukes ved rotasjon. Etter cacheutløp og mislykket nøkkelhenting avvises tilgang. Ingen autorisasjonsresultater caches, og exp kontrolleres for hver forespørsel.
- Gate returnerer generisk avvisning uten token, claims eller feildetaljer i logger/svar. Gate-nedetid gir 5xx fra Nginx og slipper ikke trafikk gjennom. Den interne auth-ruten kan ikke kalles utenfra. Access-header fjernes før privat API.

Gate verifiserer ikke live-tilbakekalling eller MFA-policy ved hver forespørsel. Et kryptografisk gyldig token kan fortsatt være gyldig lokalt etter en edge-tilbakekalling, fram til exp. MFA håndheves i Access og må bevises der. Signaturverifisering alene beviser ikke at Access-policyen er riktig konfigurert. Ved akutt hendelse stenges tunnelen og gatewayen; ikke vent på JWT- eller DNS-utløp.

cloudflared-malen krever i tillegg riktig team/AUD med access.required=true. Bare eksakt privat hostname treffer loopback-gateway; siste ingressregel er 404. Metrics bindes kun til 127.0.0.1:18083; ingen debug-logg eller automatisk oppdatering. Versjon må oppdateres kontrollert ved senere sikkerhetsbehov. Ingen catch-all proxy, LAN-nettrute eller tilgang til Docker/socket/admin inngår.

### Nettverk, cookies og containere

compose.tablet.yaml er selvstendig: prosjekt ibe160-tablet-prep og profil tablet. Bare gateway publiserer 127.0.0.1:18081; API, gate og PostgreSQL har ingen hostporter. App- og storage-nett er interne. Gate har eget keys-nett for HTTPS-henting av offentlige Cloudflare-nøkler. Lokalpilotens faktiske hostpublisering krevde i tillegg et eget ikke-internt front-bro-nett bare for gatewayen, med standard hostbinding 127.0.0.1 og IPv6 av; faktisk binding og hostlytter er kontrollert. API/DB har ingen av de to ikke-interne nettene. Gateway og gate kan ha utgående trafikk; dette er ikke en domenebegrenset egress-brannmur. Kompromittering av dem er fortsatt en risiko. Ingen Windows-/ruterbrannmurregel er endret.

Alle fire tjenester kjører uten root, med read-only rootfilsystem, cap_drop ALL og no-new-privileges. PostgreSQL bruker navngitt postgres-bruker og eget datavolum; kun nødvendige temp-/socket-kataloger er skrivbare. På et nytt volum lager init-private-role.sql approllen private_work uten SUPERUSER, CREATEDB, CREATEROLE eller REPLICATION. Den eier bare sin separate private_work-database og har DDL-rettigheter der for appens migreringer. Bootstrap-administrator tablet_bootstrap har en annen hemmelighet som **bare DB-containeren får**, aldri API-et. Dette er ikke en generell løsning med separat migreringsrolle for ordinært miljø; oppsettet gjelder bare nytt tablet-volum. API har begrenset tmpfs for import, gate ingen databasehemmelighet, og gateway ingen hemmeligheter. Ingen privileged, host-network, Docker-socket, vertens mapper med private data eller ordinære datavolumer monteres. PID-grenser er satt. Dette er ikke full ressurs-/DoS-kvalifisering.

Nginx bruker ekte statisk produksjonsbygg, ikke utviklingsserver. Hele innholdet krever admission, inkludert rot som nå serverer privat inngang direkte. Andre stier/demo gir 404, feil Host avvises, auth-ruten er intern, proxyen forsøker ikke writes på nytt. API-prefiks fjernes uten å endre Origin, CSRF eller cookies. Forwarded-headere fjernes; Uvicorn stoler ikke på dem.

API krever eksplisitt PRIVATE_HTTPS_DEPLOYMENT=1 og én kanonisk PRIVATE_ORIGIN. Det gir Secure, HttpOnly, host-only, SameSite Strict og Path=/ for auth-/CSRF-cookies, også ved sletting. Logout-lås er Secure på HTTPS. Eksisterende loopback-HTTP-modus er separat og kan ikke kombineres med HTTPS-modus. Frontend bygges med relativ /private-api, så nettbrettet kaller samme HTTPS-origin. Appens egen session/ownership/eksakt origin/signerte CSRF-kontroll beholdes. Proxyens kropp-/tidsgrenser endrer ikke strengere API-grenser.

Alle private svar har no-store. CSP begrenser forbindelser til self. Cache Bypass-regelen er nå rapportert opprettet for hele hostname hos Cloudflare; les tilbake uttrykk/regelrekkefølge og kontroller at ingen Worker, Cache Everything, transform eller annen ruting omgår dette. Faktisk effekt er uprøvd. Ikke lagre HAR-filer, Authorization-/Cookie-headere, JWT, passord eller virkelig innhold i evidens. Access-/konto-audit-logg har identitetsmetadata og skal behandles privat.

## Hemmeligheter og lokale filer

Lokalpiloten har nå egne tilfeldige DB-/bootstrap-passord og et separat tilfeldig passord for den fiktive prøvebrukeren. Disse behandles som hemmeligheter og ligger bare i ACL-begrensede, ignorerte runtime-filer; se lokalpilotrapporten. Ingen tunnel-/administrasjonshemmeligheter er opprettet eller mottatt. Fiktive JWT-nøkler/token brukes bare i isolerte testprosesser. Git og Docker-byggekontekst utelukker lokale hemmeligheter, data og Git-metadata. Rotens .dockerignore er en allowlist for nødvendige frontend-/deployfiler.

Lokalpiloten er forberedt med -LocalOnly, uten tunnel-ID eller tunnelkonfigurasjon. Ikke kjør førstegangsoppskriften nedenfor om igjen mot disse eksisterende filene; den vil nekte overskriving. Følgende er den opprinnelige fullstendige førstegangsoppskriften for en tom checkout med godkjent faktisk tunnel-ID. En senere tunnelkonfigurasjon til eksisterende lokalpilot må forberedes særskilt uten å endre passord eller policy:

~~~powershell
./scripts/prepare-tablet-files.ps1 -Hostname 'bus.DITT-DOMENE.no' `
  -TunnelId 'DIN-TUNNEL-UUID' -TeamName 'ditt-team' `
  -Audience 'DIN-64-TEGNS-AUD' -ApprovedOwnerEmail 'din-godkjente-identitet@din-idp.no' `
  -TunnelCredentialPath 'C:\LOKAL-SIKRET-MAPPE\DIN-TUNNEL-UUID.json'
./scripts/test-tablet-config.ps1
~~~

Bytt alle plassholdere. Ingen eieridentitet kan utledes fra Windows-brukernavn, chatnavn eller e-postdomene. Skriptet krever én adresse, lager ignorert .env.tablet, .private-runtime/tablet/cloudflared.yml, access-policy.json, postgres-password (approlle) og bootstrap-password (kun DB-init). Det avviser eksisterende konfigurasjon/policy, brede identitetsmønstre og kjente plassholdere. Eksisterende DB-passord bevares; ikke regenerer dem eller bruk gammel volumkonfigurasjon. Init-skriptet kjøres bare på helt nye volumer, ikke som oppgradering av et eksisterende volum. Runtime-mappens ACL begrenses **før** nye hemmeligheter skrives; mappe/filer tillater bare nåværende Windows-bruker og SYSTEM. Reparse points avvises. Restriktiv ACL beskytter ikke mot lokal administrator eller kompromittert eierkonto.

Tunnel-JSON må ligge utenfor Git-worktreet i en separat mappe med tilsvarende ACL. Klargjør/verifiser den mappens ACL før autentisering lager credentials der. protect-tablet-path.ps1 inneholder funksjonen; bruk den bare på den nye dedikerte credential-mappen, aldri rekursivt på profil, hovedrepo eller en delt mappe. Endring av eksisterende credential-mappe krever egen gjennomgang. Kontoens brede cert.pem fra tunnel login skal ikke være runtime-legitimasjon; oppbevar den som separat sikret administrasjonsmateriale. Tunnelen skal bare få sin egen JSON-fil og kjøre uten forhøyede administratorrettigheter. Ingen hemmelighet skal i argumenter, Git, chat, skjermbilde, shellhistorikk eller debug-logg.

## Utførte kontroller

| Kontroll | Resultat og avgrensning |
|---|---|
| Konto/domene | Oppdatert brukerutført status og skjermbildegjennomgang er registrert over. Ingen direkte API-avlesning, ekte app-MFA-/JWT-test eller ekstern DNS-/rutekontroll er utført. |
| Lokal eksponering | 5173/8000/8001 var loopback; 18081 var ikke i bruk. Ingen lyttende TCP 22/80/443/2375/2376/3389/5432/5985/5986 i snapshot. Docker publiserte bare loopback-appporter; DB-porter var ikke publisert. Ingen netsh portproxy-oppføringer funnet. |
| Vertens begrensninger | Windows-brannmurens tre profiler var på; effektiv regelgjennomgang er ikke utført. RDP/WinRM-tjenestene var stoppet. Ingen cloudflared/ngrok-prosess eller Cloudflare-/tunnelvariabler funnet. Eksisterende andre wildcard-lyttere, blant annet SMB/RPC, finnes. Ingen påstand om WAN-sikkerhet eller fravær av andre tunneler; ruteren/UPnP/DMZ/IPv6 er ikke inspisert. |
| JWT | 13 pytest-tester bestod med ekte RSA/PyJWT: gyldig eier, feil signatur/algoritme/issuer/AUD/identitet/type, utløp/nbf/iat, manglende claims, for langt token, feil policy, fast nøkkelkilde, cache/rotasjon og byttet godkjent eier. Den første kjøringen hadde 2 fixturefeil som delte nøkkelcache; egne fixtures og eksplisitt cachetest rettet dette. Ingen produktbypass ble lagt inn. |
| Ekte proxy/gate | 120 avviste kombinasjoner: rot/privat side/asset/API GET/API POST × manglende token og 23 ugyldige varianter. Null avviste kall nådde syntetisk API-upstream. Gyldig eier gikk gjennom; Origin/CSRF/cookies, no-store/CSP, Host og avviste stier ble kontrollert. Gate-stopp avviste sider/assets/API med 5xx. JWT-nøkkelkilden var fiktiv, ikke Cloudflare. |
| Transport | 14/14 eksisterende isolerte HTTPS-cookie-/CSRF-tester bestod på nytt som UID 10001, read-only og uten capabilities/nett. FastAPI ekte; auth/DB testdobler. Én kjent TestClient-deprecation-advarsel. Ingen virkelig innlogging/DB-lagring bevist. |
| Friske bygg | Egne nye gate-, gate-test-, gateway- og API-images bygget. Gateway kjørte fersk npm ci, TypeScript og Vite-produksjonsbygg. Proxyprøven brukte faktisk rootløst gateway-image/entrypoint/envsubst. Ingen ordinære images er bygget om. |
| PostgreSQL | Rootløs read-only/cap-drop-oppstart og SELECT 1 bestod på nytt disponibelt volum uten nettverk/hostport. Deretter bestod ny separat prøve med ekte init-skript: approllen hadde f/f/f/f for SUPERUSER/CREATEDB/CREATEROLE/REPLICATION; autentisert TCP-login og opprett/skriv/les/fjern av fiktiv testtabell bestod. Ingen appmigreringer eller ordinære data brukt. Begge engangsvolumer og containere ble fjernet. |
| Lokal konfig/ACL | Compose-kontroll og PowerShell-parsing bestod. Fiktiv fixture beviste korrekt policy-generering, current-user/SYSTEM-only ACL og at konfig/passord ikke overskrives. Senere er faktiske lokalpilotfiler/ACL/Git-ignorering og overskrivingsvern kontrollert; tunnelcredentials er fortsatt ikke opprettet. |
| Tunnelmal | cloudflared 2026.10.4 ingress validate bestod i nettverksløs engangscontainer mot plassholdermalen. Image digest: sha256:c6c7ae1d5dfdcb094ad344ed68ccffc26635c9c6be80965664c33baf064b0515. Ingen tunnel ble startet. Faktiske team/AUD/credentials/Windows-binær og edge-JWT er ikke verifisert. |
| Rydding | Egne testcontainere, interne testnett og disponibelt DB-volum fjernet; bare lokale test-images og ignorerte tmp-fixtures beholdes. git diff --check bestod. |

Isolerte tester er ikke et eksternt sikkerhetssertifikat. Hele Compose-appen kjører nå som lokalpilot med ekte separat database; ekte tunnel, TLS, Cloudflare-admission og nettbrettesting er fortsatt uprøvd.

## Integrering etter godkjent 11.6

1. Vent på godkjent 11.6 og registrer dens eksakte commit/release. Hvis den fortsatt er ukommittert, avtal godkjent snapshot i den andre chatten; ikke ta en vilkårlig kopi. Ingen Git-/indeksarbeid i D:\IBE160.
2. Overfør bare reviewede tilgangsendringer og alle nye deploy-/testfiler til en separat integreringscheckout. Denne leveransen har ingen commit å cherry-picke. Behold godkjente 11.5/11.6-ruter, notice-reader/migrering 013, recovery-helper og epoch/generasjons-/status-før-retry-vern. Sammenlign særlig private_main.py, auth.py, run.py og PrivateAccess.tsx; ikke erstatt nye produktkomponenter med 11.4-basens filer.
3. Gjenta testene mot ferdig 11.6, inkludert autorisasjon/eierskap, 302/HTML/403 fra Access, tapt lagringssvar og null automatisk POST etter utløp. Bruk eget syntetisk prosjekt/porter/volumer. Ikke bruk nåværende private-verifikator som stopper vanlig API.
4. Test rootløse migreringer, PDF-import/tempgrenser og full appflyt på **ny fiktiv database**. Ingen migrering/restore mot ordinære data. Første tablet-pilot starter tomt; eventuell senere virkelig dataoverføring krever separat godkjent backup/restore-/rådataverifisering.
5. Registrer godkjent release-identitet og de nye image-digestene. Revider avhengigheter/sårbarheter ved aktivering; låste versjoner alene er ikke sikkerhetsbevis.

## Aktiveringsplan med sperrer – lokale deler utført, publisering uutført

Hvert trinn må ha dokumentert resultat før neste trinn. Manglende identitet, MFA, avvisningsbevis eller alternativ rute er stoppgrunn, aldri grunn til midlertidig bypass.

1. **Eierbeslutninger:** godkjenn Cloudflare som mellomledd og senere kontoopprettelse. Konto/MFA-oppsett utføres av eier selv. Avklar deretter domene/registrar/pris/fornyelse ett valg om gangen; intet kjøp uten konkret godkjenning. Registrer bare offentlige identifikatorer/hostname i arbeidsnotater, ikke secrets.
2. **Kontosikring før publisering:** verifisert e-post, 2FA/reserve/recovery og sikret IdP/registrar; inventer medlemmer, tokens, aktive økter og audit. Ingen brede eller delte adminrettigheter. Konto- og MFA-oppsettet er en egen godkjenning, ikke implisitt tillatelse til DNS.
3. **Domene og Access før tunneltrafikk:** etter uttrykkelig godkjenning av eventuell sone-/navneserverendring, etabler hostname uten origin-rute til appen. Etabler og les tilbake hele Access-appens policy, godkjent eksakt eier, valgt IdP, påkrevd MFA, livstider og Cache Bypass. La Require Access protection være på i dedikert konto etter inventering. Ingen wildcard-/path-unntak. Dokumenter faktisk MFA-bevis. E-postadresse/IdP må godkjennes eksplisitt før de fylles i lokal policy.
4. **Tunnelen forberedes avslått:** velg oppdatert offisiell cloudflared-binær, kontroller signatur/checksum, ingen Windows-tjeneste/autostart. Opprett én navngitt tunnel via godkjent konto. Sikre credential-mappe først; legg bare tunnelens credential-JSON i runtime. Ingen WARP/LAN-/private-network-ruter. Lokale prepare-/config-/ACL-kontroller og ingress validate/rule kjøres med faktisk hostname/team/AUD; sluttregel skal nekte alle andre hostname. Kommandoer som tunnel login/create er fremtidige eksterne kontoendringer og skal ikke kjøres i dette arbeidet.
5. **Lokal integrert kandidat:** først etter 11.6-godkjenning og separat tillatelse til pilotoppstart, kjør fra integrert checkout:

~~~powershell
docker compose --env-file .env.tablet -f compose.tablet.yaml --profile tablet up -d --build
~~~

Dette starter bare nytt prosjekt og migrerer bare det nye tablet-volumet. Ikke kombiner Compose-filer, overstyr prosjektnavn eller monter ordinære data. Opprett fiktiv prøvebruker interaktivt med samme Compose-utvalg og exec private-api python -m app.manage provision tablet-provebruker. Passord skrives skjult; aldri argument eller -T. CLI-et reserverer synthetic-prefikset for automatiserte tester, så denne manuelle pilotdatabasen skal ikke blandes med destruktive synthetic-only-regresjonstester.

6. **Avvisning lokalt før DNS:** bruk riktig Host mot loopback-proxyen. Uten JWT skal rot, side, assets og direkte API GET/POST avvises før privat API. Kjør signatur/issuer/AUD/exp/feil-identitet-matrisen isolert. Faktisk gate-nedetid skal være fail-closed. Bekreft at bare 18081 er publisert og at nett/volum/secrets/UID/capabilities er som reviewet. HTTP-testen er ikke bevis for Secure-cookie-innlogging via HTTPS.
7. **Alternativ vei:** les ruterens portvideresending, DMZ, UPnP/PCP-mappinger og IPv6-regler med eier; ikke endre dem i denne oppgaven. Verifiser fra hjemmenett og uavhengig mobilnett at desktopens IPv4/IPv6 ikke tilbyr app/devserver, DB, Docker-API, RDP, SSH, WinRM eller adminUI. Kontroller spesielt 5173/8000/8001/18081/5432/2375/2376/3389/5985/5986/22/80/443 og eventuelle faktisk konfigurerte adminporter. Lokal portoversikt alene beviser ikke dette. Ikke aktiver hvis ukjent offentlig rute, portmapping eller uønsket IPv6-tilgang finnes. Ingen åpning av inngående porter er nødvendig.
8. **Egen publiseringsgodkjenning:** først når trinnene over er godkjent, opprett DNS-rute til akkurat denne tunnelen og start kun den manuelle foreground-prosessen. Eksempel: cloudflared tunnel --config .private-runtime/tablet/cloudflared.yml run DIN-TUNNEL-ID. Ingen generell nettverkstilgang, persistent tjeneste eller automatisk restart. Hold avstengning tilgjengelig i samme terminal. Alle prøver bruker bare fiktive data.
9. **Edge + nettbrett:** gjennomfør matrisen under. Ved uautorisert 2xx eller privat innhold: stopp tunnelen/gatewayen straks. Ikke legg inn bypass for å få testen videre. Først etter dokumentert bestått fysisk prøve kan en separat pilotdriftsbeslutning tas.

## Aktiveringsmatrise – gjenstår fysisk/eksternt

Kjør både i Brave på Lenovo/Android og med direkte HTTP-klient uten lagring/logging av credentials. Kjør hjemme og via mobilnett med Wi-Fi av. Bruk samme eksakte hostname, normal Brave Shields, nye private faner og fiktiv appkonto. Ingen tredjepartscookie-unntak skal være nødvendig. Noter versjoner og målte resultat, ingen rå JWT/HAR.

| Tilfelle | Nettside, rot og asset | Direkte API GET + ufarlig fiktiv POST |
|---|---|---|
| Ingen Access-cookie/header | Access-innlogging/nekt, aldri privat HTML/JS | Nekt/innlogging ved edge; ingen private JSON eller mutasjon. Ikke følg redirects som om de var kvitteringer. |
| Innlogget feil identitet | Avvises, ingen privat app | Avvises, selv med gyldig appcookie. |
| Godkjent identitet uten fullført MFA | Avvises av Access | Ingen passering eller mutasjon. |
| Manglende/forfalsket signatur, alg none/HS256, ukjent kid | Avvises | Avvises, ingen backend-effekt. |
| Feil issuer/AUD, utløpt/fremtidig token, manglende claims, annet email/type | Avvises | Avvises; ingen 2xx, privat JSON eller DB-endring. |
| Gyldig Access/eier/MFA, ingen appøkt | Privat login kan vises, ingen privat arbeidsdata | API 401 på beskyttet ressurs. |
| Begge innlogginger gyldige | Riktig privat side/gyldig betrodd HTTPS | Eierskap håndheves; feil Origin/CSRF 403 og fremmed ressurs trygg nekt. Fiktiv lagring/revisjon kan bekreftes. |
| Access-gate/JWKS/tunnel nede | Intet privat fallback-innhold | Ingen mutasjon/kvittering uten godkjent svar. Cached offentlig nøkkel er bare tillatt innen dokumentert TTL. |
| Tilbakekalt Access-økt | Registrer faktisk tid til avvisning og forsøk på ny innlogging | Samme kontroll med tidligere gyldig token. Stopp tunnel/gateway for umiddelbar lokal sperre. |

En klient kan ikke selv lage et ekte Cloudflare-signert token med feil issuer/AUD/exp. Slike claims ble prøvd med fiktiv nøkkelkilde lokalt. Liveprøven må bruke faktisk utløpt/eierens ekte token eller et særskilt godkjent, isolert kontrolloppsett for annen AUD/issuer; aldri opprett bred policy eller svekk produksjonspolicy for å lage fixture. Ikke last JWT opp til jwt.io eller andre nettjenester.

Prøv også lagring/reåpning/revisjon, nettbytte, flymodus, tapt svar etter aksept, to faner, appøktutløp, Access-utløp midt i redigering, serverbrudd og retur. Ingen falsk suksess eller automatisk ny POST; opprinnelig operasjon må avklares etter 11.6. Forny Access i en separat fane uten reload av fanen med uavklart arbeid. Appen har ikke offline-lagring; lukking/reload kan miste usendte forslag. Test logout/tapt logout-svar/reload og at begge innloggingslag avsluttes som forventet; app-logout avslutter ikke automatisk Access. Test stående/liggende, tastatur, forstørret tekst og dag/natt når parkert.

Test desktop-/hjemmebrudd og retur bare på pilotprosjektet; ikke stopp ordinært miljø under 11.6-testing. Ingen autostart/strømendring er gjort. Etter Windows-reboot må Docker, pilot og tunnel startes manuelt. Ressurser, viftestøy og bakgrunnsadferd på Android gjenstår å kvalifisere.

## Tilbakekalling og rask stenging

1. **Umiddelbar stenging:** Ctrl+C i akkurat den nye foreground-tunnelen. Stopp deretter bare den nye gatewayen med docker compose --env-file .env.tablet -f compose.tablet.yaml --profile tablet stop gateway. Dette stanser også loopback-tilgangen; vent ikke på DNS-cache eller JWT-utløp. I feilscenario må faktiske nye kall på både side og API beviselig avvises.
2. **Hindre ny innlogging:** fjern/stram den konkrete Allow-policyen eller sperr kompromittert IdP-identitet, og bruk Access Revoke existing tokens på appen / Revoke på brukeren. Bare revocation uten policy-/IdP-endring kan tillate ny innlogging. Tilbakekalling utføres senere som godkjent kontoendring, ikke automatisk nå.
3. Ved mistenkt credential-tyveri: tilbakekall tunnelens legitimasjon/connector i Cloudflare, og kontroller at ingen annen connector/replica kan holde den åpen. Tilbakekall relevante admin-/IdP-/appøkter separat. Lokal signaturkontroll kjenner ikke edge-revocation; hold gateway stengt til det er avklart.
4. Fjern/deaktiver bare den nye DNS-ruten etter avstengning. Behold Access-nekt til routing er kontrollert. Stopp kun pilotprosjektet med samme Compose-utvalg og down, **aldri -v/prune/reset**. Behold DB-volum, passord og nødvendige sikrede backups for inspeksjon. Ikke rull gammel kode tilbake mot et nyere schema.
5. Før eventuell gjenåpning: ny godkjenning av identitet/policy/MFA/credentials, bekreftede avvisningstester og release. Normal app-logout eller Access-logout er ikke en nødstoppsprosedyre; edge-logout kan ha propagasjonstid.

## Offisielle kilder kontrollert

- [Cloudflare Access JWT-validering](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/): fast team-JWKS, signatur, issuer og AUD. Ingen ekte token ble kopiert til eksterne validatorer.
- [Access policies](https://developers.cloudflare.com/cloudflare-one/access-controls/policies/): Include er OR, Require er AND, standardnekt og rekkefølge gjør brede/unntakspolicyer farlige.
- [Independent MFA](https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/independent-mfa/) og [MFA requirements](https://developers.cloudflare.com/cloudflare-one/access-controls/policies/mfa-requirements/): app/policykrav, tilgjengelige metoder, enrollment og IdP-AMR må kontrolleres.
- [Kontoadministratorens 2FA](https://developers.cloudflare.com/fundamentals/user-profiles/2fa/), [aktive kontoøkter](https://developers.cloudflare.com/fundamentals/account/account-security/manage-active-sessions/) og [audit](https://developers.cloudflare.com/fundamentals/account/account-security/audit-logs/).
- [Require Access protection](https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/require-access-protection/) og [Access-økter/tilbakekalling](https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/session-management/).
- [Nginx auth_request](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/), [PyJWT 2.15.1](https://pypi.org/project/PyJWT/) og [bibliotekets claims/JWKS-bruk](https://pyjwt.readthedocs.io/en/latest/usage.html).
- [Offisiell cloudflared 2026.10.4-release](https://github.com/cloudflare/cloudflared/releases/tag/2026.10.4) og [tunnelkonfigurasjon](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/local-management/configuration-file/).

## Hva eier må godkjenne videre

Konto, gratisplan, kjøpt domene og valgt identitet/Cloudflare-IdP/Authenticator er nå rapportert av eier. Tidligere konto-/domenevalg i aktiveringsplanen er historikk; gjenstående kontroller må fortsatt utføres. Dette gir ingen tillatelse til sone-/DNS-endring, pilotoppstart, integrering eller tunnelstart. Kontoendringer utenfor det uttrykkelig godkjente oppsettet må avklares særskilt.

Før faktisk publisering må eier godkjenne den konkrete Access-policyen med eksakt identitet, MFA og hostname, Cloudflare-tilliten, godkjent 11.6-release, bruk av kun nye fiktive pilotdata, samt DNS-ruten og manuell tunneloppstart etter test-/ruterkontroll. Administrator-/runtime-credentials legges lokalt, aldri i chat. Fysisk Lenovo-/mobilnettprøve og live-revocation er fortsatt uutført. Løsningen er ikke dokumentert risikofri eller ferdig sikret.
