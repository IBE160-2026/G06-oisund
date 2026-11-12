# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G06 – G06-oisund |
| **PRD vurdert** | `_bmad-output/planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md` (status `final` i frontmatter, sist endret 2026-10-31, commit e861625). `addendum.md` er også lest. |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

PRD-en er faglig presis der den er konkret: regler for bekreftelse, lagring, feil, tidspunkter og oppbevaring er skrevet så de kan testes, og omfanget er kuttet kraftig siden briefen. Risikoen er formen. Dokumentet er blitt et lagdelt endringsdokument uten egen visjon, glossar eller målemål, så UX, arkitektur og stories må lete etter hva som faktisk gjelder.

## 2. Dette fungerer godt

- **Omfanget er skåret ned og begrunnet.** §5 «SCOPE-02 decisions S02-A–G replace automatic GPS progression with manual selection…» og §2 «Deferred: OCR/scans/images, … GPS/stop progression, … PDF export» er ærlige avgrensninger. Estimatet på 60–80 timer med minst 12 timer reservert til retting og levering (§2) er realistisk.
- **Bekreftelses-, lagrings- og tidsreglene er konkrete.** §6 «An overnight time needs an explicit date/offset; never guess the day from clock order» og «A response lost after commit is resolved by authorized lookup of the same operation; retry does not duplicate effects» kan bli testtilfeller nesten direkte. FR-1 («fixed server session expiry 14 days») og retensjonsreglene (sju dager, opprydding minst hver time) er målbare.
- **Akseptansetabellen i §8 kobler krav, bevis og stories.** «AC-01 … 3–5 anonymized PDFs with independently checked expected facts … not fabricated pass» er riktig type kvalitetssikring. Det står også at KI, GPS og betalte kontoer ikke trengs for lokal kjøring (§2).

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | god | Beslutninger er navngitt (SCOPE-02, S02-A–G) og avveininger er synlige, men de ligger spredt i lag. |
| Substans | sterk | Innholdet er produktspesifikt (Europe/Oslo, ekstended-timer, 7-dagers retensjon). Ingen pynte-personas eller boilerplate. |
| Strategisk sammenheng | svak | Ingen visjon eller problemformulering. §1 beskriver leveransen, ikke hvorfor sjåføren trenger den. |
| Testbarhet | god | AC-tabellen og enkelte FR-er er gode. Andre FR-er er tette tabellrader uten konsekvenser. |
| Scope og avgrensning | god | Utsatt-listen er eksplisitt. Åpne punkter og antakelser er ikke samlet, og omfanget er fortsatt stort. |
| Brukbarhet for neste fase | svak | Ingen glossar. SM-1–SM-5 refereres uten definisjon. Mye hentes fra eksterne dokumenter. |
| Formtilpasning | god | Capability-form passer en enbrukerapp. Brukerreisene (to korte avsnitt) er for tynne for en app med mange tilstander. |

## 4. Viktigste forbedringer

### 4.1 PRD-en er et endringsdokument, ikke et gjeldende krav
- **Alvorlighet:** høy
- **Hvor:** toppnotatet «Current-scope note, 31 October 2026 …», §5 «Old numeric FR identifiers below preserve traceability; deferred rows are not implementation requirements», §9 «historical pre-implementation planning checkpoint»
- **Problem og hvorfor det betyr noe:** Fire lag (SCOPE-02, rettelse 26.10, 11.5-korreksjon, notat 31.10) ligger oppå hverandre. Seks FR-rader er «deferred», og §9 sier både at alle 20 stories er godkjent og at fixtures «still need to be established». En som lager stories eller tester, vet ikke hva som gjelder nå. Frontmatter sier `updated: 2026-10-19`, men teksten omtaler senere hendelser.
- **Forslag:** Skriv én ren versjon av «gjeldende V1». Flytt historikk og statusnotater til et endringslogg-dokument. Samle utsatte FR-er (FR-3, 7–9, 15, 23) i én liste «Utsatt» og behold ID-ene. Oppdater `updated`.

### 4.2 Mange FR-er har ikke testbare konsekvenser
- **Alvorlighet:** høy
- **Hvor:** FR-2 «reviewable unconfirmed draft with field/page uncertainty», FR-16 «No required interaction during driving», FR-17–18 «show … states correctly», FR-19 «stale/unknown check state»
- **Problem og hvorfor det betyr noe:** Ordene «correctly», «reviewable» og «stale» kan ikke bli en test uten at noen bestemmer hva de betyr. FR-17–18 er to krav i én rad, og FR-2 samler import, retting og feilhåndtering.
- **Forslag:** Gi hver FR egen ID og 2–3 «Gitt/når/så». Eksempel for FR-2: *Gitt en fixture-PDF fra AC-01 når sjåføren laster den opp, så vises et utkast med alle turer og pauser fra fasit, felt med usikker tolkning er merket, og planen er ikke bekreftet. Gitt en skannet PDF så tilbys manuell inntasting uten melding om vellykket uttrekk, og forrige bekreftede plan er uendret.* Definer «stale» med en verdi, eller skriv eksplisitt at det ikke finnes noen terskel.

### 4.3 Tese og målemål mangler i selve PRD-en
- **Alvorlighet:** høy
- **Hvor:** §1 «Build one tablet-adapted fullstack website with a database …», §8 «SM-1 … SM-2 … remain unproven field hypotheses»
- **Problem og hvorfor det betyr noe:** PRD-en sier hva som bygges, men ikke problemet (20–30 minutter daglig innsamling av informasjon) eller hvorfor en PDF-import med manuelle varsler løser det. SM-1–SM-5 er ikke definert her, og det finnes ingen motmåling. Etter at GPS og automatisk henting ble utsatt, er det uklart hva som skal gi sjåføren verdi.
- **Forslag:** Legg inn 3–4 setninger om problem og tese øverst. Lag en liten SM-tabell med mål og FR-henvisning, og minst én motmåling, for eksempel «antall manuelle rettinger per importert PDF (SM-C1) skal ikke skjules selv om det er høyt».

### 4.4 Ingen glossar, og begrepene varierer
- **Alvorlighet:** medium
- **Hvor:** §3–§6: «workday», «day», «shift», «plan»; «notice», «incident», «record»; «Vogn», «vehicle duty», «physical bus»; «recap»
- **Problem og hvorfor det betyr noe:** Stories og database-modell vil gjenbruke ulike ord for samme ting. «Vogn» (norsk) står midt i en engelsk tekst.
- **Forslag:** Lag et glossar på 8–12 termer (Workday, Activity, Plan, Notice, Bus, Vehicle duty, Outcome, Recap) og bruk dem uendret. Ta kort inn definisjonen av «supported text PDF».

### 4.5 Åpne punkter, antakelser og ikke-mål er ikke samlet
- **Alvorlighet:** medium
- **Hvor:** toppnotatet «O3–O6 remain open», §9 «Exact December deadline, assessor environment … remain open», §2 «Deferred: …»
- **Problem og hvorfor det betyr noe:** «O3–O6» forklares ikke her, og addendumet viser til en «PRD section 10» som ikke finnes. Ikke-målene ligger i ett langt avsnitt.
- **Forslag:** Legg til en kort «Åpne spørsmål» (nummerert, med eier og frist) og en punktliste «Ikke-mål».

## 5. Mekaniske funn

- FR-1–FR-25 og NFR-1–4 er sammenhengende. FR-7–9 og FR-17–18 er slått sammen og kan ikke refereres enkeltvis.
- FR-ene viser ikke til UJ-1/UJ-2, og UJ-ene har ingen navngitt protagonist. Eksterne lenker (sprint-change-proposal, `docs/submission/...`) er nødvendige for å forstå kravene.
- Ingen `[ASSUMPTION]`-tagger eller antakelsesindeks. Mellomrom mangler i §9 («note,29October2026», «all20»).
- Eiernavn står i toppnotatet. Bruk rolle eller pseudonym som i addendumet.

## 6. Før dere går videre

**Må avklares nå:** (1) hva som er gjeldende V1 (4.1) og hva som er målt (4.3), (2) hva «supported text PDF» betyr, siden AC-01 avhenger av det, og (3) om realismen holder: innlogging, 14-dagers sesjon, samtidighetskontroll, notisregister på tvers av dager og Ubuntu-hosting på 60–80 timer er mye. Si hva dere kutter først hvis tiden knapper.

**Kan vente:** glossar og SM-tabell kan gjøres parallelt med implementering. Terskler for «stale» og nøyaktig innleveringsdato kan avgjøres senere.

**Oppfølging av briefen:** *ja.* Omfanget er kuttet til minimal V1 (PDF med kontroll, manuell navigering, manuelle varsler). GPS, offline og PDF-eksport er utsatt. Akseptansekriteriene bruker anonymiserte PDF-er med fasit. Hosting er tatt inn igjen (31.10), så vær bevisst på omfanget.

## 7. Refleksjonsspørsmål

1. FR-ene har blitt endret flere ganger gjennom «korreksjoner». Hvordan sjekket dere at KI-endringene ikke skapte motsigelser mellom §6 og §8, og hva forkastet dere?
2. §1 sier «It does not certify standstill or provide live driving guidance». Hvilke KI-forslag avviste dere for å holde grensen, og hva viser at appen holder seg på riktig side?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
