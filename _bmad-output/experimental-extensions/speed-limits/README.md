# Fartsgrensevisning og forvarsel — V1.4.0

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Ferdig planleggingspakke med kildekvalifisering, spesifikasjon og én epic med sju stories, oppdatert2026-10-27. Første omfang er registrert aktuell vegfartsgrense og visuelt forvarsel omtrent 300 meter langs kvalifisert kjøreveg før neste endring. Begge beholdes i første plan. V1.4.0 er en planlagt versjon, ikke et godkjent leveranseløfte. Implementering venter på ferdigstilt og testet godkjent V1, nødvendige avhengigheter og særskilt bestilling.

## Arbeidsområde og utgangspunkt

| Kontroll | Verifisert verdi |
|---|---|
| Faktisk arbeidsmappe og repository-rot | D:/IBE160-plan-speed-limits |
| Branch | codex/plan-speed-limits |
| Nøyaktig lokal main-utgangscommit | 74849ff21bee108fe9cff93d740a96a6c6d2d7c5 |
| Commit-emne | Logg: status-story-12-1-og-12-2 |
| Remote, bare lest | origin: https://github.com/IBE160-2026/G06-oisund.git |
| Dokumentområde | _bmad-output/experimental-extensions/speed-limits/ |

Hovedarbeidsområdet var rent. Branch og worktree manglet og ble opprettet fra denne commiten. Main ble ikke byttet, ucommittet arbeid ble ikke kopiert, og eksisterende worktrees ble bevart. Ingen fetch, commit, push eller merge ble utført.

## Leseveiledning

1. [Ferdig epic og sju stories](planning/epics.md), med [sluttvalidering og beredskap](planning/validation.md).
2. [Gjeldende spesifikasjon](specs/spec-speed-limits/SPEC.md), [atferd](specs/spec-speed-limits/behavior.md), [pilotmanifest v1-planning](specs/spec-speed-limits/pilot-manifest.md), [akseptmatrise](specs/spec-speed-limits/verification.md) og [profil/porter](specs/spec-speed-limits/technical-addendum.md).
3. [Avsluttet kildekvalifisering](qualification/2026-10-27/qualification.md), [ordnet kildelenkekjede](qualification/2026-10-27/source-bound-route.json), [ikonrettigheter](specs/spec-speed-limits/signs-and-rights.md).
4. [Produktbeslutninger](plan.md), [grensesnitt](interfaces.md) og [opprinnelig research](research/technical-speed-limits-2026-10-27/research.md).
5. [BMAD-ruting](planning/evidence/routing.md), [sesjonslogg](process/jonas-oisund/999-2026-10-27-20-11-16-fartsgrenseplanlegging.md) og [åpne gjennomføringsporter](process/jonas-oisund/issues.md).

## Lesende prosjektgrunnlag

Nyeste tilgjengelige arbeidsfiler ble lest, også der README henviser til senere spesifikasjon fremfor eldre research:

- D:/IBE160-plan-complete-route-network, branch codex/plan-complete-route-network, HEAD 7cada9d2e66af9806358f582bc8ea459321a6563: README, specs/spec-complete-route-network/SPEC.md og data-contract.md. P1 gjelder datert avgang og ordnede holdeplassforekomster; geometri er ikke førsteleveranse.
- D:/IBE160-plan-position-progression, branch codex/plan-position-progression, HEAD df47a4e74ca982a2e04d6e5531e7744caf4f4717: README, specs/spec-position-progression/SPEC.md, route-interface.md og technical-addendum.md. Manuell gjenopptakelse og stoppestedsestimat er planlagt; sikker vegtilknytning følger ikke av dette.
- Lokal AGENTS.md, CLAUDE.md, sesjonslogg-oppskriften, installert bmad-deep-recon og V1 ARCHITECTURE-SPINE.md (planning-artifacts/architecture/architecture-IBE160-2026-09-23).

Begge referanse-worktrees var rene ved kontroll. Referansene er planforslag, ikke bevis på implementasjon. Ingen av dem er endret. Alle nye filer, inkludert prosessminne, sesjonslogg og issues, ligger her. Brukerens eksplisitte forbud mot commit og skriving utenfor området går foran standardoppskriften for logging.

## Gjeldende pilot og status

Valgt overflatetrasé: Polaria→Strandvegen rundt sørenden→Kvaløyvegen→Langnes→Flyplassvegen, slutt etter sørlig flyplassrundkjøring. Fire rundkjøringer er bundet til NVDB-identifikatorer. Planintervallet går fra node1139933 til1138796, med139 kildesegmenter uten nodebrudd og summert kildelengde cirka8,66km. Det er ikke en fysisk målt eller fullstendig reguleringskvalifisert bussrute.

Registrerte verdier30/40/50/60/70 er funnet i målrettede uttrekk. To baklengsbuer fra rutetjenesten er forkastet. Det tidligere265,519m-eksempelet gjennom Workinn er ugyldig; R4 med70→50 ved utkjøring til Flyplassvegen er valgt kandidat for forvarsel gjennom rundkjøring. Riktig bue er18,448m; forvarsel krever fortsatt kvalifisert videre arm.

Planleggingen er fullført gjennom epics/stories. Ingen nye produktvalg blokkerer planen. Operativ kilde-/feltkontroll, faktiske ikonfiler, implementasjonens syntetiske verifikasjon og fysisk GPS-/skiltkontroll er konkrete senere story-kriterier, ikke påstått bestått. Ferdig/testet V1 og kvalifiserte rutenett-/posisjonsavhengigheter samt separat byggbestilling kreves før implementering.

Alle nye filer, prosessminner og kildebelegg ligger her. Ingen produktimplementering, produkttester, faktisk posisjonsinnsamling, commit, push eller merge er utført. Tidligere spec-kontroller gjelder sitt historiske dokumentsett; [gjeldende sluttkontroll](planning/validation.md) gjelder hele den nye planleveransen.
