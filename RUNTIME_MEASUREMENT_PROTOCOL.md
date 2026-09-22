# Runtime Measurement Protocol

Purpose: make Phase A timing evidence comparable without adding artificial delay.

## Clock points
For each invocation record:
- `run_start_ts`: as close as practical to the beginning of substantive execution.
- `pre_close_ts`: immediately before durable close/finalization begins.
- `scheduler_write_start_ts`: immediately before the final automation update.
- `scheduler_write_end_ts`: immediately after the update returns.

Derived:
- `actual_elapsed_sec = scheduler_write_end_ts - run_start_ts`
- `close_overhead_sec = scheduler_write_end_ts - pre_close_ts`
- `useful_window_sec = pre_close_ts - run_start_ts`

Do not claim `useful_work_sec` with stopwatch precision unless it was directly observed. If tool/network waits are not separable, record `useful_window_sec` and mark `useful_work_sec` as an estimate or unknown rather than fabricating precision.

## Target interpretation
`target_runtime_min` is a voluntary handoff target/class, not permission to sleep or pad. Continue substantive bounded work while evidence-producing work remains. If substantive work is exhausted before target, close honestly and classify the run as `UNDER_TARGET_INSUFFICIENT_WORK`, not as a timing PASS for that target class.

## Duration-failure classification
Count a failure as a credible duration-boundary signal only when one or more occur near/after the target and unrelated failure evidence is absent:
- invocation terminates before durable close,
- final scheduler write cannot be attempted because the turn ends,
- durable checkpoint is missing because execution is cut off,
- repeated near-boundary runs show the same close-loss pattern.

GitHub/API/network/provider errors with explicit independent evidence are `NON_DURATION_FAILURE`.

## Retrospective wake evidence
At the next invocation, compare prior intended `FINAL_NEXT` with actual new invocation start when observable. Record `next_wake_observed=true` and `idle_gap_sec`/wake lateness if measurable. Scheduler write success alone is not WAKE_OK.

## Boundary confidence
One clean run advances the coarse probe but does not establish a production cap. One ambiguous failure does not establish a hard boundary. Reproduce ambiguous boundary failures where practical.
