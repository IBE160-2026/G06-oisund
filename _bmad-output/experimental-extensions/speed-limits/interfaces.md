# Foreslåtte grensesnitt og gjenbruk

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Konsept v0, ikke implementert API eller avtale som endrer andre utvidelser. Gjenbruk React/TypeScript → FastAPI → PostgreSQL i V1-arkitekturen. Et lite frontend-evalueringsmodul og en avgrenset backend-adapter for offentlige vegdata er foreslåtte tillegg. Ingen ny tjeneste eller databaseendring er besluttet.

| Grense | Nødvendig informasjon og ansvar |
|---|---|
| Rutenett → fartsgrense | Kontraktsversjon; bekreftet datert avgang, valgt forekomstområde, kilde-/mappingsnapshot og revisjon. Nytt nødvendig tillegg: kvalifisert rettet trasé med ordnede lenkeforekomster, geometri, NVDB-kobling, gyldighet og tvetydige forgreninger. Manglende geometri er eksplisitt. |
| Posisjon → lokal matcher | Måletid, mottakstid/monoton alder, lat/lon, accuracy, nullable bearing og speed, watch-generation og enabled/paused/interrupted. Råfikser beholdes bare i avgrenset RAM-vindu. Del én autorisert posisjonskilde; ingen ekstra skjult GPS-watch. |
| Vegsnapshot → lokal matcher | CRS, topologi, rettede overganger, lenke-ID og intervall, lengdegrunnlag, kjørefelt/medium der kvalifisert, dekningsgrense; NVDB-objekt-ID/versjon, verdi og stedfesting, virkningsdato, sist endret, hentet/kontrollert tidspunkt, katalogversjon og hash. Ukjent metadata er ukjent. |
| Matcher → grenseevaluering | Unik rettet lenkeforekomst og posisjon med usikkerhetsintervall; måletid; kandidatalternativer/avvisningsårsak; faktisk veg og forventet videre veg med separat tillit; kontrakt-/snapshot-/øktgenerasjon. Et holdeplassestimat kan ikke fylle disse feltene. |
| Evaluering → visning | current: verdi eller null + status/årsak; upcoming: verdi/endrings-ID/avstand eller null + årsak; kilde-/målealder, passerings-ID og usikkerhet. Ingen visningsfallback til gammel current når null mottas. |
| Livssyklus | Pause/Off, skjult side, tilgangstap, byttet aktivitet/trasérevisjon, avslutning og utløp invaliderer evaluering og sene callbacks. Gjenopptakelse følger den eksplisitte posisjonsflyten. Ingen oppdatering av manuelle aktivitetsvalg, utfall eller arbeidsdag fra målinger. |

Komplett rutenettplan P1 har holdeplassorden og valgfri geometri. Posisjonsplanen har NSR-koordinater og rådgivende stoppestedsestimat. Ingen av dem leverer dette nye vegtilknytningsgrensesnittet som en etablert egenskap. Krav om rettet trasé/NVDB-kobling registreres her som tillegg som senere må samordnes, uten å endre referanseplanene.

Forbered offentlig vegsnapshot etter eksplisitt valgt pilotkorridor, med fast areal-, objekt- og bytegrense, pagineringstak og begrenset overlapp ved kantene. Korridoren må inneholde relevante alternative veger og minst 300 m støttet fremoversikt; manglende kantdata stopper forvarsel. Ikke kall eksternt posisjonsendepunkt per GPS-fix. Backend mottar offentlige korridor-/snapshotreferanser, ikke privat arbeidsdag, full skiftplan eller faktisk kjørespor. Lokal matching kan dermed kjøres uten å sende råposisjoner til NVDB.

Mellomlagre offentlig referansedata separat fra private økter. Atomisk validering av sammenhengende snapshot, hash og katalog-/nettversjon hindrer delvis blanding av gamle/nye lenker. Endringer krever revalidering av koblinger og passeringsidentitet. Frys aktiv evalueringsbinding; kjente ugyldigheter stopper visning straks, og en ny versjon krever ny kvalifisering. Ingen kontinuerlig sømløs oppdatering er lovet.

Foreslå sjekk ved pilotforberedelse og før bruk, med begrenset retry/backoff ved feil. Sist vellykket kontroll er forskjellig fra kildeoppdatering og virkningsdato. En senere pilot må velge og begrunne maksimal kildealder; ingen NVDB-friskhetsgaranti er dokumentert her. Ved overskredet/ukjent kvalifisert kildealder, konflikt, hull eller kildeutfall uten brukbart snapshot: skjul verdiene og vis årsaken. Et fortsatt gyldig, kvalifisert snapshot kan brukes innenfor sin eksplisitte aldersgrense ved kort kildeutfall; dette etablerer ingen offline-garanti for V1 eller privat tilgang.

Senere oppfølging reserverer optional qualifiedSpeed {valueMps, acquiredAt, quality, origin} og previewPolicy {mode=fixed-distance, distanceM=300, version}. Senere mode=time-based kan konsumere kvalifisert fart uten å endre current/upcoming-semantikken. Ingen tidshorisont, fartfilter, fartsmåler, lyd eller overtredelsesalarm detaljplanlegges nå.

Personvernforslag: kort RAM-vindu med tids-/antallstak, bare seneste match og liten dedupliseringstilstand; rydd ved stopp/tilgangstap/øktbytte. Ingen kjørehistorikk, råfikser i logger/telemetri, private posisjonskøer eller nye persistente GPS-tabeller. Feilsøk senere med syntetiske spor og aggregerte årsakskoder uten sporbare posisjoner.

## Presisering fra spesifikasjonen 2026-10-27

Dette er et adoptert konseptuelt grensesnitt for [gjeldende spesifikasjon](specs/spec-speed-limits/SPEC.md). Ingen endring i andre utvidelsers kontrakter er implisitt godkjent. Der visningsatferd trenger presisering, gjelder behavior.md og verification.md i spesifikasjonspakken.

Matcherens utdata skal skille **currentRoadQualified**, **forwardPathQualified** og **passageQualified**, med separate årsaker. Legg til langsveg-posisjons-/avstandsintervall som inkluderer kvalifisert måle- og geometrifeil, ikke bare et accuracy-tall. Fremoverkjeden identifiserer hver innkjøring, rundkjøringsbue, utkjøring og alternativ arm frem til grensen. En kvalifisert aktuell veg trenger ikke en kvalifisert videre avkjøring; current kan dermed være satt mens upcoming er null.

Grenseevaluering returnerer separat status for ukjent aktuell, uavklart videre veg, manglende fremoverdata, ingen kjent endring i komplett 300m-horisont og grensepassering under vurdering. Varselidentitet skiller fysisk endringsforekomst/passering fra snapshotrevisjon; revisjonsbytte invaliderer, men gir ikke automatisk nytt varsel. Numerisk profil-ID/versjon og manifest-ID kreves før evaluering kan erklæres kvalifisert. Foreslått pilotmanifest binder offentlig korridor uten å late som en konkret datert bussavgang er valgt; senere integrasjon med valgt aktivitet trenger fortsatt rutekontrakten ovenfor.

Et kort målevindu og dedupliseringstilstand er øktlokalt. Stillstand kan bevare fersk vegtilknytning, men etablerer ingen ny retning. Ved ukjent kildealder/overskredet profil eller kjent ukvalifisert variabel/midlertidig regulering settes berørt verdi til null. Registrert veggrense, optional qualifiedSpeed og en eventuell fremtidig kjøretøyregelberegning er ulike felt/domener; ingen av de to siste fylles automatisk.

## SL-PLAN-1

[Datakontraktpresisering og numerisk laboratorieprofil](specs/spec-speed-limits/technical-addendum.md) og [storyfordeling](planning/epics.md) konkretiserer dette grensesnittet. Kildebasert pilotmanifest er offentlig planreferanse; det oppretter ikke privat datert rutebinding. Fullt intervall for overordnet/detaljert mapping og feltretning må følge snapshotet. R2/R3 viser hvorfor rutetjenestens korteste kjede må kontrolleres mot feltretning. Katalogens objektretning, basisnettets lenkeretning og vegens metreringsretning er tre forskjellige forhold. Ingen av referanseutvidelsenes kontrakter er endret.


## Korridorer og pakker — SL-D12

Manifestet binder en korridor til ett eller flere kvalifiserte vegdatapakker med packageId/revision/hash og en samlet packageSetId/revision. Kjernen konsumerer den normaliserte kontrakten, ikke pilotnavn eller forhåndskodede lenker. Ny korridor er et data-/kvalifiseringsbytte uten endringer i matching, grenseevaluering eller varsling. Detaljene om kompatibilitet, grensekoblinger, overlapp, konflikt og samlet ressursbudsjett står i [teknisk tillegg](specs/spec-speed-limits/technical-addendum.md). Pakke-ID holdes atskilt fra fysisk endrings-/passeringsidentitet. Rutenettets valgte korridor kan fortsatt ikke overstyre målinger om faktisk veg. Senere bydekning kan bruke flere avgrensede pakker; ingen byutrulling eller ny innsamling bestilles her.
