# GitHub-release og Ubuntu-deploy av v1.0.0 — 31. oktober 2026

Jonas autoriserte publisering av GitHub-release for eksisterende v1.0.0 og deploy av nøyaktig taggens commit, med backup, etterkontroll og dokumentasjon. Dette er en senere handling enn [V1-sluttkontrollen](v1-final-control-20261031.md), som ikke deployet eller opprettet release. O3–O6 forblir åpne med godkjent driftsoppfølging etter V1. Godkjent refleksjon og applikasjonskode er ikke endret.

## Identitet og publisering

- [GitHub-release v1.0.0](https://github.com/IBE160-2026/G06-oisund/releases/tag/v1.0.0), publisert 31.10.2026 kl.03:20:01 Europe/Oslo (02:20:01Z); verken draft eller prerelease.
- Eksakt commit for release, peeled tag og aktiv server: **`d367a0e47198aeecc52358258cb6825eecdc8c4a`**.
- Annotert tagobjekt: `38bfb0d2f629bc97ea39ca2187285d90f562d608`, uendret fra tidligere publisering. Taggen er ikke flyttet eller erstattet.
- Før arbeidet viste fetch/ls-remote main på samme d367a0e. `gh release view` viste «release not found». Releasen ble deretter opprettet med `gh release create v1.0.0 --verify-tag --target d367a0e47198aeecc52358258cb6825eecdc8c4a --title ... --notes-file ...`, eksplisitt repo `IBE160-2026/G06-oisund`. Beskrivelsen oppgir faktisk innhold, versjonsavgrensede kontroller og åpne O3–O6, uten kursinnleverings-/full sikkerhetsgodkjenning.
- Aktiv `/opt/bussassistent/current` og release-identity.json viser samme commit; `previous` er fortsatt `addd27b14fe4b26ef24d488d847d1c0d59a98946`. Releasearkivets SHA-256 `da833afc216582e4acde127e9d429b3d356e5b145c26c0a7421f123d9f7545e8` matcher en ny `git archive` av tagcommitens backend/frontend/deploy. [Identitetsmetode](v1-release-deploy-20261031/verify_identity.py), [resultat](v1-release-deploy-20261031/identity.json).

Dokumentasjonscommittene etter dette deployes ikke automatisk. De dokumenterer driften av den uendrede V1-taggen; nyere main skal ikke forveksles med aktiv servercommit.

## Førkontroll og backup

Eksisterende driftsverktøy `scripts/server.ps1` og `deploy/ubuntu/bussassistentctl.py` ble lest før bruk. Kontrollklonen var ren ved start; andre branches/worktrees og eksisterende lokale test-/driftsmiljøer ble bevart. Verktøyene er uendret fra tagcommitten. Privat migreringsmappe er Git-identisk mellom forrige aktive addd27b og d367a0e; ingen schemaendring er introdusert. Det var derfor en dokumentert rollback-vei ved behov, men rollback ble ikke nødvendig eller utført.

| Kontroll | Faktisk resultat |
|---|---|
| `server.ps1 -Action Status`, kl.03:20 | Aktiv addd27b; API/DB healthy, tunnel active/running; gateway bare på127.0.0.1:18081. [Output](v1-release-deploy-20261031/before-status.txt). |
| `server.ps1 -Action Check` | Exit0: API healthy; direkte origin uten Cloudflare-assertion avvist403. [Output](v1-release-deploy-20261031/before-check.txt). |
| `server.ps1 -Action Backup` | Exit0: serverdump kontrollert med `pg_restore --list`, overført til eksisterende ACL-beskyttet Windows-backupmappe og SHA256-sammenlignet. [Output](v1-release-deploy-20261031/predeploy-backup.txt). |
| `bussassistentctl verify-restore` | Exit0: separat fersk backup gjenopprettet i unik nettverksløs/tmpfs PostgreSQL-container; alle tabellfingeravtrykk like. Produksjonsvolum ikke montert i testcontaineren; testressursene ryddet av verktøyet. [Output](v1-release-deploy-20261031/predeploy-restore.txt). |

Windows-kopien gjelder `20261031T022031Z-addd27b14fe4b26ef24d488d847d1c0d59a98946.dump`, 114189 byte, SHA-256 **`ba2ee84cba9ef95ad449e2d37d220f9d2b61e12830b081acf3edb0cbbcd4bb07`**. Den ligger privat i `%LOCALAPPDATA%/BussassistentServer/backups`; ny lesende kontroll bekreftet samme hash på server og Windows. Selve dumpen er ikke i Git. Isolert restore brukte den nye serverdumpen med tidspunkt `20261031T022042Z`; dette er ikke feilaktig omtalt som restore av Windows-filens eksakte byte. Eksisterende verktøyers dokumenterte48t-retensjon gjelder; ingen generell backup-/volumopprydding ble kjørt.

## Faktisk deploy og etterkontroll

`pwsh -NoProfile -File scripts/server.ps1 -Action Deploy -Revision d367a0e47198aeecc52358258cb6825eecdc8c4a` kjørte kl.03:21:05–03:21:34, exit0. [Full logg](v1-release-deploy-20261031/deploy.txt), [kommando/tid/exit/hash](v1-release-deploy-20261031/deploy.json). Dette tidsintervallet er hele kommandoen, ikke en målt nedetidsvarighet.

Verktøyet arkiverte bare committede backend/frontend/deploy-filer, overførte og SHA256-kontrollerte arkivet, stage/bygde tre images med fast SHA-tag og installerte eksisterende driftsverktøy. Docker-bygg brukte tilgjengelig cache; ingen påstand om nye uncached regresjonstester. Etter bygg ble tunnel/skriver-tjenester stoppet, ny serverbackup `20261031T022121Z-addd27b…dump` tatt, `previous` bevart og `current` byttet. Compose gjenskapte app-/databasecontainere med det etablerte databasevolumet, ventet på helse og åpnet tunnelen igjen. Ingen produksjonsrestore/reset, ny konto, tilgangs-/ruterendring eller maskinomstart ble utført. Normal oppstartsopprydding/retensjon inngår i appen; det er ikke hevdet at alle produksjonsrader er byte-identiske før/etter deploy.

| Etterkontroll | Resultat og avgrensning |
|---|---|
| `server.ps1 -Action Check` | Exit0; API healthy og origin403 uten assertion. [Output](v1-release-deploy-20261031/after-check.txt). |
| `server.ps1 -Action Status` | Aktiv d367a0e; API/DB healthy; gate/gateway startet; tunnel active/running. [Output](v1-release-deploy-20261031/after-status.txt). |
| Tunnel readiness og systemd | `/ready` ga status200 med4 readyConnections; backup-timer active; ingen failed units;83GB ledig på rotfilsystemet. Boot-ID fortsatt44c550dc-d3b9-4222-8f6c-e0dcdac1a991, samme som tidligere dokumentert. [Output](v1-release-deploy-20261031/after-tunnel.txt). |
| Offentlig uinnlogget GET av app/API | Nettleseridentifisert klient fikk302 til forventet Access-login, no-store og ingen app-shell. Ingen cookies eller redirectfølging. [Resultat](v1-release-deploy-20261031/external-browser-agent.json). |
| GitHub/tag/aktivt arkiv/backup | Alle eksplisitte identitets- og hashkontroller bestod. Dette binder releasearkiv/valgt release, ikke en separat full attestasjon av alle kjørende containerbyte. [Resultat](v1-release-deploy-20261031/identity.json). |

En første HTTP-kontroll med Pythons standard User-Agent avvek fra hjelperens forventede302 og utløste AssertionError. Diagnosen viste403/no-store,17byte og ingen app-shell på begge ruter. Samme uinnloggede prøve med den tidligere brukte `Mozilla/5.0 AccessExpiryVerification/1.0` ga302. Begge observasjoner beholdes;403-prøven omskrives ikke til en bestått redirect. Forskjellen er observert klientavhengig respons, ikke bevist regel-/rotårsaksanalyse eller tegn på en åpen privat API. Ingen rollback eller tilgangsendring ble gjort på dette grunnlaget.

## Personlig eiertest

Jonas svarte **«Alle tre bestod uten feil»** på den konkrete kontrollen av den nye serverversjonen: nytt privat nettleservindu, Cloudflare/appinnlogging, ufarlig testendring i eget valgt utkast, lagring, sideoppdatering og gjenåpning. Dette er eierobservert innlogging/lagring/gjenåpning på **d367a0e**, ikke en automatisk nettlesertest eller utvidelse til den brede O3-matrisen. Eksakt enhet/nettleserversjon og handlingstidspunkter ble ikke målt. Tidligere eiertest på addd27b beholdes separat.

Siste lesende kontroll etter tilbakemeldingen, kl.03:30:52–03:30:55 Oslo, bestod: API healthy/origin403, samme aktive d367a0e, healthy API/DB og aktiv tunnel. [Final Check](v1-release-deploy-20261031/final-check.txt), [Final Status](v1-release-deploy-20261031/final-status.txt). Ingen konkret hindring gjenstår for den bestilte release-/deployoppgaven.

## Fortsatt oppfølging

O3–O6 forblir åpne innenfor [de uttrykkelig godkjente bevisgrensene](../submission/delivery-readiness.md#unperformed-operational-checks--separate-chat). Denne deployen er ikke lukking av ekstern timing/CSRF/cookie-matrise, uavhengig WAN/IPv6, patologisk OS-DNS-kansellering eller full OS/supply-chain/penetrasjonssikkerhet. Langtidsstabilitet og tidligere observert libc6-omstartsmarkør følges opp separat. Ingen kursinnlevering eller endring av godkjent refleksjon inngår.

Rå driftsutdata, kommandoer, UTC-tider, exitkoder og SHA256 ligger i [evidensmappen](v1-release-deploy-20261031/). [Capture-hjelperen](v1-release-deploy-20261031/capture.py) bevarer hver kjøring i egne filer og returnerer faktisk exitkode. Hemmeligheter, cookies, private appdata og backuper følger ikke dokumentasjonscommitten.
