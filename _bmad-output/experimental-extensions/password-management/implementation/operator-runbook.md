# Operatørrutine — PM-E1-S2/S3

**Ingen live-utstedelse før S3/full reise og eierkvalifisering.** Dette er implementert for isolerte syntetiske prøver; det er ikke deployet. Identitetskontroll, praktisk kontakt, direkte overlevering og opptaksfri operatørøkt: **utsatt – krever eier**. S3 har innløsningsside og endepunkt for isolert syntetisk kvalifisering.

Jonas er eneste operatør. SSH/servertilgang, ytre Access og appkontoen er tre ulike tilganger. Operatørkommandoen bruker eksisterende privilegert database-/containeradgang, ingen appcookie, apppassord eller administratorrolle i appen. Velg eget appbrukernavn eksplisitt ved glemt eget passord. Manglende SSH krever separat vertstilgangsgjenoppretting; manglende Access krever separat Access-hjelp. Ingen av delene repareres av en appkode. Når Jonas er utilgjengelig, må brukeren vente på ham; ingen lovnad om straksstøtte eller skjult reserveadministrator.

## Før utstedelse

1. Bekreft personen ved personlig gjenkjenning eller uavhengig etablert tilbakeanrop/kontakt. Et oppgitt brukernavn alene er ikke identitetsbevis. Avklar trygg direkte overlevering på forhånd.
2. Bruk en personlig kontrollert interaktiv terminal. Stopp ved PowerShell-transkripsjon, `script`, terminal-/SSH-opptak, sesjonsfangst, CI, shell wrappers, skjermopptak eller delt skjerm. Kontroller eventuell fjernadministrators opptakspolicy. TTY-testen oppdager ikke dette; teksten TRYGT er en operatørbekreftelse, aldri et teknisk bevis.
3. Ikke legg koden i e-post, chat, sak, logger, argumenter, miljøvariabler, filer eller URL. Foretrekk kontrollert direkte innføring. Ikke bruk utklippstavle med historikk/skysynk; avklar dette før eventuell kopiering. Brukeren velger selv sitt nye passord i appens «Glemt passord?».
4. Kontroller nøyaktig normalisert brukernavn **og UUID**, og skriv hele viste brukernavnet. Store/små bokstaver normaliseres og ytre mellomrom fjernes på samme måte som eksisterende kontoer. Ingen søk, delvis treff eller automatisk valg av egen konto. Navn med kontroll-/formattegn avvises uten kontoendring. Tomt svar, feil svar eller Ctrl-C avbryter.

## Kommandoer

I den isolerte Linux-testcontaineren (syntetiske kontoer):

```sh
docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec private-api python -m app.manage recovery-issue SYNTHETIC_BRUKERNAVN
docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec private-api python -m app.manage recovery-revoke SYNTHETIC_BRUKERNAVN
```

Erstatt plassholderen med eksakt syntetisk brukernavn. Ikke bruk `-T`, pipe eller omdirigering; stdin, stdout og stderr må være samme interaktive styrende terminal. Kommandoen avslører ingen hemmelighet på stdout/stderr; den skriver koden direkte til `/dev/tty` etter bekreftet databasecommit. Koden vises én gang med UTC-utløp, i terminalens alternative skjerm. Skriv MOTTATT etter trygg overlevering; visningen tømmes. Tømming er ingen garanti for slettet scrollback, skjermbilde eller opptak. Prosessminne er ikke en sikker slettbar hemmelighetsbeholder.

Fremtidig Ubuntu-instruksjon, **ikke utført eller autorisert for live nå**: bruk den eksisterende administratorinngangen fra en kontrollert interaktiv SSH-terminal:

```sh
sudo -n /usr/local/sbin/bussassistentctl recovery-issue BRUKERNAVN
sudo -n /usr/local/sbin/bussassistentctl recovery-revoke BRUKERNAVN
```

Helper-revisjonen er implementert i repository, men **IKKE installert på live-verten**. Den bruker validert `/opt/bussassistent/current`, fast Compose-fil `deploy/ubuntu/compose.yaml`, konfigurasjon `/etc/bussassistent/server.env`, prosjektnavn `bussassistent` og tjenesten `private-api` (se `docs/ubuntu-server.md`). Kommandoen tillater bare én brukernavnparameter, ingen ekstra flagg, prosjektvalg, vilkårlig kommando eller sti. Eksisterende root-/operasjonslås bevares; sudoers og rettigheter er ikke endret.

Helperen avviser omdirigert stdin/stdout/stderr og manglende/feil styrende forgrunnsterminal **før** Docker kan opprette en indre PTY. Docker-strømmene kobles direkte til denne terminalen; de fanges ikke i helperen eller sendes til vanlige omdirigerte strømmer. Appens egne terminal-/mål-/forhåndskontroller gjelder i tillegg. Direkte Docker-eksemplene ovenfor er kun for den syntetiske testcontaineren; de er ikke produksjonsinngangen. Verken host- eller containerkontrollen kan bevise fravær av opptak hos SSH-klient, sudo, terminal eller skjerm.

Vanlig senere gjennomgått helperinstallasjon/deploy og praktiske terminal-/opptakskontroller er **utsatt – krever eier**. Dette innfører ingen ny administrator eller generell Docker-/sudo-adgang. Ingen faktisk SSH/MFA/produksjonskommando er kjørt her.

## Livsløp og feil

Koden har 256 tilfeldige bits, 30 minutters levetid fra databasens klokke og bare SHA-256-digest lagres. Én aktiv kode per konto; ny utstedelse tilbakekaller den gamle atomisk. Høyst tre vellykkede utstedelser per konto i rullerende time. Tilbakekalling virker også etter grensen og er idempotent. Utstedelse/tilbakekalling endrer ikke passord, appøkter, UUID eller lagrede arbeidsdata. Passordendring tilbakekaller utestående kode i samme transaksjon som hashbytte og øktsletting.

Ved utløpt kode eller feil overlevering: bekreft kontoen på nytt, tilbakekall og utsted en ny kode hvis timebudsjettet tillater det. Det finnes ingen gjenvisning/henting av gammel kode. Ved avbrudd etter commit forsøker kommandoen tilbakekalling. Kandidatens UUID er kjent før transaksjonen starter; kompensasjonen tilbakekaller bare den utstedelsen, også ved usikker commit. Tidligere gyldig kode etter rollback og nyere konkurrerende utstedelse bevares. Bare eksplisitt `recovery-revoke` tilbakekaller alle utestående koder.

Hvis terminal/DB-feil gjør tilbakekalling usikker, sier kommandoen USIKKER og instruerer eksplisitt `recovery-revoke`. Gjennomfør dette når tilgangen er tilbake; ikke anta at fravær av vist kode betyr at DB ikke committet. TTL begrenser uavklart autoritet til 30 minutter. SIGINT/SIGTERM/SIGHUP/SIGTSTP håndteres; strømbrudd/SIGKILL kan ikke fanges og krever samme tilbakekallingsrutine.

Audit lagrer kun UUID, OS-kontekst (numerisk container-UID), handling, resultat og tidspunkt. Dette er **ikke bekreftet Jonas-/SSH-identitet**. Personattribusjon må korreleres med uavhengig godkjent SSH-/vertsaudit. Ingen brukertilført aktøretikett godtas. Avvisning før mutasjon (ukjent konto, manglende terminal, feil bekreftelse) lager ingen konto-/kodemutasjon. DB-feil kan også hindre audit, og fravær av audit er derfor ikke bevis for vellykket eller mislykket levering.

Ordinær cleanup tar samme kontolås, fjerner utløpte/tilbakekalte/brukte digester og audit eldre enn 30 dager i avgrensede batcher. Kjør og overvåk den etablerte cleanup-jobben slik at digester fjernes innen 24 timer; utløp må uansett kontrolleres ved S3-aksept og er aldri avhengig av cleanup. Ingen konto-/forretningsrad slettes for å tilbakekalle tilgang.

## Historisk S2/S3-handoff før S4

S4 må øve restore/rollback separat med syntetiske data: stans trafikk, gjenopprett/verifiser arbeidsdata, ugyldiggjør alle gjenopprettede appøkter og koder før åpning, og håndter eksplisitt at backup kan gjeninnføre eldre passordhash. Eldre kodekompatibilitet og gjeldende migreringskontroll må verifiseres; ingen automatisk nedgradering eller produksjonsrestore er utført.

Full syntetisk egenkonto-/lærerkontoreise er implementert i S3; S4 og praktisk eierkvalifisering gjenstår. Praktisk identitet/kontakt/overlevering uten opptak, egenkonto via faktisk SSH, eieraksept og målbrett: **utsatt – krever eier**. S2 skal ikke merkes ferdig på grunnlag av syntetisk PTY alene.



## Avgrenset dialog og sannferdig feilstatus

Hele operatørdialogen har en fast frist på fem minutter fra oppstart, ikke fem nye minutter per svar. Ved kodevisning begrenses resterende tid også av kodens databaseutløp. Ingen svar innen fristen avbryter, tømmer/gjenoppretter terminalen og forsøker kandidatavgrenset tilbakekalling. Ctrl-Z/SIGTSTP avbryter på samme måte i stedet for å suspendere en synlig kode. En forlatt menneskelig prompt blir dermed ikke stående med vertshelperens operasjonslås. Eventuell DB-/tilbakekallingsfeil håndteres som usikkert utfall, ikke som vellykket tilbakekalling.

MOTTATT gir bare bekreftet overlevering når nøyaktig den utstedte kandidaten fremdeles er aktiv og ikke utløpt under kontolåsen. Hvis passordendring, tilbakekalling, ny utstedelse eller utløp kom i mellom, gis ikke vellykket leveringsaudit: kontroller kontoen og utsted ny kode ved behov. En nyere kode tilbakekalles ikke av den gamle dialogens kompensasjon.

Tvetydig feil under eksplisitt tilbakekalling gir USIKKER tilbakekalling: kjør samme recovery-revoke på nytt, og ikke anta at tilbakekalling skjedde. Passordendring registrerer change/revoked i samme transaksjon som hashbytte, kodeinvalidering og øktsletting; aktøren er den autentiserte appkontoens UUID, ikke vertsoperatøren. Operatørhandlinger bruker fortsatt ærlig OS-kontekst, ikke antatt SSH-person. Kontrolltegn i opprinnelig brukernavn avvises også før normalisering, inkludert innledende/avsluttende tab/newline.

Disse tekniske grensene erstatter ikke praktisk identitets-, kontakt-, opptaks- eller overleveringskvalifisering: fortsatt **utsatt – krever eier**.


## Full reise i appen (S3)

Etter kontrollert kodeoverlevering åpner brukeren «Glemt passord?» ved appens innlogging og oppgir nøyaktig eksisterende brukernavn, kode og sitt eget nye passord to ganger (12–256 tegn, ingen trimming). En innlogget arbeidsflate må først forlates med uttrykkelig Logg ut og eksisterende ulagret-/pågående-arbeid-beskyttelse. API avviser en fortsatt live appøkt, også en annen konto.

Bekreftet innløsning bruker koden én gang, endrer passordet og avslutter alle kontoens appøkter atomisk. Den oppretter ingen ny økt: brukeren logger inn separat. UUID, eierskap, lagrede resultater/kvitteringer og frister beholdes. Jonas velger eget appbrukernavn på samme måte og trenger verken gammel appcookie eller glemt apppassord under utstedelse/innløsning.

Ved mistet/HTML/ugyldig svar, timeout eller avbrudd kan endringen allerede være gjennomført. Ikke gjenta koden automatisk: fullfør utlogging, prøv nytt passord, og gjennomfør eksplisitt tilbakekalling/ny utstedelse hvis nødvendig. At koden senere avvises kan bety at første forsøk lykkes; det er ikke bevis på at passordet er uendret. Feltene tømmes ved innsending og nettleseravbrudd.

Andre enheter mister gammel tilgang ved neste kontroll; ingen garanti om umiddelbar sletting av offline skjerm eller bevart ulagret innhold. Se [brukerveiledning](../../../../docs/password-recovery.md). Ytre Access og SSH forblir separate forutsetninger. Ingen live-bruk før praktisk identitet/overlevering/eieraksept og S4; **utsatt – krever eier**.

Hvis mottakeren bruker koden før operatøren skriver MOTTATT, er kandidaten allerede brukt. S2-dialogen krever fortsatt aktiv/uutløpt kandidat for leveringskvittering og kan derfor avvise MOTTATT selv om appens passordendring lyktes. Ikke tolke dette som mislykket gjenoppretting og ikke utsted ny kode automatisk. Kontroller først appens resultat og la mottakeren prøve separat innlogging med det nye passordet; tilbakekall/utsted på nytt bare hvis tilgang fortsatt må gjenopprettes. Kandidatbegrenset kompensasjon endrer ikke et allerede konsumert bevis eller passordet.

## S4 samlet kvalifisering og fremtidig driftskontroll

Den uavhengige syntetiske gateway/API/PostgreSQL-prøven er gjennomført; se [scenariobevis](s4-evidence.md) og [sluttvurdering](final-readiness.md). Oppskrift fra repository-roten: `node scripts/verify-password-s4.mjs`. Dette er bare lokale engangsressurser, ikke en produksjonskommando. Fysisk utstyr, faktisk SSH/MFA/Access, identitet/kontakt, opptaksfri overlevering og eieraksept er fortsatt **utsatt – krever eier**.

Ved fremtidig migrering/release: gjennomgå gjeldende kode og015-migreringen, fullfør eierkontrollene, bekreft backup og vedlikeholdsvindu, stans inngående trafikk/skrivearbeid og verifiser konto-IDer, eierskap, innhold, frister og kvitteringer etter migrering. Åpne først etter kontroll og uttrykkelig deploybeslutning. Det er ikke valgt en release eller utført produksjonsarbeid her.

Ved rollback: eksisterende `bussassistentctl` krever identiske private migreringsfiler. V1-kandidaten mangler015 og avvises av den vanlige rollback-inngangen selv om syntetisk testing viser at eldre kode kan lese skjema/hash. Ikke omgå denne sperren. `verify-restore` tester bare en isolert kopi; `restore-initial` nekter å erstatte en allerede deployet database. En egnet, gjennomgått og autorisert produksjonsrestore-prosedyre mangler fortsatt som kvalifisert vei for dette tilfellet; det er en releaseforutsetning, ikke en ny SQL-/sudo-oppskrift i denne rutinen.

Ved en senere autorisert restore må trafikken holdes stengt mens backup gjenopprettes, forretningsdata/frister kontrolleres, nødvendige utløpsregler kjøres og **alle** gjenopprettede appøkter og koder ugyldiggjøres. Kartlegg eldre passordhash for **hver berørt konto**. Gjennomfør kvalifisert gjenoppretting eller få en uttrykkelig, informert eieravklaring av den gjeninnførte passordautoriteten før åpning. Hvis kontakt/identitet/tilgang ikke kan kvalifiseres, forblir trafikken stengt. S4 kjenner bare sine syntetiske A-endret/B-uendret-tilfeller; dette er ingen garanti for vilkårlige virkelige brukere. Ingen ny tvungen reset-/kontolåsfunksjon er innført.

Kontroller til slutt at gamle økter/koder og erstattede passord avvises, nytt passord gir separat innlogging til riktig beholdt konto, og kontoisolasjon består. Backup kan ha eldre passord og mangle nyere arbeidsdata; aldri lov null konsekvenser. Følg den konkrete [fremtidige sjekklisten](final-readiness.md). Manglende SSH løses i separat vertstilgangsprosess; manglende ytre Access i separat Access-prosess. Jonas forblir eneste operatør, med best-effort støtte uten SLA; brukeren må vente når han ikke er tilgjengelig.
