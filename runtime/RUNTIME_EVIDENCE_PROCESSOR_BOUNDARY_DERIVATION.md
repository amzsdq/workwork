# Runtime Evidence Processor — Boundary Derivation

## Pure aggregation contract
Input: already-classified empirical records only. Simulation/legacy records are excluded from current strict-bound movement.

### Safe lower bound
A target is eligible only when at least one marker-valid `CLEAN_PASS_WAKE_OK` exists for that target/profile under the current server-clock protocol. Coarse search may advance from one such run; production cap still requires Phase-B replication.

### Failure boundary
A `DURATION_FAIL_CANDIDATE` is not automatically a confirmed failure boundary. Preserve profile and reproduce/refine. Confirmed boundary requires enough profile-controlled evidence to exclude independent causes and bracket the failure against a lower clean target.

### Under-target
`UNDER_TARGET` never moves either boundary. It is a workload/execution diagnostic even when its WORKED is longer than all prior server-clock attempts.

### Non-duration / clock-invalid
Neither moves boundaries. Preserve causal annotations because repeated infrastructure failures may require operational remediation without changing runtime inference.

## Current derived state from R3-R6
- CLEAN_PASS_WAKE_OK count: 0
- DURATION_FAIL_CANDIDATE count: 0
- UNDER_TARGET valid-pair count: 3
- NON_DURATION_FAIL count: 1 (R5; clock-invalid secondary annotation)
- SERVER_CLOCK_SAFE_LOWER_BOUND: unresolved
- SERVER_CLOCK_FAILURE_BOUNDARY: unresolved

## Important distinction
The longest valid-pair UNDER_TARGET (`R6=975s`) is **not** a safe lower bound because the active study target is 1320s and no server-clock clean-pass target class has been completed and retrospectively continued. It is survival/supporting evidence only.

## Future aggregation output
For each profile and globally:
- highest eligible clean target
- lowest credible/confirmed duration failure target
- unresolved bracket width
- clean-run replication count near candidate cap
- profile coverage
- completion-envelope failure count
- raw-pair integrity anomaly count

This aggregation rule prevents the implementation from turning increasing UNDER_TARGET durations into a false safe-bound promotion.
