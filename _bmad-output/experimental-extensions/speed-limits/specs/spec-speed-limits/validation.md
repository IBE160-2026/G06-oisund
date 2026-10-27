# Validering av spesifikasjonen

Tidligere kontroll nedenfor gjelder forrige dokumentversjon. Gjeldende sluttstatus: [SL-PLAN-1](../../planning/validation.md).
**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

2026-10-27. Dokumentkontroll, ingen produktverifikasjon.

## Sammenheng

Fem unike CAP-ID-er har intent/success. Constraints skiller ferdig/testet V1, implementerte/kvalifiserte avhengigheter, datakvalifisering og senere byggbestilling. Non-goals bevarer alle avgrensningene. Success signal viser til tolv konkrete AC-er; ingen resultater er fremstilt som utførte. Navngitt forslag, historisk kildeomtale, observert JSON, ukjente lenker og fysisk test holdes atskilt.

SL-A1 identifiserer de fire rundkjøringene foreløpig; det er ikke en verifisert nåsituasjonsliste. SL-A2 velger et operativt endepunkt etter sørlig flyplassavkjøring i Flyplassvegen, i tråd med mottatt brukeravklaring. Eksakt sluttposisjon og vegnavn på mellomkoblinger må fryses fra data. Ingen tidligere Eidvegen-/FV7772-treff er brukt som korridorbevis. Numerisk kvalitetsprofil og fysisk 300m-toleranse er åpne kvalifiseringsporter, slik at dokumentet ikke kan tas som kjørbar/godkjent pilot.

## Bevaring og sporing

| Brukerkrav / tidligere grunnlag | Bevart i |
|---|---|
| Overflatekorridor, korrigert antall, én retning, slutt etter rundkjøring | SPEC Why/assumptions, pilotmanifest CP0–CP3/R1–R4 |
| Aktuell offisiell skiltvisning, ukjent og rettigheter | CAP-1/5, behavior, signs-and-rights, AC-01/12 |
| Fast300m, mindre kommende skilt, nedtelling, begge endringsretninger | CAP-2/3, behavior, AC-02/03/06 |
| Sen oppstart, tett serie, pendling og bortfall | behavior, AC-03/04/05/10 |
| Rundkjøring før endring og uavhengig aktuell/kommende tillit | behavior vilkårsmatrise, K3, AC-07, interfaces |
| Parallelle veger, hopp, stopp, avbrudd/gjenopptakelse, avvik | CAP-4, behavior, AC-06/08/09/10/11 |
| Manglende/midlertidig/variabel regulering og kjøretøygrense-skille | CAP-5, research, signs-and-rights, interfaces, AC-12 |
| Lokal behandling, avgrenset offentlig snapshot og metadata | Constraints, adoptert interfaces/research, manifestets feltkrav |
| Senere egenfart/dynamikk, ingen alarm/lyd/kart | Non-goals og interfaces |
| Ingen bygging, tester, sporinnsamling, commit eller fulle planprosesser | Constraints/Non-goals, verification |

Wrapper-only innhold: arbeidsområde og kjøringsruting ligger i README/evidence fremfor spec-kjernen. Rå konfigurasjonsfiler er lesebevis, ikke aktiv delt konfigurasjon. Ingen epics/stories generert. Tidligere plan er oppdatert til produktvalg, interfaces presisert og README peker først til gjeldende spec. Forskningsrapporten er bevart som historisk kildegrunnlag.

## Kontrollmetode og begrensninger

Relative Markdown-lenker, følgedokumenter, CAP-/AC-ID-er, UTF-8, whitespace og filplassering kontrolleres mekanisk. Git-diff og status kontrolleres; siden planområdet var utracket ved oppstart, vises det som nye filer, ikke som en historisk baselinecommit. Et lokalt additivt dokumentdiff ligger i evidence/documents.diff og gjennomgås med git diff --no-index --check. Det er ikke en commit.

Kildekontrollen er begrenset til dokumenterte primærutdrag og offentlig JSON; ingen ny bred research eller uavhengig fysisk kontroll. Nettverktøyet kunne ikke lese hele den store 2022-PDF-en eller detaljsidene for 30/60-symbolene. Disse begrensningene er synlige der påstandene brukes. Ingen krav er falt bort som følge av dette.

Sluttkontroll bestått: [maskinelt kontrollbelegg](evidence/document-checks.json). Fem CAP-er, tolv AC-er, ingen manglende relative lenker eller whitespace-funn; alle endringer innenfor utvidelsen. Git no-index returnerer1 for nye filer også uten feilutskrift; dette er håndtert som diff, ikke feil. Ingen produkttester eller commit.

## SL-PLAN-1 avleder denne versjonen

Ny brukerbestilling tillater epics/stories; tidligere merknader om at ingen slike genereres er historiske. CAP-1–5 og AC-01–12 er bevart. Memlog SL-D10/11 overstyrer feil265,519m-R2-kandidat og tilføyer kildebundet manifest, R4-kandidat, profil og kvalifiseringsrapport. Kernel/companions er avledet fra oppdatert beslutningsminne. Gjeldende [sluttvalidering](../../planning/validation.md) dokumenterer sammenheng og bevaring; ingen produktgodkjenning.
