# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G06 – G06-oisund |
| **Product brief** | `_bmad-output/planning-artifacts/briefs/brief-IBE160-2026-09-21/brief.md` (commit `b3856aa`). `product-brief.md` i samme mappe er identisk, og det er den PRD-en viser til. `addendum.md` er også lest. |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Bør revideres før dere går videre.** Rett punktene markert «Endre» før dere lager PRD og arkitektur.

Dere har allerede laget PRD, UX, arkitektur og epics. Revisjonen gjelder derfor først og fremst omfanget: det bør skjæres ned og rettes opp i brief og PRD før dere begynner å implementere.

**Det som er bra:**

1. Problemet er uvanlig konkret og godt dokumentert. Det bygger på en reell bruker (en bussjåfør i Tromsø), konkrete kanaler (Selfservice, SMS, NavCon, Svipper), et anslått tidsbruk på 20–30 minutter per dag og funn fra elleve vaktrapport-PDF-er. Problemet er også avgrenset til fire pilotlinjer (20, 24, 28 og 42).
2. Avsnittet «Trust and failure behavior» er svært godt. Det beskriver hva appen skal gjøre når turdeteksjon, henting av avvik eller fartsgrense er usikker, og at kilde-tidspunkt ikke skal blandes med hentetidspunkt. Dette kan bli presise testtilfeller.
3. Dere er ærlige om risiko. Dere skiller mellom simulert demo og ekte vaktbruk, og dere skriver selv at omfanget er ambisiøst for 40–160 timer.

**De viktigste endringene:**

1. **Omfanget er for stort for én person og et semester.** V1 inneholder fire tekniske høyrisikoområder samtidig: tolkning av PDF-er med varierende layout, automatisk turfølging med GPS på overlappende linjer, automatisk matching av Svipper-/Entur-avvik mot turer, og fartsgrenser med varsel 100 meter før endring. Hvert av dem kan alene fylle et semester. Definer en minimal v1 som sikkert kan bli ferdig (se forslag under).
2. **Planen har vokst etter briefen.** PRD og epics har nå 8 epics og rundt 80 stories, i tillegg til detaljerte regler for offline-tid, låsing og enhetsforvaltning (TIME-01). Dette er langt mer enn briefen beskriver, og mer enn det er realistisk å implementere og teste. Bruk *correct course* til å kutte ned i stedet for å bygge ut.
3. **Suksesskriteriene bør få et funksjonelt lag.** Halvert sjekketid over tre arbeidsdager er en god felttest, men den kan ikke bli automatiske tester. Legg til kriterier som «gitt eksempel-PDF X viser oversikten riktige turer, pauser og bussbytter», som kan sjekkes mot fasit.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Vanskelig**

**Sammenlignbart med:** 3) KI-styrt simulering av prosjektledelse (vanskelig). Domenet er et annet, men nivået er det samme: mange moduler som henger sammen, og logikk som må stemme. I tillegg kommer sanntidsdata og eksterne integrasjoner.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | høy | Turdeteksjon på linjer som ligner hverandre (20 og 24), stoppprogresjon, relevansfiltrering av avvik per tur og håndtering av usikkerhet må alle stemme. |
| Datamodell – antall entiteter og relasjoner mellom dem | middels | Vakt, aktiviteter (tur, pause, bussbytte, bilaktivitet), stopp, buss, avvik og demo-data. Det er håndterbart, men relasjonene mellom vakt og rutedata er krevende. |
| Brukere, roller og innlogging | middels | Én sjåførrolle og en separat demokonto i briefen. PRD-en har senere lagt til innlogging, tilbakekalling og enhetskontroll, som øker kompleksiteten betydelig. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | lav | KI i produktet er bevisst flyttet til senere utvidelser. Det er et fornuftig valg. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | høy | Entur sanntid/SIRI-SX, Svipper-trafikkmeldinger og en ennå uavklart kilde for fartsgrenser. Ingen av dem er testet ennå. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | høy | GPS-posisjon, fart og løpende turbytte på nettbrett i bussen, inkludert tap av signal og nett. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | høy | Selfservice-PDF-ene har én eller to kolonner, varierende tetthet og sideskift, og tekstuttrekk blander kolonner. PRD-en legger i tillegg til PDF-eksport. |
| Sikkerhet og personvern | middels | Vaktdata er personlige og driftsmessige. Det er bra at kilde-PDF-ene holdes utenfor det offentlige repoet. |

**Hva vanskelighetsgraden betyr for dere:**

- _Vanskelig:_ Et vanskelig prosjekt gir større mulighet for toppkarakter, men også større risiko. For dere er risikoen ekstra stor fordi dere er alene. Definer en minimal versjon som sikkert kan bli ferdig, for eksempel vaktoversikt fra PDF med manuell korrigering og manuell turnavigering. Legg GPS-følging, automatisk avvikshenting og fartsgrenser i tydelige trinn etterpå, hver med en egen tidlig mulighetssjekk.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | stor risiko | Med 40–160 timer alene og rundt 80 stories er det ikke realistisk å bli ferdig. Dere har brukt mye tid på planlegging, og det er ennå ikke skrevet kode. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | risiko | Briefen er konkret nok, nesten for detaljert. Problemet er at antallet stories har blitt uoverkommelig. Et mål kan være 15–25 stories for v1. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | risiko | En vanlig webstakk passer godt. GPS i en bestemt nettleser på et bestemt nettbrett, offline-drift og SIRI-feeder er derimot nisje, og det er vanskelig å teste med Claude Code. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | OK | Dere har sterk domenekunnskap og kan selv avgjøre om en vaktoversikt eller et avvik er riktig. Det er et stort pluss. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | risiko | Feilhåndteringsreglene og PDF-tolkningen kan testes godt mot anonymiserte eksempelfiler med fasit. GPS-følging og fartsgrense kan bare testes med simulerte spor. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | risiko | Den planlagte demoen med fiktiv vakt og simulert progresjon er riktig grep. Sørg for at den kan startes lokalt etter README, uten ekte vaktdata, nettbrett eller tilgang til egne tjenester. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | OK | Ingen betalt språkmodell i v1. Entur er åpent. Demoen bør likevel bruke lagrede eksempeldata, slik at den ikke er avhengig av at eksterne feeder er tilgjengelige. |

**Konklusjon om gjennomførbarhet:**

- **Lite realistisk uten vesentlige endringer.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. **Minimal v1:** PDF-import med en skjerm der sjåføren kontrollerer og retter tolkningen, manuell registrering av buss, dagsoversikt over turer, pauser og bussbytter, og manuell neste/forrige-tur. Legg til en enkel liste over planlagte avvik for vaktens linjer, med kilde og tidspunkt. Allerede dette er et middels til vanskelig prosjekt.
2. **Trinn 2 og 3, bare hvis v1 er ferdig og testet:** automatisk turfølging med GPS, og deretter fartsgrenser. Kutt eller utsett offline-reglene, enhetslåsing og PDF-eksport fra PRD-en (TIME-01), og noter i PRD-en hvorfor de er utsatt.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | «Purpose and users» forklarer tydelig at dette er en sjåførassistent på nettbrett som samler vakt og driftsinformasjon i én visning, og at den er beslutningsstøtte, ikke erstatning for skilt og instrukser. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Meget konkret: kanaler, tidsbruk, feil fra en tidlig prototype og funn fra vaktrapportene. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | OK | Vaktforberedelse, aktiv tur og planlagte avvik er beskrevet fra sjåførens perspektiv. Teknologivalg er bevisst utsatt. |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Ærlig: én filtrert visning med kilder som kan sjekkes, og dere unngår bevisst å duplisere NavCon. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | OK | Én tydelig primærbruker med kjente behov. Det er en styrke at brukeren deltar direkte i evalueringen. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Juster | Tidsmålet (10–15 minutter) og tre feltdager er gode, men gir bare indikasjoner. Legg til funksjonelle kriterier som kan bli testtilfeller, for eksempel riktig tolket vakt fra en anonymisert eksempel-PDF. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Endre | Det er tydelig hva som er med og ute, men v1 er for stor. Fartsgrenser er kalt «important desired» og samtidig en «delivery risk». Bestem om de er med eller ute av v1. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Møtende busser, KI-prioritering og vær er tydelig plassert som senere utvidelser. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | Sporbarheten fra brief til PRD og stories er svært god, og commit-historikken viser beslutninger. Risikoen er at planleggingen tar all tiden. Sensor ser også etter kode og iterasjoner. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Endre | Kjerneflyten (vakt → aktiv tur → avvik) er tydelig, men alt rundt den gjør det usannsynlig at noe blir ferdig og stabilt. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Juster | Feilhåndteringsreglene er gode testkandidater. Lag anonymiserte eksempel-PDF-er og simulerte GPS-spor med forventet resultat. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | OK | Klar brukssituasjon (nettbrett i førerhuset, kort blikk, kjøring) og gjennomarbeidet UX-dokumentasjon. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Arkitekturen dekker offline, tidskontroll og enhetsforvaltning. Det er mer kompleksitet enn en minimal v1 trenger. Forenkle sammen med omfanget. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | Juster | Demoen er planlagt. Gjør den til standardveien i README, med fiktive data som ligger i repoet. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | OK | Dere holder ekte vakt-PDF-er og kursfiler utenfor repoet, og dokumentasjonen er strukturert. Husk anonymiserte testfiler i en egen mappe. |

## 3. Neste steg for gruppen

1. Kjør *correct course* og skriv ned en minimal v1 (PDF-import med kontroll, manuell buss, dagsoversikt, manuell turnavigering, enkel avviksliste). Marker GPS-følging, fartsgrenser og offline-/enhetsregler som senere trinn i brief, PRD og epics.
2. Gjør mulighetssjekken for PDF-tolkning først: ta 3–5 anonymiserte vakt-PDF-er, skriv ned forventet resultat for hver, og la det bli de første automatiske testene.
3. Start implementeringen snart, med små stories og hyppige commits, og sørg for at demomodusen kan kjøres lokalt etter README fra første utviklingsrunde.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
