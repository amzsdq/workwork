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
- `close_end_ts`: completion time of the last **required operational terminal-sync write**, not of optional post-close measurement/audit work.
- `next_invocation_start_ts`: next invocation start, used retrospectively.

Derived:
- `actual_elapsed_sec = close_end_ts - run_start_ts`
- `prearm_overhead_sec = prearm_write_end_ts - prearm_write_start_ts`
- `close_overhead_sec = close_end_ts - pre_close_ts`
- `planned_gap_sec = PREARM_NEXT - (run_start_ts + target_runtime)`
- `actual_idle_gap_sec = next_invocation_start_ts - close_end_ts`
- `wake_lateness_sec = next_invocation_start_ts - PREARM_NEXT`
- `active_window_sec = pre_close_ts - work_start_ts`

Do not claim `useful_work_sec` with stopwatch precision unless it was directly observed. If tool/network waits are not separable, record `useful_window_sec` and mark `useful_work_sec` as an estimate or unknown rather than fabricating precision.

## Close-end measurement without recursive writes
A naive scheme can recurse forever: write `close_end_ts`, then that write itself moves the close end, requiring another write.

Avoid this by defining the operational close endpoint as the completion/commit time of the final required terminal-sync write among raw terminal evidence, `state/events.log`, `state/current.json`, and `EVIDENCE_TABLE.md`.

Preferred evidence order:
1. capture `pre_close_ts` before terminal-sync work;
2. perform the required terminal-sync writes;
3. use the final required write's trustworthy commit/completion timestamp as `close_end_ts` when available;
4. if that timestamp is only available retrospectively, persist/derive it on the next invocation as measurement evidence without redefining the already-finished operational close;
5. optional post-close measurement writes are excluded from `close_overhead_sec` but should be reported separately if they materially extend wall time.

This gives a finite, reproducible completion envelope and prevents instrumentation from moving the endpoint it is trying to measure.

## Productive-window semantics
The research goal is useful work, not merely wall-clock survival. Distinguish:
- `goal_directed_window_sec`: wall-clock interval during which the invocation is continuously pursuing necessary research work, including necessary tool I/O latency that cannot be separated from that work.
- `direct_active_work_sec`: only directly measurable active work time; leave unknown when it cannot be isolated reliably.
- `substantive_unit_count`: completed useful units, used as a density cross-check rather than as a substitute for time.
- `productive_ratio`: use `direct_active_work_sec / actual_elapsed_sec` only when direct active time is actually measurable.
- `goal_directed_ratio`: `goal_directed_window_sec / actual_elapsed_sec` may be reported separately when the invocation remained continuously engaged but internal tool wait cannot be separated.

Never silently count idle/sleep/padding as productive. Never penalize a real W2 workload merely because necessary GitHub write latency is inseparable from task execution; report the metric class explicitly instead.

## Target interpretation
`target_runtime_min` is a voluntary handoff target/class, not permission to sleep or pad. Continue substantive bounded work while evidence-producing work remains. If substantive work is exhausted before target, close honestly and classify the run as `UNDER_TARGET_INSUFFICIENT_WORK`, not as a timing PASS for that target class.

## Duration-failure classification
Count a failure as a credible duration-boundary signal only when one or more occur near/after the target and unrelated failure evidence is absent:
- invocation terminates before durable close,
- pre-armed wake was valid but the invocation terminates before durable close,
- durable checkpoint is missing because execution is cut off,
- repeated near-boundary runs show the same close-loss pattern.

GitHub/API/network/provider errors with explicit independent evidence are `NON_DURATION_FAILURE`.

## Scheduler metadata caution
During an in-flight invocation, live automation metadata such as `last_run_time` may still reflect the previous completed invocation even when the same automation's updated future schedule is already visible. Therefore:
- use the scheduler update return/live schedule to verify prearm WRITE_OK/STATE_OK;
- do not use mid-run `last_run_time` as proof of the current invocation's start;
- capture `run_start_ts` independently at invocation start;
- establish wake timing retrospectively from trustworthy next-invocation evidence.

## Retrospective wake evidence
At the next invocation, compare prior `PREARM_NEXT`, prior `close_end_ts`, and actual new invocation start when observable.

Keep two concepts separate:
- `wake_observed`: a later invocation can be durably tied to the prearmed continuation path.
- `wake_timeliness`: how close that invocation start was to PREARM_NEXT, measured by `wake_lateness_sec` and `actual_idle_gap_sec`.

Legacy `WAKE_OK` used for strict Phase-A continuation means the continuation was retrospectively observed; it does not by itself prove low idle time or acceptable wake jitter. Phase B/D utilization claims require timeliness evidence as well.

Pre-arm write success alone is neither wake observation nor wake-timeliness evidence. If an intervening wake may have occurred but is not durably evidenced, do not infer a large idle gap from a later reconciliation timestamp; mark timeliness unresolved.

## Boundary confidence
One clean run plus retrospective wake observation can advance the coarse search under the strict protocol, but it does not establish a production cap or acceptable idle-time behavior. One ambiguous failure does not establish a hard boundary. Reproduce ambiguous boundary failures where practical.
