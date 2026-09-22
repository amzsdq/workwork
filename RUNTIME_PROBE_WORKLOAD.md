# Runtime Probe Workload

Purpose: provide real, bounded research work that can sustain timing probes without padding or fake waiting.

## Work units
Each probe invocation should consume as many still-useful units as needed while collecting actual elapsed/useful-work evidence.

1. Evidence integrity audit
- Reconcile README, research protocol, decision rule, state/current, and event tail.
- Identify contradictions that could corrupt runtime classification.
- Fix only contradictions that affect this study.

2. Measurement schema hardening
- Define exact event fields and allowed nullability for timing probes.
- Define START, pre-arm-write start/end, workload start, target-cross, pre-close, close-end, and next-wake timestamps.
- Keep event records compact enough for repeated use.

3. Failure-classification cases
- Enumerate duration failure, under-target, non-duration failure, malformed scheduler return, missing wake, and ambiguous close-loss cases.
- Verify each maps to exactly one boundary effect.

4. Boundary estimator review
- Check whether +2m ascent / +1m refinement can bias the recommended cap.
- Define what evidence changes lower bound, candidate upper bound, and production cap.

5. Close-reserve and pre-arm estimator
- Define rolling summary fields for close overhead and start-of-turn pre-arm overhead separately.
- Track planned gap versus actual idle gap on the following wake.
- Keep the estimator usable with sparse observations and explicit uncertainty.

6. Handoff policy simulation logic
- Derive decision records for P1-P4 using observed task-duration and close-overhead samples.
- Compare avoidable early handoff versus overshoot risk without claiming empirical runtime evidence from simulation.

7. Rollback policy
- Define when a promoted cap/policy must be reduced after later duration failures or wake-loss evidence.

8. Reproducibility audit
- Check that another relay worker can reconstruct the current target and evidence state using only durable files.

## Probe discipline
- Never sleep or spin merely to reach target time.
- If useful units are exhausted before target, classify UNDER_TARGET and create further genuinely useful study work only when justified.
- If the target is crossed while useful work is in progress, close at the next safe checkpoint; record overshoot.
- Do not count document-editing time as useful merely because it consumes time; the edit must materially improve measurement, classification, continuation safety, or policy reproducibility.
