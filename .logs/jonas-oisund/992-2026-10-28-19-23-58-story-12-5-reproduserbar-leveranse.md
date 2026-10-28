# Story 12.5 – reproduserbar leveranse

## 2026-10-28 kl. 19:23 — Jonas Øisund

### Oppgave

Gjennomfør Story 12.5 / V1-20 på egen branch og i eget worktree fra faktisk nyeste origin/main, frem til reviewklar leveranse. En leser skal kunne følge README fra rent versjonert innhold og demonstrere faktisk API/PostgreSQL uten eierens private dokumenter, kontoer, tunnel, betalte tjenester eller sanntidskilder. Bevar eksisterende drift; commit og push leveransen og sesjonsloggen uten merge, deploy, kursinnlevering eller automatisk eieraksept.

### Plan

- Les AGENTS/CLAUDE og sesjonslogg-oppskriften, autoritativ story, planleggingskopi, PRD/arkitektur/UX, 12.4-overlevering og gjeldende driftsdokumentasjon. Bruk `bmad-build`; selvstendig ferdigføring til review er uttrykkelig autorisert.
- Følg [implementeringsstoryen](../../_bmad-output/implementation-artifacts/spec-12-5-reproducible-submission.md), med FR-25/NFR-4/AC-11/12/SCOPE-02 og de beskyttede driftsgrensene.
- Lag isolerte leveransekommandoer, rydd hoved-README og samle kravsporbarhet, fiktive forventninger, KI-refleksjon, bevis og begrensninger.
- Utfør oppskriften i en ny Git-kopi med nye avhengigheter, porter og volumer; bevar faktiske feil, rett og gjenta berørte steg.
- Utfør tre uavhengige review-linser, rett beholdte funn, gjenta nødvendige kontroller, kontroller filutvalg og publiser bare 12.5-branchen. Logg og issues får egen path-begrenset commit.

### Resultat

Fersk fetch viste origin/main `99c272b09abaa5ffecf3286b406fbf065a445c7c`, nyere enn brukerens sist observerte `4c8eb80`. Ingen eksisterende 12.5-branch/worktree ble funnet. Branch `story/12-5-reproducible-submission`, worktree `D:/IBE160/tmp/story-12-5`. Opprinnelig main er fortsatt ren på samme HEAD. Ingen produktfiler, migreringer eller låste avhengigheter ble endret fra denne baselinen.

README er erstattet med én sammenhengende oppskrift. [Leveranseinngangen](../../docs/submission/README.md) samler kort produktbrief, lærerkravenes dokumenterte kildegrunnlag, syntetiske A–E-PDF-er/uavhengig fasit, samtlige gjeldende FR/NFR/AC-disposisjoner med konkrete testlenker, faktisk KI-/menneskerefleksjon og begrensninger. Historiske statusresultater beholdes i rapportene. De fem planlagte utvidelsene er uttrykkelig utenfor V1. De opprinnelige undervisningsfilene mangler i repoet; gjennomgangen bruker det versjonerte kilde-/kravnotatet og hevder ingen ny kontroll av manglende originalfiler.

`compose.submission.yaml` og `scripts/submission.mjs` oppretter fem isolerte tjenester med genererte, ignorerte hemmeligheter og syntetisk konto. Prosjekt `ibe160-submission`; frontend15325, fiktiv API18327, privat API18328; databaseporter ikke publisert. Kontoens passord genereres lokalt. Migrering001–014 og fiktiv seed er idempotente. Start/omstart bruker installerte images uten bygg/nedlasting. Vernet mot ordinære kontoer og CLI-ens reserverte syntetiske navnerom er bevart.

Ren reproduksjon: `git clone --no-local` av bare committet Git-innhold til `D:/IBE160/tmp/submission-clean-20261028`; Git-ren, uten node_modules/dist/.private-runtime og uten eksisterende demovolumer. Ferske låste npm-/Python-installasjoner og Chromium-nedlasting ble gjennomført. To nye demomiljøer med mislykket oppstart ble identitetskontrollert og erstattet med nye demovolumer/hemmeligheter før full ny initialisering; eksisterende miljøer ble ikke brukt eller berørt.

Faktiske resultater og eksakte kildeversjoner er i [reproduksjonsrapporten](../../docs/evidence/12-5-reproduction.md):

- Korrigert bred backendkommando:367 private backendtilfeller bestod i594,03s,19 faktiske fiktive HTTP/PostgreSQL-tilfeller og94 parsertilfeller bestod i8,25s samlet. Null hoppet over. Ett eksisterende Starlette TestClient-deprecation-varsel.
- Tre nye faktiske Chromium-flyter bestod i50,4s: A/C med uavhengige kildefakta, korrigering/lagring/godkjenning, buss, avvik, eksplisitt bruk, slutt/avbrudd, gjenåpning og A-omstart; B direkte lagring til separat godkjenning. Samme tre tilfeller bestod igjen etter review i73,825s; dette er gjentakelse, ikke seks unike flyter. Ingen API-mocks; bare lokale forespørselsorigins. A/C-oppsummeringene er visuelt kontrollert og versjonert med syntetiske data.
- Første Node-kontroller3/3 og Python-wrapperkontroller3/3 bestod. Etter review bestod seks Node-grupper på både Windows og nettverksløs Linux. Det er ikke en full Linux-reproduksjon.
- Seks nye faktiske databasekontroller inngår i backendkjøringen og bestod separat igjen i9,34s: uendret init/frist, fire feil målinnstillinger og avvist ordinær konto med uendrede rader.
- Utvidet runtimekontroll bestod fem registrerte prøver: hel Node-reset avviser midlertidig ordinær konto uten at noen av databasene endres; faktisk HTTP befolker plan/buss/valg/start/status/avvik/avslutning/kvitteringer; alle rader/frister i25 private og to fiktive tabeller er identiske etter stopp/start og omstart; positiv reset rydder bare demodata, bevarer hemmeligheter/migreringer/sikkerhetsinnstilling og reseeder;30 andre containere og14 andre volumer/mountrelasjoner er uendret.
- Filkontroll fant ingen av seks genererte hemmelighetsverdier i filutvalget, ingen sporede private runtime-filer eller nye arkiver. Manglende audit-grunnlag avvises i to negative kontroller uten å erstatte tidligere rapport.333 lokale lenker er kontrollert; rå konsoll-whitespace beholdes med et snevert attributtunntak bare for evidensutskriftene.

Opprinnelige feil er bevart: Vite-preview manglet skriverettighet til sin midlertidige konfigurasjonsmappe; fiktive CLI-kall arvet ikke serverens database-URL; første brede private testkommando kjørte14 fiktive tester mot feil API (14 feil/466 bestått, samlet exit1). Alle ble rettet innen leveranse-scope, og berørte steg ble gjentatt. Tidligere kjøringer er ikke omdøpt til nye eller summert inn i oppblåste totaler.

Tre uavhengige review-linser ga13 individuelle funnrader. Beholdte funn er rettet og lukket ved målrettet reinspeksjon av de opprinnelige reviewerene. To lave funn er forkastet med dokumenterte bruksgrenser: ingen samtidig førsteinitialisering i flere utsjekk og ingen kopiering av runtime-hemmeligheter til andre utsjekk for å koble gamle volumer. Ingen produktkontrakt ble endret.

Gjeldende [README](../../README.md) låser reproduksjonen til `c067fdbb20150219c041588ed4e990e7b0ef6b94`, som inneholder kilde og utført evidens. Testkopien har faktisk utført denne detach-kommandoen, er Git-ren og har fem friske tjenester på http://127.0.0.1:15325/private. Bruk bare dens lokale `.private-runtime/submission/account.json` for innlogging. Behold denne mappen med volumene. Kilde-/evidenssnapshot `c067fdb`, reviewrettinger `8d50684`, pin-dokumentasjon `5cea76e` og avsluttende reviewbevis `d40d7f02f015865b621043c564303fb67bb19136` er committet. 12.5-branchen er pushet, og remote HEAD er kontrollert lik `d40d7f02f015865b621043c564303fb67bb19136` før den separate loggcommiten.

Alle30 opprinnelige container-ID-er/images/starttider/tilstander er kontrollert uendret også etter siste omkjøring. Ingen operasjon mot jonas eller eksisterende databaser, passord, tunnel eller produksjon. Ingen merge/deploy/kursinnlevering, eieraksept, Epic12-avslutning eller utvidelsesstart. Sprint/spec står review/in-review, aksept pending. Tidligere åpne prosjektpunkter beholdes. Full Linux-oppskrift, ny fysisk enhetsprøve, naturlig sju-døgnsvarighet og nytte i faktisk bussdrift er ikke påstått.

Guidet sluttvurdering 2026-10-28 kl. 20:17: Jonas bekreftet «Det ser klart ut. Steg 1 OK» etter gjennomgang av README/oppstarts-, nettbehovs- og resetbeskrivelsen. Dokumentasjonsdelen er dermed manuelt bestått. Dette er ikke en ny installasjonskjøring eller samlet Story12.5-aksept.

Guidet sluttvurdering 2026-10-28 kl. 20:22: Jonas bekreftet «steg 2 ok». Innlogging i det isolerte demomiljøet og import av syntetisk Testskift-A.pdf med forventet dato, vognløp, ukjent fysisk buss og de to viderevalgene er manuelt bestått. Ingen lagring/godkjenning eller samlet aksept er utledet fra denne bekreftelsen. Neste prøve er manuell korrigering, eksplisitt lagring og gjenåpning.

### Åpne punkter

- Jonas sin sluttvurdering av leveranseoppskriften og uttrykkelige Story12.5-aksept gjenstår; bruk [konkret review-sjekkliste](../../docs/submission/review-checklist.md). Teknisk grønt eller push gir ikke aksept og avslutter ikke Epic12.
