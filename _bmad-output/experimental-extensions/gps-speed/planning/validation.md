# Sluttkontroll av planleggingspakken

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

2026-10-27. Kontrollomfang: dokumenter og Git-avgrensning, ingen produktkjøring.

## Faglig kontroll utført

- bmad-spec sammenheng: fire unike CAP-er med intent/success, fem kjernefelt, eksplisitte avgrensninger og målbare senere suksesskriterier. Antakelser og produktvalg er navngitt.
- Kravbevaring: brukerens målesemantikk, hele bevegelses-/avbruddsmatrisen, én kilde, personvern, korridoruavhengighet, separat fartsgrensekvalitet, Lenovo og uendret 300 m er sporet til kontrakt og stories.
- Epic-kontroll: ett brukerverdiepic, fire sekvensielle stories og 20 Given/When/Then-kriterier; FR1–6, NFR1–4, AR1–3 og UX-DR1–3 har dekning. Ingen senere story er implementeringsavhengighet for en tidligere slice.
- Avhengigheter: fart alene krever ikke ferdig fartsgrense, rutenett eller stoppestedsprogresjon. Ekte grenseintegrasjon har egen port. Målelivssyklus skilles fra rutetvetydighet.
- Arkitektur: gjenbruk eksisterende frontend og tilgang; ingen starter-template, nye tjenester, databaseendringer, GPS-persistens eller endring i godkjent V1-omfang.
- Forskningsgrunnlag: W3C, Mozilla og Chrome-dokumentasjon åpnet; API-egenskaper er adskilt fra egne slutninger og uprøvde profiler. Ingen sensor-/nøyaktighetsgaranti fra API-støtte.
- Planstatus: S1–S4 og V01–V12 er framtidig arbeid. Ingen fysisk kontroll, produkttest eller måleresultat er presentert som bestått.

## Funn som ble rettet

1. Framtidig/ugyldig måletid fikk eksplisitt time-invalid/manual-resume og kan ikke oppdatere rekkefølgeanker.
2. Utløp resetter kvalifiseringsparet; tilbakekomst gir ikke øyeblikkelig verdi fra gammel sekvens.
3. Feltlag har konkrete terskelkryssinger og synkroniseringsbudsjett; manglende verdi kan ikke regnes som bestått lagtest.
4. S1s grunnport er skilt fra S2s fullstendige dynamiske koherens, slik at det ikke blir en skjult framoveravhengighet.
5. Hver story fikk eksplisitte kravreferanser, i tillegg til kravmatrisen.

## Mekaniske kontroller

[Kontrollskript](../process/check-documents.py) verifiserer lokale Markdown-lenker, SPEC-companions og epic-inputs, JSON, UTF-8, fire CAP-er, fire stories og 20 unike GWT-kriterier, scope-merking og filavgrensning. [Faktisk resultat](../process/document-checks.json) er autoritativt for denne kjøringen. Skriptet sjekker dokumenter, ikke produktet. Eksterne referanselenker til commitbundne planer er lokalt kildekontrollert; de er ikke HTTP-testet.

Hele utvidelsens nye filinnhold gjennomgås før eksplisitt staging, inkludert kontrollskript og logger. Git diff --check, full stagingliste/diff og publiseringscommitene kontrolleres før push. Endelige commit- og pushresultater rapporteres etter utførelse; denne teksten alene er ikke bevis på publisering.

## Kvalifiseringsporter som står igjen

P1/P2 er produktvalg med anbefalte standarder. GS-Q1/Q2/Q3 er konkret fordelt på stories, med feil-/no-go-kriterier. V1-port, senere bygge- og fysisk-testautorisasjon gjelder fortsatt. [Åpne punkter](../process/jonas-oisund/issues.md) er vedlikeholdt i utvidelsens område. Pakken er ferdig til eiergjennomgang, ikke godkjent for implementering.
