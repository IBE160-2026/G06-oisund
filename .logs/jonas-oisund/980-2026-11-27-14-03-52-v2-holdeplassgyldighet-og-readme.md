# V2-holdeplassgyldighet og README

## 2026-11-27 kl. 14:03 - Jonas Øisund

### Oppgave

Rett kvalifiseringen av entydige plattformer i V2 under utviklingsfrysen. Skriv en selvstendig lokal prøveoppskrift for faglærer.

### Plan

- Avstem fersk GitHub main mot v2.0.0 og dokumenter Enturs kildegrunnlag per stoppforekomst.
- Kjør samme katalogkontroll over hele feltperioden, prøv de utpekte turene og dokumenter importbehov.
- Prøv README fra ren utsjekk og hold de to leveransene i egne lokale commits.

### Resultat

GitHub main 3457d08 ble verifisert og lokalt rekonstruert med identiske Git-objekter etter at direkte kloning feilet på DNS. Holdeplassretting og feltoppskrift ligger i 8f02300. README ligger i 3a31147.

På de samme 418 428 forekomstene gikk 7 280 av 7 280 over fra validity-unknown til GPS-kvalifisert. De 411 148 tidligere kvalifiserte forekomstene beholdt plattform, stoppested, versjon og koordinater. Enturs daterte GTFS-uttrekk bekreftet NeTEx-turer og samsvarende stopp, samt samme koordinater på de sju plattformene. Se [feltoppskriften](../../docs/v2-field-trial.md#holdeplassprogresjon-i-feltkatalogen).

25 Python-prøver, 24 Node-prøver og TypeScript/Vite-bygg besto. Syntetiske GPS-prøver brukte de faktiske stoppene fra de valgte turene i Hamna, ved flyplassen, Sandvik kryss og Prostneset. Turen over midnatt ble kontrollert mot faktisk kalenderdato og plattform. Ny NSR-revisjon krever ny import ved senere kodeoppdatering. Gamle rutevalg beholder sin fryste referanse.

README-kommandoblokkene kunne parses og Compose-konfigurasjonen validerte. Ren utsjekk av 3a31147 hadde ingen runtime-mappe eller node_modules ved oppstart. Den nøyaktige oppstartskommandoen stoppet på avvist tilgang til Docker Desktop-motorens lokale pipe før første tjeneste startet. Den ordinære PDF-tolkingen fra den rene utsjekken ga Testskift A med dato 04.02.2030, fem aktiviteter og vognløp 700001. Den offentlige ruteimportleseren godtok frosset bunt uten databaseskriving, med 21 linjer, 125 avganger på linje 28 og null manglende Quays for 30.11. Det eldre NVDB-prøvearkivet manglet kildeserie 977. Den løpende NVDB-innhentingen og publisering i det lokale Docker-miljøet er ikke verifisert denne økten.

#### Lokal Windows-prøve

Codex fikk godkjent tilgang til Docker og nettverk. Docker rapporterte `linux`, og prøven startet fra en verifisert ren desktop-utsjekk med separat prosjekt, egne volumer, eget nettverk og portene 19711–19713. De to standardvolumene ble kontrollert etter avslutning.

I Edge ble Testskift A lagret med lokal prøvekonto. Et nytt nettleservindu etter full Compose-stopp og oppstart åpnet samme ID og versjon 1 med alle fem aktivitetsobjektene identiske. Den rettede Entur-importen publiserte 21 linjer. Oppslag av linje 28 kl. 10:05 den 30.11.2026 viste 38 stopp. NVDB-importen ga veggrunnlag for tre områder, alle med **Ukjent** fartsgrense i prøven. README-punktet er lukket. Se [prøverapporten](../../docs/evidence/v2-readme-windows-20261127.md).

Isolert oppstart ligger i `a00740a`, Entur-rettingen i `87374b5` og prøverapporten med README-presisering i `f7e82ac`. Prøvemiljøet ble stoppet etter oppslagene. Prøvevolumene ble beholdt.

### Åpne punkter

- Prøv fysisk GPS, progresjon og gjenopptak på bussen. Ved senere kodeoppdatering må rutekatalogen importeres på nytt for å ta i bruk den nye NSR-revisjonen.
