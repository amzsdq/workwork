# Policy Replay Schema

Purpose: make Phase C compare P1-P4 on the same observed workload/close samples without contaminating Phase-A runtime evidence. This file defines simulation inputs/outputs only; it does not promote a policy.

## Replay input per observed unit

- `source_probe_id`
- `workload_profile`
- `unit_id`
- `admit_elapsed_sec`
- `estimated_unit_sec` if an estimate existed at admission; otherwise null
- `actual_unit_sec` when directly observable; otherwise null
- `close_overhead_sec` sample source
- `hard_cap_sec` candidate supplied by Phase B
- `safety_margin_sec` candidate supplied by Phase B
- `clean_close_observed`
- `wake_observed`
- `wake_lateness_sec` when directly observable

Do not invent missing actual durations. A replay requiring unavailable actual-unit timing is excluded from quantitative comparison or used only qualitatively.

## Policy decisions

P1 FIXED_THRESHOLD:
`admit = elapsed < fixed_cutoff`

P2 SOFT_CUTOFF_PLUS_HARD_CAP:
- before soft cutoff: admit ordinary bounded unit;
- after soft cutoff: admit only short units under the predefined short-unit bound;
- at hard cap: admit nothing new and close.

P3 ESTIMATED_NEXT_TASK_ADMISSION:
`admit iff elapsed + estimated_unit + close_reserve + safety_margin < hard_cap`

P4 ADAPTIVE_ADMISSION:
Same decision form as P3, but close reserve and/or estimation correction come from prior observed samples only. No future sample leakage is allowed in replay.

## Output per decision

- `policy_variant`
- `would_admit`
- `predicted_finish_sec`
- `actual_finish_sec` when observable
- `overshoot_sec`
- `avoidable_early_handoff_sec`
- `close_budget_remaining_sec`
- `decision_error`: NONE | FALSE_ADMIT | FALSE_REJECT | UNKNOWN

## Comparison metrics

Primary:
1. useful/goal-directed work delivered per wall-clock cycle,
2. clean-close preservation,
3. continuation/wake preservation,
4. overshoot / lost-finalization rate.

Secondary:
- early-handoff waste,
- estimate error,
- control complexity,
- profile robustness.

## Selection discipline

- Compare P1 first; add P2/P3/P4 only when a simpler policy leaves material utilization or reliability on the table.
- Prefer the simplest policy that is practically equivalent on primary metrics.
- Never let simulated success raise SAFE_LOWER_BOUND or lower FAILURE_BOUNDARY.
- Wake observation and wake timeliness are separate replay outputs; a later observed continuation does not prove low idle gap.
