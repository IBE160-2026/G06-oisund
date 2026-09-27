# UX-valideringsrapport — IBE160

- **DESIGN:** [DESIGN.md](DESIGN.md)
- **EXPERIENCE:** [EXPERIENCE.md](EXPERIENCE.md)
- **Rapporttid:** 2026-09-22T19:06:26Z
- **Status:** Historisk validering med IR-01-tillegg 2026-09-27. Produktbeslutningen er tatt; rendret kontrast, PDF og Lenovo/Brave er ikke verifisert.

## IR-01-tillegg — produkteierbeslutning 2026-09-27

Readinessgjennomgangen påviste at R2 nedenfor feilaktig sa at numeriske krav allerede var lagt til. På valideringstidspunktet fantes bare utvalgte fargeparberegninger i DESIGN, uten en generell terskel for nye tekstpar, nødvendige ikke-tekstlige elementer og fokus. Den eldre R2-statusen er historikk, ikke bevis for utført måling eller et tidligere vedtak.

Produkteier har nå vedtatt prosjektets V1-akseptansekrav i PRD NFR-1, DESIGN og EXPERIENCE: minst **4,5:1** for all informativ tekst, **3:1** for nødvendig ikke-tekstlig informasjon, og synlig fokusmarkering med areal minst tilsvarende en **2 CSS-pikslers** perimeter, **3:1** endring på samme piksler mellom fokusert/ufokusert og **3:1** mot tilstøtende farger der det trengs for å identifisere fokus. Fokus må ikke være helt tildekket. Kravene gjelder dagtema, nattema, begge Auto-utfall og relevante tilstander. Farge alene kan ikke formidle tilstand. Dette er prosjektkrav informert av WCAG 2.2, **ikke** en påstand om samlet WCAG AAA-samsvar.

**Kontroll som gjenstår:** Mål faktisk rendret UI per fargepar/tilstand, inkludert semantiske ikoner og fokus. DESIGNs bare gule soltoken mot hvit bakgrunn er beregnet til **1,59:1**. Den statiske kjøreskissen har også mørk understrek/ytterkant på solfiguren (`#171717` mot hvitt, beregnet **17,93:1**), men selve implementerte silhuetten/kanten i alle tilstander og eventuell korrigering er ikke verifisert. Mål **rendret PDF separat**, hver side og variant, med tekst og nødvendige grafiske tilstander mot faktisk bakgrunn. Registrer rå ratio, testmiljø og bestått/feilet/blokkert/ikke målt. Story 1.1, 1.3, 3.5, 3.14 og 7.4 eier avgrensede kontroller; 8.8 eier senere faktisk lesbarhet på montert Lenovo/Brave. Ingen av disse nye målingene eller E8-portene er bestått gjennom dette dokumenttillegget.

## Samlet vurdering

Dokumentene bevarer den etablerte førerflyten og de siste rettingene av veilederrollene. Kildereiser, konkrete tokens og alle fem godkjente visuelle referanser er tilgjengelige for videre arbeid. Den opprinnelige gjennomgangen fant ett uavklart livsløpsvalg og noen interne katalog-/tilstandskonflikter som måtte ryddes før endelig overlevering.

De tre valgte linsene ga 13 rå observasjoner: 4 høye, 6 middels og 3 lave. R1/O4 og R5/A1 er overlapp. Etter sammenslåing: 11 ulike funn, fordelt på 3 høye, 5 middels og 3 lave; ingen kritiske. Alle 11 er håndtert i dokumenter eller referanser, inkludert brukerens presisering om sletting etter vellykket import. Mekanisk sluttkontroll er gjennomført: tokenreferanser, lokale lenker, kilder, komponentnavn og skissenes navigasjon er kontrollert. Klokkeplassering og aktiv Auto-understrek er også visuelt kontrollert i nettleseren. Implementasjonsverifikasjon gjenstår. De opprinnelige kategorivurderingene er bevart og er ikke automatisk oppgradert etter retting.

Dette er en statisk dokument- og referansevalidering, ikke endelig godkjenning, produktsertifisering, sanntidskontroll eller testing på montert nettbrett. Lesbarhet ved sideblikk, sollys/natt, hansker/vibrasjoner, lange navn/to samtidige meldinger og faktisk nettleser-/sensorstøtte må fortsatt verifiseres på enheten.

## Opprinnelige kategorivurderinger

- Flytdekning — **tilstrekkelig (adequate)**. Kildehistoriene UJ-1/UJ-2 har hovedperson, trinn, vendepunkt og feilbaner. Delte skift og UJ-3/UJ-4 dekker de siste rolleendringene. Det opprinnelige livsløpshullet er samlet under R1/O4.
- Tokenfullstendighet — **tilstrekkelig (adequate)**. Inspiserte tokenreferanser kunne løses; farger hadde konkrete verdier og dag-/nattpar. Kontrastkrav trengte en målbar akseptansegrense.
- Komponentdekning — **tilstrekkelig (adequate)**. Begge kataloger dekket de sentrale komponentene med reelle regler. Ett komponentnavn var ulikt.
- Tilstandsdekning — **tilstrekkelig (adequate)**. Frakobling, GPS-feil, usikkerhet, overtakelse og demonstrasjon var skilt. Første oppsummeringsgjennomgang og senere lesetilgang måtte skilles tydeligere.
- Visuell referansedekning — **tilstrekkelig (adequate)**. Alle fem godkjente referanser var lenket uten foreldreløse filer. De opprinnelige kjøreskissene manglet den senere godkjente klokken.
- Omfang og overpresisering — **tilstrekkelig (adequate)**. Tokenverdier kom fra godkjente skisser og var skilt fra responsive produktkrav. Noen gjentakelser burde ryddes i språkvasken; ingen egen vesentlig feil ble registrert.
- Arv og begrepsbruk — **tilstrekkelig (adequate)**. De fem kildebanene og tokenreferansene lot seg løse. Siste brukerbeslutninger var fulgt, men noen gamle åpne markører motsa dem. R3 gjelder også begrepsbruken.
- Dokumentform — **sterk (strong)**. DESIGN fulgte kanonisk rekkefølge. EXPERIENCE hadde de påkrevde delene og relevante tilleggsdeler for plattform, tillit, bevaring og operative roller.

## Funn etter alvorlighet

### Kritisk (0)

Ingen registrerte.

### Høy (3)

#### R1 / O4 — Livsløp og eksport for importerte personplaner

**Sted:** EXPERIENCE · personvern/bevaring; UJ-3/UJ-4; koblede planer.

**Opprinnelig observasjon:** Den opprinnelige sjudagersregelen avklarte ikke hvilken arbeidsdag som styrte sletting av en annen persons importerte plan, eller om hele personens dag kunne havne i veilederens PDF. Dette var et produktvalg, ikke noe lagringsarkitekturen kunne avgjøre.

**Tiltak og avklaring:** Brukeren har presisert: Den opplastede kildekopien slettes straks etter vellykket import. Nødvendige tolkede opplysninger holdes separat innen veilederens egen arbeidsdag. Oppsummering/PDF omfatter bare faktisk fulgte deler med observerte/usikre utfall; egne aktiviteter og overtakelser holdes adskilt. Ufulgte deler av hele personplanen beholdes ikke etter dagen og eksporteres ikke. Bevarte opplysninger følger egen arbeidsdags eksisterende sjudagersfrist. Dette er private importer, ikke tilgang på tvers av kontoer. Den siste beslutningen overstyrer den eldre kildefilbevaringen for denne importen.

**Status:** Avklart av brukeren og innarbeidet i dokumentkontrakten; må fortsatt verifiseres i implementasjonen.

#### O1 — Planrevisjon manglet eksplisitt eier

**Sted:** EXPERIENCE · delte skift/revisjoner; separate egne og koblede planer.

**Opprinnelig observasjon:** Med eget skift og flere personplaner kunne samme dato, linje, retning og avgang matche feil plan. En delvis revisjon kunne også bryte koblingen til en senere medkjøringsdel uten at det ble synlig.

**Tiltak og avklaring:** Revisjonsmålet navngis før filomfang og matching. Matching begrenses til målplanen; berørte koblinger vises, og uavklarte koblinger beholdes for eksplisitt retting. Andre planer og aktiv/manuell dokumentasjon bevares.

**Status:** Rettet i dokumentkontrakten.

#### O2 — Gjenoppretting manglet aktiv rolle og overtakelseskontekst

**Sted:** EXPERIENCE · aktivt skift/gjenoppretting; GPS-timer; akutt overtakelse.

**Opprinnelig observasjon:** Et omstartet nettbrett kunne tolke oppdragets FADDER-etikett som aktiv veilederrolle selv etter «Jeg kjører». Bevaring av tur og GPS-timer alene hindret ikke at åpne veilederkontroller kom tilbake.

**Tiltak og avklaring:** Gjenoppretting bevarer faktisk fører-/veilederrolle, oppdragsrolle, plan/del, aktivt turvalg og overtakelses-/returhendelser samlet. Akutt overtatt kjøring forblir FØRER til eksplisitt tillatt retur. Et etablert GPS-bortfall blir ikke et nytt oppstartsunntak.

**Status:** Rettet i dokumentkontrakten.

### Middels (5)

#### R2 — Kontrastmålinger manglet et forpliktende minstekrav

**Sted:** DESIGN · farger; EXPERIENCE · tilgjengelighet.

**Opprinnelig observasjon:** Eksempelkontraster og ønsket om høy kontrast ga ingen målbar terskel for nye tekstkombinasjoner, fokusmarkeringer eller kontrollgrenser i begge temaer.

**Tiltak og avklaring (korrigert 2026-09-27):** Den opprinnelige påstanden om allerede innlagte numeriske krav var feil. IR-01-tillegget over dokumenterer senere produkteierbeslutning og rettet kontrakt i PRD/DESIGN/EXPERIENCE. Kravet er nå testbart; målingene er ikke utført.

**Status:** Beslutning og dokumentkontrakt rettet etter readinessfunn IR-01. Rendret UI/PDF og montert enhet gjenstår som egne bevis.

#### R4 — Avsluttet oppsummering hadde motstridende redigeringsregler

**Sted:** EXPERIENCE · avsluttet dag; oppsummering; usikker gjennomføring.

**Opprinnelig observasjon:** «Kun lesing/eksport» gjaldt tilsynelatende også den første oppsummeringen der usikre aktiviteter skulle kunne bekreftes manuelt. En implementering kunne enten blokkere påkrevd bekreftelse eller tillate den uten tidsavgrensning.

**Tiltak og avklaring:** Første gjennomgang etter avslutning skiller seg nå fra senere gjenåpning. Manuell bekreftelse bevarer sin opprinnelse; skiftet forblir avsluttet og slettefristen endres ikke.

**Status:** Rettet i dokumentkontrakten.

#### R5 / A1 — Klokken manglet i de viktigste kjøre- og feildataskissene

**Sted:** mockups/driving.html; mockups/summary-recovery.html.

**Opprinnelig observasjon:** Den samlede gallerivisningen hadde klokke, mens de opprinnelige godkjente kjøre- og GPS/nettavbruddsreferansene manglet den. Et implementasjonsteam kunne derfor overse et eksplisitt godkjent krav.

**Tiltak og avklaring:** Den samme synlige klokken er føyd til de opprinnelige referansene, med tabelltall og tydelig simulert tid. Rute-/stoppinformasjon og nedtelling er fortsatt separate.

**Status:** Rettet i referansene.

#### R6 — Gamle åpne punkter motsa senere avklaringer

**Sted:** DESIGN · sekvensgrenser; EXPERIENCE · tilstander og fullføringsstandarder.

**Opprinnelig observasjon:** Dokumentene kalte fortsatt tomme stoppfelt, reguleringstid, beholdt oppsummering og manglende Auto-støtte uavklart, selv om senere standarder eller godkjente skisser hadde avklart dem.

**Tiltak og avklaring:** De foreldede markørene peker nå på gjeldende beslutninger. Reelle spørsmål om sensorer, automatisk temautløser og enhetsstøtte står fortsatt åpne.

**Status:** Rettet i dokumentkontrakten.

#### O3 — Manuelt valgt tur ved slutt på en delvis medkjøring

**Sted:** EXPERIENCE · manuelt turvalg; medkjøringsdeler og personbytte.

**Opprinnelig observasjon:** Turvalget skulle vare til turen var ferdig, samtidig som instruktøren kunne avslutte medkjøring midt i turen og senere returnere til samme person. Uten prioriteringsregel kunne gammel turbinding følge med eller gi falsk fullføring.

**Tiltak og avklaring:** Bindingen gjelder den aktive sporingskonteksten. Eksplisitt bekreftet bytte av del/person/aktivitet avslutter den konteksten uten å fullføre eller avbryte den andres tur. En senere del etablerer aktuell tur på nytt, også hos samme person.

**Status:** Rettet i dokumentkontrakten.

### Lav (3)

#### R3 — Samme stoppkontroll hadde to komponentnavn

**Sted:** DESIGN · Components; EXPERIENCE · Component Patterns.

**Opprinnelig observasjon:** «Stop Menu controls» og «Stop correction controls» beskrev samme komponent. Navneforskjellen brøt dokumentenes avtalte paring.

**Tiltak og avklaring:** Komponentnavnet er samordnet som «Stop correction controls».

**Status:** Rettet i dokumentkontrakten.

#### A2 — Auto-valget kunne bare skilles visuelt med farge

**Sted:** Temakontroll i driving.html og summary-recovery.html; DESIGN.

**Opprinnelig observasjon:** Grå/grønn Auto og aria-pressed fungerte for enkelte brukere og hjelpemidler, men synlige tilstander var ellers identiske. Det brøt kravet om at tilstand ikke bare skal uttrykkes med farge.

**Tiltak og avklaring:** Brukeren valgte en liten understreking når Auto er aktiv. Den er lagt til sammen med de godkjente fargene, ikonene og treffområdene.

**Status:** Rettet etter eksplisitt brukervalg.

#### A3 — Nattvisningens tastaturfokus brukte dagfargen

**Sted:** mockups/remaining-screens.html · focus-visible.

**Opprinnelig observasjon:** Vanlige knapper hadde en hardkodet mørk dagblå fokusramme på nattflaten, mens stoppinngangen brukte riktig nattfarge. Dermed var fokus synlig med ulik tydelighet i samme skjerm.

**Tiltak og avklaring:** Fokus innen produktflatene følger temaets informasjonsfarge, med egnet reservefarge for den lyse gallerinavigasjonen. Tykkelse og avstand beholdes.

**Status:** Rettet i referansen.

## De ekstra linsenes vurdering

Tilgjengelighetsgjennomgangen beholdt godkjent stopphierarki, synlige fartslåser, femminuttersunntak, veilederrolle og Registrert-alternativet. Den fant en konkret klokkemangel og to tilgjengelighetsdetaljer. Statisk aksept er ikke dokumentert lesbarhet i trafikk.

Den operative gjennomgangen utfordret planrevisjon på tvers av eiere, rollebevaring ved omstart, avgrenset medkjøring mot manuelt turvalg og livsløp/eksport. Den fant ingen grunn til å gjenåpne godkjente fart-/GPS-unntak, varselkvittering per versjon eller isolasjonen mellom offentlig fiktiv demo og operative data.

## Mekaniske merknader

- Alle inspiserte tokenreferanser og fem kildebaner lot seg løse. Alle fem godkjente mockups var lenket; ingen Mermaid-syntaks ble brukt.
- R1/O4 er ett livsløpsfunn; R5/A1 er ett klokkefunn. Rå totaltall: 13 (4 høye, 6 middels, 3 lave). Ulike funn: 11 (3 høye, 5 middels, 3 lave).
- Rårapportene er bevart. Deres opprinnelige linjenumre gjelder den vurderte utgaven, før rettingene.
- Rettet dokumentkontrakt er ikke det samme som verifisert implementasjon. Rapporten gir ingen endelig sertifisering eller påstand om enhetstesting.

## Reviewerfiler

- [Dokumentkontrakt og dekning](review-rubric.md)
- [Tilgjengelighet og førerplass](review-accessibility.md)
- [Operative grensetilfeller](review-operational.md)
