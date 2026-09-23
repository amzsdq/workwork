# GitHub Server Clock Runtime Protocol

Status: FINAL INVARIANT
Repo: amzsdq/workwork
Clock lane: GitHub issue #1 ([CLOCK] Runtime Work Duration Markers)

## Final invariant
WORK_DURATION의 Source of Truth는 모델 출력이 아니라 GitHub 서버 timestamp이다.
`WORKED = END_MARKER.created_at - START_MARKER.created_at`
모델이 작성한 시간 문자열은 작업시간 판정에 사용하지 않는다.

## Authoritative clock source
Each measured invocation uses four lifecycle marker comments — START, WORK_START, PRE_CLOSE, END — plus zero or more PROGRESS comments for in-flight admission control. All are immutable issue #1 comments. Marker body is identity/role metadata only; no body-authored time is authoritative.

After creating a marker, fetch `https://api.github.com/repos/amzsdq/workwork/issues/comments/<COMMENT_ID>` and use only raw server-populated `created_at`. Normalized listings may omit created_at and are not timing sources.

## Human display
When shown to a user, preserve raw UTC and append full Asia/Seoul conversion, e.g. `2026-09-23T17:15:25Z (2026-09-24 02:15:25 KST)`. KST is display-only; calculations use raw UTC.

## Lifecycle
1. resolve probe/case;
2. create/raw-fetch START before prearm/substantive work;
3. prearm/validate same scheduler and persist active identity at earliest safe checkpoint;
4. create/raw-fetch WORK_START immediately before substantive work;
5. during work, create/raw-fetch PROGRESS when an admission/close decision needs authoritative elapsed; control elapsed = PROGRESS.created_at - START.created_at;
6. model/local time may only hint when to sample;
7. when authoritative admission enters close window, create/raw-fetch PRE_CLOSE and stop admitting new substantive work;
8. persist durable close checkpoint/finalization;
9. create/raw-fetch END exactly once;
10. compute intervals from raw server timestamps, then persist immutable terminal/event and reconcile mutable projections.

## Formulas
`WORKED = END - START`
`PREARM_OVERHEAD = WORK_START - START`
`PRODUCTIVE_WINDOW = PRE_CLOSE - WORK_START`
`CLOSE_OVERHEAD = END - PRE_CLOSE`

Post-END ledger/projection sync is outside WORKED and never creates a second END.

## Required strict evidence
Persist clock protocol/issue number; all lifecycle marker IDs + raw created_at audit copies; worked/prearm/productive/close seconds; marker_pair_valid; productive_marker_pair_valid; harness/workload-quality fields required by the current strict harness.

Invalid/missing raw START or END => CLOCK_EVIDENCE_INVALID; it cannot advance safe lower bound or create a duration failure boundary. Invalid productive markers fail the productive interval closed and must not fabricate productive time.

## Productive work relationship
WORKED is duration-boundary wall clock. Productive window, active_work_sec, goal-directed evidence, semantic substantive units, and productive ratio are separate. No productive estimate substitutes for WORKED; no clock survival alone substitutes for the current harness's substantive-work quality gate.

## Historical evidence
Pre-protocol duration is LEGACY_SUPPORTING only. Posthoc harness-quality audit may preserve valid server-clock survival while reopening a substantive-runtime promotion; never rewrite raw marker truth.

## Marker body identity
Canonical bodies should identify marker role, `probe_id`, `case_id` when available, and clock protocol. Compact role tokens (`START_MARKER`, `WORK_START_MARKER`, `PRE_CLOSE_MARKER`, `PROGRESS_MARKER`, `END_MARKER`) are accepted when raw comment ID + role + probe identity are unambiguous. Timing always comes exclusively from server `created_at`.
