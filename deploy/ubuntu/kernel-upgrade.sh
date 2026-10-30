#!/usr/bin/env bash
# One-time, approved upgrade for the Lenovo server. Never reboots or autoremoves.
set -euo pipefail
trap 'echo "STOPP: installasjonen er ikke ferdig kontrollert. Ikke start pa nytt; del feilmeldingen." >&2' ERR
[[ $EUID -eq 0 ]] || { echo "Kjor med sudo." >&2; exit 1; }
old=7.0.0-30-generic
new=7.0.0-42-generic
version=7.0.0-42.42
[[ $(uname -r) == "$old" ]] || { echo "Uventet aktiv kernel; stopp." >&2; exit 1; }
for kernel in "$old"; do
    test -s "/boot/vmlinuz-$kernel"
    test -s "/boot/initrd.img-$kernel"
    dpkg-query -W -f='${Status}\n' "linux-image-$kernel" "linux-modules-$kernel" | grep -q 'install ok installed'
done
audit=$(dpkg --audit)
[[ -z "$audit" ]] || { printf '%s\n' "$audit"; exit 1; }
available=$(df -Pk /boot | awk 'NR==2 {print $4}')
(( available > 700000 )) || { echo "For lite plass i /boot."; exit 1; }
config=/etc/default/grub.d/99-bussassistent-recovery.cfg
content=$'GRUB_TIMEOUT_STYLE=menu\nGRUB_TIMEOUT=10'
if [[ -e "$config" ]]; then
    [[ $(cat "$config") == "$content" ]] || { echo "Eksisterende GRUB-fil avviker; stopp."; exit 1; }
fi
# Mark every installed package tied to the running kernel as manually installed.
mapfile -t keep < <(dpkg-query -W -f='${binary:Package} ${db:Status-Status}\n' '*7.0.0-30*' | awk '$2 == "installed" {print $1}')
(( ${#keep[@]} >= 2 ))
apt-mark manual "${keep[@]}"
apt-get update
apt-get --simulate --no-remove install "linux-generic=$version"
apt-get --yes --no-remove install "linux-generic=$version"
install -d -m 755 /etc/default/grub.d
printf '%s\n' "$content" > "$config"
chmod 644 "$config"
update-grub
for kernel in "$old" "$new"; do
    test -s "/boot/vmlinuz-$kernel"
    test -s "/boot/initrd.img-$kernel"
    grep -Fq "vmlinuz-$kernel" /boot/grub/grub.cfg
    dpkg-query -W "linux-image-$kernel" "linux-modules-$kernel"
done
audit=$(dpkg --audit)
[[ -z "$audit" ]] || { printf '%s\n' "$audit"; exit 1; }
echo "FERDIG: ny kernel installert, gammel kernel beholdt, GRUB-meny 10 sekunder."
echo "Ingen omstart utfort. Be om kontroll av installasjonen forst."
