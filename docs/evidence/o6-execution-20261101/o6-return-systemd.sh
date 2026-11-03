#!/bin/sh
set -eu
test "$(id -u)" -eq 0
printf '%s\n' '7d15afdad13bb79311605c3aa114e7d8ac7188b8c9ed5aa59438631e33543972  /var/backups/bussassistent/o6-pre-5e521cbc/o6_host_step.py' | sha256sum -c -
/usr/bin/python3 -c 'import runpy; m=runpy.run_path('"'"'\\var\\backups\\bussassistent\\o6-pre-5e521cbc\\o6_host_step.py'"'"'); m['"'"'install'"'"']('"'"'systemd'"'"',True)'
printf '%s\n' 'Return command completed; verify packages and services before continuing.'
