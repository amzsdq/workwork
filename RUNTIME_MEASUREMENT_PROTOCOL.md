# Runtime Measurement Protocol

Purpose: make Phase A timing evidence comparable without adding artificial delay.

## Authoritative duration clock
For every new strict probe, `GITHUB_SERVER_CLOCK_PROTOCOL.md` overrides all older elapsed-time conventions.

`WORKED = END_MARKER.created_at - START_MARKER.created_at`

Only the raw GitHub server `created_at` values of the immutable issue #1 marker comments are authoritative for strict duration classification. Model/local timestamps and the secondary instrumentation below never substitute for WORKED.

## Secondary instrumentation points
When directly observable, record:
- `prearm_write_start_ts` / `prearm_write_end_ts` for scheduler-control overhead;
- `work_start_ts` for productive-window context;
- `last_normal_task_admit_ts` for admission evidence;
- `pre_close_ts` immediately before the durable close checkpoint;
- `end_marker_created_at` as the authoritative measured-work endpoint;
- `operational_sync_end_ts` after post-END terminal ledger/state/table synchronization and required consistency re-read;
- `next_invocation_start_ts` retrospectively when trustworthy.

Derived secondary metrics may include:
- `prearm_overhead_sec` when both endpoints are trustworthy;
- `close_checkpoint_overhead_sec` when the close-checkpoint interval is directly observed;
- `post_end_sync_overhead_sec = operational_sync_end_ts - end_marker_created_at` only when both are authoritative/compatible enough for that secondary metric;
- `wake_lateness_sec` and `actual_idle_gap_sec` only from trustworthy wake evidence.

Do not call any secondary elapsed metric `WORKED` or `actual_elapsed_sec` for strict boundary purposes.

## Two-endpoint close semantics
The final clock protocol intentionally separates two endpoints:

1. `MEASURED_WORK_END = END_MARKER.created_at` — ends authoritative WORKED after substantive work and durable close checkpoint.
2. `OPERATIONAL_SYNC_END` — later secondary endpoint after terminal evidence/event/state/table synchronization and consistency verification.

Post-END synchronization is bookkeeping outside WORKED. It may still matter for completion-envelope/control-overhead analysis, but it never moves END_MARKER or recursively changes WORKED.

## Productive-window semantics
Distinguish:
- `goal_directed_window_sec`: wall-clock interval continuously pursuing necessary research work, including inseparable necessary tool I/O;
- `direct_active_work_sec`: only directly measurable active work; leave unknown when it cannot be isolated;
- `substantive_unit_count`: useful-unit density cross-check;
- `productive_ratio = direct_active_work_sec / WORKED` only when direct active time is defensible;
- `goal_directed_ratio` may be reported separately when its endpoints are directly defensible.

Never count idle/sleep/padding as productive.

## Target interpretation
`target_runtime_min` is a voluntary handoff target/class, not permission to sleep or pad. Continue substantive bounded work while evidence-producing work remains. If substantive work is exhausted before target, close honestly and classify UNDER_TARGET, not PASS.

Target crossing is established only after END_MARKER exists and server-clock WORKED is computed. A model/local clock must not declare empirical target crossing.

## Duration-failure classification
A credible duration-boundary signal requires valid clock evidence when available plus near/after-target close-loss/forced termination without an independent cause. Missing marker evidence is CLOCK_EVIDENCE_INVALID rather than a duration failure. GitHub/API/network/provider failures with explicit independent evidence are NON_DURATION_FAIL.

## Scheduler metadata caution
During an in-flight invocation, live automation metadata such as `last_run_time` may reflect a previous invocation. Verify prearm from the scheduler update return/live schedule. Never use scheduler metadata or model time as the authoritative START marker.

## Retrospective wake evidence
At the next invocation, compare prior prearmed wake with trustworthy new invocation evidence. Keep `wake_observed` separate from `wake_timeliness`. Legacy WAKE_OK means continuation was observed; it does not itself prove low idle gap.

## Boundary confidence
One marker-valid clean run plus retrospective wake observation can advance coarse search but cannot promote a production cap. One ambiguous failure does not establish a hard boundary. Reproduce ambiguous boundary failures where practical.
