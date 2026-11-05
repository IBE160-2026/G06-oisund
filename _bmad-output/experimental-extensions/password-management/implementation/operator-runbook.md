# Operatørrutine — PM-E1-S2/S3

**Current code format (2026-11-05):** the readable-code correction at the end of this document supersedes the earlier 256-bit generation default. New codes use 20 characters / 100 bits; all lifecycle controls remain.

**Restore follow-up — 2026-11-04:** The owner-approved policy is now implemented on the experimental branch with isolated qualification and three-layer review completed. See [restore evidence](restore-evidence.md) and [operator restore routine](restore-runbook.md). The policy decision is closed; actual production installation/execution and owner qualification remain separate. Earlier statements about missing policy/tooling below are historical, not the current decision state.

**Oppdatert beslutningsstatus 2026-11-04:** [Fast rutine for nye passord etter restore er vedtatt](restore-policy.md). Tidligere formuleringer nedenfor om uavklart valg av passordautoritet er historiske. Implementasjon og kvalifisering av mekanismen gjenstår; ingen produksjonshandling er godkjent.

**Ingen live-utstedelse før S3/full reise og eierkvalifisering.** Dette er implementert for isolerte syntetiske prøver; det er ikke deployet. Identitetskontroll, praktisk kontakt, direkte overlevering og opptaksfri operatørøkt: **utsatt – krever eier**. S3 har innløsningsside og endepunkt for isolert syntetisk kvalifisering.

Jonas er eneste operatør. SSH/servertilgang, ytre Access og appkontoen er tre ulike tilganger. Operatørkommandoen bruker eksisterende privilegert database-/containeradgang, ingen appcookie, apppassord eller administratorrolle i appen. Velg eget appbrukernavn eksplisitt ved glemt eget passord. Manglende SSH krever separat vertstilgangsgjenoppretting; manglende Access krever separat Access-hjelp. Ingen av delene repareres av en appkode. Når Jonas er utilgjengelig, må brukeren vente på ham; ingen lovnad om straksstøtte eller skjult reserveadministrator.

## Før utstedelse

1. Bekreft personen ved personlig gjenkjenning eller uavhengig etablert tilbakeanrop/kontakt. Et oppgitt brukernavn alene er ikke identitetsbevis. Kontroller den allerede kjente institusjonsadressen eller direkte Teams-kontoen; ikke bruk en ny mottakeradresse bare fordi den oppgis i forespørselen. Samtidig kontakt under innløsning er ikke nødvendig.
2. Bruk en personlig kontrollert interaktiv terminal. Stopp ved PowerShell-transkripsjon, `script`, terminal-/SSH-opptak, sesjonsfangst, CI, shell wrappers, skjermopptak eller delt skjerm. Kontroller eventuell fjernadministrators opptakspolicy. TTY-testen oppdager ikke dette; teksten TRYGT er en operatørbekreftelse, aldri et teknisk bevis.
3. Send koden manuelt i en direkte Teams-melding eller e-post til den bekreftede, kjente institusjonskontoen, eller overfør den til eget testskjema. Ta med utløpstid med tidssone og vanlig appadresse uten kode i URL. Ingen felleskanal, CC, sak eller denne AI-chatten. Meldingshistorikk kan beholde koden; dette er ikke hemmelighetsfri meldingslagring. Koden er ubrukelig etter innløsning, tilbakekalling eller utløp. Ingen kode i logger, argumenter, miljøvariabler eller midlertidige filer. Ikke bruk utklippstavle med historikk/skysynk. Brukeren velger selv sitt nye passord i appen; det skal aldri sendes til operatøren.
4. Kontroller nøyaktig normalisert brukernavn **og UUID**, og skriv hele viste brukernavnet. Store/små bokstaver normaliseres og ytre mellomrom fjernes på samme måte som eksisterende kontoer. Ingen søk, delvis treff eller automatisk valg av egen konto. Navn med kontroll-/formattegn avvises uten kontoendring. Tomt svar, feil svar eller Ctrl-C avbryter.

## Kommandoer

I den isolerte Linux-testcontaineren (syntetiske kontoer):

```sh
docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec private-api python -m app.manage recovery-issue SYNTHETIC_BRUKERNAVN
docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec private-api python -m app.manage recovery-revoke SYNTHETIC_BRUKERNAVN
```

Erstatt plassholderen med eksakt syntetisk brukernavn. Ikke bruk `-T`, pipe eller omdirigering; stdin, stdout og stderr må være samme interaktive styrende terminal. Kommandoen avslører ingen hemmelighet på stdout/stderr; den skriver koden direkte til `/dev/tty` etter bekreftet databasecommit. Koden vises én gang med UTC-utløp, i terminalens alternative skjerm. Skriv SENDT straks koden er sendt til riktig mottaker eller overført til eget skjema; visningen tømmes. Ikke vent på svar eller lesekvittering. Dette er din bekreftelse på sending, ikke bevis på mottak. Koden er gyldig fra utstedelse, også før SENDT. Tømming er ingen garanti for slettet scrollback, skjermbilde eller opptak. Prosessminne er ikke en sikker slettbar hemmelighetsbeholder.

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

SENDT registrerer operatørens opplysning om sending når den eksakte kandidaten er aktiv/uutløpt eller allerede innløst. En brukt kode får status «allerede brukt» uten ny utstedelse eller påstand om uendret passord. Audit delivery/acknowledged betyr operatørbekreftet sending, ikke bekreftet mottak. Manglende, tilbakekalte og utløpte aktive koder avvises fortsatt; ingen kode gjenaktiveres. En nyere kode berøres ikke.

Tvetydig feil under eksplisitt tilbakekalling gir USIKKER tilbakekalling: kjør samme recovery-revoke på nytt, og ikke anta at tilbakekalling skjedde. Passordendring registrerer change/revoked i samme transaksjon som hashbytte, kodeinvalidering og øktsletting; aktøren er den autentiserte appkontoens UUID, ikke vertsoperatøren. Operatørhandlinger bruker fortsatt ærlig OS-kontekst, ikke antatt SSH-person. Kontrolltegn i opprinnelig brukernavn avvises også før normalisering, inkludert innledende/avsluttende tab/newline.

Disse tekniske grensene erstatter ikke praktisk identitets-, kontakt-, opptaks- eller overleveringskvalifisering: fortsatt **utsatt – krever eier**.


## Full reise i appen (S3)

Etter kontrollert kodeoverlevering åpner brukeren «Glemt passord?» ved appens innlogging og oppgir nøyaktig eksisterende brukernavn, kode og sitt eget nye passord to ganger (12–256 tegn, ingen trimming). En innlogget arbeidsflate må først forlates med uttrykkelig Logg ut og eksisterende ulagret-/pågående-arbeid-beskyttelse. API avviser en fortsatt live appøkt, også en annen konto.

Bekreftet innløsning bruker koden én gang, endrer passordet og avslutter alle kontoens appøkter atomisk. Den oppretter ingen ny økt: brukeren logger inn separat. UUID, eierskap, lagrede resultater/kvitteringer og frister beholdes. Jonas velger eget appbrukernavn på samme måte og trenger verken gammel appcookie eller glemt apppassord under utstedelse/innløsning.

Ved mistet/HTML/ugyldig svar, timeout eller avbrudd kan endringen allerede være gjennomført. Ikke gjenta koden automatisk: fullfør utlogging, prøv nytt passord, og gjennomfør eksplisitt tilbakekalling/ny utstedelse hvis nødvendig. At koden senere avvises kan bety at første forsøk lykkes; det er ikke bevis på at passordet er uendret. Feltene tømmes ved innsending og nettleseravbrudd.

Andre enheter mister gammel tilgang ved neste kontroll; ingen garanti om umiddelbar sletting av offline skjerm eller bevart ulagret innhold. Se [brukerveiledning](../../../../docs/password-recovery.md). Ytre Access og SSH forblir separate forutsetninger. Ingen live-bruk før praktisk identitet/overlevering/eieraksept og S4; **utsatt – krever eier**.

Mottakeren kan bruke koden før eller etter SENDT; dere trenger ikke koordinere innsendingen. SENDT endrer ikke passord eller økter. Hvis sending feiler, mottaker er feil eller utfallet er usikkert, bruk recovery-revoke for nøyaktig konto, også etter at terminalen er lukket. Ved allerede brukt kode: kontroller kontoens tilgang før eventuell ny utstedelse; tilbakekalling angrer ikke et allerede endret passord.

## S4 samlet kvalifisering og fremtidig driftskontroll

Den uavhengige syntetiske gateway/API/PostgreSQL-prøven er gjennomført; se [scenariobevis](s4-evidence.md) og [sluttvurdering](final-readiness.md). Oppskrift fra repository-roten: `node scripts/verify-password-s4.mjs`. Dette er bare lokale engangsressurser, ikke en produksjonskommando. Fysisk utstyr, faktisk SSH/MFA/Access, identitet/kontakt, opptaksfri overlevering og eieraksept er fortsatt **utsatt – krever eier**.

Ved fremtidig migrering/release: gjennomgå gjeldende kode og015-migreringen, fullfør eierkontrollene, bekreft backup og vedlikeholdsvindu, stans inngående trafikk/skrivearbeid og verifiser konto-IDer, eierskap, innhold, frister og kvitteringer etter migrering. Åpne først etter kontroll og uttrykkelig deploybeslutning. Det er ikke valgt en release eller utført produksjonsarbeid her.

Ved rollback: eksisterende `bussassistentctl` krever identiske private migreringsfiler. V1-kandidaten mangler015 og avvises av den vanlige rollback-inngangen selv om syntetisk testing viser at eldre kode kan lese skjema/hash. Ikke omgå denne sperren. `verify-restore` tester bare en isolert kopi; `restore-initial` nekter å erstatte en allerede deployet database. En egnet, gjennomgått og autorisert produksjonsrestore-prosedyre mangler fortsatt som kvalifisert vei for dette tilfellet; det er en releaseforutsetning, ikke en ny SQL-/sudo-oppskrift i denne rutinen.

Ved en senere autorisert restore må trafikken holdes stengt mens backup gjenopprettes, forretningsdata/frister kontrolleres, nødvendige utløpsregler kjøres og **alle** gjenopprettede appøkter og koder ugyldiggjøres. Kartlegg eldre passordhash for **hver berørt konto**. Gjennomfør kvalifisert gjenoppretting eller få en uttrykkelig, informert eieravklaring av den gjeninnførte passordautoriteten før åpning. Hvis kontakt/identitet/tilgang ikke kan kvalifiseres, forblir trafikken stengt. S4 kjenner bare sine syntetiske A-endret/B-uendret-tilfeller; dette er ingen garanti for vilkårlige virkelige brukere. Ingen ny tvungen reset-/kontolåsfunksjon er innført.

Kontroller til slutt at gamle økter/koder og erstattede passord avvises, nytt passord gir separat innlogging til riktig beholdt konto, og kontoisolasjon består. Backup kan ha eldre passord og mangle nyere arbeidsdata; aldri lov null konsekvenser. Følg den konkrete [fremtidige sjekklisten](final-readiness.md). Manglende SSH løses i separat vertstilgangsprosess; manglende ytre Access i separat Access-prosess. Jonas forblir eneste operatør, med best-effort støtte uten SLA; brukeren må vente når han ikke er tilgjengelig.

## v1.1.0 integration update — 2026-11-04

Maintenance main1501104 is integrated at merge b7af6b5. See the [current candidate qualification and concrete restore gap](v110-candidate.md). Historical baseline/test statements above retain their original scope. Owner-dependent stories remain open; technical existing-deployment restore/invalidation tooling also remains a distinct release prerequisite. Full O6 closure is not a blanket gate. No release or production action is authorized by this update.



## Readable-code correction — 2026-11-05

The owner requested 20 characters after the practical 43-character handoff failed. New codes use 20 independent CSPRNG selections from 32 symbols (100 bits), displayed as five groups of four. Alphabet: `ABCDEFGHJKMNOPQRSTUVWXYZ23456789`. Digit 0 is never used; O is a letter. I, L and 1 are excluded too. ASCII letter case, spaces and hyphens do not matter for new codes; Unicode lookalikes/control characters and digit 0 are rejected without substitution. Previously issued 43-character codes remain exact and case-sensitive until their original expiry. No migration or credential reset is introduced.

This supersedes the earlier 256-bit generation default, not the purpose/account binding, digest-only storage, 30-minute DB-clock TTL, one-use account transaction, 3 issues/hour or 5 admitted account attempts/15 minutes. The 100-bit uniform space remains infeasible for practical exhaustive guessing; online attempts are additionally bounded. At most 5 guesses in a bucket have probability at most 5/2^100 against a fixed live code. This is a reduction from 256 bits and must not be documented as retaining 256-bit entropy. SHA 256 stores only the canonical secret digest. Password policy and hashing are unchanged.

Manual sending by direct Teams message or email to the previously established institutional recipient is approved by the owner; the application sends no messages. The operator types SENDT after sending, without waiting for receipt or redemption. Recipient UI does not expose operator acknowledgement. Codes are already live on issue commit. An exact consumed proof can be acknowledged as already used, never revived; stale/revoked/expired active proofs remain rejected. Preserve terminal recording/clipboard controls and forbid codes in application logs, URLs, tickets, shared channels or AI chat. Message history may retain the code; its authority ends on use, revocation or expiry. The TTL remains 30 minutes; two hours was proposed but not approved. A fresh practical asynchronous handoff remains pending.
