#!/bin/bash
# Run locally with sudo after reviewing. Does not start app/tunnel or change interface configuration.
set -euo pipefail
test "$(id -u)" = 0 || { echo 'Use sudo bash bootstrap.sh'; exit 1; }
source /etc/os-release
test "$ID" = ubuntu && test "$VERSION_ID" = 26.04 || { echo 'Review OS support first'; exit 1; }
HERE="$(cd -- "$(dirname -- "$0")" && pwd)"
test -f "$HERE/bussassistentctl.py"
getent passwd jonas >/dev/null
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl python3 unattended-upgrades
install -d -m 0755 /etc/apt/keyrings
curl --fail --silent --show-error --location https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod 0644 /etc/apt/keyrings/docker.asc
cat > /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $VERSION_CODENAME
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
curl --fail --silent --show-error --location https://pkg.cloudflare.com/cloudflare-main.gpg -o /etc/apt/keyrings/cloudflare-main.gpg
chmod 0644 /etc/apt/keyrings/cloudflare-main.gpg
echo 'deb [signed-by=/etc/apt/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' > /etc/apt/sources.list.d/cloudflared.list
apt-get update
# Do not silently remove an existing Docker distribution or configuration.
if dpkg-query -W -f='${Status}' docker.io 2>/dev/null | grep -q 'install ok installed'; then
    echo 'Existing distro Docker found; review before replacing'; exit 1
fi
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin cloudflared
getent passwd bussassistent-tunnel >/dev/null || useradd --system --no-create-home --shell /usr/sbin/nologin bussassistent-tunnel
install -d -m 0755 /opt/bussassistent /opt/bussassistent/releases
install -d -m 0700 /etc/bussassistent /etc/bussassistent/secrets
install -d -o root -g jonas -m 0750 /var/backups/bussassistent
install -m 0755 "$HERE/bussassistentctl.py" /usr/local/sbin/bussassistentctl
for unit in bussassistent.service cloudflared.service bussassistent-backup.service bussassistent-backup.timer; do
    test ! -L "/etc/systemd/system/$unit"
    install -m 0644 "$HERE/$unit" "/etc/systemd/system/$unit"
done
# Administrators can deploy executable code through this command. This is a trusted admin role.
printf '%s\n' 'jonas ALL=(root) NOPASSWD: /usr/local/sbin/bussassistentctl' > /etc/sudoers.d/bussassistent
chmod 0440 /etc/sudoers.d/bussassistent
visudo -cf /etc/sudoers.d/bussassistent
install -d -m 0755 /etc/systemd/logind.conf.d /etc/systemd/journald.conf.d
cat > /etc/systemd/logind.conf.d/60-bussassistent.conf <<'EOF'
[Login]
HandleLidSwitchExternalPower=ignore
EOF
cat > /etc/systemd/journald.conf.d/60-bussassistent.conf <<'EOF'
[Journal]
SystemMaxUse=200M
MaxRetentionSec=7day
EOF
cat > /etc/apt/apt.conf.d/60-bussassistent <<'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
Unattended-Upgrade::Automatic-Reboot "false";
EOF
# The observed Netplan-generated wait command waits only for unplugged enp4s0.
# Change readiness selection, not interface addressing or the running Wi-Fi connection.
install -d -m 0755 /etc/systemd/system/systemd-networkd-wait-online.service.d
cat > /etc/systemd/system/systemd-networkd-wait-online.service.d/90-bussassistent.conf <<'EOF'
[Service]
ExecStart=
ExecStart=/usr/lib/systemd/systemd-networkd-wait-online --any --interface=enp4s0:routable --interface=wlp3s0:routable --ipv4 --timeout=30
EOF
timedatectl set-timezone Europe/Oslo
systemctl daemon-reload
systemctl restart systemd-networkd-wait-online.service
systemctl enable --now docker
# Lid/journal settings take effect on next planned reboot. Do not restart logind over SSH.
docker version --format '{{.Server.Version}}'
docker compose version
cloudflared --version
echo 'Base software installed. App/tunnel not started. Network readiness corrected; interface configuration unchanged.'
echo 'Next: protected credentials, restore rehearsal, release validation, then enable services.'
