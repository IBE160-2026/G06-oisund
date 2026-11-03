# Høye kernel-funn på produksjonsverten 3. november 2026

Produksjonens Ubuntu-build `7.0.0-42.42-generic` har **224 samsvarende rettelser i den leverte pakkehistorikken** blant de 283 unike høye CVE-ene fra 42-familien. Av de **59 uten sikker patchmatch** kan fire avgrenses til andre plattformer. 26 manglet en observert driver, modul, mount eller aktiv radio ved målingen. For 28 finnes relevant komponent eller enhetsnode, men det konkrete triggervilkåret er fortsatt uavklart. Ett treff har en lignende rettelsestittel som må kontrolleres mot riktig patchvariant. [Komplett CVE-register](o6-kernel-high-20261103.csv), [kildekvittering](o6-kernel-high-20261103-sources.json).

## Grunnlag og metode

SSH-avlesing fra kl. 22:02 Oslo bekreftet release `7921eb54e4816aaab9368c3efd851bcf692f3823`, boot `2812a231-758d-4b5e-8241-d748b52d0991` og kjørende Ubuntu-build 42.42 med upstream-basis 7.0.14. APT-policy fra eksisterende lister viste samme kandidat. Både pakkeregister og kjørende versjon ble kontrollert. [Ubuntu USN-8959-1](https://ubuntu.com/security/notices/USN-8959-1) oppgir 42.42 som rettet build for sitt varsel på Resolute generic. Varselets samlede CVE-liste dekker flere kernelvarianter. Individuell disponering her bygger derfor på installert pakkehistorikk og vertsevidens.

Samme CVE kan forekomme i flere av skannerens kilde- og binærpakker. Grunnsettet er de 283 distinkte CVE-ene som er dokumentert for 42-familien, med historiske titler fra den arkiverte triagen. For de 65 uten opprinnelig direkte tittelmatch ble Linux-leverandørens CVE-poster lest. Tittel ble sammenlignet med patchpunkter i kumulativ changelog for den installerte modulpakken. Sammenligningen normaliserte store/små bokstaver, mellomrom, linjebryting og skannerens kernel-prefiks. 80 samsvar står i 39.39 og 144 i 41.41. Kortere eller lignende patchtitler teller ikke som sikre treff. Metoden gir pakkeevidens uten separat binærattestasjon. [Historisk skannerregister](o6-execution-20261101/os-package-groups-after-host-updates.json), [arkivert triage](https://github.com/IBE160-2026/G06-oisund/blob/841fbbe337860d06456abf21c6cd0e5501ad5ffc/docs/evidence/o6-triage-20261101/high-critical.csv).

Kodeveiene ble gruppert etter subsystem i tittel. Modul- og driverstatus er øyeblikksbilder. Konfigurasjon skiller innebygd kode fra moduler som kan lastes senere. Mounttyper gjelder SSH-prosessens namespace. Gruppestatus alene avgjør ikke individuell nåbarhet. Ingen lastetest, sårbarhetsutløsning eller endring av produksjon inngikk.

## Kodeveier

| Kodevei | Høye CVE-er | Åpne i pakkevurderingen | Vertsobservasjon |
|---|---:|---:|---|
| BPF og tracing | 34 | 6 | BPF-syscall, fprobe og funksjonstracing er bygd inn. Uprivilegert BPF=2. Privilegert last, programtype og aktive trampoliner er uavklart. |
| Bluetooth | 27 | 7 | Bluetooth/USB-driver lastet og én Bluetooth-enhet. Begge Bluetooth-rfkill-oppføringer er soft blocked. Konkret pairing, ISO/SCO og RFCOMM-bruk er uavklart. |
| Filsystem og mount | 18 | 2 | ext4, overlay, squashfs og vfat i bruk. De øvrige spesifikke mounttypene i gruppen ble ikke sett i SSH-namespace. |
| Grafikk | 16 | 3 | i915 og nouveau er bundet og lastet. Ingen amdgpu, vmwgfx, vc4, v3d eller virtio_gpu i målingen. Konkret pagemap-bruk er uavklart. |
| Lagring og blokk | 11 | 0 | NVMe og AHCI er lastet og bundet. Spesifikke Fabrics-/target-, SCSI- og blokktriggere krever egen driver eller operasjon. |
| Lokale kernel-API-er | 12 | 6 | Futex, io_uring og audit er bygd inn. io_uring_disabled=0. Binder er modulbasert, uten lastet binder eller observert enhet/mount. Lokale rettigheter og konkrete operasjoner er egne vilkår. |
| NFS, RPC og RDMA | 26 | 1 | Ingen nfsd, nfs, sunrpc eller RDMA-moduler i målingen, ingen RDMA-klasse eller NFS-mount i SSH-namespace. |
| Nettverk | 56 | 7 | IPv6/XFRM er bygd inn, og bridge, veth, nf_tables og conntrack er lastet. SCTP, IPVS, flowtable og netlink queue-modulene ble ikke sett. Detaljert TC- og regelbruk er uavklart. |
| SMB | 24 | 3 | KSMBD og CIFS var ikke lastet, og CIFS-mount ble ikke sett i SSH-namespace. Tjeneste- og klientveiene vurderes separat. |
| Trådløst LAN | 25 | 12 | rtl8821ae, cfg80211 og mac80211 lastet, WLAN uten rfkill. Assosiering, BA, fragmentering, mesh/AP og kanalbytte må vurderes per CVE. iw mangler, og modus ble ikke verifisert. |
| USB, lyd og periferi | 14 | 8 | USB-kjerne og lyddrivere finnes. /dev/snd/seq finnes for audio-gruppen. Spesifikke periferi- og Thunderbolt-drivere vurderes per CVE. |
| VM og arkitektur | 20 | 4 | Intel x86_64. Ingen KVM-modul eller /dev/kvm observert. Arkitekturfunn avgrenses til korrekt CPU/plattform. |

## Det som må følges videre

- **Tilgjengelige kjøreveier (28).** Wi-Fi-gruppen omfatter 11 funn med aktiv felles kode og uavklarte særvilkår, blant annet kanalbytte, assosiering og BA/fragmentering. Den tolvte åpne Wi-Fi-raden gjelder `ath9k_htc`, som ikke var lastet. Andre oppfølgingspunkter omfatter lokale futex-, io_uring-, audit- og BPF/fprobe-baner, IPv4 TCP, TX-køvalg, page_pool, ext4, DRM, USB, TTY og ALSA compat. CSV-en angir den konkrete forutsetningen per CVE. Triggere som krever en lokal prosess, privilegier eller en særskilt konfigurasjon må vurderes på det grunnlaget. Pakkerettelse følges videre.
- **Forutsetning fraværende ved måling (26).** Dette omfatter blant annet inaktiv KSMBD, RDMA og spesifikke nett-, grafikk- og periferidrivere. Bluetooth er et eget tilfelle der modulen og maskinvaren finnes, men radioen var soft blocked. Vurder på nytt ved aktivering, ny driver, ny mount eller endret bruk. Status på pakkenivå er fortsatt åpen der patchmatch mangler.
- **Andre plattformer (4).** Blant de 59 uten sikker patchmatch gjelder CVE-2026-89907, 98712, 98719 og 98754 henholdsvis LoongArch, arm64, AMD SEV og SPARC VCC. Intel x86_64-observasjonen avklarer vertsrelevansen for disse fire.
- **Patchvariant (1).** CVE-2026-74578 krever at den korte algif_skcipher-rettelsen i changelog sammenholdes med den konkrete varianten i Linux CVE-posten. Modulen var ikke lastet. [Linux CVE-post](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/74xxx/CVE-2026-74578.json).

Kritiske rester og den dokumenterte midlertidige aksepten følges fortsatt i O6-KERNEL. Denne gjennomgangen lukker ingen øvrige O6-punkter. Neste pakkesteg er å sammenholde en støttet publisert generic-build med CVE-listen før kvalifisering. [Kritisk gjennomgang](o6-kernel-critical-20261103.md), [midlertidig aksept](o6-execution-20261101/owner-decision.json).

## Firmware

Aktiv fwupd returnerte allerede tilgjengelige kandidater uten metadataoppfriskning. KEK CA og UEFI CA har 2023-kandidater fra 2011, UEFI dbx har opptil 20260402 fra 20230501, og Logitech Unifying Receiver har opptil RQR12.10_B0032 fra RQR12.03_B0025. Dette følges som **O6-FIRMWARE**, adskilt fra kernel-CVE-ene. Identifiser og kvalifiser hver kandidat med leverandørens endringslogg, oppstarts- og gjenopprettingsforutsetninger før et eventuelt vedlikeholdsvindu. Ingen kandidat ble installert. `linux-firmware` er en separat APT-pakke og hadde samme installerte versjon og kandidat ved kontrollen.
