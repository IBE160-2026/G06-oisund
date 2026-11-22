# Nettleserrettinger for Bussassistent V2

## 2026-11-22 kl. 14:31 — Jonas Øisund

### Oppgave

Rett dokumenterte Firefox- og WebKit-avvik i V2. Overlever testet kode og eksakte noder til testchatten for selvstendig omprøving.

### Plan

- Kontroller Git-grunnlaget mot `5ddcb67` og bruk en egen lokal arbeidskopi. Avstem den [opprinnelige V2-testloggen](983-2026-11-20-22-25-31-sluttprover-v2.md), Firefox-proben, IBE160-rapportene under TIDE-cachen og den nodevise gjennomgangen i testchatten.
- Gjenskap de prioriterte symptomene med et isolert bygg og syntetiske kontoer. Kjør de 34 opprinnelige Firefox-nodene på sluttbygget og egne kontroller for WebKit, tidsvalg, fokus og informasjonskapsler.

### Resultat

- Den rene lokale V2-branchen `codex/integrate-bussassistent-v2` pekte på `b8b907fcc2c149693146b5cdcd10d5cd3cb0ca51`. Hele diffen fra `5ddcb674ced4700cd6177598ff3c325506637155` bestod av logger og dokumentasjon. Det lesende origin-oppslaget fant ingen publisert V2-peker. Rettingene ligger på `codex/fix-v2-browser-deviations` i den separate lokale klonen `ibe160-v2-browser-fixes`.
- `4478e939693ee5bf711b8683dcf597d552a8494a` rettet tid og fokus i utkast. `PrivateTimeInput.tsx` beholder valgt Oslo-forekomst når nettleseren legger til nullsekunder på samme kalenderdato. Reelle endringer i klokke eller dato krever et nytt oppslag, og ikke-null sekunder bevares gjennom lagring og gjenåpning. `PrivateDrafts.tsx` gjenoppretter fokus etter at redigeringskontrollene igjen er aktive. `style.css` gir den programmatisk fokuserte telleren etter siste utkastside synlig omriss i dag- og nattvisning.
- `private-drafts.spec.ts` aksepterer valgfritt `:00` for minuttverdier og krever fortsatt samme lokale dato, tid og UTC-offset. NUL-proben viste at Playwrights Firefox-innsetting fjernet tegnet. Testen leverer nå NUL via DOM-feltet og krever fortsatt sperret lagring, bevart verdi og tilgjengelig feilmelding. Begge tastaturprøvene venter på at tidene er klare før de setter fokus og krever fokusretur etter lagring.
- `f46bde0f9e24e2473e5a7d384e7ceeed919f879b` rettet begge passordavslagene i `PasswordChange.tsx`. Grunnlagsproben viste ved avslag for gjeldende passord at ramme-callbacken forsøkte fokus mens feltet var deaktivert, og at feltet ble aktivt senere. Skjemaet venter nå på at feltet er aktivt før det setter fokus.
- `f9c2856632587c404b69dc71b7909168ac79d5ce` rettet PDF-feilmeldingen i `PrivateAccess.tsx`. WebKit kan gi `DOMException` med navnet `SyntaxError` når HTTP 200 har ugyldig JSON. Klassifiseringen bruker nå feilnavnet. Transportbrudd og tidsavbrudd beholder egne meldinger. `tablet-transport.spec.ts` kontrollerer at ulagret arbeid beholdes gjennom alle tre feiltypene.
- Testet commit `069e15302679a50c0c4eaaa0dff7f5fb47f0ea62` knytter cookiekravet i `private-access.spec.ts` til den faktiske HTTP-headeren. Begge bredder bekreftet `SameSite=Strict`, `HttpOnly`, innlogging, gjenåpning og utlogging i Firefox og WebKit.
- Lokale TypeScript/Vite-bygg bestod. Firefox 157.0 bestod 36 av 36, som omfatter de 34 opprinnelige feilnodene og to tidskontroller. Det separate utvalget for tastatur, tid og cookie bestod 12 av 12 i Firefox 157.0 og WebKit 27.2. PDF-utvalget bestod 20 av 20 kjøringer i de to motorene, inkludert faktisk HTTP 200 med ugyldig JSON, nettverksbrudd, tidsavbrudd og avbrutt filvalg.
- Testene brukte Compose-prosjekt `ibe160-v2-browser-fix-20261122`, egen PostgreSQL-database og loopback-portene 19871, 19873 og 19875. De 45 sporede Python-kildefilene i test-API-et samsvarte med V2. Etter nedtaking var alle tre porter frie. Åtte eksisterende containere beholdt ID og oppstartstid.

**Omprøving per dokumentert Firefox-node**

Alle radene gjelder prosjektet `[firefox]`. Filnavn og testtittel identifiserer radene med samme linje. Årsaken til hvert tidligere tidsutløp uten registrert stoppunkt kan fortsatt ikke fastslås fra den opprinnelige rapporten.

| Node ved `b8b907f` | Test | Første observerte avvik | Sluttbygget |
| --- | --- | --- | --- |
| `tests/password-change.spec.ts:101:1` | typed rejection clears secrets and cancel returns focus | Gjeldende passord fikk ikke fokus etter avslag. | Bestått ved `101:1` |
| `tests/password-change.spec.ts:113:1` | unchanged password is rejected on the new password field without logout | Nytt passord fikk ikke fokus etter avslag. | Bestått ved `113:1` |
| `tests/private-drafts.spec.ts:39:1` | review fixes uncertainty preserves character-by-character multiword input save and reopen | Lagre var sperret etter at valgt Oslo-forekomst falt bort ved fokusbytte. | Bestått ved `39:1` |
| `tests/private-drafts.spec.ts:55:1` | draft bus fresh writes share Unicode rules and invalid input remains editable | Lagre var aktiv ved testens andre ugyldige verdi. Firefox-proben viste at testdriveren hadde fjernet NUL. | Bestått ved `55:1` |
| `tests/private-drafts.spec.ts:77:1` | all 201 saved drafts remain reachable and the final page reopens | Listen flyttet fokus til statusen, men statusen manglet synlig omriss. | Bestått ved `86:1` |
| `tests/private-drafts.spec.ts:166:1` | manual unknowns and unresolved time input follow activity identity through reorder and discard | Tidsutløp uten registrert første steg. | Bestått ved `175:1` |
| `tests/private-drafts.spec.ts:185:34` | keyboard save and reopen midnight facts at 768px | Status forble ulagret. Første rettingsrunde nådde lagring og avdekket manglende fokusretur. | Bestått ved `194:34` |
| `tests/private-drafts.spec.ts:185:34` | keyboard save and reopen midnight facts at 1440px | Status forble ulagret ved tastaturlagring. | Bestått ved `194:34` |
| `tests/private-drafts.spec.ts:215:1` | lost acknowledgement, authorized lookup and HTML failure retain original operation | Tidsutløp uten registrert første steg. | Bestått ved `228:1` |
| `tests/private-drafts.spec.ts:270:1` | stale revision preserves local input and offers saved comparison | Tidsutløp uten registrert første steg. | Bestått ved `283:1` |
| `tests/private-drafts.spec.ts:291:1` | JSON with an invalid acknowledgement stays unresolved until authorized lookup | Første lagreknapp var sperret. | Bestått ved `304:1` |
| `tests/private-drafts.spec.ts:318:1` | 413 keeps fields editable and a corrected draft can be saved | Lagre var sperret før 413-svaret. | Bestått ved `331:1` |
| `tests/private-drafts.spec.ts:350:1` | slightly future server creation timestamps remain valid acknowledgements | Ingen POST før tidsutløp. Lagre var sperret. | Bestått ved `363:1` |
| `tests/private-drafts.spec.ts:363:1` | supported historical Oslo offset saves and reopens unchanged | Status forble ulagret etter endring til historiske datoer. | Bestått ved `376:1` |
| `tests/private-drafts.spec.ts:377:1` | reorder and remove preserve ordered identities with their facts after reopen | Ingen POST før tidsutløp. Lagre var sperret. | Bestått ved `390:1` |
| `tests/private-drafts.spec.ts:406:1` | bus, derived suffix, clear and confirmed reset preserve the intended facts | Lagre var sperret etter ny utfylling etter tilbakestilling. | Bestått ved `419:1` |
| `tests/private-drafts.spec.ts:443:1` | confirmed deletion retains its identity through a committed lost reply | Første lagring var sperret. Sletting ble ikke nådd. | Bestått ved `456:1` |
| `tests/private-drafts.spec.ts:478:40` | deletion lookup settles only an accepted deletion (false) | Første lagreknapp var sperret. | Bestått ved `491:40` |
| `tests/private-drafts.spec.ts:478:40` | deletion lookup settles only an accepted deletion (true) | Første lagreknapp var sperret. | Bestått ved `491:40` |
| `tests/private-drafts.spec.ts:495:1` | a delayed earlier list cannot replace the post-save revision list | Lagre var sperret før testen av forsinket liste. | Bestått ved `508:1` |
| `tests/private-drafts.spec.ts:523:117` | malformed summary remains recoverable (null) | Lagre var sperret i gjenopprettingssteget. | Bestått ved `536:117` |
| `tests/private-drafts.spec.ts:523:117` | malformed summary remains recoverable (invalid) | Lagre var sperret i gjenopprettingssteget. | Bestått ved `536:117` |
| `tests/private-drafts.spec.ts:536:1` | expired deletion is unconfirmed and releases the form for a new draft | Ingen POST før tidsutløp. Lagre var sperret. | Bestått ved `549:1` |
| `tests/private-drafts.spec.ts:556:1` | backend-valid emoji text uses code-point limits through entry, save and reopen | Lagre var sperret etter gyldig emoji-inndata. | Bestått ved `569:1` |
| `tests/private-drafts.spec.ts:571:1` | stale deletion releases its lock and requires confirmed saved-version replacement | Første lagreknapp var sperret. | Bestått ved `584:1` |
| `tests/private-drafts.spec.ts:603:3` | friendly Oslo time entry › service defaults and explicit next day preserve entered dates when service date changes | Samme Oslo-tid ble lagret med eksplisitte nullsekunder. | Bestått ved `616:3` |
| `tests/private-drafts.spec.ts:628:3` | friendly Oslo time entry › incomplete and spring-gap input survives while both autumn occurrences require a choice | Vårgapets klokke ble vist med eksplisitte nullsekunder. | Bestått ved `642:3` |
| `tests/private-drafts.spec.ts:665:3` | friendly Oslo time entry › unavailable and stale resolution retains input and saves only the latest clock | Ingen POST etter ny prøving med forsinket tidsoppslag. | Bestått ved `679:3` |
| `tests/private-drafts.spec.ts:712:3` | friendly Oslo time entry › clearing saved, incomplete and gap times saves null without changing other facts | Ingen POST før tidsutløp. Lagre var sperret. | Bestått ved `757:3` |
| `tests/private-drafts.spec.ts:744:37` | terminal lost-save lookup releases only an explicitly empty recovery (false) | Lagre var sperret før oppslag av uavklart forsøk. | Bestått ved `789:37` |
| `tests/private-drafts.spec.ts:744:37` | terminal lost-save lookup releases only an explicitly empty recovery (true) | Lagre var sperret før oppslag av uavklart forsøk. | Bestått ved `789:37` |
| `tests/private-drafts.spec.ts:776:1` | feedback invalid draft bus disables save and explicit clear preserves cancel and reopen | Lagre var fortsatt sperret etter retting til 100 kodepunkter. | Bestått ved `821:1` |
| `tests/private-drafts.spec.ts:797:1` | negative intervals are explained before sending and generic validation uses friendly time guidance | Status forble ulagret fremfor å forklare negativt intervall. | Bestått ved `842:1` |
| `tests/private-drafts.spec.ts:818:1` | activity removal cancellation preserves unresolved raw input and canonical facts | Første lagring var sperret. Fjerning av aktivitet ble ikke nådd. | Bestått ved `863:1` |

### Åpne punkter

- Samordningschatten omprøver tabellens 34 Firefox-noder på `069e15302679a50c0c4eaaa0dff7f5fb47f0ea62`, med tidsvalg, begge passordavslag og tastaturlagring først. Bruk en egen kopi av denne commiten som byggegrunnlag og eget syntetisk miljø.
- Omprøv `PDF invalid-json is distinct from parser rejection` i WebKit med faktisk HTTP 200 og ugyldig JSON. Kjør kontrollene for transportbrudd og tidsavbrudd samt `keyboard login, ownership presentation and logout` ved 768 og 1440 px.
- De to navngitte laptopfilene var utilgjengelige i de lokale kildene. Testchattens 34 nodeobservasjoner og resultatrapportene på D: ga nodegrunnlaget. Ny samlet status for de opprinnelige 121 nettlesernodene og 64 nettbrettnodene følger separat samordnet kjøring.

## 2026-11-22 kl. 15:02 — Jonas Øisund

### Oppgave

Klassifiser det sporadiske bussavviket i den uavhengige Firefox-omprøvingen av `069e15302679a50c0c4eaaa0dff7f5fb47f0ea62`. Rett det ved påvist produktfeil og bevar første akseptkjøring.

### Plan

- Les det opprinnelige Playwright-sporet og sammenhold DOM-verdien før og etter utfylling med forespørsel og svar på revisjon 3.
- Gjenskap fokusrekkefølgen i eget syntetisk miljø. Sammenlign samme regresjon på tidligere og rettet kode.

### Resultat

- Det opprinnelige sporet beholdt SHA-256 `D18D57B45E68D6D87EEE75A647EFE445C14493C274939BE1214BF9ED67D66F16`. Aktivitetsbildene ved handling `roum@688` viser bussfeltet deaktivert før utfylling og aktivt med uendret U+FEFF etterpå. Lagringsstatusen viste fortsatt versjon 2. Tredje POST sendte U+FEFF, og HTTP 200 med versjon 3 bekreftet samme verdi.
- Klassifisering er en produktfeil i fokusrekkefølgen ved opplåsing. To uavhengige Firefox-prober på tidligere kode registrerte rekkefølgen lagreknapp → opplåsing → bussfelt → lagreknapp. Den sene fokusreturen kunne avbryte neste utfylling. Det tidligere NUL-funnet gjaldt testdriverens innsetting.
- I `b97f63421b059442a373ec0b8331216d4ddd2d1b` flytter `PrivateDrafts.tsx` fokusreturen til samme DOM-oppdatering som låser opp redigeringen. Et felt som allerede har fått nytt fokus beholder det. `private-drafts.spec.ts` kontrollerer før hver lagring at den nye bussverdien står i feltet, krever eksakt revisjon og prøver neste tastaturinndata rett etter opplåsing.
- Den nye regresjonen feilet på tidligere kode ved forventet fokus. Etter rettingen bestod TypeScript/Vite, 12 av 12 kjøringer i Firefox 157.0 og WebKit 27.2 samt 6 av 6 ekstra kjøringer av buss- og fokusnodene i Firefox. Min teststakk og syntetiske database ble fjernet etterpå. De ti eksisterende containerne beholdt ID og oppstartstid.

### Åpne punkter

- Samordningschatten omprøver `b97f63421b059442a373ec0b8331216d4ddd2d1b` i eget miljø. I `tests/private-drafts.spec.ts` gjelder det :55 (Unicode-bussverdi), :91 (fokus ved opplåsing), :237 (tastaturlagring ved begge bredder), :271 (tapt kvittering med oppslag) og :347 (ugyldig kvittering med oppslag). Gjenta :55 og :91 i Firefox.
