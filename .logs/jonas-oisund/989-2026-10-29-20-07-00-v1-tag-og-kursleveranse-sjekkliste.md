# V1-tag og kursleveranse – sjekkliste

## 2026-10-29 kl. 20:07 — Jonas Øisund

### Oppgave

Lag konkret sjekkliste før V1 kan tagges og leveres til kurset, basert på faktisk avslutningsgrunnlag. Ikke opprett tag/release eller lever noe; serverbonusen er utenfor.

### Plan

- Les [avslutningsrapport](../../docs/evidence/v1-main-integration-20261029.md), [leveranseindeks](../../docs/submission/README.md), README/oppskrift, [refleksjon](../../docs/submission/ai-reflection.md), kurskildenes addendum og tidligere V1-logg990/issues.
- Skill fullført produktaksept fra dokumentasjonsarbeid, versjonsfrysing og faktisk kurslogistikk. Bevar historikk og drift; ingen nye tester uten behov.

### Resultat

D1–D3, eieraksept og Epic12/lokal V1 er fullført. Ved lesekontrollen var lokal main og origin/main begge97193836ec8528f873cdef95e8c3b2e59852973a; ren arbeidskopi. Godkjent produkt/test/verktøy er C1/3c2287e, mens senere main også har endelig evidens og dokumentasjon. C067fdb er historikk. Dette arbeidet har ikke kontrollert ny fjernstatus eller opprinnelige lærerfiler/LMS og har ikke kjørt tester på nytt.

Konkret sjekkliste, i anbefalt rekkefølge:

- [ ] **Bekreft de faktiske kurskravene:** gjeldende frist, innleveringssted, tillatt/påkrevd format, eventuelle rapport-/refleksjons-/demo-/videokrav og dokumentert godkjenning av prosjektforslag/individuell leveranse. Repoets [kurskilderegister](../../_bmad-output/planning-artifacts/briefs/brief-IBE160-2026-09-21/addendum.md#course-evidence-and-delivery-constraints) er en sekundær oppsummering; originalfilene mangler, og fristen var motstridende. Ikke fastsett en dato eller et nytt vedleggskrav ut fra dette alene.
- [ ] **Ferdigstill leveransedokumentasjonen for endelig versjon:** Jonas gjennomgår refleksjonens egen stemme og dekning mot faktisk oppgave. Legg til en avgrenset sluttoppdatering om D1–D3, menneskelig aksept kontra automatiske tester, testhjelper-/dialog-/Git-bytefeil og læring der det er relevant. Eksisterende refleksjon er hovedsakelig gjennom12.5; den er et grunnlag, ikke bekreftet oppfyllelse av en utilgjengelig kursrubrikk. Bevar historiske resultater.
- [ ] **Samordne README og leveransesnapshot:** anbefalt tagmål er en endelig main-commit med både godkjent C1-produkt og endelig dokumentasjon/evidens. Ikke velg3c2287e alene som komplett leveranse uten vurdering: den commitens egen README peker fortsatt på historiskc067fdb, og den inneholder ikke den senere sluttevidensen. Nåværende README sender også leseren tilbake tilC1 og forklarer denne forskjellen. Gjør instruksjonen selvstendig på den valgte leveranseversjonen, slik at vurderer beholder korrekt kilde og tilgang til aktuell dokumentasjon.
- [ ] **Kontroller det nøyaktige leveranseinnholdet:** README, kilde/lockfiler/migrasjoner, syntetiske A–E-filer/fasit, kravsporbarhet, test/eieraksept, begrensninger og refleksjon må finnes i den frosne versjonen. Bare versjonert innhold leveres; ingen .private-runtime, ekte PDF-er, databaser/dumper/backuper, tokens/passord, node_modules eller lokale worktree-filer. Kontroller vurderers faktiske Git-tilgang. ZIP/PDF/video lages bare dersom de faktiske kurskravene krever det; repoets oppskrift krever ikke ZIP.
- [ ] **Ta en avgrenset sluttkontroll av leveranseoppskriften:** kontroller rene Git-referanser, at produktet fortsatt er identisk med godkjentC1, og at README-kommandoene treffer tiltenkt versjon/prosjekt og genererer egen syntetisk innlogging. Ved endrede kommandoer/innpakking, prøv nettopp den endrede veien isolert. Gjenbruk gyldig22/22 Lenovo,3/3 fersk reproduksjon og31/31 integrasjon; ingen automatisk bred omkjøring eller ny personlig produktaksept ved rene dokumentendringer.
- [ ] **Beslutt tag og publisering senere:** velg eksakt commit og navn (forslagv1.0.0, ikke vedtatt), kontroller navnekollisjon lokalt/origin, og få uttrykkelig instruksjon om faktisk opprettelse/push. En GitHub-release er en egen valgfri handling med mindre kurset krever den. Taggen skal ikke følge bevegelig main eller inkludere serverbonus/utvidelser.
- [ ] **Lever senere og kontroller kvitteringen:** lever akkurat godkjent lenke/tag/commit og påkrevde vedlegg gjennom riktig kanal; kontroller tilgang/nedlasting og lagre innleveringskvittering. Dette krever egen bestilling og er ikke utført av sjekklisten.

Serveroppsett, produksjonsdeploy, eksternt Access-token-/medlems-/WAN-/IPv6-/OS-bevis og utvidelser er ikke nye tag-/kursforutsetninger for den aksepterte lokale V1. De uutførte driftskontrollene er fortsatt uutført, ikke godkjente utsettelser. Ingen ny produktblokkering er funnet. Ingen tag/release, push, innlevering, produktendring, testomkjøring eller driftsoperasjon er utført; bare denne lokale logg-/issuescommitten opprettes etter prosjektregelen.

### Åpne punkter

- Bekreft gjeldende originale kurskrav, frist, prosjekt-/solo-godkjenning og vurderers innleverings-/tilgangsordning.
- Ferdigstill eiergjennomgått sluttdokumentasjon/refleksjon og selvstendig README for nøyaktig leveransesnapshot; kontroller innhold og bare nødvendig oppskriftsvei før eventuell tag/innlevering.
