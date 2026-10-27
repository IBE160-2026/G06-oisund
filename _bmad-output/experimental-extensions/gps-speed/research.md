# Avgrenset undersøkelse — rapportert egen fart

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Undersøkt 2026-10-27. Kun offisielle dokumentasjonssider; ingen faktisk GPS, brukerspor eller produkttest. Normtekst beskriver API-kontrakten, ikke oppførselen på det konkrete Lenovo-nettbrettet.

## Dokumenterte egenskaper

| Belegg | Egenskap |
|---|---|
| [W3C Geolocation §§6.6, 8.2, 9.4](https://www.w3.org/TR/geolocation/) | speed er ikke-negativ horisontal fart i m/s, eller null når utilgjengelig. timestamp angir posisjonens måletid. |
| [W3C §§6.5–7.3](https://www.w3.org/TR/geolocation/) | Watch har ingen fast rapporteringsfrekvens; implementasjonen kan begrense oppdateringer. Oppdateringer knyttes til synlige, fullt aktive dokumenter. maximumAge gjelder cache; timeout er ingen ferskhetsgaranti. enableHighAccuracy er et hint og kan koste tid/strøm. |
| [W3C §§6.6, 9](https://www.w3.org/TR/geolocation/) | accuracy beskriver koordinatnøyaktighet i meter ved 95 % konfidens. Grensesnittet har ikke speedAccuracy. API-et garanterer ingen bestemt sensor-/GPS-algoritme. Nettleser- og OS-tillatelse kan være forskjellige. |
| [Mozilla MDN: speed](https://developer.mozilla.org/en-US/docs/Web/API/GeolocationCoordinates/speed) | Dokumenterer m/s, null ved manglende måling, sikker kontekst og bred API-støtte. Støtte betyr ikke at speed er tilgjengelig på hvert apparat. |
| [Chrome DevTools Sensors](https://developer.chrome.com/docs/devtools/sensors) | Dokumenterer posisjonsoverstyring og «Location unavailable». Dette er nyttig for visningsfeil, men dokumenterer ikke fysisk fartskvalitet. |

## Vurdering og anbefaling — egne slutninger

**GPS-D1:** Velg rapportert speed som eneste fartskilde i første eksperiment. Konverteringen til km/t er eksakt faktor 3,6. Produktnavnet «GPS» er en forståelig kortform; hjelpeteksten sier at farten er beregnet fra nettbrettets posisjonstjeneste og kan være utilgjengelig/usikker. Ingen påstand om satellittlås, Doppler-måling eller sertifisert speedometer.

**GPS-D2:** Utsett reserve `avstand / Δt`. Støy i to fikser forsterkes når Δt er kort. Et syntetisk eksempel: 10 m tilsynelatende flytting på 1 s gir 36 km/t selv ved stillstand. Et langt vindu demper noen feil, men blander akselerasjon, bremsing og kø og tilfører forsinkelse. Samvarierende feil og svinger gjør en enkel accuracy-avgrensning utilstrekkelig. Vi bruker bare posisjonsdifferanser til konservativ kontroll av grove hopp, aldri som erstatningsfart. Et senere reserveforsøk må ha egen feilmodell, tidsvindu, stillstands-/køtest og uavhengig sannhetsgrunnlag. Ved varig null på Lenovo er utfallet «ikke støttet», ikke automatisk reserve.

**GPS-D3:** Start uten ekstra gjennomsnitt, medianfilter, EMA eller deadband. Innbyggede filtre er ukjente. Applikasjonen skal ikke holde høy fart gjennom nedbremsing for å gjøre tallene roligere. Oppstart/rekvalifisering med to fikser har en eksplisitt kostnad; se målekontrakten. En senere utjevning må måle både flimmerreduksjon og ekstra tidsforsinkelse i begge retninger.

**GPS-D4:** Vis heltall fra nærmeste km/t, men bevar eksakt rapportert 0 og vis «<1» ved positiv fart som ellers ville rundet til 0. Dette unngår at køfart blir falsk stillstand. Ingen stillstandsdeteksjon fra null, manglende heading, små posisjonsendringer eller utløpt verdi.

## Det kildene ikke avgjør

Faktisk speed-dekning, feil ved stillstand, oppstartstid, intern filtrering, batteribelastning og Brave/Chrome-forskjeller på Lenovo er ukjent. Koordinatnøyaktighet er ikke fartens feilmargin. Sammenhengende målinger kan dele samme feil. Enhetsprofilen, akseptkriteriene og de syntetiske scenariene i [verifikasjon](specs/spec-gps-speed/verification.md) er uprøvde forslag, ikke forskningsresultater. Senere dokumentasjon skal skille API-egenskaper, syntetisk programlogikk og fysisk måleegnethet.
