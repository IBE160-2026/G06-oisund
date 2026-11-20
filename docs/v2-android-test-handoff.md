# Fysisk Android-test for IBE160 V2

## Oppsett og verifisert dekning

Hjemme-PC-en kjører de isolerte testappene. Det private tailnettet fører TCP-portene 19661, 19663 og 4173 til laptopens loopback-relay. Laptopen videresender de samme portene med `adb reverse` til begge Android-enhetene og styrer Brave. Lenovo TB361FU kjører Android 16 (API 36), og Pixel 10 Pro XL kjører Android 17 (API 37). USB-listen på laptopen er kilden til enhetsseriene.

| App | Adresse på enheten | Verifisert byggegrunnlag | Isolerte data |
| --- | --- | --- | --- |
| IBE160 V2 | `http://127.0.0.1:19661/private` med privat API på `http://127.0.0.1:19663` | `codex/integrate-bussassistent-v2` ved `5ddcb674ced4700cd6177598ff3c325506637155` | Compose `ibe160-v2-android-20261120` med separate testvolumer for `private_work` og `fictional_assessment`. Bruk de to godkjente syntetiske kontoene og PDF-prøveutkastene. |
| TIDE Epic 4 | `http://127.0.0.1:4173/testkjoring/` | `codex/epic-4` ved `d8254e4` | Pilotens egen `pilot.sqlite` og det avtalte fiktive prøveløpet. Bruk den godkjente instruktørkontoen. |

Fire fysiske lagringsprøver bestod 20. november 2026. IBE160 lagret ulik tekst med æ, ø og å i Buss/vogn fra hver enhet og gjenåpnet samme tekst i versjon 2 etter omlasting. TIDE lagret Lenovo-kommentaren i revisjon 1 og Pixel-kommentaren i revisjon 2. Begge viste de to kommentarene etter omlasting. Vurderingen ble stående som et utkast under kjøring. Laptopens prøver dekket UI, innskriving, aktivering, skjermbilder og kontroll av lagret resultat i Brave. Hjemmemaskinen verifiserte de lagrede revisjonene. Alle tre lokale HTTP-adressene svarte 200 da dette notatet ble skrevet. [Lokal prøvelogg](../.logs/jonas-oisund/984-2026-11-20-21-10-49-privat-android-prove.md).

GPS, Androids stedstillatelser, Chrome på enhetene, feltkjøring og full vurderings- og PDF-regresjon står åpne. Bruk syntetiske posisjoner til automasjon. Reell posisjon krever egen avklaring. PC-ene, testtjenestene, tailnettet, relayet og arbeideren må være oppe, og enhetene må være USB-tilkoblet, godkjent og opplåst. Ny USB-godkjenning og fysisk opplåsing kan kreve Jonas.

### Fysisk visning av PDF-kildefakta

På byggegrunnlag `5ddcb67` bestod funksjonsprøven i Brave på både Lenovo og Pixel. Begge åpnet sitt syntetiske utkast i versjon 2 med riktig Buss/vogn-verdi, åpnet **Vis kildefakta fra PDF** og så **Kildefakta fra PDF · ikke bekreftet** og **Vognløp i kildeorden**. Etter at panelet var lukket, gjenåpnet begge utkastet med samme versjon og Buss/vogn-verdi. Prøven gjorde ingen lagring eller endring i appen.

Første åpning av utkastet måtte gjentas på begge enhetene. Lenovo viste **«Tjenesten er utilgjengelig. Inndata er beholdt.»** før det nye forsøket. Utkast- og sesjonsoppslagene ga deretter HTTP 200 på Lenovo. Den senere gjenåpningen i prøven fungerte på første forsøk på begge enhetene. Årsaken til de første forsøkene er uavklart.

Resultatet er rapportert av laptopøkten, med JSON- og skjermbildebevis i hver enhetsmappe på laptopen. Bruk `outputs/evidence/<USB-serie>/ibe-pdf-source-facts.json` og `outputs/evidence/<USB-serie>/ibe-pdf-source-facts.png`.

## Køtest fra prosjektchatten

Fra IBE160-prosjektchatten på hjemmemaskinen kan `read-only-smoke` og `pdf-source-facts` bestilles via `http://127.0.0.1:4185/jobs`. Den avgrensede arbeideren på laptopen kjører uavhengig av laptopchatten, henter køjobber på den private arbeiderporten 4186 og bruker de to godkjente USB-enhetene. Innsending på 4185 er lokal på hjemmemaskinen. Jobbene behandles sekvensielt.

Kontroller aktivt bygg før innsending. `read-only-smoke` leser synlig IBE160-UI i Brave på begge enhetene uten innlogging. `pdf-source-facts` bruker eksisterende godkjente syntetiske kontoer og de lagrede PDF-utkastene i versjon 2. Den kontrollerer kildefaktapanelet, lukker det og gjenåpner utkastet med uendret versjon og Buss/vogn. Ingen av prøvene endrer appdata. Godkjenningen gjelder de to godkjente enhetene og isolerte testmiljøer. Bruk syntetiske data og hold legitimasjon utenfor bestillinger og bevis.

Kjør én gang på hjemmemaskinen. Responsen skal ha HTTP 202 og en jobb-ID.

```powershell
$queue = 'http://127.0.0.1:4185/jobs'
$receipt = Invoke-WebRequest -Method Post -Uri $queue -ContentType 'application/json' `
  -Body '{"project":"IBE160","test":"pdf-source-facts"}'
if ($receipt.StatusCode -ne 202) { throw "Uventet svar $($receipt.StatusCode)" }
$id = ($receipt.Content | ConvertFrom-Json).id
$id
```

Les deretter den samme jobben til den er ferdig. Ta vare på ID-en ved tidsavbrudd og fortsett med GET.

```powershell
$job = Invoke-RestMethod -Method Get -Uri "$queue/$id"
$job | ConvertTo-Json -Depth 5
```

Sjekk at ID-en stemmer, at `state` er `completed` og at både `Lenovo` og `Pixel` har `passed: true`. Status `queued` eller `running` er fortsatt pågående. Status `expired` eller `passed: false` betyr at prøven ikke er bestått.

Den 20. november 2026 ga IBE160-innsendingen HTTP 202 for jobb `6b0948b9-bef2-4832-8174-04ce03b5e2c0`. Køen gikk fra `queued` via `running` til `completed`, med `passed: true` for begge enheter. Laptopens lokale bevis for samme ID bekreftet HTML-sidetittelen **Fiktiv arbeidsdag** på begge enhetene. Arbeideren krevde også riktig URL med unik jobb-ID og synlig «Privat tilgang» eller «Privat arbeidsrom». Køkvitteringen inneholder bare beståttstatus per enhet.

Den 20. november 2026 ga første `pdf-source-facts`-bestilling HTTP 202 for jobb `5460fcfe-e702-4681-9824-53f2d078c3b9`. Jobben gikk fra `queued` via `running` til `completed`, med `passed: false` på både Lenovo og Pixel. IBE160s UI og private helseendepunkt svarte HTTP 200 etter prøven. En lesende kontroll i den isolerte testdatabasen fant begge forventede utkastene med samme Buss/vogn-markører, gyldig utløpstid, PDF-kildefakta og revisjon 2.

Laptopøkten fant at arbeideren fortsatte etter at overskriften var synlig, mens utkastknappene fortsatt ble lastet. Arbeideren ble endret til å vente på den aktive **Åpne 2030-01-01 · versjon 2**-knappen før den fortsetter. Første jobb står som **ikke bestått** i køhistorikken.

Den ene koordinerte erstatningsjobben `f306874a-b3e2-40ee-8e17-7b31b0d0932c` fikk HTTP 202 og endte som `completed` med **`passed: true` på både Lenovo og Pixel**. Begge sluttkvitteringene ble lest tilbake fra køhistorikken. En ny lesende databasekontroll fant begge utkastene med uendrede Buss/vogn-markører, gyldig utløpstid, PDF-kildefakta og revisjon 2.

## Kommandoer på laptopen

Kjør fra den etablerte arbeidsmappen `C:\Users\joisu\Documents\Codex\2026-11-20\klargj-r-denne-laptopen-for-at`. Erstatt `SERIAL` med USB-serien for den valgte godkjente enheten. Relayet bruker 19221 for Lenovo og 19222 for Pixel til Braves nettleserstyring.

```powershell
.\work\tools\platform-tools\adb.exe devices -l
node outputs/mobile-browser.mjs read SERIAL http://127.0.0.1:19661/private
node outputs/mobile-browser.mjs fill SERIAL http://127.0.0.1:19661/private "#felt-id" "Prøvetekst æøå"
node outputs/mobile-browser.mjs press SERIAL http://127.0.0.1:19661/private "Eksakt knappetekst"
node outputs/mobile-browser.mjs wait SERIAL http://127.0.0.1:19661/private "Forventet tekst"
node outputs/mobile-browser.mjs reload SERIAL http://127.0.0.1:19661/private
node outputs/mobile-browser.mjs capture SERIAL http://127.0.0.1:19661/private bevisnavn
node outputs/usb-control.mjs capture SERIAL
```

`activate` kan velge en HTML-kontroll med en presis selektor. `read` maskerer passord. Bruk `wait` eller `read` etter handlinger, og bekreft lagringen etter gjenåpning. Hold IBE160 i forgrunnen mens forespørselen pågår. Bruk `Start-app-tests.cmd` ved behov når det etablerte relayet er stoppet. Etter omstart kan arbeideren startes med `Start-Android-test-worker.cmd` i vanlig Windows-økt på laptopen. Det er ingen registrert automatisk oppstart av arbeideren.

På laptopen ligger sammendraget i `outputs/App-testresultater.json` og `outputs/USB-oppsett-og-testresultater.txt`. Bevisene per enhet ligger i `outputs/evidence/<USB-serie>/`, blant annet `ibe-persisted.json`, `ibe-verified.png`, `tide-persisted.json` og `tide-native-verified.png`. Oppstart og stans på hjemmemaskinen er dokumentert i `D:\TIDE vurderingsskjema\.cache\private-android-transport\overlevering.md`. Samordne stans med begge prosjektchattene slik at testdata og andre tjenester bevares. Tailscale Serve er privat. Relayet på laptopen lytter på loopback.
