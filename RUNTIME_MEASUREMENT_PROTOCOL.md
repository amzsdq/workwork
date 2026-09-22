# Runtime Measurement Protocol

Purpose: make Phase A timing evidence comparable without adding artificial delay.

## Clock points
For each invocation record:
- `run_start_ts`: actual invocation start reference.
- `prearm_write_start_ts`: immediately before the start-of-turn automation update.
- `prearm_write_end_ts`: immediately after the pre-arm update returns.
- `work_start_ts`: immediately after successful pre-arm, before active workload.
- `target_cross_ts`: first observed timestamp at/after the target class, if reached.
- `pre_close_ts`: immediately before durable close/finalization begins.
- `close_end_ts`: immediately after the final durable checkpoint/evidence is complete.
- `next_invocation_start_ts`: next actual wake start, when observable.

Derived:
- `actual_elapsed_sec = close_end_ts - run_start_ts`
- `prearm_overhead_sec = prearm_write_end_ts - prearm_write_start_ts`
- `close_overhead_sec = close_end_ts - pre_close_ts`
- `planned_gap_sec = PREARM_NEXT - (run_start_ts + target_runtime)`
- `actual_idle_gap_sec = next_invocation_start_ts - close_end_ts`
- `active_window_sec = pre_close_ts - work_start_ts`

Do not claim `useful_work_sec` with stopwatch precision unless it was directly observed. If tool/network waits are not separable, record `useful_window_sec` and mark `useful_work_sec` as an estimate or unknown rather than fabricating precision.

## Target interpretation
`target_runtime_min` is a voluntary handoff target/class, not permission to sleep or pad. Continue substantive bounded work while evidence-producing work remains. If substantive work is exhausted before target, close honestly and classify the run as `UNDER_TARGET_INSUFFICIENT_WORK`, not as a timing PASS for that target class.

## Duration-failure classification
Count a failure as a credible duration-boundary signal only when one or more occur near/after the target and unrelated failure evidence is absent:
- invocation terminates before durable close,
- pre-armed wake was valid but the invocation terminates before durable close,
- durable checkpoint is missing because execution is cut off,
- repeated near-boundary runs show the same close-loss pattern.

GitHub/API/network/provider errors with explicit independent evidence are `NON_DURATION_FAILURE`.

## Retrospective wake evidence
At the next invocation, compare prior `PREARM_NEXT`, prior `close_end_ts`, and actual new invocation start when observable. Record `next_wake_observed=true`, `actual_idle_gap_sec`, and wake lateness. Pre-arm write success alone is not WAKE_OK.

## Boundary confidence
One clean run advances the coarse probe but does not establish a production cap. One ambiguous failure does not establish a hard boundary. Reproduce ambiguous boundary failures where practical.
