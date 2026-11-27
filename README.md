# Bussassistent V2 for Tromsø

Bussassistenten importerer skiftplaner fra tekst-PDF og lar sjåføren kontrollere, lagre og åpne dem igjen. Sjåføren kan slå opp daterte avganger, velge tur og starte holdeplassassistanse. Appen kan også vise avvik, GPS-fart og fartsgrense med 300 m-forvarsel der datagrunnlaget støtter det.

## Kjør lokalt

Oppskriften er for Windows med Git, PowerShell 7.2 eller nyere, Node.js 24 med npm og Docker Desktop med Compose v2 og Linux-containere. Start Docker Desktop og sjekk at `docker info` viser en Linux-server. Portene 19661–19663 må være ledige ved første oppstart. GitHub-kloning, første bygg av containerne og npm-installasjonen trenger internett.

**Ny klone.** Åpne PowerShell 7 i mappen du vil legge prosjektet i.

```powershell
git clone https://github.com/IBE160-2026/G06-oisund.git bussassistent
Set-Location bussassistent
```

**Allerede oppdatert med `git pull` på `main`.** Åpne PowerShell 7 i den eksisterende prosjektmappen. Her ligger `compose.v2.yaml`, `scripts` og `Eksempelfiler`.

Kjør fra prosjektmappen i begge tilfeller.

```powershell
pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner
```

Terminalen viser helseadressene etter at containerne er klare. Vent på `Open http://127.0.0.1:19661/private` og at Vite viser adressen som klar. La terminalen stå åpen. [Åpne det lokale arbeidsrommet](http://127.0.0.1:19661/private).

### Opprett prøvekonto og lagre et skift

Åpne en **andre PowerShell 7-terminal** i samme prosjektmappe mens appen kjører. Opprett prøvekontoen én gang. Skriv et lokalt passord på minst 12 tegn når terminalen ber om det.

```powershell
docker compose -p ibe160-v2-owner -f compose.v2.yaml exec private-api python -m app.manage provision v2-owner-trial
```

1. Logg inn som `v2-owner-trial` på [det lokale arbeidsrommet](http://127.0.0.1:19661/private). Du skal se **Mine utkast**.
2. Under **Velg tekst-PDF** åpner du [Eksempelfiler/Testskift-A.pdf](Eksempelfiler/Testskift-A.pdf) fra prosjektmappen. **Importsammendrag** viser fem aktiviteter i det syntetiske skiftet. Åpne **Vis alle kildefakta fra PDF** og sammenlign aktivitetene med skift A i [fasiten](Eksempelfiler/Fasit-testskift.json).
3. Velg **Alt stemmer – lagre og fortsett**. Vent til skjermen for gjennomgang av det lagrede utkastet vises.
4. Velg **Forberedelse og planlister**. Under **Mine utkast** åpner du raden **Åpne … · versjon 1** og kontrollerer at det samme skiftet vises.

Konto, PDF og lagring fungerer på din egen PC. Du bruker ditt eget lokale passord og filen som følger med repoet. Ubuntu-serveren og Cloudflare Access brukes i feltoppsettet.

### Stopp og åpne skiftet igjen

Trykk Ctrl+C i den første terminalen for å stoppe nettvisningen. Kjør deretter stoppkommandoen fra prosjektmappen.

```powershell
pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner -Stop
```

Start igjen med `pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner`. Logg inn med samme konto og åpne det samme utkastet under **Mine utkast**. Stopp bevarer Docker-volumene og den lokalt opprettede databasenøkkelen i `.private-runtime`. Bruk samme prosjektmappe ved ny oppstart. Utkast utløper sju dager etter opprettelse. Oppstartsskriptet kjører npm-installasjon ved hver oppstart. Et nytt bygg kan hente avhengigheter eller containerbilder.

Hvis siden ikke åpner, sjekk at Vite fortsatt kjører og at [privat API](http://127.0.0.1:19663/health) svarer. Bruk `docker compose -p ibe160-v2-owner -f compose.v2.yaml ps` fra prosjektmappen for å se tjenestestatus.

### Kjør prøven ved siden av et eksisterende miljø

Bruk en ren, separat utsjekk for å starte med en tom database og uten tidligere nedlastede data. Velg et ubrukt Compose-prosjektnavn, tre sammenhengende ledige loopback-porter og et subnett som ikke overlapper eksisterende Docker-nettverk. Eksempel:

```powershell
$prove = @('-Mode', 'Owner', '-ProjectName', 'ibe160-v2-readme-trial', '-UiPort', '19711', '-Subnet', '10.247.233.0/28')
pwsh -NoProfile -File scripts/v2-local.ps1 @prove
```

Åpne `http://127.0.0.1:19711/private`. Bruk `ibe160-v2-readme-trial` som prosjektnavn i kontokommandoen, tjenestestatus og begge importene nedenfor. Helseadressene bruker port 19712 og 19713. Bruk samme utsjekk og de samme argumentene for å starte igjen, og legg til `-Stop` for å stoppe. Det nye prosjektnavnet gir egne Docker-volumer, eget nettverk og egen databasenøkkelfil.

## Datagrunnlag lokalt

| Funksjon | Tilgjengelig lokalt |
| --- | --- |
| PDF, utkast og godkjenning | Virker med lokal konto og eksempelfil etter oppstart. |
| Ruteoppslag og holdeplassassistanse | Importer offentlige Entur-rutetider og NSR-plattformer for driftsdatoen. Automatisk progresjon krever valgt tur, et eksplisitt startpunkt og god nok GPS. |
| GPS-fart | Krever posisjonstillatelse og en fersk fartsmåling fra enheten. På en stasjonær PC kan fart mangle. |
| Vegmatching og fartsgrense | Importer en NVDB-pakke for aktuell Oslo-dato. Tallfestet grense og forvarsel krever ytterligere kvalifisert kildegrunnlag. Den løpende vegdatainnhentingen og WFS-oppdateringen er prøvd i Ubuntu-feltoppsettet. |
| Automatiske avvik | Oppdatering fra Entur krever internett. Koblingen til turen avhenger av hva Entur har publisert og hvilken rute som er bekreftet. |

**Datagrunnlag mangler for denne linjen og driftsdatoen** betyr at det lokale ruteoppslaget svarte, men at det ikke har en katalog for valget. **Ingen planlagt avgang denne dagen** betyr at en katalog er tilgjengelig og viser null avganger.

### Valgfritt — importer Entur-data

Kjør fra prosjektmappen i den andre terminalen mens appen er startet. Velg en dato i Enturs publiserte rutetabell. Dette henter åpne NeTEx-rutetider for Troms og NSR-plattformer, og krever internett fra Docker.

```powershell
$dag = '2026-11-30'
$lokal = @('-p', 'ibe160-v2-owner', '-f', 'compose.v2.yaml')
docker compose @lokal cp deploy/ubuntu/public_route_download.py private-api:/tmp/ibe160-public-route-download.py
docker compose @lokal exec -T private-api sh -ec 'arkiv=$(mktemp); trap "rm -f $arkiv" EXIT; python /tmp/ibe160-public-route-download.py > "$arkiv"; python -m app.route_catalogue --bundle-stdin --publish --from-date "$1" --through-date "$1" < "$arkiv"' sh $dag
```

Et vellykket resultat viser avgangstall for de 21 linjene. Åpne **Finn avgang i Tromsø** i arbeidsrommet, velg driftsdato og linje, og trykk **Hent avganger**. I det frosne feltgrunnlaget for 30.11.2026 hadde linje 28 125 avganger, blant dem **10.05 Solligården → Hamna skole øst** med 38 stopp. Ved senere prøving bytter du til en aktuell driftsdato. Entur fjerner eldre avganger fra det løpende uttrekket. [Datakilder og feltoppskrift](docs/v2-field-trial.md).

### Valgfritt — importer veggrunnlag

Kjør fra prosjektmappen mens appen er startet. Angi dagens dato i Oslo. Kommandoen henter et arkiv fra NVDB, validerer det og importerer det i lokal database. Hentingen krever internett fra Docker.

```powershell
$vegdag = '2026-11-30' # Bytt til dagens Oslo-dato
$lokal = @('-p', 'ibe160-v2-owner', '-f', 'compose.v2.yaml')
docker compose @lokal exec -T private-api sh -ec 'mappe=$(mktemp -d); trap "rm -f $mappe/veg.zip; rmdir $mappe" EXIT; python -m app.road_area_evidence --date "$1" --output "$mappe/veg.zip"; python -m app.road_area_catalogue "$mappe/veg.zip" --publish' sh $vegdag
```

Under **Vegområde og GPS-fart** velger du område og trykker **Start vegmatching**. Nettleseren kan be om posisjonstillatelse. En pakke fra NVDB alene gir veggrunnlag for Tromsøya, Kvaløya og fastlandet, med **Ukjent** fartsgrense der bekreftelse mangler. [Krav til skilt, reguleringer og forvarsel](docs/v2-field-trial.md#oppdatering-og-tilbakeføring).

## Versjoner og feltprøver

[Publisert v2.0.0](https://github.com/IBE160-2026/G06-oisund/releases/tag/v2.0.0) er sammenligningsgrunnlaget. På arbeidsgrenen er 7 280 tidligere uavklarte stoppforekomster på sju plattformer kvalifisert i den automatiserte katalogkontrollen. Tidligere kvalifiserte forekomster beholdt riktig plattform og koordinater. Fysisk GPS og faktisk progresjon på bussen gjenstår. [Testrapport og feltoppskrift](docs/v2-field-trial.md#holdeplassprogresjon-i-feltkatalogen).

## Innlevering og dokumentasjon

- [V1-milepæl, leveranse og prøveoppskrift](docs/submission/README.md)
- [Revidert PRD etter faglærerens tilbakemelding](_bmad-output/planning-artifacts/prds/prd-IBE160-2026-09-21/prd-revised-v1.0.1.md) og [arkitektur](_bmad-output/planning-artifacts/architecture/README.md)
- [V1-akseptansebevis](docs/evidence/v1-acceptance-2026-10-29.md), [V2-testbevis](docs/v2-handoff.md) og [Android-prøver](docs/v2-android-test-handoff.md)
- [Ubuntu-drift, backup og gjenoppretting](docs/ubuntu-server.md) og [O6-etterkontroll](docs/evidence/o6-kernel-44-20261127.md)

Jonas Øisund · IBE160 Programmering med KI · Høgskolen i Molde · høsten 2026
