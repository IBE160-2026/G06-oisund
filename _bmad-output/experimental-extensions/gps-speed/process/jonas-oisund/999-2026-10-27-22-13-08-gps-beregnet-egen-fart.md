# GPS-beregnet egen fart

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## 2026-10-27 kl. 22:13 — Jonas Øisund

### Oppgave

Planlegge GPS-beregnet egen fart fra avgrenset undersøkelse til kort spesifikasjon, ett epic og stories. Brukeren autoriserte isolert worktree og commit/push bare til egen eksperimentell branch; ingen produktimplementering eller fysisk posisjonsinnsamling.

### Plan

- Kontrollere worktrees, branches og origin; bruke siste kontrollerte committede speed-limits-tilstand.
- Lese prosjektinstruksjoner og fartsgrense-/posisjons-/rutenettplaner; undersøke offisielle API-kilder.
- Bruke bmad-spec og create-epics-and-stories med utdata bare i GPS-området.
- Kontrollere krav, lenker, dokumenter, privat innhold, staging og publiseringsområde.
- Leveranse: [README](../../README.md), [spesifikasjon](../../specs/spec-gps-speed/SPEC.md) og [epic/stories](../../planning/epics.md).

### Resultat

Worktree D:/IBE160-plan-gps-speed og branch codex/plan-gps-speed opprettet fra eksakt 5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c. Ren lokal codex/plan-speed-limits og live origin viste samme commit. Ingen ucommittede endringer kopiert eller andre branches byttet.

Pakken anbefaler native coords.speed, konvertering til km/t, tydelig ukjent/0/<1-semantikk, ingen posisjonsreserve og ingen ekstra utjevning i første kandidat. Fire CAP-er, ett epic, fire stories, 20 GWT-kriterier og 12 syntetiske scenarier er spesifisert. Konkret senere Lenovo/Brave/Chrome-protokoll inkluderer dekning, feil, total forsinkelse, tillatelser, livssyklus og personvern.

Sammenheng/kravbevaring og dependency-gjennomgang er utført; klokkeanomalier, reset ved utløp, målbart feltlag og S1/S2-avgrensning ble presisert. [Dokumentkontroll](../../planning/validation.md) og [maskinelt kontrollresultat](../document-checks.json) angir faktisk kontrollomfang. Ingen produkt-/enhetstest er kjørt. Kilder og uprøvde forslag er skilt.

Logg og issues ligger utvidelseslokalt etter brukerens områderegel. Eksisterende prosjekt- og fartsgrense-issues er lest og bevart. Staging var tomt før publiseringsforberedelsen. Loggfiler committes separat, deretter planpakken, og begge publiseres etter endelig staging-/commitkontroll. Denne loggteksten er skrevet før disse commitene; den påstår ikke push på forhånd. Endelige commit-ID-er finnes i branchens historikk, og faktisk remote-synkronisering bekreftes i sluttmeldingen.

### Åpne punkter

- P1/P2: Eiergjennomgang av merking/avrunding og separat eksplisitt fart-start/resume; foreslåtte standarder står i SPEC.
- GS-Q3: Avstem og kvalifiser én delbar posisjonskontroller mot senere faktisk implementasjon, særlig global stopp kontra rutetvetydighet (S1/S3).
- GS-Q1/Q2: Kvalifiser native speed, profil, uavhengig referanse, støy og forsinkelse på Lenovo i Brave og Chrome hver for seg (S2/S4); ingen fysisk kontroll er utført.
- GS-GATE: Ferdig/testet V1 og senere separat bygge-/testautorisasjon; ekte grenseintegrasjon krever sin egen kvalifiserte kontrakt. V1.4.5 er fortsatt forslag.
