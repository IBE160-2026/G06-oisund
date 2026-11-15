---
title: "Etterfølgende arkitekturvurdering – faglærerens Pytagoras-referanse"
created: 2026-11-15
updated: 2026-11-15
status: retrospective-documentation-assessment
reference_commit: 4d97c76ed7557793ce407c7f6cf6f2c269307475
reference_date: 2026-11-12
product_baseline: v1.0.1
new_product_decisions: none
---

# Etterfølgende arkitekturvurdering av Pytagoras-referansen

> **Skrevet 15. november 2026, etter ferdigstilt V1 og publisert V1.0.1.** Dette er en vurdering av et eksternt eksempel, ikke bussassistentens opprinnelige designbegrunnelse. Faglærerens originalfil er uendret. Ingen kode, teknologistakk, tjenester eller produksjon er endret gjennom vurderingen.

## 1. Kilde, intensjon og autoritet

Hele [technology.md](technology.md), inkludert §§1–8 og underpunktene om miljøvariabler, er lest. [Commit 4d97c76ed7557793ce407c7f6cf6f2c269307475](https://github.com/IBE160-2026/G06-oisund/commit/4d97c76ed7557793ce407c7f6cf6f2c269307475) ble lagt inn av Bård Pettersen 12. november 2026 med tittelen «Legg til technology.md i arkitekturmappen». Commitmeldingen sier: «Teknologioversikt fra faglærer som referanse for arkitekturarbeidet.» Resten av meldingen inneholder medforfatter- og sesjonsattribusjon, ingen ytterligere prosjektkrav.

Filen identifiserer selv `pytagoras-website-v2` / Pytagoras Forlag og beskriver butikk, kunder, betaling, abonnement, innholds-/kurstjenester og KI-assistent. Dens krav til blant annet Supabase, Railway, Resend, nøkler og replikering gjelder **den plattformen eller en nettside som skal replikere den**. Verken filen eller commitmeldingen vedtar disse valgene for bussassistenten. Eksemplet har også egne unntak: ekstra innholdstjenester kan utelates når behovet ikke finnes.

Vi bruker derfor filen som sammenligningsgrunnlag for prinsipper, og vurderer hvert prinsipp mot eget behov. Den får ikke forrang over SCOPE-02, dokumenterte eierbeslutninger eller den kvalifiserte implementasjonen. Felles bruk av FastAPI/React/PostgreSQL betyr heller ikke at de to plattformene har samme arkitektur.

**Separat dokumentasjonsspor:** Denne vurderingen følger `4d97c76`. PRD-kritikken ligger i en annen fil/commit (`e01712c`) og er fulgt opp separat. Ingen av vurderingene nedenfor tilskrives faglæreren som PRD-kritikk; ingen av de nye sammenligningene omskrives til opprinnelige eierbeslutninger.

**Kildebegrensning:** Dette arbeidet verifiserer bussassistentens kildefiler og eksisterende bevis. Pytagoras-plattformens eget repository og faktiske drift er ikke undersøkt. Beskrivelsene av den plattformen nedenfor er hva lærerreferansen oppgir, ikke en uavhengig teknisk revisjon av Pytagoras.

## 2. Kontrollert versjonsgrunnlag

| Referanse | Betydning for vurderingen |
|---|---|
| V1.0.1, `15011042b1fe093becbe68177e6396e456b1f35f` | Publisert vedlikeholdsleveranse 4. november norsk tid. [Vedlikeholdsrapport](../../../docs/evidence/v1.0.1-maintenance-20261104.md) beskriver O3–O6-status. |
| GitHub-main, `4d97c76ed7557793ce407c7f6cf6f2c269307475` | Kontrollert ved oppstart. Etter V1.0.1 er lærerens PRD-tilbakemelding og teknologioversikt lagt til; app-/deploykode er uendret mellom disse referansene. |
| Sist rapportert produksjon, `7921eb54e4816aaab9368c3efd851bcf692f3823` | V1.0.1-rapporten oppgir samme app-, container- og deploygrunnlag som releasen. Dette er et datert driftsbevis, ikke ny serverinspeksjon 15. november. |
| Passordgren, `29a77ff95cc7607b81c3351375771b6b23d2d1dd` | Kontrollert GitHub-HEAD og lokal kilde. Implementert V1.1.0-kandidat med separat kvalifikasjon og gjenstående praktiske porter; ikke dokumentert som publisert release. |
| Denne dokumentasjonsgrenen, utgangspunkt `d37511abfb97a3e87fadfc415748e764103b7738` | Inneholder allerede PRD-oppfølgingen. Arkitekturvurderingen får egne filer, egen logg og egne endringer. |

## 3. Faktisk teknologikart – ingen overføring av krav fra eksemplet

Versjoner i tabellen er kilde-/imagegrunnlaget som ble lest, ikke påstander om ny driftsmåling eller anbefaling om oppgradering.

| Område | Pytagoras-referansen oppgir | Bussassistentens undersøkte løsning og kilde |
|---|---|---|
| Produkt og struktur | Butikk/kunde/admin/KI, flere innholdstjenester og et kontrollplan | Privat sjåførverktøy; modulær FastAPI-backend, React-nettleser og PostgreSQL. Tilgangsgate/proxy er driftsgrenser, ikke egne handels-/innholdsdomener. [Arkitekturgrunnlag](architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md). |
| Frontend | Next.js 16, React, Tailwind/shadcn, rike editorer og flere moduler | React 19.3.1, TypeScript 7.0.2 og Vite 8.3.4 i [package.json](../../../frontend/package.json), med npm-lock. Vite bygger statiske filer; privat produksjonsfrontend serveres av nginx. Ingen Next.js-runtime eller behov for butikk/editor-verktøykassen er etablert. |
| Backend | FastAPI, uv, SQLAlchemy async/asyncpg, Alembic | FastAPI 0.149.0, Uvicorn 0.54.0 og psycopg 3.3.6 i [requirements.lock](../../../backend/requirements.lock). [Dockerfile](../../../backend/Dockerfile) bruker Python 3.13.18, installerer låst fil med pip under bygg og fjerner pip fra runtime. Ingen SQLAlchemy/Alembic/uv-overgang er vedtatt. |
| Database og migrasjoner | PostgreSQL 16 / Supabase, Alembic som pre-deploy | Ubuntu-grunnlaget bruker PostgreSQL 17.11 med fast image/digest i [Dockerfile.postgres](../../../deploy/ubuntu/Dockerfile.postgres). [private_storage.py](../../../backend/app/private_storage.py) bruker psycopg og ordnede SQL-migrasjoner, migrasjonsregister og PostgreSQL-transaksjonslås. [run.py](../../../backend/app/run.py) kjører migrering før API-start. Lokale vurderings-/testoppsett har egne Compose-filer; ingen SQLite-erstatning for private integrasjonsbevis. |
| Offentlig inngang | Caddy/Railway, single-origin frontend/API | Ubuntu/systemd, Cloudflare Tunnel/Access, nginx-gateway og separat Access-gate. Gateway publiseres på vertens loopback; API/database ligger på interne Docker-nett. [Compose](../../../deploy/ubuntu/compose.yaml), [nginx](../../../deploy/tablet/nginx.conf.template). Nettleseren bruker samme origin og `/private-api`; lokale vurderingsporter er et separat oppsett. |
| Innlogging og tillit | Lokal bcrypt + HS256-app-JWT, valgfri Supabase-login; egne Ed25519-capability-tokens | [auth.py](../../../backend/app/auth.py) bruker scrypt, opaque serverøkter, cookie/CSRF/Origin- og eierkontroll. Økten har fast 14-dagersfrist. Cloudflare Access-JWT valideres i [gate.py](../../../deploy/tablet/access_gate/gate.py), som ikke erstatter appens eierkontroll. Appen utsteder ikke Pytagoras-lignende innholdstokens. |
| Filer/cache | Permanente private Storage-buckets, Redis og outbox-refresh | PDF behandles kortvarig; eksplisitt lagring beholder strukturerte fakta, ikke originalarkiv. Ingen Supabase Storage, Redis eller offline-outbox. Begrenset JWKS-nøkkelcache finnes i tilgangsgaten og er ikke en katalogcache eller privat offlinebuffer. |
| Tester | Blant annet SQLite per test, Vitest og Playwright | pytest, Playwright og faktisk API/PostgreSQL i separate syntetiske miljøer. Minnedemo og HTTP-dobler er tydelig forskjellige fra database-/restartbevis. [Sporbarhet](../../../docs/submission/traceability.md), [vurderingsoppskrift](../../../scripts/submission.mjs). |
| Drift og release | Railway, offsite R2, watchdog/heartbeat, automatisk deploy fra `production` | Docker Compose/systemd, helse-/statuskontroller, backup/isolert restore og kontrollert deploy/rollback via [driftsverktøy](../../../deploy/ubuntu/bussassistentctl.py). [Driftsguide](../../../docs/ubuntu-server.md) har separate prosedyrer. Git-push deployer ikke bussassistenten automatisk. Ingen Railway-/R2-/watchdog-tjeneste innføres. |
| Betaling, KI og e-post | Stripe, Vipps, OpenRouter, Resend, valgfri Fiken | Utenfor levert produkt. PDF-import er programmert tolkning med pdfplumber, ikke KI-kjøring. V1.1.0-kandidatens administrerte kodeoverlevering er ikke integrert transaksjonsmail. |

### Egen konfigurasjon skal ikke erstattes av referansens variabelnavn

| Referanseeksempel | Bussassistentens kontrollpunkt |
|---|---|
| `APP_ENV=production` | Privat kjøring velges med `APP_MODE=private-local`. Produksjonstransport velges eksplisitt med `PRIVATE_HTTPS_DEPLOYMENT=1` og gyldig `PRIVATE_ORIGIN`; navnet `private-local` alene betyr ikke at oppsettet bare er localhost. Loopbackutvikling bruker en separat eksplisitt innstilling. |
| `DATABASE_URL`, Supabase-nøkler | Privat lagring krever `PRIVATE_DATABASE_URL` og `PRIVATE_DATABASE_PASSWORD_FILE`. `private_storage.py` avviser faktisk satt generisk `DATABASE_URL` i privat kontekst. Referansens konfig kan derfor ikke kopieres inn som en alternativ gyldig oppskrift. |
| `JWT_SECRET`, `ADMIN_EMAILS`, `RESOURCE_TOKEN_*` | Dette er ikke bussassistentens appøkt-/administrator-/rettighetsmodell. Gatepolicy og applikasjonsøkter har forskjellige ansvar; ingen nye nøkler eller administratorroller utledes. |
| `NEXT_PUBLIC_*` | Bussassistentens Vite-konfig er byggeinformasjon for klienten. [Privat frontend](../../../frontend/src/PrivateAccess.tsx) og [produksjonsbygg](../../../deploy/tablet/Dockerfile) bruker blant annet `VITE_PRIVATE_API_BASE=/private-api`. Hemmeligheter skal ikke gjøres til klientkonfig; referansens Next-variabler er ikke et nytt API for vår app. |

Bare variabelnavn og ansvar er undersøkt her. Ingen hemmelige verdier er lest, kopiert eller publisert.

## 4. Prinsipper og kontrollpunkter vurdert mot eget behov

«Allerede ivaretatt» nedenfor betyr underbygd innen angitt kode/evidens, ikke full sikkerhetssertifisering eller en ny testkjøring.

| Prinsipp i referansen | Egen relevansvurdering | Status og avgrensning for bussassistenten |
|---|---|---|
| Lokal kjøring uten eksterne leverandørnøkler (§1/§8) | Relevant for at faglærer kan kjøre leveransen uavhengig av eierens drift. | Allerede ivaretatt gjennom isolert lokal fullstack med syntetiske data og genererte lokale innloggings-/databasehemmeligheter. Dette er uavhengighet fra eier-/leverandørnøkler, **ikke null autentisering eller null hemmeligheter i alle miljøer**. [12.5-reproduksjon](../../../docs/evidence/12-5-reproduction.md). |
| Deterministisk mock-fallback (§1/§3) | Relevant som eksplisitt test-/demoteknikk. Ikke egnet som automatisk erstatning for privat tilgang, lagring eller operative kilder. | Minnedemo, syntetiske fixtures og avgrensede testdobler finnes. Privat lagrings-/autorisasjonsfeil må gi avslag/utilgjengelig/uavklart svar, aldri fiktive «ekte» data eller falsk lagringskvittering. [Gjenoppretting](../../../frontend/src/recoverOperation.ts), [feilbevis](../../../docs/evidence/11-6-server-recovery.md). Referansens egen produksjonsvakt for `JWT_SECRET` viser dessuten at dens generelle fallback-utsagn ikke betyr at all sikkerhetskonfig er valgfri. |
| Én origin og tydelige tillitsgrenser (§2) | Relevant for betrodd rute, eksponering og skillet mellom ytre tilgang og eierkontroll. | Privat drift har samme origin, nginx og intern gate/API/database. Gate-token videresendes ikke som appidentitet; backend kontrollerer egne økter, CSRF, Origin, eier og levetid. O3 er gjennomført innen dokumentert omfang. O4 er administrativt lukket med gjenstående WAN-/IPv6-bevisgrenser; ingen ny generell godkjenning. |
| Kortlivede tokens/JWKS (§2/§6.8) | Prinsippet om uttrykkelig utsteder/mottaker og avgrenset tillit er relevant. Referansens tjenestesplitt og ressursrettigheter dekker et annet behov. | Bussassistenten validerer ytre Access-JWT i en egen gate; det er ikke distribuerte app-capabilities. O5 kvalifiserer terminerbart JWKS-/DNS-oppslag. Tokenvarigheter på 5/15/60 minutter og Ed25519 er ikke nye krav til appens 14-dagers serverøkt. Ingen ekstra innholdstjeneste foreslås. |
| Hemmeligheter, sikre standarder og oppstartsvakter (§2/§6) | Relevant for å unngå hemmeligheter i Git, klientbygg og feil miljø. | Filbaserte Compose-hemmeligheter, eksplisitt HTTPS/loopbackkonfig og privat databasevakt finnes. Eksempelverdier eller manglende privat konfig erstattes ikke med produksjonsmock. Det er ansvar/prinsipp som gjenbrukes, ikke referansens navn eller nøkkelliste. |
| Modulære funksjonsområder (§3) | Relevant for avgrensning av eierskap, testing og senere utvidelser. | Modulær backend med egne domene-/lagringsmoduler er allerede valgt i SCOPE-02. Det begrunner ikke flere deploybare tjenester, et pluginsystem eller at katalog-/handelsmoduler kopieres. Referansen oppsto senere og er ikke historisk årsak til det opprinnelige valget. |
| Feature flags i frontend/backend (§3/§6.13) | Kan være relevant hvis en fremtidig funksjon må aktiveres gradvis. | Nåværende miljø-/konfiggrenser er ikke et generelt produktflaggssystem. Frontend-skjuling alene er aldri tilgangskontroll. Passordkandidatens separate gren/testmiljø er ikke det samme som et vedtatt flaggsystem. Ingen generelle `FEATURE_*` innføres. |
| Transaksjoner og migrasjoner (§3/§5) | Relevant for tapte svar, samtidige oppdateringer og bevart data ved endring. | PostgreSQL-transaksjoner, revisjoner, operasjons-ID-er og versjonerte SQL-migrasjoner finnes. Referansens særregel om aldri å kalle `rollback()` på delt SQLAlchemy-async-sesjon løser et bestemt ORM-problem; den skal **ikke** bli et generelt forbud mot rollback i psycopg-baserte transaksjoner. [Lagring](../../../backend/app/private_storage.py), [sporbarhet](../../../docs/submission/traceability.md). |
| Reproduserbare bygg og miljøer (§3–5) | Relevant for riktig test-/produksjonskilde og kontrollerte avhengigheter. | npm-lock, `requirements.lock`, faste image-digests og separate Compose-prosjekter finnes. Oppgitt lokal/staget kode, serverkilde og testversjon må fortsatt holdes atskilt. Å kopiere uv, Alembic, Next eller Railway ville være nye valg uten dokumentert behov. |
| Seed/demo kun i avgrensede miljøer (§3) | Relevant for å beskytte private data og gjøre vurderingen gjentakbar. | Syntetiske kontovakter og kontroll av prosjekt/porter/volumer finnes; reset er begrenset til vurderingskontekst. [test_submission_safety.py](../../../backend/tests/test_submission_safety.py), [scripts/submission.mjs](../../../scripts/submission.mjs). Referansens automatisk seed ved oppstart er ikke tillatelse til å seed/resette privat produksjon. |
| Backup og isolert restore (§5/§6.11/§8) | Relevant og allerede del av inkludert drift; gjenopprettbarhet må demonstreres, ikke bare anta at en kopi er tatt. | V1.0.1 har dokumenterte backup-/isolert-restore-prøver og databevaringskontroller. Windows-kopier har 48-timers oppbevaring ryddet ved vellykket kjøring; avslått maskin gir ikke absolutt slettefrist. Dette beviser ikke R2/offsite-oppsett eller et avtalt RPO/RTO. Kandidatens gjenopprettede passord/økter krever særskilt behandling, se §5. |
| Helsekontroller og varsling (§5) | Relevant å skille frisk tjeneste fra frisk funksjon og vellykket backup/opprydding. | Compose-healthchecks, systemd/status, datert driftskontroll og nyttelastfri oppryddingsobservasjon finnes. [test_cleanup_observability.py](../../../backend/tests/test_cleanup_observability.py) skiller oppryddingsfeil fra databasekontakt. Dette er ikke bevis for ekstern watchdog, døgnbemannet varsling eller et fast responstidsløfte. |
| Persondata nær ansvarlig tjeneste (§2) | Dataminimering og ikke å spre personopplysninger til ekstra tjenester er relevant. | Kortvarig PDF-behandling, strukturert lagring, eierkontroll og retensjon finnes. Ingen egen innholdstjeneste trenger `actor_ref`. Kontokoblede skift er fortsatt personopplysninger; logisk sletting fra aktiv DB betyr ikke at alle backupkopier er slettet. |
| Innholdssikkerhet og CSP (§4) | Relevant å behandle importerte/kildebaserte tekster som data. | Gateway har CSP og private cache-/rammegrenser; kilde-URL-er er avgrenset og frontend viser tekst. Ingen behov for TipTap, HTML-editor eller å kopiere Pytagoras-domener til CSP er påvist. Ingen full tilgjengelighets-/sikkerhetsrevisjon hevdes. |
| Automatisk produksjonsgren/cutover (§5/§8) | Sporbar release og kontrollert tilbakeføring er relevant; automatisk trigger er et separat valg. | Bussassistenten bruker uttrykkelig deploy/rollback med kilde-/releaseidentitet. Git-push og publisering av dokumentasjon starter ikke produksjon. `production`-gren, Railway og null-nedetidsløfte innføres ikke av referansen. |
| Betaling, e-post, regnskap, KI og permanent objektlagring (§3–8) | Utenfor nåværende problem og levert omfang. | Stripe, Vipps, Resend, Fiken, OpenRouter og Supabase Storage er ikke krav, kontoopprettingsoppgaver eller manglende leveranser i bussassistenten. Ingen slike integrasjoner opprettes. |

## 5. V1.1.0-kandidaten – samme grunnarkitektur, egne kontrollpunkter

Passordarbeidet utvider tilgangslivsløpet på egen gren; det dokumenterer ikke overgang til Pytagoras' auth-/e-post-/tjenestemodell. Den undersøkte [statusen](https://github.com/IBE160-2026/G06-oisund/blob/29a77ff95cc7607b81c3351375771b6b23d2d1dd/_bmad-output/experimental-extensions/password-management/implementation/status.md) og [eierjournalen](https://github.com/IBE160-2026/G06-oisund/blob/29a77ff95cc7607b81c3351375771b6b23d2d1dd/_bmad-output/experimental-extensions/password-management/implementation/owner-tests-20261104.md) skiller teknisk implementasjon, delvis fysisk kvalifikasjon og gjenværende aksept.

- **Appøkt og ytre tilgang forblir forskjellige:** Passordendring/gjenoppretting påvirker appens legitimasjon og økter; tap av SSH eller Cloudflare Access krever deres egne rutiner. En ytre Access-token er ikke appens passordreset.
- **Kodeoverlevering er ikke en e-postintegrasjon:** Eier har valgt manuell sending til kjent mottaker og operatørens SENDT-markering. Teknisk kontroll av denne flyten dokumenterer ikke faktisk sending/identitetskontroll eller full SSH/helper-kjede. Referansens Resend-krav skal ikke overføres.
- **Restore må håndtere gjenopplivet legitimasjon:** Kandidatens [restore-rutine](https://github.com/IBE160-2026/G06-oisund/blob/29a77ff95cc7607b81c3351375771b6b23d2d1dd/_bmad-output/experimental-extensions/password-management/implementation/restore-runbook.md) beskriver sperret trafikk/skrivere, migrering/retensjon, ugyldiggjøring av gjenopprettede passord, økter og aktive gjenopprettingsbevis, og kontrollert gjenåpning. Dette er kildebelagt kandidatfunksjonalitet, **ikke allerede levert V1.0.1-atferd eller utført produksjonsrestore**.
- **Operativ kvalifikasjon består som egen grense:** Installasjon av kandidatens vakter, faktisk overlevering/innløsning, full SSH/helper-flyt og sluttaksept kan ikke erstattes av referansens eksempelliste eller av isolerte tekniske tester. Allerede beståtte eierprøver merkes ikke som ugjort.

Den relevante oppfølgingen er å beholde disse eksisterende skillene tydelige. Vurderingen oppretter ikke nye releaseporter, krever ikke at all O6 er lukket og lover ikke V1.1.0-dato eller mer funksjonalitet.

## 6. Risiko for kildeforveksling og gjennomførte presiseringer

**Funn:** Før denne oppfølgingen lå en generisk `technology.md` direkte under prosjektets arkitekturmappe uten en README som klassifiserte filen. Filens eget produktnavn gjør proveniensen lesbar, men en leser/agent som søker etter «architecture», «technology», «påkrevd» eller miljøvariabler, kan fortsatt ta sjekklisten ut av sammenheng. Den vedtatte arkitekturfilen ligger én mappe dypere. Dette er en konkret dokumentasjonsrisiko, ikke bevis for at referansen allerede har endret kode eller beslutninger. Søk i den undersøkte checkouten fant ingen eksisterende omtale av `technology.md` utenfor selve filen.

**Tiltak gjennomført:**

1. Ny [arkitektur-README](README.md) klassifiserer ekstern referanse, vedtatt grunnlag, etterfølgende vurdering og driftsbevis, og gir en eksplisitt leseregel også for KI-agenter.
2. Prosjektets [README](../../../README.md) lenker til denne arkitekturoversikten separat fra PRD-oppfølgingen.
3. [ARCHITECTURE-SPINE.md](architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md) får bare et datert lesernotat som viser til kildeklassifisering og dette tillegget. Ingen tidligere AD-beslutning eller kravtekst skrives om som om vurderingen eksisterte ved designstart.
4. Dette tillegget samler relevant sammenligning, versjonsgrenser og oppfølging. `technology.md` beholdes på lærerens opprinnelige plassering og med uendret innhold/blob `0b8bfe7c847690280756b2dd0454bd30e347e0ca`.

**Viktige eldre formuleringer i arkitekturgrunnlaget:** `pdfplumber` som bare en kandidat, ekstern hosting utsatt (AD-13), og et generelt forbud mot historiske private backuper beskriver tidligere planlegging. Den leverte tekstparseren, inkludert Ubuntu-drift og faktisk backup er dokumentert senere. Det nye lesernotatet og dette tillegget gjør denne tidsgrensen uttrykkelig; de låner ingen teknologi fra Pytagoras for å forklare den. Modulær backend, serverautoritativ tilstand, tilgangskontroll og avgrensning mot offline/GPS er fortsatt relevante SCOPE-02-valg.

## 7. Oppfølging: dokumentasjon, eksisterende arbeid og mulige senere valg

| Kategori | Konkret punkt | Status / konsekvens |
|---|---|---|
| Dokumentasjon | Klassifisere lærerreferansen og avklare «påkrevd»/miljøvariabler/tjenesteliste | Utført i oversikt, README, spine-notat og dette tillegget. Ingen ny tjeneste eller kontooppretting kreves. |
| Dokumentasjon | Skille opprinnelig arkitektur, levert V1.0.1 og kandidatens nye kontrollpunkter | Utført med faste kilder og datert vurdering. PRD-revisjonen er uendret i denne oppfølgingen. |
| Eksisterende kandidatoppfølging | Praktisk kodeoverlevering/innløsning, SSH/helper-/installasjonskontroller og eieraksept | Videreføres i passordgrenens eksisterende status/journal. Ingen nye krav eller tester er utført her. |
| Eksisterende drift | Navngitte O6-/stabilitetsrester og O4s dokumenterte bevisbegrensninger | Består som før. O3/O5 er ikke gjenåpnet. Dette er ikke nye funn fra en sikkerhetsskanning. |
| Mulig fremtidig driftsbeslutning | Hvis et tilgjengelighetsløfte eller større avhengighet av tjenesten blir aktuelt: avklar akseptabelt datatap/gjenopprettingstid (RPO/RTO), varslingsmottaker og om dagens backupplassering er tilstrekkelig | Det er ikke funnet et slikt kvantifisert løfte i undersøkt driftsgrunnlag. Dette er et forslag ved nytt behov, ikke en mangel som automatisk må implementeres for V1.0.1/V1.1.0. Ingen offsite-/watchdogleverandør er valgt. |
| Mulig fremtidig utvikling | Ved faktisk behov for gradvis utrulling: vurder avgrensede funksjonsflagg med backendhåndheving | Ikke vedtatt, ikke nødvendig bare fordi referansen har flags. Ingen pluginsystem-/mikrotjenesteplan opprettes. |

Det gjenstår ingen kildeklassifisering eller dokumentasjonsretting som er nødvendig for denne oppgaven. Senere ønsker har ingen automatisk prioritet, frist eller produktgodkjenning. En ny ekstern integrasjon må begrunnes i bussassistentens faktiske behov og behandles separat.

## 8. Verifikasjon av dokumentasjonsendringen

Hele lærerfilen og commitmeldingen er lest. Sammenligningen bygger på de lenkede arkitektur-, pakke-/lock-, Docker-/Compose-, tilgangs-, lagrings-, gjenopprettings- og driftsfilene samt passordgrenens egne status-/restorekilder. Originalreferansens blobidentitet og uendrede PRD-filer er kontrollert, sammen med dokumentlenker og Git-diff. Spine-endringen er bare lesernotatet; kildekode og produkt-/deploykonfigurasjon er uendret.

Det er ikke kjørt app-/integrasjonstester, ny driftsinspeksjon, sikkerhetsskanning eller produksjonsrestore. Tidligere resultater beholder sitt dokumenterte miljø, tidspunkt og omfang. At et prinsipp er relevant eller allerede underbygd, er ikke bevis for alle mulige feiltilfeller.
