# workwork

Durable workspace for this ChatGPT RRULE relay.

## Single research objective
Find the maximum empirically safe useful-work duration per automation invocation and the simplest control policy that repeatedly reproduces near-optimal turns without materially increasing run-out/forced-termination risk.

## Three axes
1. SURVIVAL_BOUNDARY — strict server-clock runtime and causal termination/close outcome.
2. PRODUCTIVE_WINDOW — genuine goal-directed work delivered during that runtime.
3. COMPLETION_ENVELOPE — how late useful work can continue while preserving durable close.

## Final duration invariant
For every new strict probe:

`WORKED = END_MARKER.created_at - START_MARKER.created_at`

Only raw GitHub server `created_at` values from immutable issue #1 START/END comments are authoritative. Model-authored START/END/elapsed/local-time strings are never duration evidence. Missing/invalid marker pair => CLOCK_EVIDENCE_INVALID with no boundary effect.

Pre-protocol timing remains LEGACY_SUPPORTING_EVIDENCE only.

## Research contract
- Reuse the same automation; no replacement automation.
- Keep recurring `RRULE:FREQ=HOURLY`; no DTSTART-only one-shot/dtstart_offset_json.
- After valid START_MARKER, immediately pre-arm next wake before substantive work; no normal-close scheduler mutation.
- Phase-A planned gap baseline: +3m from authoritative START + target runtime.
- Purposeful bounded generated workload is allowed when it genuinely advances/validates the research; idle/sleep/padding is excluded.
- Clean strict pass requires valid marker pair, WORKED >= target, sustained substantive work, durable close checkpoint, verified prearm, and no duration-attributable forced stop. It remains CLEAN_PASS_PENDING_WAKE until retrospective continuation observation.
- Wake observation and wake timeliness are separate.
- Independent provider/tool failures are not runtime-boundary failures.

## Phase A — boundary search
Current server-clock case is defined by fresh `state/current.json` and `RUNTIME_RESEARCH_MASTER_PLAN.md`. Coarse ascent uses about +2m after strict clean PASS + retrospective wake observation. First credible duration failure creates a profile-specific upper candidate; refine near 1m with profile held fixed.

## Phase B — operating-cap validation
Do not equate longest success with production cap. Require repeated clean marker-valid runs, representative profiles, completion-envelope evidence, and explicit margin.

## Phase C — policy generalization
Compare P1 FIXED_THRESHOLD, P2 SOFT_CUTOFF_PLUS_HARD_CAP, P3 ESTIMATED_NEXT_TASK_ADMISSION, P4 ADAPTIVE_ADMISSION. Prefer the simplest practically equivalent policy. Simulations never move empirical boundaries.

Controlled-overlap handoff remains deferred until Phase A/B are sufficiently complete. Future quantitative handoff timing also requires authoritative server-side endpoints; model-written file timestamps are non-authoritative.

## Phase D — gap optimization
After runtime/cap policy stabilizes, test planned gap from +3m toward +2m/+1m only when reliability remains acceptable.

## Required final deliverable
SERVER_CLOCK_SAFE_LOWER_BOUND, FAILURE_BOUNDARY or unresolved, OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_OVERHEAD, SAFETY_MARGIN, NEXT_TASK_ADMISSION, validation confidence/count, workload coverage, rollback rule, selected planned gap.

## Measurement discipline
Strict duration fields:
- start_marker_comment_id / start_marker_created_at
- end_marker_comment_id / end_marker_created_at
- marker_pair_valid
- worked_sec

Separate productive/control evidence when directly defensible:
- direct active_work_sec / productive_ratio
- goal_directed_window_sec / goal_directed_ratio
- substantive_unit_count
- durable close checkpoint
- scheduler write/state verification
- secondary post-END operational-sync overhead
- overshoot from strict WORKED
- wake evidence
- failure attribution
- workload profile

Never invent missing timing values.

## Durable state
- `state/events.log` — canonical append-only experiment history.
- `state/current.json` — mutable current experiment pointer.
- `GITHUB_SERVER_CLOCK_PROTOCOL.md` — final duration clock invariant.
- `RUNTIME_RESEARCH_MASTER_PLAN.md` — canonical roadmap.
- `MAX_SAFE_RUNTIME_RESEARCH.md` — integrated research protocol.
- `RUNTIME_BOUNDARY_DECISION_RULE.md` — classification/refinement rules.
- `RUNTIME_MEASUREMENT_PROTOCOL.md` — secondary measurement semantics.

Never rewrite historical event meaning or persist credentials/session secrets.
