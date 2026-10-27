---
stepsCompleted: [1, 2, 3, 4]
status: planning-complete
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
planning_version: SL-PLAN-1
build_authorization: not-granted
inputDocuments:
  - ../specs/spec-speed-limits/SPEC.md
  - ../specs/spec-speed-limits/behavior.md
  - ../specs/spec-speed-limits/pilot-manifest.md
  - ../specs/spec-speed-limits/verification.md
  - ../specs/spec-speed-limits/signs-and-rights.md
  - ../specs/spec-speed-limits/technical-addendum.md
  - ../qualification/2026-10-27/qualification.md
  - ../interfaces.md
  - ../research/technical-speed-limits-2026-10-27/research.md
---

# V1.4.0 — Epic Breakdown

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Overview

Avgrenset brownfield-plan. SPEC/behavior gir kravgrunnlaget i stedet for ny PRD/UX; eksisterende arkitektur bevares. Brukerens forhåndsautorisasjon dekker rutineovergangene i BMAD, ikke bygging eller produktaksept. Ingen sprintstart.

## Requirements Inventory

### Functional Requirements

FR1: Vis aktuell registrert vegfartsgrense med originalt norsk skilt eller tydelig ukjent med årsak (CAP-1/5, AC-01/12).
FR2: Vis nærmeste kommende økning/reduksjon med mindre skilt og målebasert nedtelling fra omtrent300m langs relevant rettet veg; sen oppstart, tett serie og deduplisering inngår (CAP-2, AC-02–05).
FR3: Bytt aktuell verdi bare ved underbygget passering; overlapp gir ukjent, ikke gammel eller tidlig ny grense (CAP-3, AC-06).
FR4: Skill aktuell vegtillit fra videre vegvalg; håndter alle fire rundkjøringer, parallelle veger, hopp og feil arm uten tvang til plan (CAP-4, AC-07/08).
FR5: Håndter stopp, avbrudd, eksplisitt gjenopptakelse, bortfall av varsel, avvik, kontekst-/kildefeil og tilgangstap (CAP-2/4, AC-09–11).
FR6: Vis kilde-/databegrensninger og gyldighet; manglende/variable/midlertidige grenser og kjøretøyets tillatte fart må ikke fylles med ubegrunnede tall (CAP-5, AC-12).

### NonFunctional Requirements

NFR1: Kun foreground opt-in; frosset profil og versjonsbinding; ingen ukvalifiserte tall eller gamle callbacks.
NFR2: Avgrenset offentlig vegsnapshot og kort RAM-vindu; ingen full kjørehistorikk, ekstern GPS-per-fix eller utvidet privat retensjon.
NFR3: Dag/natt, lesbar skiltforskjell, tekstalternativer og status som ikke bare uttrykkes med farge.
NFR4: Kilde-/objekt-/nettversjon, gyldighet, hash og avgrenset oppdatering må være etterprøvbar; kildeutfall gir konservativ status.

### Additional Requirements

Gjenbruk React/TypeScript–FastAPI–PostgreSQL. V1 ferdig og testet; V1.2/V1.3 implementert og kvalifisert før bygging. Tillegget trenger eksplisitt rettet geometri og detaljert→overordnet vegkobling; holdeplassorden er utilstrekkelig. Ingen ny tjeneste, global konfigurasjon, synlig kart, lyd, egenfartsavhengighet eller alarm. Starter/greenfield-template gjelder ikke.

### UX Design Requirements

UX-DR1: Stort aktuelt362-skilt og mindre neste362-skilt med tydelige etiketter og ca.-avstand.
UX-DR2: Ukjent aktuell og skjult kommende har egne årsaker; ingen gammel tallfallback.
UX-DR3: Ett varselpanel per passering, uten repeterende aktivering ved terskelpendling/gjenkomst; ingen lyd.
UX-DR4: Eksisterende dag/natt/tilgangs-/fokusregler beholdes; ingen interaksjon under kjøring kreves for vanlig nedtelling.

### FR Coverage Map

| Krav | Epic / stories | Verifikasjonsgrunnlag |
|---|---|---|
| FR1 | SL-E1 /1.2,1.3 | AC-01/12 |
| FR2 | SL-E1 /1.4,1.5 | AC-02–05/07/10 |
| FR3 | SL-E1 /1.4 | AC-05/06 |
| FR4 | SL-E1 /1.3,1.5 | AC-07/08 |
| FR5 | SL-E1 /1.3,1.4,1.6 | AC-09–11 |
| FR6 | SL-E1 /1.1,1.2,1.6,1.7 | AC-11/12 |
| NFR1 |1.1,1.3–1.6 | Generasjoner/profil/ingen gamle callbacks |
| NFR2 |1.1,1.3,1.6,1.7 | RAM-/requesttak og ingen kjørehistorikk |
| NFR3 |1.2,1.7 | Tema, lesbarhet og tekstalternativ |
| NFR4 |1.1,1.6 | Proveniens/atomisk snapshot/ferskhet |
| UX-DR1/2 |1.2,1.4 | Adskilte skilt og usikkerhetsårsaker |
| UX-DR3 |1.4,1.6 | Passeringsidentitet/gjenkomst uten ny aktivering |
| UX-DR4 |1.2,1.6,1.7 | Eksisterende tilgang/fokus, ingen kjøreinteraksjon |

[AC-01–12](../specs/spec-speed-limits/verification.md) er senere kontroller, ikke beståtte tester.

## Epic List

### Epic1 / SL-E1: Forstå registrert grense og neste endring på pilotkorridoren

Brukeren kan se aktuell vegfartsgrense og visuelt 300m-forvarsel med underbygget passering og ærlig usikkerhet på valgt Polaria–flyplass-korridor. **FRs covered:** FR1–FR6. **Capabilities:** CAP-1–5.

Én epic fordi data, matching, avstand og samme skiltpanel leverer ett sammenhengende brukerutfall. Å dele dem etter tekniske lag ville skape avhengige epics uten egen nytte. Planlagt sekvens er sju avgrensede stories. Tidligere firestory-skisse er splittet for å skille kildeberedskap, visning, matching, forvarsel, kryss, livssyklus og fysisk aksept. Hver story kan aksepteres innen sin uttrykkelige støtteflate uten å vente på senere story; første del-leveranse reduserer ikke epicens krav om begge visninger.

Eksterne porter: ferdig/testet V1 og implementert/kvalifisert V1.2/V1.3, valgt datert rutebinding, samt senere byggbestilling. Pågående datagap og fysisk GPS kvalifiseres i riktige stories; de blokkerer ikke utkastet. Planen kan ferdigstilles uten å erklære disse portene bestått. Ingen implementering er autorisert.


## Epic 1: Forstå registrert grense og neste endring på pilotkorridoren

**ID: SL-E1.** Samlet første leveranse er aktuell registrert vegfartsgrense og fast300m-forvarsel, begge med ærlig usikkerhet. Mellomleveranser er interne avgrensede demonstrasjoner og endrer ikke epicens omfang. Én epic beholdes fordi dette er ett sammenhengende brukerutfall; historiene nedenfor er gjennomførbare i rekkefølge uten avhengighet på senere stories.

**Felles før start:** G0 i [teknisk tillegg](../specs/spec-speed-limits/technical-addendum.md). Alle tester/bygging som omtales nedenfor er senere arbeid. Ingen story utvider omfanget til kart, lyd, egenfart, dynamisk varsel, alarm eller kjøretøyregelberegning. Alle bruker historisk grunnlag med oppdatert kildekontroll før faktisk bruk. Ingen automatisk produksjonsaktivering etter en bestått story.

### Story 1.1: Klargjør et etterprøvbart og avgrenset pilotgrunnlag

**ID:** SL-E1-S1. **Avhengighet:** G0; ingen annen story. **Krav:** FR6, NFR1/2/4. **Størrelse:** én adapter-/manifestleveranse; ingen matcher eller UI-ombygging.

Som pilotansvarlig vil jeg klargjøre en avgrenset korridor med synlig datastatus, slik at eksperimentet bare bruker områder det kan begrunne.

**Acceptance Criteria:**

**Given** SL-P1 og de45 historiske uttrekkene, **When** pilotgrunnlaget forberedes, **Then** en versjonert offentlig snapshotpakke binder hvert valgt intervall til kilde-ID/versjon, felt, gyldighet, CRS, lengde og hash, **And** ukjent metadata, restriksjoner og dekningskanter er eksplisitte.139segmenter/8656,655m er et kontrollgrunnlag, ikke en hardkodet sannhet ved nyere kildeversjon.

**Given** R2/R3 og felt1/3, **When** rutebindingen valideres, **Then** den avviser de korte baklengsbuene og bruker kvalifisert økende retning, **And** alle valgte detaljlenker har kontrollert superstedfesting og feltanvendelighet. Nodekontakt alene godkjenner ikke svingeforbud eller busstilgang. Ikke kvalifisert del markeres utilgjengelig; den kan ikke passere G1 for full korridor.

**Given** manglende, overlappende eller feltavhengige105-verdier, **When** dekningsrapporten lages, **Then** hull og reelle konflikter skiller seg fra to50-objekter for forskjellige felt, **And** MED/MOT på objektet tolkes i lys av katalog105, ikke som generell retningslov. Ingen standard50/80 fyller hull.

**Given** begrensningene i SL-LAB-1, **When** kilden feiler, pagination går i ring eller request-/byte-/objekttak nås, **Then** uthentingen stopper med eksplisitt ufullstendig status, **And** delvis data erstatter aldri et gyldig snapshot atomisk. Ingen råposisjon, privat arbeidsdag eller full kjøreplan sendes til NVDB.

**Given** endelig støttet delområde, **When** historien leveres, **Then** pakke og dekningsrapport kan inspiseres lokalt uten produkt-GPS, **And** et manifest med uløste obligatoriske datafelt kan bare være researchgrunnlag, ikke aktiv pilotpakke. G1s gjenværende avvik har eier og konkret kildekontroll; ingen senere story trengs for å akseptere korrekt blokkering.

### Story 1.2: Vis aktuell registrert grense og tydelig ukjent tilstand

**ID:** SL-E1-S2. **Avhengighet:**1.1. **Krav:** FR1/6, NFR3, UX-DR1/2/4, AC-01/12. **Størrelse:** eksisterende panel + offisielle assets + grenseevaluering fra kontraktsinput; ingen GPS-matcher.

Som sjåfør vil jeg se et forståelig aktuelt skilt eller en tydelig ukjent tilstand, slik at utdatert eller usikkert grunnlag ikke ser sikkert ut.

**Acceptance Criteria:**

**Given** kvalifisert RoadMatch-input for samme snapshot/kontekst og kjent verdi for hele intervallet, **When** panelet rendres, **Then** det viser originalt stort362-skilt med etiketten «Registrert vegfartsgrense», **And** kontraktsfiksturer dekker30/40/50/60/70. Uten kvalifisert input er live-visningen ukjent; en syntetisk demonstrasjon merkes og blandes ikke med privat aktivitet.

**Given** null, stale, feil generasjon, ukjent veg, grenseoverlapp eller kjent ukvalifisert midlertidig/variabel regulering, **When** ny status mottas, **Then** gammel tallverdi fjernes i samme oppdatering og årsaken vises med tekst, **And** en grånet gammel verdi er ikke fallback. Registrert veggrense omtales ikke som bussens samlede tillatte fart.

**Given** offisiell EPS-kilde/NLOD-spor, **When** ikonene tas inn, **Then** assetmanifestet for hver30/40/50/60/70-fil har originalURL, utgiver, hentetid/hash, lisens, attribusjon og eventuell teknisk konvertering, **And** standardproporsjoner/farger er kontrollert; uavklart SVG-rettighet blokkerer akkurat den asseten. Ingen KI-/egenprodusert erstatning.

**Given** dag/natt og eksisterende målskjerm, **When** skilt og ukjent vises, **Then** etiketter/tekstalternativer er forståelige, status er ikke bare farge og panelet følger eksisterende tilgang/fokusregler, **And** ingen ny interaksjon kreves under vanlig kjøring. Fysisk lesbarhet kvitteres separat i1.7.

### Story 1.3: Knytt flere målinger til aktuell veg på avgrensede hovedstrekk

**ID:** SL-E1-S3. **Avhengighet:**1.1–1.2. **Krav:** FR1/4/5, NFR1/2, AC-01/08/09. **Størrelse:** rettlinjet/lokalt sammenhengende matching på1109722/1109517, integrert med panelet; usikre kryss kan gi ukjent uten støtte fra1.5.

Som sjåfør vil jeg at aktuell grense bygger på flere målinger av faktisk veg, slik at en nærliggende veg eller et GPS-hopp ikke gir et feil skilt.

**Acceptance Criteria:**

**Given** én autorisert foreground-posisjonskilde og SL-LAB-1, **When** koherente tidsordnede målinger etablerer unik faktisk veg/retning, **Then** RoadMatch binder målet til rettet lenkeforekomst og begrunnet langsveg-usikkerhetsintervall, **And** panelet viser bare en grense som gjelder hele dette intervallet. Accuracy er et filter, ikke bevis på vegidentitet.

**Given** parallelle veger eller veger over/under hverandre med uavklarte kandidater, **When** nærmeste linje eller holdeplassrekkefølge foreslår én veg, **Then** aktuell forblir ukjent til uavhengig posisjons-/topologievidens skiller dem, **And** planlagt trasé tvinger aldri målinger til denne vegen. Samme tall på to ukjente vegkandidater kvalifiserer ikke vegidentiteten.

**Given** ut-av-rekkefølge-fikser, umulige overganger eller enkeltstående hopp, **When** de mottas, **Then** de kan ikke fremme posisjon/passering, **And** utilstrekkelig gjenværende belegg gir ukjent. Faktisk koherent avvik kan kvalifisere en annen veg med data; forventet videre veg oppheves.

**Given** stillstand med tidligere kvalifisert veg og ferske konsistente fikser, **When** heading mangler eller er gammel, **Then** tidligere underbygget tilknytning kan bevares uten ny retning, **And** manglende oppdateringer over5s gir foreldet status. Grensene5s/25m/sekvens3 over2s kontrolleres både på og rett utenfor terskel i senere syntetiske forløp.

**Given** løpende matching, **When** RAM-vinduet når30fikser/30s eller konteksten oppheves, **Then** data ryddes etter profilen, **And** ingen råfikser lagres i database, browserstorage, logger eller eksterne kall. Ingen ny skjult GPS-watch opprettes.

### Story 1.4: Vis fast300m-forvarsel og underbygg passering

**ID:** SL-E1-S4. **Avhengighet:**1.1–1.3. **Krav:** FR2/3/5, UX-DR1–3, AC-02–06. **Størrelse:** avstand/grense-state-machine + lite kommende panel på allerede kvalifiserte fremoverkjeder; ingen ny kryssklassifisering.

Som sjåfør vil jeg se neste grense og avstanden frem til den, slik at jeg kan forberede både reduksjon og økning uten at aktuell grense byttes for tidlig.

**Acceptance Criteria:**

**Given** unik kvalifisert fremoverkjede og gyldig grensedata, **When** avstandsintervallet går310–320→290–300→230–240m, **Then** kommende skilt er først skjult, aktiveres så og teller ned fra målingene, **And** både50→30 og50→70 følger samme gate. Luftlinje/holdeplassavstand/timer brukes ikke. Egen fart kan være null.

**Given** første sikre måling ved120m, **When** kjeden kvalifiseres, **Then** mindre skilt og ca.120m vises straks med separat etikett, **And** aktuell grense beholdes. Intervallet295–305m aktiverer ikke.

**Given**302/298/301/297m og deretter bevegelse over320m/gjenkomst, **When** målingene gjelder samme passering, **Then** det finnes høyst én aktivering; panel kan trekkes tilbake og komme igjen uten ny animasjon, **And** avstanden kan øke ved underbygget bevegelse bort. Fersk stillstand gir ingen klokkedrevet nedtelling.

**Given** usikkerhetsintervallet overlapper grensen, **When** passeringen vurderes, **Then** aktuell er ukjent og kommende nedtelling skjules, **And** først flere koherente målinger med hele intervallet på ny side og kvalifisert overgang gir ny aktuell. Enkelt GPS-hopp forbi gir ikke passering.

**Given** to endringer80m fra hverandre og en tredje med lik verdi som naboen, **When** første endring passeres sikkert, **Then** neste vises straks med korrekt restavstand, **And** like verdier gir ingen ekstra hendelse og ukjent mellomrom hoppes aldri over. Nøkkel skiller fysisk forekomst/passering fra snapshotrevisjon.

**Given** fremoversikt eller nestegrensedata forsvinner, **When** aktuell veg fortsatt er sikker, **Then** bare upcoming fjernes med årsak, **And** «Ingen registrert endring innen300m» brukes bare ved komplett kvalifisert horisont.

### Story 1.5: Bevar riktig vegvalg gjennom pilotens kryss og rundkjøringer

**ID:** SL-E1-S5. **Avhengighet:**1.1–1.4. **Krav:** FR2/4, AC-07/08/11. **Størrelse:** kvalifisering av de fire planlagte kryssene og deres relevante alternative armer; ingen generell landsdekkende ruter.

Som sjåfør vil jeg beholde sikker aktuell grense selv om neste avkjøring er usikker, slik at forvarselet ikke gjelder en veg jeg kanskje ikke kjører.

**Acceptance Criteria:**

**Given** sikker aktuell veg før en rundkjøring, **When** flere plausible videre armer gir forskjellige fremoverforløp, **Then** current kan bestå mens upcoming skjules med «Videre veg usikker», **And** valgt rutetrasé alene opphever ikke tvetydigheten. En felles kjede frem til endringen kan kvalifiseres selv om et senere vegvalg er uavklart.

**Given** den syntetiske AC-07-kjeden140+40+70m med kvalifisert arm, **When** avstand beregnes, **Then** resultatet er250m inklusive riktig bue, **And** feil arm eller parallelle/planskilt lenker uten forbindelse avvises. Kandidatene har selvstendig forventet vegvalg, ikke ruteplanen som fasit for faktisk posisjon.

**Given** R4-kildekjeden med200m før innkjøring og18,448m bue til70→50, **When** inn-/utarm er kvalifisert, **Then** avstanden er218,448m før visningsavrunding, **And** motsigende målinger trekker varselet tilbake. Kan armen ikke underbygges før innkjøring, er korrekt skjult varsel forventet; storyen lover ikke forhåndsvarsling gjennom enhver rundkjøring.

**Given** R1–R4 med registrerte felt og forbindelser, **When** hvert kontrollpunkt verifiseres syntetisk, **Then** rett arm, feil arm, stopp og gjenopptatt bevegelse får forventet separat current/upcoming-status, **And** R2-baklengs265,519m og R3-baklengsbuen er negative regresjonseksempler. Rundkjørings70 presenteres ikke som trygg anbefalt rundkjøringsfart.

**Given** endepunkt1138796 eller grense for alternativvegdekning, **When** brukeren fortsetter utenfor støttet geometri, **Then** data-/vegkvalifisering trekkes tilbake for berørt del, **And** systemet gir ingen «ingen endring»-garanti utenfor manifestet. Data for alle relevante alternativer må være med før matching der erklæres støttet.

### Story 1.6: Håndter avbrudd, gjenopptakelse og kildebytte uten gamle verdier

**ID:** SL-E1-S6. **Avhengighet:**1.1–1.5. **Krav:** FR5/6, NFR1/2/4, UX-DR3/4, AC-09–12. **Størrelse:** integrert livssyklus/versjonsskifte; gjenbruk allerede implementert opt-in/tilgangsstyring. Basal ugyldighetskontroll i tidligere stories skal allerede virke.

Som sjåfør vil jeg se ærlig status når posisjon eller grunnlag forsvinner, slik at gamle målinger og varsler ikke blir aktuelle igjen ved en feil.

**Acceptance Criteria:**

**Given** GPS-bortfall/tunnel og foreldet evidens, **When** ferskhetsgaten faller, **Then** berørte verdier fjernes uten blind tunnel-/fartsberegning, **And** bare tap av fremoversikt påvirker ikke ellers sikker aktuell grense.

**Given** Pause/Off, skjult side, tilgangstap eller byttet aktivitet, **When** en sen callback fra forrige generasjon kommer, **Then** den ignoreres og sensing starter ikke automatisk, **And** eksplisitt gjenopptakelse krever ny vegkvalifisering i gjeldende kontekst. Private data og kort fiksvindu følger eksisterende utløp/rydding.

**Given** kort pause etter vist varsel, **When** samme fysiske passering kvalifiseres igjen, **Then** panel kan returnere uten ny aktivering, **And** reload er ny økt uten påstått varig historikk. Snapshotrevisjon alene skaper ikke en ny passering.

**Given** kildeutfall, kontrollalder>24t, snapshotalder>7d, ugyldig kilde eller ukjent påkrevd tidsmetadata i laboratorieprofilen, **When** evaluator prøver å vise en verdi, **Then** kun fortsatt eksplisitt gyldig snapshot kan brukes innen grensene, ellers ukjent, **And** hentetid erstatter aldri original virkning/endringstid. Fysisk regulering kan fortsatt avvike selv innen disse grensene.

**Given** nytt snapshot med endret geometri/grense-ID, **When** det tas i bruk, **Then** hele pakken byttes atomisk med ny kvalifisering og uten versjonsblanding, **And** automatiske aktivitet-/stoppvalg, privat retensjon og andre utvidelser endres ikke. Senere kontroller dokumenterer at råposisjoner ikke kommer i nettverks-/logg-/persistensflater.

### Story 1.7: Avgjør om begge visningene er brukbare i den avgrensede piloten

**ID:** SL-E1-S7. **Avhengighet:**1.1–1.6, separat autorisasjon til fysisk test. **Krav:** FR1–6, NFR1–4, UX-DR1–4, AC-01–12. **Størrelse:** ett avgrenset pilot- og beslutningsopplegg; feilretting blir egne senere oppgaver, ikke ubegrenset arbeid i denne storyen.

Som pilotansvarlig vil jeg ha et dokumentert beslutningsgrunnlag fra faktisk enhet og veg, slik at registrert dekning og teoretisk300m ikke forveksles med trygg, fungerende støtte.

**Acceptance Criteria:**

**Given** alle tidligere story-resultater og uttrykkelig tillatelse til fysisk kontroll, **When** piloten klargjøres, **Then** faktisk skilting/retning/vegvalg, Polaria-arbeid, midlertidige/variable begrensninger og enhet/nettleser/HTTPS kontrolleres, **And** ukvalifiserte strekninger stenges i manifestet. Sjåføren skal ikke betjene testverktøy under kjøring; observatør/opplegg avklares før tur.

**Given** SL-LAB-1 som utgangspunkt, **When** fysisk akseptprotokoll fryses før kjøring, **Then** det finnes navngitt profil, kvalifisert feilmodell/kandidatseparasjon og eksplisitt akseptvindu rundt300m samt minste varseltilgjengelighet, **And** tallene er faglig begrunnet og godkjent for forsøket før resultater leses. Manglende kriterier gir «ikke klar», ikke bestått.

**Given** Polaria→flyplassrundkjøringen med R1–R4, **When** aktuelle grenser, økning/reduksjon, passering, kø/stopp, avvik og avbrudd vurderes, **Then** hvert kontrollpunkt får forventet/faktisk resultat og årsak uten full kjørehistorikk, **And** syntetiske tettliggende/hopp-scenarioer brukes der de ikke skal fremprovoseres i trafikken. Ingen faktisk farlig manøver er et testkrav.

**Given** feil aktuell grense, feil-arm-forvarsel eller for tidlig overgang, **When** avvik observeres, **Then** berørt støtte tas ut av piloten og registreres som ikke bestått, **And** det lages ingen samlet godkjenning som skjuler avvik. Sen/manglende varsling måles mot forhåndsvalgt protokoll, ikke tilpasses etter resultatet.

**Given** fullført avgrenset kontroll, **When** beslutningsrapporten leveres, **Then** den skiller bestått/ikke bestått/ikke testet per AC og strekning med enhets-/profil-/snapshotversjon, **And** ferdig epic krever begge visningene innen erklært støttet omfang. Motsatt retning, lyd, kart, egenfart/dynamisk varsel og alarm forblir utenfor. Rapporten kan konkludere med avslag; den gir ikke automatisk produksjonsgodkjenning.
