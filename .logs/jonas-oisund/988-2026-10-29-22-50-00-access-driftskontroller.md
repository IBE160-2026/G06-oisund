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
