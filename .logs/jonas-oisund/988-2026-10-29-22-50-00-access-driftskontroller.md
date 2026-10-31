# Access-driftskontroller

## 2026-10-29 kl. 22:50 — Jonas Øisund

### Oppgave

Veilede og dokumentere to gjenværende kontroller av eksisterende Cloudflare-fjernaksess: annen faktisk medlemsidentitet mot eksakt e-postregel og ekte signert token replayet etter faktisk utløp. Bevare jonas, data, Access/MFA og eieradgang; ingen deploy, serverflytting eller bred sikkerhetsrevisjon. Commit/push uttrykkelig bestilt.

### Plan

- Lese AGENTS/CLAUDE, sesjonslogg-oppskrift, kvalifikasjonslogg, pilot-/driftsrapporter og faktisk status.
- Guide eieren trinnvis med separat B-profil, laveste medlemsrolle, negativ side/API-prøve og opprydding.
- Forberede skjult lokal DPAPI-lagring, signatur-/tjeneste-/førkontroll, faktisk venting og eksakt-token-replay uten fornyelse/redirects/appcookies.
- Dokumentere sanitert evidens, versjonsgrenser, feilforsøk, opprydding og eierens tunnelvalg.

### Resultat

Arbeid committet i `b6a98e0`: [full rapport](../../docs/evidence/access-operations-20261029.md), Capture/Replay/runner-JSON, konkret ventemetode og gjenbrukbar PowerShell-hjelper. Bare O1/O2-delen av leveranseregisteret og kvalifikasjonstillegget oppdatert; produktkode og V1-/Epic12-status urørt. Git diff --check, sanitiseringskontroll, JSON-parsing, skriptsyntaks/base64url/SHA256/klientkonstruksjon og faktisk før/etter-prøve bestod. Ingen token/cookieverdier, privat svarinnhold eller e-postadresse publisert.

Windows-driftscontainerne var stoppet. Eksisterende Ubuntu-release eb0eee3496d8999fb28615b49d4bf60124b6158f ble identifisert fra live status/current/release-identity og image-tags. Dette kvalifiserer ikke nyere integrert C1/D1–D3-kode. Image-digester/JS-bytebinding er ikke påstått; direkte Docker-lesing/generell sudo var utilgjengelig. Ingen ekstra privilegier ble gitt. Tidlige sandboxlesinger feilet og nødvendige lesekontroller ble gjentatt med verktøyets godkjente eskalering.

B ble Active med bare Minimal Account Access, nektet ved Cloudflare på side/API og fjernet igjen. Eier endret selv teamdomene under en etterspurt avlesing; dette er dokumentert, og medlemsprøven ble gjentatt på endelig bussassistent.cloudflareaccess.com med samme nekt og full opprydding. Første etter-endring-forløp uten observert MFA er beholdt; ny ren gjesteøkt krevde faktisk Authenticator. Eieradgang etter begge fjerninger bestod.

Tokenets signatur/issuer/AUD ble faktisk kontrollert. Førkontroll20:46:31–32UTC ga200/app-shell og401 uten appøkt. Ekte exp21:42:29UTC; samme token sendt21:42:50UTC ga302 til Cloudflare Access på begge mål uten privat respons. Ingen redirectfølging, tokenfornyelse eller klokkeendring. Dette er edge-evidens, ikke separat lokal gate-replay. Hjelpernes linjeskift-/dato-parsingsfeil før replay er rettet og bevart i rapporten. Gjestevinduet ble lukket under ventingen; lagret kopi muliggjorde fortsatt replay.

Token/binding/testmappe er slettet og runner avsluttet, begge kontrollert. B er fjernet. Eier bekreftet etter replay ny2FA og normal jonas-adgang. Tunnelen beholdes aktiv etter uttrykkelig beskjed, for separat Windows-av-prøve. Ingen passord/data/volum-/tjenesteendring utført av denne oppgaven. Dokumentasjon/logg publiseres med normal push; ingen force, tag, release eller kursinnlevering.

### Åpne punkter

- Ingen gjenstående arbeid innen de to bestilte testmålene. Det eksisterende sammensatte issues-punktet og O3–O6 står fortsatt åpne for øvrige Origin/CSRF/cache/timing/WAN/IPv6/DNS/OS-bevisgrenser; de er ikke prøvd eller godkjent utsatt her. Rapporten bevarer begrensningene om lokal gate, versjonsbinding og MFA-matrise.

## 2026-10-31 kl. 04:32 — Jonas Øisund

### Oppgave

Gjennomføre gjenværende O3–O6 så langt mulig uten tilgjengelig eier eller nettbrett. Bevare produksjon og andre arbeidsmiljøer, bruke isolerte syntetiske feiltester, dokumentere funn uten produktrettinger og publisere bare egen oppfølgingsbranch.

### Plan

- Lese AGENTS/CLAUDE/loggoppskrift og eksisterende leveranse-/Access-/Ubuntu-evidens; klone nyeste origin/main til egen branch.
- Avgrense konkrete kontrollmål og versjoner, kjøre HTTP-/DNS-prøver isolert og nett-/OS-kontroller lesende.
- Triagere pakke-/hemmelighetstreff, bevare feilforsøk, verifisere opprydding, dokumentere og publisere uten merge/tag/deploy.

### Resultat

Arbeidet er committet i **1407b4773ea59ec8199f45e470c70881ee6e42a4** på `followup/operations-o3-o6-20261031`, fra main5cee9e03d03d2c9c165c7f8fec64aa3e146959ab. [Full rapport](../../docs/evidence/operations-o3-o6-20261031.md) og verktøy/evidens/status er lagt til. Separat loggcommit følger; begge publiseres til oppfølgingsbranchen. Ingen merge, tag, release eller produktendring. Godkjent refleksjon uendret.

O3: faktisk Nginx-/HTTPS-modusprobe bestått. Alle15 mutasjonsfamilier bestod75 negative Origin/CSRF-kombinasjoner, reelt forbindelsesbrudd før dispatch, tapt klientsvar etter faktisk200/lagring, kvitteringsoppslag og identisk replay uten ekstra effekt.24 ikke-session-tabeller sammenlignet. O4: listener/rute/DNS-observasjon, faktisk AAAA på Cloudflare; ingen origin-skanning. Nft-lesing nektet eksisterende rettighet. O5: faktisk glibc-DNS ga klientretur3,2503s, én fortsatt blokkert arbeider og naturlig frigivelse10,0281s; recovery uten fixturefrigivelse eller restart. Hard kansellering bestod ikke kriteriet.

O6: Trivy0.76.1/DB31.10 mot fire lokale images og730 Ubuntu-pakker avdekket høye/kritiske advisoryoppføringer. Python-appens certifi er oppdatert, mens pip-vendored kopi er gammel. Kernelstikkprøver bekreftet mot Ubuntu; avgrensede NFS/Ceph/RDMA-forutsetninger ikke observert aktive, øvrig triage fortsatt åpen. Store normaliserte pakkeoppføringer er komprimert advisory-JSON, ikke databasebackup. Tolv hemmelighetsmønstre over245 commits/2997tekst-/681binærblobs: fire syntetiske URL-fixturetreff, ingen påvist virkelig hemmelighet.62nye/berørte filer også kontrollert, komprimert advisoryinnhold dekodet; ingen mønstertreff. Skriptsyntaks, lenker, staged evidenshasher og diff --check bestått.

Feilforsøk bevart: manglende loopback-flagg i første HTTP-fixture; readiness-poll med connection-refused før Uvicorn startet; Docker-health-loggrotasjon ga for streng første sammenligning; Ubuntu-parser krevde LF og lsb-release. Disse er ikke produktfeil relabellet som bestått. Alle49opprinnelige containere/22volumer beholdt, kun roterende health-logg utelatt fra eksakt metadata-sammenligning. Samtidig passordarbeid la til4containere/2volumer og oppdaterte egen branch; disse ble også bevart urørt.

Egne testprosesser, nett, credentials og tre metadataimages er ryddet; eget disposable tmp-område med skanner/cache/rårapport er fjernet etter normalisering/hashkontroll. Ingen global prune. Lesende serverkontroll04:28:49Oslo viste fortsatt **d367a0e47198aeecc52358258cb6825eecdc8c4a**, API/DB healthy, tunnelready200/4forbindelser og samme boot-ID. V1-tag/release urørt. Ingen ny brukerinnlogging, private data, produksjonsbackup eller servermutasjon inngikk.

### Åpne punkter

- O3/O4: autentisert ekstern matrise, uavhengig WAN/IPv6 og privilegert brannmur-/ruterevidens er **utsatt – krever eier**; konkret senere tilgang/betjening er spesifisert i rapporten. Ingen spørsmål eller venting på eier i denne økten.
- O5: kjent pre-socket DNS-begrensning er nå reelt gjenskapt; vurder separat kansellerbar resolver-/prosessgrense og kvalifiser ubestemt heng. Ingen produktretting tillatt i denne oppgaven.
- O6: prioriter separat triage/vedlikehold av konkrete kernel-/imagefunn. Full supply-chain/firmware-/binærhemmelighetsgaranti er ikke etablert. Vedlikeholdsvindu/libc6-markør og langtidsstabilitet beholdes åpne i eksisterende punkter.
