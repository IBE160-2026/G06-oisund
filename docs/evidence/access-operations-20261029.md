# To avgrensede Access-driftskontroller – 29. oktober 2026

Begge bestilte mål er bestått på eksisterende Ubuntu-drift: annet aktivt medlem avvist av eksplisitt e-postpolicy, og replay av samme ekte signerte token avvist etter faktisk utløp. Lokal V1/Epic 12 er fortsatt avsluttet. Ingen deploy, serverflytting eller generell sikkerhetsrevisjon ble utført i denne oppgaven.

## Testmål og faktisk versjon

Mål: `https://app.bussassistent.com/private` og `/private-api/drafts`. Lesende SSH-status før/etter prøvene viser release **`eb0eee3496d8999fb28615b49d4bf60124b6158f`**, valgt av `/opt/bussassistent/current`, med API `bussassistent-api:<release>`, frontend/proxy `bussassistent-gateway:<release>` og gate `bussassistent-access-gate:<release>`. API/database healthy, tunnel active/running, eneste publiserte appport `127.0.0.1:18081`. Databasevolumet er det eksisterende `bussassistent_private_pg`.

Serverens release-identity.json oppgir samme commit og arkiv-SHA256 `174063ffe73560594368b87094619077b6b4cb48519c820a4f52efb0523aacfc`. Lesbar release-gate har SHA256 `f2ae5aacf44192025ecc43a3978d1c08917d3de37d2c0e10752c14e3bb6367d9`; release-Compose `e7ba4ba080d98617f07be3d94ec48cac9b70f041b99975e04dc80f632784bf92`. Faktiske image-digester og separat JS-asset-identitet ble ikke innhentet: direkte Docker-inspeksjon som SSH-bruker ble nektet, og generell sudo var ikke tilgjengelig. Dette er release-/image-tag-identifikasjon fra driftsverktøyet, ikke en full byte-attestasjon av containerne. Førkontrollen har SHA256 av faktisk levert HTML i JSON-evidensen.

De eldre Windows-driftscontainerne var stoppet; ingen lokal cloudflared kjørte. Historisk `main-a48f213` er derfor ikke dette testmålet. Ubuntu var allerede satt opp av annet arbeid. D1–D3 i nyere main ble ikke deployet her, og disse resultatene kvalifiserer **ikke** nyere C1/main-produkt eller nye lokale gate-rettinger. Driftsveiledningen tablet-production.md beskriver historisk Windows-drift; faktisk nåtilstand ble lest separat. Parallelle omstarter/krasj-/nettverkstester ble først rapportert pågående; eier bekreftet stabil drift før tokeninnsamling. Nedetid er ikke brukt som avvisningsbevis.

## Konfigurasjon og brukerutført endring

Eier bekreftet én Allow-policy med bare eierens eksakte e-post, Cloudflare IdP og Restrict to account members på. Testidentiteten omtales bare som **B**. App-AUD er `11605406740b9e66f584e9bfc11d3db52f18585de0708c6d5b2741d0268fbbfa`.

Første nekt-skjermbilde viste `restless-dream-ed17.cloudflareaccess.com`, mens eldre lokal policy hadde `bussassistent`. Under etterfølgende avlesing endret eier selv **Team domain** til `bussassistent.cloudflareaccess.com`. Agenten hadde bedt om bare avlesing. Endringen er beholdt og eksplisitt dokumentert; opprinnelig samlet konfigurasjon kan derfor ikke hevdes uendret. Allow-regel, medlemsbegrensning, MFA og eierkonto ble ifølge eier beholdt. Ingen konto-/policyendring ble utført av agenten.

Et første brukerforløp etter endringen åpnet appen uten observert MFA; årsaken er ikke fastslått og resultatet beholdes. Policybildet viste Prompt for MFA on every login, og eier bekreftet bare Authenticator application valgt. Deretter viste et nytt gjestevindu først Access-innlogging; eier fullførte faktisk Authenticator-MFA og kom til appinnloggingen uten å logge inn som jonas. Faktisk token-signatur/issuer/AUD og gyldig gjennomslipp ble deretter verifisert av HTTP-prøven. Dette beviser den observerte nye autentiseringsflyten, ikke alle MFA-/SSO-varianter.

## CF-MEMBER-01 og CF-MEMBER-02

Tid: 29. oktober 2026. Manuelle handlinger ble rapportert sekvensielt i chatten, men eksakte handlingstidspunkter er ikke målt. CF-MEMBER-01 skjedde før teamdomeneendringen; CF-MEMBER-02 etter endringen og før tokenreplay. Forløpene er brukerobservasjoner, ikke instrumenterte HTTP-målinger.

For hver prøve ble en annen eierkontrollert Cloudflare-konto B invitert med **bare Minimal Account Access**, først Pending og deretter Active etter aksept i separat nettleserprofil. Eieren kontrollerte aktiv status og rolle. Dette var reelt medlemskap, ikke den historiske ikke-medlemsprøven. B var ikke tillatt av appens eneste e-postregel. Ingen appkonto eller ekstra tillatende policy ble opprettet.

| Test | Forventet | Faktisk | Grense/status |
|---|---|---|---|
| CF-MEMBER-01 side | Aktivt medlem B uten tillatt e-post nektes før appen | Cloudflare Access viste «That account does not have access.»; appinnlogging ikke vist | Bestått, Cloudflare. Skjermbildet er vurdert, ikke kopiert til Git |
| CF-MEMBER-01 API | Ingen privat API-respons | Eier rapporterte Access-avvisning også på direkte API | Bestått brukerobservasjon; HTTP-status/redirectkjede ikke avlest |
| CF-MEMBER-02 side | Samme nekt på nytt teamdomene | Eier rapporterte Cloudflare Access-avvisning før assistentens innlogging | Bestått på dagens konfigurasjon |
| CF-MEMBER-02 API | Ingen private data | Eier rapporterte Cloudflare Access-avvisning og ingen private data | Bestått på dagens konfigurasjon; HTTP-status ikke avlest |

B ble fjernet etter hver prøve. Eier bekreftet uendret eierkonto/Allow-policy og normal jonas-adgang etter hver opprydding. Ingen Revoke sessions. Resultatene tilskrives Cloudflare Access; ingen lokal gate-observasjon er utledet. Positiv prøve etter midlertidig tillatelse av B var ikke nødvendig og ble ikke utført. Ytre Cloudflare-medlemskap er ikke appinnlogging eller eierskap til appdata.

## CF-EXP-01 – faktisk signert token etter faktisk utløp

Eier kopierte appens CF_Authorization fra den autentiserte gjesteprofilen til et skjult lokalt PowerShell-felt. Tokenet ble aldri delt i chat eller argumenter. Utklippstavlen ble overskrevet av eier. DPAPI-kryptert token og privat binding ble lagret utenfor Git i LOCALAPPDATA/BussassistentAccessExpiry, med ACL-arv av og bare Jonas/SYSTEM. Ingen appsession eller andre cookies ble sendt. Gjestevinduet ble senere lukket ved et uhell; replay benyttet den allerede lagrede kopien, ikke nettleseren.

Hjelperen brukte fast HTTPS-tjeneste, eksplisitt bekreftet team/AUD, RS256-verifikasjon mot teamets offentlige JWKS, forventet issuer/audience/type og gyldighet. Tokenet ble ikke redigert eller erstattet; systemklokken ble ikke endret. SHA256-binding i den private mappen bekreftet eksakt samme token ved replay. Signaturen ble kontrollert igjen, men ekte utløp ble bevisst beholdt for etterprøven. HTTP-klienten hadde redirects og cookiejar avslått, ingen tokenfornyelse og bare GET. Ingen rårespons ble lagret; rapportene inneholder status, ufølsom redirect uten query/fragment og begrenset responsmetadata.

| Måling | UTC 29.10.2026 | Oslo | Resultat |
|---|---|---|---|
| Signert iat | 20:42:29 | 21:42:29 | Ekte token utstedt |
| Førkontroll | 20:46:31–32 | 21:46:31–32 | Signatur/issuer/AUD gyldig; /private 200 med app-shell; /private-api/drafts 401 fordi appøkt manglet; begge no-store |
| Signert exp | 21:42:29 | 22:42:29 | Faktisk utløp, ikke cookie-Expires-estimat |
| Replay | 21:42:50 | 22:42:50 | Signaturen fortsatt korrekt, exact_token_match=true; begge mål 302 til bussassistent.cloudflareaccess.com/cdn-cgi/access/login/app.bussassistent.com |

Begge etterresponser var 143 byte, uten app-shell, med no-store og identisk responsfingeravtrykk. Redirectene ble ikke fulgt; ingen privat app/API-respons ble returnert i disse forsøkene. **Bestått ved Cloudflare-kanten**, omtrent 21 sekunder etter exp. Origin-gatens mottak/avvisning er ikke separat observert, og resultatet tilskrives ikke den. Syntetisk signert utløp, naturlig nettleserutlogging og tilbakekalling beholdes som andre typer evidens.

Rå sanitert evidens i [access-operations-20261029/](access-operations-20261029/): Capture-, Replay- og runner-JSON. Feltet before_control_passed=false i Replay betyr at responsene i replay-runden ikke var førkontrollens 200/401; Capture viser true. Det er ikke et feilet førkontrollresultat. exact_token_match=false i Capture betyr at det ennå ikke finnes en tidligere kopi å sammenligne med. Endelig vurdering bygger på begge faser, ikke bare exit code 0.

### Bevarte hjelperfeil

1. Første DPAPI-gjeninnlesing feilet på filens avsluttende linjeskift før HTTP-kall. Trim av den krypterte tekstrepresentasjonen rettet innlesingen; tokenbyte ble ikke endret. Ny dekrypteringskontroll bestod.
2. Første ventende runner avsluttet før replay fordi PowerShell automatisk gjorde JSON-tid til DateTime og etterfølgende strengparsing var kulturavhengig. Rettet til eksplisitt DateTimeOffset/invariant parsing. Ny runner ble lest tilbake i waiting-tilstand og avsluttet med exit 0 etter ekte utløp.

Hjelperen er bevart som [Test-AccessExpiry.ps1](../../scripts/Test-AccessExpiry.ps1). Parsing, base64url/SHA256 og HTTP-klientkonstruksjon ble kontrollert, etterfulgt av ovenstående reelle Capture/Replay. Dette er driftsverktøy; ingen produktkode er endret. Den konkrete ventemetoden ligger sammen med evidensen.

## Opprydding og sluttstatus

- B fjernet etter begge forsøk; eier og e-postpolicy bevart ifølge eier. Ingen appdata skrevet av prøvene.
- DPAPI-token, privat binding og tom testmappe slettet 29.10 etter replay; etterkontroll viste TokenDirectoryRemaining=false og RunnerRunning=false. Sanitert evidens beholdt. Dette er filsletting, ikke en påstand om fysisk forensisk sletting av lagringsmediet.
- Eier foretok avsluttende oppdatering/innlogging etter replay, fikk 2FA og bekreftet «Alt fungerer som det skal». jonas, passord, data og databasevolumer ble ikke endret av denne oppgaven.
- Siste SSH-kontroll viste samme eb0eee3-release, healthy API/database og aktiv tunnel. **Eier ba uttrykkelig om at tunnelen skal stå på** for separat Windows-av-prøve. Ingen tjeneste ble startet/stoppet av denne verifikasjonen.
- Teamdomeneendringen er et dokumentert avvik fra opprinnelig konfigurasjon; nåværende medlemsnekt, MFA, token og eieradgang ble kontrollert etter endringen. Ingen global økttilbakekalling.

Begge avtalte testmål er fullført. O3–O6/WAN/IPv6/øvrige drifts- og sikkerhetsgrenser er ikke lukket. Ingen full lokal gate-replay, bred MFA-matrise, produksjonsdeploy av nyere main eller Windows-av-prøve er påstått. Ingen ny V1-/Epic12-aksept inngår.

## Gjenbrukbar metode

Kjør Windows PowerShell 7.2+ som operatøren med `scripts/Test-AccessExpiry.ps1 -Action Capture -Team <bekreftet-team> -Audience <bekreftet-AUD> -ReportDirectory <sanitert-evidensmappe>`. Token tastes bare i skjult prompt. Målhostname er bevisst fast til denne tjenesten. Bekreft førkontrollens 200/app-shell og 401 uten appcookie. Vent til signert exp + minst fem sekunder med faktisk klokke, og kjør samme kommando med `-Action Replay`; ingen nettleserfornyelse eller logout kreves. Kjør til slutt `-Action Cleanup` med samme StateDirectory. Ikke publiser token.dpapi eller binding.json. Verifiser faktisk status/redirect og tjenesteversjon før resultat klassifiseres. En nettverks-/JWKS-feil eller 401 alene er ikke dokumentert Access-utløpsnekt.

Kilder kontrollert: [Cloudflare IdP og medlemsbegrensning](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/cloudflare/), [Minimal Account Access](https://developers.cloudflare.com/fundamentals/manage-members/roles/), [Access-økter og logout](https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/session-management/). Logout-endepunkt ble ikke brukt fordi Cloudflare beskriver tilbakekalling på tvers av apper.
