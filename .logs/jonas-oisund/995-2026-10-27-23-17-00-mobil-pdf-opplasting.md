# Mobil PDF-opplasting

## 2026-10-27 kl. 23:17 — Jonas Øisund

### Oppgave
Feilsøk og rett umiddelbar feil ved opplasting av tre vanlige skiftkort fra mobil, slik at assistenten kan tolke dem og vise en ryddig oversikt. Brukeren presiserte at originalene skal bevares, aldri publiseres og at personopplysningene skal holdes strengt private. Mobilen er Pixel med Android; opplastingen feilet straks etter filvalg.

### Plan
- Les prosjektregler, sesjonslogg og BMAD-byggflyt; undersøk filene og hele importkjeden isolert.
- Gjenskap filvelgerens retur og tilgangskontroll med syntetiske nettlesertester; rett transporten og feilklassifiseringen.
- Test originalene midlertidig uten lagring, bruk syntetiske varige regresjoner, gjennomfør uavhengig kodegjennomgang og klargjør ferdig bygg.
- Følg [implementasjonsspesifikasjonen](../../_bmad-output/implementation-artifacts/spec-mobile-pdf-upload.md) og [testevidensen](../../docs/evidence/mobile-pdf-upload.md).

### Resultat
- Alle tre private originaler ble tolket av eksisterende parser, isolert arbeidsprosess, typet HTTP-resultat og nettleservalidering. Ingen parserendring var nødvendig.
- Gjenskapte kappløpet der filvelgeren leverer valget mens appen fortsatt kontrollerer innlogging etter retur. Opplasting ble avvist før PDF-en ble sendt, men meldingen hevdet tolkningsfeil. Testen feilet før rettingen og bestod etterpå. Eksakt feil på brukerens fysiske enhet er ennå ikke fanget direkte.
- Rettet avgrenset og avbrytbar venting på tilgang til samme økt, begge rekkefølger for filvalg/synlighet, lesing til minne før sending og bevaring av filvalget under lesing. Feilmeldinger skiller filtilgang, tilgangskontroll, transport, tolking og ugyldige svar. Utlogging, kontoendring, utløp og avbrudd hindrer fortsatt opplasting.
- 119 eksisterende backendtester bestod. 31 nettlesertester bestod samlet; deretter bestod tre fokuserte tester av ugyldig JSON, nettverksfeil og timeout under svarlesing etter siste reviewretting. TypeScript/Vite- og Docker-bygg bestod. Isolert gatewaykontroll av 120 nektvarianter, gyldig videresending og utilgjengelig tilgangsgate bestod.
- Tre midlertidige nettlesertester med originalene bestod: eksakte sendte byte, gjennomgang, eksplisitt overføring til ulagret utkast og ingen lagringskall. Lokale testdobler for innlogging/transport brukte den reelle isolerte HTTP-tolkingens svar. Ingen operativ konto eller database ble brukt.
- Originalene ble hashkontrollert og er byte-for-byte uendret. Vedlegg er utelukket fra Git og bygg; midlertidige uttrekk, rendring, JSON-svar, kontrollmanifest og private nettlesertestfiler/resultater er slettet. Varig testfixture er utelukkende syntetisk. Ingen personopplysninger fra filene er tatt inn i kode, evidens eller denne loggen.
- Uavhengig kodegjennomgang fant seks konkrete punkter; alle ble rettet, ingen utsatt. Full detaljer finnes i spesifikasjonens triage. Tidlig iOS-hypotese ble korrigert etter brukerens Android-opplysning og er ikke oppgitt som diagnose.
- Lokalt gateway-image er ferdig: `ibe160-tablet-gateway:pdf-upload-20261027`; ignorert override i `.private-runtime/mobile-pdf-upload.yaml`. Bare frontend/gateway trenger utskifting. Automatisk godkjenningskontroll avviste deploy fordi oppdatering av den kjørende delte tjenesten kan gi avbrudd og ikke ble vurdert uttrykkelig autorisert. Brukeren er spurt om konkret godkjenning. Ingen deploy ble utført; kjørende image er fortsatt `ibe160-tablet-gateway:main-2dd1b11`.
- Produktendringene er ukommittert. Bare denne loggen og issues.md committes lokalt. Ingen push.

### Åpne punkter
- Avvent uttrykkelig godkjenning for å aktivere det ferdige gateway-bygget på app.bussassistent.com; gjennomfør deretter ny opplastingstest på brukerens Pixel. Appen er ikke oppdatert, og fysisk bestått test er ikke påstått.
