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
