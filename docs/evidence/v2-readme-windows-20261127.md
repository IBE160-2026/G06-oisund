# Bussassistent V2 — lokal README-prøve på Windows 27.11.2026

## Oppsett

- `C:\workspace\ibe160-readme-desktop` hadde først samme commit som arbeidsgrenen, `57d5df2`. Git-statusen var ren, og `git clean -ndx` listet ingen ekstra filer. Kandidaten med isolert oppstart, `a00740a`, ble hentet lokalt og verifisert ren før første oppstart. Den rettede README-en i `87374b5` ble brukt ved omstart og ny Entur-import.
- `docker info --format '{{.OSType}}'` ga `linux` fra Codex. Den begrensede økten fikk også avslag på `npipe:////./pipe/docker_engine` og utgående HTTPS. Etter godkjenning fungerte Docker, npm og de åpne datakildene. Loopback ble bekreftet med en lokal lytter og med begge API-helseadressene og arbeidsrommet.
- PowerShell 7.7.0 ble kjørt portabelt med verifisert SHA-256. Prøven brukte Node.js 24.19.0, npm 11.17.0, Docker Compose 5.5.1 og Microsoft Edge 158.0.4370.33 i headless-modus med skrivebordsvisning på 1440 × 1000. Playwright fra prosjektets låsefil styrte nettleseren.
- Compose-prosjektet `ibe160-v2-readme-trial` startet med to ferske volumer, eget nettverk på `10.247.233.0/28` og portene 19711–19713 på `127.0.0.1`. Begge volumene for `ibe160-v2-owner` ble beholdt.

## Lokal konto og Testskift A

Prøvekontoen `v2-owner-trial` ble opprettet med README-kommandoen. I Edge ble repoets PDF lastet opp og alle fem aktivitetsrader sammenlignet med fasiten. Vognløpet var 700001. Tabellen viser klokkeslett på skiftdatoen 04.02.2030. [PDF](../../Eksempelfiler/Testskift-A.pdf) · [Fasit](../../Eksempelfiler/Fasit-testskift.json)

| # | Aktivitet | Tid | Strekning |
| ---: | --- | --- | --- |
| 1 | Sign-on | 06:50–06:53 | — |
| 2 | Tomkjøring, tur 90101 | 06:58–07:20 | Garasje Måneglimt → Kvartsodden kai |
| 3 | Linje 731, tur 1002 | 07:22–08:10 | Kvartsodden kai → Krystallporten |
| 4 | Tomkjøring, tur 90102 | 08:10–08:25 | Krystallporten → Garasje Måneglimt |
| 5 | Sign-off | 08:26–08:28 | — |

**Alt stemmer – lagre og fortsett** lagret utkastet. Det ble åpnet fra **Mine utkast** før stopp. Nettvisningen ble avsluttet, README-stoppkommandoen satte alle fire containere i `exited`, og de tre prøveportene sluttet å lytte. Etter oppstart med de samme volumene ble det opprettet en ny Edge-kontekst, logget inn på nytt og åpnet samme rad i **Mine utkast**.

Begge åpningene ga ID `b94277ce-a768-4b39-b9aa-e00f6d4c0009` og versjon **1**. Nettlesersvarene var identiske med lagringssvaret, inkludert ID-ene, rekkefølgen og alle feltene i de fem aktivitetsobjektene og kildefaktaene. SHA-256 for det samlede uttrekket av ID, versjon og aktiviteter var `f6d1ea3f56319d8cef9d645336af4e98c95bbd28290bb68771c02ffd3fd41a89`.

## Entur

Opprinnelig README-kommando endte i `zipfile.BadZipFile` fordi arkivet manglet som standard input til importen. Den rettede blokken ble kjørt direkte fra README med prøveprosjektnavnet. Importen publiserte 21 linjer for 30.11.2026, uten uavklarte Quay-ID-er i importkontrollen.

I **Finn avgang i Tromsø** viste linje **28** 125 planlagte avganger for **2026-11-30**. Valgt avgang var **10:05:00 · Solligården → Hamna skole øst · Hamna via sentrum** med tur-ID `TRO:ServiceJourney:28_260918108012843_1036`. Rutegrunnlaget var Entur-generasjon `1795733985884096`, SHA-256 `9c8355bb7c6d088a8f007ab7e826a10c66614b53372f8b789eeb67d3986c3d14`. [Åpent NeTEx-arkiv](https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip)

Stoppfølgen i Edge hadde 38 forekomster i samme rekkefølge som katalogsvaret. Tidene er planlagt avgang, med ankomsttid ved endestoppet.

| # | Holdeplass | Tid |
| ---: | --- | --- |
| 1 | Solligården | 10:05 |
| 2 | Forsvarsmuseet | 10:05 |
| 3 | Durmålselva | 10:06 |
| 4 | Tresletta | 10:07 |
| 5 | Slipelva sør | 10:08 |
| 6 | Slipelva nord | 10:09 |
| 7 | Gammelgård | 10:10 |
| 8 | Kaldslet gård | 10:11 |
| 9 | Reinen | 10:12 |
| 10 | Reinen skole | 10:13 |
| 11 | Hjorten | 10:14 |
| 12 | Pyramiden | 10:15 |
| 13 | Novasenteret | 10:16 |
| 14 | Tromsdalen Bruvegen | 10:17 |
| 15 | Skippergata | 10:20 |
| 16 | Torgsenteret | 10:21 |
| 17 | Fr. Langes gate F1 | 10:23 |
| 18 | Petersborggata | 10:25 |
| 19 | Bispegården | 10:26 |
| 20 | Trykkbassenget | 10:26 |
| 21 | Prestvannet | 10:28 |
| 22 | Stalheim | 10:29 |
| 23 | Soltun | 10:30 |
| 24 | Workinnmarka skole | 10:32 |
| 25 | Klimavegen | 10:33 |
| 26 | Åslivegen | 10:34 |
| 27 | Giæverbukta bussterminal | 10:37 |
| 28 | NKL | 10:38 |
| 29 | Bjorvik | 10:40 |
| 30 | Rideskolen | 10:41 |
| 31 | Bergli | 10:42 |
| 32 | Solneset skole | 10:43 |
| 33 | Fiskekroken | 10:44 |
| 34 | Hamnavegen | 10:45 |
| 35 | Toftvegen sør | 10:46 |
| 36 | Toftvegen nord | 10:47 |
| 37 | Årevegen | 10:48 |
| 38 | Hamna skole øst | 10:49 |

## NVDB

README-importen hentet åpent veggrunnlag for Oslo-dato **27.11.2026** og publiserte revisjon `7229abafd8a94fed24bed0551c3cc79271887aee178261b4682596d8452d9fa8`. Importen omfattet kildeserie 105, 721 og 977. I Edge ble hvert område valgt, vegmatching startet og responsen fra lokal API kontrollert. En simulert nettleserposisjon ble brukt til å starte visningen.

| Vegområde | Retningsbestemte vegkanter | Bekreftede grenser | Vist fartsgrense |
| --- | ---: | ---: | --- |
| Tromsøya | 14387 | 0 | Ukjent |
| Kvaløya (Eidkjosen–Slettaelva) | 6556 | 0 | Ukjent |
| Fastlandet (Skjelnan/Malmvegen–Solligården) | 13335 | 0 | Ukjent |

Den lokale prøven er gjennomført. Fysisk GPS og forvarsel hører til feltprøven, der tallfestet fartsgrense også krever kvalifisert kildegrunnlag. [Feltoppskrift](../v2-field-trial.md)
