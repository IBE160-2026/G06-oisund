---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - ../specs/spec-gps-speed/SPEC.md
  - ../specs/spec-gps-speed/measurement-and-behavior.md
  - ../specs/spec-gps-speed/verification.md
  - ../research.md
  - ../dependencies.md
status: draft-for-owner-review
approval: not-approved-for-build
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
---

# GPS-beregnet egen fart — epic og stories

## Overview

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

BMAD create-epics-and-stories, med kort SPEC og companions som kravgrunnlag i stedet for en ny PRD/UX/arkitekturprosess. Brukeren har delegert rutinevalg og sammenhengende planlegging; dette gir ingen implementeringsaksept. Foreslått versjon V1.4.5.

## Requirements Inventory

### Functional Requirements

- FR1: Vis kvalifisert native egen fart i km/t, konverter m/s×3,6.
- FR2: Skill null/ugyldig/gammel fart fra reell 0 og liten positiv køfart.
- FR3: Håndter oppstart, akselerasjon, bremsing, intervaller, støy, hopp og tidsfeil med eksplisitte kvalitets-/ferskhetsregler.
- FR4: Samordne én foreground opt-in-kilde, Pause/Off, tilgangstap og eksplisitt gjenopptakelse med posisjonsplanen.
- FR5: Vis fart uavhengig av ukjent fartsgrense/vegvalg, tydelig merket ved siden av registrert grense.
- FR6: Bevar målealder, generasjon, profil og årsak i delbart grensesnitt; gamle verdier kan ikke framstå som ferske.

### NonFunctional Requirements

- NFR1: Ingen ekstra skjult watch, råfix-logging/persistens, full historikk eller privat posisjonsnettverk; avgrenset RAM og rydding.
- NFR2: Dokumentert syntetisk logikk og senere separat Lenovo/Brave/Chrome-kvalifisering med feil-/forsinkelseskriterier.
- NFR3: Korridoruavhengig måling, regler og UI; gjenbruk eksisterende arkitektur.
- NFR4: Uprøvde terskler, metodebegrensninger og ikke-kjørte kontroller er tydelig merket.

### Additional Requirements

- AR1: Ferdig/testet V1 og separat byggbestilling før implementering. Fartsgrense/rutenett er ikke harde avhengigheter for fart alene.
- AR2: Ingen posisjonsdifferanse-reserve eller ekstra filter i første kandidat. Ingen database-/tjenesteombygging.
- AR3: Fast 300 m uendret; dynamisk avstand kun senere konsument. Ingen lyd, alarm, kart, kjøretøytilkobling eller bakgrunnsgaranti.

### UX Design Requirements

- UX-DR1: «Egen fart (GPS)» og enhet skiller seg fra registrert grenseskilt; «—» med kort årsak og «<1» for liten positiv fart.
- UX-DR2: Day/Night, responsiv layout, lesbare statuser uten kun farge, tastaturfokus og ingen kontinuerlig skjermleserannonsering av fart.
- UX-DR3: Tydelig Start/Pause/Off/Resume; retur alene starter ikke måling, og fart-resume etablerer ingen stoppeforekomst.

## Epic List

### GS-E1: Forstå egen fart med tydelig målekvalitet og registrert grense

Brukeren kan eksplisitt aktivere rådgivende egen fart, forstå bortfall og skille målingen fra registrert fartsgrense. Første fartsslice kan vurderes uten ferdig veg-/rutedata. Hele epicen venter med operativ aksept til enhetskvalifisering.

**FRs covered:** FR1–FR6. Alle NFR, AR og UX-DR inngår. Ett epic unngår oppdeling i tekniske lag.

## FR Coverage Map

| Krav | CAP | Epic / stories | Verifikasjon |
|---|---|---|---|
| FR1 | CAP-1 | GS-E1 S1/S2 | V01 |
| FR2 | CAP-1/2 | GS-E1 S1/S2 | V02/V03 |
| FR3 | CAP-2 | GS-E1 S2/S4 | V04–V07 og felt |
| FR4 | CAP-3 | GS-E1 S1/S3/S4 | V08 |
| FR5 | CAP-4 | GS-E1 S3/S4 | V09 |
| FR6 | CAP-1/2/3 | GS-E1 S1/S2/S3 | V03/V04/V08 |
| NFR1 | CAP-3 | GS-E1 S1/S3/S4 | V10 |
| NFR2/NFR4 | CAP-1/2/3/4 | GS-E1 S2/S4 | V01–V12 og felt |
| NFR3 | CAP-4 | GS-E1 S1/S3 | V11 |
| AR1/AR2/AR3 | CAP-1/3/4 | GS-E1 S1/S3/S4 | Porter, V12 |
| UX-DR1/2/3 | CAP-1/3/4 | GS-E1 S1/S3/S4 | V02/V08/V09 og UI |

## Avhengighetsrekkefølge

V1-port → S1 → S2 → S3 → S4. Ingen story avhenger av en senere story for sin avgrensede syntetiske leveranse. S1–S3 er eksperimentelle og gir ingen operativ målegodkjenning før S4. S3 kan bruke en fiktiv grenseadapter; ekte samvisning får separat integrasjonsport til kvalifisert speed-limits-kontrakt. S4 kan kvalifisere fart alene uten denne porten.

## Epic GS-E1: Forstå egen fart med tydelig målekvalitet og registrert grense

Mål: eksplisitt aktivert, rådgivende egen fart med forståelig kvalitet, og samvisning som ikke blander måling og registrert regel. Story-ID-ene er lokale for utvidelsen og endrer ingen V1-backlog.

### Story GS-E1-S1: Start og stopp en enkel, separat fartsmåling

Som sjåfør vil jeg selv starte egen fart og se om den er tilgjengelig, slik at jeg får nyttig informasjon uten krav om ferdig rute- eller fartsgrensedata.

**Avhengighet:** V1-port og ny byggeautorisasjon. Ingen full PP-/CRN-/SL-epic kreves. Revider faktisk baseline før kodeendring.

**Krav:** FR1/2/4/6, NFR1/3/4, AR1/2, UX-DR1/3.

**Omfang:** Minste delbare kontrollerabonnement, GS1-utdata, grunnleggende type/enhet/alder og to-prøvers oppstart, enkel lesbar fart/ukjent-visning. Alle livssyklus- og personverngrenser gjelder allerede her; S3 utvider samordningen og samvisningen. Eksperimentet eksponeres ikke som operativt kvalifisert fart før S2/S4.

**Acceptance Criteria:**

- **S1-AC1 — autorisert start. Given** gyldig privat tilgang, synlig side og Off, **When** brukeren velger Start og gir nødvendig tillatelse, **Then** opprettes eller gjenbrukes nøyaktig én autorisert watch, visningen er først «— / Venter på måling», og ny generasjon bindes til gjeldende kontekst. **And** uten trykk, ved nektet tillatelse eller manglende profil vises ingen målt fart.
- **S1-AC2 — native semantikk. Given** to typegyldige, tidsordnede prøver i riktig intervall (full dynamisk koherens tilføyes i S2), **When** V01/V02 kjøres med kontrollert kilde, **Then** 10 m/s vises 36 km/t, native 0 vises 0, 0,1 m/s vises <1 og null/undefined er ukjent. **And** ingen reserveberegning, grenseverdi eller gammel verdi brukes.
- **S1-AC3 — ferskhet. Given** kvalifisert fart og kilde med måletid eldre enn mottak, **When** V03 når 3000 ms fra måletid uten ny callback, **Then** qualified utløper og feltet blir «—». **And** 2500 ms gammel prøve får høyst 500 ms gjenværende levetid, ikke en ny 3 s-periode.
- **S1-AC4 — stopp og opprydding. Given** aktiv måling, **When** global Pause/Off, skjult side, tilgangstap, kontekstbytte, avslutning eller unmount skjer, **Then** watch stoppes, generasjon invalideres, fart og RAM ryddes, og sene callbacks/tillatelsesresultater gjør ingenting. **And** retur/reload starter ikke automatisk; V08/V10s grunnkontroller består.
- **S1-AC5 — konkret handoff. Given** eksisterende eller manglende posisjonskontroller, **When** delingsgrensen vurderes, **Then** GS-Q3 dokumenteres som kontrakt med én eier for watch, klokke, tilgang og global Pause/Off. **And** manglende eier realiseres bare én gang i eksisterende frontend; ingen ekstra skjult watch, backend-GPS-tabell eller endring i manuell aktivitetsstatus.

**Verifikasjon senere:** V01–V03, grunnleggende V08/V10, inspeksjon av GS1 og kildeeierskap. Kilde kan injiseres syntetisk. Ingen krav om fysisk GPS for storyens avgrensede programlogikk; ingen fysisk kvalifiseringspåstand.

### Story GS-E1-S2: Vis usikkerhet ved støy, fartsskifte og tidsfeil

Som sjåfør vil jeg få ukjent fart når målingen ikke er troverdig, slik at stopp, kø og bremsing ikke blir skjult av et gammelt tall.

**Avhengighet:** S1. Ingen senere story kreves for syntetisk verifikasjon.

**Krav:** FR2/3/6, NFR2/4, AR2, UX-DR1.

**Omfang:** Full GPS-LAB-1-kandidat, deterministisk rekkefølge/klokke/gap, koherens- og hoppsjekk, rekvalifisering og eksplisitt fravær av ekstra filter. Profilen forblir uprøvd på enheten.

**Acceptance Criteria:**

- **S2-AC1 — inngangsgrenser. Given** type-/område-/accuracy-variantene i V01/V07 og en tidligere god fart, **When** en ny tidsordnet ugyldig/null-prøve mottas, **Then** tidligere fart fjernes straks, riktig årsak vises og rekvalifisering krever nytt par. **And** null, NaN og negative verdier blir aldri 0 eller clampet.
- **S2-AC2 — tidsorden. Given** kvalifisert strøm og V04/V05, **When** duplikat, sen prøve, burst, framtidstid eller klokkehopp inntreffer, **Then** følger systemet målekontraktens prioritering uten fornyet alder fra reprise, uten forgiftet framtidsanker og med manuell resume etter klokkeanomali. **And** bruk faktisk Δt, ikke antatt 1 Hz.
- **S2-AC3 — bevegelse og stillstand. Given** V06 med uavhengig beregnede forventninger, **When** strømmen akselererer, bremser og går gjennom kø/0, **Then** nyeste koherente native fart vises uten ekstra filterlag; positiv lavfart forblir forskjellig fra 0, og null er ukjent. **And** koordinatdrift alene skaper ingen fart eller automatisk stillstand.
- **S2-AC4 — hopp og tilbakekomst. Given** et grovt hopp eller støy som avviser prøve, **When** V07 deretter leverer to nye koherente prøver, **Then** avvist verdi har aldri vært vist, og evaluatoren kan rekvalifisere uten å låses til gammelt anker. **And** ved ≥10 s råfix-gap avbrytes kontrolleren og krever manuell resume; bare speed=null med gode posisjonsfikser utløser ikke denne gapregelen.
- **S2-AC5 — evidensgrense. Given** uprøvd GPS-LAB-1, **When** syntetisk evaluering avsluttes, **Then** dokumenteres hvilke logikktilfeller som består, reset ved profilendring, og gjenværende GS-Q1/Q2. **And** terskler og koordinataccuracy omtales ikke som garantert fartsnøyaktighet; eventuell ny filteridé føres som senere forslag med målbart forsinkelsesbudsjett.

**Verifikasjon senere:** V01–V07 med fake clock, grenseverdier og invariantsjekk for ingen gammel verdi/ubegrenset buffer. Oppdatert kandidatprofil og gjenstående feltspørsmål er storyresultat, ikke gjennomført Lenovo-test.

### Story GS-E1-S3: Les fart og grense sammen og gjenoppta bevisst

Som sjåfør vil jeg skille egen fart fra registrert grense og selv gjenoppta måling etter avbrudd, slik at usikker veg eller retur til appen ikke gir misvisende informasjon.

**Avhengighet:** S2. Fiktiv adapter er tilstrekkelig for kombinasjonene. Ekte registrert grense venter på kvalifisert speed-limits-grensesnitt; dette blokkerer bare ekte grenseintegrasjon.

**Krav:** FR4/5/6, NFR1/3/4, AR1/3, UX-DR1/2/3.

**Omfang:** Samvisning, tilgjengelighet, samordning med posisjonsprogresjon og annen strekning. Ingen ny geometri-/NVDB-funksjon.

**Acceptance Criteria:**

- **S3-AC1 — uavhengige domener. Given** V09s fire kombinasjoner av kjent/ukjent fart og grense, **When** currentRoadQualified blir falsk, grensesnapshot mangler eller videre arm er usikker, **Then** ellers kvalifisert fart beholdes etter egne frister. **And** ukjent fart skjuler ikke en ellers kvalifisert grense og ingen felt kopierer den andre verdien.
- **S3-AC2 — tydelig visning. Given** Day/Night, stående/liggende og smal visning, **When** tall, «<1» og «—» vises, **Then** egen fart har egen tekstetikett/enhet og grensen egen skiltsemantikk, statuser leses uten farge alene, fokus er synlig, og skjermleseren annonserer ikke hvert fartstall. **And** ingen overskridelsesalarm eller lyd finnes.
- **S3-AC3 — gjenopptakelse. Given** V08s avbruddsmatrise og tidligere aktiv progresjon, **When** siden blir synlig eller tilgang gjenopprettes, **Then** ingen måling starter automatisk. **And** eksplisitt fart-resume får ny generasjon og nye prøver, mens progresjon fortsatt krever sitt manuelle forekomstanker; global Pause/Off stopper begge.
- **S3-AC4 — delt kilde og personvern. Given** begge forbrukere aktive, **When** fartspanelet fjernes, tilgang suspenderes eller en sen callback kommer, **Then** kildeeierskapet følger dependencies.md, maksimalt én autorisert watch finnes og felles stopp rydder alle måledata. **And** V10 finner ingen posisjoner/fartshistorikk i logger, nettverk eller persistens og ingen endring i aktivitet, utfall eller arbeidsdag.
- **S3-AC5 — gjenbruk og forvarsel. Given** to fiktive strekninger og forskjellige egenfarter, **When** V11/V12 kjøres, **Then** samme kjerne/profil/UI brukes uten korridorspesifikke grener, og dagens 300 m-policy forblir uendret. **And** framtidig qualifiedSpeed er bare en beskrevet kontrakt, ikke aktiv dynamisk avstand.

**Verifikasjon senere:** V08–V12, komponent-/nettleserprøver og kontraktkontroll mot ekte grenseadapter når tilgjengelig. Rapporter «samvisning med syntetisk grense» separat fra «ekte grenseintegrasjon kvalifisert».

### Story GS-E1-S4: Avgjør om Lenovo-målingen er egnet for eksperimentell bruk

Som produkteier vil jeg ha etterprøvbare resultater per nettleser, slik at funksjonen bare omtales som kvalifisert der målekvalitet, respons og personvern er dokumentert.

**Avhengighet:** S1–S3, ferdig/testet V1, senere autorisasjon til fysisk test og egnet uavhengig referanse. Ekte grenseintegrasjon er ikke nødvendig for fartskvalifisering.

**Krav:** FR1–FR6, NFR1/2/4, AR1/2/3, UX-DR1/2/3.

**Omfang:** Én avgrenset kvalifiseringspakke for faktisk Lenovo, Brave og Chrome. Ingen endring av målemetode, reserve eller skjult logging som del av testen.

**Acceptance Criteria:**

- **S4-AC1 — forhåndsfastsatt protokoll. Given** verifikasjonsdokumentets uprøvde kriterier, **When** forsøket forberedes, **Then** fryses enhets-/nettleser-/profilversjoner, referansens feilbudsjett, kriterier og rapportformat før måling. **And** manglende referanse/tillatelse rapporteres som ikke utført/ikke kvalifisert, ikke pass.
- **S4-AC2 — per-nettleser resultat. Given** autorisert testoppsett, **When** start, stillstand, stabil fart, akselerasjon, bremsing, kø og bortfall gjennomføres i Brave og Chrome hver for seg, **Then** rapporteres faktisk dekning, null-andel, feil og total forsinkelse mot hvert kriterium i protokollen. **And** manglende native speed eller feil grense gir no-go for berørt profil; ingen fallback innføres.
- **S4-AC3 — livssyklus og lesbarhet. Given** de to nettleserne, **When** avbrudd, tillatelse av/på, tilgangstap, mørk/lys visning og ukjent grense kontrolleres, **Then** ingen gammel fart, automatisk resume eller ekstra watch observeres, og lesbarhet/tilgjengelighet dokumenteres med saniterte bevis.
- **S4-AC4 — minimert evidens. Given** feltmålinger og ressurskontroll, **When** rapporten lagres, **Then** inneholder den kun scenarioaggregater, versjoner, begrensninger og kvalifiseringsvedtak, uten råposisjoner, privat rute eller full tidsserie. **And** batteri/varme omtales som observert, ikke som uprøvd levetidsgaranti.
- **S4-AC5 — tydelig beslutning. Given** samlede resultater, **When** epicen vurderes, **Then** skilles dokumentert programlogikk, fysisk fartskvalifisering og ekte grenseintegrasjon. **And** et avsluttet no-go-forsøk kan være ferdig undersøkelse, men gir ikke operativ epicaksept; nytt metode-/filterforslag krever ny bestilling og profil.

**Verifikasjon senere:** Hele Lenovo-tabellen og V01–V12-evidens fra tidligere stories. Ingen av disse kontrollene er utført i planleggingsoppgaven.
