---
title: "Bussjåførassistent – revidert PRD for levert V1.0.1"
status: documentation-revision
approval: no-new-product-approval-implied
created: 2026-11-15
updated: 2026-11-15
product_baseline: v1.0.1
source_commit: 4d97c76ed7557793ce407c7f6cf6f2c269307475
feedback_date: 2026-11-12
revision_timing: after-completed-V1-and-published-v1.0.1
revises: prd-historical-before-feedback-2026-11-12.md
---

# Bussjåførassistent – revidert PRD for levert V1.0.1

> **REVISJON ETTER FERDIGSTILT V1 – 15. november 2026.** Dette dokumentet reviderer [original PRD, bevart som historisk fil](prd-historical-before-feedback-2026-11-12.md), som oppfølging av [faglærerens tilbakemelding 12. november](tilbakemelding-prd.md). Revisjonen ble skrevet **etter at V1 var ferdigstilt og V1.0.1 var publisert**. Den sammenfatter eksisterende beslutninger og levert funksjonalitet i ettertid; den var ikke kravgrunnlaget som forelå før implementeringen, og er ikke en ny produktrelease.

## 1. Formål, problem og tese

Sjåføren må samle skiftopplysninger, bussinformasjon og driftsmeldinger fra flere steder, blant annet Selfservice, SMS, NavCon og nettsider. Prosjekteieren anslo i [produktbriefen](../../briefs/brief-IBE160-2026-09-21/product-brief.md) 20–30 minutter informasjonsarbeid per åttetimers arbeidsdag; dette er et erfaringsanslag, ikke en målt referanseverdi. Tesen for den avgrensede leveransen er at kontrollert tekst-PDF-import, én samlet dagsoversikt og gjenbruk av manuelt registrerte avvik kan redusere gjentatt leting og gjøre planlagt arbeid lettere å gjennomgå. Verdien avhenger av at kontroll, retting og kildevedlikehold ikke oppveier besparelsen; faktisk tidsgevinst er ikke dokumentert.

Produktet er et privat, nettbrettilpasset nettsted med React/TypeScript, FastAPI og PostgreSQL. Det brukes til forberedelse og oppslag når sjåføren står stille. Det erstatter ikke offisielle instrukser, skilting eller driftskilder, registrerer ikke at kjøretøyet står stille og gir ikke sanntidsbasert kjøreveiledning.

Dette er en **separat dokumentasjonsrevisjon** etter [faglærerens tilbakemelding](tilbakemelding-prd.md). Den samler vedtatt omfang og implementert atferd; den innfører ikke nye produktkrav. [Original PRD i historisk fil](prd-historical-before-feedback-2026-11-12.md), [addendum](addendum.md), tidligere planer og godkjente refleksjonstekster er uendret. Den gamle `prd.md`-adressen har fått et lesernotat som markerer historisk status, mens den tidligere kravteksten og avsnittslenkene er bevart. Krav-ID-ene beholdes. Endringshistorikk, kilderegister og punktvis vurdering står i [revisjonsgjennomgangen](prd-revision-review-2026-11-15.md).

## 2. Versjonsgrense og levert omfang

| Nivå | Innhold og verifisert status |
|---|---|
| Opprinnelig plan, september | Større V1 med blant annet automatisk innhenting, GPS/progresjon, offlinebruk, fadder/instruktørflyt og rapporteksport. Åtte epics og 80 stories var planlegging, ikke levert funksjonalitet. [Arkiv](../../archive/pre-scope-02-2026-10-19/README.md). |
| Avgrenset og akseptert applikasjon | SCOPE-02 ble vedtatt 19. oktober. Fire epics og 20 stories; senere D1–D3/Epic12 og personlig aksept er dokumentert 29. oktober. Kjerne: tekst-PDF, gjennomgang/retting, eksplisitt lagring/bekreftelse, fysisk buss, manuell aktivitetsvalg/status, manuelt avviksregister og oppsummering. |
| Levert V1.0.0 og V1.0.1 | Ubuntu-integrasjonen ble inkludert i V1 ved eierbeslutningen 31. oktober. V1.0.1 er vedlikeholdsleveransen på commit `15011042b1fe093becbe68177e6396e456b1f35f`, publisert 4. november norsk tid. Driftsrettelser og O3–O6-oppfølging kommer i tillegg til den aksepterte kjernen; passordutvidelsen er ikke inkludert. [Release](https://github.com/IBE160-2026/G06-oisund/releases/tag/v1.0.1), [vedlikeholdsrapport](../../../../docs/evidence/v1.0.1-maintenance-20261104.md). |
| Arbeid mot V1.1.0 | Passordendring og administrativ gjenoppretting er implementert og teknisk kvalifisert på den separate passordgrenen. Praktiske eierprøver er delvis utført; ny kodeoverlevering/innløsning, full SSH/helper-kjede og endelig aksept er ikke sluttført i det undersøkte grunnlaget. Ingen V1.1.0-release er dokumentert. Se §11. |
| Senere ønsker og egne planer | Automatisk avvikshenting, fullt rutenett, posisjonsprogresjon, fartsgrenser og GPS-fart har egne planleggingsgrener. Automatisk avvikshenting står fortsatt som planlegging i undersøkt GitHub-gren; det er ikke dokumentert som levert eller som implementert del av V1.1.0. Øvrige utsatte funksjoner står i §9. |

Den siste driftsrapporten oppgir produksjon på `7921eb54e4816aaab9368c3efd851bcf692f3823`, med samme app-, container- og deploygrunnlag som V1.0.1. Dette er **siste dokumenterte driftstilstand**, ikke en ny inspeksjon av serveren 15. november. Nyere GitHub-main `4d97c76` legger til faglærerens PRD-tilbakemelding og teknologireferanse; det er ikke en ny apprelease.

To bruksmiljøer inngår: privat drift på den dokumenterte Ubuntu-løsningen, og selvstendig lokal vurdering med faktisk frontend/API/PostgreSQL, syntetiske data og generert innlogging. Lokal vurdering krever ikke produksjonsserver, Cloudflare-tilgang, private skiftfiler, GPS eller betalte kontoer. Installasjon kan kreve nedlasting av avhengigheter. En separat minnedemo erstatter ikke fullstackbevis.

## 3. Begreper og støttet input

| Term brukt her | Presis betydning og kobling til implementasjonen |
|---|---|
| Arbeidsdag (Workday) | Det lagrede arbeidsgrunnlaget for ett skift, med tjenestedato, aktiviteter og levetid. Kan inneholde pauser og flere arbeidsperioder; ikke nødvendigvis én kalenderdato. |
| Tjenestedato (Service date) | Datoen skiftet/tjenesten tilhører. Skilles fra kalenderdatoen til en aktivitet etter midnatt. |
| Aktivitet (Activity) | Identifiserbar post, for eksempel passasjertur, pause, tomkjøring, bussbytte eller transport. ID skiller også turer på samme linje fra hverandre. Ukjent type beholdes som råkode til den er avklart. |
| Plan (Plan) | Ordnet aktivitetsinnhold med tider og kjente steder. Utkast gjennomgås og lagres før eksplisitt bekreftelse; bekreftelse starter ikke automatisk arbeidsdagen. |
| Utkast (Draft) | Ubekreftet forslag fra import eller manuell registrering. Et importresultat i nettleseren er ikke et serverlagret utkast før eksplisitt lagring. |
| Fysisk buss (Bus) | Kjøretøy sjåføren faktisk oppgir. Utledes ikke fra vognløp eller tur. |
| Vognløp (Vehicle duty) | Kildens drifts-/vognløpsidentifikator, ofte kalt «Vogn» i PDF-en. Implementasjonen kan avlede de tre siste numeriske sifrene som sanntidsvognløp; det er ikke et sanntidsoppslag eller et fysisk bussnummer. |
| Avvik (Notice) | Én kontoeid, manuelt registrert kildeopplysning med linjeomfang og sluttdato. «Incident» og «record» i eldre dokumenter er ikke egne brukerbegreper her. |
| Manuell aktivitetsstatus (Outcome) | Eksplisitt registrert fullført, hoppet over eller avbrutt. Uten registrering er status ukjent. Ikke uavhengig bekreftet utført arbeid. |
| Oppsummering (Recap) | Skrivebeskyttet oversikt etter avslutning/avbrudd med planlagt innhold og manuell/ukjent status. |
| Kildekontroll | Egen handling som registrerer at brukeren har kontrollert avviket. Skilles fra registrering, redigering, kildeoppdateringstid og avvikets gyldighet. |
| Støttet tekst-PDF | Den kvalifiserte, selekterbare tekstbaserte skiftlayouten med gjenkjennelig topptekst, to innholdskolonner og støttede aktivitets-/turrader. At en PDF inneholder tekst er alene ikke tilstrekkelig. |

**Inputgrense:** høyst 10 MiB, 20 sider og 2 MiB uttrekk fra parserprosessen; parseren har en 30-sekunders grense. Skannede/bildebaserte, krypterte, ugyldige eller ukjente layouter får feil-/manuellrute. Privatimporten avviser dessuten ukvalifiserte kalenderforhold, blant annet utvidet starttime i skifthodet og intervaller som krysser den kontrollerte sommertidsgrensen. Dette følger `private_import.py::interpret`; generell støtte for manuell Oslo-tidsregistrering betyr ikke at alle tilsvarende PDF-er kan importeres.

Innen støttet input beholdes kjente kildefakta og usikkerhet. Retning, ukjente koder og manglende opplysninger skal ikke fylles med gjetning. Den fiktive vurderingen bruker Testskift A–E og en separat skrevet JSON-fasit. Eldre anonymiserte eksempler har egen kvalifikasjon, inkludert delvis støttede resultater. Manuell komplettering er aldri et automatisk uttrekkspass. Se [inputbeskrivelse](../../../../docs/submission/supported-input.md), [parser](../../../../backend/app/pdf_import.py), [privatimport](../../../../backend/app/private_import.py) og [fasit](../../../../Eksempelfiler/Fasit-testskift.json).

## 4. Brukerreiser

**UJ-1 – Alex, privat sjåfør (pseudonym).** Alex logger inn før bruk og laster opp en støttet tekst-PDF eller oppretter et manuelt utkast. Importen vises som ubekreftet; Alex gjennomgår fakta, retter ved behov og lagrer eksplisitt. En korrekt import krever ikke obligatorisk redigering. Usikkerhet og nødvendige valg håndteres før Alex bekrefter den gjennomgåtte, lagrede revisjonen. Et nytt dokument erstatter ikke en tidligere bekreftet plan.

Alex oppgir fysisk buss uavhengig av vognløp, åpner dagsoversikten og sjekker manuelt registrerte avvik mot kilden. Alex velger aktivitet når det passer mens kjøretøyet står stille. Valg, klokkeslett og sidebytte starter eller fullfører ikke arbeid; start og manuell aktivitetsstatus er egne handlinger. Ved lagringsfeil beholdes forslaget mens siden og autorisasjonen består. Ved ukjent svar sjekkes den opprinnelige operasjonen; ved revisjonskonflikt må Alex hente serverens tilstand. Etter eksplisitt slutt/avbrudd vises skrivebeskyttet oppsummering; uregistrert arbeid er fortsatt ukjent. Ved utløpt tilgang må Alex logge inn igjen, og ved utløpt datafrist kan arbeidsdagen ikke gjenåpnes.

**UJ-2 – Kim, faglig vurderer (pseudonym).** Kim følger README i valgt checkout og starter isolert frontend/API/PostgreSQL med syntetiske data og generert innlogging. Kim prøver en korrekt import, et rettet utkast og avvist input, og kontrollerer lagring/gjenåpning, manuell navigering, avvik og avslutning. Feil-/gjenopprettingsscenarier kjøres i vurderingsmiljøet. Reset gjelder bare den eksplisitt valgte fiktive konteksten. Kim trenger ikke eierens konto, server eller private dokumenter; GPS og livekilder inngår ikke.

## 5. Funksjonelle krav med testbare konsekvenser

Kriteriene nedenfor konkretiserer eksisterende FR-er. «Gitt/når/så» er lesbare kontrollkriterier, **ikke påstander om nye testkjøringer**. §8 kobler dem til eksisterende tester og datert evidens. Felles regler i §6 gjelder alle relevante krav.

### FR-1 – Privat tilgang (UJ-1, UJ-2)

- Gitt en opprettet privat konto, når innlogging lykkes, så gis en serverøkt med fast utløp 14 dager etter autentisering. Bruk forlenger ikke fristen, og utløp krever ny innlogging også under en aktiv arbeidsdag.
- Gitt utlogging, utløpt økt, feil eier eller utløpte data, når en privat operasjon forsøkes, så avvises den etter gjeldende tilgangskontroll. Privat visning ryddes ved kjent utlogging/øktutløp; demo gir ikke tilgang til privat innhold. Ingen offentlig registrering inngår.

### FR-2 – Import, gjennomgang og feil (UJ-1, UJ-2)

- **FR-2a:** Gitt en støttet fixture og uavhengig fasit, når PDF-en importeres, så viser resultatet de forventede kjente turene/aktivitetene og kildeopplysningene, med usikkerhet bevart. Resultatet er ubekreftet og ikke lagret ved bare filvalg.
- **FR-2b:** Gitt et resultat med feil/manglende aktivitet, når Alex velger retting, legger til det manglende og lagrer, så kan den korrigerte revisjonen gjennomgås og bekreftes eksplisitt. Originale strukturerte kildefakta beholdes for sammenligning; en korrekt import kan gå videre uten redigeringsrunden.
- **FR-2c:** Gitt skannet/ikke støttet input, avbrudd eller parserfeil, når importen ikke kan fullføres, så vises en feil med manuell alternativrute, uten «vellykket uttrekk». Forrige bekreftede plan endres ikke, og originalen arkiveres ikke.

### FR-4 – Redigerbart utkast (UJ-1, UJ-2)

- Gitt et utkast, når Alex retter type, dato/tid eller kjent sted og legger til, fjerner eller ordner aktiviteter, så lagres bare den uttrykkelig valgte revisjonen; manglende kildefakta fylles ikke automatisk.
- Gitt en uavklart nødvendig tid/type, når bekreftelse forsøkes, så må problemet avklares. En ukjent råkode blir ikke stille til en støttet aktivitetstype. Manglende ikke-essensielle fakta håndteres med de eksplisitte valgene som §6 beskriver.

### FR-5 – Dagsoversikt og fysisk buss (UJ-1, UJ-2)

- Gitt en bekreftet plan med flere arbeidsperioder, når oversikten åpnes, så vises rapporteringstid, ordnede aktiviteter, kjente steder og overganger uten å dikte opp aktivitet i mellomrommene.
- Gitt et vognløp fra PDF-en, når fysisk buss oppgis/endres og lagres, så behandles den som egen opplysning. Gjenåpning viser lagret buss; endringen omskriver ikke PDF-ens opprinnelige vognløp.

### FR-6 – Manuelt aktivitetsvalg (UJ-1, UJ-2)

- Gitt to aktiviteter med samme linje, når én velges direkte eller med forrige/neste, så velges dens ID og tilhørende retning/dato, ikke vilkårlig linjematch.
- Gitt et kvittert valg, når siden gjenåpnes online med gyldig tilgang, så gjenfinnes serverlagret valg. Klokken eller posisjon velger ikke neste aktivitet.

### FR-10 – Manuelle overganger (UJ-1, UJ-2)

- Gitt første/siste aktivitet, når forrige/neste brukes ved grensen, så blir det ikke et oppdiktet nytt valg eller automatisk rundgang.
- Gitt en valgt tur, når neste aktivitet er pause, tomkjøring, bussbytte eller transport, så vises den valgte aktiviteten som planlagt. Ingen ankomstdeteksjon, ti-sekunders overgang eller automatisk returtur utløses.

### FR-11 – Eksplisitte handlinger (UJ-1, UJ-2)

- Gitt en bekreftet, ikke startet plan, når Alex bare velger aktivitet, så starter ikke skiftet og det registreres ingen utført aktivitet.
- Gitt en aktiv arbeidsdag, når Alex uttrykkelig lagrer manuell status, korrigerer buss eller avslutter, så følger bare den valgte handlingens endring. Sensedata bekrefter ikke handlingen eller at kjøretøyet står stille.

### FR-12 – Manuelt avviksregister og relevans (UJ-1, UJ-2)

- Gitt et nytt avvik, når det lagres, så kreves tittel, eksplisitt valgte linjer eller alle linjer, og en fremtidig sluttdato. Valgte linjer krever tagger; «alle» utledes ikke fra tekst.
- Gitt samme avvik for flere linjer/dager, når leseren åpnes, så brukes den ene kontoeide posten mot eksakte linjer og arbeidsdagens planlagte intervaller. Den vises én gang med samsvarende linjer; separate hendelser slås ikke sammen. Dette er ikke nøyaktig tur-/holdeplassmatching eller automatisk Svipper-dekning.

### FR-13 – Kildeopplysninger og kontrolltid (UJ-1, UJ-2)

- Gitt ukjent kildeoppdateringstid, når avviket vises, så merkes den ukjent. Registreringstid og sist kildekontroll vises separat og brukes ikke som erstatning for kildens tidspunkt.
- Gitt et registrert avvik, når det bare leses eller redigeres, så blir det ikke kildekontrollert av den grunn. Kjente HTTP(S)-kildelenker er tilgjengelige; beskrivelse/SMS kan være kildegrunnlag uten lenke.

### FR-14 – Gjenbruk, avslutning og historikk (UJ-1, UJ-2)

- Gitt et gyldig kontoeid avvik, når den opprinnelige arbeidsdagen avsluttes, slettes eller utløper, så beholdes avvikets uavhengige gyldighet for andre relevante dager.
- Gitt registrert sluttdato eller tidligere manuell avslutning, når den effektive slutten nås, så går avviket ut av den aktive leseren og blir skrivebeskyttet historikk innen sin lagringsfrist. Dette bekrefter ikke at veien er åpnet.
- Gitt et fortsatt aktivt avvik, når en forlengelse godtas før eksisterende frist, så gjelder den nye slutten. Et allerede utløpt/manuelt avsluttet avvik kan ikke gjenopplives. Dato uten klokkeslett betyr slutten av valgt Oslo-dato og merkes slik.

### FR-16 – Ingen påkrevd betjening under kjøring (UJ-1, UJ-2)

- Gitt at Alex lar visningen stå urørt gjennom en planlagt tidsgrense, når tiden passerer, så kreves ingen tidsstyrt bekreftelse for å dokumentere ankomst/progresjon; systemet antar heller ikke utført arbeid.
- Gitt at brukeren senere står stille, når manuelle handlinger utføres, så brukes de vanlige kontrollene. Det finnes ingen GPS-/hastighetsstyrt lås, opplåsingsunntak eller test som beviser faktisk stillstand. Dette er en bruksgrense, ikke en dokumentert sikkerhetseffekt.

### FR-17 – Synlig lagringstilstand (UJ-1, UJ-2)

- Gitt endrede felt, når de ennå ikke er kvittert av serveren, så vises de som ulagret, under lagring eller uavklart. «Lagret» krever gyldig bekreftelse for den aktuelle operasjonen; et transportavbrudd betyr ikke automatisk at serveren avviste endringen.
- Gitt mislykket forespørsel med fortsatt gyldig økt og åpen side, når feilen vises, så beholdes forslaget for kontroll/gjenforsøk. Utilgjengelig tjeneste vises som utilgjengelig, ikke som vellykket tomt resultat. Ingen offline-lagring loves.

### FR-18 – Kvitteringsoppslag og samtidighet (UJ-1, UJ-2)

- Gitt en mulig akseptert operasjon med tapt svar, når gjenoppretting velges, så brukes den samme operasjonen og autorisert kvitteringsoppslag. Eventuelt nytt forsøk følger ny autorisasjon og gir ikke duplikat eller ny avslutningstid.
- Gitt to faner med ulike revisjoner, når den gamle fanen forsøker å skrive, så avvises foreldet revisjon eksplisitt; nyere serverinnhold overskrives ikke stille. Automatisk sammenslåing/tvungen overskriving inngår ikke.

### FR-19 – Tomt, utilgjengelig og ikke kontrollert er ulike tilstander (UJ-1, UJ-2)

- Gitt tilgjengelig register uten poster eller uten samsvar med valget, når leseren vises, så skilles «ingen lagrede avvik» fra «ingen samsvar». Ved tjenestefeil vises utilgjengelig; ingen av tilstandene betyr avviksfrie linjer.
- Gitt `checked_at` uten verdi, når posten vises, så står den som ikke kontrollert. Gitt `checked_revision < revision`, så står kontrollen som utført før siste endring. **Det finnes ingen aldersgrense i minutter/timer som automatisk gjør en kildekontroll «stale».** Lik revisjon viser sist kontrollert-tid, ikke garantert fersk kilde eller full dekning. Ukjent gyldighetsstart merkes som delvis kjent.

### FR-20 – Gjenåpning og ulagret innhold (UJ-1, UJ-2)

- Gitt kvittert servertilstand og fortsatt tilgang/levetid, når en arbeidsdag gjenåpnes online, så gjenfinnes plan, fysisk buss, valg og manuelle statuser.
- Gitt ulagrede forslag på åpen side, når en forespørsel feiler, så beholdes forslagene under fortsatt autorisasjon og det varsles ved unngåelig navigering som vil miste dem. Lukking, omlasting eller tap av tilgang kan miste ulagret innhold; ingen privat persistent nettleserbuffer eller offline-gjenstart inngår.

### FR-21 – Terminal avslutning (UJ-1, UJ-2)

- Gitt en aktiv arbeidsdag, når slutt/avbrudd velges og deretter avbrytes i bekreftelsen, så forblir dagen åpen. Først bekreftet avslutning lagres terminalt.
- Gitt en allerede avsluttet dag, når en operasjon gjentas, så endres ikke sluttid eller gjenværende ukjente aktivitetsstatuser. Dagen kan ikke startes igjen, og ingen depotankomst utledes.

### FR-22 – Oppsummering (UJ-1, UJ-2)

- Gitt avsluttet/avbrutt dag med ukjente og manuelt registrerte statuser, når oppsummeringen vises, så skilles disse fra hverandre og fra planlagte tider.
- Gitt terminal tilstand, når oppsummeringen åpnes, så er den skrivebeskyttet. Retting av utfall skjer før avslutning; ingen etterredigering, sjåførpoeng eller rapporteksport inngår.

### FR-24 – Avgrenset datalivsløp (UJ-1, UJ-2)

- Gitt en import som lykkes, feiler eller avbrytes, når behandlingen er avsluttet, så beholdes ikke PDF-originalen som arkiv. Bare eksplisitt lagrede strukturerte felt/kildemetadata og rettinger inngår; privatimport filtrerer bort sjåførfeltet i toppteksten før lagring.
- Gitt utløpt frist etter §6, når data eller operasjonskvittering etterspørres eller et gammelt forsøk gjentas, så nektes tilgang og utløpte data gjenopprettes ikke. Serveropprydding skjer ved oppstart og minst hver time under drift.
- Gitt gjenåpning, lesing, innlogging eller retry, når levetiden vurderes, så nullstilles ikke lagringsfristen. Avvik har egen frist uavhengig av arbeidsdagen. Driftsbackup har den særskilte bevisgrensen i §6; dette er ikke løfte om fysisk sletting av alle kopier.

### FR-25 – Reproduserbar lokal vurdering (UJ-2)

- Gitt riktig README og isolert vurderingsoppsett, når Kim følger oppskriften, så kan faktisk frontend/API/PostgreSQL brukes med generert innlogging, fiktive data og støttede import-/feilscenarier uten private produksjonsdata.
- Gitt reset eller test av persistens/gjenstart, når den utføres i valgt vurderingsmiljø, så er fiktiv kontekst avgrenset fra privat drift. En separat minnedemo teller ikke som bevis for databasepersistens.

## 6. Felles regler for bekreftelse, tid og data

**Bekreftelse:** Krev tjenestedato, eksplisitte kalenderinstanser som fastsetter planlagt siste slutt, ordnede aktiviteter og avklaring av nødvendige typer/tider. Passasjerturens linje/retning/destinasjon håndteres med gjennomgåtte fakta eller eksplisitt anerkjent manglende ikke-essensiell informasjon, ikke oppdiktede verdier. Bekreftelsen gjelder gjennomgått, lagret revisjon, ikke senere usette endringer. En ny import/et nytt utkast erstatter aldri eksisterende bekreftet/aktiv dag. Etter aktivering er planstrukturen fast i denne versjonen; buss, aktivitetsvalg og manuell status er egne skrivbare opplysninger.

**Tid:** Bruk Europe/Oslo med tjenestedato og kalenderdato adskilt. Bevar kildens utvidede klokkeslett når støttet og løs kalenderen bare fra eksplisitt, kvalifisert grunnlag. Fredagens 25:30 blir ikke en lørdagstjeneste bare fordi tidspunktet er lørdag 01:30. Manuell registrering avviser ikke-eksisterende vårklokkeslett og krever forekomst ved dobbelt høstklokkeslett. Klokkerekkefølge alene er ikke tilstrekkelig til å gjette neste dato. Privatimportens snevrere kalendergrense i §3 gjelder fortsatt.

**Arbeidsdagens frist:** Ubekreftet serverlagret utkast utløper sju dager etter opprettelse. Bekreftet plan har en fast maksimumsfrist lik bekreftet planlagt siste slutt pluss sju dager. Ved serverbekreftet slutt/avbrudd brukes den tidligste av denne maksimumsfristen og faktisk slutt/avbrudd pluss sju dager. Serverens UTC-tid bestemmer tilgangsfristen, og terminal avslutning og frist lagres i samme transaksjon. Utløp er ikke fullført arbeid.

**Avvikets frist:** Kontoeid avvik og ny kommandometadata utløper sju dager etter effektiv avslutning, altså registrert sluttdato eller tidligere manuell avslutning. Dagens sletting styrer ikke denne fristen. Eldre poster uten sluttdato beholder sin eksisterende lagringsgrense til eksplisitt komplettering og blir ikke automatisk aktuelle avvik. Engangshåndteringen av allerede avsluttede eldre poster er dokumentert i 11.5-migrasjonen; den er ikke en generell fristforlengelse.

**Privat lagring:** Private svar er `no-store`; det brukes ikke privat persistent nettleserlager eller service worker. Ingen råtekst-/OCR-originalarkiv eller permanente sjåførhistorikker inngår i applikasjonen. At sjåførfeltet filtreres bort anonymiserer ikke kontokoblede skift eller fritekst. Tilgangskontroll i appen beskytter ikke mot full kontroll over database/server.

**Driftsbackup:** Ubuntu-integrasjonen inkluderer faktisk backup og isolert restore. Den eldre PRD-ens formulering «No historical private backups» beskriver derfor ikke hele levert drift. [Driftsguiden](../../../../docs/ubuntu-server.md) beskriver Windows-kopier med 48 timers oppbevaring ryddet ved neste vellykkede kjøring; det er ikke en absolutt slettefrist mens maskinen er avslått. Backup kan inneholde senere slettede rader, og opprydding/utløpsregler må håndteres før ekstern åpning etter restore. Godkjent [refleksjon](../../../../docs/submission/ai-reflection.md) skiller allerede aktiv database fra backup. Denne revisjonen dokumenterer skillet, ikke en ny backuppolicy eller påstand om sletting fra alle kopier.

## 7. Kvalitetskrav

| ID | Krav og etterprøvbar avgrensning |
|---|---|
| NFR-1 | Nettbrett/PC, merkede kontroller, tastatur, tekstforstørring, synlig fokus og manuell Dag/Natt. Informativ tekst minst 4,5:1; nødvendig ikke-tekst minst 3:1. Fokusareal tilsvarende 2 CSS-pikslers perimeter, 3:1 endring/tilstøtende kontrast etter IR-01, ikke helt skjult. Ingen mening bare gjennom farge. Kontroller faktiske tilstander, ikke bare fargepaletten. |
| NFR-2 | Planlagt, manuelt registrert, ukjent, utilgjengelig og fiktivt er ulike tilstander. Verken metadata, beliggenhet, fullføring eller kildedekning diktes opp. FR-19 gir den konkrete kontroll-/revisjonssemantikken. |
| NFR-3 | Serverbasert eierkontroll, isolasjon av demo, kortvarig originalbehandling, fast applikasjonsretensjon og anonymiserte/syntetiske publiserte eksempler. Backupgrensen i §6 må ikke skjules. |
| NFR-4 | Faktisk nettleseratferd, server-/databasegjenstart og fysisk nettbrett/PC vurderes med hver sin evidens. Viewporttest er ikke automatisk fysisk enhetsaksept eller full tilgjengelighetsrevisjon. |

## 8. Målemål, motmåling og akseptanse

SM-ID-ene kommer fra [september-PRD §9](../../archive/pre-scope-02-2026-10-19/prds/prd-IBE160-2026-09-21/prd.md.txt) og senere SCOPE-02-tilpasning i [vurdert PRD §8](prd.md#8-acceptance-and-benefit-evidence). Ingen ny målt verdi, obligatorisk feltstudie eller beståttgrense er lagt til.

| ID | Gjeldende betydning / mål | FR og evidensstatus |
|---|---|---|
| SM-1 | Hypotese: samlet informasjonsarbeid mot 10–15 minutter per dag, sammenlignet med erfaringsanslaget 20–30 minutter. Inkluder appbruk, retting, manuell avviksregistrering og kontroll av originalkilder. | FR-2/4/5/12–14. **Ikke målt i felt**; ikke et V1-akseptansepass. |
| SM-2 | Langsiktig hypotese: ingen oversette relevante planlagte avvik i evaluerte tilfeller mot kildegrunnlag. Tilfeller uten relevante avvik beviser ikke dekning. Manuell registrering avgrenser dagens løsning. | FR-12–14/19. Filtrering er testet, **reell kilde-/avviksdekning er ikke bevist**. |
| SM-3 | Etter SCOPE-02: korrekt manuelt aktivitetsvalg, også samme linje/motsatt retning og midnatt; ingen implisitt fullføring. Den tidligere GPS-/meterindikatoren er utsatt med GPS-funksjonene. | FR-6/10/11; AC-03 har funksjonell evidens. Ingen posisjonspresisjon er målt. |
| SM-4 | Etter SCOPE-02: import, retting, eksplisitt bekreftelse og reell fullstack lagring/gjenåpning/avslutning. Tidligere automatisk innhenting/offline/PDF-eksport inngår ikke i dette V1-målet. | FR-2/4/5/17/18/20–22/24; AC-01/02/06–09/11. Dokumenterte syntetiske og avgrensede faktiske tester; ingen generell feltgevinst. |
| SM-5 | Vurderer kan gjenta PC-flyt og feil med fiktive data uten privat skiftgrunnlag/GPS. | FR-25; AC-11/12 og ren reproduksjon dokumentert. Dette beviser ikke at faglæreren faktisk har gjennomført vurderingen. |
| SM-C1 | Eksisterende motmåling for betjeningsbelastning: ikke skjul manuelle inngrep/forvirrende overganger for å vise lavere søketid, og ikke oppnå gevinst gjennom betjening under kjøring. For nåværende importflyt er antall manuelle PDF-rettinger relevant å rapportere som del av dette, sammen med tidsbruken. | FR-2/4/16. 12.4 dokumenterer konkret brukerfriksjon og retting, men ingen samlet feltserie eller vedtatt maksimum for rettinger. Ingen ny automatisk målefunksjon innføres. |
| SM-C2 | Eksisterende motmåling for tillit: tell irrelevante avvik, feilaktig ferskhetsinntrykk, skjulte bortfall og uriktig fullføringsstatus ved senere evaluering, ikke bare spart tid. | FR-11/13/17–19/21/22. Konstruerte feilscenarier har testdekning; hyppighet i faktisk arbeid er ikke målt. |

Faglærerens eksempel bruker SM-C1 om PDF-rettinger. Her beholdes eksisterende SM-C1-identitet og rettinger knyttes til dens manuelle inngrep, slik at tidligere målehistorikk ikke får en ny betydning uten forklaring.

| Akseptanse | Konkret kontroll og krav | Eksisterende kilde/test/evidens |
|---|---|---|
| AC-01 | Uttrekk mot uavhengig fasit, støttet/delvis/avvist separat. FR-2. | `backend/tests/test_pdf_import.py`, [9.1-kvalifikasjon](../../../../docs/evidence/9-1-import-qualification.md), [syntetisk A–E/12.4](../../../../docs/evidence/12-4-import-experience.md). Historiske anonymiserte og nye syntetiske grunnlag holdes atskilt. |
| AC-02 | Rett tid, manglende pause, vognløp/fysisk buss og lagret oversikt. FR-4/5. | `test_private_drafts.py`, `test_private_bus.py`, `frontend/tests/shift-preparation.spec.ts`; 12.4 og C1-evidens. |
| AC-03 | Linje/retning/dato, aktivitetsgrenser og ingen automatisk fullføring. FR-6/10/11/16. | `frontend/tests/private-selection.spec.ts`, `private-selected-activity.spec.ts`, `private-outcomes.spec.ts`. |
| AC-04 | Ett kontoeid avvik, flere linjer/dager, eksakt linje-/intervallfilter og kjent/ukjent metadata. FR-12/13. | `backend/app/notice_reader_domain.py`, `backend/tests/test_notice_reader.py`, [11.5-leser](../../../../docs/evidence/11-5-line-date-notices.md). |
| AC-05 | Slutt/forlengelse, ikke-gjenoppliving, historikk og kontrolltilstander. FR-14/19. | `test_account_notices.py`, `frontend/tests/private-notice-reader.spec.ts`, [11.5-register](../../../../docs/evidence/11-5-crossday-register.md). |
| AC-06 | Avvist/avbrutt import bevarer bekreftet plan og frigjør behandlingen. FR-2/24. | `test_pdf_import.py`, `test_private_import.py`, `frontend/tests/private-import.spec.ts`, [mobilretting](../../../../docs/evidence/mobile-pdf-upload.md). |
| AC-07 | Feil, revisjonskonflikt og tapt svar uten duplikat/stille overskriving. FR-17/18/20. | `test_private_drafts.py`, `test_private_selection.py`, `frontend/src/recoverOperation.ts`, `frontend/tests/private-recovery.spec.ts`, [11.6](../../../../docs/evidence/11-6-server-recovery.md). |
| AC-08 | Avbryt bekreftelse, slutt/avbrudd én gang, ukjent forblir ukjent. FR-21/22. | `test_private_outcomes.py`, `frontend/tests/private-outcomes.spec.ts`, [11.3](../../../../docs/evidence/11-3-outcomes-and-close.md). |
| AC-09 | Eier-/øktkontroll, logout/cache, utløp, opprydding og ingen gjenoppliving. FR-1/24. | `test_private_access.py`, `test_retained_data.py`, `test_private_drafts.py`, [12.1](../../../../docs/evidence/12-1-retained-data.md). Kontrollert utløp er ikke en naturlig sjudagers feltprøve. |
| AC-10 | Faktiske inkluderte UI-tilstander, Dag/Natt, tastatur, kontrast/fokus og nettbrett/PC. NFR-1/4. | `frontend/tests/tablet-pc-private.spec.ts`, [fysisk 12.3](../../../../docs/evidence/12-3-device-acceptance-2026-10-27.md), [C1-aksept](../../../../docs/evidence/v1-acceptance-2026-10-29.md). |
| AC-11 | Ren lokal README, ekte API/PostgreSQL, gjenåpning/gjenstart og isolert reset. FR-25/NFR-4. | `frontend/submission-tests/journey.spec.ts`, `backend/tests/test_submission_safety.py`, [12.5](../../../../docs/evidence/12-5-reproduction.md), C1 og [sluttkontroll](../../../../docs/evidence/v1-final-control-20261031.md). |
| AC-12 | Krav → story → test → faktisk resultat/versjonsgrense samt KI-refleksjon. | [Sporbarhetsmatrise](../../../../docs/submission/traceability.md), [godkjent refleksjon](../../../../docs/submission/ai-reflection.md), denne revisjonen og tilhørende gjennomgang. |

Tabellen samler kontrollgrunnlaget, men endrer ikke historiske tester. Resultatene er knyttet til sine opprinnelige builds; testantall overlapper og skal ikke summeres til ett dekningsmål. Det ble ikke kjørt app-, produksjons- eller feltprøver som del av denne dokumentasjonsrevisjonen.

## 9. Utsatte krav, ikke-mål og kapasitet

| Bevart FR-ID | Utsatt funksjon |
|---|---|
| FR-3 | Ekstern rutetabellanriking. Registrerte datoer, linje, retning og endepunkter beholdes uten å produsere et hentet rutenett. |
| FR-7 | Trestoppvisning/holdeplassbasert kjørevisning. |
| FR-8 | GPS-basert holdeplassprogresjon og omkjøringsgjenfinning innen den gamle FR-8-familien. |
| FR-9 | Manuelle holdeplasskontroller som hører til den utsatte posisjons-/stoppløsningen; ikke dagens manuelle aktivitetsvalg. |
| FR-15 | Lydvarsler. |
| FR-23 | PDF-/CSV-eksport. Input-PDF-er og testbevis er ikke produktets eksportfunksjon. |

Andre ikke-mål i levert V1.0.1:

- OCR/bildeimport, direkte Selfservice-integrasjon og automatisk innhenting av driftsmeldinger.
- GPS/fartsgrense/fart, vær, møtende busser, ruteplanlegging eller KI i kjørende app.
- Bevegelseslås, automatiske overgangstimere, lyd, automatisk tema eller wake lock.
- Privat offlinepersistens, enhetsoverføring eller avansert revisjon av en aktiv plan.
- Fadder-/instruktørroller og vurderingsskjema. Dette dokumentet gjelder bussjåførassistenten.
- PDF-rapporteksport, sjåførpoeng, påkrevd tredagers feltstudie, full kilde-/sikkerhets-/tilgjengelighetssertifisering eller offentlig selvregistrering.

**Realismen i tidsestimatet:** 60–80 timer og minst 12 timer til retting/levering var eierens gjenværende planestimat ved SCOPE-02 19. oktober. Det er ikke et nytt estimat fra 15. november eller et verifisert faktisk timeforbruk. Innlogging, faste sesjoner, samtidighetsvern, avviksregister og inkludert Ubuntu-oppsett er nå implementert med separat evidens; de skal ikke fremstilles som gjenstående nyutvikling.

Den dokumenterte avgrensningen ved tidspress var å holde automatisering, GPS, offline, mentorroller og eksport utenfor kjernen og beskytte test-/leveransereserven. Tidlig PDF-feil skulle gi ny dokumentert omfangsbeslutning, ikke et falskt pass gjennom manuell inntasting. Ubuntu var først utsatt og senere uttrykkelig inkludert etter ferdigstillelse. Det finnes ikke kildegrunnlag for å finne på en ny rangert kuttliste blant allerede leverte funksjoner eller for å gjøre V1.1.0 til kurskrav. Ved senere kapasitetskonflikt er utvidelsene separate fra den leverte kjernen.

## 10. Antakelser og åpne spørsmål

### Antakelsesindeks

| ID | Antakelse og kilde | Hvordan den avgrenses |
|---|---|---|
| [ASSUMPTION] A-1 | 20–30 minutter daglig informasjonsarbeid, fra eierens anslag i briefen. | Ingen målt førverdi; kan ikke brukes som dokumentert gevinst i SM-1. |
| [ASSUMPTION] A-2 | Samlet oversikt med manuelle avvik er nyttig selv uten GPS/automatisk innhenting. Tese utledet fra briefen og SCOPE-02. | Brukeraksept av flyten finnes, men netto tidsgevinst/kildedekning er ikke undersøkt i felt. |
| [ASSUMPTION] A-3 | Historisk planleggingskapasitet 60–80 timer og forventet desemberinnlevering. | Ikke en bekreftet sluttdato, gjenstående kapasitet eller faktisk tidsregistrering i dag. |

### Åpne spørsmål og kjente bevisgrenser

Eierrollene nedenfor følger eksisterende ansvar: prosjekteier for kurs/produkt og driftsansvarlig for privat server. **Kalenderfrister er ikke fastsatt i kildene**; «før innlevering»/«før release» nedenfor er oppfølgingspunkt, ikke en oppdiktet avtale.

| ID | Konkret gjenstående spørsmål / status | Ansvar og fristgrunnlag |
|---|---|---|
| Q-1 | L1/L7: nøyaktig kursfrist, kanal/vedlegg, prosjekt-/solo-godkjenning, vurderers faktiske tilgang og innleveringskvittering er ikke verifisert i undersøkt dokumentasjon. | Prosjekteier, med faglærer for kursavklaring. Dato ikke dokumentert; avklares før komplett kursinnlevering. [Leveranseregister](../../../../docs/submission/delivery-readiness.md). |
| Q-2 | SM-1/SM-2 og motmålingene har ingen feltserie. Ingen netto tidsgevinst, full avviksdekning eller sikkerhetseffekt erklæres. | Prosjekteier dersom senere feltevaluering prioriteres. Ingen vedtatt frist eller V1-port. |
| Q-3 | O6: navngitte kernel-/bibliotek-/journalrester og langsiktig stabilitet har videre driftsoppfølging; vedlikehold, etterkontroll og avgrenset triage er utført. Firmware er særskilt utsatt. | Driftsansvarlig. Vilkår per funn i [O6-overleveringen](../../../../docs/evidence/o6-handover-20261103.md), ikke en ny generell ukesventetid eller releaseblokkering. |
| Q-4 | O4 er administrativt lukket, men uavhengig WAN-prøve, WAN-adressetype og ruterens IPv6-policy er ikke verifisert. | Bevisbegrensning under driftsansvarlig, ikke et gjenåpnet produktkrav eller påstått bestått test. Ingen ny frist. [O4-rapport](../../../../docs/evidence/o4-readonly-20261103.md). |
| Q-5 | Passordkandidatens resterende praktiske overleverings-/innløsnings-, SSH/helper- og eieraksept er ikke sluttført. Automatisk avvikshenting er fortsatt planlagt i undersøkt gren; ingen ny V1.1.0-forpliktelse utledes. | Prosjekteier/driftsansvarlig i separat utvidelse, før eventuell release etter kandidatens egne porter. Ingen dato dokumentert. §11. |
| Q-6 | Samlet faktisk timebruk er ikke dokumentert her. Om 60–80-timersestimatet holdt kan derfor ikke besvares med testresultater eller story-antall. | Prosjekteier dersom faktisk tidsbruk skal rapporteres. Ingen ny registreringsplikt/fristsatt produktoppgave. |

O3 betyr autentiserte eksterne skrive-/sesjons-/Origin-/CSRF- og nettbruddkontroller, og er fullført innen rapportert omfang. O5 gjelder terminerbart JWKS-/DNS-oppslag og er fullført, deployet og personlig testet. O4/O6 betyr henholdsvis nettverkseksponering/bevisgrense og bredere verts-/avhengighetsvedlikehold. Samlebegrepet «O3–O6 åpne» fra 31. oktober skal ikke brukes som dagens status. Ingen av de avgrensede resultatene er en uttømmende sikkerhetsgodkjenning.

## 11. V1.1.0 og senere arbeid – separat fra kravene over

Undersøkt passordgren er `codex/plan-password-management`, commit `29a77ff95cc7607b81c3351375771b6b23d2d1dd`. Den inkluderer vedlikeholdsgrunnlaget fra V1.0.1. `auth.py::change_password`, `password_recovery.py::redeem` og private API-ruter finnes på grenen. Status, faktisk kode og eierjournal støtter derfor **implementert kandidat**, ikke bare planlegging eller allerede utgitt produkt.

Den senere journalen dokumenterer beståtte PC-/nettbrettprøver av passordendring og avvisning av gamle økter, samt et konkret mislykket forsøk med for lang/tvetydig gjenopprettingskode. Etterpå er lesbart kodeformat og operatørens SENDT-flyt teknisk kvalifisert. Faktisk ny overlevering/innløsning, full SSH/helper-kjede og sluttaksept er fortsatt separate. Eldre «alle enhetsprøver venter»-formuleringer brukes derfor heller ikke som nåstatus.

Kilder på den faste grencommiten: [status](https://github.com/IBE160-2026/G06-oisund/blob/29a77ff95cc7607b81c3351375771b6b23d2d1dd/_bmad-output/experimental-extensions/password-management/implementation/status.md), [eierjournal](https://github.com/IBE160-2026/G06-oisund/blob/29a77ff95cc7607b81c3351375771b6b23d2d1dd/_bmad-output/experimental-extensions/password-management/implementation/owner-tests-20261104.md), [gjenopprettingsrutine](https://github.com/IBE160-2026/G06-oisund/blob/29a77ff95cc7607b81c3351375771b6b23d2d1dd/_bmad-output/experimental-extensions/password-management/implementation/restore-runbook.md).

Automatisk avvikshenting er undersøkt på `da867072a8a17249032c00efa51bd61979d41428`. [Grenens README](https://github.com/IBE160-2026/G06-oisund/blob/da867072a8a17249032c00efa51bd61979d41428/_bmad-output/experimental-extensions/automatic-notices/README.md) beskriver forsknings-/spesifikasjonsgrunnlag og én epic med fire stories, uttrykkelig uten implementasjon eller V1-aksept. Fullt rutenett, posisjonsprogresjon, fartsgrenser og GPS-fart forblir egne senere initiativer. De flyttes ikke inn i V1.0.1 eller V1.1.0 gjennom denne dokumentasjonen.
