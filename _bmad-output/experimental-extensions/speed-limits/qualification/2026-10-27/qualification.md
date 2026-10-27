# Kildekvalifisering — SL-Q1 / 2026-10-27

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Resultat: **avgrenset kilde- og topologikvalifisering ferdig for planlegging; ikke fysisk validert eller klar til bruk**. Korrigert planrute har 139 kildesegmenter, ingen nodebrudd og 8656,655 m summert kildelengde. Alle svingebegrensninger, faktisk skilting og GPS-kvalitet er ikke erklært bestått. Se [reproduserbar lokal kontroll](qualify-local.py), [kontrollresultat](local-audit.json) og [ordnet kildekjede](source-bound-route.json).

## Metode og belegg

45 lesende oppslag, 1 597 560 responsbyte totalt, ingen automatisk helkommunehøsting. Kildene er Kartverkets offentlige adresse-API og NVDB Les V4. Maks45 oppslag /3MB per respons var satt som ramme. Alle URL-er, UTC-tider, feil, størrelser og SHA-256 ligger i [requests.jsonl](requests.jsonl); råsvar og det avgrensede innsamlingshjelpeskriptet ligger her. HTTP200 betyr teknisk svar, ikke rett rute eller fullstendig regulering. Adresser er offentlige søkeankre, ikke vegpunkter eller innsamlede GPS-fikser. Fuzzy søk og privatvegtreff er ikke brukt som bevis på pilot.

NVDB [Vegnett](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Vegnett/), [Rute](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Rute/), [Posisjon](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Posisjon/) og [Vegobjekter](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Vegobjekter/) forklarer feltene/avgrensningene. Hentede OpenAPI-definisjoner er openapi-vegnett.json og openapi-vegobjekter.json. Produsentens dokumentasjon og data er samme kildefamilie, ikke uavhengig fysisk bekreftelse.

## Kildebekreftet geometri

[pilot-named-roads.json](pilot-named-roads.json) inneholder153 segmenter for de tre navngitte kommunale vegsystemene, med tom sluttkontroll i pilot-named-roads-tail.json. For hovedlenkesekvens **1109722** (Strandvegen) dekker51 segmenter posisjon0–1. **1109517** (Strandvegen-overgang/Kvaløyvegen) har35 segmenter posisjon0–1. Sortert kildekjede har ingen intervall-/nodebrudd; de møtes i **node1138973**. Lengdesummer er henholdsvis2637,505 og4101,444m i kildens lengdefelt; dette er ikke total pilotlengde eller målt kjøreavstand fra Polaria.

Sørgående/vestlig rundt sørenden og deretter nordgående øker kildeposisjon på disse to lenkene. strict-strand.json og strict-kvaloy.json returnerte hver KOMPLETT over avgrensede geometriankre med bare riktig hovedlenke. Sluttkontrollen binder komplette kildesegmenter fra node1139933 ved Polaria til node1138796 på Flyplassvegen, 37,570 m etter R4-utgangen. Det er et eksplisitt valgt planintervall; adresseprojeksjonen 0.00775722@1109722 er et separat offentlig søkeanker, ikke innsamlet posisjon. Kildelengde er ikke målt kjørelengde. En sum av separate rutesvar alene beviser ikke sammenheng.

| Kontroll | NVDB-lenke | Foreslått valgt rundkjøringsbue fra kilde-/rutesvar | Avgrensning |
|---|---|---|---|
| R1, Langnesvegen/Langnesbakken–Kvaløyvegen | 1126029 | 0→0.31012056, fra node3249937 til3249939 | Inn fra1126588, ut1126527; felt/forbud må sluttkontrolleres. |
| R2, Workinn/Langnestunnelen | 1126030 | 0.88033387→1 + 0→0.62975708, økende posisjon, fra1139057 til1139060 | Videre via1126028 tilR3, ikke tunnelarmen. |
| R3, Giæverbukta | 1125949 | 0.65287709→1 + 0→0.35105026, økende, fra1138977 til1138963 | Videre mot1125918/E8, ikke Ringvegen/østover. |
| R4, sørlig flyplassavkjøring | 1125950 | 0.87462251→1 og0→0.05053167, fra1138787 via3251244 til3251245 | Ut1126506/Flyplassvegen. Bypass/filterarm finnes; må ikke telle som kjørt bue. |

R1–R3: [pilot-north-roads.json](pilot-north-roads.json), et200-segmenters utsnitt som **ikke** er uttømmende. R4: [airport-circle.json](airport-circle.json),12 segmenter. Buer og armer: surface-r1-r2.json, surface-r2-r3.json, surface-r3-circle.json og surface-circle-exit.json. Kilden gir geometri/topologiske noder; brukerens bekreftede antall gjentas ikke som nytt spørsmål. Kildens retning på stedfesting/metrering er ikke automatisk lovlig kjøreretning for buss.

**Detaljert til overordnet:** super-1126527.json knytter detaljert kjørebanesekvens1126527 til overordnet1126027, med blant annet felt1/3K. super-1126487.json knytter1126487 til1125918, med blant annet felt1/3. De to siste oppslagene gir også1126588→1109517 og1126506→1125938 (super-1126588.json og super-1126506.json). Detaljert1126506 har komplett overordnet stedfesting0–0.36047074 på1125938, som er dekket av50-objekt1019488951/1. Dette dekker de valgte detaljlenkene i planforslaget; feltspesifikke svingetillatelser og alle alternative armer er fortsatt ikke verifisert. Samme relative posisjon på to slike sekvenser kan ikke sammenlignes direkte.

## Registrerte verdier og overgangspunkter

Komplett sluttkontroll er gjort for de tre **målrettede** type105-søkene, ikke for alle veger i nordutsnittet. Belegg: pilot-south-speed.json (9objekter), pilot-north-target-speed.json (8) og pilot-detailed-speed.json (3), med hver sin tomme tail. Objekter kan forekomme i flere søk. [speed-intervals.csv](speed-intervals.csv) bevarer objekter, versjon, intervall, felt, kilde og tidsmetadata; [registered-changes.json](registered-changes.json) har avledede kildegrenser og koordinater der et segment begynner på samme punkt.

| Registrert endring / område | Kildestedfesting | Objekt etter grensen / versjon |
|---|---|---|
| Strandvegen40→30 | 0.57617192@1109722, KV40500 S1D1 ca.m1522; UTM33(652445.407,7730007.401) | 91472646/1; før91472647/1 |
| Rundt sørenden30→50 | 0.00216787@1109517, UTM33(651788.3,7729809.899) | 91472898/2; før91472899/1 |
| Kvaløyvegen50→30 | 0.26535564@1109517, ca.m1075; UTM33(651356.3,7730763.8) | 932902367/1 |
| Kvaløyvegen30→50 | 0.39829852@1109517, ca.m1620; UTM33(651280.66,7731301.39) | 91472898/2 |
| Kvaløyvegen50→60 | 0.47840131@1109517, ca.m1948; UTM33(651247,7731621.09) | 91472897/1 |
| Kvaløyvegen60→50 | 0.88134235@1109517, ca.m3600; UTM33(651516.417,7733216.343) | 91472896/1 |
| R1, forbindelsen tilR2 og R2 | Overordnet1126027 og sirkler1126029/1126030; registrert50 | 91485634/3,91485668/2,91485667/3 |
| FraR2 motR3:50; vedR3:60 | 1126028 til node1138977; R3 0.65287709@1125949 ved valgt innkjøring | 91485525/6 →1019488949/2 |
| E8 motR4:60→70 | 0.36159129@1125918; EV8 S1D1 ca.m789 | 1019488950/1; før1019488949/2 |
| R4:70; flyplassutkjøring:50 | R4 1125950 registrert70; EV8 S1D1 m0–98 /1125938 registrert50 | 1019488950/1 →1019488951/1 |

Dette er **registrerte veggrenser** i NVDB, ikke attestasjon av fysisk skilt, maksimal trygg rundkjøringsfart eller bussens kjøretøygrense. R4s registrerte70 illustrerer hvorfor dette skillet er viktig. Overgangen70→50 er nå kildebundet til node3251245, fra1125950 til1126506. Eksakt fysisk skiltposisjon og midlertidig skilting gjenstår. På nordenden av1109517 finnes to50-objekter91472894/1 og91472895/1 som er feltavgrenset; de må ikke feiltolkes som dobbelt konflikt eller som retningsbevis fra MED alene.

De viste hovedgrenseobjektene er sist endret i2025. Sideuttrekket inneholder også91472893v6 med virkning2026-10-01/endring2026-10-06; dette objektet ligger utenfor valgt slutt. Hentetid er aldri ny virkningsdato. Full midlertidig/variabel dekning, alle svingeforbud/feltvalg og fysiske overgangspunkter er ikke bekreftet.

## Konkret rundkjøring før kommende grense

**Rettet funn:** Den tidligere kandidaten265,519m brukte R2 mot registrert feltretning. [V830 §7.2](https://www.vegvesen.no/globalassets/fag/handboker/hb-v830-nasjonalt-vegreferansesystem.pdf?v=491e2d) beskriver oddetallsfelt med lenkeretningen. R2/R3 har felt1/3; korteste baklengsbue fra rutetjenesten forkastes. Økende R2-bue er80,824m; med242,984m videre blir det323,808m til60-grensen ved R3. Det er ikke et før-R2-tilfelle innen300m. R3 korrigeres tilsvarende til82,336m. Dette er en konkret feil i vårt foreløpige rutevalg, ikke endring av kildefartsgrensen.

**Valgt K3-kandidat:** R4, innnode1138787 → økende bue18,448m → utgang3251245 →1126506 med registrert50. Med200m til innkjøringen er kildeavstanden218,448m til70→50. Ved en kildebasert posisjon281,552m før innkjøringen er avstanden300m. Disse posisjonene er beregnede scenariopunkter, ikke målte GPS-fikser. Dette støtter planlegging av rundkjøring mellom posisjon og endring, men forvarsel må fortsatt undertrykkes hvis valgt arm ikke er kvalifisert. Planlagt arm alene er utilstrekkelig. Ingen fartsgrense flyttes. AC-07s syntetiske250m består som separat regneeksempel.

## Negative funn som må bevares

- Nærmeste-punkt-oppslag ved sørenden og flyplassen traff privatveger. Filtrert oppslag på navngitt kommunalveg ga andre kandidater. Nærmeste veg kan ikke brukes som kjørt trasé.
- pilot-directed-route.json inneholder124 segmenter, men status4040 IKKE_FUNNET_RUTE. Lengde7380,522m er ikke en komplett pilotrute.
- surface-strand.json er KOMPLETT, men velger Bjørnøygata/Mellomvegen og avvises for valgt Strandvegen-trasé. route-north.json er KOMPLETT, men bruker forbindelser som hopper overR2/R3. surface-r3-r4.json velger filterarm uten R4-bue. Komplett API-status er ikke komplett oppfyllelse av valgt korridor.
- Noen korte rutesøk ga ingen rute; geometriankre ga brukbare hovedsekvenser. Dette er et observasjonsfunn om søkeparametre, ikke bevis på at vegene er stengt.

## Avslutning av denne datakvalifiseringen

K1: sammenhengende plankjede, navn, retning i sirkelbuene og kildeidentifikatorer dokumentert. K2: målrettede type105-intervaller og aktuelle detalj/overordnet-bindinger dokumentert; ingen full garanti for regulering eller faktisk skilting. K3: R4-kandidat dokumentert, feilaktig R2-kandidat forkastet. K4: før/etter, feil arm, parallelle veger og manglende kantdekning har eksplisitte senere scenarioer. K5: fysisk kontroll er ikke utført.

Kildesvarene er uendret; alle45 forespørslers lagrede SHA-256 stemmer. Noen eldre svar har tegnkodingsfeil i tekstnøkler; tall/ID-er ble kontrollert separat, og produksjonsadapteren må avvise ukjent schema eller dokumentere korrigering. Hele nordutsnittet er ikke komplett, og alternativvegdekning er ikke bevist. Full lovlig bussrute kan ikke utledes fra nodekjeden eller HTTP200 alene.

Gjenværende kvalifisering ligger som konkrete ferdigkriterier i [stories1.1–1.7](../../planning/epics.md), med separat [profil og porter](../../specs/spec-speed-limits/technical-addendum.md). Dette er ferdig planlegging med åpne gjennomføringsporter, ikke en erklæring om at alt kan kvalifiseres uten bygging/fysisk test. Ingen flere dataoppslag i denne runden.
