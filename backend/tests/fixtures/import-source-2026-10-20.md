# Fasit til skifteksemplene

Fasit for de sju anonymiserte PDF-ene i denne mappen, utarbeidet 20. oktober 2026 ved tekstlesing og visuell kontroll av alle ti sider. Tabellenes aktiviteter er transkribert fra PDF-ene, uavhengig av en importimplementasjon. Fasiten dokumenterer forventet innhold; den dokumenterer ikke at applikasjonen har bestått importtestene.

Se [LES-MEG.txt](LES-MEG.txt) for anonymisering og begrensninger. Dette er bearbeidede historiske skift med fiktive datoer, ikke gjeldende arbeidsplaner.

## Godkjenning

**Godkjent av Jonas Øisund 20. oktober 2026 (2026-10-20).** Godkjenningen omfatter fasiten for alle sju PDF-er og avklaringene om betalt fritid, Travel to som tomkjøring i eksempel 6, sammenslåing og navngivning av pauser, vognløp og manuell registrering av faktisk buss. Fasiten er godkjent som forventningsgrunnlag for implementering og kontroll av import. Godkjenningen er ikke en bestått importtest eller en ferdigmelding av story 9.1.

## Leseregler

- Les hver side i venstre spalte først, deretter høyre spalte, før neste side. En tur kan fortsette over både spalte- og sideskift.
- Datoene er dag/måned/år. Klokkeslett er normalisert til `HH:MM`. Tidssonen for tolkning er `Europe/Oslo`; PDF-ene oppgir ikke tidssone eksplisitt.
- Skiftdatoen beholdes også når aktiviteter fortsetter neste kalenderdag. I eksempel 4 betyr `(+1)` 6. januar 2030; øvrige tider der gjelder 5. januar.
- `UNN` betyr **Universitetssykehuset Nord-Norge**. Forkortelsen brukes bare for å gjøre denne fasiten lettere å lese.
- `tom / nummer` er tomkjøring med eget turnummer. Øvrige turer angis som `linje / turnummer`. Numrene behandles som identifikatorer. Tall som `9.1`, `16.4` og `22.6` under turnummeret er ikke linjenummer eller klokkeslett.
- Feltet `Vogn` i PDF-ene angir **vognløp**: en samling turer som skal kjøres under et skift. Det er ikke identiteten til den faktiske bussen. Gjentatt vognløp etter en pause betyr samme vognløp; endret nummer betyr bytte av vognløp og dokumenterer ikke i seg selv et fysisk bussbytte.
- Aktivitetstabellene beholder kildeetikettene og de enkelte PDF-radene. I assistentens visning kan tilstøtende pausetyper samles etter reglene nedenfor. Antallet kildeaktiviteter er derfor ikke nødvendigvis antallet aktiviteter som vises.
- Mellomrom mellom aktiviteter er ikke egne kildeaktiviteter. Ikke fyll dem automatisk med pause, kjøring eller arbeid. Steder er oppført for turene; steder for øvrige aktiviteter skal ikke presenteres som eksplisitte kildefelt når de bare kan utledes av naboturer.
- Mellomliggende holdeplasser ligger i PDF-ene. Denne fasiten dekker skifthode, vognoppføringer, alle turers endepunkter og alle øvrige eksplisitte aktiviteter. Den er ikke en full holdeplassfasit.

## Pauser i assistenten

Avklart av prosjekteier 20. oktober 2026: Tilstøtende pausetyper kan samles til én pause fra første delpauses start til siste delpauses slutt. Inngår matpause, vises hele den samlede pausen som **matpause**. Når pausen bare består av `Coffee`, vises den som **kaffepause**. `Split break` vises som **split break / deltskiftpause**.

| Eksempel | Kildeaktiviteter | Samlet pause i assistenten |
| --- | --- | --- |
| 1 | Split break 10:50–12:00 | Deltskiftpause 10:50–12:00 (1 t 10 min) |
| 1 | Coffee 14:39–15:05 | Kaffepause 14:39–15:05 (26 min) |
| 2 | MealBreak 12:01–12:31 + Paid meal before 12:31–12:43 | Matpause 12:01–12:43 (42 min) |
| 4 | MealBreak 00:45–01:15 neste dag | Matpause 00:45–01:15 neste dag (30 min) |
| 6 | Split break 09:10–15:00 | Deltskiftpause 09:10–15:00 (5 t 50 min) |
| 7 | Paid meal after 08:52–08:58 + MealBreak 08:58–09:28 | Matpause 08:52–09:28 (36 min) |
| 7 | Coffee 11:40–12:02 | Kaffepause 11:40–12:02 (22 min) |
| 7 | Coffee 14:13–14:39 | Kaffepause 14:13–14:39 (26 min) |

Sign-on, Sign-off og transportaktiviteter er ikke pausetyper i denne sammenslåingen. De to kaffepausene i eksempel 7 er adskilt av kjøring og forblir to pauser. Eksempel 3 og 5 har ingen eksplisitte pausetyper. Den betalte fritiden i eksempel 5 er beskrevet separat.

## Vognløp, sanntidsskjerm og faktisk buss

Avklart av prosjekteier 20. oktober 2026: Alle vognløpene i disse eksemplene har prefikset `960`. **De tre siste sifrene skal inn i sanntidsskjermen.** Behold dem som tre sifre, inkludert innledende nuller. Behold også det fulle vognløpsnummeret fra PDF-en.

| Eksempel | Vognløp i rekkefølge, uten gjentatte oppføringer av samme løp | Verdi til sanntidsskjermen |
| --- | --- | --- |
| 1 | 960300 → 960301 | `300` → `301` |
| 2 | 960146 | `146` |
| 3 | 960127 | `127` |
| 4 | 960090 | `090` |
| 5 | 960006 | `006` |
| 6 | 960078 → 960109 | `078` → `109` |
| 7 | 960077 → 960110 | `077` → `110` |

**Faktisk buss finnes ikke noe sted i disse PDF-ene.** Opplysningen må hentes eksternt og legges inn manuelt i assistenten. Importen skal derfor la faktisk buss være ukjent frem til manuell registrering; verken hele vognløpsnummeret eller de tre siste sifrene skal fylle feltet for faktisk buss. Tabellen angir verdier til sanntidsskjermen, ikke at sanntidsintegrasjon er implementert.

## Oversikt

Alle skift har arbeidsgiver `Tide Buss`, avdeling `Tromsø`, sjåfør `Testsjåfør (00000)` og start/sluttsted `Garasje Gimle` i skifthodet. Arbeidstid og utstrekk under er kildeverdier, ikke nye lønnsberegninger.

| Eksempel | Skift-ID | Skiftdato | Ukedag i PDF | Sider | Skift start/slutt | Arb.tid | Utstrekk | Ruteturer | Tomturer |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: |
| [1](Eksempel-1-anonymisert.pdf) | 90000001 | 2030-01-04 | Fri | 4 | 06:08–17:35 | 10h17 | 11h27 | 15 | 10 |
| [2](Eksempel-2-anonymisert.pdf) | 90000002 | 2030-01-01 | Tue | 1 | 07:51–16:42 | 8h21 | 8h51 | 8 | 2 |
| [3](Eksempel-3-anonymisert.pdf) | 90000003 | 2030-01-11 | Fri | 1 | 06:51–09:26 | 2h35 | 2h35 | 2 | 2 |
| [4](Eksempel-4-anonymisert.pdf) | 90000004 | 2030-01-05 | Sat | 1 | 22:36–04:10 (+1) | 5h04 | 5h34 | 5 | 6 |
| [5](Eksempel-5-anonymisert.pdf) | 90000005 | 2030-01-03 | Thu | 1 | 06:51–08:51 | 2h00 | 2h00 | 1 | 2 |
| [6](Eksempel-6-anonymisert.pdf) | 90000006 | 2030-01-07 | Mon | 1 | 04:50–17:07 | 6h27 | 12h17 | 6 | 5 |
| [7](Eksempel-7-anonymisert.pdf) | 90000007 | 2030-01-18 | Fri | 1 | 04:49–16:49 | 11h30 | 12h00 | 9 | 4 |

Totalt: **46 ruteturer og 31 tomkjøringer**: 30 med etiketten `tom / turnummer`, samt `Travel to` i eksempel 6, avklart som tomkjøring av prosjekteier. Sidehenvisningene i tabellene viser hvor aktiviteten står; en aktivitet over flere sider har begge sidetallene.

## Eksempel 1: flere sider, delt skift og bytte av vognløp

Vognløp `960300` står etter Sign-on 06:08–06:11 og igjen etter Sign-on 12:00–12:01. Vognløp `960301` står før tur `30 / 1027` kl. 15:10. Tillegg i hodet: `25,00% 0h00`, `40,00% 0h00`.

| Side | Tid | Aktivitet / linje og tur | Fra → til |
| --- | --- | --- | --- |
| 1 | 06:08–06:11 | Sign-on | Ikke oppgitt |
| 1 | 06:18–06:36 | tom / 75807 | Garasje Gimle → Sorgenfri |
| 1 | 06:39–07:05 | 30 / 1000 | Sorgenfri → UNN |
| 1 | 07:05–07:08 | tom / 75031 | UNN → UNN |
| 1 | 07:24–07:52 | 30 / 1005 | UNN → Sorgenfri |
| 1 | 07:56–08:26 | 30 / 1004 | Sorgenfri → UNN |
| 1 | 08:26–08:26 | tom / 75803 | UNN → UNN |
| 1 | 08:32–09:00 | 30 / 1009 | UNN → Sorgenfri |
| 1–2 | 09:02–09:29 | 30 / 1008 | Sorgenfri → UNN |
| 2 | 09:29–09:31 | tom / 75033 | UNN → UNN |
| 2 | 09:45–10:13 | 30 / 1013 | UNN → Sorgenfri |
| 2 | 10:16–10:43 | 30 / 1012 | Sorgenfri → UNN |
| 2 | 10:43–10:46 | tom / 75809 | UNN → Garasje Gimle |
| 2 | 10:49–10:50 | Sign-off | Ikke oppgitt |
| 2 | 10:50–12:00 | Split break | Ikke oppgitt |
| 2 | 12:00–12:01 | Sign-on | Ikke oppgitt |
| 2 | 12:08–12:11 | tom / 75811 | Garasje Gimle → UNN |
| 2 | 12:14–12:42 | 30 / 1017 | UNN → Sorgenfri |
| 2–3 | 12:43–13:10 | 30 / 1016 | Sorgenfri → UNN |
| 3 | 13:10–13:12 | tom / 75045 | UNN → UNN |
| 3 | 13:26–13:54 | 30 / 1021 | UNN → Sorgenfri |
| 3 | 13:57–14:24 | 30 / 1020 | Sorgenfri → UNN |
| 3 | 14:24–14:26 | tom / 75818 | UNN → UNN |
| 3 | 14:34–14:39 | Travel to | Ikke oppgitt |
| 3 | 14:39–15:05 | Coffee | Ikke oppgitt |
| 3 | 15:05–15:10 | Travel from | Ikke oppgitt |
| 3 | 15:10–15:38 | 30 / 1027 | UNN → Sorgenfri |
| 3 | 15:40–16:10 | 30 / 1026 | Sorgenfri → UNN |
| 3 | 16:10–16:13 | tom / 75037 | UNN → UNN |
| 3–4 | 16:25–16:53 | 30 / 1031 | UNN → Sorgenfri |
| 4 | 16:57–17:27 | 30 / 1030 | Sorgenfri → UNN |
| 4 | 17:27–17:30 | tom / 75814 | UNN → Garasje Gimle |
| 4 | 17:33–17:35 | Sign-off | Ikke oppgitt |

Kontrollpunkter: Ett skift med to arbeidsdeler, ikke fire skift fordi dokumentet har fire sider. Gjentatte skifthoder skal ikke bli aktiviteter. Behold tomtur `75803` med lik start- og sluttid og behold turer mellom like navngitte endepunkter. Turene `1004`, `1012` og tomtur `75818` fortsetter over spalter; turene `1008`, `1016` og `1031` fortsetter over sider.

## Eksempel 2: matpause og betalt måltidstid

Vognløp `960146` står etter begge Sign-on-aktivitetene. Tillegg: `25,00% 0h00`.

| Side | Tid | Aktivitet / linje og tur | Fra → til |
| --- | --- | --- | --- |
| 1 | 07:51–07:54 | Sign-on | Ikke oppgitt |
| 1 | 07:59–08:22 | tom / 74540 | Garasje Gimle → Solligården |
| 1 | 08:25–09:09 | 28 / 1022 | Solligården → Hamna skole øst |
| 1 | 09:09–09:59 | 28 / 1035 | Hamna skole øst → Solligården |
| 1 | 10:25–11:09 | 28 / 1034 | Solligården → Hamna skole øst |
| 1 | 11:09–11:59 | 28 / 1047 | Hamna skole øst → Solligården |
| 1 | 11:59–12:01 | Sign-off | Ikke oppgitt |
| 1 | 12:01–12:31 | MealBreak | Ikke oppgitt |
| 1 | 12:31–12:43 | Paid meal before | Ikke oppgitt |
| 1 | 12:43–12:45 | Sign-on | Ikke oppgitt |
| 1 | 12:45–13:29 | 28 / 1048 | Solligården → Hamna skole øst |
| 1 | 13:29–14:19 | 28 / 1061 | Hamna skole øst → Solligården |
| 1 | 14:35–15:19 | 28 / 1064 | Solligården → Hamna skole øst |
| 1 | 15:19–16:15 | 28 / 1077 | Hamna skole øst → Solligården |
| 1 | 16:15–16:38 | tom / 74542 | Solligården → Garasje Gimle |
| 1 | 16:40–16:42 | Sign-off | Ikke oppgitt |

Kontrollpunkter: Tur `1061` fortsetter i høyre spalte. Kilden har to rader for `MealBreak` og `Paid meal before`; assistenten kan samle dem til matpause 12:01–12:43. Oppholdet 09:59–10:25 har ingen egen aktivitetsetikett i PDF-en.

## Eksempel 3: kort skift uten eksplisitt pause

Vognløp `960127`. Tillegg: `25,00% 0h00`.

| Side | Tid | Aktivitet / linje og tur | Fra → til |
| --- | --- | --- | --- |
| 1 | 06:51–06:54 | Sign-on | Ikke oppgitt |
| 1 | 06:59–07:22 | tom / 75344 | Garasje Gimle → Solligården |
| 1 | 07:25–08:09 | 28 / 1010 | Solligården → Hamna skole øst |
| 1 | 08:09–08:59 | 28 / 1023 | Hamna skole øst → Solligården |
| 1 | 08:59–09:22 | tom / 75903 | Solligården → Garasje Gimle |
| 1 | 09:24–09:26 | Sign-off | Ikke oppgitt |

Kontrollpunkt: Skifthodets slutt og siste Sign-off er begge 09:26. Ingen eksplisitt pause skal legges til.

## Eksempel 4: skift over midnatt

Vognløp `960090` står etter begge Sign-on-aktivitetene. Tillegg: `25,00% 0h00`, `40,00% 0h00`. Skiftdato er **2030-01-05** og skiftets sluttdato er **2030-01-06**.

| Side | Tid | Aktivitet / linje og tur | Fra → til |
| --- | --- | --- | --- |
| 1 | 22:36–22:39 | Sign-on | Ikke oppgitt |
| 1 | 22:44–22:53 | tom / 7351 | Garasje Gimle → Skognesvegen |
| 1 | 22:55–23:41 | 24 / 6069 | Skognesvegen → Kroken sykehjem |
| 1 | 23:50–00:35 (+1) | 24 / 6072 | Kroken sykehjem → Skognesvegen |
| 1 | 00:35–00:44 (+1) | tom / 7405 | Skognesvegen → Garasje Gimle |
| 1 | 00:44–00:45 (+1) | Sign-off | Ikke oppgitt |
| 1 | 00:45–01:15 (+1) | MealBreak | Ikke oppgitt |
| 1 | 01:15–01:17 (+1) | Sign-on | Ikke oppgitt |
| 1 | 01:17–01:28 (+1) | tom / 7394 | Garasje Gimle → Bankgata |
| 1 | 01:30–02:03 (+1) | 33 / 6601 | Bankgata → UNN |
| 1 | 02:03–02:14 (+1) | tom / 7083 | UNN → Bankgata |
| 1 | 02:30–03:03 (+1) | 33 / 6603 | Bankgata → UNN |
| 1 | 03:03–03:14 (+1) | tom / 7084 | UNN → Bankgata |
| 1 | 03:30–04:03 (+1) | 33 / 6605 | Bankgata → UNN |
| 1 | 04:03–04:06 (+1) | tom / 7224 | UNN → Garasje Gimle |
| 1 | 04:08–04:10 (+1) | Sign-off | Ikke oppgitt |

Kontrollpunkter: Tur `6072` krysser midnatt innad i turen, ved holdeplassen Kraftforsyninga kl. 00:00. Starten er 5. januar kl. 23:50; slutten er 6. januar kl. 00:35. Sortering på klokkeslett alene gir feil rekkefølge. Hele skiftets utstrekk er 5 timer og 34 minutter.

## Eksempel 5: minstebetaling på to timer

Vognløp `960006`. Tillegg: `25,00% 0h00`.

| Side | Tid | Aktivitet / linje og tur | Fra → til |
| --- | --- | --- | --- |
| 1 | 06:51–06:54 | Sign-on | Ikke oppgitt |
| 1 | 06:59–07:38 | tom / 75619 | Garasje Gimle → Olavsvern |
| 1 | 07:40–08:13 | 413 / 1002 | Olavsvern → Skipper Arnesens veg |
| 1 | 08:13–08:25 | tom / 75620 | Skipper Arnesens veg → Garasje Gimle |
| 1 | 08:27–08:29 | Sign-off | Ikke oppgitt |

**Forklaring fra prosjekteier 20. oktober 2026:** Ingen skift kan være betalt mindre enn to timer totalt. Derfor er **08:29–08:51 betalt fritid**, uten egen aktivitetsrad i PDF-en. Tidsrommet er 22 minutter, beregnet fra siste Sign-off og skifthodets slutt.

Forventet resultat: Behold skiftslutt **08:51**, arbeidstid **2h00**, utstrekk **2h00** og siste eksplisitte aktivitets slutt **08:29**. Dette er et forklart forhold, ikke en feil som skal rettes til 08:29. Dersom betalt fritid vises som egen aktivitet, må den merkes som avledet fra prosjekteiers forklaring, ikke som en ekstra rad funnet i PDF-en. Kilden har fem eksplisitte aktiviteter; betalt fritid inngår ikke i dette antallet.

## Eksempel 6: langt skiftavbrudd og Travel to som tomkjøring

Vognløp `960078` står etter Sign-on 04:50–04:53. Vognløp `960109` står etter Sign-on 15:00–15:01 og igjen før `X43 / 1007` kl. 16:00. Tillegg: `25,00% 1h10`.

| Side | Tid | Aktivitet / linje og tur | Fra → til |
| --- | --- | --- | --- |
| 1 | 04:50–04:53 | Sign-on | Ikke oppgitt |
| 1 | 04:58–05:06 | tom / 81348 | Garasje Gimle → Skattøra Borettslag |
| 1 | 05:09–06:07 | 20 / 1001 | Skattøra Borettslag → Malmvegen snuplass |
| 1 | 06:17–06:56 | 22 / 1000 | Malmvegen snuplass → Skognesvegen |
| 1 | 07:10–07:56 | 24 / 1015 | Skognesvegen → Kroken sykehjem |
| 1 | 08:05–08:55 | 24 / 1028 | Kroken sykehjem → Skognesvegen |
| 1 | 08:55–09:07 | tom / 81351 | Skognesvegen → Garasje Gimle |
| 1 | 09:09–09:10 | Sign-off | Ikke oppgitt |
| 1 | 09:10–15:00 | Split break | Ikke oppgitt |
| 1 | 15:00–15:01 | Sign-on | Ikke oppgitt |
| 1 | 15:06–15:10 | tom / 81285 | Garasje Gimle → UNN |
| 1 | 15:12–15:33 | X35 / 1001 | UNN → Skoglyst |
| 1 | 15:33–16:00 | Travel to (tomkjøring, avklart av prosjekteier) | Skoglyst → Breivika |
| 1 | 16:00–16:34 | X43 / 1007 | Breivika → Eidkjosen |
| 1 | 16:34–17:03 | tom / 80698 | Eidkjosen → Garasje Gimle |
| 1 | 17:05–17:07 | Sign-off | Ikke oppgitt |

Kontrollpunkter: `Split break` varer 5 timer og 50 minutter. Dette er ett skift med to arbeidsdeler og forskjellige vognløp. Linjenes `X` skal bevares. Turnummer `1001` forekommer på både linje 20 og X35 og er ikke alene en unik nøkkel.

**Avklart av prosjekteier 20. oktober 2026:** `Travel to` er i dette tilfellet sammenhengende tomkjøring fra **Skoglyst til Breivika kl. 15:33–16:00**, med **27 minutters varighet**. Det er ingen ventetid underveis eller på Breivika før neste rutetur. Starttid og fra-sted følger av avslutningen på `X35 / 1001`; sluttid og til-sted følger av starten på `X43 / 1007`. PDF-raden viser bare 16:00. Fasiten bruker prosjekteiers avklaring sammen med nabopostene for å fylle ut aktiviteten; dette er ikke et uavklart tidsrom eller en generell regel for alle Travel to-aktiviteter. Behold kildeetiketten `Travel to`, klassifiser aktiviteten som tomkjøring og la turnummer være ukjent. Eksemplet har dermed fire nummererte tomturer og denne tomkjøringen, totalt fem. Antallet aktivitetsrader er uendret.

## Eksempel 7: flere linjer, pauser og bytte av vognløp

Vognløp `960077` står etter første Sign-on, etter Sign-on 09:28–09:30 og før tur `20 / 1051` kl. 12:02. Vognløp `960110` står før tur `24 / 1049` kl. 14:39. Tillegg: `25,00% 1h11`.

| Side | Tid | Aktivitet / linje og tur | Fra → til |
| --- | --- | --- | --- |
| 1 | 04:49–04:52 | Sign-on | Ikke oppgitt |
| 1 | 04:57–05:06 | tom / 69352 | Garasje Gimle → Skognesvegen |
| 1 | 05:09–06:03 | 24 / 1001 | Skognesvegen → Kroken sykehjem |
| 1 | 06:20–07:15 | 24 / 1004 | Kroken sykehjem → Skognesvegen |
| 1 | 07:29–08:23 | 24 / 1015 | Skognesvegen → Kroken sykehjem |
| 1 | 08:23–08:50 | tom / 69831 | Kroken sykehjem → Skattøra Borettslag |
| 1 | 08:50–08:52 | Sign-off | Ikke oppgitt |
| 1 | 08:52–08:58 | Paid meal after | Ikke oppgitt |
| 1 | 08:58–09:28 | MealBreak | Ikke oppgitt |
| 1 | 09:28–09:30 | Sign-on | Ikke oppgitt |
| 1 | 09:30–10:33 | 42 / 1039 | Skattøra Borettslag → Eidkjosen |
| 1 | 10:38–11:40 | 42 / 1048 | Eidkjosen → Skattøra Borettslag |
| 1 | 11:40–12:02 | Coffee | Ikke oppgitt |
| 1 | 12:02–13:00 | 20 / 1051 | Skattøra Borettslag → Malmvegen snuplass |
| 1 | 13:05–13:58 | 20 / 1060 | Malmvegen snuplass → Skattøra Borettslag |
| 1 | 13:58–14:13 | tom / 14 | Skattøra Borettslag → Skognesvegen |
| 1 | 14:13–14:39 | Coffee | Ikke oppgitt |
| 1 | 14:39–15:33 | 24 / 1049 | Skognesvegen → Kroken sykehjem |
| 1 | 15:38–16:33 | 24 / 1056 | Kroken sykehjem → Skognesvegen |
| 1 | 16:33–16:45 | tom / 69626 | Skognesvegen → Garasje Gimle |
| 1 | 16:47–16:49 | Sign-off | Ikke oppgitt |

Kontrollpunkter: Tur `42 / 1048` fortsetter i høyre spalte. Behold det korte tomturnummeret `14`. Skiftet har to Coffee-aktiviteter og ett bytte av vognløp; Sign-off før matpausen betyr ikke at hele skiftet er avsluttet.

## Bruk ved kontroll av import

Sammenlign først skiftidentitet, datoer og hodeverdier. Kontroller deretter hver aktivitetsrad i rekkefølge, turenes linje/nummer, endepunkter, tider og vognoppføringer. Kontroller særlig spalte-/sideskift, kalenderdato etter midnatt og at ukjent informasjon forblir ukjent.

| Eksempel | Eksplisitte aktivitetsrader | Viktigste kontroll |
| --- | ---: | --- |
| 1 | 33 | Fire sider til ett skift; nullminutters tomtur; delt skift; bytte av vognløp |
| 2 | 16 | Spaltefortsettelse; to pauserader kan vises som matpause 12:01–12:43 |
| 3 | 6 | Kort skift uten eksplisitt pause |
| 4 | 16 | Kalenderdato skifter midt i tur 6072 |
| 5 | 5 | Siste aktivitet 08:29, betalt skiftslutt 08:51 |
| 6 | 16 | Delt skift; X-linjer; Travel to er 27 min tomkjøring Skoglyst → Breivika uten ventetid |
| 7 | 21 | Spaltefortsettelse; tomtur 14; to Coffee-aktiviteter; bytte av vognløp |

Totalt **113 eksplisitte aktivitetsrader**, uten skifthoder, vognoppføringer, mellomliggende holdeplasser eller den forklarte betalte fritiden i eksempel 5. Bevaring av disse opplysningene er forventninger til importen; faktisk resultat og eventuell klassifisering som fullstendig/delvis/ikke støttet må registreres når importen prøves.
