# Praktiske passordprøver — oppstart 2026-11-04

Status: klargjøring kontrollert; ingen praktisk eierprøve bestått ennå.

## Kandidat og gjenbruk

Remote og lokal passordbranch er kontrollert mot `4b1260fc3f64716e2d3fba0d042f134d093beace` (produktendring `dafc19d7e11c334c531cc12c6cdf5c4340dc6e05`). Fersk origin/main er fortsatt `15011042b1fe093becbe68177e6396e456b1f35f`. Ingen produktkode er endret. [Restore-evidens](restore-evidence.md) og uendret frontend-/S1–S4-evidens gjenbrukes innen sine dokumenterte grenser. Ingen automatiserte fullkjøringer gjentas uten grunn.

## Lokalt oppsett

- Eget Compose-prosjekt `ibe160-pm-owner-20261104`, egen ny volume `ibe160-pm-owner-20261104_password_tests_private`.
- `compose.password-tests.yaml` med ignorert `tmp/pm-owner-20261104/overlay.yaml`; bare private-db/private-api startet. PG-image er tidligere kvalifisert `ibe160-password-rc-pg:20261104`; API bygget fra kandidaten. Eget testprosjekt, ingen produksjonsvolumer eller Docker-socket i containeren.
- Privat API bare `127.0.0.1:18441`; frontend bare `127.0.0.1:15440/private`. Ingen LAN-port, tunnel, brannmurendring eller produksjonsinngang.
- Frontend bygget med VITE_PRIVATE_API=http://127.0.0.1:18441 og separat output `tmp/pm-owner-20261104/dist`; TypeScript/Vite bestått. Egen skjult Vite-previewprosess; PID i samme ignorerte mappe.
- Ny database: 0 kontoer og 15 migreringer verifisert. API health=ok/private-local og frontend HTTP200. Dette er oppsettskontroll, ikke innloggingsaksept.
- Forberedt lokal `opprett-testkonto.ps1` kaller en avgrenset syntetisk provisioningprøve med skjult getpass. Krever interaktiv terminal, eksakt testmiljømarkør og tom syntetisk database; oppretter bare `synthetic-eier-pm`. Nekter eksisterende kontoer og endrer ikke passord ved omkjøring. Passord sendes ikke via argument, miljø, fil eller chat. Konto opprettes først når eier kjører steget. Faglærers separate testkonto forberedes når den prøven trengs.
- Andre eksisterende tjenester (`ibe160-v1-final-20261031`) er urørt. Oppgavens to containere og preview beholdes i drift for den pågående guidede prøven; etter avsluttet prøve stoppes bare dette prosjektet og den verifiserte preview-PIDen. Volum beholdes til resultatene er sikret; ingen automatisk sletting.

## Én prøve om gangen

1. **Neste eiersteg:** i egen terminal uten opptak/transkripsjon kjøre lokal konto-oppretting og velge et nytt testpassord (12–256 tegn), aldri et virkelig passord. Rapporter bare «Testkonto opprettet» eller feiltekst uten hemmeligheter.
2. Deretter kontrolleres appinnlogging og videre PC/nettbrettoppsett. Ikke naviger eksisterende produksjonsfane. Nettbrettet er ikke betjent eller koblet til dette miljøet ennå.
3. Praktisk full SSH → fast helper → Compose-PTY → CLI: **ikke klargjort/ikke bestått**. Lokal inventar viser bare docker-desktop WSL og ingen separat Ubuntu-testvert. Direkte container-CLI godskrives aldri som denne prøven. Separat isolert vert med uavhengig SSH og kandidatens installerte helper må etableres før prøven; produksjonsserveren brukes ikke som snarvei.
4. Resterende eierporter beholdes: trygg identitet/kodeoverlevering, issue/revoke/egen kontogjenoppretting, begge passordflyter, to enheter/nettbrudd/ulagret arbeid og personlig aksept. Resultat registreres som eieropplyst eller direkte observert, med faktisk kandidat/enhet. Ingen hemmeligheter/skjermbilder av kode/passord.

Ingen produksjon, main-merge, deploy, tag eller release. Dette lokale loopback-oppsettet dokumenterer ikke produksjons-HTTPS, Access, SSH, systemd eller fysisk nettbrettaksept. Epic/storyer forblir i review. Praktiske resultater føres her fortløpende og pushes på passordbranchen.

## Eierprøver 2026-11-05 — PC og klargjøring av nettbrett

Eierutført og rapportert i chat, samme lokale testmiljø/kandidat:
- Testkonto synthetic-eier-pm opprettet og innlogging til Privat arbeidsrom bekreftet.
- Feil gjeldende passord avvist. Vedlagt skjermbilde viste «Gjeldende passord er feil.», tømte felt og innlogget visning i nattmodus. Avbryt returnerte til arbeidsrommet uten ny innlogging. «Privat arbeidsrom» er en markør, ikke en knapp; veiledningen ble korrigert.
- To separate PC-økter (vanlig og privat nettleservindu) innlogget samtidig. Eier endret passord med riktig gjeldende passord. Bekreftelsen fortalte at passordet var endret og alle enheter logget ut; eier rapporterte innloggingsskjerm i begge vinduer.
- Ett innloggingsforsøk med gammelt passord ble avvist; nytt passord ga tilgang til arbeidsrommet. Dette kvalifiserer de beskrevne PC-prøvene, ikke to fysiske enheter eller databevaring/nettbrudd.

Oppsettsavvik: PowerShell blokkerte .ps1 etter lokal execution policy; kommandoen ble kjørt direkte uten policyendring. Første Python-forsøk fant ikke app-modulen; eksplisitt PYTHONPATH=/app rettet testkjøringen. Et tiltenkt testpassord ble før konto-oppretting feilaktig skrevet som shellkommando og kom med i eierens feilmelding. Verdien er ikke gjengitt i evidens. Eier ble instruert om å velge et annet testpassord. Ingen garanti om sletting fra lokal shellhistorikk eller chat; ingen reell credential kjent berørt.

Nettbrett: eier oppgir USB tilkoblet og feilsøking aktiv. ADB-inventar viser én enhet, men status unauthorized. Ingen reverse-regler er opprettet, ingen nettleser/produksjonsfane betjent. Neste steg krever eierens godkjenning av USB-feilsøking på enheten. Lokal frontend HTTP200 og privat API health=ok bekreftet på nytt. Første begrensede ADB-kall kunne ikke starte daemon; autorisert kall startet daemon og viste autentiseringsbehovet. Ingen omgåelse forsøkt. SSH, kodeoverlevering, fysisk to-enhetsprøve, nettbrudd og øvrig aksept står fortsatt åpne.

USB-oppfølging05.11: etter eiers bekreftelse viser ADB device (modell TB361FU). Ingen eksisterende reverse-regler; opprettet bare tcp15440→15440 og tcp18441→18441 med --no-rebind og verifisert listen. Frontend200/APIhealthok kontrollert. Ingen app/fane åpnet av agenten; eier skal åpne testadressen i en ny nettbrettfane. Enhetsinnlogging og to-enhetsprøve er ennå ikke bekreftet. Ved avslutning fjernes bare disse oppgaveopprettede reverse-reglene.

### To fysiske enheter og pågående nettbruddprøve — 2026-11-05

Eier bekreftet innlogging på nettbrettet, passordendring fra nettbrettet og at både PC og nettbrett viste innlogging etter endringen. Eier bekreftet deretter ny innlogging på begge med det nye passordet. Dette er eierutført fysisk to-enhetskontroll; ingen påstand om automatisk kontra manuell oppdatering på PC siden veiledningen tillot begge.

Eier koblet så fra USB med nettbrettets testside stående åpen, endret passord på PC og rapporterte bekreftet endring/innloggingsskjerm. Etter eiers gjeninnkobling viser ADB autorisert enhet, men reverse-listen var tom. Bare oppgavens15440/18441-regler ble gjenopprettet med --no-rebind og listen kontrollert; lokal frontend200/APIhealthok. Neste prøve er avvisning av den gamle nettbrettøkten ved fornyet serverkontakt. Resultatet er ennå ikke rapportert. Ingen eksplisitt ulagret redigering ble opprettet; denne prøven kvalifiserer derfor ikke håndtering av ulagrede data eller usikkert skriveresultat. USB-loopbackbrudd er ikke full mobilnett-/produksjonsnettprøve. Ingen nettbrettfane eller produksjon ble betjent av agenten.

Nettbruddoppfølging05.11: eier rapporterte innloggingsside etter oppdatering av nettbrettets gamle økt, deretter vellykket innlogging med nyeste passord. Første nettbruddprøve er eierbekreftet innen dette omfanget. Ny prøve med ulagret arbeid: begge innlogget, eier skrev TEST-ULAGRET i Vognløp uten å lagre, trakk USB, endret passord på PC og koblet USB til igjen. ADB autorisert, reverse-regler borte; kun15440/18441 gjenopprettet og verifisert, APIhealthok. Nettbrettsiden er ikke betjent av agenten. Neste steg er ett eksplisitt lagringsforsøk fra gammel økt dersom skjemaet fremdeles vises; forventet avvisning og ingen lagringsbekreftelse. Resultatet og eventuell etterkontroll av lagrede data gjenstår.
