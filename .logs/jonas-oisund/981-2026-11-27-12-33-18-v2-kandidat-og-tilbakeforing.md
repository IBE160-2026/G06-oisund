# V2-kandidat og tilbakeføring over migrasjon 025 og 026

## 2026-11-27 kl. 12:33 — Jonas Øisund

### Oppgave

Klargjør en samlet V2-kandidat fra fersk GitHub main med den lokalt testede Daybreak-commiten og dokumentasjonen fra O6. Prøv tilbakeføring fra produksjonsversjonen d415383 i isolert PostgreSQL med ett utkast på hver side av oppgraderingen.

### Plan

- Integrer Daybreak og O6 i en ren lokal gren og kontroller produkt- og driftstreet mot Daybreak.
- Gjenbruk bevis for identiske filer. Kjør dokumentkontroll, POSIX-hjelperprøver og tilbakeføringsprøve.
- Vurder Ubuntu og stopp før publisering eller utrulling.

### Resultat

Kildegrunnlag fccb0d78f95f7ea40e6d29c77751a25d34599cbd, Daybreak 552c0f5a6d7118df3af01f2021e9fd35e712d959 og O6 112e51977626d0eb748ce5771efcfb8dd4b6a392. Integrert i 621c82f69649b9dd348cb8358d53ffcff8ef3ffb. V2-README, produktkode, avhengigheter og nyeste drift svarer til Daybreak. O6-status ble avstemt mot den rapporterte omstarten og etterkontrollen 27. november.

468 Linux/PostgreSQL- og 18 Edge-prøver verifisert i Daybreak-bevis. 66 Ubuntu-hjelperprøver og 47 undertester besto på integrasjonen, sammen med dokumentkontrollen. PostgreSQL 17.11-prøven bekreftet at standard rollback avvises. Produksjonskoden d415383 startet med den syntetiske private_work-databasen gjenopprettet fra førdumpen på skjema 024. Utkastet før oppgradering kunne åpnes med ny kontoautoritet. Utkastet og kvitteringen skrevet etter oppgradering ga HTTP 404. Begge utkast var tilgjengelige etter separat gjenoppretting av skjema 026-dumpen og omstart med kandidaten.

Dokumentasjonen og det maskinlesbare resultatet er med fra d0f0e653493580e2f5b9b3b95bda092aac2af7e4. [Prøve og vurdering](../../docs/evidence/v2-rollback-025-026-20261127.md).

### Åpne punkter

- Før godkjent Ubuntu-utrulling, verifiser fersk backup og vedlikeholdsvindu, vertsressurser og Cloudflare-klientadresse. Avtal hvordan skriving etter backupen sikres dersom tilbakeføring trengs. Installer helper, Compose, API, gateway og Access-verifikator samlet.
