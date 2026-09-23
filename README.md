# workwork

Durable workspace for this ChatGPT RRULE relay.

## Single research objective
Find the maximum empirically safe useful-work duration per automation invocation **and** the simplest control policy that repeatedly reproduces near-optimal turns without materially increasing run-out/forced-termination risk.

The final output is not a single number. It must be an operational policy reusable by other relay workers.

## Optimization target
The research separates three axes:
1. **SURVIVAL_BOUNDARY** — how long an invocation can remain active without duration-attributable termination.
2. **PRODUCTIVE_WINDOW** — how much genuine goal-directed work is delivered during that runtime.
3. **COMPLETION_ENVELOPE** — how late useful work can continue while still preserving reliable durable close.

The objective is long-run useful-work utilization, not the longest observed run. A long sparse run is weak operating-policy evidence; a dense run that loses finalization is also unacceptable.

## Research contract
- Reuse the same automation for normal continuation; no replacement automation.
- Keep a complete recurring VEVENT containing `RRULE:FREQ=HOURLY`.
- Do not use DTSTART-only one-shot or `dtstart_offset_json`.
- Immediately after TURN_START, pre-arm the next wake before substantive work. Do not mutate the scheduler again at normal close.
- Compute NEXT_WAKE = TURN_START + target_runtime + planned_gap. Current Phase-A planned-gap baseline is +3m.
- Measure real elapsed runtime, productive/goal-directed work evidence, and completion-envelope timing separately.
- Deliberately generated bounded workload is allowed when it genuinely advances or validates this research and its profile is recorded. Idle/sleep/padding is excluded.
- A clean close requires verified prearm state, target reached, sustained substantive work, and durable close evidence. Under the strict protocol it remains `CLEAN_PASS_PENDING_WAKE` until a later invocation retrospectively confirms continuation was observed.
- Wake observation and wake timeliness are separate. A later observed continuation does not by itself prove low idle gap.
- Any platform/tool failure not plausibly caused by turn duration is classified separately rather than counted as a timeout boundary.
- Git history and `state/events.log` are recovery evidence.

## Phase A — find the runtime boundary
Current coarse sequence is approximately:
12 → 14 → 16 → 18 → 20 → continue +2m while clean.

A target advances only after clean close plus retrospective continuation observation under the strict protocol. This advances an exploratory safe lower bound, not a production cap.

Workload profiles rotate during coarse exploration. Therefore a failure at a higher target under a different profile is initially a target/profile failure pair, not automatically a universal duration boundary. During refinement, hold the failure-producing profile fixed and obtain a same-profile lower anchor when needed. Narrow at roughly 1-minute resolution.

## Phase B — validate an operating cap
Do not equate the longest one-off success with the operating limit.

A candidate operating cap should:
- have at least 5 clean repeated runs at/near the candidate,
- preserve durable close and verified prearm state,
- include retrospective continuation evidence where observable,
- leave a meaningful margin below a credible failure boundary,
- include representative workload-profile coverage,
- account for close overhead, overshoot variance, wake reliability, and wake timeliness.

If no failure boundary has been observed yet, continue ascent rather than declaring a maximum.

## Phase C — generalize into a reproducible control policy
Compare in increasing complexity:
1. P1 FIXED_THRESHOLD
2. P2 SOFT_CUTOFF_PLUS_HARD_CAP
3. P3 ESTIMATED_NEXT_TASK_ADMISSION
4. P4 ADAPTIVE_ADMISSION

P3 decision shape:
`continue iff elapsed + estimated_next_task + close_overhead + safety_margin < hard_cap`

Replay observed samples first. Add complexity only when it materially improves useful-work utilization or reliability. Simulations never alter empirical runtime boundaries.

## Phase D — optimize the prearmed gap
After runtime cap/policy are stable enough, test planned gap approximately:
3m baseline → 2m → 1m if stable.

Choose the smallest planned gap that preserves clean close and stable continuation without materially higher overlap/missed-wake risk.

## Required final deliverable
- SAFE_LOWER_BOUND
- FAILURE_BOUNDARY or unresolved
- OPERATING_CAP
- PRODUCTIVE_CAP
- SOFT_CUTOFF
- HARD_CAP
- CLOSE_OVERHEAD
- SAFETY_MARGIN
- NEXT_TASK_ADMISSION rule
- validation confidence/count
- workload-profile coverage
- rollback rule
- selected planned gap

## Measurement discipline
Track when directly observable:
- target_runtime_min
- actual_elapsed_sec
- direct active_work_sec and productive_ratio, otherwise null
- goal_directed_window_sec / goal_directed_ratio when necessary tool I/O is inseparable
- substantive_unit_count
- clean_close
- checkpoint_saved
- prearm scheduler write/state verification
- pre_close_ts / close_end_ts / close_overhead_sec
- overshoot_sec
- planned wake
- next wake observed
- wake_lateness_sec and actual_idle_gap_sec when directly evidenced
- forced_stop_or_timeout
- non_duration_failure
- workload_profile
- policy_variant during Phase C

Never invent missing timing values. Necessary tool latency may be part of a labeled goal-directed window but must not be silently relabeled as direct active work.

## Durable state
- `state/events.log` — canonical append-only experiment history.
- `state/current.json` — mutable current experiment pointer; rebuildable.
- `RUNTIME_RESEARCH_MASTER_PLAN.md` — canonical execution roadmap.
- `MAX_SAFE_RUNTIME_RESEARCH.md` — integrated research protocol.
- `RUNTIME_BOUNDARY_DECISION_RULE.md` — classification/refinement rules.
- `RUNTIME_MEASUREMENT_PROTOCOL.md` — timing semantics.

Never rewrite historical event meaning. Never persist credentials, cookies, session state, private URLs, or secrets.
