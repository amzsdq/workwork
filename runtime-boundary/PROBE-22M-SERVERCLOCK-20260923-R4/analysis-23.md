# R4 admission-policy complexity test plan

This is preparatory analysis only; no Phase C policy is activated during R4.

## Comparison order

P1 FIXED_THRESHOLD -> P2 SOFT_CUTOFF_PLUS_HARD_CAP -> P3 ESTIMATED_NEXT_TASK_ADMISSION -> P4 ADAPTIVE_ADMISSION.

## Stop rule

Stop increasing complexity when a simpler policy is practically equivalent on:
- long-run useful-work utilization,
- clean-close rate,
- next-wake success,
- overshoot/run-out,
- unnecessary early handoff,
- control overhead.

## Expected baseline

P2 is likely the strongest simple baseline because it protects a close reserve while allowing short work after a soft cutoff. P3 should only win if task-size heterogeneity causes material wasted capacity or overshoot under P2. P4 requires evidence that fixed estimates fail under changing conditions.

## Required server-clock adaptation

Any elapsed-time-dependent policy must consume server-authoritative timing state rather than model-authored elapsed strings. This requirement follows directly from the final clock invariant and should be designed before live Phase C tests.

## Current action

Preserve this plan only. Do not activate policy logic until Phase A/B gates are satisfied.
