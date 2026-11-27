# Bussassistent V2 for feltprøving i Tromsø

## Status 22. november 2026

Integrasjonsgrenen bygger på lokal main `df3fc94`, V2 `b8b907f` og nettlesergrenen gjennom `0eed724`, som inneholder rettingen `b97f634`. Passordfunksjonene og oppfølgingen ligger allerede i V2 gjennom `755b6f9` og `86a56eb`. Publisert main var `26394835f27006d528a378a484485496d610f6e8` ved siste fjernkontroll. Produksjonskontroll bekreftet `7921eb54e4816aaab9368c3efd851bcf692f3823`, frisk API og database, aktiv tunnel og avvisning uten tilgang. En fersk backup på den releasen bestod isolert restore med like tabellfingeravtrykk.

## Daterte avganger

| Linje | Vanlig hverdag | Før 09:00 30.11 | Fredag 04.12 | Lørdag 05.12 | Søndag 06.12 | Trasévarianter i perioden |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 20 | 136 | 32 | 143 | 109 | 64 | 9 |
| 21 | 19 | 3 | 19 | 0 | 0 | 2 |
| 22 | 20 | 7 | 20 | 0 | 0 | 3 |
| X23 | 14 | 8 | 14 | 0 | 0 | 2 |
| 24 | 139 | 36 | 145 | 80 | 64 | 8 |
| 26 | 103 | 25 | 109 | 81 | 63 | 8 |
| 26B | 15 | 0 | 15 | 18 | 0 | 1 |
| X27 | 8 | 4 | 8 | 0 | 0 | 3 |
| 28 | 125 | 33 | 131 | 110 | 65 | 13 |
| X29 | 8 | 4 | 8 | 0 | 0 | 3 |
| 30 | 31 | 8 | 31 | 0 | 0 | 4 |
| X31 | 5 | 4 | 5 | 0 | 0 | 1 |
| X32 | 9 | 4 | 9 | 0 | 0 | 3 |
| 33 | 91 | 22 | 94 | 57 | 38 | 7 |
| 34 | 91 | 24 | 91 | 53 | 37 | 5 |
| X35 | 9 | 5 | 9 | 0 | 0 | 3 |
| X36 | 16 | 6 | 16 | 0 | 0 | 4 |
| 40 | 91 | 19 | 96 | 75 | 61 | 8 |
| 42 | 153 | 36 | 159 | 108 | 74 | 10 |
| X43 | 15 | 8 | 15 | 0 | 0 | 4 |
| X44 | 8 | 5 | 8 | 0 | 0 | 4 |

Svippers tabellindeks viste alle 21 linjene med perioder som dekker feltprøven. Den lenkede linje 26-PDF-en har eldre gyldighet på minst én deltabell. Bruk daterte Entur-avganger og sammenlign med Svippers reiseplanlegger for den tildelte turen. Tabellen over er fra NeTEx-uttrekket for 30. november til og med 10. desember 2026. Alle 231 linje/dato-par og alle 11 150 turer samsvarte med GTFS-eksporten på tur-ID, trasévariant, stopp-ID i rekkefølge og hvert publiserte klokkeslett. NeTEx-generasjon `1795302164876896`, SHA-256 `5a39d9fae827d7494f50e19a8f5450e5643eee977a23e9344e8f8bd82a311a8e`. GTFS-generasjon `1795302186255815`, SHA-256 `6f0014b1be19b3986ea18642c5833ec19882d2b2a89b3c48478e121eaa82135e`. [Enturs nedlastinger](https://developer.entur.org/stops-and-timetable-data/) · [Svippers rutetabeller](https://svipper.no/meny/reise/rutetabeller-og-kart/rutetabeller-buss/) · [Svippers tabell for 26B](https://svipper.no/regtopp/api/route/download/pdf/26B_181126.pdf)

Kontrollerte eksempler 30. november omfatter linje 26 fra Pyramiden 05:10 med 36 stoppforekomster og linje 26 fra Pyramiden 23:33 med gjentatt plattform og siste stopp 00:20 neste kalenderdag. Andre prøver omfatter 26B fra Torgsenteret 09:54, X44 fra Smørblomstvegen 06:30 og ringrute 33 fra UNN 05:15. Kildene beskriver planlagt drift. Sjekk tildelt vakt og eventuelle aktuelle trafikkmeldinger før avgang.

## Funksjon og prøveoppskrift

1. Åpne **Finn avgang i Tromsø** i det private arbeidsrommet. Velg driftsdato, linje og **Hent avganger**. Begynn med datoen og linjen i tildelt vakt, også for en uventet morgenavgang.
2. Velg avgang etter klokkeslett, startsted og destinasjonsvisning. Sammenlign første stopp, ett stopp underveis og siste stopp med vakten. Ved to avganger samme klokkeslett, kontroller startsted og retning. Ved tur etter midnatt i samme driftsdøgn, se etter **+1 døgn**.
3. For et manuelt holdepunkt, åpne en lagret passasjertur i utkastet. Velg avgang og stoppstrekning, lagre rutereferansen og bekreft arbeidsdagen. Åpne den valgte aktiviteten og velg faktisk stoppforekomst.
4. Åpne **Vegområde og GPS-fart** for en instruktørtur med eller uten avgang. Start fartsmåling, velg eventuelt et vegområde og start vegmatching. Begge funksjonene kan bruke samme GPS-vakt. Ved avvist eller tapt tilgang opphører målingen. Etter at forbindelsen er oppe og tilgangen er bekreftet, start funksjonen på nytt.
5. Ved brudd kan en allerede åpnet offentlig stoppliste leses i samme fane. Nytt oppslag og lagring krever forbindelse og gyldig økt. Oppdater eller kontroller tilgangen ved retur. Omlasting uten nett krever at forbindelsen kommer tilbake før et nytt oppslag.

Enturs arkiv med nåværende og framtidige stopp inneholder alle 457 plattformene. Det ga entydig datert plattformversjon for 411 148 av 418 428 planlagte stoppforekomster. Ved sju plattformer mangler også gyldighet for det versjonerte stoppestedet. Følg disse manuelt og velg forekomsten på nytt ved GPS-gjenopptak. Plattformene ligger ved Tromsø Prostneset (to), Hamna skole nord, Hamna skole øst, Sandvik kryss og Tromsø lufthavn (to). Plattformversjon velges på faktisk ankomst- og avgangstid, inkludert passering av midnatt. Entur NSR-generasjon `1795345333303902`, SHA-256 `44ad13ccead173a9a6f0ce444ab855025308c016df3860ac5e3a31dd1cdb7066`. [Enturs framtidsarkiv](https://developer.entur.no/open-data/stops) · [Nordisk NeTEx-profil om gyldighet](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728563782)

Automatisk avviksvurdering gjenkjenner bekreftet linje og planlagt tidsvindu når Enturs SIRI-SX for TRO har publisert relevante opplysninger. Et avvik med ufullstendig linje-, retnings- eller stoppomfang kan kreve manuell gjennomgang.

De elleve daterte NVDB-uttakene for 30. november–10. desember ga samme graf med 18 615 rettede geometrier, inkludert begge armer ved R4 og bekreftet envegsretning mot Flyplassvegen. Den isolerte databasen har 33 pakker. Pakkene overlapper og rommer 6 556 rettede segmenter for Kvaløya, 14 387 for Tromsøya og 13 335 for fastlandet per dato. Flere grener, uavklart retning, kilder uten oppdatert bekreftelse og variable grenser kan gi **Ukjent**. Tettbygd standard på 50 km/t brukes der en etterprøvbar kontroll har avklart skilting og vedtak for strekningen. GPS-målinger og matching behandles på enheten. [NVDB vegnett](https://nvdb.atlas.vegvesen.no/docs/produkter/nvdbapil/v4/Vegnett/) · [Vegtrafikkloven § 6](https://lovdata.no/dokument/NL/lov/1965-06-18-4)

Vegvesenets åpne SituationSimple svarte fra Ubuntu 22. november med fire saker og ni underposter. Uttrekket viste vegarbeid og regulering på Fv. 862 ved Langnestunnelen, Breiviktunnelen og Tromsøbrua. Meldt regulering uten entydig grense, strekning, retning eller gyldighet gir **Ukjent** på potensielt berørte segmenter. Forvarselet holdes tilbake gjennom slike segmenter. [Vegvesenets WFS-dokumentasjon](https://dataut.vegvesen.no/dataset/trafikkmeldinger/resource/4b31e6c6-fd62-45be-a847-185659bece87)

I den isolerte prøven 22. november ga dagens NVDB- og WFS-data 459, 1 199 og 1 084 segmenter med registrert fartsgrense i de tre overlappende pakkene. Simulert kjøring langs faktisk veggeometri ga henholdsvis 60, 30 og 30 km/t på Kvaløya, Tromsøya og fastlandet. Det virkelige uttaket for 30. november viste den registrerte 50-platen ved R4 omtrent 25–26 m inn på Flyplassvegen. Appen mangler bekreftet overgang på grafnoden der, og forvarsler ved R4 holdes tilbake. [R4-skilt og grensegrunnlag](evidence/v2-road-source-20261120.md#r4-sign-and-lane-cross-check)

## Oppdatering og tilbakeføring

Etter installasjon av kandidatens kode henter serveroperatøren rutetabeller og plattformer med `sudo -n /usr/local/sbin/bussassistentctl import-routes YYYY-MM-DD YYYY-MM-DD`. Oppslaget tar inntil 14 sammenhengende driftsdatoer og inkluderer begge ender. For feltperioden brukes `2026-11-30 2026-12-10`. Kontroller resultatet mot siste Svipper-data før feltstart og oppdater ved kildeendring. Oppslag viser kildealder etter 24 timer. Importen skriver én transaksjon og sparer NSR-versjonen som brukes av frosne valg. En ufullstendig import bevarer aktiv katalog.

I et miljø med tilgang til NVDB bygger `python -m app.road_area_evidence --date YYYY-MM-DD --output nvdb.zip` et datert uttak. Kjør `python -m app.road_area_catalogue nvdb.zip` for å kontrollere det. Pakk `nvdb.zip` og eventuelt `review.json` i roten av `road-bundle.zip`. På Ubuntu importerer `sudo -n /usr/local/sbin/bussassistentctl import-road-area < road-bundle.zip` alle tre områdene atomisk. Hent et uttak for hver aktuell Oslo-dato. Et forhåndsinnhentet, datert uttak uten gjennomgåtte grenser kan brukes til vegmatching med ukjent fart på datoen det gjelder. For tallfestede grenser krever appen et uttak som er høyst sju døgn gammelt.

For strekninger der skilting og midlertidige forhold er avklart, støtter importen `--review kontrollerte-grenser.json`. Oppgi arkivets SHA-256 som `source_sha256`, `effective_date`, UTC-tidsstemplene `checked_at` og `valid_until` og et `limits`-objekt med rettet segment-ID som nøkkel. Hver verdi har `kmh`, `basis` (`registered`, `urban-default`, `sign` eller `temporary`) og `evidence` som identifiserer den daterte dokumentasjonen for hele segmentet. Forvarsler krever dessuten `transitions` med avreisende segment-ID, etterfølgende segment-ID og dokumentasjon for at skiftet gjelder i den felles noden. Gyldigheten kan vare inntil 24 timer og stopper ved midnatt i Oslo. Behold grensen ukjent hvis dokumentasjonen dekker bare en del av segmentet eller et variabelt skilt mangler aktuell status. Appen kontrollerer om den aktive områdepakken er erstattet hvert 30. sekund.

Ved `temporary` legger operatøren til `restriction` med den eksakte retningsbestemte `segment`-ID-en og `starts_at` og `ends_at` i UTC. Eventuelle `record_revisions` binder beslutningen til innholdshashen for hver fartsreguleringspost som den samme dokumentasjonen avklarer. Etter utrulling starter `sudo -n /usr/local/sbin/bussassistentctl enable-road-situations` første oppdatering og en oppdatering hver tredje minutt, gjennom en separat kortvarig prosess. `road-situation-status` viser tidspunkt, kildealder og postenes revisjoner. Appen bruker nyeste validerte uttak og kan beholde tidligere rapporterte hendelser innenfor den oppgitte perioden hvis oppdateringen feiler. WFS-oppslaget kan stedfeste meldinger som har publisert geometri. Registreringer uten geometri kan mangle i det avgrensede utsnittet.

Start `sudo -n /usr/local/sbin/bussassistentctl enable-road-area` for oppdatering av dagens NVDB-pakke og et nytt uttak kl. 00:20 Oslo-tid. En planlagt oppdatering bevarer et eksisterende uttak fra samme dag. En tvungen `refresh-road-area` kan gi et nytt kildegrunnlag som krever ny kontroll av manuelt godkjente grenser. Registrert grense kan vises i en entydig, sammenhengende del av samme veg med lik registrert grense. Det krever dagens NVDB-grunnlag og en fersk SituationSimple-observasjon. Kryss, avgreininger, variable skilt og ukjent skiltplassering kan fortsatt gi **Ukjent**. Et automatisk godkjent veginteriør gir grunnlag for aktuell grense. Et 300 m-varsel krever en separat, dokumentert overgang.

Start `sudo -n /usr/local/sbin/bussassistentctl enable-public-notices` for Entur SIRI-SX. Hver innhenting bruker en avgrenset, kortvarig prosess uten tilgang til privat nett eller private filer. API-et validerer offentlige svar før det lagrer kildestatus og versjoner. En delvis innhenting bevarer forrige komplette kildegrunnlag mens nye, ubekreftede opplysninger kan kreve manuell vurdering.

### Ressursgrenser før feltbruk

- DATEX tillater 2 048 punkter per melding og 16 384 per uttak. Ett vegoppslag får inntil én million enheter for kandidat- og punktarbeid. Det arkiverte WFS-uttaket for feltgrunnlaget hadde ni poster og 276 punkter, med høyst 82 punkter i én post. Uavklart veggrunnlag holder tilbake fartsgrense og forvarsel. Egen GPS-fart bruker fortsatt sin egen måling.
- NVDB-opprydding ved API-oppstart og hver time fjerner utløpte Oslo-datoer og beholder de to nyeste versjonene per område for dagens og kommende datoer. Den daglige oppdateringen av rutetabellen har sin egen driftsflyt.
- Ruteimport bruker en egen prosess med tak på én CPU, 640 MiB minne uten ekstra swap og 176 MiB midlertidig lagring. Grensen gir plass til rute- og plattformarkivene, en midlertidig kopi og arbeidet med de 21 linjene. Hvert stoppested har egne grenser på 4 MiB XML og 50 000 elementer. Største stoppested i feltarkivet var under 57 kB. Et GML-felt utenfor stoppestedene var ca. 1,47 MB og får plass under den separate grensen på 2 MiB. Installer den oppdaterte Ubuntu-hjelperen og Compose-fila sammen med det nye API-bildet.
- Ubuntu-gatewayen krever en gyldig Access-påstand og en entydig klientadresse for nye innlogginger og gjenoppretting. Bekreft at den loopback-bundne inngangen bare betjenes av den konfigurerte tunnelen, og at Cloudflare sender `CF-Connecting-IP` uten en Worker eller en transform som fjerner eller erstatter adressen. Kilder som deler IPv4-adresse eller IPv6 /64 deler kildegrense. Rull ut gateway, Access-verifikator og API sammen. [Cloudflares klientadressehode](https://developers.cloudflare.com/fundamentals/reference/http-headers/#cf-connecting-ip)
- SIRI-budsjettet er 8 000 identiteter, 16 000 revisjoner og 64 MiB JSON i PostgreSQL. Det arkiverte feltuttaket hadde én side på 12 870 byte XML. Budsjettet gir rom for flere dager med ordinære endringer ved uttak av denne størrelsen. Når ny innhenting overskrider budsjettet, vises ufullstendig kildekontroll med sist gyldige grunnlag og uløste konflikter.
- En konto kan ha 256 aktive utkast. Inntaket av nye lagringsforsøk teller også utløpsstyrte slettingskvitteringer mot grensen på 512. Samlet innholdsbudsjett er 64 MiB. Det gir rom for ordinær sjudagersbruk og for eksisterende paginering over 201 utkast. Kvitteringsoppslag og retry med kjent operasjons-ID er fortsatt tilgjengelige. API-et legger til to eierindekser via migrasjon 025 og 026 ved oppstart.

Den installerte versjonen `d415383` bruker migrasjon 015–024 fra V2. Kandidaten legger til 025 og 026. Standard `rollback` krever identiske migreringsfiler. I PostgreSQL-prøven startet `d415383` igjen på førdumpen med skjema 024. Utkastet lagret før oppgraderingen kunne åpnes. Utkastet lagret på skjema 026 var borte fra førdumpen og kunne gjenåpnes med kandidaten fra en separat dump av den oppgraderte databasen. Ta en fersk, verifisert backup før bytte. Hold tilgangen stengt ved feil og avstem skriving etter backupen før produksjonsrestore. [Tilbakeføringsprøve 025–026](evidence/v2-rollback-025-026-20261127.md)

På fysisk Lenovo gjenstår innlogging via beskyttet HTTPS utenfor hjemmenettet, faktisk posisjonstillatelse i Chrome og Brave, reell stillestående og bevegelig fart, skjermlås og retur, samt sammenligning med tildelt tur og aktuelle skilt. Pixel-prøve er separat. Bruk appen mens bussen står stille eller la en passasjer registrere observasjoner.
