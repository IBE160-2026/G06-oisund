# Målekontrakt og produktatferd

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Konsept GS1. Dette er foreslåtte appregler, ikke API-garantier. Begrunnelse GPS-D1–D5 finnes i [research](../../research.md) og [avhengigheter](../../dependencies.md).

## Foreslått grensesnitt

| Grense | Innhold og ansvar |
|---|---|
| Delt kilde → evaluator | contractVersion; watchGeneration; autorisert contextGeneration; lifecycle; speedMps: number/null; acquiredAt epoch-ms; receivedWallMs og receivedMonoMs; lat/lon og accuracyM for begrenset plausibilitetskontroll. Udefinert speed normaliseres til null uten numerisk coercion. |
| Profil → evaluator | profileId/revision, kvalifiseringsstatus og eksplisitte alders-, intervall-, plausibilitets- og RAM-grenser. Manglende profil gir unknown/profile-unavailable. |
| Evaluator → visning | Union: qualified med valueMps, kmhDisplay, acquiredAt, validUntilMono, generation, profileId/revision og origin=browser-reported; eller unknown med reason og generation. Ingen gammel value i unknown. |
| Fartsgrense → samvisning | Separat current.valueKmh/null og status/reason fra grensekontrakten. Ikke et felt i fartsevaluatoren. |
| Senere konsument | qualifiedSpeed beholder m/s, alder, profil og origin; en utløpt prøve er ikke konsumérbar selv om konsumenten oppdaterer sjelden. Ingen tilkobling til dynamisk forvarsel nå. |

Kjerneinput inneholder ingen korridornavn, linjenummer, Quay eller NVDB-ID. «qualified» betyr bare at målingen passerte den valgte profilen. Det finnes ikke dokumentert fartskonfidens å fylle inn; ingen oppdiktet prosent eller speedAccuracy.

## GPS-LAB-1 — uprøvd kandidatprofil

Alle tall nedenfor er eksperimentforslag som må kvalifiseres. Ikke kopier posisjonsplanens illustrative 15 s-alder til fart.

| Parameter | Kandidat | Begrunnelse / risiko |
|---|---|---|
| Fartsalder | strengt < 3000 ms fra acquiredAt | Kort grense, men selv 3 s kan være merkbart under bremsing; S4 må vurdere lavere grense. |
| Koordinataccuracy | 0–30 m, endelig tall | Grov inngangsport; dokumenterer ikke fartens feil. |
| Fartsområde | 0–55,56 m/s | Bred fysisk sanity-grense, ikke veggrense eller korridortilpasning. |
| Oppstart/rekvalifisering | to koherente native prøver, 0,5 ≤ Δt < 3 s mellom måletidene | Forhindrer visning på ett enkelt avvik; forsinker oppstart og kan gi lav tilgjengelighet. |
| Native fartsendring | absolutt Δv/Δt ≤ 12 m/s² når Δt ≥ 0,5 s | Tillater hard bremsing, avviser grove hopp. Ikke bevis på korrekt fart. |
| Grovt posisjonshopp | avvis hvis d > 60 m/s × Δt + accuracy1 + accuracy2 | d er geodetisk avstand mellom to fikser. Bare sanity-filter; accuracy er ikke hard feilgrense. |
| Materialt råfix-gap | ≥ 10 s uten ny tidsordnet, gyldig posisjonsfix | Felles kontroller avbryter og krever manuell resume. Speed=null med ellers god fix er ikke råfix-gap. |
| Klokkeavvik | > 1000 ms endring i wall-minus-monotonic forløp | Invalider sekvens; klokkehopp kan gjøre aldersbevis ubrukelig. Framtidig acquiredAt avvises også ved mindre avvik. |
| Evaluator-RAM | maksimalt to fikser, ingen eldre enn 3 s | Nok til parvurdering; bare skalar tidspunkt for siste råfix kan leve til 10 s-gapfristen. |
| Foreground-visning | ukjent ved frist; målmaks 250 ms til skjermoppdatering | Frist kontrolleres ved hver rendering og med timer, ikke bare ved neste GPS-callback. Nettleserstans er ingen kontinuitetsgaranti. |

Kildekontrollerens tentative watch-opsjoner er maximumAge=0, enableHighAccuracy=true og timeout=10000 ms, avtalt ett sted for alle forbrukere. Dette er ikke en foreskrevet samplingsfrekvens eller en garanti. Timeout og egen ferskhetsfrist har ulike formål. Ingen ekstra polling eller watch for å skjule manglende speed. Begrensningen to fikser gjelder fartsevaluatoren; en annen autorisert forbrukers eksisterende RAM-vindu må fortsatt ha eget tak og felles rydding.

## Deterministisk behandling

1. **Livssyklus først:** avvis gammel generasjon/kontekst. Uautorisert, skjult, paused/off, terminal eller interrupted gir ingen fart og ingen aktiv watch.
2. **Tidskontroll:** acquiredAt må være endelig, ikke framtidig, og nyere enn forrige behandlede timestamp i generasjonen. Duplikater/sene prøver ignoreres uten å fornye fart, RAM-alder eller gapfrist. De gamle tidspunktene kan aldri bli «nå». Framtidig eller ikke-endelig acquiredAt gir straks unknown/time-invalid og manuell resume som klokkeanomali; oppdater aldri rekkefølgeankeret fra denne prøven.
3. **Alder:** ved mottak beregnes initialAge=receivedWallMs−acquiredAt. Senere age=initialAge+(nowMono−receivedMonoMs). Ved alder ≥3000 ms er farten unknown/stale, også uten ny callback. Utløp resetter kvalifiseringsparet før nye målinger behandles. Klokkeanomalier gir interrupted/manual-resume-needed; appen må ikke bruke Math.max(0, age) til å gjemme negativ alder.
4. **Streng verdi-/fixkontroll:** endelige tall, korrekt type, speed ≥0, gyldige lat/lon og accuracy innen profil. null/undefined/NaN/Infinity/negativ eller utenfor profil gir unknown med årsak straks. Ikke Number(null), speed || 0, clamp eller fallback til tidligere verdi. Nye tidsordnede null-/avviste prøver resetter fartskvalifikasjonen.
5. **Kvalifisering:** første gyldige prøve er kandidat, «— / Venter på måling». Andre koherente prøve med riktig intervall kvalifiserer den nyeste native farten. Etterpå brukes hver ny koherent prøve direkte, uten glidende gjennomsnitt. Prøver med Δt<0,5 s kan ikke fornye fart; bevar forrige sammenligningsanker inntil en tidsadskilt prøve kan vurderes, og la vanlig alder løpe.
6. **Hopp:** et grovt koordinat-/fartshopp gir straks unknown/suspect og nullstiller paret. Den avviste prøven kan ikke brukes som kvalifiserende anker. Krev to påfølgende nye koherente prøver; ikke mål alle framtidige prøver mot et permanent gammelt anker. To samsvarende feil kan fortsatt passere: S4 må undersøke det.
7. **Gap:** etter fartsutløp, men før materialt råfix-gap, kan to nye prøver rekvalifisere automatisk innen samme fortsatt autoriserte foreground-økt. Ved ≥10 s råfix-gap, klokkeanomali, posisjonsfeil (TIMEOUT/POSITION_UNAVAILABLE), tilgangstap eller livssyklusavbrudd: stopp, rydd og krev eksplisitt resume. PERMISSION_DENIED krever også gjenopprettet tillatelse. Timer sjekker hardt gap selv uten callback.
8. **Presentasjon:** bruk nyeste kvalifiserte valueMps×3,6. Rund nærmeste heltall med halv opp for ikke-negative tall. Eksakt 0 vises 0; positiv verdi som runder til 0 vises «<1». Ingen deadband som setter små positive tall til 0.

Tidsordnet null-speed kan gi vedvarende «Fart utilgjengelig» mens posisjon er tilgjengelig. Den skal ikke automatisk stoppe andre autoriserte posisjonsforbrukere. En ugyldig tidsordnet prøve kan aldri fornye en tidligere kvalifisert fart. Fremtidig timestamp setter ikke et forgiftet høyt rekkefølgeanker.

## Stillstand, drift og dynamikk

Native 0 er en gyldig måling, med samme kvalitets-/alderskrav som andre tall. Manglende heading etablerer ikke stillstand. Posisjonsdrift alene skaper ingen beregnet fart. Små positive native verdier ved fysisk stillstand kan være støy; første kandidat skjuler ikke dette med heuristisk 0. Dersom S4 ikke kan skille stillstand fra kø med akseptabel kvalitet, er profilen ikke kvalifisert. Produktvalget blir ny dokumentert metode eller fortsatt ukjent/ikke-støttet, ikke en stille deadband-endring.

Uten ekstra filter følger farten nyeste kvalifiserte måling ved akselerasjon og nedbremsing. En brå, avvist endring gir «—», ikke holdt høy fart. Ingen interpolerte verdier mellom prøver. To-prøvers oppstart/rekvalifisering og ukjent intern plattformutjevning inngår i målt total forsinkelse. En senere filterkandidat må versjoneres og dokumentere maksimal ekstra forsinkelse for både start og stopp.

## Visning og livssyklus

Eksempel: **Egen fart (GPS): 42 km/t** ved siden av **Registrert fartsgrense: 50 km/t**. Grensen beholder sin egen skiltsemantikk; egen fart er vanlig tekst/tall, ikke et grenseskilt. Ved ukjent fart: **— km/t** og kort årsak som «Venter på måling», «Fart utilgjengelig», «Målingen er for gammel» eller «Gjenoppta måling». Ingen falmet gammel fart i hovedfeltet. Friskhet/årsak skal kunne leses uten farge alene; ingen overskridelsesfarge eller alarm.

Bevar lesbar Day/Night, responsiv plassering, tastaturfokus og tilgjengelig navn som inkluderer enheten. Ikke annonser hver fartsoppdatering som live region; annonser betydningsfull statusendring uten repetisjon. Samvisningstester omfatter kjent/kjent, kjent/ukjent, ukjent/kjent og ukjent/ukjent.

Off → eksplisitt Start → acquiring → qualified/unknown. Pause og avbrudd gir manual-resume-needed; Off krever ny Start. Skjult side, låst skjerm, pagehide/reload, tilgangssuspensjon, utlogging/utløp, avsluttet arbeidsdag og kontekstbytte invaliderer generasjon, fjerner fart og rydder RAM. Retur krever først eksisterende tilgangsrevalidering og deretter eksplisitt start/resume. Ved midlertidig tilgangssuspensjon skjules privat visning helt.

Start/resume for fart alene krever ikke et stoppeanker. Progresjon følger fortsatt posisjonsplanens manuelle forekomstvalg; fart kan ikke aktivere den, endre valgt aktivitet, registrere passeringer/utfall eller endre arbeidsdag. Felles Pause/Off stopper alle posisjonsabonnementer. Detaljert delingsvalg: [dependencies.md](../../dependencies.md).
