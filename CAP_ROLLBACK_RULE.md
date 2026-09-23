# Runtime Cap Rollback Rule

Purpose: prevent a previously promoted operating cap from remaining active after new evidence shows that its continuation risk has increased.

This rule becomes operational only after Phase B promotes a cap. It does not itself promote any cap.

## Evidence window
Maintain a rolling window of the most recent 10 eligible runs at/near the promoted operating cap. Eligible means the run had trustworthy timing evidence and no independent non-duration failure.

Track:
- clean close count,
- duration-related failure count,
- ambiguous close-loss count,
- observed next-wake count where measurable,
- wake lateness / actual idle gap where directly evidenced,
- close-overhead upper tail/max,
- overshoot beyond intended hard cap,
- productive/goal-directed work evidence separately from survival.

## Failure-layer separation
Do not collapse every bad cycle into a runtime-cap rollback.

- **Runtime/completion-envelope failure**: duration-attributable forced stop, lost durable close, or repeated close-budget exhaustion near the cap. This can justify cap rollback.
- **Wake-layer failure**: continuation missing/late despite a clean close and valid prearm. Diagnose scheduler/gap behavior first; do not automatically lower runtime cap.
- **Productivity failure**: invocation survives and closes but delivers sparse useful work. Diagnose workload/admission policy; do not call it a runtime-boundary failure.
- **Independent tool/provider failure**: classify separately; do not move the cap unless evidence links it causally to runtime pressure.

## Immediate rollback triggers
Reduce the active cap to the highest lower target class with prior clean evidence if either occurs:
1. one confirmed duration-related failure at or below the promoted cap that loses the durable close despite a valid pre-armed recurring wake; or
2. two ambiguous close-loss events at/near the cap before an independent non-duration cause is established.

Do not rollback for an explicit independent GitHub/network/tool/provider failure. Wake lateness alone is not a runtime-cap rollback trigger unless evidence shows the invocation overran into/through the prearmed wake. Sparse useful work alone is not a runtime-cap rollback trigger.

## Degradation trigger
Even without a catastrophic close-loss, re-open the cap if the rolling eligible window shows materially worse continuation behavior than during validation, including repeated overshoot or rising close-overhead that consumes the safety margin.

With sparse evidence, prefer conservative rollback rather than inventing a precise statistical threshold. Once enough samples exist, replace this qualitative trigger with an observed-rate criterion derived from the validation distribution.

## Recovery after rollback
- Return to the highest lower class with clean evidence.
- Re-estimate close reserve and safety margin from fresh runs.
- Do not immediately re-promote after one success.
- Require the normal Phase B repeated-validation rule before promotion again.

## Policy interaction
If failures are caused by admission-policy overshoot rather than the underlying runtime ceiling, first rollback the policy aggressiveness (larger reserve / earlier soft cutoff). If failures persist with conservative admission, rollback the operating cap itself.

If the problem is only poor productive density, improve workload selection/admission rather than lowering the survival cap. If the problem is only wake timeliness after a clean close, diagnose the scheduler/gap layer rather than misclassifying it as a duration boundary.

This distinction is important: `runtime boundary`, `completion envelope`, `policy-induced overshoot`, `productivity`, and `wake timeliness` are different mechanisms.

## Pre-armed gap rollback
Gap policy is separate from runtime-cap rollback.
- If a smaller planned gap causes overlap/concurrent invocation, missed close, stale-authority behavior, or materially worse wake reliability, immediately return to the last validated larger gap.
- Do not lower the runtime cap solely because a too-small planned gap caused the failure unless the failure also demonstrates a runtime-boundary problem.
- Re-promoting a smaller gap requires repeated clean wake/close evidence at the fixed runtime policy.
