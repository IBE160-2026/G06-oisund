---
id: SPEC-gps-speed
status: draft-for-owner-review
approval: not-approved-for-build
version_proposal: V1.4.5
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
created: 2026-10-27
companions:
  - measurement-and-behavior.md
  - verification.md
  - ../../research.md
  - ../../dependencies.md
sources: []
assumptions: [GS-A1, GS-A2]
open_questions: [P1, P2, GS-Q1, GS-Q2, GS-Q3]
---

# GPS-beregnet egen fart

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Dette er et planforslag, avledet med bmad-spec. SPEC og companions er samlet kontrakt; ingen kontroller av produkt eller enhet er bestått gjennom denne planleggingen.

## Why

Gi sjåføren en forståelig, rådgivende visning av egen fart sammen med registrert fartsgrense, uten å forveksle målt fart med vegens regel eller skjule måleusikkerhet. Egen fart skal også være nyttig når grensen er ukjent.

## Capabilities

- **CAP-1**
  - **intent:** Se kvalifisert egen fart i km/t og skille stillstand fra ukjent fart.
  - **success:** Fersk brukbar fart vises; null, manglende, ugyldig og gammel verdi gir «—». Rapportert reell 0 kan vises som 0; liten positiv fart som ville rundet til 0 vises «<1».
- **CAP-2**
  - **intent:** Forstå målingens begrensninger under varierende bevegelse.
  - **success:** Oppstart, akselerasjon, bremsing, kø, støy, uregelmessige intervaller, hopp og tidsfeil følger V01–V07 uten at gammel fart framstår som fersk.
- **CAP-3**
  - **intent:** Kontrollere posisjonsbruk og gjenoppta bevisst etter avbrudd.
  - **success:** Én delt kilde følger foreground opt-in, Pause/Off, tilgang, kontekst og generasjon. Sen callback eller synlig side alene gjenopptar ingenting; V08 består.
- **CAP-4**
  - **intent:** Lese fart og registrert grense som separate opplysninger på ulike strekninger.
  - **success:** Alle fire kjent/ukjent-kombinasjoner er tydelige; usikkert vegvalg skjuler ikke kvalifisert fart. V09–V12 bevarer gjenbruk og fast 300 m-forvarsel.

## Constraints

- Ferdig og testet godkjent V1 samt separat byggeautorisasjon før implementering. V1.4.5 er forslag.
- Bruk rapportert native speed gjennom én autorisert, delt posisjonskontroller; gjenbruk eksisterende frontend og private livssyklus. Avhengighetene i dependencies.md gjelder per forbruker.
- Ingen råposisjoner i logger, nettverksrapportering eller persistent lagring; ingen kjørehistorikk. Kun avgrenset RAM og rydding ved avbrudd.
- Ukjent fart må aldri fylles med 0, sist kjente fart, veggrense eller posisjonsreserve. Kvalifisering betyr passering av valgt profil, ikke dokumentert absolutt korrekt fart.
- Numeriske kvalitetsgrenser er uprøvde forslag. Lenovo/Brave og Lenovo/Chrome kvalifiseres separat, med eksplisitt feil-/forsinkelsesgrunnlag.
- Målemetode, kvalitetsregler og visning skal være korridoruavhengige. Fast 300 m beholdes.

## Non-goals

Fart fra påfølgende posisjoner som reserve, fartsoverskridelsesalarm, lyd, kart, kjøretøytilkobling, sertifisert fartsmåler, full historikk og garantert bakgrunnskontinuitet. Dynamisk forvarsel er bare en mulig senere konsument. Ingen produktimplementering, produkttester eller fysisk GPS-innsamling i planoppgaven.

## Success signal

En senere autorisert demonstrasjon består V01–V12 og den forhåndsfastsatte Lenovo-protokollen per nettleser uten falsk ferskhet, skjult innsamling eller sammenblanding med fartsgrense. Manglende native speed gir eksplisitt ikke-støttet målefunksjon; dokumentpakken kan likevel være ferdig.

## Assumptions

- **GS-A1:** Native speed kan være brukbar på målmaskinen; dette er ikke verifisert.
- **GS-A2:** GPS-LAB-1, ingen ekstra utjevning og foreslått avrunding gir en egnet første kandidat; feltkvalifisering kan forkaste kandidaten.

## Open Questions

- **P1:** Godkjenne GPS-D4 («<1» for liten positiv fart) og merking «Egen fart (GPS)» med forklarende tekst. Foreslått standard er spesifisert, ikke en planblokkering.
- **P2:** Godkjenne GPS-D5: eksplisitt fart-start/resume uten holdeplass, mens progresjon beholder sitt manuelle ankerkrav.
- **GS-Q1:** Native speed-dekning, stillstandsstøy og intern forsinkelse på faktisk Lenovo: story S4.
- **GS-Q2:** Fryse/begrunne terskler, feilbudsjett og uavhengig referanse før senere fysisk test: S2/S4.
- **GS-Q3:** Avstemme delbar kildekontrakt med faktisk posisjonsimplementasjon før integrasjon: S1/S3.
