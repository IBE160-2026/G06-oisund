# Deploy main 12.4 og konsolider fjernaksess

## 2026-10-28 kl. 17:53 — Jonas Øisund

### Oppgave
Deploy nyeste godkjente main med 12.4 og mobilrettingen til eksisterende
app.bussassistent.com, bevar jonas/passord/data og tilgangsvern, la tunnelen kjøre
videre og rydd gammelt tablet-remote-access uten tvang. Bygg, ordinære migreringer,
backup/restorekontroll, oppstart og dokumentasjon/push var uttrykkelig autorisert.

### Plan
- Lese prosjektinstruksjoner, [akseptert integrasjon](../../docs/evidence/12-4-main-integration.md),
  [fjernaksesshistorikk](997-2026-10-27-13-19-30-nettbrett-tokenlagring.md) og faktisk Git-/driftsstatus.
- Backup av nåværende fjernmiljø, isolert restore og registrerte rollback-images før oppdatering.
- Bygge verifisert main, teste med egne syntetiske data og konsolidere avhengigheter til privat operations-mappe.
- Verifisere kilde, bygg, data, Access og tunnel; arkivere og fjerne gammelt worktree;
  oppdatere [driftsveiledningen](../../docs/tablet-production.md), logg/issues og push.

### Resultat
Fersk fetch bekreftet ren main/origin `a48f2132fd0059b21b9581bf27d337cb1561d55b`.
12.4 og c0e809f-mobilrettingen er inkludert. Ingen produktendring eller 12.5.
Dokumentasjon/oppstart er committet i b862ff80d85868d325b6975e8f553dd457d5738b og
pushet til origin/main med bekreftet fjernref. Backend/frontend/deploy/compose-produkt
har null diff fra den deployede main-kilden etter dokumentasjonscommiten.

Backup av eksisterende fjern-DB, konfigurasjon og tunnelcredentials ligger privat i
operations/backups/20261028-pre-a48f213. pg_restore i nettverksløs tmpfs-PostgreSQL
bestod med identiske rader i alle offentlige tabeller. Ingen eldre konto-/datakopi ble
importert. Alle tabellrader og konto/passordhash var uendret etter deploy; jonas finnes.
14 migreringer før/etter, ordinær API-migrering idempotent. Eksisterende datavolum,
DB-image, roller og secrets beholdt. Ingen reset eller sletting av brukerdata.

API-image 26ee88cb518a og gateway-image 50242b65f742 er bygget fra a48f213 med OCI
revision og /private-api i privat frontend. Kjørende API-kilde og frontendfiler
hashkontrollert mot riktig main/isolert testbygg. JavaScript index-DOc41X9S.js,
SHA256 2d4ecd349dfd74f077210bc32d9b5e385c878c007b4111d45252642f09e54602.
Tidligere API a585b56ed625 og gateway 980c6b662cb2 er bevart med rollback-tags og
egen compose.rollback.yaml. Full identitet og kontrollert fremgangsmåte i veiledningen.

Alle fire produksjonstjenester bruker nå privat operations/compose.yaml og stabile
runtimefiler. Ingen aktiv produksjonsmount/compose-arbeidsmappe avhenger av gamle
worktrees. Bare loopback18081 er publisert. Øvrige opprinnelige containere har samme
ID/image/starttid. Portabel tunnel er startet som selvstendig skjult prosess, PID55512,
ready200/fire forbindelser; ingen tjeneste/autostart. Faktisk nedlastet remote ingress
har ett korrekt hostname, loopback18081, Access required, korrekt team/AUD mot lokal
gate og catch-all404. DNS/Access/MFA/cachepolicy er uendret. Tunnelen er bevisst latt kjøre.

71 fokuserte tester bestod:39 (7 faktiske API/PDF/hele flyter og32 kontrollerte
mobilgrenser),18 faktisk API/PostgreSQL for forbedret12.4-import/valgfri korrigering/
godkjenning/busslagring/fokus/gjenoppretting og14 nettverksløse HTTPS-/cookie-/CSRF-tester.
Én eksisterende Starlette-deprecation-advarsel. Det komplette syntetiske A-forløpet
verifiserte faktisk DB/API-restart og bevart lagring. Egne testcontainere/server er
stoppet/fjernet; eget syntetisk testvolum er beholdt uten aktiv container.
15 lokale JWT-nektprøver ga403/no-store, tre offentlige side/API-kall ga302 til Access.
Direkte kjørende API ga401 uten appøkt og403 uten gyldig Origin/CSRF, begge no-store.
Oppstartsskriptet bestod parserkontroll og gjentatt kjøring uten ny connector.

Mislykkede testadapterforsøk er skilt fra produktresultater: sandboxnettverk,
demo.html-fanen som ikke finnes i privatbygget, tmpfs-persistens ved restart,
API-migrering etter nytt syntetisk volum og feil cwd. De ble rettet uten produktendring.
Første kildekontroll brukte feil backendsti. Python-standardklient ble edge-avvist
med403; vanlig klientidentitet ga forventet302. Disse er ikke omtolket til beståtte
produktkjøringer. [Sluttbevis](../../docs/evidence/tablet-production-2026-10-28.json).

Gamle tablet-remote-access hadde16 statusoppføringer/29 filer; alle stier finnes i
main,16 filer identiske etter normalisering. Tilgangskode/test/dokumentasjon er
integrert eller videreutviklet. Hele worktreet, inklusive ignorerte midlertidige
tester/prober/hjul, er privat arkivert med906 bytekontrollerte filer; ukommittert
arbeid er også i lokal navngitt stash. Ignorert tmp er flyttet til backup.
Normal git worktree remove og branch -d fjernet worktree/setup/tablet-remote-access
uten force. Ingen origin-branch fantes. Ingen aktiv katalog ble slettet.

tablet-access-11-6 beholdes med seks ikke-main-integrerte loggcommits, privat historisk
runtime/testuttrekk og frontendavhengigheter; det er ikke lenger nødvendig for aktiv
produksjon. Branchen beholdes. Eksisterende detached12.3/12.4-testworktrees og øvrige
miljøer er bevart. Hemmeligheter, credentials, databaser og private tabellfingeravtrykk
er ikke lagt i Git eller logger. Synkede sources er urørt.

### Åpne punkter ved første overlevering
- Eierens nye innloggede kontroll på det offentlige bygget fra Pixel/Lenovo gjenstår:
  Access/MFA, jonas med eksisterende passord, native filvelger, import, valgfri korrigering,
  godkjenning og busslagring. Eksisterende Story12.4-aksept endres ikke. Automatisert
  teknisk deployverifikasjon er fullført; ingen ny fysisk eller autentisert edge-prøve
  påstås. Det eksisterende fjernaksesspunktet i issues.md er oppdatert med dette skillet.

### Oppfølging samme dag: brukerbekreftet mobilkontroll

Jonas rapporterte: «Kontrollert på mobil, det funker, versjonen er den som ble endret til i 12.4.»
Driftsrapport og maskinlesbar evidens er oppdatert med den faktiske brukerbekreftelsen.
Det eksisterende åpne punktet om praktisk kontroll etter deploy er lukket.
Bekreftelsen utvides ikke til en detaljert scenarioprotokoll, bestemt enhetsmodell
eller en separat ny MFA-/JWT-prøve. Ingen drift, data eller kode er endret i oppfølgingen.

### Åpne punkter etter mobilkontrollen
Ingen nye for denne deployen. Tidligere separate sikkerhetsbevisgrenser beholdes.
