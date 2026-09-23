# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## 1. Research objective

Answer two questions with empirical evidence:

1. What is the maximum empirically safe substantive-work duration for one automation invocation?
2. What is the simplest reproducible handoff/admission policy that operates near that limit with high long-run useful-work utilization without materially increasing forced-stop/run-out risk?

This document is the execution map. Detailed protocols remain in:
- `GITHUB_SERVER_CLOCK_PROTOCOL.md`
- `MAX_SAFE_RUNTIME_RESEARCH.md`
- `RUNTIME_BOUNDARY_DECISION_RULE.md`
- `RUNTIME_WORKLOAD_PROFILES.md`
- `RUNTIME_STRESS_WORKLOAD_MATRIX.md`
- `PROBE_EXECUTION_PLAN.md`

Evidence authority remains:
1. raw GitHub START/END marker REST resources for strict WORKED,
2. raw per-probe evidence,
3. `state/events.log`,
4. `state/current.json` as the mutable current pointer,
5. derived summaries such as `EVIDENCE_TABLE.md`.

A derived summary must never override raw/canonical evidence.

## 1A. Final work-duration clock invariant

For every new strict timing probe, `GITHUB_SERVER_CLOCK_PROTOCOL.md` is mandatory.

```
WORK_DURATION Source of Truth = GitHub server timestamp
WORKED = END_MARKER.created_at - START_MARKER.created_at
```

Model-authored START/END/time/elapsed strings are non-authoritative and must never be used to classify runtime duration.

Strict timing evidence requires a valid START_MARKER/END_MARKER pair written as immutable comments to GitHub issue #1, followed by raw REST reads of each comment's server `created_at`.

If the marker pair is invalid or unavailable, classify exact-duration evidence as `CLOCK_EVIDENCE_INVALID`. Do not advance SAFE_LOWER_BOUND and do not create a duration failure boundary.

Pre-protocol timing results remain `LEGACY_SUPPORTING_EVIDENCE`; they are preserved but cannot by themselves support a new strict promotion.

## 2. Anti-drift rule

Every invocation must answer exactly three questions before doing work:

1. What study case is active?
2. What observation will make that case terminal?
3. What exact next case follows each possible terminal result?

Do not repeat a target merely because `next_strict_target_minutes` is unchanged.

If an earlier probe for the active study case has START/checkpoint evidence but no terminal close classification, first classify or continue that incomplete probe from durable evidence before starting a replacement. A new probe must add decision value. Start-only repetition is not decision value.

### Terminal-classification write invariant

Whenever a study case reaches a terminal classification or a retrospective WAKE_OK changes its boundary effect, update the following as one logical transaction before advancing the case:

1. raw per-probe terminal evidence,
2. `state/events.log`,
3. `state/current.json`,
4. `EVIDENCE_TABLE.md` as the derived audit view.

After the writes, re-read shared-state views and verify agreement on latest terminal probe/result, SERVER_CLOCK_SAFE_LOWER_BOUND, FAILURE_BOUNDARY, current/next target, and current_case_id/next_case_id.

If they disagree, the case is not fully closed. A tool/provider failure that prevents synchronization is NON_DURATION_FAIL and must not alter the runtime boundary.

## 2A. Three-axis runtime objective

### A. SURVIVAL_BOUNDARY
How long the invocation can remain active without a duration-attributable forced stop or timeout. Strict wall-clock duration is `WORKED` from GitHub server markers only.

### B. PRODUCTIVE_WINDOW
How much of the invocation is spent on genuine goal-directed work.

Measure when directly supportable:
- active_work_sec
- productive_ratio
- goal_directed_window_sec / goal_directed_ratio when necessary tool I/O cannot be separated
- substantive_unit_count
- workload_profile

Do not manufacture work to inflate active time. Productive metrics never substitute for marker-derived WORKED.

### C. COMPLETION_ENVELOPE
How late useful work can continue while still preserving enough time for a reliable durable close.

Measure when defensible:
- last_normal_task_admit_ts
- pre_close_ts
- close_end_ts
- close_overhead_sec
- overshoot_sec
- clean_close
- checkpoint_saved

Completion-envelope timestamps are secondary instrumentation unless independently server-authoritative. They do not classify WORKED.

The purpose is to identify HARD_CAP, SOFT_CUTOFF, CLOSE_RESERVE, and PRODUCTIVE_CAP without conflating survival, productivity, and close reliability.

## 3. Phase gates

### Phase A — runtime boundary search

Current state:
- LEGACY_EXPLORATORY_LOWER_BOUND = 20m
- SERVER_CLOCK_SAFE_LOWER_BOUND = unresolved until first GITHUB_SERVER_MARKER_V1 pass + WAKE_OK
- FAILURE_BOUNDARY = unresolved
- active target = 22m server-clock revalidation
- planned_gap = +3m
- current profile = W3 MIXED_IO

Coarse ascent:
- revalidate 22m under server clock,
- then +2m while clean, rotating profiles per workload protocol.

Exit from coarse ascent:
- first credible duration-related failure creates a boundary candidate F,
- last lower server-clock clean class is L,
- move to profile-controlled refinement.

Refinement uses approximately 1m classes with the failure-producing profile fixed until a same-profile bracket is about 1m or finer. Ambiguous failure at F must be repeated once before narrowing.

### Phase B — operating-cap validation

Do not equate max observed success with the operating cap.

Promotion gate:
- at least 5 clean runs at/near candidate,
- valid server-clock marker pair for every counted run,
- no unresolved duration failure at or below candidate,
- scheduler WRITE_OK/STATE_OK,
- durable close checkpoint,
- retrospective WAKE_OK where observable,
- representative profile coverage.

Minimum profile coverage near candidate:
- W3 MIXED_IO
- W5 MICRO_UNIT_CHAIN
- at least one of W4 REASONING_HEAVY or W6 LARGE_UNIT
- W7 CLOSE_HEAVY for close-reserve characterization

### Phase C — handoff/admission policy comparison

Compare in increasing complexity:
- P1 FIXED_THRESHOLD
- P2 SOFT_CUTOFF_PLUS_HARD_CAP
- P3 ESTIMATED_NEXT_TASK_ADMISSION
- P4 ADAPTIVE_ADMISSION

Accepted overlap-handoff candidate:
- `OVERLAP_HANDOFF_BASELINE_CANDIDATE.md`
- initial baseline 15m OWNER work / successor wake at +12m / 3m nominal overlap
- successor wakes as SHADOW; only active OWNER mutates scheduler/control state
- ownership transfer fenced by generation/lease
- next cycle anchored to OWNER_ACTIVATED_AT, not SHADOW_WAKE_AT
- current evidence supports KEEP/TEST, not production promotion
- compare 15/11, 15/12, 15/13 rather than assuming +12m is final

Replay/simulate first; live-test only policies that plausibly improve the objective. Future quantitative handoff timing should use server-authoritative event timestamps when possible.

### Phase D — planned-gap optimization

After runtime cap/policy are stable enough, hold runtime policy approximately fixed and test +3m baseline, then +2m, then +1m if stable.

### Phase E — deferred cooperative parallel research

Only after Phase A boundary characterization and Phase B operating-cap validation are sufficiently complete. `PARALLEL-A14-B4-02` remains supporting-only.

## 4. Study-case queue

### SC-A22-CLOCK-01 — server-clock 22m revalidation
Profile: W3 MIXED_IO.

PASS prerequisites:
- valid GITHUB_SERVER_MARKER_V1 pair,
- WORKED >= 1320s,
- sustained substantive W3 work,
- durable close checkpoint,
- scheduler WRITE_OK/STATE_OK,
- no duration-attributable forced stop.

A clean close is CLEAN_PASS_PENDING_WAKE until retrospective WAKE_OK. Then SERVER_CLOCK_SAFE_LOWER_BOUND -> 22m and NEXT_CASE -> SC-A24-CLOCK+.

UNDER_TARGET:
- valid marker pair with WORKED <1320s and no independent failure,
- boundary unchanged; diagnose execution cause before repeat.

CLOCK_EVIDENCE_INVALID or NON_DURATION_FAIL:
- boundary unchanged.

DURATION_FAIL_CANDIDATE:
- establish/refine a profile-controlled bracket; legacy lower-bound evidence may guide test selection but cannot be the new strict lower anchor by itself.

### SC-A24-CLOCK+ — generated coarse ascent
Entry: prior server-clock target strict clean PASS + WAKE_OK.
Target: prior target +2m. Rotate workload profile. Continue until first credible duration failure.

### SC-AR-* — 1m refinement
Generated after first credible duration failure. Maintain a profile-controlled [L,F] bracket using server-clock evidence.

### SC-B-CAP-* — candidate-cap validation
At least 5 clean server-clock validations with representative profile coverage.

### SC-C-POLICY-* — policy comparison
Replay first, live test second. Stop increasing complexity when a simpler policy is practically equivalent.

### SC-D-GAP-* — planned-gap optimization
3m -> 2m -> 1m subject to continuation stability.

### SC-E-PARALLEL-01
Resume deferred `PARALLEL-A14-B4-02` only after Phase A/B gate.

## 5. Per-case record

Every new strict case should record:
- case_id
- phase
- hypothesis/question
- target_runtime_min
- workload_profile
- probe_id(s)
- clock_protocol
- start_marker_comment_id / start_marker_created_at
- end_marker_comment_id / end_marker_created_at
- worked_sec / marker_pair_valid
- terminal classification
- boundary/cap effect
- next_case_id
- anomaly/non-duration cause
- active_work_sec / productive_ratio when directly supportable
- goal_directed_window evidence when used
- substantive_unit_count
- completion-envelope evidence when defensible

## 6. Current execution pointer

CURRENT_CASE_ID = SC-A22-CLOCK-01
ACTIVE_PROBE_ID = PROBE-22M-SERVERCLOCK-20260923-R4

Immediate objective:
Continue R4 22m W3 server-clock revalidation. START marker is issue comment 5796189180 with raw server `created_at=2026-09-23T13:58:33Z`. Scheduler was pre-armed for 2026-09-23T14:23:33Z (+22m target +3m planned gap). R3 is terminal UNDER_TARGET and must not be treated as active. R4 must continue useful bounded W3 work through the target class, persist a durable close checkpoint, then create END_MARKER and classify only from the two server timestamps.

## 7. Final program completion gate

The program is complete only when it can report SERVER_CLOCK_SAFE_LOWER_BOUND, FAILURE_BOUNDARY or unresolved, OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_OVERHEAD, SAFETY_MARGIN, NEXT_TASK_ADMISSION rule, validation confidence/count, workload-profile coverage, rollback rule, and selected planned gap, each traceable to durable evidence.
