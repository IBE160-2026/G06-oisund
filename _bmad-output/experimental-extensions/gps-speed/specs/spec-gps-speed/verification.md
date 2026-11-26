# Senere verifikasjon — ingen produktkontroller kjørt

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Dette er forventet testgrunnlag for GS-E1. Alle scenarier har status **PLANLAGT / IKKE KJØRT**. Tall i GPS-LAB-1 og feltprotokollen er uprøvde forslag. Dokumentkontroll finnes separat i [validation.md](../../planning/validation.md).

## Syntetiske kontroller med uavhengige forventninger

| ID | Tilfelle og forventning | Story |
|---|---|---|
| V01 | To gode 10 m/s-fikser med 1 s mellomrom gir 36 km/t. null, undefined, NaN, Infinity, strengverdi, negativ og >55,56 gir —; ingen coercion. | S1/S2 |
| V02 | Kvalifisert 0 gir 0. 0,1 m/s gir <1; 0,5 m/s gir 2; 12,5 m/s gir 45. To null gir aldri 0. | S1/S2 |
| V03 | 2999 ms kan være kvalifisert; 3000 ms er ukjent. En 2500 ms gammel prøve kan maksimalt leve 500 ms til. Ingen callback: utløp likevel. | S1/S2 |
| V04 | Duplikat/sen prøve fornyer ingenting; framtidstid og wall/monotonic-avvik >1000 ms avbryter. Replays kan ikke holde visningen fersk. Test både forover- og bakoverhopp i klokken. | S2 |
| V05 | Oppstart krever to prøver; 0,1 s-burst fornyer ikke fart før ≥0,5 s-ankeravstand. 0,7/1,8/2,6 s-intervaller vurderes etter faktisk tid. Ved ≥3 s fartsalder kreves nytt par; ≥10 s råfix-gap krever manuell resume. | S2 |
| V06 | Syntetisk jevn 0→5→10 m/s og 10→5→0 med 1 s-steg følges uten ekstra filterlag etter kvalifisering. Kø 0→0,1→0,5→0 m/s forveksles ikke med null. Kortvarig avvisning viser —. | S2 |
| V07 | Grove koordinat- og native fartshopp avvises; negativ/for stor accuracy avvises. Stillestående koordinatdrift med native 0 lager ikke fart. Etter hopp kreves to nye koherente prøver; ingen låsing til gammelt anker. | S2 |
| V08 | Opt-in, benektet OS/nettlesertillatelse, Pause/Off, hidden/lock, pagehide, reload, timeout, tilgangstap, skift-/aktivitetsbytte og sen callback/tillatelse: ingen oppstandelse. Felles watch-telling er 0 avbrutt og maksimalt 1 aktiv. Resume fart gjenopptar ikke progresjon. | S1/S3 |
| V09 | Alle fire kjent/ukjent-kombinasjoner av egen fart og grense vises korrekt; tvetydig veg/ukjent videre arm påvirker bare berørt grenseinformasjon. | S3 |
| V10 | Inspeksjon av nettverk, logger og browser-/serverlagring finner ingen råfix, fartshistorikk eller skjult GPS-kø. RAM-tak og rydding testes også ved feil/unmount. | S1/S3 |
| V11 | Samme evaluator/profil/UI brukes med to fiktive strekninger med ulike navn/ID-er; ingen kjernelogikkendring eller hardkodet pilot. | S3 |
| V12 | Endring i egen fart endrer ikke dagens fixed-distance=300 m eller utløser lyd/alarm; qualifiedSpeed er bare mulig framtidig konsumentkontrakt. | S3 |

Forventninger beregnes selvstendig fra enheter, klokker og kontrakt; ikke snapshot av implementasjonens egne svar. Fake clock og injisert kilde dekker grenseverdier. Browseremulering kvalifiserer UI/livssyklus, ikke målekvaliteten. Kontroller også at source-timestamp aldri erstattes av mottakstid. Profilendring resetter kvalifiseringen.

## Lenovo, Brave og Chrome — konkret senere protokoll

Før test: dokumenter faktisk modell, Android-/OS-build, Brave-/Chrome-versjon, profil/revisjon, tillatelsesnivå, stedstjeneste og betrodd HTTPS. Test hver nettleser separat med samme protokoll; et resultat arves ikke på grunnlag av Chromium. Fysisk kjøring krever senere autorisasjon, fører uten testinteraksjon og observatør ved behov.

Frys terskler og et uavhengig referanseoppsett **før** måling. Et instrument med dokumentert usikkerhet ≤1 km/t i aktuelle områder er foreslått; nettbrettets andre app eller samme posisjonstjeneste er ikke uavhengig. Kjøretøyets panel er bare en grov sammenligning uten kjent feilmodell. Manglende egnet referanse gir «nøyaktighet ikke kvalifisert», selv om visningen fungerer. Ingen kjøretøytilkobling kreves eller bygges.

| Feltkontroll | Foreslått pass/fail-kriterium, per nettleser |
|---|---|
| Start | Tre kalde/varme starter i åpent miljø; kvalifisert fart innen 30 s etter samtykke ved alle tre. Rapportér faktisk tid, også feil. |
| Stillstand | 2 min kontrollert fysisk stillstand: ≥95 % tid med kvalifisert verdi, ≥95 % av kvalifisert tid viser 0, ingen viste verdier >3 km/t. Registrer andel <1 og null-speed separat. Samme test i mer skjermet miljø, rapportert separat uten garantert dekning. |
| Stabil bevegelse | Tre 30 s-segmenter i forskjellige lovlige, praktiske fartsområder: ≥95 % kvalifisert tidsdekning per segment; median absoluttfeil ≤3 km/t og p95 ≤5 km/t mot kvalifisert referanse. Anvend usikkerhetsbudsjettet konservativt, ikke trekk referansefeilen fra observert feil. |
| Akselerasjon/bremsing/kø | Tre start–stopp-sekvenser og 2 min sakte kø: total observert overgangsforsinkelse ≤2 s mot referansen; ingen gammelt tall utover aldersfristen. Oppstart med to-prøvers port inngår. Ikke godkjenn stillstandsfilter som skjuler faktisk købevegelse. |
| Manglende oppdateringer | I aktiv foreground: — senest 250 ms etter profilens 3000 ms-frist. Ved målt hardt råfix-gap på 10 s: watch stoppet, manuell resume kreves. Timerstans/OS-suspensjon rapporteres som begrensning; første synlige render viser aldri gammel fart. |
| Avbrudd | Pause/Off, skjermlås, appbytte, nettleserreload, posisjonstillatelse av/på og privat tilgangstap: hver variant gjentas 3 ganger; ingen gammel fart eller automatisk watch/start ved retur. Ny eksplisitt resume og nye prøver kreves. |
| Samvisning | Ingen fartsgrense/ukjent veg og kjent grense: egen fart virker etter sine egne regler. Samme visning leses i Day/Night og begge orienteringer. |
| Ressurser/personvern | Maksimalt én aktiv autorisert watch, ingen ved global Pause/Off/skjult side. Ingen råposisjoner i nettverk, konsoll/telemetri eller persistent lagring. Observer strøm-/varmebelastning i 20 min og beskriv praktisk begrensning; ingen batterilevetid loves. |

Overgangsforsinkelse måles ved forhåndsvalgte kryssinger av 10 km/t opp/ned, 1 km/t ved køstart/-stopp og fysisk stopp mot native 0. Referanse og app synkroniseres innen 250 ms; denne usikkerheten inngår i budsjettet. Manglende kvalifisert kryssing er ikke bestått lagtest. Ukjent-tid inngår i dekning, også under dynamikk.

Prosenter måles som tid, ikke callback-antall: høy callback-rate må ikke skjule lange hull. Aggreger feil/lag/dekning under forsøket i avgrenset RAM, deretter behold kun sammendrag per scenario og versjon uten koordinater, privat reiserute, absolutt tidsserie eller full fartshistorikk. Sanitér skjermbilder og rapporter. Ingen råfix-logging for å «bevise» personvern.

Hvis dekning, null-semantikk, støy, bremselag eller referansekrav svikter: markér berørt enhet/nettleser/profil **ikke kvalifisert**. Endringer etter et feilresultat krever ny profil og ny kontroll; ikke flytt beståttgrensen i etterkant. En teknisk undersøkelse kan avsluttes med et dokumentert no-go, men epicens operative aksept er da ikke bestått.
