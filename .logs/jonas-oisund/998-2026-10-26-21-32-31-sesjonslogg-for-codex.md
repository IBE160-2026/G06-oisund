# Sesjonslogg for Codex

## 2026-10-26 kl. 21:34 — Jonas Øisund

### Oppgave
Gjør faglærerens sesjonslogg-oppsett tilgjengelig for Codex gjennom en kort AGENTS.md i prosjektroten. Bevar lærerens filer og eventuelle lokale endringer, følg oppskriften for denne økten og ikke push.
Brukeren ba deretter eksplisitt om å committe bare AGENTS.md og pushe lokale commits til origin/main, med sesjonslogging og kontroll av Git-status.

### Plan
- Kontroller Git-status og les CLAUDE.md og .claude/skills/sesjonslogg/SKILL.md.
- Opprett en kort kobling i AGENTS.md med krav om å lese de faktiske filene.
- Les ferdig AGENTS.md, kontroller stiene og kjør git diff --check.
- Les brukerens issues.md og commit sesjonsloggen separat lokalt.
- Etter brukerens push-instruksjon: commit bare AGENTS.md, kontroller origin/main, push lokale commits og oppdater denne loggen separat.

### Resultat
Arbeidskopien var ren ved oppstart, og AGENTS.md fantes ikke. Opprettet AGENTS.md med henvisninger til lærerens instruksjoner, vilkårene for sesjonslogging og krav om faktisk lesing uten å stole på automatisk behandling av @-importer. Regler om logging, åpne punkter og lokale loggcommits er forankret, med prosjektets regler og brukerens eksplisitte instruksjoner som førende.

Hele AGENTS.md er lest tilbake. Begge refererte instruksjonsfiler og brukerens issues.md finnes. git diff --check besto. Lærerens filer, produktkode og tester er uendret. Eksisterende issues.md er lest; ingen punkter ble lagt til eller løst i denne avgrensede økten. AGENTS.md er ikke committet; bare denne sesjonsloggen committes lokalt etter oppskriften. Ingen push er utført.

Ved oppfølgingen ble bare AGENTS.md committet i `8eda38128f61400f1699aa05f06e256bc8417fd0` med meldingen `docs: koble Codex til prosjektets sesjonslogg`. Commitinnholdet og git diff --cached --check ble kontrollert. Origin/main ble bekreftet på `f5ffa4b` før push; vanlig push publiserte `52da418` (første sesjonslogg) og `8eda381` til origin/main. Denne loggoppdateringen committes og pushes separat etter brukerens instruksjon. issues.md er lest på nytt og uendret; ingen nye eller løste åpne punkter. Produktkode og tester er fortsatt uendret.

### Åpne punkter
Ingen.
