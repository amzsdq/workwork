# GitHub Server Clock Runtime Protocol

Status: FINAL INVARIANT
Repo: amzsdq/workwork
Clock lane: GitHub issue #1 ([CLOCK] Runtime Work Duration Markers)

## Final invariant

WORK_DURATION의 Source of Truth는 모델 출력이 아니라 GitHub 서버 timestamp이다.

WORKED =
END_MARKER.created_at
-
START_MARKER.created_at

모델이 작성한 시간 문자열은 작업시간 판정에 사용하지 않는다.

## Authoritative clock source

Each measured invocation uses four immutable GitHub issue comments in issue #1:

- START_MARKER: invocation timing begins
- WORK_START_MARKER: scheduler/prearm/setup is complete and substantive work begins
- PRE_CLOSE_MARKER: substantive work stops; durable close begins
- END_MARKER: durable close checkpoint is complete

The marker comment body identifies the invocation/probe but contains no authoritative time value.

After creating each marker comment, read the raw GitHub REST comment resource:

https://api.github.com/repos/amzsdq/workwork/issues/comments/<COMMENT_ID>

Use only the server-populated `created_at` value from that raw resource.

The normalized connector comment listing may omit/null `created_at`; therefore it is not the timing source.

## Marker lifecycle

At invocation start:

1. Resolve probe_id / invocation_id.
2. Create START_MARKER as the first timing action, before scheduler pre-arm and substantive work.
3. Fetch raw START created_at.
4. Pre-arm/validate scheduler and finish required setup.
5. Create WORK_START_MARKER immediately before the first substantive workload unit.
6. Fetch raw WORK_START created_at.

At normal close:

1. When the admission/close policy says to stop admitting new work, create PRE_CLOSE_MARKER.
2. Fetch raw PRE_CLOSE created_at.
3. Persist the durable close checkpoint with clock status pending.
4. Create END_MARKER immediately after that checkpoint.
5. Fetch raw END created_at.
6. Compute all timing metrics only from raw GitHub server timestamps.
7. Write marker IDs/metrics into immutable terminal evidence, then reconcile mutable projections using `runtime/TERMINAL_STATE_SYNC_PROTOCOL.md`.

Authoritative formulas:

```
WORKED = END_MARKER.created_at - START_MARKER.created_at
PREARM_OVERHEAD = WORK_START_MARKER.created_at - START_MARKER.created_at
PRODUCTIVE_WINDOW = PRE_CLOSE_MARKER.created_at - WORK_START_MARKER.created_at
CLOSE_OVERHEAD = END_MARKER.created_at - PRE_CLOSE_MARKER.created_at
```

WORKED remains the duration-boundary metric. PRODUCTIVE_WINDOW and CLOSE_OVERHEAD are separately server-clock measured; model-authored times never substitute.

The post-END terminal-ledger synchronization is bookkeeping outside WORKED. It must not create a new END time.

## Required calculation

`worked_sec = parse(END_MARKER.created_at) - parse(START_MARKER.created_at)`

No model-authored START, END, elapsed, wall-clock, local-time, or inferred timestamp may substitute for either marker.

## Evidence requirements

Every strict timing probe must persist:

- clock_protocol = GITHUB_SERVER_MARKER_V1
- clock_issue_number = 1
- start_marker_comment_id / start_marker_created_at
- work_start_marker_comment_id / work_start_marker_created_at
- pre_close_marker_comment_id / pre_close_marker_created_at
- end_marker_comment_id / end_marker_created_at
- worked_sec
- prearm_overhead_sec
- productive_window_sec
- close_overhead_sec
- marker_pair_valid = true/false
- productive_marker_pair_valid = true/false

A strict duration PASS requires `marker_pair_valid=true`.

If either marker is missing, the raw comment cannot be fetched, or either server `created_at` is unavailable, classify the exact-duration result as CLOCK_EVIDENCE_INVALID. It must not advance SAFE_LOWER_BOUND or create a duration failure boundary.

## Relationship to productive work

WORKED is authoritative wall-clock work-duration measurement.

Productive-work metrics remain separate:
- active_work_sec when directly measurable
- goal_directed_window_sec when active work cannot be separated
- substantive_unit_count
- productive_ratio only from defensible measurements

Do not substitute productive-window estimates for WORKED.

## Historical evidence

Runs completed before this protocol activation remain preserved as LEGACY_SUPPORTING_EVIDENCE.

Their model-authored time strings must not be used as authoritative exact duration under the new protocol.

Any new strict boundary/cap promotion must be supported by a valid GitHub server marker pair.

## Marker body format

START:
```
RUNTIME_START_MARKER
probe_id=<PROBE_ID>
case_id=<CASE_ID>
clock_protocol=GITHUB_SERVER_MARKER_V1
```

WORK_START:
```
RUNTIME_WORK_START_MARKER
probe_id=<PROBE_ID>
case_id=<CASE_ID>
clock_protocol=GITHUB_SERVER_MARKER_V1
```

PRE_CLOSE:
```
RUNTIME_PRE_CLOSE_MARKER
probe_id=<PROBE_ID>
case_id=<CASE_ID>
clock_protocol=GITHUB_SERVER_MARKER_V1
```

END:
```
RUNTIME_END_MARKER
probe_id=<PROBE_ID>
case_id=<CASE_ID>
clock_protocol=GITHUB_SERVER_MARKER_V1
```

The body is identity metadata only. Timing comes exclusively from GitHub server `created_at`.
