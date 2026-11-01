# O3–O5 overnight qualification requirements

Scope: owner's 2 November 2026 instruction; branch qualification only.

- O3: complete missing automatable authentication, Origin/CSRF, mutation, connection-loss, receipt recovery and duplicate-persistence controls. Reuse valid evidence on unchanged code. External authenticated/device tests require an already authorized suitable test context; distinguish them from isolation. Synthetic data only.
- O4: inspect bindings, ports, routes, IPv4/IPv6 and available router/firewall configuration read-only. Only confirmed owned infrastructure is a network target. Shared Cloudflare IPs are not origin addresses. No firewall/network changes. Record missing external vantage and administrative access.
- O5: replace the worker that can stay inside OS DNS indefinitely after caller timeout with genuinely cancellable work or isolation that can be terminated. Increasing timeouts is not a solution. Verify sustained resolver hang termination, resource cleanup, repeated failures/concurrency, DNS/network recovery, fail-closed authentication, cache bounds and key rotation.
- Run relevant regression and established project code review; fix independently actionable findings. No questions or waiting dialogs: record required user participation and continue unaffected work.
- Preserve all other branches/worktrees, dirty state, password work, production/test environments, V1 tag/releases and existing risk decisions. Commit and push work/evidence/logs to a dedicated follow-up branch. No main merge, deploy, production restart, package updates or production fault injection.
- O6 read-only stability observations are permitted; do not close O6 or create persistent jobs. Stop and remove own temporary resources before completion.

## Review context

Baseline: fetched origin/main de959f38274c44dda2b20367a207dfaf655b762b.
Production read-only observation: 5e521cbc658594a47c4568d352a50e46309573c4.
This task is operational follow-up, not a new sprint story. No story/sprint status is to be changed by code review. Workflow confirmation checkpoints are superseded by the owner's explicit instruction to run independently, fix qualified findings and ask no questions.
