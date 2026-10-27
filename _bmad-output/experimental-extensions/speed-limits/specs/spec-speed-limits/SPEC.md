---
id: SPEC-speed-limits
status: draft
approval: not-approved-for-build
version_target: V1.4.0
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
created: 2026-10-27
updated: 2026-10-27
companions:
  - behavior.md
  - pilot-manifest.md
  - verification.md
  - signs-and-rights.md
  - technical-addendum.md
  - ../../qualification/2026-10-27/qualification.md
  - ../../interfaces.md
  - ../../research/technical-speed-limits-2026-10-27/research.md
sources: []
assumptions: [SL-A1, SL-A2]
open_questions: []
---

# V1.4.0 — fartsgrensevisning og forvarsel

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Why

Gi bussjåføren et forståelig, rådgivende bilde av registrert vegfartsgrense og neste endring langs faktisk/relevant kjøreveg. Første omfang skal fungere uten egen fartsvisning, lyd eller kart. Brukerens valg er overflatetrasé Polaria → Strandvegen rundt sørenden → Kvaløyvegen → Langnes → flyplassavkjøringen, slutt etter fjerde rundkjøring.

## Capabilities

- **CAP-1**
  - **intent:** Se aktuell registrert vegfartsgrense adskilt fra kommende grense.
  - **success:** Et tydelig offisielt skilt vises bare ved kvalifisert aktuell veg, retning og datagrunnlag; ellers ukjent med årsak, uten tidligere verdi som aktuell.
- **CAP-2**
  - **intent:** Forberede seg visuelt på neste økning eller reduksjon.
  - **success:** Mindre skilt og nedtelling vises fra første kvalifiserte måling innen 300 m langs relevant veg, også ved sen oppstart; nærmeste endring, tett serie, terskelpendling og bortfall følger behavior.md.
- **CAP-3**
  - **intent:** Forstå når den kommende grensen faktisk blir aktuell.
  - **success:** Bytte skjer først etter underbygget passering; usikkerhet over grensen gir ingen for tidlig eller fortsatt gammel aktuell verdi.
- **CAP-4**
  - **intent:** Beholde nyttig informasjon uten å bli ledet til feil veg eller avkjøring.
  - **success:** Usikker videre arm skjuler forvarsel uavhengig av sikker aktuell verdi. Rundkjøring før endring, parallelle veger, hopp, stopp, avbrudd og avvik dekkes av akseptmatrisen.
- **CAP-5**
  - **intent:** Forstå databegrensninger og hva skiltvisningen representerer.
  - **success:** Mangler, alder og ukvalifisert midlertidig/variabel regulering håndteres uttrykkelig; offisielle ikonfiler har dokumentert kilde/lisensspor før distribusjon. Ingen påstand om bussens samlede tillatte fart.

## Constraints

- Bygging venter på ferdig/testet godkjent V1 og implementert/kvalifisert rutenett- og posisjonsstøtte, kvalifisert vegkobling og egen senere bestilling.
- Fast terskel 300 m beholdes i første leveranse. Planlagt trasé støtter, men overstyrer aldri motstridende posisjonsbevis. Holdeplassorden/nærmeste veg beviser ikke kjørt trasé.
- Foreground opt-in og eksplisitt gjenopptakelse følger posisjonsplanen. Pause/Off, skjult side, tilgangstap og kontekstbytte invaliderer gamle callbacks/verdier.
- Gjenbruk eksisterende React/TypeScript–FastAPI–PostgreSQL-arkitektur og private tilgangs-/utløpsgrenser. Offentlig vegsnapshot holdes separat; begrensede råfikser i RAM, ingen full kjørehistorikk eller privat posisjon til eksterne oppslag.
- Numerisk kvalitets-/aldersprofil, lenke-/objektbinding, kildegyldighet og skiltvilkår er kvalifiseringsporter. Manglende profil eller belegg er ikke en bestått pilot.

## Non-goals

Kart, lyd, GPS-fartsvisning, dynamisk varselavstand, fartsoverskridelsesalarm, kjøretøyregelberegning, motsatt pilotretning, bakgrunns-/tunnelkontinuitet og full Tromsø-dekning. Ingen produktkode, produkttester, faktisk posisjonsinnsamling, tjenester/databaseendringer, commit/push/merge i denne oppgaven. Epics/stories inngår nå i planleveransen etter ny bestilling.

## Success signal

En senere kvalifisert demonstrasjon består AC-01–AC-12 med begge skiltvisningene, underbygget passering og riktige ukjent-tilstander. Hele den valgte korridoren kan først kalles dekket når manifestets alle lenkeintervaller og fire rundkjøringer er kontrollert; ingen slik demonstrasjon er utført nå.

## Assumptions

- **SL-A1:** R1 Langnesvegen, R2 Workinn, R3 Giæverbukta og R4 sørlig flyplassavkjøring er foreslått identifisering av brukerens fire rundkjøringer, nå bundet til NVDB1126029/1126030/1125949/1125950 i planmanifestet; fysisk nåsituasjon og alle svingetillatelser er ikke verifisert.
- **SL-A2:** «Slutt etter flyplassrundkjøringen» avgrenses til første sikkert identifiserte utgående intervall i Flyplassvegen etter R4. Planlagt slutt er node1138796 etter1126506:0→1,37,570m etter R4-utgangen; terminalområdet og nordlig Grindneset-rundkjøring inngår ikke.

Ingen gjenværende produktvalg kreves for å ferdigstille denne spesifikasjonen. Tekniske hull og eventuelt avvik mellom foreslått og verifisert kryssidentitet står i pilotmanifestet; de gir ikke anledning til å gjette eller starte bygging.
