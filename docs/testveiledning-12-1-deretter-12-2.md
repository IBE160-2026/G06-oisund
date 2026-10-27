# Testveiledning: Story 12.1 først, deretter 12.2

**Endelig eieraksept 27. oktober 2026:** Jonas har nå uttrykkelig godkjent både Story12.1 og Story12.2, inkludert de kommenterte12.2-rettingene, og bedt om commit/push. Begge er `done` / `owner_acceptance: accepted`. Tidligere ventende-/delakseptstatuser nedenfor er historikk. Godkjenningen bygger på Jonas sin manuelle test og beslutning; automatiske tester er separat evidens. Ingen senere story eller ytterligere fysisk enhetskvalifikasjon inngår.

**Ny demo-retting 27. oktober:** Kjørende frontend15312 er nå bygd fra arbeidskopi basert på `c7a6170beb360b7541c5aeaced805ff78db73f3e` med avgrensede demoendringer. Bygg og37 nettlesertester bestod; [endringer, versjonshash og ny retest](evidence/12-2-manual-feedback-fixes.md). De eldre versjonsvurderingene nedenfor er historikk for det tidligere bygget; privat/backendkode er uendret.

**Gjeldende akseptstatus 27. oktober 2026:** Jonas har uttrykkelig godkjent Story 12.1 etter bestått manuell sjekkliste A–F på Jonas_desktop, Brave privat vindu (oppgitt testreferanse `83cdd2b`). Story 12.1 er `done` / `owner_acceptance: accepted`. For Story12.2 er K bestått og alle ukommenterte deler uttrykkelig godkjent. Storyen som helhet er fortsatt ikke godkjent; de kommenterte rettingene avventer ny manuell test. Eldre utsagn nedenfor om ventende testing av begge storyer er historikk og er erstattet av denne godkjenningen. Automatiske tester innebærer ikke brukeraksept; godkjenningen bygger på Jonas sin manuelle test og uttrykkelige beslutning. Ingen bredere nettbrettkvalifikasjon eller senere story godkjennes her.

Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.

Jonas sin manuelle/fysiske akseptansetest av Story 12.1 og 12.2 gjenstår. Automatiske tester innebærer ikke brukeraksept.

**Rekkefølge:** Klargjør miljøet → test 12.1 → vurder stoppunktet → test 12.2 bare hvis 12.1 består uten behov for endringer.

Begge storyene står i `review` / `in-review`. Veiledningen registrerer ingen godkjenning. Tidligere automatiske resultater finnes i [integrasjonsrapporten](evidence/12-integrated-handoff.md).

**Kontrollert versjonsgrunnlag 27. oktober:** Main var `83cdd2b344aa8ec717d42cd3ecd055daad97a222` ved siste kontroll. Kjørende bygg og siste regresjonskjøring gjelder `62a0cf4f67f2ce1ea2b0da78c76858a10d7adf11`, etter integrasjonen av tilgangsarbeidet. De fire senere commitene endrer bare dokumentasjon/logger; produkt, konfigurasjon og tester er identiske. Ny hashkontroll av kjørende filer og tidligere testinnganger bestod. Veiledningen passer derfor det kjørende bygget. Publisering av denne dokumentasjonen/loggen gir nyere main-hash uten nytt produktbygg. Se [versjonsvurdering og resultater](evidence/12-after-access-merge.md) og [maskinlesbar kontroll](evidence/12-current-main-readiness.json).

## 1. Klargjør miljø og testdata

Bruk PC-en med prosjektet i `D:\IBE160`, Docker Desktop og Edge/Brave. Adressene nedenfor er lokale på denne PC-en. Nettbrettet trenger separat tilgang til akkurat dette bygget; det eksisterende nettbrettmiljøet er en annen utrulling.

Åpne PowerShell og registrer versjonen:

```powershell
Set-Location D:\IBE160
git branch --show-current
git rev-parse HEAD
git status --short
$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'
```

Bruk `main`. Noter commit, dato, enhet og nettleser i resultatmalen nederst. Hvis produktkode eller konfigurasjon er endret lokalt, avklar hvilken versjon som skal testes. En lokal endring i selve testveiledningen endrer ikke appen.

Hvis riktig miljø allerede kjører med riktig bygg, bruk det direkte. Ellers: start Docker Desktop og kjør én linje av gangen. **Stopp ved feil før neste kommando.**

```powershell
& $py scripts/verify-story12-integration.py up
& $py scripts/verify-story12-checks.py stop-preview
& $py scripts/verify-story12-checks.py build
& $py scripts/verify-story12-integration.py prepare
& $py scripts/verify-story12-checks.py serve
```

`stop-preview` stopper bare forhåndsvisningen verktøyet kan bekrefte eierskap til. Hvis porten er opptatt av en annen prosess, rapporter dette framfor å stoppe en ukjent prosess.

| Formål | Adresse |
|---|---|
| 12.1: faktisk privat app med syntetiske data | <http://127.0.0.1:15312/private> |
| 12.2: simulering uten innlogging | <http://127.0.0.1:15312/demo> |
| 12.2: faktisk fiktiv API/PostgreSQL-flyt | <http://127.0.0.1:15312/> |

Dette er prosjektet `ibe160-story12-integration`, med egne databaser og syntetiske data. Ikke bruk de ordinære tjenestene på 5173/8000/8001 for denne gjennomgangen.

**Ikke bruk port 15323:** Den tilhører det separate `ibe160-story123-tests`-miljøet for 12.3 (API 18323/18324). For 12.1/12.2 skal adresselinjen vise **127.0.0.1:15312**. Pilotens gateway på 18081 og den eksterne pilotadressen er også andre utrullinger. Denne oppgaven aktiverer ingen tunnel og eksponerer ikke Story12-miljøet eksternt.

Åpne et nytt InPrivate-/privat vindu. Finn brukernavn og passord i `D:\IBE160\.private-runtime\story12-manual-credentials.json`. Ikke ta med passord i notater eller skjermbilder.

Testkontoen har to bekreftede planer for **2. og 3. januar 2031**, begge med linje **20**, og separate kildeutkast. Framtidsdatoene gjør at planene ikke utløper før testing. Bruk bare fiktive opplysninger og medfølgende filer, eksempelvis `Eksempelfiler/Testskift-A.pdf`.

Hvis en plan mangler etter tidligere slettetesting, kjør `prepare` igjen. Den legger til manglende testdatoer og bevarer eksisterende planer og endringer. Den nullstiller ikke kontoen; uventede datoer, duplikate planer og endret linjeomfang avvises.

## 2. Test 12.1 — grense for lagrede data

Noter **bestått / feil / ikke testet** for A–F. Ved feil: noter trinn, forventet resultat og faktisk resultat. Ikke start 12.2 før stoppunktet i del 3 er passert.

### A. Opprett ett faktisk avvik med ukjente kildeopplysninger

1. Logg inn på `/private`, og åpne planen for **2. januar 2031**.
2. Velg **Manuelt vedlikeholdte avvik → Registrer avvik**.
3. Bruk tittel `TEST 12.1 – felles avvik`, linje `20` og en fiktiv SMS-beskrivelse. La kildelenke, kildeoppdatering og start være ukjente. Sett **Gyldig tildato** til **4. januar 2031**.
4. Lagre. Lukk og åpne avviksvisningen igjen.

**Forventet:** Ett lagret avvik med dine verdier. Ukjente opplysninger forblir ukjente. Registrering eller redigering betyr ikke at kilden er kontrollert. Gjenåpning lager ikke et duplikat.

### B. Kontroller samme avvik på begge dager

1. Lukk planen, og åpne **3. januar-planen**.
2. Velg **Les avvik for linjer og datoer**, og finn avviket fra A.
3. Gå til vedlikehold, endre tittelen til `TEST 12.1 – oppdatert felles avvik`, og lagre.
4. Åpne avviket fra begge testdagene etter tur.

**Forventet:** Samme avvik vises én gang i hver relevant leservisning. Begge dager viser den oppdaterte tittelen; det finnes ikke en separat kopi for hver dag.

### C. Slett opprinnelig plan, men behold det uavhengige avviket

1. Åpne **2. januar-planen**. Gå til dagsvisningen hvis du står inne i en aktivitet.
2. Velg **Slett bekreftet plan**. Kontroller at det er riktig syntetisk plan, og bekreft nettleserens slettespørsmål.
3. Åpne **3. januar-planen**, og les avviket igjen. Last siden på nytt og kontroller på nytt.

**Forventet:** Den slettede planen er borte. Avviket og 3. januar-planen finnes fortsatt. Kildeutkastet til den slettede planen kan fortsatt finnes fram til sin egen frist; dette er ikke gjenoppretting av planen.

### D. Kildekontroll, manuell avslutning og automatisk utløp

1. Åpne avviket i vedlikehold. Velg **Kontrollerte kilden nå** som en fiktiv testhandling.
2. Kontroller at kildekontroll registreres separat. Velg deretter **Avslutt avvik manuelt**.
3. Kontroller både aktiv leser og vedlikeholdsvisning.
4. Lag et nytt avvik, `TEST 12.1 – kort levetid`, linje `20`, med **dagens dato i Oslo** og sluttid **2–3 minutter fram i tid**. La start være ukjent. Lagre og vent til sluttiden er passert.

**Forventet:** Manuelt avsluttet avvik er skjult fra aktiv lesing, men finnes som skrivebeskyttet historikk. Det kortvarige avviket blir utløpt og kan ikke forlenges etter utløpet. Avslutning beviser ikke at en vei er fri.

**Skillet du skal se etter:** Dagens kortvarige avvik overlapper ikke 2031-planene. Kontroller utløpet i **vedlikehold**, ikke ved å forvente treff i planens datofiltrerte leser. Utløpt gyldighet betyr ikke umiddelbar sletting: historikken har egen lagringsfrist på sju dager etter avslutning.

### E. Importer og avbryt uten å erstatte bekreftet arbeid

1. Kontroller at 3. januar-planen finnes.
2. Gå til **Forberedelse og planlister**, og velg `Eksempelfiler/Testskift-A.pdf` i importflyten.
3. Se på tolkingen og avbryt eller forlat importgjennomgangen. Ikke bekreft en ny plan i denne testen.
4. Åpne 3. januar-planen igjen.

**Forventet:** Eksisterende bekreftet plan er uendret. Avbrutt import erstatter den ikke. Opplastet original skal ikke bli et vedvarende filarkiv i appen. Fravær av originaler på serveren kvalifiseres også automatisk; skjermvisning alene beviser ikke dette.

### F. Utlogging, Tilbake og privat nettleserlagring

1. Mens du er innlogget: åpne eventuelt utviklerverktøy → **Network/Nettverk**. Et privat API-svar fra port **18313** skal ha `Cache-Control: no-store`.
2. Under **Application/Lagring**: kontroller at private utkast, avviksinnhold og PDF-originaler ikke ligger i Local Storage, Session Storage, IndexedDB eller service worker-/app-cache. Økt-/CSRF-informasjonskapsler under innlogging er ikke et PDF-/utkastarkiv.
3. Logg ut. Bruk nettleserens **Tilbake**, og last siden på nytt.
4. Logg inn igjen og kontroller at bare fortsatt gyldige, autoriserte serverdata åpnes.

**Forventet:** Private opplysninger er skjult etter utlogging og kan ikke gjenopprettes med Tilbake eller oppdatering uten autorisert innlogging. Planen slettet i C kommer ikke tilbake. En tillatt, ikke-privat temapreferanse er ikke privat innhold.

### Retensjonsgrenser: hva denne manuelle testen ikke beviser

Reglene er: utkast **opprettelse + sju dager**; bekreftet arbeid **den tidligste relevante fristen av planlagt slutt + sju dager og registrert serveravslutning + sju dager**; uavhengige avvik **effektiv avslutning + sju dager**. Lesing og gjentak skal ikke flytte fristene. Utløpt tilgang avvises straks; fysisk rydding skjer ved oppstart og minst hver time.

Sju dagers sletting, gamle operasjons-ID-er, transaksjoner som krysser en frist og treg enhetsklokke har separat [automatisk evidens](evidence/12-integrated-handoff.md). De er ikke manuelt bevist av A–F. Du trenger ikke vente sju dager eller endre PC-klokken i denne gjennomgangen.

Hvis du vil ha ferske tekniske kontroller i tillegg, kjør disse **før 12.2**, én om gangen. Stopp ved feil:

```powershell
& $py scripts/verify-story12-checks.py backend tests/test_retained_data.py
& $py scripts/verify-story12-checks.py browser private-retention.spec.ts private-notice-recovery-integration.spec.ts
& $py scripts/verify-story12-integration.py verify
```

Siste kommando bruker midlertidige syntetiske kontoer, omstarter integrasjonsmiljøets tjenester og **nullstiller den faktiske fiktive databasen på `/`**. Den kontrollerer at private data bevares. Derfor kjøres den før du lager lagrede fiktive eksempler i 12.2. Nye resultater skrives under `docs/evidence/`, og kommandologger under `tmp/story12/`. Dette er automatiske tester, ikke din manuelle/fysiske test.

## 3. Stoppunkt etter 12.1

| Resultat | Neste handling |
|---|---|
| A–F består, ingen endringsbehov og ingen uforklarte avvik | Noter «12.1 testet – ingen endringsbehov». Fortsett til del 4. Storyens godkjenningsstatus endres ikke automatisk. |
| Feil, endringsønske eller uklart resultat kan kreve endring i 12.1 | **Stopp. Ikke test 12.2 ennå.** Noter trinn, versjon og forventet/faktisk resultat. Behold testtilstanden til feilen er undersøkt. |
| Miljøet starter ikke, eller viktige manuelle punkter er ikke testet | Noter «blokkert/ikke ferdig testet». Avklar dette før 12.2. |

Hvis 12.1 må endres, test rettingen og berørte 12.1-punkter på nytt. Gå videre først når du igjen kan si at 12.1 ikke krever endringer. En senere 12.2-feil som berører 12.1, åpner stoppunktet igjen.

## Retest av kommenterte12.2-punkter

K er bestått og øvrige ukommenterte deler er godkjent av Jonas. Åpne <http://127.0.0.1:15312/demo> og oppdater med Ctrl+Shift+R for nytt bygg; dette nullstiller simuleringens minne, ikke faktisk lagrede/private data.

1. Lagre et forslag: tydelig statusboks ved lagringsknappen skal bekrefte simulert lagring. Endre et felt: status skal vise ulagrede endringer. Gjenta for kontomelding og aktivitetsstatus.
2. Velg «Simulert lagringsresultat → Nyere revisjon / konflikt» og lagre. Originalfeltene skal bli stående leselige og skrivebeskyttet. Under handlingene vises gjeldende og foreslåtte verdier med feltnavn, uten kode/JSON. Avbryt skal bevare forslaget; «Ta i bruk gjeldende» er et separat valg som henter lagrede verdier.
3. Velg «Mistet svar etter lagring» og lagre. Feltene skal fortsatt vises, lagring/navigasjon skal være sperret og nærliggende status skal si uavklart. La oppslag feile én gang; slå deretter opp original kvittering med haken fjernet. Bekreft lagring uten nytt lagringsforsøk.
4. Kontroller ordene «Manuell aktivitetsstatus», «Lagre aktivitetsstatus» og «Avbryt ulagret aktivitetsstatus». Ved aktivitetsbytte skal ikke forrige aktivitets lagringsbekreftelse følge med. Test gjerne dag-/nattvisning.

Disse rettingene er automatisk kontrollert, men er ikke godkjent av Jonas ennå. Ingen ny full gjennomgang av de allerede godkjente, ukommenterte delene kreves av denne veiledningen.

## 4. Test 12.2 — bare etter passert stoppunkt

### G. Normal flyt i simuleringen

1. Åpne `/demo`. Forvent **SIMULERING · bare fiktive data**, uten innlogging.
2. Velg **Åpne delvis tekst-PDF-eksempel**. Kontroller at kildeusikkerhet vises.
3. Endre vognløp/buss. Velg **Lagre forslag i simuleringen → Se lagret dag før start → Bekreft plan**.
4. Velg en aktivitet før Start. Bruk **Forrige aktivitet / Neste aktivitet** til du når begge ender av listen. På første aktivitet skal Forrige være deaktivert; på siste skal Neste være deaktivert. Det forventes ikke egne knapper for å hoppe til første/siste aktivitet.
5. Velg **Start arbeidsdagen**; avbryt én gang og bekreft deretter med **Bekreft Start**.
6. Velg **Manuell aktivitetsstatus → Fullført manuelt** for én aktivitet, og velg **Lagre aktivitetsstatus**. La en annen aktivitet stå uregistrert.

**Forventet:** Valg, navigasjon og lagring starter/fullfører ingen aktivitet automatisk. Bare eksplisitt Start starter dagen. Lagret aktivitetsstatus tilhører riktig aktivitet. Vognløp og fysisk buss holdes fra hverandre; ukjente fakta forblir ukjente.

### H. Feil ved lagring uten tap av forslag

Bruk **Nullstill simuleringen → Bekreft nullstilling** mellom forsøk ved behov. Start et nytt utkast, endre et felt og åpne **Simuler feil ved neste lagring** før lagring.

| Velg i «Simulert lagringsresultat» | Handling og forventet resultat |
|---|---|
| Utilgjengelig | Lagre. Forslaget beholdes, og appen sier ikke lagret. Prøv normal lagring igjen. |
| Nyere revisjon / konflikt | Lagre. Gjeldende og foreslåtte verdier vises hver for seg. **Avbryt konflikt** beholder forslaget; **Ta i bruk gjeldende** er et eget valg. |
| Mistet svar etter lagring | Lagre. Operasjonen er uavklart; ny lagring/navigasjon sperres. Huk av **La oppslag feile**, velg **Slå opp original kvittering**: fortsatt uavklart. Fjern haken og slå opp igjen: opprinnelig simulert kvittering gjenfinnes. |

**Forventet:** Uavklart omtales ikke som lagret eller sikkert avvist. Oppslag lager ikke en ny mutasjon. Dette er simulerte feil; faktisk API-gjentak og tapt svar har separat automatisk evidens.

### I. Kontomeldinger, ukjente fakta og fast lesetid

1. Velg **Kontomeldinger → Vedlikehold meldinger**.
2. Lag en fiktiv melding. La start, kildeoppdatering og kildelenke være ukjente. Sett slutt til **27. oktober 2026 kl. 02:00** og la linjefeltet være tomt for alle linjer. Velg **Lagre melding i simuleringen**.
3. Velg **Les kontomeldinger**. Prøv linjefilter og lesereksemplene for tomt register, ingen treff og utilgjengelig innhold.

**Forventet:** Simuleringen bruker **26. oktober 2026 kl. 23:00 i Oslo** som fast lesetid, uavhengig av dagens klokke. Slutten ovenfor ligger etter denne tiden. Manglende metadata er ukjent, ikke kildekontroll. Eldre illustrert melding uten slutt er utelatt fra aktiv lesing.

### J. Avslutning, avbrudd og gjentakbar nullstilling

1. Start en simulert dag, lagre én aktivitetsstatus og la en annen aktivitet stå uregistrert.
2. Velg **Avslutt arbeidsdagen**, og avbryt bekreftelsen én gang. Forvent retur til riktig skjerm og kontroll.
3. Avslutt deretter med bekreftelse. Kontroller antall lagrede aktivitetsstatuser og ukjente aktiviteter i oppsummeringen.
4. Åpne **Kontomeldinger** igjen. Meldingen beholder egen levetid etter avsluttet dag.
5. Velg **Nullstill simuleringen**: avbryt først, bekreft deretter og gjenta normalflyten. Prøv også **Avbryt arbeidsdagen** med bekreftelse i en ny simulering.
6. Prøv **Prøv format som ikke støttes** og merket manuell fallback. Kontroller tastatur, fokus, Dag/Natt og smal/forstørret visning.

**Forventet:** Oppsummeringen er skrivebeskyttet; uregistrerte aktivitetsstatuser fullføres ikke automatisk. Avbrutt nullstilling bevarer tilstanden, bekreftet nullstilling rydder bare simuleringens minne. Oppdatering av siden starter også simuleringen på nytt.

**Begrensninger:** Tre faste aktiviteter; fallback redigerer vognløp/buss, ikke hele aktivitetslisten. Ingen faktisk PDF-tolking i simuleringen. Eldre melding uten slutt har ingen fullføringshandling i demoen. Bredere temapersistens og fysisk enhetskvalifikasjon tilhører senere arbeid.

### K. Faktisk databaseflyt og bevaring av private testdata

Her tester du **to forskjellige sider og lagringsmåter**. `/demo` er simuleringen du har brukt hittil; data finnes bare i fanens minne. Forsiden `/` bruker den isolerte, faktiske fiktive API-en/PostgreSQL-databasen. K skal vise at en lagret dag overlever ny sideinnlasting og nullstilling av simuleringen, mens private testdata også bevares. Du skal ikke stoppe tjenester eller nullstille databaser.

1. Behold `/demo`-fanen. Åpne **en ny fane i samme private nettleservindu**, og skriv hele adressen <http://127.0.0.1:15312/> (uten `/demo` eller `/private`).
2. Forvent overskriften **Fiktiv arbeidsdag** og merket **Fiktive demodata**. Dette er en annen side enn **Prøv en fiktiv arbeidsdag**. Vent til status viser **Ikke lagret. Eksemplet er planlagt og fiktivt.** Hvis et gammelt lagret eksempel åpnes, bruk adressen uten `?day=…`, eller velg **Last inn nytt fiktivt eksempel**.
3. Noter tjenestedato, vognløp, fysisk buss og dato/klokkeslett for aktivitetene. Se at planlagt arbeid krysser midnatt: datoen skifter etter midnatt; det er ikke en negativ varighet. Ukjent fysisk buss skal ikke fylles inn automatisk.
4. Trykk **Lagre fiktiv dag**. Forvent status **Lagret og bekreftet av tjenesten.**, informasjon om bekreftet lagring/slettetid, og en adresse som nå inneholder `?day=` etterfulgt av en ID.
5. **Kopier hele denne adressen** til et testnotat. Ikke velg «Last inn nytt fiktivt eksempel» nå. Trykk **Ctrl+R** i fanen med den lagrede dagen.
6. Forvent **Lagret eksempel er hentet fra tjenesten.** Sammenlign med punkt3: samme ID i adressen, tjenestedato, vognløp, fysisk buss og aktiviteter. Det er henting av lagret dag, ikke ny lagring.
7. Gå tilbake til `/demo`-fanen. Velg **Nullstill simuleringen → Bekreft nullstilling**. Forvent at bare simuleringen går tilbake til start.
8. Åpne den **kopierte adressen fra punkt5** i en ny fane, eller lim den inn igjen i fanen med faktisk lagret dag. Forvent på nytt **Lagret eksempel er hentet fra tjenesten.**, samme ID og samme verdier. Du skal ikke trykke Lagre en gang til for å få dagen tilbake.
9. Åpne <http://127.0.0.1:15312/private> i samme private vindu. Logg inn med samme syntetiske konto som i12.1 hvis appen ber om det. **3. januar2031-planen** skal fortsatt kunne åpnes, mens **2. januar-planen** fortsatt skal være slettet. Avvikshistorikken fra12.1 skal være bevart i vedlikehold; avsluttede/utløpte avvik trenger ikke vises som aktive.
10. Rapporter K som bestått/feil/ikke testet for tre observasjoner: **lagret dag overlever Ctrl+R**, **lagret dag overlever nullstilling av `/demo`**, **private testdata er uendret**. Ved feil: noter hvilket punkt og teksten som faktisk vises; behold lagret adresse og testtilstand.

**Forventet:** Simuleringens nullstilling påvirker verken faktisk lagret fiktiv dag eller private testdata. Faktiske og simulerte kvitteringer er forskjellige. Ikke kjør det tekniske `verify`-verktøyet under K: det nullstiller den faktiske fiktive databasen som del av sin egen test.

## 5. Resultatmal

Kopier til egne testnotater. Ikke legg inn passord eller ekte arbeids-/personopplysninger.

```text
Dato og klokkeslett:
Commit:
Enhet / operativsystem / nettleser:
Adresse:

12.1: A __ B __ C __ D __ E __ F __
Endringsbehov i 12.1: ingen / beskriv
Stoppunkt: passert / stoppet / ikke ferdig

12.2: ikke startet / G __ H __ I __ J __ K __

Ved feil:
Story og trinn:
Hva jeg gjorde:
Forventet resultat:
Faktisk resultat:
Kan det gjentas?:
Skjermbilde uten passord/personopplysninger:
```

Bruk «bestått», «feil» eller «ikke testet». Noter fysisk enhetstest separat fra automatiske nettlesertester. Oppgi til slutt om du uttrykkelig godkjenner en story eller om den avventer retting/testing; ingen avkryssing her endrer prosjektstatus automatisk.
