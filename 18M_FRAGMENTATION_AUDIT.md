# 18m Fragmentation Audit

Purpose: quantify why the 18m class has produced many starts/checkpoints without a terminal decision. This is an audit of durable probe inventory, not a duration-failure claim.

## Prior unique 18m probe IDs before the current 20:00 probe

Inventory across historical namespaces shows 18 unique prior 18m probe IDs:

- `runtime/probes`: 13:10:16, 13:53:33 — 2
- `runtime-probes`: 13:30:42 — 1
- `runtime-evidence`: 14:13:42, 14:35:52, 15:14:27, 15:52:50, 16:34:54, 17:15:52, 18:19:08, 18:39:37 — 8
- `runtime`: 14:56:14, 15:33:46, 16:16:49, 17:57:03, 18:58:04 — 5
- `runtime-boundary`: 17:34:16, 19:23:15 — 2

Total prior unique 18m attempts: **18**.

The current active attempt is `PROBE-18M-20260923T200017KST`, making it the 19th unique 18m probe identifier in the durable inventory.

## Terminal-close observation

The audited prior 18m inventory is dominated by start/work/checkpoint artifacts. No prior 18m artifact in the audited namespace inventories provides a strict terminal close that can promote the 18m class.

This must **not** be interpreted as 18 duration failures. Missing close evidence alone cannot distinguish runtime cut-off from voluntary/fragmented execution.

## Operational conclusion

The 18m problem is currently an execution-quality/measurement problem before it is a proven runtime-limit problem:

- many attempts,
- no strict terminal 18m decision,
- no credible duration-failure boundary,
- substantial repeated setup/checkpoint overhead.

Therefore a new 18m probe is justified only if it materially changes execution quality: sustained useful work, direct completion-envelope timestamps, and a terminal classification. Repeating start/checkpoint-only behavior has near-zero decision value.

## Research implication

Do not optimize for probe count. Optimize for terminal decision yield:

`terminal_decision_yield = terminally_classified_probes / started_probes`

For the historical 18m class before the current probe, the strict terminal-decision yield is effectively 0/18 for boundary promotion purposes. This metric should improve before additional same-class repetition is accepted.
