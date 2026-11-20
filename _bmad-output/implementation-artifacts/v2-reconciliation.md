# V2 requirements reconciliation

## Source revisions and sequence

| Order | Historical source | V2 boundary |
| --- | --- | --- |
| 0 | Local O6 merge `df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb` | Current source review on 17 November, last physical server observation on 15 November. 51 fixed, one not affected, four open kernel residuals. Scoped risk and named library/journal/firmware dispositions retain their documented boundaries. |
| 1 | Password branch `29a77ff95cc7607b81c3351375771b6b23d2d1dd`, common product baseline `15011042b1fe093becbe68177e6396e456b1f35f` | Add reviewed migration 015 and its runtime, test, recovery and operator paths. SENDT and 30-minute authority are current. Technical replay uses disposable credentials. Personal trials stay distinct. |
| 2 | Automatic notices `da867072a8a17249032c00efa51bd61979d41428`, AN-E1-S1–S4 | Migration 016. Paged Entur TRO only. Keep public observations separate from private associations, manual notice operations, audit clocks and expiry. Local preview may enable provider refresh. |
| 3 | Complete route network `7cada9d2e66af9806358f582bc8ea459321a6563`, CRN-E1-S1–S4 | Migration 017. P1 is one line and seven explicit dates, both directions and all variants, with independent closed coverage/known absence. Preserve history from 26 October–1 November. Start current verification with 23–29 November and a pinned NeTEx generation. |
| 4 | Position progression `df47a4e74ca982a2e04d6e5531e7744caf4f4717`, PP-E1-S1–S4 | Migration 018 for the last bounded workday anchor. Requires confirmed dated trip and selected occurrence range, exact dated NSR mapping and qualified coordinates. |
| 5 | Road limits `5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c`, SL-S1–S7 | Depends on qualified directed road data and a separate matcher. Route P1 and stop order cannot establish a directed road. Cover the four-roundabout corridor only on proven intervals, with an independently qualified secondary manifest. |
| Independent | GPS speed `e2468abb8bf492007d9f9437698c80d88e9ca280`, GS-E1-S1–S4 | Start/resume without a stop anchor. No persistence or separate subscription. A route or road-data block does not block the speed evaluator or shared controller. |

## Shared rules

Public provider traffic receives only fixed, scoped public identifiers and dates. Private operations use the existing auth, same-origin and CSRF checks, parent ownership, optimistic revisions, idempotency and fixed expiry. Public source health stays distinct from null application results. No raw location crosses the browser boundary.

Use feature detection and one foreground location watch. Purge samples and revoke the generation on visibility or context loss, error, Pause/Off and session expiry. Require deliberate resume after interruption. Progression requires a manually selected occurrence even when speed can start by itself. Keep static road limit, upcoming change and own speed independent and advisory. Exact physical qualification remains pending.
