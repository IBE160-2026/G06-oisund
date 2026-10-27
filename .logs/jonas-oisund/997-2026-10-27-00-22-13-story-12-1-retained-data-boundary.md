# Story 12.1 – grense for lagrede data

## 2026-10-27 kl. 00:24 — Jonas Øisund

### Oppgave
Gjennomføre Story 12.1 frem til teknisk ferdig og klar for manuell aksept, med selvstendig implementering, isolert testing og review. Feilsøke uv-tilgangen som egen forberedelse og fortsette bare etter vellykket påkrevd Build-oppstart. Ingen registrering av eieraksept, commit, push, merge eller ordinær aktivering.

### Plan
- Lese faktiske AGENTS.md, CLAUDE.md, sesjonslogg-oppskriften, arbeidsflyt, aktiv backlog, spesifikasjoner og ferdig Epic 11-retro. Avgrense relevante åpne retropunkter.
- Kontrollere faktisk main; opprette isolert branch/worktree med registrert base og egne testporter, Compose-prosjekt, databaseklynge og volum.
- Følge [spesifikasjonen](../../_bmad-output/implementation-artifacts/spec-12-1-enforce-the-retained-data-boundary.md) og [implementeringsplanen](../../_bmad-output/specs/spec-12-1-retained-data/implementation-plan.md). Implementere, teste grensene og gjennomføre tre uavhengige review-lag med reinspection.
- Bevare ordinære tjenester/data og historisk evidens, dokumentere 12.2-integrering og overlevere konkrete manuelle teststeg.

### Resultat
- uv-feilen skyldtes sandkassens lese-/kjørebegrensning. Eksisterende WinGet uv 0.12.10 fungerte ved avgrenset kjøring utenfor sandkassen; filrettigheter var normale og ingen blokkeringsstrøm ble funnet. PATH, ACL-er, sikkerhetsfunksjoner og andre chatters miljø ble ikke endret. Den eksakte påkrevde rendererkommandoen lyktes; skillen ble ikke redigert.
- Worktree `D:/IBE160-story-12-1`, branch `story/12-1-retained-data-boundary`, base `0bae54833f38dc3dbf041d54c324c220618c21da`. main er nyere enn tidligere f5ffa4b. Arbeidet er ukommittert etter uttrykkelig instruksjon.
- Migrasjon 014 innfører tidsavgrenset, innholdsfri serverutstedelse for nye avvik via POST /notice-operations. Purget/ukjent opprinnelig opprettelses-ID kan ikke gjenskape avvik. Aksepterte kvitteringer beholdes uforanderlige under egen retensjon. Opprettelse som krysser sluttid eller operasjonsfrist rulles tilbake.
- Siste retensjonskontroll på lesinger og sideinndeling er rettet. Tomme sider kan videreføre skanningen uten å skjule gyldige senere poster. En minnebasert server-/monoton klokke hindrer at treg eller fastlåst enhetsklokke forlenger privat visning. Utløpte lagrede utkast og avviksfelt/leserinnhold tømmes; sene svar ugyldiggjøres og uavhengige nye forslag bevares.
- Den korrigerte, godkjente 11.5-modellen er beholdt: kontofelles avvik har egen levetid og slettes ikke med opprinnelig dag. Forskjellen fra eldre planleggingstekst er dokumentert. Råoriginaler forblir transient byte-/workerbehandling; ingen nye originale PDF-er eller private vedvarende nettleserlagre er innført.
- Sluttgater: **441 backend-/domene-/PDF-tester passerte** på 556,74 sekunder og **479 private Playwright-tilfeller passerte i én kjøring** på 40,4 minutter. Begge hadde exit 0 og uendrede kildefingeravtrykk. **7 restaureringskontroller og 4 prosesseierskapskontroller passerte**. Én eksisterende TestClient-deprecationadvarsel er dokumentert.
- Faktisk oppgradering av populert 013-skjema til 014, gjentatte migrasjoner og to API-oppstarter passerte: utløpte payloads/kommandoer ble fjernet, uavhengig avvik og fire gyldige rader/kvitteringer var identiske, gammel purget opprettelse ble avvist. Timeplanleggerens faktiske funksjon ble testet med akselerert venting og simulerte callbacks, også etter simulert databasefeil. Ingen faktisk én-times soak hevdes.
- Alle 44 kjørte API-/migrasjonsfiler samsvarer med host-SHA256 og er eldre enn API-oppstarten. Servert HTML/JS/CSS samsvarer med siste dist; no-store og eksponert Date er verifisert. Alle 1 017 opprinnelige main-filer er uendret. Alle 414 historiske evidensfiler er byte-identiske; nye opptak er arkivert separat. Git-statmetadata ble oppfrisket uten staging av innhold.
- Tre uavhengige review-lag og reinspection er gjennomført; ingen beholdte funn står åpne. Opprinnelige feil og klassifiseringer er bevart i [rapporten](../../docs/evidence/12-1-retained-data.md). [Maskinbeviset](../../docs/evidence/12-1-verification.json) inneholder sluttdigester og kildemanifest.
- E11-A6 og E11-A11 er teknisk løst og lukket i issues/sprint, med uttrykkelig merknad om at storyens manuelle aksept venter. A7/A8/A12 er håndtert for 12.1 og beholder bredere senere forpliktelser. Øvrige eksisterende retro-/tema-/nettbrettpunkter er bevart.
- API 18121 og frontend 15121 kjører bare for Compose-prosjektet ibe160-story121-tests. To fiktive linje-20-dager for januar 2031 er klare; testlegitimasjon finnes bare i ignorert `.private-runtime/story121-manual-credentials.json`. Bruk nytt InPrivate-vindu. Fysisk Lenovo/Android/Brave/fjernaksess er ikke kvalifisert av desktop-testene.
- Story/spec/backlog står i review og eieraksept pending. Ingen annen story er startet her. Ingen ordinær migrasjon/aktivering, staging av innhold, commit, push eller merge er utført. Det uttrykkelige commit-forbudet går foran loggoppskriftens generelle commit-steg; også denne loggen forblir ukommittert.

### Åpne punkter
- Manuell aksept av 12.1 gjenstår; følg konkrete steg i rapporten på den isolerte 15121-adressen.
- 12.2 må integrere migrasjon 014, serverutstedte opprettelses-ID-er, Date/CORS/felles klokke og API-portkonfigurasjonen etter dokumentert kontrakt.
