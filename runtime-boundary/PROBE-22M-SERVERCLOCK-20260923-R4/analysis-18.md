# R4 final-output traceability map

The final program output requires every promoted value to be traceable. This map identifies the evidence class needed for each field.

- SERVER_CLOCK_SAFE_LOWER_BOUND: highest clean target with valid marker pair + retrospective WAKE_OK.
- FAILURE_BOUNDARY: first credible duration-fail region, refined under controlled profile.
- OPERATING_CAP: Phase B repeated clean validations below/near failure region.
- PRODUCTIVE_CAP: near-cap useful-work evidence across representative profiles.
- SOFT_CUTOFF: Phase C admission-policy experiments.
- HARD_CAP: survival/completion envelope plus safety margin.
- CLOSE_OVERHEAD: server-authoritative or independently defensible close samples, summarized by distribution.
- SAFETY_MARGIN: failure bracket + variance + close/continuation uncertainty.
- NEXT_TASK_ADMISSION: Phase C comparison of P1-P4, prefer simplest practically equivalent rule.
- validation confidence/count: explicit counted clean runs and profile coverage.
- workload-profile coverage: W3/W5 plus W4 or W6 and W7 near candidate.
- rollback rule: Phase B/C observed failure modes and denominators.
- selected planned gap: Phase D 3m -> 2m -> 1m optimization after runtime policy stabilizes.

R4 directly contributes only to the first item and supporting evidence for productive/completion methodology. It must not prematurely fill later fields.
