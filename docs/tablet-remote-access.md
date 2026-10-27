# Sikker nettbrett-tilgang – forberedt, ikke aktivert

> Historisk første forberedelsesrapport. Gjeldende sikkerhetsoppsett og aktiveringsplan er nå [Sikkerhetsgjennomgang for nettbrettilgang](tablet-access-security.md). Den nye rapporten overstyrer blant annet tidligere proxy uten egen JWT-gate, 24-timersforslag, rettigheter og listen over gjenstående bygg. Bruk den nye planen ved videre arbeid.

Dato: 2026-10-26. Branch: `setup/tablet-remote-access`.
Worktree: `C:\Users\Jonas\.codex\.chatgpt-projects\g-p-6ab6b4c1c6888191a96d3242fab912b4\tablet-remote-access`.
Base: `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed` (`feat(11.4): maintain planned notices from web or SMS`).

## Avgrensning og funn

`D:\IBE160` er på `main` med omfattende lokale 11.5/11.6-endringer. Ved oppstart fantes også tre worktrees for automatisk varsling, komplett rutenett og posisjonsprogresjon; ingen brukte denne branchen. Det nye worktreet inneholder bare basecommiten pluss dette forberedelsesarbeidet. Ingen ukommittert produktkode er kopiert. Hovedmappens arbeidsfiler, index, branch og kjørende containere er ikke endret av denne oppgaven. Ingen commit, push, merge, statusendring for story/retro eller Epic 12-arbeid er utført.

Prosjektets speil-instruksjoner er lest. Ingen `AGENTS.md` ble funnet i selve applikasjonsrepoet. Relevante lesekilder: eksisterende Compose-filer, README, `auth.py`, `private_main.py`, `private_storage.py`, frontendens private innlogging, gjeldende arkitekturspine og lokal 11.6-spesifikasjon. Historiske Cloudflare-valg i arkitekturens memlog er skilt fra gjeldende spine: lokal kjøring er dagens leveranse; offentlig tilgang er utsatt, og forberedes her etter ny eksplisitt bestilling.

Repoet hadde ingen tunnelkonfigurasjon. `cloudflared` ble ikke funnet i PATH, ingen matchende Windows-tjeneste eller standardmappe `C:\Users\Jonas\.cloudflared` ble funnet ved lesekontroll. Dette beviser ikke at en Cloudflare-konto eller tunnel ikke finnes eksternt eller i en annen mappe; ingen konto ble åpnet. Den ordinære appen bruker React/Vite, FastAPI og PostgreSQL, loopback 5173/8000/8001, og separat privat lagring. API-et støttet bare eksplisitt HTTP på loopback; nettleseren hadde hardkodet API-adresse `127.0.0.1:8001`.

## Valgt forbindelse

`Lenovo / Android / Brave → HTTPS bus.<ditt-domene> → Cloudflare Access → navngitt Tunnel → cloudflared med Access JWT-validering → 127.0.0.1:18081 → Nginx → privat API → privat PostgreSQL`.

Samme HTTPS-adresse brukes hjemme og på mobilnett. Ingen portviderekobling, LAN-HTTP, separat API-domene eller VPN-klient kreves for denne løsningen. Desktop, Docker og tunnelprosessen må være tilgjengelige; hjemme- eller PC-brudd gir utilgjengelig app. Dette gir ikke offline-lagring eller nye garantier om bakgrunnsdrift på Android.

Access beskytter **hele vertsnavnet**, inkludert `/private`, alle assets og `/private-api/*`. Bruk en Self-hosted Access-app med Allow kun for eierens eksakte identitet og MFA hos identitetsleverandøren. Ingen Bypass, Everyone eller stier som unntar API/assets. Tunnelen krever signert Access JWT med rett team og AUD; manglende/feil token skal avvises før origin. Appens egen brukerkonto/passord, serverøkt og eierskapssjekker gjelder fortsatt. Access-identitet oppretter ingen appkonto.

Offisielle kilder sjekket ved forberedelsen:

- [Cloudflare Access for self-hosted apps](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/): hele appen og policyevaluering.
- [Origin parameters, offisiell kildefil](https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/partials/cloudflare-one/tunnel/origin-parameters.mdx): `originRequest.access.required`, `teamName`, `audTag` og JWT-kontroll i connector.
- [Tunnel configuration](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/local-management/configuration-file/): navngitt tunnel, ingress og avsluttende avvisningsregel.
- [Access sessions](https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/session-management/): egen applikasjons-/policy-/global levetid. Bruk 24 timer som første pilotoppsett; gjennomfør prøve med kortere utløp før normal bruk. Appens økt er fortsatt fast 14 dager, uten automatisk forlengelse.

Cloudflare avslutter klientens TLS og behandler privat HTTP-trafikk; dette er en nødvendig tillitsavklaring. Tilkoblingen videre til desktop er gjennom kryptert tunnel. Siste HTTP-strekning er lokal loopback/Docker på samme desktop. Databasen og API-et har ingen publiserte vertsporter. Lokal administrator og lokale prosesser er betrodd; loopback-proxyen er ikke en sikkerhetsgrense mot en kompromittert desktop.

## Forberedte filer og sikkerhetsegenskaper

- `compose.tablet.yaml`: selvstendig prosjekt `ibe160-tablet-prep`, profil `tablet`, nytt volum `ibe160-tablet-prep_tablet_pg`, intern DB-nettverksflate, og bare `127.0.0.1:18081` publisert. Ikke kombiner med andre Compose-filer eller overstyr prosjektnavnet.
- `deploy/tablet/Dockerfile`, privat HTML og `frontend/src/tablet.tsx`: eget statisk produksjonsbygg av kun privat inngang, ikke Vite dev-server. Ingen demo eller fiktiv API i denne inngangen. Node, PostgreSQL og Nginx er låst til image-digests.
- `deploy/tablet/nginx.conf.template`: eksakt Host, `/` til `/private`, bare privat inngang/assets/API-ruting; øvrige stier 404. `/private-api/` strippes før backend. Cookies, Origin og CSRF-header videresendes uendret. Ingen omskriving av origin/cookie-domene, ingen proxy-retry av usikre writes. 12 MiB proxygrense rommer API-ets strengere 10 MiB PDF-grense; 65 sekunder proxy-timeout overstiger frontendens frister. Access-/proxy-HTML eller ikke-JSON regnes fortsatt som uavklart feil av appen.
- `PRIVATE_HTTPS_DEPLOYMENT=1` pluss én kanonisk `PRIVATE_ORIGIN=https://...` aktiverer Secure for både session- og CSRF-cookie og sletting av session-cookie. Host-only, HttpOnly, SameSite Strict og Path `/` beholdes. Logout-lås-cookie blir Secure på HTTPS. Lokal HTTP krever fortsatt `PRIVATE_LOOPBACK_DEVELOPMENT=1`; modusene kan ikke kombineres. HTTPS tillates ikke bare fordi en klient sender forwarded-headere. Uvicorn stoler ikke på disse; proxyen fjerner dem. Innloggingens IP-begrensning ser proxyen, slik at grensen i praksis deles av brukerne på denne origin; eksisterende globale og per-bruker begrensninger beholdes.
- Frontenden bygges med `VITE_PRIVATE_API_BASE=/private-api`; bare denne relative verdien godtas. Lokal standard beholdes for eksisterende utviklingsløp. Nettbrettet kontakter derfor sitt eget HTTPS-vertsnavn, uten mixed content eller cross-site cookies. Eksakt origin og signert CSRF-kontroll beholdes også på login/logout. Ingen wildcard-CORS.
- `no-store`, CSP, nosniff, frame-nekt og ingen access-logg på proxyen. Konfigurer også **Cache Rule: Bypass cache for hele private vertsnavnet** hos Cloudflare. Fjern eventuelle Cache Everything-/Worker-/transform-regler som kan endre dette. Ingen private data, passord eller token skal inngå i logguttrekk.
- Appen har fortsatt ingen privat lagring i localStorage, sessionStorage, IndexedDB eller service worker. Uavklart lagring må avklares i samme fane; reload kan miste usendte forslag. Ikke legg til automatisk reload for Access-fornyelse. Ved utløpt Access kan fetch bli avvist/returnere HTML; bruk separat fane med samme `/private` for å fornye Access, gå så tilbake og kontroller tilgang/opprinnelig operasjon. Dette må prøves fysisk mot ferdig 11.6.

Demoen forblir lokal og fiktiv. En eventuell senere lærer-demo får eget vertsnavn, API, database, volum, konfigurasjon og tunnelregel. Ingen unntak på privat origin og ingen kobling fra demo til privat lagring. Det er ikke klargjort noen offentlig demo her.

## Lokale innstillinger og hemmeligheter

Ikke send passord, tunnel-JSON eller token i chatten. Ingen virkelige hemmeligheter er generert eller lagret i denne leveransen. Eksemplet bruker `.invalid` og avvises av API-et.

Når konto-/domeneverdiene er kjent, kjør fra valgt integrert checkout:

```powershell
./scripts/prepare-tablet-files.ps1 -Hostname 'bus.DITT-DOMENE.no' `
  -TunnelId '00000000-0000-0000-0000-000000000000' `
  -TeamName 'DITT-TEAM' -Audience '64-HEKSTEGN-FRA-ACCESS-APPEN' `
  -TunnelCredentialPath 'C:\Users\Jonas\.cloudflared\DIN-TUNNEL-ID.json'
./scripts/test-tablet-config.ps1
```

Erstatt alle eksempelverdier med faktisk liten-bokstav-hostname/team, gyldig UUID og riktig AUD. Skriptet lager bare lokale filer: ignorert `.env.tablet`, `.private-runtime/tablet/cloudflared.yml` og ny tilfeldig `.private-runtime/tablet/postgres-password`. Eksisterende konfigurasjon overskrives ikke; eksisterende DB-hemmelighet bevares. Tunnellegitimasjon opprettes senere lokalt av cloudflared og refereres med absolutt sti, utenfor Git. Begrens Windows-ACL til eier/administrator; verken secrets, konfigurasjon med credentials eller databasebackup skal inn i kildekontroll. Behold DB-passordet så lenge volumet beholdes; ny fil endrer ikke passordet i et eksisterende PostgreSQL-volum.

## Integrering etter godkjent 11.6

1. Vent på eksplisitt godkjent 11.6 og ferdig testing i den andre chatten. Registrer den eksakte godkjente commiten/release-identiteten. Hvis arbeidet fortsatt er ukommittert, avtal et godkjent snapshot i den chatten; ikke bruk worktree-basens gamle produktkode som erstatning.
2. Gjør senere integrering i en separat checkout basert på den godkjente versjonen. Denne leveransen har ingen commits å cherry-picke: ta først en reviewbar diff inkludert **alle nye filer**, og overfør bare tilgangsendringene ved godkjent integrering. Ingen blind kopi fra `D:\IBE160` og ingen Git-operasjoner i hovedmappen.
3. Sammenlign spesielt `backend/app/private_main.py` (lokale notice-/reader-ruter), `auth.py`, `run.py`, `frontend/src/PrivateAccess.tsx`, eksisterende Vite-typer og Docker-/Compose-oppsett. Behold godkjente 11.5/11.6-ruter, migrering 013, recovery-helper, generasjon/epoch-sperrer og alle status-før-retry-regler. Denne branchen inkluderer ikke disse lokale endringene. Ingen lagrings-/recovery-komponenter skal erstattes fra gammel base.
4. Gjenta transporttester, privat produksjonsbygg, proxytest og godkjent 11.6-regresjon på **syntetiske data i eget prosjekt med egne porter/volumer**. Ikke bruk dagens `verify-private-drafts.py`: det stopper vanlig API og strider mot isolasjonen i denne oppgaven. Tilpass testprosjekt/portvalg separat hvis bred 11.6-test senere kreves. Bekreft tidsfrister, uavklart kvittering og null utilsiktede POST ved Access-HTML/302/403, tapt svar og fornyelse i annen fane.
5. Dokumenter den nye testede release-identiteten, image-digests og nøyaktig deploy-checkout før publisering. Ingen migrering eller oppstart mot ordinære data i dette forberedelsesarbeidet.
6. Første nettbrettprøve bruker nytt `tablet_pg` med syntetisk konto. Det ordinære volumet gjenbrukes aldri automatisk. Hvis eksisterende private kontoer/dager skal følge med, må en separat godkjent backup/restore-plan prøves på en kopi først, med rådata-/schema-/konto-/kvitteringssammenligning og returpunkt. Ordinære data skal ikke få migreringer som del av denne leveransen. Tom pilotdatabase er standard for teknisk prøve; overføring av virkelige data krever egen beslutning.

## Senere aktivering – ikke utført

1. Avklar domene på Cloudflare, Zero Trust-konto, eieridentitet/IdP/MFA, tillit til Cloudflare og ønsket pilotdata. Registrer hostname, team, AUD og tunnel-ID. Ingen kjøp eller kontoopprettelse er utført.
2. Etter 11.6-godkjenning: installer/verifiser en valgt, signaturkontrollert cloudflared-versjon **2026.10.0 eller nyere**, uten tjenesteinstallasjon/autostart i første prøve. Opprett en separat navngitt tunnel lokalt (`cloudflared tunnel login`, deretter `cloudflared tunnel create ibe160-tablet`). Dette er fremtidige kontoendringer, ikke utførte trinn.
3. Opprett Access Self-hosted-app for hele hostname **før DNS/publisering**. Allow kun eksakt eieridentitet, MFA, 24 timers policy/app-økt; kontroller faktisk global/IdP-levetid. Ingen Bypass/Everyone/service-token i nettleseren. Legg Cache Bypass på hele hostname. Sjekk at ingen annen tunnelregel/Worker åpner samme origin.
4. Kjør forberedelsesskriptet med faktiske lokale verdier, kontroller ACL, kjør konfigurasjonskontroll. Valider tunnelreglene lokalt: `cloudflared tunnel --config .private-runtime/tablet/cloudflared.yml ingress validate` og `cloudflared tunnel --config .private-runtime/tablet/cloudflared.yml ingress rule https://DITT-HOST/private-api/auth/session`. Dette kobler ikke opp tunnelen. Verifiser at bare rett hostname treffer privat proxy, alle andre 404, og JWT-validering er på.
5. Bekreft at loopback 18081 er ledig. Først nå, på godkjent integrert kildekode og egen database, kan `docker compose --env-file .env.tablet -f compose.tablet.yaml --profile tablet up -d --build` kjøres. Det starter nye, separate tjenester og kjører migreringer **bare på nytt tablet-volum**. Ikke overstyr prosjektnavn, ikke kombiner Compose-filer. Opprett en fiktiv prøvebruker interaktivt med `docker compose --env-file .env.tablet -f compose.tablet.yaml --profile tablet exec private-api python -m app.manage provision tablet-provebruker`. Passordet oppgis skjult to ganger; ikke bruk `-T` eller passord på kommandolinjen. CLI-et reserverer `synthetic-`-prefikset for automatiserte tester, så ikke bruk det her. Dette er en egen fysisk pilotdatabase og skal ikke brukes til de destruktive regresjonstestene som krever bare automatiserte synthetic-kontoer. Bekreft CLI-bruken i godkjent release før kjøring.
6. Kontroller lokalt med eksplisitt `Host: DITT-HOST` at 18081 gir riktig privat inngang, demo 404, API uautorisert 401, feil Origin/CSRF 403 og ingen API-/DB-vertsporter. Loopback HTTP er bare proxykontroll; Secure-cookie-innlogging må testes via HTTPS. Kontroller at ordinære containere fortsatt har samme ID/starttid.
7. Opprett DNS-rute først når Access og connector-validering er kontrollert: `cloudflared tunnel route dns DIN-TUNNEL-ID DITT-HOST`. Start tunnelen i synlig, manuell terminal med `cloudflared tunnel --config .private-runtime/tablet/cloudflared.yml run DIN-TUNNEL-ID`. Ingen Windows-tjeneste, restart-policy, ruter- eller brannmurendring er forberedt som automatisk handling. Hvis utgående tunneltrafikk blokkeres, stopp og avklar; ikke åpne inngående porter.
8. Kjør testlisten under først med syntetiske data. Bekreft at ingen Access-økt eller feil AUD gir origin-tilgang. Vurder først etter prøven eventuell overvåket drift/autostart som egen beslutning. Etter desktop-omstart vil denne manuelle løsningen være utilgjengelig til Docker, tablet-prosjekt og tunnel er startet igjen; skjermlås/strømsparing/hjemmebrudd må inngå i pilotvurderingen.

## Tilbakeføring

1. Stopp **bare den nye tunnelens** foreground-prosess med Ctrl+C. Ikke stopp andre tunneler eller ordinære containere. Ved kompromittert tunnellegitimasjon: tilbakekall denne tunnelen i Cloudflare; ved kompromittert identitet: tilbakekall Access-økter og appøkter separat.
2. Fjern/deaktiver bare den nye DNS-ruten etter at tunnelen er stoppet. Behold Access-nekt inntil du er sikker på at hostname ikke kan nå en annen origin. Ikke endre eksisterende DNS.
3. `docker compose --env-file .env.tablet -f compose.tablet.yaml --profile tablet down` stopper bare det nye prosjektet. **Ingen `-v`**, ingen prune/reset, ingen sletting av passordfil/backup. Behold tablet-volum og hemmeligheter for inspeksjon. Hovedmiljøet trenger ingen restore når det ikke ble endret.
4. Ved senere dataoverføring/releasefeil: bruk den særskilt godkjente backup/restore-planen. Ikke kjør gammel appkode mot en nyere migrert database. Denne leveransen lager ikke en slik migrering eller automatisk rollback.

## Lenovo Pad / Android / Brave – fysisk testliste

Kjør når parkert, først på Wi-Fi hjemme, så med Wi-Fi av og mobilnett/deling på. Bruk samme hostname og syntetiske data. Noter Android-/Brave-versjon, klokkeslett, nett, skjermretning og faktisk resultat. Behold Brave Shields under normal innstilling først; ikke slå av beskyttelser globalt. Same-origin-oppsettet skal fungere uten tredjepartscookies. Avklar eventuelle browseravvik konkret.

| Prøve | Forventet resultat |
|---|---|
| HTTPS og innlogging | Gyldig betrodd sertifikat, ingen advarsler/mixed content; Access for eier → egen appinnlogging. Web Locks og secure context tilgjengelig. Etter Access-redirect fungerer Strict-cookies på appens egne requests. |
| Uautorisert | Ny privat Brave-fane uten Access får ingen private HTML/assets/API. Feil/annen e-post nektes. Gyldig Access uten appøkt gir appinnlogging/API 401. Feil origin/CSRF avvises. Ingen data via demo, andre stier eller direkte desktop-IP/8001/5432. |
| Lagring | Opprett/endre syntetisk utkast, bekreft lagring, last inn igjen og sammenlign identitet/revisjon/innhold. Bekreftet plan, merknad og utfall leses korrekt på begge nett. Ingen virkelig arbeidsdag brukes i første prøve. |
| Nettbytte/brudd | Wi-Fi → mobilnett, flymodus, tilbake: innhold skjules ved mislykket revalidering; forslag bevares i samme fane etter 11.6-kontrakten. Ingen falsk lagringsbekreftelse eller automatisk ny kommando. |
| Tapt lagringssvar | På isolert pilot: hold tilbake svar etter serveraksept; kontroller opprinnelig operasjon etter retur. Nøyaktig én effekt, bevart revisjonsvern, ingen duplikat eller overskriving av nyere endring. |
| Access utløp | Kort testpolicy: la Access utløpe mens appøkt lever. Avvist/HTML-svar er ingen kvittering. Forny Access i separat fane uten å laste den uavklarte fanen på nytt; kontroller tilgang og opprinnelig operasjon før videre arbeid. Test også tilbakeknapp og appbytte. |
| Appøkt/logout | Appøkt utløpt selv med gyldig Access krever appinnlogging. Logout i to faner fjerner innhold; tapt logout-svar og reload bevarer låsen til bekreftet tilbakekalling. App-logout og Access-logout er ulike; aldri anta at én avslutter begge. |
| Server/desktop borte | Stopp kun pilotens tunnel/API i avtalt test; ingen suksessmelding uten kvittering. Tilbakekomst gir eksplisitt kontroll/gjenoppretting. Test skjermlås/app bakgrunn og manuell gjenstart etter desktop-reboot separat. Ikke stopp ordinært miljø mens 11.6-testingen pågår. |
| Visning og personvern | Liggende/stående, skjermtastatur, forstørret tekst, dag/natt og Brave tilbakeknapp. Ingen private data i demo, URL, logger eller browserlagring utover nødvendige auth-/logout-cookies; ingen private visninger etter logout. |

## Utført verifisering og gjenstående bevis

Utført i denne grenen: 14/14 isolerte tester av transportmodus, Secure/HttpOnly/host-only/Strict-cookies, cookie-sletting, no-store, korrekt/manglende/forfalsket origin/CSRF og Secure-cookies over HTTP. FastAPI/Starlette var ekte, autentisering/DB var syntetiske testdobler; dette er **ikke** bevis på PostgreSQL/eierskap eller virkelig Access. Nettverksløs engangscontainer `ibe160-tablet-transport-check`, eksisterende image-ID `d43100eadc90`, skrivebeskyttet worktree, ingen port eller datavolum. 1 eksisterende Starlette TestClient-deprecation-advarsel, ingen testfeil.

TypeScript-kontroll og privat Vite 8.3.4-produksjonsbygg bestått i nettverksløs engangscontainer `ibe160-tablet-frontend-check`, eksisterende image `b41b7c1ca0de`, egne midlertidige filer i tmpfs. Separat `npm ci` i worktreet kunne ikke nå registry (DNS ENOTFOUND); derfor ble eksisterende låste avhengigheter fra frontend-imaget brukt. Dette beviser bygg med tilgjengelige avhengigheter, ikke en helt fersk nettinstallasjon/Docker-build.

`test-tablet-config.ps1` bestått med syntetisk vertsnavn: separat prosjekt/volum, bare loopback-proxy, ingen DB-/API-vertsporter og eksplisitt HTTPS-modus. `nginx -t` bestått mot rendret template i separat nettverksløs engangscontainer, Nginx-image digest `sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236`. Dette imaget er hentet lokalt; ingen ordinære images er bygget om. Compose-appen og databasen er ikke startet. Ingen ordinære data er lest gjennom appen eller migrert.

`scripts/verify-tablet-proxy.ps1` bestått med ekte Nginx og syntetisk HTTP-upstream på et nytt internt Docker-nettverk, uten publiserte porter, database eller datavolum. Verifisert privat inngang, relativ root-redirect, fjerning av API-prefiks, uendret Origin/CSRF/cookie, fjerning av forwarded-headere, no-store/CSP, uendret Secure-cookie og avvisning av demo/andre stier/ukjent Host. Første kjøring avdekket automatisk HTTP-redirect for API-prefikset uten slutt-skråstrek; eksplisitt avvisning og `absolute_redirect off` ble lagt til, og hele proxyprøven bestod etterpå. Alle prøvecontainere og det egne nettverket ble fjernet i finally; ingen ble igjen. Testen kan kjøres igjen med bare eksisterende lokale images (`--pull never`).

PowerShell-skriptene er parsede. `prepare-tablet-files.ps1` ble i tillegg kjørt i en separat `tmp/`-fixture med fiktive identifikatorer: riktig substitusjon og avvisning av overskriving bestod; testhemmeligheten var uendret etter nytt forsøk. Ingen virkelig konto-/tunnelkonfigurasjon er opprettet. `git diff --check` bestod. Siste Docker-lesekontroll viste samtidig arbeid fra den andre chatten i ordinært/disponibelt 11.6-miljø; det er ikke grunnlag for å hevde at hele miljøets tilstand var uendret gjennom tidsrommet. Denne oppgaven har bare opprettet/fjernet egne `ibe160-tablet-*`-testcontainere/nettverk og har ikke operert de ordinære tjenestene.

Gjenstår: godkjent 11.6-integrering/regresjon; helt ferskt image-bygg; cloudflared CLI-validering med faktisk hostname/team/AUD; konto/policy/cache/DNS-/sertifikatbevis; virkelig HTTPS-innlogging og PostgreSQL-lagring gjennom tunnel; Access-utløp og avvisningsbevis; alle fysiske Lenovo/Android/Brave-prøver på begge nett; desktop-strøm/restart/ressursvurdering. Ingen ekstern tilgang er aktivert, og ingen fysisk prøve er utført.

Mangler fra eier før senere aktivering: hvilket domene/hostname og Cloudflare/Zero Trust-team som skal brukes, eksakt tillatt innloggingsidentitet/IdP med MFA, lokal tunnel-ID/AUD/legitimasjonsfil, aksept av Cloudflare som mellomledd, og om en senere virkelig pilot skal starte tomt eller få en særskilt kontrollert overføring av eksisterende private data. Oppgi identifikatorer/valg; legg hemmeligheter lokalt som angitt over.
