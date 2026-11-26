# Avhengigheter, kildegrunnlag og arkitekturgjenbruk

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Leste, committede referanser

| Grunnlag | Commit og filer |
|---|---|
| Fartsgrense, følger denne branchen | 5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c: [README](../speed-limits/README.md), [SPEC](../speed-limits/specs/spec-speed-limits/SPEC.md), [interfaces](../speed-limits/interfaces.md), prosessens åpne punkter. |
| Posisjon, rent referanseworktree | df47a4e74ca982a2e04d6e5531e7744caf4f4717: [SPEC](https://github.com/IBE160-2026/G06-oisund/blob/df47a4e74ca982a2e04d6e5531e7744caf4f4717/_bmad-output/experimental-extensions/position-progression/specs/spec-position-progression/SPEC.md), README, behavior.md, route-interface.md og technical-addendum.md fra D:/IBE160-plan-position-progression. |
| Rutenett, rent referanseworktree | 7cada9d2e66af9806358f582bc8ea459321a6563: [SPEC](https://github.com/IBE160-2026/G06-oisund/blob/7cada9d2e66af9806358f582bc8ea459321a6563/_bmad-output/experimental-extensions/complete-route-network/specs/spec-complete-route-network/SPEC.md), README og data-contract.md fra D:/IBE160-plan-complete-route-network. |
| V1 ved utgangscommit | [Arkitektur](../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), rot-AGENTS.md, CLAUDE.md og faktisk sesjonslogg-SKILL.md; frontend/src/PrivateAccess.tsx, PrivateWorkdayView.tsx og useWorkdayResource.ts undersøkt for tilgang/generasjon/suspensjon. |

Referansenes historiske README-status er ikke bevis på nåværende Git-status eller gjennomført implementering. Ingen filer i referanseutvidelsene endres. GitHub-lenkene er commitbundne referanser til lokalt leste dokumenter; webinnholdet der er ikke separat kontrollert.

## Faktiske porter

| Leveranse | Må finnes/kvalifiseres | Ikke obligatorisk |
|---|---|---|
| Byggestart | Ferdig og testet godkjent V1, ny byggeautorisasjon; revider faktisk kode ved den senere baselinen. | Ingen automatisk oppheving av V1s GPS-forbud. |
| Egen fart alene | Autorisert felles foreground-posisjonskontroller, generasjonsvern, tilgang/sletting, native speed, klokke-/kvalitetsregler. | Ferdig fartsgrensefunksjon, NVDB, vegmatching, Entur, komplett rutenett, stoppestedsprogresjon eller lagret anker. |
| Samvisning med ekte grense | Kvalifisert registrert grense gjennom speed-limits-kontrakten og dens avhengigheter. | Fart må ikke forsvinne fordi currentRoadQualified er falsk eller vegsnapshot mangler. |
| Posisjonsprogresjon samtidig | Posisjonsplanens manuelle start-/gjenopptakelsesanker og egne rute-/koordinatporter. | Et manuelt stoppeanker etablerer ikke egen fart. |
| Operativ pilot | GS-E1-S4 per faktisk Lenovo-/OS-/nettleserversjon, senere eksplisitt tillatelse til kontrollert fysisk test. | Dokumentkontroll eller simulering kan ikke erstatte dette. |

## Små tillegg til eksisterende arkitektur

Gjenbruk React/TypeScript, eksisterende private tilgangsgrenser og Day/Night-visning. FastAPI/PostgreSQL beholder sine ansvarsområder; ingen nytt fartsendepunkt, GPS-tabell eller tjeneste. En ren frontend-evaluator og en liten visningskomponent abonnerer på samme autoriserte posisjonskontroller som posisjons-/fartsgrenseplanene foreslår. Dette er et nytt kontraktsforslag, ikke eksisterende implementasjon.

Hvis kontrolleren ennå ikke finnes, leverer GS-E1-S1 dens minste delbare foreground-kontrakt som en egen fartsslice; ikke en konkurrerende watch. Senere integrasjon må gjenbruke den. Målelivssyklus (tillatelse, råfix-gap, synlighet, tilgang og generasjon) holdes atskilt fra forbrukernes rutekvalitet. Rutetvetydighet, manglende Quay eller ukjent grense får ikke alene stoppe en ellers autorisert, kvalifiserbar fartstrøm.

**Samordningsvalg GPS-D5:** Start/gjenoppta egen fart krever eksplisitt handling, men ingen holdeplass. Dersom stoppestedsprogresjon også brukes, forblir den manuell-resume-needed inntil brukeren velger forekomst etter posisjonsplanen. Et fartsklikk gjenopptar aldri progresjonen. Globale Pause/Off og alle tilgangs-/synlighetsavbrudd stopper felles watch og begge forbrukere. Skjuling av bare fartspanelet kan fjerne dets abonnement; kontrolleren får bare fortsette hvis en annen synlig, eksplisitt aktiv forbruker fortsatt autoriserer den. Ingen skjult ekstra watch. Dette må kontraktkvalifiseres i S1/S3, uten å endre posisjonsplanen i denne oppgaven.

Fartsgrenseplanens optional qualifiedSpeed kan senere få den kvalifiserte utdataformen fra målekontrakten. Dynamisk forvarselavstand er bare en senere mulig konsument; fixed-distance=300 m endres ikke. Fart, registrert veggrense og kjøretøyets eventuelle samlede tillatte fart er ulike domener.
