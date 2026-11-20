# O6 source and V2 impact review, 20 November 2026

Local `main` includes the O6 source and decision record in `df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb`. The last observed server state is from 15 November. The 17 November review still records 51 kernel findings fixed, one not affected and four open, as well as open library and journald findings. Firmware remains deferred under Jonas's decision. [Prior individual dispositions](o6-kernel-source-20261117.md).

## Debian util-linux package

Debian currently marks trixie's `2.41.5-0+deb13u1` vulnerable to CVE-2026-78409. Upstream names versions starting at 2.42 as affected. The Debian source archives were downloaded from its official pool and matched the SHA-256 values and sizes declared in its `.dsc`. The original archive is `f586e35d320ff537aab3ffeca37e9ecd482ccbe013590db4429a414d8aa6a728` (9,474,992 bytes) and the Debian patch archive is `5b327ccd22f0f4ed28a389870aa51d04ecedb8693e52a1d122850f2b3188cbf6` (107,604 bytes). [Debian package](https://packages.debian.org/trixie/source/util-linux), [Debian tracker](https://security-tracker.debian.org/tracker/CVE-2026-78409), [upstream advisory](https://github.com/util-linux/util-linux/security/advisories/GHSA-8f2p-47x3-43mv).

In the exact archive, `libmount/src/hook_subdir.c:279–308` rejects the restricted-user subdirectory path before temporary mounting. The predicate in `libmount/src/context.c:406–409` is the restricted-user check. The detached fast-path field identified by upstream is absent from `hook_mount.c`. Of the eleven applied Debian patches, the only libmount code change targets source-path preparation in `context.c` around line 1998. It does not modify that predicate or either hook. The matching source therefore does not contain the specific restricted-user fast path described by the advisory. The Debian tracker discrepancy persists, and no V2 change or new installed-server evidence alters the existing O6 disposition. [Applied Debian patch series](https://sources.debian.org/src/util-linux/2.41.5-0%2Bdeb13u1/debian/patches/series/).

## V2 code and permissions

- The private API remains on the pinned Debian trixie Python image and adds no Python dependency. The route and NSR contracts use packaged or explicitly mounted public source data. The V2 runtime reads the scoped route archive through a read-only mount in its separate local sandbox.
- The notice collector is enabled explicitly by the Owner launcher. Its only provider requests are to the configured public Entur collection for fixed TRO data. It adds no host privileges, packages, production service or new credential. Private review remains behind the existing account and workday gates.
- Position stays inside the browser. Only bounded stop occurrence decisions and their evidence metadata reach the private API. GPS speed and road matching introduce no host permission. The user grants browser geolocation for each origin, profile and device used.
- The password restore helper is a privileged, explicitly invoked operator path. The candidate ships stricter bind-mount and transaction/resume checks. Installed SSH authorization, systemd, the real maintenance mounts and the hand-delivered proof remain named acceptance gates. Local PostgreSQL and mock systemd tests cover only their recorded environment.

No OS update, reboot, server observation, exploit reproduction, production change or risk decision was made during this review.
