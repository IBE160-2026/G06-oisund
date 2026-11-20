# Privat Android-prøve

## 2026-11-20 kl. 21:10 — Jonas Øisund

### Oppgave
Klargjøre hjemmemaskinens isolerte IBE160 V2- og TIDE-piloter for to Android-enheter tilkoblet laptopen via USB. Laptop-økten gjennomfører de fysiske prøvene.

### Plan
- Kontroller gjeldende arbeidskopier, eksisterende lagre og lokale lyttere. Bruk hver app sin faste loopback-opprinnelse.
- Start nye isolerte databaser og klargjør fiktive arbeidsflyter. Koble deretter de tre nødvendige app-portene via et privat tailnet.

### Resultat
- IBE160 V2 bygget fra `5ddcb67` på `codex/integrate-bussassistent-v2`. Compose-prosjekt `ibe160-v2-android-20261120` har egne volumer og fiktive data. UI og privat API svarer på loopback 19661 og 19663. Separat fiktiv API på 19662 svarer lokalt.
- To fiktive kontoer ble innlogget i installert Edge fra separat profil per konto. Nettleseren ba om privat API på `127.0.0.1:19663`. Import av generert syntetisk PDF, lagringskvittering og gjenåpnet utkast bestod for begge. Prøvepassord ligger i prosjektets ignorerte runtime-mappe.
- TIDE `d8254e4` kjører på loopback 4173 med en egen SQLite-fil. Innlogging med lokal engangskode, 22 førkriterier for kandidat og egen instruktørvisning er verifisert. Rollen og prøveløpet er klart for laptop.
- Brukeren installerte en signaturverifisert Tailscale-klient og logget inn på hjemmemaskinen. Serve konfigurerte privat TCP for 4173, 19661 og 19663. Alle tre ga HTTP 200 gjennom hjemmemaskinens tailnet-adresse med opprinnelig loopback-Host. Ingen produksjonskobling ble brukt.
- Laptop-økten rapporterte fire beståtte fysiske lagringsprøver på Lenovo og Pixel. IBE160 lagret norsk prøveinnhold i Buss/vogn og gjenåpnet versjon 2 i hver konto. TIDE lagret instruktørkommentarer sekvensielt fra begge enheter, og begge gjenåpnet de to kommentarene i revisjon 2. Hjemmekontroll av prøvelagrene ga revisjon 2 for begge IBE160-kontoene og TIDEs instruktørutkast. TIDE-løpet står under kjøring. Skjermbilder og DOM-bevis ligger på laptopen.

### Åpne punkter
- Fysisk lagring og gjenåpning er verifisert. GPS, tillatelser og feltprøvene står fortsatt under «V2 fysisk nettbrett/GPS». Det verifiserte hjemmemiljøet står på til videre Codex-testing.
