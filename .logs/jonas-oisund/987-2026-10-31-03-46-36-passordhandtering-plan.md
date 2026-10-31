# Passordhåndtering — plan

## 2026-10-31 kl. 03:46 — Jonas Øisund

### Oppgave
Planlegg egen passordendring og forsvarlig gjenoppretting for eksisterende brukere, uten implementering, produksjonsendring eller deploy. Egen eksperimentell branch fra oppdatert origin/main; commit og push dokumentasjon og sesjonslogg, ingen merge/tag/release.

### Plan
- Les AGENTS.md, CLAUDE.md og sesjonslogg-skill; undersøk autentisering, data, økter, UI, nettbrudd og Ubuntu-oppsett.
- Følg BMAD Spec og eksisterende isolasjon for eksperimentelle utvidelser. [Plan og spørsmål](../../_bmad-output/experimental-extensions/password-management/specs/spec-password-management/implementation-plan.md).
- Vurder administrativ gjenoppretting mot e-post og uavhengighet fra automatisk avviksinnhenting; skill funn, forslag og eierbeslutninger.

### Resultat
Hentet origin/main 5cee9e03d03d2c9c165c7f8fec64aa3e146959ab. Appens create_worktree avviste repoet som undermappe av prosjektroten; separat lokal klon password-management-planning ble brukt. Opprettet codex/plan-password-management fra fersk origin/main. Eksisterende v1-final-control er fortsatt ren på docs/v1-final-control; andre checkouts/worktrees, ucommittede filer og sources er urørt. Automatisk-avviksbranch da867072a8a17249032c00efa51bd61979d41428 ble kun lest.

Planleggingscommit b83367cbdabd8e0486264d8907c14aa6a6ff03bb inneholder isolert README, SPEC, kanonisk memlog, funn, gjennomføringsplan, akseptansematrise og lokal BMAD-ruting. Anbefalingen er egen passordendring + administrativ engangskode, med alle appøkter tilbakekalt og separat levering. Ved første utkast var ingen anbefaling registrert som godkjent; eierbeslutningene nedenfor erstatter denne statusen for de uttrykkelig valgte punktene. E-post vurdert med adressebekreftelse, avsendertjeneste, hemmeligheter og kontrollert nettverkstilgang. Ingen hemmeligheter hentet eller etterspurt.

Bekreftede funn: ingen e-post/resetfunksjon i kontomodellen; scrypt og 14-dagers serverøkter; ingen selvstendige dagstillatelsestokener eller varig offline-innlogging. Planen behandler avledet dagtilgang, eksisterende nettbruddshåndtering, samtidige forespørsler, låserekkefølge og risiko for innlogging med gammel hash etter tilbakestilling. Konto-ID, eierskap og lagrede data bevares.

Kontroller: BMAD-resolver og isolerte utstier, dokumentenes relative Markdown-lenker, git diff --cached --check og avgrenset filliste bestått; to dokumentgjennomganger for sammenheng og bevaring av A–E. OWASP-kilder kontrollert. Ingen produkttester kjørt: dette er bare planlegging. Ingen kode, migrasjon, produksjonskonfigurasjon, deploy, merge, tag eller release endret. Dokumentasjon og denne separate loggcommiten skal pushes til kun den autoriserte planleggingsbranchen; push-kvittering kontrolleres før sluttoppsummering.

Oppfølging samme dag: Jonas ba om å oppdatere og pushe beslutningene uten å starte implementering. Beslutningscommit **24bbfcb** oppdaterer README, SPEC, memlog og de tre følgedokumentene. Første målgruppe er Jonas og faglærer; Jonas tar administrasjon og tilbakestillinger. Administrativ engangskode, ny innlogging på alle enheter ved begge flyter og separat levering er besluttet. E-post og offentlig tilgang er utenfor første omfang; ingen permanent avvisning av fremtidig offentlig tilgang eller døgnkontinuerlig supportforpliktelse er utledet. Konkrete tekniske detaljer står fortsatt som forslag. Ingen implementering startet.

Branch var ren og lik remote før oppdateringen (fetch og 0/0-kontroll). Dokumentgjennomgang og git diff --check bestått. Q2–Q4 lukket i issues.md; Q1 presisert til gjenstående driftsrutine. Samme sesjonslogg gjenbrukt. Ingen produkttester kjørt for dokumentendringen. Push til kun planleggingsbranchen utføres etter separat loggcommit og kontrolleres mot remote.

Oppfølging — epic og implementeringsklare stories (31.10): Brukeren ba om fullført planlegging/validering og push, uten implementering. Ny fetch viste origin/main fortsatt **5cee9e03d03d2c9c165c7f8fec64aa3e146959ab**, ingen kildeendringer som påvirker planen. Planleggingsbranch var ren og 0/0 mot origin ved start. Eksisterende V1-epic 9–12 og utvidelsesprecedens AN-E1 ble undersøkt; **PM-E1** med **PM-E1-S1–S4** bruker utvidelsesnavnerommet uten å anta at Epic 13 er ledig.

Commit **41d9c14** inneholder avstemt SPEC/plan/oversikt, [epic og stories](../../_bmad-output/experimental-extensions/password-management/planning/epics.md), teknisk kontrakt, scenario-/kravdekning, workflow og valideringsrapport. Rekkefølge: S1 egen passordendring med felles øktsikkerhet, S2 administrativ utstedelse/tilbakekalling, S3 kodeinnløsning i appen, S4 samlet kvalifikasjon og operatørrutine. Egen appkonto via uavhengig SSH uten appinnlogging er eksplisitt krav, ikke et åpent valg. Adminpanel/e-post/offentlig registrering er utenfor. Separate levering og alle-enheter-innlogging er bevart.

BMAD CE sine fire dokumentfaser og mal ble brukt med isolert TOML/YAML-ruting, basert på eksisterende plan og parent PRD/arkitektur/DESIGN/EXPERIENCE. Rutinemenuer ble tilpasset brukerens uttrykkelige oppdrag om å fullføre planleggingen; ingen menybekreftelse, produktgodkjenning eller implementeringsautorisasjon er oppdiktet. Ingen Build/sprint-dispatch kjørt. Historisk PM-1–PM-4-gruppering erstattet av de konkrete storyene. Gjennomgangen rettet 44px-formulering til eksisterende 58px/IR-01, presiserte én felles låserekkefølge uten obligatorisk credential-version-migrering, og skilte terminalvisning fra bevis for fravær av opptak/logging.

Dokumentvalidering bestått: **4 stories, 33 unike akseptansekriterier, alle 20 PM-A-scenarioer, 7 FR, 5 NFR og 4 UX-krav**, relative Markdown-lenker, isolert utsti, bakoverrettede avhengigheter og ingen malplassholdere. git diff --cached --check bestått; kun utvidelsesdokumentasjon/rutingsmetadata i plancommiten. To dokumentgjennomganger for sammenheng og bevaring; ikke uavhengig agentreview. Ingen produkttester eller produksjonsoperasjoner. Storyene er spesifikasjonsmessig implementeringsklare i rekkefølge etter separat beskjed; dette er ikke produktaksept eller tillatelse til å starte. Logg oppdateres i separat commit og pushes sammen med planen; remote kontrolleres før sluttmelding.

### Åpne punkter
- Før reell bruk skal Jonas kontrollere praktisk kontakt-/identitetskontroll og sikker engangsvisning/handoff uten opptak. Rutine for egen appkonto via SSH, fravær og separat tap av SSH/outer Access er beskrevet som S2/S4-oppgaver. Ingen uavklart produktbeslutning hindrer oppstart av S1 etter autorisasjon.
- PM-E1-S1–S4 skal implementeres og testes bare etter separat oppdrag. Samlet syntetisk regresjon, migrering/restore/rollback, fysisk nettbrett/PC og personlig eieraksept gjenstår før separat releasebeslutning. Ingen versjon er fastsatt.
