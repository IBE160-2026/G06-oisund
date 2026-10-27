---
type: technical
topic: Fartsgrensevisning og forvarsel
decision: Behold aktuell vegfartsgrense og fast 300m-forvarsel i en liten kvalifisert pilot
source: primary-web-and-bounded-public-API
status: complete-with-qualification-gaps
created: 2026-10-27
updated: 2026-10-27
verified_claims: 0
unverified_claims: 3
---

# Teknisk undersøkelse

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Anbefaling

Planlegg begge visningene, men avgrens første demonstrasjon til én kvalifisert korridor. Data finnes i Tromsø; full dekning, pålitelig vegtilknytning og korrekt videre bussveg er ikke påvist. Offisielle skiltvektorer finnes. Gjenbruk disse fremfor nytegning/KI; konkret lisensspor må følge filene.

Muligheten for 300m-forvarsel følger av en foreslått sammensetning av nettverksdata og posisjonsbevis, ikke av en demonstrert ferdig kilde.

Dette er avgrenset BMAD Deep Recon Run, ikke produktverifikasjon. **D** betyr dokumentert støtte i primærkilde; **O** betyr observert i lite kildeuttrekk; **A** betyr teknisk anbefaling; **U** betyr utestet eller uavklart. D/O er ikke uavhengig bekreftet sannhet om virkelige skilt. Nesten all faglig kildeinformasjon kommer fra samme produsent; verifikasjonstillit er middels og ledgerstatus unverified når en uavhengig kilde mangler.

## Vegdata, retning og aktualitet

**D:** NVDB tilbyr vegnett og fartsgrensedata også utover riks-/fylkesveg. Det er et relevant grunnlag, uten kommunal fullstendighetsgaranti [1]. V4 dokumenterer segmenter, topologi og avgrenset geografisk uthenting [2]. Posisjonsoppslag knytter et enkelt punkt til vegnettet; det dokumenterer ikke en kvalifisert målesekvens [3].

**D/O:** Type 105 er Fartsgrense, med verdi i egenskap 2021. Det hentede katalogobjektets linjestedfesting har retning_relevant=false og kjørefelt_relevant=KAN [4]. Utvalget har likevel MED i stedfesting/segmenter. **A:** Ikke tolk dette som at verdien bare gjelder én kjøreretning. Kvalifiser katalogens og segmentenes betydning, særlig separate kjørebaner/felt og motgående kjøring. Vegreferansens metreringsretning kan være motsatt lenkeretning [5].

**D:** Vegobjekter har versjoner og historikk; endringsstrøm er paginert og kan aggregere hendelser [6][7]. **A:** Skill virkningsdato, databaseendring, vegnettversjon, hentet tidspunkt og sist kontroll. Alle må valideres samlet før aktiv visning. Dokumentasjonen er ikke bevis for oppdateringsforsinkelse i felt.

**D:** NVDB har beta-ruteberegning gjennom sammenhengende vegnett [8]. **A:** Bruk den eventuelt ved forberedelse/kvalifisering. En beregnet veg mellom stopp beviser ikke bussens faktiske trasé. Detaljert løsning for lokal flermålingsmatching er vårt forslag, beskrevet i [planen](../../plan.md), ikke en NVDB-garanti.

## Lite Tromsø-utvalg

**O:** Ett GET med kommune=5501, antall=3 og begrenset inkluder-liste ga tre objekter; ingen neste side ble hentet [9]. Utvalget ble beholdt for kontrast mellom fylkesveg, kommunal veg og kryssdel, ikke valgt som statistisk utvalg eller komplett bytrasé.

| Objekt / versjon | Registrert verdi | Vegreferanse | Hva eksemplet belyser |
|---|---|---|---|
| 91467734 / 5 | 60 km/t | FV858 S8D1 m7810–13660 | Lengre intervalldata på to lenkesekvenser, Eidvegen/Straumsvegen. |
| 91467735 / 5 | 60 km/t | KV858 S1D1 m0–114 | Kommunal veg og kort intervall. |
| 91467736 / 3 | 50 km/t | FV862 S2D1 m3675 KD1 m0–89 | Rundkjøring på lenke 1125954; videre arm krever særskilt avklaring. |

Alle tre oppgir sist_modifisert=2025-04-30T22:07:26Z. Det er ikke bevis for at reguleringen er gammel/feil, og dagens henting gjør ikke reguleringen ny. Utvalget dokumenterer verken tilstøtende 60→50-endring, motsatt retning, fysisk skilting, sentrum eller tunnel. Kommunefilteret er Tromsø kommune, ikke et løfte om bysentrum. Full pilotdekning må telles per lenkeintervall/retning, inkludert hull og konflikter; ikke bare som antall objekter.

## Skiltillustrasjoner og vilkår

**D:** Vegvesenet publiserer EPS-/bildepakker og fargeanvisninger [10]. Geonorges Trafikkskilt-pakke oppgir Statens vegvesen som eier [11]. Konkrete oppføringer 362_40 og 362_50 lenker SVG, PNG og TIFF [12][13]. **O:** 362_40.svg ble hentet med HTTP 200 (24 437 byte); originalen ligger som researchbelegg i imports/, uten endring eller produktintegrasjon [12]. Visuell kontroll ved faktisk ikonstørrelse gjenstår.

**D:** Trafikkskilt- og NVDB-datasettene er merket NLOD [1][14]. NLOD tillater viderebruk med navngivelse og uten villedende fremstilling eller inntrykk av offentlig godkjenning [15]. **U:** Den konkrete Geonorge-symbolsiden viste ikke selv et særskilt lisensfelt. NLOD-merkingen i dataportalen er relevant, men er ikke her bekreftet som eksplisitt filspesifikk lisens for hvert SVG-derivat. Før produktdistribusjon: dokumenter forbindelsen mellom valgt fil og vilkår, alternativt bruk Vegvesenets direkte EPS-pakke med avklart lisens. Dette er en kvalifiseringsoppgave, ingen allerede innhentet tillatelse.

**A:** Bevar standardens røde ring, hvite flate, sorte tall og proporsjoner også i nattmodus. Bruk separate etiketter for aktuell/kommende verdi og tekstlig alternativ. Ingen vilkårlig tallutskifting i en sirkel. Registrer original-URL, hentet dato, hash, skiltkode, lisens og eventuell rent teknisk konvertering i et senere assetmanifest. NLOD innebærer ingen kvalitetsgaranti [15].

## Begrensninger og integrasjon

**U:** Ingen hentet kilde dokumenterer full, operativ dekning av midlertidige eller variable grenser i Tromsø. En statisk registrert verdi eller registrert skiltplate er ikke dokumentasjon på aktiv visning i et variabelt skilt. Manglende data skal ikke fylles med antatt generell 50/80. Ukjent/konfliktfylt regulering må gi utilgjengelighet. Skiltplatekatalog og strekningsfartsgrense er forskjellige dataformål [4][14].

**A:** Vis registrert vegfartsgrense; ikke beregn bussens totale tillatte hastighet uten kvalifisert kjøretøy-/regelgrunnlag. Ingen busspesifikk regelmotor er undersøkt eller inkludert. Lokal matching mot avgrenset offentlig snapshot kan holde råposisjoner i RAM og unngå ekstern GPS-spørring per måling. Geometri, alternative lenker og datadekning trengs internt selv om kart er utenfor omfanget. Arkitekturgjenbruk, kildeutfall, snapshotgrenser og grensesnitt for senere fartsvisning er beskrevet i [interfaces.md](../../interfaces.md).

## Konklusjonens grenser og ny kontroll

Ingen ytelses-, nøyaktighets- eller dekningsprosent er målt. Uavhengig publiseringsbekreftelse, rute-/vegkobling, kildealderspolicy og symbolvilkår står åpne. Undersøkelsen stoppet ved avgrenset dekning av planleggingsspørsmålene; målrettet oppfølging brukes for disse hullene, ikke generell bred research.

API-/katalog- og symboltilgjengelighet må kontrolleres på nytt før kvalifisering/implementering, senest ved neste planrunde. Publiseringsdatoene på de fleste kildene er ukjente; tilgangsdato kan ikke erstatte dem i en beregnet friskhetsgaranti. Se [maskinell friskhetskontroll](checks/staleness.json): filen beregner bare neste kontroll for to daterte tilgjengelighetsobservasjoner, 2026-11-27. Kildenes ukjente publiseringsdatoer er utelatt fra beregningen og forblir et gap. Observasjonsvindu for API-kompatibilitet er høyst én måned, med tidligere ny kontroll ved kildeendringer. Ingen må påstå at selve vegreguleringen er fersk fordi API-et svarte.

## Kilder

Alle åpnet/hentet 2026-10-27. «Ukjent» gjelder publiseringsdato, ikke lesedato. Middels tillit betyr aktuell primærkilde uten uavhengig bekreftelse. Lokale utdrag er reproduksjonsbelegg.

| Ref | Støtter | Utgiver / kilde | Publisert | Tillit |
|---|---|---|---|---|
| [1] | Datasett og NLOD | [Statens vegvesen: NVDB](https://dataut.vegvesen.no/dataset/nasjonal-vegdatabank) | Ukjent | Middels |
| [2] | Segmenter og avgrensing | [Statens vegvesen: Vegnett V4](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Vegnett/) | Ukjent | Middels |
| [3] | Punktoppslag | [Statens vegvesen: Posisjon V4](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Posisjon/) | Ukjent | Middels |
| [4] | Type 105, egenskaper og stedfesting | [Statens vegvesen: Datakatalog 105](https://nvdbapiles.atlas.vegvesen.no/datakatalog/api/v1/vegobjekttyper/105), imports/catalog-105.json | Ukjent | Middels |
| [5] | Retningsbegreper | [Statens vegvesen: Retning](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/introduksjon/retning-pa-vegsystemreferanse/) | Ukjent | Middels |
| [6] | Versjoner og historikk | [Statens vegvesen: Vegobjekter V4](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Vegobjekter/) | Ukjent | Middels |
| [7] | Endringsstrøm | [Statens vegvesen: Endringer V4](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Endringer/) | Ukjent | Middels |
| [8] | Beta-ruting | [Statens vegvesen: Rute V4](https://nvdb-docs.atlas.vegvesen.no/nvdbapil/v4/Rute/) | Ukjent | Middels |
| [9] | Tre Tromsø-observasjoner | [Statens vegvesen: avgrenset GET](https://nvdbapiles.atlas.vegvesen.no/vegobjekter/api/v4/vegobjekter/105?kommune=5501&antall=3&inkluder=egenskaper,metadata,lokasjon,vegsegmenter), imports/tromso-sample.json | Observert 2026-10-27 | Middels |
| [10] | EPS og farger | [Statens vegvesen: skiltfiler](https://www.vegvesen.no/fag/veg-og-gate/trafikkskilt-og-vegoppmerking/filer-og-fargekoder-for-trafikkskilt/) | Ukjent | Middels |
| [11] | Offisiell symbolpakke/eier | [Geonorge/Kartverket: Trafikkskilt](https://register.geonorge.no/symbol/symbolpackages/details/1e2f592a-1d69-45a3-9ce1-e55a64fe1dc3) | Ukjent | Middels |
| [12] | 40-vektor og originalfil | [Geonorge: 362_40](https://register.geonorge.no/symbol/files/details/d47f210d-7ce9-4742-9527-3f5695b057ff), [SVG](https://register.geonorge.no/symbol/files/trafikkskilt/362_40.svg) | Ukjent | Middels |
| [13] | 50-vektoroppføring | [Geonorge: 362_50](https://register.geonorge.no/symbol/files/details/755738d1-e38e-4a6c-acda-bf1802b52952) | Ukjent | Middels |
| [14] | Trafikkskilt-datasett/lisens | [Statens vegvesen: Trafikkskilt](https://dataut.vegvesen.no/dataset/trafikkskilt) | Ukjent | Middels |
| [15] | Viderebruksvilkår | [data.norge.no: NLOD-oppsummering](https://data.norge.no/nlod/no) | Oppdatert 2023-03-07 | Middels |
