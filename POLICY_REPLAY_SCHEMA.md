# Policy Replay Schema

Purpose: compare P1-P4 on the same observed samples without contaminating empirical runtime boundaries.

## Timing authority
Replay is simulation. It never changes SERVER_CLOCK_SAFE_LOWER_BOUND or FAILURE_BOUNDARY.

Quantitative replay inputs that represent actual timing (`admit_elapsed_sec`, `actual_unit_sec`, close overhead, wake lateness) must carry a timing-source/authority annotation. Under the final clock discipline:
- strict probe total WORKED comes only from GitHub START/END server markers;
- model-authored timestamp strings are not actual timing inputs;
- missing actual timing stays null;
- legacy pre-server-clock timing may be used only in explicitly labeled legacy sensitivity analysis, not to validate the current production policy.

## Replay input per observed unit
- source_probe_id
- workload_profile
- unit_id
- timing_scope: CURRENT_SERVER_AUTHORITY | DIRECT_SECONDARY | LEGACY_SENSITIVITY | UNKNOWN
- admit_elapsed_sec when trustworthy, else null
- estimated_unit_sec if estimate existed at admission, else null
- actual_unit_sec when directly observable, else null
- close_reserve sample source/scope
- hard_cap candidate from Phase B
- safety_margin candidate from Phase B
- clean_close_observed
- wake_observed
- wake_lateness_sec only when authoritative/trustworthy

## Policies
P1 FIXED_THRESHOLD: admit while control elapsed estimate < fixed cutoff.

P2 SOFT_CUTOFF_PLUS_HARD_CAP: ordinary units before soft cutoff; only predefined short units after; nothing new at hard cap.

P3 ESTIMATED_NEXT_TASK_ADMISSION: admit iff control elapsed estimate + estimated unit + close reserve + safety margin < hard cap.

P4 ADAPTIVE_ADMISSION: P3 form, with reserve/estimation correction derived only from prior observed samples; no future leakage.

The in-flight elapsed estimate used for control need not itself be the final strict WORKED clock, but empirical policy evaluation after the run must reconcile outcomes against authoritative evidence and must never pretend model-local time was strict duration proof.

## Output
- policy_variant
- would_admit
- predicted_finish_sec
- actual_finish_sec when observable
- overshoot_sec
- avoidable_early_handoff_sec
- close_budget_remaining_sec
- decision_error: NONE | FALSE_ADMIT | FALSE_REJECT | UNKNOWN
- timing_scope

## Selection
Compare P1 first. Add complexity only when simpler policies materially lose utilization/reliability. Prefer the simplest practically equivalent policy. Wake observation and timeliness remain separate.
