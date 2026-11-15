---
title: "PRD – oppfølging og kontroll mot faglærerens kritikk"
created: 2026-11-15
updated: 2026-11-15
status: documentation-review
source_commit: 4d97c76ed7557793ce407c7f6cf6f2c269307475
---

# PRD – oppfølging og kontroll mot faglærerens kritikk

## 1. Kilden som faktisk ble funnet og lest

Faglærer **Bård Pettersen** la til [tilbakemelding-prd.md](https://github.com/IBE160-2026/G06-oisund/blob/e01712c801c7113eae15cc1656f2f4bce4898746/_bmad-output/planning-artifacts/prds/prd-IBE160-2026-09-21/tilbakemelding-prd.md) i [commit e01712c](https://github.com/IBE160-2026/G06-oisund/commit/e01712c801c7113eae15cc1656f2f4bce4898746), 12. november 2026. Commitens forfatter og filens innhold er kontrollert. Kilden kaller dette formativ veiledning, ikke karaktersetting.

Tilbakemeldingen identifiserer [prd.md](prd.md) med `status: final`, sist endret 31. oktober ved `e861625`, samt [addendum.md](addendum.md). Den vurderte PRD-en er dermed allerede en SCOPE-02-revisjon med senere notater, ikke en urørt septemberplan. Den større opprinnelige PRD-en finnes separat i [arkivet før SCOPE-02](../../archive/pre-scope-02-2026-10-19/prds/prd-IBE160-2026-09-21/prd.md.txt).

Leveransen er [prd-revised-v1.0.1.md](prd-revised-v1.0.1.md), med [README](README.md) som leserveiledning. [Original PRD i egen historisk fil](prd-historical-before-feedback-2026-11-12.md), addendum, faglærerens tekst, historiske beslutninger og godkjent refleksjon er bevart byteidentisk mot kontrollert GitHub-main. Etter eierens presisering før publisering har den gamle `prd.md`-adressen fått et historikknotat over uendret kravtekst; eksisterende avsnittslenker beholdes. Revisjonen er uttrykkelig datert etter ferdigstilt V1 og publisert V1.0.1, og gjør dokumentasjonsrettelser, ikke kodeendringer eller ny produktaksept.

## 2. Faglærerens uttrykkelige kritikk og min vurdering

Tabellen parafraserer kilden. «Egen vurdering» er redaksjonell analyse etter kontroll av dokumentasjon/kode, ikke nye uttalelser fra faglæreren. Forslag til utforming i kritikken blir ikke automatisk nye produktkrav.

| ID / kildepunkt | Faglæreren uttrykkelig | Egen vurdering mot faktisk prosjekt | Gjennomført tiltak og kontroll |
|---|---|---|---|
| K1 – §4.1, høy | Flere endringslag gjør gjeldende V1 uklart; utsatte FR-er står mellom aktive; §9 blander godkjente stories med fremtidig fixturearbeid; `updated` er gammel. Foreslår ren V1 og egen historikk. | Enig i dokumentasjonsproblemet. Implementasjon/aksept og V1.0.1-release finnes allerede. Gamle fixture-/Epic12-/O3–O6-notater kan ikke brukes som bevis for manglende funksjonalitet. | Ny samlet PRD med oppdatert metadata og klar versjonsgrense (§1–2), aktive FR-er (§5), separat utsattliste (§9). Historikken er samlet i denne filens §3. Originalene er ikke omskrevet. |
| K2 – §4.2, høy | FR-2/16/17–18/19 har vage ord uten testbare konsekvenser; FR-2 samler flere handlinger, FR-17–18 deler én rad. Foreslår egne ID-er og 2–3 Gitt/når/så, samt terskel eller eksplisitt fravær av terskel for «stale». | Kode/tester beskriver allerede konkrete feil-, lagrings- og kontrolltilstander. `checked_at`/`checked_revision` skiller ukontrollert fra kontroll før siste endring. Det finnes ingen tidsbasert ferskhetsterskel. Trafikksikkerhet kan ikke bevises ved en UI-test. | Alle 19 aktive FR-er har 2–3 kriterier i §5. FR-2a/b/c skiller import, retting og feil uten å erstatte FR-2-identiteten. FR-17/18 står hver for seg. FR-16 avgrenser faktisk betjening uten å love stillstandsdeteksjon; FR-19 definerer revisjons-/kontrollsemantikk og ingen tidsgrense. §8 kobler til eksisterende bevis. |
| K3 – §4.3, høy | Problem/tese og SM-1–SM-5 mangler i selve PRD-en. Verdien uten GPS/automatisk henting er uklar; motmåling mangler. | Problemet og 20–30-minuttersanslaget står i briefen; 10–15 minutter er en hypotese. Originale SM- og motmåle-ID-er finnes i septemberarkivet, mens SM-3/4 er omdefinert av SCOPE-02. Ingen kilde dokumenterer feltgevinst. | §1 gir problem/tese med kilde og begrensning. §8 definerer alle SM-er, FR-kobling, målt/ikke målt og SM-C1/C2. PDF-rettinger knyttes til eksisterende motmåling for manuelle inngrep, uten ny grense, målt verdi eller instrumentering. |
| K4 – §4.4, medium | Manglende glossar og varierende ord for dag/plan/avvik/vogn/buss/oppsummering; støttet tekst-PDF må defineres kort. | Begrepsforskjellene er viktige i faktisk datamodell. Generell «tekst-PDF» overdriver støtten; privatimporten er smalere enn generelle tidskontroller. | §3 samler 12 termer med entydig norsk hovedbegrep og kodealias, samt konkret layout-, størrelse-, side-, prosess- og kalendergrense. Vognløp og fysisk buss er separate. |
| K5 – §4.5, medium | Åpne spørsmål, antakelser og ikke-mål er spredt. O3–O6 forklares ikke. Addendum peker til en §10 som ikke finnes i vurdert PRD. Foreslår åpne spørsmål med eier/frister og punktvis ikke-mål. | Nyere vedlikeholdsrapport endrer O3–O6-status. De åpne spørsmålene kan samles, men manglende frist/godkjenning må ikke fylles inn. Addendumets §10 finnes i den arkiverte september-PRD-en. | §9 gir ikke-mål; §10 gir merket antakelsesindeks, nummererte åpne spørsmål med roller og eksplisitt udokumenterte datoer, samt forklaring/status for O3–O6. Historisk §10-henvisning er avklart i denne filens §3. |
| K6 – §3 og §5 | Brukerreisene er for tynne, mangler navngitt protagonist, og FR-ene viser ikke til UJ-1/UJ-2. | Flere reelle overganger må beskrives: import er ikke lagring, lagring er ikke bekreftelse/start, og valg er ikke fullføring. Feil/gjenoppretting og vurderingsmiljøet er vesentlige. | §4 gir Alex/Kim som eksplisitte pseudonymer med normal-, feil- og avslutningsflyt. Alle aktive FR-overskrifter viser relevante UJ-er. |
| K7 – §5 | FR-7–9 og FR-17–18 kan ikke refereres enkeltvis. | Historiske ID-er må overleve, selv om tre av dem er utsatt. Å renummerere ville bryte eksisterende matriser. | FR-17 og FR-18 er egne krav; FR-7, FR-8 og FR-9 er egne rader i §9 med opprinnelig betydning. Ingen gammel ID slettes eller gjenbrukes til en ny funksjon. |
| K8 – §5 | Eksterne dokumenter er nødvendige for å forstå selve kravene. | Bevis bør fortsatt lenkes, men daglig kravlesing skal ikke kreve rekonstruksjon fra flere rettelser. | §3–8 samler nødvendig inputdefinisjon, brukerreise, atferd, bekreftelse, tidsregler, lagring, avvik, retensjon, NFR og akseptanse. Lenker gir proveniens og testdetaljer, ikke skjulte hovedkrav. |
| K9 – §5 | Ingen `[ASSUMPTION]`-tagger/indeks; manglende mellomrom i §9; eiernavn i toppnotat bør erstattes av rolle/pseudonym. | Dette er formrettelser, ikke behov for nye personas, prognoser eller privat bakgrunn. | Ny tekst bruker roller og eksplisitte pseudonymer, leselig mellomrom/datoformat, oppdatert frontmatter og tre kildebundne antakelser. Historiske originalfiler/navn er ikke anonymisert på nytt. |
| K10 – §6, må avklares | Gjeldende V1, hva som er målt og betydningen av støttet tekst-PDF må avklares nå. | Dette kan avklares mot release, kode og tidligere evidens. Manglende feltmålinger må stå som manglende målinger, ikke som implementasjonsfeil. | PRD §2/3/8 gir direkte svar: levert V1.0.1, avgrenset input, dokumenterte funksjonsprøver og ikke målt feltgevinst. |
| K11 – §6, må avklares | Realismen i 60–80 timer må vurderes, med kutt hvis tiden knapper; innlogging/sesjoner/samtidighet/kontoeide avvik/Ubuntu er mye. | Bekymringen var rimelig for planleggingen, men oppgaven skjer etter levert V1.0.1. Disse delene finnes og har avgrenset evidens. Faktisk samlet timebruk er ikke dokumentert. Det ville være uriktig å lage en ny historisk begrunnelse eller uautorisert kuttliste i levert funksjonalitet. | §9 forklarer det historiske estimatet, testreserven, allerede vedtatte kutt og senere inkludering av ferdig Ubuntu. Utvidelser er ikke kurskrav. Q-6 beholder faktisk tidsbruk som ukjent. |
| K12 – §7, refleksjon 1 | Hvordan ble KI-korreksjoner kontrollert for motstrid mellom krav og akseptanse, og hva ble forkastet? | Sporbarhetsmatrise, uavhengige fasiter, versjonsbinding, konkrete feil/reruns og personlig avvisning av 12.4-flyten gir dokumenterbare svar. De beviser ikke at alle historiske KI-forslag er registrert. | Denne filens §5 oppsummerer bare dokumenterte kontroller og avvisninger. Godkjent personlig refleksjon er uendret; manglende historikk er ikke fylt ut. |
| K13 – §7, refleksjon 2 | Hvilke KI-forslag ble avvist for å holde grensen mot kjøreveiledning, og hva viser at appen holder grensen? | SCOPE-02 utsetter GPS, automatiske overganger/bevegelseslås og offlinearbeid. Det er verifiserbart som omfangsvalg, men ikke nødvendigvis en dokumentert liste over enkeltforslag fra KI avvist av sikkerhetsgrunner. | §5 i denne filen skiller dokumentert omfangsbeslutning fra ukjent personlig begrunnelse. PRD FR-6/10/11/16/21 gir konkrete grenser; ingen feltmålt sikkerhetseffekt hevdes. |

Faglærerens positive funn er også beholdt: tydelige bekreftelses-/lagrings-/tidsregler, faste sesjons- og retensjonsfrister, eksplisitte utsatte funksjoner og en akseptansetabell med uavhengig fasit. Revisjonen forenkler presentasjonen uten å fjerne disse egenskapene.

## 3. Historikk og retting av historiske krysshenvisninger

| Tidspunkt / kilde | Hva det etablerer | Hvordan det brukes nå |
|---|---|---|
| September-PRD og addendum | Større opprinnelig V1; SM-1–SM-5, SM-C1/C2 og §10-register for daværende beslutninger/validering. | Historikk. Addendumets «PRD section 10» viser til [denne arkiverte PRD-en, §10](../../archive/pre-scope-02-2026-10-19/prds/prd-IBE160-2026-09-21/prd.md.txt), ikke en manglende nåseksjon. Nytt gjeldende spørsmålregister finnes i revidert PRD §10; det kopierer ikke gamle uløste punkter som om de fortsatt var åpne. |
| 19. oktober, SCOPE-02 | Eiergodkjent reduksjon fra åtte epics/80 stories til fire/20, manuell aktivitetsvalg/avviksvedlikehold, online lagring og mindre oppsummering. | Produktavgrensning; de gamle sensings-/offlinekravene gjeninnføres ikke. 60–80 timer var et anslag på dette tidspunktet. |
| 26. oktober, 11.5-korreksjon | Kontoeide avvik som gjenbrukes på tvers av dager, påkrevd slutt, forlengelse før frist og separat historikk/retensjon. | Samlet i FR-12–14/19/24 og felles regler; ikke per-dag-kopiering fra tidligere modell. |
| 28.–29. oktober, 12.4/C1/D1–D3/Epic12 | Praktiske flytrettelser, konkret test- og enhetsevidens, personlig aksept og integrasjon. | «Fixtures gjenstår» og «Epic12 åpen» i gamle kontrollpunkter er ikke gjeldende implementasjonsstatus. Historiske testversjoner beholdes. |
| 31. oktober, V1.0.0 | Ubuntu-integrasjon uttrykkelig inkludert, release og etterfølgende deploy ved fast SHA. | Erstatter tidlig hosting-utsettelse for levert V1. Drift har egne bevisgrenser. |
| 4. november norsk tid, V1.0.1 | Vedlikeholdsrelease ved `1501104`. O3/O5 fullført innen omfang; O4 administrativt lukket med begrensninger; O6 utført vedlikehold/triage, restoppfølging består. | Gjeldende dokumentert vedlikeholdsstatus. Oppføringens UTC-publisering er 3. november 23:22; lokal dato er 4. november. |
| Passordgren til `29a77ff`, journal 4.–5. november | Implementert V1.1.0-kandidat, delvise praktiske pass, konkret mislykket kodeoverlevering og senere tekniske rettelser. | Kandidat, ikke V1.0.1-funksjon eller dokumentert V1.1.0-release. Nye praktiske porter er fortsatt åpne. |
| 12. november, lærerens `e01712c` og `4d97c76` | PRD-kritikk og teknologireferanse lagt til main. | Grunnlag for denne dokumentasjonsoppgaven; ingen ny produktimplementasjon. |
| 15. november, denne revisjonen | Samlet PRD, oppfølgingsmatrise og leserveiledning; etter eierens presisering også eksplisitt historisk originalfil og lesernotat på gammel adresse. | Revisjon etter ferdigstilt V1 og faglærerens tilbakemelding. Originalens innhold er bevart i egen fil; ingen kodeendring eller ny produktaksept. |

To presiseringer ble funnet ved egen implementasjonskontroll, utover lærerens uttrykkelige punkter:

1. **PDF-grensen:** `private_import.py::interpret` avviser ukvalifiserte kalenderforhold. «Manuell Oslo-tid er støttet» må ikke bli et løfte om import av alle PDF-er over klokkeomstilling. Revidert §3 sier dette eksplisitt.
2. **Backup:** Originalens generelle «No historical private backups» er ikke dekkende etter inkludert Ubuntu-drift. Driftsguiden og godkjent refleksjon dokumenterer backup og skiller aktiv database fra kopier. Revidert §6 beskriver faktisk grense uten å innføre ny oppbevaringspolicy eller love sletting som ikke er verifisert.

## 4. Kilde- og implementasjonskontroll

### Kontrollert versjonsgrunnlag

- GitHub-repository: `IBE160-2026/G06-oisund`; remote main ved lesingen: `4d97c76ed7557793ce407c7f6cf6f2c269307475`.
- V1.0.1-tagobjekt: `7c2620348a79e761e34c477c96df11c8e4862489`, peker til commit `15011042b1fe093becbe68177e6396e456b1f35f`. GitHub-release og lokal objektidentitet er kontrollert; dato er presentert i Europe/Oslo.
- Nyere main avviker fra V1.0.1 bare ved to faglærerfiler. App-, frontend- og deploygrunnlag er uendret mellom disse referansene.
- Passordgrenens lokale HEAD og undersøkte GitHub-HEAD er begge `29a77ff95cc7607b81c3351375771b6b23d2d1dd`. Grenens kode/status/journal er lest som eget bevisgrunnlag.
- Automatisk avviksgren er kontrollert mot `da867072a8a17249032c00efa51bd61979d41428`; README beskriver eksplisitt planlegging uten implementasjonsaksept.

Arbeidet ligger i en separat lokal checkout på `codex/prd-feedback-clean-20261115`. Den opprinnelige arbeidskopien og produksjonen er ikke endret. GitHub-koblingen ble brukt til kildeoppslag; lokale historikkobjekter og de to nye GitHub-filene ble brukt til en checkout med nøyaktig samme commit/tree-identitet som undersøkt main. Dette gir et etterprøvbart grunnlag uten å utgi et eldre lokalt snapshot for å være nyeste main.

### Dokumenter og kildekode som underbygger revisjonen

| Område | Kontrollgrunnlag | Hva det faktisk underbygger |
|---|---|---|
| Problem/omfang | `product-brief.md`, `sprint-change-proposal-2026-10-19.md`, vurdert `prd.md` og addendum, arkivert PRD | Eierens anslag/tese, SCOPE-02 og opprinnelige ID-er; ikke feltmåling eller dagens implementasjon alene. |
| Import | `backend/app/pdf_import.py`, `private_import.py`, `workday_domain.py`, `docs/submission/supported-input.md`, parser-/importtester og 12.4-evidens | Grenser, kjente/ukjente felt, kalenderavvisning, eksplisitt lagring/bekreftelse. Manuell retting er ikke automatisk parsersuksess. |
| Manuell bruk | `workday_domain.py`, eksisterende krav-/testmatrise med `test_private_selection.py`, `private-selection.spec.ts`, `private-outcomes.spec.ts` | Eksakte aktivitets-ID-er, ingen implisitt start/fullføring og terminal avslutning. Ingen stillstands-/sikkerhetsmåling. |
| Avvik | `backend/app/notice_reader_domain.py`, `frontend/src/PrivateNoticeReader.tsx`, `PrivateNotices.tsx`, konto-/lesertester og 11.5-evidens | Eksakte linjer/planintervaller, gjenbruk, separat gyldighet, ukjent kildeoppdatering, `checked_at`/`checked_revision`, ingen aldersbasert ferskhetsterskel. |
| Lagring/tilgang/retensjon | `frontend/src/recoverOperation.ts`, auth-/lagringskode og eksisterende tester/11.6/12.1-matrise | Opprinnelig operasjonsidentitet, autorisert gjenoppretting, revisjonsvern, faste frister og avgrenset servertilstand. |
| Akseptanse | `docs/submission/traceability.md`, C1-aksept/integrasjon, 12.5-reproduksjon og V1-sluttkontroll | Allerede utførte avgrensede resultater med egne versjoner, faktisk fysisk aksept og ren lokal oppskrift. Ikke nye kjøringer på denne revisjonen. |
| Drift | V1.0.1-release, vedlikeholdsrapport, `delivery-readiness.md`, `known-issues.md`, `ubuntu-server.md` og O6-overlevering | Oppdatert O3–O6-status, kildesnapshot kontra sist rapporterte produksjon, backupgrense og eksisterende restpunkter. |
| V1.1.0 | Passordgrenens `implementation/status.md`, eierjournal, funksjoner/ruter i `auth.py`, `password_recovery.py` og `private_main.py` | Implementert kandidat og delvis eierkvalifikasjon; praktiske porter/release er fortsatt separate. |
| Refleksjon | Godkjent `docs/submission/ai-reflection.md`, SCOPE-02 og 12.4-erfaringsrapport | Dokumenterte erfaringer og avvisning av friksjonsfylt flyt. Ingen nye personlige minner tilskrives prosjekteieren. |

### Kontroll av resultatet

Dokumentkontrollen omfatter følgende, uten appkjøring:

- Dekning av K1–K13 og alle fem prioriterte forbedringsområder.
- Bevarte FR-1–FR-25: 19 aktive med egne kriterier og seks utsatte med egne rader; FR-17/18 hver for seg, NFR-1–4 og AC-01–12 bevart.
- Alle aktive FR-er koblet til brukerreise; SM-1–5, eksisterende SM-C1/C2 og merket antakelsesindeks definert.
- Refererte lokale dokumenter, kodefiler og teststier kontrollert for eksistens; nye dokumentlenker/overskriftsankre kontrollert.
- Historisk originalkopi, addendum, kritikk og refleksjon kontrollert byteidentiske mot base. `prd.md` har bare fått historikknotatet; tidligere kravtekst og avsnittslenker er uendret. Ingen backend-, frontend-, deploy- eller produktkonfigurasjonsendring.
- Git-whitespacekontroll av dokumentene og lokal endringsoversikt.

App-/nettlesertester, fysisk eiertest, feltmåling, produksjonsinspeksjon og deploy er **ikke kjørt i denne økten**. Eksisterende resultater omtales med opprinnelig bevisgrense; de ommerkes ikke til ferske tester. Produktets faktiske restpunkter videreføres; dokumentasjonen lukker dem ikke.

## 5. Dokumenterbare svar på refleksjonsspørsmålene

**Kontroll av KI-endringer og motstrid:** SCOPE-02 endret brief, PRD, UX/arkitektur og backlog samlet. Den eksisterende sporbarhetsmatrisen knytter FR/AC/NFR til stories, konkrete testselektorer og datert evidens. Uavhengige PDF-fasiter og faktisk API/PostgreSQL- og nettleserprøving gir andre kontroller enn bare å lese generert tekst. C1-/integrasjonsrapportene binder resultatene til bestemte kilder og skiller reelle prøver fra simulerte feil. I denne revisjonen er hver aktiv FR konkretisert mot disse reglene, og historiske statussetninger holdt utenfor gjeldende krav.

En dokumentert avvisning er at prosjekteieren ikke godtok 12.4-flyten selv etter beståtte tekniske og fysiske kontroller, fordi gjennomgang og redigering var for gjentakende. Flyten ble rettet før senere godkjenning. Godkjent refleksjon sier også at omfanget hadde fått vokse for mye med KI-støtte, og at reduksjonen var nødvendig for realistisk gjennomføring med begrenset tid. Det finnes ikke grunnlag her for å rekonstruere en uttømmende liste over alle forkastede KI-forslag eller påstå at alle historiske kravkonflikter ble funnet med én bestemt metode.

**Grensen mot kjøreveiledning:** SCOPE-02 og levert kode bruker manuelle aktivitets-ID-er og uttrykkelige handlinger fremfor GPS, hastighet, automatisk progresjon og overgangstimere. Avvik er manuelt registrert kildeinformasjon; ukjent/ufullstendig dekning er synlig, og valgt aktivitet gir ikke nøyaktig holdeplassrelevans. Tester av valg/start/utfall dokumenterer at valg ikke alene betyr utført arbeid. Dette underbygger den funksjonelle grensen, men ikke trafikksikkerhet eller korrekt bruk i trafikken.

Omfangsvalgene er dokumentert, men kildene viser ikke en komplett liste over særskilte KI-forslag som eieren avviste *med sikkerhet som uttalt begrunnelse*. Det ville være en etterkonstruert personlig refleksjon å skrive en slik liste. Den godkjente refleksjonsrapporten er derfor ikke endret.

## 6. Kort sluttkontroll mot kritikken

| Faglærerens kritikk | Tiltak gjennomført | Fil/avsnitt | Eventuelt uavklart |
|---|---|---|---|
| Lagdelt PRD/uklart gjeldende V1 | Samlet revisjon, versjonstabell, atskilt historikk og utsatte FR-er; oppdatert metadata | `prd-revised-v1.0.1.md` §1–2/9; denne filen §3 | V1.1.0 er kandidat, ikke utgitt. |
| Vage FR-er/sammenslåtte ID-er | 2–3 Gitt/når/så per aktiv FR; FR-2a/b/c; FR-17/18 adskilt; konkret kontroll-/lagringssemantikk | Revidert PRD §5–6 | Ingen aldersbasert «stale»-terskel finnes; dette er nå uttrykkelig. |
| Manglende problem/tese, SM og motmåling | Problem og avgrenset verdihypotese; SM-1–5 og SM-C1/C2 med kilder og evidensstatus | Revidert PRD §1/8 | Netto tidsgevinst og feltdekning er ikke målt. |
| Begrepsvariasjon/uklar tekst-PDF | 12-termers glossar og presis input-/kalendergrense | Revidert PRD §3 | Vilkårlige PDF-layouter er ikke støttet. |
| Spredte åpne punkter/antakelser/ikke-mål og feil §10-henvisning | Samlet register med roller og kjente fristgrenser; O3–O6 forklart; historisk henvisning oppklart | Revidert PRD §9–10; denne filen §3 | Kurslogistikk, O6-rester og enkelte driftsbevis består. Frister er ikke diktet opp. |
| Tynne brukerreiser/sporbarhet og mekaniske funn | Pseudonymer, normal-/feilflyt, FR→UJ, tydelig ID-/AC-/NFR-struktur, lesbar tekst | Revidert PRD §4–8 og metadata | Ingen ny brukerhistorikk eller produktgodkjenning påstås. |
| Realisme og hva som kuttes først | Historisk estimat skilt fra levert arbeid; vedtatte kutt/testreserve og separate utvidelser forklart | Revidert PRD §9–11 | Faktisk samlet timebruk er ikke dokumentert. |
| Refleksjon om KI-kontroll og kjøregrense | Kildebelagte kontroller/avvisninger og eksplisitte kunnskapsgrenser samlet | Denne filen §5 | Full oversikt over avviste KI-forslag og deres personlige begrunnelser finnes ikke i grunnlaget. |
