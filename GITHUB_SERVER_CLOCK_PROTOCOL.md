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

Each measured invocation uses two immutable GitHub issue comments in issue #1:

- START_MARKER
- END_MARKER

The marker comment body identifies the invocation/probe but contains no authoritative time value.

After creating each marker comment, read the raw GitHub REST comment resource:

https://api.github.com/repos/amzsdq/workwork/issues/comments/<COMMENT_ID>

Use only the server-populated `created_at` value from that raw resource.

The normalized connector comment listing may omit/null `created_at`; therefore it is not the timing source.

## Marker lifecycle

At invocation start:

1. Resolve probe_id / invocation_id.
2. Create START_MARKER as the first timing action, before scheduler pre-arm and substantive work.
3. Record its GitHub comment ID.
4. Fetch the raw comment resource and persist `start_marker_created_at`.

At normal close:

1. Finish substantive work and required durable close/state synchronization.
2. Create END_MARKER.
3. Record its GitHub comment ID.
4. Fetch the raw comment resource and persist `end_marker_created_at`.
5. Compute WORKED only from the two server timestamps.

## Required calculation

`worked_sec = parse(END_MARKER.created_at) - parse(START_MARKER.created_at)`

No model-authored START, END, elapsed, wall-clock, local-time, or inferred timestamp may substitute for either marker.

## Evidence requirements

Every strict timing probe must persist:

- clock_protocol = GITHUB_SERVER_MARKER_V1
- clock_issue_number = 1
- start_marker_comment_id
- start_marker_created_at
- end_marker_comment_id
- end_marker_created_at
- worked_sec
- marker_pair_valid = true/false

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

END:
```
RUNTIME_END_MARKER
probe_id=<PROBE_ID>
case_id=<CASE_ID>
clock_protocol=GITHUB_SERVER_MARKER_V1
```

The body is identity metadata only. Timing comes exclusively from GitHub server `created_at`.
