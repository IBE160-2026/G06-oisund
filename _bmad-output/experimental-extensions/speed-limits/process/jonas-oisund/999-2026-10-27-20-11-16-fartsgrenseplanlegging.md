# Fartsgrenseplanlegging

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## 2026-10-27 kl. 21:47 — Jonas Øisund

### Oppgave

Etablere separat arbeidsområde og et avgrenset planleggingsgrunnlag for eksperimentell V1.4.0: aktuell registrert vegfartsgrense og fast 300m-forvarsel. Ingen implementering, produkttester, posisjonsinnsamling eller commit. Senere bestilling utvidet leveransen til gjenværende datakvalifisering og ferdige epics/stories.

Ny bestilling samme dato: «Commit og push til egen branch» autoriserer nå commit/push av denne planpakken og sesjonsloggen; øvrige avgrensninger består. Tidligere beskrivelser av ingen commit/push gjelder planleggingsfasen.

### Plan

- Kontrollere Git-identitet og opprette branch/worktree fra nøyaktig lokal committet main.
- Lese rutenett-/posisjonsplaner og V1-arkitektur uten endringer.
- Bruke avgrenset bmad-deep-recon Run med verifisert lokal utdataruting, primærkilder og små offentlige oppslag.
- Skrive [plan](../../plan.md), [grensesnitt](../../interfaces.md) og [research](../../research/technical-speed-limits-2026-10-27/research.md); kontrollere dokumenter og logge her.

### Resultat

Worktree D:/IBE160-plan-speed-limits, branch codex/plan-speed-limits, utgangspunkt 74849ff21bee108fe9cff93d740a96a6c6d2d7c5. Main og referanse-worktrees bevart. Alle nye filer er innenfor speed-limits. Tre offentlige NVDB-objekter, katalog 105 og én original offisiell SVG er lagret som belegg. Katalogens retning_relevant=false hindrer ukritisk tolkning av MED som retningsgyldighet. Full Tromsø-dekning, felt-/reguleringssemantikk og assetlisens er ikke kvalifisert. Begge ønskede visninger beholdes i første plan, med synlig usikkerhet og krav til sammenhengende rettet kjøreveg.

BMAD kildehenvisningskontroll bestått; uavhengig dokumentgjennomgang fant ingen vesentlig kildepåstandsmismatch. Strukturforbedring innarbeidet. Kun dokument-/Git-kontroller, ingen produkttester. Ingen kode, database, tjenester, nettverkstilgangskonfigurasjon eller delt BMAD-konfigurasjon endret. Ingen commit/push/merge, etter uttrykkelig instruks som overstyrer sesjonsloggstandardens commit og plassering.

Fortsettelse samme dato: bmad-spec brukt i verifisert lokal mappe specs/spec-speed-limits. Fem capabilities og følgedokumenter for atferd, pilotmanifest, tolv senere AC-er og ikonrettigheter er laget; root README/plan/interfaces er oppdatert. Brukeren avklarte overflatetrasé og slutt etter flyplassrundkjøringen; rettelsen tre underveis/fjerde ved slutt er bevart. PV-1/PV-2 lukket i issues. Kryssnavnene er begrunnede forslag med kildebelegg og konkrete datagap, ikke en fiktivt komplett NVDB-rute. Lite FV7772-oppslag traff Stakkevollvegen og ble avvist som pilotbelegg. Ingen nye skiltfiler eller posisjoner samlet. Tidligere selvvalgt Eidvegen-pilot erstattet. Spec Law sammenheng/bevaring kontrollert, dokumentlenker, additivt diff og whitespace er kontrollert uten funn. Ingen commit, også for denne loggen, etter eksplisitt brukerkrav.

Sluttføring: eksisterende delarbeid i qualification/planning gjenopptatt. To siste små NVDB-oppslag fullførte rammen45oppslag/1 597 560byte. Råhashene stemmer. V830-feltreglene avdekket feil R2/R3-buer i foreløpig kandidat; korrigert R2→R3 er323,808m. R4/70→50 erstatter rundkjøringskandidaten.139 ordnede segmenter uten nodebrudd,8656,655m summert kildelengde, fra1139933 til1138796. Ingen lovnad om fysisk/rutejuridisk godkjenning.

Bmad-spec avledet kernel/pilotmanifest/teknisk tillegg etter oppdatert memlog. Bmad-create-epics-and-stories fullført gjennom fire steg: én epic og sju stories med BDD, avhengigheter og FR/NFR/UX/AC-sporing. README/plan/interfaces og statuser er samordnet. EPS/NLOD valgt rettighetsspor; faktisk assetleveranse og fysisk kvalifisering er senere kriterier. Dokumentkontroller og diff finnes i [sluttvalideringen](../../planning/validation.md). Kun kilde-/dokumentkontroller; ingen produktkode eller produkttester. Ingen commit/push/merge. Alle skriveruter er innenfor utvidelsen.

Publisering etter eksplisitt bestilling: planleggingspakken er committet som 647f570fdf766b9b4303ac790cbef7d99e57ffa4 og pushet til origin/codex/plan-speed-limits. Remote-hash er verifisert med ls-remote. Commiten inneholder99 filer, kun under utvidelsen. Én blanklinje ved EOF i researchskriptet er fjernet. Utvidelseslokal .gitattributes bevarer rå JSON/JSONL/CSV/SVG uten linjeskiftkonvertering; alle44 vellykkede responsfiler fra45 forespørsler har korrekte SHA-256 også i Git-indexen. Staged Markdown/Python/attributter passerte whitespace-kontroll. Sesjonslogg og issues føres i separat loggcommit etter prosjektoppskriften. Ingen merge, implementering eller produkttester; main/referanse-worktrees er ikke endret. Ingen nye åpne produktpunkter fra publiseringen.

Presisering SL-D12: brukeren krever ny korridor gjennom manifest/kvalifiserte vegdata uten endring i matching-, grenseevaluerings- eller varslingskjernen. Spesifikasjon, grensesnitt, teknisk tillegg, pilotmanifest og eksisterende stories er samordnet i SL-PLAN-1.1. Pilotnavn/ID-er/rundkjøringer er kun data/testgrunnlag. Flere avgrensede pakker har eksplisitt kobling, kompatibilitet, overlapp-/konfliktbehandling, samlet budsjett og fysisk passeringsidentitet. NFR5 og AC-13/14 dekker korridorbytte og pakkegrenser. Fem CAP-er og sju stories beholdes. Dokumentlenker, struktur og diff kontrollert; ingen produkttester eller ny datainnsamling. Dokumentcommit8790b13b73fa4f94bc72ee736498f6a2359ea899; publisering fortsetter på samme branch etter tidligere commit/push-bestilling. Rådata er uendret.

### Åpne punkter

- QF-6: Senere AC-13/14 må bekrefte korridorbytte uten kodeendring og korrekt behandling av flere datapakker, jf. NFR5/stories1.1/1.3–1.6.

- QF-1/2 og QF-2b: Operativ kilde-/felt-/svingdekning, midlertidig/variabel regulering og faktisk ikonmanifest gjenstår i stories1.1/1.2/1.7.
- QF-3/4: Senere implementasjon/verifikasjon og fysisk profil/akseptvindu; kildeobservasjoner erstatter ikke GPS-kvalifisering.
- QF-5: Ferdig/testet V1 og kvalifiserte avhengigheter samt separat bygg-/fysisk testbestilling.

Speilet i [issues.md](issues.md). PV-1/PV-2, kildeplanlegging QF-1a og ferdig epic/storyplan QF-3a er løst. Neste aktivitet er avhengighets-/beredskapsarbeid, ikke ny full planleggingsrunde. Ingen nye produktvalg kreves nå.
