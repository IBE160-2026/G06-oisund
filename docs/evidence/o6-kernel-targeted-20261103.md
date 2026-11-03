# O6: målrettet sluttvurdering 3. november 2026

De 29 avgrensede høye treffene gir **to dokumenterte rettelser, 13 med observerte barrierer og 14 med uavklart konkret trigger**. Verten kjører fortsatt Ubuntu `7.0.0-42.42-generic`, release `7921eb54e4816aaab9368c3efd851bcf692f3823` og samme boot-ID. Målingen fra kl. 22:14 Oslo omfattet avgrensede kernelvalg, modulstatus, bruk og rettigheter. Gjeldende APT-policy tilbyr fortsatt 42.42. [Individuell disponering av alle 29](o6-kernel-targeted-20261103.csv), [kilder og observasjoner](o6-kernel-targeted-20261103-sources.json).

## Pakke- og kildebevis

- **CVE-2026-74578:** Canonicals eksakte 42.42-tag har den synkrone skcipher-banen beskrevet av leverandøren. Den tilsvarende Linux-patchen passer i revers, og fremoverkontrollen feiler. Dette avklarer den forkortede changelog-tittelen i 38.38. Ubuntu sin CVE-side viste fortsatt Resolute som berørt ved oppslag, så avviket er beholdt eksplisitt. [Canonical-kilde](https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/resolute/plain/crypto/algif_skcipher.c?h=Ubuntu-7.0.0-42.42), [Linux-patch](https://git.kernel.org/stable/c/b05defc41b27c7d0c05c45f67bf5b91c28f93669), [Ubuntu-status](https://ubuntu.com/security/CVE-2026-74578).
- **CVE-2025-40190:** ext4-kilden ved samme tag avviser refcount-wrap ved null før decrement og U64_MAX før increment. Kallestedene bruker ±1. Dette matcher rettelsens virkning, selv om en endret patchkontekst gir avslag på full reverssjekk. Lesetilgangen ga ikke superblokkens EA-inode-flagg, men kildebeviset avgjør rettelsesvurderingen. [Canonical-kilde](https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/resolute/plain/fs/ext4/xattr.c?h=Ubuntu-7.0.0-42.42), [Linux CVE-post](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2025/40xxx/CVE-2025-40190.json).
- **CVE-2026-98788:** Canonicals kilde tar fortsatt RCU-snapshot før publisering av den nye private futex-hashen. Linux-rettelsen krever motsatt rekkefølge. Den tilsvarende lokale `prctl`-operasjonen har ingen egen capability-port i kildebanen. Dette er konkret kildeevidens for videre patchoppfølging. [Canonical-kilde](https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/resolute/plain/kernel/futex/core.c?h=Ubuntu-7.0.0-42.42), [Linux-patch](https://git.kernel.org/stable/c/5d5dc18b3a9ac011619b7d3af4514bf9e9b6a6af).

For 29 CVE-er ble de siste inntil to oppgitte Linux-patchreferansene sammenholdt med filer fra Canonicals tag. 57 patcher og 54 av 55 kildefiler ble lest. Én selvtestfil for CVE-2026-98376 var utilgjengelig. Den relevante per-CPU-array-koden viser fortsatt `bpf_map_meta_equal`. Patcheksperimentet endret ingen kildefil. Første sjekk ble forkastet fordi Git hoppet over patchene under den eksisterende checkouten. Omkjøringen stengte oppdagelse av repoet og krevde eksplisitt `Checking patch` i verktøyets utskrift. En fremovermatch støtter at den konkrete hunken kan anvendes. Manglende match i begge retninger gir ingen pakkeavgjørelse. Kildebevisene er bundet til pakkeversjon og kjørende Ubuntu-build, med separat binærattestasjon utenfor omfanget.

## Gjenværende kernel-punkter og ansvar

Jonas er registrert som drifts- og risikoeier. Tabellen foreslår at han eier oppfølgingen, med teknisk verifikasjon i neste avgrensede O6-økt. Hendelsene er oppfølgingsvilkår. De er ikke nye ventetider eller løfter om automatisk overvåking.

| Punkt | Avklaring og konkret tiltak | Ansvarlig og når |
|---|---|---|
| K2 · Wi-Fi mesh/AP (3) | Observert grensesnitt er infrastrukturklient. Mesh/AP-banen avgrenses i denne konfigurasjonen. Bevar driftsrollen og kontroller leverandørrettelse. | Jonas. Før AP/mesh tas i bruk, eller ved støttet rettelse. |
| K3 · Wi-Fi klient (8) | Radio og felles klientkode er aktive. CSA, MBSSID, BA, chanctx, beacon, rate og fragmentbaner har særvilkår. Kvalifiser relevant Ubuntu-backport for Wi-Fi-drift når den publiseres. | Jonas. Ved støttet rettelse eller endret driver/AP-oppsett. |
| K4 · BPF og fprobe (6) | Uprivilegert BPF=2, tracefs root 0700, perf-paranoid=4, API/gate uten capabilities. Barrierene gjelder dagens tjenestekontekst. Privilegerte eller delegerte BPF-objekter og tracing krever egen vurdering. | Jonas. Ved pakkerettelse, delegert BPF eller endring av capability/tracing-policy. |
| K5 · DRM-pagemap (1) | Den berørte koden er i `drm_gpusvm_helper`, som var fraværende. Følg leverandørrettelse og kontroller om ny driver laster hjelperen. | Jonas. Før ny GPU/SVM-driver eller ved pakkerettelse. |
| K6 · TC-køvalg (1) | Ingen skbedit i de leste root/ingress/egress-filtrene i host-netns. Hold tiltaket knyttet til den konkrete køhandlingen. | Jonas. Før skbedit/TC-endring eller ved publisert rettelse. |
| K7 · USB/TTY (2) | Ingen non-EP0 kontrollendepunkter blant avleste USB-interface. TTY-portens samtidighetsbane er uavklart. Kontroller relevant port eller endpoint ved ny maskinvare, og følg begge patchene. | Jonas. Før ny USB/seriell bruk eller ved publisert rettelse. |
| K8 · ALSA compat (1) | 32-bit compat er mulig, men `snd_seq` var fraværende. Node 0660 audio og tjenestens grupper gir konkret tilgangsgrense. | Jonas. Før lyd/compat-tilgang gis, eller ved publisert rettelse. |
| K9 · futex og io_uring (2) | Futex har den relevante gamle rekkefølgen. io_uring er aktivt, og SQPOLL-kildevarianten er uavklart. API/gate har seccomp, men eksakte regler er uverifiserte. Prioriter en støttet pakke som dekker de konkrete kodestiene. | Jonas. Ved publisert støttet rettelse eller endring i arbeidslast eller syscall-policy. |
| K10 · audit (1) | Regelkombinasjonen er uavklart. Avklar den ved endring i audit-policy eller samtidig med kvalifisering av rettelsen, med avgrenset lesetilgang. | Jonas. Ved endring av audit-policy eller publisert rettelse. |
| K11 · IPv4 og page_pool (2) | TCP/IP og PAGE_POOL_STATS finnes. Hunkene passer fremover, mens konkret opsjons-/retransmisjons- eller driver/pool-trigger er uavklart. Følg disse patchene i neste kernelkandidat. | Jonas. Ved publisert rettelse eller endring i aktuell nettverksdriver. |
| K12 · øvrige høye funn (26) | Det tidligere registeret beskriver fraværende driver, modul, mount eller aktiv radio ved avlesing per CVE. Behold disse som situasjonsavgrensede og følg pakkerettelser. | Jonas. Ved relevant modul-, mount-, radio- eller maskinvareendring, eller publisert rettelse. |
| K13 · kritiske pakkerester (3) | CVE-2026-90162, 98725 og 98805 gjelder ksmbd, NVMe-target og TIPC. Nødvendige moduler var fraværende ved den kritiske kontrollen. Kontroller eksakte backporter når støttet generic-kandidat publiseres. | Jonas. Før funksjonene aktiveres, eller når Canonical publiserer aktuell pakke. |

Linux CNA-kildene, konkret forutsetning og patchresultater for K1–K11 finnes per CVE i registeret. For K12–K13 gjelder de tidligere individuelle vurderingene. [Høyt register](o6-kernel-high-20261103.csv), [kritisk register](o6-kernel-critical-20261103.md).

## Samlet O6-disponering

| Status | Resultat |
|---|---|
| Dokumentert rettet | 226 høye funn med pakke- eller kildebevis, og ni kritiske med samsvarende pakkehistorikk. Gjennomført image-/vertsvedlikehold og dokumenterte etterkontroller er ferdige. |
| Ikke relevant for denne verten | Fire av de høye treffene uten patchmatch krever LoongArch, arm64, AMD SEV eller SPARC VCC. Tidligere bekreftede plattformavgrensninger i pakkegruppen består. |
| Begrenset av dokumenterte barrierer | 39 høye treff med målte bruks- eller rettighetsgrenser (26 fra forrige gjennomgang og 13 her), og tre kritiske pakkerester med inaktive nødvendige moduler ved kontroll. Barrierene avgrenser eksponeringen i den målte konfigurasjonen. |
| Fortsatt uavklart | 14 høye treff med relevant kode og uavklart konkret trigger. Også de 39 barrieretreffene og de tre kritiske er åpne på pakkenivå. Ufullstendig bred OS-/leverandørkjededekning beholdes som bevisgrense. |

De dokumenterte Debian-restene er fortsatt åpne. ACL/FTS5 er avgrenset fra kartlagte normale app-/gatekodeveier. Bruk av privilegert ACL-stibehandling og en faktisk SQLite FTS5-arbeidslast må vurderes på nytt dersom kode eller administrasjon endres. Util-linux og ncurses har konkrete bruksbarrierer. Aksepten fra Jonas er midlertidig og knyttet til det dokumenterte omfanget. [Risikoaksept](o6-execution-20261101/owner-decision.json), [versjoner og leverandørstatus](o6-status-20261103.md).

| Åpent vedlikeholdspunkt | Konkret tiltak | Ansvarlig og når |
|---|---|---|
| O6-UTIL | Følg trixie-backport for CVE-2026-76642, 78408, 78409, 78410. Avklar 78409 mot eksakt mount-bane ved endret bruk. Bevar begrensninger for privilegert mount/nsenter. | Jonas. Ved støttet pakkerettelse eller ny privilegert mount/nsenter-bruk. |
| O6-NCURSES | Følg stabil rettelse for CVE-2025-69720 eller kvalifiser fjerning av verktøyet ved senere imageendring. Bevar grensen mot ubetrodd terminfo. | Jonas. Ved støttet rettelse eller ny bruk av infocmp/terminfo. |
| O6-ACL-FTS5 | Følg støttet ACL- og SQLite-rettelse. Knytt ACL-oppdatering til faktisk API-bruk og vurder SQLite-input hvis en ny FTS5-bane innføres. | Jonas. Ved støttet rettelse eller endret kode, bibliotekbruk eller administrativ sti. |
| O6-JOURNAL | Bevar den dokumenterte `ForwardToWall=no`-barrieren. Kontroller Ubuntu-rettelsen for CVE-2026-40228 når den foreligger. | Jonas. Ved støttet rettelse eller endret journald-policy. |
| O6-FIRMWARE | Separat, utsatt etter eierbeslutning. Registrerte kandidater er KEK CA, UEFI CA, UEFI dbx og Logitech Unifying Receiver. | Jonas. Gjenopptas ved uttrykkelig bestilling. |

## Sluttkriterier og anbefaling

Avslutt vedlikeholdets allerede beståtte sluttkontroller og denne avgrensede triagen som ferdig arbeid. Behold **samlet O6 åpen** med K2–K13 og bibliotek-/journalpunktene som sporbare rester. Det gjenstående er konkrete kernelrettelser eller tilstrekkelig individuell avklaring, med separate tiltak for Debian-restene. Ordinær stabilitet og backup følges i drift. Dokumentasjonen har ingen vedtatt minste observasjonstid, og den brede bevisgrensen utløser ingen ny generell kontrollrunde.

Ingen ny beslutning fra Jonas trengs for denne anbefalingen. Dersom Jonas ønsker å avslutte O6 administrativt som en avgrenset leveranse, trengs en uttrykkelig beslutning om at de åpne, navngitte punktene overtar restarbeidet. En slik omfangsbeslutning lar CVE-status og den midlertidige risikoaksepten stå som dokumentert. Firmwareutsettelsen er allerede besluttet. [Dokumenterte sluttkriterier](o6-readonly-20261102.md#sluttkriterier-nødvendig-avslutning-versus-løpende-oppfølging).
