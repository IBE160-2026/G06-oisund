# Produktatferd

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Normativt førsteomfang avledet fra CAP-1–5 og SL-D1–5. «Kvalifisert» krever frosset profil for målealder, nøyaktighet, sekvensstøtte, alternativseparasjon, geometrikvalitet og passering; tall må dokumenteres før senere pilotkjøring. Dette dokumentet oppfinner ingen fysisk bestått GPS-profil.

## Uavhengige vilkår

**Aktuell verdi:** gyldig foreground-kontekst + fersk, sammenhengende og entydig faktisk vegtilknytning/retning + kjent gyldig fartsgrense for hele mulig posisjonsintervallet. Alle relevante felt-/kjørebanekandidater må støtte samme anvendelige verdi. Ukjent vegidentitet gir ukjent selv om nærliggende veger tilfeldigvis har samme tall.

**Forvarsel:** aktuell tilknytning kvalifisert + sammenhengende rettet veg videre til en reell verdiendring + kvalifisert valg av alle relevante avkjøringer + gyldige verdier frem til/på andre siden. Uavklart arm før endringen undertrykker forvarsel. Planlagt trasé alene gjør ikke armen sikker. En entydig felles veg frem til endringen kan støttes selv om et senere kryss er uavklart.

| Aktuell veg/data | Veg til endring | Visning |
|---|---|---|
| Kvalifisert | Kvalifisert, endring innenfor terskel | Stort aktuelt skilt + mindre kommende skilt og «om ca. N m». |
| Kvalifisert | Uavklart arm, hull eller ingen kvalifisert endring innenfor terskel | Aktuell beholdes; ingen kommende skilt. Skill «Videre veg usikker»/«Forvarselsdata mangler» fra «Ingen registrert endring innen 300 m». Sistnevnte krever komplett fremoversikt. |
| Ukvalifisert faktisk veg, foreldet måling eller ugyldig aktuell data | Uansett | Aktuell ukjent med årsak; forvarsel skjult. Ingen tallfallback. |
| Posisjonsintervallet krysser verdiendringen | Tidligere varsel kan være kjent | Aktuell ukjent; kommende nedtelling skjules fordi endringen ikke sikkert ligger foran. Ingen «0 m» som blir hengende. |

Skiltene har separate etiketter «Registrert vegfartsgrense» og «Neste fartsgrense». Aktuelt skilt er størst, neste mindre men lesbart; tekstalternativ og dag-/nattlesbarhet kreves. Vis ikke en grånet gammel tallverdi som erstatning for ukjent. Usikkerhetsårsak skal være tekst, ikke bare farge. En utgangsstatus uten kjente endringer lover aldri fravær av midlertidig regulering.

## Fast 300 m og passering

Avstand er restlengde på aktuell rettet lenkeforekomst + mellomlenker + del av mållenken; inkluder innkjøring, bue og riktig utkjøring i en rundkjøring. Bruk kvalifisert metrisk grunnlag, aldri luftlinje eller avstand mellom holdeplasser. En løkke kan forekomme flere ganger og må ha forekomstidentitet.

Aktiver ved første kvalifiserte sekvens der hele estimert avstandsintervall er positivt og høyst 300 m. Nær 300 m kan usikkerhet derfor utsette visningen; dette skal måles senere, ikke skjules som nøyaktig varsling. Skjermteksten bruker avrundet sentralestimat med «ca.»; forslag er nærmeste 10 m, minst 10 m så lenge endringen sikkert er foran. Tall oppdateres fra ny kvalifisert posisjon; ingen klokke- eller egenfartsdrevet nedtelling. Ved reell fremdrift teller den ned; ved stopp holdes den bare så lenge ferske målinger fortsatt kvalifiserer tilknytningen. En reell, underbygget bevegelse bort kan øke avstanden og er ikke et nytt varsel.

| Hendelse | Krav |
|---|---|
| Første sikre måling ved 120 m | Vis straks faktisk ca.-avstand, ikke «300 m» og ikke krav om tidligere terskelkryss. |
| Økning eller reduksjon | Samme terskel/gates; ingen tidlig oppjustering av aktuell verdi. |
| Flere endringer tett | Vis nærmeste verdiendring. Etter sikker passering vises neste straks dersom innen 300 m. Like naboverdier sammenfattes. Ukjent mellomliggende intervall må ikke hoppes over. |
| Pendling 302/298/301/297 m | Én visuell aktivering per passering. Aktivt panel kan bestå litt over terskelen innen frosset hystereseprofil, med sann avstand; utover denne trekkes det tilbake. Profilen endrer ikke første aktiveringsterskel. |
| Bortfall av tidligere vist varsel | Fjern skilt/avstand straks ved tapt støtte, feil arm, hull eller foreldelse; vis årsak. Sikker aktuell verdi beholdes. Ingen forsvunnet endring registreres som passert. |
| Samme endring kvalifiseres igjen | Samme panel kan komme tilbake med ny avstand; ingen gjentatt aktiveringsanimasjon i samme passering. Ingen lyd. |
| Passering | Flere sammenhengende ferske målinger må plassere hele mulig posisjon på ny side, med underbygget rettet nettverksovergang. Før det overtar ikke neste verdi. |

Passeringstilstand nøkkeles på økt, rettet endringsforekomst og korridor-/datasnapshot. Datasnapshotbytte starter revalidering og skjuler forvarsel; det gir ikke i seg selv en ny fysisk passering eller ny animasjon. Øktlokal deduplisering beholdes over korte avbrudd; ny passering krever underbygget ny tilnærming. Reload har ny økt og ingen lovnad om vedvarende historikk/deduplisering.

## Feil veg og avbrudd

Flere tidsordnede målinger, retning og lovlige topologiske overganger skal skille parallelle veger. Et rapportert accuracy-tall er ikke i seg selv sikker vegidentitet. Stillstand etablerer ingen ny kjøreretning; ferske konsistente stillestående fikser kan bevare tidligere støttet tilknytning, men ikke løse en tvetydig avkjøring.

GPS-hopp, feil tidsrekkefølge eller umulig overgang forkastes og berørt evidens nullstilles. Ingen hopp gjennom grenser eller tvang til planlagt veg. Ved posisjonsavbrudd/tunnel trekkes verdier tilbake når profilen ikke lenger kvalifiserer posisjonen; ingen blind tunnelberegning. Pause/Off eller avbrutt sensing krever eksplisitt gjenopptakelse og ny vegkvalifisering. Manuelt valgt stopp er kontekst, aldri bevis for aktuell grense.

Ved avvik oppheves forventet videre trasé. En ny entydig faktisk veg med kvalifisert data kan gi aktuell grense; forvarsel kommer tilbake først når relevant videre veg også er kvalifisert. Tilgangstap/kontekstbytte skjuler hele den private visningen og stopper behandling etter eksisterende grenser.
