#!/bin/bash
# Read-only. Never print Netplan passwords or service environments.
set -u
printf '\n--- NETWORK ---\n'
networkctl list --no-pager
ip -brief address
ip route show default
systemctl is-enabled ssh.socket ssh.service
systemctl show systemd-networkd-wait-online.service -p ExecStart
printf '\n--- SHORT BOOT ---\n'
journalctl -b -2 --no-pager -n 80
printf '\n--- CURRENT NETWORK BOOT ---\n'
journalctl -b -u systemd-networkd-wait-online -u systemd-networkd --no-pager -n 70
printf '\n--- RESOURCES ---\n'
uname -r
lscpu | head -20
timedatectl show -p Timezone -p NTPSynchronized
df -h /
printf '\n--- SOFTWARE ---\n'
command -v docker cloudflared || true
sudo -n true 2>/dev/null && echo 'Passwordless sudo available' || echo 'Sudo requires local terminal'
