# Fysisk Android-test for IBE160 V2

## Oppsett og verifisert dekning

Hjemme-PC-en kjører de isolerte testappene. Det private tailnettet fører TCP-portene 19661, 19663 og 4173 til laptopens loopback-relay. Laptopen videresender de samme portene med `adb reverse` til begge Android-enhetene og styrer Brave. Lenovo TB361FU kjører Android 16 (API 36), og Pixel 10 Pro XL kjører Android 17 (API 37). USB-listen på laptopen er kilden til enhetsseriene.

| App | Adresse på enheten | Verifisert byggegrunnlag | Isolerte data |
| --- | --- | --- | --- |
| IBE160 V2 | `http://127.0.0.1:19661/private` med privat API på `http://127.0.0.1:19663` | `codex/integrate-bussassistent-v2` ved `5ddcb674ced4700cd6177598ff3c325506637155` | Compose `ibe160-v2-android-20261120` med separate testvolumer for `private_work` og `fictional_assessment`. Bruk de to godkjente syntetiske kontoene og PDF-prøveutkastene. |
| TIDE Epic 4 | `http://127.0.0.1:4173/testkjoring/` | `codex/epic-4` ved `d8254e4` | Pilotens egen `pilot.sqlite` og det avtalte fiktive prøveløpet. Bruk den godkjente instruktørkontoen. |

Fire fysiske lagringsprøver bestod 20. november 2026. IBE160 lagret ulik tekst med æ, ø og å i Buss/vogn fra hver enhet og gjenåpnet samme tekst i versjon 2 etter omlasting. TIDE lagret Lenovo-kommentaren i revisjon 1 og Pixel-kommentaren i revisjon 2. Begge viste de to kommentarene etter omlasting. Vurderingen ble stående som et utkast under kjøring. Laptopens prøver dekket UI, innskriving, aktivering, skjermbilder og kontroll av lagret resultat i Brave. Hjemmemaskinen verifiserte de lagrede revisjonene. Alle tre lokale HTTP-adressene svarte 200 da dette notatet ble skrevet. [Lokal prøvelogg](../.logs/jonas-oisund/984-2026-11-20-21-10-49-privat-android-prove.md).

GPS, Androids stedstillatelser, Chrome på enhetene, feltkjøring og full vurderings- og PDF-regresjon står åpne. Bruk syntetiske posisjoner til automasjon. Reell posisjon krever egen avklaring. Automatisk gjenoppstart etter omstart er uavklart. PC-ene, testtjenestene, tailnettet og relayet må være oppe, og enhetene må være USB-tilkoblet, godkjent og opplåst. Ny USB-godkjenning og fysisk opplåsing kan kreve Jonas.

## Bestill en avgrenset prøve

Laptopoverleveringen oppgir at Jonas har gitt stående godkjenning til at akkurat IBE160-, TIDE- og laptopchatten kan bestille og returnere prøver på de to godkjente USB-enhetene i isolerte miljøer. Godkjenningen omfatter bruk av de allerede godkjente prøveidentitetene. Bruk syntetiske data og hold legitimasjon utenfor meldinger og bevis. Bruk bare disse tre chattene til samordningen. Produksjonsendringer, publisering, utrulling, merge og push ligger utenfor denne godkjenningen.

1. Kontroller aktivt bygg, testadresse og hvilke testdata oppdraget kan endre. Ta med branch og commit i bestillingen. Et nytt bygg trenger eget resultat.
2. Finn laptopchat `01a1fa77-9521-7fc1-b451-a63ab3b3e304` med `list_threads` og bruk den returnerte `hostId`. Les autorisasjonen i kildetråden med `read_thread`. Ved overleveringen viste verktøyet herfra bare hjemmemaskinens lokale vert. Laptopchatten kunne derfor ikke leses direkte eller nås gjennom verifisert ruting fra denne verten.
3. Når målverten er tilgjengelig, send ett oppdrag med `send_message_to_thread` til laptopchatten. Oppgi prosjekt, byggegrunnlag, avsenderens chat-ID, enhet, testadresse, syntetiske forutsetninger, trinn, forventet UI og tillatte dataendringer. Laptopchatten eier køen. Den kjører bare ett oppdrag av gangen på hver enhet. For TIDE skal hver skriver laste gjeldende revisjon før neste lagring.
4. Bruk `wait_threads` og kontroller den faktiske kvitteringen. Før bygg, enhet og nettleser, trinn, observert resultat, vedvarende revisjon og plassering av bevis. Registrer prøven som utført først når resultatet er kontrollert.

**Reserveflyt ved manglende laptopvert.** Legg den samme fullstendige testbestillingen i IBE160-prosjektchatten. En aktiv laptopøkt kan hente den med `read_thread` fra prosjektchat `01a1f658-903b-7231-840f-51298b17a555` og returnere resultatet til samme prosjektchat med `send_message_to_thread`. Laptop → prosjekt er bekreftet av de mottatte overleveringsmeldingene. En bestilling i prosjektchatten blir liggende til en aktiv laptopøkt henter den. Hentingen krever ingen manuell kopiering av kommandoer eller testdata.

Eksempel på bestilling til laptopchatten

> IBE160 V2, branch og commit [bygg], svar til [avsenderens chat-ID]. Bruk [Lenovo eller Pixel] i Brave på `http://127.0.0.1:19661/private` med en godkjent syntetisk prøvekonto. Bruk bare et nytt syntetisk PDF-utkast. Endre Buss/vogn til [prøvetekst], lagre og vent på kvittering. Last på nytt, gjenåpne utkastet og kontroller forventet versjon og tekst. Returner observert resultat og lokal bevissti.

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

`activate` kan velge en HTML-kontroll med en presis selektor. `read` maskerer passord. Bruk `wait` eller `read` etter handlinger, og bekreft lagringen etter gjenåpning. Hold IBE160 i forgrunnen mens forespørselen pågår. Bruk `Start-app-tests.cmd` ved behov når det etablerte relayet er stoppet.

På laptopen ligger sammendraget i `outputs/App-testresultater.json` og `outputs/USB-oppsett-og-testresultater.txt`. Bevisene per enhet ligger i `outputs/evidence/<USB-serie>/`, blant annet `ibe-persisted.json`, `ibe-verified.png`, `tide-persisted.json` og `tide-native-verified.png`. Oppstart og stans på hjemmemaskinen er dokumentert i `D:\TIDE vurderingsskjema\.cache\private-android-transport\overlevering.md`. Samordne stans med begge prosjektchattene slik at testdata og andre tjenester bevares. Tailscale Serve er privat. Relayet på laptopen lytter på loopback.
