# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## 1. Research objective

Answer two questions with empirical evidence:

1. What is the maximum empirically safe substantive-work duration for one automation invocation?
2. What is the simplest reproducible handoff/admission policy that operates near that limit with high long-run useful-work utilization without materially increasing forced-stop/run-out risk?

Detailed protocols:
- `GITHUB_SERVER_CLOCK_PROTOCOL.md`
- `MAX_SAFE_RUNTIME_RESEARCH.md`
- `RUNTIME_BOUNDARY_DECISION_RULE.md`
- `RUNTIME_WORKLOAD_PROFILES.md`
- `RUNTIME_STRESS_WORKLOAD_MATRIX.md`
- `PROBE_EXECUTION_PLAN.md`

Evidence authority:
1. raw GitHub START/END marker REST resources for strict WORKED,
2. raw per-probe evidence,
3. `state/events.log`,
4. `state/current.json`,
5. derived summaries such as `EVIDENCE_TABLE.md`.

## 1A. Final work-duration clock invariant

```
WORK_DURATION Source of Truth = GitHub server timestamp
WORKED = END_MARKER.created_at - START_MARKER.created_at
```

Model-authored START/END/time/elapsed strings are non-authoritative. Strict timing requires immutable issue #1 START/END comments and raw REST `created_at`. Invalid marker pair => CLOCK_EVIDENCE_INVALID, no boundary effect. Pre-protocol timing remains legacy supporting evidence only.

## 2. Anti-drift and terminal sync

Before work: resolve active case, terminal observation, and exact next branch. Classify/continue incomplete probes before replacements. Every repeat must add decision value.

Terminal classification synchronizes raw terminal evidence + `state/events.log` + `state/current.json` + `EVIDENCE_TABLE.md`, followed by re-read verification. Sync/provider failure is NON_DURATION_FAIL.

Do not manufacture work to inflate duration. A runtime probe must have a predeclared genuinely useful workload corpus large enough for the target class. Redundant heartbeat writes, duplicate protocol prose, and repetitive validation solely to consume time are forbidden.

## 2A. Three-axis objective

A. SURVIVAL_BOUNDARY — strict WORKED + causal termination/close outcome.

B. PRODUCTIVE_WINDOW — direct active seconds only when defensible; otherwise substantive-unit and goal-directed evidence without fabrication.

C. COMPLETION_ENVELOPE — late-work admission and close reliability; derive HARD_CAP, SOFT_CUTOFF, CLOSE_RESERVE, PRODUCTIVE_CAP from evidence.

## 3. Phase gates

### Phase A — runtime boundary search

- LEGACY_EXPLORATORY_LOWER_BOUND = 20m
- SERVER_CLOCK_SAFE_LOWER_BOUND = unresolved
- FAILURE_BOUNDARY = unresolved
- active target = 22m server-clock revalidation
- planned_gap = +3m
- current profile = W3 MIXED_IO

Two server-clock 22m attempts are terminal UNDER_TARGET:
- R3 = 652s, migration/audit queue exhausted.
- R4 = 736s, R3 stopping defect corrected, but genuinely decision-relevant methodological work saturated before target; non-padding guard stopped synthetic churn.

These are experimental-workload-design failures, not duration failures. The next 22m repeat is allowed only after preparing a larger genuinely useful W3 workload/task corpus that can naturally sustain the target class. Do not start another protocol-analysis-only probe.

After a strict 22m clean PASS + WAKE_OK, continue +2m coarse ascent with rotated profiles. First credible duration-related failure creates F; obtain/refine a same-profile server-clock lower anchor and narrow to about 1m.

### Phase B — operating-cap validation

At least 5 clean marker-valid runs at/near candidate, no unresolved duration failure at/below candidate, scheduler verification, durable close, WAKE_OK where observable, representative profile coverage: W3, W5, W4 or W6, W7.

### Phase C — handoff/admission

Compare P1 FIXED_THRESHOLD, P2 SOFT_CUTOFF_PLUS_HARD_CAP, P3 ESTIMATED_NEXT_TASK_ADMISSION, P4 ADAPTIVE_ADMISSION. Stop at simplest practically equivalent policy.

Overlap candidate remains KEEP/TEST/NOT_PROMOTED: 15m owner baseline, +12m successor wake, SHADOW successor, single scheduler owner, generation fencing, next cycle anchored to OWNER_ACTIVATED_AT; later compare 15/11, 15/12, 15/13 with server-authoritative timing where feasible.

### Phase D — planned-gap optimization

After runtime/cap policy stabilizes: +3m -> +2m -> +1m if stable.

### Phase E — deferred parallel

`PARALLEL-A14-B4-02` remains supporting-only until Phase A/B sufficiently complete.

## 4. Study-case queue

### SC-A22-CLOCK-01

PASS: valid marker pair, WORKED >=1320s, sustained substantive W3 work, durable close, scheduler WRITE_OK/STATE_OK, no duration-attributable forced stop. Clean close => CLEAN_PASS_PENDING_WAKE; WAKE_OK => SERVER_CLOCK_SAFE_LOWER_BOUND=22m and SC-A24-CLOCK+.

UNDER_TARGET: valid marker pair, WORKED <1320s, no independent failure; boundary unchanged. Repeat only after correcting cause.

Current repeat prerequisite after R4: predeclare a larger genuine W3 workload corpus/task source. Protocol-analysis/checkpoint churn is explicitly insufficient.

CLOCK_EVIDENCE_INVALID/NON_DURATION_FAIL: no boundary effect.

DURATION_FAIL_CANDIDATE: profile-controlled bracket/refinement.

### SC-A24-CLOCK+
Prior server-clock clean PASS + WAKE_OK; target +2m, rotate profile.

### SC-AR-*
~1m profile-controlled refinement after first credible duration failure.

### SC-B-CAP-*
At least 5 clean validations with representative profile coverage.

### SC-C-POLICY-*
Replay then live; simplest equivalent wins.

### SC-D-GAP-*
3m -> 2m -> 1m.

### SC-E-PARALLEL-01
Resume deferred parallel only after Phase A/B gate.

## 5. Per-case record

Record case/probe identity, target/profile, clock marker IDs/timestamps, WORKED, marker validity, terminal classification, boundary effect, next case, anomaly cause, productive evidence, completion-envelope evidence.

## 6. Current execution pointer

CURRENT_CASE_ID = SC-A22-CLOCK-01
ACTIVE_PROBE_ID = none
LATEST_TERMINAL_PROBE = PROBE-22M-SERVERCLOCK-20260923-R4
LATEST_RESULT = UNDER_TARGET

Immediate objective:
Do not start another duplicate 22m probe using protocol-analysis work. First construct/select a larger genuinely useful W3 MIXED_IO workload corpus directly relevant to the runtime research/control implementation, large enough to naturally sustain 22m without synthetic padding. Then repeat SC-A22-CLOCK-01 with the same GitHub server-clock invariant and +3m planned gap.

## 7. Final completion gate

Program completes only when SERVER_CLOCK_SAFE_LOWER_BOUND, FAILURE_BOUNDARY or unresolved, OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_OVERHEAD, SAFETY_MARGIN, NEXT_TASK_ADMISSION, validation confidence/count, workload coverage, rollback rule, and selected planned gap are traceable to durable evidence.
