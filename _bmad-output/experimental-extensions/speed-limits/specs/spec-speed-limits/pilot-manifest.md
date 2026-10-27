# Pilotmanifest — Polaria til flyplassavkjøringen

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

**SL-P1 v1-planning**, Polaria→flyplassen, overflate, slutt etter fjerde rundkjøring. Retning og endepunktvalg er avklart med brukeren. Motsatt retning er utsatt. Dette fryser et kildebundet planforslag, ikke en fysisk godkjent bussrute. D=dokumentert kilde, O=observert uttrekk, F=foreslått avgrensning, U=uavklart, P=fysisk kontroll.

## Ordnet trasé og identitet

O/F: Startnode1139933 på Strandvegen ved Polaria; slutt node1138796 på Flyplassvegen,37,570m etter rundkjøringens utgang. De139 ordnede kildesegmentene har ingen nodebrudd og summerer til8656,655m, cirka8,66km. Dette er summert kildelengde, ikke GPS-målt kjørelengde. Brukerens «omtrent én mil» var lokalkunnskap. Offentlig adresseprojeksjon0.00775722@1109722 er et søkeanker, ikke pilotens faktiske brukerposisjon.

| Kontroll / navngitt vegvalg | Valgt kildesekvens / økende intervall | Kontrollpunkt |
|---|---|---|
| CP0: Strandvegen sørover fra Polaria, overflate forbi Muségata | 1109722:0→1 |1139933→1138973; ikke tunnel eller Bjørnøygata/Mellomvegen-snarvei. |
| CP1–CP2: rundt sørenden, overgang Strandvegen→Kvaløyvegen, nord via Fagereng/Holt |1109517:0→0.9902808; deretter1126588:0→1 | Navneovergangen finnes i kildekjeden; ikke avstikker til Mellomvegen. Til R1 via1138911→3249937. |
| R1: Langnesvegen/Langnesbakken–Kvaløyvegen, videre mot Workinn |1126029:0→0.31012056 |3249937→3249939,26,221m bue. |
| Kvaløyvegen til R2 |1126527:0→1, deretter1126027:0.78574639→1 |Detalj→overordnet1126027 dokumentert; innnode1139057. |
| R2: Workinn/Langnestunnelen; videre mot Giæverbukta, ikke tunnel/Huldervegen |1126030:0.88033387→1 +0→0.62975708 |1139057→1139060,80,824m bue med feltretningen. |
| Kvaløyvegen til R3 |1126028:0→1 |1139060→1138977,242,984m. |
| R3: Giæverbukta, vestover mot flyplassen, ikke Ringvegen/østlig Erling Kjeldsens veg |1125949:0.65287709→1 +0→0.35105026 |1138977→1138963,82,336m bue med feltretningen. |
| E8/Kvaløyvegen til sørlig flyplassavkjøring |1125918:0→1 |1138963→1138787; detaljerte parallelle kjørebanelenker må respekteres ved matching. |
| R4: E8/fv862/Flyplassvegen, velg Flyplassvegen |1125950:0.87462251→1 +0→0.05053167 |1138787→3251245,18,448m bue. Ikke filterarm utenom sirkelen. |
| CP3: avslutt etter rundkjøringen |1126506:0→1 |3251245→1138796; overordnet1125938:0→0.36047074. Terminal og Grindneset er utenfor. |

Detaljene, geometri i SRID5973, kildefiler/referanser, metadata og avstander står i [source-bound-route.json](../../qualification/2026-10-27/source-bound-route.json). [Kvalifiseringsrapporten](../../qualification/2026-10-27/qualification.md) bevarer råbelegg, avviste alternativer og kildebegrensninger. En topologisk kjede er ikke alene bekreftelse på alle lovlige felt/svinger, eller dagens skilting/arbeidsrestriksjoner.

## Registrerte grenser og neste endring

O: Målrettede type105/egenskap2021-uttrekk viser40→30 på Strandvegen; videre30→50→30→50→60→50 på Kvaløyvegen;50 gjennom R1/R2;60 ved R3,70 på E8,50 ved utkjøring til Flyplassvegen. [Eksakte objekt-ID-er/versjoner/felt/gyldighet](../../qualification/2026-10-27/speed-intervals.csv) og [stedfestede endringer](../../qualification/2026-10-27/registered-changes.json) er kildedata, ikke fysiske skiltobservasjoner. Registrert70 i R4 sier ikke at70 er trygg rundkjøringsfart eller bussens samlede tillatte fart.

**K3, konkret rundkjøring før endring:**70→50 ved node3251245, fra1125950 til1126506/overordnet1125938. Objekt1019488950v1→1019488951v1. Med200m igjen til R4-innkjøring blir avstanden218,448m langs valgt bue til grensen. For en300m-situasjon ligger scenariopunktet281,552m før innkjøringen. Dette er beregnede kildepunkter, ikke samlet posisjon. Ukvalifisert neste arm skjuler forvarsel, men kan beholde sikker aktuell70. Etter valgt slutt gis ingen påstand om endringer utenfor manifestet.

**Viktig rettelse:** Den tidligere265,519m-kandidaten gjennom R2 er forkastet: den brukte bue mot feltretningen. Korrekt kildebue gir323,808m til R3-grensen. AC-07s syntetiske250m illustrasjon beholdes separat. Ingen grense er flyttet for å få et passende eksempel.

## Status og kontrollpunkter

| Punkt | Avsluttet i planleggingen | Senere lukking |
|---|---|---|
| K1 | Sammenhengende plankjede, fire ring-ID-er, rettede buer og eksplisitte start/sluttnoder | Felt-/svingtillatelser for buss og Polaria-arbeid må kontrolleres i story1.1/1.7. |
| K2 | Målrettede105-uttrekk, intervaller og detaljbinding på valgt trase | Oppdatert kildealder, konflikt-/mangeldekning og faktisk midlertidig/variabel regulering i1.1/1.7. |
| K3 | R4 med virkelig registrert grense; feil R2-kandidat forkastet | Armkvalifisering og langsveg-avstand i1.4/1.5; fysisk avstand i1.7. |
| K4 | Geometri og scenarioer før/etter, feil arm, parallellveg, datakant | Alternativvegdekning og senere syntetiske kontroller i1.1/1.3–1.6. |
| K5 | Fysisk plan med stoppkriterier | Ingen fysisk test utført; story1.7. |

Ingen ny brukeravklaring om korridor/retning/antall/lyd. Dersom senere faktisk vegregulering motsier ønsket vegvalg, dokumenteres det konkrete avviket; ruten tvinges ikke. [Teknisk profil og porter](technical-addendum.md) beskriver forskjellen mellom ferdig plan og kvalifisert produkt.

## Primærkilder

- [NVDB Les V4 vegnett](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Vegnett/) og [ruteberegning](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Rute/); uttrekks-URL-er/tider/hash i [requests.jsonl](../../qualification/2026-10-27/requests.jsonl).
- [V830, §7.2 feltretning](https://www.vegvesen.no/globalassets/fag/handboker/hb-v830-nasjonalt-vegreferansesystem.pdf?v=491e2d). Dette gjelder originalt NVDB-basisnett; andre eksportformater kan ha annen geometriretning.
- [Troms fylkeskommune: arbeid ved Polaria](https://www.tromsfylke.no/aktuelt/omkjoring-pa-strandvegen.76701.aspx). Planlagt slutt er ikke ferdigmelding.
- [Vegvesenets planbeskrivelse2023](https://www.vegvesen.no/globalassets/vegprosjekter/europavei/e8flyplasstunnelen/vedlegg/planbeskrivelse-e8-flyplasstunnelen.-horingsutgave-15.12.2023..pdf?v=496fb7) og [Avinor/COWI april2025](https://www.tromsfylke.no/_f/p1/ib95ee31c-1b21-48f0-8d1f-d44e6c0527f6/planbeskrivelse.PDF) er historisk navne-/atkomststøtte. Nye planlagte tiltak behandles ikke som gjennomført.

Tidligere Eidvegen/Straumsvegen- og FV7772/Stakkevollvegen-uttrekk brukes fortsatt ikke som pilotbelegg.
